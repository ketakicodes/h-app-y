import pandas as pd
import string

# ------------------------------
# Load Dataset
# ------------------------------
file_path = "India_Menu.csv"  # Adjust the path if necessary
df = pd.read_csv(file_path)

# ------------------------------
# Step 0: Mark Vegetarian vs Non-Vegetarian
# ------------------------------
def is_vegetarian(item_name):
    """
    Returns 1 if the menu item is considered vegetarian, 0 if non-vegetarian.
    Checks for common non-veg keywords.
    """
    item_name_lower = item_name.lower()
    non_veg_keywords = ["chicken", "beef", "mutton", "fish", "prawn", "egg", "sausage"]
    for kw in non_veg_keywords:
        if kw in item_name_lower:
            return 0
    return 1

df['is_veg'] = df['Menu Items'].apply(is_vegetarian)

# ------------------------------
# Step 1: Define Expanded Texture Lexicon
# ------------------------------
texture_dict = {
    "crispy": ["crispy", "crunchy", "brittle", "fried", "nuggets"],
    "chewy": ["chewy", "tough", "rubbery", "gum"],
    "soft": ["soft", "fluffy", "tender", "muffin", "burger"],
    "smooth": ["smooth", "velvety", "creamy", "flat white"]
}

# Define a mapping from texture to a post-eating feeling.
texture_feelings = {
    "crispy": "energizing",   # e.g., lively and invigorating
    "chewy": "satisfying",    # e.g., substantial and filling
    "soft": "comforting",     # e.g., soothing and indulgent
    "smooth": "soothing",     # e.g., calming and refined
    "unknown": "neutral"      # no distinct feeling assigned
}

# ------------------------------
# Step 2: Ensemble Texture Classifier Function (Without spaCy)
# ------------------------------
def classify_texture_ensemble(item_name):
    """
    Classifies the texture of a menu item using an ensemble approach:
      - Rule-based keyword matching from an expanded lexicon.
      - Simple tokenization-based matching.
    Returns the texture (crispy, chewy, soft, smooth) with the highest combined score,
    or 'unknown' if no descriptors are found.
    """
    scores = {texture: 0 for texture in texture_dict.keys()}
    lower_name = item_name.lower()
    
    # --- Rule-Based Matching (substring search) ---
    for texture, keywords in texture_dict.items():
        for kw in keywords:
            if kw in lower_name:
                scores[texture] += 1

    # --- Simple Tokenization-Based Matching ---
    tokens = lower_name.split()
    tokens = [token.strip(string.punctuation) for token in tokens]
    for token in tokens:
        for texture, keywords in texture_dict.items():
            if token in keywords:
                scores[texture] += 1

    max_score = max(scores.values())
    if max_score == 0:
        return "unknown"
    return max(scores, key=scores.get)

# Apply the ensemble classifier to create a new 'texture' column.
df['texture'] = df['Menu Items'].apply(classify_texture_ensemble)

# ------------------------------
# Step 2.5: Assign Post-Eating Feeling Based on Texture
# ------------------------------
def assign_feeling(texture):
    """
    Maps a given texture to a post-eating feeling.
    """
    return texture_feelings.get(texture, "neutral")

df['post_eating_feeling'] = df['texture'].apply(assign_feeling)

# ------------------------------
# Step 3: User Interaction and Filtering by Texture & Diet
# ------------------------------
desired_texture = input("Enter the desired texture (e.g., crispy, chewy, soft, smooth): ").strip().lower()

# Filter items by desired texture.
filtered_df = df[df['texture'] == desired_texture]

if filtered_df.empty:
    print(f"No items found with texture '{desired_texture}'.")
else:
    # Display the first 5 matching items.
    top5_items = filtered_df.head(5)
    print(f"\nTop 5 items with texture '{desired_texture}':")
    print(top5_items[['Menu Items', 'texture', 'post_eating_feeling', 'is_veg']])
    
# Optionally, separate results by vegetarian vs non-vegetarian:
veg_items = filtered_df[filtered_df['is_veg'] == 1]
nonveg_items = filtered_df[filtered_df['is_veg'] == 0]

print("\n--- Vegetarian Items ---")
if veg_items.empty:
    print("None found.")
else:
    print(veg_items[['Menu Items', 'texture', 'post_eating_feeling']].head(5))

print("\n--- Non-Vegetarian Items ---")
if nonveg_items.empty:
    print("None found.")
else:
    print(nonveg_items[['Menu Items', 'texture', 'post_eating_feeling']].head(5))
