"""
test_generate_figures.py: Tests figure generation for CODA-CS-Q.
"""

from pathlib import Path

from generate_figures import generate_bridge_architecture_figure


def test_figure_generation(tmp_path) -> None:
    generate_bridge_architecture_figure()
    fig_path = Path(__file__).resolve().parent.parent.parent / "public_export" / "fig1_authority_descent.png"
    assert fig_path.is_file()
    assert fig_path.stat().st_size > 0
