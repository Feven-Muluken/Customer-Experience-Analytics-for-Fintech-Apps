import pandas as pd # pyright: ignore[reportMissingModuleSource]
import psycopg2
from psycopg2.extras import execute_values

# Database parameters
DB_PARAMS = {
    "host": "127.0.0.1",
    "database": "bank_reviews",
    "user": "fenet",
    "password": "Password123",
    "port": 5432
}

# Load cleaned reviews from Task 2
df = pd.read_csv("data/processed/all_reviews_clean.csv")

# Connect to PostgreSQL
conn = psycopg2.connect(**DB_PARAMS)
cur = conn.cursor()

# Insert banks
banks = df[['bank']].drop_duplicates().reset_index(drop=True)
bank_tuples = [(row['bank'], row['bank']) for _, row in banks.iterrows()]  # bank_name, app_name

execute_values(cur,
    "INSERT INTO banks (bank_name, app_name) VALUES %s ON CONFLICT DO NOTHING",
    bank_tuples
)
conn.commit()

# Get bank_ids
cur.execute("SELECT bank_id, bank_name FROM banks")
bank_map = {name: id for id, name in cur.fetchall()}

# Insert reviews
review_tuples = [
    (
        bank_map[row['bank']],
        row['review'],
        int(row['rating']),
        row['date'],
        row['sentiment_label'],
        float(row['sentiment_score']),
        row['source']
    )
    for _, row in df.iterrows()
]

execute_values(cur,
    "INSERT INTO reviews (bank_id, review_text, rating, review_date, sentiment_label, sentiment_score, source) VALUES %s",
    review_tuples
)
conn.commit()

cur.close()
conn.close()
print("Data inserted successfully!")
