"""Multiplicative sign audit of the explicit Z2 cocycle and normalized rephasings."""
from itertools import product


def main() -> None:
    bits = (0, 1)
    triples = tuple(product(bits, repeat=3))
    phase = {key: (-1) ** (key[0] * key[1] * key[2]) for key in triples}
    for a, b, c, d in product(bits, repeat=4):
        pentagon = (phase[b, c, d] * phase[(a + b) % 2, c, d]
                    * phase[a, (b + c) % 2, d] * phase[a, b, (c + d) % 2]
                    * phase[a, b, c])
        if pentagon != 1:
            raise SystemExit("cocycle identity failed")
    if any(value != 1 for key, value in phase.items() if 0 in key):
        raise SystemExit("normalization failed")
    normalized = 0
    for values in product((-1, 1), repeat=4):
        beta = dict(zip(product(bits, repeat=2), values))
        if any(beta[0, x] != 1 or beta[x, 0] != 1 for x in bits):
            continue
        normalized += 1
        boundary = {
            (a, b, c): beta[b, c] * beta[(a + b) % 2, c]
            * beta[a, (b + c) % 2] * beta[a, b]
            for a, b, c in triples
        }
        transformed = {key: phase[key] * boundary[key] for key in triples}
        if boundary[1, 1, 1] != 1 or boundary == phase:
            raise SystemExit("normalized coboundary obstruction failed")
        if transformed[1, 1, 1] != -1 or all(v == 1 for v in transformed.values()):
            raise SystemExit("negative generator sign was removed")
    if normalized != 2:
        raise SystemExit("normalization enumeration failed")
    print(f"pentagon_cases=16 cochains=16 normalized_cochains={normalized} "
          "generator_phase=-1 failures=0")


if __name__ == "__main__":
    main()
