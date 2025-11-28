# src/utils/retry.py
import time
import logging
from typing import Callable, Any, Tuple

logger = logging.getLogger("kasparro")

def retry(
    func: Callable,
    args: Tuple = (),
    kwargs: dict = None,
    retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 10.0,
    exceptions: Tuple = (Exception,),
) -> Any:
    """
    Simple retry with exponential backoff.

    Usage:
        from src.utils.retry import retry
        df = retry(pd.read_csv, args=(path,), kwargs={"encoding":"utf-8"}, retries=3)

    Parameters:
    - func: callable to run
    - args: positional args tuple
    - kwargs: keyword args dict
    - retries: number of retry attempts (default 3)
    - base_delay: initial backoff in seconds
    - max_delay: maximum backoff in seconds
    - exceptions: tuple of exception classes to catch and retry on
    """
    if kwargs is None:
        kwargs = {}

    attempt = 0
    while True:
        try:
            return func(*args, **kwargs)
        except exceptions as e:
            attempt += 1
            if attempt > retries:
                logger.error("Retry: all %d attempts failed for %s. Raising.", retries, getattr(func, "__name__", str(func)))
                raise
            wait = min(max_delay, base_delay * (2 ** (attempt - 1)))
            logger.warning("Retry attempt %d/%d for %s after error: %s. Waiting %.1fs",
                           attempt, retries, getattr(func, "__name__", str(func)), e, wait)
            time.sleep(wait)
