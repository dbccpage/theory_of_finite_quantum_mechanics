from __future__ import annotations

from dataclasses import replace

import pytest

from omega_engine.kernel.cochain_realization import (
    ClosureStatus,
    CochainRealizationV1,
    CochainWindowV1,
    realize_active_demands,
)
from omega_engine.kernel.higher_operad import Err, Ok
from omega_engine.kernel.presentation_difference import (
    ActiveObstructionV1,
    DemandV1,
    PresentationV1,
    QuestionV1,
    active_obstruction,
)


def _presentation() -> PresentationV1:
    return PresentationV1(
        points=("a", "b", "c"),
        questions=(QuestionV1("q.constant", ("0", "0", "0")),),
    )


def _demands() -> tuple[DemandV1, ...]:
    return (
        DemandV1("a", "b", True, True),
        DemandV1("b", "c", True, True),
    )


def _obstruction_ids() -> tuple[str, ...]:
    presentation = _presentation()
    values = tuple(active_obstruction(presentation, demand) for demand in _demands())
    assert all(value is not None for value in values)
    return tuple(value.obstruction_id for value in values if value is not None)


def _window() -> CochainWindowV1:
    return CochainWindowV1(
        repair_parameter_ids=("repair.alpha",),
        demand_coordinate_ids=_obstruction_ids(),
        face_ids=("face.triangle",),
        d0=((1,), (-1,)),
        d1=((1, 1),),
    )


def test_active_obstruction_has_a_content_identity() -> None:
    obstruction = active_obstruction(_presentation(), _demands()[0])
    assert obstruction is not None
    assert obstruction.obstruction_id.startswith("sha256:")
    assert obstruction.obstruction_id == active_obstruction(
        _presentation(), _demands()[0]
    ).obstruction_id


def test_active_obstruction_rejects_forged_authority() -> None:
    obstruction = active_obstruction(_presentation(), _demands()[0])
    assert obstruction is not None
    with pytest.raises(ValueError):
        replace(obstruction, authority_effect="Minted")


def test_window_checks_chain_law_exactly() -> None:
    with pytest.raises(ValueError, match=r"d1 \* d0"):
        CochainWindowV1(
            repair_parameter_ids=("repair.alpha",),
            demand_coordinate_ids=_obstruction_ids(),
            face_ids=("face.triangle",),
            d0=((1,), (1,)),
            d1=((1, 1),),
        )


def test_window_rejects_float_coefficients() -> None:
    with pytest.raises(TypeError):
        CochainWindowV1(
            repair_parameter_ids=("repair.alpha",),
            demand_coordinate_ids=_obstruction_ids(),
            face_ids=("face.triangle",),
            d0=((1.0,), (-1.0,)),
            d1=((1, 1),),
        )


def test_active_demands_require_an_explicit_window() -> None:
    result = realize_active_demands(_presentation(), _demands(), (1, -1), None)
    assert isinstance(result, Err)
    assert result.error.code == "MISSING_COCHAIN_WINDOW"


def test_unprotected_difference_is_not_a_cochain_coordinate() -> None:
    demands = (
        DemandV1("a", "b", True, False),
        _demands()[1],
    )
    result = realize_active_demands(_presentation(), demands, (1, -1), _window())
    assert isinstance(result, Err)
    assert result.error.code == "DEMAND_NOT_ACTIVE"


def test_coordinate_order_is_bound_to_obstruction_order() -> None:
    window = _window()
    reversed_window = CochainWindowV1(
        repair_parameter_ids=window.repair_parameter_ids,
        demand_coordinate_ids=tuple(reversed(window.demand_coordinate_ids)),
        face_ids=window.face_ids,
        d0=window.d0,
        d1=window.d1,
    )
    result = realize_active_demands(
        _presentation(),
        _demands(),
        (1, -1),
        reversed_window,
    )
    assert isinstance(result, Err)
    assert result.error.code == "COORDINATE_BINDING_MISMATCH"


def test_declared_integer_realization_is_admitted() -> None:
    result = realize_active_demands(_presentation(), _demands(), (1, -1), _window())
    assert isinstance(result, Ok)
    assert result.value.omega == (1, -1)
    assert result.value.window.canonical_id.startswith("sha256:")
    assert result.value.authority_effect.value == "None"


def test_exact_repair_witness_is_checked_not_asserted() -> None:
    result = realize_active_demands(_presentation(), _demands(), (1, -1), _window())
    assert isinstance(result, Ok)
    assert result.value.exact_repair_witness((-1,))
    assert not result.value.exact_repair_witness((1,))


def test_chain_law_makes_closure_invariant_under_declared_repair() -> None:
    result = realize_active_demands(_presentation(), _demands(), (2, 3), _window())
    assert isinstance(result, Ok)
    assert result.value.closure_of(result.value.repaired((7,))) == result.value.closure


def test_nonzero_d1_omega_is_only_an_active_closure_failure() -> None:
    result = realize_active_demands(_presentation(), _demands(), (1, 1), _window())
    assert isinstance(result, Ok)
    assert result.value.closure == (2,)
    assert result.value.closure_status is ClosureStatus.ACTIVE_CLOSURE_FAILURE


def test_zero_closure_does_not_claim_exactness_without_a_witness() -> None:
    result = realize_active_demands(_presentation(), _demands(), (1, -1), _window())
    assert isinstance(result, Ok)
    assert result.value.closure_status is ClosureStatus.CLOSED
    assert not result.value.exact_repair_witness((0,))
    assert result.value.exact_repair_witness((-1,))


def test_nested_matrix_mutation_is_rejected_on_reconstruction() -> None:
    window = _window()
    object.__setattr__(window, "d0", ([1], [-1]))
    with pytest.raises(TypeError):
        CochainWindowV1(
            window.repair_parameter_ids,
            window.demand_coordinate_ids,
            window.face_ids,
            window.d0,
            window.d1,
        )


def test_direct_obstruction_constructor_rejects_non_digest_bindings() -> None:
    with pytest.raises(ValueError):
        ActiveObstructionV1(
            presentation_id="presentation",
            demand_id="demand",
            pair=("a", "b"),
            shared_profile=("0",),
        )


def test_direct_active_obstruction_construction_is_sealed() -> None:
    obstruction = active_obstruction(_presentation(), _demands()[0])
    assert obstruction is not None
    with pytest.raises(ValueError, match="constructed only"):
        ActiveObstructionV1(
            presentation_id=obstruction.presentation_id,
            demand_id=obstruction.demand_id,
            pair=obstruction.pair,
            shared_profile=obstruction.shared_profile,
        )


def test_zero_coefficient_cannot_hide_an_active_obstruction() -> None:
    result = realize_active_demands(_presentation(), _demands(), (0, 1), _window())
    assert isinstance(result, Err)
    assert result.error.code == "REALIZATION_REFUSED"


def test_direct_cochain_realization_construction_is_sealed() -> None:
    admitted = realize_active_demands(
        _presentation(),
        _demands(),
        (1, -1),
        _window(),
    )
    assert isinstance(admitted, Ok)
    with pytest.raises(ValueError, match="constructed only"):
        CochainRealizationV1(
            presentation_id=admitted.value.presentation_id,
            obstruction_ids=admitted.value.obstruction_ids,
            omega=admitted.value.omega,
            window=admitted.value.window,
        )
