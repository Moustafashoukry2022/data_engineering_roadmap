import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"

def setup_logging_config():
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.DEBUG,
        filename=LOG_DIR / "pipeline.log",
        filemode="w",
        format="%(asctime)s | %(filename)s | %(levelname)s | %(message)s"
    )