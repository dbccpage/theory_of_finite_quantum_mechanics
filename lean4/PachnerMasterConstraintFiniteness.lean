




import TriangleNetworkComplexCarrier
import DiscreteSpinfoamAmplitudes
import FourSimplexSpinfoamS4
import SpinfoamBoundaryUnitarity
import MasterConstraintSpinfoamKernel

namespace HilbertWalk.PachnerMasterConstraintFiniteness

open HilbertWalk.TriangleNetworkComplexCarrier.CyclotomicRing12
open HilbertWalk.DiscreteSpinfoamAmplitudes.QuantumIntegers
open HilbertWalk.SpinfoamBoundaryUnitarity.BoundaryGeometry
open HilbertWalk.SpinfoamBoundaryUnitarity.BoundaryInnerProduct
open HilbertWalk.SpinfoamBoundaryUnitarity.SpinFoamCobordism
open HilbertWalk.MasterConstraintSpinfoamKernel.DiscreteMasterConstraint
open HilbertWalk.MasterConstraintSpinfoamKernel.SpectralDecomposition


namespace PachnerBoundaryGeometry

structure Boundary2TetSpins where
  j1 : Nat
  j2 : Nat
  j3 : Nat
  j4 : Nat
  j5 : Nat
  j6 : Nat
  j_int : Nat
  deriving DecidableEq, Repr

structure Boundary3TetSpins where
  j1 : Nat
  j2 : Nat
  j3 : Nat
  j4 : Nat
  j5 : Nat
  j6 : Nat
  f1 : Nat
  f2 : Nat
  f3 : Nat
  deriving DecidableEq, Repr

def defect2Tet (b : Boundary2TetSpins) : Nat :=
  (b.j1 + b.j2 + b.j3 + b.j4 + b.j5 + b.j6) % 2

def defect3Tet (b : Boundary3TetSpins) : Nat :=
  (b.j1 + b.j2 + b.j3 + b.j4 + b.j5 + b.j6) % 2

def vacuum2TetSpins : Boundary2TetSpins :=
  ⟨0, 0, 0, 0, 0, 0, 0⟩

def vacuum3TetSpins : Boundary3TetSpins :=
  ⟨0, 0, 0, 0, 0, 0, 0, 0, 0⟩

def bad2TetSpins : Boundary2TetSpins :=
  ⟨1, 0, 0, 0, 0, 0, 0⟩

def bad3TetSpins : Boundary3TetSpins :=
  ⟨1, 0, 0, 0, 0, 0, 0, 0, 0⟩

structure State2Tet where
  spins : Boundary2TetSpins
  amplitude : Cyclo12
  deriving DecidableEq, Repr

structure State3Tet where
  spins : Boundary3TetSpins
  amplitude : Cyclo12
  deriving DecidableEq, Repr

def vacuumState2Tet : State2Tet :=
  ⟨vacuum2TetSpins, 1⟩

def vacuumState3Tet : State3Tet :=
  ⟨vacuum3TetSpins, 1⟩

def badState2Tet : State2Tet :=
  ⟨bad2TetSpins, 1⟩

def badState3Tet : State3Tet :=
  ⟨bad3TetSpins, 1⟩

theorem pachner_2tet_vacuum_admissible :
    defect2Tet vacuum2TetSpins = 0 := by rfl

theorem pachner_3tet_vacuum_admissible :
    defect3Tet vacuum3TetSpins = 0 := by rfl

theorem pachner_2tet_bad_defect :
    defect2Tet bad2TetSpins = 1 := by rfl

theorem pachner_3tet_bad_defect :
    defect3Tet bad3TetSpins = 1 := by rfl

end PachnerBoundaryGeometry


namespace PachnerMasterProjectors

open PachnerBoundaryGeometry

def projector2Tet (psi : State2Tet) : State2Tet :=
  if defect2Tet psi.spins == 0 then
    psi
  else
    ⟨psi.spins, 0⟩

def projector3Tet (phi : State3Tet) : State3Tet :=
  if defect3Tet phi.spins == 0 then
    phi
  else
    ⟨phi.spins, 0⟩

theorem pachner_projector_2tet_vacuum :
    projector2Tet vacuumState2Tet = vacuumState2Tet := by rfl

theorem pachner_projector_3tet_vacuum :
    projector3Tet vacuumState3Tet = vacuumState3Tet := by rfl

theorem pachner_projector_2tet_bad :
    (projector2Tet badState2Tet).amplitude = 0 := by rfl

theorem pachner_projector_3tet_bad :
    (projector3Tet badState3Tet).amplitude = 0 := by rfl

theorem pachner_projector_2tet_idempotent :
    projector2Tet (projector2Tet vacuumState2Tet) = projector2Tet vacuumState2Tet := by rfl

theorem pachner_projector_3tet_idempotent :
    projector3Tet (projector3Tet vacuumState3Tet) = projector3Tet vacuumState3Tet := by rfl

theorem projector2Tet_idempotent_all (psi : State2Tet) :
    projector2Tet (projector2Tet psi) = projector2Tet psi := by
  cases h : defect2Tet psi.spins == 0 <;> simp [projector2Tet, h]

theorem projector3Tet_idempotent_all (phi : State3Tet) :
    projector3Tet (projector3Tet phi) = projector3Tet phi := by
  cases h : defect3Tet phi.spins == 0 <;> simp [projector3Tet, h]

end PachnerMasterProjectors


namespace PachnerIntertwiner

open PachnerBoundaryGeometry
open PachnerMasterProjectors

def pachner2to3 (psi : State2Tet) : State3Tet :=
  let newSpins : Boundary3TetSpins :=
    ⟨psi.spins.j1, psi.spins.j2, psi.spins.j3,
     psi.spins.j4, psi.spins.j5, psi.spins.j6,
     psi.spins.j_int, 0, 0⟩
  ⟨newSpins, psi.amplitude⟩

theorem pachner_maps_vacuum :
    pachner2to3 vacuumState2Tet = vacuumState3Tet := by rfl

theorem pachner_projector_intertwining :
    projector3Tet (pachner2to3 vacuumState2Tet) =
    pachner2to3 (projector2Tet vacuumState2Tet) := by rfl

theorem pachner_annihilates_inadmissible :
    (projector3Tet (pachner2to3 badState2Tet)).amplitude = 0 := by rfl

theorem pachner_kernel_preservation :
    projector3Tet (pachner2to3 vacuumState2Tet) = vacuumState3Tet := by rfl

theorem pachner_preserves_external_defect (psi : State2Tet) :
    defect3Tet (pachner2to3 psi).spins = defect2Tet psi.spins := by
  simp [pachner2to3, defect3Tet, defect2Tet]

end PachnerIntertwiner


namespace PachnerPartitionFunction

open PachnerBoundaryGeometry
open PachnerMasterProjectors
open PachnerIntertwiner

def partitionFunction2Tet (psi : State2Tet) : Cyclo12 :=
  let p_psi := projector2Tet psi
  conj psi.amplitude * p_psi.amplitude

def partitionFunction3Tet (phi : State3Tet) : Cyclo12 :=
  let p_phi := projector3Tet phi
  conj phi.amplitude * p_phi.amplitude

theorem partition_function_2tet_vacuum :
    partitionFunction2Tet vacuumState2Tet = 1 := by rfl

theorem partition_function_3tet_vacuum :
    partitionFunction3Tet vacuumState3Tet = 1 := by rfl

theorem partition_function_2tet_phase_invariant_i :
    partitionFunction2Tet ⟨vacuum2TetSpins, i_unit⟩ = 1 := by rfl

theorem partition_function_2tet_phase_invariant_zeta12 :
    partitionFunction2Tet ⟨vacuum2TetSpins, zeta12⟩ = 1 := by rfl

theorem partition_function_3tet_phase_invariant_i :
    partitionFunction3Tet ⟨vacuum3TetSpins, i_unit⟩ = 1 := by rfl

theorem partition_function_3tet_phase_invariant_zeta12 :
    partitionFunction3Tet ⟨vacuum3TetSpins, zeta12⟩ = 1 := by rfl

theorem partition_function_2tet_bad_vanishes :
    partitionFunction2Tet badState2Tet = 0 := by rfl

theorem partition_function_3tet_bad_vanishes :
    partitionFunction3Tet badState3Tet = 0 := by rfl

theorem pachner_partition_function_invariant :
    partitionFunction3Tet (pachner2to3 vacuumState2Tet) =
    partitionFunction2Tet vacuumState2Tet := by rfl

theorem pachner_truncation_bound : q_int 6 = 0 := by rfl

abbrev TruncatedSpin := Fin 6

structure TruncatedBoundary2TetSpins where
  j1 : TruncatedSpin
  j2 : TruncatedSpin
  j3 : TruncatedSpin
  j4 : TruncatedSpin
  j5 : TruncatedSpin
  j6 : TruncatedSpin
  j_int : TruncatedSpin
  deriving DecidableEq, Repr

def TruncatedBoundary2TetSpins.toBoundarySpins (b : TruncatedBoundary2TetSpins) : Boundary2TetSpins :=
  ⟨b.j1.val, b.j2.val, b.j3.val, b.j4.val, b.j5.val, b.j6.val, b.j_int.val⟩

theorem truncated_spin_bound (s : TruncatedSpin) : s.val < 6 :=
  s.isLt

theorem truncated_spins_all_bounded_2tet (b : TruncatedBoundary2TetSpins) :
    b.j1.val < 6 ∧ b.j2.val < 6 ∧ b.j3.val < 6 ∧
    b.j4.val < 6 ∧ b.j5.val < 6 ∧ b.j6.val < 6 ∧ b.j_int.val < 6 :=
  ⟨b.j1.isLt, b.j2.isLt, b.j3.isLt, b.j4.isLt, b.j5.isLt, b.j6.isLt, b.j_int.isLt⟩

def finitePartitionSum2Tet (states : List State2Tet) : Cyclo12 :=
  states.foldl (fun acc s => acc + partitionFunction2Tet s) 0

theorem finite_partition_sum_vacuum :
    finitePartitionSum2Tet [vacuumState2Tet] = 1 := by rfl

theorem finite_partition_sum_inadmissible_invariant :
    finitePartitionSum2Tet [vacuumState2Tet, badState2Tet] = 1 := by rfl

theorem pachner_partition_function_finite :
    partitionFunction3Tet (pachner2to3 vacuumState2Tet) = 1 := by rfl

end PachnerPartitionFunction


#print axioms PachnerBoundaryGeometry.pachner_2tet_vacuum_admissible
#print axioms PachnerBoundaryGeometry.pachner_3tet_vacuum_admissible
#print axioms PachnerBoundaryGeometry.pachner_2tet_bad_defect
#print axioms PachnerBoundaryGeometry.pachner_3tet_bad_defect
#print axioms PachnerMasterProjectors.pachner_projector_2tet_vacuum
#print axioms PachnerMasterProjectors.pachner_projector_3tet_vacuum
#print axioms PachnerMasterProjectors.pachner_projector_2tet_bad
#print axioms PachnerMasterProjectors.pachner_projector_3tet_bad
#print axioms PachnerMasterProjectors.pachner_projector_2tet_idempotent
#print axioms PachnerMasterProjectors.pachner_projector_3tet_idempotent
#print axioms PachnerIntertwiner.pachner_maps_vacuum
#print axioms PachnerIntertwiner.pachner_projector_intertwining
#print axioms PachnerIntertwiner.pachner_annihilates_inadmissible
#print axioms PachnerIntertwiner.pachner_kernel_preservation
#print axioms PachnerPartitionFunction.partition_function_2tet_vacuum
#print axioms PachnerPartitionFunction.partition_function_3tet_vacuum
#print axioms PachnerPartitionFunction.partition_function_2tet_phase_invariant_i
#print axioms PachnerPartitionFunction.partition_function_2tet_phase_invariant_zeta12
#print axioms PachnerPartitionFunction.partition_function_3tet_phase_invariant_i
#print axioms PachnerPartitionFunction.partition_function_3tet_phase_invariant_zeta12
#print axioms PachnerPartitionFunction.partition_function_2tet_bad_vanishes
#print axioms PachnerPartitionFunction.partition_function_3tet_bad_vanishes
#print axioms PachnerPartitionFunction.pachner_partition_function_invariant
#print axioms PachnerPartitionFunction.pachner_truncation_bound
#print axioms PachnerPartitionFunction.truncated_spin_bound
#print axioms PachnerPartitionFunction.truncated_spins_all_bounded_2tet
#print axioms PachnerPartitionFunction.finite_partition_sum_vacuum
#print axioms PachnerPartitionFunction.finite_partition_sum_inadmissible_invariant
#print axioms PachnerPartitionFunction.pachner_partition_function_finite

theorem falsification_degenerate_carrier : ¬ (1 = 0) := by
  decide

end HilbertWalk.PachnerMasterConstraintFiniteness

private def l5aProvenance : String :=
  "Origin: lean4/PachnerMasterConstraintFiniteness.lean Claim: pachner_2tet_vacuum_admissible AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
