"""Deterministic FCFS scheduler with explicit process-state transitions."""
from __future__ import annotations
from collections import deque
from dataclasses import dataclass, field
from .models import ProcessState, ServiceRequest


@dataclass
class FCFSScheduler:
    ready_queue: deque[ServiceRequest] = field(default_factory=deque)
    completed: list[ServiceRequest] = field(default_factory=list)
    _next_completion_order: int = 1

    def submit(self, request: ServiceRequest) -> None:
        if request.state is not ProcessState.NEW:
            raise ValueError(f"Only NEW requests can be submitted; got {request.state.value}")
        request.state = ProcessState.READY
        self.ready_queue.append(request)

    def run_next(self) -> ServiceRequest | None:
        if not self.ready_queue:
            return None
        request = self.ready_queue.popleft()
        if request.state is not ProcessState.READY:
            raise RuntimeError("Ready queue contains a request that is not READY")
        request.state = ProcessState.RUNNING
        request.result = f"Demo processing completed for {request.service_type}"
        request.state = ProcessState.TERMINATED
        request.completion_order = self._next_completion_order
        self._next_completion_order += 1
        self.completed.append(request)
        return request

    def run_all(self) -> list[ServiceRequest]:
        while self.ready_queue:
            self.run_next()
        return list(self.completed)
