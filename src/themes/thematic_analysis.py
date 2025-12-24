# -------------------------------------------
# THEMATIC ANALYSIS PIPELINE
# -------------------------------------------

import pandas as pd # pyright: ignore[reportMissingModuleSource]
import re
import os
from sklearn.feature_extraction.text import TfidfVectorizer # pyright: ignore[reportMissingModuleSource]

# Load preprocessed reviews
df = pd.read_csv("data/processed/all_reviews_clean.csv")

# -------------------------------------------------
# 1. BASIC TEXT CLEANING
# -------------------------------------------------
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"[^a-zA-Z0-9 ]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text

df["clean_text"] = df["review"].apply(clean_text)

# -------------------------------------------------
# 2. TF-IDF KEYWORD EXTRACTION
# -------------------------------------------------
vectorizer = TfidfVectorizer(
    max_df=0.8,
    min_df=5,
    ngram_range=(1, 2),    # unigrams & bigrams
    stop_words="english"
)

tfidf_matrix = vectorizer.fit_transform(df["clean_text"])
feature_names = vectorizer.get_feature_names_out()

def extract_top_keywords(tfidf_vec, feature_names, top_n=5):
    sorted_indices = tfidf_vec.toarray()[0].argsort()[::-1]
    top_features = [feature_names[i] for i in sorted_indices[:top_n]]
    return ", ".join(top_features)

df["keywords"] = [extract_top_keywords(tfidf_matrix[i], feature_names) for i in range(len(df))]

# -------------------------------------------------
# 3. RULE-BASED THEME ASSIGNMENT
# -------------------------------------------------

THEMES = {
    "Login & Access Issues": [
        "login", "log in", "password", "pin", "verification", "otp", "access", "account locked"
    ],
    "Transaction Problems": [
        "transfer", "transaction", "failed", "deducted", "not received", "delay"
    ],
    "App Performance / Speed": [
        "slow", "freeze", "crash", "loading", "hang", "lag"
    ],
    "User Interface / UX": [
        "interface", "design", "layout", "navigation", "button"
    ],
    "Customer Support": [
        "support", "help", "customer", "service", "call"
    ]
}

def assign_theme(text):
    text = text.lower()
    assigned = []

    for theme, keywords in THEMES.items():
        for kw in keywords:
            if kw in text:
                assigned.append(theme)
                break

    if not assigned:
        return "Other"

    return ", ".join(assigned)

df["theme"] = df["clean_text"].apply(assign_theme)

# -------------------------------------------------
# 4. SAVE RESULTS
# -------------------------------------------------

os.makedirs("data/themes", exist_ok=True)
output_path = "data/themes/thematic_results.csv"

df.to_csv(output_path, index=False)

print("\n✓ THEMATIC ANALYSIS COMPLETE!")
print(f"Saved results → {output_path}")

# -------------------------------------------------
# 5. SHOW SUMMARY BY BANK
# -------------------------------------------------

summary = df.groupby(["bank", "theme"]).size().reset_index(name="count")
print("\n--- THEME COUNTS PER BANK ---")
print(summary)
