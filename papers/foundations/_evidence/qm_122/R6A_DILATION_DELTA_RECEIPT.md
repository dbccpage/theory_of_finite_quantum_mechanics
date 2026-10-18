# R6A_DILATION_DELTA_RECEIPT — QM_122 v0.1.13

**AuthorityEffect:** None. This receipt records a bounded Lean
replay. It is not CPTP, not dilations of collapse, and not a
revision of the 2026-08-19 baseline.

## What changed

Frozen extra list and drop-one census stay as in v0.1.12.
This delta closes FRONTIER R6a.

`H015DilationCount.four_reversible_dilations_of_report_identity`.
Exactly four two-sided-invertible maps on Bool × Bool that fix the
report coordinate, classified by whether each report fiber flips
its ancilla. `H015.dil1` is the (false,false) flip pair;
`H015.dil2` is the (true,true) flip pair. Lean axioms `{propext}`.

R1 (mixing scale law for every vector) stays OPEN.

## Source custody

`R6A_DILATION_DELTA_SOURCE_MANIFEST.txt` binds the union closure of
`lake build FableHilbertWalk20260819`: 35 campaign modules, 27
J011Admitted roots, `lakefile.lean`, and `lean-toolchain` (64
sources).

- Source-manifest SHA-256:
  `9db3cd1d3045bbb49e9d74f0bc29c316c10bc9bcd0c6b8ffdf5cc336fad3de09`
- Aggregate closure SHA-256:
  `8ae347016b116eb09182d3bf0f0992c09cbec6095ffc5638ae18ccab8d972c65`

The commit that contains this receipt binds these bytes to history.

## Replay

From `lean4/genx/`, under the toolchain named by `lean-toolchain`:

```text
lake build FableHilbertWalk20260819
```

Result: **Build completed successfully (46 jobs)**. The printed
axiom reports for
`four_reversible_dilations_of_report_identity` and
`walk_root_four_report_id_dilations` contain only `propext`.

## Non-claims

- This does not import a channel class.
- This does not count dilations of collapse.
- This does not close R1.
- This does not recover ordinary \(M_n(\mathbb{C})\).
- This does not modify Paper 0 or the frozen PR #56 archive.
