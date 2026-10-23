import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-!
Finite Zimmermann forests for one declared overlapping diagram, and an order-0
subtraction on one declared numerator.

AuthorityEffect: None.
This is not a Feynman-parametric integrand, not a subtraction of positive degree,
and not a convergence statement for continuum loop integration.
-/
namespace CampaignDfmBphzContinuumFence

inductive Piece
  | L
  | R
  | G
  deriving DecidableEq, Repr

/-- Declared edge sets: `L = {0,1,2}`, `R = {2,3,4}`, `G = {0,1,2,3,4}`. -/
def pieceEdge : Piece → Fin 5 → Bool
  | .L, e => decide (e.val ≤ 2)
  | .R, e => decide (2 ≤ e.val)
  | .G, _ => true

def edgeList : List (Fin 5) := List.finRange 5

def isSubset (a b : Piece) : Bool :=
  edgeList.all fun e => !(pieceEdge a e) || pieceEdge b e

def isDisjoint (a b : Piece) : Bool :=
  edgeList.all fun e => !(pieceEdge a e && pieceEdge b e)

/-- Nested or disjoint, the Zimmermann compatibility relation on these three sets. -/
def isCompatible (a b : Piece) : Bool :=
  isSubset a b || isSubset b a || isDisjoint a b

theorem share_edge_two :
    pieceEdge .L 2 = true ∧ pieceEdge .R 2 = true ∧ pieceEdge .G 2 = true := by
  decide

theorem not_compatible_LR : isCompatible .L .R = false := by
  decide

theorem compatible_LG : isCompatible .L .G = true := by
  decide

theorem compatible_RG : isCompatible .R .G = true := by
  decide

/-- A subset of `{L, R, G}`, written as three membership bits. -/
structure Flag where
  l : Bool
  r : Bool
  g : Bool
  deriving DecidableEq, Repr

def flagOk (f : Flag) : Bool :=
  (!f.l || !f.r || isCompatible .L .R) &&
    (!f.l || !f.g || isCompatible .L .G) &&
      (!f.r || !f.g || isCompatible .R .G)

/-- `L` and `R` overlap, so a forest contains both of them exactly when the flag is rejected. -/
theorem overlapping_excluded_iff (l r g : Bool) :
    flagOk ⟨l, r, g⟩ = false ↔ l = true ∧ r = true := by
  cases l <;> cases r <;> cases g <;> decide

theorem overlapping_forest_count :
    (([false, true].flatMap fun l =>
        [false, true].flatMap fun r =>
          [false, true].map fun g => flagOk ⟨l, r, g⟩).count true) = 6 := by
  decide

inductive Nest
  | inner
  | outer
  deriving DecidableEq, Repr

/-- Nested control: `inner = {0,1}` sits inside `outer = {0,1,2,3}`. -/
def nestEdge : Nest → Fin 4 → Bool
  | .inner, e => decide (e.val ≤ 1)
  | .outer, _ => true

def nestList : List (Fin 4) := List.finRange 4

def nestSubset (a b : Nest) : Bool :=
  nestList.all fun e => !(nestEdge a e) || nestEdge b e

def nestDisjoint (a b : Nest) : Bool :=
  nestList.all fun e => !(nestEdge a e && nestEdge b e)

def nestCompatible (a b : Nest) : Bool :=
  nestSubset a b || nestSubset b a || nestDisjoint a b

structure NestFlag where
  inner : Bool
  outer : Bool
  deriving DecidableEq, Repr

def nestOk (f : NestFlag) : Bool :=
  !f.inner || !f.outer || nestCompatible .inner .outer

theorem nested_all_compatible (i o : Bool) : nestOk ⟨i, o⟩ = true := by
  cases i <;> cases o <;> decide

theorem nested_forest_count :
    (([false, true].flatMap fun i =>
        [false, true].map fun o => nestOk ⟨i, o⟩).count true) = 4 := by
  decide

/-- Order-0 evaluation at vanishing left, right, or joint kinematic arguments. -/
def evalL (I : ℚ → ℚ → ℚ) (_x y : ℚ) : ℚ := I 0 y
def evalR (I : ℚ → ℚ → ℚ) (x _y : ℚ) : ℚ := I x 0
def evalG (I : ℚ → ℚ → ℚ) (_x _y : ℚ) : ℚ := I 0 0

/-- Signed sum over the six forests. The forbidden pair `{L,R}` contributes nothing. -/
def sixSum (I : ℚ → ℚ → ℚ) (x y : ℚ) : ℚ :=
  I x y - evalL I x y - evalR I x y - evalG I x y
    + evalG (fun _ y => I 0 y) x y
    + evalG (fun x _ => I x 0) x y

theorem sixSum_eq_inclusion (I : ℚ → ℚ → ℚ) (x y : ℚ) :
    sixSum I x y = I x y - I 0 y - I x 0 + I 0 0 := by
  unfold sixSum evalL evalR evalG
  ring

/-- Declared numerator, not a Feynman integrand. -/
def N (x y : ℚ) : ℚ := 2 + 3 * x + 5 * y + 7 * x * y

theorem numerator_is_7xy (x y : ℚ) : sixSum N x y = 7 * x * y := by
  unfold sixSum evalL evalR evalG N
  ring

theorem quotient_is_seven (x y : ℚ) (hxy : x * y ≠ 0) :
    sixSum N x y / (x * y) = 7 := by
  have hN : sixSum N x y = 7 * (x * y) := by
    rw [numerator_is_7xy]
    ring
  rw [hN, mul_div_assoc, div_self hxy, mul_one]

/-- The three forests that omit `G` leave the constant double-pole term. -/
def threeSum (x y : ℚ) : ℚ := N x y - N 0 y - N x 0

theorem threeSum_eq (x y : ℚ) : threeSum x y = 7 * (x * y) - 2 := by
  unfold threeSum N
  ring

theorem omitted_graph_remainder (x y : ℚ) (hxy : x * y ≠ 0) :
    threeSum x y / (x * y) = 7 - 2 / (x * y) := by
  rw [threeSum_eq, sub_div, mul_div_assoc, div_self hxy, mul_one]

theorem witness_half_third :
    sixSum N (1 / 2) (1 / 3) = 7 / 6 ∧
      sixSum N (1 / 2) (1 / 3) / ((1 / 2) * (1 / 3)) = 7 ∧
        threeSum (1 / 2) (1 / 3) / ((1 / 2) * (1 / 3)) = -5 := by
  have hxy : (1 : ℚ) / 2 * ((1 : ℚ) / 3) ≠ 0 := by norm_num
  refine ⟨?_, ?_, ?_⟩
  · have h := numerator_is_7xy ((1 : ℚ) / 2) ((1 : ℚ) / 3)
    norm_num at h
    exact h
  · simpa using quotient_is_seven ((1 : ℚ) / 2) ((1 : ℚ) / 3) hxy
  · have h := omitted_graph_remainder ((1 : ℚ) / 2) ((1 : ℚ) / 3) hxy
    norm_num at h ⊢
    exact h

/-- The already-checked nested sector kernel, kept only as a different number. -/
def sectorK (z lam : ℚ) : ℚ := (1 + z * lam) / (lam * (1 + lam))

theorem sector_value :
    (sectorK (3 / 5) (1 / 2) - sectorK 0 (1 / 2)) *
        (sectorK (3 / 5) (1 / 3) - sectorK 0 (1 / 3)) = (9 : ℚ) / 50 := by
  norm_num [sectorK]

theorem sector_ne_seven :
    (sectorK (3 / 5) (1 / 2) - sectorK 0 (1 / 2)) *
        (sectorK (3 / 5) (1 / 3) - sectorK 0 (1 / 3)) ≠ 7 := by
  rw [sector_value]
  norm_num

theorem sector_formal_zero :
    ((3 : ℚ) / 5) * (3 / 5) = 9 / 25 ∧ (9 : ℚ) / 25 ≠ 7 := by
  norm_num

#print axioms share_edge_two
#print axioms not_compatible_LR
#print axioms compatible_LG
#print axioms compatible_RG
#print axioms overlapping_excluded_iff
#print axioms overlapping_forest_count
#print axioms nested_all_compatible
#print axioms nested_forest_count
#print axioms sixSum_eq_inclusion
#print axioms numerator_is_7xy
#print axioms quotient_is_seven
#print axioms threeSum_eq
#print axioms omitted_graph_remainder
#print axioms witness_half_third
#print axioms sector_value
#print axioms sector_ne_seven
#print axioms sector_formal_zero

end CampaignDfmBphzContinuumFence
