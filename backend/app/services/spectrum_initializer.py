"""
Advocate-to-hater spectrum initializer for marketing simulations.

Assigns each agent to one of five audience cohorts and calibrates their
behavioral parameters (sentiment_bias, stance, influence_weight,
activity_level) accordingly.

Distribution: 5% advocates / 15% loyalists / 50% neutrals / 20% skeptics / 10% haters
"""

import random
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Tuple


class CohortType(str, Enum):
    ADVOCATE = "advocate"
    LOYALIST = "loyalist"
    NEUTRAL = "neutral"
    SKEPTIC = "skeptic"
    HATER = "hater"


# Weighted distribution: (cohort, weight)
COHORT_WEIGHTS: List[Tuple[CohortType, float]] = [
    (CohortType.ADVOCATE, 0.05),
    (CohortType.LOYALIST, 0.15),
    (CohortType.NEUTRAL, 0.50),
    (CohortType.SKEPTIC, 0.20),
    (CohortType.HATER, 0.10),
]

_COHORT_NAMES = [c for c, _ in COHORT_WEIGHTS]
_COHORT_PROBS = [w for _, w in COHORT_WEIGHTS]


@dataclass
class CohortCalibration:
    """Behavioral calibration ranges for a cohort."""
    sentiment_bias_range: Tuple[float, float]   # (min, max)
    stance: str                                  # OASIS stance field
    influence_weight_range: Tuple[float, float]
    activity_level_range: Tuple[float, float]
    persona_hint: str                            # Injected into LLM persona prompt


COHORT_CALIBRATION = {
    CohortType.ADVOCATE: CohortCalibration(
        sentiment_bias_range=(0.7, 1.0),
        stance="supportive",
        influence_weight_range=(2.0, 3.0),
        activity_level_range=(0.7, 0.9),
        persona_hint=(
            "This person is a genuine brand advocate. They've had a strongly positive experience "
            "and actively recommend the brand to others. They post enthusiastically, defend the "
            "brand against criticism, and are among the first to share good news about it."
        ),
    ),
    CohortType.LOYALIST: CohortCalibration(
        sentiment_bias_range=(0.3, 0.65),
        stance="supportive",
        influence_weight_range=(1.2, 1.8),
        activity_level_range=(0.5, 0.7),
        persona_hint=(
            "This person is a satisfied, loyal customer. They use the product regularly and "
            "think it's good value. They don't evangelize aggressively but will speak positively "
            "when the topic comes up and occasionally share positive experiences."
        ),
    ),
    CohortType.NEUTRAL: CohortCalibration(
        sentiment_bias_range=(-0.15, 0.15),
        stance="neutral",
        influence_weight_range=(0.8, 1.2),
        activity_level_range=(0.3, 0.6),
        persona_hint=(
            "This person is undecided about the brand. They may be considering it, vaguely "
            "aware of it, or have had a mixed experience. They are open to being persuaded in "
            "either direction. Their posts tend to ask questions, compare options, or express "
            "mild curiosity without strong feelings."
        ),
    ),
    CohortType.SKEPTIC: CohortCalibration(
        sentiment_bias_range=(-0.5, -0.2),
        stance="opposing",
        influence_weight_range=(0.8, 1.3),
        activity_level_range=(0.5, 0.7),
        persona_hint=(
            "This person is skeptical of the brand. They have concerns — typically around cost, "
            "value-for-money, or trustworthiness — and haven't been convinced yet. They are not "
            "hostile but express doubt, ask pointed questions, and are more likely to share "
            "cautious or negative impressions than positive ones."
        ),
    ),
    CohortType.HATER: CohortCalibration(
        sentiment_bias_range=(-1.0, -0.55),
        stance="opposing",
        influence_weight_range=(1.5, 2.5),
        activity_level_range=(0.6, 0.85),
        persona_hint=(
            "This person actively dislikes the brand. They may have had a bad experience, "
            "distrust the company's practices, or strongly object to its pricing or privacy "
            "policies. They post critically and will amplify negative news. They are vocal "
            "and their negative sentiment influences others around them."
        ),
    ),
}


@dataclass
class BrandContext:
    """Optional brand context that sharpens cohort persona prompts."""
    brand_name: str
    primary_objection: Optional[str] = None    # e.g. "cost and privacy concerns"
    advocate_trigger: Optional[str] = None     # e.g. "reconnecting with lost contacts"
    target_segment: Optional[str] = None       # e.g. "conscious consumer"


@dataclass
class CohortAssignment:
    cohort: CohortType
    sentiment_bias: float
    stance: str
    influence_weight: float
    activity_level: float


def assign_cohorts(n: int, seed: Optional[int] = None) -> List[CohortAssignment]:
    """
    Assign n agents to cohorts using the 5/15/50/20/10 distribution.
    Returns one CohortAssignment per agent, values sampled uniformly
    within each cohort's calibration range.
    """
    rng = random.Random(seed)

    cohorts = rng.choices(_COHORT_NAMES, weights=_COHORT_PROBS, k=n)

    assignments = []
    for cohort in cohorts:
        cal = COHORT_CALIBRATION[cohort]
        assignments.append(CohortAssignment(
            cohort=cohort,
            sentiment_bias=round(rng.uniform(*cal.sentiment_bias_range), 3),
            stance=cal.stance,
            influence_weight=round(rng.uniform(*cal.influence_weight_range), 3),
            activity_level=round(rng.uniform(*cal.activity_level_range), 3),
        ))

    return assignments


def build_cohort_persona_context(
    assignment: CohortAssignment,
    brand_context: Optional[BrandContext] = None,
) -> str:
    """
    Returns a paragraph to inject into the LLM persona prompt so that
    the generated bio/persona text aligns with the assigned cohort stance.
    """
    cal = COHORT_CALIBRATION[assignment.cohort]
    lines = [
        f"Audience cohort: {assignment.cohort.value}",
        "",
        cal.persona_hint,
    ]

    if brand_context:
        lines.append("")
        lines.append(f"Brand being evaluated: {brand_context.brand_name}")

        if assignment.cohort in (CohortType.SKEPTIC, CohortType.HATER) and brand_context.primary_objection:
            lines.append(
                f"Their core objection centers on: {brand_context.primary_objection}. "
                "Make sure this tension shows up naturally in how they speak and what they post."
            )
        elif assignment.cohort in (CohortType.ADVOCATE, CohortType.LOYALIST) and brand_context.advocate_trigger:
            lines.append(
                f"The key value they get from the brand: {brand_context.advocate_trigger}. "
                "This is what they highlight and evangelize."
            )
        elif assignment.cohort == CohortType.NEUTRAL:
            parts = []
            if brand_context.advocate_trigger:
                parts.append(f"potential upside: {brand_context.advocate_trigger}")
            if brand_context.primary_objection:
                parts.append(f"concerns they've heard: {brand_context.primary_objection}")
            if parts:
                lines.append(
                    f"They're weighing {' and '.join(parts)}. "
                    "They haven't made up their mind."
                )

        if brand_context.target_segment:
            lines.append(
                f"This person fits the target segment profile of: {brand_context.target_segment}."
            )

    return "\n".join(lines)
