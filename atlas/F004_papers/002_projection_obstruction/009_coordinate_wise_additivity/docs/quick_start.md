# Tier 1 Quick-Start Card: 009_coordinate_wise_additivity

> [!NOTE]
> Tests and notebooks provide finite computational and regression evidence.
> They do not establish the manuscript's global claims or publication authority.
>
## Core Thesis & Closed-Form Results

- **Package:** `009_coordinate_wise_additivity`
- **Title:** Coordinate-Wise Additivity and Local ℓ¹ Gauge Selection (GS-000)
- **Interactive route:** reviewer and refutation notebooks with a locked replay command.

## 1-Line Verification

```bash
uv sync --frozen --extra notebooks --extra dev
uv run --frozen --extra dev python -m pytest code/tests -q -p no:debugging \
  --cov=code --cov-branch --cov-report=term-missing --cov-fail-under=95
uv run --frozen --extra notebooks python scripts/replay_notebooks.py
```

When kernel sockets are unavailable, run the separately labeled direct mode:

```bash
uv run --frozen --extra notebooks python scripts/direct_notebook_replay.py
```

The 2026-10-02 review used direct Python execution. This mode checks plain
cells and assertions, not Jupyter transport or widget interactions. The
default release verifier still requires a fresh Lean build and native
notebook replay; direct mode does not replace those gates.

## Quick Links & Tier 2 Sandbox

- Interactive Reviewer Sandbox: [`public_export/run_notebook.bat`](../public_export/run_notebook.bat)
- Interactive Refutation Sandbox: [`public_export/run_refutation.bat`](../public_export/run_refutation.bat)
- Monograph Paper: [`coordinate_wise_additivity.md`](../coordinate_wise_additivity.md)
- Claim Ledger: [`coordinate_wise_additivity_claim_ledger.md`](../coordinate_wise_additivity_claim_ledger.md)

## Reviewer & Refutation Sandboxes

- Reviewer Launcher: [`public_export/run_notebook.bat`](../public_export/run_notebook.bat) (opens `jupyter_notebooks/reviewer_coordinate_additivity.ipynb`).
- Refutation Launcher: [`public_export/run_refutation.bat`](../public_export/run_refutation.bat) (opens `jupyter_notebooks/refutation_sandbox.ipynb`).
