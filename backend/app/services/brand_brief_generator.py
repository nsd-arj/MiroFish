"""
Brand Brief Generator

Generates a comprehensive simulation brief in structured markdown from the five
brand context inputs. The brief is:
  1. Saved to disk alongside the simulation for reference.
  2. Used to auto-populate simulation_requirement when the user left it blank.
  3. Parsed for per-cohort persona enrichment (use cases → advocates/loyalists,
     objections → skeptics/haters, topics → all agents).
"""

import re
import logging
from typing import Optional

from openai import OpenAI
from ..config import Config

logger = logging.getLogger("mirofish.brand_brief")

_BRIEF_PROMPT = """\
You are a market research analyst and simulation strategist. \
Generate a comprehensive brand simulation brief in structured markdown.

Brand context inputs:
- Brand Name: {brand_name}
- Brand URL: {brand_url}
- Primary Objection: {primary_objection}
- Advocate Trigger: {advocate_trigger}
- Target Segment: {target_segment}

Output EXACTLY the following sections in this order. No preamble, no explanation \
outside the sections. Fill every section with real, specific content — no generic filler.

---

# {brand_name} — Brand Simulation Brief

**Brand:** {brand_name}
**URL:** {brand_url}

---

## What {brand_name} Is
[2–3 paragraphs. What the product does, how it works, the category it competes in, \
and its pricing or access model.]

## Primary Use Cases (Advocate Triggers)
[Expand advocate_trigger into 4–6 numbered use cases. Give each a bold sub-heading \
and 3–4 specific sub-scenarios as bullet points. Anchor each scenario in an emotional \
moment — why it matters to the person doing it.]

## Primary Objections
[Expand primary_objection into one section per major objection. Include: the objection \
in plain user language (quoted), the emotional driver behind it, and the specific \
conversion barrier it creates. Use bullet points for user quotes.]

## Target Audience Profile

### Primary Buyer Persona: [Invent a short archetype name]
[Demographics, psychographic profile (values, decision-making style), relationship \
to the product, what triggers conversion, what triggers churn or non-purchase.]

## Competitive & Cultural Context
[What alternatives users consider before or instead of this brand. Why this brand \
wins when it does. Why people churn. 3–5 sentences total.]

## Key Topics Likely to Surface in Simulation
[Exactly 10 numbered items. Format each as a realistic social media post title or \
forum thread subject line that a real user of this product might write. \
Make them specific — no generic "Is X worth it?" questions unless they name the brand.]

## Simulation Configuration Notes

**Spectrum calibration guidance:**
- **Advocates (5%):** [How their conversion story sounds. What kind of posts they write. \
What makes their advocacy credible.]
- **Loyalists (15%):** [Their relationship with the product. How they talk about it \
in context vs. proactively.]
- **Neutrals (50%):** [What they know, what they're curious about, what would move them.]
- **Skeptics (20%):** [Which specific objection drives their skepticism. \
How it shows up in their posts.]
- **Haters (10%):** [The worst-case version of the primary objection. \
What they post, what they amplify.]

**Emotional register:** [1–2 sentences on the dominant emotional tone of social \
discussions about this brand — is it personal, practical, suspicious, hopeful, etc.]

## Simulation Requirement

> [A single paragraph of 4–6 sentences. Start with the brand name. Describe a specific \
moment of brand visibility or social tension — a wave of posts, a feature change, a \
news event, or an organic spike in attention — that sets the simulation in motion. \
Name the competing forces (advocates vs. skeptics, use case believers vs. objectors). \
End by stating what the simulation should surface: which use cases generate the most \
peer advocacy, where the brand is most vulnerable, or what sentiment trajectory emerges.]
"""


def generate_brand_brief(
    brand_name: str,
    brand_url: Optional[str] = None,
    primary_objection: Optional[str] = None,
    advocate_trigger: Optional[str] = None,
    target_segment: Optional[str] = None,
) -> str:
    """Call the LLM to generate a full brand simulation brief.

    Returns the raw markdown string. Raises on API failure.
    """
    client = OpenAI(
        api_key=Config.LLM_API_KEY,
        base_url=Config.LLM_BASE_URL,
    )

    prompt = _BRIEF_PROMPT.format(
        brand_name=brand_name,
        brand_url=brand_url or "N/A",
        primary_objection=primary_objection or "not specified",
        advocate_trigger=advocate_trigger or "not specified",
        target_segment=target_segment or "not specified",
    )

    logger.info("Generating brand brief for '%s'", brand_name)
    response = client.chat.completions.create(
        model=Config.LLM_MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=3000,
    )

    brief = response.choices[0].message.content.strip()
    logger.info("Brand brief generated (%d chars)", len(brief))
    return brief


# ---------------------------------------------------------------------------
# Section extraction helpers
# ---------------------------------------------------------------------------

def _extract_section(brief: str, heading: str) -> str:
    """Return the body of the first `## <heading>` section (stripped)."""
    pattern = rf"## {re.escape(heading)}\n(.*?)(?=\n## |\Z)"
    match = re.search(pattern, brief, re.DOTALL)
    return match.group(1).strip() if match else ""


def extract_simulation_requirement(brief: str) -> str:
    """Return the Simulation Requirement blockquote as plain text."""
    section = _extract_section(brief, "Simulation Requirement")
    if not section:
        return ""
    # Strip leading '>' from blockquote lines
    lines = [re.sub(r"^>\s?", "", line) for line in section.splitlines()]
    return " ".join(line.strip() for line in lines if line.strip())


def extract_use_cases(brief: str) -> str:
    """Return the Primary Use Cases section (truncated for prompt injection)."""
    return _extract_section(brief, "Primary Use Cases (Advocate Triggers)")[:600]


def extract_objections(brief: str) -> str:
    """Return the Primary Objections section (truncated for prompt injection)."""
    return _extract_section(brief, "Primary Objections")[:500]


def extract_topics(brief: str) -> str:
    """Return the Key Topics section (truncated for prompt injection)."""
    return _extract_section(brief, "Key Topics Likely to Surface in Simulation")[:400]


def extract_audience(brief: str) -> str:
    """Return the Target Audience Profile section (truncated)."""
    return _extract_section(brief, "Target Audience Profile")[:400]
