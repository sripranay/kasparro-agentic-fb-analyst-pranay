# src/utils/loader.py
import yaml
import pandas as pd
from pathlib import Path
from typing import Any, Dict


def load_config(path: str) -> Dict[str, Any]:
    """
    Load YAML config and return a Python dict.
    Path is relative to project root, e.g. "config/config.yaml"
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Config file not found: {p.resolve()}")

    with open(p, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    # Backwards-compatible aliases and defaults
    if "data" in cfg:
        cfg["data"].setdefault("sample", cfg["data"].get("sample_mode", False))
        cfg["data"].setdefault("sample_n", cfg["data"].get("sample_n", 500))
        # keep both keys for convenience
        cfg["data"].setdefault("dataset_path", cfg["data"].get("dataset_path", cfg["data"].get("path", "data/synthetic_fb_ads_undergarments.csv")))

    return cfg


def load_data(path: str, sample: bool = False, sample_n: int = 500) -> pd.DataFrame:
    """
    Load dataset CSV using pandas and return a DataFrame.
    If `sample` is True, returns top `sample_n` rows (deterministic).
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Dataset not found: {p.resolve()}")

    # read CSV with pandas
    df = pd.read_csv(p)

    if sample:
        return df.head(sample_n).copy()
    return df
