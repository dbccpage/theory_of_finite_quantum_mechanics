# R4_R6B_DELTA_RECEIPT — QM_122 v0.1.15

**AuthorityEffect:** None. This receipt records a bounded Lean
replay. It is not a Hilbert unitary group, not a count of all
linear isometries of (Z[i])^2, not CPTP, and not a revision of the
2026-08-19 baseline.

## What changed

FRONTIER R4. `H006Envelope.two_permutation_lifts_envelope_strict`:
on Bool the reversible report maps are identity and toggle; their
permU extensions are identity and coordinate-swap. `H006.swapI` is
an isometry outside that pair. Not a Hilbert unitary group. Not a
count of all linear isometries of (Z[i])^2.
Lean axioms `{propext, Quot.sound}`.

FRONTIER R6b. `H015CollapseDilations.four_reversible_dilations_of_collapse`:
under the declared convention that the ancilla is prepared at
false, exactly four two-sided-invertible maps on Bool × Bool send
the prepared slice to collapse on the report coordinate. Not CPTP.
Not identity dilations. Convention is declared, not derived.
Lean axioms `{propext}`.

## Source custody

`r4_r6b_delta_source_manifest.txt` binds the union closure of
`lake build FableHilbertWalk20260819`: 38 campaign modules, 27
J011Admitted roots, `lakefile.lean`, and `lean-toolchain` (67
sources).

- Source-manifest SHA-256:
  `6d34c7fbe36b1ddd1bf21cd647c4cff206eed05359e43a48737a66d2bbedffdb`
- Aggregate closure SHA-256:
  `cc614a2abcb309ed3185f45928944a2977f90aed96395c5bdbdf14cc6af1312a`

The commit that contains this receipt binds these bytes to history.

## Replay

From `lean4/genx/`, under the toolchain named by `lean-toolchain`:

```text
lake build FableHilbertWalk20260819
```

Result: **Build completed successfully (49 jobs)**. The printed
axiom reports for `two_permutation_lifts_envelope_strict` and
`walk_root_two_permutation_lifts` contain only `propext` and
`Quot.sound`. The printed axiom reports for
`four_reversible_dilations_of_collapse` and
`walk_root_four_collapse_dilations` contain only `propext`.

## Non-claims

- This does not classify all linear isometries of (Z[i])^2.
- This does not recover a Hilbert unitary group.
- This does not select CPTP channels or a preferred dilation.
- This does not recover ordinary \(M_n(\mathbb{C})\).
- This does not modify Paper 0 or the frozen PR #56 archive.
- Frozen `evidence/frontier.md` stays SHA-256 `4c16a694…`.
