# src/db/insert_reviews.py
import os
import pandas as pd # pyright: ignore[reportMissingModuleSource]
from sqlalchemy import create_engine, text # pyright: ignore[reportMissingImports]
from sqlalchemy.engine.url import URL # pyright: ignore[reportMissingImports]
from sqlalchemy.exc import SQLAlchemyError # pyright: ignore[reportMissingImports]
from dotenv import load_dotenv # pyright: ignore[reportMissingImports]

load_dotenv()

DB = {
    "drivername": "postgresql+psycopg2",
    "username": os.getenv("DB_USER", "fenet"),
    "password": os.getenv("DB_PASSWORD", ""),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "database": os.getenv("DB_NAME", "bank_reviews"),
}

CSV_PATH = os.getenv("PROCESSED_CSV", "data/processed/all_reviews_clean.csv")

def get_engine():
    url = URL.create(**DB)
    return create_engine(url, echo=False, pool_pre_ping=True)

def ensure_banks_table(engine, bank_map):
    with engine.connect() as conn:
        for key, name in bank_map.items():
            # upsert bank key/name/app_id (if app_id available in config)
            upsert = text("""
            INSERT INTO banks (bank_key, bank_name)
            VALUES (:bank_key, :bank_name)
            ON CONFLICT (bank_key) DO UPDATE
              SET bank_name = EXCLUDED.bank_name
            RETURNING bank_id;
            """)
            res = conn.execute(upsert, {"bank_key": key, "bank_name": name})
            # consume result to ensure insertion
            _ = res.fetchone()

def load_csv_and_insert(engine, csv_path, bank_key_col="bank"):
    df = pd.read_csv(csv_path)
    # normalize columns (ensure these exist)
    # expected: bank, review, rating, date, source (adapt if different)
    df = df.rename(columns={
        "review": "review_text",
        "date": "review_date",
        "bank": "bank_key",
        "rating": "rating"
    })
    df['review_date'] = pd.to_datetime(df['review_date'], errors='coerce').dt.date

    with engine.begin() as conn:
        # build bank_key -> bank_id map
        bank_keys = df['bank_key'].dropna().unique().tolist()
        q = text("SELECT bank_id, bank_key FROM banks WHERE bank_key = ANY(:keys)")
        rows = conn.execute(q, {"keys": bank_keys}).fetchall()
        existing = {r['bank_key']: r['bank_id'] for r in rows}

        # insert banks missing
        for k in bank_keys:
            if k not in existing:
                r = conn.execute(text("INSERT INTO banks (bank_key, bank_name) VALUES (:k, :k) RETURNING bank_id"), {"k": k})
                existing[k] = r.fetchone()['bank_id']

        # Prepare rows for insertion
        to_insert = []
        for _, row in df.iterrows():
            bank_key = row['bank_key']
            bank_id = existing.get(bank_key)
            if pd.isna(row['review_text']) or not bank_id:
                continue
            to_insert.append({
                "bank_id": int(bank_id),
                "review_text": str(row['review_text']),
                "rating": int(row['rating']) if not pd.isna(row['rating']) else None,
                "review_date": row['review_date'],
                "sentiment_label": row.get('sentiment_label'),
                "sentiment_score": row.get('sentiment_score'),
                "source": row.get('source')
            })

        if not to_insert:
            print("No rows to insert.")
            return

        # Use bulk insert
        conn.execute(
            text("""INSERT INTO reviews
                    (bank_id, review_text, rating, review_date, sentiment_label, sentiment_score, source)
                    VALUES (:bank_id, :review_text, :rating, :review_date, :sentiment_label, :sentiment_score, :source)
                """),
            to_insert
        )
    print(f"Inserted {len(to_insert)} reviews into DB.")

if __name__ == "__main__":
    from config import BANK_NAMES  # pyright: ignore[reportMissingImports] # you should have BANK_NAMES mapping in config.py
    engine = get_engine()
    # create tables if not exists (assumes schema.sql has run, otherwise run it)
    # Optionally run schema here:
    schema_path = os.path.join(os.path.dirname(__file__), "..", "sql", "schema.sql")
    # ensure banks exist in table
    ensure_banks_table(engine, BANK_NAMES)
    load_csv_and_insert(engine, CSV_PATH)
