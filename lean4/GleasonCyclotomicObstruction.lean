

namespace HilbertWalk.GleasonCyclotomicObstruction


structure Vec4 where
  x0 : Int
  x1 : Int
  x2 : Int
  x3 : Int
  deriving DecidableEq, Repr

def dot4 (u v : Vec4) : Int :=
  u.x0 * v.x0 + u.x1 * v.x1 + u.x2 * v.x2 + u.x3 * v.x3

def norm_sq4 (v : Vec4) : Int :=
  dot4 v v

def v0  : Vec4 := ⟨1, 1, 1, 1⟩
def v1  : Vec4 := ⟨1, 1, 1, -1⟩
def v2  : Vec4 := ⟨1, 1, 0, 0⟩
def v3  : Vec4 := ⟨1, 1, -1, -1⟩
def v4  : Vec4 := ⟨1, 0, 1, 0⟩
def v5  : Vec4 := ⟨1, 0, 0, 1⟩
def v6  : Vec4 := ⟨1, 0, 0, -1⟩
def v7  : Vec4 := ⟨1, 0, -1, 0⟩
def v8  : Vec4 := ⟨1, -1, 1, 1⟩
def v9  : Vec4 := ⟨1, -1, 0, 0⟩
def v10 : Vec4 := ⟨1, -1, -1, 1⟩
def v11 : Vec4 := ⟨1, -1, -1, -1⟩
def v12 : Vec4 := ⟨0, 1, 0, 1⟩
def v13 : Vec4 := ⟨0, 1, 0, 0⟩
def v14 : Vec4 := ⟨0, 1, -1, 0⟩
def v15 : Vec4 := ⟨0, 0, 1, 0⟩
def v16 : Vec4 := ⟨0, 0, 1, -1⟩
def v17 : Vec4 := ⟨0, 0, 0, 1⟩

def cabello18 : List Vec4 :=
  [v0, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16, v17]

theorem cabello_18_count : cabello18.length = 18 := by rfl

def tetrad0 : List Vec4 := [v2, v9, v15, v17]
def tetrad1 : List Vec4 := [v4, v7, v13, v17]
def tetrad2 : List Vec4 := [v5, v6, v13, v15]
def tetrad3 : List Vec4 := [v0, v3, v9, v16]
def tetrad4 : List Vec4 := [v0, v6, v10, v14]
def tetrad5 : List Vec4 := [v1, v5, v11, v14]
def tetrad6 : List Vec4 := [v1, v7, v8, v12]
def tetrad7 : List Vec4 := [v2, v8, v11, v16]
def tetrad8 : List Vec4 := [v3, v4, v10, v12]

def cabello_contexts : List (List Vec4) :=
  [tetrad0, tetrad1, tetrad2, tetrad3, tetrad4, tetrad5, tetrad6, tetrad7, tetrad8]

theorem cabello_9_tetrad_count : cabello_contexts.length = 9 := by rfl

def is_pairwise_ortho4 (a b c d : Vec4) : Bool :=
  dot4 a b == 0 && dot4 a c == 0 && dot4 a d == 0 &&
  dot4 b c == 0 && dot4 b d == 0 && dot4 c d == 0

theorem cabello_tetrads_orthogonal :
    is_pairwise_ortho4 v2 v9 v15 v17 = true ∧
    is_pairwise_ortho4 v4 v7 v13 v17 = true ∧
    is_pairwise_ortho4 v5 v6 v13 v15 = true ∧
    is_pairwise_ortho4 v0 v3 v9 v16 = true ∧
    is_pairwise_ortho4 v0 v6 v10 v14 = true ∧
    is_pairwise_ortho4 v1 v5 v11 v14 = true ∧
    is_pairwise_ortho4 v1 v7 v8 v12 = true ∧
    is_pairwise_ortho4 v2 v8 v11 v16 = true ∧
    is_pairwise_ortho4 v3 v4 v10 v12 = true := by
  decide

theorem cabello_no_integer_frame_assignment (f : Vec4 → Int)
    (h0 : f v2 + f v9 + f v15 + f v17 = 1)
    (h1 : f v4 + f v7 + f v13 + f v17 = 1)
    (h2 : f v5 + f v6 + f v13 + f v15 = 1)
    (h3 : f v0 + f v3 + f v9 + f v16 = 1)
    (h4 : f v0 + f v6 + f v10 + f v14 = 1)
    (h5 : f v1 + f v5 + f v11 + f v14 = 1)
    (h6 : f v1 + f v7 + f v8 + f v12 = 1)
    (h7 : f v2 + f v8 + f v11 + f v16 = 1)
    (h8 : f v3 + f v4 + f v10 + f v12 = 1) : False := by
  omega


structure SymMat4 where
  m00 : Int
  m01 : Int
  m02 : Int
  m03 : Int
  m11 : Int
  m12 : Int
  m13 : Int
  m22 : Int
  m23 : Int
  m33 : Int
  deriving DecidableEq, Repr

def quad_form (M : SymMat4) (x : Vec4) : Int :=
  M.m00 * x.x0 * x.x0 + M.m11 * x.x1 * x.x1 + M.m22 * x.x2 * x.x2 + M.m33 * x.x3 * x.x3 +
  2 * (M.m01 * x.x0 * x.x1 + M.m02 * x.x0 * x.x2 + M.m03 * x.x0 * x.x3 +
       M.m12 * x.x1 * x.x2 + M.m13 * x.x1 * x.x3 +
       M.m23 * x.x2 * x.x3)

def M_bad : SymMat4 := {
  m00 := 0, m01 := 0, m02 := 0, m03 := 0,
  m11 := 2, m12 := 1, m13 := -1,
  m22 := 0, m23 := -1,
  m33 := 0
}

def scaled_ratio_4 (v : Vec4) : Int :=
  (quad_form M_bad v * 4) / norm_sq4 v

theorem bad_mat_rays_nonneg :
    (0 ≤ quad_form M_bad v0) ∧ (0 ≤ quad_form M_bad v1) ∧
    (0 ≤ quad_form M_bad v2) ∧ (0 ≤ quad_form M_bad v3) ∧
    (0 ≤ quad_form M_bad v4) ∧ (0 ≤ quad_form M_bad v5) ∧
    (0 ≤ quad_form M_bad v6) ∧ (0 ≤ quad_form M_bad v7) ∧
    (0 ≤ quad_form M_bad v8) ∧ (0 ≤ quad_form M_bad v9) ∧
    (0 ≤ quad_form M_bad v10) ∧ (0 ≤ quad_form M_bad v11) ∧
    (0 ≤ quad_form M_bad v12) ∧ (0 ≤ quad_form M_bad v13) ∧
    (0 ≤ quad_form M_bad v14) ∧ (0 ≤ quad_form M_bad v15) ∧
    (0 ≤ quad_form M_bad v16) ∧ (0 ≤ quad_form M_bad v17) := by
  decide

theorem bad_mat_rays_bounded :
    (quad_form M_bad v0 ≤ 2 * norm_sq4 v0) ∧
    (quad_form M_bad v1 ≤ 2 * norm_sq4 v1) ∧
    (quad_form M_bad v2 ≤ 2 * norm_sq4 v2) ∧
    (quad_form M_bad v3 ≤ 2 * norm_sq4 v3) ∧
    (quad_form M_bad v4 ≤ 2 * norm_sq4 v4) ∧
    (quad_form M_bad v5 ≤ 2 * norm_sq4 v5) ∧
    (quad_form M_bad v6 ≤ 2 * norm_sq4 v6) ∧
    (quad_form M_bad v7 ≤ 2 * norm_sq4 v7) ∧
    (quad_form M_bad v8 ≤ 2 * norm_sq4 v8) ∧
    (quad_form M_bad v9 ≤ 2 * norm_sq4 v9) ∧
    (quad_form M_bad v10 ≤ 2 * norm_sq4 v10) ∧
    (quad_form M_bad v11 ≤ 2 * norm_sq4 v11) ∧
    (quad_form M_bad v12 ≤ 2 * norm_sq4 v12) ∧
    (quad_form M_bad v13 ≤ 2 * norm_sq4 v13) ∧
    (quad_form M_bad v14 ≤ 2 * norm_sq4 v14) ∧
    (quad_form M_bad v15 ≤ 2 * norm_sq4 v15) ∧
    (quad_form M_bad v16 ≤ 2 * norm_sq4 v16) ∧
    (quad_form M_bad v17 ≤ 2 * norm_sq4 v17) := by
  decide

def tetrad_sum_scaled_4 (a b c d : Vec4) : Int :=
  scaled_ratio_4 a + scaled_ratio_4 b + scaled_ratio_4 c + scaled_ratio_4 d

theorem bad_mat_tetrad_sums_8 :
    tetrad_sum_scaled_4 v2 v9 v15 v17 = 8 ∧
    tetrad_sum_scaled_4 v4 v7 v13 v17 = 8 ∧
    tetrad_sum_scaled_4 v5 v6 v13 v15 = 8 ∧
    tetrad_sum_scaled_4 v0 v3 v9 v16 = 8 ∧
    tetrad_sum_scaled_4 v0 v6 v10 v14 = 8 ∧
    tetrad_sum_scaled_4 v1 v5 v11 v14 = 8 ∧
    tetrad_sum_scaled_4 v1 v7 v8 v12 = 8 ∧
    tetrad_sum_scaled_4 v2 v8 v11 v16 = 8 ∧
    tetrad_sum_scaled_4 v3 v4 v10 v12 = 8 := by
  decide

def w_witness : Vec4 := ⟨0, 0, 1, 1⟩

theorem bad_mat_witness_negative :
    quad_form M_bad w_witness = -2 := by rfl

theorem frame_additivity_not_force_psd :
    (quad_form M_bad w_witness < 0) ∧
    (tetrad_sum_scaled_4 v2 v9 v15 v17 = 8) ∧
    (0 ≤ quad_form M_bad v0) := by
  decide

theorem all_cabello_checks_do_not_certify_psd :
    cabello18.all (fun v => decide (0 < norm_sq4 v ∧
      0 ≤ quad_form M_bad v ∧ quad_form M_bad v ≤ 2 * norm_sq4 v)) = true ∧
    cabello_contexts.all (fun c =>
      (c.map scaled_ratio_4).foldl (· + ·) 0 == (8 : Int)) = true ∧
    quad_form M_bad w_witness < 0 := by
  decide


structure Vec3 where
  x : Int
  y : Int
  z : Int
  deriving DecidableEq, Repr

def norm_sq3 (v : Vec3) : Int :=
  v.x * v.x + v.y * v.y + v.z * v.z

def on_sphere_25 (v : Vec3) : Prop :=
  norm_sq3 v = 25

def in_U (v : Vec3) : Prop :=
  2 * (v.z * v.z) < 25

def in_V (v : Vec3) : Prop :=
  2 * (v.z * v.z) > 25

theorem no_int_2z2_eq_25 (z : Int) :
    2 * (z * z) ≠ 25 := by
  omega

theorem sphere_clopen_partition (v : Vec3) (_h : on_sphere_25 v) :
    in_U v ∨ in_V v := by
  dsimp [in_U, in_V]
  have h_ne := no_int_2z2_eq_25 v.z
  omega

theorem U_disjoint_V (v : Vec3) :
    ¬ (in_U v ∧ in_V v) := by
  dsimp [in_U, in_V]
  omega

def pole_x : Vec3 := ⟨5, 0, 0⟩
def pole_z : Vec3 := ⟨0, 0, 5⟩

theorem pole_x_on_sphere : on_sphere_25 pole_x := by rfl
theorem pole_x_in_U : in_U pole_x := by
  dsimp [in_U, pole_x]
  omega

theorem pole_z_on_sphere : on_sphere_25 pole_z := by rfl
theorem pole_z_in_V : in_V pole_z := by
  dsimp [in_V, pole_z]
  omega

theorem sphere_disconnected_witness :
    (on_sphere_25 pole_x ∧ in_U pole_x) ∧
    (on_sphere_25 pole_z ∧ in_V pole_z) ∧
    (∀ v, on_sphere_25 v → in_U v ∨ in_V v) ∧
    (∀ v, ¬ (in_U v ∧ in_V v)) := by
  refine ⟨⟨pole_x_on_sphere, pole_x_in_U⟩, ⟨pole_z_on_sphere, pole_z_in_V⟩, ?_, U_disjoint_V⟩
  intro v hv
  exact sphere_clopen_partition v hv


def targetConductor120 : Nat := 120
def discSqrt7 : Nat := 28

theorem disc_28_not_dvd_120 : ¬ (28 ∣ targetConductor120) := by decide

theorem prime_7_not_dvd_120 : ¬ (7 ∣ targetConductor120) := by decide

theorem no_int_7z2_eq_25 (z : Int) :
    7 * (z * z) ≠ 25 := by
  have h_lin (X : Int) : 7 * X ≠ 25 := by omega
  exact h_lin (z * z)

def in_U7 (v : Vec3) : Prop :=
  7 * (v.z * v.z) < 25

def in_V7 (v : Vec3) : Prop :=
  7 * (v.z * v.z) > 25

theorem sphere_clopen_partition_7 (v : Vec3) (_h : on_sphere_25 v) :
    in_U7 v ∨ in_V7 v := by
  dsimp [in_U7, in_V7]
  have h_ne := no_int_7z2_eq_25 v.z
  omega

theorem U7_disjoint_V7 (v : Vec3) :
    ¬ (in_U7 v ∧ in_V7 v) := by
  dsimp [in_U7, in_V7]
  omega

theorem pole_x_in_U7 : in_U7 pole_x := by
  dsimp [in_U7, pole_x]
  omega

theorem pole_z_in_V7 : in_V7 pole_z := by
  dsimp [in_V7, pole_z]
  omega

theorem sphere_disconnected_sqrt7_witness :
    (on_sphere_25 pole_x ∧ in_U7 pole_x) ∧
    (on_sphere_25 pole_z ∧ in_V7 pole_z) ∧
    (∀ v, on_sphere_25 v → in_U7 v ∨ in_V7 v) ∧
    (∀ v, ¬ (in_U7 v ∧ in_V7 v)) := by
  refine ⟨⟨pole_x_on_sphere, pole_x_in_U7⟩, ⟨pole_z_on_sphere, pole_z_in_V7⟩, ?_, U7_disjoint_V7⟩
  intro v hv
  exact sphere_clopen_partition_7 v hv


inductive GleasonGapResolution where
  | open_conditional (reason : String)
  deriving Repr, DecidableEq

def resolution_gap_004 : GleasonGapResolution :=
  GleasonGapResolution.open_conditional
    "Dense-subfield frame functions remain open; the integer partition is not a topology proof"

def resolution_gap_010 : GleasonGapResolution :=
  GleasonGapResolution.open_conditional
    "Born uniqueness remains open; no necessity theorem for continuum completion is supplied"

theorem cabello_finite_contextuality_not_psd :
    (quad_form M_bad w_witness = -2) ∧
    (tetrad_sum_scaled_4 v2 v9 v15 v17 = 8) ∧
    (0 ≤ quad_form M_bad v0) ∧
    (resolution_gap_004 ≠ resolution_gap_010) := by
  decide

#print axioms cabello_18_count
#print axioms cabello_9_tetrad_count
#print axioms cabello_tetrads_orthogonal
#print axioms cabello_no_integer_frame_assignment
#print axioms all_cabello_checks_do_not_certify_psd
#print axioms bad_mat_rays_nonneg
#print axioms bad_mat_rays_bounded
#print axioms bad_mat_tetrad_sums_8
#print axioms bad_mat_witness_negative
#print axioms frame_additivity_not_force_psd
#print axioms no_int_2z2_eq_25
#print axioms sphere_clopen_partition
#print axioms U_disjoint_V
#print axioms sphere_disconnected_witness
#print axioms disc_28_not_dvd_120
#print axioms prime_7_not_dvd_120
#print axioms sphere_clopen_partition_7
#print axioms U7_disjoint_V7
#print axioms sphere_disconnected_sqrt7_witness
#print axioms cabello_finite_contextuality_not_psd

end HilbertWalk.GleasonCyclotomicObstruction

private def l5aProvenance : String :=
  "Origin: lean4/GleasonCyclotomicObstruction.lean Claim: cabello_18_count AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
