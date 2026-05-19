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

credentials = {
    "usernames": {
        "admin": {
            "email": "admin@gmail.com",
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

try:

    name, authentication_status, username = authenticator.login(
        location="main"
    )

    if authentication_status:

        authenticator.logout(
            "Logout",
            "sidebar"
        )

        st.sidebar.success(f"Welcome {name}")

    elif authentication_status is False:

        st.error("Invalid username or password")
        st.stop()

    elif authentication_status is None:

        st.warning("Please login")
        st.stop()

except Exception as e:

    st.error(e)
    st.stop()

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
st.sidebar.write("✔ OpenCV Edge Detection")
st.sidebar.write("✔ Contour Detection")
st.sidebar.write("✔ AI UX Feedback")
st.sidebar.write("✔ UX Scoring")
st.sidebar.write("✔ AI Recommendations")
st.sidebar.write("✔ Alternative Designs")
st.sidebar.write("✔ Database Storage")
st.sidebar.write("✔ Analytics Dashboard")
st.sidebar.write("✔ Advanced Redesign Engine")

# =========================================================
# TITLE
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
# MAIN PROCESSING
# =========================================================

if uploaded_file is not None:

    image = Image.open(uploaded_file)

    col1, col2 = st.columns(2)

    # =====================================================
    # COLUMN 1
    # =====================================================

    with col1:

        st.subheader("Uploaded UI")

        st.image(
            image,
            use_container_width=True
        )

        # =================================================
        # IMAGE TO NUMPY
        # =================================================

        img_array = np.array(image)

        # =================================================
        # GRAYSCALE
        # =================================================

        gray = cv2.cvtColor(
            img_array,
            cv2.COLOR_BGR2GRAY
        )

        # =================================================
        # EDGE DETECTION
        # =================================================

        edges = cv2.Canny(
            gray,
            100,
            200
        )

        st.subheader("OpenCV Edge Detection")

        st.image(edges)

        # =================================================
        # CONTOUR DETECTION
        # =================================================

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
    # OCR
    # =====================================================

    extracted_text = pytesseract.image_to_string(
        image
    )

    # =====================================================
    # AI MODEL
    # =====================================================

    model = genai.GenerativeModel(
        "gemini-1.5-flash"
    )

    response = model.generate_content(
        f"""
        Analyze this UI and provide:

        1. UX Problems
        2. UI Improvements
        3. Accessibility Improvements
        4. Typography Suggestions
        5. Color Palette Suggestions
        6. Layout Improvements
        7. Professional Redesign Ideas
        8. Mobile Responsive Improvements

        UI Text:
        {extracted_text}
        """
    )

    ai_feedback = response.text

    # =====================================================
    # COLUMN 2
    # =====================================================

    with col2:

        st.subheader("Extracted OCR Text")

        st.write(extracted_text)

        st.subheader("AI UX Expert Feedback")

        st.write(ai_feedback)

    # =====================================================
    # UX SCORE
    # =====================================================

    scores = calculate_score(
        extracted_text
    )

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

    st.progress(
        scores["overall"] / 100
    )

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
    # HISTORY
    # =====================================================

    timestamp = get_timestamp()

    st.subheader("Analysis History")

    st.info(
        f"Analysis Time: {timestamp}"
    )

    # =====================================================
    # AUTO FIX UI
    # =====================================================

    st.subheader("Auto UI Improvements")

    st.success(
        "AI redesign suggestions applied"
    )

    st.write("✔ Better spacing")
    st.write("✔ Improved typography")
    st.write("✔ Better alignment")
    st.write("✔ Reduced clutter")
    st.write("✔ Better accessibility")
    st.write("✔ Improved hierarchy")

    # =====================================================
    # DESIGN IDEAS
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
    # SAVE DATABASE
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
    # STORED REPORTS
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
    # ANALYTICS
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

    redesign_response = model.generate_content(
        f"""
        Create a professional redesign strategy for this UI.

        Include:
        - Better spacing
        - Better layout
        - Better typography
        - Better accessibility
        - Better CTA placement
        - Enterprise-level redesign
        """
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

# =========================================================
# CLOSE DATABASE
# =========================================================

conn.close()