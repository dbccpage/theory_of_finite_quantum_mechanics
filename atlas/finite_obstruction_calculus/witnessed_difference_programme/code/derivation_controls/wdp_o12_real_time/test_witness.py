import importlib.util
from fractions import Fraction
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location("wdp_o12_real_time_witness", path)
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise RuntimeError("witness loader is missing")
    spec.loader.exec_module(module)
    return module


def _expected():
    mass = Fraction(1, 4)
    moment_1 = Fraction(0)
    moment_2 = Fraction(1, 2)
    return {
        "L": 4,
        "dimension": 16,
        "theta": 0,
        "trace_denominator": 64,
        "builders_agree": 1,
        "projector_identity": 1,
        "k_symmetric": 1,
        "commutator_is_edge_sum": 1,
        "four_point_identity": 1,
        "edge_count": 4,
        "edge_squared_trace": 8,
        "edge_squared_tau": Fraction(1, 2),
        "off_edge_pairs": 12,
        "off_edge_nonzero": 0,
        "tr_A2_sq": 64,
        "tr_A2_comm": 0,
        "tr_comm4_sq": 2048,
        "tr_A_sq": 16,
        "tr_A_comm": 0,
        "tr_comm_sq": 32,
        "mass": mass,
        "moment_1": moment_1,
        "moment_2": moment_2,
        "s0": mass,
        "s1": Fraction(0),
        "s2": Fraction(-1, 2),
        "euclidean_u0": mass,
        "euclidean_u_half": mass,
        "euclidean_u1": mass,
        "euclidean_circle_second": Fraction(0),
        "euclidean_displays_s2": 0,
        "L6": 6,
        "L6_dimension": 64,
        "L6_trace_denominator": 384,
        "L6_edge_squared_trace": 32,
        "L6_off_edge_pairs": 30,
        "L6_off_edge_nonzero": 0,
        "L6_tr_A2_sq": 384,
        "L6_tr_A2_comm": 0,
        "L6_tr_comm4_sq": 12288,
        "L6_tr_A_sq": 96,
        "L6_tr_A_comm": 0,
        "L6_tr_comm_sq": 192,
        "L6_mass": mass,
        "L6_moment_1": moment_1,
        "L6_moment_2": moment_2,
        "L6_copies_unscaled": 0,
        "L6_copies_scaled": 0,
        "L2_same_two_sites": 1,
        "L2_off_edge_trace": -2,
        "L2_diagonal_sum": 4,
        "L2_signed_sum": 8,
        "L2_orthogonality": 0,
        "real_time_density_supplied": 0,
        "spectral_density_supplied": 0,
        "lebesgue_density": 0,
        "theta_positive": 0,
        "volume_limit": 0,
        "trotter_20_12": 0,
        "continuum_limit": 0,
        "gibbs_moments_supplied": 0,
        "closed_real_time_law": 0,
        "higher_dimensional_sum": 0,
        "second_time_index": 0,
    }


def test_atomic_moments_are_exact() -> None:
    result = _load().witness()
    expected = _expected()
    assert result == expected
    for key in (
        "mass",
        "moment_1",
        "moment_2",
        "s0",
        "s1",
        "s2",
        "edge_squared_tau",
        "euclidean_u0",
        "euclidean_u_half",
        "euclidean_u1",
        "euclidean_circle_second",
        "L6_mass",
        "L6_moment_1",
        "L6_moment_2",
    ):
        assert type(result[key]) is Fraction
    for value in result.values():
        assert type(value) is int or type(value) is Fraction
        assert type(value) is not float
    assert result["tr_A2_sq"] == 4 * result["tr_A_sq"] == 64
    assert result["tr_comm4_sq"] == 64 * result["tr_comm_sq"] == 2048
    assert result["tr_A2_comm"] == 16 * result["tr_A_comm"] == 0
    assert Fraction(result["tr_A_sq"], result["trace_denominator"]) == Fraction(1, 4)
    assert Fraction(result["tr_A_comm"], result["trace_denominator"]) == 0
    assert Fraction(result["tr_comm_sq"], result["trace_denominator"]) == Fraction(1, 2)
    assert result["s0"] == result["mass"] == Fraction(1, 4)
    assert result["s1"] == result["moment_1"] == 0
    assert result["s2"] == -result["moment_2"] == Fraction(-1, 2)
    assert result["edge_squared_tau"] == Fraction(result["edge_squared_trace"], result["dimension"])
    assert result["euclidean_circle_second"] == 0
    assert result["euclidean_circle_second"] != result["s2"]
    assert result["euclidean_displays_s2"] == 0
    assert result["L6_tr_A_sq"] == 6 * (1 << 4)
    assert result["L6_tr_comm_sq"] == 6 * (1 << 5)
    assert Fraction(result["L6_tr_A_sq"], result["L6_trace_denominator"]) == Fraction(1, 4)
    assert Fraction(result["L6_tr_comm_sq"], result["L6_trace_denominator"]) == Fraction(1, 2)
    assert (result["L6_tr_A_sq"], result["L6_tr_A_comm"], result["L6_tr_comm_sq"]) != (
        result["tr_A_sq"],
        result["tr_A_comm"],
        result["tr_comm_sq"],
    )
    assert (result["L6_tr_A2_sq"], result["L6_tr_A2_comm"], result["L6_tr_comm4_sq"]) != (
        64,
        0,
        2048,
    )
    assert result["L6_copies_unscaled"] == 0
    assert result["L6_copies_scaled"] == 0
    assert result["L2_off_edge_trace"] != 0
    assert result["L2_diagonal_sum"] != result["L2_signed_sum"]
    assert result["L2_orthogonality"] == 0
    assert result["off_edge_nonzero"] == 0
    assert result["L6_off_edge_nonzero"] == 0
    assert result["continuum_limit"] == 0
    assert result["lebesgue_density"] == 0
    assert result["spectral_density_supplied"] == 0
    assert result["real_time_density_supplied"] == 0
    assert result["theta_positive"] == 0
    assert result["volume_limit"] == 0
    assert result["trotter_20_12"] == 0
    assert result["higher_dimensional_sum"] == 0
    assert result["second_time_index"] == 0
    assert result["closed_real_time_law"] == 0
    assert result["gibbs_moments_supplied"] == 0


def test_trace_helpers_match_the_witness() -> None:
    module = _load()
    result = module.witness()
    assert module.carrier_traces(4) == (16, 0, 32)
    assert module.scaled_traces(4) == (64, 0, 2048)
    assert module.carrier_traces(6) == (96, 0, 192)
    assert module.scaled_traces(6) == (384, 0, 12288)
    assert module.carrier_traces(4) == (
        result["tr_A_sq"],
        result["tr_A_comm"],
        result["tr_comm_sq"],
    )
    assert module.carrier_traces(6) != module.carrier_traces(4)
    assert module.scaled_traces(6) != module.scaled_traces(4)


def test_excluded_claims_are_refused() -> None:
    module = _load()
    with pytest.raises(ValueError, match="L=2") as caught:
        module.carrier_traces(2)
    assert "-2" in str(caught.value)
    with pytest.raises(ValueError, match="Lebesgue"):
        module.refuse_spectral_density()
    with pytest.raises(ValueError, match="continuum"):
        module.refuse_continuum()
    with pytest.raises(ValueError, match="infinity"):
        module.refuse_volume_limit()
    with pytest.raises(ValueError, match="20.12"):
        module.refuse_trotter_covariance()
    with pytest.raises(ValueError, match="theta>0"):
        module.refuse_positive_theta(Fraction(1, 192))
    with pytest.raises(ValueError, match="exact rational"):
        module.refuse_positive_theta(1 / 192)
    module.refuse_positive_theta(0)
    module.refuse_positive_theta(Fraction(0))
    with pytest.raises(ValueError, match="stay on L=4"):
        module.refuse_copied_labelled_integers(6)
    module.refuse_copied_labelled_integers(4)
    with pytest.raises(ValueError, match="higher-dimensional"):
        module.refuse_higher_dimensional_sum(2, Fraction(1, 4))
    with pytest.raises(ValueError, match="exact rational"):
        module.refuse_higher_dimensional_sum(1, 1 / 4)
    module.refuse_higher_dimensional_sum(1, Fraction(1, 4))
    with pytest.raises(ValueError, match="not a spectral density"):
        module.refuse_closed_real_time()
    with pytest.raises(ValueError, match="even and at least 4"):
        module.carrier_traces(5)
    with pytest.raises(ValueError, match="even and at least 4"):
        module.scaled_traces(2)

