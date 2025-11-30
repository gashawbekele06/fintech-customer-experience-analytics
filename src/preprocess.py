<<<<<<< HEAD:src/preprocess.py
import sys
import os
from pathlib import Path

# Ensure src directory is on sys.path so imports like `from config import ...` work
SRC_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SRC_DIR.parent
sys.path.insert(0, str(SRC_DIR))

import pandas as pd
import numpy as np
from datetime import datetime
import re

# Import config from src/config.py
from config import DATA_PATHS

# Resolve DATA_PATHS relative to project root if they are not absolute
for key, val in list(DATA_PATHS.items()):
    p = Path(val)
    if not p.is_absolute():
        DATA_PATHS[key] = str((PROJECT_ROOT / p).resolve())
    else:
        DATA_PATHS[key] = str(p.resolve())


=======
import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from config import DATA_PATHS

>>>>>>> 51e74fa8169188e17a83164d9041c5485e778056:preprocessing.py
class ReviewPreprocessor:
    def __init__(self, input_path=None, output_path=None):
        self.input_path = input_path or DATA_PATHS['raw_reviews']
        self.output_path = output_path or DATA_PATHS['processed_reviews']
        self.df = None
        self.stats = {}

    def load_data(self):
<<<<<<< HEAD:src/preprocess.py
        """Load raw reviews data"""
=======
>>>>>>> 51e74fa8169188e17a83164d9041c5485e778056:preprocessing.py
        print("Loading raw data...")
        try:
            self.df = pd.read_csv(self.input_path)
            print(f"Loaded {len(self.df)} reviews")
            self.stats['original_count'] = len(self.df)
            return True
        except FileNotFoundError:
<<<<<<< HEAD:src/preprocess.py
            print(f"ERROR: File not found: {self.input_path}")
            return False
        except Exception as e:
            print(f"ERROR: Failed to load data: {str(e)}")
            return False

    def check_missing_data(self):
        """Check for missing data"""
        print("\n[1/6] Checking for missing data...")
        missing = self.df.isnull().sum()
        missing_pct = (missing / len(self.df)) * 100
        print("\nMissing values:")
        for col in missing.index:
            if missing[col] > 0:
                print(f"  {col}: {missing[col]} ({missing_pct[col]:.2f}%)")

=======
            print(f"File not found: {self.input_path}")
            return False
        except Exception as e:
            print(f"Failed to load data: {e}")
            return False

    def check_missing_data(self):
        print("[1/6] Checking for missing data...")
        missing = self.df.isnull().sum()
>>>>>>> 51e74fa8169188e17a83164d9041c5485e778056:preprocessing.py
        self.stats['missing_before'] = missing.to_dict()
        critical_cols = ['review_text', 'rating', 'bank_name']
        missing_critical = self.df[critical_cols].isnull().sum()
        if missing_critical.sum() > 0:
<<<<<<< HEAD:src/preprocess.py
            print("\nWARNING: Missing values in critical columns:")
            print(missing_critical[missing_critical > 0])

    def handle_missing_values(self):
        """Handle missing values"""
        print("\n[2/6] Handling missing values...")
=======
            print(f"Missing values in critical columns:\n{missing_critical}")

    def handle_missing_values(self):
        print("[2/6] Handling missing values...")
>>>>>>> 51e74fa8169188e17a83164d9041c5485e778056:preprocessing.py
        critical_cols = ['review_text', 'rating', 'bank_name']
        before_count = len(self.df)
        self.df = self.df.dropna(subset=critical_cols)
        removed = before_count - len(self.df)
        if removed > 0:
            print(f"Removed {removed} rows with missing critical values")
<<<<<<< HEAD:src/preprocess.py

=======
>>>>>>> 51e74fa8169188e17a83164d9041c5485e778056:preprocessing.py
        self.df['user_name'] = self.df['user_name'].fillna('Anonymous')
        self.df['thumbs_up'] = self.df['thumbs_up'].fillna(0)
        self.df['reply_content'] = self.df['reply_content'].fillna('')
        self.stats['rows_removed_missing'] = removed
<<<<<<< HEAD:src/preprocess.py
        self.stats['count_after_missing'] = len(self.df)

    def normalize_dates(self):
        """Normalize date formats to YYYY-MM-DD"""
        print("\n[3/6] Normalizing dates...")
        try:
            self.df['review_date'] = pd.to_datetime(self.df['review_date'])
            self.df['review_date'] = self.df['review_date'].dt.date
            self.df['review_year'] = pd.to_datetime(self.df['review_date']).dt.year
            self.df['review_month'] = pd.to_datetime(self.df['review_date']).dt.month
            print(f"Date range: {self.df['review_date'].min()} to {self.df['review_date'].max()}")
        except Exception as e:
            print(f"WARNING: Error normalizing dates: {str(e)}")

    def clean_text(self):
        """Clean review text"""
        print("\n[4/6] Cleaning text...")

        def clean_review_text(text):
            """Inner function to clean individual review text strings"""
=======

    def normalize_dates(self):
        print("[3/6] Normalizing dates...")
        try:
            self.df['review_date'] = pd.to_datetime(self.df['review_date'], errors='coerce')
            self.df['review_date'] = self.df['review_date'].dt.date
            self.df['review_year'] = pd.to_datetime(self.df['review_date']).dt.year
            self.df['review_month'] = pd.to_datetime(self.df['review_date']).dt.month
        except Exception as e:
            print(f"Error normalizing dates: {e}")

    def clean_text(self):
        print("[4/6] Cleaning text...")
        def clean_review_text(text):
>>>>>>> 51e74fa8169188e17a83164d9041c5485e778056:preprocessing.py
            if pd.isna(text) or text == '':
                return ''
            text = str(text)
            text = re.sub(r'\s+', ' ', text)
<<<<<<< HEAD:src/preprocess.py
            text = text.strip()
            return text

        self.df['review_text'] = self.df['review_text'].apply(clean_review_text)

=======
            return text.strip()
        self.df['review_text'] = self.df['review_text'].apply(clean_review_text)
>>>>>>> 51e74fa8169188e17a83164d9041c5485e778056:preprocessing.py
        before_count = len(self.df)
        self.df = self.df[self.df['review_text'].str.len() > 0]
        removed = before_count - len(self.df)
        if removed > 0:
            print(f"Removed {removed} reviews with empty text")
<<<<<<< HEAD:src/preprocess.py

        self.df['text_length'] = self.df['review_text'].str.len()

=======
        self.df['text_length'] = self.df['review_text'].str.len()
>>>>>>> 51e74fa8169188e17a83164d9041c5485e778056:preprocessing.py
        self.stats['empty_reviews_removed'] = removed

    def validate_ratings(self):
<<<<<<< HEAD:src/preprocess.py
        """Validate rating values (should be 1-5)"""
        print("\n[5/6] Validating ratings...")
        invalid = self.df[(self.df['rating'] < 1) | (self.df['rating'] > 5)]
        if len(invalid) > 0:
            print(f"WARNING: Found {len(invalid)} reviews with invalid ratings")
            self.df = self.df[(self.df['rating'] >= 1) & (self.df['rating'] <= 5)]
        else:
            print("All ratings are valid (1-5)")

        self.stats['invalid_ratings_removed'] = len(invalid)

    def prepare_final_output(self):
        """Prepare final output format"""
        print("\n[6/6] Preparing final output...")

=======
        print("[5/6] Validating ratings...")
        invalid = self.df[(self.df['rating'] < 1) | (self.df['rating'] > 5)]
        if len(invalid) > 0:
            print(f"Found {len(invalid)} invalid ratings")
            self.df = self.df[(self.df['rating'] >= 1) & (self.df['rating'] <= 5)]
        self.stats['invalid_ratings_removed'] = len(invalid)

    def prepare_final_output(self):
        print("[6/6] Preparing final output...")
>>>>>>> 51e74fa8169188e17a83164d9041c5485e778056:preprocessing.py
        output_columns = [
            'review_id','review_text','rating','review_date',
            'review_year','review_month','bank_code','bank_name',
            'user_name','thumbs_up','text_length','source'
        ]
        output_columns = [col for col in output_columns if col in self.df.columns]
<<<<<<< HEAD:src/preprocess.py
        self.df = self.df[output_columns]
        self.df = self.df.sort_values(['bank_code', 'review_date'], ascending=[True, False])
        self.df = self.df.reset_index(drop=True)
        print(f"Final dataset: {len(self.df)} reviews")

    def save_data(self):
        """Save processed data"""
        print("\nSaving processed data...")

=======
        self.df = self.df[output_columns].sort_values(['bank_code','review_date'], ascending=[True, False])
        self.df = self.df.reset_index(drop=True)

    def save_data(self):
        print("Saving processed data...")
>>>>>>> 51e74fa8169188e17a83164d9041c5485e778056:preprocessing.py
        try:
            os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
            self.df.to_csv(self.output_path, index=False)
            print(f"Data saved to: {self.output_path}")
<<<<<<< HEAD:src/preprocess.py

            self.stats['final_count'] = len(self.df)
            return True
        except Exception as e:
            print(f"ERROR: Failed to save data: {str(e)}")
            return False

    def generate_report(self):
        """Generate preprocessing report"""
        print("\n" + "=" * 60)
        print("PREPROCESSING REPORT")
        print("=" * 60)
        print(f"\nOriginal records: {self.stats.get('original_count', 0)}")
        print(f"Records with missing critical data: {self.stats.get('rows_removed_missing', 0)}")
        print(f"Empty reviews removed: {self.stats.get('empty_reviews_removed', 0)}")
        print(f"Invalid ratings removed: {self.stats.get('invalid_ratings_removed', 0)}")
        print(f"Final records: {self.stats.get('final_count', 0)}")
        if self.stats.get('original_count', 0) > 0:
            retention_rate = (self.stats.get('final_count', 0) / self.stats.get('original_count', 1)) * 100
            error_rate = 100 - retention_rate
            print(f"\nData retention rate: {retention_rate:.2f}%")
            print(f"Data error rate: {error_rate:.2f}%")

            if error_rate < 5:
                print("✓ Data quality: EXCELLENT (<5% errors)")
            elif error_rate < 10:
                print("✓ Data quality: GOOD (<10% errors)")
            else:
                print("⚠ Data quality: NEEDS ATTENTION (>10% errors)")
        if self.df is not None:
            print("\nReviews per bank:")
            bank_counts = self.df['bank_name'].value_counts()
            for bank, count in bank_counts.items():
                print(f"  {bank}: {count}")
            print("\nRating distribution:")
            rating_counts = self.df['rating'].value_counts().sort_index(ascending=False)
            for rating, count in rating_counts.items():
                pct = (count / len(self.df)) * 100
                print(f"  {'⭐' * int(rating)}: {count} ({pct:.1f}%)")
            print(f"\nDate range: {self.df['review_date'].min()} to {self.df['review_date'].max()}")
            print(f"\nText statistics:")
            print(f"  Average length: {self.df['text_length'].mean():.0f} characters")
            print(f"  Median length: {self.df['text_length'].median():.0f} characters")
            print(f"  Min length: {self.df['text_length'].min()}")
            print(f"  Max length: {self.df['text_length'].max()}")

    def process(self):
        """Run complete preprocessing pipeline"""
        print("=" * 60)
        print("STARTING DATA PREPROCESSING")
        print("=" * 60)
=======
            self.stats['final_count'] = len(self.df)
            return True
        except Exception as e:
            print(f"Failed to save data: {e}")
            return False

    def process(self):
        print("Starting preprocessing pipeline...")
>>>>>>> 51e74fa8169188e17a83164d9041c5485e778056:preprocessing.py
        if not self.load_data():
            return False
        self.check_missing_data()
        self.handle_missing_values()
        self.normalize_dates()
        self.clean_text()
        self.validate_ratings()
        self.prepare_final_output()
<<<<<<< HEAD:src/preprocess.py

=======
>>>>>>> 51e74fa8169188e17a83164d9041c5485e778056:preprocessing.py
        if self.save_data():
            return True
<<<<<<< HEAD:src/preprocess.py

        return False


def main():
    """Main execution function"""
    preprocessor = ReviewPreprocessor()
    success = preprocessor.process()
    if success:
        print("\n✓ Preprocessing completed successfully!")
        return preprocessor.df
    else:
        print("\n✗ Preprocessing failed!")
        return None


if __name__ == "__main__":
    processed_df = main()
=======
        return False

# --------------------------------------------------
# Example Usage
# --------------------------------------------------
if __name__ == "__main__":
    preprocessor = ReviewPreprocessor()
    if preprocessor.process():
        print("Preprocessing completed successfully!")
        # If you have plot_review_stats defined, you can call it here
        # preprocessor.plot_review_stats()
    else:
        print("Preprocessing failed.")
>>>>>>> 51e74fa8169188e17a83164d9041c5485e778056:preprocessing.py
