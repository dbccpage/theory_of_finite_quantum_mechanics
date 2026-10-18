"""Fitness as an observation with separate dimensions, not a score.

`EPIC-OE-PROMPT-CIV-001` section 6 specifies `FitnessVectorV1` as "a
manifest-bound observation with separate dimensions, raw counts, uncertainty, and
missing-data state", and then lists what it must not do. Two of those
prohibitions shape this module:

> [it must not] collapse inconclusive results into failures or passes; or hide
> dimension tradeoffs behind a single undocumented scalar.

Both are easy to violate by accident and hard to notice afterwards.

**Inconclusive is a third value, not a soft failure.** A dimension that could not
be evaluated is not a dimension that failed. Folding the two together loses the
difference between "this candidate is worse" and "we did not find out", and the
loss is invisible downstream because both arrive as a number that is not a pass.
So the outcome vocabulary is four-valued -- `PASS`, `FAIL`, `INCONCLUSIVE`,
`MISSING` -- and any aggregate reports the four separately rather than returning
a ratio that has silently chosen how to treat two of them.

**A scalar requires its formula frozen first.** The epic: "If a scalar is needed
for a preregistered experiment, its formula, units, weights, tie rule, and
sensitivity analysis are frozen before outcomes are observed." So a vector
carrying a scalar without a preregistration digest is refused, and the
preregistration itself must carry all five parts.

**Fitness has no status field.** The acceptance conditions say fitness "changes
review ordering only and cannot change lifecycle status". Rather than validating
a status nobody may set, there is nowhere to set one.

`AuthorityEffect: None`. Ranking who gets reviewed is not deciding what is true.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Mapping

FITNESS_VECTOR_SCHEMA_V1 = "omega.prompt_civilization.fitness-vector.v1"
PREREGISTRATION_SCHEMA_V1 = "omega.prompt_civilization.scalar-preregistration.v1"

DIMENSION_OUTCOMES = frozenset({"PASS", "FAIL", "INCONCLUSIVE", "MISSING"})
DECIDED_OUTCOMES = frozenset({"PASS", "FAIL"})
UNDECIDED_OUTCOMES = frozenset({"INCONCLUSIVE", "MISSING"})

PREREGISTRATION_PARTS = ("formula", "units", "weights", "tie_rule", "sensitivity")

COMPARISON_BINDINGS = ("preregistration_digest", "checker_id", "holdout_digest")


class FitnessError(RuntimeError):
    """A typed refusal naming which rule failed."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(f"{code}: {message}")
        self.code = code


def _digest(value: Any, label: str) -> str:
    if type(value) is not str or not value.startswith("sha256:") or len(value) != 71:
        raise FitnessError("BAD_DIGEST", f"{label} must be a sha256: digest")
    return value


def _semantic_id(schema: str, payload: Mapping[str, Any]) -> str:
    body = json.dumps(
        {"schema": schema, **dict(payload)},
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(body).hexdigest()


@dataclass(frozen=True, slots=True)
class ScalarPreregistrationV1:
    """The five things that must be frozen before outcomes are observed."""

    formula: str
    units: str
    weights: tuple[tuple[str, str], ...]
    tie_rule: str
    sensitivity: str
    schema_version: str = PREREGISTRATION_SCHEMA_V1
    preregistration_digest: str = ""

    def __post_init__(self) -> None:
        for part in ("formula", "units", "tie_rule", "sensitivity"):
            value = getattr(self, part)
            if type(value) is not str or not value.strip():
                raise FitnessError(
                    "PREREGISTRATION_INCOMPLETE",
                    f"{part} must be stated before outcomes are observed",
                )
        if type(self.weights) is not tuple or not self.weights:
            raise FitnessError(
                "PREREGISTRATION_INCOMPLETE",
                "weights must be a nonempty tuple of (dimension, weight) pairs",
            )
        for pair in self.weights:
            if type(pair) is not tuple or len(pair) != 2:
                raise FitnessError(
                    "PREREGISTRATION_INCOMPLETE",
                    "each weight must be a (dimension, weight) pair",
                )
        names = [name for name, _ in self.weights]
        if len(set(names)) != len(names):
            raise FitnessError(
                "PREREGISTRATION_INCOMPLETE", "a dimension is weighted twice"
            )
        if self.schema_version != PREREGISTRATION_SCHEMA_V1:
            raise FitnessError("SCHEMA", "unsupported preregistration schema")
        expected = _semantic_id(PREREGISTRATION_SCHEMA_V1, self._payload())
        if self.preregistration_digest and self.preregistration_digest != expected:
            raise FitnessError(
                "PREREGISTRATION_DIGEST",
                "preregistration_digest does not match canonical content",
            )
        object.__setattr__(self, "preregistration_digest", expected)

    def _payload(self) -> dict[str, Any]:
        return {
            "formula": self.formula,
            "schema_version": self.schema_version,
            "sensitivity": self.sensitivity,
            "tie_rule": self.tie_rule,
            "units": self.units,
            "weights": [list(pair) for pair in self.weights],
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            **self._payload(),
            "preregistration_digest": self.preregistration_digest,
        }


@dataclass(frozen=True, slots=True)
class FitnessDimensionV1:
    """One measured dimension, carrying its own uncertainty and missing state."""

    name: str
    outcome: str
    observed: int | None
    total: int | None
    uncertainty: str

    def __post_init__(self) -> None:
        if type(self.name) is not str or not self.name:
            raise FitnessError("BAD_DIMENSION", "name must be a nonempty string")
        if self.outcome not in DIMENSION_OUTCOMES:
            raise FitnessError(
                "BAD_OUTCOME",
                f"{self.outcome!r} is not one of {sorted(DIMENSION_OUTCOMES)}",
            )
        if self.outcome == "MISSING":
            if self.observed is not None or self.total is not None:
                raise FitnessError(
                    "MISSING_WITH_COUNTS",
                    "a MISSING dimension was not evaluated, so it has no counts; "
                    "counts here would describe an evaluation that did not happen",
                )
        else:
            for label, value in (("observed", self.observed), ("total", self.total)):
                if type(value) is not int or type(value) is bool or value < 0:
                    raise FitnessError(
                        "BAD_COUNTS",
                        f"{label} must be a non-negative integer for an evaluated "
                        f"dimension, got {value!r}",
                    )
            if self.observed > self.total:
                raise FitnessError(
                    "BAD_COUNTS", "observed exceeds total"
                )
        if type(self.uncertainty) is not str or not self.uncertainty.strip():
            raise FitnessError(
                "UNCERTAINTY_ABSENT",
                f"dimension {self.name!r} states no uncertainty; the epic "
                "requires it on every dimension",
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "observed": self.observed,
            "outcome": self.outcome,
            "total": self.total,
            "uncertainty": self.uncertainty,
        }


@dataclass(frozen=True, slots=True)
class FitnessVectorV1:
    """A manifest-bound observation. It ranks review order and nothing else."""

    manifest_digest: str
    candidate_digest: str
    checker_id: str
    holdout_digest: str
    dimensions: tuple[FitnessDimensionV1, ...]
    scalar: str | None = None
    preregistration_digest: str = ""
    authority_effect: str = "None"
    schema_version: str = FITNESS_VECTOR_SCHEMA_V1
    vector_id: str = ""

    def __post_init__(self) -> None:
        _digest(self.manifest_digest, "manifest_digest")
        _digest(self.candidate_digest, "candidate_digest")
        _digest(self.holdout_digest, "holdout_digest")
        if type(self.checker_id) is not str or not self.checker_id:
            raise FitnessError("BAD_FIELD", "checker_id must be a nonempty string")
        if type(self.dimensions) is not tuple or not self.dimensions:
            raise FitnessError(
                "NO_DIMENSIONS",
                "a fitness vector with no dimensions ranks on nothing",
            )
        for dimension in self.dimensions:
            if type(dimension) is not FitnessDimensionV1:
                raise FitnessError(
                    "BAD_DIMENSION", "each dimension must be a FitnessDimensionV1"
                )
        names = [dimension.name for dimension in self.dimensions]
        if len(set(names)) != len(names):
            raise FitnessError("BAD_DIMENSION", "a dimension name appears twice")

        if self.scalar is not None:
            if not self.preregistration_digest:
                raise FitnessError(
                    "SCALAR_NOT_PREREGISTERED",
                    "a scalar hides dimension tradeoffs unless its formula, "
                    "units, weights, tie rule and sensitivity were frozen before "
                    "outcomes were observed",
                )
            _digest(self.preregistration_digest, "preregistration_digest")
            if type(self.scalar) is not str or not self.scalar.strip():
                raise FitnessError(
                    "BAD_SCALAR", "scalar must be a nonempty exact string"
                )

        if self.authority_effect != "None":
            raise FitnessError("AUTHORITY", "authority_effect must be None")
        if self.schema_version != FITNESS_VECTOR_SCHEMA_V1:
            raise FitnessError("SCHEMA", "unsupported fitness vector schema")
        expected = _semantic_id(FITNESS_VECTOR_SCHEMA_V1, self._payload())
        if self.vector_id and self.vector_id != expected:
            raise FitnessError(
                "VECTOR_ID", "vector_id does not match canonical content"
            )
        object.__setattr__(self, "vector_id", expected)

    def outcome_tally(self) -> dict[str, int]:
        """Every outcome reported separately, including the two that did not decide.

        There is deliberately no `pass_rate()`. A ratio has to choose what to do
        with `INCONCLUSIVE` and `MISSING`, and whatever it chooses is the
        collapse the epic forbids -- silently, because the caller sees only a
        number.
        """
        tally = {outcome: 0 for outcome in sorted(DIMENSION_OUTCOMES)}
        for dimension in self.dimensions:
            tally[dimension.outcome] += 1
        return tally

    def is_conclusive(self) -> bool:
        """True when every dimension decided. Reported, never assumed."""
        return all(
            dimension.outcome in DECIDED_OUTCOMES for dimension in self.dimensions
        )

    def undecided_dimensions(self) -> tuple[str, ...]:
        return tuple(
            dimension.name
            for dimension in self.dimensions
            if dimension.outcome in UNDECIDED_OUTCOMES
        )

    def comparable_with(self, other: "FitnessVectorV1") -> bool:
        """Whether two vectors may be compared at all.

        The acceptance condition: "changing a fitness formula, weight, seed,
        checker, holdout, renderer, or model" invalidates comparison. Two
        vectors measured under different conditions are two measurements, not a
        ranking.
        """
        if type(other) is not FitnessVectorV1:
            raise FitnessError("BAD_COMPARISON", "expected a FitnessVectorV1")
        return all(
            getattr(self, binding) == getattr(other, binding)
            for binding in COMPARISON_BINDINGS
        )

    def _payload(self) -> dict[str, Any]:
        return {
            "authority_effect": self.authority_effect,
            "candidate_digest": self.candidate_digest,
            "checker_id": self.checker_id,
            "dimensions": [dimension.to_dict() for dimension in self.dimensions],
            "holdout_digest": self.holdout_digest,
            "manifest_digest": self.manifest_digest,
            "preregistration_digest": self.preregistration_digest,
            "scalar": self.scalar,
            "schema_version": self.schema_version,
        }

    def to_dict(self) -> dict[str, Any]:
        return {**self._payload(), "vector_id": self.vector_id}


__all__ = [
    "COMPARISON_BINDINGS",
    "DECIDED_OUTCOMES",
    "DIMENSION_OUTCOMES",
    "FITNESS_VECTOR_SCHEMA_V1",
    "FitnessDimensionV1",
    "FitnessError",
    "FitnessVectorV1",
    "PREREGISTRATION_PARTS",
    "PREREGISTRATION_SCHEMA_V1",
    "ScalarPreregistrationV1",
    "UNDECIDED_OUTCOMES",
]
