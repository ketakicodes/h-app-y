import streamlit as st
import pandas as pd

# ---- ✅ Fix: Set Page Config First ----
st.set_page_config(page_title="Mind", page_icon="💜", layout="centered")

# ---- Custom CSS ----
st.markdown(
    """
    <style>
        .stApp { background: radial-gradient(circle, rgba(173, 83, 137, 1) 10%, rgba(108, 92, 231, 1) 40%, rgba(72, 52, 212, 1) 70%, rgba(48, 51, 107, 1) 100%); color: white; }
        h1, h2, h3, p, label { color: white !important; font-weight: bold; text-align: center; }
    </style>
    """,
    unsafe_allow_html=True
)

# ---- Title ----
st.title("💜 Mood-Based Food Recommender (Research-Backed!)")
st.subheader("Tell us how you're feeling today!")

# ---- Mood Slider ----
mood_rating = st.slider("Move the slider to select your mood:", 1, 10, 5)

# Mood Labels
mood_labels = {
    1: "😢 Sad", 2: "😞 Down", 3: "😕 Meh", 4: "😐 Neutral",
    5: "🙂 Slightly Happy", 6: "😊 Happy", 7: "😁 Very Happy",
    8: "🤩 Excited", 9: "🎉 Super Excited", 10: "🥳 Extremely Happy"
}
st.markdown(f"### {mood_labels[mood_rating]}")

# Mood Guide (Research-Backed!)
st.markdown("""
*Mood Guide (Research-Backed!):*  
🟣 *1-3* → Comfort food (Higher protein & moderate fats)  
🟡 *4-6* → Balanced meals (Good carbs, protein & fats)  
🟢 *7-10* → Energy-boosting food (Healthy carbs, fiber & moderate protein)  
""")

# ---- Category Selection ----
category = st.selectbox("What type of food do you prefer?", ["Veg", "Non-Veg"])

# ---- Improved Category Classifier ----
NON_VEG_KEYWORDS = ["chicken", "egg", "fish", "beef", "mutton", "bacon", "sausage", "pepperoni"]
VEG_KEYWORDS = ["paneer", "cheese", "butter", "milk"]

def classify_category(menu_item):
    """Classifies food into Veg or Non-Veg using keywords."""
    item_lower = menu_item.lower()
    if any(word in item_lower for word in NON_VEG_KEYWORDS):
        return "Non-Veg"
    return "Veg"

# ---- Data Preprocessing ----
def preprocess_data(file_path):
    """Loads & cleans menu data, calculates scores, and assigns categories."""
    try:
        df = pd.read_csv(file_path)
        df.columns = df.columns.str.strip()

        # Classify Veg / Non-Veg
        df["Category"] = df["Menu Items"].apply(classify_category)

        # ✅ Compute Carb Quality Score (Research-Backed!)
        df['Carb Quality Score'] = df['Total carbohydrate (g)'] - (df['Added Sugars (g)'] * 2)

        # ✅ Define High-Quality & Low-Quality Carbs (Based on Research)
        df['High Quality Carb'] = ((df['Added Sugars (g)'] < 2) & (df['Total carbohydrate (g)'] / df['Protein (g)'] < 3)).astype(int)
        df['Low Quality Carb'] = ((df['Added Sugars (g)'] > 5) | (df['Total carbohydrate (g)'] / df['Protein (g)'] > 5)).astype(int)

        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# ---- Mood-Based Weight Adjustments (Research-Backed!) ----
def compute_mood_score(df, mood_rating):
    """Calculates Mood Support Score dynamically based on research-backed mood levels."""
    
    # ✅ Define Mood Buckets & Weights  
    if mood_rating <= 3:  # Low Mood → Comfort Foods
        mood_bucket = "Low Mood"
        W_hc, W_p, W_f, W_lc = 1.5, 1.5, 1.2, 1.5
    elif 4 <= mood_rating <= 6:  # Moderate Mood → Balanced Choices
        mood_bucket = "Moderate Mood"
        W_hc, W_p, W_f, W_lc = 1.2, 1.2, 1.0, 1.2
    else:  # High Mood → Energy-Boosting Foods
        mood_bucket = "High Mood"
        W_hc, W_p, W_f, W_lc = 1.0, 1.0, 0.8, 1.0

    # ✅ Compute Mood Support Score  
    df['Mood Support Score'] = (
        W_hc * df['High Quality Carb'] +
        W_p * df['Protein (g)'] +
        W_f * df['Total Fat (g)'] -
        W_lc * df['Low Quality Carb']
    )

    return df, mood_bucket

# ---- Recommendation Logic (Research-Backed!) ----
def recommend_items(df, category, mood_bucket, top_n=3):
    """Filters by category, mood-based criteria, sorts, and returns recommendations."""
    df_filtered = df[df['Category'].str.lower() == category.lower()]

    # Filter foods based on mood bucket preferences
    if mood_bucket == "Low Mood":  # Comfort foods
        df_filtered = df_filtered[df_filtered['Protein (g)'] > 5]
    elif mood_bucket == "Moderate Mood":  # Balanced meals
        df_filtered = df_filtered[(df_filtered['High Quality Carb'] == 1) & (df_filtered['Low Quality Carb'] == 0)]
    else:  # High Mood → Energy-boosting
        df_filtered = df_filtered[df_filtered['Carb Quality Score'] > 10]

    df_sorted = df_filtered.sort_values(by='Mood Support Score', ascending=False)
    return df_sorted.head(top_n)

# ---- Submit Button ----
if st.button("Get My Food Recommendations 🍔"):
    file_path = "mcdonalds_menu.csv"  
    df = preprocess_data(file_path)

    if df is not None:
        df, mood_bucket = compute_mood_score(df, mood_rating)
        top_recommendations = recommend_items(df, category, mood_bucket)

        # Display Recommendations
        st.subheader(f"🍽️ Your Top Food Recommendations ({mood_bucket}) (Research-Backed!):")
        for _, row in top_recommendations.iterrows():
            st.write(f"*{row['Menu Items']}*")
            st.write(f"🔥 Calories: {row['Energy (kCal)']} | 🍞 Carbs: {row['Total carbohydrate (g)']}g | 🥩 Protein: {row['Protein (g)']}g | 🍬 Sugar: {row['Added Sugars (g)']}g")
            st.write(f"💜 Mood Support Score: {round(row['Mood Support Score'], 2)}\n")
