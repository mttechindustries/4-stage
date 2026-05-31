from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class PSTScore:
    sigma: float = 0.0
    fracture_norm: float = 0.0
    embodiment_friction: float = 0.0
    component_scores: dict[str, float] = field(default_factory=dict)
    evaluation_timestamp: str = ""
    sigma_threshold: float = 1.0
    fracture_threshold: float = 0.5
    friction_threshold: float = 0.3

    @property
    def is_survivable(self) -> bool:
        return self.sigma > self.sigma_threshold

    @property
    def is_fracture_acceptable(self) -> bool:
        return self.fracture_norm < self.fracture_threshold

    @property
    def is_friction_acceptable(self) -> bool:
        return self.embodiment_friction < self.friction_threshold

    @property
    def passes_all(self) -> bool:
        return self.is_survivable and self.is_fracture_acceptable and self.is_friction_acceptable

    def to_dict(self) -> dict[str, Any]:
        return {
            "sigma": self.sigma,
            "fracture_norm": self.fracture_norm,
            "embodiment_friction": self.embodiment_friction,
            "is_survivable": self.is_survivable,
            "is_fracture_acceptable": self.is_fracture_acceptable,
            "is_friction_acceptable": self.is_friction_acceptable,
            "passes_all": self.passes_all,
            "component_scores": self.component_scores,
        }


class PSTEvaluator:
    def __init__(self, sigma_threshold: float = 1.0, fracture_threshold: float = 0.5, friction_threshold: float = 0.3) -> None:
        self.sigma_threshold = sigma_threshold
        self.fracture_threshold = fracture_threshold
        self.friction_threshold = friction_threshold
        self._component_evaluators: dict[str, Callable[[dict[str, Any]], float]] = {}

    def register_component_evaluator(self, name: str, evaluator: Callable[[dict[str, Any]], float]) -> None:
        self._component_evaluators[name] = evaluator

    def evaluate(self, candidate: dict[str, Any]) -> PSTScore:
        architecture = candidate.get("architecture", {})
        dependencies = candidate.get("dependencies", [])
        risk_factors = candidate.get("risk_factors", [])
        test_coverage = float(candidate.get("test_coverage", 0.0))
        sovereignty_score = float(candidate.get("user_sovereignty_score", 0.0))
        provenance = float(candidate.get("provenance_completeness", 0.0))

        component_scores: dict[str, float] = {
            "architecture": self._score_architecture(architecture),
            "dependencies": self._score_dependencies(dependencies),
            "risk_mitigation": self._score_risks(risk_factors),
            "test_coverage": test_coverage,
            "user_sovereignty": sovereignty_score,
            "provenance": provenance,
        }

        for name, evaluator in self._component_evaluators.items():
            component_scores[name] = float(evaluator(candidate))

        log_sum = sum(math.log(max(s, 0.001)) for s in component_scores.values())
        sigma = math.exp(log_sum / len(component_scores))

        mean = sum(component_scores.values()) / len(component_scores)
        variance = sum((s - mean) ** 2 for s in component_scores.values()) / len(component_scores)
        fracture = math.sqrt(variance)
        friction = self._compute_friction(candidate, component_scores)

        return PSTScore(
            sigma=sigma,
            fracture_norm=fracture,
            embodiment_friction=friction,
            component_scores=component_scores,
            sigma_threshold=self.sigma_threshold,
            fracture_threshold=self.fracture_threshold,
            friction_threshold=self.friction_threshold,
        )

    def _score_architecture(self, architecture: dict[str, Any]) -> float:
        if not architecture:
            return 0.3
        scores = [0.8 if isinstance(config, dict) else 0.5 for config in architecture.values()]
        return sum(scores) / len(scores)

    def _score_dependencies(self, dependencies: list[Any]) -> float:
        if not dependencies:
            return 1.0
        base = max(0.2, 1.0 - (len(dependencies) * 0.05))
        concentrated = sum(1 for item in dependencies if isinstance(item, dict) and item.get("single_source", False))
        return max(0.1, base - (concentrated * 0.2))

    def _score_risks(self, risk_factors: list[Any]) -> float:
        if not risk_factors:
            return 0.7
        mitigated = sum(1 for item in risk_factors if isinstance(item, dict) and item.get("mitigated", False))
        return mitigated / len(risk_factors)

    def _compute_friction(self, candidate: dict[str, Any], component_scores: dict[str, float]) -> float:
        friction = 0.0
        if not candidate.get("has_prototype", False):
            friction += 0.3
        if float(candidate.get("test_coverage", 0.0)) <= 0.5:
            friction += 0.2
        if not candidate.get("documentation_complete", False):
            friction += 0.15
        mean = sum(component_scores.values()) / len(component_scores)
        variance = sum((s - mean) ** 2 for s in component_scores.values()) / len(component_scores)
        return min(friction + variance * 0.5, 1.0)

    def evaluate_with_gate(self, candidate: dict[str, Any]) -> tuple[PSTScore, str]:
        score = self.evaluate(candidate)
        if score.sigma <= self.sigma_threshold:
            return score, "FAIL_SIGMA"
        if score.fracture_norm >= self.fracture_threshold:
            return score, "FAIL_FRACTURE"
        if score.embodiment_friction >= self.friction_threshold:
            return score, "FAIL_FRICTION"
        return score, "PASS"
