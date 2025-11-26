# src/agents/planner_agent.py
import datetime
from typing import Dict, List

class PlannerAgent:
    """
    Simple rule-based Planner Agent.
    Input: user query string
    Output: dict with 'query', 'timestamp', 'steps' (ordered), and 'notes'
    """

    def __init__(self, config: Dict):
        self.config = config

    def _base_steps(self) -> List[str]:
        return [
            "load_data",
            "compute_kpis",
            "compute_trends",
            "detect_roas_changes",
            "generate_hypotheses",
            "validate_hypotheses",
            "generate_creative_recommendations",
            "compile_report"
        ]

    def plan(self, user_query: str) -> Dict:
        """
        Convert user_query into a sequence of subtasks.
        This is intentionally simple and deterministic:
        - Look for keywords and add focused steps or parameters.
        """
        q = user_query.strip().lower()

        steps = self._base_steps()
        notes = []

        # detect focused intent keywords and tweak steps/notes
        if "roas" in q and ("drop" in q or "decrease" in q or "fall" in q):
            notes.append("Focus on recent ROAS drop: compare lookback windows (recent vs previous).")
            # ensure detect_roas_changes and validate_hypotheses are present early
            # move them earlier in the sequence
            steps.remove("detect_roas_changes")
            steps.insert(2, "detect_roas_changes")
            steps.remove("validate_hypotheses")
            steps.insert(4, "validate_hypotheses")

        if "creative" in q or "ctr" in q:
            notes.append("Include creative-message analysis and CTR-based recommendations.")
            # make sure creative generation runs
            if "generate_creative_recommendations" not in steps:
                steps.append("generate_creative_recommendations")

        if "audience" in q or "fatigue" in q:
            notes.append("Check audience sizes, impressions and frequency for signs of fatigue.")
            # add extra step for audience checks
            if "check_audience_signals" not in steps:
                steps.insert(3, "check_audience_signals")

        # default time settings
        ts = datetime.datetime.utcnow().isoformat() + "Z"

        plan = {
            "query": user_query,
            "timestamp": ts,
            "steps": steps,
            "notes": notes,
            "schema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "timestamp": {"type": "string"},
                    "steps": {"type": "array", "items": {"type": "string"}},
                    "notes": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["query", "timestamp", "steps"]
            }
        }
        return plan
