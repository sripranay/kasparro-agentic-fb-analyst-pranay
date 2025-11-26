# test_load_config.py (or run in a notebook cell)
import yaml
from pathlib import Path
cfg_path = Path("config/config.yaml")
assert cfg_path.exists(), f"Config file not found: {cfg_path}"
with open(cfg_path, "r") as f:
    cfg = yaml.safe_load(f)
print("Config keys:", list(cfg.keys()))
print("Dataset path:", cfg['data']['dataset_path'])
print("Sample mode:", cfg['data']['sample_mode'])
