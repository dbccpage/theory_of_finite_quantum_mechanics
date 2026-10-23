# Quick start — CODA-A: Residuals of Projections, Kernels, and Cokernels

For a linear correction, `residual(C, x) = x - Cx`. If `C² = C`, the residual lies in `ker(C)`, and equal residuals identify classes modulo `im(C)`. Commuting linear maps transport residuals.

A-T1–A-T7 are algebraic statements. The Lean model uses additive groups; A-T7 proves the unique underlying quotient function, while scalar linearity is proved in the manuscript and checked in finite rational matrix examples. A-T8 is a declared commitment without a proof. A-T9 assumes finite rational coordinate spaces with the coordinate l1 norm and `im(C) = im(d0)`.

The finite classifier calls a closed cochain with positive quotient distance `ClosedResidual` (the project-specific Anomalon). A residual supplies diagnostic data; it supplies no authorization or causal provenance.

## Replay

Start each command block from this extracted package's root, using its own Python environment (Python 3.11 or newer). The replay extra declares test, notebook, lint, and type tools. A release environment lock records the exact verified versions; these minimum dependency declarations alone are not a lock.

```console
python -m pip install -e ".[replay]"
python -m pytest code/tests -v
python -m ruff check code
python -m mypy --config-file pyproject.toml code/coda_a_core.py code/cochain_presentation.py
```

Use `-n auto` with pytest for optional parallel execution. Collect current test counts with `python -m pytest code/tests --collect-only -q`.

Replay the notebooks from this package root:

```console
python -m nbclient jupyter_notebooks/000_what_is_left_over.ipynb
python -m nbclient jupyter_notebooks/001_when_a_projection_eats_the_leftover.ipynb
python -m nbclient jupyter_notebooks/002_moving_leftovers_with_a_linear_map.ipynb
```

Enter `lean4/` so Elan selects the toolchain pinned there. This block returns to the package root:

```console
cd lean4
lake build
lake env lean Core.lean
cd ..
```

Generate the figure and build the manuscript from the package root:

```console
python code/generate_figures.py
xelatex -interaction=nonstopmode -halt-on-error coda_a.tex
```

The claim ledger and `docs/lean_claim_map.md` state the exact formal scope. Build success, finite tests, and general mathematical claims are separate evidence. Standard kernel axiom dependencies are reported by the entrypoint axiom queries.
