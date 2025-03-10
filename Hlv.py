import pandas as pd
import numpy as np

# ------------------------------
# Load & Preprocess Data
# ------------------------------
file_path = "India_Menu.csv"  # Adjust the file path if necessary
df = pd.read_csv(file_path)

# Fill missing Sodium (mg) values with the median.
df['Sodium (mg)'] = df['Sodium (mg)'].fillna(df['Sodium (mg)'].median())

# ------------------------------
# Step 1: Identify Vegetarian Items
# ------------------------------
def is_vegetarian(item_name):
    """
    Returns 1 if the menu item is considered vegetarian, 0 if non-vegetarian.
    Checks non-veg keywords first.
    """
    item_name_lower = item_name.lower()
    non_veg_keywords = ["chicken", "beef", "mutton", "fish", "prawn", "egg", "sausage"]
    for kw in non_veg_keywords:
        if kw in item_name_lower:
            return 0
    return 1

df['is_veg'] = df['Menu Items'].apply(is_vegetarian)

# ------------------------------
# Step 2: Processing Indicator
# ------------------------------
def is_processed(item_name):
    """
    Returns 1 if the item appears to be processed (e.g., 'fried', 'nuggets', 'muffin', 'sausage'),
    and 0 otherwise.
    """
    name = item_name.lower()
    processed_keywords = ["fried", "nuggets", "muffin", "sausage"]
    for kw in processed_keywords:
        if kw in name:
            return 1
    return 0

df['is_processed'] = df['Menu Items'].apply(is_processed)

# ------------------------------
# Step 3: Compute Healthy Fat Ratio
# ------------------------------
# Ratio of unsaturated fats (Total fat minus Sat & Trans fat) to Total fat.
df['healthy_fat_ratio'] = np.where(
    df['Total fat (g)'] > 0,
    (df['Total fat (g)'] - df['Sat Fat (g)'] - df['Trans fat (g)']) / df['Total fat (g)'],
    1
)

# ------------------------------
# Step 4: Compute Energy Density
# ------------------------------
def extract_weight(serve_size):
    """
    Extracts numeric serving weight in grams from a string (e.g., '168 g').
    """
    try:
        return float(serve_size.split()[0])
    except:
        return np.nan

df['serve_weight'] = df['Per Serve Size'].apply(extract_weight)
df['serve_weight'] = df['serve_weight'].fillna(df['serve_weight'].median())
df['energy_density'] = df['Energy (kCal)'] / df['serve_weight']  # kCal per gram; lower is better.

# ------------------------------
# Step 5: Compute Carbohydrate Quality
# ------------------------------
# We use (Total Carbohydrate - Total Sugars) / Total Carbohydrate as a proxy for complex carbohydrate quality.
df['complex_carb_ratio'] = np.where(
    df['Total carbohydrate (g)'] > 0,
    (df['Total carbohydrate (g)'] - df['Total Sugars (g)']) / df['Total carbohydrate (g)'],
    1
)

# ------------------------------
# Step 6: Incorporate Cholesterol
# ------------------------------
# Lower cholesterol is favored.
# The column name in your dataset is assumed to be "Cholesterols (mg)".
# (If the column name differs, please adjust accordingly.)
 
# ------------------------------
# Step 7: Normalization Function
# ------------------------------
def min_max_normalize(series, invert=False):
    normalized = (series - series.min()) / (series.max() - series.min())
    return 1 - normalized if invert else normalized

# Normalize available nutritional metrics:
df['norm_protein']         = min_max_normalize(df['Protein (g)'], invert=False)             # Higher is better.
df['norm_trans_fat']       = min_max_normalize(df['Trans fat (g)'], invert=True)              # Lower is better.
df['norm_added_sugars']    = min_max_normalize(df['Added Sugars (g)'], invert=True)           # Lower is better.
df['norm_sodium']          = min_max_normalize(df['Sodium (mg)'], invert=True)                  # Lower is better.
df['norm_sat_fat']         = min_max_normalize(df['Sat Fat (g)'], invert=True)                  # Lower is better.
df['norm_healthy_fat']     = min_max_normalize(df['healthy_fat_ratio'], invert=False)           # Higher is better.
df['norm_energy_density']  = min_max_normalize(df['energy_density'], invert=True)               # Lower energy density is better.
df['norm_complex_carb']    = min_max_normalize(df['complex_carb_ratio'], invert=False)          # Higher is better.
df['norm_cholesterol']     = min_max_normalize(df['Cholesterols (mg)'], invert=True)            # Lower is better.

# ------------------------------
# Step 8: Compute Composite "Vibrational" Score
# ------------------------------
# Weights (inspired by evidence-based profiling and Tufts Food Compass):
w_protein       = 0.15  # Nutrient density
w_trans         = 0.10  # Penalize unhealthy fats
w_added_sugars  = 0.10  # Penalize excess sugars
w_sodium        = 0.10  # Penalize high sodium
w_sat           = 0.08  # Penalize high saturated fat
w_veg           = 0.08  # Bonus for plant-based (vegetarian) items
w_healthy_fat   = 0.07  # Reward quality fats
w_energy        = 0.08  # Favor lower energy density
w_complex_carb  = 0.10  # Reward complex carbohydrate quality
w_cholesterol   = 0.10  # Penalize high cholesterol
w_processed     = 0.08  # Penalty for processed items (subtracted)

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

# ------------------------------
# Step 9: Filter and Display Results
# ------------------------------

# (a) Top 10 High Vibrational Vegetarian Items:
df_veg = df[df['is_veg'] == 1]
top10_veg = df_veg.sort_values(by='vibrational_score', ascending=False).head(10)

print("Top 10 High Vibrational Vegetarian Items (Enhanced Model):")
print(top10_veg[['Menu Items', 'vibrational_score', 'Protein (g)', 'Trans fat (g)',
                 'Added Sugars (g)', 'Sodium (mg)', 'Sat Fat (g)', 'healthy_fat_ratio',
                 'energy_density', 'complex_carb_ratio', 'Cholesterols (mg)',
                 'is_processed', 'is_veg']])
print("\n" + "="*80 + "\n")

# (b) Top 10 Low Vibrational Foods:
low_vibrational = df.sort_values(by='vibrational_score', ascending=True).head(10)

print("Top 10 Low Vibrational Foods (Enhanced Model):")
print(low_vibrational[['Menu Items', 'vibrational_score', 'Protein (g)', 'Trans fat (g)',
                       'Added Sugars (g)', 'Sodium (mg)', 'Sat Fat (g)', 'healthy_fat_ratio',
                       'energy_density', 'complex_carb_ratio', 'Cholesterols (mg)',
                       'is_processed', 'is_veg']])
