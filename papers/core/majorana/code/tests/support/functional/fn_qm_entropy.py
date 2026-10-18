"""Entropy observables.

Faithful port of ``crates/omega_engine.crates.engine/src/quantum/entropy.rs``.

All `_lossy_normalized` / `_lossy` variants silently renormalize and skip
invalid entries; the `_checked` variants fail closed by raising
:class:`EntropyError`.
"""

from __future__ import annotations
import math

EPSILON = 2.220446049250313e-16  


class EntropyError(Exception):
    pass


class LossyEntropyAuthorityPathRefusal(EntropyError):
    def __init__(self, msg="LOSSY_ENTROPY_AUTHORITY_PATH_REFUSED"):
        super().__init__(msg)
        self.refusal_route = "LOSSY_ENTROPY_AUTHORITY_PATH_REFUSED"


def assert_admitted_entropy_path(lossy: bool, authority_admitted: bool = False):
    if lossy and authority_admitted:
        raise LossyEntropyAuthorityPathRefusal()


class EmptyDistribution(EntropyError):
    pass


class NonFiniteProbability(EntropyError):
    def __init__(self, index):
        super().__init__(f"non-finite probability at index {index}")
        self.index = index


class NegativeProbability(EntropyError):
    def __init__(self, index, value):
        super().__init__(f"negative probability at index {index}: {value}")
        self.index = index
        self.value = value


class ProbabilitySumNotOne(EntropyError):
    def __init__(self, sum_value):
        super().__init__(f"probability sum not one: {sum_value}")
        self.sum = sum_value


class InsufficientHistory(EntropyError):
    pass


class InvalidWindow(EntropyError):
    pass


class InvalidTolerance(EntropyError):
    pass


def shannon_lossy_normalized(probabilities) -> float:
    total = sum(p for p in probabilities if math.isfinite(p) and p > 0.0)
    if total <= EPSILON or not math.isfinite(total):
        return 0.0
    acc = 0.0
    for p in probabilities:
        if not math.isfinite(p) or p <= 0.0:
            continue
        q = p / total
        acc += -q * math.log(q)
    return acc


def shannon(probabilities) -> float:
    return shannon_lossy_normalized(probabilities)


def shannon_checked(probabilities) -> float:
    if not probabilities:
        raise EmptyDistribution("empty distribution")

    total = 0.0
    for i, p in enumerate(probabilities):
        if not math.isfinite(p):
            raise NonFiniteProbability(i)
        if p < 0.0:
            raise NegativeProbability(i, p)
        total += p

    if abs(total - 1.0) > 1e-10:
        raise ProbabilitySumNotOne(total)

    return sum(-p * math.log(p) for p in probabilities if p > 0.0)


def magnitude_entropy_lossy(weights) -> float:
    total = sum(abs(w) for w in weights if math.isfinite(w))
    if total <= EPSILON or not math.isfinite(total):
        return 0.0
    acc = 0.0
    for w in weights:
        if math.isfinite(w) and abs(w) > 0.0:
            p = abs(w) / total
            acc += -p * math.log(p)
    return acc


def magnitude_entropy(weights) -> float:
    return magnitude_entropy_lossy(weights)


def entropy_change_rate(history) -> float:
    if len(history) < 2:
        return 0.0
    a = history[-2]
    b = history[-1]
    if not math.isfinite(a) or not math.isfinite(b):
        return math.nan
    return b - a


def is_converging(history, tolerance: float, window: int) -> bool:
    if not math.isfinite(tolerance) or tolerance < 0.0 or window == 0:
        return False
    if any(not math.isfinite(x) for x in history):
        return False
    if len(history) < 2:
        return False
    w = min(window, len(history) - 1)
    tail = history[len(history) - w - 1 :]
    return all(abs(tail[i + 1] - tail[i]) <= tolerance for i in range(len(tail) - 1))


def is_converging_checked(history, tolerance: float, window: int) -> bool:
    if not math.isfinite(tolerance) or tolerance < 0.0:
        raise InvalidTolerance(f"invalid tolerance: {tolerance}")
    if window == 0:
        raise InvalidWindow(f"invalid window size: {window}")
    if len(history) < 2:
        raise InsufficientHistory("insufficient history for convergence check")
    for index, x in enumerate(history):
        if not math.isfinite(x):
            raise NonFiniteProbability(index)
    w = min(window, len(history) - 1)
    tail = history[len(history) - w - 1 :]
    return all(abs(tail[i + 1] - tail[i]) <= tolerance for i in range(len(tail) - 1))



