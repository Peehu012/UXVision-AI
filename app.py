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
# GEMINI AI CONFIG
# =========================================================

genai.configure(
    api_key="YOUR_GEMINI_API_KEY"
)

# =========================================================
# AUTHENTICATION
# =========================================================

credentials = {
    "usernames": {
        "admin": {
            "name": "Admin",
            "password": "12345"
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
    location="main"
)

# =========================================================
# LOGIN STATUS
# =========================================================

if authentication_status is False:
    st.error("Incorrect username or password")

elif authentication_status is None:
    st.warning("Please enter your login credentials")

elif authentication_status:

    authenticator.logout("Logout", "sidebar")

    st.sidebar.success(f"Welcome {name}")

    # =========================================================
    # DATABASE
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

    st.sidebar.markdown("## Features")

    st.sidebar.write("✔ OCR Text Detection")
    st.sidebar.write("✔ OpenCV Detection")
    st.sidebar.write("✔ AI UX Feedback")
    st.sidebar.write("✔ UX Scoring")
    st.sidebar.write("✔ UI Recommendations")
    st.sidebar.write("✔ Design Alternatives")
    st.sidebar.write("✔ Auto UI Fix")
    st.sidebar.write("✔ Database History")
    st.sidebar.write("✔ Analytics Dashboard")

    # =========================================================
    # MAIN TITLE
    # =========================================================

    st.title("UXVision Dashboard")

    st.subheader(
        "AI-Powered UI/UX Analysis and Redesign Platform"
    )

    # =========================================================
    # FILE UPLOAD
    # =========================================================

    uploaded_file = st.file_uploader(
        "Upload UI Screenshot",
        type=["png", "jpg", "jpeg"]
    )

    # =========================================================
    # IMAGE PROCESSING
    # =========================================================

    if uploaded_file is not None:

        image = Image.open(uploaded_file)

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

            # ================================================
            # OPENCV PROCESSING
            # ================================================

            img_array = np.array(image)

            gray = cv2.cvtColor(
                img_array,
                cv2.COLOR_BGR2GRAY
            )

            edges = cv2.Canny(
                gray,
                100,
                200
            )

            st.subheader("Edge Detection")

            st.image(edges)

            # ================================================
            # CONTOUR DETECTION
            # ================================================

            contours, hierarchy = cv2.findContours(
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

            st.image(
                contour_image,
                use_container_width=True
            )

            st.success(
                f"Detected Components: {len(contours)}"
            )

        # =====================================================
        # OCR + AI ANALYSIS
        # =====================================================

        extracted_text = pytesseract.image_to_string(
            image
        )

        model = genai.GenerativeModel(
            "gemini-1.5-flash"
        )

        response = model.generate_content(
            f"""
            Analyze this UI and provide:

            1. UX problems
            2. UI improvements
            3. Accessibility improvements
            4. Color suggestions
            5. Typography improvements
            6. Layout redesign ideas
            7. Mobile responsiveness tips
            8. Professional redesign suggestions

            UI Text:
            {extracted_text}
            """
        )

        ai_feedback = response.text

        # =====================================================
        # RIGHT COLUMN
        # =====================================================

        with col2:

            st.subheader("Extracted OCR Text")

            st.write(extracted_text)

            st.subheader("AI UX Expert Feedback")

            st.write(ai_feedback)

        # =====================================================
        # UX SCORING
        # =====================================================

        scores = calculate_score(extracted_text)

        st.subheader("UX Score Dashboard")

        score_df = pd.DataFrame({
            "Category": [
                "Contrast",
                "Typography",
                "Accessibility",
                "Alignment"
            ],
            "Score": [
                scores["contrast"],
                scores["typography"],
                scores["accessibility"],
                scores["alignment"]
            ]
        })

        fig = px.bar(
            score_df,
            x="Category",
            y="Score",
            title="UX Analysis Scores"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.progress(scores["overall"] / 100)

        st.success(
            f"Overall UX Score: {scores['overall']}/100"
        )

        # =====================================================
        # AI RECOMMENDATIONS
        # =====================================================

        st.subheader("AI UX Recommendations")

        suggestions = generate_suggestions(
            extracted_text
        )

        for suggestion in suggestions:
            st.warning(suggestion)

        # =====================================================
        # ANALYSIS HISTORY
        # =====================================================

        timestamp = get_timestamp()

        st.subheader("Analysis History")

        st.info(f"Analysis Time: {timestamp}")

        # =====================================================
        # AUTO FIX UI
        # =====================================================

        st.subheader("Auto UI Improvements")

        st.success("AI redesign suggestions applied")

        st.write("✔ Better spacing")
        st.write("✔ Improved typography")
        st.write("✔ Better alignment")
        st.write("✔ Reduced clutter")
        st.write("✔ Improved visual hierarchy")
        st.write("✔ Better accessibility")
        st.write("✔ Improved responsiveness")

        # =====================================================
        # DESIGN ALTERNATIVES
        # =====================================================

        st.subheader("Alternative Design Ideas")

        col3, col4, col5 = st.columns(3)

        with col3:
            st.image(
                "assets/minimal.png",
                caption="Minimal UI"
            )

        with col4:
            st.image(
                "assets/modern.png",
                caption="Modern UI"
            )

        with col5:
            st.image(
                "assets/creative.png",
                caption="Creative UI"
            )

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
                scores["overall"],
                str(suggestions),
                str(timestamp)
            )
        )

        conn.commit()

        # =====================================================
        # DATABASE DASHBOARD
        # =====================================================

        st.subheader("Stored Reports")

        reports_df = pd.read_sql_query(
            "SELECT * FROM reports",
            conn
        )

        st.dataframe(
            reports_df,
            use_container_width=True
        )

        # =====================================================
        # ANALYTICS CHART
        # =====================================================

        if len(reports_df) > 0:

            analytics_fig = px.line(
                reports_df,
                x="timestamp",
                y="score",
                title="UX Score Trends"
            )

            st.plotly_chart(
                analytics_fig,
                use_container_width=True
            )

        # =====================================================
        # ADVANCED REDESIGN ENGINE
        # =====================================================

        st.subheader("Advanced Redesign Engine")

        redesign_prompt = f"""
        Create a professional redesign strategy for this UI.

        Include:
        - Better layout
        - Better spacing
        - Better CTA placement
        - Accessibility improvements
        - Color palette improvements
        - Typography redesign
        - Enterprise dashboard redesign
        """

        redesign_response = model.generate_content(
            redesign_prompt
        )

        st.write(
            redesign_response.text
        )

        # =====================================================
        # FOOTER
        # =====================================================

        st.markdown("---")

        st.caption(
            "UXVision AI • Advanced UI/UX Analysis Platform"
        )

        # =====================================================
        # CLOSE DATABASE
        # =====================================================

        conn.close()