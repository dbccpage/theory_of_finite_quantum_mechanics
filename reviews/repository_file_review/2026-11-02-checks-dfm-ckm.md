# File review: CKM physics fence checker

AuthorityEffect: None.

The 267-line Python source and the logical contents of its adjacent contract
were read. The source bytes match the isolated worktree. Python 3.14.7 in
normal and optimized mode reported 2,376 sign actions, 4,388 pair decisions,
one nonreal reconstruction, and 11 invalid-domain refusals with no failure.
These are finite checks of supplied nonzero rescalings, not a physical CKM or
Yukawa derivation.

## `dfm-ckm-physics-fence.contract.score.yaml`

- **File score: 4.** Required adjacent contract; it binds the current source.
  Its historical `L3D` assessment, including the earlier support exception,
  is below the user's L4B target.
- Two cited Lean replay evidence hashes no longer match their current files;
  the independent receipt still matches. Preserve the historical records and
  append a fresh source-specific assessment with current evidence.

## `dfm-ckm-physics-fence.py`

- **File score: 4.** Referenced by the DFM node and evidence pages. The exact
  normalization, equivalence witness and malformed-input controls are useful
  and need a stronger value-object boundary and bounded enumeration policy.
- **Bytes:** `c892785ddff595611d83acaade1166e5d755e00a42d84104d60fdad3b793c48b`.
- **SCORING.md:** L3, Exact profile. G1/G2 have at most D ceilings due to
  stale evidence and mutable exact values; Radon 6.0.1 reports maximum CCN
  17, which caps G5 at C. Remaining evidence is unassessed; L4B not met.
- **Mutable exact value object.** `GR(1)` validates its constructor, but its
  `re` and `im` attributes remain writable. Setting `g.re = 0.1` makes the
  object contain a float, and `shape(((g,),))` accepts it as a valid label.
  Make a clearly named Gaussian-rational value object immutable and validate
  both components at construction. Add tests for attempted mutation and exact
  value preservation across the normalization/action boundary.
- **Carrier and resource limits.** `sign_tables(0, 1)` produces `[()]`,
  although `shape` requires a nonempty table. The function materializes
  `2^(height*width)` tables, and all-pairs checks grow as `4^(height*width)`.
  Validate positive integer dimensions and explicitly bound or stream the
  enumeration; return typed failures for invalid or oversized requests.
  The fixed CLI uses small valid dimensions.
- **Composition and claims.** The single `GR` class can be named for its
  domain role and separated from finite case generation, while preserving an
  independent oracle. The contract correctly distinguishes arbitrary
  nonzero rational rescaling from unit-modulus physical rephasing; retain
  that distinction when changing names or compressing the code.
