import logging

logging.basicConfig(
    filename="app/infrastructure/logs/db_save.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)