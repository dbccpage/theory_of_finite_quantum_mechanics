/-!
  HaltingQuotient.lean — Binary Computational Projections and the Halting Quotient

  Status: FORMAL LEAN 4 SPECIFICATION & THEOREM REGISTER
  AuthorityEffect: None
  Primary Reference: `sealed-derivation-v1` (`3100c4e`)
  Claims: `PO-023-C1`, `PO-023-C2`, `PO-023-C3`, `PO-023-C4`, `INV-BIN-PROJ`

  Formalizes:
  1. Three-class operational execution states (HaltsWith0, HaltsWith1, Diverges).
  2. The Pigeonhole Collision Theorem: any binary projection π : ExecutionClass → Bool
     collapses at least two distinct operational termination classes.
  3. Non-invertibility: no binary observation admits a faithful left inverse.
  4. Non-faithful quotient: binary observation cannot separate three distinct behaviors.
-/

namespace HaltingQuotient

universe u

/-- Three operational termination classes for discrete computational processes. -/
inductive ExecutionClass : Type
  | HaltsWith0 : ExecutionClass
  | HaltsWith1 : ExecutionClass
  | Diverges   : ExecutionClass
deriving DecidableEq, Repr

/-- All three execution classes are mutually distinct. -/
theorem halts0_ne_halts1 : ExecutionClass.HaltsWith0 ≠ ExecutionClass.HaltsWith1 := by
  intro h; nomatch h

theorem halts0_ne_diverges : ExecutionClass.HaltsWith0 ≠ ExecutionClass.Diverges := by
  intro h; nomatch h

theorem halts1_ne_diverges : ExecutionClass.HaltsWith1 ≠ ExecutionClass.Diverges := by
  intro h; nomatch h

/--
  Theorem (Claim `PO-023-C1` / `INV-BIN-PROJ`):
  Every binary observation projection π : ExecutionClass → Bool has a collision:
  there exist distinct classes c1 ≠ c2 with π(c1) = π(c2).
-/
theorem binary_projection_has_collision (π : ExecutionClass → Bool) :
    ∃ (c1 c2 : ExecutionClass), c1 ≠ c2 ∧ π c1 = π c2 := by
  cases h0 : π ExecutionClass.HaltsWith0 <;>
  cases h1 : π ExecutionClass.HaltsWith1 <;>
  cases hd : π ExecutionClass.Diverges
  · -- false, false, false
    exact ⟨ExecutionClass.HaltsWith0, ExecutionClass.HaltsWith1, halts0_ne_halts1, by rw [h0, h1]⟩
  · -- false, false, true
    exact ⟨ExecutionClass.HaltsWith0, ExecutionClass.HaltsWith1, halts0_ne_halts1, by rw [h0, h1]⟩
  · -- false, true, false
    exact ⟨ExecutionClass.HaltsWith0, ExecutionClass.Diverges, halts0_ne_diverges, by rw [h0, hd]⟩
  · -- false, true, true
    exact ⟨ExecutionClass.HaltsWith1, ExecutionClass.Diverges, halts1_ne_diverges, by rw [h1, hd]⟩
  · -- true, false, false
    exact ⟨ExecutionClass.HaltsWith1, ExecutionClass.Diverges, halts1_ne_diverges, by rw [h1, hd]⟩
  · -- true, false, true
    exact ⟨ExecutionClass.HaltsWith0, ExecutionClass.Diverges, halts0_ne_diverges, by rw [h0, hd]⟩
  · -- true, true, false
    exact ⟨ExecutionClass.HaltsWith0, ExecutionClass.HaltsWith1, halts0_ne_halts1, by rw [h0, h1]⟩
  · -- true, true, true
    exact ⟨ExecutionClass.HaltsWith0, ExecutionClass.HaltsWith1, halts0_ne_halts1, by rw [h0, h1]⟩

/--
  Theorem (Claim `PO-023-C2`):
  No binary observation projection is injective.
-/
theorem binary_projection_not_injective (π : ExecutionClass → Bool) :
    ¬ (∀ c1 c2, π c1 = π c2 → c1 = c2) := by
  intro hinj
  rcases binary_projection_has_collision π with ⟨c1, c2, hne, heq⟩
  exact hne (hinj c1 c2 heq)

/--
  Theorem (Claim `PO-023-C3`):
  No binary projection admits a faithful reconstruction / left inverse σ : Bool → ExecutionClass.
-/
theorem binary_projection_no_left_inverse (π : ExecutionClass → Bool) :
    ¬ (∃ (σ : Bool → ExecutionClass), ∀ c, σ (π c) = c) := by
  intro ⟨σ, hinv⟩
  rcases binary_projection_has_collision π with ⟨c1, c2, hne, heq⟩
  have h1 : σ (π c1) = c1 := hinv c1
  have h2 : σ (π c2) = c2 := hinv c2
  rw [heq] at h1
  rw [h1] at h2
  exact hne h2

/--
  Theorem (Claim `PO-023-C4`):
  The binary halting quotient π_halt(HaltsWith0) = true, π_halt(HaltsWith1) = true,
  π_halt(Diverges) = false conflates the distinct outputs 0 and 1.
-/
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
