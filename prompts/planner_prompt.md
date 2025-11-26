\# Planner Agent Prompt (documentation)



Purpose:

\- Decompose a user instruction into an ordered set of subtasks.

\- Provide notes describing focus areas and expected outputs.



Input: plain text user query (e.g. "Analyze ROAS drop last 30 days")

Output: JSON with fields:

&nbsp; - query: original text

&nbsp; - timestamp: ISO UTC

&nbsp; - steps: ordered list of subtasks (strings)

&nbsp; - notes: optional list of short notes



Reasoning template:

Think:

&nbsp; - Identify keywords (roas, drop, ctr, creative, audience, fatigue)

Analyze:

&nbsp; - Map keywords to steps

&nbsp; - Guarantee core steps exist: load\_data, compute\_kpis, compute\_trends, detect\_roas\_changes, validate\_hypotheses, generate\_creative\_recommendations, compile\_report

Conclude:

&nbsp; - Return structured plan (see schema)



Example output (pretty):

{

&nbsp; "query": "Analyze ROAS drop",

&nbsp; "timestamp": "2025-11-26T04:30:00Z",

&nbsp; "steps": \[

&nbsp;    "load\_data",

&nbsp;    "compute\_kpis",

&nbsp;    "detect\_roas\_changes",

&nbsp;    "compute\_trends",

&nbsp;    "validate\_hypotheses",

&nbsp;    "generate\_creative\_recommendations",

&nbsp;    "compile\_report"

&nbsp; ],

&nbsp; "notes": \[

&nbsp;    "Focus on recent vs previous window (lookback\_days)",

&nbsp;    "Check CTR and impressions"

&nbsp; ]

}



