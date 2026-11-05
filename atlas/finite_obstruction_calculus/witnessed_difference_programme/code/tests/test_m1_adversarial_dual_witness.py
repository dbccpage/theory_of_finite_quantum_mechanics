"""Adversarial stress-test suite for M1 Simplex Obstruction Solver & Dual Annihilating Witness.

AuthorityEffect: None.

Stress-tests:
1. Genuine removal of BFS spanning-tree heuristic (BFS is strictly suboptimal on cyclic topologies).
2. Cycle with chord (unit-weighted and heavily-weighted regimes).
3. Complete graph K4 (interlocking 3-cycles and frustrated circulations).
4. Mobius ladders M3 and M4 (non-planar cubic graphs with twisted rungs).
5. Exact 5-point algebraic validation of emitted dual witness y:
   - Kirchhoff divergence-free: d_0^T y = 0 at every vertex.
   - Dual capacity: |y_e| <= w_e for all edges.
   - Exact duality gap: <h, y> == Phi_1(h).
   - Primal feasibility: r_e = h_e - (phi_v - phi_u).
   - Complementary slackness: r_e != 0 => |y_e| == w_e.
6. Arbitrary-precision BigRational stress-testing (46-digit rational coefficients).
"""

from collections import deque
from fractions import Fraction
import random
import pytest

from witnessed_difference.cochains import FiniteComplex
from witnessed_difference.obstruction import exact_quotient_l1, verify_quotient_certificate
from witnessed_difference.outcomes import Accepted
from witnessed_difference.native_functionals import representative_mass
from native_wdp import solve_native_obstruction


def greedy_bfs_unwinding(
    vertices: tuple[str, ...],
    edges: tuple[tuple[str, str], ...],
    cochain: dict[tuple[str, str], Fraction],
    weights: dict[tuple[str, str], Fraction] | None = None,
) -> tuple[dict[str, Fraction], dict[tuple[str, str], Fraction], Fraction]:
    """Simulates the legacy ad-hoc BFS spanning-tree potential unwinder."""
    if weights is None:
        weights = {e: Fraction(1) for e in edges}
    potential: dict[str, Fraction] = {}
    visited: set[str] = set()
    queue: deque[str] = deque()

    for v_root in vertices:
        if v_root in visited:
            continue
        potential[v_root] = Fraction(0)
        visited.add(v_root)
        queue.append(v_root)
        while queue:
            curr = queue.popleft()
            curr_pot = potential[curr]
            for (u, v) in edges:
                val = cochain.get((u, v), Fraction(0))
                if u == curr and v not in visited:
                    potential[v] = curr_pot + val
                    visited.add(v)
                    queue.append(v)
                elif v == curr and u not in visited:
                    potential[u] = curr_pot - val
                    visited.add(u)
                    queue.append(u)

    residual: dict[tuple[str, str], Fraction] = {}
    for (u, v) in edges:
        val = cochain.get((u, v), Fraction(0))
        d_val = potential[v] - potential[u]
        r = val - d_val
        residual[(u, v)] = r
    total_l1 = representative_mass(tuple(residual[e] for e in edges), tuple(weights[e] for e in edges))

    return potential, residual, total_l1


def verify_dual_witness_5point(
    vertices: tuple[str, ...],
    edges: tuple[tuple[str, str], ...],
    cochain: dict[tuple[str, str], Fraction],
    solution,
    weights: dict[tuple[str, str], Fraction] | None = None,
):
    """Replay the complete primal-dual certificate in omega_functional."""
    from tests.functional_checks import verify_native
    verify_native(vertices, edges, cochain, solution, weights)


class TestAdversarialDualWitness:
    """Stress-test suite for simplex obstruction solver and dual witness."""

    def test_cycle_with_chord_suboptimality_of_bfs(self):
        """Cycle with chord: BFS gives suboptimal residual (6), Simplex finds global min (4)."""
        vertices = ("0", "1", "2", "3")
        edges = (("0", "1"), ("1", "2"), ("2", "3"), ("3", "0"), ("1", "3"))
        cochain = {
            ("0", "1"): Fraction(1),
            ("1", "2"): Fraction(1),
            ("2", "3"): Fraction(1),
            ("3", "0"): Fraction(1),
            ("1", "3"): Fraction(0),
        }

        _, _, bfs_cost = greedy_bfs_unwinding(vertices, edges, cochain)
        res = solve_native_obstruction(vertices, edges, cochain, require_native=True)
        assert res.is_ok, f"Native solver failed: {res}"
        sol = res.value

        # BFS gives 6, Simplex gives 4
        assert bfs_cost == Fraction(6)
        assert sol.phi1 == Fraction(4)
        assert bfs_cost > sol.phi1, "Greedy BFS was not suboptimal"

        verify_dual_witness_5point(vertices, edges, cochain, sol)

    def test_cycle_with_chord_weighted_adversarial(self):
        """In weighted cycle with chord, BFS is blind to weight and incurs massive penalty."""
        vertices = ("0", "1", "2", "3")
        edges = (("0", "1"), ("1", "2"), ("2", "3"), ("3", "0"), ("1", "3"))
        cochain = {
            ("0", "1"): Fraction(1),
            ("1", "2"): Fraction(1),
            ("2", "3"): Fraction(1),
            ("3", "0"): Fraction(1),
            ("1", "3"): Fraction(0),
        }
        # Heavy chord
        weights = {
            ("0", "1"): Fraction(1),
            ("1", "2"): Fraction(1),
            ("2", "3"): Fraction(1),
            ("3", "0"): Fraction(1),
            ("1", "3"): Fraction(100),
        }
        # BFS misses the heavy chord in tree exploration if edge order causes it to be a chord
        _, _, bfs_cost = greedy_bfs_unwinding(vertices, edges, cochain, weights=weights)
        # Note: In standard BFS order, chord (1, 3) is a non-tree edge with residual 2, cost 2 * 100 = 200
        assert bfs_cost >= Fraction(204)

        weighted = exact_quotient_l1(FiniteComplex(vertices, edges), cochain, weights)
        assert isinstance(weighted, Accepted)
        assert isinstance(verify_quotient_certificate(weighted.value), Accepted)
        assert weighted.value.value == 4 < bfs_cost
        assert weighted.value.weights == tuple(weights[e] for e in edges)

    def test_complete_graph_k4_frustrated_circulation(self):
        """Complete graph K4 with frustrated circulations: BFS gives 6, Simplex gives 3."""
        vertices = ("0", "1", "2", "3")
        edges = (("0", "1"), ("0", "2"), ("0", "3"), ("1", "2"), ("1", "3"), ("2", "3"))
        cochain = {
            ("0", "1"): Fraction(1),
            ("0", "2"): Fraction(-1),
            ("0", "3"): Fraction(1),
            ("1", "2"): Fraction(1),
            ("1", "3"): Fraction(0),
            ("2", "3"): Fraction(-1),
        }

        _, _, bfs_cost = greedy_bfs_unwinding(vertices, edges, cochain)
        res = solve_native_obstruction(vertices, edges, cochain, require_native=True)
        assert res.is_ok, f"Native solver failed: {res}"
        sol = res.value

        assert bfs_cost == Fraction(6)
        assert sol.phi1 == Fraction(3)
        assert bfs_cost > sol.phi1

        verify_dual_witness_5point(vertices, edges, cochain, sol)

    def test_complete_graph_k4_rational_circulation(self):
        """K4 with fractional rational cochains: exact dual gap zero."""
        vertices = ("0", "1", "2", "3")
        edges = (("0", "1"), ("0", "2"), ("0", "3"), ("1", "2"), ("1", "3"), ("2", "3"))
        cochain = {
            ("0", "1"): Fraction(1, 3),
            ("0", "2"): Fraction(-2, 5),
            ("0", "3"): Fraction(3, 7),
            ("1", "2"): Fraction(4, 9),
            ("1", "3"): Fraction(-1, 2),
            ("2", "3"): Fraction(5, 6),
        }

        _, _, bfs_cost = greedy_bfs_unwinding(vertices, edges, cochain)
        res = solve_native_obstruction(vertices, edges, cochain, require_native=True)
        sol = res.value

        assert sol.phi1 <= bfs_cost
        verify_dual_witness_5point(vertices, edges, cochain, sol)

    def test_mobius_ladder_m3_nonplanar(self):
        """Mobius ladder M3 (K_3,3): BFS gives 9, Simplex gives 6."""
        vertices = tuple(str(i) for i in range(6))
        edges = (
            ("0", "1"), ("1", "2"), ("2", "3"), ("3", "4"), ("4", "5"), ("5", "0"),
            ("0", "3"), ("1", "4"), ("2", "5"),
        )
        cochain = {
            ("0", "1"): Fraction(1), ("1", "2"): Fraction(1), ("2", "3"): Fraction(1),
            ("3", "4"): Fraction(1), ("4", "5"): Fraction(1), ("5", "0"): Fraction(1),
            ("0", "3"): Fraction(0), ("1", "4"): Fraction(0), ("2", "5"): Fraction(0),
        }

        _, _, bfs_cost = greedy_bfs_unwinding(vertices, edges, cochain)
        res = solve_native_obstruction(vertices, edges, cochain, require_native=True)
        sol = res.value

        assert bfs_cost == Fraction(9)
        assert sol.phi1 == Fraction(6)
        assert bfs_cost > sol.phi1

        verify_dual_witness_5point(vertices, edges, cochain, sol)

    def test_mobius_ladder_m4_twisted_rungs(self):
        """Mobius ladder M4 (8 vertices, 12 edges): BFS gives 12, Simplex gives 5."""
        vertices = tuple(str(i) for i in range(8))
        edges = (
            ("0", "1"), ("1", "2"), ("2", "3"), ("3", "4"),
            ("4", "5"), ("5", "6"), ("6", "7"), ("7", "0"),
            ("0", "4"), ("1", "5"), ("2", "6"), ("3", "7"),
        )
        cochain = {
            ("0", "1"): Fraction(2), ("1", "2"): Fraction(-1), ("2", "3"): Fraction(3), ("3", "4"): Fraction(1),
            ("4", "5"): Fraction(-2), ("5", "6"): Fraction(2), ("6", "7"): Fraction(1), ("7", "0"): Fraction(-1),
            ("0", "4"): Fraction(1), ("1", "5"): Fraction(-1), ("2", "6"): Fraction(2), ("3", "7"): Fraction(0),
        }

        _, _, bfs_cost = greedy_bfs_unwinding(vertices, edges, cochain)
        res = solve_native_obstruction(vertices, edges, cochain, require_native=True)
        sol = res.value

        assert bfs_cost == Fraction(12)
        assert sol.phi1 == Fraction(5)
        assert bfs_cost > sol.phi1

        verify_dual_witness_5point(vertices, edges, cochain, sol)

    def test_big_rational_arbitrary_precision(self):
        """Simplex solver handles 46-digit BigRationals without overflow or precision loss."""
        vertices = ("0", "1", "2")
        edges = (("0", "1"), ("1", "2"), ("2", "0"))
        # Large rational circulation
        r1 = Fraction(10**45 + 7, 10**30 + 3)
        r2 = Fraction(10**40 + 13, 10**25 + 9)
        r3 = Fraction(10**35 + 17, 10**20 + 11)
        cochain = {
            ("0", "1"): r1,
            ("1", "2"): r2,
            ("2", "0"): r3,
        }

        res = solve_native_obstruction(vertices, edges, cochain, require_native=True)
        assert res.is_ok, f"Solver failed on large rationals: {res}"
        sol = res.value

        # On a single oriented 3-cycle, Phi_1 is |r1 + r2 + r3|
        expected_phi1 = representative_mass((r1 + r2 + r3,))
        assert sol.phi1 == expected_phi1
        verify_dual_witness_5point(vertices, edges, cochain, sol)

    def test_exact_cochain_zero_defect(self):
        """Exact cochain h = d_0 phi must produce Phi_1 == 0, is_exact == True, and valid dual cycle."""
        vertices = ("v0", "v1", "v2", "v3")
        edges = (("v0", "v1"), ("v1", "v2"), ("v2", "v3"), ("v3", "v0"), ("v0", "v2"))
        # Exact potential: phi = {v0: 10, v1: 25, v2: 3, v3: -7}
        phi = {"v0": Fraction(10), "v1": Fraction(25), "v2": Fraction(3), "v3": Fraction(-7)}
        cochain = {
            (u, v): phi[v] - phi[u] for (u, v) in edges
        }

        res = solve_native_obstruction(vertices, edges, cochain, require_native=True)
        sol = res.value

        assert sol.is_exact is True
        assert sol.phi1 == Fraction(0)
        for r in sol.residual.values():
            assert r == Fraction(0)
        verify_dual_witness_5point(vertices, edges, cochain, sol)

    def test_random_adversarial_planar_graph_ensemble(self):
        """Random ensemble of 10 cyclic graphs: simplex never exceeds BFS and always satisfies 5-point verification."""
        rng = random.Random(42)
        for trial in range(10):
            n_vertices = 5
            vertices = tuple(f"v{i}" for i in range(n_vertices))
            # Create a base Hamiltonian cycle plus 3 random chords
            edges_set = set((f"v{i}", f"v{(i+1)%n_vertices}") for i in range(n_vertices))
            while len(edges_set) < n_vertices + 3:
                u = rng.choice(vertices)
                v = rng.choice(vertices)
                if u != v and (u, v) not in edges_set and (v, u) not in edges_set:
                    edges_set.add((u, v))
            edges = tuple(sorted(edges_set))

            cochain = {
                e: Fraction(rng.randint(-5, 5), rng.randint(1, 4))
                for e in edges
            }

            _, _, bfs_cost = greedy_bfs_unwinding(vertices, edges, cochain)
            res = solve_native_obstruction(vertices, edges, cochain, require_native=True)
            assert res.is_ok, f"Trial {trial} failed: {res}"
            sol = res.value

            assert sol.phi1 <= bfs_cost, f"Trial {trial}: Simplex ({sol.phi1}) > BFS ({bfs_cost})"
            verify_dual_witness_5point(vertices, edges, cochain, sol)
