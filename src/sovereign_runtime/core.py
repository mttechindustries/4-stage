from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from enum import Enum, IntEnum
import hashlib
import json
import secrets
from typing import Any


class PermissionClass(IntEnum):
    READ_ONLY = 0
    DRAFT_RECOMMEND = 1
    PREPARE_ACTION = 2
    REVERSIBLE_ACTION = 3
    HIGH_RISK_ACTION = 4
    RESTRICTED_ACTION = 5

    @property
    def label(self) -> str:
        return {
            0: "read-only",
            1: "draft-recommend",
            2: "prepare-action",
            3: "reversible-action",
            4: "high-risk-action",
            5: "restricted-action",
        }[int(self)]

    @property
    def requires_review(self) -> bool:
        return int(self) >= 2

    @property
    def requires_confirmation(self) -> bool:
        return int(self) >= 3

    @property
    def blocked_by_default(self) -> bool:
        return int(self) >= 5


class RealizationType(str, Enum):
    POINT = "point_realization"
    REGIONAL = "regional_realization"
    TRAJECTORY = "trajectory_realization"
    FRACTURED = "fractured_realization"
    NO_DOMINANCE = "no_dominance"


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_digest(value: str | bytes) -> str:
    if isinstance(value, str):
        value = value.encode("utf-8")
    return "sha256:" + hashlib.sha256(value).hexdigest()


def new_id(prefix: str) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    return f"{prefix}_{stamp}_{secrets.token_hex(4)}"


@dataclass
class ActionContext:
    tool: str
    action_description: str
    parameters: dict[str, Any] | None = None
    data_sensitivity: list[str] | None = None


@dataclass
class PermissionDecision:
    allowed: bool
    permission_class: PermissionClass
    requires_review: bool
    requires_confirmation: bool
    blocked_by_default: bool
    reason: str


class PermissionEngine:
    TOOL_RULES: dict[str, PermissionClass] = {
        "search.query": PermissionClass.READ_ONLY,
        "file.read": PermissionClass.READ_ONLY,
        "document.draft": PermissionClass.DRAFT_RECOMMEND,
        "report.generate": PermissionClass.DRAFT_RECOMMEND,
        "workflow.stage": PermissionClass.PREPARE_ACTION,
        "file.write": PermissionClass.REVERSIBLE_ACTION,
        "deployment.push": PermissionClass.HIGH_RISK_ACTION,
    }

    def classify(self, context: ActionContext) -> PermissionDecision:
        permission_class = self.TOOL_RULES.get(context.tool, PermissionClass.PREPARE_ACTION)
        text = f"{context.action_description} {' '.join(context.data_sensitivity or [])}".lower()
        if any(word in text for word in ["restricted", "sensitive", "irreversible", "external"]):
            permission_class = PermissionClass(min(int(permission_class) + 1, 5))
        return PermissionDecision(
            allowed=not permission_class.blocked_by_default,
            permission_class=permission_class,
            requires_review=permission_class.requires_review,
            requires_confirmation=permission_class.requires_confirmation,
            blocked_by_default=permission_class.blocked_by_default,
            reason=f"{context.tool} classified as {permission_class.label}",
        )


@dataclass
class CoherenceResult:
    sigma: float
    fracture_norm: float
    embodiment_friction: float
    q_value: int | None
    passed: bool
    result: str


class CoherenceGate:
    def __init__(self, sigma_min: float = 1.0, fracture_max: float = 0.35, friction_max: float = 0.30) -> None:
        self.sigma_min = sigma_min
        self.fracture_max = fracture_max
        self.friction_max = friction_max

    def evaluate(self, sigma: float, fracture_norm: float, embodiment_friction: float, q_value: int | None = None) -> CoherenceResult:
        if q_value == 0:
            return CoherenceResult(sigma, fracture_norm, embodiment_friction, q_value, False, "FAIL_Q_GATE")
        if sigma <= self.sigma_min:
            return CoherenceResult(sigma, fracture_norm, embodiment_friction, q_value, False, "FAIL_SIGMA")
        if fracture_norm >= self.fracture_max:
            return CoherenceResult(sigma, fracture_norm, embodiment_friction, q_value, False, "FAIL_FRACTURE")
        if embodiment_friction >= self.friction_max:
            return CoherenceResult(sigma, fracture_norm, embodiment_friction, q_value, False, "FAIL_FRICTION")
        return CoherenceResult(sigma, fracture_norm, embodiment_friction, q_value, True, "PASS")


@dataclass
class EAReceipt:
    receipt_version: str
    receipt_id: str
    action_id: str
    session_id: str
    agent_id: str
    model_id: str
    tool_used: str
    permission_class: int
    user_veto_available: bool
    user_confirmed: bool | None
    prompt_hash: str
    output_hash: str
    derivative_created: bool
    export_available: bool
    rollback_available: bool
    coherence: dict[str, Any] | None
    q_gate: dict[str, Any]
    created_at: str

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2, sort_keys=True)


class ReceiptGenerator:
    def __init__(self, agent_id: str = "mtti_sovereign_agent_runtime", model_id: str = "runtime/local") -> None:
        self.agent_id = agent_id
        self.model_id = model_id
        self.session_id = new_id("sess")

    def create(self, context: ActionContext, output: str, decision: PermissionDecision, prompt: str = "", coherence: CoherenceResult | None = None, q_required: bool = False, user_confirmed: bool | None = None) -> EAReceipt:
        return EAReceipt(
            receipt_version="0.1",
            receipt_id=new_id("rcpt"),
            action_id=new_id("act"),
            session_id=self.session_id,
            agent_id=self.agent_id,
            model_id=self.model_id,
            tool_used=context.tool,
            permission_class=int(decision.permission_class),
            user_veto_available=True,
            user_confirmed=user_confirmed,
            prompt_hash=sha256_digest(prompt or context.action_description),
            output_hash=sha256_digest(output),
            derivative_created=True,
            export_available=True,
            rollback_available=int(decision.permission_class) <= 3,
            coherence=asdict(coherence) if coherence else None,
            q_gate={"required": q_required, "q_value": coherence.q_value if coherence else None},
            created_at=now_iso(),
        )


class RealizationOperator:
    def resolve(self, dominance: float, confidence: float) -> dict[str, Any]:
        if dominance >= 0.82 and confidence >= 0.75:
            kind = RealizationType.POINT
        elif dominance >= 0.55 and confidence >= 0.55:
            kind = RealizationType.REGIONAL
        elif dominance >= 0.35:
            kind = RealizationType.TRAJECTORY
        elif confidence < 0.35:
            kind = RealizationType.NO_DOMINANCE
        else:
            kind = RealizationType.FRACTURED
        return {"realization_type": kind.value, "dominance": dominance, "confidence": confidence}
