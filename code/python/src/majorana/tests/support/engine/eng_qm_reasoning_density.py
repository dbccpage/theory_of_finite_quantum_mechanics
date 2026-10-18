"""Experimental density diagnostics for information-system reasoning traces.

Faithful port of ``crates/omega_engine.crates.engine/src/quantum/reasoning_density.rs``.
"""

from __future__ import annotations
import math
from typing import List, Optional

CONTRACT_ID = "urn:omega:qm:reasoning_density_engine:file:v1.0.0"
AUTHORITY_EFFECT = "None"

from omega_engine.crates.linear_algebra_theory.density import (
    DensityMatrixConfig,
    DimensionMismatch,
    InvalidTopK,
    NegativeWeight,
    NonFiniteEntry,
    NoValidStates,
    NumericalDensityMatrix,
    WeightSumNotOne,
    ZeroDimension,
    ZeroVector,
    NonPhysical,
    InvalidWindow,
)
from omega_engine.crates.type.qm_engine import (
    DensityConstruction,
    DensityTrajectory,
    ReasoningDensityConfig,
    ReasoningDensityReport,
)


def sequence_ensemble_density(
    rows: List[List[float]],
    weights: Optional[List[float]],
    config: ReasoningDensityConfig,
    density_config: DensityMatrixConfig,
) -> tuple[NumericalDensityMatrix, ReasoningDensityReport]:
    dim = validate_rows(rows)
    norm_weights = normalized_weights(weights, len(rows), density_config)
    return sequence_ensemble_density_impl(
        rows, dim, norm_weights, config, density_config
    )


def sequence_ensemble_density_impl(
    rows: List[List[float]],
    dim: int,
    weights: List[float],
    config: ReasoningDensityConfig,
    density_config: DensityMatrixConfig,
) -> tuple[NumericalDensityMatrix, ReasoningDensityReport]:
    components = []
    for row, weight in zip(rows, weights):
        psi = row_to_softmax_amplitudes(row, dim, config.top_k, density_config)
        density = NumericalDensityMatrix.from_amplitudes(psi, density_config)
        components.append((density, weight))

    density = NumericalDensityMatrix.try_mixture(components, density_config)
    report = report_for(
        density,
        DensityConstruction.SequenceMixture,
        len(rows),
        config.top_k,
    )
    return density, report


def window_density_trajectory(
    rows: List[List[float]],
    window_size: int,
    stride: int,
    config: ReasoningDensityConfig,
    density_config: DensityMatrixConfig,
) -> DensityTrajectory:
    dim = validate_rows(rows)
    if window_size == 0:
        raise InvalidWindow("window size must be positive")
    if stride == 0:
        raise InvalidWindow("stride must be positive")
    if window_size > len(rows):
        raise NoValidStates("window size is larger than rows count")

    source_timestamps = None
    if config.timestamps is not None:
        validate_timestamps(config.timestamps, len(rows))
        source_timestamps = config.timestamps

    states = []
    timestamps = []
    reports = []
    start = 0
    window_index = 0
    window_weights = [1.0 / window_size] * window_size

    while start + window_size <= len(rows):
        density, report = sequence_ensemble_density_impl(
            rows[start : start + window_size],
            dim,
            window_weights,
            config,
            density_config,
        )
        report.construction = DensityConstruction.WindowedTrajectory
        report.source_count = window_size

        states.append(density)
        ts = (
            source_timestamps[start]
            if source_timestamps is not None
            else float(window_index)
        )
        timestamps.append(ts)
        reports.append(report)

        start += stride
        window_index += 1

    return DensityTrajectory(states=states, timestamps=timestamps, reports=reports)


def report_for(
    density: NumericalDensityMatrix,
    construction: "DensityConstruction",
    source_count: int,
    top_k: Optional[int],
) -> ReasoningDensityReport:
    try:
        entropy = density.von_neumann_entropy()
    except Exception as e:
        raise NonPhysical(f"Failed to compute entropy: {e}") from e

    return ReasoningDensityReport(
        construction=construction,
        source_count=source_count,
        dim=density.dim(),
        entropy=entropy,
        purity=density.purity(),
        l1_coherence=density.l1_coherence(),
        top_k=top_k,
    )


def validate_rows(rows: List[List[float]]) -> int:
    if not rows:
        raise NoValidStates("rows list is empty")
    first = rows[0]
    if not first:
        raise ZeroDimension("row dimension must be positive")
    dim = len(first)

    for row_index, row in enumerate(rows):
        if not row:
            raise ZeroDimension("row dimension must be positive")
        if len(row) != dim:
            raise DimensionMismatch(
                f"Dimension mismatch: expected {dim}, actual {len(row)} at row {row_index}"
            )
        for col_index, value in enumerate(row):
            if not math.isfinite(value):
                raise NonFiniteEntry(
                    f"Non-finite entry at row {row_index}, col {col_index}"
                )

    return dim


def validate_timestamps(timestamps: List[float], expected: int) -> None:
    if len(timestamps) != expected:
        raise DimensionMismatch(
            f"Timestamps count mismatch: expected {expected}, actual {len(timestamps)}"
        )
    for index, value in enumerate(timestamps):
        if not math.isfinite(value):
            raise NonFiniteEntry(f"Non-finite timestamp at index {index}")


def normalized_weights(
    weights: Optional[List[float]],
    count: int,
    density_config: DensityMatrixConfig,
) -> List[float]:
    if count == 0:
        raise NoValidStates("no valid states")

    if weights is None:
        return [1.0 / count] * count

    if len(weights) != count:
        raise DimensionMismatch(
            f"Weights count mismatch: expected {count}, actual {len(weights)}"
        )

    for index, weight in enumerate(weights):
        if not math.isfinite(weight):
            raise NonFiniteEntry(f"Non-finite weight at index {index}")
        if weight < 0.0:
            raise NegativeWeight(f"Negative weight at index {index}: {weight}")

    sum_w = sum(weights)
    if sum_w <= density_config.zero_norm_tol():
        raise WeightSumNotOne(f"Weight sum too small: sum={sum_w}")

    return [w / sum_w for w in weights]


def row_to_softmax_amplitudes(
    row: List[float],
    dim: int,
    top_k: Optional[int],
    density_config: DensityMatrixConfig,
) -> List[complex]:
    selected = selected_indices(row, dim, top_k)
    max_value = max(row[idx] for idx in selected)

    exps = []
    exp_sum = 0.0
    for idx in selected:
        val = math.exp(row[idx] - max_value)
        if not math.isfinite(val):
            raise NonPhysical("non-physical softmax exponentiation result")
        exp_sum += val
        exps.append((idx, val))

    if exp_sum <= density_config.zero_norm_tol() or not math.isfinite(exp_sum):
        raise ZeroVector("softmax sum is zero or non-finite")

    psi = [complex(0.0, 0.0)] * dim
    for idx, val in exps:
        psi[idx] = complex(math.sqrt(val / exp_sum), 0.0)

    return psi


def selected_indices(
    row: List[float],
    dim: int,
    top_k: Optional[int],
) -> List[int]:
    if top_k is None:
        return list(range(dim))
    if top_k == 0:
        raise InvalidTopK("invalid top_k: 0")
    if top_k >= dim:
        return list(range(dim))

    indices = list(range(dim))
    indices.sort(key=lambda idx: (-row[idx], idx))
    return indices[:top_k]


from omega_engine.crates.engine.base.eng_base import Engine


class ReasoningDensityEngine(Engine):
    authority_effect = "None"
    implements = (CONTRACT_ID,)





