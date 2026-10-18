"""SP4a: SM/SUSY Proximity Census via Exhaustive Feature Distance Search.

Exhaustive search over 10^3 = 1000 finite group triples from a 10-element menu.
Minimum L1 distance to SM extra vector is 3, achieved by (D4, Z3, 1) and (Q8, Z3, 1).
Simplex shadow (Z3, Z2, 1) has distance 11.

AuthorityEffect: None.
"""

from __future__ import annotations

import sys
import os
import numpy as np

# Re-export from the pre-existing stdlib l1_sm_susy_proximity module for full parity
sys.path.insert(0, os.path.dirname(__file__))
import l1_sm_susy_proximity as l1_prox

GROUP_MENU = [(g.name, g.order, g.abelian) for g in l1_prox.FINITE_MENU]
SM_TARGET = np.array(l1_prox.SM_GAUGE_EXTRAS, dtype=float)


def feature_vector(g2_name: str, g1_name: str, g0_name: str) -> np.ndarray:
    g2 = l1_prox.group_by_name(g2_name)
    g1 = l1_prox.group_by_name(g1_name)
    g0 = l1_prox.group_by_name(g0_name)
    return np.array(l1_prox.features(g2, g1, g0, lie_extra=0), dtype=float)


def exhaustive_census() -> dict:
    """Search all 1000 triples for minimum L1 distance to SM target."""
    m, winners = l1_prox.min_sm_distance()
    g2_s, g1_s, g0_s = l1_prox.simplex_shadow()
    shadow_dist = l1_prox.sm_distance(l1_prox.features(g2_s, g1_s, g0_s))

    all_distances = {}
    rows = l1_prox.discrete_321_census()
    for a, b, c, d in rows:
        all_distances[(a, b, c)] = float(d)

    return {
        "min_distance": float(m),
        "min_triples": winners,
        "n_triples_searched": len(rows),
        "shadow_triple": (g2_s.name, g1_s.name, g0_s.name),
        "shadow_distance": float(shadow_dist),
        "all_distances": all_distances,
    }
