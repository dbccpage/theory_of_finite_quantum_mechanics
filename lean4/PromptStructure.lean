import PrimitiveDifference
import HilbertWalkGleasonFin
import HilbertWalkGleasonExtrasDropOne
import FinitePresentedCarrier
import DiscreteDynamicsStone
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith

/- Literal kernel scope; native tables have separate matrix/coordinate bridges.
   Real powers, finite Gaussian coefficients and all interfaces are admitted.
   AuthorityEffect: None. -/
namespace QuantumMechanics.PromptStructure

theorem power_real_unique (p : ℝ) :
    (3/5:ℝ)^p+(4/5:ℝ)^p=1 ↔ p=2 := by
  have h2 : (3/5:ℝ)^(2:ℝ)+(4/5:ℝ)^(2:ℝ)=1 := by norm_num [Real.rpow_two]
  constructor
  · intro h
    rcases lt_trichotomy p 2 with hp | hp | hp
    · have h3 := Real.rpow_lt_rpow_of_exponent_gt (x := (3/5:ℝ)) (by norm_num) (by norm_num) hp
      have h4 := Real.rpow_lt_rpow_of_exponent_gt (x := (4/5:ℝ)) (by norm_num) (by norm_num) hp
      linarith
    · exact hp
    · have h3 := Real.rpow_lt_rpow_of_exponent_gt (x := (3/5:ℝ)) (by norm_num) (by norm_num) hp
      have h4 := Real.rpow_lt_rpow_of_exponent_gt (x := (4/5:ℝ)) (by norm_num) (by norm_num) hp
      linarith
  · rintro rfl; exact h2

def i3 (f : Rat → Rat) (a b c : Rat) : Rat :=
  f (a+b+c)-f (a+b)-f (a+c)-f (b+c)+f a+f b+f c-f 0
theorem power_one_sign_control : i3 (fun t => |t|) 1 1 1=0 ∧
    i3 (fun t => |t|) 1 1 (-1)=2 := by norm_num [i3]
theorem selection_distinct_readouts :
    (1/5:Rat)+4/5=1 ∧ (1/17:Rat)+16/17=1 ∧ (1/5:Rat)≠1/17 := by norm_num

theorem quotient_equivalence {A B : Type} (P : OmegaCore.PrimitiveDifference A B) :
    Equivalence P.ZeroRel := P.zeroRel_equivalence
theorem quotient_classes {A B : Type} (P : OmegaCore.PrimitiveDifference A B) (x y : A) :
    P.classOf x=P.classOf y ↔ P.ZeroRel x y := P.classOf_eq_iff_zeroRel
theorem report_kernel {X Q : Type} (C : HilbertWalk.FinitePresentedCarrier.PresentedCarrier X Q) (x y : X) :
    HilbertWalk.FinitePresentedCarrier.sameReport C x y ↔ C.pres x=C.pres y :=
  HilbertWalk.FinitePresentedCarrier.sameReport_iff C x y

theorem sorkin_polynomial (alpha beta a b c : Rat) :
    i3 (fun t => alpha*t^2+beta*t^4) a b c=12*beta*a*b*c*(a+b+c) := by unfold i3; ring
theorem sorkin_family_selection (alpha beta : Rat) :
    (∀ a b c, i3 (fun t => alpha*t^2+beta*t^4) a b c=0) ↔ beta=0 := by
  constructor
  · intro h; have hh := h 1 1 1
    rw [sorkin_polynomial] at hh
    norm_num at hh
    linarith
  · rintro rfl; intro a b c; rw [sorkin_polynomial]; ring
theorem galois_basis_invariance (A B : Rat) : 7*A+4*B=7*A-4*B ↔ B=0 := by constructor <;> intro h <;> linarith

theorem pinching_squared (a b : Rat) : 4*a*a ≤ 4*(a*a+b*b) := by nlinarith [sq_nonneg b]
theorem positive_rescaling (c x y : Rat) (hc : 0<c) (h : x≤y) : c*x≤c*y :=
  mul_le_mul_of_nonneg_left h (le_of_lt hc)
theorem tracezero_scalar_shift (a b d c x y z : Rat) (hz : x+y+z=0) :
    (a+c)*x+(b+c)*y+(d+c)*z=a*x+b*y+d*z := by
  have hz0 : z = -x-y := by linarith
  rw [hz0]; ring
theorem k23_witness_objectives : (3:Rat)*(6/3)=6 ∧ (3:Rat)*(6/4)=9/2 := by norm_num

def pquad (a b c d : Rat) : Rat := a*a-b*b-c*c+d*d+2*a*d+2*b*c
theorem tsirelson_minus_sos (a b c d : Rat) :
    2*(a*a+b*b+c*c+d*d)-pquad a b c d=(a-d)^2+(b-c)^2+2*b^2+2*c^2 := by unfold pquad; ring
theorem tsirelson_plus_sos (a b c d : Rat) :
    2*(a*a+b*b+c*c+d*d)+pquad a b c d=(a+d)^2+2*a^2+2*d^2+(b+c)^2 := by unfold pquad; ring
theorem tsirelson_fixed_bound (a b c d : Rat) :
    -2*(a*a+b*b+c*c+d*d)≤pquad a b c d ∧ pquad a b c d≤2*(a*a+b*b+c*c+d*d) := by
  have hm := tsirelson_minus_sos a b c d
  have hp := tsirelson_plus_sos a b c d
  constructor <;> nlinarith [sq_nonneg (a-d),sq_nonneg (b-c),sq_nonneg (a+d),sq_nonneg (b+c),sq_nonneg a,sq_nonneg b,sq_nonneg c,sq_nonneg d]
theorem tsirelson_scaled_attainment : pquad 1 0 0 1=4 ∧ (1:Rat)^2+0^2+0^2+1^2=2 := by norm_num [pquad]

open HilbertWalk.GleasonExtrasDropOne
theorem census_nodup : allExtras.Nodup := extras_nodup
theorem census_partition : allExtras.length=8 ∧ lostExtras.length=3 ∧ openExtras.length=5 :=
  ⟨extra_list_length,lost_length,open_length⟩
-- These counts concern the declared list; rfl verdicts do not prove necessity.

open HilbertWalk.HWKernel
open HilbertWalk.FreeLinearization
open HilbertWalk.GleasonFin
theorem gauss_recovery {Q : Type} [DecidableEq Q] (E : Enum Q)
    (T : LinearEnd Q gaussPack) (v : Vec GaussInt Q) (x : Q) :
    T.map v x=applyMat gaussPack E (matOf T) v x := apply_eq_matOf E T v x
theorem gauss_unique {Q : Type} [DecidableEq Q] (E : Enum Q)
    (T : LinearEnd Q gaussPack) (A : Mat GaussInt Q)
    (h : ∀ v x, T.map v x=applyMat gaussPack E A v x) :
    ∀ i j, matOf T i j=A i j := matrix_of_end_unique E T A h
theorem gauss_composition {Q : Type} (E : Enum Q) (A B : Mat GaussInt Q)
    (v : Vec GaussInt Q) (i : Q) :
    applyMat gaussPack E (mmul gaussPack E A B) v i=applyMat gaussPack E A (applyMat gaussPack E B v) i := mmul_as_composition gaussPack E A B v i
theorem gauss_adjoint {Q : Type} (E : Enum Q) (A : Mat GaussInt Q) (u v : Vec GaussInt Q) :
    HilbertWalk.InnerProductAdmission.sesq gaussPack E (applyMat gaussPack E A u) v=
    HilbertWalk.InnerProductAdmission.sesq gaussPack E u (applyMat gaussPack E (adj gaussPack A) v) := sesq_conj_transpose gaussPack E A u v

theorem time_no_bool_root : ¬ ∃ f : Bool → Bool, ∀ b, f (f b)=HilbertWalk.DiscreteDynamicsStone.toggle b :=
  HilbertWalk.DiscreteDynamicsStone.no_bool_half_step
theorem time_two_scaled_roots :
    HilbertWalk.DiscreteDynamicsStone.mat2g_mul HilbertWalk.DiscreteDynamicsStone.neg_M_scaled HilbertWalk.DiscreteDynamicsStone.neg_M_scaled=HilbertWalk.DiscreteDynamicsStone.four_X ∧
    HilbertWalk.DiscreteDynamicsStone.neg_M_scaled≠HilbertWalk.DiscreteDynamicsStone.M_scaled :=
  HilbertWalk.DiscreteDynamicsStone.interpolant_not_unique

#print axioms power_real_unique
#print axioms power_one_sign_control
#print axioms selection_distinct_readouts
#print axioms quotient_equivalence
#print axioms quotient_classes
#print axioms report_kernel
#print axioms sorkin_polynomial
#print axioms sorkin_family_selection
#print axioms galois_basis_invariance
#print axioms pinching_squared
#print axioms positive_rescaling
#print axioms tracezero_scalar_shift
#print axioms k23_witness_objectives
#print axioms tsirelson_minus_sos
#print axioms tsirelson_plus_sos
#print axioms tsirelson_fixed_bound
#print axioms tsirelson_scaled_attainment
#print axioms census_nodup
#print axioms census_partition
#print axioms gauss_recovery
#print axioms gauss_unique
#print axioms gauss_composition
#print axioms gauss_adjoint
#print axioms time_no_bool_root
#print axioms time_two_scaled_roots
end QuantumMechanics.PromptStructure
