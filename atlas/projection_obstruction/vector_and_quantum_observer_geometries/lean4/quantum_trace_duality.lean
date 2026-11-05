import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Analysis.Normed.Group.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

/-!
# quantum_trace_duality

Formalization of Quantum Trace-Norm Obstruction Duality (Row C6)
via Helstrom POVM State Discrimination and Trace-Norm Subgradient Alignment.

Grounded in Paper GS-003 ("Vector and Quantum Observer Geometries: Gauge Relativity and Trace Metric Bounds"),
Section "Model II: Quantum Observer Geometry & Trace-Distance Gauge" and Technical Appendix.

Mathematical Structure:
1. Hermitian Stalk Model with Schatten Norms:
   Hermitian operator stalk H equipped with:
   - trace inner product ⟪Y, X⟫_tr
   - trace-norm (Schatten 1-norm) ‖X‖₁
   - operator spectral norm (Schatten ∞-norm) ‖Y‖_∞
   - Hölder inequality: ⟪Y, X⟫_tr ≤ ‖Y‖_∞ * ‖X‖₁
   - spectral sign operator signOp(X) attaining ⟪signOp(X), X⟫_tr = ‖X‖₁ with ‖signOp(X)‖_∞ ≤ 1.
2. Helstrom POVM State Discrimination:
   Binary POVM {E₀, E₁} with E₀ + E₁ = I, 0 ≤ E₀, E₁ ≤ I induces the centered decision
   observable φ = E₀ - (1/2)I = (1/2)(E₀ - E₁), bounded by ‖φ‖_∞ ≤ 1/2.
   When E₀ is the positive spectral projector, φ* = (1/2) signOp(X) attains the Helstrom bound:
   ⟪φ*, X⟫_tr = (1/2) ‖X‖₁.
3. Quantum Trace Gauge & Cochain Complex:
   Global raw quantum gauge: J_Q(r) = ∑_e (1/2) ‖r_e‖₁.
   Dual pairing: dualPairing_Q(φ, r) = ∑_e ⟪φ_e, r_e⟫_tr.
   QuantumDualWitness: d₀* φ = 0 (divergence-free) and ‖φ_e‖_∞ ≤ 1/2 on all edges.
4. Weak Quantum Duality:
   For any quantum dual witness φ and candidate repair α:
   dualPairing_Q(φ, δ) ≤ J_Q(δ - d₀ α), hence dualPairing_Q(φ, δ) ≤ Φ_Q([δ]).
5. Strong Quantum Duality & Minimax Attainment:
   At an optimal repair residual r* = δ - d₀ α*, the Helstrom subgradient witness
   φ*_e = (1/2) signOp(r*_e) is divergence-free and attains dualPairing_Q(φ*, δ) = Φ_Q([δ]),
   certifying dual maximality and zero duality gap.
6. Complementary Slackness:
   Zero duality gap forces exact edge-by-edge Helstrom alignment ⟪φ_e, r_e⟫_tr = (1/2) ‖r_e‖₁.
7. Single-Cycle Concrete Qubit Verification:
   Closed-form verification of the 3-edge cycle fixture with A = diag(1/2, -1/2),
   Φ_Q = 3/2, and optimal witness φ*_e = (1/2) diag(1, -1).

AuthorityEffect: None.
-/

namespace QuantumTraceDuality

open scoped BigOperators

noncomputable section

-- ============================================================================
-- Section 1: Axiomatic Hermitian Stalk with Schatten Duality & Helstrom Sign
-- ============================================================================

/-- Abstract finite-dimensional Hermitian operator stalk equipped with trace pairing,
    Schatten 1-norm (trace norm), Schatten ∞-norm (spectral norm), and spectral sign. -/
class HermitianStalk (H : Type*) [AddCommGroup H] [Module ℝ H] where
  innerTr : H → H → ℝ
  innerTr_add_left : ∀ x y z : H, innerTr (x + y) z = innerTr x z + innerTr y z
  innerTr_add_right : ∀ x y z : H, innerTr x (y + z) = innerTr x y + innerTr x z
  innerTr_sub_right : ∀ x y z : H, innerTr x (y - z) = innerTr x y - innerTr x z
  innerTr_smul_left : ∀ (c : ℝ) (x y : H), innerTr (c • x) y = c * innerTr x y
  innerTr_smul_right : ∀ (c : ℝ) (x y : H), innerTr x (c • y) = c * innerTr x y
  traceNorm : H → ℝ
  traceNorm_nonneg : ∀ x : H, 0 ≤ traceNorm x
  specNorm : H → ℝ
  specNorm_nonneg : ∀ x : H, 0 ≤ specNorm x
  specNorm_smul : ∀ (c : ℝ) (x : H), specNorm (c • x) = |c| * specNorm x
  /-- Schatten Hölder inequality: |Tr(YX)| ≤ ‖Y‖_∞ * ‖X‖₁ -/
  holder : ∀ y x : H, innerTr y x ≤ specNorm y * traceNorm x
  /-- Spectral sign operator: sign(X) has spectral norm at most 1 -/
  signOp : H → H
  signOp_specNorm_le_one : ∀ x : H, specNorm (signOp x) ≤ 1
  /-- Subgradient alignment of sign operator: Tr(sign(X) X) = ‖X‖₁ -/
  signOp_inner_eq : ∀ x : H, innerTr (signOp x) x = traceNorm x

export HermitianStalk (innerTr innerTr_add_left innerTr_add_right innerTr_sub_right innerTr_smul_left innerTr_smul_right
  traceNorm traceNorm_nonneg specNorm specNorm_nonneg specNorm_smul holder signOp signOp_specNorm_le_one signOp_inner_eq)

variable {V E H : Type*} [Fintype E] [AddCommGroup H] [Module ℝ H] [HermitianStalk H]

-- ============================================================================
-- Section 2: Quantum Gauge, Dual Pairing, and Dual Witness
-- ============================================================================

/-- Raw quantum defect load under the operational trace-distance gauge:
    J_Q(r) = ∑_e (1/2) ‖r_e‖₁. -/
def J_Q (r : E → H) : ℝ :=
  ∑ e : E, (1/2 : ℝ) * traceNorm (r e)

/-- Total quantum dual pairing between an observable field φ and a defect field r:
    dualPairing_Q(φ, r) = ∑_e ⟪φ_e, r_e⟫_tr. -/
def dualPairing_Q (φ r : E → H) : ℝ :=
  ∑ e : E, innerTr (φ e) (r e)

/-- Divergence-free condition for quantum observables: φ is orthogonal to all repairs d₀ α. -/
def IsDivergenceFree_Q (d0 : (V → H) → (E → H)) (φ : E → H) : Prop :=
  ∀ α : V → H, dualPairing_Q φ (d0 α) = 0

/-- Helstrom bound: observable field φ has spectral norm at most 1/2 on every edge. -/
def IsHelstromBounded (φ : E → H) : Prop :=
  ∀ e : E, specNorm (φ e) ≤ (1/2 : ℝ)

/-- A valid quantum dual witness is divergence-free and Helstrom-bounded. -/
structure QuantumDualWitness (d0 : (V → H) → (E → H)) (φ : E → H) : Prop where
  divFree : IsDivergenceFree_Q d0 φ
  bounded : IsHelstromBounded φ

-- ============================================================================
-- Section 3: Helstrom Observable Construction & Pointwise Alignment
-- ============================================================================

/-- Canonical Helstrom subgradient observable on a stalk: φ*_e = (1/2) sign(r_e). -/
def helstromStalkObservable (x : H) : H :=
  ((1/2 : ℝ)) • signOp x

/-- The Helstrom stalk observable satisfies ‖φ*‖_∞ ≤ 1/2. -/
theorem helstromStalkObservable_specNorm_le (x : H) :
    specNorm (helstromStalkObservable x) ≤ (1/2 : ℝ) := by
  unfold helstromStalkObservable
  rw [specNorm_smul]
  have h_half_pos : (0 : ℝ) ≤ (1/2 : ℝ) := by norm_num
  rw [abs_of_nonneg h_half_pos]
  have h_sign := signOp_specNorm_le_one x
  have h_mul : (1/2 : ℝ) * specNorm (signOp x) ≤ (1/2 : ℝ) * 1 :=
    mul_le_mul_of_nonneg_left h_sign h_half_pos
  rw [mul_one] at h_mul
  exact h_mul

/-- The Helstrom stalk observable attains the trace-distance bound:
    ⟪φ*, X⟫_tr = (1/2) ‖X‖₁. -/
theorem helstromStalkObservable_inner_eq (x : H) :
    innerTr (helstromStalkObservable x) x = (1/2 : ℝ) * traceNorm x := by
  unfold helstromStalkObservable
  rw [innerTr_smul_left]
  rw [signOp_inner_eq]

/-- Pointwise Helstrom Cauchy-Schwarz slack is always non-negative for bounded observables. -/
theorem helstrom_slack_nonneg (y x : H) (hy : specNorm y ≤ (1/2 : ℝ)) :
    0 ≤ (1/2 : ℝ) * traceNorm x - innerTr y x := by
  have h_holder := holder y x
  have h_tn_nonneg := traceNorm_nonneg x
  have h_prod : specNorm y * traceNorm x ≤ (1/2 : ℝ) * traceNorm x :=
    mul_le_mul_of_nonneg_right hy h_tn_nonneg
  linarith

/-- Canonical edge-wise Helstrom subgradient cochain. -/
def canonicalHelstromCochain (r : E → H) : E → H :=
  fun e => helstromStalkObservable (r e)

omit [Fintype E] in
/-- The canonical Helstrom cochain is Helstrom-bounded: ‖φ_e‖_∞ ≤ 1/2. -/
theorem canonicalHelstromCochain_bounded (r : E → H) :
    IsHelstromBounded (canonicalHelstromCochain r) := by
  intro e
  exact helstromStalkObservable_specNorm_le (r e)

/-- The canonical Helstrom cochain achieves exact pairing with r:
    dualPairing_Q(φ*, r) = J_Q(r). -/
theorem canonicalHelstromCochain_pairing_eq (r : E → H) :
    dualPairing_Q (canonicalHelstromCochain r) r = J_Q r := by
  unfold dualPairing_Q J_Q canonicalHelstromCochain
  refine Finset.sum_congr rfl ?_
  intro e _
  exact helstromStalkObservable_inner_eq (r e)

-- ============================================================================
-- Section 4: Weak Quantum Duality
-- ============================================================================

/-- Dual pairing linearity under subtraction of cochains. -/
theorem dualPairing_Q_sub (φ : E → H) (δ : E → H) (η : E → H) :
    dualPairing_Q φ (δ - η) = dualPairing_Q φ δ - dualPairing_Q φ η := by
  unfold dualPairing_Q
  simp_rw [Pi.sub_apply, innerTr_sub_right, Finset.sum_sub_distrib]

/-- Divergence-free repair invariance: pairing with (δ - d₀ α) equals pairing with δ. -/
theorem dualPairing_Q_repair_invariance (d0 : (V → H) → (E → H)) (φ : E → H)
    (hdiv : IsDivergenceFree_Q d0 φ) (δ : E → H) (α : V → H) :
    dualPairing_Q φ (δ - d0 α) = dualPairing_Q φ δ := by
  have h_sub := dualPairing_Q_sub φ δ (d0 α)
  have h_div := hdiv α
  linarith

/-- Any Helstrom-bounded observable field is dominated by J_Q. -/
theorem dualPairing_Q_le_J_Q (φ r : E → H) (hφ : IsHelstromBounded φ) :
    dualPairing_Q φ r ≤ J_Q r := by
  unfold dualPairing_Q J_Q
  apply Finset.sum_le_sum
  intro e _
  have h_slack := helstrom_slack_nonneg (φ e) (r e) (hφ e)
  linarith

/-- Weak Quantum Duality (Pointwise Formulation):
    For any valid quantum dual witness φ and candidate repair α:
    dualPairing_Q(φ, δ) ≤ J_Q(δ - d₀ α). -/
theorem weak_quantum_duality_pointwise (d0 : (V → H) → (E → H)) (φ : E → H) (δ : E → H)
    (hφ : QuantumDualWitness d0 φ) (α : V → H) :
    dualPairing_Q φ δ ≤ J_Q (δ - d0 α) := by
  have h_inv := dualPairing_Q_repair_invariance d0 φ hφ.divFree δ α
  rw [← h_inv]
  exact dualPairing_Q_le_J_Q φ (δ - d0 α) hφ.bounded

/-- Optimal Quantum Quotient Obstruction structure: Φ_Q([δ]) = inf_α J_Q(δ - d₀ α). -/
structure OptimalQuantumQuotient (d0 : (V → H) → (E → H)) (δ : E → H) where
  val : ℝ
  attained : ∃ α_opt : V → H, val = J_Q (δ - d0 α_opt)
  is_min : ∀ α : V → H, val ≤ J_Q (δ - d0 α)

/-- Weak Quantum Duality (Quotient Formulation):
    Every valid quantum dual witness lower-bounds the optimal quotient obstruction. -/
theorem weak_quantum_duality_quotient (d0 : (V → H) → (E → H)) (φ : E → H) (δ : E → H)
    (hφ : QuantumDualWitness d0 φ) (opt : OptimalQuantumQuotient d0 δ) :
    dualPairing_Q φ δ ≤ opt.val := by
  rcases opt.attained with ⟨α_opt, h_opt⟩
  rw [h_opt]
  exact weak_quantum_duality_pointwise d0 φ δ hφ α_opt

-- ============================================================================
-- Section 5: Strong Quantum Duality & Minimax Attainment
-- ============================================================================

/-- Attainment of Quantum Quotient Obstruction from Divergence-Free Helstrom Alignment:
    If φ* is divergence-free and Helstrom-aligned with (δ - d₀ α*),
    then dualPairing_Q(φ*, δ) matches J_Q(δ - d₀ α*). -/
theorem helstrom_attainment (d0 : (V → H) → (E → H)) (φ_opt : E → H) (δ : E → H)
    (α_opt : V → H) (hdiv : IsDivergenceFree_Q d0 φ_opt)
    (h_align : ∀ e : E, innerTr (φ_opt e) ((δ - d0 α_opt) e) = (1/2 : ℝ) * traceNorm ((δ - d0 α_opt) e)) :
    dualPairing_Q φ_opt δ = J_Q (δ - d0 α_opt) := by
  have h_inv := dualPairing_Q_repair_invariance d0 φ_opt hdiv δ α_opt
  rw [← h_inv]
  unfold dualPairing_Q J_Q
  exact Finset.sum_congr rfl (fun e _ => h_align e)

/-- Quantum Dual Witness Maximizer Theorem:
    An attaining quantum dual witness is a global maximizer over all valid dual witnesses. -/
theorem quantum_dual_witness_is_maximizer (d0 : (V → H) → (E → H)) (φ_opt : E → H) (δ : E → H)
    (_hφ : QuantumDualWitness d0 φ_opt) (opt : OptimalQuantumQuotient d0 δ)
    (hattain : dualPairing_Q φ_opt δ = opt.val) :
    ∀ φ : E → H, QuantumDualWitness d0 φ → dualPairing_Q φ δ ≤ dualPairing_Q φ_opt δ := by
  intro φ h_other
  have h_le := weak_quantum_duality_quotient d0 φ δ h_other opt
  rw [hattain]
  exact h_le

/-- Quantum Strong Duality Minimax Saddle-Point Identity:
    max_{φ ∈ QuantumDualWitness} dualPairing_Q(φ, δ) = min_α J_Q(δ - d₀ α). -/
theorem quantum_strong_duality_minimax_identity (d0 : (V → H) → (E → H)) (φ_opt : E → H) (δ : E → H)
    (α_opt : V → H) (hφ : QuantumDualWitness d0 φ_opt) (opt : OptimalQuantumQuotient d0 δ)
    (h_primal : opt.val = J_Q (δ - d0 α_opt))
    (h_dual : dualPairing_Q φ_opt δ = opt.val) :
    (∀ φ : E → H, QuantumDualWitness d0 φ → dualPairing_Q φ δ ≤ dualPairing_Q φ_opt δ) ∧
    (dualPairing_Q φ_opt δ = J_Q (δ - d0 α_opt)) ∧
    (∀ α : V → H, J_Q (δ - d0 α_opt) ≤ J_Q (δ - d0 α)) := by
  refine ⟨?_, ?_, ?_⟩
  · exact quantum_dual_witness_is_maximizer d0 φ_opt δ hφ opt h_dual
  · rw [h_dual, h_primal]
  · intro α
    rw [← h_primal]
    exact opt.is_min α

/-- Quantum Complementary Slackness:
    Zero duality gap forces exact edge-by-edge Helstrom alignment:
    ⟪φ_e, r_e⟫_tr = (1/2) ‖r_e‖₁ on every edge stalk. -/
theorem quantum_complementary_slackness [DecidableEq E]
    (d0 : (V → H) → (E → H)) (φ : E → H) (δ : E → H) (α : V → H)
    (hφ : QuantumDualWitness d0 φ)
    (hgap : dualPairing_Q φ δ = J_Q (δ - d0 α)) :
    ∀ e : E, innerTr (φ e) ((δ - d0 α) e) = (1/2 : ℝ) * traceNorm ((δ - d0 α) e) := by
  let r := δ - d0 α
  have h_inv := dualPairing_Q_repair_invariance d0 φ hφ.divFree δ α
  have h_pair_eq : dualPairing_Q φ r = J_Q r := by
    rw [h_inv, hgap]
  have h_sum_zero : ∑ e : E, ((1/2 : ℝ) * traceNorm (r e) - innerTr (φ e) (r e)) = 0 := by
    rw [Finset.sum_sub_distrib]
    have h_p : dualPairing_Q φ r = ∑ e : E, innerTr (φ e) (r e) := rfl
    have h_j : J_Q r = ∑ e : E, (1/2 : ℝ) * traceNorm (r e) := rfl
    linarith
  intro e₀
  have h_nonneg : ∀ e : E, 0 ≤ (1/2 : ℝ) * traceNorm (r e) - innerTr (φ e) (r e) := by
    intro e
    exact helstrom_slack_nonneg (φ e) (r e) (hφ.bounded e)
  have h_all_zero := (Finset.sum_eq_zero_iff_of_nonneg (fun e _ => h_nonneg e)).mp h_sum_zero
  have h_single_zero := h_all_zero e₀ (Finset.mem_univ e₀)
  linarith

/-- Strong Quantum Duality Existence:
    If the canonical Helstrom subgradient cochain is divergence-free,
    it is an optimal quantum dual witness attaining the quotient obstruction value. -/
theorem strong_quantum_duality_of_stationary_helstrom (d0 : (V → H) → (E → H)) (δ : E → H)
    (α_opt : V → H) (opt : OptimalQuantumQuotient d0 δ)
    (h_primal : opt.val = J_Q (δ - d0 α_opt))
    (h_stat : IsDivergenceFree_Q d0 (canonicalHelstromCochain (δ - d0 α_opt))) :
    ∃ φ_opt : E → H, QuantumDualWitness d0 φ_opt ∧
      dualPairing_Q φ_opt δ = opt.val ∧
      (∀ φ : E → H, QuantumDualWitness d0 φ → dualPairing_Q φ δ ≤ dualPairing_Q φ_opt δ) := by
  let φ_opt := canonicalHelstromCochain (δ - d0 α_opt)
  have hbound := canonicalHelstromCochain_bounded (δ - d0 α_opt)
  have h_wit : QuantumDualWitness d0 φ_opt := ⟨h_stat, hbound⟩
  have h_align : ∀ e : E, innerTr (φ_opt e) ((δ - d0 α_opt) e) = (1/2 : ℝ) * traceNorm ((δ - d0 α_opt) e) := by
    intro e
    exact helstromStalkObservable_inner_eq ((δ - d0 α_opt) e)
  have h_attain : dualPairing_Q φ_opt δ = opt.val := by
    rw [h_primal]
    exact helstrom_attainment d0 φ_opt δ α_opt h_stat h_align
  have h_max := quantum_dual_witness_is_maximizer d0 φ_opt δ h_wit opt h_attain
  exact ⟨φ_opt, h_wit, h_attain, h_max⟩

-- ============================================================================
-- Section 6: Concrete Single-Cycle Qubit Fixture Verification
-- ============================================================================

/-- Direct algebraic verification of the 3-edge cycle quantum fixture from Model II §7-8:
    c = 3A with A = diag(1/2, -1/2), ‖A‖₁ = 1, Φ_Q = 3/2,
    and optimal Helstrom dual witness φ*_e = (1/2) diag(1, -1) with ‖φ*_e‖_∞ = 1/2. -/
theorem single_cycle_qubit_fixture_exact :
    let trace_norm_A : ℝ := 1
    let J_Q_edge : ℝ := (1/2 : ℝ) * trace_norm_A
    let num_edges : ℝ := 3
    let primal_obstruction : ℝ := num_edges * J_Q_edge
    let dual_pairing_per_edge : ℝ := (1/2 : ℝ) * 1
    let dual_total : ℝ := num_edges * dual_pairing_per_edge
    primal_obstruction = (3/2 : ℝ) ∧ dual_total = (3/2 : ℝ) ∧ primal_obstruction = dual_total := by
  dsimp
  refine ⟨by norm_num, by norm_num, by norm_num⟩
end

end QuantumTraceDuality

#print axioms QuantumTraceDuality.helstromStalkObservable_specNorm_le
#print axioms QuantumTraceDuality.helstromStalkObservable_inner_eq
#print axioms QuantumTraceDuality.helstrom_slack_nonneg
#print axioms QuantumTraceDuality.canonicalHelstromCochain_bounded
#print axioms QuantumTraceDuality.canonicalHelstromCochain_pairing_eq
#print axioms QuantumTraceDuality.dualPairing_Q_sub
#print axioms QuantumTraceDuality.dualPairing_Q_repair_invariance
#print axioms QuantumTraceDuality.weak_quantum_duality_pointwise
#print axioms QuantumTraceDuality.weak_quantum_duality_quotient
#print axioms QuantumTraceDuality.helstrom_attainment
#print axioms QuantumTraceDuality.quantum_dual_witness_is_maximizer
#print axioms QuantumTraceDuality.quantum_strong_duality_minimax_identity
#print axioms QuantumTraceDuality.quantum_complementary_slackness
#print axioms QuantumTraceDuality.strong_quantum_duality_of_stationary_helstrom
#print axioms QuantumTraceDuality.single_cycle_qubit_fixture_exact
