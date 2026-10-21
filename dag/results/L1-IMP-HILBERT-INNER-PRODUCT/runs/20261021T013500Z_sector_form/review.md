# Mathematical review and boundaries

AuthorityEffect: None.

## The question

The L1 to L2 lift admits a Hilbert inner product on the linearised sector carrier (node
L1-IMP-HILBERT-INNER-PRODUCT). H005 shows the admission is not forced by the carrier: the standard form
and `diag(1, 2)` are both positive definite on the same two-sector carrier (`gram_not_unique`), and the
19 October audit added `diag(2, 3)`. The reason is a gauge freedom: the l1 data only fix the squared
amplitudes `|c_i|² = w_i` (QM_020 Thm 4), and a diagonal Gram weight can be absorbed into the amplitude
of each sector. So the carrier plus weights cannot see the Gram diagonal, and something else must pin it.

## What is established

Let `V = Fin n → ℚ` (or `Fin n → ℚ(i)`) and let a candidate form be a symmetric (Hermitian) Gram
matrix `G` with readout `qf G x = x ⬝ᵥ (G *ᵥ x)` (`hf H x = re (x* H x)`), the readout the Born carriers
`BornMatrixCarrier` / `BornHermitianCarrier` already use to order effects. Two laws are imposed on the
readout:

1. **Sector additivity.** `qf G (u + v) = qf G u + qf G v` whenever `u` and `v` have disjoint sector
   supports. This is the quadratic transcription of edgewise l1 additivity: the l1 sector weight obeys
   exactly this law on disjoint supports (`l1_disjoint_additive`; L1-GS000-EDGEWISE-L1, and the D1
   additivity defect of QM_020 Thm 2a vanishes on disjoint supports of the same sign).
2. **Sector symmetry.** The readout is invariant under a set `S` of sector permutations whose generated
   group acts transitively on sectors (`Invariant`, `Generated`, `TransitiveOn`). This is the
   permutation-isometry envelope of H006 taken as a law of the readout.

Then:

- **Orthogonality** (`offdiag_pair_sum_eq_zero`, `offdiag_eq_zero`, `qf_eq_sum_diag_sq_of_sectorAdditive`).
  Evaluating additivity on the pair `(e_i, e_j)` gives `G i j + G j i = 0`; with symmetry `G i j = 0`.
  Without symmetry the readout is still `Σ G i i · x i²`, because the skew part of `G` is invisible to
  the readout (`qf_eq_zero_of_skew`). This is the content of L1-IMP-ORTHOGONAL-ADDITIVITY, obtained from
  the additivity law alone: the sector basis is orthogonal for every sector-additive form.
  Over `ℚ(i)` additivity is tested along two directions in each pair, `e_j` and `i·e_j`; the first kills
  `re(H i j + H j i)`, the second `im(H j i − H i j)`, and `Hᴴ = H` gives `H i j = 0`. The control
  `imagLeak12 = [[1, i], [−i, 1]]` is Hermitian and additive on `(e₀, e₁)` along the real direction but
  not along `(e₀, i·e₁)`: the second direction is needed.
- **Collapse** (`diag_eq_of_invariant`, `diag_const_of_transitive`, `eq_smul_one`, `eq_smul_one_generated`).
  Invariance under `σ` applied to `e_j` gives `G (σ j) (σ j) = G j j`; invariance is closed under
  products and inverses (`invariant_mul`, `invariant_inv`), so it holds on the generated group, and
  transitivity makes the diagonal constant. Hence `G = c • 1` with `c = G i₀ i₀` (over `ℚ(i)`:
  `c = re H i₀ i₀`, a rational scalar), the readout is `c · (x ⬝ᵥ x)` and the pairing `c · (x ⬝ᵥ y)`.
  `c > 0` when the readout is positive definite (`scale_pos`).
- **Uniqueness and nonvacuity.** Two forms satisfying the laws agree once one diagonal entry is matched
  (`unique_of_normalized`) and are proportional in general (`unique_up_to_scale`); the unit-normalised
  selected form is `1` (`eq_one_of_normalized`), i.e. exactly the `qf 1` / `hf 1` of the Born carriers.
  `1` satisfies both laws (`one_sectorAdditive`, `one_invariant`) and is positive definite.
- **Countermodels, each hypothesis used.** `diag(1, 2)` is symmetric, positive definite and sector
  additive but not invariant under the swap and not scalar (`diag12_not_invariant_swap`,
  `diag12_not_scalar`): the H005 non-uniqueness is exactly the failure of the symmetry law.
  `1 + (all ones) = [[2, 1], [1, 2]]` is symmetric, positive definite and invariant under the swap,
  which generates a transitive group, but not sector additive and not scalar
  (`unif12_not_sectorAdditive`, `unif12_not_scalar`).

The Python and Rust twins replay the chain exactly on supplied matrices: the pair sums as additivity
defects, the diagonal readout, the invariance defects, the generated group and its orbits, the scale
certificate with an exact witness for whichever hypothesis fails first, and the countermodels.

## Consequence for the Born chain

The effect-additive Born representation (runs 20261020T205000Z and 20261020T224000Z) took the carrier
with its standard form and effect additivity as inputs, and its open item 2 asked for the operational
source of effect additivity. The present run shows that the standard form is not a free choice: given
sector additivity and transitive sector symmetry of the readout, it is the unique form up to a unit
scale, and the orthogonality of the sector basis that effect additivity on projections presupposes is a
theorem rather than an import. The remaining imports under the Born chain are the scalar field, the
quadratic shape of the readout, and the two laws themselves.

## What is supplied, not derived

- The sector carrier `Fin n → ℚ` (or `ℚ(i)`), the scalar field, and the quadratic shape of the readout
  are inputs. Nothing derives them from primitive difference.
- Sector additivity of the quadratic readout is a hypothesis. It is transcribed from the l1 additivity
  law of the sector weights, but the step from "weights are l1 additive" to "the quadratic readout of
  the lift is additive on disjoint supports" is itself an assumption about the lift.
- Transitive sector symmetry is a hypothesis: the finite theory supplies a permutation envelope (H006),
  not a statement that the readout must be invariant under it; sectors with distinguished labels would
  break it, and then the diagonal is only constant on orbits (`diag_const_of_transitive` for each
  orbit; the twins report the orbit values).
- The scale `c` is a unit choice; `c > 0` needs positive definiteness, which is assumed, not derived.
- No continuity, no real numbers, no complex numbers: everything is exact over `ℚ` and `ℚ(i)`.

## Mechanical notes

Lean 4.33.1, pinned Mathlib cache, targeted imports; accepted receipts `s01` (`SectorFormUniqueness`)
and `h01` (`SectorFormHermitian`) by `tools/replay.py` with the sealed oleans of `BornEffectValuation`,
`BornMatrixCarrier`, `BornGaussRat`, `BornHermitianCarrier` and `BornHermitianPsdDecomposition` restored
into `build/` from the Born runs' receipts; `tools/seal.py receipts` checks exit codes, custody digests,
absence of `sorry`/`axiom`/`opaque`/`unsafe`, absence of diagnostics, and that every printed axiom list
is within `{propext, Classical.choice, Quot.sound}`. No noncomputable definitions are introduced.
