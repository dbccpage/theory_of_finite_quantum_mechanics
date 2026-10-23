"""DDC letter D: descent to a coarser carrier with an exact loss ledger.

``pi: Q^(n+k) -> Q^n`` keeps the first ``n`` coordinates. The loss vector is
``x - iota(pi(x))`` (the dropped tail) and the loss scalar is its l1 norm, so
the loss is zero exactly when ``x`` already lies in ``iota(Q^n)``. A D step
without a loss ledger is refused on the tape as ``REFUSED_MISSING_LOSS_LEDGER``
(Law 6); ``ledger_entry`` is the ledger this module books.

Leaf module: standard library only, loadable by path. AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Dict, List, Tuple


def _exact(value: object) -> Fraction:
    if isinstance(value, (bool, float)) or not isinstance(value, (int, Fraction)):
        raise ValueError(f"NOT_EXACT: {value!r}")
    return Fraction(value)


@dataclass(frozen=True)
class DescentReceipt:
    operation: str
    paper_id: str
    source_dim: int
    target_dim: int
    coarse_vector: Tuple[Fraction, ...]
    loss_vector: Tuple[Fraction, ...]
    loss_scalar: Fraction
    is_lossless: bool
    status: str
    authority_effect: str = "None"

    def __post_init__(self) -> None:
        coarse = tuple(_exact(x) for x in self.coarse_vector)
        loss = tuple(_exact(x) for x in self.loss_vector)
        scalar = _exact(self.loss_scalar)
        if (type(self.source_dim) is not int or type(self.target_dim) is not int
                or self.target_dim < 0 or self.source_dim < self.target_dim
                or len(coarse) != self.target_dim or len(loss) != self.source_dim - self.target_dim
                or scalar != sum((abs(x) for x in loss), Fraction(0))
                or type(self.is_lossless) is not bool or self.is_lossless != (scalar == 0)
                or self.status != ("LOSSLESS_DESCENT" if scalar == 0 else "DESCENT_WITH_LOSS")):
            raise ValueError("INVALID_LOSS_LEDGER")
        object.__setattr__(self, "coarse_vector", coarse)
        object.__setattr__(self, "loss_vector", loss)
        object.__setattr__(self, "loss_scalar", scalar)


class DescentProjector:
    """Exact projector lowering carrier dimension with explicit loss accounting."""

    def __init__(self, target_dim: int):
        if type(target_dim) is not int:
            raise ValueError(f"target_dim must be an int, not {type(target_dim).__name__}")
        if target_dim < 0:
            raise ValueError(f"NEGATIVE_TARGET_DIMENSION: {target_dim}")
        self.target_dim = target_dim

    def descend(self, vector: List[Fraction]) -> DescentReceipt:
        """Project to ``target_dim`` coordinates and book the exact loss."""
        vector = [_exact(value) for value in vector]
        if len(vector) < self.target_dim:
            raise ValueError(f"Vector dimension {len(vector)} less than target dimension {self.target_dim}")
        coarse = tuple(vector[: self.target_dim])
        loss_tail = tuple(vector[self.target_dim :])
        loss_scalar = sum((abs(x) for x in loss_tail), Fraction(0))
        is_lossless = loss_scalar == 0
        return DescentReceipt(
            operation="D",
            paper_id="DDC-D",
            source_dim=len(vector),
            target_dim=self.target_dim,
            coarse_vector=coarse,
            loss_vector=loss_tail,
            loss_scalar=loss_scalar,
            is_lossless=is_lossless,
            status="LOSSLESS_DESCENT" if is_lossless else "DESCENT_WITH_LOSS",
        )


def ledger_entry(receipt: DescentReceipt) -> Dict[str, object]:
    """The loss-ledger entry a D step must carry."""
    return {
        "source_dim": receipt.source_dim,
        "target_dim": receipt.target_dim,
        "loss_vector": list(receipt.loss_vector),
        "loss_scalar": receipt.loss_scalar,
        "is_lossless": receipt.is_lossless,
    }
