import Std

/-! Finite/rational model of recovery, locality error and conditioning.
    Analytic Lieb-Robinson hypotheses and physical trace-norm estimates are
    written proofs/imports, not conclusions of this core-only module. -/
namespace WitnessedDifference.LocalObservationCompletion

theorem decoder_iff {E R} (obs : E → R) (equiv : E → E → Prop)
    (e0 : E)
    (symmetric : ∀ e f, equiv e f → equiv f e)
    (transitive : ∀ e f g, equiv e f → equiv f g → equiv e g) :
    (∃ decode : R → E, ∀ e, equiv e (decode (obs e))) ↔
      ∀ e f, obs e = obs f → equiv e f := by
  classical
  constructor
  · rintro ⟨decode, h⟩ e f he
    exact transitive e _ f (h e) (he ▸ symmetric f _ (h f))
  · intro h
    let decode (r : R) := if hr : ∃ e, obs e = r then Classical.choose hr else e0
    refine ⟨decode, ?_⟩
    intro e
    have hr : ∃ f, obs f = obs e := ⟨e, rfl⟩
    simp only [decode, dif_pos hr]
    exact h e _ (Classical.choose_spec hr).symm

def repairClass (x y : Bool × Bool × Bool) : Prop :=
  x.2.2 = y.2.2 ∧ Bool.xor x.1 x.2.1 = Bool.xor y.1 y.2.1

def completeObserver (x : Bool × Bool × Bool) : Bool × Bool :=
  (Bool.xor x.1 x.2.1, x.2.2)

def binaryDecoder (r : Bool × Bool) : Bool × Bool × Bool := (false, r.1, r.2)

theorem concrete_binary_decoder (x y z : Bool) :
    repairClass (x, y, z) (binaryDecoder (completeObserver (x, y, z))) := by
  cases x <;> cases y <;> cases z <;> simp [repairClass, binaryDecoder, completeObserver]

theorem blind_observer_collision :
    ¬ repairClass (false, false, false) (false, false, true) := by simp [repairClass]

theorem abs_le_iff (a b : Rat) : a.abs ≤ b ↔ -b ≤ a ∧ a ≤ b := by
  unfold Rat.abs
  split <;> grind

theorem abs_triangle (a b : Rat) : (a+b).abs ≤ a.abs+b.abs := by
  have ha := (abs_le_iff a a.abs).mp Rat.le_refl
  have hb := (abs_le_iff b b.abs).mp Rat.le_refl
  apply (abs_le_iff _ _).mpr
  constructor <;> grind

theorem local_readout_bound (read near tail normState beta : Rat)
    (split : read = near+tail) (equalJointMarginal : near = 0)
    (traceBound : tail.abs ≤ normState*beta)
    (stateBound : normState ≤ 2) (tailBound : 0 ≤ beta) : read.abs ≤ 2*beta := by
  have hm := Rat.mul_le_mul_of_nonneg_right stateBound tailBound
  have he : read = tail := by grind
  rw [he]
  exact Rat.le_trans traceBound hm

theorem conditioning_bound (delta alpha kappa eta beta : Rat)
    (decoding : delta ≤ 2*alpha+kappa*eta) (locality : eta ≤ 2*beta)
    (hk : 0 ≤ kappa) : delta ≤ 2*alpha+2*kappa*beta := by
  have hm := Rat.mul_le_mul_of_nonneg_left locality hk
  grind

theorem common_report_error (u v report delta : Rat)
    (separation : delta ≤ (u-v).abs)
    (hu : (u-report).abs < delta/2) (hv : (v-report).abs < delta/2) : False := by
  have h := abs_triangle (u-report) (report-v)
  rw [Rat.abs_sub_comm (x := report) (y := v)] at h
  have he : u-report+(report-v) = u-v := by grind
  rw [he] at h
  grind

theorem triangle_circulation_invariant (a b c x y z : Rat) :
    (a-(y-x))+(b-(z-y))+(c-(x-z)) = a+b+c := by grind

theorem corrected_triangle_gradient :
    ((0 : Rat)-1, (1 : Rat)-0, (0 : Rat)-0) = (-1, 1, 0) := by
  simp [Rat.sub_eq_add_neg, Rat.zero_add, Rat.add_zero]

theorem actual_exchange_product : (1 : Int)*(-1)*1*1*(-1)*(-1) = -1 := by decide

theorem six_negative_hops_do_not_exchange : (-1 : Int)^6 = 1 := by decide

end WitnessedDifference.LocalObservationCompletion

#print axioms WitnessedDifference.LocalObservationCompletion.decoder_iff
#print axioms WitnessedDifference.LocalObservationCompletion.concrete_binary_decoder
#print axioms WitnessedDifference.LocalObservationCompletion.blind_observer_collision
#print axioms WitnessedDifference.LocalObservationCompletion.abs_triangle
#print axioms WitnessedDifference.LocalObservationCompletion.local_readout_bound
#print axioms WitnessedDifference.LocalObservationCompletion.conditioning_bound
#print axioms WitnessedDifference.LocalObservationCompletion.common_report_error
#print axioms WitnessedDifference.LocalObservationCompletion.triangle_circulation_invariant
#print axioms WitnessedDifference.LocalObservationCompletion.corrected_triangle_gradient
#print axioms WitnessedDifference.LocalObservationCompletion.actual_exchange_product
#print axioms WitnessedDifference.LocalObservationCompletion.six_negative_hops_do_not_exchange
