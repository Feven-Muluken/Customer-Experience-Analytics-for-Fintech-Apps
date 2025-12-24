from .scraping.google_play_scraper import scrape_reviews
from .preprocessing.clean_reviews import clean_reviews


if __name__ == "__main__":
    # Step 1: Scrape reviews
    bank_apps = {
         "CBE": "com.combanketh.mobilebanking",
       "Awash": "com.sc.awashpay",
       "AmharaBank": "com.amharabank.Aba_mobile_banking"
    }
    df_raw = scrape_reviews(bank_apps)

    # Step 2: Save raw data
    df_raw.to_csv("data/raw/all_reviews_raw.csv", index=False)

    # Step 3: Clean data
    clean_reviews("data/raw/all_reviews_raw.csv",
                  "data/processed/all_reviews_clean.csv")
