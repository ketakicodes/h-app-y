import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.cluster import KMeans

# Load dataset
def load_data():
    df = pd.read_csv("C:/Users/vaish/OneDrive/Desktop/happy_codebase/h-app-y/data/India_Menu.csv")
    df["Sodium (mg)"].fillna(df["Sodium (mg)"].mean(), inplace=True)
    
    selected_features = ["Energy (kCal)", "Protein (g)", "Total fat (g)",
                         "Sat Fat (g)", "Total carbohydrate (g)",
                         "Total Sugars (g)", "Added Sugars (g)", "Sodium (mg)"]
    
    df_selected = df[selected_features]
    
    # Scale data
    scaler = MinMaxScaler()
    df_scaled = pd.DataFrame(scaler.fit_transform(df_selected), columns=df_selected.columns)
    df_scaled["Menu Items"] = df["Menu Items"].values
    df_scaled["Menu Category"] = df["Menu Category"].values
    
    # Create feeling-based scores
    df_scaled["Energetic_Score"] = df_scaled["Total carbohydrate (g)"] * 0.5 + df_scaled["Protein (g)"] * 0.5
    df_scaled["Lean_Score"] = df_scaled["Protein (g)"] * 0.6 - df_scaled["Total fat (g)"] * 0.4
    df_scaled["Satiated_Score"] = df_scaled["Protein (g)"] * 0.5 + df_scaled["Total fat (g)"] * 0.5
    df_scaled["Avoid_Bloating_Score"] = -df_scaled["Sodium (mg)"] * 0.5 - df_scaled["Total carbohydrate (g)"] * 0.3 - df_scaled["Added Sugars (g)"] * 0.2
    
    # Clustering
    X = df_scaled[["Energetic_Score", "Lean_Score", "Satiated_Score", "Avoid_Bloating_Score"]]
    scaler_std = StandardScaler()
    X_scaled = scaler_std.fit_transform(X)
    
    kmeans = KMeans(n_clusters=4, random_state=42)
    df_scaled["Cluster"] = kmeans.fit_predict(X_scaled)
    
    return df_scaled

# Meal recommendation based on feeling
def recommend_meals(df, feeling):
    feeling_map = {
        "⚡ Energetic": "Energetic_Score",
        "🏋 Lean": "Lean_Score",
        "🍛 Satiated": "Satiated_Score",
        "💨 Avoid Bloating": "Avoid_Bloating_Score"
    }
    
    if feeling not in feeling_map:
        return None
    
    top_meals = df.sort_values(by=feeling_map[feeling], ascending=False).head(5)
    return top_meals[["Menu Items", "Menu Category"]]

# Streamlit UI
st.set_page_config(page_title="Meal Recommender", page_icon="🍽", layout="wide")
st.title("🍽 Smart Meal Recommendation System")
st.write("### Find the best meal based on how you want to feel after eating! 😋")

# Load Data
df = load_data()

# Feeling selection UI
st.write("#### Select how you want to feel after your meal:")
col1, col2, col3, col4 = st.columns(4)

with col1:
    feeling = st.button("⚡ Energetic")
    if feeling:
        selected_feeling = "⚡ Energetic"

with col2:
    feeling = st.button("🏋 Lean")
    if feeling:
        selected_feeling = "🏋 Lean"

with col3:
    feeling = st.button("🍛 Satiated")
    if feeling:
        selected_feeling = "🍛 Satiated"

with col4:
    feeling = st.button("💨 Avoid Bloating")
    if feeling:
        selected_feeling = "💨 Avoid Bloating"

# Display Recommendations
if 'selected_feeling' in locals():
    st.write(f"### Recommended Meals for {selected_feeling}")
    recommendations = recommend_meals(df, selected_feeling)
    if recommendations is not None:
        st.dataframe(recommendations, use_container_width=True)
    else:
        st.error("Something went wrong! Please try again.")
