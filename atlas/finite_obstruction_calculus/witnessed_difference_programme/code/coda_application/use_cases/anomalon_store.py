# -*- coding: utf-8 -*-
"""
Persistent append-only anomalon register (JSON Lines).

The domain register (``AnomalonRegistry``) keeps no files and reads no clock. This use
case gives it a store that survives the process: one JSON object per line, appended and
flushed, never rewritten. The path is ``$CODA_ANOMALON_REGISTER`` when set, otherwise
``~/.coda/anomalon_register.jsonl``. Reading de-duplicates by fingerprint, first record
first, so a concurrent double append cannot change a retained record.

AuthorityEffect: None.
"""

from __future__ import annotations

import json
import os
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

from coda_application.domain.anomalon_registry import AnomalonRecord, AnomalonRegistry

ENV_VAR = "CODA_ANOMALON_REGISTER"
_LOCK = threading.Lock()


def default_register_path() -> Path:
    configured = os.environ.get(ENV_VAR, "").strip()
    return Path(configured) if configured else Path.home() / ".coda" / "anomalon_register.jsonl"


class JsonlAnomalonStore:
    """Append-only JSONL store; each line is one registration."""

    def __init__(self, path: Path) -> None:
        self.path = Path(path)

    def load(self) -> List[AnomalonRecord]:
        if not self.path.is_file():
            return []
        records: List[AnomalonRecord] = []
        with _LOCK:
            lines = self.path.read_text(encoding="utf-8").splitlines()
        for line in lines:
            if line.strip():
                records.append(AnomalonRecord.from_json(json.loads(line)))
        return records

    def append(self, record: AnomalonRecord) -> None:
        line = dict(record.to_json(), registered_at_utc=datetime.now(timezone.utc).isoformat())
        with _LOCK:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.path, "a", encoding="utf-8", newline="\n") as fh:
                fh.write(json.dumps(line, sort_keys=True) + "\n")
                fh.flush()
                os.fsync(fh.fileno())


_STORES: Dict[str, JsonlAnomalonStore] = {}


def configured_store() -> JsonlAnomalonStore:
    """The store for the currently configured path (one object per path per process)."""
    path = str(default_register_path())
    with _LOCK:
        store = _STORES.get(path)
        if store is None:
            store = _STORES[path] = JsonlAnomalonStore(Path(path))
        return store


def install() -> None:
    """Point the global anomalon register at the persistent store."""
    AnomalonRegistry.configure_store(configured_store)
