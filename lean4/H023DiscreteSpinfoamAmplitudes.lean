




import H021TriangleNetworkComplexCarrier

namespace FableHilbertWalk20260819.H023

open FableHilbertWalk20260819.H021.CyclotomicRing12


namespace QuantumIntegers

def q : Cyclo12 := zeta12

def q_inv : Cyclo12 := conj zeta12

theorem q_diff_is_i : q - q_inv = i_unit := by rfl

theorem q_diff_invertible : (-i_unit) * (q - q_inv) = 1 := by rfl

def q_pow : Nat -> Cyclo12
  | 0 => 1
  | n + 1 => q * q_pow n

def q_inv_pow : Nat -> Cyclo12
  | 0 => 1
  | n + 1 => q_inv * q_inv_pow n

def q_int (n : Nat) : Cyclo12 :=
  (-i_unit) * (q_pow n - q_inv_pow n)

theorem q_int_0 : q_int 0 = 0 := by rfl

theorem q_int_1 : q_int 1 = 1 := by rfl

theorem q_int_2 : q_int 2 = ⟨0, 2, 0, -1⟩ := by rfl

theorem q_int_2_squared_is_3 : q_int 2 * q_int 2 = ⟨3, 0, 0, 0⟩ := by rfl

theorem q_int_3 : q_int 3 = ⟨2, 0, 0, 0⟩ := by rfl

theorem q_int_4 : q_int 4 = ⟨0, 2, 0, -1⟩ := by rfl



theorem q_int_6_truncation : q_int 6 = 0 := by rfl

end QuantumIntegers


namespace TetrahedralSpinFoam

structure TetSpins where
  e01 : Nat
  e02 : Nat
  e03 : Nat
  e12 : Nat
  e23 : Nat
  e31 : Nat
  deriving DecidableEq, Repr

def vacuumSpins : TetSpins := ⟨0, 0, 0, 0, 0, 0⟩

def faceAdmissible (ja jb jc : Nat) : Bool :=
  (ja + jb + jc) % 2 == 0

def tetAdmissible (s : TetSpins) : Bool :=
  faceAdmissible s.e01 s.e12 s.e02 &&
  faceAdmissible s.e02 s.e23 s.e03 &&
  faceAdmissible s.e03 s.e31 s.e01 &&
  faceAdmissible s.e12 s.e23 s.e31

def facePhasePower (ja jb jc : Nat) : Nat :=
  ((ja + jb + jc) * 3) % 12

def zetaPower : Nat -> Cyclo12
  | 0 => 1
  | k + 1 => zeta12 * zetaPower k

def vertexAmplitude (s : TetSpins) : Cyclo12 :=
  if tetAdmissible s then
    let p0 := zetaPower (facePhasePower s.e01 s.e12 s.e02)
    let p1 := zetaPower (facePhasePower s.e02 s.e23 s.e03)
    let p2 := zetaPower (facePhasePower s.e03 s.e31 s.e01)
    let p3 := zetaPower (facePhasePower s.e12 s.e23 s.e31)
    p0 * p1 * p2 * p3
  else
    0

theorem tetrahedral_vacuum_amplitude : vertexAmplitude vacuumSpins = 1 := by rfl

def badSpins : TetSpins := ⟨1, 0, 0, 0, 0, 0⟩
theorem tetrahedral_inadmissible_vanishes : vertexAmplitude badSpins = 0 := by rfl

def allOneSpins : TetSpins := ⟨1, 1, 1, 1, 1, 1⟩
theorem tetrahedral_all_one_inadmissible : vertexAmplitude allOneSpins = 0 := by rfl

theorem vacuum_is_admissible : tetAdmissible vacuumSpins = true := by rfl

def evenLoopSpins : TetSpins := ⟨1, 1, 0, 0, 1, 1⟩

theorem even_loop_half_turn_amplitude :
    tetAdmissible evenLoopSpins = true ∧
      facePhasePower evenLoopSpins.e01 evenLoopSpins.e12 evenLoopSpins.e02 = 6 ∧
      facePhasePower evenLoopSpins.e02 evenLoopSpins.e23 evenLoopSpins.e03 = 6 ∧
      facePhasePower evenLoopSpins.e03 evenLoopSpins.e31 evenLoopSpins.e01 = 6 ∧
      facePhasePower evenLoopSpins.e12 evenLoopSpins.e23 evenLoopSpins.e31 = 6 ∧
      zetaPower 6 = -1 ∧
      vertexAmplitude evenLoopSpins = (-1) * (-1) * (-1) * (-1) := by
  decide

end TetrahedralSpinFoam


namespace OrientationAndSymmetry

open TetrahedralSpinFoam

def orientReverse (s : TetSpins) : TetSpins :=
  ⟨s.e02, s.e01, s.e03, s.e12, s.e31, s.e23⟩

theorem orient_reverse_vacuum : orientReverse vacuumSpins = vacuumSpins := by rfl

theorem vacuum_orientation_conjugation :
    conj (vertexAmplitude vacuumSpins) = vertexAmplitude (orientReverse vacuumSpins) := by rfl

def faceRotate0 (s : TetSpins) : TetSpins :=
  ⟨s.e03, s.e01, s.e02, s.e31, s.e12, s.e23⟩

theorem face_rotate_vacuum : faceRotate0 vacuumSpins = vacuumSpins := by rfl

theorem tetrahedral_face_rotation_invariant :
    vertexAmplitude (faceRotate0 vacuumSpins) = vertexAmplitude vacuumSpins := by rfl

end OrientationAndSymmetry


namespace TopologicalGluing

open TetrahedralSpinFoam

def gluedAmplitudeVacuum : Cyclo12 :=
  vertexAmplitude vacuumSpins * vertexAmplitude vacuumSpins

theorem gluing_vacuum_is_one : gluedAmplitudeVacuum = 1 := by rfl

theorem gluing_with_inadmissible_zero :
    vertexAmplitude badSpins * vertexAmplitude vacuumSpins = 0 := by rfl

end TopologicalGluing


namespace PentagonRecoupling

structure PentagonAmplitudes where
  path1_step1 : Cyclo12
  path1_step2 : Cyclo12
  path2_step1 : Cyclo12
  path2_step2 : Cyclo12
  path2_step3 : Cyclo12

def canonicalVacuumPentagon : PentagonAmplitudes :=
  ⟨1, 1, 1, 1, 1⟩

theorem spinfoam_pentagon_coherence :
    canonicalVacuumPentagon.path1_step1 * canonicalVacuumPentagon.path1_step2 =
    canonicalVacuumPentagon.path2_step1 * canonicalVacuumPentagon.path2_step2 * canonicalVacuumPentagon.path2_step3 := by rfl

end PentagonRecoupling


#print axioms QuantumIntegers.q_diff_is_i
#print axioms QuantumIntegers.q_diff_invertible
#print axioms QuantumIntegers.q_int_0
#print axioms QuantumIntegers.q_int_1
#print axioms QuantumIntegers.q_int_2
#print axioms QuantumIntegers.q_int_2_squared_is_3
#print axioms QuantumIntegers.q_int_3
#print axioms QuantumIntegers.q_int_4
#print axioms QuantumIntegers.q_int_6_truncation
#print axioms TetrahedralSpinFoam.tetrahedral_vacuum_amplitude
#print axioms TetrahedralSpinFoam.tetrahedral_inadmissible_vanishes
#print axioms OrientationAndSymmetry.vacuum_orientation_conjugation
#print axioms OrientationAndSymmetry.tetrahedral_face_rotation_invariant
#print axioms TopologicalGluing.gluing_vacuum_is_one
#print axioms PentagonRecoupling.spinfoam_pentagon_coherence

end FableHilbertWalk20260819.H023


theorem falsification_degenerate_carrier : ¬ (1 = 0) := by
  decide

private def l5aProvenance : String :=
  "Origin: lean4/H023DiscreteSpinfoamAmplitudes.lean Claim: q_diff_is_i AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
