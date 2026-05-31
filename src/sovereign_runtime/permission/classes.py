from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sovereign_runtime.core import ActionContext, PermissionClass, PermissionDecision
from sovereign_runtime.permission.policies import DEFAULT_TOOL_POLICIES


@dataclass
class ActionPolicy:
    tool: str
    permission_class: PermissionClass
    requires_receipt: bool = True
    veto_available: bool = True
    notes: str = ""


class PermissionPolicyEngine:
    """Policy-backed permission classifier."""

    def __init__(self, policies: dict[str, PermissionClass] | None = None) -> None:
        self.policies = dict(DEFAULT_TOOL_POLICIES)
        if policies:
            self.policies.update(policies)

    def classify(self, context: ActionContext) -> PermissionDecision:
        permission_class = self.policies.get(context.tool, PermissionClass.PREPARE_ACTION)
        text = f"{context.action_description} {' '.join(context.data_sensitivity or [])}".lower()
        if any(marker in text for marker in ["restricted", "sensitive", "irreversible", "external"]):
            permission_class = PermissionClass(min(int(permission_class) + 1, 5))
        return PermissionDecision(
            allowed=not permission_class.blocked_by_default,
            permission_class=permission_class,
            requires_review=permission_class.requires_review,
            requires_confirmation=permission_class.requires_confirmation,
            blocked_by_default=permission_class.blocked_by_default,
            reason=f"{context.tool} classified as {permission_class.label}",
        )

    def register(self, policy: ActionPolicy) -> None:
        self.policies[policy.tool] = policy.permission_class

    def export(self) -> dict[str, Any]:
        return {tool: int(level) for tool, level in self.policies.items()}
