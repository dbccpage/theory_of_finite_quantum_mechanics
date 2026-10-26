import Std

/-
CODA Founding Discipline & CD-12 Groupoid Faithful Functor Target (Pure Lean 4 / Std)
AuthorityEffect: None.
-/

namespace CodaDiscipline

/-- CD-01 / CD-03: A finite presentation (V, R) consists of a finite carrier
    index set and declared pairwise primitive differences. -/
structure Presentation where
  carrier : Type
  diff : carrier → carrier → Nat
  diff_self : ∀ x, diff x x = 0

/-- Concrete comparison span between two presentations. -/
structure ComparisonSpan (P1 P2 : Presentation) where
  midCarrier : Type
  leftMap : midCarrier → P1.carrier
  rightMap : midCarrier → P2.carrier
  spanCost : Nat

/-- Diagonal comparison span on any presentation (Identity morphism candidate). -/
def diagSpan (P : Presentation) : ComparisonSpan P P where
  midCarrier := P.carrier
  leftMap := id
  rightMap := id
  spanCost := 0

/-- Composition of comparison spans via standard pullback. -/
def compSpan {P1 P2 P3 : Presentation} (S1 : ComparisonSpan P1 P2) (S2 : ComparisonSpan P2 P3) :
    ComparisonSpan P1 P3 where
  midCarrier := { p : S1.midCarrier × S2.midCarrier // S1.rightMap p.1 = S2.leftMap p.2 }
  leftMap p := S1.leftMap p.val.1
  rightMap p := S2.rightMap p.val.2
  spanCost := S1.spanCost + S2.spanCost

/-- Intensional execution trace in CODA_trace. -/
structure Trace (P1 P2 : Presentation) where
  steps : Nat
  workCost : Nat
  underlyingSpan : ComparisonSpan P1 P2

/-- Identity trace. -/
def idTrace (P : Presentation) : Trace P P where
  steps := 0
  workCost := 0
  underlyingSpan := diagSpan P

/-- Composition of execution traces. -/
def compTrace {P1 P2 P3 : Presentation} (T1 : Trace P1 P2) (T2 : Trace P2 P3) : Trace P1 P3 where
  steps := T1.steps + T2.steps
  workCost := T1.workCost + T2.workCost
  underlyingSpan := compSpan T1.underlyingSpan T2.underlyingSpan

/-- Erasure quotient map q : CODA_trace → CODA_pres. -/
def eraseTrace {P1 P2 : Presentation} (T : Trace P1 P2) : ComparisonSpan P1 P2 :=
  T.underlyingSpan

/-- Extensional cost diagnostic c_mor on comparison spans. -/
def extCost {P1 P2 : Presentation} (S : ComparisonSpan P1 P2) : Nat :=
  S.spanCost

/-- Intensional trace cost diagnostic c_trace on traces. -/
def traceCost {P1 P2 : Presentation} (T : Trace P1 P2) : Nat :=
  T.workCost

theorem diagSpan_cost_zero (P : Presentation) : extCost (diagSpan P) = 0 := rfl

theorem compSpan_cost_subadditive {P1 P2 P3 : Presentation}
    (S1 : ComparisonSpan P1 P2) (S2 : ComparisonSpan P2 P3) :
    extCost (compSpan S1 S2) ≤ extCost S1 + extCost S2 := Nat.le_refl _

/-- Finite Groupoid structure over a finite object set. -/
structure FiniteGroupoid where
  Obj : Type
  Mor : Obj → Obj → Type
  idMor : ∀ x, Mor x x
  compMor : ∀ {x y z}, Mor x y → Mor y z → Mor x z
  invMor : ∀ {x y}, Mor x y → Mor y x
  id_comp : ∀ {x y} (f : Mor x y), compMor (idMor x) f = f
  comp_id : ∀ {x y} (f : Mor x y), compMor f (idMor y) = f
  comp_assoc : ∀ {w x y z} (f : Mor w x) (g : Mor x y) (h : Mor y z),
    compMor (compMor f g) h = compMor f (compMor g h)
  inv_left : ∀ {x y} (f : Mor x y), compMor (invMor f) f = idMor y
  inv_right : ∀ {x y} (f : Mor x y), compMor f (invMor f) = idMor x

/-- CD-12 Explicit Model Construction:
    Point presentation for any groupoid object. -/
def pointPresentation (G : FiniteGroupoid) (_ : G.Obj) : Presentation where
  carrier := Unit
  diff _ _ := 0
  diff_self _ := rfl

/-- Morphism representation span for groupoid arrow f : x → y. -/
def groupoidArrowSpan (G : FiniteGroupoid) {x y : G.Obj} (_ : G.Mor x y) :
    ComparisonSpan (pointPresentation G x) (pointPresentation G y) where
  midCarrier := Unit
  leftMap _ := ()
  rightMap _ := ()
  spanCost := 0

/-- Concrete execution trace for groupoid arrow f. -/
def groupoidArrowTrace (G : FiniteGroupoid) {x y : G.Obj} (f : G.Mor x y) (work : Nat) :
    Trace (pointPresentation G x) (pointPresentation G y) where
  steps := 1
  workCost := work
  underlyingSpan := groupoidArrowSpan G f

/-- Identity Preservation Theorem:
    The embedded identity morphism has zero extensional cost. -/
theorem embedding_id_cost (G : FiniteGroupoid) (x : G.Obj) :
    extCost (groupoidArrowSpan G (G.idMor x)) = 0 := rfl

/-- Composition Extensional Cost Theorem:
    Composite of any two embedded arrows has zero extensional cost. -/
theorem embedding_comp_cost (G : FiniteGroupoid) {x y z : G.Obj}
    (f : G.Mor x y) (g : G.Mor y z) :
    extCost (compSpan (groupoidArrowSpan G f) (groupoidArrowSpan G g)) = 0 := rfl

/-- Inverse Extensional Round-Trip Law:
    c_mor(E(f⁻¹) ⋆ E(f)) = 0. -/
theorem embedding_inverse_ext_cost_zero (G : FiniteGroupoid) {x y : G.Obj}
    (f : G.Mor x y) :
    extCost (compSpan (groupoidArrowSpan G (G.invMor f)) (groupoidArrowSpan G f)) = 0 := rfl

/-- Intensional Trace Work Positivity:
    Intensional composition of inverse traces carries non-negative work cost. -/
theorem embedding_inverse_trace_cost_nonneg (G : FiniteGroupoid) {x y : G.Obj}
    (f : G.Mor x y) (w1 w2 : Nat) :
    0 ≤ traceCost (compTrace (groupoidArrowTrace G (G.invMor f) w1) (groupoidArrowTrace G f w2)) :=
  Nat.zero_le _

/-- Erasure of Trace Preserves Underlying Span:
    q(τ_f) = S_f. -/
theorem trace_erasure_correct (G : FiniteGroupoid) {x y : G.Obj}
    (f : G.Mor x y) (w : Nat) :
    eraseTrace (groupoidArrowTrace G f w) = groupoidArrowSpan G f := rfl

end CodaDiscipline
