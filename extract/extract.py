import pandas as pd
from config.settings import DATA_DIR, FILES

def load_csv(file_key):
    """Load CSV into Pandas DataFrame."""
    path = DATA_DIR / FILES[file_key]
    return pd.read_csv(path)

def extract_all():
    """Extract all raw files into a dictionary of DataFrames."""
    return {key: load_csv(key) for key in FILES}
