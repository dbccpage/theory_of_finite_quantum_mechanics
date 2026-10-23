"""The DDC tape automaton: step laws, control laws, and receipts.

This module is the executable counterpart of ``lean4/Ddc/Law.lean``; the two
state the same laws. A step is a letter, the state after it, and the
witnesses it carries. The paper laws refine the deposited historical comparison specification.
``ENGINE_CODES`` and ``PAPER_CODES`` retain their historical names; they do not
state which checks a current deployed engine performs.

``State`` and ``Witness`` are inputs to an abstract policy checker. Use
``measure`` to compute diagnostics, and pass ``carriers`` to ``run_tape`` to
recompute them and check that R preserves the quotient class. Witness flags
remain hypotheses; this module does not authenticate receipts or licences.
AuthorityEffect: None.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from fractions import Fraction
from typing import List, Mapping, Optional, Sequence, Tuple

import cochain
from integration_tape import ExecutionTape, canonical_json
from typed_refusal import M_REASONS

LETTERS = ("E", "R", "C", "I", "Λ", "D", "M", "T")
FIXED_CARRIER = ("E", "R")
INERT = ("I", "M", "T")
RESTRUCTURE = ("C", "D", "Λ")

OPEN_CONTROL = "Open"
REFUSED = "Refused"
TERMINALIZED = "Terminalized"

EXACT = cochain.EXACT_REPAIR
CLOSED = cochain.CLOSED_RESIDUAL
ACTIVE = cochain.ACTIVE_CLOSURE_FAILURE

# Violation codes in the historical comparison specification (same names as OpViolation).
ENGINE_CODES = (
    "ExactRepairLeftResidual",
    "FixedCarrierOpChangedCarrier",
    "ResidualProjectionChangedMass",
    "InertOpMutatedState",
    "TerminalizedOpenResidual",
    "CarrierUnchangedUnderRestructure",
)
# Additional paper laws beyond the historical comparison model.
PAPER_CODES = (
    "ExactRepairFromNonExactClass",
    "ExactRepairLeftDefect",
    "ResidualProjectionChangedClosure",
    "ContextExposureLoweredObstruction",
    "MissingReceipt",
    "MissingLossLedger",
    "UnlicensedLift",
    "LiftWithoutTrigger",
    "MissingRefusalReason",
    "BlindDetector",
    "TerminalAbsorbing",
    "RefusalAbsorbing",
    "UnknownLetter",
)

REASON_FOR = {
    "ExactRepairFromNonExactClass": "REFUSED_NON_ZERO_CURL",
    "MissingReceipt": "REFUSED_MISSING_RECEIPT",
    "MissingLossLedger": "REFUSED_MISSING_LOSS_LEDGER",
    "UnlicensedLift": "REFUSED_UNLICENSED_LIFT",
    "LiftWithoutTrigger": "REFUSED_LIFT_TRIGGER",
    "TerminalizedOpenResidual": "REFUSED_OPEN_OBSTRUCTION",
    "BlindDetector": "REFUSED_DETECTOR_INADEQUATE",
}


@dataclass(frozen=True)
class State:
    """Abstract state; direct construction does not certify its diagnostics."""

    carrier: str
    residual: Tuple[Fraction | int, ...]
    phi: Fraction | int
    gamma: Fraction | int
    adequate: bool = True

    def __post_init__(self) -> None:
        if not isinstance(self.carrier, str) or not self.carrier:
            raise ValueError("carrier must be a nonempty string")
        object.__setattr__(self, "residual", cochain.exact_vector(self.residual))
        object.__setattr__(self, "phi", cochain.exact(self.phi))
        object.__setattr__(self, "gamma", cochain.exact(self.gamma))
        if type(self.adequate) is not bool:
            raise TypeError("adequate must be bool")
        if self.phi < 0 or self.gamma < 0:
            raise ValueError("NEGATIVE_DIAGNOSTIC")

    @property
    def cls(self) -> str:
        if self.gamma > 0:
            return ACTIVE
        return EXACT if self.phi == 0 else CLOSED

    def digest(self) -> str:
        body = canonical_json(
            {
                "carrier": self.carrier,
                "residual": list(self.residual),
                "phi": self.phi,
                "gamma": self.gamma,
                "adequate": self.adequate,
            }
        )
        return hashlib.sha256(body.encode("utf-8")).hexdigest()


def measure(cx: cochain.Complex, residual: Sequence[object], carrier: str, adequate: bool = True) -> State:
    """A state whose Phi1 (dual-certified) and Gamma2 are computed from the declared complex."""
    x = cochain.exact_vector(residual)
    return State(carrier, x, cochain.phi1_certificate(cx, x).value, cochain.gamma2(cx, x), adequate)


@dataclass(frozen=True)
class Witness:
    """Abstract assumptions about evidence presence, not evidence verification."""
    receipt: bool = False
    loss_ledger: bool = False
    lift_licence: bool = False
    reason: Optional[str] = None

    def __post_init__(self) -> None:
        for name in ("receipt", "loss_ledger", "lift_licence"):
            value = getattr(self, name)
            if type(value) is not bool:
                raise TypeError(f"{name} must be bool, not {type(value).__name__}")


@dataclass(frozen=True)
class Step:
    letter: str
    after: State
    witness: Witness = field(default_factory=Witness)


def step_violations(letter: str, before: State, after: State, witness: Witness) -> Tuple[str, ...]:
    """Every paper law the step breaks; empty means lawful."""
    v: List[str] = []
    same_carrier = before.carrier == after.carrier
    if letter == "E":
        if not same_carrier:
            v.append("FixedCarrierOpChangedCarrier")
        if before.cls != EXACT:
            v.append("ExactRepairFromNonExactClass")
        if after.phi != 0 or after.gamma != 0:
            v.append("ExactRepairLeftResidual")
        if any(x != 0 for x in after.residual):
            v.append("ExactRepairLeftDefect")
        if not before.adequate:
            v.append("BlindDetector")
    elif letter == "R":
        if not same_carrier:
            v.append("FixedCarrierOpChangedCarrier")
        if after.phi != before.phi:
            v.append("ResidualProjectionChangedMass")
        if after.gamma != before.gamma:
            v.append("ResidualProjectionChangedClosure")
        if not before.adequate:
            v.append("BlindDetector")
    elif letter == "C":
        if same_carrier:
            v.append("CarrierUnchangedUnderRestructure")
        if after.phi < before.phi or after.gamma < before.gamma:
            v.append("ContextExposureLoweredObstruction")
    elif letter == "I":
        if after != before:
            v.append("InertOpMutatedState")
        if not witness.receipt:
            v.append("MissingReceipt")
    elif letter == "Λ":
        if same_carrier:
            v.append("CarrierUnchangedUnderRestructure")
        if not witness.lift_licence:
            v.append("UnlicensedLift")
        if not (before.cls == CLOSED or not before.adequate):
            v.append("LiftWithoutTrigger")
    elif letter == "D":
        if same_carrier:
            v.append("CarrierUnchangedUnderRestructure")
        if not witness.loss_ledger:
            v.append("MissingLossLedger")
    elif letter == "M":
        if after != before:
            v.append("InertOpMutatedState")
        if witness.reason not in M_REASONS:
            v.append("MissingRefusalReason")
    elif letter == "T":
        if after != before:
            v.append("InertOpMutatedState")
        if after.gamma != 0:
            v.append("TerminalizedOpenResidual")
        if not before.adequate:
            v.append("BlindDetector")
    else:
        v.append("UnknownLetter")
    return tuple(v)


def engine_violations(letter: str, before: State, after: State) -> Tuple[str, ...]:
    """The deposited historical comparison laws on the same abstract state."""
    v: List[str] = []
    same_carrier = before.carrier == after.carrier
    if letter in FIXED_CARRIER and not same_carrier:
        v.append("FixedCarrierOpChangedCarrier")
    if letter == "E" and (after.phi != 0 or after.gamma != 0):
        v.append("ExactRepairLeftResidual")
    if letter == "R" and after.phi != before.phi:
        v.append("ResidualProjectionChangedMass")
    if letter in INERT and after != before:
        v.append("InertOpMutatedState")
    if letter == "T" and after.gamma != 0:
        v.append("TerminalizedOpenResidual")
    if letter in RESTRUCTURE and same_carrier:
        v.append("CarrierUnchangedUnderRestructure")
    return tuple(v)


def control_violation(control: str, letter: str) -> Optional[str]:
    if control == TERMINALIZED:
        return "TerminalAbsorbing"
    if control == REFUSED and letter not in ("C", "Λ", "T"):
        return "RefusalAbsorbing"
    return None


def next_control(control: str, letter: str) -> str:
    if letter == "T":
        return TERMINALIZED
    if letter == "M":
        return REFUSED
    if control == REFUSED:
        return OPEN_CONTROL
    return control


def routing_terminal(state: State) -> str:
    """Routing axis of a lawful T: CheckPassed on an exact state, Residual on a closed one."""
    return "CheckPassed" if state.cls == EXACT else "Residual"


@dataclass
class TapeRun:
    lawful: bool
    letters: str
    final_state: State
    final_control: str
    halted_at: Optional[int]
    violations: Tuple[str, ...]
    tape: ExecutionTape

    @property
    def authority_effect(self) -> str:
        return "None"


def run_tape(
    initial: State,
    steps: Sequence[Step],
    control: str = OPEN_CONTROL,
    genesis_root: str = "DDC_TAPE_GENESIS",
    carriers: Mapping[str, cochain.Complex] | None = None,
) -> TapeRun:
    """Check abstract laws, optionally recomputing diagnostics on supplied carriers.

    A successful result is conditional on witness flags and detector adequacy.
    The optional carrier map also checks R's stronger quotient-preservation
    obligation; the Lean ``stepLaw`` only checks its diagnostic invariants.
    """
    if control not in (OPEN_CONTROL, REFUSED, TERMINALIZED):
        raise ValueError("UNKNOWN_CONTROL")
    if carriers is not None:
        carriers = dict(carriers)
        identities = {name: {"vertices": cx.vertices, "edges": cx.edges, "faces": cx.faces,
                             "weights": tuple(cx.weight(i) for i in range(len(cx.edges)))}
                      for name, cx in carriers.items()}
        genesis_root += ":" + hashlib.sha256(canonical_json(identities).encode("utf-8")).hexdigest()
    tape = ExecutionTape(genesis_root)
    state = initial
    if carriers is not None:
        violations = measured_state_violations(state, carriers)
        if violations:
            return TapeRun(False, "", state, control, 0, violations, tape)
    for index, step in enumerate(steps):
        violations = tuple(
            code
            for code in (control_violation(control, step.letter),)
            if code is not None
        ) + step_violations(step.letter, state, step.after, step.witness)
        if carriers is not None:
            violations += measured_state_violations(step.after, carriers)
            if not violations and step.letter == "R":
                difference = cochain.exact_vector(tuple(a - b for a, b in zip(state.residual, step.after.residual)))
                if cochain.exact_potential(carriers[state.carrier], difference) is None:
                    violations += ("ResidualProjectionChangedClass",)
        if violations:
            return TapeRun(False, "".join(s.letter for s in steps[:index]), state, control, index, violations, tape)
        control = next_control(control, step.letter)
        tape.append(
            step.letter,
            {
                "step_index": index,
                "before_digest": state.digest(),
                "after_digest": step.after.digest(),
                "carrier_before": state.carrier,
                "carrier_after": step.after.carrier,
                "class_before": state.cls,
                "class_after": step.after.cls,
                "phi_before": state.phi,
                "phi_after": step.after.phi,
                "gamma_before": state.gamma,
                "gamma_after": step.after.gamma,
                "witness": {
                    "receipt": step.witness.receipt,
                    "loss_ledger": step.witness.loss_ledger,
                    "lift_licence": step.witness.lift_licence,
                    "reason": step.witness.reason,
                },
                "control_after": control,
                "routing_terminal": routing_terminal(step.after) if step.letter == "T" else None,
                "authority_effect": "None",
            },
        )
        state = step.after
    return TapeRun(True, "".join(s.letter for s in steps), state, control, None, (), tape)


def measured_state_violations(state: State, carriers: Mapping[str, cochain.Complex]) -> Tuple[str, ...]:
    cx = carriers.get(state.carrier)
    if cx is None:
        return ("UnknownCarrier",)
    try:
        measured = measure(cx, state.residual, state.carrier, state.adequate)
    except cochain.CochainError as error:
        return (error.code,)
    return () if measured == state else ("DiagnosticMismatch",)
