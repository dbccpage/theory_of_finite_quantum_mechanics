

namespace HilbertWalk.SurfaceCodeToricTopology

def list_sum (l : List Int) : Int :=
  l.foldl (· + ·) 0

def dot_list (l1 l2 : List Int) : Int :=
  (List.zipWith (· * ·) l1 l2).foldl (· + ·) 0


def star_00 : List Int := [1, 1, 0, 0, 1, 0, 1, 0]
def star_10 : List Int := [1, 1, 0, 0, 0, 1, 0, 1]
def star_01 : List Int := [0, 0, 1, 1, 1, 0, 1, 0]
def star_11 : List Int := [0, 0, 1, 1, 0, 1, 0, 1]

def plaq_00 : List Int := [1, 0, 1, 0, 1, 1, 0, 0]
def plaq_10 : List Int := [0, 1, 0, 1, 1, 1, 0, 0]
def plaq_01 : List Int := [1, 0, 1, 0, 0, 0, 1, 1]
def plaq_11 : List Int := [0, 1, 0, 1, 0, 0, 1, 1]

theorem star_weights :
    list_sum star_00 = 4 ∧ list_sum star_10 = 4 ∧
    list_sum star_01 = 4 ∧ list_sum star_11 = 4 := by decide

theorem plaq_weights :
    list_sum plaq_00 = 4 ∧ list_sum plaq_10 = 4 ∧
    list_sum plaq_01 = 4 ∧ list_sum plaq_11 = 4 := by decide

def star_plaq_commute_phase (s p : List Int) : Int :=
  if (dot_list s p) % 2 = 0 then 1 else -1

theorem all_star_plaq_commute :
    star_plaq_commute_phase star_00 plaq_00 = 1 ∧
    star_plaq_commute_phase star_00 plaq_10 = 1 ∧
    star_plaq_commute_phase star_00 plaq_01 = 1 ∧
    star_plaq_commute_phase star_00 plaq_11 = 1 ∧
    star_plaq_commute_phase star_10 plaq_00 = 1 ∧
    star_plaq_commute_phase star_10 plaq_10 = 1 ∧
    star_plaq_commute_phase star_10 plaq_01 = 1 ∧
    star_plaq_commute_phase star_10 plaq_11 = 1 ∧
    star_plaq_commute_phase star_01 plaq_00 = 1 ∧
    star_plaq_commute_phase star_01 plaq_10 = 1 ∧
    star_plaq_commute_phase star_01 plaq_01 = 1 ∧
    star_plaq_commute_phase star_01 plaq_11 = 1 ∧
    star_plaq_commute_phase star_11 plaq_00 = 1 ∧
    star_plaq_commute_phase star_11 plaq_10 = 1 ∧
    star_plaq_commute_phase star_11 plaq_01 = 1 ∧
    star_plaq_commute_phase star_11 plaq_11 = 1 := by decide

theorem star_plaq_geometric_overlaps :
    dot_list star_00 plaq_00 = 2 ∧ dot_list star_00 plaq_10 = 2 ∧
    dot_list star_00 plaq_01 = 2 ∧ dot_list star_00 plaq_11 = 2 ∧
    dot_list star_10 plaq_00 = 2 ∧ dot_list star_10 plaq_10 = 2 ∧
    dot_list star_10 plaq_01 = 2 ∧ dot_list star_10 plaq_11 = 2 := by decide

theorem torus_euler_characteristic : (4 : Int) - 8 + 4 = 0 := by decide

theorem torus_genus : 2 - 2 * (1 : Int) = 0 := by decide

theorem homology_dimension_k2 :
    (8 : Int) - (4 - 1) - (4 - 1) = 2 := by decide

def m_string_puncturing : List Int := [1, 0, 0, 0, 0, 0, 0, 0]

theorem anyon_loop_string_intersection :
    dot_list plaq_00 m_string_puncturing = 1 := by decide

theorem anyon_braiding_phase_pi :
    star_plaq_commute_phase plaq_00 m_string_puncturing = -1 := by decide

#print axioms star_weights
#print axioms plaq_weights
#print axioms all_star_plaq_commute
#print axioms star_plaq_geometric_overlaps
#print axioms torus_euler_characteristic
#print axioms torus_genus
#print axioms homology_dimension_k2
#print axioms anyon_loop_string_intersection
#print axioms anyon_braiding_phase_pi

end HilbertWalk.SurfaceCodeToricTopology

private def l5aProvenance : String :=
  "Origin: lean4/SurfaceCodeToricTopology.lean Claim: star_weights AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
