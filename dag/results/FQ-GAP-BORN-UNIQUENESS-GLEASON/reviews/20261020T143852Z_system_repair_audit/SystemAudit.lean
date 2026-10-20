import ReconstructionGeometry

/-! Audit witnesses: a genuine inhabited System, and rejection of the old phantom.
No Jordan catalogue or classification bridge is supplied or assumed for these checks. -/
noncomputable section
namespace FiniteQM.ReconstructionAudit
open Set ReconstructionGeometry

abbrev Z := Space 0

def oneEffect : Effect ({0} : Set Z) where
  functional := AffineMap.const ℝ Z 1
  nonnegative := by intro x hx; simp
  bounded := by intro x hx; simp

def zeroFrame : Fin 1 → Z := fun _ => 0

theorem zeroFrame_valid : Frame ({0} : Set Z) zeroFrame := by
  refine ⟨?_, ?_, ?_⟩
  · intro i j _; exact Subsingleton.elim _ _
  · intro i; simp [zeroFrame]
  · refine ⟨fun _ => oneEffect, ?_, ?_⟩
    · intro x hx; simp [oneEffect]
    · intro i j
      have hij : i = j := Subsingleton.elim _ _
      simp [oneEffect, hij]

/-- A concrete rank-one, dimension-one system inhabits the repaired interface. -/
def trivialSystem : System 0 where
  states := {0}
  nonempty := ⟨0, rfl⟩
  convex := convex_singleton 0
  compact := isCompact_singleton
  full := by
    apply top_unique
    intro x hx
    have hzero : x = (0 : Z) := Subsingleton.elim _ _
    rw [hzero]
    exact mem_affineSpan ℝ (by simp)
  rank := 1
  rank_pos := by decide
  frame_bound := by
    intro m f hf
    by_contra h
    have hm : 2 ≤ m := by omega
    let i : Fin m := ⟨0, by omega⟩
    let j : Fin m := ⟨1, by omega⟩
    have hval := congrArg Fin.val (hf.distinct (Subsingleton.elim (f i) (f j)))
    change (0 : ℕ) = 1 at hval
    omega
  frame_attained := ⟨zeroFrame, zeroFrame_valid⟩

theorem trivialSystem_spectral : trivialSystem.Spectral := by
  intro x hx
  have hxzero : x = (0 : Z) := Subsingleton.elim _ _
  refine ⟨1, zeroFrame, zeroFrame_valid, ?_⟩
  rw [hxzero]
  apply subset_convexHull
  exact ⟨0, rfl⟩

theorem trivialSystem_stronglySymmetric : trivialSystem.StronglySymmetric := by
  intro m f g _ _
  exact ⟨System.Reversible.identity trivialSystem, fun _ => Subsingleton.elim _ _⟩

theorem trivialSystem_rank_one : trivialSystem.rank = 1 := rfl
theorem trivialSystem_dim_one : trivialSystem.dim = 1 := rfl

/-- An explicit negative control using the corrected semantics, without any Jordan input. -/
theorem no_spectral_rank_one_dim_two {n : ℕ} (A : System n) (hS : A.Spectral) :
    ¬ (A.rank = 1 ∧ A.dim = 2) := by
  rintro ⟨hr, hd⟩
  have h := A.rank_one_dim_one hS hr
  omega

#print axioms oneEffect
#print axioms zeroFrame_valid
#print axioms trivialSystem
#print axioms trivialSystem_spectral
#print axioms trivialSystem_stronglySymmetric
#print axioms trivialSystem_rank_one
#print axioms trivialSystem_dim_one
#print axioms no_spectral_rank_one_dim_two
end FiniteQM.ReconstructionAudit