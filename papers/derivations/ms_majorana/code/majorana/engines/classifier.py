from __future__ import annotations

"""End-to-end residual classifier: residual -> terminal + certificate.

The schedule class, ``dim_h1``, class coordinates, and ``Phi_1`` are the native
``majorana_gf2_diagnostic`` operation ``classify``. This module formats that
receipt; it does not recompute the terminal::

    d1 . d0 != 0, or bad shape          -> RepresentationInvalid
    r in im d0                          -> Exact
    d1 r != 0                           -> OpenObstruction
    closed, non-exact, Phi_1 capped     -> ClosedResidual   (honest fallback)
    closed, non-exact, Phi_1 certified  -> TypedHarmonic    (class + witness)

`TypedHarmonic` strictly dominates `ClosedResidual`; it is not a rename. When
the l1 search hits its budget the terminal degrades, so the pipeline never
asserts a minimum it did not compute.

Every certificate carries ``AuthorityEffect: None``.
"""


from typing import Any, Mapping

from omega_engine.crates.majorana.carriers.parity_carrier import MajoranaParityCarrier
from omega_engine.crates.majorana.core.gf2_diagnostic import classify_native
from omega_engine.crates.majorana.engines.harmonic import DEFAULT_BUDGET
from omega_engine.crates.majorana.engines.terminalizer import (
    hamming_weight,
    normal_form_mod_image,
)

TERMINALS: tuple[str, ...] = (
    "Exact",
    "ClosedResidual",
    "OpenObstruction",
    "TypedHarmonic",
    "RepresentationInvalid",
)

TERMINAL_READINGS: dict[str, str] = {
    "Exact": "pure gauge: an MZM reference-frame relabelling; no defect",
    "OpenObstruction": (
        "an island parity constraint is violated; a localized "
        "violated declared island parity relation, named by the coherence witness; "
        "physical cause UNDETERMINED"
    ),
    "ClosedResidual": (
        "consistent with every island constraint but not gauge: a logical "
        "parity error whose minimum weight was not certified"
    ),
    "TypedHarmonic": (
        "a logical parity error, identified in the H^1 basis, with a "
        "certified minimum-weight witness"
    ),
    "RepresentationInvalid": "the declared carrier is not a cochain complex",
}


def _empty_cohomology_fields() -> dict[str, Any]:
    return {
        "class_coordinates": None,
        "class_id": None,
        "phi1_weight": None,
        "phi1_exact": None,
        "phi1_representative": None,
        "phi1_alpha": None,
        "phi1_searched": None,
        "phi1_coset_size": None,
        "phi1_verified": None,
    }


def _algebraic_class_id(
    status: str,
    native: Mapping[str, Any],
    normal_form: list[int] | None,
) -> str:
    if status == "Exact":
        return "exact"
    if status == "RepresentationInvalid":
        return "representation-invalid:complex_relation_violation"
    if status == "OpenObstruction":
        witness = native["coherence_witness"] or []
        return "open-obstruction:" + "".join(str(int(bit) & 1) for bit in witness)
    if status == "TypedHarmonic":
        return f"typed-harmonic:{native['class_id']}:w{native['phi1_weight']}"
    return "closed-residual:" + "".join(str(int(bit) & 1) for bit in (normal_form or []))


def classify(
    d0: list[list[int]],
    d1: list[list[int]],
    residual: list[int],
    budget: int = DEFAULT_BUDGET,
) -> dict[str, Any]:
    """Classify ``residual`` against the complex ``d0, d1``.

    The terminal, ``dim_h1``, and ``Phi_1`` fields are copied from native
    operation ``classify``. ``budget`` is forwarded; exceeding it is the
    native degradation of `TypedHarmonic` to `ClosedResidual`.
    """
    native = classify_native(d0, d1, residual, budget=budget)
    status = native["terminal"]
    if status == "RepresentationInvalid":
        certificate = {
            "terminal_status": status,
            "reason": "D1*D0 != 0",
            "certificate_alpha": None,
            "normal_form": None,
            "coherence_witness": None,
            "q1_norm": None,
            "algebraic_class_id": "representation-invalid:complex_relation_violation",
            **_empty_cohomology_fields(),
            "dim_h1": None,
            "authority_effect": "None",
            "terminal_reading": TERMINAL_READINGS[status],
        }
        return certificate

    normal_form = (
        None
        if status == "Exact"
        else normal_form_mod_image(d0, d1, [int(bit) & 1 for bit in residual])
    )
    q1_norm = 0 if status == "Exact" else hamming_weight(normal_form or [])
    certificate = {
        "terminal_status": status,
        "reason": native["reason"],
        "certificate_alpha": native["certificate_alpha"],
        "normal_form": normal_form,
        "coherence_witness": native["coherence_witness"],
        "q1_norm": q1_norm,
        "algebraic_class_id": _algebraic_class_id(status, native, normal_form),
        "class_coordinates": native["class_coordinates"],
        "class_id": native["class_id"],
        "phi1_weight": native["phi1_weight"],
        "phi1_exact": native["phi1_exact"],
        "phi1_representative": native["phi1_representative"],
        "phi1_alpha": native["phi1_alpha"],
        "phi1_searched": native["phi1_searched"],
        "phi1_coset_size": native["phi1_coset_size"],
        "phi1_verified": native["phi1_verified"],
        "dim_h1": native["dim_h1"],
        "authority_effect": "None",
        "terminal_reading": TERMINAL_READINGS[status],
    }
    return certificate


def classify_carrier(
    carrier: MajoranaParityCarrier,
    budget: int = DEFAULT_BUDGET,
) -> dict[str, Any]:
    """Classify a carrier's own declared residual."""
    return classify(carrier.D0, carrier.D1, carrier.residual, budget=budget)




