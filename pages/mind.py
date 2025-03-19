import streamlit as st
from streamlit_extras.switch_page_button import switch_page  # For automatic navigation

st.set_page_config(
    page_title="Mind",
    page_icon="🧠",
    layout="centered"
)

# ---- Custom CSS for Aesthetic Aura Background, Centered Text, and Buttons ----
st.markdown(
    """
    <style>
        /* Radial Gradient Background */
        .stApp {
            background: radial-gradient(
                circle at center,
                #ad5389 10%,
                #6c5ce7 40%,
                #4834d4 70%,
                #30336b 100%
            );
            color: white;
            font-family: "sans-serif";
        }

        /* Center text for headings & paragraphs */
        h1, h2, h3, h4, h5, h6, p {
            text-align: center;
            color: #FFFFFF;
        }

        /* Style the buttons */
        .stButton > button {
            background-color: #ff69b4; /* Hot pink */
            color: #FFFFFF;
            font-weight: bold;
            border-radius: 20px;
            padding: 0.75rem 1.5rem;
            margin: 0.5rem 0;
            box-shadow: 0px 4px 15px rgba(255, 255, 255, 0.3);
            transition: all 0.3s ease-in-out;
            border: none;
        }
        .stButton > button:hover {
            background-color: #ff1493; /* Deeper pink */
            transform: scale(1.05);
            cursor: pointer;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ---- Title & Description with Emojis ----
st.title("🧠 Mind-Based Analysis 🧠")
st.write("Choose how you’d like to analyze your food from a mind perspective: 🤔")

# ---- Button Layout ----
col_left, col_center, col_right = st.columns([2, 1, 2], gap="large")

with col_left:
    mood_option = st.button("😄 Mood Wise")
with col_right:
    texture_option = st.button("🌊 Texture Wise")

# ---- Page Navigation ----
if mood_option:
    switch_page("Mood")
if texture_option:
    switch_page("Texture")
