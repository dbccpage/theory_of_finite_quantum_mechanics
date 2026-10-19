import Mathlib.Data.List.Basic

/-! AuthorityEffect: None. Universal map/fiber and all-word necessity
arguments for the declared predicates. Fixed Rust witness tables and their
case completeness use separate source/native evidence; no extracted Rust
constructor or phenomenological theorem is claimed. -/
namespace TFQM.FunctionalClassification
variable {X I R S : Type}

def FiberConstant (q : X → R) (s : X → S) : Prop :=
  ∀ x y, q x = q y → s x = s y
def Stable (value : X → R) (t : X → X) : Prop := ∀ x, value x = value (t x)
noncomputable def factor (q : X → R) (s : X → S) (y : Set.range q) : S :=
  s (Classical.choose y.property)
theorem factor_spec (q : X → R) (s : X → S) (h : FiberConstant q s) (x : X) :
    factor q s ⟨q x, ⟨x, rfl⟩⟩ = s x :=
  h _ _ (Classical.choose_spec (show ∃ a, q a = q x from ⟨x, rfl⟩))
theorem factor_iff (q : X → R) (s : X → S) :
    (∃ g : Set.range q → S, ∀ x, g ⟨q x, ⟨x, rfl⟩⟩ = s x) ↔ FiberConstant q s := by
  constructor
  · rintro ⟨g, law⟩ x y same
    have sub : (⟨q x, ⟨x, rfl⟩⟩ : Set.range q) = ⟨q y, ⟨y, rfl⟩⟩ := Subtype.ext same
    exact (law x).symm.trans ((congrArg g sub).trans (law y))
  · intro h
    exact ⟨factor q s, factor_spec q s h⟩
theorem injective_fibers (q : X → R) (s : X → S) (h : Function.Injective q) :
    FiberConstant q s := by
  intro x y same
  exact congrArg s (h same)
theorem linked_stable (q : X → R) (s : X → S) (t : X → X)
    (linked : FiberConstant q s) (stable : Stable q t) : Stable s t := by
  intro x
  exact linked x (t x) (stable x)
theorem functional_necessary (q : X → R) (s : X → S) (t : X → X) :
    (Function.Injective q → FiberConstant q s) ∧
      (FiberConstant q s → Stable q t → Stable s t) :=
  ⟨injective_fibers q s, linked_stable q s t⟩

def Tolerance (q : X → R) (s : X → S) : Prop := ∃ x y, q x ≠ q y ∧ s x = s y
theorem recognized_injective_iff (q : X → R) (s : X → S) (linked : FiberConstant q s) :
    Function.Injective s ↔ Function.Injective q ∧ ¬Tolerance q s := by
  constructor
  · intro inj
    constructor
    · intro x y same
      exact inj (linked x y same)
    · rintro ⟨x, y, different, same⟩
      exact different (congrArg q (inj same))
  · rintro ⟨inj, noTolerance⟩ x y same
    apply inj
    by_contra different
    exact noTolerance ⟨x, y, different, same⟩

def run (d : X → I → X) (x : X) : List I → X
  | [] => x
  | i :: w => run d (d x i) w
def FutureEqual (s : X → S) (d : X → I → X) (x y : X) : Prop :=
  ∀ w, s (run d x w) = s (run d y w)
def Minimal (s : X → S) (d : X → I → X) : Prop := ∀ x y, FutureEqual s d x y → x = y
theorem empty_word {s : X → S} {d : X → I → X} {x y : X}
    (h : FutureEqual s d x y) : s x = s y := h []
theorem injective_minimal (s : X → S) (d : X → I → X) (h : Function.Injective s) :
    Minimal s d := by
  intro x y same
  exact h (empty_word same)
theorem inactive_run (d : X → I → X) (inactive : ∀ x i, d x i = x) (x : X) (w : List I) :
    run d x w = x := by
  induction w generalizing x with
  | nil => rfl
  | cons i w ih => simpa only [run, inactive] using ih x
theorem inactive_future (s : X → S) (d : X → I → X) (inactive : ∀ x i, d x i = x) (x y : X) :
    FutureEqual s d x y ↔ s x = s y := by
  constructor
  · exact empty_word
  · intro same w
    simpa only [inactive_run d inactive] using same
theorem inactive_minimal (s : X → S) (d : X → I → X) (inactive : ∀ x i, d x i = x) :
    Minimal s d ↔ Function.Injective s := by
  constructor
  · intro minimal x y same
    exact minimal x y ((inactive_future s d inactive x y).mpr same)
  · exact injective_minimal s d
theorem inactive_bijective (d : X → I → X) (inactive : ∀ x i, d x i = x) (i : I) :
    Function.Bijective (fun x => d x i) := by
  constructor
  · intro x y same
    simpa only [inactive] using same
  · intro y
    exact ⟨y, inactive y i⟩
theorem retention_injective_necessity (q : X → R) (s : X → S) (d : X → I → X)
    (linked : FiberConstant q s) (observable : Function.Injective q) (noTolerance : ¬Tolerance q s) :
    Minimal s d :=
  injective_minimal s d ((recognized_injective_iff q s linked).mpr ⟨observable, noTolerance⟩)
theorem retention_inactive_necessity (q : X → R) (s : X → S) (d : X → I → X)
    (linked : FiberConstant q s) (inactive : ∀ x i, d x i = x) :
    (∀ i, Function.Bijective (fun x => d x i)) ∧
      (Minimal s d ↔ Function.Injective q ∧ ¬Tolerance q s) :=
  ⟨inactive_bijective d inactive, (inactive_minimal s d inactive).trans (recognized_injective_iff q s linked)⟩
theorem singleton_injective [Subsingleton X] (q : X → R) : Function.Injective q := by
  intro x y _
  exact Subsingleton.elim x y
theorem singleton_no_tolerance [Subsingleton X] (q : X → R) (s : X → S) : ¬Tolerance q s := by
  rintro ⟨x, y, different, _⟩
  exact different (congrArg q (Subsingleton.elim x y))
theorem singleton_inactive [Subsingleton X] (d : X → I → X) : ∀ x i, d x i = x := by
  intro x i
  exact Subsingleton.elim _ _
theorem singleton_minimal [Subsingleton X] (s : X → S) (d : X → I → X) : Minimal s d := by
  intro x y _
  exact Subsingleton.elim x y

def Allowed (linked presentationStable reportStable blind : Bool) : Bool :=
  (blind || linked) && !(linked && presentationStable && !reportStable)
theorem twenty_signatures :
    ((List.range 32).filter (fun bits => Allowed (bits % 2 == 1) (bits / 2 % 2 == 1)
      (bits / 4 % 2 == 1) (bits / 16 % 2 == 1))).length = 20 := by decide
theorem implication_countermodel_iff {N : Nat} (allowed : (Fin N → Bool) → Prop)
    (premises : (Fin N → Bool) → Prop) (conclusion : (Fin N → Bool) → Prop) :
    (¬∀ flags, allowed flags → premises flags → conclusion flags) ↔
      ∃ flags, allowed flags ∧ premises flags ∧ ¬conclusion flags := by
  classical
  simp only [not_forall, not_imp]
end TFQM.FunctionalClassification

#print axioms TFQM.FunctionalClassification.factor_spec
#print axioms TFQM.FunctionalClassification.factor_iff
#print axioms TFQM.FunctionalClassification.injective_fibers
#print axioms TFQM.FunctionalClassification.linked_stable
#print axioms TFQM.FunctionalClassification.functional_necessary
#print axioms TFQM.FunctionalClassification.recognized_injective_iff
#print axioms TFQM.FunctionalClassification.empty_word
#print axioms TFQM.FunctionalClassification.injective_minimal
#print axioms TFQM.FunctionalClassification.inactive_run
#print axioms TFQM.FunctionalClassification.inactive_future
#print axioms TFQM.FunctionalClassification.inactive_minimal
#print axioms TFQM.FunctionalClassification.inactive_bijective
#print axioms TFQM.FunctionalClassification.retention_injective_necessity
#print axioms TFQM.FunctionalClassification.retention_inactive_necessity
#print axioms TFQM.FunctionalClassification.singleton_injective
#print axioms TFQM.FunctionalClassification.singleton_no_tolerance
#print axioms TFQM.FunctionalClassification.singleton_inactive
#print axioms TFQM.FunctionalClassification.singleton_minimal
#print axioms TFQM.FunctionalClassification.twenty_signatures
#print axioms TFQM.FunctionalClassification.implication_countermodel_iff
