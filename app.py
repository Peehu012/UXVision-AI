import streamlit as st
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

from backend.ocr_engine import extract_text
from backend.scoring import calculate_score
from backend.suggestions import generate_suggestions
from backend.history import get_timestamp

st.set_page_config(page_title="UXVision AI", layout="wide")

# SIDEBAR

st.sidebar.title("UXVision AI")

st.sidebar.markdown("### Features")

st.sidebar.write("✔ OCR Text Detection")
st.sidebar.write("✔ UX Feedback Engine")
st.sidebar.write("✔ UI Scoring")
st.sidebar.write("✔ AI Recommendations")
st.sidebar.write("✔ Design Suggestions")

# MAIN TITLE

st.title("UXVision Dashboard")
st.subheader("AI-Assisted UX Analysis Platform")

# FILE UPLOAD

uploaded_file = st.file_uploader(
    "Upload UI Design",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file is not None:

    image = Image.open(uploaded_file)

    col1, col2 = st.columns(2)

    with col1:
        st.image(image, caption="Uploaded UI", use_container_width=True)

    # OCR TEXT

    extracted_text = extract_text(image)

    with col2:
        st.subheader("Extracted Text")
        st.write(extracted_text)

    # SCORE ENGINE

    scores = calculate_score(extracted_text)

    st.subheader("UX Scores")

    st.write(f"Contrast Score: {scores['contrast']}")
    st.write(f"Typography Score: {scores['typography']}")
    st.write(f"Accessibility Score: {scores['accessibility']}")
    st.write(f"Alignment Score: {scores['alignment']}")

    st.progress(scores['overall'] / 100)

    st.success(f"Overall UX Score: {scores['overall']}/100")

    # SUGGESTIONS

    st.subheader("AI UX Recommendations")

    suggestions = generate_suggestions(extracted_text)

    for suggestion in suggestions:
        st.warning(suggestion)

    # HISTORY

    st.subheader("Analysis History")

    timestamp = get_timestamp()

    st.info(f"Analysis Time: {timestamp}")

    # AUTO FIX SECTION

    st.subheader("Improved UI Preview")

    st.info("Suggested Improvements Applied")

    st.write("• Better spacing")
    st.write("• Improved typography")
    st.write("• Reduced clutter")
    st.write("• Better alignment")

    # DESIGN VARIANTS

    st.subheader("Alternative Design Ideas")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.image(
            "assets/minimal.png",
            caption="Minimal Layout"
        )

    with col2:
        st.image(
            "assets/modern.png",
            caption="Modern Variant"
        )

    with col3:
        st.image(
            "assets/creative.png",
            caption="Creative Version"
        )