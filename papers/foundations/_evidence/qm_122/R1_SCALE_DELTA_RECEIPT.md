# R1_SCALE_DELTA_RECEIPT — QM_122 v0.1.14

**AuthorityEffect:** None. This receipt records a bounded Lean
replay. It is not a probability interpretation, not uniqueness of
the quadratic readout, and not a revision of the 2026-08-19
baseline.

## What changed

FRONTIER R1. `H010Scale.mix_doubles_total_any`: for every GaussInt
amplitude vector on Bool, `totalWeight (mix v) = 2 * totalWeight v`.
The identity is the parallelogram law
`|z+w|^2 + |z-w|^2 = 2(|z|^2+|w|^2)`.
`H010.mix_doubles_total` is the psi1/psi2 special case.
Lean axioms `{propext, Quot.sound}`.

## Source custody

`R1_SCALE_DELTA_SOURCE_MANIFEST.txt` binds the union closure of
`lake build FableHilbertWalk20260819`: 36 campaign modules, 27
J011Admitted roots, `lakefile.lean`, and `lean-toolchain` (65
sources).

- Source-manifest SHA-256:
  `f6c3d8d3e8efea6e90426d0c45ed038abad992251ee57e4efe8eaa49298010d3`
- Aggregate closure SHA-256:
  `01cffe6da958afe957d1bfb0d4ad57a48d32c84617b9aefe7d7d3838fc5b6c85`

The commit that contains this receipt binds these bytes to history.

## Replay

From `lean4/genx/`, under the toolchain named by `lean-toolchain`:

```text
lake build FableHilbertWalk20260819
```

Result: **Build completed successfully (47 jobs)**. The printed
axiom reports for `mix_doubles_total_any` and
`walk_root_mix_doubles_total_any` contain only `propext` and
`Quot.sound`.

## Non-claims

- This does not interpret weights as probabilities.
- This does not uniquely select the quadratic readout.
- This does not recover ordinary \(M_n(\mathbb{C})\).
- This does not modify Paper 0 or the frozen PR #56 archive.
