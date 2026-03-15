from src.loader import load_data
from src.validator import validate_data
from src.transformer import transform_data
from src.api_client import upload_record
from src.logger import logger


logger.info("Starting billing data migration pipeline")

df = load_data("data/customers.csv")

errors = validate_data(df)

logger.info("Validation completed")

records = transform_data(df)

success = 0

for record in records:

    if upload_record(record):
        success += 1
        logger.info(f"Uploaded customer {record['customer_id']}")


print("\nUpload Summary")

print("Total records:", len(records))
print("Uploaded successfully:", success)

logger.info("Pipeline finished successfully")