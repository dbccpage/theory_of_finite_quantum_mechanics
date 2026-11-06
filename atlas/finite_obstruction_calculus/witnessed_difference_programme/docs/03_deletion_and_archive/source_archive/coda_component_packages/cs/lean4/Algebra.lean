/-!
# Reconstruction CS algebra

Self-contained formalization of the core mathematical claims for CODA-CS:
- CS-D1: Fiber constancy (Coda.FiberConstant)
- CS-D2: Factorization (Coda.Factors)
- CS-L1: Factorization implies fiber constancy (Coda.factor_implies_constant)
- CS-T1: Refinement preserves descent (Coda.CS.refinement_preserves_descent)
- CS-T2: Family observation equality is pointwise (Coda.CS.family_observation)
- CS-T3: First coordinate collision obstructs second coordinate (Coda.CS.finite_shadow_collision)
- CS-T4: Strict refinement countermodel (Coda.CS.refinement_strict_countermodel)

AuthorityEffect: None.
-/

namespace Coda

universe u v w x

/-- Definition CS-D1: Fiber constancy. -/
def FiberConstant {X : Type u} {P : Type v} {Y : Type w}
    (p : X → P) (q : X → Y) : Prop :=
  ∀ a b, p a = p b → q a = q b

/-- Definition CS-D2: Factorization. -/
def Factors {X : Type u} {P : Type v} {Y : Type w}
    (p : X → P) (q : X → Y) : Prop :=
  ∃ g : P → Y, ∀ a, g (p a) = q a

/-- Lemma CS-L1: Factorization implies fiber constancy. -/
theorem factor_implies_constant {X : Type u} {P : Type v} {Y : Type w}
    {p : X → P} {q : X → Y} (h : Factors p q) : FiberConstant p q := by
  obtain ⟨g, hg⟩ := h
  intro a b hab
  rw [← hg a, ← hg b, hab]

/-- Contrapositive obstruction form: collision obstructs factorization.
    If p(x) = p(y) but q(x) ≠ q(y), then q does not factor through p. -/
theorem collision_obstructs_factor {X : Type u} {P : Type v} {Y : Type w}
    {p : X → P} {q : X → Y} {a b : X}
    (same : p a = p b) (different : q a ≠ q b) : ¬ Factors p q := by
  intro h
  exact different (factor_implies_constant h a b same)

namespace CS

/-- Theorem CS-T1: Refinement preserves descent.
    If q is fiber-constant for forget ∘ fine, it is fiber-constant for fine. -/
theorem refinement_preserves_descent {X : Type u} {A : Type v} {B : Type w} {Y : Type x} (fine : X → B)
    (forget : B → A) (q : X → Y) (h : Coda.FiberConstant (forget ∘ fine) q) :
    Coda.FiberConstant fine q := by
  intro a b same
  exact h a b (congrArg forget same)

/-- Theorem CS-T2: Family observation equality is pointwise. -/
theorem family_observation {I : Type u} {X : Type v} {P : I → Type w}
    (observe : (i : I) → X → P i) {a b : X} :
    (fun i => observe i a) = (fun i => observe i b) ↔ ∀ i, observe i a = observe i b := by
  constructor
  · intro h i; exact congrFun h i
  · exact funext

/-- Theorem CS-T3: The first coordinate does not determine the second (collision). -/
theorem finite_shadow_collision :
    ¬ Coda.Factors (fun x : Bool × Bool => x.1) (fun x => x.2) := by
  exact Coda.collision_obstructs_factor (a := (false, false)) (b := (false, true)) rfl (by decide)

/-- Theorem CS-T4: The fine look can factor when the coarse look cannot. -/
theorem refinement_strict_countermodel :
    Coda.Factors (fun x : Bool × Bool => x) (fun x => x.2) ∧
      ¬ Coda.Factors (fun x : Bool × Bool => x.1) (fun x => x.2) := by
  exact ⟨⟨Prod.snd, fun _ => rfl⟩, finite_shadow_collision⟩

end CS
end Coda

#check Coda.CS.refinement_preserves_descent
#print axioms Coda.CS.refinement_preserves_descent
#check Coda.CS.family_observation
#print axioms Coda.CS.family_observation
#check Coda.CS.finite_shadow_collision
#print axioms Coda.CS.finite_shadow_collision
#check Coda.CS.refinement_strict_countermodel
#print axioms Coda.CS.refinement_strict_countermodel
