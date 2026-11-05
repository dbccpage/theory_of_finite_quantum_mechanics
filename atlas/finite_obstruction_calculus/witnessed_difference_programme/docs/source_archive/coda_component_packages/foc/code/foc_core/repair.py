"""Finite repair moves, registries, and stabilization evidence for CODA-FOC.

Bounded Context: CODA.FOC (Finite Obstruction Calculus)
AuthorityEffect: None.
Constraint: Zero floating-point operations in exact algebraic decision paths.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from sympy import Rational

from .exact_arithmetic import (
    _digest_exact,
    _digest_strings,
    _exact_scalar,
    _exact_vector,
    _is_sha256,
)
from .packets import (
    FiniteObstructionPacket,
    ObstructionResult,
    RepairDisposition,
)


@dataclass(frozen=True, slots=True)
class RepairCheck:
    """Witness record for one declared repair move verification."""

    move_id: str
    disposition: RepairDisposition
    witness_digest: str

    def __post_init__(self) -> None:
        if not isinstance(self.move_id, str) or not self.move_id.strip():
            raise ValueError("move_id must be a nonempty string")
        if not isinstance(self.disposition, RepairDisposition):
            raise TypeError(f"disposition must be a RepairDisposition, got {type(self.disposition)}")


@dataclass(frozen=True, slots=True)
class StabilizationEvidence:
    """Self-contained audit receipt for stabilized survivor routing.

    Invariants:
    - AuthorityEffect is None.
    - All digests are 64-character SHA-256 hex strings.
    - Budget limits and spent counts are valid non-negative integers.
    - Validates against an independently supplied FiniteRepairRegistry via fresh replay.
    """

    input_digest: str
    observer_digest: str
    registry_scope: str
    registry_entries: tuple[str, ...]
    registry_digest: str
    completeness_receipt_digest: str
    evaluator_id: str
    budget_limit: int
    budget_spent: int
    checks: tuple[RepairCheck, ...]
    bindings_digest: str
    authority_effect: str = "None"

    @classmethod
    def create(
        cls,
        result: ObstructionResult,
        *,
        registry_scope: str,
        registry_entries: Iterable[str],
        completeness_receipt_digest: str,
        evaluator_id: str,
        budget_limit: int,
        budget_spent: int,
        checks: Iterable[RepairCheck],
        bindings_digest: str,
    ) -> "StabilizationEvidence":
        entries = tuple(registry_entries)
        return cls(
            input_digest=result.input_digest,
            observer_digest=result.observer_digest,
            registry_scope=registry_scope,
            registry_entries=entries,
            registry_digest=_digest_strings("registry", (registry_scope, *entries)),
            completeness_receipt_digest=completeness_receipt_digest,
            evaluator_id=evaluator_id,
            budget_limit=budget_limit,
            budget_spent=budget_spent,
            checks=tuple(checks),
            bindings_digest=bindings_digest,
        )

    def valid_for(
        self, result: ObstructionResult, registry: FiniteRepairRegistry | None = None
    ) -> bool:
        """Verify evidence validity against result and independent registry replay."""
        if not isinstance(registry, FiniteRepairRegistry):
            return False
        if self.authority_effect != "None":
            return False
        if self.input_digest != result.input_digest:
            return False
        if self.observer_digest != result.observer_digest:
            return False
        if not self.registry_scope or not self.evaluator_id:
            return False
        if (
            type(self.budget_limit) is not int or type(self.budget_spent) is not int
            or self.budget_limit < len(registry.moves)
            or not 0 <= self.budget_spent <= self.budget_limit
        ):
            return False
        if not all(
            _is_sha256(value)
            for value in (
                self.registry_digest,
                self.completeness_receipt_digest,
                self.bindings_digest,
            )
        ):
            return False
        if not self.registry_entries or len(set(self.registry_entries)) != len(
            self.registry_entries
        ):
            return False
        if self.registry_digest != _digest_strings(
            "registry", (self.registry_scope, *self.registry_entries)
        ):
            return False
        check_ids = tuple(check.move_id for check in self.checks)
        if len(set(check_ids)) != len(check_ids) or set(check_ids) != set(
            self.registry_entries
        ):
            return False
        if not all(
            check.disposition is RepairDisposition.NO_ADMISSIBLE_REPAIR
            and _is_sha256(check.witness_digest)
            for check in self.checks
        ):
            return False
        baseline, expected = registry.replay(self.budget_limit)
        return result == baseline and self == expected


@dataclass(frozen=True, slots=True)
class FiniteRepairMove:
    """One declared additive correction; no claim about undeclared operations."""

    move_id: str
    correction: tuple[Rational, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.move_id, str) or not self.move_id.strip():
            raise ValueError("move_id must be a nonempty string")
        object.__setattr__(self, "correction", tuple(_exact_scalar(v) for v in self.correction))


@dataclass(frozen=True, slots=True)
class FiniteRepairRegistry:
    """Complete by declaration for this finite list, not for an external license policy.

    A move is improving exactly when its corrected defect has smaller Phi1.
    The caller supplies this immutable scope independently of the evidence record.
    """

    packet: FiniteObstructionPacket
    defect: tuple[Rational, ...]
    scope: str
    moves: tuple[FiniteRepairMove, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "defect", tuple(_exact_scalar(v) for v in self.defect))
        object.__setattr__(self, "moves", tuple(self.moves))
        if type(self.packet) is not FiniteObstructionPacket or any(
            type(move) is not FiniteRepairMove for move in self.moves
        ):
            raise TypeError("registry requires immutable packet and move records")
        if not isinstance(self.scope, str) or not self.scope.strip():
            raise ValueError("a finite registry needs a nonempty scope")
        ids = tuple(move.move_id for move in self.moves)
        if not ids or len(ids) != len(set(ids)):
            raise ValueError("a finite registry needs distinct nonempty move IDs")
        if len(self.defect) != self.packet.d0.rows or any(
            len(move.correction) != len(self.defect) for move in self.moves
        ):
            raise ValueError("registry corrections must inhabit C1")
        self.packet.validate()

    def replay(self, budget_limit: int) -> tuple[ObstructionResult, StabilizationEvidence]:
        """Replay every declared move against self and produce stabilization evidence."""
        if type(budget_limit) is not int or budget_limit < len(self.moves):
            raise ValueError("budget must permit replay of every declared move")
        from .diagnosis import diagnose

        result = diagnose(self.packet, self.defect)
        entries = tuple(move.move_id for move in self.moves)
        witnesses: list[RepairCheck] = []
        move_digests: list[str] = []
        for move in self.moves:
            correction = _exact_vector(move.correction)
            trial = diagnose(self.packet, _exact_vector(self.defect) + correction)
            disposition = (
                RepairDisposition.REPAIR_AVAILABLE
                if trial.phi1.value < result.phi1.value
                else RepairDisposition.NO_ADMISSIBLE_REPAIR
            )
            move_digest = _digest_exact("finite-additive-correction-v1", correction)
            move_digests.append(move_digest)
            witnesses.append(
                RepairCheck(
                    move.move_id,
                    disposition,
                    _digest_strings(
                        "finite-repair-replay-v1",
                        (
                            move.move_id,
                            move_digest,
                            result.input_digest,
                            trial.input_digest,
                            str(trial.phi1.value),
                            str(trial.gamma2.value),
                            disposition.value,
                        ),
                    ),
                )
            )
        content_digest = _digest_strings(
            "finite-registry-content-v1",
            (
                self.scope,
                result.input_digest,
                *entries,
                *move_digests,
            ),
        )
        evidence = StabilizationEvidence.create(
            result,
            registry_scope=self.scope,
            registry_entries=entries,
            completeness_receipt_digest=content_digest,
            evaluator_id="finite-additive-phi1-replay-v1",
            budget_limit=budget_limit,
            budget_spent=len(self.moves),
            checks=witnesses,
            bindings_digest=_digest_strings(
                "finite-registry-bindings-v1",
                (
                    content_digest,
                    result.input_digest,
                    result.observer_digest,
                ),
            ),
        )
        return result, evidence


__all__ = [
    "FiniteRepairMove",
    "FiniteRepairRegistry",
    "RepairCheck",
    "StabilizationEvidence",
]
