import logging

logging.basicConfig(
    filename="infrastructure/logs/logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)