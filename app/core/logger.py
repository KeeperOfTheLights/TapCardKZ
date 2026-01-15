import os
import sys
import logging
from logging.handlers import RotatingFileHandler

from app.core.config import config

LOG_DIR: str = config.LOG_DIR
os.makedirs(LOG_DIR, exist_ok=True)

formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")

console_handler: logging.Handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

file_handler: logging.Handler = RotatingFileHandler(
    os.path.join(LOG_DIR, "app.log"),
    maxBytes=5*1024*1024,
    backupCount=5
)
file_handler.setFormatter(formatter)


error_handler: RotatingFileHandler = RotatingFileHandler(
    os.path.join(LOG_DIR, "errors.log"),
    maxBytes=5*1024*1024,
    backupCount=5
)
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)

logger: logging.Logger = logging.getLogger("taply")
logger.setLevel(logging.INFO)
logger.addHandler(console_handler)
logger.addHandler(file_handler)
logger.addHandler(error_handler)
