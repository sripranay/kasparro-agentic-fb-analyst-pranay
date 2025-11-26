# src/agents/data_agent.py
import pandas as pd


class DataAgent:
    """
    Simple Data Agent that loads the dataset, returns a small summary dict.
    The orchestrator or test script should call load_config() and pass the config here.
    """

    def __init__(self, config: dict):
        self.config = config
        # dataset_path from config (relative path)
        self.dataset_path = config["data"]["dataset_path"]
        # sample flag (True/False) - configured in config.yaml
        self.sample = config["data"].get("sample", False)
        self.sample_n = config["data"].get("sample_n", 500)
        self.df = None

    def load_data(self):
        """Load CSV dataset. Returns basic info dict."""
        self.df = pd.read_csv(self.dataset_path)
        if self.sample:
            # keep deterministic top rows for quick dev
            self.df = self.df.head(self.sample_n)

        return {"rows": len(self.df), "columns": list(self.df.columns)}

    def missing_values(self):
        """Return missing values per column as dict."""
        return self.df.isnull().sum().to_dict()

    def basic_stats(self):
        """Return numeric column descriptive statistics as dict."""
        return self.df.describe(include="all").to_dict()

    def run(self):
        """Main entry for tests/orchestrator to call."""
        info = self.load_data()
        missing = self.missing_values()
        stats = self.basic_stats()
        return {"dataset_info": info, "missing_values": missing, "basic_stats": stats}
