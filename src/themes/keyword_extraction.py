# src/themes/keyword_extraction.py
import pandas as pd # pyright: ignore[reportMissingModuleSource]
import re
from sklearn.feature_extraction.text import TfidfVectorizer # pyright: ignore[reportMissingModuleSource]
from collections import Counter
import spacy # pyright: ignore[reportMissingImports]

nlp = spacy.load("en_core_web_sm")

def simple_clean(text):
    text = str(text).lower()
    text = re.sub(r'http\S+|www.\S+', '', text)
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def top_n_keywords_by_bank(df, n=30):
    results = {}
    for bank, group in df.groupby('bank'):
        texts = group['review'].fillna("").map(simple_clean).tolist()
        # use TF-IDF on bank texts
        vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1,2), max_features=1000)
        X = vectorizer.fit_transform(texts)
        # sum tfidf scores for each feature
        scores = X.sum(axis=0).A1
        features = vectorizer.get_feature_names_out()
        feat_scores = list(zip(features, scores))
        feat_scores.sort(key=lambda x: x[1], reverse=True)
        results[bank] = feat_scores[:n]
    return results

if __name__ == "__main__":
    df = pd.read_csv("data/processed/all_reviews_clean.csv")
    keywords = top_n_keywords_by_bank(df, n=50)
    # save per bank
    for bank, items in keywords.items():
        pd.DataFrame(items, columns=["keyword", "tfidf"]).to_csv(f"data/processed/{bank}_keywords.csv", index=False)
        print(bank, "-> saved top keywords")
