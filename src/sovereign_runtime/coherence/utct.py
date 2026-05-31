from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from sovereign_runtime.coherence.pst import PSTEvaluator


class UTCTStatus(str, Enum):
    COHERENT = "coherent"
    COHERENT_UNDER_PRESSURE = "coherent_under_pressure"
    DEGRADED = "degraded"
    FRACTURED = "fractured"
    COLLAPSED = "collapsed"


@dataclass
class StressScenario:
    name: str
    description: str
    pressure_level: float
    duration: str
    affected_subsystems: list[str] = field(default_factory=list)


@dataclass
class UTCTCoherenceStatus:
    status: UTCTStatus
    sigma_at_rest: float
    sigma_under_pressure: float
    sigma_degradation: float
    fracture_growth: float
    recovery_path: str | None = None
    critical_subsystem: str | None = None
    pressure_scenarios_tested: list[str] = field(default_factory=list)
    traversal_log: list[dict[str, Any]] = field(default_factory=list)

    @property
    def is_coherent(self) -> bool:
        return self.status in (UTCTStatus.COHERENT, UTCTStatus.COHERENT_UNDER_PRESSURE)

    @property
    def is_degraded(self) -> bool:
        return self.status == UTCTStatus.DEGRADED

    @property
    def is_fractured(self) -> bool:
        return self.status in (UTCTStatus.FRACTURED, UTCTStatus.COLLAPSED)

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status.value,
            "sigma_at_rest": self.sigma_at_rest,
            "sigma_under_pressure": self.sigma_under_pressure,
            "sigma_degradation": self.sigma_degradation,
            "fracture_growth": self.fracture_growth,
            "recovery_path": self.recovery_path,
            "critical_subsystem": self.critical_subsystem,
            "pressure_scenarios_tested": self.pressure_scenarios_tested,
            "is_coherent": self.is_coherent,
            "is_degraded": self.is_degraded,
            "is_fractured": self.is_fractured,
        }


class UTCTEvaluator:
    DEFAULT_SCENARIOS: list[StressScenario] = [
        StressScenario("prompt_pressure", "Input stress on intent and routing", 0.6, "acute", ["intent_parser", "tool_router"]),
        StressScenario("supply_interruption", "Dependency becomes unavailable", 0.7, "sustained", ["tool_router", "supply_twin"]),
        StressScenario("veto_load", "Repeated local veto and control checks", 0.5, "chronic", ["permission_gate", "agent_runtime"]),
        StressScenario("model_drift", "Runtime behavior shifts unexpectedly", 0.8, "chronic", ["agent_runtime", "coherence_monitor"]),
        StressScenario("policy_shift", "Requirements change mid-flight", 0.75, "acute", ["compliance_twin", "permission_gate"]),
        StressScenario("data_path_pressure", "Stress on data path and audit trail", 0.9, "acute", ["data_provenance", "export_layer", "audit"]),
    ]

    def __init__(self, pst_evaluator: PSTEvaluator | None = None) -> None:
        self.pst_evaluator = pst_evaluator or PSTEvaluator()
        self._scenarios = list(self.DEFAULT_SCENARIOS)

    def add_scenario(self, scenario: StressScenario) -> None:
        self._scenarios.append(scenario)

    def traverse(self, candidate: dict[str, Any], scenarios: list[StressScenario] | None = None) -> UTCTCoherenceStatus:
        scenarios = scenarios or self._scenarios
        baseline = self.pst_evaluator.evaluate(candidate)
        sigma_at_rest = baseline.sigma
        fracture_at_rest = baseline.fracture_norm
        worst_sigma = sigma_at_rest
        worst_fracture = fracture_at_rest
        critical_subsystem: str | None = None
        traversal_log: list[dict[str, Any]] = []
        tested: list[str] = []

        for scenario in scenarios:
            tested.append(scenario.name)
            pressure_sigma = self._apply_pressure(sigma_at_rest, scenario)
            pressure_fracture = self._apply_fracture_pressure(fracture_at_rest, scenario)
            if pressure_sigma < worst_sigma:
                worst_sigma = pressure_sigma
                critical_subsystem = scenario.affected_subsystems[0] if scenario.affected_subsystems else None
            worst_fracture = max(worst_fracture, pressure_fracture)
            traversal_log.append({
                "scenario": scenario.name,
                "pressure_level": scenario.pressure_level,
                "sigma_under_pressure": pressure_sigma,
                "fracture_under_pressure": pressure_fracture,
                "affected_subsystems": scenario.affected_subsystems,
            })

        sigma_degradation = sigma_at_rest - worst_sigma
        fracture_growth = worst_fracture - fracture_at_rest

        if worst_sigma < 0.5 or worst_fracture > 0.8:
            status = UTCTStatus.COLLAPSED
            recovery = None
        elif worst_sigma < 0.8 or worst_fracture > 0.6:
            status = UTCTStatus.FRACTURED
            recovery = f"Repair critical subsystem: {critical_subsystem}"
        elif sigma_degradation > 0.3 or fracture_growth > 0.2:
            status = UTCTStatus.DEGRADED
            recovery = f"Strengthen subsystem: {critical_subsystem}"
        elif sigma_degradation > 0.1:
            status = UTCTStatus.COHERENT_UNDER_PRESSURE
            recovery = None
        else:
            status = UTCTStatus.COHERENT
            recovery = None

        return UTCTCoherenceStatus(status, sigma_at_rest, worst_sigma, sigma_degradation, fracture_growth, recovery, critical_subsystem, tested, traversal_log)

    def _apply_pressure(self, baseline_sigma: float, scenario: StressScenario) -> float:
        reduction = scenario.pressure_level * 0.4
        if scenario.duration == "chronic":
            reduction *= 1.3
        return max(0.1, baseline_sigma - reduction)

    def _apply_fracture_pressure(self, baseline_fracture: float, scenario: StressScenario) -> float:
        growth = scenario.pressure_level * 0.3
        if scenario.duration == "sustained":
            growth *= 1.2
        return min(1.0, baseline_fracture + growth)
