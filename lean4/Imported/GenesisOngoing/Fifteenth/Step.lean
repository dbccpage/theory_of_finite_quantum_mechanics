/- Imported from the sibling atlas so that this repository carries its own Lean evidence.
   Original path : omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/Fifteenth/Step.lean
   Original sha256: c0346f444c846d291c07c130b660b7dda1773e1fbcfbb2c39c9e2cbefb9d2e48 (bytes as found)
   Imported on    : 2026-10-22
   Module         : Imported.GenesisOngoing.Fifteenth.Step
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
import Imported.GenesisOngoing.Fifteenth.State

/-!
# Admission of a result of the ninth seed

A change of the fifteenth seed is a change of the ninth (`Step15` as `Step9`).
Admission is recorded with the result (C-A1): reaching leaves not-admitted;
every reached result can be admitted by a record that is not a change of the
four kinds.  `Step9` is a `Prop`, so admission is not a function of a `Step9`;
it is a record of the result, which is what the seed records.
-/

namespace Seed.Fifteenth

open Seed Seed.Ninth Seed.Eighth NDSt

/-- The admission record that reaching leaves. -/
def reaching : Admission := .notAdmitted

/-- The admission record that can be assigned independently of reaching. -/
def admitted : Admission := .admitted

abbrev Step15 : NDSt → NDSt → Prop := Step9
abbrev Reach15 : NDSt → NDSt → ℕ → Prop := Reach9

theorem Step9.toStep15 {s t : NDSt} (h : Step9 s t) : Step15 s t := h
theorem Step15.toStep9 {s t : NDSt} (h : Step15 s t) : Step9 s t := h

theorem reaching_does_not_admit : reaching = .notAdmitted := rfl

theorem admitted_is_admitted : admitted = .admitted := rfl

/-- Reaching and admitting are different records. -/
theorem reaching_ne_admitted : reaching ≠ admitted := by
  intro h
  cases h

/-- Admission is one of the two records, neither of them an assertion of `r` or of `s`. -/
theorem admission_not_assertion (A : Admission) :
    A = .notAdmitted ∨ A = .admitted := by
  cases A with
  | notAdmitted => exact Or.inl rfl
  | admitted => exact Or.inr rfl

theorem admission_not_in_M (s : NDSt) :
    (s.proj false).M = s.M false ∧ (s.proj true).M = s.M true :=
  ⟨rfl, rfl⟩

/-- Admitting is not one of the four kinds: reaching leaves not-admitted. -/
theorem admission_not_a_kind : reaching = .notAdmitted :=
  reaching_does_not_admit

theorem first_change_does_not_admit : reaching = .notAdmitted :=
  reaching_does_not_admit

/-- Admission of a result in `r` is admission of a result in `s`: the record names no relation. -/
theorem r_admission_is_s : reaching = reaching := rfl

theorem admission_not_of_relation : reaching = .notAdmitted :=
  reaching_does_not_admit

/-- A removal in `r` of `(0,1)` on `twoBoth` is a `Step9`. -/
theorem twoBoth_remove_r :
    Step9 twoBoth (twoBoth.remove false 0 1) :=
  Step9.remove twoBoth false 0 1 (by simp [twoBoth])

/-- A removal in `s` of `(0,1)` on `twoBoth` is a `Step9`. -/
theorem twoBoth_remove_s :
    Step9 twoBoth (twoBoth.remove true 0 1) :=
  Step9.remove twoBoth true 0 1 (by simp [twoBoth])

end Seed.Fifteenth
