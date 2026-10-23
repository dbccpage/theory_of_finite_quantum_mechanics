"""
Integration tests for 006_vector_and_quantum_observer_geometries.
Paper: GS-003 (006_vector_and_quantum_observer_geometries)
AuthorityEffect: None.
"""

import sys
from pathlib import Path

code_dir = Path(__file__).resolve().parent.parent
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from mod_006_vector_and_quantum_observer_geometries_core import PaperEvaluator


def test_package_evaluator_passes() -> None:
    evaluator = PaperEvaluator()
    res = evaluator.evaluate()
    assert res["paper_id"] == "006_vector_and_quantum_observer_geometries"
    assert res["status"] == "EVALUATED_PASS"
    assert res["authority"] == "None"
    assert "demonstrations" in res
    assert "demo_1_classical_triangle" in res["demonstrations"]
    assert "demo_2_quantum_triangle" in res["demonstrations"]
    assert "demo_3_bloch_vs_qutrit" in res["demonstrations"]
    assert "demo_4_cptp_monotonicity" in res["demonstrations"]


def test_generate_figures_run() -> None:
    from generate_figures import generate_figure

    generate_figure()
    export_dir = Path(__file__).resolve().parents[2] / "public_export"
    assert (
        export_dir / "fig1_006_vector_and_quantum_observer_geometries_readout.png"
    ).exists()
