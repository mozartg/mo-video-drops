from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class VSRRState:
    def __init__(self, path: Path, data: dict[str, Any]) -> None:
        self.path = path
        self.data = data

    @classmethod
    def load(cls, path: Path, job_id: str) -> "VSRRState":
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
        else:
            data = {
                "schema": "vsrr-2.0-state/v1",
                "job_id": job_id,
                "status": "starting",
                "phase": "initialize",
                "blockers": {},
                "receipts": [],
            }
        instance = cls(path, data)
        instance.save()
        return instance

    def save(self) -> None:
        self.data["updated_at"] = datetime.now(timezone.utc).isoformat()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(self.path.suffix + ".tmp")
        temporary.write_text(json.dumps(self.data, indent=2), encoding="utf-8")
        temporary.replace(self.path)

    def checkpoint(self, phase: str, status: str, receipt: str | None = None) -> None:
        self.data["phase"] = phase
        self.data["status"] = status
        if receipt:
            self.data["receipts"].append(receipt)
        self.save()

    def record_failure(
        self,
        route: str,
        blocker_id: str,
        evidence: str,
        method: str,
    ) -> None:
        blocker = self.data["blockers"].setdefault(route, {
            "blocker_id": blocker_id,
            "attempts": [],
            "status": "OPEN",
        })
        blocker["attempts"].append({
            "method": method,
            "evidence": evidence,
            "recorded_at": datetime.now(timezone.utc).isoformat(),
        })
        blocker["status"] = "PARKED" if len(blocker["attempts"]) >= 2 else "RETRY_WITH_DIFFERENT_METHOD"
        self.save()

    def route_status(self, route: str) -> str:
        blocker = self.data["blockers"].get(route)
        return blocker["status"] if blocker else "AVAILABLE"

