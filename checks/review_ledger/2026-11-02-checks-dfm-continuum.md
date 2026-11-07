# File review: finite continuum-interface checker

AuthorityEffect: None.

The 219-line Python source and the logical contents of its existing companion
were read. The source bytes matched the isolated review worktree. With Python
3.14.7 and SymPy 1.14.0, both normal and optimized runs passed 85 finite loop
words, 255 append cases, three invalid-path refusals and the fixed noncommuting
matrix witnesses. No smooth continuum construction follows.

## `dfm-continuum-interface.contract.score.yaml`

- **File score: 4.** Required adjacent metadata; the current contract binds
  the source bytes. Its historical `L3D` score and earlier support exception
  do not meet the user's L4B target.
- Two of three cited Lean replay hashes no longer match current files; the
  mutation receipt still matches. Keep historical entries and append a
  source-specific assessment with current evidence.
- The contract describes typed walk endpoints as an owned invariant. The
  Python `SignedPath` is an unvalidated tuple of signed loop names on one
  vertex; endpoint-indexed general walks are a separate formal-model claim.
  Distinguish those boundaries in the current contract.

## `dfm-continuum-interface.py`

- **File score: 4.** Referenced by the DFM node and evidence pages; the
  independent finite noncommuting matrix and footprint checks are useful,
  but their reusable input boundary needs repair.
- **Bytes:** `17f37543b78c25ba4f84e40ffb904c0df8a0e37cb16436302d7ec7e4b5aa19de`.
- **SCORING.md:** L3, Exact profile; G1/G2 have at most D ceilings because
  the old contract mixes formal and executable boundaries and the transport
  helper accepts invalid matrices. Other gates remain unassessed; L4B not met.
- **Validated constructor can be bypassed.** `mat` rejects floats and
  determinant values other than one, but `path_transport` accepts arbitrary
  SymPy matrices directly. A determinant-2 matrix, a float-valued identity,
  and a singular matrix each pass through a positive signed edge. A negative
  signed singular edge instead raises SymPy's raw `NonInvertibleMatrixError`.
  Use an immutable validated `SL(2,Z)` label/value object at every entry
  point and return typed errors; add negative tests for all four cases.
  The fixed CLI constructs valid labels through `mat`.
- **Path composition and names.** The loop-word checker validates signs and
  edge names for its supplied one-vertex model. `transport` and `dress` use
  separate raw string paths and can raise `KeyError` for missing labels.
  Model graph, oriented edge and walk as named bounded-domain values if the
  helpers are reused; check composable endpoints only for the graph model
  where those endpoints are represented. Retain the zero-import independent
  witness or an independent oracle when composing shared code.
- **Evidence boundary:** Radon 6.0.1 reports maximum CCN 8, matching the old
  numeric observation. This does not establish all higher-grade tests,
  mutation coverage, continuum limits, or physical dynamics.
