from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sovereign_runtime.coherence.fracture import FractureTensor, FractureTensorEngine
from sovereign_runtime.coherence.pst import PSTEvaluator, PSTScore


@dataclass
class EmbodimentGateInput:
    candidate: dict[str, Any]
    require_q_gate: bool = False
    q_value: int | None = None
    q_gate_context: dict[str, Any] | None = None


@dataclass
class EmbodimentGateOutput:
    result: str
    pst_score: PSTScore
    fracture_tensor: FractureTensor
    q_gate_passed: bool | None
    recommendation: str
    next_steps: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "result": self.result,
            "pst_score": self.pst_score.to_dict(),
            "fracture_tensor": self.fracture_tensor.to_dict(),
            "q_gate_passed": self.q_gate_passed,
            "recommendation": self.recommendation,
            "next_steps": self.next_steps,
        }


class EmbodimentGate:
    def __init__(self, sigma_threshold: float = 1.0, fracture_threshold: float = 0.5, friction_threshold: float = 0.3) -> None:
        self.pst_evaluator = PSTEvaluator(sigma_threshold, fracture_threshold, friction_threshold)
        self.fracture_engine = FractureTensorEngine()
        self.sigma_threshold = sigma_threshold
        self.fracture_threshold = fracture_threshold
        self.friction_threshold = friction_threshold

    def evaluate(self, input_data: EmbodimentGateInput) -> EmbodimentGateOutput:
        candidate = input_data.candidate
        pst_score = self.pst_evaluator.evaluate(candidate)
        fracture_tensor = self.fracture_engine.analyze(candidate)

        q_passed: bool | None = None
        if input_data.require_q_gate:
            q_passed = input_data.q_value == 1
            if not q_passed:
                return EmbodimentGateOutput(
                    result="FAIL_Q_GATE",
                    pst_score=pst_score,
                    fracture_tensor=fracture_tensor,
                    q_gate_passed=False,
                    recommendation="Q-gate failed. Causal provenance continuity was not established.",
                    next_steps=["Re-establish causal chain", "Verify provenance anchors", "Re-run Q verification"],
                )

        if pst_score.sigma <= self.sigma_threshold:
            return EmbodimentGateOutput(
                result="FAIL_SIGMA",
                pst_score=pst_score,
                fracture_tensor=fracture_tensor,
                q_gate_passed=q_passed,
                recommendation=f"Sigma {pst_score.sigma:.3f} is below threshold {self.sigma_threshold}.",
                next_steps=["Strengthen weakest component", "Add redundancy", "Re-evaluate after repair"],
            )

        if fracture_tensor.frobenius_norm >= self.fracture_threshold:
            repair_plan = self.fracture_engine.synthesize_repair(fracture_tensor)
            return EmbodimentGateOutput(
                result="FAIL_FRACTURE",
                pst_score=pst_score,
                fracture_tensor=fracture_tensor,
                q_gate_passed=q_passed,
                recommendation=f"Fracture norm {fracture_tensor.frobenius_norm:.3f} exceeds threshold {self.fracture_threshold}.",
                next_steps=[
                    f"Execute {repair_plan['repairable_fractures']} repairs",
                    f"Estimated effort: {repair_plan['estimated_total_effort']:.2f}",
                    "Re-evaluate after repair",
                ],
            )

        if pst_score.embodiment_friction >= self.friction_threshold:
            return EmbodimentGateOutput(
                result="FAIL_FRICTION",
                pst_score=pst_score,
                fracture_tensor=fracture_tensor,
                q_gate_passed=q_passed,
                recommendation=f"Embodiment friction {pst_score.embodiment_friction:.3f} is above threshold {self.friction_threshold}.",
                next_steps=["Complete prototype", "Add test coverage", "Complete documentation"],
            )

        return EmbodimentGateOutput(
            result="PASS",
            pst_score=pst_score,
            fracture_tensor=fracture_tensor,
            q_gate_passed=q_passed,
            recommendation="Candidate passes all gates. Proceed to implementation.",
            next_steps=["Begin implementation", "Maintain coherence monitoring", "Schedule re-evaluation"],
        )
