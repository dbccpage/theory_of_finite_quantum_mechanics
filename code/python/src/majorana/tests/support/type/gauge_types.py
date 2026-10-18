from pydantic import ConfigDict
"""Data structures for matrix group sampling experiments and constraint checks.

These types are plain metadata containers. They perform NO validation, NO
derivation, and NO enforcement of the mathematical or physical properties they
describe: they only store the parameters and boolean outcomes recorded by
external probes. Nothing here carries authority or a verified guarantee.
"""

from pydantic.dataclasses import dataclass
from typing import List, Tuple, Callable, Optional
import numpy as np


@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class MatrixGroupSpec:
    """Metadata container for a matrix group experiment.

    This records the parameters and sampling method used for numerical probes.
    """

    name: str
    dim: int
    rank: int
    factors: List[Tuple[str, int]]

    # sample_fn should return an (rep_dim x rep_dim) numpy array
    sample_fn: Callable[[], np.ndarray]
    is_product: bool
    rep_dim: int

    def __post_init__(self):
        assert self.dim > 0, "Dimension must be positive"
        assert self.rep_dim > 0, "Representation dimension must be positive"
        assert self.rank >= 0, "Rank cannot be negative"


@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class L1LocalizationResult:
    """Stores summary statistics from a group-sampling algorithm."""

    group_name: str
    graph_size: int
    min_cost: float
    mean_cost: float
    std_cost: float
    zero_fraction: float
    n_samples: int

    # List of sampled matrices achieving min_cost
    best_config: Optional[List[np.ndarray]] = None


@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class ConstraintCheckResult:
    """Metadata container for specific constraint evaluations.

    Note: These flags store the boolean result of mathematical checks
    and do not carry physically derived anomaly-cancellation guarantees.
    """

    group_name: str
    gravitational_ok: bool
    cubic_ok: bool
    witten_ok: bool
    all_ok: bool
    details: str


# Legacy aliases for backward compatibility with active pipelines
GaugeGroupSpec = MatrixGroupSpec

# Metadata-only alias: stores boolean outcomes of constraint checks; it is NOT
# a verified anomaly-cancellation result (no derivation or enforcement).
AnomalyCancellationMetadata = ConstraintCheckResult

# Backward-compatible alias. Despite the name, this is metadata only (the same
# ConstraintCheckResult container) and does NOT constitute a verified
# anomaly-cancellation result.
AnomalyCancellationResult = ConstraintCheckResult


