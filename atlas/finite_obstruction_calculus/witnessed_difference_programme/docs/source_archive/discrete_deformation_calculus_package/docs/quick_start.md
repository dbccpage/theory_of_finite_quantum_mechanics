# Quick start

Read the [package README](../README.md) for installation and verification.
Run the commands from the package directory or the extracted release directory.

## Learn in three steps

1. Open [Entering the calculus](../jupyter_notebooks/01_enter_the_calculus.ipynb).
   Measure the hollow square: Φ₁ = 1 and Γ₂ = 0. Double its defect; Φ₁ becomes 2.
2. Open [Trying to break the laws](../jupyter_notebooks/02_falsify_the_laws.ipynb).
   Remove a receipt or descent ledger and inspect the exact refusal.
3. Read the [monograph](../discrete_deformation_calculus.md) and [references](references.md)
   for cochain definitions, exact diagnostics, and literature references.

The notebooks test quotient-class confusion and rehashed-history attacks,
with predict-before-run prompts and feedback specific to each notebook.

Both notebooks discover the package from its directory, their own directory,
or the repository root. Replay them independently using the selected Python:

```bash
python scripts/replay_notebooks.py --check
python -m pytest -q code/tests/test_review_regressions.py
```

Common misconception: Γ₂ = 0 says the cochain is closed; it does not say the
cochain is exact. Likewise an abstract witness flag does not authenticate the
corresponding receipt or licence. The examples have exact rational inputs;
floating point and Boolean stand-ins for rational numbers are refused.
