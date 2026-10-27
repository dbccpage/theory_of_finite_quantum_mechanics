

namespace HilbertWalk.OctahedralMubCliftonKent


theorem binary_spin_squared (x : Int) (h : x = 0 ∨ x = 1) :
    (2 * x - 1) ^ 2 = 1 := by
  rcases h with rfl | rfl
  · decide
  · decide

structure MUBVertex where
  xz : Int
  xx : Int
  xy : Int
  hz : xz = 0 ∨ xz = 1
  hx : xx = 0 ∨ xx = 1
  hy : xy = 0 ∨ xy = 1

def bloch_radius_sq (v : MUBVertex) : Int :=
  (2 * v.xz - 1) ^ 2 + (2 * v.xx - 1) ^ 2 + (2 * v.xy - 1) ^ 2

theorem octahedral_bloch_radius_sq_is_three (v : MUBVertex) :
    bloch_radius_sq v = 3 := by
  dsimp [bloch_radius_sq]
  have hz := binary_spin_squared v.xz v.hz
  have hx := binary_spin_squared v.xx v.hx
  have hy := binary_spin_squared v.xy v.hy
  rw [hz, hx, hy]
  rfl

theorem octahedral_non_psd_reconstruction_obstruction (v : MUBVertex) :
    bloch_radius_sq v > 1 := by
  rw [octahedral_bloch_radius_sq_is_three v]
  decide

theorem clifton_kent_non_psd_obstruction (v : MUBVertex) :
    bloch_radius_sq v > 1 :=
  octahedral_non_psd_reconstruction_obstruction v


def v000 : MUBVertex := ⟨0, 0, 0, Or.inl rfl, Or.inl rfl, Or.inl rfl⟩
def v001 : MUBVertex := ⟨0, 0, 1, Or.inl rfl, Or.inl rfl, Or.inr rfl⟩
def v010 : MUBVertex := ⟨0, 1, 0, Or.inl rfl, Or.inr rfl, Or.inl rfl⟩
def v011 : MUBVertex := ⟨0, 1, 1, Or.inl rfl, Or.inr rfl, Or.inr rfl⟩
def v100 : MUBVertex := ⟨1, 0, 0, Or.inr rfl, Or.inl rfl, Or.inl rfl⟩
def v101 : MUBVertex := ⟨1, 0, 1, Or.inr rfl, Or.inl rfl, Or.inr rfl⟩
def v110 : MUBVertex := ⟨1, 1, 0, Or.inr rfl, Or.inr rfl, Or.inl rfl⟩
def v111 : MUBVertex := ⟨1, 1, 1, Or.inr rfl, Or.inr rfl, Or.inr rfl⟩

theorem all_eight_vertices_eval :
    bloch_radius_sq v000 = 3 ∧
    bloch_radius_sq v001 = 3 ∧
    bloch_radius_sq v010 = 3 ∧
    bloch_radius_sq v011 = 3 ∧
    bloch_radius_sq v100 = 3 ∧
    bloch_radius_sq v101 = 3 ∧
    bloch_radius_sq v110 = 3 ∧
    bloch_radius_sq v111 = 3 := by
  refine ⟨rfl, rfl, rfl, rfl, rfl, rfl, rfl, rfl⟩


theorem graph_state_symplectic_commutation (a_uv : Int) :
    (a_uv + a_uv) % 2 = 0 := by
  have h : a_uv + a_uv = 2 * a_uv := by omega
  rw [h, Int.mul_emod_right]

#print axioms binary_spin_squared
#print axioms octahedral_bloch_radius_sq_is_three
#print axioms clifton_kent_non_psd_obstruction
#print axioms all_eight_vertices_eval
#print axioms graph_state_symplectic_commutation

end HilbertWalk.OctahedralMubCliftonKent

private def l5aProvenance : String :=
  "Origin: lean4/OctahedralMubCliftonKent.lean Claim: binary_spin_squared AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
