/- Imported so that this repository carries its own Lean evidence.
   Original sha256: 2d36b5427b54767a391d0760ac563ea300c4e7381809c059610ad592bfa28fa5 (bytes as found)
   Imported on    : 2026-10-22
   Module         : Imported.WitnessedDifference.WitnessedDifference.PointedRelation
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
import Imported.WitnessedDifference.WitnessedDifference.Core

/-!
# Pointed relations: relatedness, distinctness, and irreflexivity

A pointed relation is a carrier `X`, a binary relation `R` on `X`, and two
marked points `a b : X`. Two properties of the marked pair are kept apart:
relatedness `R a b` and distinctness `a ≠ b`.

- Relatedness does not imply distinctness: the one-point carrier with a
  self-loop relates its point to itself.
- Distinctness does not imply relatedness: the empty relation on a two-point
  carrier relates nothing, although its two points differ.
- Relatedness together with irreflexivity of `R` implies distinctness.

The self-loop countermodel is also the reason irreflexivity cannot be dropped
from the third item. The non-implications are stated as negated universal
propositions over every carrier in a fixed universe. This file declares no
synthetic axioms.
-/

namespace WitnessedDifference.PointedRelation

universe u

/-- The total relation on the one-point carrier: a single self-loop. -/
def selfLoop : PUnit.{u + 1} → PUnit.{u + 1} → Prop :=
  fun _ _ => True

/-- The empty relation on the two-point carrier `ULift Bool`. -/
def emptyTwo : ULift.{u} Bool → ULift.{u} Bool → Prop :=
  fun _ _ => False

/-- The self-loop countermodel: the carrier has exactly one point, the marked
pair is related, and the marked points are equal. -/
theorem self_loop_countermodel :
    (∀ x y : PUnit.{u + 1}, x = y)
      ∧ selfLoop PUnit.unit PUnit.unit
      ∧ ¬ (PUnit.unit : PUnit.{u + 1}) ≠ PUnit.unit := by
  refine ⟨fun _ _ => rfl, trivial, fun hne => hne rfl⟩

/-- The empty-relation countermodel: the carrier has exactly two points, the
marked points differ, and the marked pair is not related. -/
theorem empty_two_countermodel :
    (∀ x : ULift.{u} Bool, x = ⟨false⟩ ∨ x = ⟨true⟩)
      ∧ (⟨false⟩ : ULift.{u} Bool) ≠ ⟨true⟩
      ∧ ¬ emptyTwo.{u} ⟨false⟩ ⟨true⟩ := by
  refine ⟨?_, ?_, fun h => h⟩
  · intro x
    obtain ⟨b⟩ := x
    cases b
    · exact Or.inl rfl
    · exact Or.inr rfl
  · intro heq
    exact Bool.noConfusion (congrArg ULift.down heq)

/-- Relatedness does not imply distinctness. The one-point self-loop is a
countermodel. -/
theorem related_not_implies_distinct :
    ¬ ∀ (X : Type u) (R : X → X → Prop) (a b : X), R a b → a ≠ b := by
  intro himp
  exact himp PUnit.{u + 1} selfLoop PUnit.unit PUnit.unit trivial rfl

/-- Distinctness does not imply relatedness. The empty relation on a
two-point carrier is a countermodel. -/
theorem distinct_not_implies_related :
    ¬ ∀ (X : Type u) (R : X → X → Prop) (a b : X), a ≠ b → R a b := by
  intro himp
  exact himp (ULift.{u} Bool) emptyTwo ⟨false⟩ ⟨true⟩
    empty_two_countermodel.2.1

/-- Relatedness under an irreflexive relation forces distinctness. -/
theorem irreflexive_related_implies_distinct {X : Sort u}
    (R : X → X → Prop) (hirrefl : ∀ x, ¬ R x x) {a b : X}
    (hrel : R a b) : a ≠ b := by
  intro heq
  subst heq
  exact hirrefl a hrel

/-- The three facts about a pointed relation `(X, R, a, b)`, stated over
every carrier in the universe `Type u`: relatedness does not imply
distinctness, distinctness does not imply relatedness, and relatedness
together with irreflexivity implies distinctness. -/
theorem pointed_relation_independence :
    (¬ ∀ (X : Type u) (R : X → X → Prop) (a b : X), R a b → a ≠ b)
      ∧ (¬ ∀ (X : Type u) (R : X → X → Prop) (a b : X), a ≠ b → R a b)
      ∧ (∀ (X : Type u) (R : X → X → Prop) (a b : X),
          (∀ x, ¬ R x x) → R a b → a ≠ b) := by
  refine ⟨related_not_implies_distinct, distinct_not_implies_related, ?_⟩
  intro X R a b hirrefl hrel
  exact irreflexive_related_implies_distinct R hirrefl hrel

/-- Row WDP-CH01-P02 on finite carriers: a related pair on a one-point carrier
that is not distinct, a distinct pair on a two-point carrier that is not
related, and apartness from relatedness under irreflexivity. -/
theorem pointed_relation_independence_fin :
    (∃ (R : Fin 1 → Fin 1 → Prop) (a b : Fin 1), R a b ∧ a = b) ∧
    (∃ (R : Fin 2 → Fin 2 → Prop) (a b : Fin 2), a ≠ b ∧ ¬ R a b) ∧
    (∀ {X : Type} (R : X → X → Prop), (∀ x, ¬ R x x) → ∀ a b : X, R a b → a ≠ b) := by
  refine ⟨⟨fun _ _ => True, 0, 0, trivial, rfl⟩, ⟨fun _ _ => False, 0, 1, by decide, id⟩, ?_⟩
  intro X R hirrefl a b hrel heq
  subst heq
  exact hirrefl a hrel

end WitnessedDifference.PointedRelation
