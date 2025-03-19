import streamlit as st
import pandas as pd
import string

# ------------------------------
# Page Configuration & Aesthetics
# ------------------------------
st.set_page_config(page_title="Texture Vibes", page_icon="✨", layout="centered")

# Custom Styling: Same aura aesthetic as soul.py
st.markdown("""
    <style>
        /* Aura Gradient Background */
        .stApp {
            background: radial-gradient(circle, rgba(173,83,137,1) 10%, rgba(108,92,231,1) 40%, rgba(72,52,212,1) 70%, rgba(48,51,107,1) 100%);
            color: white;
        }
        /* White Text with Bold and Centered Alignment */
        h1, h2, h3, h4, h5, h6, p, label {
            color: white !important;
            font-weight: bold;
            text-align: center;
        }
        /* Centering and Styling for Selectbox */
        .stSelectbox {
            margin: auto;
            display: block;
            width: 50%;
        }
        /* Styling for Buttons (if needed) */
        .stButton > button {
            background-color: #ff69b4; /* Hot pink */
            color: white;
            font-weight: bold;
            border-radius: 20px;
            padding: 10px 25px;
            box-shadow: 0px 4px 15px rgba(255, 255, 255, 0.3);
            transition: all 0.3s ease-in-out;
            border: none;
        }
        .stButton > button:hover {
            background-color: #ff1493; /* Deeper pink */
            transform: scale(1.05);
            cursor: pointer;
        }
        /* Highlight Box Styling for Results */
        .highlight-box {
            background-color: rgba(255, 255, 255, 0.2);
            padding: 10px;
            border-radius: 10px;
            font-weight: bold;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# ------------------------------
# Load Dataset
# ------------------------------
file_path = "India_Menu.csv"  # Adjust if necessary
try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    st.error("⚠️ Error: Menu file not found. Please check the file path.")
    st.stop()

# ------------------------------
# Step 1: Define Texture Lexicon & Mapping
# ------------------------------
texture_dict = {
    "Crispy 🍟": ["crispy", "crunchy", "brittle", "fried", "nuggets"],
    "Chewy 🍬": ["chewy", "tough", "rubbery", "gum"],
    "Soft 🥞": ["soft", "fluffy", "tender", "muffin", "burger"],
    "Smooth ☕": ["smooth", "velvety", "creamy", "flat white"]
}

texture_feelings = {
    "Crispy 🍟": "⚡ Energizing",
    "Chewy 🍬": "💪 Satisfying",
    "Soft 🥞": "🛌 Comforting",
    "Smooth ☕": "🌊 Soothing",
    "Unknown ❓": "😐 Neutral"
}

# ------------------------------
# Step 2: Texture Classification
# ------------------------------
def classify_texture(item_name):
    """
    Classifies the texture of a food item based on predefined keywords.
    """
    scores = {texture: 0 for texture in texture_dict.keys()}
    lower_name = item_name.lower()
    # Keyword matching from lexicon
    for texture, keywords in texture_dict.items():
        for kw in keywords:
            if kw in lower_name:
                scores[texture] += 1
    max_score = max(scores.values())
    if max_score == 0:
        return "Unknown ❓"
    return max(scores, key=scores.get)

# Apply classification to dataset
df['Texture'] = df['Menu Items'].apply(classify_texture)
df['Feeling'] = df['Texture'].apply(lambda x: texture_feelings.get(x, "😐 Neutral"))

# ------------------------------
# Step 3: User Interaction
# ------------------------------
st.markdown("<h1>🔮 Discover Your Food's Texture Energy 🔮</h1>", unsafe_allow_html=True)
st.markdown("<p>Select a texture to see foods that match your vibe ✨</p>", unsafe_allow_html=True)

texture_choice = st.selectbox("Choose a Texture", list(texture_dict.keys()), index=0)

filtered_df = df[df['Texture'] == texture_choice]

# ------------------------------
# Step 4: Display Results
# ------------------------------
if filtered_df.empty:
    st.warning(f"⚠️ No items found with texture '{texture_choice}'. Try another!")
else:
    st.markdown(f"<div class='highlight-box'>✨ {texture_choice} foods give a feeling of {texture_feelings[texture_choice]} ✨</div>", unsafe_allow_html=True)
    st.dataframe(filtered_df[['Menu Items', 'Texture', 'Feeling']].head(10), use_container_width=True)
