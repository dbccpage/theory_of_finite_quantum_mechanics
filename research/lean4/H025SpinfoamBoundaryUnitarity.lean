




import H021TriangleNetworkComplexCarrier
import H023DiscreteSpinfoamAmplitudes
import H024FourSimplexSpinfoamS4

namespace FableHilbertWalk20260819.H025

open FableHilbertWalk20260819.H021.CyclotomicRing12
open FableHilbertWalk20260819.H023.QuantumIntegers
open FableHilbertWalk20260819.H023.TetrahedralSpinFoam
open FableHilbertWalk20260819.H024.FourSimplexGeometry
open FableHilbertWalk20260819.H024.TenJAmplitude
open FableHilbertWalk20260819.H024.SimplicialSymmetries
open FableHilbertWalk20260819.H024.S4PartitionFunction


namespace BoundaryGeometry

structure BoundaryTetrahedronSpins where
  j1 : Nat
  j2 : Nat
  j3 : Nat
  j4 : Nat
  deriving DecidableEq, Repr

def vacuumBoundary : BoundaryTetrahedronSpins :=
  ⟨0, 0, 0, 0⟩

def boundaryAdmissible (b : BoundaryTetrahedronSpins) : Bool :=
  (b.j1 + b.j2 + b.j3 + b.j4) % 2 == 0

theorem boundary_vacuum_admissible : boundaryAdmissible vacuumBoundary = true := by rfl

def badBoundary : BoundaryTetrahedronSpins :=
  ⟨1, 0, 0, 0⟩

theorem boundary_inadmissible_witness : boundaryAdmissible badBoundary = false := by rfl

end BoundaryGeometry


namespace BoundaryInnerProduct

open BoundaryGeometry

structure BoundaryState where
  spins : BoundaryTetrahedronSpins
  amplitude : Cyclo12
  deriving DecidableEq, Repr

def vacuumState : BoundaryState :=
  ⟨vacuumBoundary, 1⟩

def innerProduct (psi1 psi2 : BoundaryState) : Cyclo12 :=
  if psi1.spins == psi2.spins && boundaryAdmissible psi1.spins then
    conj psi1.amplitude * psi2.amplitude
  else
    0

def normSquared (psi : BoundaryState) : Cyclo12 :=
  innerProduct psi psi

theorem boundary_inner_product_vacuum_norm : normSquared vacuumState = 1 := by rfl

def badState : BoundaryState :=
  ⟨badBoundary, 1⟩

theorem boundary_inadmissible_zero_norm : normSquared badState = 0 := by rfl

theorem normSquared_admissible (b : BoundaryTetrahedronSpins) (c : Cyclo12)
    (h : boundaryAdmissible b = true) :
    normSquared ⟨b, c⟩ = conj c * c := by
  unfold normSquared innerProduct
  have hb : (b == b) = true := by simp
  simp [hb, h]

end BoundaryInnerProduct


namespace SpinFoamCobordism

open BoundaryGeometry
open BoundaryInnerProduct

structure CobordismData where
  spins : Simplex4Spins
  deriving DecidableEq, Repr

def vacuumCobordism : CobordismData :=
  ⟨vacuum4Spins⟩

def transitionAmplitude (s_in s_out : BoundaryTetrahedronSpins) (W : CobordismData) : Cyclo12 :=
  if s_in == s_out && boundaryAdmissible s_in then
    amplitude10j W.spins
  else
    0

theorem vacuum_transition_is_one :
    transitionAmplitude vacuumBoundary vacuumBoundary vacuumCobordism = 1 := by rfl

theorem inadmissible_boundary_annihilated :
    transitionAmplitude badBoundary vacuumBoundary vacuumCobordism = 0 := by rfl

end SpinFoamCobordism


namespace CobordismAlgebra

open BoundaryGeometry
open BoundaryInnerProduct
open SpinFoamCobordism

def cobordismAdjoint (W : CobordismData) : CobordismData :=
  ⟨orientReverse4 W.spins⟩

theorem vacuum_cobordism_self_adjoint :
    cobordismAdjoint vacuumCobordism = vacuumCobordism := by rfl

theorem cobordism_orientation_adjoint :
    transitionAmplitude vacuumBoundary vacuumBoundary (cobordismAdjoint vacuumCobordism) =
    conj (transitionAmplitude vacuumBoundary vacuumBoundary vacuumCobordism) := by rfl

def composeVacuumSector (W12 W23 : CobordismData) : Cyclo12 :=
  let amp1 := transitionAmplitude vacuumBoundary vacuumBoundary W12
  let amp2 := transitionAmplitude vacuumBoundary vacuumBoundary W23
  amp2 * amp1

theorem cobordism_composition_law :
    composeVacuumSector vacuumCobordism vacuumCobordism = 1 := by rfl

end CobordismAlgebra


namespace DiscreteUnitarity

open BoundaryGeometry
open BoundaryInnerProduct
open SpinFoamCobordism
open CobordismAlgebra

def unitarySandwichVacuum (W : CobordismData) : Cyclo12 :=
  let W_adj := cobordismAdjoint W
  let amp := transitionAmplitude vacuumBoundary vacuumBoundary W
  let amp_adj := transitionAmplitude vacuumBoundary vacuumBoundary W_adj
  amp_adj * amp

theorem discrete_unitarity_vacuum_sandwich :
    unitarySandwichVacuum vacuumCobordism = 1 := by rfl

def evolveState (W : CobordismData) (psi : BoundaryState) : BoundaryState :=
  let new_amp := transitionAmplitude psi.spins psi.spins W * psi.amplitude
  ⟨psi.spins, new_amp⟩

theorem discrete_unitarity_norm_preservation :
    normSquared (evolveState vacuumCobordism vacuumState) = normSquared vacuumState := by rfl

def admissibleBasis8 : List BoundaryTetrahedronSpins := [
  ⟨0, 0, 0, 0⟩,
  ⟨1, 1, 0, 0⟩,
  ⟨1, 0, 1, 0⟩,
  ⟨1, 0, 0, 1⟩,
  ⟨0, 1, 1, 0⟩,
  ⟨0, 1, 0, 1⟩,
  ⟨0, 0, 1, 1⟩,
  ⟨1, 1, 1, 1⟩
]

theorem admissible_basis8_all_admissible :
    ∀ s ∈ admissibleBasis8, boundaryAdmissible s = true := by
  decide

theorem admissible_basis8_nodup : admissibleBasis8.Nodup := by
  decide

def composeIntermediateSum (W12 W23 : CobordismData) (s_in s_out : BoundaryTetrahedronSpins) : Cyclo12 :=
  admissibleBasis8.foldl (fun acc s_mid =>
    acc + (transitionAmplitude s_mid s_out W23 * transitionAmplitude s_in s_mid W12)) 0

def unitarySandwichIntermediate (W : CobordismData) (s_in s_out : BoundaryTetrahedronSpins) : Cyclo12 :=
  let W_adj := cobordismAdjoint W
  admissibleBasis8.foldl (fun acc s_mid =>
    acc + (transitionAmplitude s_out s_mid W_adj * transitionAmplitude s_in s_mid W)) 0

def evolveWavepacket (W : CobordismData) (psi : BoundaryTetrahedronSpins → Cyclo12) :
    BoundaryTetrahedronSpins → Cyclo12 :=
  fun s_out =>
    admissibleBasis8.foldl (fun acc s_in =>
      acc + transitionAmplitude s_in s_out W * psi s_in) 0

theorem discrete_unitarity_intermediate_sandwich_vacuum :
    ∀ s ∈ admissibleBasis8,
      unitarySandwichIntermediate vacuumCobordism s s = 1 := by
  decide

theorem discrete_unitarity_intermediate_sandwich_orthogonal :
    unitarySandwichIntermediate vacuumCobordism ⟨0, 0, 0, 0⟩ ⟨1, 1, 0, 0⟩ = 0 := by
  decide

theorem evolve_wavepacket_vacuum_identity :
    evolveWavepacket vacuumCobordism (fun s => if s == vacuumBoundary then 1 else 0) vacuumBoundary = 1 := by
  decide

theorem quantum_dimension_truncation_bound : q_int 6 = 0 := by rfl

end DiscreteUnitarity


#print axioms BoundaryGeometry.boundary_vacuum_admissible
#print axioms BoundaryGeometry.boundary_inadmissible_witness
#print axioms BoundaryInnerProduct.boundary_inner_product_vacuum_norm
#print axioms BoundaryInnerProduct.boundary_inadmissible_zero_norm
#print axioms SpinFoamCobordism.vacuum_transition_is_one
#print axioms SpinFoamCobordism.inadmissible_boundary_annihilated
#print axioms CobordismAlgebra.vacuum_cobordism_self_adjoint
#print axioms CobordismAlgebra.cobordism_orientation_adjoint
#print axioms CobordismAlgebra.cobordism_composition_law
#print axioms DiscreteUnitarity.discrete_unitarity_vacuum_sandwich
#print axioms DiscreteUnitarity.discrete_unitarity_norm_preservation
#print axioms DiscreteUnitarity.admissible_basis8_all_admissible
#print axioms DiscreteUnitarity.admissible_basis8_nodup
#print axioms DiscreteUnitarity.discrete_unitarity_intermediate_sandwich_vacuum
#print axioms DiscreteUnitarity.discrete_unitarity_intermediate_sandwich_orthogonal
#print axioms DiscreteUnitarity.evolve_wavepacket_vacuum_identity
#print axioms DiscreteUnitarity.quantum_dimension_truncation_bound

end FableHilbertWalk20260819.H025

private def l5aProvenance : String :=
  "Origin: lean4/H025SpinfoamBoundaryUnitarity.lean Claim: boundary_vacuum_admissible AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
