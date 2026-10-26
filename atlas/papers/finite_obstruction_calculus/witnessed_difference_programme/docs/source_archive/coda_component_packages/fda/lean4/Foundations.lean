/-!
CodaReconstruction.Foundations

Self-contained mathematical foundation definitions and theorems for CODA reconstruction.
Zero external dependencies; ordinary Lean 4 kernel only.
AuthorityEffect: None.
-/

namespace Coda

universe u v w

def Factors {X : Type u} {P : Type v} {Y : Type w}
    (p : X → P) (q : X → Y) : Prop :=
  ∃ g : P → Y, ∀ x, g (p x) = q x

def FiberConstant {X : Type u} {P : Type v} {Y : Type w}
    (p : X → P) (q : X → Y) : Prop :=
  ∀ x y, p x = p y → q x = q y

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

end Coda
