from sovereign_runtime import (
    ActionContext,
    AnchorLedger,
    BundleWriter,
    CoherenceGate,
    EAReceiptGenerator,
    EAReceiptVerifier,
    PermissionGate,
    PermissionPolicyEngine,
    RuntimeLog,
)


def test_receipt_generator_and_verifier():
    context = ActionContext(tool="workflow.stage", action_description="Prepare runtime output")
    decision = PermissionPolicyEngine().classify(context)
    coherence = CoherenceGate().evaluate(1.2, 0.2, 0.1, 1)
    receipt = EAReceiptGenerator().create(context, "prepared", decision, coherence=coherence, user_confirmed=True)
    verification = EAReceiptVerifier().verify(receipt)
    assert verification.valid is True
    assert receipt.receipt_hash is not None


def test_permission_gate_requires_confirmation_for_class_three():
    gate = PermissionGate()
    context = ActionContext(tool="file.write", action_description="Write runtime output")
    result = gate.check(context, user_confirmed=False)
    assert result.passed is False
    assert result.reason == "confirmation_required"
    confirmed = gate.check(context, user_confirmed=True)
    assert confirmed.passed is True


def test_runtime_log_bundle_writer():
    log = RuntimeLog()
    log.append("coherence", "candidate", {"sigma": 1.2})
    bundle = BundleWriter().create(log.list())
    assert bundle.bundle_id.startswith("bundle_")
    assert len(bundle.records) == 1


def test_anchor_ledger_hash_match():
    ledger = AnchorLedger()
    anchor = ledger.set("provenance", "traceable causal record")
    assert ledger.require_match("provenance", anchor.hash) is True
