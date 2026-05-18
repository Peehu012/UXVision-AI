def calculate_score(extracted_text):

    contrast_score = 85
    typography_score = 80
    accessibility_score = 90
    alignment_score = 75

    overall_score = (
        contrast_score +
        typography_score +
        accessibility_score +
        alignment_score
    ) // 4

    if len(extracted_text) > 300:
        overall_score -= 10

    if "search" in extracted_text.lower():
        overall_score += 5

    if "submit" in extracted_text.lower():
        overall_score += 5

    return {
        "contrast": contrast_score,
        "typography": typography_score,
        "accessibility": accessibility_score,
        "alignment": alignment_score,
        "overall": overall_score
    }