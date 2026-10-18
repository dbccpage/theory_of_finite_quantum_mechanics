import math
import numbers
import numpy as np
from typing import List, Tuple, Dict, Any, Union


def _validate_finite_scalars(
    x: Union[np.ndarray, List[float], Dict[Any, float]],
) -> List[float]:
    if isinstance(x, dict):
        items = list(x.values())
    elif isinstance(x, np.ndarray):
        items = x.tolist()
    else:
        items = list(x) if isinstance(x, (list, tuple)) else [x]

    flat = []

    def _flatten(lst):
        for item in lst:
            if isinstance(item, (list, tuple)):
                _flatten(item)
            else:
                flat.append(item)

    _flatten(items)

    for v in flat:
        if isinstance(v, bool) or not isinstance(v, numbers.Real):
            raise TypeError(
                f"l1 input elements must be real scalars, got {type(v).__name__}"
            )
        if not math.isfinite(float(v)):
            raise ValueError(f"l1 input elements must be finite, got {v}")
    return [float(v) for v in flat]


def l1_coboundary_norm(
    edges: List[Tuple[Any, Any]], section: Dict[Any, float]
) -> float:
    """
    Compute Σ_e |s(b) - s(a)| over directed edges (a, b).

    Utility-level: a missing section key raises KeyError by design.
    """
    total = 0.0
    for a, b in edges:
        if a not in section or b not in section:
            raise KeyError(f"Missing section value for edge ({a}, {b})")
        total += abs(float(section[b]) - float(section[a]))
    return total


def l1(x: Union[np.ndarray, List[float], Dict[Any, float]]) -> float:
    """Canonical L1 norm for vectors (or dict-valued coboundaries)."""
    vals = _validate_finite_scalars(x)
    return float(sum(abs(v) for v in vals))


def l1_norm(x: Union[np.ndarray, List[float], Dict[Any, float]]) -> float:
    """Canonical L1 norm alias."""
    return l1(x)


def compute_l1_norm(x: Union[Dict, List[float], np.ndarray]) -> float:
    """Compute L1 norm. Resolves dicts (coboundaries) and arrays."""
    return l1(x)


def l2_norm(x: Union[np.ndarray, List[float], Dict[Any, float]]) -> float:
    """Canonical L2 norm."""
    vals = _validate_finite_scalars(x)
    return float(math.sqrt(sum(v * v for v in vals)))


def l1_l2_comparison(x: Union[np.ndarray, List[float], Dict[Any, float]]) -> Dict[str, Any]:
    """Compare L1 and L2 norms."""
    n1 = l1_norm(x)
    n2 = l2_norm(x)
    vals = _validate_finite_scalars(x)
    dim = len(vals)
    delta = n1 - n2
    delta_max = (math.sqrt(dim) - 1.0) * n2 if dim > 0 else 0.0
    return {
        "dim": dim,
        "norm_l1": n1,
        "norm_l2": n2,
        "delta": delta,
        "delta_max_permitted": delta_max,
        "sharpness_case": "SPARSE" if delta < 1e-9 else ("UNIFORM" if abs(delta - delta_max) < 1e-9 else "INTERMEDIATE"),
    }


