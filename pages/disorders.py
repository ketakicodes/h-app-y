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
# Helper Functions for Filtering
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

# ------------------------------
# Improved Ranking for Diabetes Using a Weighted Score
# ------------------------------
def compute_diabetes_score(df):
    """
    Compute a diabetes-specific score:
      - Lower total sugars and total carbohydrates are better.
      - Higher protein is beneficial (thus subtracting its normalized value).
    The score is computed as:
         0.5 * norm_sugars + 0.5 * norm_carbs - 0.3 * norm_protein
    """
    df = df.copy()
    # Scale each nutrient individually
    scaler_sugars = MinMaxScaler()
    scaler_carbs = MinMaxScaler()
    scaler_protein = MinMaxScaler()
    
    df["norm_sugars"] = scaler_sugars.fit_transform(df[["Total Sugars (g)"]])
    df["norm_carbs"] = scaler_carbs.fit_transform(df[["Total carbohydrate (g)"]])
    df["norm_protein"] = scaler_protein.fit_transform(df[["Protein (g)"]])
    
    # Compute weighted score: lower score is better
    df["Diabetes_Score"] = 0.5 * df["norm_sugars"] + 0.5 * df["norm_carbs"] - 0.3 * df["norm_protein"]
    return df

# ------------------------------
# Recommendation Functions for Each Condition
# ------------------------------
def recommend_for_diabetes(df):
    # First, filter out dishes with extremely high sugars or carbs
    filtered = filter_diabetes(df, sugar_threshold=5, carb_threshold=20)
    # Compute a more nuanced score for diabetes
    scored_df = compute_diabetes_score(filtered)
    # Rank dishes by the computed Diabetes_Score (ascending order is better)
    ranked = scored_df.sort_values("Diabetes_Score", ascending=True)
    return ranked.head(10)[["Menu Items", "Menu Category", "Total Sugars (g)", "Total carbohydrate (g)", "Protein (g)", "Diabetes_Score"]]

def recommend_for_lactose_intolerance(df):
    filtered = filter_lactose(df)
    # For lactose intolerance, you might prioritize lower energy (and thus possibly lighter meals)
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
