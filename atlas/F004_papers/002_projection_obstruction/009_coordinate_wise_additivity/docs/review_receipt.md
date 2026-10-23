# Repository-draft review — 2026-10-02

Scope: GS-000, `009_coordinate_wise_additivity`, unpublished work following
canonical v6.1.1. No new public version or DOI is assigned.

## Findings and resulting changes

| Finding | Correction |
|---|---|
| Fixed-profile per-edge sameness was said to fail weighted aggregation | §3.5 now establishes descent for a fixed profile; coarser-total and varying-profile examples use separate carriers and relations |
| Kernel structure was said to uniquely determine norm geometry | §3.6 gives the shared-zero-kernel L1/L2 counterexample; classification uses the full observer bundle |
| PCC implication lacked a packaged bridge | Marked interpretive/open with the missing projection and congruence data stated |
| Basis extraction did not exclude k=0; local seminorm inheritance was implicit | Declared k≥1, empty-edge convention, and the zero-value / single-edge restriction argument |
| CE5's unrestricted exponent range did not isolate homogeneity | Restricted the subadditive candidate to 0<p<1 after weakening seminormhood; p=2 helper remains narrower and unpromoted |
| Lean CE1/CE3 scope differed from the actual prose models | Distinguished natural-number quadratic/polynomial helpers from real L2/cancellation witnesses |
| Counterexample headings were swallowed by open Markdown quotes in PDF | Closed the quote blocks and verified all five headings in extracted and rendered output |
| Cut discussion omitted orientation and continuous-minimizer boundaries | Added weighted finite coarea proof; absolute TV counts both crossing orientations; binary minimizers exist but are not mandatory |
| Probes could accept NaN outputs or missing data; zip silently truncated counts | Reject invalid carriers, nonfinite/negative outputs and weights, empty probes, bad orbit indices, and mismatched lengths; uniform collapse uses exact stored-weight equality |
| Imported quantum functions accepted invalid state/channel data | Added finite matrix and density checks, nonempty finite trials, and an explicit convex mixing range 0≤p≤1; stated CPTP non-increase rather than global strict contraction |
| Metadata included a related identifier with no identifier | Removed the incomplete relation; added a failing regression for absent/empty identifiers |
| Descriptions mislabeled the finite theorem as Banach-presheaf rigidity | Replaced descriptions and keywords with the actual finite scope |
| Stored launcher hashes differed from Git checkout bytes | Regenerated both manifests; package attributes now keep text at LF on all platforms |

## Executed checks

- Locked installation: `uv sync --frozen --extra notebooks --extra dev`.
- Python 3.12.14: **131 tests passed**, **98.78% statement/branch coverage**;
  required threshold 95%.
- `ruff check .`: passed; `mypy code`: passed, 14 source files.
- Exact Landau exercises: passed (basis weight, three quotient comparisons,
  weighted coarea, cancellation, and channel factor).
- `scripts/direct_notebook_replay.py`: all three notebooks passed in separate
  Python subprocesses, with 1 / 4 / 6 code cells respectively. This checks
  plain Python code and assertions and captures the Agg plot; it is not
  native kernel replay or widget testing. Recorded notebook metadata states
  the execution method, and tests bind the exact source/output file bytes.
- Pandoc 3.1.3 / XeLaTeX (TeX Live 2023): rebuilt the 26-page manuscript PDF;
  no overfull-box or missing-character diagnostics. All final pages rendered
  for visual inspection; all five counterexample headings were checked.
- Both manifests and the deterministic 2026-10-02 ZIP were regenerated and
  checked for exact tree/manifest/archive agreement with the existing
  fail-closed release helpers. This is a selected byte-integrity check.
- Unchanged Lean sources match the historical provenance digests. The
  stored 43-target axiom report was checked against the declared targets
  and standard-axiom allowlist as a historical receipt check only.

## Checks unavailable in this environment

Native `scripts/replay_notebooks.py` could not start its first Jupyter kernel:
local-interface discovery returned `Operation not permitted`, followed by
`Kernel died before replying to kernel_info`. Direct execution is a separate,
explicit computational mode and does not replace this release gate.

Fresh Lean compilation was unavailable: the local Lean executable returned
`error: failed to locate application`; the pinned v4.34.0-rc1 toolchain could
not be replayed. The proof sources and historical 2026-09-28 axiom receipt
were retained unchanged. No fresh build or full release-verifier pass is
claimed. The default verifier still requires a clean Lean build and native
notebook replay.

The Zenodo canonical record could not be independently retrieved during this
review. Its existing version, date, and DOI were preserved from repository
metadata. This changed package is not an upload candidate under the already
published v6.1.1 DOI.

Before a separately authorized future release, replay the full verifier in an
environment with the pinned Lean toolchain and functioning Jupyter sockets,
and reconcile the open formalization obligations in the claim ledger. Passing
integrity checks alone does not prove the manuscript or publish a record.
