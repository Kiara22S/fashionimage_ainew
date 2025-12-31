from google import genai
from google.genai import types
import os
import traceback
from dotenv import load_dotenv
import concurrent.futures
from .promptengine import buildprompt
from .imagelogic import prepareimage
from io import BytesIO
from PIL import Image

load_dotenv()

# Initialize the 2025 Client
client = genai.Client(api_key=os.getenv("GEMINIAPI_KEY"))

def run_singlegeneration(shirtfile, gender, bodytype, patternfile=None, color_name=None):
    try:
        processed_shirt = prepareimage(shirtfile)
        negative_constraints = (
            " NEGATIVE_CONSTRAINTS: Do not change the neckline. Do not add collars. "
            "Do not add buttons. Do not change the garment silhouette. Do not remove hair. "
            "The model MUST have a natural hairstyle. No bald heads."
        )
        
        if patternfile:
            processed_pattern = prepareimage(patternfile)
            prompt_text = buildprompt('texture overlay', gender, bodytype,color_name=color_name)
            content_list = [
                "OBJECTIVE: Apply the texture from the PATTERN_IMAGE to the garment in the SOURCE_IMAGE.",
                "SOURCE_IMAGE:", processed_shirt, 
                "PATTERN_IMAGE:", processed_pattern,
                prompt_text
            ]
        else:
            prompt_text = buildprompt('virtual try on', gender, bodytype,color_name=color_name)
            content_list = [
                "OBJECTIVE: Change the color of the garment in the SOURCE_IMAGE while keeping the shape identical.",
                "SOURCE_IMAGE:", processed_shirt,
                prompt_text
            ]
        # Use the 2.5 Flash Image model
        response = client.models.generate_content(
            model='gemini-3-pro-image-preview',
            contents=content_list,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
           
                safety_settings=[
                    types.SafetySetting(
                        category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                        threshold="BLOCK_NONE"
                    )
                ]
            )
        )

        # 🚀 CORRECT EXTRACTION FOR 2025 SDK
        # We loop through candidates -> content -> parts
        for part in response.candidates[0].content.parts:
            if part.inline_data:
                # Return the raw bytes or convert to PIL image
                return Image.open(BytesIO(part.inline_data.data))
        
        raise Exception("No image data found in model response.")

    except Exception as e:
        print(f"--- Backend Error ---")
        traceback.print_exc()
        raise e

def runbatch_pipeline(uploaded_files, gender, bodytype, pattern_file=None,color_name=None):
    all_results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        future_to_file = {
            executor.submit(run_singlegeneration, f, gender, bodytype, pattern_file,color_name): f 
            for f in uploaded_files
        }
        for future in concurrent.futures.as_completed(future_to_file):
            file_name = future_to_file[future].name
            try:
                img_obj = future.result()
                all_results.append({"file_name": file_name, "output": img_obj})
            except Exception as e:
                all_results.append({"file_name": file_name, "output": f"Error: {str(e)}"})
    return all_results