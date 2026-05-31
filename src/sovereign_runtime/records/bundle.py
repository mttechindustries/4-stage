from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any
import json

from sovereign_runtime.core import new_id, now_iso
from sovereign_runtime.records.log import RuntimeEvent


@dataclass
class RuntimeBundle:
    bundle_id: str
    created_at: str
    records: list[dict[str, Any]]

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2, sort_keys=True)


class BundleWriter:
    """Writes runtime evidence bundles to disk."""

    def create(self, events: list[RuntimeEvent]) -> RuntimeBundle:
        return RuntimeBundle(
            bundle_id=new_id("bundle"),
            created_at=now_iso(),
            records=[event.to_dict() for event in events],
        )

    def write(self, bundle: RuntimeBundle, path: str | Path) -> Path:
        output = Path(path)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(bundle.to_json(), encoding="utf-8")
        return output
