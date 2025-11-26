# src/utils/logger.py
import logging
from logging import Logger
from pathlib import Path
import sys
from typing import Optional


def setup_logger(
    name: str = "kasparro",
    level: int = logging.INFO,
    logfile: str = "logs/app.log",
    console: bool = True,
) -> Logger:
    """
    Create and return a configured logger.

    - Creates logs directory if missing.
    - Adds a RotatingFileHandler-like simple file handler (no dependency).
    - Optionally adds console handler for immediate feedback.

    Usage:
        logger = setup_logger()
        logger.info("Started")
    """
    # Ensure logs directory exists
    p = Path(logfile).parent
    p.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid adding handlers multiple times if function called repeatedly
    if logger.handlers:
        return logger

    # File handler (simple)
    fh = logging.FileHandler(logfile, encoding="utf-8")
    fh.setLevel(level)
    fh_formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    fh.setFormatter(fh_formatter)
    logger.addHandler(fh)

    # Console handler
    if console:
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(level)
        ch_formatter = logging.Formatter("%(levelname)s: %(message)s")
        ch.setFormatter(ch_formatter)
        logger.addHandler(ch)

    # Make logger propagation False to avoid double logs
    logger.propagate = False
    return logger


# module-level default logger (easy import)
default_logger = setup_logger()
