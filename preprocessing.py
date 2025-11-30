import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from config import DATA_PATHS

class ReviewPreprocessor:
    def __init__(self, input_path=None, output_path=None):
        self.input_path = input_path or DATA_PATHS['raw_reviews']
        self.output_path = output_path or DATA_PATHS['processed_reviews']
        self.df = None
        self.stats = {}

    def load_data(self):
        print("Loading raw data...")
        try:
            self.df = pd.read_csv(self.input_path)
            print(f"Loaded {len(self.df)} reviews")
            self.stats['original_count'] = len(self.df)
            return True
        except FileNotFoundError:
            print(f"File not found: {self.input_path}")
            return False
        except Exception as e:
            print(f"Failed to load data: {e}")
            return False

    def check_missing_data(self):
        print("[1/6] Checking for missing data...")
        missing = self.df.isnull().sum()
        self.stats['missing_before'] = missing.to_dict()
        critical_cols = ['review_text', 'rating', 'bank_name']
        missing_critical = self.df[critical_cols].isnull().sum()
        if missing_critical.sum() > 0:
            print(f"Missing values in critical columns:\n{missing_critical}")

    def handle_missing_values(self):
        print("[2/6] Handling missing values...")
        critical_cols = ['review_text', 'rating', 'bank_name']
        before_count = len(self.df)
        self.df = self.df.dropna(subset=critical_cols)
        removed = before_count - len(self.df)
        if removed > 0:
            print(f"Removed {removed} rows with missing critical values")
        self.df['user_name'] = self.df['user_name'].fillna('Anonymous')
        self.df['thumbs_up'] = self.df['thumbs_up'].fillna(0)
        self.df['reply_content'] = self.df['reply_content'].fillna('')
        self.stats['rows_removed_missing'] = removed

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
            if pd.isna(text) or text == '':
                return ''
            text = str(text)
            text = re.sub(r'\s+', ' ', text)
            return text.strip()
        self.df['review_text'] = self.df['review_text'].apply(clean_review_text)
        before_count = len(self.df)
        self.df = self.df[self.df['review_text'].str.len() > 0]
        removed = before_count - len(self.df)
        if removed > 0:
            print(f"Removed {removed} reviews with empty text")
        self.df['text_length'] = self.df['review_text'].str.len()
        self.stats['empty_reviews_removed'] = removed

    def validate_ratings(self):
        print("[5/6] Validating ratings...")
        invalid = self.df[(self.df['rating'] < 1) | (self.df['rating'] > 5)]
        if len(invalid) > 0:
            print(f"Found {len(invalid)} invalid ratings")
            self.df = self.df[(self.df['rating'] >= 1) & (self.df['rating'] <= 5)]
        self.stats['invalid_ratings_removed'] = len(invalid)

    def prepare_final_output(self):
        print("[6/6] Preparing final output...")
        output_columns = [
            'review_id','review_text','rating','review_date',
            'review_year','review_month','bank_code','bank_name',
            'user_name','thumbs_up','text_length','source'
        ]
        output_columns = [col for col in output_columns if col in self.df.columns]
        self.df = self.df[output_columns].sort_values(['bank_code','review_date'], ascending=[True, False])
        self.df = self.df.reset_index(drop=True)

    def save_data(self):
        print("Saving processed data...")
        try:
            os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
            self.df.to_csv(self.output_path, index=False)
            print(f"Data saved to: {self.output_path}")
            self.stats['final_count'] = len(self.df)
            return True
        except Exception as e:
            print(f"Failed to save data: {e}")
            return False

    def process(self):
        print("Starting preprocessing pipeline...")
        if not self.load_data():
            return False
        self.check_missing_data()
        self.handle_missing_values()
        self.normalize_dates()
        self.clean_text()
        self.validate_ratings()
        self.prepare_final_output()
        if self.save_data():
            return True
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
