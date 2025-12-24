# src/themes/theme_clustering.py
import pandas as pd # pyright: ignore[reportMissingModuleSource]
import re

THEME_RULES = {
    "Account Access Issues": [r"login", r"sign in", r"password", r"otp", r"can't access", r"account locked"],
    "Transaction Performance": [r"transfer", r"transaction", r"payment", r"failed transaction", r"timeout"],
    "User Interface & Experience": [r"ui", r"interface", r"navigation", r"slow", r"design", r"easy to use"],
    "Customer Support": [r"support", r"customer service", r"call center", r"help", r"response"],
    "Feature Requests": [r"dark mode", r"fingerprint", r"biometric", r"offline", r"statement"]
}

def assign_themes_to_review(text):
    text = str(text).lower()
    matched = set()
    for theme, patterns in THEME_RULES.items():
        for p in patterns:
            if re.search(p, text):
                matched.add(theme)
                break
    return list(matched)

def apply_themes_to_df(input_csv="data/processed/all_reviews_clean.csv", output_csv="data/processed/all_reviews_with_themes.csv"):
    df = pd.read_csv(input_csv)
    df['themes'] = df['review'].fillna("").apply(assign_themes_to_review)
    df.to_csv(output_csv, index=False)
    print("Saved themes to", output_csv)

if __name__ == "__main__":
    apply_themes_to_df()
