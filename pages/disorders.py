import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# ------------------------------
# Page Config & Aesthetics
# ------------------------------
st.set_page_config(page_title="Disorders", page_icon="🩺", layout="centered")

st.title("Disorder-Wise Meal Recommendations 🩺")
st.subheader("Select your health condition to view top dish recommendations:")

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
    df = pd.read_csv("India_Menu.csv")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# ------------------------------
# Diabetes Score Calculation (Original Formula)
# ------------------------------
def compute_diabetes_score(df):
    """
    Compute a diabetes-specific score:
      - Lower total sugars and total carbohydrates are better.
      - Higher protein is beneficial (thus subtracting its normalized value).
    Score formula:
         0.5 * norm_sugars + 0.5 * norm_carbs - 0.3 * norm_protein
    """
    df = df.copy()
    scaler_sugars = MinMaxScaler()
    scaler_carbs = MinMaxScaler()
    scaler_protein = MinMaxScaler()
    
    df["norm_sugars"] = scaler_sugars.fit_transform(df[["Total Sugars (g)"]])
    df["norm_carbs"] = scaler_carbs.fit_transform(df[["Total carbohydrate (g)"]])
    df["norm_protein"] = scaler_protein.fit_transform(df[["Protein (g)"]])
    
    df["Diabetes_Score"] = 0.5 * df["norm_sugars"] + 0.5 * df["norm_carbs"] - 0.3 * df["norm_protein"]
    return df

# ------------------------------
# PCOS/PCOD Score Calculation
# ------------------------------
def compute_pcos_score(df):
    """
    Compute a PCOS-specific score:
      - High protein and fiber are beneficial.
      - Low sugars and processed carbs.
    Score formula:
      0.4 * norm_protein + 0.3 * norm_fiber - 0.3 * norm_sugars - 0.2 * norm_carbs
    """
    df = df.copy()
    scaler_protein = MinMaxScaler()
    scaler_fiber = MinMaxScaler()
    scaler_sugars = MinMaxScaler()
    scaler_carbs = MinMaxScaler()
    
    df["norm_protein"] = scaler_protein.fit_transform(df[["Protein (g)"]])
    df["norm_fiber"] = scaler_fiber.fit_transform(df[["Dietary Fiber (g)"]])
    df["norm_sugars"] = scaler_sugars.fit_transform(df[["Total Sugars (g)"]])
    df["norm_carbs"] = scaler_carbs.fit_transform(df[["Total carbohydrate (g)"]])
    
    df["PCOS_Score"] = 0.4 * df["norm_protein"] + 0.3 * df["norm_fiber"] - 0.3 * df["norm_sugars"] - 0.2 * df["norm_carbs"]
    return df

# ------------------------------
# Filtering Functions for Other Conditions
# ------------------------------
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
    return ranked.head(10)[["Menu Items", "Menu Category", "Protein (g)", "Dietary Fiber (g)", "Total Sugars (g)", "Total carbohydrate (g)", "PCOS_Score"]]

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
if condition == "Diabetes":
    st.write("### Top 10 Dishes for Diabetes")
    recommendations = recommend_for_diabetes(df)
elif condition == "PCOS/PCOD":
    st.write("### Top 10 Dishes for PCOS/PCOD")
    recommendations = recommend_for_pcos(df)
elif condition == "Lactose Intolerance":
    st.write("### Top 10 Dishes for Lactose Intolerance")
    recommendations = recommend_for_lactose_intolerance(df)
elif condition == "Gluten Intolerance":
    st.write("### Top 10 Dishes for Gluten Intolerance")
    recommendations = recommend_for_gluten_intolerance(df)
elif condition == "Nut Allergy":
    st.write("### Top 10 Dishes for Nut Allergy")
    recommendations = recommend_for_allergy(df, allergen="nuts")

st.dataframe(recommendations, use_container_width=True)
