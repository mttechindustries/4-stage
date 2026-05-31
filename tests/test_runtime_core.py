from sovereign_runtime import (
    ActionContext,
    CoherenceGate,
    EmbodimentGate,
    EmbodimentGateInput,
    PermissionEngine,
    PSTEvaluator,
    QGate,
    RealizationOperator,
    ReceiptGenerator,
)


def candidate_config():
    return {
        "architecture": {
            "permission": {"mitigations": ["veto"], "integrates_with_audit": True},
            "audit": {"mitigations": ["receipt"]},
            "agent": {"mitigations": ["bounded_tools"], "integrates_with_receipts": True},
            "receipts": {"mitigations": ["hashing"]},
            "coherence": {"mitigations": ["pst"], "integrates_with_qgate": True},
            "qgate": {"mitigations": ["causal_chain"]},
            "data": {"mitigations": ["export"], "integrates_with_export": True},
            "export": {"mitigations": ["json"]},
            "ux": {"mitigations": ["clear_receipts"]},
            "trust": {"mitigations": ["provenance"]},
            "supply": {"mitigations": ["fallback"]},
            "compliance": {"mitigations": ["inventory"]},
            "autonomy": {"mitigations": ["permission_classes"]},
            "launch": {"mitigations": ["llms_txt"]},
            "identity": {"mitigations": ["q_gate"]},
        },
        "dependencies": [{"name": "local_runtime", "single_source": False}],
        "risk_factors": [{"name": "tool_drift", "mitigated": True}],
        "test_coverage": 0.82,
        "user_sovereignty_score": 0.92,
        "provenance_completeness": 0.94,
        "has_prototype": True,
        "documentation_complete": True,
    }


def test_permission_engine_classifies_action():
    context = ActionContext(tool="workflow.stage", action_description="Prepare runtime output")
    decision = PermissionEngine().classify(context)
    assert decision.allowed is True
    assert int(decision.permission_class) == 2


def test_core_coherence_gate_passes_stable_candidate():
    result = CoherenceGate().evaluate(1.18, 0.24, 0.16, 1)
    assert result.passed is True
    assert result.result == "PASS"


def test_pst_evaluator_outputs_score():
    score = PSTEvaluator().evaluate(candidate_config())
    assert score.sigma > 0
    assert "provenance" in score.component_scores


def test_q_gate_blocks_broken_continuity():
    result = QGate().evaluate(
        causal_chain_score=0.2,
        provenance_score=0.95,
        state_similarity=0.99,
        anchor_match=True,
    )
    assert result.passed is False
    assert result.q_value == 0


def test_realization_operator_resolves_candidate_region():
    result = RealizationOperator().resolve(
        candidates={
            "local_first_runtime": {
                "stability": 0.88,
                "coherence": 0.84,
                "provenance": 0.92,
                "reversibility": 0.82,
                "supply_resilience": 0.72,
                "mx_readability": 0.78,
            },
            "cloud_only_runtime": {
                "stability": 0.62,
                "coherence": 0.58,
                "provenance": 0.55,
                "reversibility": 0.42,
                "supply_resilience": 0.36,
                "mx_readability": 0.66,
            },
        }
    )
    assert result.realization_type in {"point_realization", "regional_realization", "trajectory_realization"}
    assert result.selected_candidate == "local_first_runtime"


def test_embodiment_gate_returns_structured_output():
    output = EmbodimentGate(fracture_threshold=3.0).evaluate(
        EmbodimentGateInput(candidate=candidate_config(), require_q_gate=True, q_value=1)
    )
    assert output.result in {"PASS", "FAIL_SIGMA", "FAIL_FRACTURE", "FAIL_FRICTION"}
    assert "pst_score" in output.to_dict()


def test_receipt_serializes():
    context = ActionContext(tool="workflow.stage", action_description="Prepare runtime output")
    decision = PermissionEngine().classify(context)
    coherence = CoherenceGate().evaluate(1.18, 0.24, 0.16, 1)
    receipt = ReceiptGenerator().create(context, "prepared", decision, coherence=coherence, q_required=True, user_confirmed=True)
    payload = receipt.to_json()
    assert "receipt_id" in payload
    assert "q_gate" in payload
