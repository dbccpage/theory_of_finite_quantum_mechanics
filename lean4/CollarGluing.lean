/- Conditional interfaces and arithmetic examples only.
No Rust receipt instantiates the curvature, Gramian representation, or coverage
hypotheses in this module. The named theorem statements are the precise scope.
AuthorityEffect: None.
-/
import WallTransport
import ZeroRelVariety
import ModuliReduction
import AlgebraicCornerReconstruction
import KarlssonManifold
import KarlssonVolumeObstruction

namespace MUB6.Gluing.CollarGluing

open MUB6.Gluing
open MUB6.Gluing.Variety
open MUB6.Gluing.Orbits
open MUB6.Gluing.ModuliReduction
open MUB6.Gluing.Karlsson
open MUB6.Gluing.KarlssonVolume

structure ExactFraction where
  num : Nat
  den : Nat
  den_pos : 0 < den
deriving DecidableEq, Repr

def ExactFraction.lt (a b : ExactFraction) : Prop :=
  a.num * b.den < b.num * a.den

instance (a b : ExactFraction) : Decidable (a.lt b) :=
  inferInstanceAs (Decidable (a.num * b.den < b.num * a.den))

def ExactFraction.sub (a b : ExactFraction) (_h : b.lt a) : ExactFraction where
  num := a.num * b.den - b.num * a.den
  den := a.den * b.den
  den_pos := Nat.mul_pos a.den_pos b.den_pos

def ExactFraction.mul (a b : ExactFraction) : ExactFraction where
  num := a.num * b.num
  den := a.den * b.den
  den_pos := Nat.mul_pos a.den_pos b.den_pos

def ExactFraction.le (a b : ExactFraction) : Prop :=
  a.num * b.den ≤ b.num * a.den

instance (a b : ExactFraction) : Decidable (a.le b) :=
  inferInstanceAs (Decidable (a.num * b.den ≤ b.num * a.den))

def ExactFraction.equiv (a b : ExactFraction) : Prop :=
  a.num * b.den = b.num * a.den

instance (a b : ExactFraction) : Decidable (a.equiv b) :=
  inferInstanceAs (Decidable (a.num * b.den = b.num * a.den))

def delta_frac : ExactFraction := ⟨1, 1000, by decide⟩


def epsilon_d6_frac : ExactFraction := ⟨37249, 90000, by decide⟩

def lipschitz_lz_frac : ExactFraction := ⟨85, 9, by decide⟩

def erosion_frac : ExactFraction := ⟨17, 1800, by decide⟩

theorem barrier_inequality_frac : erosion_frac.lt epsilon_d6_frac := by
  decide

def margin_frac : ExactFraction :=
  epsilon_d6_frac.sub erosion_frac barrier_inequality_frac

theorem barrier_margin_pos : 0 < margin_frac.num := by
  decide

def margin_reduced_frac : ExactFraction := ⟨12133, 30000, by decide⟩

theorem margin_reduced_eq :
    margin_frac.num * margin_reduced_frac.den = margin_reduced_frac.num * margin_frac.den := by
  decide

structure CollarPoint where
  point : TorusPoint3
  delta : Nat
  h_z_pos : 0 < point.z.val
  h_z_le : point.z.val ≤ delta
deriving Repr

structure CollarTripleWitness where
  collar_point : CollarPoint
  witness : KarlssonTripleWitness
  point_eq : witness.point = collar_point.point

structure CollarBarrierParameters (C : CurvatureCarrier) where
  epsilon_d6 : C.M
  delta : C.M
  lipschitz_lz : C.M
  erosion : C.M
  h_barrier : C.lt erosion epsilon_d6

def collar_barrier_margin {C : CurvatureCarrier} (params : CollarBarrierParameters C) : C.M :=
  C.sub params.epsilon_d6 params.erosion

theorem collar_barrier_margin_pos {C : CurvatureCarrier} (params : CollarBarrierParameters C) :
    C.lt C.zero (collar_barrier_margin params) :=
  C.sub_pos_of_lt params.h_barrier

def HasCollarCurvatureBound
    {C : CurvatureCarrier} (CS : CurvatureSpace C)
    (params : CollarBarrierParameters C)
    (T : MUTriple) : Prop :=
  HasCurvatureBound CS T (collar_barrier_margin params)

theorem collar_extension_obstruction
    {C : CurvatureCarrier} (CS : CurvatureSpace C)
    (params : CollarBarrierParameters C)
    (T : MUTriple)
    (h_bound : HasCollarCurvatureBound CS params T) :
    ZeroRelVarietyEmpty T ∧ ¬ HasFourthBasis T := by
  have h_pos : C.lt C.zero (collar_barrier_margin params) :=
    collar_barrier_margin_pos params
  have h_empty : ZeroRelVarietyEmpty T :=
    curvature_bound_implies_variety_empty CS T (collar_barrier_margin params) h_pos h_bound
  have h_no4 : ¬ HasFourthBasis T :=
    (no_fourth_basis_iff_variety_empty T).mpr h_empty
  exact ⟨h_empty, h_no4⟩

theorem collar_transverse_no_fourth_basis
    {C : CurvatureCarrier} (CS : CurvatureSpace C)
    (params : CollarBarrierParameters C)
    (W : CollarTripleWitness)
    (h_bound : HasCollarCurvatureBound CS params W.witness.triple) :
    ZeroRelVarietyEmpty W.witness.triple ∧ ¬ HasFourthBasis W.witness.triple :=
  collar_extension_obstruction CS params W.witness.triple h_bound

theorem collar_boundary_retracts_to_dita (x y : PhaseAngle) :
    DitaOrbit (KarlssonSliceZero x y) :=
  dita_embeds_as_slice_zero x y

theorem collar_gluing_grand_synthesis
    {C : CurvatureCarrier} (CS : CurvatureSpace C)
    (params : CollarBarrierParameters C)
    (W : CollarTripleWitness)
    (h_bound : HasCollarCurvatureBound CS params W.witness.triple)
    (h_cov : ModuliCoverageConjecture)
    (h_atlas : AtlasCoversKnownModuli)
    (h_gauge : GaugeInvariantClassMembership)
    (h_g2_var : G2_Variety)
    (h_g3 : G3) :
    ZeroRelVarietyEmpty W.witness.triple ∧
    ¬ HasFourthBasis W.witness.triple ∧
    NoCompleteMUB6 := by
  have h_collar := collar_transverse_no_fourth_basis CS params W h_bound
  have h_grand := moduli_reduction_grand_synthesis h_cov h_atlas h_gauge h_g2_var h_g3
  exact ⟨h_collar.1, h_collar.2, h_grand⟩

#print axioms barrier_inequality_frac
#print axioms barrier_margin_pos
#print axioms margin_reduced_eq
#print axioms collar_barrier_margin_pos
#print axioms collar_extension_obstruction
#print axioms collar_transverse_no_fourth_basis
#print axioms collar_boundary_retracts_to_dita
#print axioms collar_gluing_grand_synthesis

end MUB6.Gluing.CollarGluing
