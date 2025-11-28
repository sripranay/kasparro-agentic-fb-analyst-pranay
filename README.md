# Kasparro Agentic Facebook Ads Performance Analyst  
### Multi-Agent System for ROAS Diagnosis & Creative Recommendations  
 

---

##  Overview  
This project implements a **multi-agent AI system** that analyzes Facebook Ads performance, detects the root causes behind ROAS changes, and generates new creative ideas for improving low-CTR campaigns.

It is built according to the **Kasparro Applied AI Engineer Technical Assessment** and includes:
- KPI computation  
- Trend detection  
- Hypothesis generation & validation  
- Creative theme generation  
- Automated reporting  

---

##  Objectives  
The system is designed to:

- Diagnose **why ROAS changed**  
- Detect performance drivers such as:  
  - Creative fatigue  
  - Audience saturation  
  - Low CTR / high CPC  
  - Declining impressions  
  - Weak conversion rate  
- Generate **new ad creatives** from existing messages  
- Produce a final **human-readable report** summarizing:  
  - Insights  
  - Evidence  
  - Validated hypotheses  
  - Creative recommendations  

---

##  Multi-Agent Architecture  

### **1. Planner Agent**
Breaks the task into actionable steps:
- `load_data`  
- `compute_kpis`  
- `detect_roas_changes`  
- `compute_trends`  
- `generate_hypotheses`  
- `validate_hypotheses`  
- `generate_creative_recommendations`  
- `compile_report`  

---

### **2. Data Agent**
- Loads dataset from `data/*.csv`  
- Handles sampling mode  
- Computes KPIs (CTR, CPC, CPA, ROAS, CPM)  
- Performs data validation & schema checks  
- Returns clean DataFrame and summary  

---

### **3. Insight / Trends Agent**
- Compares **recent window** vs **previous window**  
- Detects metric changes:  
  - ROAS  
  - CTR  
  - Spend  
  - Impressions  
  - Purchases  
- Generates hypotheses such as:  
  - “CTR dropped due to creative fatigue.”  
  - “Spend fell, reducing delivery.”  
  - “Purchases down due to weak conversion.”  

---

### **4. Evaluator Agent**
For every hypothesis, it:  
- Computes percentage change  
- Generates evidence  
- Estimates confidence  
- Marks as *validated / not validated*  
- Saves to `reports/insights.json`  

---

### **5. Creative Agent**
- Identifies low-CTR segments  
- Creates **new ad headlines** and **CTA messages**  
- Saves to `reports/creatives.json`  

---

##  Project Structure

```md
├── config/
│   └── config.yaml
├── data/
│   └── synthetic_fb_ads_undergarments.csv
├── prompts/                  # Prompt templates for all agents
├── reports/                  # Generated insights, creatives, final report
│   ├── insights.json
│   ├── creatives.json
│   └── report.md
├── scripts/                  # Optional test utilities
├── src/
│   ├── agents/               # planner, data, trends, evaluator, creative
│   └── utils/                # logger, helpers, retry, schema validator
├── run.py                    # Main orchestrator
└── README.md
```
### **How to Run the System**
### 1. Install dependencies
`pip install -r requirements.txt`

### 2. Run the full ROAS analysis
`python run.py "Analyze ROAS drop"`

### **Output Files Generated**

After running the system, the following outputs are created:

- `reports/insights.json` – validated hypotheses

- `reports/creatives.json` – creative recommendations

- `reports/report.md` – final full analysis report

### Example Output Summary
```
Validated insights: 1 / 5  
Creatives generated for: WOMEN Seamless Everyday  
Outputs saved to: reports/
```
### **Dataset Used**

A synthetic e-commerce Facebook Ads dataset containing:

`campaign_name`, `adset_name`, `date`, `spend`,` impressions`, `clicks`,
`ctr`,` purchases`,` revenue`,` roas`,
`creative_message`, `creative_type`, `audience_type`,
`platform`, `country`

### **Configuration**

Main config file:
```
config/config.yaml
```


### **Includes:**

dataset path

sampling options

thresholds

windows

creative generation settings