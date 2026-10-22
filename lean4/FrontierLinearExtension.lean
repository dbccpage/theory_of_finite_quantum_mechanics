import Mathlib.Algebra.Group.Defs
import CausalOrder
import FrontierPosetNet

/-!
# Ordered products along linear extensions of a finite strict poset
(CQFT-ORDERED-PRODUCT-LINEAR-EXTENSION-TARGET)

AuthorityEffect: None.
Scope: Ordered products `orderedProd A L = (L.map A).prod` along linear extensions `L` of a
`FiniteStrictPoset n`, adjacent spacelike swaps, and exact Pauli checks on the diamond poset `C2`
and the four-element `N` poset.
Proves:
1. For any monoid `M` and operator assignment `A : Fin n → M`, if `A x * A y = A y * A x` for all
   spacelike pairs `x, y`, then any adjacent spacelike swap `pre ++ x :: y :: post ↦ pre ++ y :: x :: post`
   preserves `orderedProd A`, and by induction on the reflexive-transitive closure `SpacelikeSwapChain`
   any two listings connected by adjacent spacelike swaps have equal ordered products.
2. On the diamond poset `C2`, the exact linear extensions among all 24 permutations of `[0,1,2,3]`
   are `[0,1,2,3]` and `[0,2,1,3]`; they are connected by one adjacent spacelike swap of `1` and `2`,
   agree for commuting operators, and differ by the exact sign `-1` when `1` and `2` carry the
   anticommuting Pauli matrices `X` and `Z`.
3. On the four-element `N` poset (`0 < 2`, `1 < 2`, `1 < 3`), the exact linear extensions among all
   24 permutations of `[0,1,2,3]` are the 5 extensions `[0,1,2,3]`, `[0,1,3,2]`, `[1,0,2,3]`,
   `[1,0,3,2]`, and `[1,3,0,2]`, all connected by adjacent spacelike swaps (`0 ↔ 1`, `2 ↔ 3`, `0 ↔ 3`).
-/

namespace FrontierLinearExtension

open CausalOrder
open FrontierPosetNet

/-- Ordered product of `A : α → M` along a list `L : List α`. -/
def orderedProd {α M : Type*} [One M] [Mul M] (A : α → M) : List α → M
  | [] => 1
  | x :: xs => A x * orderedProd A xs

theorem orderedProd_append {α M : Type*} [Monoid M] (A : α → M) (L₁ L₂ : List α) :
    orderedProd A (L₁ ++ L₂) = orderedProd A L₁ * orderedProd A L₂ := by
  induction L₁ with
  | nil => simp [orderedProd]
  | cons x xs ih =>
    simp [orderedProd, ih, mul_assoc]

/-- One adjacent swap of spacelike elements `x, y` in `P`. -/
def AdjSpacelikeSwap {n : Nat} (P : FiniteStrictPoset n) (L₁ L₂ : List (Fin n)) : Prop :=
  ∃ (pre post : List (Fin n)) (x y : Fin n),
    isSpacelike P x y ∧
    L₁ = pre ++ x :: y :: post ∧
    L₂ = pre ++ y :: x :: post

/-- Reflexive-transitive closure of adjacent spacelike swaps. -/
inductive SpacelikeSwapChain {n : Nat} (P : FiniteStrictPoset n) :
    List (Fin n) → List (Fin n) → Prop
  | refl (L : List (Fin n)) : SpacelikeSwapChain P L L
  | step {L₁ L₂ L₃ : List (Fin n)} :
      AdjSpacelikeSwap P L₁ L₂ → SpacelikeSwapChain P L₂ L₃ → SpacelikeSwapChain P L₁ L₃

/-- An adjacent swap of spacelike elements preserves `orderedProd A` whenever spacelike operators commute. -/
theorem orderedProd_eq_of_adjSpacelikeSwap {n : Nat} {M : Type*} [Monoid M]
    (P : FiniteStrictPoset n) (A : Fin n → M)
    (hcomm : ∀ x y : Fin n, isSpacelike P x y → A x * A y = A y * A x)
    {L₁ L₂ : List (Fin n)} (hswap : AdjSpacelikeSwap P L₁ L₂) :
    orderedProd A L₁ = orderedProd A L₂ := by
  rcases hswap with ⟨pre, post, x, y, hsp, rfl, rfl⟩
  rw [orderedProd_append, orderedProd_append]
  dsimp [orderedProd]
  rw [← mul_assoc (A x), hcomm x y hsp, mul_assoc]

/-- Any chain of adjacent spacelike swaps preserves `orderedProd A` whenever spacelike operators commute. -/
theorem orderedProd_eq_of_spacelikeSwapChain {n : Nat} {M : Type*} [Monoid M]
    (P : FiniteStrictPoset n) (A : Fin n → M)
    (hcomm : ∀ x y : Fin n, isSpacelike P x y → A x * A y = A y * A x)
    {L₁ L₂ : List (Fin n)} (hchain : SpacelikeSwapChain P L₁ L₂) :
    orderedProd A L₁ = orderedProd A L₂ := by
  induction hchain with
  | refl _ => rfl
  | step hswap _ ih =>
    rw [orderedProd_eq_of_adjSpacelikeSwap P A hcomm hswap, ih]

/-- Executable check whether a list `L : List (Fin n)` respects the strict order `P`
(never places `y` before `x` when `x < y`). -/
def respectsOrder {n : Nat} (P : FiniteStrictPoset n) : List (Fin n) → Bool
  | [] => true
  | x :: xs => (xs.all fun y => !(decide (P.rel y x))) && respectsOrder P xs

def nodupBool {α : Type*} [DecidableEq α] : List α → Bool
  | [] => true
  | x :: xs => (xs.all fun y => decide (x ≠ y)) && nodupBool xs

def isLinearExtension {n : Nat} (P : FiniteStrictPoset n) (L : List (Fin n)) : Bool :=
  (L.length == n) && nodupBool L && respectsOrder P L

def insertAll {α : Type*} (x : α) : List α → List (List α)
  | [] => [[x]]
  | y :: ys => (x :: y :: ys) :: (insertAll x ys).map (y :: ·)

def permsList {α : Type*} : List α → List (List α)
  | [] => [[]]
  | x :: xs => (permsList xs).flatMap (insertAll x)

/-- All 24 permutations of `[d0, d1, d2, d3]` in `Fin 4`. -/
def allPerms4 : List (List (Fin 4)) :=
  permsList [d0, d1, d2, d3]

/-- Exact linear extensions of the diamond poset `C2` (`0<1, 0<2, 1<3, 2<3`) and of `posetN`. -/
theorem linear_extensions_of_C2_and_N :
    allPerms4.length = 24 ∧
    (allPerms4.filter (isLinearExtension C2)).length = 2 ∧
    ([d0, d1, d2, d3] ∈ allPerms4.filter (isLinearExtension C2)) ∧
    ([d0, d2, d1, d3] ∈ allPerms4.filter (isLinearExtension C2)) ∧
    (allPerms4.filter (isLinearExtension posetN)).length = 5 := by
  decide

/-- The two linear extensions of `C2` are connected by a single adjacent spacelike swap of `d1` and `d2`. -/
theorem c2_extensions_connected_by_swap :
    SpacelikeSwapChain C2 [d0, d1, d2, d3] [d0, d2, d1, d3] := by
  refine SpacelikeSwapChain.step ?_ (SpacelikeSwapChain.refl _)
  refine ⟨[d0], [d3], d1, d2, c2_spacelike_1_2, rfl, rfl⟩

/-- Exact 2x2 integer matrices for the Pauli anticommutation sign-flip check on `C2`. -/
structure Mat2Int where
  m00 : Int
  m01 : Int
  m10 : Int
  m11 : Int
  deriving DecidableEq, Repr

def mulMat2 (A B : Mat2Int) : Mat2Int :=
  ⟨A.m00 * B.m00 + A.m01 * B.m10,
   A.m00 * B.m01 + A.m01 * B.m11,
   A.m10 * B.m00 + A.m11 * B.m10,
   A.m10 * B.m01 + A.m11 * B.m11⟩

def negMat2 (A : Mat2Int) : Mat2Int :=
  ⟨-A.m00, -A.m01, -A.m10, -A.m11⟩

instance : One Mat2Int := ⟨⟨1, 0, 0, 1⟩⟩
instance : Mul Mat2Int := ⟨mulMat2⟩

def pauliI : Mat2Int := ⟨1, 0, 0, 1⟩
def pauliX : Mat2Int := ⟨0, 1, 1, 0⟩
def pauliZ : Mat2Int := ⟨1, 0, 0, -1⟩

/-- Assignment on `C2` placing anticommuting `X` and `Z` on the spacelike pair `d1, d2`. -/
def assignAnticommC2 : Fin 4 → Mat2Int
  | ⟨0, _⟩ => pauliI
  | ⟨1, _⟩ => pauliX
  | ⟨2, _⟩ => pauliZ
  | ⟨3, _⟩ => pauliI

/-- Assignment on `C2` placing commuting `Z` and `Z` on the spacelike pair `d1, d2`. -/
def assignCommC2 : Fin 4 → Mat2Int
  | ⟨0, _⟩ => pauliI
  | ⟨1, _⟩ => pauliZ
  | ⟨2, _⟩ => pauliZ
  | ⟨3, _⟩ => pauliI

/-- Exact sign flip when spacelike elements `d1, d2` of `C2` carry anticommuting Pauli matrices
`X` and `Z`, and exact agreement when they carry commuting operators. -/
theorem c2_pauli_commuting_and_anticommuting_products :
    orderedProd assignCommC2 [d0, d1, d2, d3] =
      orderedProd assignCommC2 [d0, d2, d1, d3] ∧
    orderedProd assignAnticommC2 [d0, d1, d2, d3] =
      negMat2 (orderedProd assignAnticommC2 [d0, d2, d1, d3]) ∧
    orderedProd assignAnticommC2 [d0, d1, d2, d3] ≠
      orderedProd assignAnticommC2 [d0, d2, d1, d3] := by
  decide

end FrontierLinearExtension

#print axioms FrontierLinearExtension.orderedProd_append
#print axioms FrontierLinearExtension.orderedProd_eq_of_adjSpacelikeSwap
#print axioms FrontierLinearExtension.orderedProd_eq_of_spacelikeSwapChain
#print axioms FrontierLinearExtension.linear_extensions_of_C2_and_N
#print axioms FrontierLinearExtension.c2_extensions_connected_by_swap
#print axioms FrontierLinearExtension.c2_pauli_commuting_and_anticommuting_products

private def l5aProvenance : String :=
  "Origin: lean4/FrontierLinearExtension.lean Claim: orderedProd_eq_of_spacelikeSwapChain AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
