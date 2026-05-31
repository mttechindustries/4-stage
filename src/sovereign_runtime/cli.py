from __future__ import annotations

import json
import click
from rich.console import Console
from rich.table import Table

from sovereign_runtime.core import (
    ActionContext,
    CoherenceGate,
    PermissionEngine,
    ReceiptGenerator,
    RealizationOperator,
)

console = Console()


@click.group()
def main() -> None:
    """MTTI Sovereign Agent Runtime command line interface."""


@main.command("classify")
@click.option("--tool", default="workflow.stage", show_default=True)
@click.option("--description", default="Prepare a staged agent action", show_default=True)
def classify(tool: str, description: str) -> None:
    """Classify an action into a permission class."""
    context = ActionContext(tool=tool, action_description=description)
    decision = PermissionEngine().classify(context)
    table = Table(title="Permission Decision")
    table.add_column("Field")
    table.add_column("Value")
    table.add_row("allowed", str(decision.allowed))
    table.add_row("permission_class", str(int(decision.permission_class)))
    table.add_row("label", decision.permission_class.label)
    table.add_row("requires_review", str(decision.requires_review))
    table.add_row("requires_confirmation", str(decision.requires_confirmation))
    table.add_row("reason", decision.reason)
    console.print(table)


@main.command("gate")
@click.option("--sigma", default=1.18, type=float, show_default=True)
@click.option("--fracture", default=0.24, type=float, show_default=True)
@click.option("--friction", default=0.16, type=float, show_default=True)
@click.option("--q", default=1, type=int, show_default=True)
def gate(sigma: float, fracture: float, friction: float, q: int) -> None:
    """Run the PST / UTCT / Q embodiment gate."""
    result = CoherenceGate().evaluate(sigma, fracture, friction, q)
    console.print_json(json.dumps(result.__dict__))


@main.command("receipt")
@click.option("--tool", default="workflow.stage", show_default=True)
@click.option("--description", default="Prepare a staged sovereign agent action", show_default=True)
@click.option("--output", default="Action prepared for review", show_default=True)
def receipt(tool: str, description: str, output: str) -> None:
    """Generate an EA Receipt for a sample action."""
    context = ActionContext(tool=tool, action_description=description)
    decision = PermissionEngine().classify(context)
    coherence = CoherenceGate().evaluate(1.18, 0.24, 0.16, 1)
    ea_receipt = ReceiptGenerator().create(
        context=context,
        output=output,
        decision=decision,
        prompt=description,
        coherence=coherence,
        q_required=True,
        user_confirmed=not decision.requires_confirmation,
    )
    console.print_json(ea_receipt.to_json())


@main.command("realize")
@click.option("--dominance", default=0.72, type=float, show_default=True)
@click.option("--confidence", default=0.68, type=float, show_default=True)
def realize(dominance: float, confidence: float) -> None:
    """Resolve a realization type from dominance and confidence."""
    console.print_json(json.dumps(RealizationOperator().resolve(dominance, confidence)))


if __name__ == "__main__":
    main()
