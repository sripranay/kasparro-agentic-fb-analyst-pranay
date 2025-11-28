# Facebook Ads Agentic Analysis Report

Generated: 2025-11-28 14:29 UTC

## Quick summary

Top validated insights:

- ROAS improved — campaigns are becoming more efficient. — roas changed by 5.58% (recent: 6.574655544298444, previous: 6.227011039963705) (confidence: 0.251)


## Validated Insights (full)

### ROAS improved — campaigns are becoming more efficient.

- Evidence: roas changed by 5.58% (recent: 6.574655544298444, previous: 6.227011039963705)

- Confidence: 0.251

- Validated: True


### CTR fell — creatives may be fatiguing or less relevant.

- Evidence: CTR changed by -0.73% (recent: 0.0124, previous: 0.0125)

- Confidence: 0.044

- Validated: False


### Spend decreased — could limit reach and impressions.

- Evidence: spend changed by -2.84% (recent: 150936.68, previous: 155351.96000000002)

- Confidence: 0.099

- Validated: False


### Impressions dropped — audience size or delivery issues possible.

- Evidence: impressions changed by -0.41% (recent: 86641669, previous: 86996972)

- Confidence: 0.057

- Validated: False


### Purchases down — conversion drop or weaker creative performance.

- Evidence: purchases changed by -1.59% (recent: 28517, previous: 28979)

- Confidence: 0.136

- Validated: False



## Creative Recommendations

1. Doctors — breathable fabric. Shop now

2. Doctors Recommend — breathable fabric. Shop now

3. Breathable Design — breathable fabric. Shop now

4. Doctors: breathable fabric — Shop now

5. Doctors Recommend: breathable fabric — Shop now

6. Breathable Design: breathable fabric — Shop now

7. Try the comfort Doctors. Shop now

8. Try the comfort Doctors Recommend. Shop now


Rationale:

Derived 3 headline anchors from creative message keywords: doctors, recommend, breathable, organic, cotton. Focused on benefit: breathable fabric. CTR observed: 0.0053 — used to decide CTA urgency.


## Config snapshot

```json

{
  "project": {
    "name": "kasparro-agentic-fb-analyst-pranay",
    "version": "0.1.0",
    "author": "Your Name"
  },
  "data": {
    "dataset_path": "data/synthetic_fb_ads_undergarments.csv",
    "sample_mode": true,
    "sample_n": 1000,
    "sample": true
  },
  "thresholds": {
    "roas_drop_pct": 0.2,
    "ctr_drop_pct": 0.15,
    "ctr_low_threshold": 0.01,
    "roas_low_threshold": 0.5,
    "spend_high_pctile": 0.9
  },
  "analysis": {
    "trend_window_days": 14,
    "lookback_days": 30
  },
  "outputs": {
    "reports_dir": "reports",
    "logs_dir": "logs",
    "insights_file": "reports/insights.json",
    "creatives_file": "reports/creatives.json",
    "report_md": "reports/report.md"
  },
  "runtime": {
    "random_seed": 42,
    "verbose": true
  }
}

```
