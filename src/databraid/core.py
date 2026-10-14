from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from collections.abc import Callable, Iterable
from threading import RLock
from typing import Any


@dataclass(frozen=True)
class LineageEvent:
    output: str
    inputs: tuple[str, ...]
    operation: str
    timestamp: str
    metadata: dict[str, Any]


class Lineage:
    def __init__(self, clock: Callable[[], datetime] | None = None) -> None:
        self.events: list[LineageEvent] = []
        self._clock = clock or (lambda: datetime.now(timezone.utc))
        self._lock = RLock()

    def add(
        self,
        output: str,
        inputs: Iterable[str],
        operation: str,
        *,
        metadata: dict[str, Any] | None = None,
    ) -> LineageEvent:
        if not output or not operation:
            raise ValueError("output and operation must not be empty")
        normalized_inputs = tuple(inputs)
        if any(not item for item in normalized_inputs):
            raise ValueError("lineage identifiers must not be empty")
        timestamp = self._clock()
        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=timezone.utc)
        event = LineageEvent(output, normalized_inputs, operation, timestamp.isoformat(), dict(metadata or {}))
        with self._lock:
            self.events.append(event)
        return event

    def as_dicts(self) -> list[dict[str, Any]]:
        with self._lock:
            return [asdict(event) for event in self.events]

    def for_output(self, output: str) -> list[LineageEvent]:
        with self._lock:
            return [event for event in self.events if event.output == output]
