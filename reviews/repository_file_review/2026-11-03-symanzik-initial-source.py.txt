"""Independent check for DFM-SYMANZIK-QED-AE-FENCE.

Connected 3-edge subsets and cotree products are recomputed with integers.
This file imports no repository code.
"""


EDGES = ((0, 1), (0, 2), (1, 3), (2, 3), (1, 2))
WEIGHTS = (2, 3, 5, 7, 11)


def run(mask):
    parents = [0, 1, 2, 3]

    def parent(x):
        return parents[x] if x < 4 else x

    def find(x):
        return parent(parent(parent(x)))

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parents[rb] = ra

    for i, (a, b) in enumerate(EDGES):
        if (mask >> i) & 1:
            union(a, b)
    return len({find(v) for v in range(4)})


def prod(mask, weights):
    value = 1
    for i, weight in enumerate(weights):
        if ((mask >> i) & 1) == 0:
            value *= weight
    return value


def main():
    listed = []
    connected = []
    for mask in range(32):
        if bin(mask).count("1") != 3:
            continue
        listed.append(mask)
        if run(mask) == 1:
            connected.append(mask)
        elif run(mask) != 2:
            raise SystemExit(f"unexpected components {mask}")
    if listed != [7, 11, 13, 14, 19, 21, 22, 25, 26, 28]:
        raise SystemExit(f"listed {listed}")
    if connected != [7, 11, 13, 14, 21, 22, 25, 26]:
        raise SystemExit(f"connected {connected}")
    if run(19) != 2 or run(28) != 2:
        raise SystemExit("disconnected")
    total = sum(prod(mask, WEIGHTS) for mask in connected)
    unit = sum(prod(mask, (1, 1, 1, 1, 1)) for mask in connected)
    if total != 247 or unit != 8:
        raise SystemExit(f"sums {total} {unit}")
    print("eight connected masks 7, 11, 13, 14, 21, 22, 25, 26")
    print("two disconnected masks 19 and 28 have 2 components")
    print("cotree sum at weights 2, 3, 5, 7, 11 is 247; unit sum is 8")
    print("checked: ten 3-edge masks, eight components, two cotree sums")


if __name__ == "__main__":
    main()
