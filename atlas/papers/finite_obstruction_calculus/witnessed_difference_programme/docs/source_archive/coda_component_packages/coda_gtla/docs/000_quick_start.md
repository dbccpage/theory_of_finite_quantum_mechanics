# CODA-GTLA 3.2.1 — quick start

Run from this extracted package directory:

```console
python -m pip install -e ".[test]"
python -m pytest code/tests -q
```

For Lean, run `lake build` and `lake env lean Core.lean` in `lean4/` (use `Algebra.lean` for the residual-algebra audit).
Read `coda_gtla_monograph.md` and `docs/lean_claim_map.md` for exact scope.
The licence record is declared model data, not external authentication.
