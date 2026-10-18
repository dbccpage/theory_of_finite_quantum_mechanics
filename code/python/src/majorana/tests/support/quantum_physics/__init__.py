"""Universe Anomalonica Quantum Physics Subsystem Package.

AuthorityEffect: None.
"""

import warnings

warnings.warn(
    "omega_engine.crates.quantum_physics is deprecated, use workspace Rust crates / PyO3 extensions",
    DeprecationWarning,
    stacklevel=2,
)

from . import (
    bipartite_carrier,
    bipartite_retraction,
    born_normalization,
    chern_simons,
    contextuality_f2,
    cptp_channel,
    diagonal_density,
    interference,
    primitives,
    quantum_correlation,
    quantum_lattice,
)

__all__ = [
    "bipartite_carrier",
    "bipartite_retraction",
    "born_normalization",
    "chern_simons",
    "contextuality_f2",
    "cptp_channel",
    "diagonal_density",
    "interference",
    "primitives",
    "quantum_correlation",
    "quantum_lattice",
]
