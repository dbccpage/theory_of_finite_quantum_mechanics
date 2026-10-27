/- Imported so that this repository carries its own Lean evidence.
   Original sha256: 729b3a6f64cde47e4fb3ccb6da95f9574c0700072807fc4e42e153e3e715f28c (bytes as found)
   Imported on    : 2026-10-22
   Module         : Imported.PreGenesisToMssn.Observation
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
import Imported.PreGenesisToMssn.Paper

/-! Observation quotients and the pointed relational two-vertex graph. The
codomain of an observation may depend on its index. D2 has one relation edge;
uniqueness concerns vertex maps preserving that relation, not unspecified
choices among parallel edge identities in a multigraph. -/
namespace PreMssn.Observation
universe u v w s

def SameProfile {A : Type u} {I : Type v} {V : I → Type w}
    (observe : ∀ i, A → V i) (a b : A) : Prop := ∀ i, observe i a = observe i b

def profileSetoid {A : Type u} {I : Type v} {V : I → Type w}
    (observe : ∀ i, A → V i) : Setoid A where
  r := SameProfile observe
  iseqv := ⟨fun _ _ => rfl, fun h i => (h i).symm,
    fun h₁ h₂ i => (h₁ i).trans (h₂ i)⟩

def Observed {A : Type u} {I : Type v} {V : I → Type w}
    (observe : ∀ i, A → V i) := Quotient (profileSetoid observe)

def profileClass {A : Type u} {I : Type v} {V : I → Type w}
    (observe : ∀ i, A → V i) (a : A) : Observed observe := Quotient.mk _ a

theorem profile_class_eq_iff {A : Type u} {I : Type v} {V : I → Type w}
    (observe : ∀ i, A → V i) (a b : A) :
    profileClass observe a = profileClass observe b ↔ SameProfile observe a b :=
  ⟨fun h => Quotient.exact (s := profileSetoid observe) h,
    fun h => Quotient.sound (s := profileSetoid observe) h⟩

theorem empty_profiles_equal {A : Type u} {V : Empty → Type w}
    (observe : ∀ i, A → V i) (a b : A) :
    profileClass observe a = profileClass observe b :=
  (profile_class_eq_iff observe a b).mpr (fun i => Empty.elim i)

/-- A task descends exactly when it is constant on observational classes.
The quotient lift itself needs no selected representative or choice axiom. -/
theorem task_descent_iff {A : Type u} {I : Type v} {V : I → Type w} {S : Type s}
    (observe : ∀ i, A → V i) (task : A → S) :
    (∃ f : Observed observe → S, ∀ a, f (profileClass observe a) = task a) ↔
    (∀ a b, SameProfile observe a b → task a = task b) := by
  constructor
  · rintro ⟨f, hf⟩ a b h
    rw [← hf a, ← hf b, (profile_class_eq_iff observe a b).mpr h]
  · intro h
    exact ⟨Quotient.lift task h, fun _ => rfl⟩

theorem task_descent_unique {A : Type u} {I : Type v} {V : I → Type w} {S : Type s}
    (observe : ∀ i, A → V i) (task : A → S) (f g : Observed observe → S)
    (hf : ∀ a, f (profileClass observe a) = task a)
    (hg : ∀ a, g (profileClass observe a) = task a) : f = g := by
  funext q
  induction q using Quotient.inductionOn with
  | _ a => exact (hf a).trans (hg a).symm

theorem collapsed_quotient_barrier {A : Type u} {I : Type v} {V : I → Type w}
    {S : Type s} (observe : ∀ i, A → V i) (task : A → S) (a b : A)
    (same : SameProfile observe a b) (different : task a ≠ task b) :
    ¬∃ f : Observed observe → S, ∀ x, f (profileClass observe x) = task x := by
  intro hf
  exact different ((task_descent_iff observe task).mp hf a b same)

def D2Edge (a b : Bool) : Prop := a = false ∧ b = true

structure D2Map {A : Type u} (R : A → A → Prop) where
  vertices : Bool → A
  preserves : ∀ x y, D2Edge x y → R (vertices x) (vertices y)

def pointedMap {A : Type u} (R : A → A → Prop) (a b : A) (edge : R a b) :
    D2Map R where
  vertices x := if x then b else a
  preserves x y h := by
    obtain ⟨hx, hy⟩ := h
    rw [hx, hy]
    exact edge

theorem pointed_map_endpoints {A : Type u} (R : A → A → Prop) (a b : A)
    (edge : R a b) :
    (pointedMap R a b edge).vertices false = a ∧
    (pointedMap R a b edge).vertices true = b := ⟨rfl, rfl⟩

theorem pointed_map_unique {A : Type u} (R : A → A → Prop) (a b : A)
    (edge : R a b) (f : D2Map R) (ha : f.vertices false = a)
    (hb : f.vertices true = b) : f = pointedMap R a b edge := by
  have hv : f.vertices = (pointedMap R a b edge).vertices := by
    funext x
    cases x
    · exact ha
    · exact hb
  cases f
  cases hv
  rfl

theorem pointed_map_exists_unique {A : Type u} (R : A → A → Prop) (a b : A)
    (edge : R a b) :
    ∃ f : D2Map R, (f.vertices false = a ∧ f.vertices true = b) ∧
      ∀ g : D2Map R, g.vertices false = a → g.vertices true = b → g = f :=
  ⟨pointedMap R a b edge, pointed_map_endpoints R a b edge,
    fun g ha hb => pointed_map_unique R a b edge g ha hb⟩

end PreMssn.Observation
