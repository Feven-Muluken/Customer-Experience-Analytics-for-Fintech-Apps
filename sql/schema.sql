DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS banks;

CREATE TABLE banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name VARCHAR(100) NOT NULL,
    app_id VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE reviews (
    review_id SERIAL PRIMARY KEY,
    bank_id INTEGER REFERENCES banks(bank_id) ON DELETE CASCADE,
    review_text TEXT,
    rating INT,
    review_date TIMESTAMP,
    sentiment_label VARCHAR(10),
    sentiment_score FLOAT,
    source VARCHAR(50)
);
