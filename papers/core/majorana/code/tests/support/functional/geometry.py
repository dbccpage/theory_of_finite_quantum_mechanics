import math


def regge_curvature_deficit(valence: float) -> float:
    """
    Deficit epsilon = 2*pi - k * (pi/3)
    Equilibrium: k = 6 => epsilon = 0.
    """
    return 2.0 * math.pi - valence * (math.pi / 3.0)


def cosmological_overshoot_curvature(overshoot_rate: float) -> float:
    """
    Average valence = 6 + overshoot_rate.
    Calculates the average negative Regge curvature.
    """
    avg_valence = 6.0 + overshoot_rate
    return regge_curvature_deficit(avg_valence)

