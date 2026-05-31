from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from sovereign_runtime.core import new_id


@dataclass
class AgentPlan:
    plan_id: str
    objective: str
    steps: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {"plan_id": self.plan_id, "objective": self.objective, "steps": self.steps}


class AgentPlanner:
    """Creates bounded multi-step plans for the runtime."""

    def create_plan(self, objective: str, requested_tools: list[str] | None = None) -> AgentPlan:
        tools = requested_tools or ["workflow.stage"]
        steps = [
            {"order": index + 1, "tool": tool, "description": f"Use {tool} for objective segment {index + 1}"}
            for index, tool in enumerate(tools)
        ]
        return AgentPlan(plan_id=new_id("plan"), objective=objective, steps=steps)
