from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sovereign_runtime.core import ActionContext, PermissionDecision
from sovereign_runtime.permission.classes import PermissionPolicyEngine


@dataclass
class PermissionGateResult:
    passed: bool
    decision: PermissionDecision
    review_available: bool
    confirmation_required: bool
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "permission_class": int(self.decision.permission_class),
            "review_available": self.review_available,
            "confirmation_required": self.confirmation_required,
            "reason": self.reason,
        }


class PermissionGate:
    """Runtime boundary between plan and tool use."""

    def __init__(self, engine: PermissionPolicyEngine | None = None) -> None:
        self.engine = engine or PermissionPolicyEngine()

    def check(self, context: ActionContext, *, user_confirmed: bool | None = None, stop_requested: bool = False) -> PermissionGateResult:
        decision = self.engine.classify(context)
        if stop_requested:
            return PermissionGateResult(False, decision, True, decision.requires_confirmation, "user_stop_requested")
        if decision.blocked_by_default:
            return PermissionGateResult(False, decision, True, True, "blocked_by_default")
        if decision.requires_confirmation and user_confirmed is not True:
            return PermissionGateResult(False, decision, True, True, "confirmation_required")
        return PermissionGateResult(True, decision, True, decision.requires_confirmation, decision.reason)
