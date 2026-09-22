"""Centralized logging setup for the ETL pipeline."""

import logging
import os
from pathlib import Path


def get_logger(name: str, log_dir: str = "logs", log_file: str = "pipeline.log",
                level: str = "INFO") -> logging.Logger:
    """
    Create (or retrieve) a configured logger that writes to both console and file.

    Args:
        name: Logger name, typically __name__ of the calling module.
        log_dir: Directory to write the log file into (created if missing).
        log_file: Name of the log file.
        level: Logging level as a string (DEBUG, INFO, WARNING, ERROR).

    Returns:
        A configured logging.Logger instance.
    """
    Path(log_dir).mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    # Avoid duplicate handlers if get_logger is called multiple times
    if not logger.handlers:
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        file_handler = logging.FileHandler(os.path.join(log_dir, log_file))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
