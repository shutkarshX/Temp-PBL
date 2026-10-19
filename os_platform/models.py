"""Request/process model for the educational citizen-services simulator."""
from __future__ import annotations
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any


class ProcessState(str, Enum):
    NEW = "new"
    READY = "ready"
    RUNNING = "running"
    WAITING = "waiting"
    TERMINATED = "terminated"


@dataclass
class ServiceRequest:
    request_id: str
    citizen_id: str
    service_type: str
    description: str
    arrival_time: int = 0
    state: ProcessState = ProcessState.NEW
    completion_order: int | None = None
    result: str | None = None

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["state"] = self.state.value
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ServiceRequest":
        values = dict(data)
        values["state"] = ProcessState(values.get("state", ProcessState.NEW.value))
        return cls(**values)
