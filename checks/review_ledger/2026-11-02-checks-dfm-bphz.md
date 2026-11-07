# File review: BPHZ continuum fence checker

AuthorityEffect: None.

The 230-line Python source and its existing companion's logical records were
read. The source bytes match the isolated review worktree. The fixed checker
passed with Python 3.14.7 in both normal and optimized mode. Its scope remains
the supplied finite forest/projector examples, not continuum convergence.

## `dfm-bphz-continuum-fence.contract.score.yaml`

- **File score: 4.** Required adjacent contract and source digest match. The
  historical score `L3D` and its authorized support-exception notation do not
  satisfy the user's current L4B target.
- Two of its three cited evidence hashes no longer match their current replay
  files; the independent-check receipt still matches. Keep historical records
  unchanged and append fresh evidence and a source-specific assessment.

## `dfm-bphz-continuum-fence.py`

- **File score: 4.** Referenced by the DFM node and evidence pages. This
  script has useful exact-input and noncommuting-projector refusals and needs
  boundary handling and maintainability improvements.
- **Bytes:** `0cad33ad25b1937de952b38c978ac1ef1058f91a938dc39efb5ad18f5be27752`.
- **SCORING.md:** L3, Exact profile; G1/G3 have at most D ceilings because
  historical replay evidence is stale and malformed input can produce an
  untyped exception. Full five-gate evidence is unassessed; L4B not met.
- **Shape validation.** `checked_reduce` validates exact entries,
  idempotence and pairwise commutation, but a three-entry matrix reaches an
  `IndexError` in `multiply` rather than an explicit invalid-shape result.
  Validate a four-entry exact matrix as a value object before multiplication;
  add short, long and non-sequence negative cases with typed failures.
- **Forest identity.** `forests(("L", "L"), OVERLAP)` returns duplicate
  `("L",)` entries and admits `("L", "L")`. The CLI supplies distinct
  labels. Make the named-forest input a set or reject duplicate/unknown labels,
  and test both cases so the API's output represents the intended carrier.
- **Verification boundary.** `check_family` checks that the reduction is
  idempotent and its image is killed by each supplied projector, but it does
  not directly test the converse that every common-kernel vector is fixed.
  A separate bounded review harness checked that equivalence for all **77**
  enumerated commuting families and **25** vectors each: **1,925 comparisons
  passed**. Retain this as scoped evidence or add a durable independent
  regression; it is not a general proof.
- **Composition:** move top-level execution behind a `main` entry point and
  separate finite forest fixtures from the reusable exact projector value and
  typed result. Maintain an independent checker for the Lean/client boundary.
  Radon 6.0.1 reports maximum CCN 11, consistent with the old numeric CCN
  observation; no new full complexity or mutation certification is claimed.
