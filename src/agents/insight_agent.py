# src/agents/insight_agent.py

import pandas as pd
from typing import Dict, Any

class InsightAgent:
    """
    Produces insights + hypotheses from summary statistics and full dataframe.
    Fully deterministic, no LLM used.
    """

    def __init__(self, config: Dict):
        self.config = config
        self.lookback_days = self.config["analysis"]["lookback_days"]

    def _compute_window(self, df: pd.DataFrame) -> Dict[str, float]:
        """Compute aggregates for a given window of data."""
        return {
            "spend": df["spend"].sum(),
            "impressions": df["impressions"].sum(),
            "clicks": df["clicks"].sum(),
            "purchases": df["purchases"].sum(),
            "revenue": df["revenue"].sum(),
            "ctr": (df["clicks"].sum() / df["impressions"].sum()) if df["impressions"].sum() > 0 else 0,
            "cpc": (df["spend"].sum() / df["clicks"].sum()) if df["clicks"].sum() > 0 else 0,
            "cpa": (df["spend"].sum() / df["purchases"].sum()) if df["purchases"].sum() > 0 else 0,
            "roas": (df["revenue"].sum() / df["spend"].sum()) if df["spend"].sum() > 0 else 0,
        }

    def _percent_change(self, new: float, old: float) -> float:
        if old == 0:
            return 0
        return ((new - old) / old) * 100

    def _generate_hypotheses(self, recent: Dict, previous: Dict) -> list:
        hyp = []

        # ROAS Hypotheses
        if recent["roas"] < previous["roas"]:
            hyp.append("ROAS dropped — possible cause: spend increased faster than revenue.")
            hyp.append("Purchases may have dropped or CPC increased.")
        else:
            hyp.append("ROAS improved — campaigns are becoming more efficient.")

        # CTR Hypotheses
        if recent["ctr"] < previous["ctr"]:
            hyp.append("CTR fell — creatives may be fatiguing or less relevant.")
        else:
            hyp.append("CTR improved — creative messaging is resonating better.")

        # Spend Changes
        if recent["spend"] > previous["spend"]:
            hyp.append("Spend increased — check if this aligns with CTR and purchases.")
        else:
            hyp.append("Spend decreased — could limit reach and impressions.")

        # Impressions Changes
        if recent["impressions"] < previous["impressions"]:
            hyp.append("Impressions dropped — audience size or delivery issues possible.")
        else:
            hyp.append("Impressions increased — reach expanded.")

        # Purchases
        if recent["purchases"] < previous["purchases"]:
            hyp.append("Purchases down — conversion drop or weaker creative performance.")
        else:
            hyp.append("Purchases increased — stronger funnel efficiency.")

        return hyp

    def analyze(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        1. Split data into recent + previous windows
        2. Compute aggregates
        3. Generate percent changes
        4. Produce insights + hypotheses
        """
        df["date"] = pd.to_datetime(df["date"])
        max_date = df["date"].max()

        recent_window = df[df["date"] >= (max_date - pd.Timedelta(days=self.lookback_days))]
        previous_window = df[
            (df["date"] < (max_date - pd.Timedelta(days=self.lookback_days)))
            & (df["date"] >= (max_date - pd.Timedelta(days=self.lookback_days * 2)))
        ]

        recent = self._compute_window(recent_window)
        previous = self._compute_window(previous_window)

        percent_changes = {
            k: self._percent_change(recent[k], previous[k])
            for k in recent
        }

        hypotheses = self._generate_hypotheses(recent, previous)

        return {
            "recent_window": recent,
            "previous_window": previous,
            "percent_changes": percent_changes,
            "hypotheses": hypotheses,
        }
