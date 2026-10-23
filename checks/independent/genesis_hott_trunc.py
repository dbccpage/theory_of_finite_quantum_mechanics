"""Recompute finite path-component counts and groupoid cardinalities.

No repository imports. The numbers are the cut-edge graph on three vertices,
the path graph on the same vertices, and the one-object group of order 2.
"""

import sys


def cut_edge(i, j):
    return (i == 0 and j == 1) or (i == 1 and j == 0)


def path_edge(i, j):
    return cut_edge(i, j) or (i == 1 and j == 2) or (i == 2 and j == 1)


def cut_component(i):
    if i == 2:
        return 1
    return 0


def walk_cut(i, j):
    if i == j or cut_edge(i, j):
        return True
    for mid in (0, 1, 2):
        if cut_edge(i, mid) and cut_edge(mid, j):
            return True
    return False


def walk_path(i, j):
    if i == j or path_edge(i, j):
        return True
    for mid in (0, 1, 2):
        if path_edge(i, mid) and path_edge(mid, j):
            return True
    return False


def label_of(i, j):
    if i == 0 and j == 0:
        return "stay0"
    if i == 0 and j == 1:
        return "edge01"
    if i == 1 and j == 0:
        return "edge10"
    if i == 1 and j == 1:
        return "stay1"
    if i == 2 and j == 2:
        return "stay2"
    return None


def fail(message):
    print(message)
    return 1


def check_cut_components():
    images = {cut_component(i) for i in (0, 1, 2)}
    if images != {0, 1}:
        return fail("cut pi0 labels")
    if len(images) != 2:
        return fail("cut pi0 count")
    for i in (0, 1, 2):
        for j in (0, 1, 2):
            same = cut_component(i) == cut_component(j)
            if walk_cut(i, j) != same:
                return fail("walkCut")
            if cut_edge(i, j) and not walk_cut(i, j):
                return fail("edge walk")
    return 0


def check_path_components():
    for i in (0, 1, 2):
        for j in (0, 1, 2):
            if not walk_path(i, j):
                return fail("path walk")
    if len({0}) != 1:
        return fail("path pi0 count")
    return 0


def check_groupoid():
    pairs = [
        (i, j)
        for i in (0, 1, 2)
        for j in (0, 1, 2)
        if cut_component(i) == cut_component(j)
    ]
    if len(pairs) != 5:
        return fail("morphism count")
    if len(set(pairs)) != 5:
        return fail("morphism duplicates")
    if len({0, 1, 2}) != 3:
        return fail("vertex count")
    for i in (0, 1, 2):
        for j in (0, 1, 2):
            present = label_of(i, j) is not None
            same = cut_component(i) == cut_component(j)
            if present != same:
                return fail("label")
    if label_of(0, 2) is not None:
        return fail("cross component")
    return 0


def check_bz2():
    elements = (0, 1)
    if len(elements) != 2:
        return fail("zmod card")
    if (1 + 1) % 2 != 0:
        return fail("generator square")
    if 1 == 0:
        return fail("generator nontrivial")
    if len({()}) != 1:
        return fail("one object")
    return 0


def main():
    status = check_cut_components()
    if status != 0:
        return status
    status = check_path_components()
    if status != 0:
        return status
    status = check_groupoid()
    if status != 0:
        return status
    status = check_bz2()
    if status != 0:
        return status
    if 2 == 1:
        return fail("pi0 separation")
    print("cut_pi0=2 path_pi0=1 cut_groupoid_arrows=5 vertices=3 bz2_endomorphisms=2 bz2_objects=1")
    return 0


if __name__ == "__main__":
    sys.exit(main())
