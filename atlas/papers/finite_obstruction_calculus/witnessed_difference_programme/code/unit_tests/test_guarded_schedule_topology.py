"""Exact census, independent orientation, and hostile certificate controls."""

import sys
from copy import deepcopy
from fractions import Fraction
from itertools import combinations
from pathlib import Path

CODE = Path(__file__).resolve().parents[1]
PACKAGE = CODE.parent
sys.path.insert(0, str(PACKAGE))
sys.path.insert(0, str(CODE))

import pytest  # noqa: E402
from guarded_schedule_topology import algebra, experiment  # noqa: E402
from guarded_schedule_topology.algebra import (  # noqa: E402
    Matrix,
    certify_homology,
    check_homology,
    check_top_cycle_pairing,
    matrices,
    reduce_integer_boundary,
    replay_reduction,
    verify_chain,
)
from guarded_schedule_topology.model import (  # noqa: E402
    TopologyRefusal,
    block_legal,
    boundary,
    direct_cell_baseline,
    direct_word_legal,
    enumerate_cells,
    task_cells,
    vertex_refinements,
)
from scripts import verify_guarded_schedule_topology as cli  # noqa: E402


@pytest.mark.parametrize("n,c", [(n, c) for n in range(1, 4) for c in range(n + 1)])
def test_block_recursion_equals_all_refining_native_count_words(n, c):
    cells = enumerate_cells(n, c)
    assert cells == direct_cell_baseline(n, c)
    assert all(block_legal(cell, n, c) for level in cells for cell in level)
    verify_chain(matrices(cells))


def test_one_legal_vertex_does_not_admit_an_unsafe_whole_face():
    # At count one, finishing the first pair before starting the second is
    # legal. The opposite ordering of the middle block is refused.
    cell = ((0,), (1, 2), (3,))
    assert direct_word_legal((0, 1, 2, 3), 2, 1)
    assert not direct_word_legal((0, 2, 1, 3), 2, 1)
    assert not block_legal(cell, 2, 1)
    assert cell not in {face for level in enumerate_cells(2, 1) for face in level}
    assert {direct_word_legal(word, 2, 1) for word in vertex_refinements(cell)} == {True, False}


def test_precedence_is_distinct_from_numeric_count_guard():
    assert not direct_word_legal((1, 0), 1, 1)
    assert not block_legal(((0, 1),), 1, 1)


def determinant_sign(columns):
    """Independent geometric incidence oracle, using exact rational elimination."""
    matrix = [[Fraction(value) for value in row] for row in zip(*columns)]
    sign = 1
    for i in range(len(matrix)):
        pivot = next(j for j in range(i, len(matrix)) if matrix[j][i])
        if pivot != i:
            matrix[i], matrix[pivot] = matrix[pivot], matrix[i]
            sign *= -1
        value = matrix[i][i]
        sign *= 1 if value > 0 else -1
        for j in range(i + 1, len(matrix)):
            factor = matrix[j][i] / value
            for k in range(i, len(matrix)):
                matrix[j][k] -= factor * matrix[i][k]
    return sign


def geometric_incidence(block, left, right):
    # In the parent e_b-e_last basis a zero-sum vector has coordinates given
    # by all but its final ambient coordinate. This oracle never counts
    # shuffle inversions or calls the implementation's sign rule.
    normal = tuple(-len(right) if b in left else len(left) for b in block[:-1])
    tangents = [tuple(int(b == x) - int(b == part[-1]) for b in block[:-1])
                for part in (left, right) for x in part[:-1]]
    return determinant_sign([normal, *tangents])


@pytest.mark.parametrize("size", range(2, 9))
def test_boundary_sign_agrees_with_outward_normal_orientation(size):
    block = tuple(range(size))
    actual = boundary((block,))
    for k in range(1, size):
        for left in combinations(block, k):
            right = tuple(x for x in block if x not in left)
            assert actual[(left, right)] == geometric_incidence(block, left, right)
    # A preceding 1-dimensional block reverses the product-boundary sign.
    shifted = tuple(x + 2 for x in block)
    for face, sign in boundary(((0, 1), shifted)).items():
        if face[0] == (0, 1):
            assert sign == -geometric_incidence(shifted, face[1], face[2])


@pytest.fixture(scope="module")
def four_pair_sphere():
    cells = enumerate_cells(4, 3)
    chain = matrices(cells)
    proof, result = certify_homology(chain)
    return cells, chain, proof, result


def test_full_four_pair_integral_homology(four_pair_sphere):
    _, _, _, result = four_pair_sphere
    assert result["f_vector"] == [1944, 5400, 5340, 2184, 302]
    assert result["boundary_ranks"] == [0, 1943, 3457, 1882, 302]
    assert result["integral_betti"] == [1, 0, 1, 0, 0]
    assert result["torsion_free"] is True


def test_intermediate_capacity_has_seven_independent_one_cycles():
    _, actual = certify_homology(matrices(enumerate_cells(4, 2)))
    assert actual["f_vector"] == [648, 1368, 876, 168, 6]
    assert actual["integral_betti"] == [1, 7, 0, 0, 0]
    _, smaller = certify_homology(matrices(task_cells(4, 2)))
    assert smaller["f_vector"] == [24, 36, 6]
    assert smaller["integral_betti"] == [1, 7, 0]


def test_task_complex_sphere_reduction_has_fourteen_faces():
    _, result = certify_homology(matrices(task_cells(4, 3)))
    assert result["f_vector"] == [24, 36, 14]
    assert result["integral_betti"] == [1, 0, 1]


@pytest.mark.parametrize("n", [3, 4])
def test_explicit_nonexact_top_cochain_pairs_with_a_closed_cycle(n):
    cells = task_cells(n, n - 1)
    facets = boundary((tuple(range(n)),))
    proof = {"degree": n - 2,
             "cycle": [[i, facets[cell]] for i, cell in enumerate(cells[-1])],
             "cochain": [[0, 1]], "pairing": facets[cells[-1][0]]}
    checked = check_top_cycle_pairing(matrices(cells), proof)
    assert checked["cochain_not_exact"] and checked["cycle_not_boundary"]
    assert abs(checked["pairing"]) == 1
    proof["cycle"][0][1] *= -1
    with pytest.raises(TopologyRefusal, match="nonzero boundary"):
        check_top_cycle_pairing(matrices(cells), proof)


def test_two_skeleton_alone_has_spurious_second_homology(four_pair_sphere):
    _, chain, _, _ = four_pair_sphere
    _, truncated = certify_homology(chain[:3])
    assert truncated["integral_betti"] == [1, 0, 1883]


def test_missing_boundary_cell_is_refused():
    levels = enumerate_cells(2, 2)
    with pytest.raises(TopologyRefusal, match="closed under"):
        matrices((levels[0][1:], *levels[1:]))


def test_one_incidence_sign_change_breaks_boundary_squared_zero():
    chain = list(matrices(enumerate_cells(2, 2)))
    columns = list(chain[2].columns)
    incidences = list(columns[0])
    row, sign = incidences[0]
    incidences[0] = row, -sign
    columns[0] = tuple(incidences)
    chain[2] = Matrix(chain[2].rows, tuple(columns))
    with pytest.raises(TopologyRefusal, match="squared"):
        verify_chain(tuple(chain))


def test_consistent_cell_orientation_reversal_preserves_homology(four_pair_sphere):
    _, chain, _, expected = four_pair_sphere
    moved = list(chain)
    columns = list(moved[2].columns)
    columns[0] = tuple((row, -value) for row, value in columns[0])
    moved[2] = Matrix(moved[2].rows, tuple(columns))
    moved[3] = Matrix(moved[3].rows, tuple(
        tuple((row, -value if row == 0 else value) for row, value in column)
        for column in moved[3].columns))
    _, actual = certify_homology(tuple(moved))
    assert actual["integral_betti"] == expected["integral_betti"]


@pytest.mark.parametrize("matrix", [
    Matrix(1, (((0, 2),),)),
    Matrix(2, (((0, 1), (1, 1)), ((0, 1), (1, -1)))),
    Matrix(1, (((0, 2),), ((0, 3),))),
])
def test_nonunit_residual_means_unclassified_not_a_torsion_claim(matrix):
    proof = reduce_integer_boundary(matrix)
    replayed = replay_reduction(matrix, proof)
    assert not replayed["residual_zero"]
    assert replayed["smith_invariants"] == "unclassified"
    chain = (Matrix(0, tuple(() for _ in range(matrix.rows))), matrix)
    result = check_homology(chain, {"reductions": [
        reduce_integer_boundary(chain[0]), proof]})
    assert result["status"] == "UNCLASSIFIED_NONUNIT_RESIDUAL"
    assert result["torsion_free"] is None
    assert result["integral_betti"] is None


def test_checker_does_not_call_pivot_search(monkeypatch):
    chain = matrices(enumerate_cells(3, 2))
    proof, expected = certify_homology(chain)
    def forbidden(*_):
        raise AssertionError("rank proposer was called by checker")
    monkeypatch.setattr(algebra, "reduce_integer_boundary", forbidden)
    assert check_homology(chain, proof) == expected


@pytest.mark.parametrize("mutation", ["sign", "boolean", "omit", "repeat", "residual"])
def test_forged_pivot_certificate_is_refused(mutation):
    matrix = matrices(enumerate_cells(2, 2))[1]
    proof = deepcopy(reduce_integer_boundary(matrix))
    if mutation == "sign":
        proof["pivots"][0][2] *= -1
    elif mutation == "boolean":
        proof["pivots"][0][0] = True
    elif mutation == "omit":
        proof["pivots"].pop()
    elif mutation == "repeat":
        proof["pivots"][1] = proof["pivots"][0]
    else:
        proof["residual"] = [[0, [[0, 1]]]]
    with pytest.raises(TopologyRefusal):
        replay_reduction(matrix, proof)


@pytest.mark.parametrize("n,c", [(True, 1), (2, True), (0, 0), (5, 1), (2, -1), (2, 3)])
def test_invalid_bounded_parameters_are_refused(n, c):
    with pytest.raises(TopologyRefusal):
        enumerate_cells(n, c)


@pytest.mark.parametrize("cell", [((0, 0), (1, 2, 3)), ((True,), (0, 2, 3)),
                                  ((1, 0), (2, 3)), ((0,), (1,), ())])
def test_invalid_cell_inputs_are_refused(cell):
    with pytest.raises(TopologyRefusal):
        block_legal(cell, 2, 2)


@pytest.mark.parametrize("raw", ['{"x":1,"x":2}', '{"x":1.0}', '{"x":NaN}'])
def test_json_parser_refuses_ambiguous_numbers_and_duplicate_keys(tmp_path, raw):
    path = tmp_path / "certificate.json"
    path.write_text(raw)
    with pytest.raises(TopologyRefusal):
        experiment.read_certificate(path)


def test_cli_refuses_protected_source_output_before_any_computation():
    source = Path(cli.__file__)
    before = source.read_bytes()
    assert cli.main(["build", "--certificate", str(source)]) == 1
    assert source.read_bytes() == before


def test_cli_refuses_hardlinked_receipt_and_linked_output(tmp_path):
    certificate = tmp_path / "certificate.json"
    certificate.write_text("{}")
    receipt = tmp_path / "receipt.json"
    receipt.hardlink_to(certificate)
    with pytest.raises(TopologyRefusal, match="aliases"):
        cli.check_output(receipt, [certificate])
    linked = tmp_path / "linked.json"
    linked.symlink_to(certificate)
    with pytest.raises(TopologyRefusal, match="linked"):
        cli.check_output(linked, [])


def test_certificate_inventory_cannot_omit_cases_or_booleanize_indices(monkeypatch):
    monkeypatch.setattr(experiment, "MAX_PAIRS", 1)
    proof = experiment.build_certificate(PACKAGE)
    checked = experiment.check_certificate(PACKAGE, proof)
    assert len(checked["cases"]) == 2
    missing = deepcopy(proof)
    missing["cases"].pop()
    with pytest.raises(TopologyRefusal, match="every declared"):
        experiment.check_certificate(PACKAGE, missing)
    booleans = deepcopy(proof)
    booleans["cases"][0]["pairs"] = True
    with pytest.raises(TopologyRefusal, match="inventory"):
        experiment.check_certificate(PACKAGE, booleans)
