from __future__ import annotations

from dataclasses import replace

import pytest

from omega_engine.kernel.cell_grammar import (
    BoundaryUseV1,
    CellGrammarV1,
    OrientedEdgeV1,
    OrientedFaceV1,
    build_cochain_window_from_cells,
    cell_grammar_replays,
)
from omega_engine.kernel.cochain_realization import ClosureStatus, realize_active_demands
from omega_engine.kernel.higher_operad import Err, Ok
from omega_engine.kernel.presentation_difference import (
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
        DemandV1("a", "c", True, True),
        DemandV1("b", "c", True, True),
    )


def _obstruction_ids() -> tuple[str, ...]:
    values = tuple(active_obstruction(_presentation(), demand) for demand in _demands())
    assert all(value is not None for value in values)
    return tuple(value.obstruction_id for value in values if value is not None)


def _triangle() -> CellGrammarV1:
    ab, ac, bc = _obstruction_ids()
    return CellGrammarV1(
        vertex_ids=("a", "b", "c"),
        edges=(
            OrientedEdgeV1("e.ab", ab, "a", "b"),
            OrientedEdgeV1("e.ac", ac, "a", "c"),
            OrientedEdgeV1("e.bc", bc, "b", "c"),
        ),
        faces=(
            OrientedFaceV1(
                "f.abc",
                (
                    BoundaryUseV1("e.ab", 1),
                    BoundaryUseV1("e.bc", 1),
                    BoundaryUseV1("e.ac", -1),
                ),
            ),
        ),
    )


def test_triangle_constructs_incidence_coboundaries() -> None:
    result = build_cochain_window_from_cells(_triangle())
    assert isinstance(result, Ok)
    assert result.value.repair_parameter_ids == ("a", "b", "c")
    assert result.value.d0 == ((-1, 1, 0), (-1, 0, 1), (0, -1, 1))
    assert result.value.d1 == ((1, -1, 1),)


def test_constructed_window_integrates_with_active_obstructions() -> None:
    built = build_cochain_window_from_cells(_triangle())
    assert isinstance(built, Ok)
    realized = realize_active_demands(
        _presentation(),
        _demands(),
        (1, -1, 1),
        built.value,
    )
    assert isinstance(realized, Ok)
    assert realized.value.closure == (3,)
    assert realized.value.closure_status is ClosureStatus.ACTIVE_CLOSURE_FAILURE


def test_closed_triangle_cochain_window_satisfies_chain_law_by_construction() -> None:
    built = build_cochain_window_from_cells(_triangle())
    assert isinstance(built, Ok)
    for repair in ((1, 0, 0), (0, 2, -4), (7, 8, 9)):
        correction = tuple(
            sum(entry * value for entry, value in zip(row, repair))
            for row in built.value.d0
        )
        assert tuple(
            sum(entry * value for entry, value in zip(row, correction))
            for row in built.value.d1
        ) == (0,)


def test_open_face_boundary_is_refused() -> None:
    grammar = _triangle()
    broken = replace(
        grammar,
        faces=(
            OrientedFaceV1(
                "f.open",
                (BoundaryUseV1("e.ab", 1), BoundaryUseV1("e.bc", 1)),
            ),
        ),
    )
    result = build_cochain_window_from_cells(broken)
    assert isinstance(result, Err)
    assert result.error.code == "FACE_BOUNDARY_NOT_CLOSED"


def test_face_cannot_reference_an_undeclared_edge() -> None:
    with pytest.raises(ValueError, match="boundary edge"):
        replace(
            _triangle(),
            faces=(
                OrientedFaceV1("f.bad", (BoundaryUseV1("e.missing", 1),)),
            ),
        )


def test_normalized_face_rejects_duplicate_edge_uses() -> None:
    with pytest.raises(ValueError, match="at most once"):
        OrientedFaceV1(
            "f.duplicate",
            (BoundaryUseV1("e.ab", 1), BoundaryUseV1("e.ab", -1)),
        )


@pytest.mark.parametrize("coefficient", [0, 1.0, True])
def test_boundary_coefficients_are_nonzero_exact_integers(coefficient: object) -> None:
    with pytest.raises(ValueError):
        BoundaryUseV1("e.ab", coefficient)  # type: ignore[arg-type]


def test_edge_endpoints_must_be_declared() -> None:
    with pytest.raises(ValueError, match="endpoint"):
        CellGrammarV1(
            vertex_ids=("a", "b"),
            edges=(OrientedEdgeV1("e.ac", "d.ac", "a", "c"),),
            faces=(),
        )


def test_v1_demand_edge_cannot_be_a_loop() -> None:
    with pytest.raises(ValueError, match="distinct endpoints"):
        OrientedEdgeV1("e.aa", "d.aa", "a", "a")


def test_permutation_of_declarations_has_the_same_grammar_identity() -> None:
    grammar = _triangle()
    permuted = CellGrammarV1(
        vertex_ids=tuple(reversed(grammar.vertex_ids)),
        edges=tuple(reversed(grammar.edges)),
        faces=grammar.faces,
    )
    assert permuted == grammar
    assert permuted.canonical_id == grammar.canonical_id


def test_nested_tuple_mutation_fails_replay() -> None:
    grammar = _triangle()
    object.__setattr__(grammar, "edges", list(grammar.edges))
    assert not cell_grammar_replays(grammar)
    result = build_cochain_window_from_cells(grammar)
    assert isinstance(result, Err)
    assert result.error.code == "MALFORMED_CELL_GRAMMAR"


def test_nested_edge_mutation_fails_replay() -> None:
    grammar = _triangle()
    object.__setattr__(grammar.edges[0], "coordinate_id", ["forged"])
    assert not cell_grammar_replays(grammar)
    result = build_cochain_window_from_cells(grammar)
    assert isinstance(result, Err)
    assert result.error.code == "MALFORMED_CELL_GRAMMAR"


def test_nested_boundary_use_mutation_fails_reconstruction() -> None:
    grammar = _triangle()
    object.__setattr__(grammar.faces[0].boundary[0], "coefficient", 1.5)
    assert not cell_grammar_replays(grammar)


def test_authority_cannot_be_minted_by_a_cell() -> None:
    with pytest.raises(ValueError, match="AuthorityEffect None"):
        replace(_triangle().edges[0], authority_effect="Minted")


def test_graph_without_faces_constructs_a_degree_one_window_only() -> None:
    grammar = CellGrammarV1(
        vertex_ids=("a", "b"),
        edges=(OrientedEdgeV1("e.ab", "d.ab", "a", "b"),),
        faces=(),
    )
    result = build_cochain_window_from_cells(grammar)
    assert isinstance(result, Ok)
    assert result.value.d0 == ((-1, 1),)
    assert result.value.d1 == ()
    assert result.value.face_ids == ()
