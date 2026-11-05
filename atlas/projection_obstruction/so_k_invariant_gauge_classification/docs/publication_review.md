# Publication review of GS-002 v2.0.0

Review date: 2026-10-02. Baseline commit:
`adc3d57001a0491945fce1ccd203f696c57c389b`.

The paper's local rigidity, conditional aggregation, flat quotient duality,
single-cycle formula, and closure argument are consistent after the repairs
below. The contribution is a scoped finite obstruction application of
classical norm and convex-analysis results. The package remains a
**v2.0.0 candidate**, with the original candidate date. This
review neither creates a Zenodo version nor promotes partial formalizations
to complete proofs. Fresh Lean and notebook kernel gates remain required
before publication.

## Findings and repairs

| Finding | Repair and evidence |
|---|---|
| Imported unit-body statement omitted boundedness | Restored it, matching companion §2.2, Theorem 2.2. The whole vector space is a counterexample without it. Imported status is retained. |
| Compact orbit-body hypotheses were vague | Specified a continuous linear compact-group action, bounded spanning seed, and balanced convex hull. |
| Simple graph notation excluded the implemented theta graph | Declared indexed edges and source/target maps, allowing parallel comparisons. |
| Transport direction and ordinary divergence scope were unclear | Defined source-to-target transport and target-stalk defect; restricted ordinary divergence and cycle formulas to identity transports. |
| Cochain quotient could be read as cohomology of a filled complex | Distinguished all-cochain $C^1/\operatorname{im}d_0$ from $\ker d_1/\operatorname{im}d_0$. |
| Cycle exactness and extremum attainment were too compressed | Added explicit vertex partial-sum repairs, closed-subspace/compactness attainment arguments, and the scalar-incidence operator-norm proof. |
| Small circulation was treated as zero before its weighted cost was considered | Cycle routing now precedes zero-witness shortcuts. Nonzero circulation is preserved, including underflow-scale data; cycle norms use stable hypotenuse reduction. Zero-witness acceptance checks the weighted gap. |
| NaN-valued and vacuous random audits could pass | Reject nonfinite/negative gauge values and an empty effective sample; report the actual tested sample count. |
| Certificate tolerances and solver paths disagreed | Reject invalid tolerances; the smoothed path uses the declared tolerance for gap, divergence, and ball violations. |
| A degenerate face could supply an invalid cycle orientation | Derive the traversal from graph edges rather than assuming a face's repeated terms enumerate the cycle. |
| Small positive costs were labeled exact, and uncertified candidates supplied a quotient ratio | Computed-zero reporting uses zero cost, not a threshold; the ratio requires a positive tolerance-qualified quotient. Numerical flags remain qualified, not exact membership proofs. |
| Metadata had an incomplete source relation | Added the repository source identifier. Validation rejects incomplete related URLs, invalid calendar dates, and the wrong publication type. |
| Stored axiom dependencies were not compared with fresh results | Require exact declared target and dependency agreement, alongside the axiom allowlist. Isolated tests reject forged and mismatched receipts. |

The claim map now covers C1–C27, including imported, historical, and withdrawn
entries with their actual evidence limits. No code module is assigned as a
proof of an imported classification result. All mapped paths exist. The
historical withdrawn holonomy, unrestricted extreme-weight stability, and
McLachlan extension claims remain withdrawn.

The study guide, sixteen written Landau problems, worked solutions, and
notebook assertions cover hypotheses, counterexamples, signed weights,
quotient versus representative costs, closure, and evidence scope. Bibliographic
identifiers for the companion preprints follow the repository's record
registry; the imported gauge correspondence also has an immutable source link.
Live status of the existing Zenodo record was not retrievable in this review,
so no new publication/version status is asserted from that service.

## Fresh validation

| Check | Result |
|---|---|
| Locked installation | `uv sync --frozen --extra dev --extra notebooks` passed with Python 3.12.14. |
| Baseline suite | 129 tests; 98.00% combined statement/branch coverage. |
| New runtime regression probes before repair | 31 failed, 2 passed; failures reproduced the reported defects. |
| Final suite | 172 tests in 15 modules; 99.04% statement coverage, 96.21% branch coverage, 98.27% combined; the 95% gate passes. |
| Static checks | Ruff 0.14.13 passed; Mypy 1.19.1 passed for 32 source files. |
| Notebook examples | All 13 code cells and assertions passed in separate fresh Python processes, including three regenerated Agg plots. This is **not kernel replay**. |
| Lean source custody | All 8 source and 3 configuration hashes match the retained 2026-09-28 receipt. The source census has 39 theorem/lemma declarations and 40 print targets including `SO2Matrix`. |
| Manuscript | Markdown-generated TeX and PDF built with Pandoc 3.1.3 and XeLaTeX; no missing glyphs or overfull boxes. All pages rendered and inspected, with critical mathematics checked at full size. |
| Release envelope | Canonical manifest/tree bijection, metadata shape, deterministic ZIP byte/member/metadata checks, and extraction validation passed. These are custody checks. |

The machine-readable [validation receipt](validation_receipt.json) binds these
checks to source digests and the notebook replay method. Raw test and static
check summaries are in `validation/`.

## Required gates still blocked

The fresh pinned Lean/Lake gate could not start because this host has no
usable `lake` command for `leanprover/lean4:v4.34.0-rc1`. The dated receipt
is retained unchanged in substance; no fresh Lean success is claimed.

The required notebook subprocess kernel replay could not start because the
host denied Jupyter/ZMQ socket operations and the kernel died before
`kernel_info`. Sequential Python cell replay checks examples and assertions,
but does not replace this gate. Source notebooks record that narrower method.

The full `verify_deposit.py` command therefore **does not pass on this host**.
Its required gates have not been weakened or bypassed. On a host with the
pinned toolchain and working Jupyter kernels, run:

```bash
uv sync --frozen --extra dev --extra notebooks
uv run --frozen --extra notebooks python verify_deposit.py
```

Resolve any fresh build/census mismatch against its pinned sources rather
than treating the stored receipt as current. Confirm the intended Zenodo
version relationship during deposit preparation. A passing envelope gate
still establishes custody and scoped checks, not mathematical authority or
publication approval.
