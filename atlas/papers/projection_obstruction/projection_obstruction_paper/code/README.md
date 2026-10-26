# `code/` — production Python source for PO-000

`code/` **is** the production source of this deposit. Tests live in
`code/tests/`. There is no other Python layout.

*Historical note (2026-08-31, v6.3 Zenodo republication):* an earlier
revision of this file described `code/` as a "flat compatibility mirror" of a
production package at `src/po000/` with tests at a root `tests/`, synced by
`scripts/sync_code_mirror_from_src.py`. That src-layout migration was never
applied to this deposit — no `src/` or top-level `tests/` directory exists
here — so the mirror doctrine was false and is withdrawn. The migration
scripts were first retained under `scripts/` marked historical, then deleted
outright on 2026-08-31 by author decision (along with the dormant
`check_claim_ir.py` gate); this note is their remaining record.

## Dependencies

Standard library + `numpy` + `scipy` + `pytest`. The exact certificate rail runs on
the stdlib-only engine in [`exactsym.py`](exactsym.py) (rationals, exact
matrices, and the small symbolic surface the certificates need); the
numerical replay rail uses numpy and scipy. `matplotlib` is optional and only
needed by the notebooks. The v6.4 exact Taylor-coefficient module
`short_time_jets.py` as well as `polynomial_onset.py`, `local_persistent_zero.py`,
and `derivation_replays.py` additionally require SymPy (`pip install .[jets]`
from the package root). Its targeted cases include exact onset and
locality controls plus numerical remainder checks; they do not certify
the analytic infinite-volume theorem.

## Verify

```bash
# from the package root
python -m pytest code/tests
```

(`pyproject.toml` sets `testpaths = ["code/tests"]` and
`pythonpath = ["code"]`, so a bare `python -m pytest` from the root is
equivalent.)

To replay the claim ledger and verify the receipt independently:

```bash
PYTHONPATH=code python code/replay.py --output evidence/000_mechanization_run.json
python code/verify_certificate.py evidence/000_mechanization_run.json
```

Notebooks add the flat directory to their path and use bare imports:

```python
sys.path.insert(0, str(ROOT / "code"))
from falsification_sandbox import run_all_breaks
```

## Lean honesty (public sentence)

Lean certifies the algebraic RE hierarchy, abstract defect transfer, the
Theorem 4.2 weighted/orbit singleton cores, and the §7.4 observer-visibility
layer; the short-time quantum bound is paper-proved with Python finite
replays — not a Lean quantum theorem. Per-file Lean build status is in
`../lean4/README.md`.
