"""
Pytest integration test suite for Route C: The Fourier Landing Bypass.

Validates:
1. Complete graph transition count: binom(7, 2) = 21 pairwise transitions in MUB(6).
2. Discrete pigeonhole arithmetic on the Route C premises:
   - Non-identity bases: 6 = n_dita + n_tao + n_szollosi + n_haagerup
   - Cross-orbit restriction: n_tao + n_szollosi <= 1
   - Defect-0 isolation: n_haagerup <= 0
   - Forced Fourier count: n_dita >= 5
   - Forced Fourier pairs: binom(n_dita, 2) >= 10
   - Total forced Fourier edges: >= 15 out of 21 edges
3. Tensor-product lower bound for d = 2 * 3: min(2+1, 3+1) = 3 MUBs exist.
   The upper bound is d + 1 = 7; the maximum for d = 6 is open.
4. Lean 4 source check: RouteCFourierLandingBypass.lean contains no active
   `sorry` or `admit` token.

Scope: items 1-3 restate premise arithmetic. They are not evidence for the
conditional Lean theorem `no_complete_mub6_via_route_c`, whose landing
hypothesis remains a premise.

AuthorityEffect: None.
"""

from math import comb
from pathlib import Path


def test_transition_graph_combinatorics_21_edges():
    total_bases = 7
    total_pairs = comb(total_bases, 2)
    assert total_pairs == 21, f"Expected 21 pairwise transitions, got {total_pairs}"


def test_discrete_pigeonhole_fourier_lower_bounds():
    total_non_identity = 6
    for n_tao in [0, 1]:
        for n_szollosi in [0, 1]:
            if n_tao + n_szollosi > 1:
                continue
            n_haagerup = 0
            n_dita = total_non_identity - (n_tao + n_szollosi + n_haagerup)
            assert n_dita >= 5, f"Expected n_dita >= 5, got {n_dita}"

            fourier_pairs = comb(n_dita, 2)
            assert fourier_pairs >= 10, f"Expected fourier_pairs >= 10, got {fourier_pairs}"

            total_fourier_edges = n_dita + fourier_pairs
            assert total_fourier_edges >= 15, f"Expected >= 15 Fourier edges, got {total_fourier_edges}"
            assert total_fourier_edges > 0, "Fourier avoidance was unexpectedly possible"


def test_tensor_product_mub_lower_bound():
    p1 = 2
    p2 = 3
    dim = p1 * p2
    assert dim == 6
    lower_bound = min(p1 + 1, p2 + 1)
    upper_bound = dim + 1
    assert lower_bound == 3, f"Expected tensor-product lower bound 3, got {lower_bound}"
    assert upper_bound == 7
    assert lower_bound < upper_bound


def test_lean4_route_c_formalization_integrity():
    repo_root = next((p for p in Path(__file__).resolve().parents if (p / "pyproject.toml").is_file()), Path(__file__).resolve().parents[3])
    lean_file = repo_root / "lean4" / "RouteCFourierLandingBypass.lean"
    if not lean_file.exists():
        if (repo_root / "lean4" / "research_programs" / "mub6" / "RouteCFourierLandingBypass.lean").exists():
            lean_file = repo_root / "lean4" / "research_programs" / "mub6" / "RouteCFourierLandingBypass.lean"
        else:
            lean_file = Path(r"C:\Users\a343o\source\repos\the_symbol_game\lean4\research_programs\mub6\RouteCFourierLandingBypass.lean")
    assert lean_file.exists(), f"Lean file not found at {lean_file}"

    content = lean_file.read_text(encoding="utf-8")
    import re
    stripped = re.sub(r"/-\!?(.*?)-/", "", content, flags=re.DOTALL)
    stripped = re.sub(r"--.*", "", stripped)
    tokens = stripped.split()
    assert "sorry" not in tokens, "Found active 'sorry' keyword in RouteCFourierLandingBypass.lean"
    assert "admit" not in tokens, "Found active 'admit' keyword in RouteCFourierLandingBypass.lean"
    assert "no_complete_mub6_via_route_c" in content
    assert "route_c_grand_synthesis" in content
    assert "AllTransitionsAvoidFourier" in content
