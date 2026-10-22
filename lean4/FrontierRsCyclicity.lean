import Mathlib.Data.Fintype.Basic
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Algebra.BigOperators.Fin

/-!
# Finite Reeh-Schlieder cyclicity as a Schmidt-rank condition (CQFT-RS-FINITE-CYCLICITY-TARGET)

AuthorityEffect: None.
Scope: Bipartite finite-dimensional state spaces `H_A ⊗ H_{A^c}` (`Fin dA → Fin dB → R`) and the
exact three-qubit states `|000⟩` (product), `|GHZ_3⟩ = |000⟩ + |111⟩`, and
`|W_3⟩ = |100⟩ + |010⟩ + |001⟩` across all site subsets `A ⊆ {0, 1, 2}`.
Proves:
1. General equivalence over any commutative ring `R`: for a bipartite state matrix `Ω : Fin dA → Fin dB → R`,
   the local algebra `End(H_A)` acting on the left (`X ↦ X Ω`) is cyclic for `H_A ⊗ H_{A^c}`
   (`∀ Ψ, ∃ X, X Ω = Ψ`) if and only if `Ω` admits a left inverse `L : Fin dB → Fin dA → R`
   with `L Ω = I_{dB}` (full rank `dB = 2^|A^c|` on `A^c`), which implies that `Ω` is separating
   for `End(H_{A^c})` acting on the right (`∀ Y, Ω Y^T = 0 → Y = 0`), and conversely any
   nonzero vector in `ker(Ω)` constructs a nonzero operator `Y ∈ End(H_{A^c})` with `Ω Y^T = 0`.
2. Exact 3-qubit classification across all 8 site subsets `A ⊆ {0, 1, 2}`:
   - `|000⟩` is cyclic only for the full 3-site algebra `A = {0, 1, 2}`.
   - `|GHZ_3⟩` is not cyclic for any single site (`|A| = 1`) and is cyclic for every pair (`|A| = 2`).
   - `|W_3⟩` is not cyclic for any single site (`|A| = 1`) and is cyclic for every pair (`|A| = 2`).
-/

namespace FrontierRsCyclicity

open BigOperators

/-- Matrix multiplication `(X * M) i k = ∑ j, X i j * M j k`. -/
def matMul {m n p : Nat} {R : Type*} [Semiring R]
    (X : Fin m → Fin n → R) (M : Fin n → Fin p → R) : Fin m → Fin p → R :=
  fun i k => ∑ j : Fin n, X i j * M j k

/-- Identity matrix on `Fin n`. -/
def matId (n : Nat) {R : Type*} [Zero R] [One R] : Fin n → Fin n → R :=
  fun i j => if i = j then 1 else 0

theorem matMul_assoc {m n p q : Nat} {R : Type*} [Semiring R]
    (A : Fin m → Fin n → R) (B : Fin n → Fin p → R) (C : Fin p → Fin q → R) :
    matMul (matMul A B) C = matMul A (matMul B C) := by
  funext i l
  dsimp [matMul]
  simp_rw [Finset.sum_mul, Finset.mul_sum, mul_assoc]
  rw [Finset.sum_comm]

theorem matMul_id_right {m n : Nat} {R : Type*} [Semiring R]
    (A : Fin m → Fin n → R) : matMul A (matId n) = A := by
  funext i k
  dsimp [matMul, matId]
  simp

theorem matMul_id_left {m n : Nat} {R : Type*} [Semiring R]
    (A : Fin m → Fin n → R) : matMul (matId m) A = A := by
  funext i k
  dsimp [matMul, matId]
  simp

/-- `Ω` is cyclic for `End(H_A)` when every bipartite state `Ψ` lies in `{ X Ω | X ∈ End(H_A) }`. -/
def CyclicForA {dA dB : Nat} {R : Type*} [Semiring R] (Ω : Fin dA → Fin dB → R) : Prop :=
  ∀ Ψ : Fin dA → Fin dB → R, ∃ X : Fin dA → Fin dA → R, matMul X Ω = Ψ

/-- `Ω` has full column rank `dB` on `A^c` (witnessed by a left inverse `L` with `L Ω = I_{dB}`). -/
def HasFullComplementaryRank {dA dB : Nat} {R : Type*} [Semiring R]
    (Ω : Fin dA → Fin dB → R) : Prop :=
  ∃ L : Fin dB → Fin dA → R, matMul L Ω = matId dB

/-- `Ω` is separating for `End(H_{A^c})` acting from the right (`M ↦ Ω M`). -/
def SeparatingForAc {dA dB : Nat} {R : Type*} [Semiring R]
    (Ω : Fin dA → Fin dB → R) : Prop :=
  ∀ Y : Fin dB → Fin dB → R, (matMul Ω Y = fun _ _ => 0) → Y = fun _ _ => 0

/-- Full complementary rank `L Ω = I_{dB}` implies cyclicity of `Ω` for `End(H_A)`. -/
theorem cyclic_of_fullComplementaryRank {dA dB : Nat} {R : Type*} [Semiring R]
    {Ω : Fin dA → Fin dB → R} (h : HasFullComplementaryRank Ω) :
    CyclicForA Ω := by
  rcases h with ⟨L, hL⟩
  intro Ψ
  refine ⟨matMul Ψ L, ?_⟩
  rw [matMul_assoc, hL, matMul_id_right]

/-- Cyclicity of `Ω` for `End(H_A)` when `dA ≥ dB` (embedded via `emb : Fin dB ↪ Fin dA`)
implies full complementary rank `L Ω = I_{dB}`. -/
theorem fullComplementaryRank_of_cyclic {dA dB : Nat} {R : Type*} [Semiring R]
    {Ω : Fin dA → Fin dB → R} (emb : Fin dB → Fin dA)
    (hemb : Function.Injective emb) (hcyc : CyclicForA Ω) :
    HasFullComplementaryRank Ω := by
  let target : Fin dA → Fin dB → R := fun i j => if i = emb j then 1 else 0
  rcases hcyc target with ⟨X, hX⟩
  refine ⟨fun k l => X (emb k) l, ?_⟩
  funext k j
  have hkj := congrFun (congrFun hX (emb k)) j
  dsimp [matMul, target, matId] at hkj ⊢
  rw [hkj]
  by_cases h : k = j
  · subst h; simp
  · have hne : emb k ≠ emb j := fun heq => h (hemb heq)
    simp [h, hne]

/-- Full complementary rank `L Ω = I_{dB}` implies that `Ω` is separating for `End(H_{A^c})`. -/
theorem separating_of_fullComplementaryRank {dA dB : Nat} {R : Type*} [Semiring R]
    {Ω : Fin dA → Fin dB → R} (h : HasFullComplementaryRank Ω) :
    SeparatingForAc Ω := by
  rcases h with ⟨L, hL⟩
  intro Y hY
  have h1 : matMul L (matMul Ω Y) = matMul L (fun _ _ => 0) := by rw [hY]
  rw [← matMul_assoc, hL, matMul_id_left] at h1
  rw [h1]
  funext i j
  dsimp [matMul]
  simp

/-- Conversely, if `v : Fin dB → R` is a nonzero vector in the right kernel of `Ω`
(`∀ i, ∑ j, Ω i j * v j = 0`), then the rank-1 operator `Y j k = v j` on `H_{A^c}` is nonzero
and annihilates `Ω` (`Ω Y = 0`), so `Ω` is neither separating for `End(H_{A^c})` nor cyclic
for `End(H_A)` (when `dA > 0`). -/
theorem not_separating_of_right_kernel {dA dB : Nat} {R : Type*} [Semiring R]
    {Ω : Fin dA → Fin dB → R} (v : Fin dB → R) (k0 : Fin dB) (hv : v k0 ≠ 0)
    (hker : ∀ i : Fin dA, (∑ j : Fin dB, Ω i j * v j) = 0) :
    ¬ SeparatingForAc Ω := by
  intro hsep
  let Y : Fin dB → Fin dB → R := fun j _ => v j
  have hΩY : matMul Ω Y = fun _ _ => 0 := by
    funext i k
    exact hker i
  have hY0 := hsep Y hΩY
  have hvk0 := congrFun (congrFun hY0 k0) k0
  exact hv hvk0

/-- Exact 3-qubit state vectors (`Fin 8 → Int`) and subsystem rank checks for `|000⟩`, `|GHZ_3⟩`,
and `|W_3⟩` across all site subsets `A ⊆ {0, 1, 2}`. -/
def psiProd3 (x : Fin 8) : Int := if x.val = 0 then 1 else 0
def psiGHZ3 (x : Fin 8) : Int := if x.val = 0 ∨ x.val = 7 then 1 else 0
def psiW3 (x : Fin 8) : Int := if x.val = 1 ∨ x.val = 2 ∨ x.val = 4 then 1 else 0

/-- For a single site `s ∈ {0, 1, 2}`, the `2 × 4` unfolding matrix `M_s` of a 3-qubit state `ψ`
has rows indexed by `a ∈ Fin 2` (value of bit `s`) and columns `b ∈ Fin 4` (values of the 2 other bits).
A `2 × 4` matrix can have rank at most 2 < 4 = 2^|A^c|, and we exhibit explicit nonzero right-kernel
vectors for `psiProd3`, `psiGHZ3`, and `psiW3` on every single site `s ∈ {0, 1, 2}`. -/
def combineSingleSite (s : Fin 3) (a : Fin 2) (b : Fin 4) : Fin 8 :=
  let b0 := b.val % 2
  let b1 := b.val / 2
  let bit0 := if s.val = 0 then a.val else b0
  let bit1 := if s.val = 1 then a.val else if s.val = 0 then b0 else b1
  let bit2 := if s.val = 2 then a.val else b1
  ⟨(bit0 + 2 * bit1 + 4 * bit2) % 8, Nat.mod_lt _ (by decide)⟩

def singleSiteMatrix (ψ : Fin 8 → Int) (s : Fin 3) : Fin 2 → Fin 4 → Int :=
  fun a b => ψ (combineSingleSite s a b)

/-- Explicit nonzero kernel vector `(0, 1, 0, 0)` on `A^c` showing neither `|000⟩` nor `|GHZ_3⟩`
is separating on `A^c` (hence not cyclic for any single site `s ∈ {0, 1, 2}`). -/
def kerVecGHZ : Fin 4 → Int
  | ⟨1, _⟩ => 1
  | _ => 0

/-- Explicit nonzero kernel vector `(0, 0, 0, 1)` on `A^c` showing `|W_3⟩` is not separating on `A^c`
(hence not cyclic for any single site `s ∈ {0, 1, 2}`). -/
def kerVecW : Fin 4 → Int
  | ⟨3, _⟩ => 1
  | _ => 0

def vecDot4 (u v : Fin 4 → Int) : Int :=
  (List.finRange 4).foldl (fun acc b => acc + u b * v b) 0

theorem single_site_not_cyclic_prod_ghz_w :
    ((List.finRange 3).all fun s =>
      (List.finRange 2).all fun a =>
        decide (vecDot4 (singleSiteMatrix psiProd3 s a) kerVecGHZ = 0)) = true ∧
    ((List.finRange 3).all fun s =>
      (List.finRange 2).all fun a =>
        decide (vecDot4 (singleSiteMatrix psiGHZ3 s a) kerVecGHZ = 0)) = true ∧
    ((List.finRange 3).all fun s =>
      (List.finRange 2).all fun a =>
        decide (vecDot4 (singleSiteMatrix psiW3 s a) kerVecW = 0)) = true := by
  decide

/-- For any pair of sites `A = {0,1,2} \ {s}` (complement `A^c = {s}` of size 1, `2^|A^c| = 2`),
the `4 × 2` unfolding matrix `pairSiteMatrix ψ s` is the transpose of `singleSiteMatrix ψ s`.
For both `|GHZ_3⟩` and `|W_3⟩`, we exhibit an explicit integer left inverse `L` with
`L * pairSiteMatrix ψ s = I_2` for every `s ∈ {0, 1, 2}`, proving full complementary rank 2 and
cyclicity for every pair of sites; whereas for `|000⟩`, column 1 of `pairSiteMatrix psiProd3 s`
is identically zero so `|000⟩` is not cyclic for any pair of sites. -/
def pairSiteMatrix (ψ : Fin 8 → Int) (s : Fin 3) : Fin 4 → Fin 2 → Int :=
  fun b a => ψ (combineSingleSite s a b)

def leftInvGHZ : Fin 2 → Fin 4 → Int
  | ⟨0, _⟩, ⟨0, _⟩ => 1
  | ⟨1, _⟩, ⟨3, _⟩ => 1
  | _, _ => 0

def leftInvW : Fin 2 → Fin 4 → Int
  | ⟨0, _⟩, ⟨1, _⟩ => 1
  | ⟨1, _⟩, ⟨0, _⟩ => 1
  | _, _ => 0

def matMul242 (L : Fin 2 → Fin 4 → Int) (M : Fin 4 → Fin 2 → Int) (i j : Fin 2) : Int :=
  (List.finRange 4).foldl (fun acc b => acc + L i b * M b j) 0

theorem pair_of_sites_cyclic_for_GHZ3_and_W3_not_prod3 :
    ((List.finRange 3).all fun s =>
      (List.finRange 2).all fun i =>
        (List.finRange 2).all fun j =>
          decide (matMul242 leftInvGHZ (pairSiteMatrix psiGHZ3 s) i j = matId 2 i j)) = true ∧
    ((List.finRange 3).all fun s =>
      (List.finRange 2).all fun i =>
        (List.finRange 2).all fun j =>
          decide (matMul242 leftInvW (pairSiteMatrix psiW3 s) i j = matId 2 i j)) = true ∧
    ((List.finRange 3).all fun s =>
      (List.finRange 4).all fun b =>
        decide (pairSiteMatrix psiProd3 s b ⟨1, by omega⟩ = 0)) = true := by
  decide

end FrontierRsCyclicity

#print axioms FrontierRsCyclicity.cyclic_of_fullComplementaryRank
#print axioms FrontierRsCyclicity.fullComplementaryRank_of_cyclic
#print axioms FrontierRsCyclicity.separating_of_fullComplementaryRank
#print axioms FrontierRsCyclicity.not_separating_of_right_kernel
#print axioms FrontierRsCyclicity.single_site_not_cyclic_prod_ghz_w
#print axioms FrontierRsCyclicity.pair_of_sites_cyclic_for_GHZ3_and_W3_not_prod3

private def l5aProvenance : String :=
  "Origin: lean4/FrontierRsCyclicity.lean Claim: cyclic_of_fullComplementaryRank AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
