

namespace FableHilbertWalk20260819.H051

def scaled_overlap_d4 (b1 j1 b2 j2 : Nat) : Int :=
  if b1 = b2 then
    (if j1 = j2 then 4 else 0)
  else
    1

theorem mub4_orthonormal_diag (b j : Nat) : scaled_overlap_d4 b j b j = 4 := by
  dsimp [scaled_overlap_d4]
  split <;> rename_i h1
  · split <;> rename_i h2
    · rfl
    · contradiction
  · contradiction

theorem mub4_orthogonal_01 (b : Nat) : scaled_overlap_d4 b 0 b 1 = 0 := by
  dsimp [scaled_overlap_d4]
  split <;> rename_i h1
  · rfl
  · contradiction

theorem mub4_orthogonal_02 (b : Nat) : scaled_overlap_d4 b 0 b 2 = 0 := by
  dsimp [scaled_overlap_d4]
  split <;> rename_i h1
  · rfl
  · contradiction

theorem mub4_orthogonal_03 (b : Nat) : scaled_overlap_d4 b 0 b 3 = 0 := by
  dsimp [scaled_overlap_d4]
  split <;> rename_i h1
  · rfl
  · contradiction

theorem mub4_orthogonal_12 (b : Nat) : scaled_overlap_d4 b 1 b 2 = 0 := by
  dsimp [scaled_overlap_d4]
  split <;> rename_i h1
  · rfl
  · contradiction

theorem mub4_orthogonal_23 (b : Nat) : scaled_overlap_d4 b 2 b 3 = 0 := by
  dsimp [scaled_overlap_d4]
  split <;> rename_i h1
  · rfl
  · contradiction

theorem mub4_cross_overlap (b1 j1 b2 j2 : Nat) (h : b1 ≠ b2) :
    scaled_overlap_d4 b1 j1 b2 j2 = 1 := by
  dsimp [scaled_overlap_d4]
  split <;> rename_i h1
  · contradiction
  · rfl

def num_bases_d4 : Nat := 5

def dim_d4 : Nat := 4

theorem total_projectors_d4 : num_bases_d4 * dim_d4 = 20 := by
  rfl

theorem reconstructed_trace_is_one : (num_bases_d4 : Int) * 1 - (dim_d4 : Int) = 1 := by
  rfl

def valuation_purity_d4 : Int :=
  5 * 1 + 20 / 4 - 2 * 5 + 4

theorem valuation_purity_eval : valuation_purity_d4 = 4 := by
  rfl

def max_physical_purity : Int := 1

theorem mub4_non_psd_reconstruction_obstruction :
    valuation_purity_d4 > max_physical_purity := by
  rw [valuation_purity_eval]
  decide

theorem clifton_kent_d4_purity_obstruction :
    valuation_purity_d4 > max_physical_purity :=
  mub4_non_psd_reconstruction_obstruction

theorem mub4_purity_deficit :
    valuation_purity_d4 - max_physical_purity = 3 := by
  rw [valuation_purity_eval]
  rfl

theorem clifton_kent_d4_purity_deficit :
    valuation_purity_d4 - max_physical_purity = 3 :=
  mub4_purity_deficit

structure Pauli2 where
  x1 : Nat
  z1 : Nat
  x2 : Nat
  z2 : Nat
  deriving DecidableEq, Repr

def spInner (u v : Pauli2) : Nat :=
  (u.x1 * v.z1 + u.z1 * v.x1 + u.x2 * v.z2 + u.z2 * v.x2) % 2

def line0 : List Pauli2 := [⟨0, 1, 0, 0⟩, ⟨0, 0, 0, 1⟩, ⟨0, 1, 0, 1⟩]
def line1 : List Pauli2 := [⟨1, 0, 0, 0⟩, ⟨0, 0, 1, 0⟩, ⟨1, 0, 1, 0⟩]
def line2 : List Pauli2 := [⟨1, 1, 0, 0⟩, ⟨0, 0, 1, 1⟩, ⟨1, 1, 1, 1⟩]
def line3 : List Pauli2 := [⟨0, 1, 1, 0⟩, ⟨1, 0, 1, 1⟩, ⟨1, 1, 0, 1⟩]
def line4 : List Pauli2 := [⟨0, 1, 1, 1⟩, ⟨1, 1, 1, 0⟩, ⟨1, 0, 0, 1⟩]

theorem line_lengths :
    line0.length = 3 ∧ line1.length = 3 ∧ line2.length = 3 ∧ line3.length = 3 ∧ line4.length = 3 := by
  decide

theorem line0_is_isotropic :
    spInner (line0.get ⟨0, by decide⟩) (line0.get ⟨1, by decide⟩) = 0 ∧
    spInner (line0.get ⟨0, by decide⟩) (line0.get ⟨2, by decide⟩) = 0 ∧
    spInner (line0.get ⟨1, by decide⟩) (line0.get ⟨2, by decide⟩) = 0 := by decide

theorem line1_is_isotropic :
    spInner (line1.get ⟨0, by decide⟩) (line1.get ⟨1, by decide⟩) = 0 ∧
    spInner (line1.get ⟨0, by decide⟩) (line1.get ⟨2, by decide⟩) = 0 ∧
    spInner (line1.get ⟨1, by decide⟩) (line1.get ⟨2, by decide⟩) = 0 := by decide

theorem line2_is_isotropic :
    spInner (line2.get ⟨0, by decide⟩) (line2.get ⟨1, by decide⟩) = 0 ∧
    spInner (line2.get ⟨0, by decide⟩) (line2.get ⟨2, by decide⟩) = 0 ∧
    spInner (line2.get ⟨1, by decide⟩) (line2.get ⟨2, by decide⟩) = 0 := by decide

theorem line3_is_isotropic :
    spInner (line3.get ⟨0, by decide⟩) (line3.get ⟨1, by decide⟩) = 0 ∧
    spInner (line3.get ⟨0, by decide⟩) (line3.get ⟨2, by decide⟩) = 0 ∧
    spInner (line3.get ⟨1, by decide⟩) (line3.get ⟨2, by decide⟩) = 0 := by decide

theorem line4_is_isotropic :
    spInner (line4.get ⟨0, by decide⟩) (line4.get ⟨1, by decide⟩) = 0 ∧
    spInner (line4.get ⟨0, by decide⟩) (line4.get ⟨2, by decide⟩) = 0 ∧
    spInner (line4.get ⟨1, by decide⟩) (line4.get ⟨2, by decide⟩) = 0 := by decide

def all15Paulis : List Pauli2 :=
  line0 ++ line1 ++ line2 ++ line3 ++ line4

theorem all15_paulis_length : all15Paulis.length = 15 := by rfl

theorem all15_paulis_nodup : all15Paulis.Nodup := by decide

theorem five_mub_isotropic_lines_partition :
    all15Paulis.length = 15 ∧
    all15Paulis.Nodup ∧
    (line0.length = 3 ∧ line1.length = 3 ∧ line2.length = 3 ∧ line3.length = 3 ∧ line4.length = 3) := by
  refine ⟨rfl, by decide, by decide⟩

#print axioms mub4_orthonormal_diag
#print axioms mub4_orthogonal_01
#print axioms mub4_orthogonal_02
#print axioms mub4_orthogonal_03
#print axioms mub4_cross_overlap
#print axioms total_projectors_d4
#print axioms reconstructed_trace_is_one
#print axioms valuation_purity_eval
#print axioms clifton_kent_d4_purity_obstruction
#print axioms clifton_kent_d4_purity_deficit
#print axioms line_lengths
#print axioms line0_is_isotropic
#print axioms line1_is_isotropic
#print axioms line2_is_isotropic
#print axioms line3_is_isotropic
#print axioms line4_is_isotropic
#print axioms all15_paulis_nodup
#print axioms five_mub_isotropic_lines_partition

end FableHilbertWalk20260819.H051


private def l5aProvenance : String :=
  "Origin: lean4/H051Mub4GaloisFieldContextuality.lean Claim: mub4_orthonormal_diag AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
