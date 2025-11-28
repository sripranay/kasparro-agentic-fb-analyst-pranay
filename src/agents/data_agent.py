# src/agents/data_agent.py
import pandas as pd
from typing import Dict, Any, Optional

from src.utils.logger import logger, timed_agent
from src.utils.retry import retry
from src.utils.schema import validate_schema
from src.utils.helpers import compute_kpis, summarize_df


class DataAgent:
    """
    Data Agent: loads the dataset robustly, validates schema, computes KPIs,
    and returns small summaries for use by other agents.
    """

    def __init__(self, config: dict):
        self.config = config
        # dataset_path from config (relative path)
        self.dataset_path = config["data"]["dataset_path"]
        # sample flag (True/False) - configured in config.yaml
        self.sample = config["data"].get("sample", False)
        self.sample_n = config["data"].get("sample_n", 500)
        self.df: Optional[pd.DataFrame] = None

    def _read_csv_with_retry(self, path: str) -> pd.DataFrame:
        """Read CSV using the retry helper to handle transient IO errors."""
        logger.info("Attempting to load CSV with retry: %s", path)
        df = retry(pd.read_csv, args=(path,), kwargs={"encoding": "utf-8"}, retries=3, base_delay=1.0)
        logger.info("CSV read complete: rows=%s cols=%s", df.shape[0], df.shape[1])
        return df

    def load_data(self) -> Dict[str, Any]:
        """
        Load CSV, validate schema, optionally sample, compute KPIs, and return dataset info.
        Returns:
            dict with rows, columns, sample flag, and summary stats.
        """
        with timed_agent("data_agent", {"path": self.dataset_path, "sample": self.sample}):
            # 1) robust load
            df = self._read_csv_with_retry(self.dataset_path)

            # 2) basic schema validation
            try:
                validate_schema(df.columns)
            except Exception as e:
                # log and re-raise so orchestrator can handle gracefully
                logger.exception("Schema validation failed: %s", e)
                raise

            # 3) sample if requested (keeps determinism during dev)
            if self.sample:
                logger.info("Sampling first %d rows for dev mode", self.sample_n)
                df = df.head(self.sample_n)

            # 4) compute KPI columns safely
            try:
                df = compute_kpis(df)
                logger.info("Computed KPIs: added columns if missing (ctr,cpc,cpa,roas)")
            except Exception as e:
                logger.exception("Error computing KPIs: %s", e)
                raise

            # 5) persist to self and return summary
            self.df = df
            summary = summarize_df(df)

            info = {"rows": len(df), "columns": list(df.columns)}
            logger.info("DataAgent.load_data finished: rows=%d columns=%d", info["rows"], len(info["columns"]))
            return {"dataset_info": info, "summary": summary}

    def missing_values(self) -> Dict[str, int]:
        """Return missing values per column as dict."""
        if self.df is None:
            logger.warning("missing_values called before data loaded")
            return {}
        return self.df.isnull().sum().to_dict()

    def basic_stats(self) -> Dict[str, Any]:
        """Return numeric column descriptive statistics as dict."""
        if self.df is None:
            logger.warning("basic_stats called before data loaded")
            return {}
        return self.df.describe(include="all").to_dict()

    def get_df(self) -> Optional[pd.DataFrame]:
        """Return processed DataFrame (after load_data)."""
        return self.df

    def run(self) -> Dict[str, Any]:
        """Main entry for orchestrator to call — returns dataset info, missing vals, and basic stats."""
        res = self.load_data()
        missing = self.missing_values()
        stats = self.basic_stats()
        return {"dataset_info": res.get("dataset_info"), "missing_values": missing, "basic_stats": stats}
