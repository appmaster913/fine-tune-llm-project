def load_data(file_path):
    """Load data from a specified file path."""
    import pandas as pd
    return pd.read_csv(file_path)

def save_model(model, file_path):
    """Save the trained model to a specified file path."""
    import joblib
    joblib.dump(model, file_path)

def load_model(file_path):
    """Load a model from a specified file path."""
    import joblib
    return joblib.load(file_path)

def preprocess_text(text):
    """Preprocess the input text for model training."""
    import re
    text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace
    text = text.strip()  # Remove leading and trailing whitespace
    return text

def split_data(data, train_size=0.8):
    """Split the data into training and testing sets."""
    from sklearn.model_selection import train_test_split
    return train_test_split(data, train_size=train_size)