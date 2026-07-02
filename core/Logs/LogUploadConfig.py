import logging

logging.basicConfig(
    filename="infrastructure/logs/uploads_logs.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)