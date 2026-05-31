from __future__ import annotations

from dataclasses import asdict
from typing import Any

from sovereign_runtime.core import ActionContext, PermissionDecision, new_id, now_iso, sha256_digest
from sovereign_runtime.receipts.schema import EAReceiptRecord


class EAReceiptGenerator:
    """Generates EA Receipt Protocol records with hash chaining."""

    def __init__(self, agent_id: str = "mtti_sovereign_agent_runtime", model_id: str = "runtime/local") -> None:
        self.agent_id = agent_id
        self.model_id = model_id
        self.session_id = new_id("sess")
        self.previous_receipt_hash: str | None = None

    def create(
        self,
        context: ActionContext,
        output: str,
        decision: PermissionDecision,
        *,
        prompt: str | None = None,
        source_refs: list[str] | None = None,
        data_sources_used: list[str] | None = None,
        retention_status: str = "user-controlled",
        q_gate: dict[str, Any] | None = None,
        coherence: Any | None = None,
        user_confirmed: bool | None = None,
    ) -> EAReceiptRecord:
        coherence_payload = None
        if coherence is not None:
            coherence_payload = asdict(coherence) if hasattr(coherence, "__dataclass_fields__") else dict(coherence)

        record = EAReceiptRecord(
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
            source_refs=source_refs or [],
            data_sources_used=data_sources_used or [],
            derivative_created=True,
            retention_status=retention_status,
            export_available=True,
            rollback_available=int(decision.permission_class) <= 3,
            q_gate=q_gate or {"required": False, "q_value": None},
            coherence=coherence_payload,
            created_at=now_iso(),
            previous_receipt_hash=self.previous_receipt_hash,
        )
        record.receipt_hash = sha256_digest(record.to_json())
        self.previous_receipt_hash = record.receipt_hash
        return record
