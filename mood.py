import pandas as pd

# List of keywords to identify food category
NON_VEG_KEYWORDS = ["chicken", "egg", "fish", "beef", "mutton", "bacon", "pepperoni"]
VEGETARIAN_KEYWORDS = ["paneer", "cheese", "butter", "milk", "mayonnaise"]
VEGAN_BLACKLIST = VEGETARIAN_KEYWORDS  # Any item containing these is not Vegan

# Function to classify food category based on item name
def classify_category(menu_items):
    """Classifies an item as Veg, Non-Veg, or Vegan based on keywords."""
    item_lower = menu_items.lower()

    # Check for Non-Veg keywords
    if any(word in item_lower for word in NON_VEG_KEYWORDS):
        return "Non-Veg"

    # Check for Vegan blacklist
    if any(word in item_lower for word in VEGAN_BLACKLIST):
        return "Veg"  # Vegetarian but not Vegan
venv\Scripts\activate

    return "Vegan"  # If no animal-based products found, classify as Vegan

# Load and preprocess McDonald's menu data
def preprocess_data(file_path):
    """Loads data, cleans column names, and assigns category (Veg, Non-Veg, Vegan)."""
    try:
        df = pd.read_csv(file_path)
        df.columns = df.columns.str.strip()  # Remove extra spaces in column names

        # Assign category to each item
        df["Category"] = df["Menu Items"].apply(classify_category)

        return df
    except FileNotFoundError:
        print("Error: File not found. Ensure 'mcdonalds_menu.csv' is in the correct directory.")
        exit()
    except Exception as e:
        print(f"Error: {e}")
        exit()

# Compute Carb Quality Score
def calculate_carb_quality(df):
    """Computes carb quality score to assess complex vs. refined carbs."""
    df['Carb Quality Score'] = df['Total carbohydrate (g)'] - (df['Total Sugars (g)'] * 2)
    df['Carb Type'] = df.apply(lambda row: 'High' if row['Total Sugars (g)'] < 2 and (row['Total carbohydrate (g)'] / max(row['Protein (g)'], 1)) < 3
                               else 'Low' if row['Total Sugars (g)'] > 5 and (row['Total carbohydrate (g)'] / max(row['Protein (g)'], 1)) > 5
                               else 'Moderate', axis=1)
    return df

# Compute Mood Support Score
def calculate_mood_score(df, mood_rating):
    """Computes a mood support score for each menu item."""
    scores = []

    for _, row in df.iterrows():
        score = 0

        # High-quality carbs boost serotonin
        if row['Carb Type'] == 'High':
            score += 3  # Reward complex carbs

        # Low-quality carbs cause sugar crashes
        if row['Carb Type'] == 'Low':
            score -= 3  # Penalize high sugar, refined carbs

        # Higher protein supports neurotransmitter function
        score += row['Protein (g)'] * 0.2  # Give +0.2 points per gram of protein

        # Omega-3 boosts mood (if available)
        if 'Omega-3 (g)' in df.columns and row['Omega-3 (g)'] > 0:
            score += 4  # Reward healthy fats

        # Adjust if mood is very low (≤3)
        if mood_rating <= 3:
            score *= 1.5  # Boost nutrient impact when mood is low

        scores.append(score)

    df['Mood Support Score'] = scores
    return df

# Get top recommended items
def recommend_items(df, category, top_n=3):
    """Filters by category (Veg/Non-Veg/Vegan), sorts items by Mood Support Score, and returns recommendations."""
    df_filtered = df[df['Category'].str.lower() == category.lower()]  # Filter by category
    df_sorted = df_filtered.sort_values(by='Mood Support Score', ascending=False)
    return df_sorted.head(top_n)

# Main function to run the recommendation system
def main():
    file_path = "/content/India_Menu.csv"

    # Load and preprocess data
    df = preprocess_data(file_path)

    # Ensure required columns exist
    required_columns = {'Menu Item', 'Energy (kCal)', 'Protein (g)', 'Total fat (g)', 'Sat Fat (g)', 'Trans fat (g)',
                        'Cholesterol (mg)', 'Total carbohydrate (g)', 'Total Sugars (g)', 'Sodium (mg)', 'Category'}
    if not required_columns.issubset(df.columns):
        print("Error: Missing required columns in the CSV file.")
        exit()

    # Ask for user mood input
    try:
        mood_rating = int(input("On a scale of 1 to 10, how is your mood today? (1 = very low, 10 = very high): "))
        if not (1 <= mood_rating <= 10):
            raise ValueError
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 10.")
        exit()

    # Ask user for Veg/Non-Veg/Vegan preference
    category = input("Do you prefer 'Veg', 'Non-Veg', or 'Vegan' items? ").strip().capitalize()
    if category not in ['Veg', 'Non-Veg', 'Vegan']:
        print("Invalid choice. Please enter 'Veg', 'Non-Veg', or 'Vegan'.")
        exit()

    # Compute carb quality
    df = calculate_carb_quality(df)

    # Calculate mood support scores
    df = calculate_mood_score(df, mood_rating)

    # Get top recommendations based on category and mood
    top_recommendations = recommend_items(df, category)

    # Display results
    print("\n Top Food Recommendations Based on Your Mood \n")
    for _, row in top_recommendations.iterrows():
        print(f" {row['Menu Items']}")
        print(f"   Calories: {row['Energy (kCal)']} | Carbs: {row['Total carbohydrate (g)']}g | Protein: {row['Protein (g)']}g | Sugar: {row['Total Sugars (g)']}g")
        print(f"   Mood Support Score: {round(row['Mood Support Score'], 2)}\n")

# Run the script
if __name__ == "__main__":
    main()
