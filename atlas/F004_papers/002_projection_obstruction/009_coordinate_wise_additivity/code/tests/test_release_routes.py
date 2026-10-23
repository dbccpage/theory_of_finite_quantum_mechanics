"""Check that reader-facing routes resolve to the reviewed package artifacts."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_canonical_reader_targets_exist() -> None:
    targets = (
        "coordinate_wise_additivity.md",
        "coordinate_wise_additivity.pdf",
        "coordinate_wise_additivity.tex",
        "coordinate_wise_additivity_claim_ledger.md",
        "docs/quick_start.md",
        "lean4/gs003_core.lean",
        "lean4/gs003_coordinate_l1.lean",
        "jupyter_notebooks/reviewer_coordinate_additivity.ipynb",
        "jupyter_notebooks/refutation_sandbox.ipynb",
    )
    missing = [target for target in targets if not (ROOT / target).is_file()]
    assert not missing


def test_launchers_use_exact_notebook_routes() -> None:
    expectations = {
        "public_export/run_notebook.bat": (
            "jupyter_notebooks\\reviewer_coordinate_additivity.ipynb",
            ("001_reviewer_", "002_refutation_"),
        ),
        "public_export/run_notebook.sh": (
            "jupyter_notebooks/reviewer_coordinate_additivity.ipynb",
            ("001_reviewer_", "002_refutation_"),
        ),
        "public_export/run_refutation.bat": (
            "jupyter_notebooks\\refutation_sandbox.ipynb",
            ("001_reviewer_", "002_refutation_"),
        ),
        "public_export/run_refutation.sh": (
            "jupyter_notebooks/refutation_sandbox.ipynb",
            ("001_reviewer_", "002_refutation_"),
        ),
    }
    for relative, (target, stale_routes) in expectations.items():
        text = (ROOT / relative).read_text(encoding="utf-8")
        assert target in text
        assert all(stale not in text for stale in stale_routes)


def test_active_reader_docs_do_not_use_obsolete_routes() -> None:
    active_docs = (
        "README.md",
        "docs/quick_start.md",
        "docs/lean_claim_map.md",
        "docs/references.md",
        "code/README.md",
        "coordinate_wise_additivity.md",
        "coordinate_wise_additivity_claim_ledger.md",
    )
    obsolete = (
        "jupyter_notebooks/001_reviewer_coordinate_additivity.ipynb",
        "jupyter_notebooks/002_refutation_sandbox.ipynb",
        "000_gs003_core.lean",
        "000_gs003_coordinate_l1.lean",
        "docs/000_quick_start.md",
        "docs/GS000_ZENODO_METADATA.json",
        "lean4/research_programs/004_projection_obstruction/009_coordinate_wise_additivity/",
        "[index:index:CoordinateL1.lean]",
    )
    for relative in active_docs:
        text = (ROOT / relative).read_text(encoding="utf-8")
        assert all(stale not in text for stale in obsolete), relative
