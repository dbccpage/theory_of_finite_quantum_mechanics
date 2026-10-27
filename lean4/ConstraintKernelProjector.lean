import Mathlib.Tactic.Ring

/- A declared finite-dimensional symmetric constraint and its distinct kernel projector.
This is not a construction of a Wheeler-DeWitt operator or diffeomorphism action. -/
namespace ConstraintKernelProjector

abbrev Vec := Int × Int × Int

def zero : Vec := (0, 0, 0)

def constraint (v : Vec) : Vec := (0, 2 * v.2.1, -v.2.2)

def project (v : Vec) : Vec := (v.1, 0, 0)

def dot (v w : Vec) : Int := v.1 * w.1 + v.2.1 * w.2.1 + v.2.2 * w.2.2

def subtract (v w : Vec) : Vec := (v.1 - w.1, v.2.1 - w.2.1, v.2.2 - w.2.2)

theorem constraint_symmetric (v w : Vec) :
    dot (constraint v) w = dot v (constraint w) := by
  simp only [constraint, dot]
  ring

theorem kernel_characterization (v : Vec) :
    constraint v = zero ↔ v.2.1 = 0 ∧ v.2.2 = 0 := by
  constructor
  · intro h
    have h₁ := congrArg (fun z : Vec => z.2.1) h
    have h₂ := congrArg (fun z : Vec => z.2.2) h
    simp only [constraint, zero] at h₁ h₂
    omega
  · rintro ⟨h₁, h₂⟩
    simp [constraint, zero, h₁, h₂]

theorem projector_idempotent (v : Vec) : project (project v) = project v := rfl

theorem projected_vector_satisfies_constraint (v : Vec) :
    constraint (project v) = zero := by simp [constraint, project, zero]

theorem projector_fixes_exactly_kernel (v : Vec) :
    project v = v ↔ constraint v = zero := by
  rw [kernel_characterization]
  constructor
  · intro h
    exact ⟨(congrArg (fun z : Vec => z.2.1) h).symm,
      (congrArg (fun z : Vec => z.2.2) h).symm⟩
  · rintro ⟨h₁, h₂⟩
    rcases v with ⟨x, y, z⟩
    simp only at h₁ h₂
    simp [project, h₁, h₂]

theorem projection_residual_orthogonal_to_kernel (v w : Vec)
    (hw : constraint w = zero) : dot (subtract v (project v)) w = 0 := by
  obtain ⟨h₁, h₂⟩ := (kernel_characterization w).mp hw
  simp [dot, subtract, project, h₁, h₂]

theorem nontrivial_kernel : constraint (1, 0, 0) = zero ∧ (1, 0, 0) ≠ zero := by
  decide

theorem constraint_is_indefinite :
    dot (0, 1, 0) (constraint (0, 1, 0)) > 0 ∧
    dot (0, 0, 1) (constraint (0, 0, 1)) < 0 := by decide

theorem constraint_is_not_projector :
    constraint (constraint (0, 1, 0)) ≠ constraint (0, 1, 0) := by decide

#print axioms constraint_symmetric
#print axioms kernel_characterization
#print axioms projector_idempotent
#print axioms projected_vector_satisfies_constraint
#print axioms projector_fixes_exactly_kernel
#print axioms projection_residual_orthogonal_to_kernel
#print axioms nontrivial_kernel
#print axioms constraint_is_indefinite
#print axioms constraint_is_not_projector
end ConstraintKernelProjector
