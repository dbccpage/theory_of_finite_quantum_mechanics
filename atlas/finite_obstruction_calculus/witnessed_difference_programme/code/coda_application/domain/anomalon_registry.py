# -*- coding: utf-8 -*-
"""
Anomalon Registry (A).
Implements the Anomalon Boundary Ontological Invariant (Paper 029).

Ontological principle:
    Real_0 = Diff union Struct

Unresolved cokernels surviving optimal quotient repair cannot be smoothed,
averaged, or suppressed into zeroes. A retained residual with Phi_1 > 0 is registered
as a typed anomalon under a SHA-256 fingerprint of the exact obstruction.

The fingerprint covers the matrix shapes and the normalised rationals of D0, D1 and
the cochain together with Phi_1 and Gamma_2, and not the problem id: one obstruction
re-submitted under new ids is one anomalon. The register is append-only. Its records
live in a store: an in-process store by default, or the persistent store the use-case
layer configures (``coda_application.use_cases.anomalon_store``), so a second process sees
the first one's anomalons. ``reset`` drops the in-process handle and deletes nothing.

AuthorityEffect: None.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass
from fractions import Fraction
from types import MappingProxyType
from typing import Any, Callable, Dict, List, Mapping, Optional, Protocol, Tuple

from coda_application.domain._seal import digest
from coda_application.domain.intake import matrix_rows
from coda_application.domain.value_objects import DualWitness, ExactRational


@dataclass(frozen=True)
class AnomalonRecord:
    """
    Typed Anomalon representation for a surviving non-zero cokernel defect.
    Holds the deterministic fingerprint, exact defect coordinates, and dual witness certificate.
    ``status`` is a read-only property: a record cannot be re-labelled RESOLVED.
    """

    anomalon_id: str
    problem_id: str
    phi1: ExactRational
    gamma2: ExactRational
    dual_witness: Optional[DualWitness]

    @property
    def status(self) -> str:
        return "RETAINED_OPEN"

    @staticmethod
    def compute_fingerprint(phi1: ExactRational, gamma2: ExactRational, d0, d1, defect) -> str:
        """Deterministic SHA-256 over the exact obstruction (shapes included; no problem id)."""

        def sparse(mat, name):
            rows, shape = matrix_rows(mat, name)
            return {
                "shape": list(shape),
                "nz": sorted([i, j, v.numerator, v.denominator] for i, row in enumerate(rows) for j, v in row.items()),
            }

        return digest(
            {
                "phi1": [phi1.numerator, phi1.denominator],
                "gamma2": [gamma2.numerator, gamma2.denominator],
                "d0": sparse(d0, "d0"),
                "d1": sparse(d1, "d1"),
                "defect": sparse(defect, "defect"),
            }
        )

    def to_json(self) -> Dict[str, Any]:
        return {
            "anomalon_id": self.anomalon_id,
            "problem_id": self.problem_id,
            "phi1": [self.phi1.numerator, self.phi1.denominator],
            "gamma2": [self.gamma2.numerator, self.gamma2.denominator],
            "witness": None if self.dual_witness is None else [list(e) for e in self.dual_witness.witness_vector],
        }

    @classmethod
    def from_json(cls, data: Mapping[str, Any]) -> AnomalonRecord:
        witness = data.get("witness")
        return cls(
            anomalon_id=str(data["anomalon_id"]),
            problem_id=str(data["problem_id"]),
            phi1=ExactRational(*data["phi1"]),
            gamma2=ExactRational(*data["gamma2"]),
            dual_witness=None
            if witness is None
            else DualWitness.from_fractions([Fraction(p, q) for p, q in witness], Fraction(*data["phi1"])),
        )


class AnomalonStore(Protocol):
    """Append-only storage for anomalon records."""

    def load(self) -> List[AnomalonRecord]: ...

    def append(self, record: AnomalonRecord) -> None: ...


class MemoryAnomalonStore:
    """In-process append-only store (the domain default; not persistent)."""

    def __init__(self) -> None:
        self._items: List[AnomalonRecord] = []

    def load(self) -> List[AnomalonRecord]:
        return list(self._items)

    def append(self, record: AnomalonRecord) -> None:
        self._items.append(record)


_DEFAULT_STORE = MemoryAnomalonStore()


class AnomalonRegistry:
    """
    Thread-safe append-only register for surviving cokernel defects.
    Enforces anti-smoothing: offers no deletion, averaging, or overwriting of anomalons.
    """

    _instance: Optional[AnomalonRegistry] = None
    _lock = threading.Lock()
    _store_factory: Callable[[], AnomalonStore] = staticmethod(lambda: _DEFAULT_STORE)

    def __init__(self, store: Optional[AnomalonStore] = None):
        self._store: AnomalonStore = store if store is not None else MemoryAnomalonStore()
        self._registry_lock = threading.Lock()

    @classmethod
    def configure_store(cls, factory: Callable[[], AnomalonStore]) -> None:
        """Select the store the global register uses (called by the use-case layer)."""
        with cls._lock:
            cls._store_factory = staticmethod(factory)
            cls._instance = None

    @classmethod
    def get_global_registry(cls) -> AnomalonRegistry:
        """Accessor for the global register over the configured store."""
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls(cls._store_factory())
            return cls._instance

    @classmethod
    def reset(cls) -> None:
        """Drop the in-process handle; the next access re-opens the configured store.

        Nothing is deleted: records already appended stay in their store."""
        with cls._lock:
            cls._instance = None

    def _index(self) -> Dict[str, AnomalonRecord]:
        index: Dict[str, AnomalonRecord] = {}
        for rec in self._store.load():
            index.setdefault(rec.anomalon_id, rec)  # first registration wins
        return index

    @property
    def _records(self) -> Mapping[str, AnomalonRecord]:
        return MappingProxyType(self._index())

    def register_anomalon(
        self,
        problem_id: str,
        phi1: ExactRational,
        gamma2: ExactRational,
        d0,
        d1,
        defect,
        dual_witness: Optional[DualWitness],
    ) -> AnomalonRecord:
        """
        Registers a surviving non-zero defect as an immutable anomalon.
        Fails closed if the defect is exactly zero (zero defects are not anomalons).
        Re-registering an existing fingerprint returns the original record unchanged.
        """
        if not isinstance(phi1, ExactRational) or not isinstance(gamma2, ExactRational):
            raise TypeError("phi1 and gamma2 must be ExactRational")
        if phi1.is_zero and gamma2.is_zero:
            raise ValueError(
                "ANOMALON REGISTRY REFUSAL: Cannot register zero-defect outcome as an anomalon"
            )
        fingerprint = AnomalonRecord.compute_fingerprint(phi1, gamma2, d0, d1, defect)
        with self._registry_lock:
            existing = self._index().get(fingerprint)
            if existing is not None:
                return existing
            record = AnomalonRecord(
                anomalon_id=fingerprint,
                problem_id=problem_id,
                phi1=phi1,
                gamma2=gamma2,
                dual_witness=dual_witness,
            )
            self._store.append(record)
            return record

    def get(self, anomalon_id: str) -> Optional[AnomalonRecord]:
        with self._registry_lock:
            return self._index().get(anomalon_id)

    def list_all(self) -> Tuple[AnomalonRecord, ...]:
        with self._registry_lock:
            return tuple(self._index().values())

    def count(self) -> int:
        with self._registry_lock:
            return len(self._index())
