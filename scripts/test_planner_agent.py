# scripts/test_planner_agent.py
import sys, os
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

from src.utils.loader import load_config
from src.agents.planner_agent import PlannerAgent

cfg = load_config("config/config.yaml")
planner = PlannerAgent(cfg)

tests = [
    "Analyze ROAS drop in the last 14 days",
    "Suggest creative improvements for low CTR campaigns",
    "Investigate audience fatigue and ROAS fall",
    "Quick summary"
]

for t in tests:
    plan = planner.plan(t)
    print("\n--- QUERY ---")
    print(t)
    print("--- PLAN ---")
    print("Steps:", plan["steps"])
    print("Notes:", plan["notes"])
