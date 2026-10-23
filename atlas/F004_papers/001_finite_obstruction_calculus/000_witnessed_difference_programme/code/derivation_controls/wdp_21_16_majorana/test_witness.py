import importlib.util
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("wdp_21_16_majorana_witness", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_witness_packets_are_exact() -> None:
    result = _load().witness()
    assert all(type(value) is int for value in result.values())
    assert result == {
        "a_admitted": 8,
        "a_kernel": 4,
        "a_outside_b": 2,
        "a_classes": 2,
        "a_b_in_kernel": 1,
        "a_distinguishes": 0,
        "a_bperp": 4,
        "a_singleton_separators": 2,
        "a_separators_keeping_classes": 0,
        "a_minimum_extra_rows": 1,
        "a_named_kernel": 2,
        "a_named_classes": 1,
        "a_named_equals_b": 1,
        "a_named_repairs": 8,
        "b_edges": 18,
        "b_pauli_bits": 36,
        "b_e1": 37,
        "b_e2": 667,
        "b_duplicate_face_pairs": 0,
        "b_duplicate_star_pairs": 0,
        "b_ball2_kernel": 1,
        "b_e1_distinguishes": 1,
        "b_y_weight": 2,
        "b_y_in_kernel": 0,
        "b_lx_weight": 3,
        "b_lx_index_sum": 18,
        "b_lx_face_support": 0,
        "b_lx_in_kernel": 1,
        "b_lx_flux": 3,
        "b_lx_in_s": 0,
        "b_e2_weight_one": 1,
        "b_e2_weight_two": 2,
        "b_e2_syndromes_equal": 1,
        "b_e2_diff_is_lx": 1,
        "b_e2_diff_in_s": 0,
        "b_e2_distinguishes": 0,
        "b_partial_bits": 7,
        "b_partial_edge_sum": 1,
        "b_partial_equal": 1,
        "b_partial_common_face": 0,
        "b_partial_retained_weight": 1,
        "b_partial_omitted_support": 2,
        "b_partial_support_is_omitted": 1,
        "b_partial_diff_in_kernel": 0,
        "b_partial_diff_in_s": 0,
        "b_partial_distinguishes": 0,
        "b_star_flux_failures": 0,
        "b_commutation_odd": 0,
        "packet_answers_agree": 0,
        "bullet_closed": 0,
        "refused_names": 10,
    }


def test_unbound_bullet_and_float_are_refused() -> None:
    module = _load()
    with pytest.raises(ValueError, match="section_21_16_yes_no"):
        module.refuse("section_21_16_yes_no")
    with pytest.raises(ValueError, match="quotient_count_4"):
        module.refuse("quotient_count_4")
    with pytest.raises(TypeError, match="float tolerance"):
        module.refuse(0.0)
    assert module.refuse("bullet_closed") == 0
    assert module.refuse("a_distinguishes") == 0
    assert module.refuse("b_e1_distinguishes") == 1
