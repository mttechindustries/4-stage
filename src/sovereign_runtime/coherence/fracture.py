from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any


@dataclass
class FractureComponent:
    subsystem: str
    fracture_type: str
    severity: float
    description: str
    repairable: bool = True
    repair_cost: float = 0.5


@dataclass
class FractureTensor:
    components: list[FractureComponent] = field(default_factory=list)

    @property
    def frobenius_norm(self) -> float:
        if not self.components:
            return 0.0
        return math.sqrt(sum(component.severity ** 2 for component in self.components))

    @property
    def max_severity(self) -> float:
        if not self.components:
            return 0.0
        return max(component.severity for component in self.components)

    @property
    def repairable_fraction(self) -> float:
        if not self.components:
            return 1.0
        repairable = sum(1 for component in self.components if component.repairable)
        return repairable / len(self.components)

    @property
    def critical_fractures(self) -> list[FractureComponent]:
        return [component for component in self.components if component.severity > 0.7]

    def to_dict(self) -> dict[str, Any]:
        return {
            "frobenius_norm": self.frobenius_norm,
            "max_severity": self.max_severity,
            "repairable_fraction": self.repairable_fraction,
            "component_count": len(self.components),
            "critical_count": len(self.critical_fractures),
            "components": [component.__dict__ for component in self.components],
        }


class FractureTensorEngine:
    FRACTURE_PATTERNS: dict[str, dict[str, Any]] = {
        "ux_confusion": {"subsystem": "ux", "fracture_type": "cognitive_load", "description": "User cannot understand runtime output"},
        "trust_gap": {"subsystem": "trust", "fracture_type": "provenance_missing", "description": "No provenance receipt for action"},
        "supply_single_source": {"subsystem": "supply", "fracture_type": "dependency_concentration", "description": "Single-source dependency creates fragility"},
        "compliance_ambiguity": {"subsystem": "compliance", "fracture_type": "boundary_unclear", "description": "Unclear consent or operating boundary"},
        "autonomy_overreach": {"subsystem": "autonomy", "fracture_type": "authority_mismatch", "description": "Runtime action lacks local veto path"},
        "data_trap": {"subsystem": "data", "fracture_type": "export_failure", "description": "No export or delete proof available"},
        "mx_unreadable": {"subsystem": "launch", "fracture_type": "machine_opacity", "description": "Machine readers cannot cite source docs"},
        "coherence_drift": {"subsystem": "coherence", "fracture_type": "stability_decay", "description": "Stability scores degrade without detection"},
        "q_gate_bypass": {"subsystem": "identity", "fracture_type": "continuity_failure", "description": "Continuity not Q-gated"},
    }

    def __init__(self) -> None:
        self._custom_patterns: dict[str, dict[str, Any]] = {}

    def register_pattern(self, name: str, pattern: dict[str, Any]) -> None:
        self._custom_patterns[name] = pattern

    def analyze(self, candidate: dict[str, Any]) -> FractureTensor:
        components: list[FractureComponent] = []
        for pattern in {**self.FRACTURE_PATTERNS, **self._custom_patterns}.values():
            severity = self._evaluate_pattern(pattern, candidate)
            if severity > 0.0:
                components.append(FractureComponent(
                    subsystem=pattern["subsystem"],
                    fracture_type=pattern["fracture_type"],
                    severity=severity,
                    description=pattern["description"],
                    repairable=severity < 0.9,
                    repair_cost=min(1.0, severity * 1.2),
                ))
        components.extend(self._analyze_integrations(candidate))
        return FractureTensor(components=components)

    def _evaluate_pattern(self, pattern: dict[str, Any], candidate: dict[str, Any]) -> float:
        subsystem = pattern["subsystem"]
        config = candidate.get("architecture", {}).get(subsystem, {})
        if not config:
            return 0.7
        mitigations = config.get("mitigations", []) if isinstance(config, dict) else []
        if mitigations:
            return max(0.1, 0.7 - (len(mitigations) * 0.15))
        return 0.5

    def _analyze_integrations(self, candidate: dict[str, Any]) -> list[FractureComponent]:
        components: list[FractureComponent] = []
        architecture = candidate.get("architecture", {})
        required = [("permission", "audit"), ("agent", "receipts"), ("coherence", "qgate"), ("data", "export")]
        for left, right in required:
            if left in architecture and right in architecture:
                config = architecture.get(left, {})
                linked = isinstance(config, dict) and config.get(f"integrates_with_{right}", False)
                if not linked:
                    components.append(FractureComponent(f"{left}-{right}", "integration_gap", 0.4, f"Missing integration between {left} and {right}", True, 0.3))
        return components

    def synthesize_repair(self, tensor: FractureTensor) -> dict[str, Any]:
        components = sorted(tensor.components, key=lambda item: (item.severity, -item.repair_cost), reverse=True)
        repairs = []
        for component in components:
            if component.repairable:
                repairs.append({
                    "priority": "critical" if component.severity > 0.7 else "high" if component.severity > 0.5 else "medium",
                    "subsystem": component.subsystem,
                    "fracture_type": component.fracture_type,
                    "action": f"Address {component.description}",
                    "estimated_effort": component.repair_cost,
                    "severity": component.severity,
                })
        return {
            "total_fractures": len(tensor.components),
            "repairable_fractures": len(repairs),
            "estimated_total_effort": sum(repair["estimated_effort"] for repair in repairs),
            "repairs": repairs,
        }
