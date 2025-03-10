import streamlit as st
import pandas as pd
import numpy as np

# ------------------------------
# Page Configuration
# ------------------------------
st.set_page_config(page_title="Soul", page_icon="🌟", layout="centered")

# ------------------------------
# Custom CSS for Aesthetic Aura Background & Button Styling
# ------------------------------
st.markdown(
    """
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
        /* Make buttons hot pink by default and deeper pink on hover */
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
            color: white;
            transform: scale(1.05);
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------------------
# Page Header
# ------------------------------
st.title("🌟 Soul-Based Analysis")
st.subheader("Discover Your Food's Vibrational Energy")

# ------------------------------
# Center the Button with Columns
# ------------------------------
col_left, col_mid, col_right = st.columns([1,2,1])
with col_mid:
    if st.button("Show High Vibe & Low Vibe Foods"):
        file_path = "India_Menu.csv"  # Adjust path as needed
        try:
            df = pd.read_csv(file_path)
        except Exception as e:
            st.error(f"Error loading file: {e}")
            st.stop()

        # Fill missing Sodium (mg) values with the median.
        df['Sodium (mg)'] = df['Sodium (mg)'].fillna(df['Sodium (mg)'].median())

        # Step 1: Identify Vegetarian Items
        def is_vegetarian(item_name):
            item_name_lower = item_name.lower()
            non_veg_keywords = ["chicken", "beef", "mutton", "fish", "prawn", "egg", "sausage"]
            for kw in non_veg_keywords:
                if kw in item_name_lower:
                    return 0
            return 1

        df['is_veg'] = df['Menu Items'].apply(is_vegetarian)

        # Step 2: Processing Indicator
        def is_processed(item_name):
            name = item_name.lower()
            processed_keywords = ["fried", "nuggets", "muffin", "sausage"]
            for kw in processed_keywords:
                if kw in name:
                    return 1
            return 0

        df['is_processed'] = df['Menu Items'].apply(is_processed)

        # Step 3: Compute Healthy Fat Ratio
        df['healthy_fat_ratio'] = np.where(
            df['Total fat (g)'] > 0,
            (df['Total fat (g)'] - df['Sat Fat (g)'] - df['Trans fat (g)']) / df['Total fat (g)'],
            1
        )

        # Step 4: Compute Energy Density
        def extract_weight(serve_size):
            try:
                return float(serve_size.split()[0])
            except:
                return np.nan

        df['serve_weight'] = df['Per Serve Size'].apply(extract_weight)
        df['serve_weight'] = df['serve_weight'].fillna(df['serve_weight'].median())
        df['energy_density'] = df['Energy (kCal)'] / df['serve_weight']

        # Step 5: Compute Carbohydrate Quality
        df['complex_carb_ratio'] = np.where(
            df['Total carbohydrate (g)'] > 0,
            (df['Total carbohydrate (g)'] - df['Total Sugars (g)']) / df['Total carbohydrate (g)'],
            1
        )

        # Step 7: Normalization Function
        def min_max_normalize(series, invert=False):
            normalized = (series - series.min()) / (series.max() - series.min())
            return 1 - normalized if invert else normalized

        # Normalize metrics
        df['norm_protein']         = min_max_normalize(df['Protein (g)'], invert=False)
        df['norm_trans_fat']       = min_max_normalize(df['Trans fat (g)'], invert=True)
        df['norm_added_sugars']    = min_max_normalize(df['Added Sugars (g)'], invert=True)
        df['norm_sodium']          = min_max_normalize(df['Sodium (mg)'], invert=True)
        df['norm_sat_fat']         = min_max_normalize(df['Sat Fat (g)'], invert=True)
        df['norm_healthy_fat']     = min_max_normalize(df['healthy_fat_ratio'], invert=False)
        df['norm_energy_density']  = min_max_normalize(df['energy_density'], invert=True)
        df['norm_complex_carb']    = min_max_normalize(df['complex_carb_ratio'], invert=False)
        df['norm_cholesterol']     = min_max_normalize(df['Cholesterols (mg)'], invert=True)

        # Step 8: Compute Composite "Vibrational" Score
        w_protein       = 0.15
        w_trans         = 0.10
        w_added_sugars  = 0.10
        w_sodium        = 0.10
        w_sat           = 0.08
        w_veg           = 0.08
        w_healthy_fat   = 0.07
        w_energy        = 0.08
        w_complex_carb  = 0.10
        w_cholesterol   = 0.10
        w_processed     = 0.08

        df['vibrational_score'] = (
            w_protein      * df['norm_protein'] +
            w_trans        * df['norm_trans_fat'] +
            w_added_sugars * df['norm_added_sugars'] +
            w_sodium       * df['norm_sodium'] +
            w_sat          * df['norm_sat_fat'] +
            w_veg          * df['is_veg'] +
            w_healthy_fat  * df['norm_healthy_fat'] +
            w_energy       * df['norm_energy_density'] +
            w_complex_carb * df['norm_complex_carb'] +
            w_cholesterol  * df['norm_cholesterol'] -
            w_processed    * df['is_processed']
        )

        # Step 9: Filter and Display Results
        df_veg = df[df['is_veg'] == 1]
        top10_veg = df_veg.sort_values(by='vibrational_score', ascending=False).head(10)
        low_vibrational = df.sort_values(by='vibrational_score', ascending=True).head(10)

        st.subheader("💫 Top 10 High Vibrational Vegetarian Items")
        st.dataframe(top10_veg[[
            'Menu Items', 'vibrational_score', 'Protein (g)', 'Trans fat (g)',
            'Added Sugars (g)', 'Sodium (mg)', 'Sat Fat (g)', 'healthy_fat_ratio',
            'energy_density', 'complex_carb_ratio', 'Cholesterols (mg)',
            'is_processed', 'is_veg'
        ]])

        st.subheader("🔥 Top 10 Low Vibrational Foods")
        st.dataframe(low_vibrational[[
            'Menu Items', 'vibrational_score', 'Protein (g)', 'Trans fat (g)',
            'Added Sugars (g)', 'Sodium (mg)', 'Sat Fat (g)', 'healthy_fat_ratio',
            'energy_density', 'complex_carb_ratio', 'Cholesterols (mg)',
            'is_processed', 'is_veg'
        ]])
