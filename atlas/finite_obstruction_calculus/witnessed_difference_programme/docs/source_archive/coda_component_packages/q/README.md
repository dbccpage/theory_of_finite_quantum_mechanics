# CODA-Q: Metric completion and midpoint enclosure

Version 3.1.1 · 2026-09-28 · preprint  
**Zenodo Record:** <https://zenodo.org/records/23025349>  
**DOI:** [10.5281/zenodo.23025349](https://doi.org/10.5281/zenodo.23025349)  

The note treats metric completion, the completion of the rationals, unique
uniformly continuous extension, and exact rational interval enclosure.
Concrete mathlib declarations supply the metric results. Python demonstrates
finite bisection, finite-list checks, and an off-sample query collision.

Run from this extracted package directory:

```console
python -m pip install -e .
python -m pytest code/tests -q
cd lean4
lake build
lake env lean Algebra.lean
```

The three notebooks in `jupyter_notebooks/` work from the package root or
the notebook directory. A midpoint is an approximation candidate; its
`midpoint_self_distance` is zero by definition and is not its error relative
to the enclosed real number. `error_bound` is the certified half-width.

The active claim ledger and `docs/claim_code_map.yaml` distinguish formal
metric statements from finite tests. `docs/coda_q_legacy_ledger.md`
is historical provenance for an earlier quarantine/quantum paper; those
old APIs and external proof claims are not current package capabilities.
