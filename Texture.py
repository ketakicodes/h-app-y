import pandas as pd

# Load the dataset
file_path = "India_Menu.csv"  # Adjust the path if necessary
df = pd.read_csv(file_path)

# Function to classify texture based on the menu item name.
def classify_texture(item_name):
    """
    Classifies the texture of a menu item using simple keyword heuristics.
      - Items containing 'nuggets' or 'fried' are considered 'crispy'
      - Items containing 'wrap' are considered 'chewy'
      - Items containing 'muffin' are considered 'soft'
      - 'Flat White' is classified as 'smooth'
      - Items containing 'burger' are classified as 'soft'
      - Otherwise, texture is 'unknown'
    """
    name = item_name.lower()
    if "nuggets" in name or "fried" in name:
        return "crispy"
    elif "wrap" in name:
        return "chewy"
    elif "muffin" in name:
        return "soft"
    elif "flat white" in name:
        return "smooth"
    elif "burger" in name:
        return "soft"
    else:
        return "unknown"

# Apply the texture classification to the 'Menu Items' column.
df['texture'] = df['Menu Items'].apply(classify_texture)

# Ask the user for the desired texture.
desired_texture = input("Enter the desired texture (e.g., crispy, chewy, soft, smooth): ").strip().lower()

# Filter items that match the desired texture.
filtered_df = df[df['texture'] == desired_texture]

if filtered_df.empty:
    print(f"No items found with texture '{desired_texture}'.")
else:
    # Display the first 5 items (or "top 5") that match the desired texture.
    top5_items = filtered_df.head(5)
    print(f"\nTop 5 items with texture '{desired_texture}':")
    print(top5_items[['Menu Items', 'texture']])
