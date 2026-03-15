import argparse
import sys

from src.config import load_config
from src.loader import load_data
from src.validator import validate_data, filter_valid_records
from src.transformer import transform_data
from src.api_client import upload_batch
from src.logger import logger


def main():
    parser = argparse.ArgumentParser(description="Billing Data Migration Pipeline")
    parser.add_argument(
        "--input", "-i",
        help="Path to input CSV file (overrides config.yaml)",
    )
    parser.add_argument(
        "--config", "-c",
        default="config.yaml",
        help="Path to config file (default: config.yaml)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and transform only, skip upload",
    )
    args = parser.parse_args()

    logger.info("Starting billing data migration pipeline")

    config = load_config(args.config)
    input_file = args.input or config["pipeline"]["input_file"]

    # Load
    df = load_data(input_file)

    # Validate
    errors, invalid_indices = validate_data(df)
    if errors:
        logger.info(f"Validation found {len(errors)} issue(s):")
        for error in errors:
            logger.info(f"  - {error}")

    # Filter out invalid records
    valid_df, rejected_df = filter_valid_records(df, invalid_indices)

    # Save rejected records
    if not rejected_df.empty:
        rejected_path = config["pipeline"]["rejected_file"]
        rejected_df.to_csv(rejected_path, index=False)
        logger.info(f"Rejected records saved to {rejected_path}")

    if valid_df.empty:
        logger.warning("No valid records to process. Exiting.")
        sys.exit(1)

    # Transform
    records = transform_data(valid_df)

    # Upload
    if args.dry_run:
        logger.info("Dry run mode — skipping upload")
    else:
        api_config = config["api"]
        results = upload_batch(
            records,
            api_url=api_config["url"],
            timeout=api_config["timeout"],
            retries=api_config["retries"],
            backoff_factor=api_config["backoff_factor"],
        )
        logger.info("Upload Summary:")
        logger.info(f"  Total valid records: {len(records)}")
        logger.info(f"  Uploaded successfully: {len(results['success'])}")
        logger.info(f"  Failed: {len(results['failed'])}")
        if results["failed"]:
            logger.warning(f"  Failed customer IDs: {results['failed']}")

    logger.info("Pipeline finished")


if __name__ == "__main__":
    main()
