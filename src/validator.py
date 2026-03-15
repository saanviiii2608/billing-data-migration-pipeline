import pandas as pd
from src.logger import logger


def validate_data(df):
    errors = []
    invalid_indices = set()

    # Check for missing customer names
    missing_names = df[df["customer_name"].isnull()]
    if not missing_names.empty:
        ids = missing_names["customer_id"].tolist()
        errors.append(f"Missing customer names for IDs: {ids}")
        invalid_indices.update(missing_names.index)
        logger.warning(f"Missing customer names found for IDs: {ids}")

    # Check for negative usage
    negative_usage = df[df["usage"] < 0]
    if not negative_usage.empty:
        ids = negative_usage["customer_id"].tolist()
        errors.append(f"Negative usage values for IDs: {ids}")
        invalid_indices.update(negative_usage.index)
        logger.warning(f"Negative usage found for IDs: {ids}")

    # Check for duplicate customer IDs
    duplicates = df[df.duplicated("customer_id", keep=False)]
    if not duplicates.empty:
        dup_ids = duplicates["customer_id"].unique().tolist()
        errors.append(f"Duplicate customer IDs: {dup_ids}")
        dup_rows = df[df.duplicated("customer_id", keep="first")]
        invalid_indices.update(dup_rows.index)
        logger.warning(f"Duplicate customer IDs detected: {dup_ids}")

    return errors, invalid_indices


def filter_valid_records(df, invalid_indices):
    valid_df = df.drop(index=invalid_indices)
    rejected_df = df.loc[list(invalid_indices)]
    logger.info(f"Validation: {len(valid_df)} valid, {len(rejected_df)} rejected")
    return valid_df, rejected_df
