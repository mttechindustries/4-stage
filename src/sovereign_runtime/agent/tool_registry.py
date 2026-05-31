from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class ToolDefinition:
    name: str
    description: str
    handler: Callable[..., Any] | None = None
    metadata: dict[str, Any] | None = None


class ToolRegistry:
    """Registry for runtime tool definitions."""

    def __init__(self) -> None:
        self.tools: dict[str, ToolDefinition] = {}

    def register(self, tool: ToolDefinition) -> None:
        self.tools[tool.name] = tool

    def get(self, name: str) -> ToolDefinition | None:
        return self.tools.get(name)

    def names(self) -> list[str]:
        return sorted(self.tools)

    def to_dict(self) -> dict[str, Any]:
        return {
            name: {"description": tool.description, "metadata": tool.metadata or {}}
            for name, tool in self.tools.items()
        }
