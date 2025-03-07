import pandas as pd
import numpy as np

# Load the dataset
file_path = "India_Menu.csv"  # Adjust the file path if necessary
df = pd.read_csv(file_path)

# Fill missing values for Sodium (mg) with the median
df['Sodium (mg)'] = df['Sodium (mg)'].fillna(df['Sodium (mg)'].median())

# Helper function: Identify if an item is vegetarian.
def is_vegetarian(item_name):
    """
    Returns 1 if the menu item is considered vegetarian, 0 if non-vegetarian.
    Checks non-veg keywords first so that if an item contains any non-veg terms,
    it is flagged as non-vegetarian.
    """
    item_name_lower = item_name.lower()
    non_veg_keywords = ["chicken", "beef", "mutton", "fish", "prawn", "egg","sausage"]
    for kw in non_veg_keywords:
        if kw in item_name_lower:
            return 0
    return 1

# Create a new column that flags vegetarian items (1 for veg, 0 for non-veg)
df['is_veg'] = df['Menu Items'].apply(is_vegetarian)

# Define a function for min-max normalization.
def min_max_normalize(series, invert=False):
    normalized = (series - series.min()) / (series.max() - series.min())
    if invert:
        normalized = 1 - normalized
    return normalized

# Normalize the nutritional metrics.
df['norm_protein'] = min_max_normalize(df['Protein (g)'], invert=False)  # Higher is better
df['norm_trans_fat'] = min_max_normalize(df['Trans fat (g)'], invert=True)  # Lower is better
df['norm_added_sugars'] = min_max_normalize(df['Added Sugars (g)'], invert=True)  # Lower is better
df['norm_sodium'] = min_max_normalize(df['Sodium (mg)'], invert=True)  # Lower is better
df['norm_sat_fat'] = min_max_normalize(df['Sat Fat (g)'], invert=True)  # Lower is better

# Define weights for each factor.
w_protein = 0.3    # Protein is a strong positive indicator.
w_trans   = 0.2    # Low trans fats are important.
w_sugar   = 0.2    # Lower added sugars improve vibrational quality.
w_sodium  = 0.2    # Lower sodium correlates with less processing.
w_sat     = 0.1    # Lower saturated fat is better.
w_veg     = 0.1    # Vegetarian items receive an extra bonus.

# Compute the composite vibrational score.
df['vibrational_score'] = (
    w_protein * df['norm_protein'] +
    w_trans   * df['norm_trans_fat'] +
    w_sugar   * df['norm_added_sugars'] +
    w_sodium  * df['norm_sodium'] +
    w_sat     * df['norm_sat_fat'] +
    w_veg     * df['is_veg']  # Bonus if the item is vegetarian.
)

# Filter out non-vegetarian items: only keep items where is_veg == 1.
df_veg = df[df['is_veg'] == 1]

# Sort the vegetarian items by vibrational score in descending order and select the top 10.
top10_veg = df_veg.sort_values(by='vibrational_score', ascending=False).head(10)

# Display the top 10 high vibrational vegetarian items.
print("Top 10 High Vibrational Vegetarian Items:")
print(top10_veg[['Menu Items', 'vibrational_score', 'Protein (g)', 'Trans fat (g)', 
                 'Added Sugars (g)', 'Sodium (mg)', 'Sat Fat (g)', 'is_veg']])
