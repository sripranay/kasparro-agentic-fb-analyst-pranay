# Evaluation Checklist — Kasparro Agentic Facebook Ads Analyst  
This checklist summarizes all required components of the assignment and verifies that each has been implemented correctly.

---

## 1. Architecture Requirements

### ✔ Multi-Agent System Implemented
- [x] Planner Agent
- [x] Data Agent
- [x] Insight Agent
- [x] Evaluator Agent
- [x] Creative Agent

### ✔ Planner → Evaluator Loop
- [x] Planner decomposes task
- [x] Insight Agent generates hypotheses
- [x] Evaluator validates hypotheses with metrics
- [x] Creative Agent generates improved creatives
- [x] run.py orchestrates full pipeline

---

## 2. Prompt Requirements
- [x] planner_prompt.md
- [x] insight_prompt.md
- [x] evaluator_prompt.md
- [x] creative_prompt.md

All prompts include:
- Goal
- Required Behaviors
- Input
- Output
- JSON format
- Reasoning rules (Think → Analyze → Conclude)

---

## 3. Data + KPI Requirements
- [x] Dataset loaded through Data Agent
- [x] compute_kpis function calculates CTR, CPC, CPA, ROAS
- [x] summarize_df implemented
- [x] Window split for recent vs previous data
- [x] Percent change calculations implemented

---

## 4. Evaluation Logic Requirements
- [x] Hypotheses validated numerically
- [x] Confidence scoring (0–1)
- [x] Metrics used: CTR, CPC, CPM, Purchases, Spend, ROAS
- [x] Outputs structured in `reports/insights.json`

---

## 5. Creative Generation Requirements
- [x] Detect low-CTR campaigns
- [x] Generate headlines, bodies, CTAs
- [x] Output stored in `reports/creatives.json`
- [x] Grounded in dataset’s creative_message vocabulary

---

## 6. Output Files (Mandatory)
- [x] agent_graph.md
- [x] run.py
- [x] insights.json
- [x] creatives.json
- [x] report.md
- [x] README.md

---

## 7. Repository Structure (Required)
- [x] src/agents/
- [x] src/utils/
- [x] prompts/
- [x] config/config.yaml
- [x] data/ + README
- [x] reports/
- [x] requirements.txt
- [x] run.py
- [x] README.md

Optional but Included:
- [x] logs/
- [x] helpers.py
- [x] logger.py

---

## 8. Reproducibility
- [x] requirements.txt pinned
- [x] config-driven design
- [x] CLI command:
```bash
python run.py "Analyze ROAS drop"
