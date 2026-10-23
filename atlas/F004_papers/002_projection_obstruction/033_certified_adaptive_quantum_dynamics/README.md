# PO-033: Adaptive Quantum Dynamics from Projection Residuals

The historical directory name says certified. The numerical prototype status is `HEURISTIC_UNCERTIFIED`. C2's algebraic idempotence and C3's regression counterexample are the proved part of the ledger. A certified trajectory would need validated integration, actual-defect control, conservative quadrature, and floating-point enclosures. Those are not in this package.

Jeremy H. Carroll & CODA Research Consortium. Updated 2026-10-11;
version 1.0.1. This is a research preprint package, not a published
Zenodo record. The historical title is retained for traceability.

The manuscript gives a conditional classical bound using the **actual**
trajectory defect and an initial mismatch term. Its edge form applies to ideal
product/cluster-product projected dynamics. The numerical prototype samples that
ideal tangent residual while integrating approximately; it does not bound
integration or quadrature error or enforce a requested tolerance. Its status is
`HEURISTIC_UNCERTIFIED`. `max_bond` means a ceiling on cluster qubits.

The review repaired residual/state timing, full cluster-factor sensing,
one-sided merge accounting, feasible merge selection, cluster-order bias,
periodic two-site bond counting, time origins, density/grid validation, and
rectangular norm witnesses. A regression shows that a norm witness alone does
not establish a best tangent projection. See `review_report.md` for results
and `review_observations.json` for six fully parameterized numerical runs.

Fresh review suite: **136 passed**, **99.01% statement coverage** (710 statements,
7 missed; 95% enforced). Coverage measures exercised source, not a theorem proof.

## Install and verify

Requires Python 3.10 or later. From this directory:

~~~bash
python -m pip install -e './code[dev,notebooks]'
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python verify_deposit.py --skip-lean
~~~

The verifier checks both metadata files, six ledger IDs and actual evidence
definitions, the full pytest suite with **at least 95%** statement coverage,
every declared hash, exact ZIP inventory and contents, manuscript digest
association in TeX/PDF, numerical observations, and notebook code-cell replay
from both supported directories. Poppler's `pdfinfo` is needed for the
PDF association check. The explicit Lean skip appears in the result.

For the fresh conditional Lean checks, install the pinned toolchain and run:

~~~bash
python verify_deposit.py
~~~

This runs `lake build` and the axiom audit. Both passed on 2026-10-11
with pinned Lean 4.34.0: 11 declarations, using only `propext`/`Quot.sound`
or no axioms. The proof sources and historical report are preserved, and
`lean4/README.md` states their abstract Nat/Int scope. They do not
mechanize the continuous analytic result or establish solver tolerance satisfaction.

For just the Python suite:

~~~bash
cd code
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -m pytest -q -p no:cacheprovider --cov=caqd --cov-report=term-missing --cov-fail-under=95
~~~

The sampled-bound utilities refuse nonfinite derived estimates and preserve a
streaming accumulator on refusal. Large finite trapezoids avoid intermediate
sum overflow; zero estimates with positive reference error show an infinite
ratio. These checks add no numerical-certification claim.

## Numerical reproduction

From the package root:

~~~bash
python scripts/reproduce_review.py --check
python scripts/replay_notebook.py
python scripts/replay_notebook.py --from-notebook-dir
~~~

The notebook contains editable Python parameters and plots; it has no slider
widgets. Committed outputs are cleared to prevent stale plots from being
mistaken for new evidence. Headless replay executes its code cells and
assertions, not a live Jupyter UI. All reference comparisons are floating-point
observations, not mathematical certification.

## Rebuild manuscript and release

The Markdown manuscript is canonical. Pandoc and XeLaTeX are needed to rebuild
its TeX/PDF. The builder records its source digest and uses a fixed review-date
epoch. Inspect the rendered pages after any content change.

~~~bash
python scripts/build_paper_artifacts.py
python scripts/rebuild_release.py
python scripts/rebuild_release.py --check
~~~

The existing archive filename `certified_adaptive_quantum_dynamics_2026-10-01.zip`
and deterministic ZIP timestamp are retained; the reviewed contents and
metadata date are 2026-10-11 (version 1.0.1). The archive includes payload plus both manifests
and excludes the outer ZIP itself, caches, and transient scratch. The retained
LaTeX log and auxiliary files document the manuscript build.
Rebuilding never publishes to Zenodo.

After extracting the ZIP, enter its `certified_adaptive_quantum_dynamics`
directory and use:

~~~bash
python verify_deposit.py --extracted --skip-lean
~~~

This checks the extracted payload and explicitly omits the outer archive check.
Loose and archive payload inventories must otherwise match exactly. Metadata
and byte integrity checks are not publication sign-off.

## Licenses

Text, figures, and documentation: CC-BY-4.0 (`LICENSE`). Code, notebook,
tooling, and Lean sources: Apache-2.0 (`LICENSE-CODE`). Both deposit metadata
files agree with these existing license files and the package version.
