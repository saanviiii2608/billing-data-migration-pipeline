import time
import requests
from src.logger import logger


def upload_record(record, api_url, timeout=30, retries=3, backoff_factor=2):
    for attempt in range(1, retries + 1):
        try:
            response = requests.post(api_url, json=record, timeout=timeout)
            if response.status_code == 200:
                return True
            logger.warning(
                f"Upload failed for customer {record.get('customer_id')}: "
                f"status {response.status_code} (attempt {attempt}/{retries})"
            )
        except requests.exceptions.Timeout:
            logger.warning(
                f"Timeout uploading customer {record.get('customer_id')} "
                f"(attempt {attempt}/{retries})"
            )
        except requests.exceptions.ConnectionError:
            logger.warning(
                f"Connection error uploading customer {record.get('customer_id')} "
                f"(attempt {attempt}/{retries})"
            )
        except requests.exceptions.RequestException as e:
            logger.error(
                f"Unexpected error uploading customer {record.get('customer_id')}: {e}"
            )
            return False

        if attempt < retries:
            wait = backoff_factor ** attempt
            logger.info(f"Retrying in {wait}s...")
            time.sleep(wait)

    logger.error(
        f"Failed to upload customer {record.get('customer_id')} after {retries} attempts"
    )
    return False


def upload_batch(records, api_url, timeout=30, retries=3, backoff_factor=2):
    results = {"success": [], "failed": []}
    for record in records:
        if upload_record(record, api_url, timeout, retries, backoff_factor):
            results["success"].append(record["customer_id"])
        else:
            results["failed"].append(record["customer_id"])
    return results
