# GS-000 — Coordinate-Wise Additivity

**Title:** Coordinate-Wise Additivity and Local ℓ¹ Gauge Selection (GS-000)\
**Author:** Jeremy H. Carroll  
**Canonical publication:** Zenodo **v6.1.1**

**Canonical version DOI:** [10.5281/zenodo.20723753](https://doi.org/10.5281/zenodo.20723753)

**Concept DOI:** [10.5281/zenodo.18944809](https://doi.org/10.5281/zenodo.18944809)  
**Historical version (v6.0):** [10.5281/zenodo.20173236](https://doi.org/10.5281/zenodo.20173236)  

**Repository state:** unpublished post-v6.1.1 draft; no later version or DOI is claimed

---

## What this package is

Finite combinatorial base case: edge locality + coordinate permutation symmetry + disjoint-coordinate additivity force coordinatewise $\ell^1$ edgewise; graph invariance gives orbit-weighted $\ell^1$; unweighted global $\ell^1$ needs edge-transitivity or explicit uniformity. Not finite-structural $\ell^1$.

## Verify (production code)

```bash
cd atlas/papers/projection_obstruction/coordinate_wise_additivity
uv sync --frozen --extra notebooks --extra dev
uv run --frozen --extra dev python -m pytest code/tests -q -p no:debugging \
  --cov=code --cov-branch --cov-report=term-missing --cov-fail-under=95
uv run --frozen --extra dev ruff check .
uv run --frozen --extra dev mypy code
uv run --frozen --extra notebooks python scripts/replay_notebooks.py
```

The focused suite contains **131 tests**. The 2026-10-02 review passed the
Python suite with 98.78% branch coverage, Ruff, and mypy. All three notebooks'
plain Python cells ran in isolated subprocesses using the explicit direct
mode below. Native Jupyter kernel replay was unavailable because this
environment blocks kernel sockets; direct execution does not verify widget
interaction or Jupyter transport. The Lean sources remain bound to their
historical 2026-09-28 receipt, with no fresh Lean compilation in this review.

```bash
uv run --frozen --extra notebooks python scripts/direct_notebook_replay.py
```

Direct mode leaves source notebooks unchanged. `--record` explicitly replaces
their stored outputs and records the direct execution method in notebook
metadata. These are repository-draft computational results only.

After regenerating the Lean receipt, manifests, and archive from the intended
release tree, run the fail-closed release-envelope gate:

```bash
uv run --frozen --extra notebooks python verify_deposit.py
```

`--tree-only` skips only the ZIP comparison. Passing either mode is an
integrity result, not a proof of the paper's claims or publication readiness.

On Windows, run the Lean portion from a genuinely short filesystem path and
set `LEAN_NUM_THREADS=1`; drive-letter aliases can be canonicalized back to a
long path by Lake. For the full verifier, point `TEMP` and `TMP` at an existing
short writable directory before invoking it.

Production module: `code/coord_additivity.py` (tests import this surface).

## Human surfaces

| Surface | Path |
|---|---|
| Monograph | `coordinate_wise_additivity.md` |
| PDF / TeX | `coordinate_wise_additivity.pdf` · `.tex` (local rebuild; Zenodo hosts published PDF) |
| PDF build receipt | `docs/pdf_build_receipt.md` |
| Claim ledger | `coordinate_wise_additivity_claim_ledger.md` |
| Reviewer notebook | `jupyter_notebooks/reviewer_coordinate_additivity.ipynb` |
| Refutation | `jupyter_notebooks/refutation_sandbox.ipynb` |
| Launchers | `public_export/run_notebook.*` · `run_refutation.*` |
| Lean mirror | `lean4/` |
| Review findings and checks | [`docs/review_receipt.md`](docs/review_receipt.md) |

Rebuild the manuscript with `python scripts/render_paper.py` (Pandoc 3 and
XeLaTeX required). The draft snapshot archive is
`coordinate_wise_additivity_2026-10-02.zip`; its filename is a snapshot date,
not a new publication version. Manifests bind the actual Git checkout bytes.

## Lean public inventory (anti-junk)

**Include:** manuscript, ledger, change log, `LICENSE`, this README, PDF/TeX if current, `code/coord_additivity.py` + `code/tests/`, notebooks, launchers, Lean cores, `docs/quick_start.md`, `docs/descriptions.md`, `docs/keywords.md`, `docs/references.md`, `zenodo_metadata.json`, `pyproject.toml`, `uv.lock`, and reproducible evidence.

**Exclude:** interpreter/test caches, generated Lean build products, transient
coverage files, and internal working directories.

## DOI chain (verified live 2026-08-02)

| Record | DOI | Note |
|---|---|---|
| Concept | 10.5281/zenodo.18944809 | Stable concept |
| v6.0 | 10.5281/zenodo.20173236 | Historical; sibling papers often cite this |
| **v6.1.1 (canonical publication)** | **10.5281/zenodo.20723753** | Prefer for new cites |

**Not a first mint:** this paper is already published. The current repository
tree contains later, unpublished work. It must not be described as v6.1.2,
uploaded under the v6.1.1 DOI, or treated as a new publication without a
separate author-controlled release decision.

## License

CC-BY-4.0 (text/figures) · Apache-2.0 (code/notebooks) as declared on Zenodo / `LICENSE`.
