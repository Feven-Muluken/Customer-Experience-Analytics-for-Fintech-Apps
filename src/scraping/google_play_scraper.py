from google_play_scraper import reviews, Sort
import pandas as pd # pyright: ignore[reportMissingModuleSource]
import time

def scrape_reviews(apps, reviews_per_app=500):
    """
    Scrape reviews from Google Play Store.
    """
    all_reviews = []

    for bank, app_id in apps.items():
        print(f"\n🔍 Scraping reviews for: {bank} ({app_id})...")

        try:
            result, _ = reviews(
                app_id,
                lang='en',
                country='et',   # IMPORTANT: use Ethiopia store
                sort=Sort.NEWEST,
                count=reviews_per_app
            )
        except Exception as e:
            print(f"❌ Failed to scrape {bank}: {e}")
            continue

        print(f"➡ Found {len(result)} reviews")

        for r in result:
            all_reviews.append({
                "review": r.get("content", ""),
                "rating": r.get("score", None),
                "date": r.get("at", None),
                "bank": bank,
                "source": "Google Play"
            })

        # Avoid Play Store temporary blocking
        time.sleep(2)

    df = pd.DataFrame(all_reviews)
    return df


if __name__ == "__main__":
    bank_apps = {
       "CBE": "com.combanketh.mobilebanking",
       "Awash": "com.sc.awashpay",
       "AmharaBank": "com.amharabank.Aba_mobile_banking"
    }

    df_raw = scrape_reviews(bank_apps, reviews_per_app=300)

    # Ensure folder exists
    import os
    os.makedirs("data/raw", exist_ok=True)

    file_path = "data/raw/all_reviews_raw.csv"
    df_raw.to_csv(file_path, index=False)

    print(f"\n Saved raw reviews → {file_path}")
    print(f"Total reviews collected: {len(df_raw)}")
