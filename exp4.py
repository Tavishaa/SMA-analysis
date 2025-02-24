import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Define the existing directory where CSV is stored
save_path = r"C:/Users/91702/OneDrive/Desktop/SMA"

# Load dataset (Ensure the file exists in the specified path)
file_path = os.path.join(save_path, "olympics_2024_data_20250217_214839.csv")
df = pd.read_csv(file_path)

# Display the first few rows
print("Dataset Preview:")
print(df.head())

# Convert 'created_utc' to datetime format (if applicable)
df['created_utc'] = pd.to_datetime(df['created_utc'], errors='coerce')

# Check for missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Fill missing values (if needed)
df.fillna("", inplace=True)

# Descriptive statistics
print("\nDescriptive Statistics:")
print(df.describe())

# Engagement Level Analysis
print("\nEngagement Level Distribution:")
print(df['engagement_level'].value_counts())

# Category Distribution
print("\nCategory Distribution:")
print(df['category'].value_counts())

# --- Visualization Starts Here ---
# 1️⃣ Bar Chart: Post Categories Distribution
plt.figure(figsize=(10,6))
df['category'].value_counts().plot(kind='bar', color='skyblue', edgecolor='black')
plt.title("Post Categories Distribution")
plt.xlabel("Category")
plt.ylabel("Number of Posts")
plt.xticks(rotation=45)
plt.savefig(os.path.join(save_path, "bar_chart.png"))
plt.show()

# 2️⃣ Scatter Plot: Score vs. Number of Comments (Engagement Analysis)
plt.figure(figsize=(8,5))
sns.scatterplot(data=df, x='score', y='num_comments', hue='engagement_level', palette="viridis")
plt.title("Score vs. Number of Comments")
plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.savefig(os.path.join(save_path, "scatter_plot.png")) 
plt.show()

# 3️⃣ Box Plot: Scores across different categories
plt.figure(figsize=(12,6))  
sns.boxplot(data=df, x='category', y='score', palette="Set3", showfliers=True)  
plt.title("Scores Across Different Categories")
plt.xlabel("Category")
plt.ylabel("Score")
plt.xticks(rotation=30, ha="right")  
plt.grid(axis='y', linestyle="--", alpha=0.7) 
plt.savefig(os.path.join(save_path, "box_plot.png")) 
plt.show()

# Save the cleaned data
cleaned_csv_path = os.path.join(save_path, "cleaned_olympics_data.csv")
df.to_csv(cleaned_csv_path, index=False)

print(f"\n EDA and Visualization Completed. Graphs saved in: {save_path}")
print(f"Processed data saved as '{cleaned_csv_path}'.")
