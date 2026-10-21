import Mathlib.Data.Fintype.Card
import Mathlib.Data.Fintype.Sum
import Mathlib.Data.Fintype.Pi
import Mathlib.SetTheory.Cardinal.Finite

/-!
# Typed old-image recovery implies injectivity of the lift, and nothing more

AuthorityEffect: None.  Scope: a lift `u : A → B` and a typed recovery `r : B → A ⊕ E` that returns the old term
on the old image (`OldImageLaw`).  The theorems are general over arbitrary types; the small `Fin` counterexamples
are instances.  Source: `Paper.lean` line 54 / `Paper001.lean` line 103 (`old_image_injective`, general over
arbitrary `A B`), and `Paper001.lean` lines 111, 128, 138 (`off_image_not_implied`, `observation_not_implied`,
`repair_not_implied`, all fixed `Fin` instances, not general statements).

* `old_image_injective`: the law implies `u` injective.
* `injective_iff_exists_law`: injectivity is also sufficient for the existence of a recovery, so the law carries
  exactly the information "u is injective" and no more.
* `law_freedom_off_image`: for injective `u`, the value of a law-satisfying `r` at an off-image point is
  completely free, so off-image rejection (`r b = inr e`) is not implied (`off_image_not_implied_general`).
* `observation_not_implied_general`, `repair_not_implied_general`: the law places no constraint on observations
  or on an obstruction predicate.
* `law_card`: for injective `u` between finite types, the number of laws is `(|A| + 1) ^ (|B| - |A|)` (the free
  values at the off-image points), which is `1` exactly when `u` is onto.
Nothing here is a statement about S(n), about repair of obstructions, or about any physical reading.
-/

namespace OldImageInjective

/-- Typed recovery of old terms on the old image. -/
def OldImageLaw {A B E : Type} (u : A → B) (r : B → A ⊕ E) : Prop := ∀ a, r (u a) = Sum.inl a

/-- Typed old-image recovery implies injectivity of the lift. -/
theorem old_image_injective {A B E : Type} (u : A → B) (r : B → A ⊕ E) (h : OldImageLaw u r) :
    Function.Injective u := by
  intro a b hab
  have h1 : (Sum.inl a : A ⊕ E) = Sum.inl b := by rw [← h a, hab, h b]
  exact Sum.inl.inj h1

/-- A pigeonhole consequence: a lift with a recovery cannot have a larger source than target. -/
theorem law_card_le {A B E : Type} [Fintype A] [Fintype B] (u : A → B) (r : B → A ⊕ E)
    (h : OldImageLaw u r) : Fintype.card A ≤ Fintype.card B :=
  Fintype.card_le_of_injective u (old_image_injective u r h)

/-- Any injective lift admits a recovery that extends the law by an arbitrary value `x` off the image. -/
theorem law_freedom_off_image {A B E : Type} (u : A → B) (hu : Function.Injective u)
    (x : A ⊕ E) : ∃ r : B → A ⊕ E, OldImageLaw u r ∧ (∀ b, (∀ a, u a ≠ b) → r b = x) := by
  classical
  refine ⟨fun b => if h : ∃ a, u a = b then Sum.inl (Classical.choose h) else x, ?_, ?_⟩
  · intro a
    have h : ∃ a', u a' = u a := ⟨a, rfl⟩
    have hc : Classical.choose h = a := hu (Classical.choose_spec h)
    simp only [dif_pos h, hc]
  · intro b hb
    have h : ¬ ∃ a, u a = b := fun ⟨a, ha⟩ => hb a ha
    simp only [dif_neg h]

/-- Injectivity is also sufficient: the law says exactly that the lift is injective. -/
theorem injective_iff_exists_law {A B : Type} (u : A → B) :
    Function.Injective u ↔ ∃ r : B → A ⊕ Unit, OldImageLaw u r := by
  constructor
  · intro hu
    exact (fun ⟨r, hr, _⟩ => ⟨r, hr⟩) (law_freedom_off_image (E := Unit) u hu (Sum.inr ()))
  · rintro ⟨r, hr⟩
    exact old_image_injective u r hr

/-- Off-image rejection is not implied by the law: for any injective lift with a point `b0` off its image and
any old term `a0`, there are two recoveries obeying the law, one refusing `b0` and one accepting it as `a0`. -/
theorem off_image_not_implied_general {A B E : Type} (u : A → B) (hu : Function.Injective u) (b0 : B)
    (hb0 : ∀ a, u a ≠ b0) (a0 : A) (e : E) :
    ∃ r r' : B → A ⊕ E, OldImageLaw u r ∧ OldImageLaw u r' ∧ r b0 = Sum.inr e ∧ r' b0 ≠ Sum.inr e := by
  obtain ⟨r, hr, hr0⟩ := law_freedom_off_image (E := E) u hu (Sum.inr e)
  obtain ⟨r', hr', hr0'⟩ := law_freedom_off_image (E := E) u hu (Sum.inl a0)
  refine ⟨r, r', hr, hr', hr0 b0 hb0, ?_⟩
  rw [hr0' b0 hb0]
  intro h
  cases h

/-- Instance of the previous theorem (`Fin 1 → Fin 2`), with both recoveries written out. -/
theorem off_image_not_implied_instance :
    ∃ (u : Fin 1 → Fin 2) (r r' : Fin 2 → Fin 1 ⊕ Unit),
      (∀ a, r (u a) = Sum.inl a) ∧ (∀ a, r' (u a) = Sum.inl a) ∧ (∀ a, u a ≠ 1) ∧
        r 1 = Sum.inr () ∧ r' 1 ≠ Sum.inr () :=
  ⟨fun _ => 0, fun b => if b = 0 then Sum.inl 0 else Sum.inr (), fun _ => Sum.inl 0,
    by decide, by decide, by decide, by decide, by decide⟩

/-- Observation preservation (`q'` read through the lift equals `q`). -/
def ObsPreserved {A B O : Type} (u : A → B) (q : A → O) (q' : B → O) : Prop := ∀ a, q' (u a) = q a

/-- The law does not imply observation preservation: constant observations that differ. -/
theorem observation_not_implied_general {A B E O : Type} [Nonempty A] (u : A → B) (r : B → A ⊕ E)
    (_h : OldImageLaw u r) (o0 o1 : O) (hne : o0 ≠ o1) :
    ∃ (q : A → O) (q' : B → O), ¬ ObsPreserved u q q' := by
  refine ⟨fun _ => o0, fun _ => o1, ?_⟩
  intro hp
  obtain ⟨a⟩ := ‹Nonempty A›
  exact hne (hp a).symm

/-- And preservation is a separate, satisfiable condition on the same lift: `q := q' ∘ u`. -/
theorem observation_preserved_possible {A B O : Type} (u : A → B) (q' : B → O) :
    ObsPreserved u (fun a => q' (u a)) q' := fun _ => rfl

/-- Instance on `Fin 2` (the source witness): the identity lift with `q = 0`, `q' = val`. -/
theorem observation_not_implied_instance :
    ∃ (u : Fin 2 → Fin 2) (r : Fin 2 → Fin 2 ⊕ Unit) (q q' : Fin 2 → Nat),
      (∀ a, r (u a) = Sum.inl a) ∧ ¬ (∀ a, q' (u a) = q a) :=
  ⟨id, fun a => Sum.inl a, fun _ => 0, fun a => a.val, fun _ => rfl, by decide⟩

/-- The identity lift satisfies the law and leaves every predicate on the old terms exactly as it was, so
the law alone repairs no obstruction. -/
theorem repair_not_implied_general {A : Type} (obstruction : A → Prop) :
    OldImageLaw (id : A → A) (fun a => (Sum.inl a : A ⊕ Unit)) ∧ ∀ a, obstruction a ↔ obstruction (id a) :=
  ⟨fun _ => rfl, fun _ => Iff.rfl⟩

/-- Instance (`Fin 1`), the source witness: the single point stays obstructed after the lift. -/
theorem repair_not_implied_instance :
    ∃ (u : Fin 1 → Fin 1) (r : Fin 1 → Fin 1 ⊕ Unit) (obstruction : Fin 1 → Bool),
      (∀ a, r (u a) = Sum.inl a) ∧ obstruction 0 = true ∧ obstruction (u 0) = true :=
  ⟨id, fun a => Sum.inl a, fun _ => true, fun _ => rfl, rfl, rfl⟩

/-- Number of recoveries obeying the law for an injective lift: free values at the off-image points. -/
theorem law_card {A B : Type} [Fintype A] [Fintype B] (u : A → B)
    (hu : Function.Injective u) :
    Nat.card {r : B → A ⊕ Unit // OldImageLaw u r} =
      (Fintype.card A + 1) ^ (Fintype.card B - Fintype.card A) := by
  classical
  let φ : Set.range u → A := (Equiv.ofInjective u hu).symm
  have hφ : ∀ a (h : u a ∈ Set.range u), φ ⟨u a, h⟩ = a := fun a h =>
    (Equiv.symm_apply_eq _).mpr rfl
  let e : {r : B → A ⊕ Unit // OldImageLaw u r} ≃ ({b : B // b ∉ Set.range u} → A ⊕ Unit) :=
    { toFun := fun r s => r.1 s.1
      invFun := fun g => ⟨fun b => if h : b ∈ Set.range u then Sum.inl (φ ⟨b, h⟩) else g ⟨b, h⟩, by
        intro a
        have h : u a ∈ Set.range u := ⟨a, rfl⟩
        simp only [h, dite_true, hφ]⟩
      left_inv := by
        rintro ⟨r, hr⟩
        apply Subtype.ext
        funext b
        by_cases h : b ∈ Set.range u
        · obtain ⟨a, rfl⟩ := h
          have h2 : u a ∈ Set.range u := ⟨a, rfl⟩
          simp only [h2, dite_true, hφ]
          exact (hr a).symm
        · simp only [h, dite_false]
      right_inv := by
        intro g
        funext s
        simp only [s.2, dite_false] }
  rw [Nat.card_congr e]
  have hS : Fintype.card {b : B // b ∉ Set.range u} = Fintype.card B - Fintype.card A := by
    have h1 := Fintype.card_subtype_compl (fun b : B => b ∈ Set.range u)
    have h2 : Fintype.card {b : B // b ∈ Set.range u} = Fintype.card A :=
      (Fintype.card_congr (Equiv.ofInjective u hu)).symm
    rw [h2] at h1
    convert h1
  rw [Nat.card_eq_fintype_card, Fintype.card_fun, hS, Fintype.card_sum, Fintype.card_unit]

end OldImageInjective

#print axioms OldImageInjective.old_image_injective
#print axioms OldImageInjective.injective_iff_exists_law
#print axioms OldImageInjective.law_freedom_off_image
#print axioms OldImageInjective.off_image_not_implied_general
#print axioms OldImageInjective.off_image_not_implied_instance
#print axioms OldImageInjective.observation_not_implied_general
#print axioms OldImageInjective.observation_preserved_possible
#print axioms OldImageInjective.observation_not_implied_instance
#print axioms OldImageInjective.repair_not_implied_general
#print axioms OldImageInjective.repair_not_implied_instance
#print axioms OldImageInjective.law_card_le
#print axioms OldImageInjective.law_card
