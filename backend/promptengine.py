def buildprompt(condition, gender, bodytype, pattern_name='none', color_name=None):
    """
    Build an AI image generation prompt for virtual fashion try-on.
    
    Args:
        condition: Type of rendering ('simple try on', 'virtual try on', or pattern-based)
        gender: Model type ('male', 'kid boy', 'kid girl', or 'female')
        bodytype: Shot framing ('Full-Body', 'Upper-Body', or 'Lower-Body')
        pattern_name: Textile pattern to apply (default: 'none')
        color_name: Color override (hex code starting with '#' or color name)
    
    Returns:
        str: Complete prompt for AI image generation
    """
    # Model description based on gender
    match gender.lower() if gender else "":
        case 'male':
            model_desc = ("Professional male fashion model, natural hairstyle, realistic skin texture, "
                         "editorial studio photography, neutral expression, high-end commercial lighting")
        case 'kid boy':
            model_desc = ("Youthful kid boy model, age 8, professional fashion catalog style, "
                         "cheerful neutral expression, small stature")
        case 'kid girl':
            model_desc = ("Youthful kid girl model, age 8, professional fashion catalog style, "
                         "cheerful neutral expression, small stature")
        case _:
            model_desc = ("Professional female mannequin-style editorial model, realistic hair texture, "
                         "neutral expression")

    # Framing description based on body type
    match bodytype:
        case 'Full-Body':
            framing_desc = "Head-to-toe full length shot, high-end commercial studio setting"
        case "Upper-Body":
            framing_desc = ("Vertical portrait shot including the head, torso, and waist. "
                           "The camera is positioned back far enough to show the entire length "
                           "of the garment including the bottom hemline and the top of the model's trousers. "
                           "Leave clear empty space at the very bottom of the frame")
        case _:
            framing_desc = "Lower garment focused framing, highlighting fabric drape"
    
    # Geometry preservation instruction (used across all conditions)
    geometry_instruction = (" CRITICAL GEOMETRY PRESERVATION: Maintain the EXACT garment structure from the reference image. "
                           "Do NOT alter the neckline style, collar shape, sleeve length, or hemline. "
                           "If the reference has a round neck, keep it round. If V-neck, keep it V-neck. "
                           "Preserve 100% structural fidelity to the original design")
    
    # Color instruction based on input type
    match color_name:
        # Case 1: User provided a Hex Code (e.g., #828e5c)
        case str() if color_name.startswith("#"):
            color_instr = (f" [PIXEL-PERFECT RECOLOR] Change the garment fabric hue to {color_name}."
                          f"{geometry_instruction}.")
        
        # Case 2: User provided a Name (e.g., Olive Green)
        case str() if len(color_name.strip()) > 0:
            color_instr = (f" [COLOR OVERRIDE] Render the fabric in a professional {color_name.strip()} shade."
                          f"{geometry_instruction}.")
        
        # Case 3: color_name is None or empty (THE FALLBACK)
        case _:
            color_instr = f" Maintain the original colors and textures of the uploaded garment reference.{geometry_instruction}."
    
    # Base prompt structure
    base = (
        f"Commercial e-commerce product photography of a {model_desc}. "
        f"Technical framing: {framing_desc}. High-key studio lighting, clean gray background. "
        "Strictly professional retail catalog style. No skin-revealing content."
    )
    
    # Build final prompt based on condition
    match condition.lower():
        case "simple try on" | "virtual try on":
            # Virtual try-on: Apply garment to model with optional color change
            return (f"{base}{color_instr} "
                   "The model must wear the EXACT garment from the reference image. "
                   "Only modify the color and model placement, do not redesign the clothing structure.")
        
        case _:
            # Pattern/Texture application mode
            pattern_desc = f" a high-fidelity {pattern_name} textile print" if pattern_name and pattern_name.lower() != 'none' else " the specified pattern"
            return (f"{base}{color_instr} "
                   f"[PATTERN OVERRIDE] Apply{pattern_desc} to every visible surface of the garment fabric. "
                   "Ensure the pattern wraps naturally and realistically around all fabric folds, "
                   "seams, and shadows without distorting the clothing's structural design.")
               