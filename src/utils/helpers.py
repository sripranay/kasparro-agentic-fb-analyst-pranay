# src/utils/helpers.py
"""
General helpers used across agents:
- load_config
- ensure_dir
- save_json, load_json
- iso_utc_now
- validate_schema (lightweight)
- small backoff helper (calls retry.retry if you have that module)
"""

import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from pathlib import Path
from pprint import pformat

# Try to import project retry utility if present (you said you added retry.py)
try:
    from src.utils.retry import retry_on_exception  # type: ignore
except Exception:
    # fallback no-op decorator
    def retry_on_exception(*args, **kwargs):
        def _inner(fn):
            return fn
        return _inner


def load_config(path: str = "config/config.yaml") -> Dict[str, Any]:
    """
    Load YAML or JSON config.
    Keep dependency minimal: if pyyaml present use YAML else expect JSON.
    """
    import yaml  # pyyaml should be in requirements

    if not os.path.exists(path):
        raise FileNotFoundError(f"Config file not found: {path}")

    with open(path, "r", encoding="utf-8") as fh:
        if path.endswith((".yaml", ".yml")):
            return yaml.safe_load(fh)
        else:
            return json.load(fh)


def ensure_dir(path: str):
    Path(path).mkdir(parents=True, exist_ok=True)


def iso_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def save_json(obj: Any, path: str, pretty: bool = True):
    ensure_dir(os.path.dirname(path) or ".")
    with open(path, "w", encoding="utf-8") as fh:
        if pretty:
            json.dump(obj, fh, ensure_ascii=False, indent=2)
        else:
            json.dump(obj, fh, ensure_ascii=False)


def load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def save_report_md(text: str, path: str = "reports/report.md"):
    ensure_dir(os.path.dirname(path) or ".")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def validate_schema(df_columns: list, required: Optional[list] = None) -> Dict[str, Any]:
    """
    Lightweight schema check — returns summary dict:
    {ok: bool, missing: [...], extra: [...]}
    """
    required = required or [
        "campaign_name",
        "adset_name",
        "date",
        "spend",
        "impressions",
        "clicks",
        "purchases",
        "revenue",
    ]
    present = set(df_columns)
    required_set = set(required)
    missing = sorted(list(required_set - present))
    extra = sorted(list(present - required_set))
    return {"ok": len(missing) == 0, "missing": missing, "extra": extra}


# Example wrapper used by DataAgent to add retries for load_data
@retry_on_exception(max_attempts=3, initial_wait=0.5, backoff_factor=2)
def safe_read_csv(path: str, **kwargs):
    import pandas as pd

    return pd.read_csv(path, **kwargs)


if __name__ == "__main__":
    # quick sanity
    print("iso_utc_now:", iso_utc_now())
    print("validate_schema example:", pformat(validate_schema(["campaign_name", "date", "spend", "impressions", "clicks", "purchases", "revenue"])))
