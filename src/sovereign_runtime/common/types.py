from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum


class EmbodimentResult(str, Enum):
    PASS = "PASS"
    FAIL_SIGMA = "FAIL_SIGMA"
    FAIL_FRACTURE = "FAIL_FRACTURE"
    FAIL_FRICTION = "FAIL_FRICTION"
    FAIL_Q_GATE = "FAIL_Q_GATE"
    NO_BUILD = "NO_BUILD"


class UTCTStatus(str, Enum):
    COHERENT = "coherent"
    COHERENT_UNDER_PRESSURE = "coherent_under_pressure"
    DEGRADED = "degraded"
    FRACTURED = "fractured"
    COLLAPSED = "collapsed"


class QValue(int, Enum):
    CAUSAL_INTACT = 1
    CAUSAL_BROKEN = 0


def current_iso_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
