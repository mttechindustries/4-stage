from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class ContinuityAssessment:
    causal_chain_score: float
    provenance_score: float
    state_similarity: float
    anchor_match: bool
    q_value: int
    status: str
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()


class ContinuityChecker:
    """
    Identity/provenance continuity checker.

    Similarity alone is not enough. Q is determined by causal chain and
    provenance continuity first; resemblance cannot override Q=0.
    """

    def __init__(self, causal_threshold: float = 0.75, provenance_threshold: float = 0.75) -> None:
        self.causal_threshold = causal_threshold
        self.provenance_threshold = provenance_threshold

    def assess(
        self,
        *,
        causal_chain_score: float,
        provenance_score: float,
        state_similarity: float,
        anchor_match: bool,
    ) -> ContinuityAssessment:
        if not anchor_match:
            return ContinuityAssessment(
                causal_chain_score,
                provenance_score,
                state_similarity,
                anchor_match,
                0,
                "replica_or_reinstantiation",
                "Anchor mismatch breaks continuity regardless of resemblance.",
            )
        if causal_chain_score < self.causal_threshold:
            return ContinuityAssessment(
                causal_chain_score,
                provenance_score,
                state_similarity,
                anchor_match,
                0,
                "causal_chain_broken",
                "Causal chain below threshold; Q=0 overrides similarity.",
            )
        if provenance_score < self.provenance_threshold:
            return ContinuityAssessment(
                causal_chain_score,
                provenance_score,
                state_similarity,
                anchor_match,
                0,
                "provenance_insufficient",
                "Provenance score below threshold; continuity not established.",
            )
        if state_similarity < 0.45:
            return ContinuityAssessment(
                causal_chain_score,
                provenance_score,
                state_similarity,
                anchor_match,
                1,
                "degraded_continuation",
                "Causal continuity exists but state similarity is degraded.",
            )
        return ContinuityAssessment(
            causal_chain_score,
            provenance_score,
            state_similarity,
            anchor_match,
            1,
            "genuine_continuation",
            "Causal chain, provenance, and anchor continuity established.",
        )
