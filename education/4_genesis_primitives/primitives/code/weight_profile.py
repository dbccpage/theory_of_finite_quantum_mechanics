"""Genesis Primitives Category 17: Weight Profiles, Ray Equivalence & Pre-Measure.

Selected educational models related to 19L57G1 (lean4/Derivation/WeightProfile.lean, CountTransport.lean, code/derivation/weight_profile.py).
Classification: Genesis Foundation Substrate.
AuthorityEffect: None.

Additive valuations over integer carriers, ray equivalence without float division,
scaling invariance, and discrete pre-measure transport.
"""

from __future__ import annotations

from typing import Sequence

Weights = dict[int, int]


def _validate_weights(carrier: Sequence[int], weights: Weights) -> None:
    if (
        any(type(point) is not int or point < 0 for point in carrier)
        or len(set(carrier)) != len(carrier)
        or any(
            type(point) is not int or point not in carrier or type(value) is not int or value < 0
            for point, value in weights.items()
        )
    ):
        raise ValueError("REFUSED_SHAPE: weights require a declared finite natural-number carrier")


def total(carrier: Sequence[int], w: Weights) -> int:
    """Raw sum of weights on the carrier."""
    _validate_weights(carrier, w)
    return sum(w.get(p, 0) for p in carrier)


def same_profile(carrier: Sequence[int], w: Weights, v: Weights) -> bool:
    """Decides whether w and v represent the same projective weight profile.
    Computed via exact cross-multiplication over integers:
        w(p) * total(v) == v(p) * total(w)
    Strictly avoids floating-point division.
    """
    tw, tv = total(carrier, w), total(carrier, v)
    if tw <= 0 or tv <= 0:
        return False
    return all(w.get(p, 0) * tv == v.get(p, 0) * tw for p in carrier)


def same_ray(carrier: Sequence[int], w: Weights, v: Weights, max_scale: int = 100) -> bool:
    """Exact finite nonnegative integer ray equality.

    Positive total masses provide integer scaling witnesses directly. Both zero
    rays agree. The historical max_scale argument is validated for compatibility
    but no longer truncates the mathematical existence question.
    """
    if type(max_scale) is not int or max_scale < 1:
        raise ValueError("REFUSED_SHAPE: legacy scale bound must be a positive integer")
    tw, tv = total(carrier, w), total(carrier, v)
    if tw == 0 or tv == 0:
        return tw == tv
    return all(tv * w.get(point, 0) == tw * v.get(point, 0) for point in carrier)


def transport_weights(mapping: dict[int, int], w: Weights) -> Weights:
    """Transports weights along a relabeling/morphism map."""
    _validate_weights(tuple(w), w)
    if any(
        type(source) is not int or type(target) is not int or source < 0 or target < 0
        for source, target in mapping.items()
    ):
        raise ValueError("REFUSED_SHAPE: weight transport needs exact natural-number indices")
    out: Weights = {}
    for src, val in w.items():
        dst = mapping.get(src, src)
        out[dst] = out.get(dst, 0) + val
    return out
