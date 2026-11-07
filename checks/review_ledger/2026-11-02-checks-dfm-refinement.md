# File review: binary-refinement limit checker

AuthorityEffect: None.

The 149-line Python source and the logical contents of its existing adjacent
contract were read. The source bytes matched the isolated worktree. A normal
Python 3.14.7 run reported **14,642** successful finite checks. The continuum
limit and completeness results remain separate conditional Lean statements.

## `dfm-continuum-refinement-limit.contract.score.yaml`

- **File score: 4.** Required adjacent metadata and current source hash match.
  Its historical `L3D` score falls below the requested L4B floor.
- The cited Lean replay and independent derivation-note hashes no longer
  match their current files; the review-document pin matches. Preserve the
  historical record and append a fresh source-bound assessment.

## `dfm-continuum-refinement-limit.py`

- **File score: 4.** Referenced by the DFM node and evidence pages. The exact
  scalar, finite S3 and negative-control examples need input and result-state
  repair before broader reuse.
- **Bytes:** `f4954a40a525a19e69588eb436c2810f2c021e4456e6d4f3595998ff41c0220d`.
- **SCORING.md:** L3, Exact profile; G1/G2/G3 have at most D ceilings for
  stale evidence and the boundary and counter errors below. Other gates are
  unassessed; composite/token null, L4B not established.
- **Counter accumulates between executions.** `checks` is global and `main`
  does not reset it. Two calls in one process report `[14642, 29284]`, even
  though each executes the same checks. Put the counter in a per-run result
  value and test repeated and failed runs so reported counts describe one run.
- **Invalid refinement domains.** `endpoints((2,))` returns `(1, 3/2)` even
  though words are meant to contain binary booleans; `leaves((), -1)` recurses
  until `RecursionError`, and `True` is accepted as depth 1. Validate a
  binary-word value object and a nonnegative non-boolean integer depth, with
  typed failure results and negative tests. `leaves` also materializes `2^n`
  results, so declare and enforce a resource bound or stream the traversal.
- **Finite group boundary.** `mul` and `inv` assume valid three-element
  permutations but accept raw tuples. Name and validate the S3 value object
  and reject malformed values rather than relying on indexing errors.
- **Composition:** separate the run report from scalar and noncommutative
  controls; keep the supplied geometric-bound hypotheses and the distinction
  between finite evidence and the Lean limit theorem. Radon 6.0.1 reports
  maximum CCN 12; no complete higher-grade structural or mutation audit ran.
