from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sovereign_runtime.qgate.continuity import ContinuityAssessment, ContinuityChecker


@dataclass
class QGateResult:
    q_value: int
    passed: bool
    status: str
    reason: str
    assessment: ContinuityAssessment

    def to_dict(self) -> dict[str, Any]:
        return {
            "q_value": self.q_value,
            "passed": self.passed,
            "status": self.status,
            "reason": self.reason,
            "assessment": self.assessment.to_dict(),
        }


class QGate:
    """
    Hard binary causal provenance gate.

    Q=1 means continuity is causally established.
    Q=0 means the result is replica-like or re-instantiated, even if it resembles
    the expected state.
    """

    def __init__(self, checker: ContinuityChecker | None = None) -> None:
        self.checker = checker or ContinuityChecker()

    def evaluate(
        self,
        *,
        causal_chain_score: float,
        provenance_score: float,
        state_similarity: float,
        anchor_match: bool,
    ) -> QGateResult:
        assessment = self.checker.assess(
            causal_chain_score=causal_chain_score,
            provenance_score=provenance_score,
            state_similarity=state_similarity,
            anchor_match=anchor_match,
        )
        return QGateResult(
            q_value=assessment.q_value,
            passed=assessment.q_value == 1,
            status=assessment.status,
            reason=assessment.reason,
            assessment=assessment,
        )

    def require_pass(self, **kwargs: Any) -> QGateResult:
        result = self.evaluate(**kwargs)
        if not result.passed:
            raise ValueError(f"Q Gate failed: {result.status} — {result.reason}")
        return result
