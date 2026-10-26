"""Exact rational two-qubit readout fixture and separate certificate checks."""

from fractions import Fraction as Q

from .checker import check_congruence


def trace_product(a, b):
    return sum(Q(a[i][j]) * Q(b[j][i]) for i in range(len(a)) for j in range(len(a)))


def marginal(a):
    return [[sum(Q(a[2 * i + k][2 * j + k]) for k in range(2)) for j in range(2)] for i in range(2)]


def check_locality(problem, certificate):
    """No commutator-trace shortcut: replay the actual bound density/readout data."""
    try:
        rho, sigma, near, operator = [problem[k] for k in ("rho", "sigma", "near", "operator")]
        if any(
            len(a) != 4 or any(len(row) != 4 for row in a) for a in (rho, sigma, near, operator)
        ):
            return False
        if any(
            type(x) is not str or str(Q(x)) != x
            for a in (rho, sigma, near, operator)
            for row in a
            for x in row
        ):
            return False
        matrices = {"rho": rho, "sigma": sigma}
        if any(sum(Q(a[i][i]) for i in range(4)) != 1 for a in (rho, sigma)) or marginal(
            rho
        ) != marginal(sigma):
            return False
        # near must be A tensor identity on the unobserved second qubit.
        if any(
            Q(near[2 * i + k][2 * j + offset]) != (Q(near[2 * i][2 * j]) if k == offset else 0)
            for i in range(2)
            for j in range(2)
            for k in range(2)
            for offset in range(2)
        ):
            return False
        beta = Q(problem["beta"])
        if beta < 0:
            return False
        tail = [[Q(operator[i][j]) - Q(near[i][j]) for j in range(4)] for i in range(4)]
        for sign, name in ((1, "upper"), (-1, "lower")):
            matrices[name] = [
                [str((beta if i == j else 0) + sign * tail[i][j]) for j in range(4)]
                for i in range(4)
            ]
        if set(certificate) != {"forms", "readout_difference"} or set(certificate["forms"]) != set(
            matrices
        ):
            return False
        for name, a in matrices.items():
            witness = certificate["forms"][name]
            if not check_congruence(a, witness) or any(Q(x) < 0 for x in witness["diagonal"]):
                return False
        delta = [[Q(rho[i][j]) - Q(sigma[i][j]) for j in range(4)] for i in range(4)]
        actual = trace_product(delta, operator)
        return Q(certificate["readout_difference"]) == actual and abs(actual) <= 2 * beta
    except (ValueError, TypeError, KeyError, ZeroDivisionError):
        return False


def fixture():
    rho = [["1/2", "0", "0", "1/2"], ["0"] * 4, ["0"] * 4, ["1/2", "0", "0", "1/2"]]
    sigma = [["1/2", "0", "0", "-1/2"], ["0"] * 4, ["0"] * 4, ["-1/2", "0", "0", "1/2"]]
    near = [[str((1 if i < 2 else -1) if i == j else 0) for j in range(4)] for i in range(4)]
    operator = [
        [str(Q(near[i][j]) + (Q(1, 8) if j == 3 - i else 0)) for j in range(4)] for i in range(4)
    ]
    return {"rho": rho, "sigma": sigma, "near": near, "operator": operator, "beta": "1/8"}
