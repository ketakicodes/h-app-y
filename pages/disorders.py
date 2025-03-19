import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# ------------------------------
# Page Config & Aesthetics
# ------------------------------
st.set_page_config(page_title="Disorders", page_icon="🍽️", layout="centered")

# Custom Styling: Matching Texture Vibes Aesthetic
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
        /* Styling for Buttons */
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
# Page Title
# ------------------------------
st.markdown("<h1>🍽️ Smart Meal Recommender</h1>", unsafe_allow_html=True)
st.markdown("<p>✨ Select your health condition to get personalized meal recommendations ✨</p>", unsafe_allow_html=True)

# ------------------------------
# Health Condition Selector
# ------------------------------
condition = st.selectbox(
    "Choose a Health Condition:",
    ["Diabetes", "Lactose Intolerance", "Gluten Intolerance", "Nut Allergy", "PCOS/PCOD"]
)

# ------------------------------
# Data Loading & Caching
# ------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("India_Menu.csv")  # Ensure correct path
    df.columns = df.columns.str.strip()  # Remove accidental spaces
    return df

df = load_data()

# ------------------------------
# Scoring Functions
# ------------------------------
def compute_diabetes_score(df):
    df = df.copy()
    scaler_sugars = MinMaxScaler()
    scaler_carbs = MinMaxScaler()
    scaler_protein = MinMaxScaler()
    
    df["norm_sugars"] = scaler_sugars.fit_transform(df[["Total Sugars (g)"]])
    df["norm_carbs"] = scaler_carbs.fit_transform(df[["Total carbohydrate (g)"]])
    df["norm_protein"] = scaler_protein.fit_transform(df[["Protein (g)"]])
    
    df["Diabetes_Score"] = 0.6 * df["norm_sugars"] + 0.4 * df["norm_carbs"] - 0.3 * df["norm_protein"]
    return df

def compute_pcos_score(df):
    df = df.copy()
    scaler_protein = MinMaxScaler()
    scaler_sugars = MinMaxScaler()
    scaler_carbs = MinMaxScaler()
    
    df["norm_protein"] = scaler_protein.fit_transform(df[["Protein (g)"]])
    df["norm_sugars"] = scaler_sugars.fit_transform(df[["Total Sugars (g)"]])
    df["norm_carbs"] = scaler_carbs.fit_transform(df[["Total carbohydrate (g)"]])
    
    df["PCOS_Score"] = 0.5 * df["norm_protein"] - 0.3 * df["norm_sugars"] - 0.2 * df["norm_carbs"]
    return df

# ------------------------------
# Filtering Functions
# ------------------------------
def filter_lactose(df):
    dairy_keywords = ["milk", "cheese", "cream", "butter", "yogurt", "paneer"]
    mask = df["Menu Items"].str.lower().apply(lambda x: not any(word in x for word in dairy_keywords))
    return df[mask]

def filter_gluten(df):
    gluten_keywords = ["wheat", "barley", "rye", "bread", "pasta", "roti"]
    mask = df["Menu Items"].str.lower().apply(lambda x: not any(word in x for word in gluten_keywords))
    return df[mask]

def filter_allergen(df, allergen_keywords):
    mask = df["Menu Items"].str.lower().apply(lambda x: not any(word in x for word in allergen_keywords))
    return df[mask]

# ------------------------------
# Recommendation Functions
# ------------------------------
def recommend_for_diabetes(df):
    filtered = df[(df["Total Sugars (g)"] <= 5) & (df["Total carbohydrate (g)"] <= 20)]
    scored_df = compute_diabetes_score(filtered)
    ranked = scored_df.sort_values("Diabetes_Score", ascending=True)
    return ranked.head(10)[["Menu Items", "Menu Category", "Total Sugars (g)", "Total carbohydrate (g)", "Protein (g)", "Diabetes_Score"]]

def recommend_for_pcos(df):
    avoid_keywords = ["milk", "cheese", "bread", "pasta", "sugar", "fried"]
    mask = df["Menu Items"].str.lower().apply(lambda x: not any(word in x for word in avoid_keywords))
    filtered = df[mask]
    scored_df = compute_pcos_score(filtered)
    ranked = scored_df.sort_values("PCOS_Score", ascending=False)
    return ranked.head(10)[["Menu Items", "Menu Category", "Protein (g)", "Total Sugars (g)", "Total carbohydrate (g)", "PCOS_Score"]]

def recommend_for_lactose_intolerance(df):
    filtered = filter_lactose(df)
    ranked = filtered.sort_values("Energy (kCal)", ascending=True)
    return ranked.head(10)[["Menu Items", "Menu Category", "Energy (kCal)"]]

def recommend_for_gluten_intolerance(df):
    filtered = filter_gluten(df)
    ranked = filtered.sort_values("Energy (kCal)", ascending=True)
    return ranked.head(10)[["Menu Items", "Menu Category", "Energy (kCal)"]]

def recommend_for_allergy(df, allergen="nuts"):
    allergen_map = {
        "nuts": ["almond", "cashew", "peanut", "walnut"],
        "soy": ["soy", "tofu"],
        "shellfish": ["shrimp", "crab", "lobster"],
    }
    keywords = allergen_map.get(allergen.lower(), [])
    filtered = filter_allergen(df, keywords)
    ranked = filtered.sort_values("Energy (kCal)", ascending=True)
    return ranked.head(10)[["Menu Items", "Menu Category", "Energy (kCal)"]]

# ------------------------------
# Display Recommendations
# ------------------------------
st.markdown(f"<div class='highlight-box'>✨ Best meal recommendations for {condition}! ✨</div>", unsafe_allow_html=True)

if condition == "Diabetes":
    recommendations = recommend_for_diabetes(df)
elif condition == "PCOS/PCOD":
    recommendations = recommend_for_pcos(df)
elif condition == "Lactose Intolerance":
    recommendations = recommend_for_lactose_intolerance(df)
elif condition == "Gluten Intolerance":
    recommendations = recommend_for_gluten_intolerance(df)
elif condition == "Nut Allergy":
    recommendations = recommend_for_allergy(df, allergen="nuts")

st.dataframe(recommendations, use_container_width=True)
