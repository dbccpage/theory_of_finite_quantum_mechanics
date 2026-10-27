# Finite Distinction Carriers and History Escape

Version 1.1.0 · 2026-10-08 · Author-review prose preprint; not externally published.

Read the [manuscript](wd2_finite_distinction_carriers_and_history_escape.md)
or its [PDF](wd2_finite_distinction_carriers_and_history_escape.pdf).

The manuscript states finite-horizon observational equivalence,
stabilization, shortest separating words, and the smallest deterministic
quotient. The report extension has an explicit sufficient factorization
hypothesis. These are classical finite-state minimization results, not a
reconstruction of quantum theory.

Lean 4 elaborates Theorem WD2-T1 in `lean4/FiniteDistinction.lean`.
`code/finite_distinction.py` evaluates the sharp chain, the update-stable
pair, and the factored report. Lemma WD2-L1 and records WD2-T2 through
WD2-T6 are not Lean theorems in this package. The
[reading notebook](jupyter_notebooks/001_reviewer_wd2_finite_distinction_carriers_and_history_escape.ipynb)
contains Markdown cells only.

From the package root, with Python 3.12:

```bash
py -3.12 verify_deposit.py --test code/tests/test_proved_rows.py --lean
```

Checksum-only checks, which do not elaborate the proofs:

```bash
python verify_deposit.py
python scripts/regen_sha256sums.py --check
python tools/rebuild_release.py --check
```

On Windows, use `py -3.12` in place of `python`.
See [quick start](docs/quick_start.md) for the PDF rebuild commands.

The manuscript, documentation, and prose notebook retain CC-BY-4.0.
The notebook launchers retain Apache-2.0. Packaging utilities copied from
the repository's paper template retain PolyForm Noncommercial 1.0.0;
see [LICENSE](LICENSE) and [LICENSE-CODE](LICENSE-CODE).
