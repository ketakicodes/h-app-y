import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.cluster import KMeans

# ------------------------------
# Page Config & Aesthetics
# ------------------------------
st.set_page_config(page_title="Meal Recommender", page_icon="🍽", layout="centered")

st.markdown("""
<style>
    /* Aura Gradient Background */
    .stApp {
        background: radial-gradient(circle, rgba(173,83,137,1) 10%, rgba(108,92,231,1) 40%, rgba(72,52,212,1) 70%, rgba(48,51,107,1) 100%);
        color: white;
        font-family: "sans-serif";
    }
    /* Centered and Bold White Text */
    h1, h2, h3, h4, h5, h6, p, label {
        text-align: center;
        color: white !important;
        font-weight: bold;
    }
    /* Buttons: hot pink, fixed width, extra spacing, hover effect */
    .stButton > button {
        background-color: #ff69b4; /* Hot pink */
        color: white;
        font-weight: bold;
        border-radius: 20px;
        padding: 10px 25px;
        margin: 5px;             /* Spacing around each button */
        width: 160px;            /* Fixed width for uniform size */
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
""", unsafe_allow_html=True)

# ------------------------------
# Data Loading and Preprocessing
# ------------------------------
def load_data():
    # Adjust path if necessary
    df = pd.read_csv("India_Menu.csv")

    # Fill missing Sodium with mean
    df["Sodium (mg)"].fillna(df["Sodium (mg)"].mean(), inplace=True)

    selected_features = [
        "Energy (kCal)",
        "Protein (g)",
        "Total fat (g)",
        "Sat Fat (g)",
        "Total carbohydrate (g)",
        "Total Sugars (g)",
        "Added Sugars (g)",
        "Sodium (mg)"
    ]

    df_selected = df[selected_features]

    # Scale data using MinMaxScaler
    scaler = MinMaxScaler()
    df_scaled = pd.DataFrame(
        scaler.fit_transform(df_selected),
        columns=df_selected.columns
    )
    df_scaled["Menu Items"] = df["Menu Items"].values
    df_scaled["Menu Category"] = df["Menu Category"].values

    # Create feeling-based scores
    df_scaled["Energetic_Score"] = (
        df_scaled["Total carbohydrate (g)"] * 0.5
        + df_scaled["Protein (g)"] * 0.5
    )
    df_scaled["Lean_Score"] = (
        df_scaled["Protein (g)"] * 0.6
        - df_scaled["Total fat (g)"] * 0.4
    )
    df_scaled["Satiated_Score"] = (
        df_scaled["Protein (g)"] * 0.5
        + df_scaled["Total fat (g)"] * 0.5
    )
    df_scaled["Avoid_Bloating_Score"] = (
        -df_scaled["Sodium (mg)"] * 0.5
        - df_scaled["Total carbohydrate (g)"] * 0.3
        - df_scaled["Added Sugars (g)"] * 0.2
    )

    # Clustering
    X = df_scaled[[
        "Energetic_Score",
        "Lean_Score",
        "Satiated_Score",
        "Avoid_Bloating_Score"
    ]]
    scaler_std = StandardScaler()
    X_scaled = scaler_std.fit_transform(X)

    kmeans = KMeans(n_clusters=4, random_state=42)
    df_scaled["Cluster"] = kmeans.fit_predict(X_scaled)

    return df_scaled

# ------------------------------
# Meal Recommendation Function
# ------------------------------
def recommend_meals(df, feeling):
    feeling_map = {
        "⚡ Energetic": "Energetic_Score",
        "🏋 Lean": "Lean_Score",
        "🍛 Satiated": "Satiated_Score",
        "💨 Avoid Bloating": "Avoid_Bloating_Score"
    }

    if feeling not in feeling_map:
        return None

    # Sort descending by the chosen feeling's score
    top_meals = df.sort_values(
        by=feeling_map[feeling],
        ascending=False
    ).head(5)

    return top_meals[["Menu Items", "Menu Category"]]

# ------------------------------
# Streamlit UI
# ------------------------------
st.title("🍽 Smart Meal Recommender")
st.write("### Select How You Want to Feel After Your Meal:")

df = load_data()

# Create 4 columns with extra gap
col1, col2, col3, col4 = st.columns(4, gap="large")

selected_feeling = None

with col1:
    if st.button("⚡ Energetic"):
        selected_feeling = "⚡ Energetic"

with col2:
    if st.button("🏋 Lean"):
        selected_feeling = "🏋 Lean"

with col3:
    if st.button("🍛 Satiated"):
        selected_feeling = "🍛 Satiated"

with col4:
    if st.button("💨 Avoid Bloating"):
        selected_feeling = "💨 Avoid Bloating"

# Display Recommendations
if selected_feeling:
    st.write(f"### Recommended Meals for {selected_feeling}")
    recommendations = recommend_meals(df, selected_feeling)
    if recommendations is not None:
        st.dataframe(recommendations, use_container_width=True)
    else:
        st.error("Something went wrong! Please try again.")
