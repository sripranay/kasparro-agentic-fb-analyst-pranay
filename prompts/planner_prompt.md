# Planner Agent Prompt (documentation)

Purpose:
- Decompose a user instruction into a clear, ordered plan of subtasks the system will execute.
- Provide short notes on each step describing expected inputs, outputs, and any important constraints.
- Produce a JSON plan that is machine-readable and human-readable so the orchestrator can run tasks sequentially.

Input:
- A plain text user query (for example: "Analyze ROAS drop last 30 days" or "Generate creatives for low CTR campaigns").

Planner behavior rules:
1. Keep the plan short and executable (4–12 steps for typical requests).
2. Prefer deterministic, testable steps — each step should map to an agent or function name in the codebase.
3. When possible, include lightweight checks and early exits (e.g., "validate schema" before heavy computation).
4. Always include a final "compile_report" step which gathers outputs into `reports/report.md`.
5. Use existing agent names exactly: `load_data`, `compute_kpis`, `detect_roas_changes`, `compute_trends`, `generate_hypotheses`, `validate_hypotheses`, `generate_creative_recommendations`, `compile_report`.
6. If the dataset is large or sample mode is enabled, include `sample_mode` notes in the plan.
7. Include observability steps: log start/finish for each major step and save partial outputs to `reports/` for traceability.

Output (machine JSON):
Return valid JSON with the following schema:

{
  "query": "<original user query>",
  "timestamp": "<ISO UTC timestamp>",
  "plan": [
    {
      "step_id": 1,
      "name": "load_data",
      "description": "Load dataset from configured path, validate schema, return dataframe",
      "inputs": {"dataset_path": "config.data.dataset_path"},
      "outputs": ["df", "load_info"],
      "notes": "Retry up to 3 times on transient IO errors, sample if config.data.sample is true"
    },
    {
      "step_id": 2,
      "name": "compute_kpis",
      "description": "Compute CTR, CPC, CPA, ROAS and aggregate to daily/campaign levels",
      "inputs": ["df"],
      "outputs": ["kpi_df", "kpi_summary"]
    },
    ...
    {
      "step_id": N,
      "name": "compile_report",
      "description": "Merge validated insights and creative suggestions into `reports/report.md` and save JSON files",
      "inputs": ["insights.json", "creatives.json"],
      "outputs": ["reports/report.md", "reports/insights.json", "reports/creatives.json"]
    }
  ],
  "observability": {
    "logging": true,
    "log_file": "run.log",
    "save_partial_outputs": true
  },
  "constraints": {
    "max_runtime_seconds": 600,
    "memory_limit_mb": 4096
  }
}

Human-friendly notes:
- Each plan step must map to a function or agent class in `src/agents/` or `src/utils/`.
- Steps that can run in parallel (e.g., creative generation per campaign) should be flagged with `"parallel": true` in the step object.
- If a step fails, include a clear `retry` instruction and an early-exit reason in the plan output.
- When returning the JSON plan, set `plan.length` and include a short `summary` string that can be logged immediately.

Example (small):
Input: "Analyze ROAS drop last 30 days"

Output (summary):
{
  "query": "Analyze ROAS drop last 30 days",
  "timestamp": "2025-11-28T16:00:00Z",
  "plan": [
    {"step_id":1,"name":"load_data",...},
    {"step_id":2,"name":"compute_kpis",...},
    {"step_id":3,"name":"detect_roas_changes",...},
    {"step_id":4,"name":"compute_trends",...},
    {"step_id":5,"name":"generate_hypotheses",...},
    {"step_id":6,"name":"validate_hypotheses",...},
    {"step_id":7,"name":"generate_creative_recommendations",...},
    {"step_id":8,"name":"compile_report",...}
  ],
  "observability": {"logging":true,"log_file":"run.log"}
}

--- End of planner_prompt.md content
