import sys
import os

# --- FIX PATH ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

# Import after path fix
from src.agents.data_agent import DataAgent
from src.utils.loader import load_config

config = load_config("config/config.yaml")
agent = DataAgent(config)

summary = agent.run()

print("\n--- DATA SUMMARY ---")
print(summary)
