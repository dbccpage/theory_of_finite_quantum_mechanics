import GleasonRationalPlane
import BornRedundancy
import InterferenceNonDescent
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

/- Scope-specific statements. Native output tables are not kernel theorems.
   Text inventories are not proof audits. AuthorityEffect: None. -/
namespace QuantumMechanics.PromptPhaseScope
open HilbertWalk.HWKernel
open HilbertWalk.FreeLinearization
open HilbertWalk.PhaseBlindPresentation
open HilbertWalk.PhaseFiber
open HilbertWalk.InterferenceNonDescent
open ProjectionFiber.Core
open FiniteQm.GleasonRationalPlane

theorem continuum_two_not_unit (a : Int) : 2*a ≠ 1 := by omega
theorem continuum_discriminant (l : Rat) :
    4*(l*l-l-1)+5 = (2*l-1)^2 := by ring

-- Coverage of a proper subset cannot supply a missing member's obligation.
theorem corpus_partial_coverage {I : Type} (covered : I → Prop) (i : I)
    (missing : ¬covered i) : ¬(∀ j, covered j) := by
  intro h; exact missing (h i)

-- A conditional transport schema, not a theorem about actual filesystem bytes.
theorem custody_changed_pin {S : Type} (hash : S → String) (x y : S)
    (changed : hash x ≠ hash y) : x ≠ y := by
  intro h; exact changed (congrArg hash h)

theorem tensor_product_det (a b c d : Rat) :
    (a*c)*(b*d)-(a*d)*(b*c)=0 := by ring
theorem tensor_entangled_det : (1:Rat)*1-0*0=1 := by norm_num

theorem u1_cayley_cleared (t : Rat) :
    (1-t*t)^2+(2*t)^2=(1+t*t)^2 := by ring
theorem u1_half_square_constraint (a b : Rat)
    (h : a*a-b*b=3/5) (hn : a*a+b*b=1) : a*a=4/5 := by linarith

theorem d2_no_quadratic : ¬ ∃ a b c : Rat, ∀ x y : Rat,
    x ≠ 0 ∨ y ≠ 0 → a*x*x+2*b*x*y+c*y*y=binaryRay x y*(x*x+y*y) :=
  no_quadratic_representation
theorem d2_frame_sum (x y u v : Rat) (hxy : x≠0 ∨ y≠0)
    (huv : u≠0 ∨ v≠0) (horth : x*u+y*v=0) :
    binaryRay x y+binaryRay u v=1 := orthogonal_frame_sum x y u v hxy huv horth
theorem d2_scale (x y k : Rat) (hk : k≠0) :
    binaryRay (k*x) (k*y)=binaryRay x y := scale_invariant x y k hk
theorem interference_no_descent :
    ¬ ∃ f : (Bool → Int) → (Bool → Int),
      ∀ v : Vec GaussInt Bool, readout v=f (phaseBlind v) := no_descent_through_fiber
theorem interference_mass_doubles :
    totalWeight enumBool (mix psi1)=2*totalWeight enumBool psi1 ∧
    totalWeight enumBool (mix psi2)=2*totalWeight enumBool psi2 := mix_doubles_total
theorem zero_integer_row_characterization (M : BornRedundancy.Mat2) :
    BornRedundancy.DescentCompatible M ↔ BornRedundancy.RowSparse M :=
  BornRedundancy.descent_compatible_iff_row_sparse M
theorem zero_projective_cancellation :
    ((1+1:Rat)^2,(1+1:Rat)^2) ≠ ((1-1:Rat)^2,(1-1:Rat)^2) := by norm_num
theorem fiber_relative : ZeroRel (phasePD Bool) psi1 psi2 ∧ psi1≠psi2 := relative_phase_in_fiber
theorem fiber_global {Q : Type} (v : Vec GaussInt Q) :
    ZeroRel (phasePD Q) (fun x => GaussInt.gmul GaussInt.gi (v x)) v := global_phase_in_fiber v
theorem fiber_equivalence {Q : Type} (u v : Vec GaussInt Q) :
    ZeroRel (phasePD Q) u v ↔ phaseBlind u=phaseBlind v := phasePD_zeroRel_iff u v
theorem fiber_unit_orbit_incomplete : (5:Int)^2+0^2=3^2+4^2 ∧
    (3,4) ≠ (5,0) ∧ (3,4) ≠ (0,5) ∧ (3,4) ≠ (-5,0) ∧ (3,4) ≠ (0,-5) := by decide

theorem weights_two_preparations :
    (1/2:Rat)+1/2=1 ∧ (1/3:Rat)+2/3=1 ∧ (1/2:Rat)≠1/3 := by norm_num
theorem weights_signed_control : (2:Rat)+(-1)=1 ∧ 2*2+(-1)*(-2)>2 := by norm_num
theorem weights_convex_bound (p q s t : Rat) (hp : 0≤p) (hq : 0≤q)
    (hs : -2≤s ∧ s≤2) (ht : -2≤t ∧ t≤2) :
    -2*(p+q)≤p*s+q*t ∧ p*s+q*t≤2*(p+q) := by
  constructor <;> nlinarith

#print axioms continuum_two_not_unit
#print axioms continuum_discriminant
#print axioms corpus_partial_coverage
#print axioms custody_changed_pin
#print axioms tensor_product_det
#print axioms tensor_entangled_det
#print axioms u1_cayley_cleared
#print axioms u1_half_square_constraint
#print axioms d2_no_quadratic
#print axioms d2_frame_sum
#print axioms d2_scale
#print axioms interference_no_descent
#print axioms interference_mass_doubles
#print axioms zero_integer_row_characterization
#print axioms zero_projective_cancellation
#print axioms fiber_relative
#print axioms fiber_global
#print axioms fiber_equivalence
#print axioms fiber_unit_orbit_incomplete
#print axioms weights_two_preparations
#print axioms weights_signed_control
#print axioms weights_convex_bound
#check d2_no_quadratic
#check d2_frame_sum
#check d2_scale
#check interference_no_descent
#check interference_mass_doubles
#check zero_integer_row_characterization
#check fiber_relative
#check fiber_global
#check fiber_equivalence
end QuantumMechanics.PromptPhaseScope
