# COUNTERMODEL_REGISTER — fable_hilbert_walk_20260819

**AuthorityEffect:** None.

One separating model for every claim that a lift is NOT forced
(gate G5) — finite except where the refuted claim logically
requires an infinite or receipt-shaped separator (rows 1 and 3).
Every entry names a compiled Lean declaration in this folder (or,
for row 3, a printed axiom receipt); none is prose-only.
"Separates X from Y" means: X holds on the model, Y fails, so no
argument from X alone can reach Y.

| # | rung | non-forced claim refuted | separator / receipt witness | Lean declaration |
|---|------|--------------------------|------------------|------------------|
| 1 | H000 | "presentation calculus implies finiteness" | Nat with parity presentation satisfies all PrimitiveDifference laws; no `Enum Nat` exists | `H000.no_enum_nat`, `H000.parity_laws_hold` |
| 2 | H001 | "unequal marks supply probability semantics" | signed vector (−1, 2): mass one, nonnegativity fails; uniform vector (1, 1): nonneg, mass two | `H001.signed_mass_one` + `H001.signed_not_nonneg`; `H001.double_nonneg` + `H001.double_not_normalized` |
| 3 | H001 | "a dense mass carrier is free in this host" | receipt-shaped separator: each of the nine Rat laws `ratPack` requires depends on `Classical.choice` (per-law receipts printed; not claimed for every Rat lemma) | printed receipts for `ratPack` and its nine law fields, `axiom_report.txt` (a receipt, not a declaration) |
| 4 | H002 | "selected-representative checks certify descent" | E018 model: fixes every section point (`E018.T_on_section`), splits the (false,·) fiber (`E018.splits_fiber`), no descended map | `H002.descent_failure_replay` (trunk `E018.no_tbar`), `E018.T_on_section`, `E018.splits_fiber` |
| 5 | H003 | "determinism implies reversibility" | two-state collapse `c(_) = false` has no two-sided inverse | `H003.collapse_not_reversible` |
| 6 | H004 | "the coefficient carrier is determined" | δ_true + δ_true = 0 over F2, ≠ 0 over Int: same formal sum, different geometry | `H004.f2_superposition_cancels`, `H004.int_superposition_persists` |
| 7 | H005 | "free linearization supplies the Gram form" | identity Gram and diag(1,2) Gram disagree on δ_true (1 vs 2) | `H005.gram_not_unique` |
| 8 | H005 | "positive-definiteness comes with the construction" | (1,1) over F2 is nonzero with zero self-pairing | `H005.f2_isotropic` |
| 9 | H006 | "the permutation envelope is all isometries" | swapI = i·SWAP preserves the form, is no permutation lift | `H006.swapI_isometry`, `H006.swapI_not_permutation` |
| 10 | H007 | "the complex carrier is selected below H007" | representative H004/H005/H006 theorems instantiated over Int (obligation 6's R replaced by the host-admissible real-like carrier Int, disclosed) | `H007.real_pipeline_complete` |
| 11 | H008 | "phase-blind weights determine the state" | ψ₁=(1,1), ψ₂=(1,−1): equal weights, unequal vectors | `H008.equal_weights`, `H008.distinct_vectors` |
| 12 | H009 | "the phase fiber is the global-unit orbit" | ψ₂ shares ψ₁'s fiber (`H009.relative_phase_in_fiber`) but is not ANY scalar multiple of ψ₁ — a fortiori no unit multiple, enumeration-free | `H009.psi2_not_scalar_multiple` (also `psi2_not_unit_multiple` for the enumerated form) |
| 13 | H010 | "phase differences are unobservable" (mutation: they'd stay invisible) | unnormalized Hadamard separates ψ₁ from ψ₂: readouts (4,0) vs (0,4) | `H010.mix_separates` |
| 14 | H010 | "the mixed readout factors through the phase quotient" | the two witnesses under one fiber with different readouts | `H010.no_descent_through_fiber` |
| 15 | H010 | mutation 1 (G6): witness survives with phase removed | ψ₂ ↦ literal (1,1) mutant (defined independently, not aliased): separation provably collapses | `H010.mutation_phase_removed`, `H010.mutant_is_phase_stripped` |
| 16 | H010 | mutation 2 (G6): mixing unnecessary | witnesses provably indistinguishable without mixing (the statement that can fail); descent of the unmixed readout recorded definitionally for contrast | `H010.diagonal_blind_on_witnesses` (G6-sensitive), `H010.mutation_diagonal_readout` (definitional) |
| 16b | H002 | mutation 3 (G6): descent witness survives with fiber-splitting flip removed | stripping the flip from E018's dynamics restores congruence AND a descended map exists | `H002.mutation_descent_restored` |
| 17 | H011 | "interference selects C / U(1)" | the whole witness realized over Int (sign group {±1} only) | `H010.int_realization`, `H010.int_no_descent` |
| 18 | H012 | "noncommutativity lives in the weight layer" | diagonal matrices commute (theorem); nilpotent pair does not | `H012.diagonal_commutes`, `H012.noncomm_witness` |
| 19 | H013 | "the quadratic rule is the unique positive scale-distinct readout" — NOT "positivity + normalization pin the Born rule" (that needs a shared-contract rival; open O-6, `H013.born_nonuniqueness_open` = false) | quartic readout: positive, not a rescaling of the quadratic rule, differs on amplitudes (2,1) — but at a different total (17 vs 5), so no shared normalization contract | `H013.quartic_rival`, `H013.quartic_not_proportional`, `H013.weights_pinned` |
| 20 | H014 | "the tensor host is exhausted by product states" (entanglement witness) — NOT "tensor is not forced", which stays open (`H014.tensor_not_forced_open` = false) | tensor host carries a non-product vector while the direct-sum host is exhausted by its component embedding — structurally inequivalent rules | `H014.bell_not_product`, `H014.sum_component_embedding_surjective` |
| 21 | H015 | "any dynamics extends to an isometry on the same basis" | collapse: form preservation contradicts basis action (1 = 0) | `H015.collapse_no_isometry` |
| 22 | H015 | "the dilation is canonical" | id and (x, ¬h): distinct reversible dilations, same reduced dynamics | `H015.same_reduction`, `H015.dilations_distinct` |
| 23 | H016 | "discrete steps interpolate at report level" | toggle has no square root among the four Bool endomaps | `H016.no_report_half_step` |
| 24 | H016 | "the amplitude interpolant is canonical" | M and −M both square to 4·SWAP, M ≠ −M | `H016.sqrtSwap_squares_to_scaled_swap`, `H016.sqrtSwapNeg_also_squares`, `H016.interpolant_not_unique` |

## Open obligations without countermodels (declared, not asserted)

Per G5, claims we could NOT separate are listed as open rather than
asserted:

- **O-1**: whether some strengthening of the selector pack (H011)
  short of full QM_062 assumptions already excludes the sign
  carrier. Open; needs a theorem or a finer countermodel.
- **O-2**: whether the quartic rival (H013) survives a
  noncontextuality axiom at dimension 2. Open; Gleason's own
  dimension bound suggests dimension-2 rivals persist, but no
  local theorem states this.
- **O-3**: a choice-free dense coefficient carrier for this host
  (H001 boundary). Open; would require building Q from scratch
  inside the campaign with choice-free lemmas.
- **O-4**: whether the collapse map itself admits a reversible
  dilation under an explicit ancilla-preparation convention (the
  H015 witnesses dilate the identity, not the collapse). Open;
  needs the convention formalized, then a construction or a
  refutation.
- **O-5**: whether tensor composition is "not forced" — i.e.
  whether a rival composition (direct sum or other) satisfies the
  same composition interface the physics demands. H014 proves the
  entanglement witness and the structural inequivalence, but not
  this; a precise interface is not formalized
  (`H014.tensor_not_forced_open` = false). Open.
- **O-6**: a same-normalization-contract Born non-uniqueness — two
  effect-bearing readouts on one common state/effect domain, both
  meeting one fixed normalization, that differ. H013 gives only a
  positive non-proportional rival at a *different* total (17 vs 5),
  not a shared-contract rival (`H013.born_nonuniqueness_open` =
  false). Open; expected achievable at dimension 2 (where Gleason
  fails) once a division-free fixed-scale contract is formalized.

**AuthorityEffect:** None.
