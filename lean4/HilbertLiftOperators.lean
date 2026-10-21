import HilbertLiftIntrinsicUniformity
import Mathlib.Analysis.Normed.Operator.Basic

/-!
# Lifting bounded exact operators; the unbounded coordinate-sum functional

Origin: dag/results/FQ-GAP-CONTINUUM-HILBERT-LIFT/runs/20261021T003000Z_lift_steps
Claim: a `ℚ`-linear map `A` of the exact carrier with a rational quadratic bound
`qinner (A f) (A f) ≤ C * qinner f f` is uniformly continuous for the intrinsic uniformity and
extends uniquely to a continuous `ℝ`-linear operator on the real Hilbert lift with
`‖T x‖² ≤ C ‖x‖²` (operator norm at most `√C`); the stage projections and the unilateral shift
are such operators (the shift lifts to an isometry); and the `ℚ`-linear coordinate-sum
functional admits no continuous extension to the lift, although the harmonic vectors it
diverges on have squared norm at most `2`.
AuthorityEffect: None
Scope Fence: the bound `C` is a hypothesis on the exact operator; nothing selects which exact
operators are physical.  No dynamics, generator, spectrum or Born pairing is constructed.
Level: L5
-/

namespace HilbertLift

open Filter Topology UniformSpace Uniformity Finset

/-- A bounded exact operator: a `ℚ`-linear map of the exact carrier with a rational quadratic
bound. -/
structure BoundedExactOperator where
  /-- The exact `ℚ`-linear map. -/
  A : Carrier →ₗ[ℚ] Carrier
  /-- The rational quadratic bound. -/
  bound : ℚ
  bound_nonneg : 0 ≤ bound
  norm_sq_le : ∀ f : Carrier, qinner (A f) (A f) ≤ bound * qinner f f

namespace BoundedExactOperator

variable (T : BoundedExactOperator)

theorem sqdist_map_le (f g : Carrier) : sqdist (T.A f) (T.A g) ≤ T.bound * sqdist f g := by
  unfold sqdist
  rw [← map_sub]
  exact T.norm_sq_le (f - g)

theorem bound_add_one_pos : 0 < T.bound + 1 := by
  linarith [T.bound_nonneg]

theorem sqdist_map_lt {f g : Carrier} {ε : ℚ} (hε : 0 < ε)
    (hfg : sqdist f g < ε / (T.bound + 1)) : sqdist (T.A f) (T.A g) < ε := by
  have hb := T.bound_nonneg
  have hb1 := T.bound_add_one_pos
  calc sqdist (T.A f) (T.A g) ≤ T.bound * sqdist f g := T.sqdist_map_le f g
    _ ≤ T.bound * (ε / (T.bound + 1)) := by gcongr
    _ < ε := by
      rw [mul_div_assoc', div_lt_iff₀ hb1]
      nlinarith

theorem isCauchyL2_map {x : ℕ → Carrier} (hx : IsCauchyL2 x) :
    IsCauchyL2 fun n => T.A (x n) := by
  intro ε hε
  obtain ⟨N, hN⟩ := hx (ε / (T.bound + 1)) (div_pos hε T.bound_add_one_pos)
  exact ⟨N, fun m hm n hn => T.sqdist_map_lt hε (hN m hm n hn)⟩

/-- A bounded exact operator is uniformly continuous for the intrinsic uniformity. -/
theorem uniformContinuous_A : UniformContinuous T.A := by
  rw [uniformity_hasBasis_sqdist.uniformContinuous_iff uniformity_hasBasis_sqdist]
  intro ε hε
  refine ⟨ε / (T.bound + 1), div_pos hε T.bound_add_one_pos, fun f g hfg => ?_⟩
  exact T.sqdist_map_lt hε hfg

/-- The lifted operator on the real Hilbert lift. -/
noncomputable def liftOp : HilbertLiftSpace ℝ → HilbertLiftSpace ℝ :=
  fun x => completionEquivLift (Completion.map T.A (completionEquivLift.symm x))

theorem liftOp_lift (f : Carrier) : T.liftOp (lift ℝ f) = lift ℝ (T.A f) := by
  unfold liftOp
  rw [completionEquivLift_symm_lift, Completion.map_coe T.uniformContinuous_A,
    completionEquivLift_coe]

theorem continuous_liftOp : Continuous T.liftOp :=
  completionEquivLift.continuous.comp
    (Completion.continuous_map.comp completionEquivLift.continuous_symm)

/-- Uniqueness: any continuous map agreeing with `A` on exact vectors is the lifted operator. -/
theorem liftOp_unique {S : HilbertLiftSpace ℝ → HilbertLiftSpace ℝ} (hS : Continuous S)
    (h : ∀ f : Carrier, S (lift ℝ f) = lift ℝ (T.A f)) : S = T.liftOp :=
  ext_of_lift hS T.continuous_liftOp fun f => by rw [h, liftOp_lift]

theorem norm_liftOp_sq_le (x : HilbertLiftSpace ℝ) :
    ‖T.liftOp x‖ ^ 2 ≤ (T.bound : ℝ) * ‖x‖ ^ 2 := by
  refine denseRange_lift_real.induction_on x ?_ ?_
  · exact isClosed_le (T.continuous_liftOp.norm.pow 2) (continuous_const.mul (continuous_norm.pow 2))
  · intro f
    rw [liftOp_lift, norm_lift_sq, norm_lift_sq]
    exact_mod_cast T.norm_sq_le f

theorem liftOp_add (x y : HilbertLiftSpace ℝ) : T.liftOp (x + y) = T.liftOp x + T.liftOp y := by
  have hd : DenseRange (Prod.map (lift ℝ) (lift ℝ)) :=
    denseRange_lift_real.prodMap denseRange_lift_real
  refine hd.induction_on
    (p := fun p : HilbertLiftSpace ℝ × HilbertLiftSpace ℝ =>
      T.liftOp (p.1 + p.2) = T.liftOp p.1 + T.liftOp p.2) (x, y) ?_ ?_
  · exact isClosed_eq (T.continuous_liftOp.comp continuous_add)
      ((T.continuous_liftOp.comp continuous_fst).add (T.continuous_liftOp.comp continuous_snd))
  · rintro ⟨f, g⟩
    show T.liftOp (lift ℝ f + lift ℝ g) = T.liftOp (lift ℝ f) + T.liftOp (lift ℝ g)
    rw [← lift_add, liftOp_lift, liftOp_lift, liftOp_lift, map_add, lift_add]

theorem liftOp_qsmul (q : ℚ) (x : HilbertLiftSpace ℝ) :
    T.liftOp ((q : ℝ) • x) = (q : ℝ) • T.liftOp x := by
  refine denseRange_lift_real.induction_on x ?_ ?_
  · exact isClosed_eq (T.continuous_liftOp.comp (continuous_const_smul _))
      ((continuous_const_smul (q : ℝ)).comp T.continuous_liftOp)
  · intro f
    rw [← lift_smul, liftOp_lift, liftOp_lift, map_smul, lift_smul]

theorem liftOp_smul (r : ℝ) (x : HilbertLiftSpace ℝ) : T.liftOp (r • x) = r • T.liftOp x := by
  refine Rat.denseRange_cast.induction_on
    (p := fun r : ℝ => T.liftOp (r • x) = r • T.liftOp x) r ?_ ?_
  · exact isClosed_eq (T.continuous_liftOp.comp (continuous_id.smul continuous_const))
      (continuous_id.smul continuous_const)
  · intro q
    exact T.liftOp_qsmul q x

/-- The lifted operator as a continuous `ℝ`-linear map. -/
noncomputable def toCLM : HilbertLiftSpace ℝ →L[ℝ] HilbertLiftSpace ℝ :=
  { toFun := T.liftOp
    map_add' := T.liftOp_add
    map_smul' := T.liftOp_smul
    cont := T.continuous_liftOp }

theorem toCLM_apply (x : HilbertLiftSpace ℝ) : T.toCLM x = T.liftOp x := rfl

theorem toCLM_lift (f : Carrier) : T.toCLM (lift ℝ f) = lift ℝ (T.A f) := T.liftOp_lift f

theorem norm_toCLM_le (x : HilbertLiftSpace ℝ) : ‖T.toCLM x‖ ≤ Real.sqrt T.bound * ‖x‖ := by
  rw [toCLM_apply]
  have h := T.norm_liftOp_sq_le x
  have hb : (0 : ℝ) ≤ T.bound := by exact_mod_cast T.bound_nonneg
  calc ‖T.liftOp x‖ = Real.sqrt (‖T.liftOp x‖ ^ 2) := (Real.sqrt_sq (norm_nonneg _)).symm
    _ ≤ Real.sqrt ((T.bound : ℝ) * ‖x‖ ^ 2) := Real.sqrt_le_sqrt h
    _ = Real.sqrt T.bound * ‖x‖ := by rw [Real.sqrt_mul hb, Real.sqrt_sq (norm_nonneg _)]

theorem opNorm_toCLM_le : ‖T.toCLM‖ ≤ Real.sqrt T.bound :=
  ContinuousLinearMap.opNorm_le_bound _ (Real.sqrt_nonneg _) T.norm_toCLM_le

end BoundedExactOperator

/-! ### Examples: stage projections and the unilateral shift -/

theorem trunc_add (n : ℕ) (f g : Carrier) : trunc n (f + g) = trunc n f + trunc n g := by
  funext i
  simp [trunc]

theorem trunc_smul (n : ℕ) (c : ℚ) (f : Carrier) : trunc n (c • f) = c • trunc n f := by
  funext i
  simp [trunc]

/-- The exact projection onto report size `n`. -/
noncomputable def projMap (n : ℕ) : Carrier →ₗ[ℚ] Carrier where
  toFun f := ofFin (trunc n f)
  map_add' f g := by rw [trunc_add, ofFin_add]
  map_smul' c f := by rw [trunc_smul, ofFin_smul]; rfl

theorem projMap_apply (n : ℕ) (f : Carrier) : projMap n f = ofFin (trunc n f) := rfl

/-- The stage projection is a bounded exact operator with bound `1` (Bessel). -/
noncomputable def proj (n : ℕ) : BoundedExactOperator where
  A := projMap n
  bound := 1
  bound_nonneg := zero_le_one
  norm_sq_le f := by
    rw [projMap_apply, qinner_ofFin, one_mul]
    exact finInner_trunc_le n f

theorem proj_lift (n : ℕ) (f : Carrier) : (proj n).liftOp (lift ℝ f) = liftFin ℝ (trunc n f) :=
  (proj n).liftOp_lift f

/-- The unilateral shift `e_i ↦ e_{i+1}` as a `ℚ`-linear map. -/
noncomputable def shiftMap : Carrier →ₗ[ℚ] Carrier := Finsupp.lmapDomain ℚ ℚ Nat.succ

theorem shiftMap_apply (f : Carrier) : shiftMap f = Finsupp.mapDomain Nat.succ f :=
  Finsupp.lmapDomain_apply _ _ _ _

/-- The shift preserves the exact inner product. -/
theorem qinner_shift (f g : Carrier) : qinner (shiftMap f) (shiftMap g) = qinner f g := by
  rw [shiftMap_apply, shiftMap_apply]
  unfold qinner
  rw [Finsupp.sum_mapDomain_index_inj Nat.succ_injective]
  exact Finsupp.sum_congr fun i _ => by rw [Finsupp.mapDomain_apply_of_injective Nat.succ_injective]

/-- The shift is a bounded exact operator with bound `1`. -/
noncomputable def shift : BoundedExactOperator where
  A := shiftMap
  bound := 1
  bound_nonneg := zero_le_one
  norm_sq_le f := by rw [qinner_shift, one_mul]

/-- The lifted shift is an isometry of the real Hilbert lift. -/
theorem norm_shift_liftOp (x : HilbertLiftSpace ℝ) : ‖shift.liftOp x‖ = ‖x‖ := by
  refine denseRange_lift_real.induction_on x ?_ ?_
  · exact isClosed_eq shift.continuous_liftOp.norm continuous_norm
  · intro f
    have h : ‖shift.liftOp (lift ℝ f)‖ ^ 2 = ‖lift ℝ f‖ ^ 2 := by
      rw [shift.liftOp_lift, norm_lift_sq, norm_lift_sq]
      show ((qinner (shiftMap f) (shiftMap f) : ℚ) : ℝ) = _
      rw [qinner_shift]
    exact (pow_left_inj₀ (norm_nonneg _) (norm_nonneg _) two_ne_zero).mp h

/-! ### The coordinate-sum functional has no continuous extension -/

/-- The coordinate sum `Σ_i f i`, a `ℚ`-linear functional on the exact carrier. -/
noncomputable def coordSum (f : Carrier) : ℚ := f.sum fun _ a => a

theorem coordSum_add (f g : Carrier) : coordSum (f + g) = coordSum f + coordSum g := by
  unfold coordSum
  exact Finsupp.sum_add_index' (fun _ => rfl) (fun _ _ _ => rfl)

theorem coordSum_smul (c : ℚ) (f : Carrier) : coordSum (c • f) = c * coordSum f := by
  unfold coordSum
  rw [Finsupp.sum_smul_index' (fun _ => rfl), Finsupp.mul_sum]
  exact Finsupp.sum_congr fun _ _ => rfl

theorem coordSum_harmonic (N : ℕ) : coordSum (harmonic N) = ∑ i ∈ range N, harmonicTerm i := by
  unfold coordSum
  rw [Finsupp.sum_of_support_subset _ (support_harmonic_subset N) _ (fun _ _ => rfl)]
  exact Finset.sum_congr rfl fun i hi => by rw [harmonic_apply, if_pos (mem_range.mp hi)]

theorem coordSum_harmonic_gap {n : ℕ} (hn : 1 ≤ n) :
    1 / 2 ≤ coordSum (harmonic (2 * n)) - coordSum (harmonic n) := by
  rw [coordSum_harmonic, coordSum_harmonic, range_eq_Ico, range_eq_Ico,
    ← Finset.sum_Ico_consecutive _ (Nat.zero_le n) (by omega : n ≤ 2 * n)]
  have h := sum_harmonicTerm_Ico_ge n hn
  linarith

theorem harmonicTerm_zero : harmonicTerm 0 = 1 := by
  norm_num [harmonicTerm]

/-- The harmonic vectors have squared norm at most `2`. -/
theorem qinner_harmonic_le_two (N : ℕ) : qinner (harmonic N) (harmonic N) ≤ 2 := by
  have h0 : harmonic 0 = 0 := Finsupp.ext fun i => by simp
  have h1 : qinner (harmonic N) (harmonic N) = sqdist (harmonic N) (harmonic 0) := by
    rw [sqdist, h0, sub_zero]
  rw [h1, sqdist_harmonic (Nat.zero_le N)]
  rcases Nat.eq_zero_or_pos N with hN | hN
  · subst hN
    simp
  · rw [← Finset.sum_Ico_consecutive _ (Nat.zero_le 1) hN]
    have h2 := sum_harmonicTerm_sq_le (le_refl 1) N hN
    have h3 : ∑ i ∈ Ico 0 1, harmonicTerm i ^ 2 = 1 := by
      simp [harmonicTerm_zero]
    have h4 : (0 : ℚ) ≤ 1 / (N : ℚ) := by positivity
    rw [h3]
    linarith

/-- No continuous real functional on the lift restricts to the coordinate sum on exact
vectors: linearity without a bound does not lift. -/
theorem no_continuous_extension_coordSum :
    ¬ ∃ Λ : HilbertLiftSpace ℝ → ℝ, Continuous Λ ∧
      ∀ f : Carrier, Λ (lift ℝ f) = (coordSum f : ℝ) := by
  rintro ⟨Λ, hΛ, hf⟩
  obtain ⟨h, hh⟩ := exists_limit_of_isCauchyL2 (𝕜 := ℝ) harmonic harmonic_isCauchyL2
  have ht : Tendsto (fun n => Λ (lift ℝ (harmonic n))) atTop (𝓝 (Λ h)) :=
    (hΛ.tendsto h).comp hh
  have hc := ht.cauchySeq
  rw [Metric.cauchySeq_iff] at hc
  obtain ⟨N, hN⟩ := hc (1 / 2) (by norm_num)
  have h1 := hN (2 * (N + 1)) (by omega) (N + 1) (by omega)
  rw [hf, hf, Real.dist_eq] at h1
  have h2 := coordSum_harmonic_gap (n := N + 1) (by omega)
  have h3 := (Rat.cast_le (K := ℝ)).mpr h2
  push_cast at h3
  have h4 := le_abs_self
    ((coordSum (harmonic (2 * (N + 1))) : ℝ) - coordSum (harmonic (N + 1)))
  linarith

/-- Summary: bounded exact operators lift to continuous linear operators with the same
quadratic bound, uniquely; the shift lifts to an isometry; the coordinate sum does not lift. -/
theorem operator_lift_summary :
    (∀ T : BoundedExactOperator, ∀ f : Carrier, T.toCLM (lift ℝ f) = lift ℝ (T.A f)) ∧
    (∀ T : BoundedExactOperator, ‖T.toCLM‖ ≤ Real.sqrt T.bound) ∧
    (∀ x : HilbertLiftSpace ℝ, ‖shift.liftOp x‖ = ‖x‖) ∧
    ¬ ∃ Λ : HilbertLiftSpace ℝ → ℝ, Continuous Λ ∧
      ∀ f : Carrier, Λ (lift ℝ f) = (coordSum f : ℝ) :=
  ⟨fun T => T.toCLM_lift, fun T => T.opNorm_toCLM_le, norm_shift_liftOp,
    no_continuous_extension_coordSum⟩

end HilbertLift

#print axioms HilbertLift.BoundedExactOperator.sqdist_map_le
#print axioms HilbertLift.BoundedExactOperator.isCauchyL2_map
#print axioms HilbertLift.BoundedExactOperator.uniformContinuous_A
#print axioms HilbertLift.BoundedExactOperator.liftOp_lift
#print axioms HilbertLift.BoundedExactOperator.continuous_liftOp
#print axioms HilbertLift.BoundedExactOperator.liftOp_unique
#print axioms HilbertLift.BoundedExactOperator.norm_liftOp_sq_le
#print axioms HilbertLift.BoundedExactOperator.liftOp_add
#print axioms HilbertLift.BoundedExactOperator.liftOp_qsmul
#print axioms HilbertLift.BoundedExactOperator.liftOp_smul
#print axioms HilbertLift.BoundedExactOperator.toCLM_lift
#print axioms HilbertLift.BoundedExactOperator.norm_toCLM_le
#print axioms HilbertLift.BoundedExactOperator.opNorm_toCLM_le
#print axioms HilbertLift.trunc_add
#print axioms HilbertLift.trunc_smul
#print axioms HilbertLift.proj_lift
#print axioms HilbertLift.qinner_shift
#print axioms HilbertLift.norm_shift_liftOp
#print axioms HilbertLift.coordSum_add
#print axioms HilbertLift.coordSum_smul
#print axioms HilbertLift.coordSum_harmonic
#print axioms HilbertLift.coordSum_harmonic_gap
#print axioms HilbertLift.qinner_harmonic_le_two
#print axioms HilbertLift.no_continuous_extension_coordSum
#print axioms HilbertLift.operator_lift_summary
