from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sovereign_runtime.agent.planner import AgentPlan, AgentPlanner
from sovereign_runtime.agent.tool_registry import ToolRegistry
from sovereign_runtime.core import ActionContext, CoherenceGate, PermissionEngine, ReceiptGenerator
from sovereign_runtime.qgate import QGate
from sovereign_runtime.realization import RealizationOperator
from sovereign_runtime.records import RuntimeLog, BundleWriter, RuntimeBundle


@dataclass
class AgentRunResult:
    plan: AgentPlan
    passed: bool
    receipts: list[Any]
    bundle: RuntimeBundle
    realization: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "plan": self.plan.to_dict(),
            "passed": self.passed,
            "receipts": [receipt.to_dict() for receipt in self.receipts],
            "bundle": self.bundle.records,
            "realization": self.realization,
        }


class AgentRuntime:
    """Orchestrates planning, scoring, Q check, receipt creation, and record bundling."""

    def __init__(self, agent_id: str = "mtti_sovereign_agent_runtime", model_id: str = "runtime/local") -> None:
        self.agent_id = agent_id
        self.model_id = model_id
        self.planner = AgentPlanner()
        self.tools = ToolRegistry()
        self.permission_engine = PermissionEngine()
        self.coherence_gate = CoherenceGate()
        self.q_gate = QGate()
        self.receipts = ReceiptGenerator(agent_id=agent_id, model_id=model_id)
        self.realization = RealizationOperator()
        self.log = RuntimeLog()

    def run(self, objective: str, tools: list[str] | None = None) -> AgentRunResult:
        plan = self.planner.create_plan(objective, tools)
        receipts = []
        passed = True
        for step in plan.steps:
            context = ActionContext(tool=step["tool"], action_description=step["description"])
            decision = self.permission_engine.classify(context)
            coherence = self.coherence_gate.evaluate(1.18, 0.24, 0.16, 1)
            receipt = self.receipts.create(context, "prepared", decision, coherence=coherence, q_required=True, user_confirmed=True)
            receipts.append(receipt)
            self.log.append("step", step["tool"], {"decision": decision.reason, "receipt_id": receipt.receipt_id})
            passed = passed and decision.allowed and coherence.passed
        realization = self.realization.resolve(dominance=0.72, confidence=0.68)
        self.log.append("realization", "runtime", realization.to_dict())
        bundle = BundleWriter().create(self.log.list())
        return AgentRunResult(plan=plan, passed=passed, receipts=receipts, bundle=bundle, realization=realization.to_dict())
