# Agent Graph – Kasparro Agentic Facebook Ads Analyst  
### Multi-Agent System Architecture Diagram & Flow Explanation  


---

## Overview  
This document explains the full agent graph, the responsibilities of each agent, and how data flows through the entire system from user query → final report.

The system contains **5 agents**, orchestrated by the **Planner Agent**.

---

## Agent Graph Diagram (Text-Based)

```md
+------------------+
|   User Query     |
+--------+---------+
         |
         v
+------------------+
|  Planner Agent   |
| (creates plan)   |
+----+----+--------+
     |    | 
     |    v
     |   Step 1: load_data
     |   Step 2: compute_kpis
     |   Step 3: detect_roas_changes
     |   Step 4: compute_trends
     |   Step 5: generate_hypotheses
     |   Step 6: validate_hypotheses
     |   Step 7: generate_creatives
     |   Step 8: compile_report
     |
     v
+-------------------+
|    Data Agent     |
|  Loads + cleans   |
|     dataset       |
+-------------------+
         |
         v
+-------------------+
|  Insight Agent    |
| Trend analysis &  |
| hypothesis gen    |
+-------------------+
         |
         v
+-------------------+
| Evaluator Agent   |
| Validates ROAS,   |
| CTR, CPC shifts   |
+-------------------+
         |
         v
+-------------------+
| Creative Agent    |
| Generates new     |
| ad messaging      |
+-------------------+
         |
         v
+-------------------+
|   Final Report    |
| insights.json     |
| creatives.json    |
| report.md         |
+-------------------+
```

## Agent Responsibilities

1️⃣ Planner Agent

Reads user query  
Converts it into structured steps  
Orchestrates the order of agents  
Ensures system follows assignment's reasoning flow  

2️⃣ Data Agent

Responsible for data operations:  
Load CSV  
Clean missing values  
Compute KPIs (CTR, CPC, CPA, ROAS)  
Return processed dataset  

3️⃣ Insight Agent

Splits data into recent vs previous windows  
Detects performance trends  
Generates natural-language hypotheses  

4️⃣ Evaluator Agent

Validates hypotheses using numeric metrics  
Computes percent change & confidence  
Saves results to reports/insights.json  

5️⃣ Creative Agent

Identifies low-CTR campaigns  
Generates new ad messaging ideas  
Saves output to reports/creatives.json  


## Full Data Flow

User Query  
    ↓  
Planner Agent  
    ↓  
Data Agent → cleans & computes KPIs  
    ↓  
Insight Agent → trend analysis & hypotheses  
    ↓  
Evaluator Agent → numerical validation  
    ↓  
Creative Agent → new ad copy  
    ↓  
Final Report (report.md + insights.json + creatives.json)  


## How to Run

```bash
python run.py "Analyze ROAS drop"
```
## Output Files
```MD
reports/
 ├── insights.json
 ├── creatives.json
 └── report.md
