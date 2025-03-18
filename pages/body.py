import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.cluster import KMeans

# ---- Page Configuration ----
st.set_page_config(page_title="Meal Recommender", page_icon="🍽️", layout="wide")

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

    /* Title Styling */
    h1 {
        text-align: center;
        color: #FFFFFF;
        font-size: 3.5rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        margin-bottom: 0.3rem;
    }

    /* Subtitle Styling */
    h2, h3, h4, h5, h6, p {
        text-align: center;
        color: #f0f0f0;
        margin: 0.5rem 0;
    }

    /* Radio Button Styling */
    .stRadio > label {
        font-size: 1.2rem;
        font-weight: bold;
        color: #FFD700;
    }

    /* Dataframe Styling */
    .stDataFrame {
        background-color: rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        padding: 10px;
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

# ---- Title ----
st.title("🍽️ Smart Meal Recommendation System")
st.write("### Find the best meal based on how you want to feel after eating! 😋")

# ---- Load Dataset ----
@st.cache_data
def load_data():
    df = pd.read_csv("India_Menu_New.csv")

    df["Sodium (mg)"].fillna(df["Sodium (mg)"].mean(), inplace=True)
    df["Veg/Non-Veg"] = df["Veg/Non-Veg"].str.strip().str.title()

    selected_features = ["Energy (kCal)", "Protein (g)", "Total fat (g)",
                         "Sat Fat (g)", "Total carbohydrate (g)",
                         "Total Sugars (g)", "Added Sugars (g)", "Sodium (mg)"]
    
    df_selected = df[selected_features]

    scaler = MinMaxScaler()
    df_scaled = pd.DataFrame(scaler.fit_transform(df_selected), columns=df_selected.columns)

    df_scaled["Menu Items"] = df["Menu Items"].values
    df_scaled["Menu Category"] = df["Menu Category"].values
    df_scaled["Veg/Non-Veg"] = df["Veg/Non-Veg"].values

    df_scaled["Energetic_Score"] = df_scaled["Total carbohydrate (g)"] * 0.5 + df_scaled["Protein (g)"] * 0.5
    df_scaled["Lean_Score"] = df_scaled["Protein (g)"] * 0.6 - df_scaled["Total fat (g)"] * 0.4
    df_scaled["Satiated_Score"] = df_scaled["Protein (g)"] * 0.5 + df_scaled["Total fat (g)"] * 0.5
    df_scaled["Avoid_Bloating_Score"] = -df_scaled["Sodium (mg)"] * 0.5 - df_scaled["Total carbohydrate (g)"] * 0.3 - df_scaled["Added Sugars (g)"] * 0.2

    X = df_scaled[["Energetic_Score", "Lean_Score", "Satiated_Score", "Avoid_Bloating_Score"]]
    scaler_std = StandardScaler()
    X_scaled = scaler_std.fit_transform(X)

    kmeans = KMeans(n_clusters=4, random_state=42)
    df_scaled["Cluster"] = kmeans.fit_predict(X_scaled)

    return df_scaled

df = load_data()

# ---- Feeling Selection UI ----
st.write("#### Select how you want to feel after your meal:")
feeling = st.radio(
    "Choose your desired feeling:",
    ["⚡ Energetic", "🏋️ Lean", "🍛 Satiated", "💨 Avoid Bloating"],
    horizontal=True
)

# ---- Meal Type Selection UI ----
st.write("#### Select your meal type:")
meal_type = st.radio(
    "Choose your meal preference:",
    ["Veg", "Non-Veg"],
    horizontal=True
)

# ---- Recommendation Logic ----
def recommend_meals(df, feeling, meal_type):
    feeling_map = {
        "⚡ Energetic": "Energetic_Score",
        "🏋️ Lean": "Lean_Score",
        "🍛 Satiated": "Satiated_Score",
        "💨 Avoid Bloating": "Avoid_Bloating_Score"
    }

    df_filtered = df[df["Veg/Non-Veg"] == meal_type]
    top_meals = df_filtered.sort_values(by=feeling_map[feeling], ascending=False).head(5)
    
    return top_meals[["Menu Items", "Menu Category", "Veg/Non-Veg"]]

# ---- Display Recommendations ----
if feeling and meal_type:
    st.write(f"### Recommended {meal_type} Meals for {feeling}")
    recommendations = recommend_meals(df, feeling, meal_type)

    if recommendations is not None and not recommendations.empty:
        st.dataframe(recommendations, use_container_width=True)
    else:
        st.error("No recommendations found! Please check your selection and try again.")
