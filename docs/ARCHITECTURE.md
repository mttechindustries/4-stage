# MTTI Sovereign Agent Runtime Architecture

Owner: **MT Tech Industries LLC**

This repository is the working product embodiment of a sovereignty-grade agentic product platform. It is not a chatbot wrapper and not generic automation. It is a runtime and product-intelligence layer for agentic systems that need bounded autonomy, provenance, coherence monitoring, Q-gated continuity, and realization-aware decision support.

## Core stack

```txt
User intent
  -> permission classification
  -> local veto / review / confirmation boundary
  -> PST / UTCT coherence evaluation
  -> Q Gate continuity validation when required
  -> constrained execution
  -> EA Receipt generation
  -> Realization Operator decision support
  -> exportable audit trail
```

## Modules

| Module | Purpose |
|---|---|
| `sovereign_runtime.core` | Runtime primitives: permission class, coherence gate, receipt generator, basic realization operator. |
| `sovereign_runtime.coherence.pst` | PST-style candidate scoring: sigma, fracture norm, embodiment friction. |
| `sovereign_runtime.coherence.utct` | UTCT traversal: whether the candidate remains coherent under pressure. |
| `sovereign_runtime.coherence.fracture` | Fracture Tensor analysis and repair synthesis. |
| `sovereign_runtime.coherence.embodiment_gate` | Build / no-build gate combining PST, fracture, friction, and Q when required. |
| `sovereign_runtime.qgate` | ICR/Q Gate: causal provenance continuity, where Q=0 overrides resemblance. |
| `sovereign_runtime.realization` | Realization Operator: point, regional, trajectory, fractured, and no-dominance outputs. |
| `sovereign_runtime.cli` | Command-line interface for classifying, gating, generating receipts, and resolving realization. |

## PST / UTCT / Q Gate / R Operator roles

### PST

PST turns candidate product states into measurable stability conditions:

```txt
Sigma: survivability
Fracture norm: structural weakness
Embodiment friction: readiness gap
```

The implementation does not claim the final mathematical kernel is complete. It establishes the product runtime interface where the deeper proprietary PST engines can connect without changing the public shape.

### UTCT

UTCT asks whether the system remains coherent under pressure, not merely whether it survives static scoring. Stress scenarios lower sigma and grow fracture, producing coherent, degraded, fractured, or collapsed traversal states.

### Q Gate

Q Gate enforces causal provenance continuity. Similarity alone cannot pass the gate. If causal chain, provenance, or anchor continuity fails, Q=0 and the system classifies the output as replica-like or re-instantiated.

### Realization Operator

The Realization Operator resolves whether a candidate path is structurally actualizing as a point, region, trajectory, fractured field, or no-dominance state. It prevents false precision when dominance is weak.

## Product intent

The first shippable form is the **Sovereign Agent Runtime SDK + EA Receipt Protocol**.

The larger platform grows into:

1. EA Receipt Standard
2. Sovereign Agent Runtime SDK
3. Coherence Audit Dashboard
4. Digital Twin Failure Simulator
5. Sovereignty-Grade Product Intelligence Platform

## Ownership

All repository contents are proprietary to **MT Tech Industries LLC** unless explicitly stated otherwise in writing by MT Tech Industries LLC.
