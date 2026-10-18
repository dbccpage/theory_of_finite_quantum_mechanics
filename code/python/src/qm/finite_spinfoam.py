"""Euler characteristic of the boundary of a tetrahedron.

Vertices, edges, and faces are counted from the complete graph K4 and its
triangles. The characteristic is V - E + F.
"""
from itertools import combinations


class SpinfoamError(Exception):
    """The counted complex is not a tetrahedral boundary."""


def tetrahedron_euler() -> int:
    """Return V - E + F for the four vertices of a tetrahedron."""
    vertices = (0, 1, 2, 3)
    edges = list(combinations(vertices, 2))
    faces = list(combinations(vertices, 3))
    for face in faces:
        face_edges = list(combinations(face, 2))
        if any(edge not in edges for edge in face_edges):
            raise SpinfoamError("a face uses an edge that was not counted")
    characteristic = len(vertices) - len(edges) + len(faces)
    if len(vertices) != 4 or len(edges) != 6 or len(faces) != 4:
        raise SpinfoamError(
            f"counts are V={len(vertices)} E={len(edges)} F={len(faces)}"
        )
    return characteristic
