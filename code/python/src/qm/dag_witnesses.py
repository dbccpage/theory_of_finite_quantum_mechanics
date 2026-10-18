"""Topological witness for a finite causal DAG.

A Kahn traversal records a linear extension. The witness is the number of
edges that point backward in that extension.
"""
from fractions import Fraction


class DagWitnessError(Exception):
    """The relation is not a DAG or the extension is not linear."""


def backward_edge_count() -> int:
    """Return the number of backward edges in a Kahn order of the diamond.

    Edges are 0→1, 0→2, 1→3, 2→3. The order is produced by always releasing
    the least ready vertex, and each original edge is then compared with it.
    """
    edges = ((0, 1), (0, 2), (1, 3), (2, 3))
    vertices = (0, 1, 2, 3)
    indegree = {vertex: 0 for vertex in vertices}
    for _source, target in edges:
        indegree[target] += 1
    ready = sorted(vertex for vertex, degree in indegree.items() if degree == 0)
    order = []
    while ready:
        source = ready.pop(0)
        order.append(source)
        released = []
        for origin, target in edges:
            if origin != source:
                continue
            indegree[target] -= 1
            if indegree[target] == 0:
                released.append(target)
        ready.extend(sorted(released))
    if len(order) != len(vertices):
        raise DagWitnessError("the priced relation has a cycle")
    position = {vertex: index for index, vertex in enumerate(order)}
    backward = 0
    for source, target in edges:
        if position[source] >= position[target]:
            backward += 1
    span = Fraction(len(order), len(vertices))
    if span != 1:
        raise DagWitnessError(f"order span is {span}")
    return backward
