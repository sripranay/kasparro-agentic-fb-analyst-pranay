# src/utils/logger.py
import logging
from logging import Logger
from pathlib import Path
import sys
import json
import time
from typing import Optional, Callable, Any, Dict
from contextlib import contextmanager

LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
DEFAULT_LOGFILE = LOG_DIR / "app.log"


def setup_logger(
    name: str = "kasparro",
    level: int = logging.INFO,
    logfile: str = str(DEFAULT_LOGFILE),
    console: bool = True,
) -> Logger:
    """
    Configure and return a logger. Idempotent (safe to call multiple times).
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if logger.handlers:
        return logger

    # File handler
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

    logger.propagate = False
    return logger


# default logger for easy import
logger = setup_logger()


# --- convenience helpers for agent observability ----------------------------

def agent_log_start(agent_name: str, details: Optional[Dict[str, Any]] = None) -> None:
    """Log an agent start with optional details dict."""
    msg = f"AGENT_START | {agent_name}"
    if details:
        try:
            msg += " | " + json.dumps(details, default=str)
        except Exception:
            msg += " | (details unavailable)"
    logger.info(msg)


def agent_log_end(agent_name: str, details: Optional[Dict[str, Any]] = None) -> None:
    """Log an agent end with optional details dict."""
    msg = f"AGENT_END   | {agent_name}"
    if details:
        try:
            msg += " | " + json.dumps(details, default=str)
        except Exception:
            msg += " | (details unavailable)"
    logger.info(msg)


@contextmanager
def timed_agent(agent_name: str, details: Optional[Dict[str, Any]] = None):
    """Context manager to measure agent execution time and log start/end."""
    start = time.time()
    agent_log_start(agent_name, details)
    try:
        yield
    except Exception as e:
        logger.exception(f"AGENT_ERROR | {agent_name} | {e}")
        raise
    finally:
        duration = time.time() - start
        agent_log_end(agent_name, {"duration_s": round(duration, 3)})
