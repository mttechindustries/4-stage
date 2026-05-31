from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any

from sovereign_runtime.core import new_id, now_iso


@dataclass
class RuntimeEvent:
    event_id: str
    event_type: str
    subject: str
    payload: dict[str, Any]
    created_at: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class RuntimeLog:
    """Append-only runtime event ledger."""

    def __init__(self) -> None:
        self.events: list[RuntimeEvent] = []

    def append(self, event_type: str, subject: str, payload: dict[str, Any] | None = None) -> RuntimeEvent:
        event = RuntimeEvent(
            event_id=new_id("evt"),
            event_type=event_type,
            subject=subject,
            payload=payload or {},
            created_at=now_iso(),
        )
        self.events.append(event)
        return event

    def list(self) -> list[RuntimeEvent]:
        return list(self.events)

    def to_dict(self) -> dict[str, Any]:
        return {"events": [event.to_dict() for event in self.events]}
