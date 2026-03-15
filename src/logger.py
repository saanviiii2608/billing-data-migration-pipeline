import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("migration.log"),
        logging.StreamHandler(sys.stdout),
    ],
)

logger = logging.getLogger("billing_pipeline")
