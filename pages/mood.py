import streamlit as st
import pandas as pd

# ---- ✅ Fix: Set Page Config First ----
st.set_page_config(
    page_title="Mind", page_icon="💜", layout="centered")

# ---- Custom CSS for Aesthetic Aura Background ----
st.markdown(
    """
    <style>
        /* Aura Gradient Background */
        .stApp {
            background: radial-gradient(circle, rgba(173, 83, 137, 1) 10%, rgba(108, 92, 231, 1) 40%, rgba(72, 52, 212, 1) 70%, rgba(48, 51, 107, 1) 100%);
            color: white;
        }

        /* White Text */
        h1, h2, h3, h4, h5, h6, p, label {
            color: white !important;
            font-weight: bold;
            text-align: center;
        }

        /* Centering Elements */
        .stSlider, .stSelectbox, .stButton {
            margin: auto;
            display: flex;
            justify-content: center;
        }

        /* Custom Styling for Buttons */
        .stButton > button {
            background-color: white;
            color: #8E44AD;
            font-weight: bold;
            border-radius: 20px;
            padding: 10px 25px;
            box-shadow: 0px 4px 15px rgba(255, 255, 255, 0.3);
            transition: all 0.3s ease-in-out;
        }
        .stButton > button:hover {
            background-color: #8E44AD;
            color: white;
            transform: scale(1.05);
        }

        /* Custom Styling for Sliders & Selectbox */
        .stSlider, .stSelectbox {
            background: rgba(255, 255, 255, 0.2);
            border-radius: 20px;
            padding: 10px;
        }
        
    </style>
    """,
    unsafe_allow_html=True
)

# ---- Title & Subtitle ----
st.title("💜 Mood-Based Food Recommender")
st.subheader("Tell us how you're feeling today!")

# ---- Mood Slider (1-10) with Dynamic Emoji ----
mood_rating = st.slider("Move the slider to select your mood:", 1, 10, 5)

# Mood Mapping (1 = Sad, 10 = Extremely Happy)
mood_labels = {
    1: "😢 Sad",
    2: "😞 Down",
    3: "😕 Meh",
    4: "😐 Neutral",
    5: "🙂 Slightly Happy",
    6: "😊 Happy",
    7: "😁 Very Happy",
    8: "🤩 Excited",
    9: "🎉 Super Excited",
    10: "🥳 Extremely Happy"
}

# Display Mood Based on Slider
st.markdown(f"### {mood_labels[mood_rating]}")

# Mood Guide
st.markdown("""
*Mood Guide:*  
🟣 *1-3* → Feeling low 😢 (Need comfort food?)  
🟡 *4-6* → Neutral/Happy 😊 (Balanced meal might be best!)  
🟢 *7-10* → Super Happy 🥳 (Go for energy-boosting food!)  
""")

# ---- Category Selection ----
category = st.selectbox(
    "What type of food do you prefer?",
    ["Veg", "Non-Veg"]
)

# ---- Food Recommendation Logic ----

# List of keywords to identify food category
NON_VEG_KEYWORDS = ["chicken", "egg", "fish", "beef", "mutton", "bacon", "pepperoni"]
VEGETARIAN_KEYWORDS = ["paneer", "cheese", "butter", "milk", "mayonnaise"]

# Function to classify food category based on item name
def classify_category(menu_item):
    """Classifies an item as Veg or Non-Veg based on keywords."""
    item_lower = menu_item.lower()

    # Check for Non-Veg keywords
    if any(word in item_lower for word in NON_VEG_KEYWORDS):
        return "Non-Veg"

    return "Veg"  # If no Non-Veg keywords found, classify as Veg

# Load and preprocess menu data
def preprocess_data(file_path):
    """Loads data, cleans column names, and assigns category (Veg or Non-Veg)."""
    try:
        df = pd.read_csv(file_path)
        df.columns = df.columns.str.strip()  # Remove extra spaces in column names

        # Assign category to each item
        df["Category"] = df["Menu Items"].apply(classify_category)

        return df
    except FileNotFoundError:
        st.error("Error: File not found. Ensure 'India_Menu.csv' is in the correct directory.")
        return None
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# ---- ✅ Updated Recommendation Logic with Proper Weights ----
def recommend_items(df, category, mood_rating, top_n=3):
    """Filters by category (Veg/Non-Veg), applies weighted meal selection, and sorts by Mood Support Score."""
    df_filtered = df[df['Category'].str.lower() == category.lower()]  

    # **Weighted Adjustments**
    if mood_rating <= 3:  # Low Mood (Comfort Food)
        df_filtered["Weighted Score"] = (
            (df_filtered["Protein (g)"] * 0.4) +  
            (df_filtered["Total Fat (g)"] * 0.5) -  
            (df_filtered["Total Sugars (g)"] * 0.3)  
        )

    elif 4 <= mood_rating <= 6:  # Neutral Mood (Balanced Meals)
        df_filtered["Weighted Score"] = (
            (df_filtered["Protein (g)"] * 0.3) +  
            (df_filtered["Total carbohydrate (g)"] * 0.4) -  
            (df_filtered["Total Sugars (g)"] * 0.2)  
        )

    else:  # High Mood (Energy-Boosting)
        df_filtered["Weighted Score"] = (
            (df_filtered["Total carbohydrate (g)"] * 0.5) +  
            (df_filtered["Protein (g)"] * 0.3) -  
            (df_filtered["Total Fat (g)"] * 0.2)  
        )

    df_sorted = df_filtered.sort_values(by='Weighted Score', ascending=False)
    return df_sorted.head(top_n)

# ---- Submit Button ----
if st.button("Get My Food Recommendations 🍔"):
    # Load data
    file_path = "India_Menu_New.csv"  
    df = preprocess_data(file_path)

    if df is not None:
        df = recommend_items(df, category, mood_rating)

        st.subheader("🍽️ Your Top Food Recommendations:")
        for _, row in df.iterrows():
            st.write(f"*{row['Menu Items']}*")
            st.write(f"🔥 Calories: {row['Energy (kCal)']} | 🍞 Carbs: {row['Total carbohydrate (g)']}g | 🥩 Protein: {row['Protein (g)']}g | 🍬 Sugar: {row['Total Sugars (g)']}g")
            st.write(f"💜 Weighted Score: {round(row['Weighted Score'], 2)}\n")
