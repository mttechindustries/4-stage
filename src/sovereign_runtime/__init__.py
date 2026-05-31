"""MTTI Sovereign Agent Runtime package."""

__version__ = "0.1.0"
__company__ = "MT Tech Industries LLC"

from sovereign_runtime.common.types import PermissionClass, ContinuityStatus, RealizationType
from sovereign_runtime.receipts.schema import EAReceipt
from sovereign_runtime.permission.classes import PermissionEngine, ActionContext, PermissionDecision
from sovereign_runtime.permission.gate import PermissionGate

__all__ = [
    "EAReceipt",
    "PermissionClass",
    "PermissionEngine",
    "ActionContext",
    "PermissionDecision",
    "PermissionGate",
    "ContinuityStatus",
    "RealizationType",
]
