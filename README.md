# Bank Reviews Project - Task 1

## Overview
Collect, preprocess, and store Google Play reviews for three banks.

## Folder Structure
- data/raw: raw scraped reviews
- data/processed: cleaned CSV dataset
- src/scraping: scraping scripts
- src/preprocessing: data cleaning scripts
- src/utils: helper functions
- src/main.py: run full pipeline

## Steps
1. Scrape reviews: `python src/scraping/google_play_scraper.py`
2. Clean reviews: `python src/preprocessing/clean_reviews.py`
3. Or run full pipeline: `python src/main.py`

## Requirements
`pip install -r requirements.txt`
