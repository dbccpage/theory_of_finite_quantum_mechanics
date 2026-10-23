/-
Copyright (c) 2026 CODA Authors. All rights reserved.
Released under Apache 2.0 / CC-BY-4.0 license.
Authors: Jeremy H. Carroll

CODA: Calculus of Obstruction, Descent, and Authority
Founding Discipline & CD-12 Groupoid Faithful Functor Target

AuthorityEffect: None.
-/

import Mathlib.Data.Real.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Tactic

namespace CodaDiscipline

/-- CD-01 / CD-03: A finite presentation (V, R) consists of a finite carrier
    index set and declared pairwise primitive differences. -/
structure Presentation where
  carrier : Type
  [fintypeCarrier : Fintype carrier]
  [decEqCarrier : DecidableEq carrier]
  diff : carrier → carrier → ℝ
  diff_self : ∀ x, diff x x = 0
  diff_nonneg : ∀ x y, 0 ≤ diff x y

attribute [instance] Presentation.fintypeCarrier Presentation.decEqCarrier

/-- Concrete comparison span between two presentations. -/
structure ComparisonSpan (P1 P2 : Presentation) where
  midCarrier : Type
  [fintypeMid : Fintype midCarrier]
  [decEqMid : DecidableEq midCarrier]
  leftMap : midCarrier → P1.carrier
  rightMap : midCarrier → P2.carrier
  spanCost : ℝ
  spanCost_nonneg : 0 ≤ spanCost

attribute [instance] ComparisonSpan.fintypeMid ComparisonSpan.decEqMid

/-- Diagonal comparison span on any presentation (Identity morphism candidate). -/
def diagSpan (P : Presentation) : ComparisonSpan P P where
  midCarrier := P.carrier
  leftMap := id
  rightMap := id
  spanCost := 0
  spanCost_nonneg := le_rfl

/-- Composition of comparison spans via standard pullback. -/
def compSpan {P1 P2 P3 : Presentation} (S1 : ComparisonSpan P1 P2) (S2 : ComparisonSpan P2 P3) :
    ComparisonSpan P1 P3 where
  midCarrier := { p : S1.midCarrier × S2.midCarrier // S1.rightMap p.1 = S2.leftMap p.2 }
  leftMap p := S1.leftMap p.val.1
  rightMap p := S2.rightMap p.val.2
  spanCost := S1.spanCost + S2.spanCost
  spanCost_nonneg := add_nonneg S1.spanCost_nonneg S2.spanCost_nonneg

/-- Intensional execution trace in CODA_trace. -/
structure Trace (P1 P2 : Presentation) where
  steps : ℕ
  workCost : ℝ
  workCost_nonneg : 0 ≤ workCost
  underlyingSpan : ComparisonSpan P1 P2

/-- Identity trace. -/
def idTrace (P : Presentation) : Trace P P where
  steps := 0
  workCost := 0
  workCost_nonneg := le_rfl
  underlyingSpan := diagSpan P

/-- Composition of execution traces. -/
def compTrace {P1 P2 P3 : Presentation} (T1 : Trace P1 P2) (T2 : Trace P2 P3) : Trace P1 P3 where
  steps := T1.steps + T2.steps
  workCost := T1.workCost + T2.workCost
  workCost_nonneg := add_nonneg T1.workCost_nonneg T2.workCost_nonneg
  underlyingSpan := compSpan T1.underlyingSpan T2.underlyingSpan

/-- Erasure quotient map q : CODA_trace → CODA_pres. -/
def eraseTrace {P1 P2 : Presentation} (T : Trace P1 P2) : ComparisonSpan P1 P2 :=
  T.underlyingSpan

/-- Extensional cost diagnostic c_mor on comparison spans. -/
def extCost {P1 P2 : Presentation} (S : ComparisonSpan P1 P2) : ℝ :=
  S.spanCost

/-- Intensional trace cost diagnostic c_trace on traces. -/
def traceCost {P1 P2 : Presentation} (T : Trace P1 P2) : ℝ :=
  T.workCost

theorem diagSpan_cost_zero (P : Presentation) : extCost (diagSpan P) = 0 := rfl

theorem compSpan_cost_subadditive {P1 P2 P3 : Presentation}
    (S1 : ComparisonSpan P1 P2) (S2 : ComparisonSpan P2 P3) :
    extCost (compSpan S1 S2) ≤ extCost S1 + extCost S2 := by
  dsimp [extCost, compSpan]
  exact le_rfl

/-- Finite Groupoid structure over a finite object set. -/
structure FiniteGroupoid where
  Obj : Type
  [fintypeObj : Fintype Obj]
  [decEqObj : DecidableEq Obj]
  Mor : Obj → Obj → Type
  [fintypeMor : ∀ x y, Fintype (Mor x y)]
  [decEqMor : ∀ x y, DecidableEq (Mor x y)]
  idMor : ∀ x, Mor x x
  compMor : ∀ {x y z}, Mor x y → Mor y z → Mor x z
  invMor : ∀ {x y}, Mor x y → Mor y x
  id_comp : ∀ {x y} (f : Mor x y), compMor (idMor x) f = f
  comp_id : ∀ {x y} (f : Mor x y), compMor f (idMor y) = f
  comp_assoc : ∀ {w x y z} (f : Mor w x) (g : Mor x y) (h : Mor y z),
    compMor (compMor f g) h = compMor f (compMor g h)
  inv_left : ∀ {x y} (f : Mor x y), compMor (invMor f) f = idMor y
  inv_right : ∀ {x y} (f : Mor x y), compMor f (invMor f) = idMor x

attribute [instance] FiniteGroupoid.fintypeObj FiniteGroupoid.decEqObj
attribute [instance] FiniteGroupoid.fintypeMor FiniteGroupoid.decEqMor

/-- CD-12 Explicit Model Construction:
    Point presentation for any groupoid object. -/
def pointPresentation (G : FiniteGroupoid) (x : G.Obj) : Presentation where
  carrier := Unit
  diff _ _ := 0
  diff_self _ := rfl
  diff_nonneg _ _ := le_rfl

/-- Morphism representation span for groupoid arrow f : x → y. -/
def groupoidArrowSpan (G : FiniteGroupoid) {x y : G.Obj} (_ : G.Mor x y) :
    ComparisonSpan (pointPresentation G x) (pointPresentation G y) where
  midCarrier := Unit
  leftMap _ := ()
  rightMap _ := ()
  spanCost := 0
  spanCost_nonneg := le_rfl

/-- Concrete execution trace for groupoid arrow f. -/
def groupoidArrowTrace (G : FiniteGroupoid) {x y : G.Obj} (f : G.Mor x y) (work : ℝ) (h_w : 0 ≤ work) :
    Trace (pointPresentation G x) (pointPresentation G y) where
  steps := 1
  workCost := work
  workCost_nonneg := h_w
  underlyingSpan := groupoidArrowSpan G f

/-- Identity Preservation Theorem:
    The embedded identity morphism has zero extensional cost. -/
theorem embedding_id_cost (G : FiniteGroupoid) (x : G.Obj) :
    extCost (groupoidArrowSpan G (G.idMor x)) = 0 := rfl

/-- Composition Extensional Cost Theorem:
    Composite of any two embedded arrows has zero extensional cost. -/
theorem embedding_comp_cost (G : FiniteGroupoid) {x y z : G.Obj}
    (f : G.Mor x y) (g : G.Mor y z) :
    extCost (compSpan (groupoidArrowSpan G f) (groupoidArrowSpan G g)) = 0 := by
  dsimp [extCost, compSpan, groupoidArrowSpan]
  ring

/-- Inverse Extensional Round-Trip Law:
    c_mor(E(f⁻¹) ⋆ E(f)) = 0. -/
theorem embedding_inverse_ext_cost_zero (G : FiniteGroupoid) {x y : G.Obj}
    (f : G.Mor x y) :
    extCost (compSpan (groupoidArrowSpan G (G.invMor f)) (groupoidArrowSpan G f)) = 0 := by
  dsimp [extCost, compSpan, groupoidArrowSpan]
  ring

/-- Intensional Trace Work Positivity:
    Intensional composition of inverse traces carries non-negative work cost. -/
theorem embedding_inverse_trace_cost_nonneg (G : FiniteGroupoid) {x y : G.Obj}
    (f : G.Mor x y) (w1 w2 : ℝ) (hw1 : 0 ≤ w1) (hw2 : 0 ≤ w2) :
    0 ≤ traceCost (compTrace (groupoidArrowTrace G (G.invMor f) w1 hw1) (groupoidArrowTrace G f w2 hw2)) := by
  dsimp [traceCost, compTrace, groupoidArrowTrace]
  exact add_nonneg hw1 hw2

/-- Erasure of Trace Preserves Underlying Span:
    q(τ_f) = S_f. -/
theorem trace_erasure_correct (G : FiniteGroupoid) {x y : G.Obj}
    (f : G.Mor x y) (w : ℝ) (hw : 0 ≤ w) :
    eraseTrace (groupoidArrowTrace G f w hw) = groupoidArrowSpan G f := rfl

#print axioms diagSpan_cost_zero
#print axioms compSpan_cost_subadditive
#print axioms embedding_id_cost
#print axioms embedding_comp_cost
#print axioms embedding_inverse_ext_cost_zero
#print axioms embedding_inverse_trace_cost_nonneg
#print axioms trace_erasure_correct

end CodaDiscipline
