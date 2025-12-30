def buildprompt(condition, gender, bodytype, pattern_name='none', color_name=None):
  
    match gender.lower() if gender else "":
        case 'male':          
            model_desc=("Professional male fashion model, natural hairstyle, realistic skin texture, editorial studio photography, neutral expression, high-end commercial lighting")
        case 'kid boy':
            model_desc=("youthful kid boy model, age 8, professional fashion catalog style, cheerful neutral expression, small stature")
        case 'kid girl':
            model_desc=("youthful kid girl model, age 8, professional fashion catalog style, cheerful neutral expression, small stature")
        case _:
            model_desc=("professional female mannequin-style editorial model, neutral expression")


    match bodytype:
        case 'Full-Body':
            framing_desc = "head-to-toe full length shot, high-end commercial studio setting"
        case "Upper-Body":
            framing_desc = "vertical portrait shot including the head, torso, and waist. "
            "The camera is positioned back far enough to show the entire length "
            "of the garment including the bottom hemline and the top of the model's trousers. "
            "Leave clear empty space at the very bottom of the frame."
        case _:
            framing_desc ="lower garment focused framing, highlighting fabric drape"
            
    match color_name:
        case str() if color_name.startswith("#"):
            color_instr = f" The garment must be rendered in the specific hex color code {color_name}."
        case str() if len(color_name) > 0:
            color_instr = f" The garment should be rendered in a professional {color_name} shade."
        case _:
            color_instr = ""

    base = (
        f"Commercial e-commerce product photography of a {model_desc}. "
        f"Technical framing: {framing_desc}. High-key studio lighting, clean gray background. "
        "Strictly professional retail catalog style. No skin-revealing content."
    )
    

    match condition.lower():
        case "simple try on" | "virtual try on":
            return base + color_instr + (
                " The model is wearing the uploaded garment strictly. "
                "Maintain exact fabric weave from the reference image."
            )
        case _:
            
            return base + color_instr + (
                f" Apply a professional {pattern_name} textile print to the surface of the clothing. "
                "Ensure the pattern wraps naturally around the fabric folds and shadows."
            )