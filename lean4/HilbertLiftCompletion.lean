import HilbertLiftRationalUniformity
import Mathlib.Analysis.InnerProductSpace.Completion
import Mathlib.Analysis.Normed.Group.Completion
import Mathlib.Topology.MetricSpace.Completion
import Mathlib.Topology.Sequences

/-!
# The controlled Hilbert completion of the exact carriers

Origin: dag/results/FQ-GAP-CONTINUUM-HILBERT-LIFT/runs/20261020T230000Z_completion
Claim: for `𝕜 = ℝ` or `ℂ`, the finitely supported `𝕜`-sequences `PreH 𝕜 := ℕ →₀ 𝕜` carry the
inner product `Σ conj(f i) g i`; the Hilbert lift `HilbertLiftSpace 𝕜` is Mathlib's Hausdorff
completion of `PreH 𝕜`, a complete inner product space; the explicit embedding `lift 𝕜` of the
exact carrier `ℕ →₀ ℚ` is inner-product preserving, injective and compatible with the finite
stages; a sequence of exact vectors is Cauchy in the lift exactly when it is ℓ²-Cauchy with
rational tolerances, every such sequence has a limit in the lift, and (for `𝕜 = ℝ`) the exact
vectors are dense, every element of the lift is such a limit, continuous maps out of the lift are
determined by their values on exact vectors, and the lift is strictly larger than the exact
carrier.
AuthorityEffect: None
Scope Fence: the scalar field `𝕜` (so `ℝ` or `ℂ`, hence the completion `ℚ → ℝ`) and the ℓ²
uniformity are the supplied hypotheses; nothing selects them.  Density is proved for `𝕜 = ℝ`
with the rational real carrier; for `𝕜 = ℂ` the rational real carrier embeds isometrically but
is not dense (a Gaussian-rational carrier is required).  No operator, dynamics, Born rule,
tensor structure or physical interpretation is constructed.  The instances on `PreH 𝕜` are
declared on the abbreviation `ℕ →₀ 𝕜`; no other module of this run places a norm on `Finsupp`.
Level: L5
-/

namespace HilbertLift

open Finset Filter Topology UniformSpace

section Scalars

variable (𝕜 : Type*) [RCLike 𝕜]

/-- The scalar-extended pre-Hilbert carrier: finitely supported `𝕜`-sequences. -/
abbrev PreH : Type _ := ℕ →₀ 𝕜

/-- The inner product `Σ conj (f i) * g i` on the pre-Hilbert carrier. -/
noncomputable def preInner (f g : PreH 𝕜) : 𝕜 := f.sum fun i a => (starRingEnd 𝕜) a * g i

variable {𝕜}

theorem preInner_eq_sum (f g : PreH 𝕜) {s : Finset ℕ} (hs : f.support ⊆ s) :
    preInner 𝕜 f g = ∑ i ∈ s, (starRingEnd 𝕜) (f i) * g i :=
  Finsupp.sum_of_support_subset f hs _ (fun _ _ => by simp)

theorem preInner_conj_symm (f g : PreH 𝕜) :
    (starRingEnd 𝕜) (preInner 𝕜 g f) = preInner 𝕜 f g := by
  rw [preInner_eq_sum g f (s := f.support ∪ g.support) subset_union_right,
    preInner_eq_sum f g (s := f.support ∪ g.support) subset_union_left, map_sum]
  refine Finset.sum_congr rfl fun i _ => ?_
  rw [map_mul, RCLike.conj_conj, mul_comm]

theorem preInner_add_left (f g h : PreH 𝕜) :
    preInner 𝕜 (f + g) h = preInner 𝕜 f h + preInner 𝕜 g h := by
  classical
  rw [preInner_eq_sum (f + g) h (s := f.support ∪ g.support) Finsupp.support_add,
    preInner_eq_sum f h (s := f.support ∪ g.support) subset_union_left,
    preInner_eq_sum g h (s := f.support ∪ g.support) subset_union_right,
    ← Finset.sum_add_distrib]
  refine Finset.sum_congr rfl fun i _ => ?_
  rw [Finsupp.add_apply, map_add, add_mul]

theorem preInner_smul_left (r : 𝕜) (f g : PreH 𝕜) :
    preInner 𝕜 (r • f) g = (starRingEnd 𝕜) r * preInner 𝕜 f g := by
  rw [preInner_eq_sum (r • f) g (s := f.support) Finsupp.support_smul,
    preInner_eq_sum f g (subset_refl _), Finset.mul_sum]
  refine Finset.sum_congr rfl fun i _ => ?_
  rw [Finsupp.smul_apply, smul_eq_mul, map_mul, mul_assoc]

theorem re_conj_mul_self (z : 𝕜) : RCLike.re ((starRingEnd 𝕜) z * z) = ‖z‖ ^ 2 := by
  rw [RCLike.conj_mul, ← RCLike.ofReal_pow, RCLike.ofReal_re]

theorem re_preInner_self (f : PreH 𝕜) {s : Finset ℕ} (hs : f.support ⊆ s) :
    RCLike.re (preInner 𝕜 f f) = ∑ i ∈ s, ‖f i‖ ^ 2 := by
  rw [preInner_eq_sum f f hs, map_sum]
  exact Finset.sum_congr rfl fun i _ => re_conj_mul_self _

theorem re_preInner_self_nonneg (f : PreH 𝕜) : 0 ≤ RCLike.re (preInner 𝕜 f f) := by
  rw [re_preInner_self f (subset_refl _)]
  exact Finset.sum_nonneg fun i _ => by positivity

theorem preInner_self_eq_zero (f : PreH 𝕜) (h : preInner 𝕜 f f = 0) : f = 0 := by
  have h0 : ∑ i ∈ f.support, ‖f i‖ ^ 2 = 0 := by
    rw [← re_preInner_self f (subset_refl _), h, map_zero]
  rw [Finset.sum_eq_zero_iff_of_nonneg (fun i _ => by positivity)] at h0
  ext i
  by_cases hi : i ∈ f.support
  · have h1 : ‖f i‖ = 0 := (pow_eq_zero_iff two_ne_zero).mp (h0 i hi)
    simpa using norm_eq_zero.mp h1
  · simpa using Finsupp.notMem_support_iff.mp hi

variable (𝕜) in
/-- The inner-product core of the pre-Hilbert carrier. -/
noncomputable instance instCorePreH : InnerProductSpace.Core 𝕜 (PreH 𝕜) where
  inner := preInner 𝕜
  conj_inner_symm := preInner_conj_symm
  re_inner_nonneg := re_preInner_self_nonneg
  add_left := preInner_add_left
  smul_left := fun f g r => preInner_smul_left r f g
  definite := preInner_self_eq_zero

noncomputable instance instNormedAddCommGroupPreH : NormedAddCommGroup (PreH 𝕜) :=
  InnerProductSpace.Core.toNormedAddCommGroup (𝕜 := 𝕜)

noncomputable instance instInnerProductSpacePreH : InnerProductSpace 𝕜 (PreH 𝕜) :=
  InnerProductSpace.ofCore _

theorem inner_def (f g : PreH 𝕜) : inner 𝕜 f g = preInner 𝕜 f g := rfl

variable (𝕜) in
/-- The Hilbert lift: the Hausdorff completion of the pre-Hilbert carrier. -/
abbrev HilbertLiftSpace : Type _ := Completion (PreH 𝕜)

/-- The lift is complete. -/
theorem hilbertLiftSpace_complete : CompleteSpace (HilbertLiftSpace 𝕜) := inferInstance

/-- The lift carries an inner product space structure over `𝕜` (Mathlib's instance on the
completion of an inner product space). -/
theorem hilbertLiftSpace_innerProductSpace : Nonempty (InnerProductSpace 𝕜 (HilbertLiftSpace 𝕜)) :=
  ⟨inferInstance⟩

variable (𝕜) in
/-- Scalar lift of exact rational sequences. -/
noncomputable def castSeq (f : Carrier) : PreH 𝕜 :=
  Finsupp.mapRange (Rat.cast : ℚ → 𝕜) Rat.cast_zero f

@[simp] theorem castSeq_apply (f : Carrier) (i : ℕ) : castSeq 𝕜 f i = (f i : 𝕜) :=
  Finsupp.mapRange_apply

theorem support_castSeq_subset (f : Carrier) : (castSeq 𝕜 f).support ⊆ f.support :=
  Finsupp.support_mapRange

theorem castSeq_sub (f g : Carrier) : castSeq 𝕜 (f - g) = castSeq 𝕜 f - castSeq 𝕜 g :=
  Finsupp.mapRange_sub (fun _ _ => Rat.cast_sub _ _) f g

theorem castSeq_add (f g : Carrier) : castSeq 𝕜 (f + g) = castSeq 𝕜 f + castSeq 𝕜 g :=
  Finsupp.mapRange_add (fun _ _ => Rat.cast_add _ _) f g

theorem castSeq_smul (q : ℚ) (f : Carrier) : castSeq 𝕜 (q • f) = (q : 𝕜) • castSeq 𝕜 f :=
  Finsupp.ext fun i => by
    simp only [castSeq_apply, Finsupp.smul_apply, smul_eq_mul, Rat.cast_mul]

theorem castSeq_injective : Function.Injective (castSeq 𝕜) := by
  intro f g h
  ext i
  have := congrArg (fun v : PreH 𝕜 => v i) h
  simp only [castSeq_apply] at this
  exact Rat.cast_injective this

/-- The exact inner product is preserved by the scalar lift. -/
theorem inner_castSeq (f g : Carrier) :
    inner 𝕜 (castSeq 𝕜 f) (castSeq 𝕜 g) = (qinner f g : 𝕜) := by
  rw [inner_def]
  unfold preInner castSeq
  rw [Finsupp.sum_mapRange_index (fun _ => by simp)]
  unfold qinner Finsupp.sum
  rw [Rat.cast_sum]
  refine Finset.sum_congr rfl fun i _ => ?_
  simp only [Finsupp.mapRange_apply, map_ratCast, Rat.cast_mul]

theorem norm_castSeq_sq (f : Carrier) : ‖castSeq 𝕜 f‖ ^ 2 = (qinner f f : ℝ) := by
  rw [norm_sq_eq_re_inner (𝕜 := 𝕜), inner_castSeq, ← RCLike.ofReal_ratCast, RCLike.ofReal_re]

variable (𝕜) in
/-- The explicit embedding of the exact carrier into the Hilbert lift. -/
noncomputable def lift (f : Carrier) : HilbertLiftSpace 𝕜 := ((castSeq 𝕜 f : PreH 𝕜) : Completion (PreH 𝕜))

variable (𝕜) in
/-- The embedding of a finite stage. -/
noncomputable def liftFin {n : ℕ} (x : FinCarrier n) : HilbertLiftSpace 𝕜 := lift 𝕜 (ofFin x)

/-- Compatibility with zero padding: the finite stages form a cocone over the lift. -/
theorem liftFin_pad {n m : ℕ} (h : n ≤ m) (x : FinCarrier n) :
    liftFin 𝕜 (pad h x) = liftFin 𝕜 x := by
  unfold liftFin
  rw [ofFin_pad]

/-- The exact inner product is preserved by the lift. -/
theorem inner_lift (f g : Carrier) : inner 𝕜 (lift 𝕜 f) (lift 𝕜 g) = (qinner f g : 𝕜) := by
  unfold lift
  rw [Completion.inner_coe, inner_castSeq]

theorem inner_liftFin {n : ℕ} (x y : FinCarrier n) :
    inner 𝕜 (liftFin 𝕜 x) (liftFin 𝕜 y) = (finInner x y : 𝕜) := by
  unfold liftFin
  rw [inner_lift, qinner_ofFin]

theorem norm_lift_sq (f : Carrier) : ‖lift 𝕜 f‖ ^ 2 = (qinner f f : ℝ) := by
  unfold lift
  rw [Completion.norm_coe, norm_castSeq_sq]

theorem lift_sub (f g : Carrier) : lift 𝕜 (f - g) = lift 𝕜 f - lift 𝕜 g := by
  unfold lift
  rw [castSeq_sub, Completion.coe_sub]

theorem lift_add (f g : Carrier) : lift 𝕜 (f + g) = lift 𝕜 f + lift 𝕜 g := by
  unfold lift
  rw [castSeq_add, Completion.coe_add]

theorem lift_smul (q : ℚ) (f : Carrier) : lift 𝕜 (q • f) = (q : 𝕜) • lift 𝕜 f := by
  unfold lift
  rw [castSeq_smul, Completion.coe_smul]

/-- The squared distance in the lift is the exact rational squared distance. -/
theorem dist_lift_sq (f g : Carrier) : dist (lift 𝕜 f) (lift 𝕜 g) ^ 2 = (sqdist f g : ℝ) := by
  rw [dist_eq_norm, ← lift_sub, norm_lift_sq]
  rfl

theorem lift_injective : Function.Injective (lift 𝕜) := by
  intro f g h
  have h1 : dist (lift 𝕜 f) (lift 𝕜 g) = 0 := by rw [h, dist_self]
  have h2 : (sqdist f g : ℝ) = 0 := by rw [← dist_lift_sq (𝕜 := 𝕜), h1, zero_pow two_ne_zero]
  have h3 : sqdist f g = 0 := by exact_mod_cast h2
  have h4 : f - g = 0 := (qinner_self_eq_zero_iff (f - g)).mp h3
  exact sub_eq_zero.mp h4

theorem liftFin_injective {n : ℕ} : Function.Injective (liftFin 𝕜 (n := n)) :=
  fun _ _ h => ofFin_injective (lift_injective h)

theorem lt_of_sq_lt {a b : ℝ} (ha : 0 ≤ a) (hb : 0 ≤ b) (h : a ^ 2 < b ^ 2) : a < b := by
  have h1 := abs_lt_of_sq_lt_sq h hb
  rwa [abs_of_nonneg ha] at h1

/-- Topology control: a sequence of exact vectors is Cauchy in the lift exactly when it is
ℓ²-Cauchy with rational tolerances. -/
theorem cauchySeq_lift_iff (x : ℕ → Carrier) :
    CauchySeq (fun n => lift 𝕜 (x n)) ↔ IsCauchyL2 x := by
  rw [Metric.cauchySeq_iff]
  constructor
  · intro h ε hε
    have hε' : (0 : ℝ) < ε := by exact_mod_cast hε
    obtain ⟨N, hN⟩ := h (Real.sqrt ε) (Real.sqrt_pos.mpr hε')
    refine ⟨N, fun m hm n hn => ?_⟩
    have h1 := hN m hm n hn
    have h2 := (Real.lt_sqrt dist_nonneg).mp h1
    rw [dist_lift_sq] at h2
    exact_mod_cast h2
  · intro h ε hε
    obtain ⟨δ, hδ0, hδ⟩ := exists_rat_btwn (pow_pos hε 2)
    obtain ⟨N, hN⟩ := h δ (by exact_mod_cast hδ0)
    refine ⟨N, fun m hm n hn => ?_⟩
    have h1 : (sqdist (x m) (x n) : ℝ) < δ := by exact_mod_cast hN m hm n hn
    have h2 : dist (lift 𝕜 (x m)) (lift 𝕜 (x n)) ^ 2 < ε ^ 2 := by
      rw [dist_lift_sq]
      linarith
    exact lt_of_sq_lt dist_nonneg hε.le h2

/-- Convergence to an exact vector in the lift is ℓ² convergence with rational tolerances. -/
theorem tendsto_lift_iff (x : ℕ → Carrier) (f : Carrier) :
    Tendsto (fun n => lift 𝕜 (x n)) atTop (𝓝 (lift 𝕜 f)) ↔ TendsToL2 x f := by
  rw [Metric.tendsto_atTop]
  constructor
  · intro h ε hε
    have hε' : (0 : ℝ) < ε := by exact_mod_cast hε
    obtain ⟨N, hN⟩ := h (Real.sqrt ε) (Real.sqrt_pos.mpr hε')
    refine ⟨N, fun n hn => ?_⟩
    have h1 := hN n hn
    have h2 := (Real.lt_sqrt dist_nonneg).mp h1
    rw [dist_lift_sq] at h2
    exact_mod_cast h2
  · intro h ε hε
    obtain ⟨δ, hδ0, hδ⟩ := exists_rat_btwn (pow_pos hε 2)
    obtain ⟨N, hN⟩ := h δ (by exact_mod_cast hδ0)
    refine ⟨N, fun n hn => ?_⟩
    have h1 : (sqdist (x n) f : ℝ) < δ := by exact_mod_cast hN n hn
    have h2 : dist (lift 𝕜 (x n)) (lift 𝕜 f) ^ 2 < ε ^ 2 := by
      rw [dist_lift_sq]
      linarith
    exact lt_of_sq_lt dist_nonneg hε.le h2

/-- Convergence hypothesis discharged: every ℓ²-Cauchy sequence of exact vectors has a limit in
the lift. -/
theorem exists_limit_of_isCauchyL2 (x : ℕ → Carrier) (hx : IsCauchyL2 x) :
    ∃ h : HilbertLiftSpace 𝕜, Tendsto (fun n => lift 𝕜 (x n)) atTop (𝓝 h) :=
  cauchySeq_tendsto_of_complete ((cauchySeq_lift_iff x).mpr hx)

theorem limit_unique (x : ℕ → Carrier) {h₁ h₂ : HilbertLiftSpace 𝕜}
    (H₁ : Tendsto (fun n => lift 𝕜 (x n)) atTop (𝓝 h₁))
    (H₂ : Tendsto (fun n => lift 𝕜 (x n)) atTop (𝓝 h₂)) : h₁ = h₂ :=
  tendsto_nhds_unique H₁ H₂

theorem isCauchyL2_of_tendsto (x : ℕ → Carrier) {h : HilbertLiftSpace 𝕜}
    (H : Tendsto (fun n => lift 𝕜 (x n)) atTop (𝓝 h)) : IsCauchyL2 x :=
  (cauchySeq_lift_iff x).mp H.cauchySeq

/-- Every ℓ²-Cauchy sequence with an exact limit converges to it in the lift. -/
theorem tendsto_lift_of_tendsToL2 (x : ℕ → Carrier) (f : Carrier) (h : TendsToL2 x f) :
    Tendsto (fun n => lift 𝕜 (x n)) atTop (𝓝 (lift 𝕜 f)) :=
  (tendsto_lift_iff x f).mpr h

end Scalars

section Real

theorem norm_sq_eq_sum_real (g : PreH ℝ) {s : Finset ℕ} (hs : g.support ⊆ s) :
    ‖g‖ ^ 2 = ∑ i ∈ s, (g i) ^ 2 := by
  rw [norm_sq_eq_re_inner (𝕜 := ℝ), inner_def, re_preInner_self g hs]
  simp only [Real.norm_eq_abs, sq_abs]

/-- Density of the exact rational carrier in the real pre-Hilbert carrier. -/
theorem denseRange_castSeq_real : DenseRange (castSeq ℝ) := by
  classical
  rw [Metric.denseRange_iff]
  intro f r hr
  set s := f.support with hs
  have hδpos : 0 < r / ((s.card : ℝ) + 1) := by positivity
  have hq : ∀ i, ∃ q : ℚ, |f i - q| < r / ((s.card : ℝ) + 1) :=
    fun i => exists_rat_near (f i) hδpos
  choose qf hqf using hq
  refine ⟨Finsupp.onFinset s (fun i => if i ∈ s then qf i else 0) fun i hi => ?_, ?_⟩
  · by_contra h
    exact hi (if_neg h)
  set q : Carrier := Finsupp.onFinset s (fun i => if i ∈ s then qf i else 0) fun i hi => by
    by_contra h
    exact hi (if_neg h) with hqdef
  have hsupp : (f - castSeq ℝ q).support ⊆ s := by
    refine Finsupp.support_sub.trans (Finset.union_subset (subset_refl _) ?_)
    exact (support_castSeq_subset q).trans Finsupp.support_onFinset_subset
  have hterm : ∀ i ∈ s, ((f - castSeq ℝ q) i) ^ 2 < (r / ((s.card : ℝ) + 1)) ^ 2 := by
    intro i hi
    have h1 : (f - castSeq ℝ q) i = f i - qf i := by
      rw [Finsupp.sub_apply, castSeq_apply, hqdef, Finsupp.onFinset_apply, if_pos hi]
    rw [h1]
    have h2 := abs_lt.mp (hqf i)
    exact sq_lt_sq' h2.1 h2.2
  have hsq : ‖f - castSeq ℝ q‖ ^ 2 < r ^ 2 := by
    rw [norm_sq_eq_sum_real _ hsupp]
    rcases s.eq_empty_or_nonempty with he | hne
    · rw [he, Finset.sum_empty]
      positivity
    · have hk : (0 : ℝ) < (s.card : ℝ) ^ 2 + s.card + 1 := by positivity
      calc ∑ i ∈ s, ((f - castSeq ℝ q) i) ^ 2
          < ∑ _i ∈ s, (r / ((s.card : ℝ) + 1)) ^ 2 := Finset.sum_lt_sum_of_nonempty hne hterm
        _ = (s.card : ℝ) * (r / ((s.card : ℝ) + 1)) ^ 2 := by
          rw [Finset.sum_const, nsmul_eq_mul]
        _ < r ^ 2 := by
          rw [div_pow, mul_div_assoc', div_lt_iff₀ (by positivity)]
          nlinarith [mul_pos (pow_pos hr 2) hk]
  rw [dist_eq_norm]
  exact lt_of_sq_lt (norm_nonneg _) hr.le hsq

/-- Density of the exact carrier in the real Hilbert lift. -/
theorem denseRange_lift_real : DenseRange (lift ℝ) :=
  Completion.denseRange_coe.comp denseRange_castSeq_real (Completion.continuous_coe _)

/-- Every element of the real lift is the limit of an ℓ²-Cauchy sequence of exact vectors. -/
theorem exists_exact_tendsto (h : HilbertLiftSpace ℝ) :
    ∃ x : ℕ → Carrier, IsCauchyL2 x ∧ Tendsto (fun n => lift ℝ (x n)) atTop (𝓝 h) := by
  have hmem : h ∈ closure (Set.range (lift ℝ)) := by
    rw [denseRange_lift_real.closure_range]
    trivial
  rw [mem_closure_iff_seq_limit] at hmem
  obtain ⟨u, hu, hlim⟩ := hmem
  choose x hx using hu
  have hux : (fun n => lift ℝ (x n)) = u := funext hx
  refine ⟨x, ?_, hux ▸ hlim⟩
  exact isCauchyL2_of_tendsto x (hux ▸ hlim)

/-- Control: a continuous map out of the real lift is determined by its values on exact
vectors. -/
theorem ext_of_lift {Y : Type*} [TopologicalSpace Y] [T2Space Y] {F G : HilbertLiftSpace ℝ → Y}
    (hF : Continuous F) (hG : Continuous G) (h : ∀ f : Carrier, F (lift ℝ f) = G (lift ℝ f)) :
    F = G :=
  denseRange_lift_real.equalizer hF hG (funext h)

/-- Strictness: the limit of the harmonic witness is not an exact vector. -/
theorem exists_not_mem_range_lift : ∃ h : HilbertLiftSpace ℝ, h ∉ Set.range (lift ℝ) := by
  obtain ⟨h, hh⟩ := exists_limit_of_isCauchyL2 (𝕜 := ℝ) harmonic harmonic_isCauchyL2
  refine ⟨h, ?_⟩
  rintro ⟨f, rfl⟩
  exact harmonic_not_tendsTo f ((tendsto_lift_iff harmonic f).mp hh)

theorem lift_not_surjective : ¬ Function.Surjective (lift ℝ) := by
  intro hs
  obtain ⟨h, hh⟩ := exists_not_mem_range_lift
  exact hh (hs h)

/-- The controlled completion, packaged: inner-product preserving, injective, dense, with the
rational ℓ² Cauchy condition characterising Cauchy sequences, every such sequence convergent,
and the lift strictly larger than the exact carrier. -/
theorem controlled_completion :
    (∀ f g : Carrier, inner ℝ (lift ℝ f) (lift ℝ g) = (qinner f g : ℝ)) ∧
    Function.Injective (lift ℝ) ∧
    DenseRange (lift ℝ) ∧
    (∀ x : ℕ → Carrier, CauchySeq (fun n => lift ℝ (x n)) ↔ IsCauchyL2 x) ∧
    (∀ x : ℕ → Carrier, IsCauchyL2 x → ∃ h : HilbertLiftSpace ℝ,
      Tendsto (fun n => lift ℝ (x n)) atTop (𝓝 h)) ∧
    ¬ Function.Surjective (lift ℝ) :=
  ⟨inner_lift, lift_injective, denseRange_lift_real, cauchySeq_lift_iff,
    exists_limit_of_isCauchyL2, lift_not_surjective⟩

end Real

end HilbertLift

#print axioms HilbertLift.preInner_conj_symm
#print axioms HilbertLift.preInner_add_left
#print axioms HilbertLift.preInner_smul_left
#print axioms HilbertLift.re_preInner_self
#print axioms HilbertLift.re_preInner_self_nonneg
#print axioms HilbertLift.preInner_self_eq_zero
#print axioms HilbertLift.hilbertLiftSpace_complete
#print axioms HilbertLift.hilbertLiftSpace_innerProductSpace
#print axioms HilbertLift.castSeq_sub
#print axioms HilbertLift.castSeq_add
#print axioms HilbertLift.castSeq_smul
#print axioms HilbertLift.castSeq_injective
#print axioms HilbertLift.inner_castSeq
#print axioms HilbertLift.norm_castSeq_sq
#print axioms HilbertLift.liftFin_pad
#print axioms HilbertLift.inner_lift
#print axioms HilbertLift.inner_liftFin
#print axioms HilbertLift.norm_lift_sq
#print axioms HilbertLift.lift_sub
#print axioms HilbertLift.lift_add
#print axioms HilbertLift.lift_smul
#print axioms HilbertLift.dist_lift_sq
#print axioms HilbertLift.lift_injective
#print axioms HilbertLift.liftFin_injective
#print axioms HilbertLift.cauchySeq_lift_iff
#print axioms HilbertLift.tendsto_lift_iff
#print axioms HilbertLift.exists_limit_of_isCauchyL2
#print axioms HilbertLift.limit_unique
#print axioms HilbertLift.isCauchyL2_of_tendsto
#print axioms HilbertLift.tendsto_lift_of_tendsToL2
#print axioms HilbertLift.norm_sq_eq_sum_real
#print axioms HilbertLift.denseRange_castSeq_real
#print axioms HilbertLift.denseRange_lift_real
#print axioms HilbertLift.exists_exact_tendsto
#print axioms HilbertLift.ext_of_lift
#print axioms HilbertLift.exists_not_mem_range_lift
#print axioms HilbertLift.lift_not_surjective
#print axioms HilbertLift.controlled_completion
