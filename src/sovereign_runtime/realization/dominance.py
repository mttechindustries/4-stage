from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class DominanceAssessment:
    candidate_id: str
    stability: float
    coherence: float
    provenance: float
    reversibility: float
    supply_resilience: float
    mx_readability: float
    dominance_score: float
    confidence: float

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()


class DominanceEvaluator:
    """Scores candidate trajectories for structural dominance."""

    def evaluate(self, candidate_id: str, metrics: dict[str, float]) -> DominanceAssessment:
        stability = float(metrics.get("stability", 0.0))
        coherence = float(metrics.get("coherence", 0.0))
        provenance = float(metrics.get("provenance", 0.0))
        reversibility = float(metrics.get("reversibility", 0.0))
        supply_resilience = float(metrics.get("supply_resilience", 0.0))
        mx_readability = float(metrics.get("mx_readability", 0.0))
        weights = {
            "stability": 0.24,
            "coherence": 0.20,
            "provenance": 0.20,
            "reversibility": 0.12,
            "supply_resilience": 0.12,
            "mx_readability": 0.12,
        }
        dominance = (
            stability * weights["stability"]
            + coherence * weights["coherence"]
            + provenance * weights["provenance"]
            + reversibility * weights["reversibility"]
            + supply_resilience * weights["supply_resilience"]
            + mx_readability * weights["mx_readability"]
        )
        values = [stability, coherence, provenance, reversibility, supply_resilience, mx_readability]
        spread = max(values) - min(values)
        confidence = max(0.0, min(1.0, dominance * (1.0 - spread * 0.35)))
        return DominanceAssessment(candidate_id, stability, coherence, provenance, reversibility, supply_resilience, mx_readability, dominance, confidence)
