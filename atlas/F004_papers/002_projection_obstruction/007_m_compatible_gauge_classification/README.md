# GS-001 — M-Compatible Gauge Classification

**Title:** M-Compatible Gauge Classification for Banach Presheaf Coboundaries: The ℓ¹ Maximal-Symmetry Endpoint  
**Author:** Jeremy H. Carroll  
**Status:** Published Zenodo (latest **v4.6**)  
**Version DOI (latest):** [10.5281/zenodo.20677155](https://doi.org/10.5281/zenodo.20677155)  
**Concept DOI:** [10.5281/zenodo.18897080](https://doi.org/10.5281/zenodo.18897080)  
**Historical version (v4.2, often cited as 20564214):** [10.5281/zenodo.20564214](https://doi.org/10.5281/zenodo.20564214)  

---

## What this package is

Conditional diagnostic classification: under maximal bounded-linear local symmetry plus edge-additive aggregation, local gauges are proportional to native stalk norms and the global diagnostic is a weighted $\ell^1$ edge sum. Not finite-structural $\ell^1$; not CPTP→trace-norm uniqueness alone.

## Verify (production code)

```bash
cd omega_engine/research/published/004_projection_obstruction/007_m_compatible_gauge_classification
python -m pytest code/tests -q -p no:debugging
```

Production modules live under `code/gs001/` with facade `code/gs001_gauges.py`.

## Human surfaces

| Surface | Path |
|---|---|
| Monograph | `007_m_compatible_gauge_classification.md` |
| Claim ledger | `007_m_compatible_gauge_classification_claim_ledger.md` |
| Reviewer notebook | `jupyter_notebooks/001_reviewer_m_compatible_gauges.ipynb` |
| Refutation | `jupyter_notebooks/002_refutation_sandbox.ipynb` |
| Launchers | `public_export/run_notebook.*` · `run_refutation.*` |
| Lean mirror | `lean4/research_programs/004_projection_obstruction/007_m_compatible_gauge_classification/` |

## Lean public inventory (anti-junk)

**Include in any public zip:** manuscript, ledger, change log, `LICENSE`, this README, `code/gs001/` + `gs001_gauges.py` + `code/tests/`, notebooks, `public_export/` launchers, Lean `*.lean` + Lean README, `docs/000_quick_start.md`, `docs/descriptions.md`, `docs/keywords.md`, `docs/references.md`, `docs/GS001_ZENODO_METADATA.json`, evidence coverage receipts if honest.

**Exclude:** `__pycache__/`, `*.pyc`, `docs/dev_rips/`, `docs/rt/`, `docs/scratchpad/`, `.pytest_cache/`, empty e2e/integration shells, agent OMC scratch.

## DOI chain (verified live 2026-08-02)

| Record | DOI | Note |
|---|---|---|
| Concept | 10.5281/zenodo.18897080 | Stable concept |
| v4.2 | 10.5281/zenodo.20564214 | Historical; PO-000 bibliography often cites this |
| **v4.6 (latest)** | **10.5281/zenodo.20677155** | Prefer for new cites |

## License

CC-BY-4.0 (text/figures) · Apache-2.0 (code/notebooks) as declared on Zenodo / `LICENSE`.
