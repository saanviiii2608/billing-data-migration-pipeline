import pandas as pd

def load_data(file_path):

    print("Loading dataset...")

    df = pd.read_csv(file_path)

    print(f"{len(df)} records loaded")

    return df