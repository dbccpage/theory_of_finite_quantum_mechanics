"""Create the paper walkthrough. Execution is separate and checked."""

from pathlib import Path

import nbformat as nbf


def build(path: Path) -> None:
    notebook = nbf.v4.new_notebook()
    cells = [
        nbf.v4.new_markdown_cell(
            "# CODA: an exact finite walkthrough\n\n"
            "Companion to `coda.md` version 2.0.0. The calculations illustrate "
            "stated finite instances. General analytic statements and the open "
            "faithful-functor target keep their separate ledger status. "
            "AuthorityEffect: None."
        ),
        nbf.v4.new_code_cell(
            "from pathlib import Path\nimport sys\n"
            "from fractions import Fraction\nfrom itertools import product\n"
            "candidates = (Path.cwd(), Path.cwd().parent)\n"
            "root = next(p for p in candidates if (p / 'coda.md').is_file())\n"
            "sys.path.insert(0, str(root / 'code'))\n"
            "from coda_core import (Collision, factor_or_collision, evaluate_menu,\n"
            "    coordinate_packet, verify_coordinate_certificate, parity_sections,\n"
            "    affine_quadrature, sample_collision, standing)\n"
            "from audit_legacy_embedding import audit\nprint('Exact arithmetic ready')"
        ),
        nbf.v4.new_markdown_cell(
            "## 1. A query that descends, and one that does not\n\n"
            "On the four states `(u,v)`, displaying `u` recovers `2*u` but loses `v`. "
            "The routine returns an actual collision rather than a confidence score "
            "(CODA-02, CODA-03)."
        ),
        nbf.v4.new_code_cell(
            "states = tuple(product((0, 1), repeat=2))\n"
            "good = factor_or_collision(states, lambda x: x[0], lambda x: 2*x[0])\n"
            "bad = factor_or_collision(states, lambda x: x[0], lambda x: x[1])\n"
            "assert good == {0: 0, 1: 2}\nassert isinstance(bad, Collision)\n"
            "print('Image factor:', good)\nprint('Collision:', bad)"
        ),
        nbf.v4.new_markdown_cell(
            "## 2. A timeout is not exhaustion\n\n"
            "An unchecked successful repair defeats a negative conclusion. Full "
            "enumeration retains both equal-cost repairs (CODA-04)."
        ),
        nbf.v4.new_code_cell(
            "partial = evaluate_menu({'r0': 0, 'r1': 1}, lambda r: r == 'r1', 1)\n"
            "full = evaluate_menu({'r0': 0, 'r1': 1}, lambda r: r == 'r1')\n"
            "ties = evaluate_menu({'left': 1, 'right': 1}, lambda r: True)\n"
            "assert partial.status == 'BudgetUnknown' and partial.minima == ()\n"
            "assert full.repairs == ('r1',) and ties.minima == ('left', 'right')\n"
            "print(partial)\nprint(full)\nprint(ties)"
        ),
        nbf.v4.new_markdown_cell(
            "## 3. Three FOC outcomes, with checked dual bounds\n\n"
            "For `d0(t)=(t,0,0)` and `d1(a,b,c)=c`, the optimal repair is `-a`. "
            "The residual and its scalar diagnostics are different objects "
            "(CODA-05, CODA-06)."
        ),
        nbf.v4.new_code_cell(
            "for state in ((2, 0, 0), (2, 3, 0), (2, 3, 5)):\n"
            "    certificate = coordinate_packet(state)\n"
            "    assert verify_coordinate_certificate(certificate)\n"
            "    print(state, certificate.grade, 'phi =', certificate.phi, 'gamma =', certificate.gamma)"
        ),
        nbf.v4.new_markdown_cell(
            "## 4. Local solvability without a global section\n\n"
            "Each of three parity constraints can be solved alone. The first two "
            "require equality; the third requires inequality. No common assignment "
            "exists. This does not start with a compatible sheaf matching family "
            "(CODA-08)."
        ),
        nbf.v4.new_code_cell(
            "edges = ((0, 1, 0), (1, 2, 0), (2, 0, 1))\n"
            "local_counts = [len(parity_sections(3, [e])) for e in edges]\n"
            "global_sections = parity_sections(3, edges)\n"
            "assert local_counts == [4, 4, 4] and global_sections == ()\n"
            "print('Local section counts:', local_counts)\nprint('Global sections:', global_sections)"
        ),
        nbf.v4.new_markdown_cell(
            "## 5. An affine integral and a finite-sample collision\n\n"
            "The affine model gives exact sums. Arbitrary continuous functions "
            "need not share its integral: the squared polynomial perturbation in "
            "§6 vanishes at all three samples and adds exactly `1/84` to the area "
            "(CODA-09, CODA-10)."
        ),
        nbf.v4.new_code_cell(
            "values = affine_quadrature(10)\n"
            "collision = sample_collision()\n"
            "assert values['left'] == 45 and values['right'] == 55 and values['trapezoid'] == 50\n"
            "assert collision['perturbation_at_nodes'] == (0, 0, 0)\n"
            "assert collision['area_difference'] == Fraction(1, 84)\n"
            "print({k: str(v) for k, v in values.items()})\n"
            "print('Same samples, integrals:', collision['base_integral'], collision['perturbed_integral'])"
        ),
        nbf.v4.new_markdown_cell(
            "## 6. Evidence and a faithful-looking label\n\n"
            "The declared evidence/grant conjunction does not supply a missing "
            "grant. The inherited embedding's positive checker also does not "
            "supply injectivity: execute the actual historical code and compare "
            "the span data (CODA-11, CODA-12)."
        ),
        nbf.v4.new_code_cell(
            "assert standing(True, False) is False\n"
            "legacy = audit()\n"
            "assert legacy['distinct_arrows'] and legacy['identical_span_data']\n"
            "assert legacy['legacy_checker_reports_faithful']\n"
            "print('Evidence without grant:', standing(True, False))\n"
            "print(legacy['verdict'])\nprint('General target:', legacy['target_status'])"
        ),
        nbf.v4.new_markdown_cell(
            "## 7. Figures and evidence map\n\n"
            "The figures below are generated by `code/generate_figures.py` from "
            "the exact values above. Plotting uses floating-point screen coordinates. "
            "The manuscript proofs and `coda_claim_ledger.md` state the wider scope."
        ),
        nbf.v4.new_code_cell(
            "from IPython.display import Image, display\n"
            "for name in ('coda_foc_outcomes.png', 'coda_quadrature.png'):\n"
            "    display(Image(filename=str(root / 'images' / name)))"
        ),
    ]
    for index, cell in enumerate(cells):
        cell.id = f"coda-{index:02d}"
    notebook.cells = cells
    notebook.metadata.kernelspec = {
        "name": "python3",
        "language": "python",
        "display_name": "Python 3",
    }
    notebook.metadata.language_info = {"name": "python", "version": "3.12"}
    path.parent.mkdir(parents=True, exist_ok=True)
    nbf.write(notebook, path)


if __name__ == "__main__":
    build(
        Path(__file__).resolve().parents[1]
        / "jupyter_notebooks/01_coda_walkthrough.ipynb"
    )
