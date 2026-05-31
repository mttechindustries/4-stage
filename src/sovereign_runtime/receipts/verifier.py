from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sovereign_runtime.core import sha256_digest
from sovereign_runtime.receipts.schema import EAReceiptRecord


@dataclass
class ReceiptVerification:
    valid: bool
    schema_valid: bool
    hash_valid: bool
    chain_reference_present: bool
    errors: list[str]

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()


class EAReceiptVerifier:
    """Verifies receipt shape and hash integrity."""

    def verify(self, receipt: EAReceiptRecord) -> ReceiptVerification:
        errors: list[str] = []
        required = [
            receipt.receipt_version,
            receipt.receipt_id,
            receipt.action_id,
            receipt.session_id,
            receipt.agent_id,
            receipt.model_id,
            receipt.tool_used,
            receipt.prompt_hash,
            receipt.output_hash,
            receipt.created_at,
        ]
        schema_valid = all(required)
        if not schema_valid:
            errors.append("missing_required_receipt_fields")

        stored_hash = receipt.receipt_hash
        receipt.receipt_hash = None
        recomputed = sha256_digest(receipt.to_json())
        receipt.receipt_hash = stored_hash
        hash_valid = stored_hash == recomputed
        if not hash_valid:
            errors.append("receipt_hash_mismatch")

        return ReceiptVerification(
            valid=schema_valid and hash_valid and not errors,
            schema_valid=schema_valid,
            hash_valid=hash_valid,
            chain_reference_present=receipt.previous_receipt_hash is not None,
            errors=errors,
        )
