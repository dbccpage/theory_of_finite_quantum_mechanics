import Mathlib.Algebra.Group.Defs
import CausalOrder
import FrontierPosetNet
import FrontierLinearExtension

/-!
# Campaign: CQFT-CAUSAL-FACTORIZATION-IMPORT (TFQ-2109) — Bogoliubov Relative S-Matrix Algebra, Poset-N Swap Connectivity, and Diagonal Counterterm Fence

AuthorityEffect: None.

This module narrows `CQFT-CAUSAL-FACTORIZATION-IMPORT` (`TFQ-2109`, stage `CAUSAL_QFT`,
status `IMPORTED_ASSUMPTION`, audited against Epstein and Glaser 1973, Section 1.1 pp. 214–215,
Section 2.1 eq. (9) p. 218, Section 2.2 eq. (30) p. 223, and Brunetti and Fredenhagen 2000,
`arXiv:math-ph/9903028`, Section 1 eq. (2) p. 4 and Section 3 Condition P3 p. 15) into three
exact finite/algebraic components and non-equivalence fences:

1. **Abstract Bogoliubov Relative S-Matrix Algebra (`V(g, h) = S(g)⁻¹ S(g + h)`) and Causal Asymmetry**:
   - Over any group `G` and additive coupling carrier `A`, the relative Bogoliubov scattering
     operator `bogoliubovV S g h = (S g)⁻¹ * S (g + h)` satisfies the identity law
     `bogoliubovV S g 0 = 1` (`bogoliubovV_zero`) and the unconditional telescoping cocycle law
     `bogoliubovV S g h1 * bogoliubovV S (g + h1) h2 = bogoliubovV S g (h1 + h2)`
     (`bogoliubovV_cocycle_telescoping`).
   - Consequently, Epstein-Glaser causal factorization
     `bogoliubovV S g (h1 + h2) = bogoliubovV S g h1 * bogoliubovV S g h2` holds if and only if
     switching on `h1` outside the causal past of `h2` leaves the relative S-matrix for `h2`
     invariant: `bogoliubovV S (g + h1) h2 = bogoliubovV S g h2`
     (`bogoliubovV_factorization_iff_background_shift_invariance`), and at `g = 0` (`S 0 = 1`)
     reduces to `S (h1 + h2) = S h1 * S h2` (`bogoliubovV_causal_factorization_at_zero_iff`).
   - On the finite diamond poset `C2`, the Epstein-Glaser condition `noInCausalPast P L₁ L₂`
     (`L₁ ∩ I⁻(L₂) = ∅`) holds symmetrically for spacelike pairs (`([d1], [d2])` and `([d2], [d1])`)
     and asymmetrically for future-before-past splits (`([d1, d2, d3], [d0])` vs. `([d0], [d1, d2, d3])`)
     (`c2_epstein_glaser_separation_asymmetry`).

2. **Complete Adjacent-Spacelike-Swap Connectivity and Ordered-Product Equality on `posetN`**:
   - Discharging the explicit finite-poset connectivity question noted in `TFQ-2110`
     (`CQFT-ORDERED-PRODUCT-LINEAR-EXTENSION-TARGET`), we prove that all `5` linear extensions
     `extN0, extN1, extN2, extN3, extN4` of the 4-element `N` poset (`0 < 2`, `1 < 2`, `1 < 3`)
     are connected by chains of adjacent spacelike swaps (`posetN_all_five_extensions_swap_connected`),
     and that for every monoid `M` and spacelike-commuting operator assignment `A : Fin 4 → M`,
     all `5` linear extensions yield the identical ordered product
     (`posetN_all_five_ordered_products_eq`), while anticommuting Pauli operators `X, Z` on the
     spacelike pair `(n0, n3)` flip the sign between `extN3` and `extN4`
     (`posetN_pauli_commuting_vs_anticommuting_witness`).

3. **Coincident-Diagonal Renormalization Ambiguity Fence (`Δ_n` Distribution Extension vs. Finite Posets)**:
   - By `spacelike_irrefl`, no vertex `x` of a `FiniteStrictPoset n` is spacelike to itself, and on
     a two-point kernel `twoPointKernelWithCounterterm T1 c x y`, off-diagonal factorization (`x ≠ y`)
     is completely invariant under any diagonal counterterm `c : Int`, whereas the coincident diagonal
     `x = y` shifts by `c₁ - c₂ ≠ 0` (`diagonal_counterterm_preserves_off_diagonal_factorization`),
     mirroring the $\binom{\omega + 4}{4}$-parameter Epstein-Glaser polynomial counterterm freedom at
     singular order $\omega \ge 0$ (`coincident_diagonal_not_spacelike_and_counterterm_dim`).
-/

namespace CampaignCqftCausalFactorizationImport

open CausalOrder
open FrontierPosetNet
open FrontierLinearExtension

-- ============================================================================
-- 1. Bogoliubov Relative S-Matrix Algebra (`V(g, h) = S(g)⁻¹ S(g + h)`)
-- ============================================================================

/-- Relative Bogoliubov scattering operator `V(g, h) = S(g)⁻¹ * S(g + h)` from Epstein-Glaser (1973)
Section 2.1 eq. (9) p. 218 and Brunetti-Fredenhagen (2000) Section 1 eq. (2) p. 4. -/
def bogoliubovV {A G : Type*} [Add A] [Group G] (S : A → G) (g h : A) : G :=
  (S g)⁻¹ * S (g + h)

/-- Theorem 1: At zero perturbation `h = 0`, the relative Bogoliubov operator is the identity:
`bogoliubovV S g 0 = 1`. -/
theorem bogoliubovV_zero {A G : Type*} [AddZeroClass A] [Group G] (S : A → G) (g : A) :
    bogoliubovV S g 0 = 1 := by
  dsimp [bogoliubovV]
  rw [add_zero, inv_mul_cancel]

/-- Theorem 2: Unconditional telescoping cocycle law for the relative Bogoliubov operator:
`V(g, h1) * V(g + h1, h2) = V(g, h1 + h2)` in any group `G` and additive semigroup `A`. -/
theorem bogoliubovV_cocycle_telescoping {A G : Type*} [AddSemigroup A] [Group G]
    (S : A → G) (g h1 h2 : A) :
    bogoliubovV S g h1 * bogoliubovV S (g + h1) h2 = bogoliubovV S g (h1 + h2) := by
  dsimp [bogoliubovV]
  rw [mul_assoc, ← mul_assoc (S (g + h1)), mul_inv_cancel, one_mul, add_assoc]

/-- Theorem 3: Epstein-Glaser causal factorization `V(g, h1 + h2) = V(g, h1) * V(g, h2)` holds
if and only if switching on `h1` leaves the relative S-matrix for `h2` invariant:
`V(g + h1, h2) = V(g, h2)` (Epstein-Glaser 1973 Section 2.1 Condition (Caus. 1) eq. (9)). -/
theorem bogoliubovV_factorization_iff_background_shift_invariance
    {A G : Type*} [AddSemigroup A] [Group G] (S : A → G) (g h1 h2 : A) :
    bogoliubovV S g (h1 + h2) = bogoliubovV S g h1 * bogoliubovV S g h2 ↔
      bogoliubovV S (g + h1) h2 = bogoliubovV S g h2 := by
  rw [← bogoliubovV_cocycle_telescoping S g h1 h2]
  constructor
  · intro h
    exact mul_left_cancel h
  · intro h
    rw [h]

/-- Theorem 4: At zero background coupling `g = 0` with `S 0 = 1`, Bogoliubov factorization
`V(0, h1 + h2) = V(0, h1) * V(0, h2)` is equivalent to `S (h1 + h2) = S h1 * S h2`. -/
theorem bogoliubovV_causal_factorization_at_zero_iff
    {A G : Type*} [AddZeroClass A] [Group G] (S : A → G) (hS0 : S 0 = 1) (h1 h2 : A) :
    bogoliubovV S 0 (h1 + h2) = bogoliubovV S 0 h1 * bogoliubovV S 0 h2 ↔
      S (h1 + h2) = S h1 * S h2 := by
  have hinv1 : (1 : G)⁻¹ = 1 := by
    rw [← mul_one (1 : G)⁻¹, inv_mul_cancel]
  dsimp [bogoliubovV]
  rw [hS0, hinv1, zero_add, zero_add, zero_add, one_mul, one_mul, one_mul]

/-- Finite-poset counterpart of the Epstein-Glaser support condition
`supp h1 ∩ (supp h2 + V⁻) = ∅`: no vertex `x ∈ L₁` lies in the strict causal past (`P.rel x y`)
of any vertex `y ∈ L₂`. This holds both when `L₁` and `L₂` are elementwise spacelike and when
`L₁` lies in the causal future of `L₂`. -/
def noInCausalPast {n : Nat} (P : FiniteStrictPoset n) (L₁ L₂ : List (Fin n)) : Bool :=
  L₁.all fun x => L₂.all fun y => !(decide (P.rel x y))

/-- Elementwise spacelike separation between two vertex lists `L₁` and `L₂`. -/
def allSpacelikeBetween {n : Nat} (P : FiniteStrictPoset n) (L₁ L₂ : List (Fin n)) : Bool :=
  L₁.all fun x => L₂.all fun y => decide (isSpacelike P x y)

/-- Theorem 5: On the 4-element diamond poset `C2` (`0 < 1, 0 < 2, 1 < 3, 2 < 3`), the
Epstein-Glaser condition `noInCausalPast C2` strictly generalizes symmetric spacelike separation:
it holds in both directions for the spacelike pair `([d1], [d2])`, holds one-way for the
future-before-past partition `([d1, d2, d3], [d0])` (where `allSpacelikeBetween` is `false`),
and fails for the reversed past-before-future partition `([d0], [d1, d2, d3])`. -/
theorem c2_epstein_glaser_separation_asymmetry :
    allSpacelikeBetween C2 [d1] [d2] = true ∧
    noInCausalPast C2 [d1] [d2] = true ∧
    noInCausalPast C2 [d2] [d1] = true ∧
    noInCausalPast C2 [d1, d2, d3] [d0] = true ∧
    allSpacelikeBetween C2 [d1, d2, d3] [d0] = false ∧
    noInCausalPast C2 [d0] [d1, d2, d3] = false := by
  decide

-- ============================================================================
-- 2. Complete Linear-Extension Swap Connectivity on the 4-Element `N` Poset
-- ============================================================================

/-- The five linear extensions of the 4-element `N` poset (`0 < 2`, `1 < 2`, `1 < 3`). -/
def extN0 : List (Fin 4) := [n0, n1, n2, n3]
def extN1 : List (Fin 4) := [n0, n1, n3, n2]
def extN2 : List (Fin 4) := [n1, n0, n2, n3]
def extN3 : List (Fin 4) := [n1, n0, n3, n2]
def extN4 : List (Fin 4) := [n1, n3, n0, n2]

/-- Theorem 6: All three unordered spacelike pairs `{n0, n1}`, `{n2, n3}`, and `{n0, n3}` on
`posetN` satisfy `isSpacelike posetN` in both directions. -/
theorem posetN_all_spacelike_pairs :
    isSpacelike posetN n0 n1 ∧
    isSpacelike posetN n1 n0 ∧
    isSpacelike posetN n2 n3 ∧
    isSpacelike posetN n3 n2 ∧
    isSpacelike posetN n0 n3 ∧
    isSpacelike posetN n3 n0 := by
  decide

/-- Theorem 7: Among all 24 permutations of `Fin 4`, the exact linear extensions of `posetN`
have count `5` and include `extN0, extN1, extN2, extN3, extN4`. -/
theorem posetN_exact_five_linear_extensions :
    (allPerms4.filter (isLinearExtension posetN)).length = 5 ∧
    extN0 ∈ allPerms4.filter (isLinearExtension posetN) ∧
    extN1 ∈ allPerms4.filter (isLinearExtension posetN) ∧
    extN2 ∈ allPerms4.filter (isLinearExtension posetN) ∧
    extN3 ∈ allPerms4.filter (isLinearExtension posetN) ∧
    extN4 ∈ allPerms4.filter (isLinearExtension posetN) := by
  decide

/-- Theorem 8: All five linear extensions of `posetN` are connected to `extN0` by chains of
adjacent spacelike swaps (`SpacelikeSwapChain posetN`), discharging the finite-poset connectivity
question for `posetN` noted in `TFQ-2110`. -/
theorem posetN_all_five_extensions_swap_connected :
    SpacelikeSwapChain posetN extN0 extN1 ∧
    SpacelikeSwapChain posetN extN0 extN2 ∧
    SpacelikeSwapChain posetN extN0 extN3 ∧
    SpacelikeSwapChain posetN extN0 extN4 := by
  have h01 : AdjSpacelikeSwap posetN extN0 extN1 :=
    ⟨[n0, n1], [], n2, n3, by decide, rfl, rfl⟩
  have h02 : AdjSpacelikeSwap posetN extN0 extN2 :=
    ⟨[], [n2, n3], n0, n1, by decide, rfl, rfl⟩
  have h23 : AdjSpacelikeSwap posetN extN2 extN3 :=
    ⟨[n1, n0], [], n2, n3, by decide, rfl, rfl⟩
  have h34 : AdjSpacelikeSwap posetN extN3 extN4 :=
    ⟨[n1], [n2], n0, n3, by decide, rfl, rfl⟩
  refine ⟨?_, ?_, ?_, ?_⟩
  · exact SpacelikeSwapChain.step h01 (SpacelikeSwapChain.refl _)
  · exact SpacelikeSwapChain.step h02 (SpacelikeSwapChain.refl _)
  · exact SpacelikeSwapChain.step h02 (SpacelikeSwapChain.step h23 (SpacelikeSwapChain.refl _))
  · exact SpacelikeSwapChain.step h02
      (SpacelikeSwapChain.step h23 (SpacelikeSwapChain.step h34 (SpacelikeSwapChain.refl _)))

/-- Theorem 9: For every monoid `M` and operator assignment `A : Fin 4 → M` that commutes on all
spacelike pairs of `posetN`, all five linear extensions of `posetN` have identical ordered
products `orderedProd A extNk = orderedProd A extN0`. -/
theorem posetN_all_five_ordered_products_eq {M : Type*} [Monoid M] (A : Fin 4 → M)
    (hcomm : ∀ x y : Fin 4, isSpacelike posetN x y → A x * A y = A y * A x) :
    orderedProd A extN1 = orderedProd A extN0 ∧
    orderedProd A extN2 = orderedProd A extN0 ∧
    orderedProd A extN3 = orderedProd A extN0 ∧
    orderedProd A extN4 = orderedProd A extN0 := by
  rcases posetN_all_five_extensions_swap_connected with ⟨c1, c2, c3, c4⟩
  refine ⟨?_, ?_, ?_, ?_⟩
  · exact (orderedProd_eq_of_spacelikeSwapChain posetN A hcomm c1).symm
  · exact (orderedProd_eq_of_spacelikeSwapChain posetN A hcomm c2).symm
  · exact (orderedProd_eq_of_spacelikeSwapChain posetN A hcomm c3).symm
  · exact (orderedProd_eq_of_spacelikeSwapChain posetN A hcomm c4).symm

/-- Assignment on `posetN` placing commuting `pauliZ` on `n0, n3` and `pauliI` on `n1, n2`. -/
def assignCommN : Fin 4 → Mat2Int
  | ⟨0, _⟩ => pauliZ
  | ⟨1, _⟩ => pauliI
  | ⟨2, _⟩ => pauliI
  | ⟨3, _⟩ => pauliZ

/-- Assignment on `posetN` placing anticommuting `pauliX` and `pauliZ` on the spacelike pair
`(n0, n3)` and `pauliI` on `n1, n2`. -/
def assignAnticommN : Fin 4 → Mat2Int
  | ⟨0, _⟩ => pauliX
  | ⟨1, _⟩ => pauliI
  | ⟨2, _⟩ => pauliI
  | ⟨3, _⟩ => pauliZ

/-- Theorem 10: On `posetN`, when the spacelike pair `(n0, n3)` carries commuting Pauli matrices,
all five linear extensions yield the same 2×2 matrix product, whereas when `(n0, n3)` carries
anticommuting Pauli matrices `X` and `Z`, the adjacent spacelike swap `extN3 ↔ extN4` flips the
sign of the ordered product (`orderedProd assignAnticommN extN3 = negMat2 (orderedProd assignAnticommN extN4)`). -/
theorem posetN_pauli_commuting_vs_anticommuting_witness :
    orderedProd assignCommN extN0 = orderedProd assignCommN extN4 ∧
    orderedProd assignAnticommN extN0 = orderedProd assignAnticommN extN3 ∧
    orderedProd assignAnticommN extN3 = negMat2 (orderedProd assignAnticommN extN4) ∧
    orderedProd assignAnticommN extN3 ≠ orderedProd assignAnticommN extN4 := by
  decide

-- ============================================================================
-- 3. Coincident-Diagonal Renormalization Ambiguity Fence (`Δ_n` Extension)
-- ============================================================================

/-- Dimension `binom(omega + 4, 4)` of the space of polynomial renormalization counterterms
`∑_{|α| ≤ ω} C_α ∂^α δ(x - y)` of singular degree `ω ≥ 0` in 4D Minkowski spacetime
(Epstein-Glaser 1973 Section 2.2; Brunetti-Fredenhagen 2000 Section 3). -/
def egCountertermDim4D (omega : Nat) : Nat :=
  (omega + 1) * (omega + 2) * (omega + 3) * (omega + 4) / 24

/-- Two-point kernel on `Fin n` with coincident-diagonal contact counterterm `c : Int`:
off the diagonal (`x ≠ y`) it factorizes as `T1 x * T1 y`; on the coincident diagonal (`x = y`)
it carries the contact counterterm `T1 x * T1 x + c`. -/
def twoPointKernelWithCounterterm {n : Nat} (T1 : Fin n → Int) (c : Int) (x y : Fin n) : Int :=
  if x = y then T1 x * T1 x + c else T1 x * T1 y

/-- Theorem 11: By irreflexivity (`spacelike_irrefl`), no coincident pair `(x, x)` on the diagonal
of a `FiniteStrictPoset n` is spacelike separated, and in 4D the Epstein-Glaser polynomial
counterterm dimension at singular degrees `ω = 0, 1, 2, 3, 4` is `1, 5, 15, 35, 70`. -/
theorem coincident_diagonal_not_spacelike_and_counterterm_dim :
    (∀ {n : Nat} (P : FiniteStrictPoset n) (x : Fin n), ¬ isSpacelike P x x) ∧
    egCountertermDim4D 0 = 1 ∧
    egCountertermDim4D 1 = 5 ∧
    egCountertermDim4D 2 = 15 ∧
    egCountertermDim4D 3 = 35 ∧
    egCountertermDim4D 4 = 70 := by
  refine ⟨fun P x => spacelike_irrefl P x, by decide, by decide, by decide, by decide, by decide⟩

/-- Theorem 12: Off-diagonal causal factorization (`x ≠ y`) is invariant under any coincident-point
counterterm `c`, whereas on the coincident diagonal (`x = y`) two extensions with `c₁ ≠ c₂`
differ by `c₁ - c₂ ≠ 0`, so off-diagonal causal factorization alone never fixes the diagonal
extension. -/
theorem diagonal_counterterm_preserves_off_diagonal_factorization
    {n : Nat} (T1 : Fin n → Int) (c1 c2 : Int) (x y : Fin n) :
    (x ≠ y → twoPointKernelWithCounterterm T1 c1 x y = twoPointKernelWithCounterterm T1 c2 x y) ∧
    twoPointKernelWithCounterterm T1 c1 x x - twoPointKernelWithCounterterm T1 c2 x x = c1 - c2 := by
  refine ⟨?_, ?_⟩
  · intro hne
    simp [twoPointKernelWithCounterterm, hne]
  · simp [twoPointKernelWithCounterterm]
    omega

end CampaignCqftCausalFactorizationImport

#print axioms CampaignCqftCausalFactorizationImport.bogoliubovV_zero
#print axioms CampaignCqftCausalFactorizationImport.bogoliubovV_cocycle_telescoping
#print axioms CampaignCqftCausalFactorizationImport.bogoliubovV_factorization_iff_background_shift_invariance
#print axioms CampaignCqftCausalFactorizationImport.bogoliubovV_causal_factorization_at_zero_iff
#print axioms CampaignCqftCausalFactorizationImport.c2_epstein_glaser_separation_asymmetry
#print axioms CampaignCqftCausalFactorizationImport.posetN_all_spacelike_pairs
#print axioms CampaignCqftCausalFactorizationImport.posetN_exact_five_linear_extensions
#print axioms CampaignCqftCausalFactorizationImport.posetN_all_five_extensions_swap_connected
#print axioms CampaignCqftCausalFactorizationImport.posetN_all_five_ordered_products_eq
#print axioms CampaignCqftCausalFactorizationImport.posetN_pauli_commuting_vs_anticommuting_witness
#print axioms CampaignCqftCausalFactorizationImport.coincident_diagonal_not_spacelike_and_counterterm_dim
#print axioms CampaignCqftCausalFactorizationImport.diagonal_counterterm_preserves_off_diagonal_factorization

private def l5aProvenance : String :=
  "Origin: lean4/CampaignCqftCausalFactorizationImport.lean Claim: CQFT-CAUSAL-FACTORIZATION-IMPORT AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
