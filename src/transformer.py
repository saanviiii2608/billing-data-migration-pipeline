import pandas as pd
from src.logger import logger


def transform_data(df):
    logger.info(f"Transforming {len(df)} records")
    try:
        records = []
        for row in df.to_dict(orient="records"):
            customer_name = row["customer_name"]
            if pd.isna(customer_name):
                customer_name = "Unknown Customer"

            record = {
                "customer_id": int(row["customer_id"]),
                "customer_name": customer_name,
                "subscription": {
                    "plan": row["plan"],
                    "price": float(row["price"]),
                },
                "usage": int(row["usage"]),
            }
            records.append(record)

        logger.info(f"Transformed {len(records)} records successfully")
        return records
    except KeyError as e:
        logger.error(f"Missing column during transformation: {e}")
        raise ValueError(f"Missing required column: {e}")
