"""Functional Observers."""

from __future__ import annotations
from dataclasses import dataclass
import numpy as np


@dataclass
class Observer:
    name: str
    projection_matrix: np.ndarray

    def observe(self, state: np.ndarray) -> np.ndarray:
        return np.dot(self.projection_matrix, state)


from dataclasses import dataclass  
from enum import Enum  
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


ObserverKind = Enum(
    "ObserverKind",
    {
        "Projection": "Projection",
        "Precision": "Precision",
        "SignEraser": "SignEraser",
        "LineageForget": "LineageForget",
        "BudgetBlind": "BudgetBlind",
        "WitnessBlind": "WitnessBlind",
        "Custom": "Custom",
    },
    type=str,
)
ObserverKind.__doc__ = "Structural mirror of Rust ``ObserverKind`` variants."


@dataclass(init=False)
class ObserverLawWitness(_RustSurfaceObject):
    """Structural mirror of Rust ``ObserverLawWitness``."""

    idempotent_replay_hash: Any = None
    repair_compat_replay_hash: Any = None
    lossy_phi_replay_hash: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = (
            "idempotent_replay_hash",
            "repair_compat_replay_hash",
            "lossy_phi_replay_hash",
        )
        if len(args) > len(names):
            raise TypeError("ObserverLawWitness received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)


@dataclass(init=False)
class VerifiedObserver(_RustSurfaceObject):
    """Structural mirror of Rust ``VerifiedObserver``."""

    observer: Any = None
    witness: Any = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        names = ("observer", "witness")
        if len(args) > len(names):
            raise TypeError("VerifiedObserver received too many positional arguments")
        for fld, value in zip(names, args):
            setattr(self, fld, value)
        for fld in names[len(args) :]:
            setattr(self, fld, kwargs.pop(fld, None))
        for fld, value in kwargs.items():
            setattr(self, fld, value)




