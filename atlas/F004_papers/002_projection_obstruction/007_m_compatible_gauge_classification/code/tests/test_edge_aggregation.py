"""T13-T19: Presheaf edge diagram, path coherence, and P1 edgewise aggregation tests for GS-001.

Verifies isometric edge diagrams, path coherence on poset diamonds, and weighted l1 aggregation.
"""

import sys
from pathlib import Path
import numpy as np
import pytest

_pkg = Path(__file__).resolve().parents[1]
if str(_pkg / "code") not in sys.path:
    sys.path.insert(0, str(_pkg / "code"))

from norms import l1, l2
from diagrams import EdgeDiagram, path_coherence_holds, evaluate_p1_edgewise_sum


def test_t13_t16_edge_diagram_and_path_coherence():
    """T13-T16: Test EdgeDiagram construction and presheaf path coherence F(a <= c) = F(b <= c) o F(a <= b)."""
    edges = ((0, 1), (1, 2))
    weights = (1.5, 2.5)
    gauges = (l1, l2)

    diagram = EdgeDiagram(edges, weights, gauges)
    assert len(diagram.edges) == 2

    # Path coherence on poset diamond
    f_ab = np.array([[1.0, 0.0], [0.0, 1.0]])
    f_bc = np.array([[2.0, 0.0], [0.0, 3.0]])
    f_ac = np.array([[2.0, 0.0], [0.0, 3.0]])  # f_bc @ f_ab

    assert path_coherence_holds(f_ab, f_bc, f_ac)

    # Incoherent composition
    f_ac_bad = np.array([[1.0, 0.0], [0.0, 1.0]])
    assert not path_coherence_holds(f_ab, f_bc, f_ac_bad)


def test_t17_t19_p1_edgewise_sum_evaluation():
    """T17-T19: Test P1 edgewise weighted l1 sum diagnostic evaluation D(s) = sum_e w_e nu_e(delta_e s)."""
    edges = ((0, 1), (1, 2))
    weights = (1.0, 2.0)
    gauges = (l1, l1)
    diagram = EdgeDiagram(edges, weights, gauges)

    cochain_components = [np.array([3.0, -4.0]), np.array([1.0, 1.0])]
    # e0: 1.0 * l1([3, -4]) = 1.0 * 7 = 7.0
    # e1: 2.0 * l1([1, 1]) = 2.0 * 2 = 4.0
    # Total = 11.0
    val = evaluate_p1_edgewise_sum(diagram, cochain_components)
    assert np.isclose(val, 11.0)

    # Error conditions
    with pytest.raises(ValueError, match="Cochain components count mismatch"):
        evaluate_p1_edgewise_sum(diagram, [np.array([1.0])])

    with pytest.raises(ValueError, match="Edge count mismatch"):
        EdgeDiagram(edges, (1.0,), gauges)
