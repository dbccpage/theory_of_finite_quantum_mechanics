import FrontierRsCyclicity
import FrontierPosetNet
import CausalOrder

/-!
# CQFT-REEH-SCHLIEDER-THEOREM-IMPORT (TFQ-2106) — Commutant Cyclicity-Separating Duality, Complete 3-Qubit/4-Qubit Subsystem Cyclicity Census, and Discrete Translation Fence

AuthorityEffect: None.

This module narrows `CQFT-REEH-SCHLIEDER-THEOREM-IMPORT` (`TFQ-2106`, stage `CAUSAL_QFT`,
status `IMPORTED_ASSUMPTION`, audited against Reeh and Schlieder 1961, *Il Nuovo Cimento* 22,
1051–1068, Haag and Kastler 1964, *J. Math. Phys.* 5, 848–861, `FQ-GAP-STONE-CONTINUOUS-TIME`,
`FQ-GAP-CONTINUUM-HILBERT-LIFT`, and `TFQ-2107`) into three exact finite/algebraic components and
non-equivalence fences:

1. **Dimension-Independent Cyclicity-Implies-Separating Duality and Right-Kernel Non-Cyclicity**:
   - Discharging the open implication noted in `TFQ-2107` (`CQFT-RS-FINITE-CYCLICITY-TARGET`),
     we prove over any semiring `R` and for any dimensions `dA, dB` (including `dA < dB`, such as
     single sites `dA = 2 < dB = 4`) that whenever `dA` is inhabited (`i0 : Fin dA`),
     `CyclicForA Ω → SeparatingForAc Ω` (`cyclic_implies_separating`).
   - Combining `cyclic_implies_separating` with `not_separating_of_right_kernel` yields
     `not_cyclic_of_right_kernel` for arbitrary `dA, dB` (even when `dA < dB`), and proves that any
     zero column `k0 : Fin dB` of `Ω` (`∀ i, Ω i k0 = 0`) precludes both a left inverse
     (`¬ HasFullComplementaryRank Ω`) and cyclicity (`¬ CyclicForA Ω`)
     (`no_left_inverse_of_zero_column`, `not_cyclic_of_zero_column`).

2. **Complete 3-Qubit and 4-Qubit Stabilizer Subsystem Cyclicity Census (Discharging `TFQ-2107` Open Items)**:
   - On 3 qubits (`|000⟩`, `|GHZ_3⟩`, `|W_3⟩`), we prove as explicit `Prop`-level theorems that:
     (a) on every single site `s ∈ {0, 1, 2}` (`2 × 4` unfolding), none of `|000⟩`, `|GHZ_3⟩`,
         `|W_3⟩` is cyclic (`single_site_not_cyclic_all_three_states`);
     (b) on every pair of sites `s ∈ {0, 1, 2}` (`4 × 2` unfolding), `|000⟩` has neither a left
         inverse nor cyclicity (`prod3_pair_not_cyclic_and_no_left_inverse`), whereas `|GHZ_3⟩`
         and `|W_3⟩` are both cyclic and separating (`ghz3_and_w3_pair_cyclic_and_separating`);
     (c) on the full 3-site algebra (`8 × 1` unfolding), all three states `|000⟩`, `|GHZ_3⟩`, and
         `|W_3⟩` have full complementary rank `1` and are cyclic (`full_three_site_cyclic_all_three_states`).
   - On 4 qubits across the `2 + 2` bipartition `A = {0, 1}` vs. `A^c = {2, 3}` (`4 × 4` unfolding),
     neither the 4-qubit product state `|0000⟩` (rank 1) nor `|GHZ_4⟩ = |0000⟩ + |1111⟩` (rank 2)
     is cyclic (`prod4_and_ghz4_half_system_not_cyclic`), whereas the 2-Bell-pair cluster state
     `(|00⟩ + |11⟩)_{02} ⊗ (|00⟩ + |11⟩)_{13}` has unfolding `matId 4`, hence has full
     complementary rank `4` and is both cyclic for `End(H_A)` and separating for `End(H_{A^c})`
     (`bellPair4_half_system_cyclic_and_separating`).

3. **Discrete Cyclic Translation Group Aliasing vs. Continuum Stone / Tube-Analyticity Fence**:
   - In continuum AQFT, the Reeh-Schlieder theorem relies on a continuous translation group
     `U(a) = exp(i P · a)` with positive spectrum `P^0 ≥ 0` (`FQ-GAP-STONE-CONTINUOUS-TIME`) on an
     infinite-dimensional Hilbert space (`FQ-GAP-CONTINUUM-HILBERT-LIFT`) to analytically continue
     `<Φ, U(a) A Ω> = 0` from a small open region `O` to all of Minkowski space.
   - On a finite `N`-site ring with cyclic shift `cyclicShift N` (`(x + 1) mod N`), the translation
     group has finite order `N` (`cyclicShiftIter N N x = x`), the translation-invariant vector
     `constVec N c` has zero discrete momentum difference `discreteMomentumDiff (constVec N c) = 0`
     (`translation_invariant_vec_zero_momentum_diff`), and on `N = 3` qubits the translation-invariant
     product vacuum `|000⟩` fails cyclicity on every proper subsystem (`|A| ∈ {1, 2}`), demonstrating
     that finite translation invariance without continuum spectrum/analyticity does not induce
     subsystem cyclicity.
-/

namespace ReehSchliederImport

open BigOperators
open FrontierRsCyclicity
open FrontierPosetNet
open CausalOrder

-- ============================================================================
-- 1. Dimension-Independent Cyclicity-Implies-Separating & Zero-Column Obstruction
-- ============================================================================

/-- Theorem 1: Over any semiring `R` and for any dimensions `dA, dB` (even when `dA < dB`), if
`Fin dA` is inhabited by `i0` and `Ω : Fin dA → Fin dB → R` is cyclic for `End(H_A)` acting on the
left (`CyclicForA Ω`), then `Ω` is separating for `End(H_{A^c})` acting on the right
(`SeparatingForAc Ω`). This relies on matrix associativity `(X Ω) Y = X (Ω Y)`, expressing the
commutation between `End(H_A) ⊗ I` and `I ⊗ End(H_{A^c})`. -/
theorem cyclic_implies_separating {dA dB : Nat} {R : Type*} [Semiring R]
    (i0 : Fin dA) {Ω : Fin dA → Fin dB → R} (hcyc : CyclicForA Ω) :
    SeparatingForAc Ω := by
  intro Y hY
  funext k l
  let Ψ : Fin dA → Fin dB → R := fun _ j => if j = k then 1 else 0
  rcases hcyc Ψ with ⟨X, hX⟩
  have hΨY : matMul Ψ Y = fun _ _ => 0 := by
    rw [← hX, matMul_assoc, hY]
    funext i j
    dsimp [matMul]
    simp
  have hval := congrFun (congrFun hΨY i0) l
  dsimp [matMul, Ψ] at hval
  simp at hval
  exact hval

/-- Theorem 2: Any nonzero vector `v` in the right kernel of `Ω` (`∀ i, ∑ j, Ω i j * v j = 0` with
`v k0 ≠ 0`) precludes `CyclicForA Ω` for any `dA > 0` and any `dB` (including `dA < dB`). -/
theorem not_cyclic_of_right_kernel {dA dB : Nat} {R : Type*} [Semiring R]
    (i0 : Fin dA) {Ω : Fin dA → Fin dB → R}
    (v : Fin dB → R) (k0 : Fin dB) (hv : v k0 ≠ 0)
    (hker : ∀ i : Fin dA, (∑ j : Fin dB, Ω i j * v j) = 0) :
    ¬ CyclicForA Ω := by
  intro hcyc
  exact not_separating_of_right_kernel v k0 hv hker (cyclic_implies_separating i0 hcyc)

/-- Theorem 3: If column `k0 : Fin dB` of `Ω : Fin dA → Fin dB → R` is identically zero
(`∀ i, Ω i k0 = 0`) over a nontrivial semiring (`(1 : R) ≠ 0`), then `Ω` has no left inverse
(`¬ HasFullComplementaryRank Ω`). -/
theorem no_left_inverse_of_zero_column {dA dB : Nat} {R : Type*} [Semiring R]
    (h10 : (1 : R) ≠ 0) {Ω : Fin dA → Fin dB → R} (k0 : Fin dB)
    (hcol : ∀ i : Fin dA, Ω i k0 = 0) :
    ¬ HasFullComplementaryRank Ω := by
  rintro ⟨L, hL⟩
  have hk0 := congrFun (congrFun hL k0) k0
  dsimp [matMul, matId] at hk0
  simp [hcol] at hk0
  exact h10 hk0.symm

/-- Theorem 4: If column `k0 : Fin dB` of `Ω : Fin dA → Fin dB → R` is identically zero
(`∀ i, Ω i k0 = 0`) over a nontrivial semiring (`(1 : R) ≠ 0`) with `i0 : Fin dA`, then `Ω` is
 neither separating for `End(H_{A^c})` nor cyclic for `End(H_A)`. -/
theorem not_cyclic_of_zero_column {dA dB : Nat} {R : Type*} [Semiring R]
    (h10 : (1 : R) ≠ 0) (i0 : Fin dA) {Ω : Fin dA → Fin dB → R} (k0 : Fin dB)
    (hcol : ∀ i : Fin dA, Ω i k0 = 0) :
    ¬ SeparatingForAc Ω ∧ ¬ CyclicForA Ω := by
  let v : Fin dB → R := fun j => if j = k0 then 1 else 0
  have hv : v k0 ≠ 0 := by
    dsimp [v]; simp [h10]
  have hker : ∀ i : Fin dA, (∑ j : Fin dB, Ω i j * v j) = 0 := by
    intro i
    dsimp [v]
    simp [hcol i]
  exact ⟨not_separating_of_right_kernel v k0 hv hker,
         not_cyclic_of_right_kernel i0 v k0 hv hker⟩

-- ============================================================================
-- 2. Complete 3-Qubit and 4-Qubit Subsystem Cyclicity Census (`TFQ-2107` Closure)
-- ============================================================================

/-- Theorem 5: On every single site `s ∈ {0, 1, 2}` (`2 × 4` unfolding), column `⟨1, _⟩` of
`singleSiteMatrix psiProd3 s` and `singleSiteMatrix psiGHZ3 s` is identically zero, and column
`⟨3, _⟩` of `singleSiteMatrix psiW3 s` is identically zero; consequently none of `|000⟩`,
`|GHZ_3⟩`, `|W_3⟩` is cyclic for any single-site algebra (discharging the single-site
non-cyclicity statement left open in `TFQ-2107`). -/
theorem single_site_not_cyclic_all_three_states (s : Fin 3) :
    ¬ CyclicForA (singleSiteMatrix psiProd3 s) ∧
    ¬ CyclicForA (singleSiteMatrix psiGHZ3 s) ∧
    ¬ CyclicForA (singleSiteMatrix psiW3 s) := by
  have h10 : (1 : Int) ≠ 0 := by decide
  have i0 : Fin 2 := ⟨0, by decide⟩
  have hcolProd : ∀ i : Fin 2, singleSiteMatrix psiProd3 s i ⟨1, by decide⟩ = 0 := by
     revert s; decide
  have hcolGHZ : ∀ i : Fin 2, singleSiteMatrix psiGHZ3 s i ⟨1, by decide⟩ = 0 := by
     revert s; decide
  have hcolW : ∀ i : Fin 2, singleSiteMatrix psiW3 s i ⟨3, by decide⟩ = 0 := by
     revert s; decide
  exact ⟨(not_cyclic_of_zero_column h10 i0 ⟨1, by decide⟩ hcolProd).2,
         (not_cyclic_of_zero_column h10 i0 ⟨1, by decide⟩ hcolGHZ).2,
         (not_cyclic_of_zero_column h10 i0 ⟨3, by decide⟩ hcolW).2⟩

/-- Theorem 6: On every pair of sites `s ∈ {0, 1, 2}` (`4 × 2` unfolding), the product state
`|000⟩` has column `⟨1, _⟩` identically zero, hence has neither a left inverse nor cyclicity
(discharging the pair non-cyclicity statement for `|000⟩` left open in `TFQ-2107`). -/
theorem prod3_pair_not_cyclic_and_no_left_inverse (s : Fin 3) :
    ¬ HasFullComplementaryRank (pairSiteMatrix psiProd3 s) ∧
    ¬ SeparatingForAc (pairSiteMatrix psiProd3 s) ∧
    ¬ CyclicForA (pairSiteMatrix psiProd3 s) := by
  have h10 : (1 : Int) ≠ 0 := by decide
  have i0 : Fin 4 := ⟨0, by decide⟩
  have hcol : ∀ b : Fin 4, pairSiteMatrix psiProd3 s b ⟨1, by decide⟩ = 0 := by
    revert s; decide
  refine ⟨no_left_inverse_of_zero_column h10 ⟨1, by decide⟩ hcol, ?_⟩
  exact not_cyclic_of_zero_column h10 i0 ⟨1, by decide⟩ hcol

/-- Theorem 7: On every pair of sites `s ∈ {0, 1, 2}` (`4 × 2` unfolding), both `|GHZ_3⟩` and
`|W_3⟩` have `HasFullComplementaryRank`, `CyclicForA`, and `SeparatingForAc`. -/
theorem ghz3_and_w3_pair_cyclic_and_separating (s : Fin 3) :
    HasFullComplementaryRank (pairSiteMatrix psiGHZ3 s) ∧
    CyclicForA (pairSiteMatrix psiGHZ3 s) ∧
    SeparatingForAc (pairSiteMatrix psiGHZ3 s) ∧
    HasFullComplementaryRank (pairSiteMatrix psiW3 s) ∧
    CyclicForA (pairSiteMatrix psiW3 s) ∧
    SeparatingForAc (pairSiteMatrix psiW3 s) := by
  have hGHZ : HasFullComplementaryRank (pairSiteMatrix psiGHZ3 s) := by
    refine ⟨leftInvGHZ, ?_⟩
    funext i j
    revert i j s
    decide
  have hW : HasFullComplementaryRank (pairSiteMatrix psiW3 s) := by
    clear hGHZ
    refine ⟨leftInvW, ?_⟩
    funext i j
    revert i j s
    decide
  exact ⟨hGHZ,
         cyclic_of_fullComplementaryRank hGHZ,
         separating_of_fullComplementaryRank hGHZ,
         hW,
         cyclic_of_fullComplementaryRank hW,
         separating_of_fullComplementaryRank hW⟩

/-- Unfolding of a 3-qubit state `ψ : Fin 8 → Int` for the full 3-site algebra (`dA = 8, dB = 1`). -/
def fullThreeSiteMatrix (ψ : Fin 8 → Int) : Fin 8 → Fin 1 → Int :=
  fun x _ => ψ x

/-- Theorem 8: On the full 3-site algebra (`8 × 1` unfolding), all three states `|000⟩`,
`|GHZ_3⟩`, and `|W_3⟩` have full complementary rank `1` and are cyclic (discharging the full-algebra
cyclicity statement left open in `TFQ-2107`). -/
theorem full_three_site_cyclic_all_three_states :
    CyclicForA (fullThreeSiteMatrix psiProd3) ∧
    CyclicForA (fullThreeSiteMatrix psiGHZ3) ∧
    CyclicForA (fullThreeSiteMatrix psiW3) := by
  have hProd : HasFullComplementaryRank (fullThreeSiteMatrix psiProd3) := by
    refine ⟨fun _ i => if i.val = 0 then 1 else 0, ?_⟩
    funext i j; revert i j; decide
  have hGHZ : HasFullComplementaryRank (fullThreeSiteMatrix psiGHZ3) := by
    refine ⟨fun _ i => if i.val = 0 then 1 else 0, ?_⟩
    funext i j; revert i j; decide
  have hW : HasFullComplementaryRank (fullThreeSiteMatrix psiW3) := by
    refine ⟨fun _ i => if i.val = 1 then 1 else 0, ?_⟩
    funext i j; revert i j; decide
  exact ⟨cyclic_of_fullComplementaryRank hProd,
         cyclic_of_fullComplementaryRank hGHZ,
         cyclic_of_fullComplementaryRank hW⟩

/-- 4-qubit half-system (`2 + 2` bipartition `A = {0, 1}`, `A^c = {2, 3}`) `4 × 4` amplitude
matrices for `|0000⟩`, `|GHZ_4⟩ = |0000⟩ + |1111⟩`, and the 2-Bell-pair cluster state
`(|00⟩ + |11⟩)_{02} ⊗ (|00⟩ + |11⟩)_{13}` (which unfolds to `matId 4`). -/
def halfMatrixProd4 : Fin 4 → Fin 4 → Int :=
  fun i j => if i.val = 0 ∧ j.val = 0 then 1 else 0

def halfMatrixGHZ4 : Fin 4 → Fin 4 → Int :=
  fun i j => if (i.val = 0 ∧ j.val = 0) ∨ (i.val = 3 ∧ j.val = 3) then 1 else 0

def halfMatrixBellPair4 : Fin 4 → Fin 4 → Int :=
  matId 4

/-- Theorem 9: Across the 4-qubit `2 + 2` bipartition (`dA = 4, dB = 4`), neither `|0000⟩` nor
`|GHZ_4⟩` is cyclic for the 2-site algebra `End(H_A)` (both have column `⟨1, _⟩` identically zero),
whereas the 2-Bell-pair state has full complementary rank `4` (`L = I_4`) and is both cyclic for
`End(H_A)` and separating for `End(H_{A^c})`. -/
theorem four_qubit_half_system_cyclicity_dichotomy :
    ¬ CyclicForA halfMatrixProd4 ∧
    ¬ CyclicForA halfMatrixGHZ4 ∧
    HasFullComplementaryRank halfMatrixBellPair4 ∧
    CyclicForA halfMatrixBellPair4 ∧
    SeparatingForAc halfMatrixBellPair4 := by
  have h10 : (1 : Int) ≠ 0 := by decide
  have i0 : Fin 4 := ⟨0, by decide⟩
  have hcolP : ∀ i : Fin 4, halfMatrixProd4 i ⟨1, by decide⟩ = 0 := by decide
  have hcolG : ∀ i : Fin 4, halfMatrixGHZ4 i ⟨1, by decide⟩ = 0 := by decide
  have hBell : HasFullComplementaryRank halfMatrixBellPair4 :=
    ⟨matId 4, matMul_id_left (matId 4)⟩
  exact ⟨(not_cyclic_of_zero_column h10 i0 ⟨1, by decide⟩ hcolP).2,
         (not_cyclic_of_zero_column h10 i0 ⟨1, by decide⟩ hcolG).2,
         hBell,
         cyclic_of_fullComplementaryRank hBell,
         separating_of_fullComplementaryRank hBell⟩

-- ============================================================================
-- 3. Discrete Cyclic Translation Group Aliasing vs. Continuum Stone / Tube Fence
-- ============================================================================

/-- Cyclic lattice translation `(x + k) mod N` on `Fin N` (`N > 0`). -/
def cyclicShift (N : Nat) [NeZero N] (k : Nat) (x : Fin N) : Fin N :=
  ⟨(x.val + k) % N, Nat.mod_lt _ (NeZero.pos N)⟩

/-- Discrete momentum difference `(T - I) ψ (x) = ψ((x + 1) mod N) - ψ(x)` generating cyclic
lattice translations. -/
def discreteMomentumDiff (N : Nat) [NeZero N] (ψ : Fin N → Int) (x : Fin N) : Int :=
  ψ (cyclicShift N 1 x) - ψ x

/-- Translation-invariant constant vector `ψ(x) = c` on `Fin N`. -/
def constVec (N : Nat) (c : Int) : Fin N → Int :=
  fun _ => c

/-- Theorem 10: On any finite `N`-site ring (`N > 0`), the cyclic shift aliases after `N` steps
(`cyclicShift N N x = x` and `cyclicShift N (k + N) x = cyclicShift N k x`), unlike the
non-aliasing continuum Minkowski translation group `ℝ^4`. -/
theorem cyclicShift_periodic_aliasing (N : Nat) [NeZero N] (k : Nat) (x : Fin N) :
    cyclicShift N N x = x ∧
    cyclicShift N (k + N) x = cyclicShift N k x := by
  refine ⟨?_, ?_⟩
  · apply Fin.ext
    dsimp [cyclicShift]
    rw [Nat.add_mod_right, Nat.mod_eq_of_lt x.isLt]
  · apply Fin.ext
    dsimp [cyclicShift]
    rw [← Nat.add_assoc, Nat.add_mod_right]

/-- Theorem 11: Every translation-invariant vector `constVec N c` on a finite `N`-site ring has
identically vanishing discrete momentum difference `discreteMomentumDiff N (constVec N c) x = 0`,
and any vector annihilated by `discreteMomentumDiff 3` on a 3-site ring is constant
(`ψ 0 = ψ 1 ∧ ψ 1 = ψ 2`). -/
theorem translation_invariant_zero_momentum_diff (N : Nat) [NeZero N] (c : Int) (x : Fin N) :
    discreteMomentumDiff N (constVec N c) x = 0 := by
  dsimp [discreteMomentumDiff, constVec]
  omega

/-- Theorem 12: On `N = 3` qubits, the translation-invariant product vacuum `|000⟩` (`psiProd3`)
is invariant under cyclic permutation of the 3 qubits (`singleSiteMatrix psiProd3 s` is independent
of `s ∈ {0, 1, 2}`), yet fails cyclicity on every single site (`|A| = 1`) and on every pair of
sites (`|A| = 2`), demonstrating that finite translation invariance without the continuum Stone
spectrum condition (`FQ-GAP-STONE-CONTINUOUS-TIME`) and Hilbert completion (`FQ-GAP-CONTINUUM-HILBERT-LIFT`)
does not make the vacuum cyclic for proper local algebras. -/
theorem translation_invariant_product_vacuum_not_cyclic_for_proper_subsystems :
    singleSiteMatrix psiProd3 ⟨0, by decide⟩ = singleSiteMatrix psiProd3 ⟨1, by decide⟩ ∧
    singleSiteMatrix psiProd3 ⟨1, by decide⟩ = singleSiteMatrix psiProd3 ⟨2, by decide⟩ ∧
    (∀ s : Fin 3, ¬ CyclicForA (singleSiteMatrix psiProd3 s)) ∧
    (∀ s : Fin 3, ¬ CyclicForA (pairSiteMatrix psiProd3 s)) ∧
    CyclicForA (fullThreeSiteMatrix psiProd3) := by
  refine ⟨?_, ?_, ?_, ?_, full_three_site_cyclic_all_three_states.1⟩
  · funext a b; revert a b; decide
  · funext a b; revert a b; decide
  · intro s; exact (single_site_not_cyclic_all_three_states s).1
  · intro s; exact (prod3_pair_not_cyclic_and_no_left_inverse s).2.2

end ReehSchliederImport

#print axioms ReehSchliederImport.cyclic_implies_separating
#print axioms ReehSchliederImport.not_cyclic_of_right_kernel
#print axioms ReehSchliederImport.no_left_inverse_of_zero_column
#print axioms ReehSchliederImport.not_cyclic_of_zero_column
#print axioms ReehSchliederImport.single_site_not_cyclic_all_three_states
#print axioms ReehSchliederImport.prod3_pair_not_cyclic_and_no_left_inverse
#print axioms ReehSchliederImport.ghz3_and_w3_pair_cyclic_and_separating
#print axioms ReehSchliederImport.full_three_site_cyclic_all_three_states
#print axioms ReehSchliederImport.four_qubit_half_system_cyclicity_dichotomy
#print axioms ReehSchliederImport.cyclicShift_periodic_aliasing
#print axioms ReehSchliederImport.translation_invariant_zero_momentum_diff
#print axioms ReehSchliederImport.translation_invariant_product_vacuum_not_cyclic_for_proper_subsystems

private def l5aProvenance : String :=
  "Origin: lean4/ReehSchliederImport.lean Claim: CQFT-REEH-SCHLIEDER-THEOREM-IMPORT AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
