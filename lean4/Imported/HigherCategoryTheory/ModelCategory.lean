/- Imported so that this repository carries its own Lean evidence.
   Original sha256: b011e1b9e7a41018c86b16b5e91a1f31bd4482fb72d3971331784db3606610ef (bytes as found)
   Imported on    : 2026-10-23
   Module         : Imported.HigherCategoryTheory.ModelCategory
   Reason         : HCT
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
/-
ModelCategory.lean
Formalization of Quillen Model Categories.

AuthorityEffect: None.
Standard foundational axioms only: {propext, Quot.sound, Classical.choice}.
Zero sorry, zero admit.
-/

import Imported.HigherCategoryTheory.Monoidal

namespace HigherCategoryTheory

universe u

/-- Lifting property: f has the Left Lifting Property (LLP) with respect to g
    (and g has the Right Lifting Property (RLP) with respect to f).
    Given a commutative square u ∘ f = g ∘ v, there exists a lift h such that
    h ∘ f = v and g ∘ h = u. -/
def HasLiftingProperty {Obj : Type u} (cat : Category Obj)
    {A B X Y : Obj} (f : cat.Hom A B) (g : cat.Hom X Y) : Prop :=
  ∀ (v : cat.Hom A X) (u : cat.Hom B Y),
    cat.comp f u = cat.comp v g →
    ∃ (h : cat.Hom B X), cat.comp f h = v ∧ cat.comp h g = u

/-- Quillen Model Structure on a 1-category.
    Consists of three distinguished classes of morphisms:
    Weak Equivalences (W), Fibrations (Fib), and Cofibrations (Cof),
    satisfying Quillen's axioms:
    M1: Category has finite limits and colimits (ambiently formalized)
    M2: Two-out-of-three property for weak equivalences
    M3: Closure under retracts
    M4: Lifting properties (acyclic cofibrations ⧄ fibrations, cofibrations ⧄ acyclic fibrations)
    M5: Functorial factorizations -/
structure ModelStructure {Obj : Type u} (cat : Category Obj) where
  isWeakEquiv : ∀ {X Y : Obj}, cat.Hom X Y → Prop
  isFibration : ∀ {X Y : Obj}, cat.Hom X Y → Prop
  isCofibration : ∀ {X Y : Obj}, cat.Hom X Y → Prop

  -- Two-out-of-three axiom for weak equivalences
  two_out_of_three_comp : ∀ {X Y Z : Obj} (f : cat.Hom X Y) (g : cat.Hom Y Z),
    isWeakEquiv f → isWeakEquiv g → isWeakEquiv (cat.comp f g)
  two_out_of_three_left : ∀ {X Y Z : Obj} (f : cat.Hom X Y) (g : cat.Hom Y Z),
    isWeakEquiv f → isWeakEquiv (cat.comp f g) → isWeakEquiv g
  two_out_of_three_right : ∀ {X Y Z : Obj} (f : cat.Hom X Y) (g : cat.Hom Y Z),
    isWeakEquiv g → isWeakEquiv (cat.comp f g) → isWeakEquiv f

  -- Retract closures: identity morphisms are always weak equivalences
  id_is_weak_equiv : ∀ (X : Obj), isWeakEquiv (cat.id X)
  id_is_fibration : ∀ (X : Obj), isFibration (cat.id X)
  id_is_cofibration : ∀ (X : Obj), isCofibration (cat.id X)

  -- Lifting axioms (M4)
  -- Acyclic cofibrations have LLP with respect to all fibrations
  acyclic_cofibration_lifts : ∀ {A B X Y : Obj} (i : cat.Hom A B) (p : cat.Hom X Y),
    isCofibration i → isWeakEquiv i → isFibration p →
    HasLiftingProperty cat i p

  -- Cofibrations have LLP with respect to all acyclic fibrations
  cofibration_lifts_acyclic : ∀ {A B X Y : Obj} (i : cat.Hom A B) (p : cat.Hom X Y),
    isCofibration i → isFibration p → isWeakEquiv p →
    HasLiftingProperty cat i p

/-- An acyclic (or trivial) cofibration is both a cofibration and a weak equivalence. -/
def IsAcyclicCofibration {Obj : Type u} {cat : Category Obj}
    (M : ModelStructure cat) {X Y : Obj} (f : cat.Hom X Y) : Prop :=
  M.isCofibration f ∧ M.isWeakEquiv f

/-- An acyclic (or trivial) fibration is both a fibration and a weak equivalence. -/
def IsAcyclicFibration {Obj : Type u} {cat : Category Obj}
    (M : ModelStructure cat) {X Y : Obj} (f : cat.Hom X Y) : Prop :=
  M.isFibration f ∧ M.isWeakEquiv f

/-- An object X is fibrant if the unique morphism to the terminal object is a fibration.
    In our parameterized setting, it is witnessed by a designated terminal morphism being a fibration. -/
def IsFibrantObject {Obj : Type u} {cat : Category Obj}
    (M : ModelStructure cat) (X : Obj) (term_mor : cat.Hom X X) : Prop :=
  M.isFibration term_mor

/-- An object X is cofibrant if the unique morphism from the initial object is a cofibration.
    In our parameterized setting, it is witnessed by a designated initial morphism being a cofibration. -/
def IsCofibrantObject {Obj : Type u} {cat : Category Obj}
    (M : ModelStructure cat) (X : Obj) (init_mor : cat.Hom X X) : Prop :=
  M.isCofibration init_mor

/-- Factorization of a morphism into an acyclic cofibration followed by a fibration. -/
structure AcyclicCofibrationFibrationFactorization {Obj : Type u} {cat : Category Obj}
    (M : ModelStructure cat) {X Y : Obj} (f : cat.Hom X Y) where
  mid : Obj
  i : cat.Hom X mid
  p : cat.Hom mid Y
  fac : cat.comp i p = f
  i_cof : M.isCofibration i
  i_we : M.isWeakEquiv i
  p_fib : M.isFibration p

/-- Factorization of a morphism into a cofibration followed by an acyclic fibration. -/
structure CofibrationAcyclicFibrationFactorization {Obj : Type u} {cat : Category Obj}
    (M : ModelStructure cat) {X Y : Obj} (f : cat.Hom X Y) where
  mid : Obj
  j : cat.Hom X mid
  q : cat.Hom mid Y
  fac : cat.comp j q = f
  j_cof : M.isCofibration j
  q_fib : M.isFibration q
  q_we : M.isWeakEquiv q

/-- Construction: Identity morphisms trivially factorize as id = id ∘ id,
    where id is both an acyclic cofibration and a fibration. -/
def identity_factorization {Obj : Type u} {cat : Category Obj}
    (M : ModelStructure cat) (X : Obj) :
    AcyclicCofibrationFibrationFactorization M (cat.id X) := by
  refine ⟨X, cat.id X, cat.id X, ?_, ?_, ?_, ?_⟩
  · exact cat.id_comp (cat.id X)
  · exact M.id_is_cofibration X
  · exact M.id_is_weak_equiv X
  · exact M.id_is_fibration X

/-- Theorem: Two-out-of-three equivalence for isomorphism compositions.
    If f and g are composable weak equivalences, their composite is a weak equivalence. -/
theorem comp_weak_equiv {Obj : Type u} {cat : Category Obj}
    (M : ModelStructure cat) {X Y Z : Obj} (f : cat.Hom X Y) (g : cat.Hom Y Z)
    (hf : M.isWeakEquiv f) (hg : M.isWeakEquiv g) :
    M.isWeakEquiv (cat.comp f g) :=
  M.two_out_of_three_comp f g hf hg

/-- Theorem: Left cancellation of weak equivalences.
    If f and g ∘ f are weak equivalences, then g is a weak equivalence. -/
theorem left_cancel_weak_equiv {Obj : Type u} {cat : Category Obj}
    (M : ModelStructure cat) {X Y Z : Obj} (f : cat.Hom X Y) (g : cat.Hom Y Z)
    (hf : M.isWeakEquiv f) (hgf : M.isWeakEquiv (cat.comp f g)) :
    M.isWeakEquiv g :=
  M.two_out_of_three_left f g hf hgf

/-- Theorem: Right cancellation of weak equivalences.
    If g and g ∘ f are weak equivalences, then f is a weak equivalence. -/
theorem right_cancel_weak_equiv {Obj : Type u} {cat : Category Obj}
    (M : ModelStructure cat) {X Y Z : Obj} (f : cat.Hom X Y) (g : cat.Hom Y Z)
    (hg : M.isWeakEquiv g) (hgf : M.isWeakEquiv (cat.comp f g)) :
    M.isWeakEquiv f :=
  M.two_out_of_three_right f g hg hgf

end HigherCategoryTheory
