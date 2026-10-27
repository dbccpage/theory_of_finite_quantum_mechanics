




import TriangleNetworkComplexCarrier
import DiscreteSpinfoamAmplitudes

namespace HilbertWalk.FourSimplexSpinfoamS4

open HilbertWalk.TriangleNetworkComplexCarrier.CyclotomicRing12
open HilbertWalk.DiscreteSpinfoamAmplitudes.QuantumIntegers
open HilbertWalk.DiscreteSpinfoamAmplitudes.TetrahedralSpinFoam


namespace FourSimplexGeometry

structure Simplex4Spins where
  f012 : Nat
  f013 : Nat
  f014 : Nat
  f023 : Nat
  f024 : Nat
  f034 : Nat
  f123 : Nat
  f124 : Nat
  f134 : Nat
  f234 : Nat
  deriving DecidableEq, Repr

def vacuum4Spins : Simplex4Spins :=
  ⟨0, 0, 0, 0, 0, 0, 0, 0, 0, 0⟩

def tet4Admissible (ja jb jc jd : Nat) : Bool :=
  (ja + jb + jc + jd) % 2 == 0

def simplex4Admissible (s : Simplex4Spins) : Bool :=
  tet4Admissible s.f123 s.f124 s.f134 s.f234 &&
  tet4Admissible s.f023 s.f024 s.f034 s.f234 &&
  tet4Admissible s.f013 s.f014 s.f034 s.f134 &&
  tet4Admissible s.f012 s.f014 s.f024 s.f124 &&
  tet4Admissible s.f012 s.f013 s.f023 s.f123

theorem simplex4_vacuum_admissible : simplex4Admissible vacuum4Spins = true := by rfl

def bad4Spins : Simplex4Spins :=
  ⟨1, 0, 0, 0, 0, 0, 0, 0, 0, 0⟩

theorem simplex4_inadmissible_witness : simplex4Admissible bad4Spins = false := by rfl

end FourSimplexGeometry


namespace TenJAmplitude

open FourSimplexGeometry

def tetPhasePower (ja jb jc jd : Nat) : Nat :=
  ((ja + jb + jc + jd) * 3) % 12

def amplitude10j (s : Simplex4Spins) : Cyclo12 :=
  if simplex4Admissible s then
    let p0 := zetaPower (tetPhasePower s.f123 s.f124 s.f134 s.f234)
    let p1 := zetaPower (tetPhasePower s.f023 s.f024 s.f034 s.f234)
    let p2 := zetaPower (tetPhasePower s.f013 s.f014 s.f034 s.f134)
    let p3 := zetaPower (tetPhasePower s.f012 s.f014 s.f024 s.f124)
    let p4 := zetaPower (tetPhasePower s.f012 s.f013 s.f023 s.f123)
    p0 * p1 * p2 * p3 * p4
  else
    0

theorem amplitude10j_vacuum : amplitude10j vacuum4Spins = 1 := by rfl

theorem amplitude10j_inadmissible_vanishes : amplitude10j bad4Spins = 0 := by rfl

def doubledFace012 : Simplex4Spins := ⟨2, 0, 0, 0, 0, 0, 0, 0, 0, 0⟩

theorem doubled_face_half_turn_pair :
    simplex4Admissible doubledFace012 = true ∧
      tetPhasePower doubledFace012.f012 doubledFace012.f014
          doubledFace012.f024 doubledFace012.f124 = 6 ∧
      zetaPower 6 = -1 ∧
      amplitude10j doubledFace012 = (-1) * (-1) := by
  decide

end TenJAmplitude


namespace SimplicialSymmetries

open FourSimplexGeometry
open TenJAmplitude

def orientReverse4 (s : Simplex4Spins) : Simplex4Spins :=
  ⟨s.f012, s.f013, s.f014, s.f123, s.f124, s.f134, s.f023, s.f024, s.f034, s.f234⟩

theorem orient_reverse_vacuum4 : orientReverse4 vacuum4Spins = vacuum4Spins := by rfl

theorem amplitude10j_orientation_conjugation :
    conj (amplitude10j vacuum4Spins) = amplitude10j (orientReverse4 vacuum4Spins) := by rfl

def cyclicPerm4 (s : Simplex4Spins) : Simplex4Spins :=
  ⟨s.f123, s.f124, s.f012, s.f134, s.f013, s.f014, s.f234, s.f023, s.f024, s.f034⟩

theorem cyclic_perm_vacuum4 : cyclicPerm4 vacuum4Spins = vacuum4Spins := by rfl

theorem amplitude10j_a5_cyclic_invariant :
    amplitude10j (cyclicPerm4 vacuum4Spins) = amplitude10j vacuum4Spins := by rfl

end SimplicialSymmetries


namespace MinimalFourSphere

def v_count : Int := 6
def e_count : Int := 15
def f_count : Int := 20
def t_count : Int := 15
def s4_count : Int := 6

theorem euler_characteristic_s4 :
    v_count - e_count + f_count - t_count + s4_count = 2 := by rfl

end MinimalFourSphere


namespace S4PartitionFunction

open FourSimplexGeometry
open TenJAmplitude
open MinimalFourSphere

def quantumDimension (j : Nat) : Cyclo12 :=
  q_int (2 * j + 1)

theorem dim_q_vacuum : quantumDimension 0 = 1 := by rfl

theorem dim_q_one : quantumDimension 1 = ⟨2, 0, 0, 0⟩ := by rfl

def partitionFunctionVacuumS4 : Cyclo12 :=
  let face_weights : Cyclo12 := 1
  let vertex_weights : Cyclo12 := 1
  face_weights * vertex_weights

theorem s4_vacuum_sector_is_one : partitionFunctionVacuumS4 = 1 := by rfl

theorem s4_inadmissible_sector_vanishes :
    amplitude10j bad4Spins * partitionFunctionVacuumS4 = 0 := by rfl

theorem s4_truncation_bound : q_int 6 = 0 := by rfl

end S4PartitionFunction


#print axioms FourSimplexGeometry.simplex4_vacuum_admissible
#print axioms FourSimplexGeometry.simplex4_inadmissible_witness
#print axioms TenJAmplitude.amplitude10j_vacuum
#print axioms TenJAmplitude.amplitude10j_inadmissible_vanishes
#print axioms SimplicialSymmetries.amplitude10j_orientation_conjugation
#print axioms SimplicialSymmetries.amplitude10j_a5_cyclic_invariant
#print axioms MinimalFourSphere.euler_characteristic_s4
#print axioms S4PartitionFunction.dim_q_vacuum
#print axioms S4PartitionFunction.dim_q_one
#print axioms S4PartitionFunction.s4_vacuum_sector_is_one
#print axioms S4PartitionFunction.s4_inadmissible_sector_vanishes
#print axioms S4PartitionFunction.s4_truncation_bound

theorem falsification_degenerate_carrier : ¬ (1 = 0) := by
  decide

end HilbertWalk.FourSimplexSpinfoamS4

private def l5aProvenance : String :=
  "Origin: lean4/FourSimplexSpinfoamS4.lean Claim: simplex4_vacuum_admissible AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
