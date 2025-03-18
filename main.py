import streamlit as st
from streamlit_extras.switch_page_button import switch_page  # For automatic page navigation

st.set_page_config(
    page_title="H-APP-Y Landing Page",
    page_icon="🍟",
    layout="centered"
)

# ---- Custom Styling ----
st.markdown(
    """
    <style>
    /* Import Google Font: Poppins */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

    /* Overall App Styling */
    .stApp {
        background: radial-gradient(
            circle at center,
            #ad5389 10%,
            #6c5ce7 40%,
            #4834d4 70%,
            #30336b 100%
        );
        font-family: 'Poppins', sans-serif;
        color: #FFFFFF;
    }

    /* Title and Subheader Styling */
    h1 {
        text-align: center;
        color: #FFFFFF;
        font-size: 3.5rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        margin-bottom: 0.3rem;
    }
    
    /* Slogan Styling */
    .slogan {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #ffd700;
        margin-top: -10px;
        text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.3);
    }

    h2, h3, h4, h5, h6, p {
        text-align: center;
        color: #f0f0f0;
        margin: 0.5rem 0;
    }

    /* Button Styling */
    .stButton > button {
        background-color: #ff69b4;
        color: #FFFFFF;
        font-weight: 600;
        border-radius: 30px;
        padding: 1rem 2rem;
        margin: 1rem;
        font-size: 1.1rem;
        box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease-in-out;
        border: none;
    }
    .stButton > button:hover {
        background-color: #ff1493;
        transform: translateY(-3px) scale(1.05);
        cursor: pointer;
        box-shadow: 0px 12px 20px rgba(0, 0, 0, 0.2);
    }

    /* Feedback Button Styling */
    .feedback-btn {
        display: flex;
        justify-content: center;
        margin-top: 20px;
    }
    .feedback-btn a {
        background-color: #ffcc00;
        color: #000;
        font-size: 1.2rem;
        font-weight: bold;
        text-decoration: none;
        padding: 12px 24px;
        border-radius: 30px;
        box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease-in-out;
    }
    .feedback-btn a:hover {
        background-color: #ffaa00;
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0px 12px 20px rgba(0, 0, 0, 0.2);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---- Title & Slogan ----
st.title("WELCOME TO H-APP-Y 😊")
st.markdown("<p class='slogan'>✨ H-APP-Y, we got you! 💖✨</p>", unsafe_allow_html=True)

# ---- Subtitle ----
st.subheader("McDonald's Edition 🍔🍟")
st.write("<p style='font-size:1.25rem;'>How do you want to analyze your food today?</p>", unsafe_allow_html=True)

# ---- Three Buttons (Mind, Body, Soul) ----
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    if st.button("💡 MIND WISE"):
        switch_page("Mind")
with col2:
    if st.button("💪 BODY WISE"):
        switch_page("Body")
with col3:
    if st.button("🌟 SOUL WISE"):
        switch_page("Soul")

# ---- New Row for Centered Disorders Wise Option ----
st.markdown("<br>", unsafe_allow_html=True)
col_left, col_center, col_right = st.columns(3)
with col_center:
    if st.button("🩺 DISORDERS WISE"):
        switch_page("Disorders")

# ---- Feedback Form Button ----
st.markdown(
    """
    <div class="feedback-btn">
        <a href="https://forms.gle/7p36QtJ1qdiha31m6" target="_blank">💬 Give Feedback</a>
    </div>
    """,
    unsafe_allow_html=True
)
