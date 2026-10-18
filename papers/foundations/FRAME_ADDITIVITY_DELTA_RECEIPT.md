# FRAME_ADDITIVITY_DELTA_RECEIPT — QM_122 v0.1.2

**AuthorityEffect:** None. This receipt records a bounded Lean
replay and its source custody. It is not a physical claim, a
uniqueness theorem, or a revision of the 2026-08-19 baseline.

## What changed

The frozen PR #56 archive remains in `BUILD_RECEIPT.md` and
`SOURCE_MANIFEST.txt`. This separate delta adds
`H013_frame_additivity.lean` and its root import. It formalizes the
named scale-2 condition rather than merely reporting two numerical
totals:

```text
frameAdditiveAtScaleTwo readout :=
  for every state and every two orthogonal scale-2 frames,
  the two frame totals for readout are equal.
```

The compiled theorem is:

```text
H013Frame.fourth_power_dies_under_frame_additivity :
  not (frameAdditiveAtScaleTwo quarticAlong)
```

Its counterexample uses state `(2,1)`, frames `(1,1)`, `(1,-1)` and
`(1,i)`, `(1,-i)`, and fourth-power totals 82 and 50. The quadratic
readout totals 10 on those same two frames. That witness agreement is
not a proof that the quadratic readout satisfies the quantified
condition globally.

## Source custody

`FRAME_ADDITIVITY_DELTA_SOURCE_MANIFEST.txt` binds the union closure
of `lake build FableHilbertWalk20260819`: 22 campaign modules, 27
J011Admitted roots, `lakefile.lean`, and `lean-toolchain` (51
sources). Its per-file lines and aggregate are specified there.

- Source-manifest SHA-256:
  `3c9ba7af2810d0e9b4db39d266738aef4c8beeab64af48530f1a7d06a4ca71cd`
- Aggregate closure SHA-256:
  `a40cca67f2c3045e18ee0168bd071d593ca9c0eb48c1deba9e03be848e679ce4`

The commit that contains this receipt binds these bytes to history;
the receipt does not try to name its own future commit hash.

## Replay

From `lean4/genx/`, under the toolchain named by `lean-toolchain`:

```text
lake build FableHilbertWalk20260819
```

Result: **Build completed successfully (33 jobs)**. The printed axiom
reports for `H013Frame.fourth_power_dies_under_frame_additivity` and
`FableHilbertWalk20260819.walk_root_reaches_frame_additivity` contain
only `propext`.

## Non-claims

- This does not prove global frame additivity for the quadratic rule.
- This does not prove the Born square unique among all readouts.
- This does not show that the named condition is physically mandated.
- This does not thread one carrier through the full Hilbert walk.
- This does not modify Paper 0 or replace the PR #56 baseline.
