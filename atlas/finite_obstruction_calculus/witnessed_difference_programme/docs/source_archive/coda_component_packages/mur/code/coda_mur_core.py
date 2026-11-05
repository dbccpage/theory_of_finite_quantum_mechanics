# -*- coding: utf-8 -*-
"""
coda_mur_core.py: Certified Representation Transport Gate for CODA-MUR (Omega-chi).

Core Mechanics:
1. Representation Regimes & Morphisms (MorphismKind: exact, quotient, embedding, approximation, unmeasured).
2. Descent Compatibility Certificate (chi_F : D_B F => barF D_A) with finite verification model.
3. Loss Ledger Monoid (L_{G circ F} = L_G + L_F) with strict dimension accounting.
4. Kind Composition Monoid: full 5x5 total order monoid with exact identity and unmeasured absorption.
5. Terminal Non-Bypass Firewall: chi_F alone is NOT sufficient for target authority;
   explicit target terminalization tau_B and target IsAuth_B are mandatory.
6. Exact Cochain Quotient Solver Bridge with verified dual witness certificates.
7. Zero Floats Invariant: all numerical scalars are exact sympy.Rational or fractions.Fraction.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from typing import Any, Callable, Optional, Tuple, Union, cast

from cochain_presentation import (
    LinearRepairProblem,
    QuotientDistanceCertificate,
    exact_equal,
    exact_matrix_from_matrix,
)
from sympy import ImmutableMatrix, Integer, Rational
from sympy.matrices.matrixbase import MatrixBase

# Exact rational diagnostic constants for policy branches (schematic diagnostics, not empirical defect bounds)
DIAGNOSTIC_NO_TRANSPORT = Rational(1, 1)
DIAGNOSTIC_UNPRICED_LOSS = Rational(3, 4)
DIAGNOSTIC_NO_TERMINAL = Rational(1, 2)
DIAGNOSTIC_TARGET_UNAUTH = Rational(1, 4)
DIAGNOSTIC_SUCCESS = Rational(0, 1)

# Backward-compatible aliases
RESIDUAL_NO_TRANSPORT = DIAGNOSTIC_NO_TRANSPORT
RESIDUAL_UNPRICED_LOSS = DIAGNOSTIC_UNPRICED_LOSS
RESIDUAL_NO_TERMINAL = DIAGNOSTIC_NO_TERMINAL
RESIDUAL_TARGET_UNAUTH = DIAGNOSTIC_TARGET_UNAUTH
RESIDUAL_SUCCESS = DIAGNOSTIC_SUCCESS


def _validate_exact_rational(val: Any, name: str) -> Rational:
    """Ensure value is an exact rational or integer, rejecting floats and booleans."""
    if isinstance(val, bool):
        raise TypeError(f"{name} must be an exact rational or integer, got bool")
    if isinstance(val, float) or (getattr(val, "dtype", None) is not None and "float" in str(val.dtype)):
        raise TypeError(f"{name} must be an exact rational or integer, got float (floats strictly forbidden)")
    if isinstance(val, (int, Integer, Fraction, Rational)):
        return Rational(val)
    if isinstance(val, str):
        try:
            return Rational(val)
        except Exception as exc:
            raise TypeError(f"{name} string could not be converted to exact Rational: {exc}") from exc
    raise TypeError(f"{name} must be an exact rational or integer, got {type(val).__name__}")


def _validate_exact_int(val: Any, name: str) -> int:
    """Ensure value is an exact non-negative integer, rejecting floats and booleans."""
    if isinstance(val, bool):
        raise TypeError(f"{name} must be an integer, got bool")
    dtype = getattr(val, "dtype", None)
    if not isinstance(val, (int, Integer)) or (dtype is not None and "float" in str(dtype)):
        raise TypeError(f"{name} must be an integer, got {type(val).__name__}")
    int_val = int(val)
    if int_val < 0:
        raise ValueError(f"{name} must be non-negative, got {int_val}")
    return int_val


def _validate_strict_bool(val: Any, name: str) -> bool:
    """Ensure value is strictly of type bool, rejecting strings and numbers."""
    if not isinstance(val, bool):
        raise TypeError(f"{name} must be bool, got {type(val).__name__} ({val!r})")
    return val


class MorphismKind(str, Enum):
    """Classification of representation morphisms (MUR-D1 / MUR-D2)."""

    EXACT = "exact"
    EMBEDDING = "embedding"
    QUOTIENT = "quotient"
    APPROXIMATION = "approximation"
    UNMEASURED = "unmeasured"

    def is_loss_required(self) -> bool:
        """Quotient, approximation, and unmeasured morphisms require declared loss accounting."""
        return self in (
            MorphismKind.QUOTIENT,
            MorphismKind.APPROXIMATION,
            MorphismKind.UNMEASURED,
        )


_KIND_ORDER = {
    MorphismKind.EXACT: 0,
    MorphismKind.EMBEDDING: 1,
    MorphismKind.QUOTIENT: 2,
    MorphismKind.APPROXIMATION: 3,
    MorphismKind.UNMEASURED: 4,
}


def compose_kinds(kind_f: MorphismKind, kind_g: MorphismKind) -> MorphismKind:
    """
    Associative kind composition monoid for representation transport.

    Ordered total-order semilattice with identity EXACT:
      EXACT (0) < EMBEDDING (1) < QUOTIENT (2) < APPROXIMATION (3) < UNMEASURED (4)

    Properties:
    - Left & Right identity: compose_kinds(EXACT, k) == k == compose_kinds(k, EXACT)
    - Associativity: compose_kinds(compose_kinds(a, b), c) == compose_kinds(a, compose_kinds(b, c))
    - Absorbing element: compose_kinds(UNMEASURED, k) == UNMEASURED
    """
    return max((kind_f, kind_g), key=_KIND_ORDER.__getitem__)


@dataclass(frozen=True)
class LossLedger:
    """
    Finite loss ledger recording representation loss dimensions (MUR-D3 / MUR-T8).

    e: erasure (quotient identification of fibres)
    i: imprecision (scale/resolution reduction)
    a: approximation (discretization/truncation)
    u: unmeasured (opaque transformation)
    loss_mass: exact rational loss metric
    """

    e: bool = False
    i: bool = False
    a: bool = False
    u: bool = False
    loss_mass: Rational = Rational(0, 1)

    def __init__(
        self,
        e: bool = False,
        i: bool = False,
        a: bool = False,
        u: bool = False,
        loss_mass: Union[int, Rational, Fraction, str] = Rational(0, 1),
    ) -> None:
        object.__setattr__(self, "e", _validate_strict_bool(e, "e"))
        object.__setattr__(self, "i", _validate_strict_bool(i, "i"))
        object.__setattr__(self, "a", _validate_strict_bool(a, "a"))
        object.__setattr__(self, "u", _validate_strict_bool(u, "u"))
        validated_mass = _validate_exact_rational(loss_mass, "loss_mass")
        if validated_mass < 0:
            raise ValueError(f"loss_mass must be non-negative, got {validated_mass}")
        object.__setattr__(self, "loss_mass", validated_mass)

    @classmethod
    def empty(cls) -> LossLedger:
        return cls(e=False, i=False, a=False, u=False, loss_mass=Rational(0, 1))

    def is_empty(self) -> bool:
        return not (self.e or self.i or self.a or self.u or self.loss_mass > 0)

    def is_valid_for_kind(self, kind: MorphismKind) -> bool:
        """Verify that the qualitative loss dimension matches the morphism kind obligations."""
        if not kind.is_loss_required():
            return True
        if self.is_empty():
            return False
        if kind == MorphismKind.QUOTIENT:
            return self.e is True
        if kind == MorphismKind.APPROXIMATION:
            return (self.a is True) or (self.i is True)
        return self.u is True  # Remaining loss-requiring kind: UNMEASURED.

    def accumulate(self, other: LossLedger) -> LossLedger:
        """Associative monoidal loss accumulation (MUR-T8: L_{G circ F} = L_G + L_F)."""
        return LossLedger(
            e=self.e or other.e,
            i=self.i or other.i,
            a=self.a or other.a,
            u=self.u or other.u,
            loss_mass=self.loss_mass + other.loss_mass,
        )


@dataclass(frozen=True)
class DescentSquareCertificate:
    """
    Descent square certificate chi_F : D_B F => barF D_A (MUR-D2).

    Verification requires all four maps and a non-empty finite source carrier.
    Boolean flags can veto a certificate; they never replace pointwise checks.
    Optional defect evidence is bound to a declared cochain and repair map.
    """

    source_regime: str
    target_regime: str
    morphism_name: str
    morphism_kind: MorphismKind
    chi_certified: bool
    commutes: bool = True
    loss_ledger: Optional[LossLedger] = None
    defect_vector: Optional[MatrixBase] = None
    state_map: Optional[Callable[[Any], Any]] = None
    observation_map: Optional[Callable[[Any], Any]] = None
    source_look: Optional[Callable[[Any], Any]] = None
    target_look: Optional[Callable[[Any], Any]] = None
    carrier: Optional[Tuple[Any, ...]] = None
    leg_ledgers: Optional[Tuple[Optional[LossLedger], ...]] = None
    repair_map: Optional[MatrixBase] = None

    def __post_init__(self) -> None:
        _validate_strict_bool(self.chi_certified, "chi_certified")
        _validate_strict_bool(self.commutes, "commutes")
        if self.carrier is not None:
            object.__setattr__(self, "carrier", tuple(self.carrier))
        if self.leg_ledgers is not None:
            object.__setattr__(self, "leg_ledgers", tuple(self.leg_ledgers))
        for name in ("defect_vector", "repair_map"):
            value = getattr(self, name)
            if value is not None:
                object.__setattr__(self, name, ImmutableMatrix(exact_matrix_from_matrix(value)))

    def verify(self) -> bool:
        """Evaluate the complete declared square on every listed source."""
        if not (self.chi_certified and self.commutes and self.carrier):
            return False
        state, observations = self.state_map, self.observation_map
        source, target = self.source_look, self.target_look
        if not (callable(state) and callable(observations) and callable(source) and callable(target)):
            return False
        try:
            return all(target(state(x)) == observations(source(x)) for x in self.carrier)
        except Exception:
            return False

    def is_valid(self) -> bool:
        """Full certificate validity check enforcing commutation, verification, and ledger rules."""
        if not (self.chi_certified and self.commutes):
            return False

        if not self.verify():
            return False

        if self.morphism_kind.is_loss_required():
            if self.loss_ledger is None or self.loss_ledger.is_empty():
                return False
            if not self.loss_ledger.is_valid_for_kind(self.morphism_kind):
                return False
        else:
            # Exact and embedding morphisms must be strictly loss-free
            if self.loss_ledger is not None and not self.loss_ledger.is_empty():
                return False
        return True



def _extract_leaves(cert: DescentSquareCertificate) -> Tuple[Optional[LossLedger], ...]:
    if cert.leg_ledgers is not None and len(cert.leg_ledgers) > 0:
        return cert.leg_ledgers
    return (cert.loss_ledger,)


def paste_certificates(
    chi_f: DescentSquareCertificate,
    chi_g: DescentSquareCertificate,
    composite_name: Optional[str] = None,
) -> DescentSquareCertificate:
    """
    Pasting law for descent square certificates (MUR-T1 / MUR-T2).

    Requires both input legs to be independently valid.
    Composes kinds via the associative 5x5 total-order monoid.
    Enforces shared intermediate presentation agreement, carrier coverage,
    associative leaf preservation, and strict defect vector shape compatibility.
    """
    if not chi_f.is_valid():
        raise ValueError(f"Cannot paste: first leg '{chi_f.morphism_name}' is not valid")
    if not chi_g.is_valid():
        raise ValueError(f"Cannot paste: second leg '{chi_g.morphism_name}' is not valid")
    if chi_f.target_regime != chi_g.source_regime:
        raise ValueError(
            f"Cannot paste certificates: target '{chi_f.target_regime}' does not match source '{chi_g.source_regime}'"
        )

    # Incompatible defect vectors: require declared matching spaces/shapes
    composite_defect = None
    if chi_f.defect_vector is not None and chi_g.defect_vector is not None:
        if chi_f.defect_vector.shape != chi_g.defect_vector.shape:
            raise ValueError(
                f"Cannot paste certificates: incompatible defect vector spaces/shapes "
                f"({chi_f.defect_vector.shape} != {chi_g.defect_vector.shape})"
            )
        composite_defect = chi_f.defect_vector + chi_g.defect_vector
    elif chi_g.defect_vector is not None:
        composite_defect = chi_g.defect_vector
    elif chi_f.defect_vector is not None:
        composite_defect = chi_f.defect_vector

    # Intermediate presentation agreement and carrier coverage for finite models
    # is_valid above requires a complete finite square on each leg.
    assert chi_f.carrier is not None
    assert chi_f.state_map is not None
    assert chi_f.target_look is not None
    assert chi_g.source_look is not None
    assert chi_g.carrier is not None
    assert chi_g.target_look is not None
    assert chi_g.state_map is not None
    assert chi_g.observation_map is not None

    for x in chi_f.carrier:
        y = chi_f.state_map(x)
        # Check intermediate observation/look agreement
        try:
            look_f = chi_f.target_look(y)
            look_g = chi_g.source_look(y)
        except Exception as exc:
            raise ValueError(f"Cannot paste certificates: intermediate observation/look evaluation failed on {y!r}: {exc}") from exc
        if look_f != look_g:
            raise ValueError(
                f"Cannot paste certificates: intermediate observation/look maps disagree on state {y!r} "
                f"({look_f!r} != {look_g!r})"
            )

        # Check coverage by second carrier or dynamic verification
        if y not in chi_g.carrier:
            try:
                route_st = chi_g.target_look(chi_g.state_map(y))
                route_ob = chi_g.observation_map(chi_g.source_look(y))
                if route_st != route_ob:
                    raise ValueError(
                        f"Cannot paste certificates: intermediate state {y!r} from carrier not covered by second leg"
                    )
            except Exception as exc:
                raise ValueError(
                    f"Cannot paste certificates: intermediate state {y!r} from carrier not covered by second leg: {exc}"
                ) from exc

    composite_kind = compose_kinds(chi_f.morphism_kind, chi_g.morphism_kind)

    # Addition of defect coordinates has a common declared repair model only
    # when both supplied models agree. Never attach an unrelated model.
    composite_repair_map = chi_f.repair_map if chi_f.repair_map is not None else chi_g.repair_map
    if chi_f.repair_map is not None and chi_g.repair_map is not None:
        if not exact_equal(chi_f.repair_map, chi_g.repair_map):
            raise ValueError("Cannot paste certificates: repair models disagree")

    # Accumulate loss ledgers and preserve leaf sequence history
    ledger_f = chi_f.loss_ledger or LossLedger.empty()
    ledger_g = chi_g.loss_ledger or LossLedger.empty()
    composite_ledger = ledger_f.accumulate(ledger_g)
    per_leg = _extract_leaves(chi_f) + _extract_leaves(chi_g)

    f_state, g_state = chi_f.state_map, chi_g.state_map
    f_obs, g_obs = chi_f.observation_map, chi_g.observation_map
    assert f_state is not None and g_state is not None
    assert f_obs is not None and g_obs is not None

    def composite_state_map(x: Any) -> Any:
        return g_state(f_state(x))

    def composite_obs_map(a: Any) -> Any:
        return g_obs(f_obs(a))

    result_cert = DescentSquareCertificate(
        source_regime=chi_f.source_regime,
        target_regime=chi_g.target_regime,
        morphism_name=composite_name or f"{chi_g.morphism_name}_circ_{chi_f.morphism_name}",
        morphism_kind=composite_kind,
        chi_certified=chi_f.chi_certified and chi_g.chi_certified,
        commutes=chi_f.commutes and chi_g.commutes,
        loss_ledger=composite_ledger if not composite_ledger.is_empty() else None,
        defect_vector=composite_defect,
        repair_map=composite_repair_map,
        state_map=composite_state_map,
        observation_map=composite_obs_map,
        source_look=chi_f.source_look,
        target_look=chi_g.target_look,
        carrier=chi_f.carrier,
        leg_ledgers=per_leg,
    )

    if not result_cert.is_valid():
        raise ValueError(f"Cannot paste certificates: composite certificate '{result_cert.morphism_name}' is not valid")

    return result_cert



@dataclass(frozen=True)
class FiniteCoreAction:
    """
    Induced finite-core action on live cores.
    Maps accepted core representatives from source to target regime loss-free.
    """

    source_regime: str
    target_regime: str
    action_map: Callable[[Any], Any]
    is_loss_free: bool = True

    def apply(self, source_core: Any) -> Any:
        return self.action_map(source_core)

    def compose(self, next_action: FiniteCoreAction) -> FiniteCoreAction:
        if self.target_regime != next_action.source_regime:
            raise ValueError(
                f"Cannot compose actions: target '{self.target_regime}' != source '{next_action.source_regime}'"
            )
        return FiniteCoreAction(
            source_regime=self.source_regime,
            target_regime=next_action.target_regime,
            action_map=lambda x: next_action.apply(self.apply(x)),
            is_loss_free=self.is_loss_free and next_action.is_loss_free,
        )


@dataclass(frozen=True)
class TerminalRegime:
    """Target representation regime with explicit terminalization (MUR-T6)."""

    regime_id: str
    terminalize: Callable[[Any], Optional[str]]
    is_auth: Callable[[str], bool]


@dataclass(frozen=True)
class TransportResult:
    """Result of certified representation transport and target terminalization."""

    inhabited: bool
    target_terminal: Optional[str]
    refusal_code: Optional[str]
    residual_mass: Rational
    certificate: Optional[DescentSquareCertificate]
    quotient_certificate: Optional[QuotientDistanceCertificate] = None
    authority_effect: str = "None"


def compute_transport_quotient_obstruction(
    repair_map: MatrixBase,
    defect_cochain: MatrixBase,
) -> QuotientDistanceCertificate:
    """
    Solve exact quotient obstruction Q^1_chi = C^1_chi / im(d0).

    Uses LinearRepairProblem to compute exact l1 distance with certified dual witness.
    """
    problem = LinearRepairProblem(repair_map)
    return problem.quotient_l1_distance(defect_cochain)


def evaluate_transport_authority(
    source_artifact_id: str,
    target_regime: TerminalRegime,
    transported_artifact: Any,
    certificate: Optional[DescentSquareCertificate],
    quotient_certificate: Optional[QuotientDistanceCertificate] = None,
    action: Optional[FiniteCoreAction] = None,
    source_regime: Optional[str] = None,
) -> TransportResult:
    """Check a finite square, the requested transport, its loss and local terminal.

    The declared callbacks are trusted to describe the intended finite model;
    their evaluated equalities do not establish external semantic truth.
    """
    snapshot: Optional[QuotientDistanceCertificate] = None

    def refuse(code: str, mass: Rational = DIAGNOSTIC_NO_TRANSPORT,
               terminal: Optional[str] = None) -> TransportResult:
        return TransportResult(False, terminal, code, mass, certificate, snapshot)

    if certificate is None or not certificate.verify():
        return refuse("R_notransport")
    if certificate.target_regime != target_regime.regime_id:
        return refuse("R_regime_mismatch")
    if source_regime is not None and certificate.source_regime != source_regime:
        return refuse("R_regime_mismatch")

    # Also evaluate the requested source. This explicitly extends the checked
    # finite set when it was not among the stored carrier representatives.
    state = cast(Callable[[Any], Any], certificate.state_map)
    observations = cast(Callable[[Any], Any], certificate.observation_map)
    source = cast(Callable[[Any], Any], certificate.source_look)
    target = cast(Callable[[Any], Any], certificate.target_look)
    try:
        expected = state(source_artifact_id)
        if target(expected) != observations(source(source_artifact_id)):
            return refuse("R_notransport")
    except Exception:
        return refuse("R_notransport")
    if action is not None:
        if action.source_regime != certificate.source_regime or action.target_regime != certificate.target_regime:
            raise ValueError("FiniteCoreAction regimes do not match certificate")
        try:
            if action.apply(source_artifact_id) != expected:
                return refuse("R_substituted_artifact")
        except Exception:
            return refuse("R_substituted_artifact")
    if transported_artifact is None:
        transported_artifact = expected
    elif transported_artifact != expected:
        return refuse("R_substituted_artifact")

    ledger = certificate.loss_ledger
    if certificate.morphism_kind.is_loss_required():
        if ledger is None or not ledger.is_valid_for_kind(certificate.morphism_kind):
            return refuse("R_unpriced_loss", DIAGNOSTIC_UNPRICED_LOSS)
    elif ledger is not None and not ledger.is_empty():
        return refuse("R_unpriced_loss", DIAGNOSTIC_UNPRICED_LOSS)

    if quotient_certificate is not None:
        if not isinstance(quotient_certificate, QuotientDistanceCertificate):
            return refuse("R_malformed_quotient")
        snapshot = quotient_certificate.snapshot()
        if (not snapshot.verify() or certificate.defect_vector is None
                or certificate.repair_map is None
                or not exact_equal(snapshot.cochain, certificate.defect_vector)
                or not exact_equal(snapshot.repair_map, certificate.repair_map)):
            return refuse("R_malformed_quotient")
        if snapshot.distance > 0:
            return refuse("R_obstruction", snapshot.distance)
    elif certificate.defect_vector is not None and any(v != 0 for v in certificate.defect_vector):
        return refuse("R_obstruction")

    target_terminal = target_regime.terminalize(transported_artifact)
    if target_terminal is not None and type(target_terminal) is not str:
        raise TypeError("target_regime.terminalize must return Optional[str]")
    if target_terminal is None:
        return refuse("R_noterminal", DIAGNOSTIC_NO_TERMINAL)
    auth_result = target_regime.is_auth(target_terminal)
    if type(auth_result) is not bool:
        raise TypeError("target_regime.is_auth must return strictly of type bool")
    if not auth_result:
        return refuse("R_target_unauth", DIAGNOSTIC_TARGET_UNAUTH, target_terminal)
    return TransportResult(True, target_terminal, None, DIAGNOSTIC_SUCCESS, certificate, snapshot)
