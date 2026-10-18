"""Bounded cycle-correction action candidates."""

from omega_engine.crates.type.cycle_aware import CorrectionStrategy


def apply_correction(omega: list, harmonic: list, target_edges: list, strategy) -> list:
    if not CorrectionStrategy.is_valid(strategy):
        return list(omega)
    corrected = list(omega)
    for index in target_edges:
        if index >= len(corrected) or index >= len(harmonic):
            continue
        if strategy == CorrectionStrategy.HarmonicSnap:
            corrected[index] = harmonic[index]
        elif isinstance(strategy, dict) and strategy.get("type") == "GradientStep":
            alpha = strategy.get("alpha")
            corrected[index] = omega[index] + alpha * (harmonic[index] - omega[index])
    return corrected


__all__ = ["apply_correction"]
