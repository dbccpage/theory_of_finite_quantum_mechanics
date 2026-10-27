import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-!
Finite Zimmermann forests for one declared overlapping diagram, and an order-0
subtraction on one declared numerator.

AuthorityEffect: None.
This is not a Feynman-parametric integrand, not a subtraction of positive degree,
and not a convergence statement for continuum loop integration.
-/
namespace DressingFieldBphzContinuumFence

/-! Finite subtraction API over supplied commuting additive projectors.
No integrand, Taylor degree or continuum convergence is inferred. -/
namespace Subtraction
variable {A : Type*} [AddCommGroup A]

structure Projector (A : Type*) [AddCommGroup A] where
  map : A →+ A
  idempotent : ∀ x, map (map x) = map x

def Projector.remainder (p : Projector A) : A →+ A := AddMonoidHom.id A - p.map

def Commute (p q : Projector A) : Prop := ∀ x, p.map (q.map x) = q.map (p.map x)

def Compatible (ps : List (Projector A)) : Prop :=
  ∀ p ∈ ps, ∀ q ∈ ps, Commute p q

def reduce : List (Projector A) → A →+ A
  | [] => AddMonoidHom.id A
  | p :: ps => p.remainder.comp (reduce ps)

theorem Projector.kills_remainder (p : Projector A) (x : A) :
    p.map (p.remainder x) = 0 := by
  simp [Projector.remainder, map_sub, p.idempotent]

theorem map_remainder (p q : Projector A) (h : Commute p q) (x : A) :
    p.map (q.remainder x) = q.remainder (p.map x) := by
  simp [Projector.remainder, map_sub, h x]

theorem reduce_fixed (ps : List (Projector A)) (x : A)
    (h : ∀ p ∈ ps, p.map x = 0) : reduce ps x = x := by
  induction ps with
  | nil => rfl
  | cons p ps ih =>
    have ht : ∀ q ∈ ps, q.map x = 0 := fun q hq => h q (List.mem_cons_of_mem _ hq)
    have hp := h p (List.mem_cons_self)
    simp [reduce, ih ht, Projector.remainder, hp]

theorem reduce_killed (ps : List (Projector A)) (hc : Compatible ps)
    (p : Projector A) (hp : p ∈ ps) (x : A) : p.map (reduce ps x) = 0 := by
  induction ps with
  | nil => simp at hp
  | cons q qs ih =>
    have ht : Compatible qs := fun a ha b hb =>
      hc a (List.mem_cons_of_mem _ ha) b (List.mem_cons_of_mem _ hb)
    rcases List.mem_cons.mp hp with he | hm
    · subst p
      exact q.kills_remainder (reduce qs x)
    · have hcomm := hc p (List.mem_cons_of_mem _ hm) q List.mem_cons_self
      change p.map (q.remainder (reduce qs x)) = 0
      rw [map_remainder p q hcomm, ih ht hm]
      exact q.remainder.map_zero

theorem reduce_idempotent (ps : List (Projector A)) (hc : Compatible ps) (x : A) :
    reduce ps (reduce ps x) = reduce ps x :=
  reduce_fixed ps _ (fun p hp => reduce_killed ps hc p hp x)

theorem reduce_fixed_iff (ps : List (Projector A)) (hc : Compatible ps) (x : A) :
    reduce ps x = x ↔ ∀ p ∈ ps, p.map x = 0 := by
  constructor
  · intro h p hp
    rw [← h]
    exact reduce_killed ps hc p hp x
  · exact reduce_fixed ps x

/-- A reusable projector onto the intersection of the supplied kernels. -/
def kernelProjector (ps : List (Projector A)) (hc : Compatible ps) : Projector A :=
  ⟨reduce ps, reduce_idempotent ps hc⟩

theorem reduce_append (ps qs : List (Projector A)) (x : A) :
    reduce (ps ++ qs) x = reduce ps (reduce qs x) := by
  induction ps with
  | nil => rfl
  | cons p ps ih => simp [reduce, ih]

/-- Further subtraction by a subfamily leaves a jointly reduced value unchanged. -/
theorem reduce_absorbs (ps qs : List (Projector A)) (hc : Compatible qs)
    (hsub : ∀ p ∈ ps, p ∈ qs) (x : A) : reduce ps (reduce qs x) = reduce qs x :=
  reduce_fixed ps _ (fun p hp => reduce_killed qs hc p (hsub p hp) x)

end Subtraction

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

/-- Concrete client: evaluation at zero is an additive idempotent. -/
def leftProjection : Subtraction.Projector (ℚ → ℚ → ℚ) where
  map := { toFun := evalL, map_zero' := rfl, map_add' := fun _ _ => rfl }
  idempotent := fun _ => rfl

def rightProjection : Subtraction.Projector (ℚ → ℚ → ℚ) where
  map := { toFun := evalR, map_zero' := rfl, map_add' := fun _ _ => rfl }
  idempotent := fun _ => rfl

theorem evaluations_compatible : Subtraction.Compatible [leftProjection, rightProjection] := by
  intro p hp q hq I
  simp only [List.mem_cons, List.not_mem_nil, or_false] at hp hq
  rcases hp with rfl | rfl <;> rcases hq with rfl | rfl <;> rfl

theorem sixSum_is_reduction (I : ℚ → ℚ → ℚ) (x y : ℚ) :
    sixSum I x y = Subtraction.reduce [leftProjection, rightProjection] I x y := by
  rw [sixSum_eq_inclusion]
  change I x y - I 0 y - I x 0 + I 0 0 = (I x y - I x 0) - (I 0 y - I 0 0)
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

#print axioms evaluations_compatible
#print axioms sixSum_is_reduction
#print axioms Subtraction.Projector.kills_remainder
#print axioms Subtraction.map_remainder
#print axioms Subtraction.reduce_fixed
#print axioms Subtraction.reduce_killed
#print axioms Subtraction.reduce_idempotent
#print axioms Subtraction.reduce_fixed_iff
#print axioms Subtraction.kernelProjector
#print axioms Subtraction.reduce_append
#print axioms Subtraction.reduce_absorbs
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

end DressingFieldBphzContinuumFence
