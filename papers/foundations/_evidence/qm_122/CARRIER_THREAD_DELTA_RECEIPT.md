# CARRIER_THREAD_DELTA_RECEIPT — QM_122 v0.1.4

**AuthorityEffect:** None. This receipt records a bounded Lean
replay and its source custody. It is not a physical claim, a
derivation of quantum mechanics, or a revision of the 2026-08-19
baseline.

## What changed

The frozen PR #56 archive remains in `BUILD_RECEIPT.md` and
`SOURCE_MANIFEST.txt`. The v0.1.2 frame-additivity delta remains
in its own receipt. This separate delta adds two theorems.

1. `HWCarrierThread.one_carrier_through_mixing_leftover`.
   Amplitudes on the H000 presented carrier ride along that
   carrier's presentation map. Same-report points get the same
   amplitude. Pushing phase-blind weights back along the
   presentation recovers twice the report-level weight, because
   each report fiber has two points. Mixing leftover is then the
   leftover of that report end. Lean axioms `{propext, Quot.sound}`.
   This does **not** thread one carrier through the whole walk.

2. `H014Bilin.embed_eq_tensor`. On Bool × Bool, any map that is
   additive and integer-homogeneous in each slot, and that sends a
   pair of report-basis vectors to the corresponding product-basis
   vector, equals the pointwise product already named in
   `H014.tensor`. Lean axioms `{propext, Quot.sound}`. The cartesian
   product of report sets is an import of that interface. Direct sum
   lives on a different host and is not a rival here. This does
   **not** prove that product is the only legal way to combine
   systems.

## Source custody

`CARRIER_THREAD_DELTA_SOURCE_MANIFEST.txt` binds the union closure
of `lake build FableHilbertWalk20260819`: 24 campaign modules, 27
J011Admitted roots, `lakefile.lean`, and `lean-toolchain` (53
sources). Its per-file lines and aggregate are specified there.

- Source-manifest SHA-256:
  `09f34b09a9dcbe87c5b6ce170b6dec71d6787e8331a4c17d906be768fa45c2ea`
- Aggregate closure SHA-256:
  `fbbf10145b5fbfcc15d4dc60770d2e41a1584cc69ce93c5ef92f2e3db64643fb`

The commit that contains this receipt binds these bytes to history;
the receipt does not try to name its own future commit hash.

## Replay

From `lean4/genx/`, under the toolchain named by `lean-toolchain`:

```text
lake build FableHilbertWalk20260819
```

Result: **Build completed successfully (35 jobs)**. The printed axiom
reports for `one_carrier_through_mixing_leftover`,
`embed_eq_tensor`,
`walk_root_threads_one_carrier_through_mixing`, and
`walk_root_bilinear_product_unique` contain only `propext` and
`Quot.sound`.

## Non-claims

- This does not close the whole walk on one presented carrier.
- This does not exclude the sign group in favour of the circle.
- This does not exhibit two Born-style effect rules on one shared total.
- This does not recover finite complex matrices.
- This does not assign SUSY or SU(3)×SU(2)×U(1).
- This does not modify Paper 0 or replace the PR #56 baseline.
