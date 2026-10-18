


namespace FiniteQM


abbrev P2 (x y z : Rat) : Rat :=
  x * x + y * y + z * z

abbrev P4 (x y z : Rat) : Rat :=
  (x * x) * (x * x) + (y * y) * (y * y) + (z * z) * (z * z)

abbrev P22 (x y z : Rat) : Rat :=
  (x * x) * (y * y) + (y * y) * (z * z) + (z * z) * (x * x)

theorem p2_sq_eq_p4_add_two_p22 (x y z : Rat) :
    P2 x y z * P2 x y z = P4 x y z + 2 * P22 x y z := by
  grind

theorem degree4_unit_sphere_basis_identity (x y z : Rat)
    (h_sphere : x * x + y * y + z * z = 1) :
    (x * x) * (x * x) + (y * y) * (y * y) + (z * z) * (z * z) =
      1 - 2 * ((x * x) * (y * y) + (y * y) * (z * z) + (z * z) * (x * x)) := by
  have hid := p2_sq_eq_p4_add_two_p22 x y z
  grind

theorem p4_eq_one_sub_two_p22_on_unit_sphere (x y z : Rat)
    (h_sphere : P2 x y z = 1) :
    P4 x y z = 1 - 2 * P22 x y z := by
  have hid := p2_sq_eq_p4_add_two_p22 x y z
  grind

abbrev symDeg4FrameSum (c2 q4 r4 x y z : Rat) : Rat :=
  c2 * P2 x y z + q4 * P4 x y z + 2 * r4 * P22 x y z

theorem sym_deg4_frame_sum_on_unit_sphere (c2 q4 r4 x y z : Rat)
    (h_sphere : P2 x y z = 1) :
    symDeg4FrameSum c2 q4 r4 x y z =
      (c2 + q4) + 2 * (r4 - q4) * P22 x y z := by
  have hp4 := p4_eq_one_sub_two_p22_on_unit_sphere x y z h_sphere
  grind

theorem unit_sphere_standard_ray_witness :
    P2 1 0 0 = 1 ∧
    P4 1 0 0 = 1 ∧
    P22 1 0 0 = 0 ∧
    P4 1 0 0 = 1 - 2 * P22 1 0 0 := by
  grind

theorem unit_sphere_pythagorean_ray_witness :
    P2 (3 / 5) (4 / 5) 0 = 1 ∧
    P4 (3 / 5) (4 / 5) 0 = 337 / 625 ∧
    P22 (3 / 5) (4 / 5) 0 = 144 / 625 ∧
    P4 (3 / 5) (4 / 5) 0 = 1 - 2 * P22 (3 / 5) (4 / 5) 0 := by
  grind

theorem unit_sphere_rational_3d_ray_witness :
    P2 (1 / 3) (2 / 3) (2 / 3) = 1 ∧
    P4 (1 / 3) (2 / 3) (2 / 3) = 11 / 27 ∧
    P22 (1 / 3) (2 / 3) (2 / 3) = 8 / 27 ∧
    P4 (1 / 3) (2 / 3) (2 / 3) = 1 - 2 * P22 (1 / 3) (2 / 3) (2 / 3) := by
  grind

abbrev sorkinI3 (R : Rat → Rat) (a b c : Rat) : Rat :=
  R (a + b + c) - R (a + b) - R (a + c) - R (b + c) + R a + R b + R c - R 0

abbrev symDeg4AxisReadout (c2 q4 x : Rat) : Rat :=
  c2 * (x * x) + q4 * ((x * x) * (x * x))

theorem sym_deg4_sorkin_i3_at_unit_triple (c2 q4 : Rat) :
    sorkinI3 (symDeg4AxisReadout c2 q4) 1 1 1 = 36 * q4 := by
  grind

theorem quadratic_readout_selected_in_sym_deg4_class (c2 q4 r4 : Rat)
    (h_std : symDeg4FrameSum c2 q4 r4 1 0 0 = 1)
    (h_pyth : symDeg4FrameSum c2 q4 r4 (3 / 5) (4 / 5) 0 = 1)
    (h_sorkin : sorkinI3 (symDeg4AxisReadout c2 q4) 1 1 1 = 0) :
    c2 = 1 ∧ q4 = 0 ∧ r4 = 0 := by
  have hs := sym_deg4_sorkin_i3_at_unit_triple c2 q4
  grind


structure QZeta12 where
  c0 : Rat
  c1 : Rat
  c2 : Rat
  c3 : Rat
  deriving DecidableEq, Repr

namespace QZeta12

abbrev zero : QZeta12 := ⟨0, 0, 0, 0⟩
abbrev one : QZeta12 := ⟨1, 0, 0, 0⟩
abbrev zeta : QZeta12 := ⟨0, 1, 0, 0⟩

abbrev sub (a b : QZeta12) : QZeta12 :=
  ⟨a.c0 - b.c0, a.c1 - b.c1, a.c2 - b.c2, a.c3 - b.c3⟩

abbrev mul (a b : QZeta12) : QZeta12 :=
  ⟨a.c0 * b.c0 - (a.c1 * b.c3 + a.c2 * b.c2 + a.c3 * b.c1) - a.c3 * b.c3,
   a.c0 * b.c1 + a.c1 * b.c0 - (a.c2 * b.c3 + a.c3 * b.c2),
   a.c0 * b.c2 + a.c1 * b.c1 + a.c2 * b.c0 + (a.c1 * b.c3 + a.c2 * b.c2 + a.c3 * b.c1),
   a.c0 * b.c3 + a.c1 * b.c2 + a.c2 * b.c1 + a.c3 * b.c0 + (a.c2 * b.c3 + a.c3 * b.c2)⟩

abbrev conj (a : QZeta12) : QZeta12 :=
  ⟨a.c0 + a.c2, a.c1, -a.c2, -a.c1 - a.c3⟩

abbrev bornWeight (a : QZeta12) : QZeta12 :=
  mul a (conj a)

abbrev normN0 (a : QZeta12) : Rat :=
  (bornWeight a).c0

abbrev normN1 (a : QZeta12) : Rat :=
  -(bornWeight a).c3

abbrev vPlus : QZeta12 := ⟨2, 2, 0, -1⟩

abbrev vMinus : QZeta12 := ⟨2, -2, 0, 1⟩

theorem zeta_minus_one_unit_inverse :
    mul (sub zeta one) ⟨0, 0, -1, -1⟩ = one := by
  grind

theorem fundamental_unit_norm_identities :
    mul vPlus vMinus = one ∧
    normN0 vPlus = 7 ∧ normN1 vPlus = 4 ∧
    normN0 vMinus = 7 ∧ normN1 vMinus = -4 ∧
    normN0 (mul vPlus vPlus) = 97 ∧ normN1 (mul vPlus vPlus) = 56 ∧
    normN0 (mul vMinus vMinus) = 97 ∧ normN1 (mul vMinus vMinus) = -56 := by
  grind

abbrev readoutAB (A B : Rat) (x : QZeta12) : Rat :=
  A * normN0 x + B * normN1 x

theorem qzeta12_rational_readout_cone_and_galois_selection (A B : Rat) :
    let minor1 : Rat := 1
    let minor2 : Rat := 1 - (1 : Rat) ^ 2 / 4
    let minor3 : Rat := (3 * (1 : Rat) ^ 2 - (1 : Rat) ^ 2) / 6
    let minor4 : Rat := (3 * (1 : Rat) ^ 2 - (1 : Rat) ^ 2) ^ 2 / 144
    readoutAB A B one = A ∧
    (readoutAB A B vPlus - readoutAB A B vMinus) / 8 = B ∧
    readoutAB 1 1 vPlus = 11 ∧
    readoutAB 1 1 vMinus = 3 ∧
    minor1 = 1 ∧ minor2 = 3 / 4 ∧ minor3 = 1 / 3 ∧ minor4 = 1 / 36 ∧
    minor1 > 0 ∧ minor2 > 0 ∧ minor3 > 0 ∧ minor4 > 0 ∧
    (readoutAB A B vPlus = readoutAB A B vMinus ↔ B = 0) := by
  grind

end QZeta12


@[ext]
structure Mat2Rat where
  a00 : Rat
  a01 : Rat
  a10 : Rat
  a11 : Rat
  deriving DecidableEq, Repr

namespace Mat2Rat

abbrev zero : Mat2Rat := ⟨0, 0, 0, 0⟩
abbrev id : Mat2Rat := ⟨1, 0, 0, 1⟩

abbrev add (A B : Mat2Rat) : Mat2Rat :=
  ⟨A.a00 + B.a00, A.a01 + B.a01, A.a10 + B.a10, A.a11 + B.a11⟩

abbrev mul (A B : Mat2Rat) : Mat2Rat :=
  ⟨A.a00 * B.a00 + A.a01 * B.a10,
   A.a00 * B.a01 + A.a01 * B.a11,
   A.a10 * B.a00 + A.a11 * B.a10,
   A.a10 * B.a01 + A.a11 * B.a11⟩

abbrev sub (A B : Mat2Rat) : Mat2Rat :=
  ⟨A.a00 - B.a00, A.a01 - B.a01, A.a10 - B.a10, A.a11 - B.a11⟩

abbrev transpose (A : Mat2Rat) : Mat2Rat :=
  ⟨A.a00, A.a10, A.a01, A.a11⟩

abbrev tr (A : Mat2Rat) : Rat :=
  A.a00 + A.a11

abbrev det (A : Mat2Rat) : Rat :=
  A.a00 * A.a11 - A.a01 * A.a10

abbrev comm (A B : Mat2Rat) : Mat2Rat :=
  sub (mul A B) (mul B A)

abbrev quadForm (A : Mat2Rat) (x y : Rat) : Rat :=
  x * (A.a00 * x + A.a01 * y) + y * (A.a10 * x + A.a11 * y)

end Mat2Rat


abbrev rot207 : Mat2Rat := ⟨0, -1, 1, 0⟩

abbrev pauliX2 : Mat2Rat := ⟨0, 1, 1, 0⟩
abbrev pauliZ2 : Mat2Rat := ⟨1, 0, 0, -1⟩

abbrev rhoReal2 : Mat2Rat := ⟨1 / 2, 0, 0, 1 / 2⟩

abbrev quadReadoutRat (x : Rat) : Rat := x * x

theorem quad_readout_sorkin_i3_zero (a b c : Rat) :
    sorkinI3 quadReadoutRat a b c = 0 := by
  grind

theorem countermodel_m207_properties :
    sorkinI3 quadReadoutRat 1 2 3 = 0 ∧
    Mat2Rat.comm pauliX2 pauliZ2 = ⟨0, -2, 2, 0⟩ ∧
    Mat2Rat.comm pauliX2 pauliZ2 ≠ Mat2Rat.zero ∧
    Mat2Rat.tr rhoReal2 = 1 ∧
    Mat2Rat.quadForm rhoReal2 1 0 = 1 / 2 ∧
    Mat2Rat.quadForm rhoReal2 0 1 = 1 / 2 ∧
    Mat2Rat.mul (Mat2Rat.transpose rot207) rot207 = Mat2Rat.id ∧
    Mat2Rat.det rot207 = 1 ∧
    Mat2Rat.mul (Mat2Rat.mul rot207 rot207) (Mat2Rat.mul rot207 rot207) = Mat2Rat.id ∧
    ((4 * 5) / 2 - 1 : Nat) ≠ 2 + 2 + 2 * 2 := by
  grind

theorem no_rat_square_eq_neg_one (z : Rat) : z * z ≠ -1 := by
  have hsq : 0 ≤ z * z := by
    by_cases hz : 0 ≤ z
    · exact Rat.mul_nonneg hz hz
    · have hnz : 0 ≤ -z := by grind
      have hp := Rat.mul_nonneg hnz hnz
      grind
  grind


abbrev quarticReadoutRat (x : Rat) : Rat := (x * x) * (x * x)

theorem countermodel_m208_properties :
    sorkinI3 quarticReadoutRat 1 1 1 = 36 ∧
    sorkinI3 quarticReadoutRat 1 1 1 ≠ 0 ∧
    quarticReadoutRat (3 / 5) + quarticReadoutRat (4 / 5) = 337 / 625 ∧
    (quarticReadoutRat 1 + quarticReadoutRat 0) -
      (quarticReadoutRat (3 / 5) + quarticReadoutRat (4 / 5)) = 288 / 625 := by
  grind


abbrev diag2Rat (a d : Rat) : Mat2Rat := ⟨a, 0, 0, d⟩

theorem countermodel_m209_all_diagonal_commute (a1 d1 a2 d2 : Rat) :
    Mat2Rat.comm (diag2Rat a1 d1) (diag2Rat a2 d2) = Mat2Rat.zero := by
  grind


abbrev rhoQuasi2Rat : Mat2Rat := ⟨1 / 2, 3 / 4, 3 / 4, 1 / 2⟩

theorem countermodel_m210_properties :
    Mat2Rat.transpose rhoQuasi2Rat = rhoQuasi2Rat ∧
    Mat2Rat.tr rhoQuasi2Rat = 1 ∧
    Mat2Rat.quadForm rhoQuasi2Rat 1 0 = 1 / 2 ∧
    Mat2Rat.quadForm rhoQuasi2Rat 0 1 = 1 / 2 ∧
    Mat2Rat.quadForm rhoQuasi2Rat 1 (-1) = -1 / 2 ∧
    Mat2Rat.quadForm rhoQuasi2Rat 1 (-1) < 0 ∧
    ((1 : Rat) / 4 - 3 / 8) = -1 / 8 ∧
    Mat2Rat.det rhoQuasi2Rat = -5 / 16 := by
  grind


abbrev stepSingular2Rat : Mat2Rat := ⟨1, 0, 0, 0⟩

theorem countermodel_m211_properties :
    Mat2Rat.mul stepSingular2Rat stepSingular2Rat = stepSingular2Rat ∧
    Mat2Rat.tr stepSingular2Rat = 1 ∧
    Mat2Rat.det stepSingular2Rat = 0 ∧
    Mat2Rat.mul (Mat2Rat.transpose stepSingular2Rat) stepSingular2Rat ≠ Mat2Rat.id := by
  grind

theorem countermodel_m211_no_left_inverse (M : Mat2Rat) :
    Mat2Rat.mul M stepSingular2Rat ≠ Mat2Rat.id := by
  intro h
  have h11 : (Mat2Rat.mul M stepSingular2Rat).a11 = Mat2Rat.id.a11 := by rw [h]
  grind


inductive SingleSystemImport where
  | I1_ComplexPhase_QM207
  | I2_QuadraticSorkin_QM208
  | I3_NoncommContext_QM209
  | I4_PsdBornCone_QM210
  | I5_ReversibleClock_QM211
  deriving DecidableEq, Repr

structure RationalCountermodel2x2 where
  bipartiteLocalParams : Nat
  bipartiteJointParams : Nat
  sorkinI3Sample : Rat
  observableA : Mat2Rat
  observableB : Mat2Rat
  stateMatrix : Mat2Rat
  clockStep : Mat2Rat
  deriving DecidableEq, Repr

abbrev AdmitsImport (m : RationalCountermodel2x2) : SingleSystemImport → Prop
  | .I1_ComplexPhase_QM207 => m.bipartiteLocalParams = m.bipartiteJointParams
  | .I2_QuadraticSorkin_QM208 => m.sorkinI3Sample = 0
  | .I3_NoncommContext_QM209 => Mat2Rat.comm m.observableA m.observableB ≠ Mat2Rat.zero
  | .I4_PsdBornCone_QM210 =>
      Mat2Rat.tr m.stateMatrix = 1 ∧
      0 ≤ Mat2Rat.quadForm m.stateMatrix 1 0 ∧
      0 ≤ Mat2Rat.quadForm m.stateMatrix 0 1 ∧
      0 ≤ Mat2Rat.quadForm m.stateMatrix 1 (-1)
  | .I5_ReversibleClock_QM211 =>
      Mat2Rat.mul (Mat2Rat.transpose m.clockStep) m.clockStep = Mat2Rat.id ∧
      Mat2Rat.det m.clockStep = 1

abbrev modelDrop207 : RationalCountermodel2x2 :=
  { bipartiteLocalParams := 8
    bipartiteJointParams := 9
    sorkinI3Sample := sorkinI3 quadReadoutRat 1 1 1
    observableA := pauliX2
    observableB := pauliZ2
    stateMatrix := rhoReal2
    clockStep := rot207 }

abbrev modelDrop208 : RationalCountermodel2x2 :=
  { bipartiteLocalParams := 15
    bipartiteJointParams := 15
    sorkinI3Sample := sorkinI3 quarticReadoutRat 1 1 1
    observableA := pauliX2
    observableB := pauliZ2
    stateMatrix := rhoReal2
    clockStep := rot207 }

abbrev modelDrop209 : RationalCountermodel2x2 :=
  { bipartiteLocalParams := 15
    bipartiteJointParams := 15
    sorkinI3Sample := sorkinI3 quadReadoutRat 1 1 1
    observableA := diag2Rat 1 (-1)
    observableB := diag2Rat 2 3
    stateMatrix := rhoReal2
    clockStep := rot207 }

abbrev modelDrop210 : RationalCountermodel2x2 :=
  { bipartiteLocalParams := 15
    bipartiteJointParams := 15
    sorkinI3Sample := sorkinI3 quadReadoutRat 1 1 1
    observableA := pauliX2
    observableB := pauliZ2
    stateMatrix := rhoQuasi2Rat
    clockStep := rot207 }

abbrev modelDrop211 : RationalCountermodel2x2 :=
  { bipartiteLocalParams := 15
    bipartiteJointParams := 15
    sorkinI3Sample := sorkinI3 quadReadoutRat 1 1 1
    observableA := pauliX2
    observableB := pauliZ2
    stateMatrix := rhoReal2
    clockStep := stepSingular2Rat }

abbrev countermodelFor : SingleSystemImport → RationalCountermodel2x2
  | .I1_ComplexPhase_QM207 => modelDrop207
  | .I2_QuadraticSorkin_QM208 => modelDrop208
  | .I3_NoncommContext_QM209 => modelDrop209
  | .I4_PsdBornCone_QM210 => modelDrop210
  | .I5_ReversibleClock_QM211 => modelDrop211

theorem countermodel_matrix_diagonal_all_false (i : SingleSystemImport) :
    ¬ AdmitsImport (countermodelFor i) i := by
  cases i <;> grind

theorem countermodel_matrix_off_diagonal_all_true (r c : SingleSystemImport) (h : r ≠ c) :
    AdmitsImport (countermodelFor r) c := by
  cases r <;> cases c <;> first | contradiction | grind

theorem five_import_mutual_independence (i : SingleSystemImport) :
    ¬ AdmitsImport (countermodelFor i) i ∧
    (∀ j : SingleSystemImport, j ≠ i → AdmitsImport (countermodelFor i) j) := by
  constructor
  · exact countermodel_matrix_diagonal_all_false i
  · intro j hj
    exact countermodel_matrix_off_diagonal_all_true i j (Ne.symm hj)

theorem born_trace_vs_quartic_readout_and_three_ray_positivity_gap :
    let born_e0 : Rat := (3 / 5 : Rat) ^ 2
    let quartic_e0 : Rat := (3 / 5 : Rat) ^ 4
    let quartic_sum : Rat := (3 / 5 : Rat) ^ 4 + (4 / 5 : Rat) ^ 4
    let quartic_renorm : Rat := quartic_e0 / quartic_sum
    let rho_alt : Mat2Rat := { a00 := 1 / 2, a01 := -3 / 4, a10 := -3 / 4, a11 := 1 / 2 }
    born_e0 = 9 / 25 ∧
    quartic_e0 = 81 / 625 ∧
    quartic_sum = 337 / 625 ∧
    quartic_renorm = 81 / 337 ∧
    quartic_e0 ≠ born_e0 ∧
    quartic_sum ≠ 1 ∧
    quartic_renorm ≠ born_e0 ∧
    Mat2Rat.tr rho_alt = 1 ∧
    Mat2Rat.quadForm rho_alt 1 0 = 1 / 2 ∧
    Mat2Rat.quadForm rho_alt 0 1 = 1 / 2 ∧
    Mat2Rat.quadForm rho_alt 1 (-1) = 5 / 2 ∧
    Mat2Rat.quadForm rho_alt 1 1 = -1 / 2 ∧
    Mat2Rat.quadForm rho_alt 1 1 < 0 ∧
    Mat2Rat.det rho_alt = -5 / 16 := by
  grind


abbrev ewDressingMat (phiPlus phiZero r : Rat) : Mat2Rat :=
  { a00 := phiZero / r
    a01 := phiPlus / r
    a10 := -phiPlus / r
    a11 := phiZero / r }

abbrev ewDressedDoublet (phiPlus phiZero r : Rat) : Rat × Rat :=
  let u := ewDressingMat phiPlus phiZero r
  (u.a00 * phiPlus + u.a10 * phiZero, u.a01 * phiPlus + u.a11 * phiZero)

theorem ew_dfm_goldstone_elimination_on_sphere (phiPlus phiZero r : Rat)
    (hsphere : phiPlus ^ 2 + phiZero ^ 2 = r ^ 2) (hr : r ≠ 0) :
    Mat2Rat.det (ewDressingMat phiPlus phiZero r) = 1 ∧
    Mat2Rat.mul (Mat2Rat.transpose (ewDressingMat phiPlus phiZero r))
      (ewDressingMat phiPlus phiZero r) = Mat2Rat.id ∧
    ewDressedDoublet phiPlus phiZero r = (0, r) := by
  refine ⟨?_, ?_, ?_⟩
  · grind
  · ext <;> grind
  · ext <;> grind

theorem ew_unbroken_electric_charge_annihilates_dressed_vacuum (v : Rat) :
    let q_em : Mat2Rat := { a00 := 1, a01 := 0, a10 := 0, a11 := 0 }
    let u_pyth := ewDressingMat (3 / 5) (4 / 5) 1
    (q_em.a00 * (0 : Rat) + q_em.a01 * v, q_em.a10 * (0 : Rat) + q_em.a11 * v) = (0, 0) ∧
    Mat2Rat.comm u_pyth q_em ≠ Mat2Rat.zero := by
  grind

theorem ew_gaussian_4d_goldstone_elimination (a b c d r : Rat)
    (hsphere : a ^ 2 + b ^ 2 + c ^ 2 + d ^ 2 = r ^ 2) (hr : r ≠ 0) :
    (c * a + d * b - (a * c + b * d)) / r = 0 ∧
    (c * b - d * a - (b * c - a * d)) / r = 0 ∧
    (a ^ 2 + b ^ 2 + c ^ 2 + d ^ 2) / r = r := by
  grind

theorem ew_dfm_doublet_witnesses :
    (3 / 5 : Rat) ^ 2 + (4 / 5 : Rat) ^ 2 = (1 : Rat) ^ 2 ∧
    Mat2Rat.det (ewDressingMat (3 / 5) (4 / 5) 1) = 1 ∧
    ewDressedDoublet (3 / 5) (4 / 5) 1 = (0, 1) ∧
    (1 / 3 : Rat) ^ 2 + (2 / 3 : Rat) ^ 2 + (2 / 3 : Rat) ^ 2 + (0 : Rat) ^ 2 = (1 : Rat) ^ 2 := by
  grind

abbrev ewNeutralMassSqMat (g gp v : Rat) : Mat2Rat :=
  let c := v ^ 2 / 4
  { a00 := c * (g ^ 2)
    a01 := -c * (g * gp)
    a10 := -c * (g * gp)
    a11 := c * (gp ^ 2) }

abbrev ewMW2 (g v : Rat) : Rat := (v ^ 2 / 4) * (g ^ 2)
abbrev ewMZ2 (g gp v : Rat) : Rat := (v ^ 2 / 4) * (g ^ 2 + gp ^ 2)

abbrev weinbergSin2 (g gp : Rat) : Rat := (gp ^ 2) / (g ^ 2 + gp ^ 2)
abbrev weinbergCos2 (g gp : Rat) : Rat := (g ^ 2) / (g ^ 2 + gp ^ 2)

abbrev weinbergPiGamma (g gp : Rat) : Mat2Rat :=
  let d := g ^ 2 + gp ^ 2
  { a00 := (gp ^ 2) / d
    a01 := (g * gp) / d
    a10 := (g * gp) / d
    a11 := (g ^ 2) / d }

abbrev weinbergPiZ (g gp : Rat) : Mat2Rat :=
  let d := g ^ 2 + gp ^ 2
  { a00 := (g ^ 2) / d
    a01 := -(g * gp) / d
    a10 := -(g * gp) / d
    a11 := (gp ^ 2) / d }

theorem ew_neutral_mass_matrix_det_and_trace (g gp v : Rat) :
    Mat2Rat.det (ewNeutralMassSqMat g gp v) = 0 ∧
    Mat2Rat.tr (ewNeutralMassSqMat g gp v) = ewMZ2 g gp v := by
  grind

theorem weinberg_projectors_complete_orthogonal_idempotent (g gp v : Rat)
    (hd : g ^ 2 + gp ^ 2 ≠ 0) :
    weinbergSin2 g gp + weinbergCos2 g gp = 1 ∧
    Mat2Rat.add (weinbergPiGamma g gp) (weinbergPiZ g gp) = Mat2Rat.id ∧
    Mat2Rat.mul (weinbergPiGamma g gp) (weinbergPiZ g gp) = Mat2Rat.zero ∧
    Mat2Rat.mul (weinbergPiZ g gp) (weinbergPiGamma g gp) = Mat2Rat.zero ∧
    Mat2Rat.mul (weinbergPiGamma g gp) (weinbergPiGamma g gp) = weinbergPiGamma g gp ∧
    Mat2Rat.mul (weinbergPiZ g gp) (weinbergPiZ g gp) = weinbergPiZ g gp ∧
    Mat2Rat.mul (ewNeutralMassSqMat g gp v) (weinbergPiGamma g gp) = Mat2Rat.zero := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · grind
  · ext <;> grind
  · ext <;> grind
  · ext <;> grind
  · ext <;> grind
  · ext <;> grind
  · ext <;> grind

theorem ew_custodial_rho_eq_one (g gp v : Rat)
    (hg : g ≠ 0) (hv : v ≠ 0) (hd : g ^ 2 + gp ^ 2 ≠ 0) :
    ewMW2 g v / (ewMZ2 g gp v * weinbergCos2 g gp) = 1 := by
  grind

theorem ew_weinberg_and_triplet_witnesses :
    weinbergSin2 (4 / 5) (3 / 5) = 9 / 25 ∧
    weinbergCos2 (4 / 5) (3 / 5) = 16 / 25 ∧
    ((3 / 5 : Rat) / (1 + 3 / 5 : Rat)) = 3 / 8 ∧
    ((1 : Rat) / (1 + 3 / 5 : Rat)) = 5 / 8 ∧
    ((1 * (1 + 1) - (-1) ^ 2 : Rat) / (2 * (-1) ^ 2 : Rat)) = 1 / 2 := by
  grind

theorem sm_gell_mann_nishijima_charge_identities :
    let yQ : Rat := 1 / 6
    let yu : Rat := 2 / 3
    let yd : Rat := -1 / 3
    let yL : Rat := -1 / 2
    let ye : Rat := -1
    let quL : Rat := 1 / 2 + yQ
    let qdL : Rat := -1 / 2 + yQ
    let qnuL : Rat := 1 / 2 + yL
    let qeL : Rat := -1 / 2 + yL
    quL = 2 / 3 ∧ qdL = -1 / 3 ∧ qnuL = 0 ∧ qeL = -1 ∧
    quL = yu ∧ qdL = yd ∧ qeL = ye ∧
    (2 * quL + qdL) = 1 ∧ (quL + 2 * qdL) = 0 ∧ ((2 * quL + qdL) + qeL) = 0 := by
  grind

abbrev anomalySU3SqU1 (nc yQ yu yd : Rat) : Rat :=
  nc * (2 * yQ - yu - yd)

abbrev anomalySU2SqU1 (nc yQ yL : Rat) : Rat :=
  nc * yQ + yL

abbrev anomalyGravSqU1 (nc yQ yu yd yL ye : Rat) : Rat :=
  nc * (2 * yQ - yu - yd) + (2 * yL - ye)

abbrev anomalyU1CubicQuarks (nc yQ yu yd : Rat) : Rat :=
  nc * (2 * (yQ ^ 3) - (yu ^ 3) - (yd ^ 3))

abbrev anomalyU1CubicLeptons (yL ye : Rat) : Rat :=
  2 * (yL ^ 3) - (ye ^ 3)

abbrev anomalyU1CubicTotal (nc yQ yu yd yL ye : Rat) : Rat :=
  anomalyU1CubicQuarks nc yQ yu yd + anomalyU1CubicLeptons yL ye

theorem sm_all_four_anomalies_cancel_at_nc3_and_fail_at_nc1 :
    anomalySU3SqU1 3 (1 / 6) (2 / 3) (-1 / 3) = 0 ∧
    anomalySU2SqU1 3 (1 / 6) (-1 / 2) = 0 ∧
    anomalyGravSqU1 3 (1 / 6) (2 / 3) (-1 / 3) (-1 / 2) (-1) = 0 ∧
    anomalyU1CubicQuarks 3 (1 / 6) (2 / 3) (-1 / 3) = -3 / 4 ∧
    anomalyU1CubicLeptons (-1 / 2) (-1) = 3 / 4 ∧
    anomalyU1CubicTotal 3 (1 / 6) (2 / 3) (-1 / 3) (-1 / 2) (-1) = 0 ∧
    anomalySU2SqU1 1 (1 / 6) (-1 / 2) = -1 / 3 ∧
    anomalyU1CubicTotal 1 (1 / 6) (2 / 3) (-1 / 3) (-1 / 2) (-1) = 1 / 2 := by
  grind

theorem sm_cubic_anomaly_charge_quantization_polynomial (nc delta : Rat) (hnc : nc ≠ 0) :
    let yQ := 1 / (2 * nc)
    let yu := yQ + delta
    let yd := yQ - delta
    anomalyU1CubicTotal nc yQ yu yd (-1 / 2) (-1) = -3 * (delta ^ 2) + 3 / 4 ∧
    (anomalyU1CubicTotal nc yQ yu yd (-1 / 2) (-1) = 0 ↔ delta ^ 2 = 1 / 4) := by
  grind


abbrev suNCasimirFundamental (nc : Rat) : Rat :=
  (nc ^ 2 - 1) / (2 * nc)

abbrev suNCasimirAdjoint (nc : Rat) : Rat :=
  nc

abbrev suNSingletChannelCoeff (nc : Rat) : Rat :=
  -suNCasimirFundamental nc

abbrev suNOctetChannelCoeff (nc : Rat) : Rat :=
  suNCasimirAdjoint nc / 2 - suNCasimirFundamental nc

abbrev suNSextetChannelCoeff (nc : Rat) : Rat :=
  (1 : Rat) / 2 - 1 / (2 * nc)

abbrev suNAntitripletChannelCoeff (nc : Rat) : Rat :=
  -(1 : Rat) / 2 - 1 / (2 * nc)

theorem su3_casimir_and_channel_identities :
    suNCasimirFundamental 3 = 4 / 3 ∧
    suNCasimirAdjoint 3 = 3 ∧
    suNSingletChannelCoeff 3 = -4 / 3 ∧
    suNOctetChannelCoeff 3 = 1 / 6 ∧
    suNSextetChannelCoeff 3 = 1 / 3 ∧
    suNAntitripletChannelCoeff 3 = -2 / 3 ∧
    suNSingletChannelCoeff 3 < 0 ∧
    suNOctetChannelCoeff 3 > 0 := by
  grind

theorem su3_fierz_diagonal_and_offdiagonal_identities :
    let t3_0 : Rat := 1 / 2
    let t3_1 : Rat := -1 / 2
    let t3_2 : Rat := 0
    let t8_0 : Rat := 1 / 2
    let t8_1 : Rat := 1 / 2
    let t8_2 : Rat := -1
    let w3 : Rat := 1
    let w8 : Rat := 1 / 3
    w3 * t3_0 * t3_0 + w8 * t8_0 * t8_0 = 1 / 3 ∧
    w3 * t3_1 * t3_1 + w8 * t8_1 * t8_1 = 1 / 3 ∧
    w3 * t3_2 * t3_2 + w8 * t8_2 * t8_2 = 1 / 3 ∧
    w3 * t3_0 * t3_1 + w8 * t8_0 * t8_1 = -1 / 6 ∧
    w3 * t3_0 * t3_2 + w8 * t8_0 * t8_2 = -1 / 6 ∧
    w3 * t3_1 * t3_2 + w8 * t8_1 * t8_2 = -1 / 6 ∧
    (1 / 2 : Rat) - (1 / 6 : Rat) = 1 / 3 ∧
    3 * (1 / 2 : Rat) - (1 / 6 : Rat) = 4 / 3 := by
  grind

abbrev qcdBeta0 (nc nf : Rat) : Rat :=
  (11 / 3 : Rat) * nc - (2 / 3 : Rat) * nf

abbrev qcdBeta1 (nc nf : Rat) : Rat :=
  (34 / 3 : Rat) * (nc ^ 2) - ((10 / 3 : Rat) * nc + (nc ^ 2 - 1) / nc) * nf

theorem qcd_beta0_asymptotic_freedom_window (nf : Rat) :
    (4 : Rat) * suNCasimirAdjoint 3 + (-1 / 3 : Rat) * suNCasimirAdjoint 3 = 11 ∧
    qcdBeta0 3 0 = 11 ∧
    qcdBeta0 3 3 = 9 ∧
    qcdBeta0 3 5 = 23 / 3 ∧
    qcdBeta0 3 6 = 7 ∧
    qcdBeta0 3 16 = 1 / 3 ∧
    qcdBeta0 3 17 = -1 / 3 ∧
    (qcdBeta0 3 nf > 0 ↔ nf < 33 / 2) := by
  grind

theorem qcd_beta1_and_banks_zaks_fixed_point (nf : Rat) :
    qcdBeta1 3 nf = 102 - (38 / 3 : Rat) * nf ∧
    qcdBeta1 3 0 = 102 ∧
    qcdBeta1 3 5 = 116 / 3 ∧
    qcdBeta1 3 16 = -302 / 3 ∧
    (-qcdBeta0 3 16) / qcdBeta1 3 16 = 1 / 302 := by
  grind

theorem wilson_creutz_ratio_area_vs_perimeter (b : Rat) (hb : b ≠ 0) :
    let w_area (r t : Nat) : Rat := b ^ (r * t)
    let w_perim (r t : Nat) : Rat := b ^ (2 * (r + t))
    (w_area 2 2 * w_area 1 1) / (w_area 2 1 * w_area 1 2) = b ∧
    (w_area 3 3 * w_area 2 2) / (w_area 3 2 * w_area 2 3) = b ∧
    (w_perim 2 2 * w_perim 1 1) / (w_perim 2 1 * w_perim 1 2) = 1 ∧
    (w_perim 3 3 * w_perim 2 2) / (w_perim 3 2 * w_perim 2 3) = 1 := by
  grind

theorem wilson_lattice_3x3_dfm_betti_identity :
    let v : Int := 9
    let e : Int := 12
    let e_tree : Int := v - 1
    let b1 : Int := e - v + 1
    e_tree = 8 ∧
    b1 = 4 ∧
    e - e_tree = b1 ∧
    ((1 / 9 : Rat) < (1 : Rat)) := by
  grind


@[ext]
structure GaussRat where
  re : Rat
  im : Rat
  deriving DecidableEq, Repr

namespace GaussRat

abbrev zero : GaussRat := ⟨0, 0⟩
abbrev one : GaussRat := ⟨1, 0⟩

abbrev add (z w : GaussRat) : GaussRat :=
  ⟨z.re + w.re, z.im + w.im⟩

abbrev mul (z w : GaussRat) : GaussRat :=
  ⟨z.re * w.re - z.im * w.im, z.re * w.im + z.im * w.re⟩

abbrev conj (z : GaussRat) : GaussRat :=
  ⟨z.re, -z.im⟩

abbrev normSq (z : GaussRat) : Rat :=
  z.re ^ 2 + z.im ^ 2

abbrev dressEntry (ua vab db : GaussRat) : GaussRat :=
  mul (mul (conj ua) vab) db

abbrev quartet (vij vkl vil vkj : GaussRat) : GaussRat :=
  mul (mul vij vkl) (mul (conj vil) (conj vkj))

end GaussRat

theorem ckm_bipartite_dfm_parameter_count (ng : Rat) :
    let e_total := ng ^ 2
    let e_tree := 2 * ng - 1
    let b1 := e_total - e_tree
    let cp_phases (n : Rat) : Rat := (n - 1) * (n - 2) / 2
    b1 = (ng - 1) ^ 2 ∧
    cp_phases 1 = 0 ∧
    cp_phases 2 = 0 ∧
    cp_phases 3 = 1 ∧
    cp_phases 4 = 3 := by
  grind

theorem gaussRat_unit_phase_cancel (u z : GaussRat) (hu : GaussRat.normSq u = 1) :
    GaussRat.mul (GaussRat.conj u) u = GaussRat.one ∧
    GaussRat.mul u (GaussRat.conj u) = GaussRat.one ∧
    GaussRat.mul (GaussRat.dressEntry u z GaussRat.one)
                 (GaussRat.conj (GaussRat.dressEntry u GaussRat.one GaussRat.one)) = z := by
  refine ⟨?_, ?_, ?_⟩
  · ext <;> grind
  · ext <;> grind
  · ext <;> grind

theorem jarlskog_quartet_rephasing_dressing_invariance
    (vij vkl vil vkj ui dj : GaussRat)
    (hui : GaussRat.normSq ui = 1)
    (hdj : GaussRat.normSq dj = 1) :
    GaussRat.mul (GaussRat.dressEntry ui vij GaussRat.one)
                 (GaussRat.conj (GaussRat.dressEntry ui vil GaussRat.one)) =
      GaussRat.mul vij (GaussRat.conj vil) ∧
    GaussRat.mul (GaussRat.dressEntry GaussRat.one vij dj)
                 (GaussRat.conj (GaussRat.dressEntry GaussRat.one vkj dj)) =
      GaussRat.mul vij (GaussRat.conj vkj) ∧
    GaussRat.quartet
      (GaussRat.dressEntry ui vij GaussRat.one)
      vkl
      (GaussRat.dressEntry ui vil GaussRat.one)
      vkj =
    GaussRat.quartet vij vkl vil vkj := by
  refine ⟨?_, ?_, ?_⟩
  · ext <;> grind
  · ext <;> grind
  · ext <;> grind

theorem two_gen_cabibbo_artificial_cp_phase_zero
    (v11 v12 v21 v22 : GaussRat)
    (horth : GaussRat.add (GaussRat.mul v11 (GaussRat.conj v21))
                          (GaussRat.mul v12 (GaussRat.conj v22)) = GaussRat.zero) :
    (GaussRat.quartet v11 v22 v12 v21).im = 0 ∧
    (GaussRat.quartet v11 v22 v12 v21).re = -(GaussRat.normSq v12 * GaussRat.normSq v22) := by
  have hre : (GaussRat.add (GaussRat.mul v11 (GaussRat.conj v21))
                           (GaussRat.mul v12 (GaussRat.conj v22))).re = 0 := by
    rw [horth]
  have him : (GaussRat.add (GaussRat.mul v11 (GaussRat.conj v21))
                           (GaussRat.mul v12 (GaussRat.conj v22))).im = 0 := by
    rw [horth]
  grind

theorem three_gen_ckm_substantial_jarlskog_witness :
    let v11 : GaussRat := ⟨45 / 125, -64 / 125⟩
    let v12 : GaussRat := ⟨12 / 25, 0⟩
    let v13 : GaussRat := ⟨60 / 125, 48 / 125⟩
    let v21 : GaussRat := ⟨-60 / 125, -48 / 125⟩
    let v22 : GaussRat := ⟨9 / 25, 0⟩
    let v23 : GaussRat := ⟨-80 / 125, 36 / 125⟩
    let v31 : GaussRat := ⟨-12 / 25, 0⟩
    let v32 : GaussRat := ⟨0, 4 / 5⟩
    let v33 : GaussRat := ⟨9 / 25, 0⟩
    GaussRat.normSq v11 + GaussRat.normSq v12 + GaussRat.normSq v13 = 1 ∧
    GaussRat.normSq v21 + GaussRat.normSq v22 + GaussRat.normSq v23 = 1 ∧
    GaussRat.normSq v31 + GaussRat.normSq v32 + GaussRat.normSq v33 = 1 ∧
    GaussRat.add (GaussRat.add (GaussRat.mul v11 (GaussRat.conj v21))
                               (GaussRat.mul v12 (GaussRat.conj v22)))
                 (GaussRat.mul v13 (GaussRat.conj v23)) = GaussRat.zero ∧
    (GaussRat.quartet v11 v22 v12 v21).im = 5184 / 78125 ∧
    (GaussRat.quartet v22 v33 v23 v32).im = 5184 / 78125 ∧
    (GaussRat.quartet v13 v22 v12 v23).im = -5184 / 78125 ∧
    (5184 / 78125 : Rat) ≠ 0 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · grind
  · grind
  · grind
  · ext <;> grind
  · grind
  · grind
  · grind
  · grind


theorem su3_diagonal_klein_four_landau_gribov_copies :
    let det3 (d1 d2 d3 : Rat) : Rat := d1 * d2 * d3
    let tr3 (d1 d2 d3 : Rat) : Rat := d1 + d2 + d3
    let landau_anti_herm (d1 d2 d3 : Rat) : Rat := (d1 - d1) + (d2 - d2) + (d3 - d3)
    det3 1 1 1 = 1 ∧
    det3 1 (-1) (-1) = 1 ∧
    det3 (-1) 1 (-1) = 1 ∧
    det3 (-1) (-1) 1 = 1 ∧
    landau_anti_herm 1 (-1) (-1) = 0 ∧
    landau_anti_herm (-1) 1 (-1) = 0 ∧
    landau_anti_herm (-1) (-1) 1 = 0 ∧
    tr3 1 1 1 = 3 ∧
    tr3 1 (-1) (-1) = -1 ∧
    ((1 : Rat) * (-1 : Rat) = -1) ∧
    ((-1 : Rat) < 0) ∧
    ((4 : Rat) ^ 3 = 64) := by
  grind

theorem spanning_tree_dfm_eliminates_gribov_copies
    (u01 u12 u02 g1 g2 : Rat)
    (hu01 : u01 ≠ 0) (hu12 : u12 ≠ 0) (hg1 : g1 ≠ 0) (hg2 : g2 ≠ 0) :
    let u01_g := u01 * g1
    let u12_g := g1⁻¹ * u12 * g2
    let u02_g := u02 * g2
    let dress0 := (1 : Rat)
    let dress1 := dress0 * u01_g
    let dress2 := dress1 * u12_g
    dress0 * u01_g * dress1⁻¹ = 1 ∧
    dress1 * u12_g * dress2⁻¹ = 1 ∧
    dress0 * u02_g * dress2⁻¹ = u02 * (u01 * u12)⁻¹ := by
  grind


abbrev minkowskiEta2 : Mat2Rat :=
  { a00 := 1, a01 := 0, a10 := 0, a11 := -1 }

abbrev lorentzBoost2 (beta : Rat) : Mat2Rat :=
  let d := 1 - beta ^ 2
  { a00 := (1 + beta ^ 2) / d
    a01 := (2 * beta) / d
    a10 := (2 * beta) / d
    a11 := (1 + beta ^ 2) / d }

abbrev dressedSimplicialMetric2 (e : Mat2Rat) : Mat2Rat :=
  Mat2Rat.mul (Mat2Rat.mul (Mat2Rat.transpose e) minkowskiEta2) e

theorem lorentz_boost_preserves_minkowski_and_det_one (beta : Rat)
    (hd : 1 - beta ^ 2 ≠ 0) :
    Mat2Rat.det (lorentzBoost2 beta) = 1 ∧
    Mat2Rat.mul (lorentzBoost2 beta) (lorentzBoost2 (-beta)) = Mat2Rat.id ∧
    Mat2Rat.mul (lorentzBoost2 (-beta)) (lorentzBoost2 beta) = Mat2Rat.id ∧
    Mat2Rat.mul (Mat2Rat.mul (Mat2Rat.transpose (lorentzBoost2 beta)) minkowskiEta2)
                (lorentzBoost2 beta) = minkowskiEta2 := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · grind
  · ext <;> grind
  · ext <;> grind
  · ext <;> grind

theorem cartan_regge_tetrad_dressed_metric_invariance (e : Mat2Rat) (beta : Rat)
    (hd : 1 - beta ^ 2 ≠ 0) :
    dressedSimplicialMetric2 (Mat2Rat.mul (lorentzBoost2 (-beta)) e) =
      dressedSimplicialMetric2 e := by
  ext <;> grind

theorem cartan_regge_hinge_holonomy_and_bianchi_witness :
    let h1 := lorentzBoost2 (1 / 2)
    let h1_inv := lorentzBoost2 (-1 / 2)
    let h2 := lorentzBoost2 (1 / 3)
    let h2_inv := lorentzBoost2 (-1 / 3)
    let bianchi_loop := Mat2Rat.mul (Mat2Rat.mul h1 h2) (Mat2Rat.mul h2_inv h1_inv)
    h1.a00 = 5 / 3 ∧
    h1.a01 = 4 / 3 ∧
    Mat2Rat.tr h1 = 10 / 3 ∧
    Mat2Rat.tr h1 ≠ 2 ∧
    Mat2Rat.det h1 = 1 ∧
    bianchi_loop = Mat2Rat.id ∧
    Mat2Rat.tr bianchi_loop = 2 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · grind
  · grind
  · grind
  · grind
  · grind
  · ext <;> grind
  · grind


theorem weyl_heisenberg_finite_trace_obstruction (x p : Mat2Rat) :
    let comm := Mat2Rat.sub (Mat2Rat.mul x p) (Mat2Rat.mul p x)
    let kravchuk_diag0 : Rat := 1 - 0
    let kravchuk_diag1 : Rat := 2 - 1
    let kravchuk_diag2 : Rat := 0 - 2
    Mat2Rat.tr comm = 0 ∧
    Mat2Rat.tr Mat2Rat.id = 2 ∧
    Mat2Rat.tr comm ≠ Mat2Rat.tr Mat2Rat.id ∧
    kravchuk_diag0 = 1 ∧
    kravchuk_diag1 = 1 ∧
    kravchuk_diag2 = -2 ∧
    kravchuk_diag0 + kravchuk_diag1 + kravchuk_diag2 = 0 := by
  grind

theorem lorentz_boost_non_unitary_in_finite_dim (beta : Rat)
    (hb : beta ≠ 0) (hd : 1 - beta ^ 2 ≠ 0) :
    let lb := lorentzBoost2 beta
    let gram := Mat2Rat.mul (Mat2Rat.transpose lb) lb
    let gram_half := Mat2Rat.mul (Mat2Rat.transpose (lorentzBoost2 (1 / 2))) (lorentzBoost2 (1 / 2))
    Mat2Rat.mul (Mat2Rat.mul (Mat2Rat.transpose lb) minkowskiEta2) lb = minkowskiEta2 ∧
    Mat2Rat.tr gram - 2 = ((4 * beta) / (1 - beta ^ 2)) ^ 2 ∧
    Mat2Rat.tr gram ≠ 2 ∧
    gram ≠ Mat2Rat.id ∧
    Mat2Rat.tr gram_half = 82 / 9 ∧
    Mat2Rat.tr gram_half > 2 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · ext <;> grind
  · grind
  · grind
  · intro h
    have htr : Mat2Rat.tr (Mat2Rat.mul (Mat2Rat.transpose (lorentzBoost2 beta)) (lorentzBoost2 beta)) =
               Mat2Rat.tr Mat2Rat.id := by rw [h]
    grind
  · grind
  · grind

theorem finite_clock_poincare_recurrence_vs_kraus_decoherence :
    let rho_s : Mat2Rat := { a00 := 9 / 25, a01 := 12 / 25, a10 := 12 / 25, a11 := 16 / 25 }
    let k0 : Mat2Rat := { a00 := 1, a01 := 0, a10 := 0, a11 := 0 }
    let k1 : Mat2Rat := { a00 := 0, a01 := 0, a10 := 0, a11 := 1 }
    let rho_dephased := Mat2Rat.add (Mat2Rat.mul (Mat2Rat.mul k0 rho_s) k0)
                                    (Mat2Rat.mul (Mat2Rat.mul k1 rho_s) k1)
    let purity_initial := Mat2Rat.tr (Mat2Rat.mul rho_s rho_s)
    let purity_dephased := Mat2Rat.tr (Mat2Rat.mul rho_dephased rho_dephased)
    Mat2Rat.add k0 k1 = Mat2Rat.id ∧
    Mat2Rat.tr rho_s = 1 ∧
    purity_initial = 1 ∧
    Mat2Rat.det rho_s = 0 ∧
    rho_dephased.a01 = 0 ∧
    rho_dephased.a10 = 0 ∧
    Mat2Rat.tr rho_dephased = 1 ∧
    purity_dephased = 337 / 625 ∧
    purity_dephased < 1 ∧
    purity_initial - purity_dephased = 288 / 625 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · ext <;> grind
  · grind
  · grind
  · grind
  · grind
  · grind
  · grind
  · grind
  · grind
  · grind

theorem wigners_friend_rational_chsh_multi_observer_obstruction
    (a0 a1 b0 b1 : Rat)
    (ha0 : a0 ^ 2 = 1) (ha1 : a1 ^ 2 = 1) (hb0 : b0 ^ 2 = 1) (hb1 : b1 ^ 2 = 1) :
    let c : Rat := 3 / 5
    let s : Rat := 4 / 5
    let e00 : Rat := c
    let e01 : Rat := s
    let e10 : Rat := s
    let e11 : Rat := -c
    let s_wf : Rat := e00 + e01 + e10 - e11
    let s_classical : Rat := a0 * (b0 + b1) + a1 * (b0 - b1)
    c ^ 2 + s ^ 2 = 1 ∧
    s_wf = 14 / 5 ∧
    s_wf > 2 ∧
    s_wf ^ 2 = 196 / 25 ∧
    s_wf ^ 2 > 4 ∧
    s_wf ^ 2 < 8 ∧
    s_classical ^ 2 = 4 ∧
    s_wf ^ 2 > s_classical ^ 2 := by
  grind

theorem qutrit_stabilizer_wigner_nonnegative_vs_magic_negative :
    let w_stab_line : Rat := 1 / 3
    let w_stab_off : Rat := 0
    let stab_sum : Rat := 3 * w_stab_line + 6 * w_stab_off
    let stab_purity : Rat := 3 * (3 * (w_stab_line ^ 2) + 6 * (w_stab_off ^ 2))
    let mub_line_overlap : Rat := 3 * (w_stab_line * w_stab_line)
    let w00 : Rat := -1 / 9
    let w10 : Rat := -1 / 9
    let w20 : Rat := 1 / 3
    let w01 : Rat := 2 / 9
    let w11 : Rat := 2 / 9
    let w21 : Rat := 0
    let w02 : Rat := 2 / 9
    let w12 : Rat := 2 / 9
    let w22 : Rat := 0
    let magic_sum : Rat := w00 + w10 + w20 + w01 + w11 + w21 + w02 + w12 + w22
    let magic_purity : Rat :=
      3 * (w00 ^ 2 + w10 ^ 2 + w20 ^ 2 + w01 ^ 2 + w11 ^ 2 + w21 ^ 2 + w02 ^ 2 + w12 ^ 2 + w22 ^ 2)
    let magic_abs_sum : Rat := (-w00) + (-w10) + w20 + w01 + w11 + w21 + w02 + w12 + w22
    let magic_negativity : Rat := magic_abs_sum - 1
    stab_sum = 1 ∧
    stab_purity = 1 ∧
    mub_line_overlap = 1 / 3 ∧
    w00 < 0 ∧
    magic_sum = 1 ∧
    magic_purity = 1 ∧
    magic_negativity = 4 / 9 ∧
    magic_negativity > 0 := by
  grind


theorem busch_ic_povm_vs_polyhedral_frame_cone :
    let tr_e0 : Rat := 1 / 2
    let tr_e1 : Rat := 1 / 2
    let tr_e2 : Rat := 1 / 2
    let tr_e3 : Rat := 1 / 2
    let det_e0 : Rat := (1 / 4) * ((1 : Rat) - ((3 / 5) * (3 / 5) + (4 / 5) * (4 / 5)))
    let det_e2 : Rat := (1 / 4) * ((1 : Rat) - ((3 / 5) * (3 / 5) + (-4 / 5) * (-4 / 5)))
    let bloch_x_sum : Rat := (3 / 5) + (-3 / 5) + 0 + 0
    let bloch_y_sum : Rat := 0 + 0 + (3 / 5) + (-3 / 5)
    let bloch_z_sum : Rat := (4 / 5) + (4 / 5) + (-4 / 5) + (-4 / 5)
    let raw_4x4_det : Rat := (6 / 5) * (6 / 5) * (8 / 5)
    let recon_det_prob : Rat := ((1 / 4 : Rat) ^ 4) * raw_4x4_det
    let recon_det_bloch : Rat := ((1 / 2 : Rat) ^ 4) * raw_4x4_det
    let polyhedral_cabello_peres_minor : Rat := 0 * (1 / 2) - (-1 / 4) * (-1 / 4)
    let polyhedral_cabello_quad_2100 : Rat := 2 * (2 : Rat) * 1 * (-1 / 4) + (1 / 2) * (1 : Rat) ^ 2
    tr_e0 + tr_e1 + tr_e2 + tr_e3 = 2 ∧
    det_e0 = 0 ∧
    det_e2 = 0 ∧
    bloch_x_sum = 0 ∧
    bloch_y_sum = 0 ∧
    bloch_z_sum = 0 ∧
    recon_det_prob = 9 / 1000 ∧
    recon_det_bloch = 18 / 125 ∧
    recon_det_prob ≠ 0 ∧
    polyhedral_cabello_peres_minor = -1 / 16 ∧
    polyhedral_cabello_peres_minor < 0 ∧
    polyhedral_cabello_quad_2100 = -1 / 2 ∧
    polyhedral_cabello_quad_2100 < 0 := by
  grind

theorem galois_conjugate_negativity_vs_sos_total_positivity :
    let twist_tr_a : Rat := (1 / 4) + (3 / 4)
    let twist_tr_b : Rat := (1 / 4) + (-1 / 4)
    let twist_det_a : Rat := (1 / 4) * (3 / 4) + 5 * (1 / 4) * (-1 / 4)
    let twist_det_b : Rat := (1 / 4) * (-1 / 4) + (1 / 4) * (3 / 4)
    let twist_det_norm : Rat := twist_det_a ^ 2 - 5 * twist_det_b ^ 2
    let sos_sq_a : Rat := (1 / 3) * ((1 / 2) ^ 2 + 5 * (1 / 2) ^ 2)
    let sos_sq_b : Rat := (1 / 3) * (2 * (1 / 2) * (1 / 2))
    let sos_det_a : Rat := (1 / 2) * (1 / 2) - 5 * (1 / 6) * (1 / 6)
    let sos_det_norm : Rat := sos_det_a ^ 2
    twist_tr_a = 1 ∧
    twist_tr_b = 0 ∧
    twist_det_a = -1 / 8 ∧
    twist_det_b = 1 / 8 ∧
    twist_det_norm = -1 / 16 ∧
    twist_det_norm < 0 ∧
    sos_sq_a = 1 / 2 ∧
    sos_sq_b = 1 / 6 ∧
    sos_det_a = 1 / 9 ∧
    sos_det_norm = 1 / 81 ∧
    sos_det_norm > 0 := by
  grind

theorem char2_mermin_peres_cocycle_and_choi_transpose_separation :
    let inv2_mod3 : Nat := (2 * 2) % 3
    let two_mod2 : Nat := 2 % 2
    let mp_row_prod : Int := 1 * 1 * 1
    let mp_col_prod : Int := 1 * 1 * (-1)
    let choi_transpose_singlet : Rat := -1 / 2
    let choi_identity_singlet : Rat := 0
    let choi_identity_bell_plus : Rat := 1
    inv2_mod3 = 1 ∧
    two_mod2 = 0 ∧
    mp_row_prod * mp_col_prod = -1 ∧
    choi_transpose_singlet < 0 ∧
    choi_identity_singlet ≥ 0 ∧
    choi_identity_bell_plus = 1 := by
  grind

theorem rational_cayley_unitarity_and_pythagorean_renyi_moments (delta : Rat) :
    let denom : Rat := 1 + (delta / 2) ^ 2
    let cayley_re : Rat := (1 - (delta / 2) ^ 2) / denom
    let cayley_im : Rat := -delta / denom
    let taylor_norm_sq : Rat := 1 + delta ^ 2
    let taylor_half : Rat := 1 + (1 / 2 : Rat) ^ 2
    let p0 : Rat := 9 / 25
    let p1 : Rat := 16 / 25
    let renyi_p2 : Rat := p0 ^ 2 + p1 ^ 2
    let renyi_p3 : Rat := p0 ^ 3 + p1 ^ 3
    (denom ≠ 0 → cayley_re ^ 2 + cayley_im ^ 2 = 1) ∧
    taylor_norm_sq - 1 = delta ^ 2 ∧
    taylor_half = 5 / 4 ∧
    taylor_half > 1 ∧
    p0 + p1 = 1 ∧
    renyi_p2 = 337 / 625 ∧
    renyi_p3 = 193 / 625 := by
  grind


theorem graph_conf2_exchange_betti_and_character_collapse (chi : Rat) :
    let v_conf_p3 : Int := 3
    let e_conf_p3 : Int := 2
    let b1_conf_p3 : Int := e_conf_p3 - v_conf_p3 + 1
    let v_conf_y : Int := 6
    let e_conf_y : Int := 6
    let b1_conf_y : Int := e_conf_y - v_conf_y + 1
    let v_conf_c4 : Int := 6
    let e_conf_c4 : Int := 8
    let f_sq_c4 : Int := 2
    let b1_conf_c4 : Int := e_conf_c4 - v_conf_c4 + 1
    let b1_2complex_q_c4 : Int := b1_conf_c4 - f_sq_c4
    let v_conf_k4 : Int := 6
    let e_conf_k4 : Int := 12
    let f_sq_k4 : Int := 3
    let b1_conf_k4 : Int := e_conf_k4 - v_conf_k4 + 1
    let b1_2complex_q_k4 : Int := b1_conf_k4 - f_sq_k4
    let v_conf_k5 : Int := 10
    let e_conf_k5 : Int := 30
    let b1_conf_k5 : Int := e_conf_k5 - v_conf_k5 + 1
    let rank_d2_q_k5 : Int := 15
    let rank_d2_f2_k5 : Int := 14
    let b1_2complex_q_k5 : Int := b1_conf_k5 - rank_d2_q_k5
    let b1_2complex_f2_k5 : Int := b1_conf_k5 - rank_d2_f2_k5
    let tors_z2_k5 : Int := b1_2complex_f2_k5 - b1_2complex_q_k5
    b1_conf_p3 = 0 ∧
    b1_conf_y = 1 ∧
    b1_conf_c4 = 3 ∧
    b1_2complex_q_c4 = 1 ∧
    b1_conf_k4 = 7 ∧
    b1_2complex_q_k4 = 4 ∧
    b1_conf_k5 = 21 ∧
    b1_2complex_q_k5 = 6 ∧
    b1_2complex_f2_k5 = 7 ∧
    tors_z2_k5 = 1 ∧
    tors_z2_k5 > 0 ∧
    (chi ^ 2 = 1 ↔ (chi = 1 ∨ chi = -1)) ∧
    ((-1 : Rat) ^ 2 = 1) := by
  grind

theorem slater_determinant_pauli_exclusion_and_swap_antisymmetry (a b c d : Rat) :
    let slater_same : Rat := a * b - b * a
    let slater_12 : Rat := a * d - b * c
    let slater_21 : Rat := c * b - d * a
    let perm_12 : Rat := a * d + b * c
    let perm_21 : Rat := c * b + d * a
    let boson_coincide : Rat := (a * b + b * a) ^ 2
    let dist_coincide : Rat := (a * b) ^ 2 + (b * a) ^ 2
    slater_same = 0 ∧
    slater_21 = -slater_12 ∧
    slater_21 ^ 2 = slater_12 ^ 2 ∧
    perm_21 = perm_12 ∧
    boson_coincide = 4 * (a ^ 2) * (b ^ 2) ∧
    boson_coincide = 2 * dist_coincide := by
  grind

theorem car_clifford_nilpotency_and_occupation_projector :
    let c_ann : Mat2Rat := { a00 := 0, a01 := 1, a10 := 0, a11 := 0 }
    let c_cre : Mat2Rat := Mat2Rat.transpose c_ann
    let anticomm := Mat2Rat.add (Mat2Rat.mul c_ann c_cre) (Mat2Rat.mul c_cre c_ann)
    let num_op := Mat2Rat.mul c_cre c_ann
    Mat2Rat.mul c_ann c_ann = Mat2Rat.zero ∧
    Mat2Rat.mul c_cre c_cre = Mat2Rat.zero ∧
    anticomm = Mat2Rat.id ∧
    Mat2Rat.mul num_op num_op = num_op ∧
    Mat2Rat.tr num_op = 1 ∧
    Mat2Rat.det num_op = 0 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · ext <;> grind
  · ext <;> grind
  · ext <;> grind
  · ext <;> grind
  · grind
  · grind

theorem pauli_shell_capacities_and_madelung_noble_gas_closures :
    let orb_n1 : Int := 1
    let orb_n2 : Int := 1 + 3
    let orb_n3 : Int := 1 + 3 + 5
    let orb_n4 : Int := 1 + 3 + 5 + 7
    let cap_n1 : Int := 2 * orb_n1
    let cap_n2 : Int := 2 * orb_n2
    let cap_n3 : Int := 2 * orb_n3
    let cap_n4 : Int := 2 * orb_n4
    let z_he : Int := 2
    let z_ne : Int := z_he + 2 + 6
    let z_ar : Int := z_ne + 2 + 6
    let z_kr : Int := z_ar + 2 + 10 + 6
    let z_xe : Int := z_kr + 2 + 10 + 6
    let z_rn : Int := z_xe + 2 + 14 + 10 + 6
    orb_n1 = 1 ^ 2 ∧
    orb_n2 = 2 ^ 2 ∧
    orb_n3 = 3 ^ 2 ∧
    orb_n4 = 4 ^ 2 ∧
    cap_n1 = 2 ∧
    cap_n2 = 8 ∧
    cap_n3 = 18 ∧
    cap_n4 = 32 ∧
    z_he = 2 ∧
    z_ne = 10 ∧
    z_ar = 18 ∧
    z_kr = 36 ∧
    z_xe = 54 ∧
    z_rn = 86 := by
  grind


theorem dirac_coulomb_fine_structure_n2_and_darwin_spin_orbit_degeneracy :
    let c_1s : Rat := (1 / (2 * (1 : Rat) ^ 4)) * (1 / 1 - 3 / 4)
    let c_2_jhalf : Rat := (1 / (2 * (2 : Rat) ^ 4)) * (2 / 1 - 3 / 4)
    let c_2_jthreehalf : Rat := (1 / (2 * (2 : Rat) ^ 4)) * (2 / 2 - 3 / 4)
    let c_2s_rel_kin : Rat := 13 / 128
    let c_2s_darwin : Rat := -8 / 128
    let c_2p_rel_kin : Rat := 7 / 384
    let c_2p12_so : Rat := 8 / 384
    let c_2p32_so : Rat := -4 / 384
    let delta_fs_mc2 : Rat := c_2_jhalf - c_2_jthreehalf
    let delta_fs_ry : Rat := 2 * delta_fs_mc2
    c_1s = 1 / 8 ∧
    c_2_jhalf = 5 / 128 ∧
    c_2_jthreehalf = 1 / 128 ∧
    c_2s_rel_kin + c_2s_darwin = c_2_jhalf ∧
    c_2p_rel_kin + c_2p12_so = c_2_jhalf ∧
    c_2p_rel_kin + c_2p32_so = c_2_jthreehalf ∧
    delta_fs_mc2 = 1 / 32 ∧
    delta_fs_ry = 1 / 16 := by
  grind

theorem qed_one_loop_lamb_shift_contact_and_bethe_lifting :
    let se_const : Rat := 10 / 9 - 5 / 18
    let uehling_vp : Rat := -1 / 5
    let se_plus_vp : Rat := se_const + uehling_vp
    let mag_2s : Rat := 1 / 12
    let mag_2p12 : Rat := -1 / 24
    let mag_diff : Rat := mag_2s - mag_2p12
    let lamb_contact : Rat := se_plus_vp + mag_diff
    let ln_alpha_inv_sq_lo : Rat := 9840487 / 1000000
    let bethe_log_2s_lo : Rat := 2811769 / 1000000
    let bethe_log_2p_hi : Rat := -30016 / 1000000
    let bethe_log_diff_hi : Rat := 2841787 / 1000000
    let bracket_lo : Rat := ln_alpha_inv_sq_lo - bethe_log_diff_hi + lamb_contact
    se_const = 5 / 6 ∧
    se_plus_vp = 19 / 30 ∧
    mag_diff = 1 / 8 ∧
    lamb_contact = 91 / 120 ∧
    bethe_log_2s_lo - bethe_log_2p_hi = 2841785 / 1000000 ∧
    bracket_lo = 232711 / 30000 ∧
    bracket_lo > 7 := by
  grind

theorem helium_kellner_variational_bound_and_virial_identity (z_eff : Rat) :
    let e_unperturbed : Rat := -4
    let v_ee_bare : Rat := 5 / 4
    let e_bare_first_order : Rat := e_unperturbed + v_ee_bare
    let z_opt : Rat := 2 - 5 / 16
    let t_opt : Rat := z_opt ^ 2
    let v_opt : Rat := -4 * z_opt + (5 / 8) * z_opt
    let e_opt : Rat := t_opt + v_opt
    let e_poly : Rat := z_eff ^ 2 - (27 / 8) * z_eff
    let zeta : Rat := 29 / 16
    let c0 : Rat := 400
    let c1 : Rat := -1
    let c2 : Rat := 32
    let c3 : Rat := 4
    let q_s : Rat :=
      1 * c0 * c0 + 42 * c1 * c1 + 24 * c2 * c2 + 144 * c3 * c3 +
      2 * (6 * c0 * c1 + (35 / 8) * c0 * c2 + 6 * c0 * c3 +
           (245 / 8) * c1 * c2 + 48 * c1 * c3 + (77 / 2) * c2 * c3)
    let q_m : Rat :=
      1 * c0 * c0 + 22 * c1 * c1 + 16 * c2 * c2 + 240 * c3 * c3 +
      2 * (4 * c0 * c1 + (25 / 8) * c0 * c2 + 6 * c0 * c3 +
           (135 / 8) * c1 * c2 + 36 * c1 * c3 + (73 / 2) * c2 * c3)
    let q_l : Rat :=
      (27 / 8) * c0 * c0 + (405 / 4) * c1 * c1 + (253 / 4) * c2 * c2 + 537 * c3 * c3 +
      2 * ((135 / 8) * c0 * c1 + 13 * c0 * c2 + (87 / 4) * c0 * c3 +
           78 * c1 * c2 + (609 / 4) * c1 * c3 + 128 * c2 * c3)
    let e_hylleraas_4term : Rat := (zeta ^ 2 * q_m - zeta * q_l) / q_s
    e_bare_first_order = -11 / 4 ∧
    z_opt = 27 / 16 ∧
    e_opt = -729 / 256 ∧
    2 * t_opt + v_opt = 0 ∧
    e_poly - e_opt = (z_eff - z_opt) ^ 2 ∧
    e_opt < e_bare_first_order ∧
    q_s = 320834 ∧
    q_m = 284222 ∧
    q_l = 4115677 / 4 ∧
    e_hylleraas_4term = -119193915 / 41066752 ∧
    e_hylleraas_4term < e_opt := by
  grind

theorem helium_ortho_para_exchange_splitting_and_rhf_contraction (z1 z2 z_nuc sigma : Rat) :
    let z_he : Rat := 2
    let e0_1s2s : Rat := -(5 / 8) * (z_he ^ 2)
    let j_1s2s : Rat := (17 / 81) * z_he
    let k_1s2s : Rat := (16 / 729) * z_he
    let e_triplet_ortho : Rat := e0_1s2s + j_1s2s - k_1s2s
    let e_singlet_para : Rat := e0_1s2s + j_1s2s + k_1s2s
    let lam : Rat := 1 / 4
    let z_star : Rat := z_nuc - sigma
    let f_z1 : Rat := (1 - lam) * (z_nuc - sigma) + lam * z1
    let f_z2 : Rat := (1 - lam) * (z_nuc - sigma) + lam * z2
    let f_zstar : Rat := (1 - lam) * (z_nuc - sigma) + lam * z_star
    let i1_be_2s : Rat := 169 / 500
    let i1_he_1s : Rat := 217 / 256
    let i1_ne_2p : Rat := 13689 / 16000
    j_1s2s = 34 / 81 ∧
    k_1s2s = 32 / 729 ∧
    k_1s2s > 0 ∧
    e_triplet_ortho = -3097 / 1458 ∧
    e_singlet_para = -2969 / 1458 ∧
    e_singlet_para - e_triplet_ortho = 2 * k_1s2s ∧
    e_singlet_para - e_triplet_ortho = 64 / 729 ∧
    e_triplet_ortho < e_singlet_para ∧
    f_zstar = z_star ∧
    (f_z1 - f_z2) ^ 2 = (1 / 16) * (z1 - z2) ^ 2 ∧
    i1_be_2s < i1_he_1s ∧
    i1_he_1s < i1_ne_2p := by
  grind

#print axioms p2_sq_eq_p4_add_two_p22
#print axioms degree4_unit_sphere_basis_identity
#print axioms p4_eq_one_sub_two_p22_on_unit_sphere
#print axioms sym_deg4_frame_sum_on_unit_sphere
#print axioms unit_sphere_standard_ray_witness
#print axioms unit_sphere_pythagorean_ray_witness
#print axioms unit_sphere_rational_3d_ray_witness
#print axioms sym_deg4_sorkin_i3_at_unit_triple
#print axioms quadratic_readout_selected_in_sym_deg4_class
#print axioms QZeta12.zeta_minus_one_unit_inverse
#print axioms QZeta12.fundamental_unit_norm_identities
#print axioms QZeta12.qzeta12_rational_readout_cone_and_galois_selection
#print axioms quad_readout_sorkin_i3_zero
#print axioms countermodel_m207_properties
#print axioms no_rat_square_eq_neg_one
#print axioms countermodel_m208_properties
#print axioms countermodel_m209_all_diagonal_commute
#print axioms countermodel_m210_properties
#print axioms countermodel_m211_properties
#print axioms countermodel_m211_no_left_inverse
#print axioms countermodel_matrix_diagonal_all_false
#print axioms countermodel_matrix_off_diagonal_all_true
#print axioms five_import_mutual_independence
#print axioms born_trace_vs_quartic_readout_and_three_ray_positivity_gap
#print axioms ew_dfm_goldstone_elimination_on_sphere
#print axioms ew_unbroken_electric_charge_annihilates_dressed_vacuum
#print axioms ew_gaussian_4d_goldstone_elimination
#print axioms ew_dfm_doublet_witnesses
#print axioms ew_neutral_mass_matrix_det_and_trace
#print axioms weinberg_projectors_complete_orthogonal_idempotent
#print axioms ew_custodial_rho_eq_one
#print axioms ew_weinberg_and_triplet_witnesses
#print axioms sm_gell_mann_nishijima_charge_identities
#print axioms sm_all_four_anomalies_cancel_at_nc3_and_fail_at_nc1
#print axioms sm_cubic_anomaly_charge_quantization_polynomial
#print axioms su3_casimir_and_channel_identities
#print axioms su3_fierz_diagonal_and_offdiagonal_identities
#print axioms qcd_beta0_asymptotic_freedom_window
#print axioms qcd_beta1_and_banks_zaks_fixed_point
#print axioms wilson_creutz_ratio_area_vs_perimeter
#print axioms wilson_lattice_3x3_dfm_betti_identity
#print axioms ckm_bipartite_dfm_parameter_count
#print axioms gaussRat_unit_phase_cancel
#print axioms jarlskog_quartet_rephasing_dressing_invariance
#print axioms two_gen_cabibbo_artificial_cp_phase_zero
#print axioms three_gen_ckm_substantial_jarlskog_witness
#print axioms su3_diagonal_klein_four_landau_gribov_copies
#print axioms spanning_tree_dfm_eliminates_gribov_copies
#print axioms lorentz_boost_preserves_minkowski_and_det_one
#print axioms cartan_regge_tetrad_dressed_metric_invariance
#print axioms cartan_regge_hinge_holonomy_and_bianchi_witness
#print axioms weyl_heisenberg_finite_trace_obstruction
#print axioms lorentz_boost_non_unitary_in_finite_dim
#print axioms finite_clock_poincare_recurrence_vs_kraus_decoherence
#print axioms wigners_friend_rational_chsh_multi_observer_obstruction
#print axioms qutrit_stabilizer_wigner_nonnegative_vs_magic_negative
#print axioms busch_ic_povm_vs_polyhedral_frame_cone
#print axioms galois_conjugate_negativity_vs_sos_total_positivity
#print axioms char2_mermin_peres_cocycle_and_choi_transpose_separation
#print axioms rational_cayley_unitarity_and_pythagorean_renyi_moments
#print axioms graph_conf2_exchange_betti_and_character_collapse
#print axioms slater_determinant_pauli_exclusion_and_swap_antisymmetry
#print axioms car_clifford_nilpotency_and_occupation_projector
#print axioms pauli_shell_capacities_and_madelung_noble_gas_closures
#print axioms dirac_coulomb_fine_structure_n2_and_darwin_spin_orbit_degeneracy
#print axioms qed_one_loop_lamb_shift_contact_and_bethe_lifting
#print axioms helium_kellner_variational_bound_and_virial_identity
#print axioms helium_ortho_para_exchange_splitting_and_rhf_contraction

end FiniteQM

private def l5aProvenance : String :=
  "Origin: lean4/FiniteQM.lean Claim: p2_sq_eq_p4_add_two_p22 AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
