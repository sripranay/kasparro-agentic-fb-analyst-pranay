# scripts/test_creative_agent.py
import sys, os
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

from src.utils.loader import load_config
from src.agents.creative_agent import CreativeAgent
import json

cfg = load_config("config/config.yaml")

agent = CreativeAgent(config=cfg)

# Example run - adapt campaign and message as needed
campaign = "Men Bold Colors Drop"
current_message = "No ride-up guarantee — best-selling men briefs."
ctr_value = 0.008  # example low CTR

result = agent.generate_creatives(
    campaign_name=campaign,
    current_message=current_message,
    ctr_value=ctr_value,
    max_ideas=6
)

print("\n--- GENERATED CREATIVE RECOMMENDATIONS ---")
for i, idea in enumerate(result["ideas"], 1):
    print(f"{i}. {idea}")

# Save to reports/creatives.json
os.makedirs("reports", exist_ok=True)
with open("reports/creatives.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2)

print("\nSaved creatives to reports/creatives.json")
