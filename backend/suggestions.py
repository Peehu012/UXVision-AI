def generate_suggestions(extracted_text):

    suggestions = []

    if len(extracted_text) < 50:
        suggestions.append("Add more descriptive content.")

    if extracted_text.count("\n") > 20:
        suggestions.append("Reduce text clutter.")

    if "login" not in extracted_text.lower():
        suggestions.append("Login section not clearly visible.")

    if "signup" not in extracted_text.lower():
        suggestions.append("Signup option may be missing.")

    if "search" not in extracted_text.lower():
        suggestions.append("Search functionality could improve navigation.")

    return suggestions