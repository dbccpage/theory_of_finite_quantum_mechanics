


namespace HaltingQuotient

universe u

inductive ExecutionClass : Type
  | HaltsWith0 : ExecutionClass
  | HaltsWith1 : ExecutionClass
  | Diverges   : ExecutionClass
deriving DecidableEq, Repr

theorem halts0_ne_halts1 : ExecutionClass.HaltsWith0 ≠ ExecutionClass.HaltsWith1 := by
  intro h; nomatch h

theorem halts0_ne_diverges : ExecutionClass.HaltsWith0 ≠ ExecutionClass.Diverges := by
  intro h; nomatch h

theorem halts1_ne_diverges : ExecutionClass.HaltsWith1 ≠ ExecutionClass.Diverges := by
  intro h; nomatch h

theorem binary_projection_has_collision (π : ExecutionClass → Bool) :
    ∃ (c1 c2 : ExecutionClass), c1 ≠ c2 ∧ π c1 = π c2 := by
  cases h0 : π ExecutionClass.HaltsWith0 <;>
  cases h1 : π ExecutionClass.HaltsWith1 <;>
  cases hd : π ExecutionClass.Diverges
  ·
    exact ⟨ExecutionClass.HaltsWith0, ExecutionClass.HaltsWith1, halts0_ne_halts1, by rw [h0, h1]⟩
  ·
    exact ⟨ExecutionClass.HaltsWith0, ExecutionClass.HaltsWith1, halts0_ne_halts1, by rw [h0, h1]⟩
  ·
    exact ⟨ExecutionClass.HaltsWith0, ExecutionClass.Diverges, halts0_ne_diverges, by rw [h0, hd]⟩
  ·
    exact ⟨ExecutionClass.HaltsWith1, ExecutionClass.Diverges, halts1_ne_diverges, by rw [h1, hd]⟩
  ·
    exact ⟨ExecutionClass.HaltsWith1, ExecutionClass.Diverges, halts1_ne_diverges, by rw [h1, hd]⟩
  ·
    exact ⟨ExecutionClass.HaltsWith0, ExecutionClass.Diverges, halts0_ne_diverges, by rw [h0, hd]⟩
  ·
    exact ⟨ExecutionClass.HaltsWith0, ExecutionClass.HaltsWith1, halts0_ne_halts1, by rw [h0, h1]⟩
  ·
    exact ⟨ExecutionClass.HaltsWith0, ExecutionClass.HaltsWith1, halts0_ne_halts1, by rw [h0, h1]⟩

theorem binary_projection_not_injective (π : ExecutionClass → Bool) :
    ¬ (∀ c1 c2, π c1 = π c2 → c1 = c2) := by
  intro hinj
  rcases binary_projection_has_collision π with ⟨c1, c2, hne, heq⟩
  exact hne (hinj c1 c2 heq)

theorem binary_projection_no_left_inverse (π : ExecutionClass → Bool) :
    ¬ (∃ (σ : Bool → ExecutionClass), ∀ c, σ (π c) = c) := by
  intro ⟨σ, hinv⟩
  rcases binary_projection_has_collision π with ⟨c1, c2, hne, heq⟩
  have h1 : σ (π c1) = c1 := hinv c1
  have h2 : σ (π c2) = c2 := hinv c2
  rw [heq] at h1
  rw [h1] at h2
  exact hne h2

def standardHaltingProjection : ExecutionClass → Bool
  | ExecutionClass.HaltsWith0 => true
  | ExecutionClass.HaltsWith1 => true
  | ExecutionClass.Diverges   => false

theorem standard_halting_collapses_outputs :
    standardHaltingProjection ExecutionClass.HaltsWith0 =
    standardHaltingProjection ExecutionClass.HaltsWith1 ∧
    ExecutionClass.HaltsWith0 ≠ ExecutionClass.HaltsWith1 := by
  constructor
  · rfl
  · exact halts0_ne_halts1

end HaltingQuotient
