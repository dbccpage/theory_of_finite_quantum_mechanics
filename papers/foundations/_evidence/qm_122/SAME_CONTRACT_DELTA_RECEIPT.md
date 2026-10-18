# SAME_CONTRACT_DELTA_RECEIPT — QM_122 v0.1.5

**AuthorityEffect:** None. This receipt records a bounded Lean
replay and its source custody. It is not a physical claim, a
Gleason theorem, or a revision of the 2026-08-19 baseline.

## What changed

The frozen PR #56 archive remains in `BUILD_RECEIPT.md` and
`SOURCE_MANIFEST.txt`. Earlier deltas remain in their own receipts.
This separate delta adds one theorem.

`H013Contract.two_effect_rules_share_unit_total_and_disagree`.
Two effect-bearing pairings of the same quadratic weights:

- the declared dual pairing `bornRule`;
- the report-swapped pairing `swappedRule`.

Both send the unit effect (value 1 at every report) to the total
weight of the state. Both stay nonnegative on nonnegative effects.
They disagree on the false-indicator at amplitudes (2,1): 4 versus
1. Lean axioms `{propext, Quot.sound}`.

This contract does not include frame additivity, noncontextuality,
or dimension at least 3. Gleason uniqueness remains imported. The
quartic rival in H013 is a different comparison: it does not share
the unit-effect total.

## Source custody

`SAME_CONTRACT_DELTA_SOURCE_MANIFEST.txt` binds the union closure
of `lake build FableHilbertWalk20260819`: 25 campaign modules, 27
J011Admitted roots, `lakefile.lean`, and `lean-toolchain` (54
sources). Its per-file lines and aggregate are specified there.

- Source-manifest SHA-256:
  `deaaecfca32dad99f2fe5a33f0371baf90ed42833df140637346eaf114048855`
- Aggregate closure SHA-256:
  `d7d3eacea16385c2351c4634564145131492b75d957591262373b38fb69be78a`

The commit that contains this receipt binds these bytes to history;
the receipt does not try to name its own future commit hash.

## Replay

From `lean4/genx/`, under the toolchain named by `lean-toolchain`:

```text
lake build FableHilbertWalk20260819
```

Result: **Build completed successfully (36 jobs)**. The printed axiom
reports for `two_effect_rules_share_unit_total_and_disagree` and
`walk_root_two_effect_rules_share_unit_total` contain only
`propext` and `Quot.sound`.

## Non-claims

- This does not refute Gleason uniqueness.
- This does not exclude the sign group in favour of the circle.
- This does not force cartesian product as the only way to combine systems.
- This does not recover finite complex matrices.
- This does not assign SUSY or SU(3)×SU(2)×U(1).
- This does not modify Paper 0 or replace the PR #56 baseline.
