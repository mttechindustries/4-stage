from __future__ import annotations

from sovereign_runtime.core import PermissionClass

DEFAULT_TOOL_POLICIES: dict[str, PermissionClass] = {
    "search.query": PermissionClass.READ_ONLY,
    "file.read": PermissionClass.READ_ONLY,
    "document.draft": PermissionClass.DRAFT_RECOMMEND,
    "report.generate": PermissionClass.DRAFT_RECOMMEND,
    "workflow.stage": PermissionClass.PREPARE_ACTION,
    "file.write": PermissionClass.REVERSIBLE_ACTION,
    "deployment.push": PermissionClass.HIGH_RISK_ACTION,
}
