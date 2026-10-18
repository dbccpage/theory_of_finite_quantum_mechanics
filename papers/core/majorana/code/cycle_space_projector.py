"""Cycle space projector functional."""

import numpy as np
from typing import List, Tuple


def compute_cycle_space_projector_graph_only(
    n_nodes: int, edges: List[Tuple[int, int]]
) -> np.ndarray:
    """
    Computes the orthogonal projection matrix onto the harmonic cycle space (im(d₀)⊥)
    for a graph complex where ker(d₁) is assumed to be the whole space.
    """
    if not edges:
        return np.zeros((0, 0))

    b = np.zeros((len(edges), n_nodes))
    for i, (u, v) in enumerate(edges):
        b[i, u] = -1.0
        b[i, v] = 1.0

    b_pinv = np.linalg.pinv(b, rcond=1e-10)

    exact_proj = b @ b_pinv
    cycle_proj = np.eye(len(edges)) - exact_proj

    cycle_proj = 0.5 * (cycle_proj + cycle_proj.T)
    return cycle_proj


from typing import Any  


class _RustSurfaceMeta(type):
    def __getattr__(cls, name: str) -> Any:
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(name)

        def unavailable(*args: Any, **kwargs: Any) -> Any:
            raise NotImplementedError(
                f"Behavioral method {cls.__name__}.{name} is not ported"
            )

        return unavailable


class _RustSurfaceObject(metaclass=_RustSurfaceMeta):
    def __getattr__(self, name: str) -> Any:
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(name)

        def unavailable(*args: Any, **kwargs: Any) -> Any:
            raise NotImplementedError(
                f"Behavioral method {type(self).__name__}.{name} is not ported"
            )

        return unavailable


def compute_harmonic_basis(*args: Any, **kwargs: Any) -> Any:
    """Structural mirror of Rust callable ``compute_harmonic_basis``."""

    raise NotImplementedError(
        "Behavioral port not implemented; Rust authority: omega_engine/crates/omega_homology/src/cycle_space_projector.rs::compute_harmonic_basis"
    )



