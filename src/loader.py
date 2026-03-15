import pandas as pd
from src.logger import logger

REQUIRED_COLUMNS = {"customer_id", "customer_name", "plan", "price", "usage"}


def load_data(file_path):
    logger.info(f"Loading dataset from {file_path}")
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"Input file not found: {file_path}")
    except pd.errors.EmptyDataError:
        logger.error(f"File is empty: {file_path}")
        raise ValueError(f"Input file is empty: {file_path}")

    missing_cols = REQUIRED_COLUMNS - set(df.columns)
    if missing_cols:
        logger.error(f"Missing required columns: {missing_cols}")
        raise ValueError(f"Missing required columns: {missing_cols}")

    logger.info(f"{len(df)} records loaded")
    return df
