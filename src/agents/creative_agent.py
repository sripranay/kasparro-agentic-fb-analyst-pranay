# src/agents/creative_agent.py
from typing import Dict, Any, List
import re

class CreativeAgent:
    """
    Simple rule-based creative improvement generator.
    Input: campaign_name, current_message, ctr_value (float)
    Output: dict with ranked ideas, rationale, and metadata
    """

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        # basic templates
        self.templates = [
            "{headline} — {benefit}. {cta}",
            "{headline}: {benefit} — {cta}",
            "{emotion} {headline}. {cta}",
            "{headline} — limited time: {cta}",
            "{question} {headline}? {cta}"
        ]
        # CTA options
        self.ctas = [
            "Shop now",
            "Upgrade today",
            "Try it risk-free",
            "Buy now",
            "Learn more"
        ]
        # Benefits examples (fallback)
        self.benefits = [
            "all-day comfort",
            "breathable fabric",
            "no ride-up fit",
            "better support",
            "engineered for movement"
        ]

    def _extract_keywords(self, text: str) -> List[str]:
        if not text:
            return []
        # lowercase, remove punctuation, get words of length>3
        s = re.sub(r"[^\w\s]", " ", text.lower())
        words = [w for w in s.split() if len(w) > 3]
        # return unique preserving order
        seen = set()
        out = []
        for w in words:
            if w not in seen:
                seen.add(w)
                out.append(w)
        return out

    def _pick_headlines(self, keywords: List[str]) -> List[str]:
        if not keywords:
            return ["Comfort You’ll Actually Love", "Engineered For Everyday Comfort"]
        # create few short headline options from keywords
        headlines = []
        if len(keywords) >= 1:
            headlines.append(keywords[0].capitalize())
        if len(keywords) >= 2:
            headlines.append(f"{keywords[0].capitalize()} {keywords[1].capitalize()}")
        if "comfort" in keywords:
            headlines.append("All-day Comfort")
        if "breathable" in keywords:
            headlines.append("Breathable Design")
        # short unique list
        seen = set()
        out = []
        for h in headlines:
            if h not in seen:
                seen.add(h)
                out.append(h)
        return out[:5]

    def _pick_benefit(self, keywords: List[str]) -> str:
        # choose benefit matching keyword if possible
        for k in ["comfort", "breathable", "support", "stretch", "ride-up", "fit"]:
            if k in keywords:
                return f"{k} benefits" if k not in ["comfort","breathable"] else ("all-day comfort" if k=="comfort" else "breathable fabric")
        # fallback
        return self.benefits[0]

    def _make_cta(self, ctr_value: float) -> str:
        # if ctr very low, use urgency/try CTA
        if ctr_value is not None and ctr_value < 0.01:
            return "Limited stock — shop now"
        # otherwise choose neutral CTA
        return "Shop now"

    def generate_creatives(self,
                           campaign_name: str,
                           current_message: str,
                           ctr_value: float = None,
                           max_ideas: int = 6) -> Dict[str, Any]:
        """
        Returns:
          {
            "campaign_name": str,
            "current_message": str,
            "ctr": float,
            "ideas": [str,...],
            "rationale": str
          }
        """
        keywords = self._extract_keywords(current_message)
        headlines = self._pick_headlines(keywords)
        benefit = self._pick_benefit(keywords)
        cta = self._make_cta(ctr_value)
        ideas = []
        rationale_points = []

        # Build ideas using templates
        for t in self.templates:
            for h in headlines:
                headline = h
                emotion = "Try the comfort"
                question = "Tired of riding up?"
                # pick CTA - some templates expect short CTA
                short_cta = cta if len(cta.split()) <= 3 else "Shop now"
                idea = t.format(
                    headline=headline,
                    benefit=benefit,
                    cta=short_cta,
                    emotion=emotion,
                    question=question
                )
                # dedupe and collect
                if idea not in ideas:
                    ideas.append(idea)
                if len(ideas) >= max_ideas:
                    break
            if len(ideas) >= max_ideas:
                break

        # Add a few variations that flip focus: feature -> benefit -> social proof -> urgency
        if len(ideas) < max_ideas:
            if keywords:
                ideas.append(f"{keywords[0].capitalize()} that works — {benefit}. {cta}")
        if len(ideas) < max_ideas:
            ideas.append(f"See why thousands prefer {campaign_name}. {cta}")

        # Rationale summary
        rationale_points.append(f"Derived {len(headlines)} headline anchors from creative message keywords: {', '.join(keywords[:5])}.")
        rationale_points.append(f"Focused on benefit: {benefit}.")
        if ctr_value is not None:
            rationale_points.append(f"CTR observed: {ctr_value:.4f} — used to decide CTA urgency.")
        rationale = " ".join(rationale_points)

        return {
            "campaign_name": campaign_name,
            "current_message": current_message,
            "ctr": ctr_value,
            "ideas": ideas[:max_ideas],
            "rationale": rationale
        }
