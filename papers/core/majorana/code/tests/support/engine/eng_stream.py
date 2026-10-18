"""Parallel JSONL streaming engine.

Faithful port of ``crates/omega_engine.crates.engine/src/engine_stream.rs``.
"""

from __future__ import annotations
import concurrent.futures
from typing import Callable, Iterable, List, TypeVar

Out = TypeVar("Out")


class StreamingEngine:
    """Massively parallel puzzle streaming engine."""

    @staticmethod
    def process_stream(
        reader: Iterable[str],
        batch_size: int,
        solver: Callable[[str], Out],
    ) -> List[Out]:
        """Streams lines from reader and dispatches them to solver in parallel.

        Keeps RAM usage flat and utilizes multiple cores.
        """
        results = []
        batch = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for line in reader:
                cleaned = line.rstrip("\r\n")
                if cleaned:
                    batch.append(cleaned)
                if len(batch) >= batch_size:
                    results.extend(list(executor.map(solver, batch)))
                    batch = []
            if batch:
                results.extend(list(executor.map(solver, batch)))
        return results



