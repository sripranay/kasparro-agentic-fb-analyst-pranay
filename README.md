# Kasparro Agentic Facebook Ads Performance Analyst  
### Multi-Agent System for ROAS Diagnosis & Creative Recommendations  


---

##  Overview  
This project implements a **multi-agent AI system** that automatically analyzes Facebook Ads performance, detects reasons behind ROAS changes, and generates new creative ideas for low-CTR campaigns.  

It follows the exact assignment requirements provided by **Kasparro Applied AI Engineer Assessment**.

---

##  Objectives  
The system is designed to:

- Detect **why ROAS changed** over time  
- Identify **drivers** such as:  
  - creative fatigue  
  - audience burnout  
  - high CPC / low CTR  
  - declining impressions or purchases  
- Generate **new creative messages** based on existing creative text  
- Produce a **final report** summarizing insights, evidence, and recommendations  

---

##  Multi-Agent Architecture  

### **1. Planner Agent**
Breaks the user query into structured steps:
- `load_data`
- `compute_kpis`
- `detect_roas_changes`
- `compute_trends`
- `generate_hypotheses`
- `validate_hypotheses`
- `generate_creative_recommendations`
- `compile_report`

### **2. Data Agent**
- Loads dataset from `data/…csv`
- Computes KPIs: CTR, CPC, CPA, ROAS  
- Returns clean DataFrame + summary statistics  

### **3. Insight Agent**
- Compares *recent 7-day window* vs *previous 7-day window*  
- Detects trends and creates hypotheses such as:  
  - “CTR dropped due to creative fatigue.”  
  - “Spend increased causing efficiency loss.”  

### **4. Evaluator Agent**
- Quantitatively checks each hypothesis  
- Computes % change, confidence, validation flag  
- Saves results to `reports/insights.json`

### **5. Creative Agent**
- Identifies low-CTR campaigns  
- Generates **new ad headlines + CTA messages**  
- Saves to `reports/creatives.json`

---
### **Project Structure**

```md
├── config/
│   └── config.yaml
├── data/
│   └── synthetic_fb_ads_undergarments.csv
├── prompts/           # agent prompt templates
├── reports/           # insights.json, creatives.json, report.md
├── scripts/           # test scripts for each agent
├── src/
│   ├── agents/        # planner, data, insight, evaluator, creative
│   └── utils/         # loader, kpi calculations
├── run.py             # main orchestrator
└── README.md
```
---

## ▶️ How to Run the System

### **1. Install dependencies**
```bash
pip install -r requirements.txt
```

### **2. Run full ROAS analysis**
```
python run.py "Analyze ROAS drop"
```

### **3. Output Files Generated**
After running, you will get:

 reports/insights.json – validated hypotheses
 reports/creatives.json – new creative ideas
 reports/report.md – final human-readable report

### **Example Output Summary**
```
yaml
Copy code
Validated insights: 1 / 5
Creatives generated for: WOMEN Seamless Everyday
Outputs saved to: reports/
```
 ### **Dataset Used**
A synthetic e-commerce Facebook Ads dataset containing:
campaign_name, adset_name, date, spend, impressions, clicks, ctr, purchases, revenue, roas, creative_message, creative_type, audience_type, platform, country

### **Configuration**
```
arduino
Copy code
config/config.yaml
```
---





