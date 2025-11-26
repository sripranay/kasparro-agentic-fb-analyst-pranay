# src/agents/evaluator_agent.py
import json
from typing import Dict, Any, List
from pathlib import Path


class EvaluatorAgent:
    """
    Validates hypotheses produced by InsightAgent using numeric checks and config thresholds.
    Produces evidence text and a confidence score (0.0 - 1.0) for each hypothesis.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        # thresholds from config (convert to percent where config uses fraction)
        self.roas_threshold_pct = float(self.config["thresholds"].get("roas_drop_pct", 0.20)) * 100.0
        self.ctr_threshold_pct = float(self.config["thresholds"].get("ctr_drop_pct", 0.15)) * 100.0
        self.ctr_low_threshold = float(self.config["thresholds"].get("ctr_low_threshold", 0.01)) * 100.0
        self.roas_low_threshold = float(self.config["thresholds"].get("roas_low_threshold", 0.5))
        self.spend_high_pctile = float(self.config["thresholds"].get("spend_high_pctile", 0.9))

    def _as_float(self, value) -> float:
        try:
            return float(value)
        except Exception:
            return 0.0

    def _score_change(self, change_pct: float, threshold_pct: float) -> float:
        """
        Score magnitude relative to threshold.
        If change_pct >= threshold_pct -> score approaches 1.0 (capped).
        For small changes score is proportionally smaller.
        """
        if threshold_pct <= 0:
            return min(1.0, abs(change_pct) / 100.0)
        score = min(1.0, abs(change_pct) / threshold_pct)
        return float(score)

    def _build_evidence(self, metric: str, recent: Dict[str, Any], previous: Dict[str, Any], change_pct: float) -> str:
        r = recent.get(metric, 0)
        p = previous.get(metric, 0)
        # format percentages specially for ctr/roas?
        if metric in ("ctr",):
            return f"{metric.upper()} changed by {change_pct:.2f}% (recent: {r:.4f}, previous: {p:.4f})"
        else:
            return f"{metric} changed by {change_pct:.2f}% (recent: {r}, previous: {p})"

    def validate(self, insight_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Validates the hypotheses returned by InsightAgent.
        Expects insight_result to contain:
          - recent_window (dict of metrics)
          - previous_window (dict of metrics)
          - percent_changes (dict metric -> percent)
          - hypotheses (list of hypothesis strings)
        Returns a list of dicts with fields:
          hypothesis, evidence, confidence (0-1), validated (bool)
        """
        recent = insight_result.get("recent_window", {})
        previous = insight_result.get("previous_window", {})
        percent_changes = {k: self._as_float(v) for k, v in insight_result.get("percent_changes", {}).items()}
        hyps = insight_result.get("hypotheses", [])

        validated = []

        # We'll map common keywords to metrics
        for h in hyps:
            h_lower = h.lower()
            entry = {"hypothesis": h, "evidence": "", "confidence": 0.0, "validated": False}

            # ROAS related
            if "roas" in h_lower:
                change = percent_changes.get("roas", 0.0)
                score = self._score_change(change, self.roas_threshold_pct)
                # match direction: if string says 'dropped' or 'fell' -> expect negative change
                expects_drop = ("drop" in h_lower) or ("fell" in h_lower) or ("decrease" in h_lower)
                direction_match = (change < 0) if expects_drop else (change >= 0)
                # base confidence from magnitude
                conf = score * (0.9 if direction_match else 0.5)
                entry["evidence"] = self._build_evidence("roas", recent, previous, change)
                entry["confidence"] = round(float(conf), 3)
                entry["validated"] = bool(conf > 0.25 and direction_match)

            # CTR related
            elif "ctr" in h_lower or "click" in h_lower:
                change = percent_changes.get("ctr", 0.0)
                score = self._score_change(change, self.ctr_threshold_pct)
                expects_drop = ("drop" in h_lower) or ("fell" in h_lower) or ("decrease" in h_lower) or ("fatigu" in h_lower)
                direction_match = (change < 0) if expects_drop else (change >= 0)
                # If absolute ctr is very low, bump confidence
                recent_ctr = self._as_float(recent.get("ctr", 0.0)) * 100.0
                low_ctr_flag = recent_ctr > 0 and recent_ctr < self.ctr_low_threshold
                conf = score * (0.9 if direction_match else 0.5)
                if low_ctr_flag:
                    conf = min(1.0, conf + 0.15)
                entry["evidence"] = self._build_evidence("ctr", recent, previous, change)
                entry["confidence"] = round(float(conf), 3)
                entry["validated"] = bool(conf > 0.3 and direction_match)

            # Spend related
            elif "spend" in h_lower:
                change = percent_changes.get("spend", 0.0)
                # percent of change vs small threshold - reuse roas threshold as heuristic
                score = self._score_change(change, self.roas_threshold_pct)
                entry["evidence"] = self._build_evidence("spend", recent, previous, change)
                conf = score * 0.7
                entry["confidence"] = round(float(conf), 3)
                entry["validated"] = bool(conf > 0.25)

            # Impressions / audience
            elif "impression" in h_lower or "audience" in h_lower or "frequency" in h_lower:
                change = percent_changes.get("impressions", 0.0)
                score = self._score_change(change, 5.0)  # small heuristic threshold 5%
                entry["evidence"] = self._build_evidence("impressions", recent, previous, change)
                entry["confidence"] = round(float(score * 0.7), 3)
                entry["validated"] = bool(abs(change) > 3.0)

            # Purchases / conversion
            elif "purchase" in h_lower or "conversion" in h_lower or "cpa" in h_lower:
                change = percent_changes.get("purchases", 0.0)
                score = self._score_change(change, 10.0)  # 10% heuristic
                entry["evidence"] = self._build_evidence("purchases", recent, previous, change)
                entry["confidence"] = round(float(score * 0.85), 3)
                entry["validated"] = bool(score > 0.25 and (change < 0 if "down" in h_lower or "drop" in h_lower or "fell" in h_lower else True))

            else:
                # fallback: use ROAS percent change as generic evidence
                change = percent_changes.get("roas", 0.0)
                score = self._score_change(change, self.roas_threshold_pct)
                entry["evidence"] = self._build_evidence("roas", recent, previous, change)
                entry["confidence"] = round(float(score * 0.5), 3)
                entry["validated"] = bool(score > 0.4)

            validated.append(entry)

        return validated

    def save_insights(self, validated_hypotheses: List[Dict[str, Any]], out_path: str = "reports/insights.json") -> None:
        """
        Persist validated hypotheses to JSON for submission.
        """
        p = Path(out_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            json.dump({"validated_hypotheses": validated_hypotheses}, f, indent=2)
