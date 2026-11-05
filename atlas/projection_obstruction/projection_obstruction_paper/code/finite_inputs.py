"""Declared finite inputs, shared as data by producer and independent checker.

The separable mixture (|000><000| + |111><111|)/2 has pair moments 1
and one-site moments 0. Its distance from product is not entanglement evidence.
The three-factor input is a declared moment/error contract, not laboratory data.
"""

from __future__ import annotations


def measurement_requests() -> dict[str, dict]:
    common = {
        "site_count": 3,
        "reading_error": "1/30",
        "coverage_assumption": "Each listed joint and single-site moment has simultaneous absolute error at most 1/30; supplied as a premise.",
        "repair_rule": "oriented_cycle_gradients_mean_l1",
    }
    pairs = [[{"site": i, "axis": "Z"} for i in support] for support in ((0, 1), (1, 2), (0, 2))]
    triples = [[{"site": i, "axis": axis} for i in range(3)] for axis in ("X", "Y", "Z")]
    def request(factors, arity, joint):
        return {"contract": {**common, "arity": arity, "observables": [
            {"id": f"o{i}", "factors": f} for i, f in enumerate(factors)]},
            "joint_moments": joint,
            "factor_moments": [["0"] * arity for _ in factors],
            "repair_potential": ["0"] * 3, "dual_witness": ["1/3"] * 3}
    ring = [[{"site": i, "axis": "X" if i == j else "Z"}
             for i in sorted(((j - 1) % 5, j, (j + 1) % 5))] for j in range(5)]
    physical = {"contract": {**common, "site_count": 5, "arity": 3,
        "observables": [{"id": f"K{j}", "factors": f} for j, f in enumerate(ring)]},
        "joint_moments": ["-1"] * 5, "factor_moments": [["0"] * 3 for _ in ring],
        "repair_potential": ["0"] * 5, "dual_witness": ["-1/5"] * 5}
    return {"separable_correlated": request(pairs, 2, ["1"] * 3),
            "three_factor": request(triples, 3, ["1/4"] * 3),
            "ising_five_cycle": physical}


def local_zero_models():
    import sympy as sp
    from local_persistent_zero import LocalModel, LocalTerm

    identity, x = sp.eye(2), sp.Matrix([[0, 1], [1, 0]])
    y, z, rho = sp.Matrix([[0, -sp.I], [sp.I, 0]]), sp.diag(1, -1), sp.diag(1, 0)
    return {
        "commuting_boundary": LocalModel((2, 2), (0,),
            (LocalTerm((0, 1), sp.kronecker_product(z, x)),), (identity, z), rho,
            ({(0, 1): sp.S.One, (0, 0): -sp.S.One},), 1),
        "rotating_polynomial": LocalModel((2,), (0,), (LocalTerm((0,), x),),
            (identity, x, y, z), rho,
            ({(0, 0, 2, 0): sp.S.One, (0, 0, 0, 2): sp.S.One,
              (0, 0, 0, 0): -sp.S.One},), 2),
    }
