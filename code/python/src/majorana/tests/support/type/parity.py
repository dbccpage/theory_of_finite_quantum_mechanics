from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, List


class ProdBindingStatus(str, Enum):
    """Declared relationship between a Python PROTO symbol and its PROD home."""

    PROTO_ONLY = "PROTO_ONLY"
    STRUCTURAL_MIRROR = "STRUCTURAL_MIRROR"
    FORMULA_MIRROR = "FORMULA_MIRROR"
    FFI_BOUND = "FFI_BOUND"


@dataclass(frozen=True)
class SymbolHome:
    """Static registry entry describing the PROTO/PROD relationship for one symbol."""

    symbol: str
    proto_path: str
    prod_crate: str
    prod_path: str
    prod_status: ProdBindingStatus
    notes: str = ""


@dataclass
class ParityReceipt:
    """Result of one parity comparison. AuthorityEffect remains None."""

    symbol: str
    proto_value: Any
    prod_value: Any
    parity_residual: float
    prod_status: ProdBindingStatus
    math_path: List[str] = field(default_factory=list)
    authority_effect: str = "None"
    ffi_bound: bool = False
