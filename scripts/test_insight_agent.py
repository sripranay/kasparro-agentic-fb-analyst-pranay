# scripts/test_insight_agent.py
import sys
import os

# make project root importable
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

from src.utils.loader import load_config, load_data
from src.agents.insight_agent import InsightAgent

# Load config
cfg = load_config("config/config.yaml")

# Determine dataset path from config
dataset_path = cfg["data"].get("dataset_path") or cfg["data"].get("path") or "data/synthetic_fb_ads_undergarments.csv"
sample_mode = cfg["data"].get("sample", False)
sample_n = cfg["data"].get("sample_n", 500)

# Load dataset (sample if requested)
df = load_data(dataset_path, sample=sample_mode, sample_n=sample_n)

# Create agent and analyze
insight = InsightAgent(cfg)
result = insight.analyze(df)

print("\n--- RECENT WINDOW ---")
print(result["recent_window"])

print("\n--- PREVIOUS WINDOW ---")
print(result["previous_window"])

print("\n--- PERCENT CHANGES ---")
print(result["percent_changes"])

print("\n--- HYPOTHESES ---")
for h in result["hypotheses"]:
    print("-", h)
