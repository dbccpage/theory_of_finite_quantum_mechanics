import json
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass, field

@dataclass
class DebtEntry:
    filename: str
    sha256: str
    status: str
    missing_fields: List[str] = field(default_factory=list)

class ReplayLedger:
    def __init__(self, receipt_path: str):
        self.receipt_path = receipt_path
        self.legacy_artifacts: List[DebtEntry] = []
        self.scoped_artifacts: List[DebtEntry] = []
        self._load()

    def _load(self):
        with open(self.receipt_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for art in data.get("artifacts", []):
            entry = DebtEntry(
                filename=art["filename"],
                sha256=art["sha256"],
                status=art["status"],
                missing_fields=["full_replay_data"]
            )
            if art["status"] == "LEGACY_DIGEST_ONLY_NOT_MATHEMATICALLY_REPLAYED":
                self.legacy_artifacts.append(entry)
            elif art["status"] == "SCOPED_DIAGNOSTIC_REPLAYED":
                self.scoped_artifacts.append(entry)

    def replay_status_summary(self) -> Dict[str, Any]:
        return {
            "legacy_count": len(self.legacy_artifacts),
            "scoped_count": len(self.scoped_artifacts),
            "total_count": len(self.legacy_artifacts) + len(self.scoped_artifacts),
            "blocking_items": [
                entry.filename for entry in self.legacy_artifacts
            ]
        }

    def debt_report(self) -> Dict[str, Any]:
        return {
            "legacy_debt": [
                {
                    "filename": e.filename,
                    "sha256": e.sha256,
                    "status": e.status,
                    "missing_fields": e.missing_fields
                } for e in self.legacy_artifacts
            ],
            "scoped_debt": [
                {
                    "filename": e.filename,
                    "sha256": e.sha256,
                    "status": e.status,
                    "missing_fields": e.missing_fields
                } for e in self.scoped_artifacts
            ]
        }
