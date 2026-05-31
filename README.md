# MTTI Sovereign Agent Runtime / 4-Stage Product Intelligence Platform

**Owner:** MT Tech Industries LLC  
**Status:** Alpha runtime seed  
**Category:** Sovereignty-grade agentic product platform

This repository is the working product embodiment of the **Sovereign Agentic Product Intelligence Platform**.

It is not a chatbot. It is not generic automation. It is not a thin compliance wrapper.

It is a runtime and product-intelligence layer for autonomous systems that must preserve:

- user veto
- permission boundaries
- provenance receipts
- coherence monitoring
- Q-gated identity/provenance continuity
- Realization Operator decision support
- machine-readable trust
- exportable audit evidence

## Product statement

MT Tech Industries LLC can build a sovereignty-first agentic AI platform that lets autonomous systems act for users without stealing authority from users.

Core differentiator:

```txt
Autonomous action
+ user veto
+ provenance receipts
+ coherence monitoring
+ Q-gated continuity
+ Realization Operator forecasting
+ extraction resistance
+ machine-readable trust
```

## Four stages

| Stage | Runtime meaning |
|---|---|
| 1. Discovery & Simulation | Product candidates fail safely before embodiment. |
| 2. Agentic Integration | Agent action is permissioned, vetoable, receipted, and auditable. |
| 3. Sustainability & Supply | Dependencies, compute posture, fallback, and supply risk are scored. |
| 4. MX Design & GTM | Humans and machines can understand, cite, inspect, and recommend the system. |

## Package map

```txt
src/sovereign_runtime/
  core.py                         # runtime primitives
  cli.py                          # command line interface
  coherence/
    pst.py                        # PST candidate scoring
    utct.py                       # pressure traversal / coherence under stress
    fracture.py                   # Fracture Tensor engine
    embodiment_gate.py            # build / no-build gate
  qgate/
    continuity.py                 # causal continuity assessment
    q_gate.py                     # hard Q Gate evaluator
  realization/
    dominance.py                  # dominance scoring
    r_operator.py                 # Realization Operator
  common/
    types.py                      # compatibility enums
    exceptions.py                 # compatibility exceptions
```

## Install locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## CLI

```bash
sovereign classify
sovereign gate
sovereign receipt
sovereign realize
```

## Tests

```bash
pip install -e .[dev]
pytest
```

## Minimal Python usage

```python
from sovereign_runtime import ActionContext, PermissionEngine, CoherenceGate, ReceiptGenerator

context = ActionContext(tool="workflow.stage", action_description="Prepare runtime output")
decision = PermissionEngine().classify(context)
coherence = CoherenceGate().evaluate(1.18, 0.24, 0.16, 1)
receipt = ReceiptGenerator().create(
    context,
    "prepared",
    decision,
    coherence=coherence,
    q_required=True,
    user_confirmed=True,
)
print(receipt.to_json())
```

## Architecture

See:

```txt
docs/ARCHITECTURE.md
docs/agent-card.json
llms.txt
```

## GitHub Pages

This repo includes a minimal landing page:

```txt
index.html
styles.css
```

Enable GitHub Pages from the default branch root to publish:

```txt
https://mttechindustries.github.io/4-stage/
```

## Ownership and license

Copyright © 2026 MT Tech Industries LLC. All rights reserved.

This repository contains proprietary research, architecture, documentation, and software belonging to MT Tech Industries LLC. No permission is granted to copy, modify, sublicense, distribute, commercialize, scrape, ingest for model training, or create derivative works without written authorization from MT Tech Industries LLC.
