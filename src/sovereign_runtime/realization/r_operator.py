from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sovereign_runtime.realization.dominance import DominanceAssessment, DominanceEvaluator


@dataclass
class RealizationResult:
    realization_type: str
    selected_candidate: str | None
    dominance_score: float
    confidence: float
    reason: str
    assessment: DominanceAssessment | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "realization_type": self.realization_type,
            "selected_candidate": self.selected_candidate,
            "dominance_score": self.dominance_score,
            "confidence": self.confidence,
            "reason": self.reason,
            "assessment": self.assessment.to_dict() if self.assessment else None,
        }


class RealizationOperator:
    """
    Resolves which validated future trajectory is structurally actualizing.

    It does not merely list possibilities. It classifies the realization regime:
    point, regional, trajectory, fractured, or no-dominance.
    """

    def __init__(self, evaluator: DominanceEvaluator | None = None) -> None:
        self.evaluator = evaluator or DominanceEvaluator()

    def resolve(self, candidates: dict[str, dict[str, float]] | None = None, *, dominance: float | None = None, confidence: float | None = None) -> RealizationResult:
        if candidates:
            assessments = [self.evaluator.evaluate(candidate_id, metrics) for candidate_id, metrics in candidates.items()]
            assessments.sort(key=lambda item: item.dominance_score, reverse=True)
            top = assessments[0]
            second = assessments[1] if len(assessments) > 1 else None
            separation = top.dominance_score - (second.dominance_score if second else 0.0)
            return self._classify(top.dominance_score, top.confidence, top.candidate_id, separation, top)

        if dominance is None or confidence is None:
            raise ValueError("Provide either candidates or dominance/confidence.")
        return self._classify(dominance, confidence, None, 1.0, None)

    def _classify(self, dominance: float, confidence: float, candidate_id: str | None, separation: float, assessment: DominanceAssessment | None) -> RealizationResult:
        if dominance >= 0.82 and confidence >= 0.75 and separation >= 0.12:
            return RealizationResult("point_realization", candidate_id, dominance, confidence, "One trajectory is structurally dominant.", assessment)
        if dominance >= 0.60 and confidence >= 0.55:
            return RealizationResult("regional_realization", candidate_id, dominance, confidence, "A stable region exists, but point selection is not fully resolved.", assessment)
        if dominance >= 0.42:
            return RealizationResult("trajectory_realization", candidate_id, dominance, confidence, "A trajectory is emerging but requires continued observation.", assessment)
        if confidence < 0.35:
            return RealizationResult("no_dominance", None, dominance, confidence, "No reliable dominance relation is established.", assessment)
        return RealizationResult("fractured_realization", candidate_id, dominance, confidence, "The realization field is fractured; forced certainty would be false precision.", assessment)
