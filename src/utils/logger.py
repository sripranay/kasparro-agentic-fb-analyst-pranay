# src/utils/logger.py
"""
Robust logger for the project.

Features:
- Console + rotating file handler
- ISO timestamps
- Optional debug_mode (set via config)
- get_logger(name) to use per-module loggers
- tail_log(file, lines) helper for quick checks (returns last n lines)
"""

import logging
import logging.handlers
import os
from datetime import datetime
from typing import Optional, List

LOG_DIR = os.getenv("KASPARRO_LOG_DIR", "logs")
LOG_FILE = os.path.join(LOG_DIR, "run.log")
MAX_BYTES = 5 * 1024 * 1024  # 5 MB
BACKUP_COUNT = 5


def ensure_log_dir():
    os.makedirs(LOG_DIR, exist_ok=True)


def configure_root_logger(level: int = logging.INFO, console: bool = True):
    """
    Configure root logger. Safe to call multiple times.
    """
    ensure_log_dir()

    root = logging.getLogger()
    if root.handlers:
        # already configured - avoid duplicate handlers
        return

    root.setLevel(level)

    fmt = "%(asctime)s | %(levelname)-5s | %(name)s | %(message)s"
    datefmt = "%Y-%m-%dT%H:%M:%SZ"

    # Rotating file handler
    file_handler = logging.handlers.RotatingFileHandler(
        LOG_FILE, maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT, encoding="utf-8"
    )
    file_formatter = logging.Formatter(fmt, datefmt=datefmt)
    file_handler.setFormatter(file_formatter)
    root.addHandler(file_handler)

    # Console handler
    if console:
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter(fmt, datefmt=datefmt)
        console_handler.setFormatter(console_formatter)
        root.addHandler(console_handler)


def get_logger(name: Optional[str] = None, level: Optional[int] = None) -> logging.Logger:
    """
    Returns a named logger. Call configure_root_logger() once during app start.
    """
    if not logging.getLogger().handlers:
        # default configure if user forgot to call configure_root_logger
        configure_root_logger()

    logger = logging.getLogger(name)
    if level is not None:
        logger.setLevel(level)
    return logger


def tail_log(path: Optional[str] = None, lines: int = 50) -> List[str]:
    """
    Return the last `lines` lines from path (or default LOG_FILE).
    Returns list of strings (lines). Safe if file doesn't exist.
    """
    path = path or LOG_FILE
    if not os.path.exists(path):
        return []
    with open(path, "rb") as fh:
        fh.seek(0, os.SEEK_END)
        end = fh.tell()
        block_size = 1024
        data = b""
        while end > 0 and data.count(b"\n") <= lines:
            read_size = min(block_size, end)
            fh.seek(end - read_size, os.SEEK_SET)
            data = fh.read(read_size) + data
            end -= read_size
        # decode and split
        text = data.decode("utf-8", errors="ignore")
        return text.strip().splitlines()[-lines:]


# Small convenience for quick CLI usage
if __name__ == "__main__":
    configure_root_logger()
    logger = get_logger("logger-test")
    logger.info("Logger initialized")
    print("--- last 10 log lines ---")
    for l in tail_log(lines=10):
        print(l)
