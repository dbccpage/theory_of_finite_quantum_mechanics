# CODA-Q 3.1.1 — quick start

The main results concern metric completion and midpoint enclosure.

From the extracted package root:

```console
python -m pip install -e .
python -m pytest code/tests -q
```

In `lean4/`, run `lake build` and `lake env lean Algebra.lean`.
The Python examples check finite exact rational data. Completion, density,
surjectivity and uniform extension are Lean/mathlib statements, not Python
smoke-test conclusions. See `../coda_q_claim_ledger.md`.
