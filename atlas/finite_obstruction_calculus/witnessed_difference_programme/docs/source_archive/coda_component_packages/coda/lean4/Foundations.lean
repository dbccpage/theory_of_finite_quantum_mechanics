import Std

/- Independent CODA-side proofs of the stated elementary lemmas.
   No sealed derivation is imported. AuthorityEffect: None. -/
namespace Coda

universe u v w

structure WitnessedDifference where
  Carrier : Type u
  apart : Carrier → Carrier → Prop
  irrefl : ∀ x, ¬ apart x x
  left : Carrier
  right : Carrier
  witness : apart left right

theorem witnessed_distinct (d : WitnessedDifference) : d.left ≠ d.right := by
  intro h
  have witness := d.witness
  rw [h] at witness
  exact d.irrefl d.right witness

theorem detector_pair_distinct {X : Type u} {V : Type v}
    (delta : X → X → V) (zero : V) (diagonal : ∀ x, delta x x = zero)
    {a b : X} (nonzero : delta a b ≠ zero) : a ≠ b := by
  intro h
  subst b
  exact nonzero (diagonal a)

def FiberConstant {X : Type u} {P : Type v} {Y : Type w}
    (p : X → P) (q : X → Y) : Prop :=
  ∀ x y, p x = p y → q x = q y

def Image {X : Type u} {P : Type v} (p : X → P) :=
  {z : P // ∃ x, p x = z}

def imagePoint {X : Type u} {P : Type v} (p : X → P) (x : X) : Image p :=
  ⟨p x, ⟨x, rfl⟩⟩

theorem observation_equivalence {X : Type u} {P : Type v} (p : X → P) :
    Equivalence (fun x y => p x = p y) :=
  ⟨fun _ => rfl, fun h => h.symm, fun h₁ h₂ => h₁.trans h₂⟩

theorem factor_implies_constant {X : Type u} {P : Type v} {Y : Type w}
    (p : X → P) (q : X → Y) (factor : P → Y)
    (spec : ∀ x, factor (p x) = q x) : FiberConstant p q := by
  intro x y h
  rw [← spec x, ← spec y, h]

theorem collision_obstructs_factor {X : Type u} {P : Type v} {Y : Type w}
    (p : X → P) (q : X → Y) {x y : X}
    (same : p x = p y) (different : q x ≠ q y) :
    ¬ ∃ factor : P → Y, ∀ z, factor (p z) = q z := by
  rintro ⟨factor, spec⟩
  exact different (factor_implies_constant p q factor spec x y same)

noncomputable def imageFactor {X : Type u} {P : Type v} {Y : Type w}
    (p : X → P) (q : X → Y) (z : Image p) : Y :=
  q (Classical.choose z.property)

theorem image_factor_spec {X : Type u} {P : Type v} {Y : Type w}
    (p : X → P) (q : X → Y) (h : FiberConstant p q) (x : X) :
    imageFactor p q (imagePoint p x) = q x := by
  exact h _ x (Classical.choose_spec (imagePoint p x).property)

theorem image_factor_iff {X : Type u} {P : Type v} {Y : Type w}
    (p : X → P) (q : X → Y) :
    (∃ factor : Image p → Y, ∀ x, factor (imagePoint p x) = q x) ↔
      FiberConstant p q := by
  constructor
  · rintro ⟨factor, spec⟩ x y h
    have hp : imagePoint p x = imagePoint p y := Subtype.ext h
    rw [← spec x, ← spec y, hp]
  · intro h
    exact ⟨imageFactor p q, image_factor_spec p q h⟩

theorem image_factor_unique {X : Type u} {P : Type v} {Y : Type w}
    (p : X → P) (q : X → Y) (f g : Image p → Y)
    (hf : ∀ x, f (imagePoint p x) = q x)
    (hg : ∀ x, g (imagePoint p x) = q x) : f = g := by
  funext z
  obtain ⟨x, hx⟩ := z.property
  have hz : imagePoint p x = z := Subtype.ext hx
  rw [← hz, hf, hg]

theorem coarsening_preserves_collision {X : Type u} {P : Type v} {Y : Type w}
    {p : X → P} {q : X → Y} {x y : X} (same : p x = p y)
    (different : q x ≠ q y) {Z : Type} (c : P → Z) :
    c (p x) = c (p y) ∧ q x ≠ q y :=
  ⟨congrArg c same, different⟩

theorem augmentation_must_separate {X : Type u} {P : Type v} {Y : Type w}
    (p : X → P) (q : X → Y) (factor : P → Y)
    (spec : ∀ x, factor (p x) = q x) {x y : X}
    (different : q x ≠ q y) : p x ≠ p y := by
  intro same
  exact different (factor_implies_constant p q factor spec x y same)

def Exhausted {X : Type u} (menu works : X → Prop) : Prop :=
  ∀ x, menu x → ¬ works x

theorem witness_refutes_exhaustion {X : Type u} {menu works : X → Prop}
    {x : X} (member : menu x) (working : works x) : ¬ Exhausted menu works := by
  intro h
  exact h x member working

theorem exhausted_submenu {X : Type u} {small large works : X → Prop}
    (sub : ∀ x, small x → large x) (h : Exhausted large works) :
    Exhausted small works := by
  intro x hx
  exact h x (sub x hx)

theorem truncated_search_countermodel :
    Exhausted (fun b : Bool => b = false) (fun b => b = true) ∧
    ¬ Exhausted (fun _ : Bool => True) (fun b => b = true) := by
  constructor
  · intro b hb
    subst b
    decide
  · intro h
    exact h true trivial rfl

theorem tied_minima {X : Type u} {V : Type v} (le : V → V → Prop)
    (cost : X → V) {a b : X} (same : cost a = cost b)
    (least : ∀ x, le (cost a) (cost x)) : ∀ x, le (cost b) (cost x) := by
  intro x
  rw [← same]
  exact least x

end Coda
