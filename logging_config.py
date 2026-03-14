import logging
import os
from typing import NoReturn

def setup_logging() -> None:
    """
    Configure Python logging for the 5G Digital Twin Simulator.
    Logs are written to logs/simulator.log and also output to the console.
    Log level: INFO
    Log format: %(asctime)s | %(levelname)s | %(name)s | %(message)s
    Ensures the logs directory exists.
    """
    log_dir = "logs"
    log_file = os.path.join(log_dir, "simulator.log")
    os.makedirs(log_dir, exist_ok=True)
    log_format = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler(log_file, mode='a', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
