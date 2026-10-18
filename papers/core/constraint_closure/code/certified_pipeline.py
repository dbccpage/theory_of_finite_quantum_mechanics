"""Certified transformation pipeline module.

Provides fingerprinted data containers, SHA-256 state transition certificates,
and validated sequential pipeline execution.

contract_id: urn:omega:math:hashes:v1.0.0
contract_id: urn:omega:math:transport_certificate:v1.0.0
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Tuple


@dataclass(frozen=True, slots=True)
class Tag:
    """Named marker tag for data categorization."""
    name: str


@dataclass(frozen=True, slots=True)
class FingerprintedBag:
    """Immutable key-value container producing deterministic SHA-256 fingerprints.

    Uses length-prefixed structured canonical encoding to prevent collision ambiguities.
    contract_id: urn:omega:math:hashes:v1.0.0
    """
    name: str
    data: Dict[str, str]

    def fingerprint(self) -> str:
        """Deterministic SHA-256 fingerprint using canonical length-prefixed encoding."""
        h = hashlib.sha256()
        name_bytes = self.name.encode("utf-8")
        h.update(f"{len(name_bytes)}:".encode("ascii"))
        h.update(name_bytes)
        h.update(b";")
        for k in sorted(self.data):
            k_bytes = k.encode("utf-8")
            v_bytes = self.data[k].encode("utf-8")
            h.update(f"{len(k_bytes)}:".encode("ascii"))
            h.update(k_bytes)
            h.update(b"=")
            h.update(f"{len(v_bytes)}:".encode("ascii"))
            h.update(v_bytes)
            h.update(b";")
        return h.hexdigest()


@dataclass(frozen=True, slots=True)
class TransitionCert:
    """State hash integrity certificate tracking sequential container fingerprints.

    Verifies format and consistency of before/after cryptographic hashes.
    Note: Validates state hash format and transition recording; does not
    independently prove mathematical or physical correctness of the underlying transform.
    contract_id: urn:omega:math:transport_certificate:v1.0.0
    """
    source_hash: str
    target_hash: str
    step_name: str
    ok: bool = True

    def __post_init__(self) -> None:
        if not self.source_hash:
            raise ValueError("source_hash must be non-empty")
        if not self.target_hash:
            raise ValueError("target_hash must be non-empty")
        if not self.step_name:
            raise ValueError("step_name must be non-empty")

    def is_valid(self) -> bool:
        """Validates hash string formatting (64 hex characters) and step execution flag."""
        return self.ok and len(self.source_hash) == 64 and len(self.target_hash) == 64


class Step:
    """Individual transformation step emitting a transition certificate."""

    def __init__(self, name: str, transform: Callable[[FingerprintedBag], FingerprintedBag]):
        if not name:
            raise ValueError("Step name must be non-empty")
        self.name = name
        self.transform = transform

    def run(self, bag: FingerprintedBag) -> Tuple[FingerprintedBag, TransitionCert]:
        before = bag.fingerprint()
        after_bag = self.transform(bag)
        cert = TransitionCert(
            source_hash=before,
            target_hash=after_bag.fingerprint(),
            step_name=self.name,
        )
        return after_bag, cert


class Pipeline:
    """Sequentially executes steps while asserting certificate validity."""

    def __init__(self, name: str, steps: List[Step]):
        if not name:
            raise ValueError("Pipeline name must be non-empty")
        self.name = name
        self.steps = list(steps)

    def run(self, bag: FingerprintedBag) -> Tuple[FingerprintedBag, List[TransitionCert]]:
        current = bag
        certs: List[TransitionCert] = []
        for step in self.steps:
            current, cert = step.run(current)
            certs.append(cert)
            if not cert.is_valid():
                raise RuntimeError(f"Pipeline halted at step: {step.name}")
        return current, certs
