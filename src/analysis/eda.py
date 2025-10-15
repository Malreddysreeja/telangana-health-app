import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Paths
PROCESSED_DATA_PATH = "data/processed/cleaned_data.csv"
OUTPUT_PATH = "data/processed/eda_outputs"

# Ensure output folder exists
os.makedirs(OUTPUT_PATH, exist_ok=True)

def run_eda():
    # Load data
    df = pd.read_csv(PROCESSED_DATA_PATH)
    print("Data Loaded Successfully!\n")
    print(df.head())

    # Basic statistics
    print("\nDataset Info:")
    print(df.info())
    print("\nSummary Statistics:")
    print(df.describe(include="all"))

    # Example 1: Disease distribution
    plt.figure(figsize=(10, 6))
    df['Disease'].value_counts().plot(kind='bar', color="skyblue", edgecolor="black")
    plt.title("Disease Distribution")
    plt.xlabel("Disease")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_PATH}/disease_distribution.png")
    plt.close()

    # Example 2: Cases over time (if year/month exists)
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df['Year'] = df['Date'].dt.year
        yearly_cases = df.groupby('Year')['Cases'].sum()

        plt.figure(figsize=(10, 6))
        yearly_cases.plot(kind='line', marker='o', color="green")
        plt.title("Cases Over Years")
        plt.xlabel("Year")
        plt.ylabel("Total Cases")
        plt.tight_layout()
        plt.savefig(f"{OUTPUT_PATH}/cases_over_years.png")
        plt.close()

    # Example 3: Cases by season
    if 'season' in df.columns:
        plt.figure(figsize=(8, 6))
        sns.boxplot(x='season', y='Cases', data=df, palette="Set2")
        plt.title("Cases by Season")
        plt.tight_layout()
        plt.savefig(f"{OUTPUT_PATH}/cases_by_season.png")
        plt.close()

    # Example 4: District-wise cases
    if 'District' in df.columns:
        district_cases = df.groupby('District')['Cases'].sum().sort_values(ascending=False)
        plt.figure(figsize=(12, 6))
        district_cases.plot(kind='bar', color="orange", edgecolor="black")
        plt.title("Total Cases by District")
        plt.xlabel("District")
        plt.ylabel("Total Cases")
        plt.xticks(rotation=75)
        plt.tight_layout()
        plt.savefig(f"{OUTPUT_PATH}/cases_by_district.png")
        plt.close()

    print(f"\n✅ EDA completed! Graphs saved in: {OUTPUT_PATH}")

if __name__ == "__main__":
    run_eda()
