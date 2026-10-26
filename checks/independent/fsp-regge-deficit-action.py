"""Exact symbolic and integer audit of finite deficit sums; no geometry is inferred."""
from itertools import product
import sympy as sp


def main() -> None:
    area = sp.Matrix(sp.symbols("A0:3"))
    other = sp.Matrix(sp.symbols("B0:3"))
    turn, scale, mix = sp.symbols("T lambda mu")
    angles = [sp.symbols("u0:2"), sp.symbols("v0:3"), sp.symbols("w0:1")]
    angle_sums = sp.Matrix([sum(row) for row in angles])
    deficits = sp.ones(3, 1) * turn - angle_sums
    action = (area.T * deficits)[0]
    expanded = turn * sum(area) - (area.T * angle_sums)[0]
    linear = (((scale * area + mix * other).T * deficits)[0]
              - scale * action - mix * (other.T * deficits)[0])
    a, b, d = sp.symbols("a b d")
    identities = (action - expanded, linear, a * d + b * d - (a + b) * d)
    if any(sp.expand(expr) != 0 for expr in identities):
        raise SystemExit("symbolic finite-action identity failed")
    cases = 0
    for weights in product((-2, 0, 3), repeat=3):
        for curvature in product((-1, 0, 2), repeat=3):
            direct = sum(x * y for x, y in zip(weights, curvature))
            matrix_value = (sp.Matrix(weights).T * sp.Matrix(curvature))[0]
            if direct != matrix_value:
                raise SystemExit("matrix contraction disagrees with exact sum")
            if not any(curvature) and direct != 0:
                raise SystemExit("flat deficits gave nonzero action")
            cases += 1
    cancellation = sum(a * e for a, e in zip((1, 1), (1, -1)))
    distinct_areas = [sum(a * e for a, e in zip((area,), (1,))) for area in (1, 2)]
    if cancellation != 0 or distinct_areas != [1, 2]:
        raise SystemExit("nonflat cancellation/area-dependence witnesses failed")
    print(f"symbolic_identities={len(identities)} integer_cases={cases} "
          f"nonflat_action={cancellation} area_actions={distinct_areas} failures=0")


if __name__ == "__main__":
    main()
