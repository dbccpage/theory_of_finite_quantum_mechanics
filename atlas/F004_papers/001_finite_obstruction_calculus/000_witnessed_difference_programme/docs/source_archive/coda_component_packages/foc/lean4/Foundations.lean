import Mathlib.Data.Set.Function

/-! Independently defined CODA interfaces. No sealed source is imported. -/
namespace Coda
universe u v w

structure WitnessedDifference where
  Carrier : Type u
  relation : Carrier → Carrier → Prop
  irrefl : ∀ x, ¬ relation x x
  left : Carrier
  right : Carrier
  witness : relation left right

theorem witnessed_distinct (d : WitnessedDifference) : d.left ≠ d.right := by
  intro h
  exact d.irrefl d.left (h ▸ d.witness)

def differenceOfDetector {X Δ : Type u} (δ : X → X → Δ) (zero : Δ)
    (diagonal : ∀ x, δ x x = zero) (a b : X) (w : δ a b ≠ zero) : WitnessedDifference where
  Carrier := X
  relation := fun x y => δ x y ≠ zero
  irrefl := fun x h => h (diagonal x)
  left := a
  right := b
  witness := w

theorem detector_pair_distinct {X Δ : Type u} (δ : X → X → Δ) (zero : Δ)
    (diagonal : ∀ x, δ x x = zero) (a b : X) (w : δ a b ≠ zero) : a ≠ b :=
  witnessed_distinct (differenceOfDetector δ zero diagonal a b w)

theorem observation_equivalence {X P : Type*} (p : X → P) :
    Equivalence (fun x y => p x = p y) :=
  ⟨fun _ => rfl, fun h => h.symm, fun h₁ h₂ => h₁.trans h₂⟩

def FiberConstant {X : Type u} {P : Type v} {Y : Type w}
    (p : X → P) (q : X → Y) : Prop :=
  ∀ x y, p x = p y → q x = q y

def Factors {X : Type u} {P : Type v} {Y : Type w}
    (p : X → P) (q : X → Y) : Prop :=
  ∃ g : P → Y, ∀ x, g (p x) = q x

theorem factor_implies_constant {X : Type u} {P : Type v} {Y : Type w}
    {p : X → P} {q : X → Y} (h : Factors p q) : FiberConstant p q := by
  obtain ⟨g, hg⟩ := h
  intro x y hxy
  rw [← hg x, ← hg y, hxy]

theorem collision_obstructs_factor {X : Type u} {P : Type v} {Y : Type w}
    {p : X → P} {q : X → Y} {x y : X}
    (same : p x = p y) (different : q x ≠ q y) : ¬ Factors p q := by
  intro h
  exact different (factor_implies_constant h x y same)

noncomputable def imageFactor {X : Type u} {P : Type v} {Y : Type w}
    (p : X → P) (q : X → Y) : Set.range p → Y :=
  fun z => q (Classical.choose z.property)

theorem image_factor_spec {X : Type u} {P : Type v} {Y : Type w}
    {p : X → P} {q : X → Y} (h : FiberConstant p q) (x : X) :
    imageFactor p q ⟨p x, ⟨x, rfl⟩⟩ = q x := by
  apply h
  exact Classical.choose_spec (show p x ∈ Set.range p from ⟨x, rfl⟩)

theorem image_factor_iff {X : Type u} {P : Type v} {Y : Type w}
    (p : X → P) (q : X → Y) :
    (∃ g : Set.range p → Y, ∀ x, g ⟨p x, ⟨x, rfl⟩⟩ = q x) ↔
      FiberConstant p q := by
  constructor
  · rintro ⟨g, hg⟩ x y same
    have eq : (⟨p x, ⟨x, rfl⟩⟩ : Set.range p) = ⟨p y, ⟨y, rfl⟩⟩ := Subtype.ext same
    rw [← hg x, ← hg y, eq]
  · intro h
    exact ⟨imageFactor p q, image_factor_spec h⟩

theorem image_factor_unique {X : Type u} {P : Type v} {Y : Type w}
    (p : X → P) (q : X → Y) (g h : Set.range p → Y)
    (hg : ∀ x, g ⟨p x, ⟨x, rfl⟩⟩ = q x)
    (hh : ∀ x, h ⟨p x, ⟨x, rfl⟩⟩ = q x) : g = h := by
  funext z
  obtain ⟨x, hx⟩ := z.property
  have hz : z = ⟨p x, ⟨x, rfl⟩⟩ := Subtype.ext hx.symm
  rw [hz, hg, hh]

/-- Exhaustion is relative to the full declared menu. -/
def Exhausted {A : Type u} (menu : Set A) (repairs : A → Prop) : Prop :=
  ∀ a ∈ menu, ¬ repairs a

theorem witness_refutes_exhaustion {A : Type u} {menu : Set A} {repairs : A → Prop}
    {a : A} (member : a ∈ menu) (works : repairs a) : ¬ Exhausted menu repairs := by
  intro exhausted
  exact exhausted a member works

theorem exhausted_submenu {A : Type u} {small large : Set A} {repairs : A → Prop}
    (inc : small ⊆ large) (h : Exhausted large repairs) : Exhausted small repairs := by
  intro a ha
  exact h a (inc ha)

theorem truncated_search_countermodel :
    Exhausted ({false} : Set Bool) (fun a => a = true) ∧
      ¬ Exhausted (Set.univ : Set Bool) (fun a => a = true) := by
  constructor
  · intro a ha
    have h : a = false := Set.mem_singleton_iff.mp ha
    simp [h]
  · exact witness_refutes_exhaustion (Set.mem_univ true) rfl


theorem tied_minima {A B : Type*} [Preorder B] (cost : A → B) {a b : A}
    (same : cost a = cost b) (minimal : ∀ x, cost a ≤ cost x) : ∀ x, cost b ≤ cost x := by
  intro x
  rw [← same]
  exact minimal x
end Coda

