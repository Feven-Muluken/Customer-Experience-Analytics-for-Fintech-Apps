import pandas as pd # pyright: ignore[reportMissingModuleSource]
from dateutil import parser # pyright: ignore[reportMissingModuleSource]

def clean_reviews(input_file="data/raw/all_reviews_raw.csv",
                  output_file="data/processed/all_reviews_clean.csv"):
    """
    Clean and preprocess reviews:
    - Remove duplicates
    - Handle missing values
    - Normalize date format
    - Save cleaned CSV
    """
    df = pd.read_csv(input_file)

    # Remove duplicates
    df = df.drop_duplicates(subset=['review'])

    # Drop missing review or rating
    df = df.dropna(subset=['review', 'rating'])

    # Normalize date to YYYY-MM-DD
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')

    # Save cleaned dataset
    df.to_csv(output_file, index=False)
    print(f"Saved cleaned dataset to {output_file}")

if __name__ == "__main__":
    clean_reviews()
