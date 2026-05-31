from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any
import json

ReceiptHash = str


@dataclass
class EAReceiptRecord:
    """EA Receipt Protocol record.

    The receipt answers: what happened, under what authority, using what
    evidence, with what derivative output, and with what ability to veto,
    export, or roll back.
    """

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
    prompt_hash: ReceiptHash
    output_hash: ReceiptHash
    source_refs: list[str]
    data_sources_used: list[str]
    derivative_created: bool
    retention_status: str
    export_available: bool
    rollback_available: bool
    q_gate: dict[str, Any]
    coherence: dict[str, Any] | None
    created_at: str
    previous_receipt_hash: ReceiptHash | None = None
    receipt_hash: ReceiptHash | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, sort_keys=True)

    @classmethod
    def from_json(cls, payload: str) -> "EAReceiptRecord":
        return cls(**json.loads(payload))
