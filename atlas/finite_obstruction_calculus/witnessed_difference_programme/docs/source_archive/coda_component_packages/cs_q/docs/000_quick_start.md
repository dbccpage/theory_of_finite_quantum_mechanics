# Quick start — Finite Profile Factorization and Sampling Limits (CODA-CS-Q)

A query factors on the realized profile image exactly when it is constant on the profile fibres. A decoder with uniform error epsilon bounds collision distance by twice epsilon; value equality at zero error requires metric separation.

Lean proves image equivalence and uniqueness, abstract distance inequalities, and the extension obstruction. Its sampling counterexample uses Boolean signals on three points. The real quadratic endpoint/midpoint counterexample is proved in prose and checked at rational points. The Lipschitz declaration is a monotone-scale schema; no real-metric instance is built here.

Python solves on a declared nonempty finite observation domain D. Each solve copies states and observes each profile/query pair once; the returned lookup covers only Prof(D) and raises KeyError elsewhere. Deterministic non-mutating callables and stable hashable profiles are required. ImagePoint requires a profile binding and an explicit supplied factor. Admission flags require actual booleans; all eight checks must pass. The 14-slot Lean schema records hypotheses, not continuum existence proofs.

## Replay

Start each command block from this extracted package's root, using its own Python environment (Python 3.11 or newer). The replay extra declares test, notebook, lint, and type tools. A release environment lock records the exact verified versions; these minimum dependency declarations alone are not a lock.

```console
python -m pip install -e ".[replay]"
python -m pytest code/tests -v
python -m ruff check code
python -m mypy --config-file pyproject.toml code/coda_cs_q_bridge_core.py code/cochain_presentation.py
```

Use `-n auto` with pytest for optional parallel execution. Collect current test counts with `python -m pytest code/tests --collect-only -q`.

Replay the notebooks from this package root:

```console
python -m nbclient jupyter_notebooks/000_two_dots_do_not_make_a_curve.ipynb
python -m nbclient jupyter_notebooks/001_when_a_blurry_view_still_answers.ipynb
python -m nbclient jupyter_notebooks/002_nearby_inputs_nearby_answers.ipynb
```

Enter `lean4/` so Elan selects the toolchain pinned there. This block returns to the package root:

```console
cd lean4
lake build
lake env lean coda_cs_q_000.lean
cd ..
```

Generate the figure and build the manuscript from the package root:

```console
python code/generate_figures.py
xelatex -interaction=nonstopmode -halt-on-error coda_cs_q_bridge.tex
```

The claim ledger and `docs/lean_claim_map.md` state the exact formal scope. Build success, finite tests, and general mathematical claims are separate evidence. Standard kernel axiom dependencies are reported by the entrypoint axiom queries.
