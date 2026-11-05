#!/usr/bin/env python3
"""Exact rational observer completion and small polyhedral recovery problems.

Exact rational linear algebra and finite witness search. Functional values
are evaluated by the native omega_functional adapter; no floating point or network.
The general algorithms intentionally use exhaustive finite enumeration.
See sharp_observer_completion_theorem.md for definitions and complexity scope.
"""
import json
import sys
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import combinations, product

from witnessed_difference.native_functionals import representative_mass, polyhedral_gauge, dual_bound


def require(condition, message):
    if not condition:
        raise ValueError(message)


def rational(value, *, wire=False):
    """Exact scalars; wire values are canonical integer/fraction strings."""
    require(type(value) in ((str,) if wire else (str, int, F)), "exact rational required")
    result = F(value)
    if type(value) is str:
        require(str(result) == value, "noncanonical rational string")
    return result


def decode_json(text):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, "duplicate JSON key: " + key)
            result[key] = value
        return result

    def nonexact(value):
        raise ValueError("nonexact JSON number: " + value)

    return json.loads(text, object_pairs_hook=pairs, parse_float=nonexact,
                      parse_constant=nonexact)


def read_json(path):
    with open(path, encoding="utf-8") as stream:
        return decode_json(stream.read())


def same_json(left, right):
    """Compare JSON types as well as values; True is not integer one."""
    return json.dumps(left, sort_keys=True, separators=(",", ":")) == json.dumps(
        right, sort_keys=True, separators=(",", ":"))


@dataclass(frozen=True)
class M:
    a: tuple
    c: int

    def __init__(self, rows, cols=None):
        rows = tuple(tuple(rational(x) for x in row) for row in rows)
        if cols is None:
            cols = len(rows[0]) if rows else 0
        require(type(cols) is int and cols >= 0, "nonnegative integer column count")
        require(all(len(row) == cols for row in rows), "ragged matrix")
        object.__setattr__(self, "a", rows)
        object.__setattr__(self, "c", cols)

    @property
    def r(self):
        return len(self.a)

    @property
    def T(self):
        return M([[self.a[i][j] for i in range(self.r)] for j in range(self.c)], self.r)

    def __matmul__(self, b):
        require(self.c == b.r, "matrix product shape")
        return M([[sum((self.a[i][k] * b.a[k][j] for k in range(self.c)), F(0))
                   for j in range(b.c)] for i in range(self.r)], b.c)

    def __add__(self, b):
        require((self.r, self.c) == (b.r, b.c), "matrix sum shape")
        return M([[x+y for x, y in zip(a, bb)] for a, bb in zip(self.a, b.a)], self.c)

    def __neg__(self):
        return M([[-x for x in row] for row in self.a], self.c)

    def __sub__(self, b):
        return self + (-b)

    def cols(self, ids):
        return M([[row[i] for i in ids] for row in self.a], len(ids))

    def rows(self, ids):
        return M([self.a[i] for i in ids], self.c)

    def encode(self):
        return {"rows": self.r, "cols": self.c,
                "data": [[str(x) for x in row] for row in self.a]}

    @staticmethod
    def decode(value):
        require(type(value) is dict and set(value) == {"rows", "cols", "data"}, "matrix fields")
        require(all(type(value[key]) is int and value[key] >= 0 for key in ("rows", "cols")),
                "nonnegative integer matrix dimensions")
        require(type(value["data"]) is list and all(type(row) is list for row in value["data"]),
                "matrix array required")
        for row in value["data"]:
            for entry in row:
                rational(entry, wire=True)
        m = M(value["data"], value["cols"])
        require((m.r, m.c) == (value["rows"], value["cols"]), "matrix dimensions")
        return m


def zero(r, c):
    return M([[0]*c for _ in range(r)], c)


def eye(n):
    return M([[int(i == j) for j in range(n)] for i in range(n)], n)


def hc(*matrices):
    r = matrices[0].r
    require(all(a.r == r for a in matrices), "horizontal shape")
    return M([sum((list(a.a[i]) for a in matrices), []) for i in range(r)],
             sum(a.c for a in matrices))


def vc(*matrices):
    c = matrices[0].c
    require(all(a.c == c for a in matrices), "vertical shape")
    return M([row for a in matrices for row in a.a], c)


def rref(a):
    rows = [list(row) for row in a.a]
    pivots = []
    i = 0
    for j in range(a.c):
        p = next((k for k in range(i, a.r) if rows[k][j]), None)
        if p is None:
            continue
        rows[i], rows[p] = rows[p], rows[i]
        d = rows[i][j]
        rows[i] = [x/d for x in rows[i]]
        for k in range(a.r):
            if k != i:
                d = rows[k][j]
                rows[k] = [x-d*y for x, y in zip(rows[k], rows[i])]
        pivots.append(j)
        i += 1
        if i == a.r:
            break
    return M(rows, a.c), pivots


def rank(a):
    return len(rref(a)[1])


def basis(a):
    return a.cols(rref(a)[1])


def null(a):
    rr, ps = rref(a)
    free = [j for j in range(a.c) if j not in ps]
    result = [[F(0)]*len(free) for _ in range(a.c)]
    for t, f in enumerate(free):
        result[f][t] = F(1)
        for i, p in enumerate(ps):
            result[p][t] = -rr.a[i][f]
    return M(result, len(free))


def solve(a, b):
    require(a.r == b.r, "solve shape")
    rr, ps = rref(hc(a, b))
    require(all(p < a.c for p in ps), "inconsistent equations")
    out = [[F(0)]*b.c for _ in range(a.c)]
    for i, p in enumerate(ps):
        out[p] = list(rr.a[i][a.c:])
    x = M(out, b.c)
    require(a @ x == b, "solve verification")
    return x


def inverse(a):
    require(a.r == a.c and rank(a) == a.r, "not invertible")
    return solve(a, eye(a.r))


def extend(a, candidates):
    b = a
    for j in range(candidates.c):
        trial = hc(b, candidates.cols([j]))
        if rank(trial) > b.c:
            b = trial
    return b


def spaces(d, q):
    require(q.c == d.r, "carrier mismatch")
    s = basis(d)
    n = null(q)
    h = s @ null(q @ s)
    return s, n, h


def guarantees(d, a):
    s, n, h = spaces(d, a)
    return {"raw": h.c == 0, "quotient": rank(hc(s, n)) == s.c}


def construct(d, q, target):
    s, n, h = spaces(d, q)
    k, r = n.c, h.c
    adapted = extend(extend(extend(h, n), s), eye(d.r))
    inv = inverse(adapted)
    indices = {"raw": list(range(r)), "quotient": list(range(r, k)),
               "both": list(range(k))}[target]
    rr = inv.rows(indices)
    return {
        "target": target, "R": rr.encode(), "minimum": len(indices),
        "dimensions": {"B": s.c, "K": k, "intersection": r},
        "B_basis": s.encode(), "K_basis": n.encode(), "intersection_basis": h.encode(),
        "adapted_basis": adapted.encode(), "adapted_inverse": inv.encode(),
    }


def check_completion(d, q, receipt):
    """Recompute the dimension lower bound and test the supplied measurements."""
    keys = {"target", "R", "minimum", "dimensions", "B_basis", "K_basis", "intersection_basis"}
    require(set(receipt) in (keys, keys | {"adapted_basis", "adapted_inverse"}), "completion fields")
    rr = M.decode(receipt["R"])
    target = receipt["target"]
    require(target in ("raw", "quotient", "both"), "target")
    s, n, h = spaces(d, q)
    require(type(receipt["minimum"]) is int and
            all(type(x) is int for x in receipt["dimensions"].values()), "integer dimension claims")
    require(receipt["dimensions"] == {"B": s.c, "K": n.c, "intersection": h.c},
            "dimension claim")
    minimum = {"raw": h.c, "quotient": n.c-h.c, "both": n.c}[target]
    require(rr.c == d.r and rr.r == minimum == receipt["minimum"], "minimum claim")
    for name, actual in (("B_basis", s), ("K_basis", n), ("intersection_basis", h)):
        supplied = M.decode(receipt[name])
        require(supplied.r == actual.r and supplied.c == actual.c and
                rank(supplied) == actual.c and rank(hc(actual, supplied)) == actual.c,
                "basis claim " + name)
    if "adapted_basis" in receipt:
        e = M.decode(receipt["adapted_basis"])
        ei = M.decode(receipt["adapted_inverse"])
        require((e.r, e.c) == (d.r, d.r) and (ei.r, ei.c) == (d.r, d.r), "adapted shape")
        require(e @ ei == eye(d.r) and ei @ e == eye(d.r), "adapted inverse")
        for actual, supplied in (
            (h, e.cols(range(h.c))),
            (n, e.cols(range(n.c))),
            (s, hc(e.cols(range(h.c)), e.cols(range(n.c, n.c+s.c-h.c)))),
        ):
            require(supplied.c == actual.c and rank(supplied) == actual.c and
                    rank(hc(actual, supplied)) == actual.c, "adapted subspace order")
    g = guarantees(d, vc(q, rr))
    require(all(g[x] for x in (("raw", "quotient") if target == "both" else (target,))),
            "completion guarantee")
    return True


def failure(d, q, target):
    s, n, h = spaces(d, q)
    if target in ("raw", "both") and h.c:
        z = h.cols([0])
        return {"kind": "raw", "z": z.encode(), "preimage": solve(d, z).encode()}
    if target in ("quotient", "both"):
        for j in range(n.c):
            z = n.cols([j])
            if rank(hc(s, z)) > s.c:
                y = solve(vc(s.T, z.T), vc(zero(s.c, 1), M([[1]]))).T
                return {"kind": "quotient", "z": z.encode(), "separator": y.encode()}
    return None


def check_failure(d, q, receipt):
    keys = {"kind", "z", "preimage"} if receipt["kind"] == "raw" else {"kind", "z", "separator"}
    require(set(receipt) == keys, "failure fields")
    z = M.decode(receipt["z"])
    require(z.r == d.r and z.c == 1 and z != zero(d.r, 1), "nonzero witness")
    require(q @ z == zero(q.r, 1), "invisibility")
    if receipt["kind"] == "raw":
        require(d @ M.decode(receipt["preimage"]) == z, "raw realization")
    else:
        require(receipt["kind"] == "quotient", "failure kind")
        y = M.decode(receipt["separator"])
        require(y @ d == zero(1, d.c) and y @ z == M([[1]]), "quotient separation")
    return True


def l1(x):
    require(x.c == 1, "vector required")
    return representative_mass(row[0] for row in x.a)


def op1(a):
    return max((representative_mass(a.a[i][j] for i in range(a.r)) for j in range(a.c)),
               default=F(0))


def facets_l1(n):
    """Exponential representation, intended only for small generic examples."""
    return M(list(product((-1, 1), repeat=n)), n)


def facets_linf(n):
    return vc(eye(n), -eye(n))


def validate_norm(h, n):
    require(h.c == n and (h.r > 0 or n == 0) and rank(h) == n, "norm facets do not span")
    rows = set(h.a)
    require(all(tuple(-x for x in row) in rows for row in rows), "not symmetric")


def norm(h, v):
    require(v.c == 1 and v.r == h.c, "norm vector shape")
    validate_norm(h, v.r)
    return polyhedral_gauge(h.a, (row[0] for row in v.a))


def vertices(g, rhs):
    """All vertices of {x: g*x<=rhs}; completeness by all active bases."""
    out = {}
    for ids in combinations(range(g.r), g.c):
        square = g.rows(ids)
        if rank(square) != g.c:
            continue
        x = solve(square, rhs.rows(ids))
        gx = g @ x
        if all(gx.a[i][0] <= rhs.a[i][0] for i in range(g.r)):
            out[x.a] = (x, ids)
    return [out[k] for k in sorted(out)]


def distance_certificate(h, s, v):
    """Primal and dual exact LP witnesses for min_a ||v-Sa||_H."""
    validate_norm(h, v.r)
    require(v.c == 1 and s.r == v.r, "distance carrier shape")
    require(rank(s) == s.c, "repair basis")
    if v.r == 0:
        return {"v": v.encode(), "repair_coefficients": zero(0, 1).encode(),
                "value": "0", "mu": zero(h.r, 1).encode(), "zero_dimensional": True}
    ones = M([[1]]*h.r)
    g = hc(-(h @ s), -ones)
    rhs = -(h @ v)
    candidates = vertices(g, rhs)
    require(candidates, "distance epigraph unexpectedly has no vertex")
    primal, active = min(candidates, key=lambda item: item[0].a[s.c][0])
    t = primal.a[s.c][0]
    constraints = vc(M([[1]*h.r]), s.T @ h.T)
    target = vc(M([[1]]), zero(s.c, 1))
    # Independent equality rows allow enumeration of all basic feasible duals.
    row_ids = rref(constraints.T)[1]
    ce = constraints.rows(row_ids)
    te = target.rows(row_ids)
    dual = None
    for ids in combinations(range(h.r), ce.r):
        sub = ce.cols(ids)
        if rank(sub) != ce.r:
            continue
        vals = solve(sub, te)
        if any(row[0] < 0 for row in vals.a):
            continue
        mu = [[F(0)] for _ in range(h.r)]
        for i, j in enumerate(ids):
            mu[j][0] = vals.a[i][0]
        mu = M(mu)
        if constraints @ mu == target and (mu.T @ h @ v).a[0][0] == t:
            dual = mu
            break
    require(dual is not None, "no matching dual certificate")
    return {"v": v.encode(), "repair_coefficients": primal.rows(range(s.c)).encode(),
            "value": str(t), "mu": dual.encode()}


def check_distance(h, s, receipt):
    validate_norm(h, h.c)
    v = M.decode(receipt["v"])
    a = M.decode(receipt["repair_coefficients"])
    mu = M.decode(receipt["mu"])
    t = rational(receipt["value"], wire=True)
    require(v.c == 1 and v.r == h.c and s.r == h.c, "distance carrier shape")
    if h.c == 0:
        require(s.c == 0 and same_json(receipt, distance_certificate(h, s, v)),
                "zero distance convention")
        return F(0)
    require(set(receipt) == {"v", "repair_coefficients", "value", "mu"}, "distance fields")
    require(mu.r == h.r and mu.c == 1 and all(x[0] >= 0 for x in mu.a), "dual signs")
    require(sum(x[0] for x in mu.a) == 1, "dual normalization")
    require(s.T @ h.T @ mu == zero(s.c, 1), "dual annihilation")
    # Convex facet weights give a dual form. These positive coordinate weights
    # only admit its signed pairing to the canonical checker; the polyhedral
    # gauge, simplex constraint and annihilation supply the actual bounds.
    dual = h.T @ mu
    weights = tuple(1 + representative_mass(h.a[i][j] for i in range(h.r)) for j in range(h.c))
    lower = dual_bound(s.a, s.c, tuple(row[0] for row in v.a), weights,
                       tuple(row[0] for row in dual.a))
    require(norm(h, v-s @ a) == t == lower, "matching bounds")
    return t


def recovery_certificate(d, a, h, f, target):
    """Sharp constant; potentially enormous finite enumeration."""
    require(target in ("raw", "quotient"), "recovery target")
    validate_norm(h, d.r)
    validate_norm(f, a.r)
    require(guarantees(d, a)[target], "no finite constant: request failure witness")
    s = basis(d)
    if target == "raw":
        lifted = s
        e = None
        m = a @ s
    else:
        e = extend(s, eye(d.r)).cols(range(s.c, d.r))
        t = basis(a @ s)
        m = hc(a @ e, -t)
        lifted = e
    dimension = s.c if target == "raw" else d.r-s.c
    if dimension == 0:
        return {"target": target, "constant": "0", "vertices": [], "vacuous": True}
    require(rank(m) == m.c, "unbounded lifted recovery polytope")
    vv = vertices(f @ m, M([[1]]*f.r))
    records = []
    for x, ids in vv:
        v = lifted @ (x if target == "raw" else x.rows(range(e.c)))
        if target == "raw":
            obj = norm(h, v)
            dist = None
        else:
            dist = distance_certificate(h, s, v)
            obj = F(dist["value"])
        records.append({"point": x.encode(), "active_rows": list(ids),
                        "value": str(obj), "distance": dist})
    require(records, "no recovery vertices")
    return {"target": target, "constant": str(max(F(x["value"]) for x in records)),
            "vertices": records, "vacuous": False}


def check_recovery(d, a, h, f, receipt):
    require(set(receipt) == {"target", "constant", "vertices", "vacuous"}, "recovery fields")
    target = receipt["target"]
    require(target in ("raw", "quotient") and guarantees(d, a)[target], "soundness")
    validate_norm(h, d.r)
    validate_norm(f, a.r)
    s = basis(d)
    dimension = s.c if target == "raw" else d.r-s.c
    if not dimension:
        require(same_json(receipt, {"target": target, "constant": "0",
                                   "vertices": [], "vacuous": True}), "vacuous constant")
        return True
    require(receipt["vacuous"] is False, "nonvacuous recovery")
    e = extend(s, eye(d.r)).cols(range(s.c, d.r))
    m = a @ s if target == "raw" else hc(a @ e, -basis(a @ s))
    g, ones = f @ m, M([[1]]*f.r)
    expected = {v.a for v, _ in vertices(g, ones)}
    supplied = set()
    values = []
    for item in receipt["vertices"]:
        require(set(item) == {"point", "active_rows", "value", "distance"}, "vertex fields")
        x = M.decode(item["point"])
        ids = item["active_rows"]
        require(type(ids) is list and len(ids) == g.c and
                all(type(i) is int and 0 <= i < g.r for i in ids) and
                len(set(ids)) == len(ids), "active row indices")
        require(rank(g.rows(ids)) == g.c and g.rows(ids) @ x == ones.rows(ids),
                "active row witness")
        require(x.a not in supplied, "duplicate vertex")
        supplied.add(x.a)
        v = s @ x if target == "raw" else e @ x.rows(range(e.c))
        if target == "raw":
            require(item["distance"] is None, "raw recovery has no distance claim")
            val = norm(h, v)
        else:
            require(M.decode(item["distance"]["v"]) == v, "distance query binding")
            val = check_distance(h, s, item["distance"])
        require(val == rational(item["value"], wire=True), "vertex value")
        values.append(val)
    require(supplied == expected, "incomplete or extraneous vertex enumeration")
    require(rational(receipt["constant"], wire=True) == max(values), "sharp constant")
    return True


def check_input(data):
    allowed = {"d0", "Q", "target", "V_facets", "augmented_facets"}
    require(type(data) is dict and {"d0", "Q", "target"} <= set(data) <= allowed,
            "input fields")
    require(data["target"] in ("raw", "quotient", "both"), "input target")
    d, q = M.decode(data["d0"]), M.decode(data["Q"])
    require(q.c == d.r, "input carrier mismatch")
    require(("V_facets" in data) == ("augmented_facets" in data), "paired norm declarations")
    if "V_facets" in data:
        s, n, h = spaces(d, q)
        minimum = {"raw": h.c, "quotient": n.c-h.c, "both": n.c}[data["target"]]
        validate_norm(M.decode(data["V_facets"]), d.r)
        validate_norm(M.decode(data["augmented_facets"]), q.r + minimum)
    return d, q


def check_receipt(data, expected):
    """Bind every supported claim to a separately supplied input and norms."""
    d, q = check_input(expected)
    require(same_json(data["input"], expected), "receipt differs from expected input")
    keys = {"input", "initial_failure", "completion", "authority_effect"}
    if "V_facets" in expected:
        keys.add("recovery")
    require(set(data) == keys, "receipt fields")
    require(data["authority_effect"] == "None", "authority field")
    target = expected["target"]
    require(data["completion"]["target"] == target, "target binding")
    check_completion(d, q, data["completion"])
    targets = ["raw", "quotient"] if target == "both" else [target]
    failed = [name for name in targets if not guarantees(d, q)[name]]
    witness = data["initial_failure"]
    if failed:
        require(type(witness) is dict and witness["kind"] in failed, "missing or unrelated failure")
        check_failure(d, q, witness)
    else:
        require(witness is None, "false initial failure")
    if "recovery" in data:
        a = vc(q, M.decode(data["completion"]["R"]))
        require([r["target"] for r in data["recovery"]] == targets, "recovery targets")
        for rr in data["recovery"]:
            check_recovery(d, a, M.decode(expected["V_facets"]),
                           M.decode(expected["augmented_facets"]), rr)
    return True


def run_input(data):
    d, q = check_input(data)
    target = data["target"]
    out = {"input": data, "initial_failure": failure(d, q, target),
           "completion": construct(d, q, target), "authority_effect": "None"}
    check_completion(d, q, out["completion"])
    if out["initial_failure"]:
        check_failure(d, q, out["initial_failure"])
    if "V_facets" in data:
        a = vc(q, M.decode(out["completion"]["R"]))
        h, f = M.decode(data["V_facets"]), M.decode(data["augmented_facets"])
        out["recovery"] = [recovery_certificate(d, a, h, f, t)
                           for t in (("raw", "quotient") if target == "both" else (target,))]
        for rr in out["recovery"]:
            check_recovery(d, a, h, f, rr)
    check_receipt(out, data)
    return out


if __name__ == "__main__":
    require(len(sys.argv) in (3, 4) and sys.argv[1] in ("solve", "check"),
            "usage: observer_completion.py solve INPUT.json | check RECEIPT.json INPUT.json")
    data = read_json(sys.argv[2])
    if sys.argv[1] == "solve":
        require(len(sys.argv) == 3, "solve takes one input file")
        print(json.dumps(run_input(data), indent=2))
    else:
        require(len(sys.argv) == 4, "check needs a separate expected-input file")
        expected = read_json(sys.argv[3])
        check_receipt(data, expected)
        print("Exact certificate checks passed.")
