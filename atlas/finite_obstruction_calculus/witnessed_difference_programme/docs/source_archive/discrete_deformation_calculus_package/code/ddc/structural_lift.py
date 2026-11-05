"""DDC letter Λ: licensed structural lift by zero-padding the carrier.

``iota: Q^n -> Q^(n+k)`` pads with zeros, so every l_p norm and every inner
product among old vectors is unchanged, and the new coordinates are
orthogonal to the old image. A lift needs a licence; a lift trigger is not a
licence. An explicit trigger must be ClosedResidual or DetectorInadequate (Law 4).
Licence identifiers and trigger classes are declared inputs, not authenticated
authorization or independently recomputed detector evidence.

A lift cannot make a non-exact residual exact: restriction back to the old
carrier commutes with ``d0``, so an exact extension would restrict to an exact
original. The survivor persists and is re-measured on the new carrier.

Leaf module: standard library only, loadable by path. AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import List, Optional, Sequence, Set, Tuple

LIFT_TRIGGERS = ("ClosedResidual", "DetectorInadequate")


def _exact(value: object) -> Fraction:
    if isinstance(value, (bool, float)) or not isinstance(value, (int, Fraction)):
        raise ValueError(f"NOT_EXACT: {value!r}")
    return Fraction(value)


def l1_norm(vector: List[Fraction]) -> Fraction:
    return sum((abs(_exact(x)) for x in vector), Fraction(0))


@dataclass(frozen=True)
class LiftReceipt:
    operation: str
    paper_id: str
    initial_dim: int
    extended_dim: int
    license_id: str
    lifted_vector: List[Fraction]
    success: bool
    error: Optional[str] = None
    trigger: Optional[str] = None
    authority_effect: str = "None"


class StructuralLifter:
    """Licensed carrier dimension expansion."""

    def __init__(self, authorized_licenses: Set[str]):
        self.authorized_licenses = frozenset(authorized_licenses)

    def _refuse(self, vector: List[Fraction], license_id: str, error: str, trigger: Optional[str]) -> LiftReceipt:
        return LiftReceipt(
            operation="Lambda",
            paper_id="DDC-L",
            initial_dim=len(vector),
            extended_dim=len(vector),
            license_id=license_id,
            lifted_vector=list(vector),
            success=False,
            error=error,
            trigger=trigger,
        )

    def lift(
        self,
        vector: List[Fraction],
        added_dims: int,
        license_id: str,
        trigger: Optional[str] = None,
    ) -> LiftReceipt:
        """Zero-pad if licensed and accompanied by an explicit Law 4 trigger."""
        vector = [_exact(value) for value in vector]
        if type(added_dims) is not int:
            raise ValueError(f"added_dims must be an int, not {type(added_dims).__name__}")
        if license_id not in self.authorized_licenses:
            return self._refuse(vector, license_id, "REFUSED_UNLICENSED_LIFT", trigger)
        if added_dims < 0:
            return self._refuse(vector, license_id, "INVALID_NEGATIVE_EXPANSION", trigger)
        if trigger not in LIFT_TRIGGERS:
            return self._refuse(vector, license_id, "REFUSED_LIFT_TRIGGER", trigger)
        lifted = list(vector) + [Fraction(0)] * added_dims
        return LiftReceipt(
            operation="Lambda",
            paper_id="DDC-L",
            initial_dim=len(vector),
            extended_dim=len(lifted),
            license_id=license_id,
            lifted_vector=lifted,
            success=True,
            error=None,
            trigger=trigger,
        )


@dataclass(frozen=True)
class FiniteLambdaStep:
    """Exact diagnostic row with declared Boolean descent/validity assumptions.

    The flags do not verify a preservation witness or an external contract.
    """

    before_phi: Fraction
    before_gamma: Fraction
    after_phi: Fraction
    after_gamma: Fraction
    is_descent: bool
    is_valid: bool

    def __post_init__(self) -> None:
        for name in ("before_phi", "before_gamma", "after_phi", "after_gamma"):
            value = _exact(getattr(self, name))
            if value < 0:
                raise ValueError("NEGATIVE_DIAGNOSTIC")
            object.__setattr__(self, name, value)
        for name in ("is_descent", "is_valid"):
            if type(getattr(self, name)) is not bool:
                raise TypeError(f"{name} must be bool")


@dataclass(frozen=True)
class FiniteLambdaLedger:
    """Abstract chaining analogue of L-DDA-44/45, conditional on row flags.

    Endpoints and adjacency are checked here; external certificate validity,
    preservation and descent semantics are not established by these flags.
    """

    initial_phi: Fraction
    initial_gamma: Fraction
    steps: Tuple[FiniteLambdaStep, ...]
    terminal_phi: Fraction
    terminal_gamma: Fraction

    def __post_init__(self) -> None:
        for name in ("initial_phi", "initial_gamma", "terminal_phi", "terminal_gamma"):
            value = _exact(getattr(self, name))
            if value < 0:
                raise ValueError("NEGATIVE_DIAGNOSTIC")
            object.__setattr__(self, name, value)
        steps = tuple(self.steps)
        if any(not isinstance(step, FiniteLambdaStep) for step in steps):
            raise TypeError("steps must contain FiniteLambdaStep rows")
        object.__setattr__(self, "steps", steps)

    @classmethod
    def new(
        cls,
        initial: Tuple[object, object],
        steps: Sequence[FiniteLambdaStep],
        terminal: Tuple[object, object],
    ) -> FiniteLambdaLedger:
        init_phi, init_gamma = _exact(initial[0]), _exact(initial[1])
        term_phi, term_gamma = _exact(terminal[0]), _exact(terminal[1])
        return cls(
            initial_phi=init_phi,
            initial_gamma=init_gamma,
            steps=tuple(steps),
            terminal_phi=term_phi,
            terminal_gamma=term_gamma,
        )

    def require_chained(self) -> bool:
        """Check the abstract sequence gate, conditional on supplied flags:

        1. An empty ledger requires initial == terminal and resolved (phi=0, gamma=0).
        2. Non-empty ledger: step[0].before == initial, step[-1].after == terminal.
        3. Step adjacency: step[i].after == step[i+1].before for all i.
        4. Every non-final row has the declared is_descent flag True.
        5. The final row has the declared is_valid flag True.

        This is not execution of the Rust require_descent_step/require_valid
        methods and supplies no proof of contract conformance.
        """
        if not self.steps:
            if (self.initial_phi, self.initial_gamma) != (self.terminal_phi, self.terminal_gamma):
                raise ValueError("EMPTY_LEDGER_ENDPOINT_MISMATCH: initial != terminal")
            if self.initial_phi != 0 or self.initial_gamma != 0:
                raise ValueError("EMPTY_LEDGER_UNRESOLVED: empty ledger requires resolved endpoints (0, 0)")
            return True

        if (self.steps[0].before_phi, self.steps[0].before_gamma) != (self.initial_phi, self.initial_gamma):
            raise ValueError("HEAD_MISMATCH: step[0].before != initial")

        if (self.steps[-1].after_phi, self.steps[-1].after_gamma) != (self.terminal_phi, self.terminal_gamma):
            raise ValueError("TAIL_MISMATCH: step[-1].after != terminal")

        for i in range(len(self.steps) - 1):
            curr_step = self.steps[i]
            next_step = self.steps[i + 1]
            if (curr_step.after_phi, curr_step.after_gamma) != (next_step.before_phi, next_step.before_gamma):
                raise ValueError(f"BROKEN_CHAIN: step[{i}].after != step[{i+1}].before")
            if not curr_step.is_descent:
                raise ValueError(f"NON_FINAL_ROW_NOT_DESCENT: step[{i}] is not a descent step")

        if not self.steps[-1].is_valid:
            raise ValueError("FINAL_ROW_INVALID: final step is not valid")

        return True
