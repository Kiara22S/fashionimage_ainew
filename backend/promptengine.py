def buildprompt(condition, gender, bodytype, pattern_name='none', color_name=None, view_direction="front"):
    import random
  
    # SIMPLE MODEL DESCRIPTIONS
    match gender.lower() if gender else "":
        case 'male':          
            model_desc = "a professional male model"
        case 'kid boy':
            model_desc = "a young boy, age 8"
        case 'kid girl':
            model_desc = "a young girl, age 8"
        case _:
            model_desc = "a professional female model"

    # SIMPLE FRAMING
    match bodytype:
        case 'Full-Body':
            framing_desc = "full body, head to toe"
        case "Upper-Body":
            framing_desc = "upper body from shoulders down"
        case _:
            framing_desc = "lower body focus"
    
    # COLOR INSTRUCTIONS - VERY STRICT
    match color_name:
        case str() if color_name.startswith("#"):
            color_instr = (f"Apply color {color_name} to the garment. "
                          "PRESERVE this exact color. Do not shift. Do not change shade.")
        case str() if len(color_name) > 0:
            color_instr = (f"Render the garment in {color_name}. Keep this color exact. No variations.")
        case _:
            color_instr = ("PRESERVE THE EXACT COLOR FROM SOURCE_IMAGE. Do not change. Do not shift shade. "
                          "Keep pattern/texture identical. Same color in every view.")
    
    # SIMPLE VIEW INSTRUCTIONS
    match view_direction.lower():
        case "front":
            view_instr = "Model faces camera, showing front of garment."
        case "back":
            view_instr = "Model faces away, showing back of garment."
        case "left side":
            view_instr = "Model in left profile, showing side of garment."
        case "closeup":
            view_instr = "Close-up shot of upper garment, showing details and texture."
        case _:
            view_instr = ""

    # SIMPLE BASE PROMPT
    base = (
        f"Professional product photography. Simple image of {model_desc} wearing the garment in {framing_desc} view. "
        f"{view_instr} "
        f"Clean studio background. Professional lighting. "
        f"{color_instr} "
        "CRITICAL: The garment color and pattern MUST match SOURCE_IMAGE exactly. "
        "Do not create variations. Keep everything identical to the source."
    )
    
    return base
               