import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# ------------------------------
# Page Config & Aesthetics
# ------------------------------
st.set_page_config(page_title="Disorders Wise Meal Recommendations", page_icon="🩺", layout="centered")

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
            margin-bottom: 0.5rem;
        }
        h2, h3, h4, h5, h6, p, label {
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
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------------------
# Title & Introduction
# ------------------------------
st.title("Disorders Wise Meal Recommendations 🩺")
st.subheader("Select your health condition to view top dish recommendations:")

# ------------------------------
# Health Condition Selector
# ------------------------------
condition = st.selectbox(
    "Choose a Health Condition:",
    ["Diabetes", "Lactose Intolerance", "Gluten Intolerance", "Nut Allergy"]
)

# ------------------------------
# Data Loading & Caching
# ------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("India_Menu.csv")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# ------------------------------
# Helper Functions for Filtering & Ranking
# ------------------------------
def filter_diabetes(df, sugar_threshold=5, carb_threshold=20):
    """Filter dishes suitable for diabetes by limiting sugars and carbs."""
    return df[(df["Total Sugars (g)"] <= sugar_threshold) & 
              (df["Total carbohydrate (g)"] <= carb_threshold)]

def filter_lactose(df):
    """Exclude dishes containing dairy-related keywords."""
    dairy_keywords = ["milk", "cheese", "cream", "butter", "yogurt"]
    mask = df["Menu Items"].str.lower().apply(lambda x: not any(word in x for word in dairy_keywords))
    return df[mask]

def filter_gluten(df):
    """Exclude dishes containing gluten-related keywords."""
    gluten_keywords = ["wheat", "barley", "rye", "bread", "pasta"]
    mask = df["Menu Items"].str.lower().apply(lambda x: not any(word in x for word in gluten_keywords))
    return df[mask]

def filter_allergen(df, allergen_keywords):
    """Exclude dishes containing specified allergen keywords."""
    mask = df["Menu Items"].str.lower().apply(lambda x: not any(word in x for word in allergen_keywords))
    return df[mask]

def rank_dishes(df, nutrient_columns):
    """Rank dishes by normalizing selected nutrient columns and summing them (lower score is better)."""
    scaler = MinMaxScaler()
    norm_values = scaler.fit_transform(df[nutrient_columns])
    df['Nutrient_Score'] = norm_values.sum(axis=1)
    return df.sort_values('Nutrient_Score')

# ------------------------------
# Recommendation Functions for Each Condition
# ------------------------------
def recommend_for_diabetes(df):
    filtered = filter_diabetes(df, sugar_threshold=5, carb_threshold=20)
    ranked = rank_dishes(filtered, ["Total Sugars (g)", "Total carbohydrate (g)"])
    return ranked.head(10)[["Menu Items", "Menu Category", "Total Sugars (g)", "Total carbohydrate (g)"]]

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
# Display Recommendations Based on User Selection
# ------------------------------
if condition == "Diabetes":
    st.write("### Top 10 Dishes for Diabetes")
    recommendations = recommend_for_diabetes(df)
    st.dataframe(recommendations, use_container_width=True)
elif condition == "Lactose Intolerance":
    st.write("### Top 10 Dishes for Lactose Intolerance")
    recommendations = recommend_for_lactose_intolerance(df)
    st.dataframe(recommendations, use_container_width=True)
elif condition == "Gluten Intolerance":
    st.write("### Top 10 Dishes for Gluten Intolerance")
    recommendations = recommend_for_gluten_intolerance(df)
    st.dataframe(recommendations, use_container_width=True)
elif condition == "Nut Allergy":
    st.write("### Top 10 Dishes for Nut Allergy")
    recommendations = recommend_for_allergy(df, allergen="nuts")
    st.dataframe(recommendations, use_container_width=True)
