import logging, sys
from logging.handlers import RotatingFileHandler

def setup_logging():
    fmt = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    logging.basicConfig(
        level=logging.INFO,
        format=fmt,
        handlers=[
            logging.StreamHandler(sys.stdout),
            RotatingFileHandler("app.log", maxBytes=2_000_000, backupCount=3, encoding="utf-8")
        ],
    )
    return logging.getLogger("job-aggregator")