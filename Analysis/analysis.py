# Importing necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
try:
    data = pd.read_csv(r"C:\Users\thehe\Downloads\food_Ingredients.csv")
except FileNotFoundError:
    print("File not found. Please check the file path.")
    exit()
# Inspect the first few rows of the dataset and its structure
# This helps in understanding the data better
print(data.head())  # Display the first 5 rows
print(data.info())  # Display column names, non-null counts, and data types

# Remove unnecessary columns
# Check if there is an unnamed index column and drop it if present
if 'Unnamed: 0' in data.columns:
    data = data.drop(columns=['Unnamed: 0'])

# Handle missing values
# Fill any missing values with the median value of the column
print(data.isnull().sum())
data = data.fillna(data.median())

# Add derived metrics (new features)
# Calculate 'calories_density' as calories per unit size
# Calculate 'nutrient_richness' as the sum of specific nutrients
data['calories_density'] = data['calories_kcal'] / data['size']
data['nutrient_richness'] = data[['vitA_g', 'calcium_mg', 'vitC_mg', 'zinc_mg']].sum(axis=1)

# Exploratory Data Analysis (EDA) - Visualizations

# Plot the distribution of calories
# Use a histogram with KDE to visualize the distribution of 'calories_kcal'
sns.histplot(data['calories_kcal'], kde=True, bins=30)
plt.title('Distribution of Calories')
plt.xlabel('Calories (kcal)')
plt.ylabel('Frequency')
plt.tight_layout()
plt.show()

# Plot the distribution of macronutrients (fats, carbs, proteins)
# A boxplot helps visualize the spread and outliers in the data
macronutrients = ['fats_g', 'carb_g', 'protein_g']
sns.boxplot(data[macronutrients])
plt.title('Macronutrient Distribution')
plt.ylabel('Grams (g)')
plt.tight_layout()
plt.show()

# Correlation heatmap to visualize relationships between numerical columns
# The heatmap will show the correlation between various features
plt.figure(figsize=(10, 8))
sns.heatmap(data.corr(), annot=True, cmap='coolwarm', fmt=".1f")
plt.title('Correlation Matrix')
plt.tight_layout()
plt.show()

# Scatter plot of calories density vs nutrient richness
# To visualize the relationship between calorie density and nutrient richness
plt.figure(figsize=(8, 6))
sns.scatterplot(x='calories_density', y='nutrient_richness', hue='quality', data=data)
plt.title('Calories Density vs Nutrient Richness')
plt.xlabel('Calories Density')
plt.ylabel('Nutrient Richness')
plt.legend(title='Quality')
plt.tight_layout()
plt.show()

# Flagging low sodium and high protein foods
# Create new boolean columns for low sodium and high protein foods based on specific thresholds
data['low_sodium'] = data['sod_mg'] < 140
data['high_protein'] = data['protein_g'] > 5

# Summary of flagged data
# Calculate the percentage of products that meet the low sodium and high protein criteria
summary = data[['low_sodium', 'high_protein']].mean() * 100
print("Percentage of products with low sodium and high protein:")
print(summary)

# Save the cleaned data to a new CSV file for future use
# Ensure the path is correct where you want to save the cleaned dataset
data.to_csv(r"D:\Cleaned data\cleaned_babyfood_Ingredients.csv", index=False)

