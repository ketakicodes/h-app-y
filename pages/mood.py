import streamlit as st
import pandas as pd

# ---- ✅ Set Up Streamlit Page ----
st.set_page_config(page_title="Mind", page_icon="💜", layout="centered")

# ---- 🌟 Custom CSS ----
st.markdown("""
    <style>
        .stApp { background: radial-gradient(circle, rgba(173, 83, 137, 1) 10%, rgba(108, 92, 231, 1) 40%, rgba(72, 52, 212, 1) 70%, rgba(48, 51, 107, 1) 100%); color: white; }
        h1, h2, h3, p, label { color: white !important; font-weight: bold; text-align: center; }
    </style>
    """,
    unsafe_allow_html=True
)

# ---- 💜 Title ----
st.title("💜 Mood-Based Food Recommender (Research-Backed!)")
st.subheader("Tell us how you're feeling today!")

# ---- 🎭 Mood Slider ----
mood_rating = st.slider("Move the slider to select your mood:", 1, 10, 5)

# ---- 🟢 Mood Labels ----
mood_labels = {
    1: "😢 Sad", 2: "😞 Down", 3: "😕 Meh", 4: "😐 Neutral",
    5: "🙂 Slightly Happy", 6: "😊 Happy", 7: "😁 Very Happy",
    8: "🤩 Excited", 9: "🎉 Super Excited", 10: "🥳 Extremely Happy"
}
st.markdown(f"### {mood_labels[mood_rating]}")

# ---- 📊 Mood Guide (Research-Backed!) ----
st.markdown("""
*Mood Guide (Research-Backed!):*  
🟣 **Low Mood (1-3)** → Comfort food (Higher protein & moderate fats)  
🟡 **Neutral Mood (4-6)** → Balanced meals (Good carbs, protein & fats)  
🟢 **High Mood (7-10)** → Energy-boosting food (Healthy carbs, fiber & moderate protein)  
""")

# ---- 🍽️ Category Selection ----
category = st.selectbox("What type of food do you prefer?", ["Veg", "Non-Veg"])

# ---- 🚫 Safer Category Classification ----
NON_VEG_KEYWORDS = ["chicken", "egg", "fish", "beef", "mutton", "bacon", "sausage", "pepperoni"]
VEG_KEYWORDS = ["paneer", "cheese", "butter", "milk"]

def classify_category(menu_item):
    """Classifies food into Veg or Non-Veg using keywords."""
    item_lower = menu_item.lower()
    if any(word in item_lower for word in NON_VEG_KEYWORDS):
        return "Non-Veg"
    return "Veg"

# ---- 📂 Data Preprocessing ----
def preprocess_data(file_path):
    """Loads & cleans menu data, calculates scores, and assigns categories."""
    try:
        df = pd.read_csv(file_path)
        df.columns = df.columns.str.strip()

        # ✅ Assign Veg / Non-Veg
        df["Category"] = df["Menu Items"].apply(classify_category)

        # ✅ Compute Carb Quality Score (Research-Backed!)
        df['Carb Quality Score'] = df['Total carbohydrate (g)'] - (df['Added Sugars (g)'] * 2)

        # ✅ Define High-Quality & Low-Quality Carbs
        df['High Quality Carb'] = ((df['Added Sugars (g)'] < 2) & (df['Total carbohydrate (g)'] / df['Protein (g)'] < 3)).astype(int)
        df['Low Quality Carb'] = ((df['Added Sugars (g)'] > 5) | (df['Total carbohydrate (g)'] / df['Protein (g)'] > 5)).astype(int)

        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# ---- 🧠 Mood-Based Weight Adjustments (Fully Dynamic!) ----
def compute_mood_score(df, mood_rating):
    """Calculates Mood Support Score dynamically based on research-backed mood levels."""

    # ✅ Adjust Weights Based on Mood  
    if mood_rating <= 3:  # Low Mood → Comfort Foods
        W_hc, W_p, W_f, W_lc = 2.0, 1.8, 1.5, 2.0
    elif 4 <= mood_rating <= 6:  # Moderate Mood → Balanced Choices
        W_hc, W_p, W_f, W_lc = 1.5, 1.5, 1.2, 1.5
    else:  # High Mood → Energy-Boosting Foods
        W_hc, W_p, W_f, W_lc = 1.2, 1.2, 1.0, 1.0

    # ✅ Compute Mood Support Score  
    df['Mood Support Score'] = (
        W_hc * df['High Quality Carb'] +
        W_p * df['Protein (g)'] +
        W_f * df['Total Fat (g)'] -
        W_lc * df['Low Quality Carb']
    )

    return df

# ---- 🍽️ Dynamic Mood-Based Recommendation ----
def recommend_items(df, category, mood_rating, top_n=3):
    """Filters & sorts items based on mood-specific criteria."""
    df_filtered = df[df['Category'].str.lower() == category.lower()]

    # ✅ Apply Mood-Specific Filtering  
    if mood_rating <= 3:  # Comfort foods (higher protein & fats)
        df_filtered = df_filtered[(df_filtered['Protein (g)'] > 6) & (df_filtered['Total Fat (g)'] > 5)]
    elif 4 <= mood_rating <= 6:  # Balanced meals
        df_filtered = df_filtered[(df_filtered['High Quality Carb'] == 1) & (df_filtered['Low Quality Carb'] == 0)]
    else:  # Energy-boosting foods
        df_filtered = df_filtered[df_filtered['Carb Quality Score'] > 8]

    df_sorted = df_filtered.sort_values(by='Mood Support Score', ascending=False)
    return df_sorted.head(top_n)

# ---- 🔘 Get Recommendations ----
if st.button("Get My Food Recommendations 🍔"):
    file_path = "India_Menu.csv"  
    df = preprocess_data(file_path)

    if df is not None:
        df = compute_mood_score(df, mood_rating)
        top_recommendations = recommend_items(df, category, mood_rating)

        # ✅ 🎉 Show Dynamic Recommendations  
        st.subheader(f"🍽️ Your Top Food Recommendations (Research-Backed!):")
        for _, row in top_recommendations.iterrows():
            st.write(f"*{row['Menu Items']}*")
            st.write(f"🔥 Calories: {row['Energy (kCal)']} | 🍞 Carbs: {row['Total carbohydrate (g)']}g | 🥩 Protein: {row['Protein (g)']}g | 🍬 Sugar: {row['Added Sugars (g)']}g")
            st.write(f"💜 Mood Support Score: {round(row['Mood Support Score'], 2)}\n")
