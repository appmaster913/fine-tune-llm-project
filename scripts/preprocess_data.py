import pandas as pd
import os

def preprocess_data(raw_data_path, processed_data_path):
    # Load raw data
    raw_data = pd.read_csv(raw_data_path)

    # Example preprocessing steps
    # 1. Remove duplicates
    raw_data.drop_duplicates(inplace=True)

    # 2. Fill missing values
    raw_data.fillna(method='ffill', inplace=True)

    # 3. Convert text to lowercase
    raw_data['text_column'] = raw_data['text_column'].str.lower()

    # Save processed data
    os.makedirs(os.path.dirname(processed_data_path), exist_ok=True)
    raw_data.to_csv(processed_data_path, index=False)

if __name__ == "__main__":
    raw_data_path = 'data/raw/customer_data.csv'  # Update with actual raw data path
    processed_data_path = 'data/processed/processed_customer_data.csv'  # Update with desired processed data path
    preprocess_data(raw_data_path, processed_data_path)