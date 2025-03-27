import streamlit as st

# ---- Page Config ----
st.set_page_config(
    page_title="H-APP-Y Landing Page",
    page_icon="🍟",
    layout="wide"
)

# ---- Custom Styling ----
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

    .stApp {
        background: radial-gradient(circle at center, #ad5389 10%, #6c5ce7 40%, #4834d4 70%, #30336b 100%);
        font-family: 'Poppins', sans-serif;
        color: #FFFFFF;
        text-align: center;
    }

    /* Center Align Everything */
    h1, h2, h3, h4, h5, h6, p {
        text-align: center;
    }

    /* Button Styling */
    .stButton > button {
        background-color: #ff69b4;
        color: #FFFFFF;
        font-weight: 600;
        border-radius: 30px;
        padding: 1rem 2rem;
        margin: 1rem auto; /* Centering */
        font-size: 1.1rem;
        box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease-in-out;
        display: block; /* Ensures centering */
    }

    .stButton > button:hover {
        background-color: #ff1493;
        transform: translateY(-3px) scale(1.05);
        cursor: pointer;
        box-shadow: 0px 12px 20px rgba(0, 0, 0, 0.2);
    }

    /* Center the Feedback Button */
    .feedback-container {
        text-align: center;
        margin-top: 20px;
    }

    .feedback-container a {
        background-color: #ffcc00;
        color: #000;
        font-size: 1.2rem;
        font-weight: bold;
        text-decoration: none;
        padding: 12px 24px;
        border-radius: 30px;
        box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease-in-out;
        display: inline-block;
    }

    .feedback-container a:hover {
        background-color: #ffb700;
        transform: translateY(-3px);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---- Landing Page UI ----
st.title("WELCOME TO H-APP-Y 😊")
st.markdown("<p style='font-size: 2.5rem; color:#ffd700;'>✨ H-APP-Y, we got you! 💖✨</p>", unsafe_allow_html=True)

st.subheader("McDonald's Edition 🍔🍟")
st.write("<p style='font-size:1.25rem;'>How do you want to analyze your food today?</p>", unsafe_allow_html=True)

# ---- Buttons (All Centered) ----
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("💡 MIND WISE"):
        st.switch_page("pages/mind.py")

with col2:
    if st.button("💪 BODY WISE"):
        st.switch_page("pages/body.py")

with col3:
    if st.button("🌟 SOUL WISE"):
        st.switch_page("pages/soul.py")

# ---- Centered Disorders Wise Option ----
st.markdown("<br>", unsafe_allow_html=True)
col_empty, col_disorders, col_empty2 = st.columns([1, 2, 1])  # Ensures centering

with col_disorders:
    if st.button("🩺 DISORDERS WISE"):
        st.switch_page("pages/disorders.py")

# ---- Feedback Form Button (Centered) ----
st.markdown(
    """
    <div class="feedback-container">
        <a href="https://forms.gle/7p36QtJ1qdiha31m6" target="_blank">💬 Give Feedback</a>
    </div>
    """,
    unsafe_allow_html=True
)
