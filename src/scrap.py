<<<<<<< HEAD:src/scrap.py
import sys
import os
from pathlib import Path

# --- Adjust paths for new project layout ---
# Assume this script will live in the project root (or run from root).
# Project root contains `src/` and `notebooks/`. Ensure `src` is on sys.path
BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"
sys.path.insert(0, str(SRC_DIR))

from google_play_scraper import app, Sort, reviews_all, reviews
=======
"""
Google Play Store Review Scraper
Task: Collect reviews, ratings, dates, and app names for three banks.
Target: 400+ reviews per bank (≈1200 total).
"""

import os
import time
>>>>>>> 51e74fa8169188e17a83164d9041c5485e778056:scraper.py
import pandas as pd
from datetime import datetime
from tqdm import tqdm
<<<<<<< HEAD:src/scrap.py

# Import config from src/config.py
from config import APP_IDS, BANK_NAMES, SCRAPING_CONFIG, DATA_PATHS

# If DATA_PATHS entries are relative, resolve them relative to project root
for key, val in list(DATA_PATHS.items()):
    p = Path(val)
    if not p.is_absolute():
        DATA_PATHS[key] = str((BASE_DIR / p).resolve())
    else:
        DATA_PATHS[key] = str(p.resolve())

=======
from google_play_scraper import app, Sort, reviews

# --------------------------------------------------
# Configuration
# --------------------------------------------------
>>>>>>> 51e74fa8169188e17a83164d9041c5485e778056:scraper.py

BANKS = {
    "CBE": {
        "name": "Commercial Bank of Ethiopia",
        "app_id": "com.combanketh.mobilebanking"
    },
    "Awash": {
        "name": "Awash Bank",
        "app_id": "com.sc.awashpay"
    },
    "Amharabank": {
        "name": "Amharabank",
        "app_id": "com.amharabank.Aba_mobile_banking"
    }
}

REVIEWS_PER_BANK = 400
MAX_RETRIES = 3
LANG = "en"
COUNTRY = "et"
DELAY = 2  # seconds between banks

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "raw")
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "reviews_raw.csv")
APP_INFO_FILE = os.path.join(OUTPUT_DIR, "app_info.csv")

# --------------------------------------------------
# Scraper Functions
# --------------------------------------------------

def get_app_info(app_id, bank_code, bank_name):
    """Fetch app metadata (rating, installs, etc.)."""
    try:
        result = app(app_id, lang=LANG, country=COUNTRY)
        return {
            "bank_code": bank_code,
            "bank_name": bank_name,
            "app_id": app_id,
            "title": result.get("title", "N/A"),
            "score": result.get("score", 0),
            "ratings": result.get("ratings", 0),
            "reviews": result.get("reviews", 0),
            "installs": result.get("installs", "N/A"),
        }
    except Exception as e:
        print(f"Error fetching app info for {bank_name}: {e}")
        return None

def scrape_reviews(app_id, bank_code, bank_name, count=400):
    """Scrape reviews for a specific app with retry logic."""
    print(f"Scraping reviews for {bank_name} ({app_id})...")
    for attempt in range(MAX_RETRIES):
        try:
            result, _ = reviews(
                app_id,
                lang=LANG,
                country=COUNTRY,
                sort=Sort.NEWEST,
                count=count,
                filter_score_with=None,
            )
            print(f"Collected {len(result)} reviews for {bank_name}")
            return result
        except Exception as e:
            print(f"Attempt {attempt+1} failed for {bank_name}: {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(5)
            else:
                print(f"Failed to scrape {bank_name} after {MAX_RETRIES} attempts")
                return []
    return []

def process_reviews(reviews_data, bank_code, bank_name):
    """Format raw reviews into structured dictionaries."""
    processed = []
    for review in reviews_data:
        processed.append({
            "review_id": review.get("reviewId", ""),
            "review_text": review.get("content", ""),
            "rating": review.get("score", 0),
            "review_date": review.get("at", datetime.now()),
            "user_name": review.get("userName", "Anonymous"),
            "thumbs_up": review.get("thumbsUpCount", 0),
            "reply_content": review.get("replyContent", None),
            "bank_code": bank_code,
            "bank_name": bank_name,
            "app_version": review.get("reviewCreatedVersion", "N/A"),
            "source": "Google Play",
        })
    return processed

# --------------------------------------------------
# Main Execution
# --------------------------------------------------

def main():
    all_reviews = []
    app_info_list = []

    print("Starting Google Play Store Review Scraper...")

    # Phase 1: App Info
    for code, bank in BANKS.items():
        info = get_app_info(bank["app_id"], code, bank["name"])
        if info:
            app_info_list.append(info)

    if app_info_list:
        pd.DataFrame(app_info_list).to_csv(APP_INFO_FILE, index=False)
        print(f"App info saved to {APP_INFO_FILE}")

    # Phase 2: Reviews
    for code, bank in tqdm(BANKS.items(), desc="Banks"):
        reviews_data = scrape_reviews(bank["app_id"], code, bank["name"], REVIEWS_PER_BANK)
        if reviews_data:
            processed = process_reviews(reviews_data, code, bank["name"])
            all_reviews.extend(processed)
        time.sleep(DELAY)

    # Phase 3: Save
    if all_reviews:
        df = pd.DataFrame(all_reviews)
        df.drop_duplicates(subset=["review_id"], inplace=True)
        df.to_csv(OUTPUT_FILE, index=False)
        print(f"Scraping complete. Total reviews collected: {len(df)}")
        print(f"Data saved to {OUTPUT_FILE}")
    else:
        print("No reviews collected!")

if __name__ == "__main__":
    main()
