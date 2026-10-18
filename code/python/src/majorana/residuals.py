import math
from dataclasses import field
from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True, slots=True)
class ResidualKernelReport:
    source_id: str
    target_id: str
    actual_value: float
    estimated_value: float
    rke: float
    nrke: float
    actual_zero: bool
    estimated_positive: bool


from enum import Enum


class ResidualFamilyId(str, Enum):
    GTTA_GROUND_STATE_UNLIFTED = "GTTA_GROUND_STATE_UNLIFTED"
    GENERIC_RESIDUAL = "GENERIC_RESIDUAL"


@dataclass
class ResidualFamily:
    family_id: ResidualFamilyId
    description: str = ""


class ResidualRegistry:
    def __init__(self) -> None:
        self._families: Dict[ResidualFamilyId, ResidualFamily] = {}

    def register(self, family: ResidualFamily) -> None:
        if family.family_id in self._families:
            raise ValueError(f"Residual family {family.family_id} already registered")
        self._families[family.family_id] = family



def _require_finite_nonnegative(value: float, name: str) -> float:
    if isinstance(value, bool):
        raise ValueError(f"{name} must be a finite non-negative float, not bool")
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    if value < 0.0:
        raise ValueError(f"{name} must be non-negative")
    return value


def residual_kernel_error(
    actual: Mapping[tuple[str, str], float],
    estimated: Mapping[tuple[str, str], float],
    source_id: str,
    target_id: str,
    epsilon: float = 1e-12,
) -> ResidualKernelReport:
    if not isinstance(source_id, str):
        raise ValueError("source_id must be a string")
    if not source_id:
        raise ValueError("source_id cannot be empty")
    if not isinstance(target_id, str):
        raise ValueError("target_id must be a string")
    if not target_id:
        raise ValueError("target_id cannot be empty")

    epsilon = _require_finite_nonnegative(epsilon, "epsilon")
    if epsilon == 0.0:
        raise ValueError("epsilon must be positive")

    key = (source_id, target_id)

    actual_value = _require_finite_nonnegative(
        actual.get(key, 0.0),
        f"actual[{key!r}]",
    )
    estimated_value = _require_finite_nonnegative(
        estimated.get(key, 0.0),
        f"estimated[{key!r}]",
    )

    rke = abs(actual_value - estimated_value)
    nrke = rke / (actual_value + epsilon)

    return ResidualKernelReport(
        source_id=source_id,
        target_id=target_id,
        actual_value=actual_value,
        estimated_value=estimated_value,
        rke=rke,
        nrke=nrke,
        actual_zero=(actual_value == 0.0),
        estimated_positive=(estimated_value > 0.0),
    )


from dataclasses import dataclass  
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


DEFAULT_EPSILON: Any = None





