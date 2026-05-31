"""MTTI Sovereign Agent Runtime package."""

__version__ = "0.1.0"
__company__ = "MT Tech Industries LLC"

from sovereign_runtime.core import (
    ActionContext,
    CoherenceGate,
    CoherenceResult,
    EAReceipt,
    PermissionClass,
    PermissionDecision,
    PermissionEngine,
    ReceiptGenerator,
)
from sovereign_runtime.coherence import (
    EmbodimentGate,
    EmbodimentGateInput,
    EmbodimentGateOutput,
    FractureComponent,
    FractureTensor,
    FractureTensorEngine,
    PSTEvaluator,
    PSTScore,
    StressScenario,
    UTCTCoherenceStatus,
    UTCTEvaluator,
)
from sovereign_runtime.qgate import QGate, QGateResult, ContinuityAssessment, ContinuityChecker
from sovereign_runtime.realization import (
    DominanceAssessment,
    DominanceEvaluator,
    RealizationOperator,
    RealizationResult,
)

__all__ = [
    "ActionContext",
    "CoherenceGate",
    "CoherenceResult",
    "EAReceipt",
    "PermissionClass",
    "PermissionDecision",
    "PermissionEngine",
    "ReceiptGenerator",
    "PSTScore",
    "PSTEvaluator",
    "StressScenario",
    "UTCTCoherenceStatus",
    "UTCTEvaluator",
    "FractureComponent",
    "FractureTensor",
    "FractureTensorEngine",
    "EmbodimentGate",
    "EmbodimentGateInput",
    "EmbodimentGateOutput",
    "QGate",
    "QGateResult",
    "ContinuityAssessment",
    "ContinuityChecker",
    "DominanceAssessment",
    "DominanceEvaluator",
    "RealizationOperator",
    "RealizationResult",
]
