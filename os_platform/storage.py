"""JSON persistence for synthetic citizen-service requests."""
from __future__ import annotations
import json
from pathlib import Path
from .models import ServiceRequest


def save_requests(path: str | Path, requests: list[ServiceRequest]) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps([request.to_dict() for request in requests], indent=2) + "\n",
        encoding="utf-8",
    )


def load_requests(path: str | Path) -> list[ServiceRequest]:
    source = Path(path)
    if not source.exists():
        return []
    raw = json.loads(source.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError("Request storage must contain a JSON list")
    return [ServiceRequest.from_dict(item) for item in raw]
