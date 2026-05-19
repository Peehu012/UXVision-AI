import streamlit as st
from PIL import Image
import pytesseract
import streamlit_authenticator as stauth
import google.generativeai as genai
import cv2
import numpy as np
import sqlite3
import plotly.express as px
import pandas as pd

from backend.ocr_engine import extract_text
from backend.scoring import calculate_score
from backend.suggestions import generate_suggestions
from backend.history import get_timestamp

# -------------------------------
# PAGE CONFIG
# -------------------------------

st.set_page_config(
    page_title="UXVision AI",
    layout="wide"
)

# -------------------------------
# GEMINI API
# -------------------------------

genai.configure(
    api_key="YOUR_GEMINI_API_KEY"
)

# -------------------------------
# AUTHENTICATION
# -------------------------------

names = ["Admin"]
usernames = ["admin"]
passwords = ["12345"]

hashed_passwords = stauth.Hasher.hash_passwords(passwords)

credentials = {
    "usernames": {
        "admin": {
            "name": "Admin",
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

authenticator.login()

# -------------------------------
# LOGIN STATUS
# -------------------------------

if st.session_state["authentication_status"] is False:
    st.error("Incorrect username or password")
    st.stop()

elif st.session_state["authentication_status"] is None:
    st.warning("Please login")
    st.stop()

elif st.session_state["authentication_status"]:

    st.success(
        f"Welcome {st.session_state['name']}"
    )

    # -------------------------------
    # TESSERACT
    # -------------------------------

    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )

    # -------------------------------
    # SIDEBAR
    # -------------------------------

    st.sidebar.title("UXVision AI")

    page = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "Analysis",
            "History",
            "AI Redesigns"
        ]
    )

    st.sidebar.markdown("### Features")

    st.sidebar.write("✔ OCR Text Detection")
    st.sidebar.write("✔ UX Feedback Engine")
    st.sidebar.write("✔ UI Scoring")
    st.sidebar.write("✔ AI Recommendations")
    st.sidebar.write("✔ Design Suggestions")
    st.sidebar.write("✔ OpenCV Detection")
    st.sidebar.write("✔ AI Redesign Engine")

    # -------------------------------
    # DASHBOARD PAGE
    # -------------------------------

    if page == "Dashboard":

        st.title("UXVision Dashboard")

        st.subheader(
            "AI-Assisted UX Analysis Platform"
        )

        st.image(
            "assets/modern_ui.png",
            use_container_width=True
        )

        st.info(
            "Upload UI screenshots and receive AI-powered UX analysis."
        )

    # -------------------------------
    # ANALYSIS PAGE
    # -------------------------------

    elif page == "Analysis":

        st.title("UI Analysis")

        uploaded_file = st.file_uploader(
            "Upload UI Design",
            type=["png", "jpg", "jpeg"]
        )

        if uploaded_file is not None:

            image = Image.open(uploaded_file)

            img_array = np.array(image)

            # -------------------------------
            # LAYOUT
            # -------------------------------

            col1, col2 = st.columns(2)

            # -------------------------------
            # ORIGINAL IMAGE
            # -------------------------------

            with col1:

                st.subheader("Uploaded UI")

                st.image(
                    image,
                    use_container_width=True
                )

                # -------------------------------
                # OPENCV EDGE DETECTION
                # -------------------------------

                gray = cv2.cvtColor(
                    img_array,
                    cv2.COLOR_BGR2GRAY
                )

                edges = cv2.Canny(
                    gray,
                    100,
                    200
                )

                st.subheader(
                    "OpenCV Edge Detection"
                )

                st.image(edges)

                # -------------------------------
                # CONTOUR DETECTION
                # -------------------------------

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

                st.subheader(
                    "Detected UI Components"
                )

                st.image(
                    contour_image,
                    use_container_width=True
                )

                st.write(
                    f"Total Components Detected: {len(contours)}"
                )

            # -------------------------------
            # OCR + AI
            # -------------------------------

            extracted_text = pytesseract.image_to_string(image)

            with col2:

                st.subheader("Extracted Text")

                st.write(extracted_text)

                # -------------------------------
                # GEMINI AI
                # -------------------------------

                model = genai.GenerativeModel(
                    "gemini-1.5-flash"
                )

                response = model.generate_content(
                    f"""
                    Analyze this UI and provide:

                    1. UX issues
                    2. Accessibility problems
                    3. Layout improvements
                    4. Typography suggestions
                    5. Enterprise redesign advice

                    UI Text:
                    {extracted_text}
                    """
                )

                ai_feedback = response.text

                st.subheader(
                    "AI UX Expert Feedback"
                )

                st.write(ai_feedback)

            # -------------------------------
            # SCORING ENGINE
            # -------------------------------

            scores = calculate_score(extracted_text)

            st.subheader("UX Scores")

            st.write(
                f"Contrast Score: {scores['contrast']}"
            )

            st.write(
                f"Typography Score: {scores['typography']}"
            )

            st.write(
                f"Accessibility Score: {scores['accessibility']}"
            )

            st.write(
                f"Alignment Score: {scores['alignment']}"
            )

            st.progress(scores['overall'] / 100)

            st.success(
                f"Overall UX Score: {scores['overall']}/100"
            )

            # -------------------------------
            # CHARTS
            # -------------------------------

            chart_data = pd.DataFrame({
                "Metric": [
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
                x="Metric",
                y="Score",
                title="UX Score Analysis"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            # -------------------------------
            # SUGGESTIONS
            # -------------------------------

            st.subheader(
                "AI UX Recommendations"
            )

            suggestions = generate_suggestions(
                extracted_text
            )

            for suggestion in suggestions:
                st.warning(suggestion)

            # -------------------------------
            # AUTO FIX UI
            # -------------------------------

            st.subheader("Auto Fixed UI")

            fix_col1, fix_col2 = st.columns(2)

            with fix_col1:
                st.image(
                    image,
                    caption="Original UI",
                    use_container_width=True
                )

            with fix_col2:
                st.image(
                    "assets/modern_ui.png",
                    caption="Improved UI",
                    use_container_width=True
                )

            # -------------------------------
            # DESIGN VARIANTS
            # -------------------------------

            st.subheader(
                "Alternative Design Ideas"
            )

            design_col1, design_col2, design_col3 = st.columns(3)

            with design_col1:
                st.image(
                    "assets/minimal.png",
                    caption="Minimal Layout",
                    use_container_width=True
                )

            with design_col2:
                st.image(
                    "assets/modern.png",
                    caption="Modern Variant",
                    use_container_width=True
                )

            with design_col3:
                st.image(
                    "assets/creative.png",
                    caption="Creative Version",
                    use_container_width=True
                )

            # -------------------------------
            # DATABASE
            # -------------------------------

            conn = sqlite3.connect(
                "uxvision.db"
            )

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

            timestamp = get_timestamp()

            cursor.execute(
                """
                INSERT INTO reports (
                    image_name,
                    score,
                    suggestions,
                    timestamp
                )
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

            conn.close()

            # -------------------------------
            # HISTORY INFO
            # -------------------------------

            st.subheader("Analysis History")

            st.info(
                f"Analysis Time: {timestamp}"
            )

    # -------------------------------
    # HISTORY PAGE
    # -------------------------------

    elif page == "History":

        st.title("Analysis History")

        conn = sqlite3.connect(
            "uxvision.db"
        )

        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM reports"
        )

        data = cursor.fetchall()

        conn.close()

        if data:

            for row in data:

                st.write(
                    f"""
                    Image: {row[1]}
                    | Score: {row[2]}
                    | Time: {row[4]}
                    """
                )

                st.write(row[3])

                st.divider()

        else:

            st.warning(
                "No analysis history found."
            )

    # -------------------------------
    # AI REDESIGN PAGE
    # -------------------------------

    elif page == "AI Redesigns":

        st.title("Advanced AI Redesign Engine")

        st.image(
            "assets/modern_ui.png",
            caption="Enterprise Dashboard",
            use_container_width=True
        )

        st.image(
            "assets/minimal.png",
            caption="Minimal Redesign",
            use_container_width=True
        )

        st.image(
            "assets/creative.png",
            caption="Creative Redesign",
            use_container_width=True
        )