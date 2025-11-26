# scripts/test_evaluator_agent.py
import sys, os
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

from src.utils.loader import load_config, load_data
from src.agents.data_agent import DataAgent
from src.agents.insight_agent import InsightAgent
from src.agents.evaluator_agent import EvaluatorAgent

cfg = load_config("config/config.yaml")

# load dataset (respect sample mode)
dataset_path = cfg["data"].get("dataset_path")
sample_mode = cfg["data"].get("sample", False)
sample_n = cfg["data"].get("sample_n", 500)

df = load_data(dataset_path, sample=sample_mode, sample_n=sample_n)

print("Running InsightAgent...")
insight_agent = InsightAgent(cfg)
insight_result = insight_agent.analyze(df)

print("Running EvaluatorAgent...")
eval_agent = EvaluatorAgent(cfg)
validated = eval_agent.validate(insight_result)

# print results
print("\n--- VALIDATED HYPOTHESES ---")
for v in validated:
    print("-", v["hypothesis"])
    print("  evidence:", v["evidence"])
    print("  confidence:", v["confidence"])
    print("  validated:", v["validated"])

# save to reports/insights.json
eval_agent.save_insights(validated, out_path="reports/insights.json")
print("\nSaved insights to reports/insights.json")
