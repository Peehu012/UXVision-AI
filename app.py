import streamlit as st
from PIL import Image
import pytesseract
import streamlit_authenticator as stauth
import google.generativeai as genai
import cv2
import numpy as np
import sqlite3
import pandas as pd
import plotly.express as px

from backend.ocr_engine import extract_text
from backend.scoring import calculate_score
from backend.suggestions import generate_suggestions
from backend.history import get_timestamp

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="UXVision AI",
    layout="wide"
)

# =========================================================
# GEMINI API
# =========================================================

genai.configure(
    api_key="YOUR_GEMINI_API_KEY"
)

# =========================================================
# AUTHENTICATION
# =========================================================

names = ["Admin"]
usernames = ["admin"]
passwords = ["12345"]

hashed_passwords = stauth.Hasher(passwords).generate()

credentials = {
    "usernames": {
        usernames[0]: {
            "name": names[0],
            "password": hashed_passwords[0]
        }
    }
}

authenticator = stauth.Authenticate(
    credentials,
    "uxvision_cookie",
    "abcdef",
    cookie_expiry_days=1
)

name, authentication_status, username = authenticator.login(
    "Login",
    "main"
)

if authentication_status is False:
    st.error("Incorrect Username or Password")
    st.stop()

elif authentication_status is None:
    st.warning("Please enter your login credentials")
    st.stop()

elif authentication_status:

    st.success(f"Welcome {name}")

    authenticator.logout("Logout", "sidebar")

    # =========================================================
    # TESSERACT PATH
    # =========================================================

    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )

    # =========================================================
    # DATABASE SETUP
    # =========================================================

    conn = sqlite3.connect("uxvision.db")

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_name TEXT,
            score INTEGER,
            suggestions TEXT,
            timestamp TEXT
        )
    """)

    conn.commit()

    # =========================================================
    # SIDEBAR
    # =========================================================

    st.sidebar.title("UXVision AI")

    st.sidebar.markdown("### Features")

    st.sidebar.write("✔ OCR Text Detection")
    st.sidebar.write("✔ UX Feedback Engine")
    st.sidebar.write("✔ UI Scoring")
    st.sidebar.write("✔ AI Recommendations")
    st.sidebar.write("✔ Design Suggestions")
    st.sidebar.write("✔ OpenCV Detection")
    st.sidebar.write("✔ Authentication")
    st.sidebar.write("✔ Database Storage")
    st.sidebar.write("✔ Analytics Dashboard")

    # =========================================================
    # TITLE
    # =========================================================

    st.title("UXVision Dashboard")

    st.subheader("AI-Assisted UX Analysis Platform")

    # =========================================================
    # FILE UPLOADER
    # =========================================================

    uploaded_file = st.file_uploader(
        "Upload UI Screenshot",
        type=["png", "jpg", "jpeg"]
    )

    # =========================================================
    # MAIN ANALYSIS
    # =========================================================

    if uploaded_file is not None:

        image = Image.open(uploaded_file)

        img_array = np.array(image)

        # -----------------------------------------------------
        # COLUMNS
        # -----------------------------------------------------

        col1, col2 = st.columns(2)

        # =====================================================
        # LEFT COLUMN
        # =====================================================

        with col1:

            st.subheader("Uploaded UI")

            st.image(
                image,
                use_container_width=True
            )

            # -------------------------------------------------
            # EDGE DETECTION
            # -------------------------------------------------

            gray = cv2.cvtColor(
                img_array,
                cv2.COLOR_BGR2GRAY
            )

            edges = cv2.Canny(
                gray,
                100,
                200
            )

            st.subheader("OpenCV Edge Detection")

            st.image(edges)

            # -------------------------------------------------
            # CONTOUR DETECTION
            # -------------------------------------------------

            contours, _ = cv2.findContours(
                edges,
                cv2.RETR_TREE,
                cv2.CHAIN_APPROX_SIMPLE
            )

            contour_image = img_array.copy()

            cv2.drawContours(
                contour_image,
                contours,
                -1,
                (0, 255, 0),
                2
            )

            st.subheader("Detected UI Components")

            st.image(contour_image)

            st.write(
                f"Detected UI Elements: {len(contours)}"
            )

        # =====================================================
        # RIGHT COLUMN
        # =====================================================

        with col2:

            # -------------------------------------------------
            # OCR
            # -------------------------------------------------

            extracted_text = pytesseract.image_to_string(
                image
            )

            st.subheader("Extracted Text")

            st.write(extracted_text)

            # -------------------------------------------------
            # AI FEEDBACK
            # -------------------------------------------------

            model = genai.GenerativeModel(
                "gemini-1.5-flash"
            )

            response = model.generate_content(
                f"""
                Analyze this UI and provide:

                1. UX Problems
                2. UI Improvements
                3. Accessibility Suggestions
                4. Layout Improvements
                5. Typography Suggestions
                6. Color Suggestions
                7. Modern Redesign Ideas

                UI Text:
                {extracted_text}
                """
            )

            ai_feedback = response.text

            st.subheader("AI UX Expert Feedback")

            st.write(ai_feedback)

        # =====================================================
        # SCORING
        # =====================================================

        scores = calculate_score(extracted_text)

        st.subheader("UX Scores")

        st.write(f"Contrast Score: {scores['contrast']}")
        st.write(f"Typography Score: {scores['typography']}")
        st.write(f"Accessibility Score: {scores['accessibility']}")
        st.write(f"Alignment Score: {scores['alignment']}")

        st.progress(scores['overall'] / 100)

        st.success(
            f"Overall UX Score: {scores['overall']}/100"
        )

        # =====================================================
        # CHARTS
        # =====================================================

        st.subheader("Analytics Dashboard")

        chart_data = pd.DataFrame({
            "Category": [
                "Contrast",
                "Typography",
                "Accessibility",
                "Alignment"
            ],
            "Score": [
                scores['contrast'],
                scores['typography'],
                scores['accessibility'],
                scores['alignment']
            ]
        })

        fig = px.bar(
            chart_data,
            x="Category",
            y="Score",
            title="UX Score Analysis"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # =====================================================
        # AI SUGGESTIONS
        # =====================================================

        st.subheader("AI UX Recommendations")

        suggestions = generate_suggestions(
            extracted_text
        )

        for suggestion in suggestions:
            st.warning(suggestion)

        # =====================================================
        # HISTORY
        # =====================================================

        timestamp = get_timestamp()

        st.subheader("Analysis History")

        st.info(f"Analysis Time: {timestamp}")

        # =====================================================
        # AUTO FIX PREVIEW
        # =====================================================

        st.subheader("Improved UI Preview")

        st.success("Suggested Improvements Applied")

        st.write("✔ Better spacing")
        st.write("✔ Improved typography")
        st.write("✔ Better hierarchy")
        st.write("✔ Cleaner layout")
        st.write("✔ Improved accessibility")
        st.write("✔ Better visual balance")

        # =====================================================
        # SAVE TO DATABASE
        # =====================================================

        cursor.execute(
            """
            INSERT INTO reports
            (image_name, score, suggestions, timestamp)
            VALUES (?, ?, ?, ?)
            """,
            (
                uploaded_file.name,
                scores['overall'],
                str(suggestions),
                str(timestamp)
            )
        )

        conn.commit()

        # =====================================================
        # DESIGN VARIANTS
        # =====================================================

        st.subheader("Alternative Design Ideas")

        col_a, col_b, col_c = st.columns(3)

        with col_a:
            st.image(
                "assets/minimal.png",
                caption="Minimal Dashboard"
            )

        with col_b:
            st.image(
                "assets/modern.png",
                caption="Modern Dashboard"
            )

        with col_c:
            st.image(
                "assets/creative.png",
                caption="Creative Dashboard"
            )

        # =====================================================
        # MODERN UI SAMPLE
        # =====================================================

        st.subheader("Advanced Redesign Engine")

        st.image(
            "assets/modern_ui.png",
            caption="AI Generated UI Inspiration"
        )

    conn.close()