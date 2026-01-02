def buildprompt(condition, gender, bodytype, pattern_name='none', color_name=None):
  
    match gender.lower() if gender else "":
        case 'male':          
            model_desc=("High-end fashion photography of a professional male model, natural hairstyle, "
                        "highly detailed realistic skin texture, visible skin pores, editorial studio, "
                        "natural relaxed pose, high-end commercial lighting"
                        "[DYNAMIC OUTFIT]: If the uploaded garment is a top,"
                        "pair it with matching slim-fit trousers. If it is a full outfit, do not add extra layers.")
        case 'kid boy':
            model_desc=("Youthful kid boy model, age 8, professional fashion catalog style, "
                        "natural human features, cheerful expression, small stature")
        case 'kid girl':
            model_desc=("Youthful kid girl model, age 8, professional fashion catalog style, "
                        "natural human features, cheerful expression, small stature")
        case _:
            
            model_desc=("Full-featured professional female fashion model, realistic human skin, "
                        "natural flowing hairstyle with individual hair strands visible, "
                        "elegant neutral expression, lifelike human features"
                         "[DYNAMIC OUTFIT RULE]: Analyze the garment type in SOURCE_IMAGE. "
                          "1. IF the garment is a TOP (shirt, kurti, blouse): The model MUST wear matching "
                          "professional straight-fit trousers to ensure a modest look. "
                          "2. IF the garment is a BOTTOM or FULL OUTFIT (shorts, pants, skirt, maxi dress): "
                          "Do NOT add extra trousers. Render the garment exactly as it is without layering. "
                          "Ensure the output reflects a logical, single-layer retail outfit.")


    match bodytype:
        case 'Full-Body':
            framing_desc = "head-to-toe full length shot, high-end commercial studio setting"
            length_guard = (
                " [STRUCTURAL LOCK]: Maintain the exact spatial relationship between the "
                "garment hemline and the model's limbs. If there is a gap between the "
                "hem and the knees in the source, that exact gap must exist in the output. "
                "Do not fill empty space with extra fabric. Preserve the original skin-to-fabric ratio."
            )
        case "Upper-Body":
            framing_desc = "vertical portrait shot including the head, torso, and waist. "
            "The camera is positioned back far enough to show the entire length "
            "of the garment including the bottom hemline and the top of the model's trousers. "
            "Leave clear empty space at the very bottom of the frame."
            length_guard=" [STRUCTURAL LOCK]: Preserve the original crop and hemline position relative to the waist."
        case _:
            framing_desc ="lower garment focused framing, highlighting fabric drape"
            length_guard=" [FEATURE LOCK]: Sharp focus on pocket geometry and hemline drape. Do not blur edges."
            
    match color_name:
        # Case 1: User provided a Hex Code (e.g., #828e5c)
        case str() if color_name.startswith("#"):
            color_instr = (f" [COMMAND: PIXEL-PERFECT RECOLOR] Change the garment fabric hue to {color_name}. "
                             "CRITICAL: Maintain the exact neckline geometry of the source image. "
                             "If the reference is a round neck, the output MUST be a round neck. "
                             "Do not add collars, V-cuts, or buttons. Keep the original silhouette 100% intact.")
        
        # Case 2: User provided a Name (e.g., Olive Green)
        
        case str() if len(color_name) > 0:
            color_instr = (f" [COMMAND: COLOR OVERRIDE] Render the fabric in a professional {color_name} shade. "
                              "Ensure the garment structure, specifically the round neckline, remains identical to the upload.")
        
        # Case 3: color_name is None or empty (THE FALLBACK)
        case _:
            color_instr =(" [STRICT DATA LOCK]: MANDATORY. Do not modify, simplify, or re-render the "
                        "original fabric colors or textures. You must perform a bit-by-bit transfer "
                "of the source garment's factory wash, distress marks, and color gradients. "
                "CRITICAL: The output garment must be a 100% pixel-accurate match to the "
                "SOURCE_IMAGE in terms of hue, saturation, and textile finish.")
    base = (
        f"Commercial e-commerce product photography of a {model_desc} on a real human model. "
        "The output must never be a mannequin or a flat-lay garment on a table. "
        f"Technical framing: {framing_desc}. High-key studio lighting, clean gray background. "
        "Strictly professional retail catalog style. No skin-revealing content."
    )
    

    match condition.lower():
        case "simple try on" | "virtual try on":
            return base + color_instr + (
            " [COMMAND: UNIFIED ANCHOR & CLEAN]: You must merge the SOURCE_IMAGE with the model's anatomy. "
                "1. NO FLOATING: The garment must be 100% attached to the model's body, following their pose and gravity. "
                "2. PATTERN LOCK: Transfer the EXACT textile print, graphics, and embroidery with bit-by-bit accuracy. "
                "3. CLUTTER REMOVAL: Do not render price tags, paper labels, or extra fabric bundles from the source. "
                "4. EMPTY HANDS: The model's hands must be empty; remove any cloth held in their arms. "
                "5. CLEAN BORDERS: Ensure the garment ends naturally against the skin or background with no artifacts."
            )
       


        case _:
            # Case for Pattern/Texture application
            return base + color_instr +   (f" MANDATORY PATTERN OVERRIDE: Apply a high-fidelity {pattern_name} textile print "
                "to every visible surface of the garment fabric. "
                "GEOMETRIC INTEGRITY: You must maintain the exact original neckline shape and silhouette. "
                "If the reference is a round neck, it MUST remain a round neck. "
                "Ensure the pattern wraps naturally and realistically around all fabric folds, "
                "seams, and shadows without distorting the clothing's structural design")
               