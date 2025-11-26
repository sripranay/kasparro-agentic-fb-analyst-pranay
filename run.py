# run.py
"""
Main orchestrator. Usage (from project root):
    python run.py "Analyze ROAS drop"

This script:
- loads config
- loads dataset (sample mode if configured)
- runs Planner to build steps (optional)
- runs InsightAgent -> EvaluatorAgent -> CreativeAgent
- saves outputs: reports/insights.json, reports/creatives.json, reports/report.md
"""
import sys
import os
import json
from datetime import datetime

# ensure project root is on path when run from project root
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.append(PROJECT_ROOT)

from src.utils.loader import load_config, load_data
from src.agents.planner_agent import PlannerAgent
from src.agents.insight_agent import InsightAgent
from src.agents.evaluator_agent import EvaluatorAgent
from src.agents.creative_agent import CreativeAgent

def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, default=str)

def write_report_md(path, insights_validated, creatives, config, summary_text=None):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    lines = []
    lines.append(f"# Facebook Ads Agentic Analysis Report\n")
    lines.append(f"Generated: {now}\n")
    lines.append(f"## Quick summary\n")
    if summary_text:
        lines.append(summary_text + "\n")
    else:
        # build quick summary from top validated hypotheses
        top = [h for h in insights_validated if h.get("validated")]
        if top:
            lines.append("Top validated insights:\n")
            for t in top:
                lines.append(f"- {t['hypothesis']} — {t['evidence']} (confidence: {t['confidence']})\n")
        else:
            lines.append("No high-confidence validated hypotheses found. See details below.\n")

    lines.append("\n## Validated Insights (full)\n")
    for h in insights_validated:
        lines.append(f"### {h['hypothesis']}\n")
        lines.append(f"- Evidence: {h['evidence']}\n")
        lines.append(f"- Confidence: {h['confidence']}\n")
        lines.append(f"- Validated: {h['validated']}\n\n")

    lines.append("\n## Creative Recommendations\n")
    if creatives and "ideas" in creatives:
        for i, idea in enumerate(creatives["ideas"], 1):
            lines.append(f"{i}. {idea}\n")
        lines.append("\nRationale:\n")
        lines.append(creatives.get("rationale", "") + "\n")
    else:
        lines.append("No creative recommendations generated.\n")

    lines.append("\n## Config snapshot\n")
    lines.append("```json\n")
    lines.append(json.dumps(config, indent=2))
    lines.append("\n```\n")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

def orchestrate(query: str):
    cfg = load_config("config/config.yaml")

    # load dataset (respect sample mode)
    dataset_path = cfg["data"].get("dataset_path") or cfg["data"].get("path") or "data/synthetic_fb_ads_undergarments.csv"
    sample_mode = cfg["data"].get("sample", False)
    sample_n = cfg["data"].get("sample_n", 500)
    print("Loading data:", dataset_path, "sample_mode:", sample_mode)
    df = load_data(dataset_path, sample=sample_mode, sample_n=sample_n)

    # Planner (optional - used to describe steps; safe fallback)
    planner = PlannerAgent(cfg)
    plan = planner.plan(query)
    print("Plan steps:", plan.get("steps", []))

    # Insight
    insight_agent = InsightAgent(cfg)
    insight_result = insight_agent.analyze(df)
    # Save raw insight_result for debugging
    write_json("reports/insight_result_raw.json", insight_result)

    # Evaluator
    eval_agent = EvaluatorAgent(cfg)
    validated = eval_agent.validate(insight_result)
    eval_agent.save_insights(validated, out_path="reports/insights.json")
    print("Saved validated insights to reports/insights.json")

    # Creative: choose a low-CTR campaign to generate creatives for
    # Simple heuristic: pick the hypothesis mentioning CTR drop OR pick sample campaign
    campaign_to_use = None
    # try to find a campaign name in dataframe with low ctr
    try:
        # compute campaign-level ctr and pick campaign with lowest ctr
        df2 = df.copy()
        df2["ctr"] = df2["clicks"] / df2["impressions"].replace({0: 1})
        campaign_ctr = df2.groupby("campaign_name")["ctr"].mean().sort_values()
        if not campaign_ctr.empty:
            campaign_to_use = campaign_ctr.index[0]
            campaign_ctr_value = float(campaign_ctr.iloc[0])
        else:
            campaign_to_use = None
            campaign_ctr_value = None
    except Exception:
        campaign_to_use = None
        campaign_ctr_value = None

    creative_agent = CreativeAgent(cfg)
    creatives_out = {}
    if campaign_to_use:
        # find an example current_message for the campaign
        msg_row = df[df["campaign_name"] == campaign_to_use]["creative_message"].dropna()
        current_message = msg_row.iloc[0] if not msg_row.empty else ""
        creatives_out = creative_agent.generate_creatives(
            campaign_name=campaign_to_use,
            current_message=current_message,
            ctr_value=campaign_ctr_value,
            max_ideas=8
        )
        write_json("reports/creatives.json", creatives_out)
        print("Saved creatives to reports/creatives.json")
    else:
        print("No campaign selected for creative generation.")

    # final report.md
    write_report_md("reports/report.md", validated, creatives_out, cfg)
    print("Saved final report to reports/report.md")

    # print short summary
    print("\n=== RUN SUMMARY ===")
    successes = [h for h in validated if h.get("validated")]
    print(f"Validated insights: {len(successes)} / {len(validated)}")
    if creatives_out:
        print(f"Creative ideas generated for campaign: {creatives_out.get('campaign_name')}")
    print("Outputs: reports/insights.json, reports/creatives.json, reports/report.md")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run.py \"Analyze ROAS drop\"")
        sys.exit(1)
    query = sys.argv[1]
    orchestrate(query)
