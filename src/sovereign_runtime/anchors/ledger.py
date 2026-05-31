from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any
import json

from sovereign_runtime.core import sha256_digest


@dataclass
class AnchorDefinition:
    name: str
    definition: str
    version: str = "0.1"
    owner: str = "MT Tech Industries LLC"

    @property
    def hash(self) -> str:
        return sha256_digest(json.dumps(asdict(self), sort_keys=True))

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["hash"] = self.hash
        return payload


class AnchorLedger:
    """Stores user-owned definitions that runtime systems must not silently redefine."""

    def __init__(self) -> None:
        self.anchors: dict[str, AnchorDefinition] = {}

    def set(self, name: str, definition: str, version: str = "0.1") -> AnchorDefinition:
        anchor = AnchorDefinition(name=name, definition=definition, version=version)
        self.anchors[name] = anchor
        return anchor

    def get(self, name: str) -> AnchorDefinition | None:
        return self.anchors.get(name)

    def require_match(self, name: str, expected_hash: str) -> bool:
        anchor = self.get(name)
        return anchor is not None and anchor.hash == expected_hash

    def to_dict(self) -> dict[str, Any]:
        return {name: anchor.to_dict() for name, anchor in self.anchors.items()}
