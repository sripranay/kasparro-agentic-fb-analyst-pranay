# Creative Agent Prompt (documentation)

Purpose:
- Generate new creative ad ideas to improve CTR and engagement.
- Rewrite existing creative messages in multiple variations.
- Follow brand-safe tone and short ad-copy style.

Input: JSON from validated insights, including:
- low CTR campaigns
- existing creative message
- performance metrics

Output: JSON:
- campaign_name
- original_message
- generated_messages: list of 3–6 variations

Guidelines for the model:
1. Keep messages short (3–10 words).
2. Must include CTA such as "Shop now", "Try now", "Learn more".
3. Follow tone of the existing creative (comfort, premium, fashion, etc.)
4. Do NOT invent product names — use given campaign info.
5. Each generated message should be unique.

Example Output:
{
  "campaign_name": "WOMEN Seamless Everyday",
  "original": "All-day comfort. Shop now",
  "generated_messages": [
    "Seamless comfort all day – Shop now",
    "Feel the comfort. Try now",
    "Your everyday seamless fit – Shop today",
    "Soft comfort made for you – Shop now"
  ]
}
