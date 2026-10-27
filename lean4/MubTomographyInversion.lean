

namespace HilbertWalk.MubTomographyInversion

def scaled_overlap (b1 j1 b2 j2 : Nat) : Int :=
  if b1 = b2 then
    (if j1 = j2 then 3 else 0)
  else
    1

theorem mub_orthonormal_diag (b j : Nat) : scaled_overlap b j b j = 3 := by
  dsimp [scaled_overlap]
  split <;> rename_i h1
  · split <;> rename_i h2
    · rfl
    · contradiction
  · contradiction

theorem mub_orthogonal_01 (b : Nat) : scaled_overlap b 0 b 1 = 0 := by
  dsimp [scaled_overlap]
  split <;> rename_i h1
  · rfl
  · contradiction

theorem mub_orthogonal_02 (b : Nat) : scaled_overlap b 0 b 2 = 0 := by
  dsimp [scaled_overlap]
  split <;> rename_i h1
  · rfl
  · contradiction

theorem mub_orthogonal_12 (b : Nat) : scaled_overlap b 1 b 2 = 0 := by
  dsimp [scaled_overlap]
  split <;> rename_i h1
  · rfl
  · contradiction

theorem mub_cross_overlap (b1 b2 j1 j2 : Nat) (h : b1 ≠ b2) :
    scaled_overlap b1 j1 b2 j2 = 1 := by
  dsimp [scaled_overlap]
  split <;> rename_i h1
  · contradiction
  · rfl

structure MUBProbabilities where
  p00 : Int
  p01 : Int
  p02 : Int
  p10 : Int
  p11 : Int
  p12 : Int
  p20 : Int
  p21 : Int
  p22 : Int
  p30 : Int
  p31 : Int
  p32 : Int
  norm0 : p00 + p01 + p02 = 3
  norm1 : p10 + p11 + p12 = 3
  norm2 : p20 + p21 + p22 = 3
  norm3 : p30 + p31 + p32 = 3
  deriving DecidableEq, Repr

def reconstructed_overlap_scaled (p : MUBProbabilities) (beta mu : Nat) : Int :=
  (p.p00 * scaled_overlap 0 0 beta mu + p.p01 * scaled_overlap 0 1 beta mu + p.p02 * scaled_overlap 0 2 beta mu +
   p.p10 * scaled_overlap 1 0 beta mu + p.p11 * scaled_overlap 1 1 beta mu + p.p12 * scaled_overlap 1 2 beta mu +
   p.p20 * scaled_overlap 2 0 beta mu + p.p21 * scaled_overlap 2 1 beta mu + p.p22 * scaled_overlap 2 2 beta mu +
   p.p30 * scaled_overlap 3 0 beta mu + p.p31 * scaled_overlap 3 1 beta mu + p.p32 * scaled_overlap 3 2 beta mu) / 3 - 3

theorem exact_inversion_b0_j0 (p : MUBProbabilities) :
    (p.p00 * 3 + p.p01 * 0 + p.p02 * 0 +
     (p.p10 + p.p11 + p.p12) * 1 +
     (p.p20 + p.p21 + p.p22) * 1 +
     (p.p30 + p.p31 + p.p32) * 1) - 9 = 3 * p.p00 := by
  have n1 := p.norm1
  have n2 := p.norm2
  have n3 := p.norm3
  omega

theorem exact_inversion_b0_j1 (p : MUBProbabilities) :
    (p.p00 * 0 + p.p01 * 3 + p.p02 * 0 +
     (p.p10 + p.p11 + p.p12) * 1 +
     (p.p20 + p.p21 + p.p22) * 1 +
     (p.p30 + p.p31 + p.p32) * 1) - 9 = 3 * p.p01 := by
  have n1 := p.norm1
  have n2 := p.norm2
  have n3 := p.norm3
  omega

theorem exact_inversion_b0_j2 (p : MUBProbabilities) :
    (p.p00 * 0 + p.p01 * 0 + p.p02 * 3 +
     (p.p10 + p.p11 + p.p12) * 1 +
     (p.p20 + p.p21 + p.p22) * 1 +
     (p.p30 + p.p31 + p.p32) * 1) - 9 = 3 * p.p02 := by
  have n1 := p.norm1
  have n2 := p.norm2
  have n3 := p.norm3
  omega

def prob_mixed : MUBProbabilities :=
  ⟨1, 1, 1,
   1, 1, 1,
   1, 1, 1,
   1, 1, 1,
   by decide, by decide, by decide, by decide⟩

theorem mixed_state_inversion_b0 :
    reconstructed_overlap_scaled prob_mixed 0 0 = 1 ∧
    reconstructed_overlap_scaled prob_mixed 0 1 = 1 ∧
    reconstructed_overlap_scaled prob_mixed 0 2 = 1 := by decide

theorem mixed_state_inversion_all_bases :
    reconstructed_overlap_scaled prob_mixed 0 0 = 1 ∧
    reconstructed_overlap_scaled prob_mixed 1 0 = 1 ∧
    reconstructed_overlap_scaled prob_mixed 2 0 = 1 ∧
    reconstructed_overlap_scaled prob_mixed 3 0 = 1 := by decide

def prob_pure0 : MUBProbabilities :=
  ⟨3, 0, 0,
   1, 1, 1,
   1, 1, 1,
   1, 1, 1,
   by decide, by decide, by decide, by decide⟩

theorem pure_state_0_inversion :
    reconstructed_overlap_scaled prob_pure0 0 0 = 3 ∧
    reconstructed_overlap_scaled prob_pure0 0 1 = 0 ∧
    reconstructed_overlap_scaled prob_pure0 0 2 = 0 ∧
    reconstructed_overlap_scaled prob_pure0 1 0 = 1 ∧
    reconstructed_overlap_scaled prob_pure0 2 0 = 1 ∧
    reconstructed_overlap_scaled prob_pure0 3 0 = 1 := by decide

def prob_pure1 : MUBProbabilities :=
  ⟨0, 3, 0,
   1, 1, 1,
   1, 1, 1,
   1, 1, 1,
   by decide, by decide, by decide, by decide⟩

theorem pure_state_1_inversion :
    reconstructed_overlap_scaled prob_pure1 0 0 = 0 ∧
    reconstructed_overlap_scaled prob_pure1 0 1 = 3 ∧
    reconstructed_overlap_scaled prob_pure1 0 2 = 0 := by decide

#print axioms mub_orthonormal_diag
#print axioms mub_orthogonal_01
#print axioms mub_orthogonal_02
#print axioms mub_orthogonal_12
#print axioms mub_cross_overlap
#print axioms exact_inversion_b0_j0
#print axioms exact_inversion_b0_j1
#print axioms exact_inversion_b0_j2
#print axioms mixed_state_inversion_b0
#print axioms mixed_state_inversion_all_bases
#print axioms pure_state_0_inversion
#print axioms pure_state_1_inversion

end HilbertWalk.MubTomographyInversion

private def l5aProvenance : String :=
  "Origin: lean4/MubTomographyInversion.lean Claim: mub_orthonormal_diag AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
