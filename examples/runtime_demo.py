from sovereign_runtime import ActionContext, CoherenceGate, PermissionEngine, ReceiptGenerator
from sovereign_runtime.qgate import QGate
from sovereign_runtime.realization import RealizationOperator
from sovereign_runtime.records import RuntimeLog, BundleWriter

context = ActionContext(tool="workflow.stage", action_description="Prepare runtime output")
decision = PermissionEngine().classify(context)
coherence = CoherenceGate().evaluate(1.18, 0.24, 0.16, 1)
q_result = QGate().evaluate(
    causal_chain_score=0.91,
    provenance_score=0.88,
    state_similarity=0.79,
    anchor_match=True,
)
receipt = ReceiptGenerator().create(
    context,
    "prepared",
    decision,
    coherence=coherence,
    q_required=True,
    user_confirmed=True,
)
realization = RealizationOperator().resolve(dominance=0.72, confidence=0.68)

log = RuntimeLog()
log.append("permission", "workflow.stage", decision.__dict__)
log.append("coherence", "candidate", coherence.__dict__)
log.append("q_gate", "continuity", q_result.to_dict())
log.append("receipt", receipt.receipt_id, receipt.to_dict())
log.append("realization", "candidate", realization.to_dict())

bundle = BundleWriter().create(log.list())
print(bundle.to_json())
