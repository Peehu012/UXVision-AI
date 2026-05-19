import streamlit as st
from PIL import Image
import pytesseract
import streamlit_authenticator as stauth
import google.generativeai as genai
import cv2
import numpy as np

genai.configure(api_key="AIzaSyCs37tlAhDrIyNiZ-6AP3rFfQSzBuEYDSU")

names = ["Admin"]
usernames = ["admin"]

passwords = ["12345"]

hashed_passwords = stauth.Hasher.hash_passwords(passwords)

authenticator = stauth.Authenticate(
    names,
    usernames,
    hashed_passwords,
    "uxvision",
    "abcdef",
    cookie_expiry_days=1
)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
    st.success(f"Welcome {name}")

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

        img_array = np.array(image)

        gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)

        edges = cv2.Canny(gray, 100, 200)

        st.subheader("OpenCV Edge Detection")

        st.image(edges)

        contour_image = img_array.copy()

        cv2.drawContours(
            contour_image,
            contours,
            -1,
            (0, 255, 0),
            2
        )

        st.image(contour_image, caption="Detected UI Elements")
        

    # OCR TEXT

    extracted_text = pytesseract.image_to_string(image)

    model = genai.GenerativeModel("gemini-1.5-flash")

    response = model.generate_content(
        f"Analyze this UI text and provide UX improvements:\n{extracted_text}"
    )

    ai_feedback = response.text

    st.subheader("AI UX Expert Feedback")

    st.write(ai_feedback)

    st.subheader("Alternative Design Ideas")

    st.image("assets/modern_ui.png")

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

    conn = sqlite3.connect("uxvision.db")

    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO reports (image_name, score, suggestions, timestamp) VALUES (?, ?, ?, ?)",
        (
            uploaded_file.name,
            score,
            str(suggestions),
            str(timestamp)
        )
    )

    conn.commit()
    conn.close()

    timestamp = get_timestamp()

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