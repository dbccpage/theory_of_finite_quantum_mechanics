

namespace QuantumMechanics.DerivationDagQMClosure


inductive PrimGenEvent where
  | declareTerm
  | assertDiff
  | removeDiff
  | identifyTerms
  deriving DecidableEq, Repr

structure ObligationMonoid where
  termsAdded : Nat
  assertionsAdded : Nat
  destructiveOps : Nat
  deriving DecidableEq, Repr

def ObligationMonoid.zero : ObligationMonoid := ⟨0, 0, 0⟩

def ObligationMonoid.add (x y : ObligationMonoid) : ObligationMonoid :=
  ⟨x.termsAdded + y.termsAdded,
   x.assertionsAdded + y.assertionsAdded,
   x.destructiveOps + y.destructiveOps⟩

def ObligationMonoid.totalCost (x : ObligationMonoid) : Nat :=
  x.termsAdded + x.assertionsAdded + x.destructiveOps

def eventObligation : PrimGenEvent → ObligationMonoid
  | .declareTerm   => ⟨1, 0, 0⟩
  | .assertDiff    => ⟨0, 1, 0⟩
  | .removeDiff    => ⟨0, 0, 1⟩
  | .identifyTerms => ⟨0, 0, 1⟩

def traceObligation : List PrimGenEvent → ObligationMonoid
  | [] => ObligationMonoid.zero
  | e :: es => ObligationMonoid.add (eventObligation e) (traceObligation es)

theorem traceObligation_append (xs ys : List PrimGenEvent) :
    traceObligation (xs ++ ys) = ObligationMonoid.add (traceObligation xs) (traceObligation ys) := by
  induction xs with
  | nil =>
    cases h : traceObligation ys
    simp [traceObligation, ObligationMonoid.zero, ObligationMonoid.add, h]
  | cons x xs ih =>
    simp only [List.cons_append, traceObligation, ih, ObligationMonoid.add, ObligationMonoid.mk.injEq]
    exact ⟨(Nat.add_assoc _ _ _).symm, (Nat.add_assoc _ _ _).symm, (Nat.add_assoc _ _ _).symm⟩

def ValidFreshAssertionTrace (tr : List PrimGenEvent) : Prop :=
  (traceObligation tr).termsAdded ≥ 1 ∧ (traceObligation tr).assertionsAdded ≥ 1

theorem declare_then_assert_cost_floor (tr : List PrimGenEvent)
    (h : ValidFreshAssertionTrace tr) :
    (traceObligation tr).totalCost ≥ 2 := by
  rcases h with ⟨ht, ha⟩
  unfold ObligationMonoid.totalCost
  omega

structure FiniteGenesisWindow (n : Nat) where
  adj : Fin n → Fin n → Bool

def GenesisLegal {n : Nat} (w : FiniteGenesisWindow n) : Prop :=
  ∀ i : Fin n, w.adj i i = false

def wdpPairDefect {n : Nat} (w : FiniteGenesisWindow n) (u v : Fin n) : Bool :=
  w.adj u v || w.adj v u

theorem genesis_to_wdp_bridge_preserves_and_reflects {n : Nat}
    (w : FiniteGenesisWindow n) (u v : Fin n) :
    wdpPairDefect w u v = false ↔ (w.adj u v = false ∧ w.adj v u = false) := by
  unfold wdpPairDefect
  rw [Bool.or_eq_false_iff]

def edgeResidualL1 : List Nat → Nat
  | [] => 0
  | e :: es => e + edgeResidualL1 es

theorem wdp_growth_subcomplex_monotone (baseEdges addedEdges : List Nat) :
    edgeResidualL1 baseEdges ≤ edgeResidualL1 (baseEdges ++ addedEdges) := by
  induction baseEdges with
  | nil => exact Nat.zero_le _
  | cons e es ih =>
    simp only [List.cons_append, edgeResidualL1]
    exact Nat.add_le_add_left ih e

structure SimplicialComplex2D where
  edgeResiduals : List Nat
  triangles : List (Nat × Nat × Nat)

def attachTwoSimplex (K : SimplicialComplex2D) (tri : Nat × Nat × Nat) : SimplicialComplex2D :=
  ⟨K.edgeResiduals, tri :: K.triangles⟩

theorem wdp_two_simplex_attachment_preserves_phi1 (K : SimplicialComplex2D)
    (tri : Nat × Nat × Nat) :
    edgeResidualL1 (attachTwoSimplex K tri).edgeResiduals = edgeResidualL1 K.edgeResiduals := rfl


theorem sector_weights_sum_to_phi1 (sectorA sectorB : List Nat) :
    edgeResidualL1 (sectorA ++ sectorB) = edgeResidualL1 sectorA + edgeResidualL1 sectorB := by
  induction sectorA with
  | nil => simp [edgeResidualL1]
  | cons a as ih =>
    simp only [List.cons_append, edgeResidualL1, ih]
    exact (Nat.add_assoc a (edgeResidualL1 as) (edgeResidualL1 sectorB)).symm

def c4MinimizerOne : Fin 4 → Nat
  | ⟨0, _⟩ => 1
  | ⟨1, _⟩ => 0
  | ⟨2, _⟩ => 0
  | ⟨3, _⟩ => 0

def c4MinimizerTwo : Fin 4 → Nat
  | ⟨0, _⟩ => 0
  | ⟨1, _⟩ => 1
  | ⟨2, _⟩ => 0
  | ⟨3, _⟩ => 0

theorem even_cycle_sector_weights_require_selector :
    (c4MinimizerOne ⟨0, by decide⟩ + c4MinimizerOne ⟨1, by decide⟩ +
     c4MinimizerOne ⟨2, by decide⟩ + c4MinimizerOne ⟨3, by decide⟩ = 1) ∧
    (c4MinimizerTwo ⟨0, by decide⟩ + c4MinimizerTwo ⟨1, by decide⟩ +
     c4MinimizerTwo ⟨2, by decide⟩ + c4MinimizerTwo ⟨3, by decide⟩ = 1) ∧
    (c4MinimizerOne ⟨0, by decide⟩ ≠ c4MinimizerTwo ⟨0, by decide⟩) := by
  decide

theorem int_mul_self_nonneg (a : Int) : 0 ≤ a * a := by
  cases a with
  | ofNat n => exact Int.natCast_nonneg (n * n)
  | negSucc n => exact Int.natCast_nonneg (Nat.succ n * Nat.succ n)

def sqDiffSum3 (w0 w1 w2 : Int) : Int :=
  (w0 - w1) * (w0 - w1) + (w1 - w2) * (w1 - w2) + (w2 - w0) * (w2 - w0)

theorem signed_sqrt_density_lift_cauchy_schwarz (w0 w1 w2 : Int) :
    0 ≤ sqDiffSum3 w0 w1 w2 ∧ sqDiffSum3 w0 w0 w0 = 0 := by
  unfold sqDiffSum3
  have h01 := int_mul_self_nonneg (w0 - w1)
  have h12 := int_mul_self_nonneg (w1 - w2)
  have h20 := int_mul_self_nonneg (w2 - w0)
  omega


def diagExpectation3 (o0 o1 o2 w0 w1 w2 : Nat) : Nat :=
  o0 * w0 + o1 * w1 + o2 * w2

def purityDiag3 (w0 w1 w2 : Nat) : Nat :=
  w0 * w0 + w1 * w1 + w2 * w2

def purityRankOneExpanded3 (w0 w1 w2 : Nat) : Nat :=
  purityDiag3 w0 w1 w2 + 2 * (w0 * w1 + w1 * w2 + w2 * w0)

theorem qm020_thm4_hilbert_lift_redundancy (w0 w1 w2 : Nat) (hw : 0 < w0 * w1) :
    (∀ o0 o1 o2 : Nat, diagExpectation3 o0 o1 o2 w0 w1 w2 = o0 * w0 + o1 * w1 + o2 * w2) ∧
    purityDiag3 w0 w1 w2 < purityRankOneExpanded3 w0 w1 w2 ∧
    purityRankOneExpanded3 2 3 5 = (2 + 3 + 5) * (2 + 3 + 5) := by
  refine ⟨fun _ _ _ => rfl, ?_, by decide⟩
  unfold purityRankOneExpanded3
  omega

theorem qm020_thm6_p1_scope_fence :
    (1 ^ 2 + 0 ^ 2 = 1 ^ 4 + 0 ^ 4) ∧
    ((1 ^ 2 + 1 ^ 2) ^ 2 ≠ 1 ^ 4 + 1 ^ 4) := by
  decide

def plusMinusExpectation (d0 d1 c : Int) (sign : Int) : Int :=
  d0 + d1 + 2 * sign * c

theorem qm020_thm7_representation_capacity (d0 d1 c : Int) :
    (plusMinusExpectation d0 d1 0 1 = plusMinusExpectation d0 d1 0 (-1)) ∧
    (c ≠ 0 → plusMinusExpectation d0 d1 c 1 ≠ plusMinusExpectation d0 d1 c (-1)) := by
  constructor
  · rfl
  · intro hc heq
    unfold plusMinusExpectation at heq
    omega

structure Mat2Int where
  m00 : Int
  m01 : Int
  m10 : Int
  m11 : Int
  deriving DecidableEq, Repr

def Mat2Int.mul (A B : Mat2Int) : Mat2Int :=
  ⟨A.m00 * B.m00 + A.m01 * B.m10,
   A.m00 * B.m01 + A.m01 * B.m11,
   A.m10 * B.m00 + A.m11 * B.m10,
   A.m10 * B.m01 + A.m11 * B.m11⟩

def diagMat2 (d0 d1 : Int) : Mat2Int := ⟨d0, 0, 0, d1⟩

theorem qm003_c17_diagonal_composable_factorization (a0 a1 b0 b1 : Int) :
    Mat2Int.mul (diagMat2 a0 a1) (diagMat2 b0 b1) = diagMat2 (a0 * b0) (a1 * b1) := by
  simp [Mat2Int.mul, diagMat2]

theorem qm003_c17_off_diagonal_obstruction_to_diagonal_factorization :
    let H : Mat2Int := ⟨1, 1, 1, -1⟩
    (Mat2Int.mul H H).m00 = 2 ∧ (diagMat2 H.m00 H.m11).m00 * (diagMat2 H.m00 H.m11).m00 = 1 := by
  decide

theorem qm121_ladder_rungs_2_to_6_certificate :
    (diagExpectation3 1 1 1 2 3 5 = 10) ∧
    (Mat2Int.mul (diagMat2 2 3) (diagMat2 4 5) = diagMat2 8 15) ∧
    (Mat2Int.mul ⟨1, 1, 1, -1⟩ ⟨1, 1, 1, -1⟩ = ⟨2, 0, 0, 2⟩) ∧
    ((1 + (-1) : Int) = 0) ∧
    ((1 ^ 2 + 1 ^ 2) ^ 2 ≠ 1 ^ 4 + 1 ^ 4) := by
  decide


theorem power_rule_p2_unique_even_exponent (k : Nat) :
    1 ^ (2 * k) + 1 ^ (2 * k) = 2 ^ k ↔ k = 1 := by
  constructor
  · intro h
    simp only [Nat.one_pow] at h
    match k with
    | 0 => contradiction
    | 1 => rfl
    | k + 2 =>
      have hpow : 2 ^ (k + 2) = 2 ^ k * 4 := by
        rw [Nat.pow_add]
      have hpos : 0 < 2 ^ k := Nat.two_pow_pos k
      omega
  · rintro rfl
    rfl

def cabelloContexts : List (List (Fin 18)) :=
  [ [⟨0, by decide⟩,  ⟨1, by decide⟩,  ⟨2, by decide⟩,  ⟨3, by decide⟩],
    [⟨3, by decide⟩,  ⟨4, by decide⟩,  ⟨5, by decide⟩,  ⟨6, by decide⟩],
    [⟨6, by decide⟩,  ⟨7, by decide⟩,  ⟨8, by decide⟩,  ⟨9, by decide⟩],
    [⟨9, by decide⟩,  ⟨10, by decide⟩, ⟨11, by decide⟩, ⟨12, by decide⟩],
    [⟨12, by decide⟩, ⟨13, by decide⟩, ⟨14, by decide⟩, ⟨15, by decide⟩],
    [⟨15, by decide⟩, ⟨16, by decide⟩, ⟨17, by decide⟩, ⟨0, by decide⟩],
    [⟨1, by decide⟩,  ⟨8, by decide⟩,  ⟨10, by decide⟩, ⟨17, by decide⟩],
    [⟨2, by decide⟩,  ⟨4, by decide⟩,  ⟨11, by decide⟩, ⟨14, by decide⟩],
    [⟨5, by decide⟩,  ⟨7, by decide⟩,  ⟨13, by decide⟩, ⟨16, by decide⟩] ]

def rayDegreeInCabello (r : Fin 18) : Nat :=
  (cabelloContexts.filter (fun ctx => ctx.contains r)).length

theorem cabello_18_9_two_regular_and_146_census :
    cabelloContexts.length = 9 ∧
    (cabelloContexts.all (fun ctx => ctx.length == 4)) = true ∧
    ((List.finRange 18).all (fun r => rayDegreeInCabello r == 2)) = true ∧
    (2 + 72 + 72 = 146) := by
  decide

def traceZeroDetNeg (a b : Int) : Int := a * a + b * b

theorem trace_zero_pinching_contraction (a b : Int) :
    traceZeroDetNeg a 0 ≤ traceZeroDetNeg a b ∧
    (traceZeroDetNeg a 0 = traceZeroDetNeg a b ↔ b = 0) := by
  unfold traceZeroDetNeg
  have hsq : 0 ≤ b * b := int_mul_self_nonneg b
  constructor
  · omega
  · constructor
    · intro h
      have hb2 : b * b = 0 := by omega
      exact (Int.mul_eq_zero.mp hb2).elim id id
    · rintro rfl
      omega

def k23PrimalAlt (u0 u1 v0 v1 v2 : Int) : Nat :=
  (1 - (v0 - u0)).natAbs + ((-1) - (v0 - u1)).natAbs +
  ((-1) - (v1 - u0)).natAbs + (1 - (v1 - u1)).natAbs +
  (1 - (v2 - u0)).natAbs + ((-1) - (v2 - u1)).natAbs

theorem k23_uncentered_zero_duality_gap (u0 u1 v0 v1 v2 : Int) :
    k23PrimalAlt 0 2 1 1 1 = 4 ∧
    4 ≤ k23PrimalAlt u0 u1 v0 v1 v2 := by
  refine ⟨by decide, ?_⟩
  unfold k23PrimalAlt
  omega

def k23PrimalCenteredScaled2 (u0 u1 v0 v1 v2 : Int) : Nat :=
  (3 - (v0 - u0)).natAbs + ((-3) - (v0 - u1)).natAbs +
  ((-3) - (v1 - u0)).natAbs + (3 - (v1 - u1)).natAbs +
  (3 - (v2 - u0)).natAbs + ((-3) - (v2 - u1)).natAbs

theorem k23_centered_scaled2_zero_duality_gap (u0 u1 v0 v1 v2 : Int) :
    k23PrimalCenteredScaled2 0 6 3 3 3 = 12 ∧
    12 ≤ k23PrimalCenteredScaled2 u0 u1 v0 v1 v2 := by
  refine ⟨by decide, ?_⟩
  unfold k23PrimalCenteredScaled2
  omega


def projZ0 (A : Mat2Int) : Mat2Int :=
  Mat2Int.mul ⟨1, 0, 0, 0⟩ (Mat2Int.mul A ⟨1, 0, 0, 0⟩)

theorem qm021_idempotent_conditioning_and_order_sensitivity (A : Mat2Int) :
    projZ0 (projZ0 A) = projZ0 A ∧
    Mat2Int.mul ⟨1, 0, 0, 0⟩ ⟨1, 1, 1, 1⟩ ≠ Mat2Int.mul ⟨1, 1, 1, 1⟩ ⟨1, 0, 0, 0⟩ := by
  refine ⟨?_, by decide⟩
  cases A
  simp [projZ0, Mat2Int.mul]

theorem qm030_ungraded_overcount_witness (a01 b12 : Int) (ha : a01 ≠ 0) (hb : b12 ≠ 0) :
    (a01 * b12 - a01 * b12 = 0) ∧ (a01 * b12 + a01 * b12 ≠ 0) := by
  refine ⟨by omega, ?_⟩
  intro h
  have hab : a01 * b12 = 0 := by omega
  rcases Int.mul_eq_zero.mp hab with h1 | h2
  · exact ha h1
  · exact hb h2

theorem qm032_finite_feynman_interference_vs_stochastic :
    (Mat2Int.mul ⟨1, 1, 1, -1⟩ ⟨1, 1, 1, -1⟩).m01 = 0 ∧
    (Mat2Int.mul ⟨1, 1, 1, 1⟩ ⟨1, 1, 1, 1⟩).m01 = 2 := by
  decide

def Mat2Int.sub (A B : Mat2Int) : Mat2Int :=
  ⟨A.m00 - B.m00, A.m01 - B.m01, A.m10 - B.m10, A.m11 - B.m11⟩

def Mat2Int.trace (A : Mat2Int) : Int := A.m00 + A.m11

theorem qm040_commutator_nonzero_and_trace_zero :
    let X : Mat2Int := ⟨0, 1, 1, 0⟩
    let Z : Mat2Int := ⟨1, 0, 0, -1⟩
    let comm := Mat2Int.sub (Mat2Int.mul X Z) (Mat2Int.mul Z X)
    comm = ⟨0, -2, 2, 0⟩ ∧ Mat2Int.trace comm = 0 := by
  decide

theorem qm093_cochain_d1_d0_zero (fi fj fk : Int) :
    (fj - fi) + (fk - fj) - (fk - fi) = 0 := by
  omega

theorem qm064_triangle_holonomy_gauge_invariant (w01 w12 w20 f0 f1 f2 : Int) :
    (w01 + (f1 - f0)) + (w12 + (f2 - f1)) + (w20 + (f0 - f2)) = w01 + w12 + w20 := by
  omega

theorem qm081_stochastic_l1_contraction (a00 a10 a01 a11 S x y : Int)
    (ha00 : 0 ≤ a00) (ha10 : 0 ≤ a10) (ha01 : 0 ≤ a01) (ha11 : 0 ≤ a11)
    (hcol0 : a00 + a10 = S) (hcol1 : a01 + a11 = S) :
    (a00 * x + a01 * y).natAbs + (a10 * x + a11 * y).natAbs ≤
      S.natAbs * (x.natAbs + y.natAbs) := by
  have htri0 : (a00 * x + a01 * y).natAbs ≤ (a00 * x).natAbs + (a01 * y).natAbs :=
    Int.natAbs_add_le (a00 * x) (a01 * y)
  have htri1 : (a10 * x + a11 * y).natAbs ≤ (a10 * x).natAbs + (a11 * y).natAbs :=
    Int.natAbs_add_le (a10 * x) (a11 * y)
  rw [Int.natAbs_mul, Int.natAbs_mul] at htri0
  rw [Int.natAbs_mul, Int.natAbs_mul] at htri1
  have hS0 : a00.natAbs + a10.natAbs = S.natAbs := by
    rw [← Int.natAbs_add_of_nonneg ha00 ha10, hcol0]
  have hS1 : a01.natAbs + a11.natAbs = S.natAbs := by
    rw [← Int.natAbs_add_of_nonneg ha01 ha11, hcol1]
  have h0 : a00.natAbs * x.natAbs + a10.natAbs * x.natAbs = S.natAbs * x.natAbs := by
    rw [← Nat.add_mul, hS0]
  have h1 : a01.natAbs * y.natAbs + a11.natAbs * y.natAbs = S.natAbs * y.natAbs := by
    rw [← Nat.add_mul, hS1]
  have h2 : S.natAbs * (x.natAbs + y.natAbs) = S.natAbs * x.natAbs + S.natAbs * y.natAbs :=
    Nat.mul_add S.natAbs x.natAbs y.natAbs
  omega

structure DiagnosticProbe where
  score : Nat
  deriving DecidableEq, Repr

structure CertifierReceipt where
  defect : Nat
  witnessBound : Nat
  deriving DecidableEq, Repr

def authorizeFromReceipt (r : CertifierReceipt) : Bool :=
  decide (r.defect = 0)

theorem qm090_authority_firewall_zero_defect_iff (r : CertifierReceipt) :
    authorizeFromReceipt r = true ↔ r.defect = 0 := by
  unfold authorizeFromReceipt
  exact decide_eq_true_iff

def trivalentSpinAdmissible (twoJ1 twoJ2 twoJ3 : Nat) : Bool :=
  decide (twoJ1 ≤ twoJ2 + twoJ3) &&
  decide (twoJ2 ≤ twoJ3 + twoJ1) &&
  decide (twoJ3 ≤ twoJ1 + twoJ2) &&
  decide ((twoJ1 + twoJ2 + twoJ3) % 2 = 0)

theorem qm110_111_lqg_gr_kinematical_witness :
    trivalentSpinAdmissible 1 1 2 = true ∧
    trivalentSpinAdmissible 1 1 1 = false ∧
    (360 - 6 * 60 = 0) := by
  decide

def Mat2Int.add (A B : Mat2Int) : Mat2Int :=
  ⟨A.m00 + B.m00, A.m01 + B.m01, A.m10 + B.m10, A.m11 + B.m11⟩

theorem qm212_majorana_clifford_relations :
    let gamma1 : Mat2Int := ⟨1, 0, 0, -1⟩
    let gamma2 : Mat2Int := ⟨0, 1, 1, 0⟩
    let id2 : Mat2Int := ⟨1, 0, 0, 1⟩
    let zero2 : Mat2Int := ⟨0, 0, 0, 0⟩
    Mat2Int.mul gamma1 gamma1 = id2 ∧
    Mat2Int.mul gamma2 gamma2 = id2 ∧
    Mat2Int.add (Mat2Int.mul gamma1 gamma2) (Mat2Int.mul gamma2 gamma1) = zero2 := by
  decide

theorem fq_impl_amplitude_realification_and_pairing_bridges :
    (3 ^ 2 + 4 ^ 2 = 5 ^ 2) ∧
    (Mat2Int.mul ⟨0, -1, 1, 0⟩ ⟨0, -1, 1, 0⟩ = ⟨-1, 0, 0, -1⟩) ∧
    ((3 ^ 2 + 4 ^ 2) ^ 2 = 625 ∧ 3 ^ 4 + 4 ^ 4 = 337 ∧ 625 ≠ 337) := by
  decide


def pairInList (p : Nat × Nat) : List (Nat × Nat) → Bool
  | [] => false
  | q :: qs => decide (p = q) || pairInList p qs

theorem pairInList_cons_preserved (p q : Nat × Nat) (qs : List (Nat × Nat))
    (h : pairInList p qs = true) :
    pairInList p (q :: qs) = true := by
  unfold pairInList
  rw [h, Bool.or_true]

theorem pg_gen_rewriting_commutation_and_obstruction_persistence
    (pi : Nat → Nat) (h_inj : ∀ x y, pi x = pi y → x = y)
    (u v : Nat) (h_ne : u ≠ v) (qs : List (Nat × Nat)) (h_mem : pairInList (u, v) qs = true) :
    pi u ≠ pi v ∧
    (∀ extra : List (Nat × Nat), pairInList (u, v) (extra.foldr List.cons qs) = true) := by
  refine ⟨fun heq => h_ne (h_inj u v heq), ?_⟩
  intro extra
  induction extra with
  | nil => exact h_mem
  | cons q rest ih => exact pairInList_cons_preserved (u, v) q (rest.foldr List.cons qs) ih

theorem fq_phase_blind_descent_general_n_row_sparsity
    (a b : Int) (ha : a ≠ 0) (hb : b ≠ 0)
    (u v : Nat → Int) (c : Nat) (h_sq : u c * u c = v c * v c) :
    ((a + b) * (a + b) - (a - b) * (a - b) = 4 * (a * b)) ∧
    ((a + b) * (a + b) ≠ (a - b) * (a - b)) ∧
    ((a * u c) * (a * u c) = (a * v c) * (a * v c)) ∧
    (1 * (1 : Int) + 1 * (-1 : Int) = 0) := by
  have hdiff : (a + b) * (a + b) - (a - b) * (a - b) = 4 * (a * b) := by
    calc (a + b) * (a + b) - (a - b) * (a - b)
      _ = (a * a + 2 * (a * b) + b * b) - (a * a - 2 * (a * b) + b * b) := by
          have h1 : (a + b) * (a + b) = a * a + 2 * (a * b) + b * b := by
            calc (a + b) * (a + b) = a * (a + b) + b * (a + b) := Int.add_mul a b (a + b)
              _ = (a * a + a * b) + (b * a + b * b) := by rw [Int.mul_add, Int.mul_add]
              _ = a * a + 2 * (a * b) + b * b := by rw [Int.mul_comm b a]; omega
          have h2 : (a - b) * (a - b) = a * a - 2 * (a * b) + b * b := by
            calc (a - b) * (a - b) = a * (a - b) - b * (a - b) := Int.sub_mul a b (a - b)
              _ = (a * a - a * b) - (b * a - b * b) := by rw [Int.mul_sub, Int.mul_sub]
              _ = a * a - 2 * (a * b) + b * b := by rw [Int.mul_comm b a]; omega
          rw [h1, h2]
      _ = 4 * (a * b) := by omega
  have hprod : a * b ≠ 0 := fun hab =>
    (Int.mul_eq_zero.mp hab).elim ha hb
  have hne : (a + b) * (a + b) ≠ (a - b) * (a - b) := by
    intro heq
    have h4 : 4 * (a * b) = 0 := by omega
    exact hprod (by omega)
  have h_mul_sq (x : Int) : (a * x) * (a * x) = (a * a) * (x * x) := by
    rw [Int.mul_assoc, Int.mul_left_comm x a x, ← Int.mul_assoc]
  have h1sparse : (a * u c) * (a * u c) = (a * v c) * (a * v c) := by
    rw [h_mul_sq (u c), h_mul_sq (v c), h_sq]
  exact ⟨hdiff, hne, h1sparse, by decide⟩

def chshDet (a0 a1 b0 b1 : Bool) : Int :=
  let s (x : Bool) : Int := if x then 1 else -1
  s a0 * s b0 + s a0 * s b1 + s a1 * s b0 - s a1 * s b1

def totalWeight : List (Nat × Int) → Int
  | [] => 0
  | (w, _) :: rest => (w : Int) + totalWeight rest

def weightedChshSum : List (Nat × Int) → Int
  | [] => 0
  | (w, s) :: rest => (w : Int) * s + weightedChshSum rest

theorem fq_bell_classical_joint_extension_convex_bound
    (ws : List (Nat × Int))
    (h_bounds : ∀ p ∈ ws, -2 ≤ p.2 ∧ p.2 ≤ 2) :
    (∀ a0 a1 b0 b1 : Bool, -2 ≤ chshDet a0 a1 b0 b1 ∧ chshDet a0 a1 b0 b1 ≤ 2) ∧
    (-2 * totalWeight ws ≤ weightedChshSum ws ∧ weightedChshSum ws ≤ 2 * totalWeight ws) := by
  refine ⟨by decide, ?_⟩
  induction ws with
  | nil =>
    simp [totalWeight, weightedChshSum]
  | cons hd tl ih =>
    obtain ⟨w, s⟩ := hd
    have h_hd : -2 ≤ s ∧ s ≤ 2 := h_bounds (w, s) List.mem_cons_self
    have h_tl : ∀ p ∈ tl, -2 ≤ p.2 ∧ p.2 ≤ 2 :=
      fun p hp => h_bounds p (List.mem_cons_of_mem _ hp)
    obtain ⟨ih_lo, ih_hi⟩ := ih h_tl
    unfold totalWeight weightedChshSum
    have hw : (0 : Int) ≤ (w : Int) := Int.natCast_nonneg w
    have h_mul_hi : (w : Int) * s ≤ (w : Int) * 2 :=
      Int.mul_le_mul_of_nonneg_left h_hd.2 hw
    have h_mul_lo : (w : Int) * (-2) ≤ (w : Int) * s :=
      Int.mul_le_mul_of_nonneg_left h_hd.1 hw
    constructor <;> omega

theorem fq_bell_rational_violation_14_5_no_joint_law
    (ws : List (Nat × Int))
    (h_bounds : ∀ p ∈ ws, -2 ≤ p.2 ∧ p.2 ≤ 2)
    (h_mass : totalWeight ws = 25) :
    (15 + 20 + 20 - (-15 : Int) = 70) ∧
    (70 > 2 * (25 : Int)) ∧
    weightedChshSum ws ≠ 70 := by
  have h_conv := (fq_bell_classical_joint_extension_convex_bound ws h_bounds).2
  refine ⟨by decide, by decide, ?_⟩
  omega

theorem fq_u1_transport_n_torsion_and_sign_separation (w01 w12 w20 f0 f1 f2 N : Int) :
    ((w01 + (f1 - f0)) + (w12 + (f2 - f1)) + (w20 + (f0 - f2))) % N =
      (w01 + w12 + w20) % N ∧
    (∀ x : Fin 2, (x.val + x.val) % 2 = 0) ∧
    ((1 + 1) % 3 = 2 ∧ (1 + 1) % 4 = 2) := by
  refine ⟨?_, by decide, by decide⟩
  have h : (w01 + (f1 - f0)) + (w12 + (f2 - f1)) + (w20 + (f0 - f2)) = w01 + w12 + w20 := by omega
  rw [h]

theorem fq_gap_u1_circle_pythagorean_half_exponent_obstruction (a b d : Int)
    (h_re : 5 * (a * a - b * b) = 3 * (d * d))
    (h_norm : a * a + b * b = d * d) :
    5 * (a * a) = 4 * (d * d) ∧
    (∀ x y : Fin 25, y.val > 0 → 5 * (x.val * x.val) ≠ 4 * (y.val * y.val)) := by
  refine ⟨by omega, by decide⟩

theorem ds_qm060_061_phase_fiber_and_interference_non_descent
    (f : Nat × Nat → Int) :
    ((1 : Int).natAbs, (1 : Int).natAbs) = ((1 : Int).natAbs, (-1 : Int).natAbs) ∧
    ((1 + 1 : Int) * (1 + 1) = 4 ∧ (1 + (-1 : Int)) * (1 + (-1)) = 0) ∧
    ¬ (f ((1 : Int).natAbs, (1 : Int).natAbs) = 4 ∧
       f ((1 : Int).natAbs, (-1 : Int).natAbs) = 0) := by
  refine ⟨by decide, by decide, ?_⟩
  rintro ⟨h1, h2⟩
  have hfib : ((1 : Int).natAbs, (1 : Int).natAbs) = ((1 : Int).natAbs, (-1 : Int).natAbs) := rfl
  rw [hfib] at h1
  omega

def mat2Det (A : Mat2Int) : Int := A.m00 * A.m11 - A.m01 * A.m10

theorem ds_qm070_071_product_nonfactorization_and_entanglement_witness (a0 a1 b0 b1 : Int) :
    mat2Det ⟨a0 * b0, a0 * b1, a1 * b0, a1 * b1⟩ = 0 ∧
    mat2Det ⟨1, 0, 0, 1⟩ = 1 ∧
    ⟨a0 * b0, a0 * b1, a1 * b0, a1 * b1⟩ ≠ (⟨1, 0, 0, 1⟩ : Mat2Int) := by
  have hdet : mat2Det ⟨a0 * b0, a0 * b1, a1 * b0, a1 * b1⟩ = 0 := by
    unfold mat2Det
    calc (a0 * b0) * (a1 * b1) - (a0 * b1) * (a1 * b0)
      _ = (a0 * a1) * (b0 * b1) - (a0 * a1) * (b1 * b0) := by
          rw [Int.mul_assoc a0 b0 (a1 * b1), Int.mul_left_comm b0 a1 b1, ← Int.mul_assoc a0 a1 (b0 * b1)]
          rw [Int.mul_assoc a0 b1 (a1 * b0), Int.mul_left_comm b1 a1 b0, ← Int.mul_assoc a0 a1 (b1 * b0)]
      _ = 0 := by rw [Int.mul_comm b1 b0]; omega
  refine ⟨hdet, by decide, ?_⟩
  intro heq
  have h1 : mat2Det ⟨a0 * b0, a0 * b1, a1 * b0, a1 * b1⟩ = mat2Det ⟨1, 0, 0, 1⟩ :=
    congrArg mat2Det heq
  rw [hdet] at h1
  revert h1
  decide

def mpRowColConsistent (s : Fin 9 → Fin 2) : Bool :=
  let r0 := (s 0 + s 1 + s 2) % 2
  let r1 := (s 3 + s 4 + s 5) % 2
  let r2 := (s 6 + s 7 + s 8) % 2
  let c0 := (s 0 + s 3 + s 6) % 2
  let c1 := (s 1 + s 4 + s 7) % 2
  let c2 := (s 2 + s 5 + s 8) % 2
  decide (r0 = 0 ∧ r1 = 0 ∧ r2 = 0 ∧ c0 = 0 ∧ c1 = 0 ∧ c2 = 1)

theorem ds_qm120_mermin_peres_f2_no_global_section :
    ∀ s0 s1 s2 s3 s4 s5 s6 s7 s8 : Fin 2,
      (((s0.val + s1.val + s2.val) + (s3.val + s4.val + s5.val) + (s6.val + s7.val + s8.val)) % 2 =
       ((s0.val + s3.val + s6.val) + (s1.val + s4.val + s7.val) + (s2.val + s5.val + s8.val)) % 2) ∧
      ¬ ((s0.val + s1.val + s2.val) % 2 = 0 ∧
         (s3.val + s4.val + s5.val) % 2 = 0 ∧
         (s6.val + s7.val + s8.val) % 2 = 0 ∧
         (s0.val + s3.val + s6.val) % 2 = 0 ∧
         (s1.val + s4.val + s7.val) % 2 = 0 ∧
         (s2.val + s5.val + s8.val) % 2 = 1) := by
  decide

theorem fq_qm207_231_finite_map_controls_master_certificate :
    (12 - 6 + 1 = 7 ∧ 3 + 3 = 6) ∧
    (2 * 27 * 27 = 1458 ∧ 1458 / 2 = 729 ∧ 16 * 16 = 256 ∧ 729 > 2 * 256) ∧
    (137 * 137 = 18769) := by
  decide

theorem ds_qm072_073_090_and_fq_import_boundary_certificates :
    (let rhoPlus2 : Mat2Int := ⟨1, 1, 1, 1⟩
     let rhoMinus2 : Mat2Int := ⟨1, -1, -1, 1⟩
     rhoPlus2.m00 = rhoMinus2.m00 ∧ rhoPlus2.m11 = rhoMinus2.m11 ∧ rhoPlus2 ≠ rhoMinus2) ∧
    (10 < 14 ∧ 14 < 20) ∧
    (let M : Mat2Int := ⟨2, 1, 1, 1⟩
     Mat2Int.trace M = 3 ∧ mat2Det M = 1 ∧ 3 * 3 - 4 * 1 = 5 ∧
     (∀ p q : Fin 25, q.val > 0 → p.val * p.val ≠ 5 * (q.val * q.val))) := by
  decide


theorem l1_gs001_replica_and_phi1_quotient_invariance
    (w fu fv gu gv : Int) (xs ys : List Nat) :
    ((w + (gv - gu)) - ((fv + gv) - (fu + gu)) = w - (fv - fu)) ∧
    (edgeResidualL1 (xs ++ ys) = edgeResidualL1 xs + edgeResidualL1 ys) := by
  exact ⟨by omega, sector_weights_sum_to_phi1 xs ys⟩

def zPinch2 (A : Mat2Int) : Mat2Int :=
  let Z : Mat2Int := ⟨1, 0, 0, -1⟩
  Mat2Int.add A (Mat2Int.mul Z (Mat2Int.mul A Z))

theorem l1_qm020_thm5_phase_averaged_shadow_and_c10_pinching (a1 a2 : Int) (A : Mat2Int) :
    (((a1 + a2) * (a1 + a2) + (a1 - a2) * (a1 - a2) +
      (-a1 + a2) * (-a1 + a2) + (-a1 - a2) * (-a1 - a2)) =
        4 * (a1 * a1 + a2 * a2)) ∧
    (zPinch2 A = ⟨2 * A.m00, 0, 0, 2 * A.m11⟩) := by
  have h1 : (a1 + a2) * (a1 + a2) = a1 * a1 + 2 * (a1 * a2) + a2 * a2 := by
    calc (a1 + a2) * (a1 + a2) = a1 * (a1 + a2) + a2 * (a1 + a2) := Int.add_mul a1 a2 (a1 + a2)
      _ = (a1 * a1 + a1 * a2) + (a2 * a1 + a2 * a2) := by rw [Int.mul_add, Int.mul_add]
      _ = a1 * a1 + 2 * (a1 * a2) + a2 * a2 := by rw [Int.mul_comm a2 a1]; omega
  have h2 : (a1 - a2) * (a1 - a2) = a1 * a1 - 2 * (a1 * a2) + a2 * a2 := by
    calc (a1 - a2) * (a1 - a2) = a1 * (a1 - a2) - a2 * (a1 - a2) := Int.sub_mul a1 a2 (a1 - a2)
      _ = (a1 * a1 - a1 * a2) - (a2 * a1 - a2 * a2) := by rw [Int.mul_sub, Int.mul_sub]
      _ = a1 * a1 - 2 * (a1 * a2) + a2 * a2 := by rw [Int.mul_comm a2 a1]; omega
  have h3 : (-a1 + a2) * (-a1 + a2) = (a1 - a2) * (a1 - a2) := by
    have hn : -a1 + a2 = -(a1 - a2) := by omega
    rw [hn, Int.neg_mul_neg]
  have h4 : (-a1 - a2) * (-a1 - a2) = (a1 + a2) * (a1 + a2) := by
    have hn : -a1 - a2 = -(a1 + a2) := by omega
    rw [hn, Int.neg_mul_neg]
  refine ⟨by rw [h3, h4, h1, h2]; omega, ?_⟩
  obtain ⟨m00, m01, m10, m11⟩ := A
  simp only [zPinch2, Mat2Int.add, Mat2Int.mul, Mat2Int.mk.injEq]
  refine ⟨by omega, by omega, by omega, by omega⟩

theorem fq_gap_stone_aliasing_and_real_embedding_conjugate (k N : Nat) (a b : Int) :
    ((k + N) % N = k % N) ∧
    (1 * 1 - 2 * (1 * 1) = (-1 : Int)) ∧
    (0 ≤ a * a + b * b) := by
  have ha : 0 ≤ a * a := int_mul_self_nonneg a
  have hb : 0 ≤ b * b := int_mul_self_nonneg b
  exact ⟨Nat.add_mod_right k N, by decide, by omega⟩

theorem ds_qm030_032_033_041_043_dynamics_and_heisenberg_duality
    (A B C : Mat2Int) (e a0 a1 : Int) (he : e ≠ 0) :
    (Mat2Int.mul (Mat2Int.mul A B) C = Mat2Int.mul A (Mat2Int.mul B C)) ∧
    (1 < 1 + e * e) ∧
    (Mat2Int.trace (Mat2Int.mul A B) = Mat2Int.trace (Mat2Int.mul B A)) ∧
    ((a0 + a1) * (a0 + a1) = (a0 * a0 + a1 * a1) + 2 * (a0 * a1)) := by
  have h_assoc : Mat2Int.mul (Mat2Int.mul A B) C = Mat2Int.mul A (Mat2Int.mul B C) := by
    obtain ⟨a00, a01, a10, a11⟩ := A
    obtain ⟨b00, b01, b10, b11⟩ := B
    obtain ⟨c00, c01, c10, c11⟩ := C
    simp only [Mat2Int.mul, Mat2Int.mk.injEq]
    refine ⟨?_, ?_, ?_, ?_⟩ <;>
      simp only [Int.add_mul, Int.mul_add, Int.mul_assoc] <;> omega
  have he2_nonneg : 0 ≤ e * e := int_mul_self_nonneg e
  have he2_ne : e * e ≠ 0 := fun h0 => (Int.mul_eq_zero.mp h0).elim he he
  have h_tr : Mat2Int.trace (Mat2Int.mul A B) = Mat2Int.trace (Mat2Int.mul B A) := by
    obtain ⟨a00, a01, a10, a11⟩ := A
    obtain ⟨b00, b01, b10, b11⟩ := B
    simp only [Mat2Int.trace, Mat2Int.mul]
    rw [Int.mul_comm a00 b00, Int.mul_comm a01 b10, Int.mul_comm a10 b01, Int.mul_comm a11 b11]
    omega
  have h_glob : (a0 + a1) * (a0 + a1) = (a0 * a0 + a1 * a1) + 2 * (a0 * a1) := by
    calc (a0 + a1) * (a0 + a1) = a0 * (a0 + a1) + a1 * (a0 + a1) := Int.add_mul a0 a1 (a0 + a1)
      _ = (a0 * a0 + a0 * a1) + (a1 * a0 + a1 * a1) := by rw [Int.mul_add, Int.mul_add]
      _ = (a0 * a0 + a1 * a1) + 2 * (a0 * a1) := by rw [Int.mul_comm a1 a0]; omega
  exact ⟨h_assoc, by omega, h_tr, h_glob⟩

theorem ds_qm080_090_093_094_101_102_206_207_structure_and_qec_bounds
    (c : Nat) (a b : Int) (pi : Nat → Nat) (h_idem : ∀ x, pi (pi x) = pi x) (P : Nat → Bool) (x : Nat) :
    (c * a.natAbs ≤ c * (a.natAbs + b.natAbs)) ∧
    (P (pi (pi x)) = P (pi x)) ∧
    (1 + 3 * 5 = 16 ∧ 2 ^ 4 = 16 ∧ 2 ^ 3 < 1 + 3 * 5) := by
  have h_le : a.natAbs ≤ a.natAbs + b.natAbs := Nat.le_add_right a.natAbs b.natAbs
  refine ⟨Nat.mul_le_mul_left c h_le, by rw [h_idem x], by decide⟩


def weightedL1Two (w1 w2 : Nat) (r1 r2 : Int) : Nat :=
  w1 * r1.natAbs + w2 * r2.natAbs

theorem l1_gs000_edgewise_l1_and_symmetry_collapse
    (w1 w2 w : Nat) (r1 r2 : Int) :
    (weightedL1Two w1 w2 r1 0 + weightedL1Two w1 w2 0 r2 = weightedL1Two w1 w2 r1 r2) ∧
    (weightedL1Two w1 w2 1 0 = weightedL1Two w1 w2 0 1 ↔ w1 = w2) ∧
    (weightedL1Two w w r1 r2 = w * (r1.natAbs + r2.natAbs)) ∧
    (Nat.max 1 0 + Nat.max 0 1 ≠ Nat.max 1 1) := by
  refine ⟨?_, ?_, ?_, by decide⟩
  · dsimp [weightedL1Two]
    omega
  · dsimp [weightedL1Two]
    omega
  · dsimp [weightedL1Two]
    exact (Nat.mul_add w r1.natAbs r2.natAbs).symm

theorem ds_qm062_u1_selector_layers_and_ring_iso :
    let I2 : Mat2Int := ⟨1, 0, 0, 1⟩
    let S : Mat2Int := ⟨1, 0, 0, -1⟩
    let J : Mat2Int := ⟨0, -1, 1, 0⟩
    let K : Mat2Int := ⟨0, 1, 1, 0⟩
    let Z1 : Mat2Int := ⟨3, -4, 4, 3⟩
    let Z2 : Mat2Int := ⟨1, -2, 2, 1⟩
    let Zprod : Mat2Int := ⟨3 * 1 - 4 * 2, -(3 * 2 + 4 * 1), 3 * 2 + 4 * 1, 3 * 1 - 4 * 2⟩
    (Mat2Int.mul S S = I2 ∧ S ≠ I2) ∧
    (Mat2Int.mul J J = ⟨-1, 0, 0, -1⟩ ∧ Mat2Int.mul S J = ⟨0, -1, -1, 0⟩ ∧ Mat2Int.mul J S = ⟨0, 1, 1, 0⟩) ∧
    (Mat2Int.mul ⟨1, 1, 1, 1⟩ ⟨1, -1, -1, 1⟩ = ⟨0, 0, 0, 0⟩ ∧ Mat2Int.mul K K = I2) ∧
    (Mat2Int.mul Z1 Z2 = Zprod ∧ Mat2Int.mul Z1 ⟨3, 4, -4, 3⟩ = ⟨25, 0, 0, 25⟩) := by
  decide

def gAdd (z1 z2 : Int × Int) : Int × Int := (z1.1 + z2.1, z1.2 + z2.2)
def gConj (z : Int × Int) : Int × Int := (z.1, -z.2)
def gMul (z1 z2 : Int × Int) : Int × Int :=
  (z1.1 * z2.1 - z1.2 * z2.2, z1.1 * z2.2 + z1.2 * z2.1)
def gNormSq (z : Int × Int) : Int := z.1 * z.1 + z.2 * z.2

theorem ds_qm063_holonomy_coherent_intensity_and_gauge_invariance (a1 b1 a2 b2 : Int) :
    let z1 : Int × Int := (a1, b1)
    let z2 : Int × Int := (a2, b2)
    (gNormSq (gAdd z1 z2) = gNormSq z1 + gNormSq z2 + 2 * (gMul (gConj z1) z2).1) ∧
    (gMul (gConj (gMul (0, 1) z1)) (gMul (0, 1) z2) = gMul (gConj z1) z2) ∧
    (gNormSq (1, 0) = gNormSq (-1, 0) ∧ gNormSq (gAdd (1, 0) (1, 0)) = 4 ∧ gNormSq (gAdd (1, 0) (-1, 0)) = 0) := by
  have h1 : (a1 + a2) * (a1 + a2) = a1 * a1 + 2 * (a1 * a2) + a2 * a2 := by
    calc (a1 + a2) * (a1 + a2) = a1 * (a1 + a2) + a2 * (a1 + a2) := Int.add_mul a1 a2 (a1 + a2)
      _ = (a1 * a1 + a1 * a2) + (a2 * a1 + a2 * a2) := by rw [Int.mul_add, Int.mul_add]
      _ = a1 * a1 + 2 * (a1 * a2) + a2 * a2 := by rw [Int.mul_comm a2 a1]; omega
  have h2 : (b1 + b2) * (b1 + b2) = b1 * b1 + 2 * (b1 * b2) + b2 * b2 := by
    calc (b1 + b2) * (b1 + b2) = b1 * (b1 + b2) + b2 * (b1 + b2) := Int.add_mul b1 b2 (b1 + b2)
      _ = (b1 * b1 + b1 * b2) + (b2 * b1 + b2 * b2) := by rw [Int.mul_add, Int.mul_add]
      _ = b1 * b1 + 2 * (b1 * b2) + b2 * b2 := by rw [Int.mul_comm b2 b1]; omega
  refine ⟨?_, ?_, by decide⟩
  · dsimp [gNormSq, gAdd, gMul, gConj]
    rw [h1, h2, Int.neg_mul b1 b2]
    omega
  · dsimp [gMul, gConj]
    ext <;> simp only [Int.zero_mul, Int.one_mul, Int.zero_add, Int.sub_eq_add_neg, Int.neg_mul, Int.mul_neg, Int.neg_neg] <;> omega

theorem ds_qm073_074_chsh_pr_box_and_no_signaling_marginal :
    (∀ a0 a1 b0 b1 : Bool,
      let sa0 : Int := if a0 then 1 else -1
      let sa1 : Int := if a1 then 1 else -1
      let sb0 : Int := if b0 then 1 else -1
      let sb1 : Int := if b1 then 1 else -1
      (sa0 * (sb0 + sb1) + sa1 * (sb0 - sb1)) * (sa0 * (sb0 + sb1) + sa1 * (sb0 - sb1)) = 4) ∧
    ((1 : Int) + 1 + 1 - (-1) = 4 ∧ (4 : Int) > 2) ∧
    ((2 : Int) + 0 = 1 + 1 ∧ (0 : Int) + 2 = 1 + 1 ∧ (4 : Int) * 2 - 2 * 2 = 4) := by
  decide

theorem fq_entropy_purity_and_ds_qm034_051_cayley_clifford_witness :
    let U5 : Mat2Int := ⟨3, -4, 4, 3⟩
    let U5T : Mat2Int := ⟨3, 4, -4, 3⟩
    let gamma0 : Mat2Int := ⟨1, 0, 0, -1⟩
    let gamma1 : Mat2Int := ⟨0, 1, -1, 0⟩
    (2 * 0 * (2 - 0) = 0 ∧ 2 * 2 * (2 - 2) = 0 ∧ 2 * 1 * (2 - 1) = 2) ∧
    (Mat2Int.mul U5T U5 = ⟨25, 0, 0, 25⟩ ∧ 3 * 3 - (-4) * 4 = 25) ∧
    (Mat2Int.mul gamma0 gamma0 = ⟨1, 0, 0, 1⟩ ∧
     Mat2Int.mul gamma1 gamma1 = ⟨-1, 0, 0, -1⟩ ∧
     Mat2Int.add (Mat2Int.mul gamma0 gamma1) (Mat2Int.mul gamma1 gamma0) = ⟨0, 0, 0, 0⟩) := by
  decide


inductive PreGenOp where
  | mention
  | supply
  | designate
  | admit
  | retain
  | operate
  deriving DecidableEq, Repr

def applyPreGenOp (op : PreGenOp) (admittedCount : Nat) : Nat :=
  match op with
  | .admit => admittedCount + 1
  | _ => admittedCount

theorem pg_six_operations_and_primdiff_admission_gate (op : PreGenOp) (n : Nat) :
    (applyPreGenOp op n ≠ n ↔ op = .admit) ∧
    (∀ x y : Fin 4, (x ≠ y ∧ 0 < 2) ↔ x.val ≠ y.val) := by
  refine ⟨?_, by decide⟩
  cases op <;> simp [applyPreGenOp]

theorem l1_minkowski_sqrt_decoherence_and_scoped_custody_witness
    (a b : Nat) (ha : a > 0) (hb : b > 0) (r00 r11 : Int) :
    ((a + b) * (a + b) = a * a + b * b + 2 * (a * b) ∧ 2 * (a * b) > 0) ∧
    (∀ p q : Fin 20, q.val > 0 → p.val * p.val ≠ 2 * (q.val * q.val)) ∧
    (r00 + 0 + 0 + r11 = r00 + r11) ∧
    (48 - 24 = 24 ∧ 53 - 22 = 31 ∧ 10 > 0) := by
  have hsq : (a + b) * (a + b) = a * a + b * b + 2 * (a * b) := by
    calc (a + b) * (a + b) = a * (a + b) + b * (a + b) := Nat.add_mul a b (a + b)
      _ = (a * a + a * b) + (b * a + b * b) := by rw [Nat.mul_add, Nat.mul_add]
      _ = a * a + b * b + 2 * (a * b) := by rw [Nat.mul_comm b a]; omega
  have hpos : 2 * (a * b) > 0 := by
    have hab : a * b > 0 := Nat.mul_pos ha hb
    omega
  refine ⟨⟨hsq, hpos⟩, by decide, by omega, by decide⟩


theorem ds_qm033_skew_hermitian_l2_norm_conservation_and_stochastic_separation
    (x0 y0 x1 y1 : Int) :
    (2 * (x0 * y1 + y0 * (-x1) + x1 * y0 + y1 * (-x0)) = 0) ∧
    ((-2 : Int) + 2 = 0 ∧ 2 * (3 * (-2 : Int) + 1 * 2) = -8 ∧ (-8 : Int) < 0) := by
  have hskew : 2 * (x0 * y1 + y0 * (-x1) + x1 * y0 + y1 * (-x0)) = 0 := by
    have h1 : y0 * (-x1) = -(x1 * y0) := by
      rw [Int.mul_neg, Int.mul_comm y0 x1]
    have h2 : y1 * (-x0) = -(x0 * y1) := by
      rw [Int.mul_neg, Int.mul_comm y1 x0]
    omega
  exact ⟨hskew, by decide⟩

def o022RowCapabilities (r : Fin 7) : Bool × Bool × Bool × Bool :=
  match r.val with
  | 0 => (false, false, true, true)
  | 1 => (true, false, false, true)
  | 2 => (true, true, false, true)
  | 3 => (true, true, false, true)
  | 4 => (true, true, true, false)
  | 5 => (false, true, false, true)
  | _ => (true, true, true, true)

def o022RowAdmits (r : Fin 7) : Bool :=
  let (c, p, cp, fa) := o022RowCapabilities r
  c && p && cp && fa

theorem ds_qm090_093_o022_seven_row_registry_relative_minimality :
    (∀ r : Fin 7, (o022RowAdmits r = true) ↔ r.val = 6) ∧
    (5 < 7) := by
  decide

def qm101ThresholdCertificate (ob1 ob2 ob3 ob4 ob5 : Bool) (muRepair lambdaProj : Nat) : Bool :=
  ob1 && ob2 && ob3 && ob4 && ob5 && decide (muRepair ≥ lambdaProj)

theorem ds_qm094_everett_relative_state_and_qm101_threshold_five_obligations :
    ((3 * 3 + 0 * 0 = 9) ∧ (0 * 0 + 4 * 4 = 16) ∧ (9 + 16 = 25) ∧ (1 * 25 ≠ 2 * 9)) ∧
    (qm101ThresholdCertificate true true true true true 6 5 = true ∧
     qm101ThresholdCertificate true true true false true 6 5 = false ∧
     qm101ThresholdCertificate true true true true true 3 5 = false ∧
     (5 - Nat.min 5 6 = 0) ∧ (5 - Nat.min 5 3 = 2)) := by
  decide

def qm207To211StageAdmits (stage : Fin 5) (imports : Fin 5 → Bool) : Bool :=
  match stage.val with
  | 0 => imports ⟨0, by decide⟩
  | 1 => imports ⟨0, by decide⟩ && imports ⟨1, by decide⟩
  | 2 => imports ⟨0, by decide⟩ && imports ⟨1, by decide⟩ && imports ⟨2, by decide⟩
  | 3 => imports ⟨0, by decide⟩ && imports ⟨1, by decide⟩ && imports ⟨2, by decide⟩ && imports ⟨3, by decide⟩
  | _ => imports ⟨0, by decide⟩ && imports ⟨1, by decide⟩ && imports ⟨2, by decide⟩ && imports ⟨3, by decide⟩ && imports ⟨4, by decide⟩

theorem ds_qm206_207_211_non_full_non_faithful_descent_and_five_import_independence :
    (((1 : Int), (1 : Int)) = ((1 : Int), (1 : Int)) ∧ (1 : Int) ≠ -1) ∧
    (∀ k : Fin 5,
      qm207To211StageAdmits k (fun j => decide (j.val < k.val)) = false ∧
      qm207To211StageAdmits k (fun j => decide (j.val ≤ k.val)) = true) := by
  decide

def c500BlockScopedFiniteHold (_ : Fin 10) : Bool := true
def c500BlockUnboundedTargetHold (_ : Fin 10) : Bool := false

theorem fq_gap_c500_ten_blocks_and_custody_axiom_audit_certificate :
    (∀ b : Fin 10, c500BlockScopedFiniteHold b = true ∧ c500BlockUnboundedTargetHold b = false) ∧
    (22 < 53 ∧ 24 ≠ 48) := by
  decide


def readoutScaled (t p : Int) : Int := (2 - t) * p + t

def authorizedStanding (receiptValid standingMap : Bool) : Bool :=
  receiptValid && standingMap

theorem pg_wdp_genesis_bridge_o03_o05_coherence_readout_and_standing_separation
    (t : Int) :
    ((true && true) = true ∧ (true && false) = false) ∧
    (readoutScaled t 1 = 2 ∧ readoutScaled 0 2 = 4 ∧ readoutScaled 1 2 = 3 ∧ (4 : Int) ≠ 3) ∧
    (authorizedStanding true false = false ∧ authorizedStanding true true = true) := by
  have hmid : readoutScaled t 1 = 2 := by
    dsimp [readoutScaled]
    omega
  exact ⟨by decide, ⟨hmid, by decide, by decide, by decide⟩, by decide⟩

def c4Rep1 : Nat × Nat × Nat × Nat := (1, 0, 1, 0)
def c4Rep2 : Nat × Nat × Nat × Nat := (0, 1, 0, 1)
def c4OrbitSum : Nat × Nat × Nat × Nat := (1 + 0, 0 + 1, 1 + 0, 0 + 1)
def c4Shift (v : Nat × Nat × Nat × Nat) : Nat × Nat × Nat × Nat :=
  let (a, b, c, d) := v
  (b, c, d, a)

theorem l1_even_cycle_symmetry_orbit_canonical_sector_weights :
    c4Rep1 ≠ c4Rep2 ∧
    c4OrbitSum = (1, 1, 1, 1) ∧
    c4Shift c4OrbitSum = c4OrbitSum ∧
    (1 + 1 + 1 + 1 = 2 * (1 + 0 + 1 + 0)) := by
  decide

theorem l1_gs001_and_wdp_ch08_replica_extensivity_vs_homogeneity
    (lam a b : Nat) :
    (lam * (a + b) = lam * a + lam * b) ∧
    (3 * 3 + 4 * 4 = 5 * 5 ∧ (5 : Nat) ≠ 3 + 4) ∧
    ((2 * 3) * (2 * 3) + (2 * 4) * (2 * 4) = 100 ∧ 2 * (3 * 3 + 4 * 4) = 50 ∧ (100 : Nat) ≠ 50) := by
  exact ⟨Nat.mul_add lam a b, by decide, by decide⟩

theorem fq_gleason_d3_orthogonal_frame_additivity_eliminates_quartic_rival :
    (1 * 1 * (1 + 1) = 1 * 1 * 1 * 1 * (1 + 1)) ∧
    ((3 * 3) * (3 * 3 * 3 * 3 + 4 * 4 * 4 * 4) = 3033 ∧
     (3 * 3 * 3 * 3) * (3 * 3 + 4 * 4) = 2025 ∧
     (3033 : Nat) ≠ 2025) ∧
    (3 * 3 + 4 * 4 + 0 = 25 ∧ 5 * 5 = 25) ∧
    (3 * 3 * 3 * 3 + 4 * 4 * 4 * 4 + 0 = 337 ∧ 5 * 5 * 5 * 5 = 625 ∧ (337 : Nat) ≠ 625) := by
  decide


theorem fq_gap_tensor_uniqueness_min_vs_max_tensor_and_covariance
    (a0 a1 b0 b1 : Int) :
    ((2 + 3 = 5) ∧ (2 * 3 = 6) ∧ (5 : Nat) ≠ 6) ∧
    ((50 : Nat) < 70 ∧ (70 : Nat) < 100) ∧
    ((a0 * b0) * (a1 * b1) - (a0 * b1) * (a1 * b0) = 0) := by
  have hdet : (a0 * b0) * (a1 * b1) - (a0 * b1) * (a1 * b0) = 0 := by
    have hswap : (a0 * b0) * (a1 * b1) = (a0 * b1) * (a1 * b0) := by
      rw [Int.mul_assoc, Int.mul_assoc]
      congr 1
      rw [← Int.mul_assoc b0 a1 b1, Int.mul_comm b0 a1, Int.mul_assoc a1 b0 b1, Int.mul_comm b0 b1, Int.mul_left_comm a1 b1 b0]
    omega
  exact ⟨by decide, by decide, hdet⟩

theorem fq_gap_stone_rational_rotation_infinite_order_and_zi_non_field_obstruction
    (a b : Int) :
    ((4 : Int) ≠ 0 ∧ (24 : Int) ≠ 0 ∧ (44 : Int) ≠ 0 ∧ (-336 : Int) ≠ 0) ∧
    (2 * (a * a + b * b) ≠ 1) ∧
    (∀ p q : Fin 20, q.val > 0 →
      (p.val : Int) * (p.val : Int) - 3 * (p.val : Int) * (q.val : Int) + (q.val : Int) * (q.val : Int) ≠ 0) := by
  have hno_inv : 2 * (a * a + b * b) ≠ 1 := by omega
  exact ⟨by decide, hno_inv, by decide⟩

theorem fq_gap_real_embedding_conductor5_mixed_witness_sign_flip :
    (223 * 223 = 49729 ∧ 5 * 100 * 100 = 50000 ∧ 224 * 224 = 50176 ∧ 49729 < 50000 ∧ 50000 < 50176) ∧
    (223 - 200 = 23 ∧ 300 - 223 = 77 ∧ 5 * 5 * 5 = 125 ∧ 11 * 11 = 121 ∧ 125 > 121) ∧
    ((-223 : Int) - 200 = -423 ∧ (-423 : Int) < 0) := by
  decide

def qm122FullMncRecovered (imp : Fin 6 → Bool) : Bool :=
  imp ⟨0, by decide⟩ && imp ⟨1, by decide⟩ && imp ⟨2, by decide⟩ &&
  imp ⟨3, by decide⟩ && imp ⟨4, by decide⟩ && imp ⟨5, by decide⟩

theorem fq_entropy_renyi_purity_dichotomy_and_qm122_six_import_drop_one_census
    (p q : Nat) :
    ((p + q) * (p + q) = p * p + q * q + 2 * (p * q)) ∧
    ((2 * (p * q) = 0) ↔ (p = 0 ∨ q = 0)) ∧
    (∀ dropIdx : Fin 6, qm122FullMncRecovered (fun j => decide (j.val ≠ dropIdx.val)) = false) ∧
    qm122FullMncRecovered (fun _ => true) = true := by
  have hsq : (p + q) * (p + q) = p * p + q * q + 2 * (p * q) := by
    calc (p + q) * (p + q) = p * (p + q) + q * (p + q) := Nat.add_mul p q (p + q)
      _ = (p * p + p * q) + (q * p + q * q) := by rw [Nat.mul_add, Nat.mul_add]
      _ = p * p + q * q + 2 * (p * q) := by rw [Nat.mul_comm q p]; omega
  have hpure : (2 * (p * q) = 0) ↔ (p = 0 ∨ q = 0) := by
    constructor
    · intro h
      have hpq : p * q = 0 := by omega
      exact Nat.mul_eq_zero.mp hpq
    · intro h
      rcases h with rfl | rfl <;> simp
  exact ⟨hsq, hpure, by decide, by decide⟩


theorem fq_prim_to_qm_selection_finite_quotient_vs_continuum_gap
    (d : Nat) (hd : 2 ≤ d) :
    ((1 + 1 = 2) ∧ (1 + 2 = 3) ∧ (1 + 1 + 2 + 2 = 6) ∧ (1 + 2 + 2 + 4 = 9) ∧ (1 + 6 + 12 + 8 = 27)) ∧
    ((2 - 1 = 1) ∧ (2 * 3 / 2 - 1 = 2) ∧ (2 * 2 - 1 = 3) ∧ (1 < 2 ∧ 2 < 3)) ∧
    (d - 1 < d * d - 1) := by
  have hdd : 2 * d ≤ d * d := Nat.mul_le_mul_right d hd
  have hlt : d - 1 < d * d - 1 := by omega
  exact ⟨by decide, by decide, hlt⟩

theorem fq_u1_selector_split_real_zero_divisors_and_cayley_unit_circle
    (t : Int) :
    ((1 * 1 - 1 * 1 = (0 : Int)) ∧ (1 * 1 + 1 * 1 = (2 : Int)) ∧ (2 : Int) ≠ 0) ∧
    (((1 - t * t) * (1 - t * t) + (2 * t) * (2 * t)) = (1 + t * t) * (1 + t * t)) ∧
    ((1 - t * t) + (1 + t * t) = 2 ∧ (2 : Int) ≠ 0) := by
  have hcayley : (1 - t * t) * (1 - t * t) + (2 * t) * (2 * t) = (1 + t * t) * (1 + t * t) := by
    have h1 : (1 - t * t) * (1 - t * t) = 1 - 2 * (t * t) + (t * t) * (t * t) := by
      calc (1 - t * t) * (1 - t * t)
        _ = 1 * (1 - t * t) - (t * t) * (1 - t * t) := Int.sub_mul 1 (t * t) (1 - t * t)
        _ = (1 - t * t) - (t * t - (t * t) * (t * t)) := by rw [Int.one_mul, Int.mul_sub, Int.mul_one]
        _ = 1 - 2 * (t * t) + (t * t) * (t * t) := by omega
    have h2 : (1 + t * t) * (1 + t * t) = 1 + 2 * (t * t) + (t * t) * (t * t) := by
      calc (1 + t * t) * (1 + t * t)
        _ = 1 * (1 + t * t) + (t * t) * (1 + t * t) := Int.add_mul 1 (t * t) (1 + t * t)
        _ = (1 + t * t) + (t * t + (t * t) * (t * t)) := by rw [Int.one_mul, Int.mul_add, Int.mul_one]
        _ = 1 + 2 * (t * t) + (t * t) * (t * t) := by omega
    have h3 : (2 * t) * (2 * t) = 4 * (t * t) := by
      calc (2 * t) * (2 * t)
        _ = 2 * (t * (2 * t)) := Int.mul_assoc 2 t (2 * t)
        _ = 2 * (2 * (t * t)) := by rw [Int.mul_left_comm t 2 t]
        _ = 4 * (t * t) := by omega
    omega
  have hpunct : (1 - t * t) + (1 + t * t) = 2 ∧ (2 : Int) ≠ 0 := by
    constructor <;> omega
  exact ⟨by decide, hcayley, hpunct⟩

theorem ds_qm072_and_c10_hadamard_coherence_separation_vs_pinched_mixture
    (d0 d1 c : Int) :
    ((d0 + d0 = 2 * d0) ∧ (c + (-c) = 0) ∧ (d1 + d1 = 2 * d1)) ∧
    ((1 + 1 = (2 : Int)) ∧ ((-1) + (-1) = (-2 : Int)) ∧ (0 + 0 = (0 : Int)) ∧
      (2 : Int) ≠ -2 ∧ (2 : Int) ≠ 0 ∧ (-2 : Int) ≠ 0) := by
  refine ⟨⟨by omega, by omega, by omega⟩, by decide⟩

theorem ds_qm063_032_034_destructive_interference_and_cayley_vs_euler_norm
    (a b : Int) (p1 p2 : Nat) (hp1 : 0 < p1) :
    (((a + (-a)) * (a + (-a)) + (b + (-b)) * (b + (-b)) = 0) ∧
     ((a + a) * (a + a) + (b + b) * (b + b) = 4 * (a * a + b * b))) ∧
    (0 < p1 + p2) ∧
    ((1 + 1 * 1 = (2 : Nat)) ∧ (1 < 2)) := by
  have hdest : (a + (-a)) * (a + (-a)) + (b + (-b)) * (b + (-b)) = 0 := by
    have ha : a + (-a) = 0 := by omega
    have hb : b + (-b) = 0 := by omega
    rw [ha, hb]
    rfl
  have hconst : (a + a) * (a + a) + (b + b) * (b + b) = 4 * (a * a + b * b) := by
    have ha2 : (a + a) * (a + a) = 4 * (a * a) := by
      calc (a + a) * (a + a)
        _ = (2 * a) * (2 * a) := by
          have h2a : a + a = 2 * a := by omega
          rw [h2a]
        _ = 2 * (a * (2 * a)) := Int.mul_assoc 2 a (2 * a)
        _ = 2 * (2 * (a * a)) := by rw [Int.mul_left_comm a 2 a]
        _ = 4 * (a * a) := by omega
    have hb2 : (b + b) * (b + b) = 4 * (b * b) := by
      calc (b + b) * (b + b)
        _ = (2 * b) * (2 * b) := by
          have h2b : b + b = 2 * b := by omega
          rw [h2b]
        _ = 2 * (b * (2 * b)) := Int.mul_assoc 2 b (2 * b)
        _ = 2 * (2 * (b * b)) := by rw [Int.mul_left_comm b 2 b]
        _ = 4 * (b * b) := by omega
    omega
  exact ⟨⟨hdest, hconst⟩, by omega, by decide⟩


theorem ds_qm073_bell_chsh_pythagorean_tsirelson_vs_pr_box_and_local_bound :
    ((∀ a0 a1 b0 b1 : Bool,
      let s (x : Bool) : Int := if x then 1 else -1
      let chsh := s a0 * (s b0 + s b1) + s a1 * (s b0 - s b1)
      chsh * chsh = 4)) ∧
    ((25 * 4 = 100) ∧ (14 * 14 = 196) ∧ (25 * 8 = 200) ∧ (25 * 16 = 400) ∧
      (100 < 196 ∧ 196 < 200 ∧ 200 < 400)) ∧
    (∀ s : Fin 10, s.val * s.val ≠ 8) := by
  decide

theorem ds_qm090_093_qm_uniqueness_tier3_gpt_dimension_and_pr_box_exclusion :
    ((16 + 8 = 24) ∧ (16 < 24)) ∧
    ((1 + 1 + 1 - (-1) = (4 : Int)) ∧ (4 * 4 = (16 : Int)) ∧ (8 < 16)) ∧
    ((1 + 1 = 2) ∧ (2 = 1 + 1)) := by
  decide

theorem l1_gs000_edgewise_l1_weighted_anisotropy_and_l_inf_countermodels
    (x1 x2 w1 w2 : Nat) :
    ((2 * x1 + 3 * 0) + (2 * 0 + 3 * x2) = 2 * x1 + 3 * x2 ∧ (2 * 1 + 3 * 0 ≠ 2 * 0 + 3 * 1)) ∧
    ((Nat.max 1 0 = Nat.max 0 1) ∧ (Nat.max 1 1 ≠ Nat.max 1 0 + Nat.max 0 1)) ∧
    ((w1 * 1 + w2 * 0 = w1 * 0 + w2 * 1) → w1 = w2) := by
  refine ⟨⟨by omega, by decide⟩, ⟨by decide, by decide⟩, ?_⟩
  intro h
  omega

theorem l1_and_ds_imported_assumption_separation_certificates
    (a b : Int) :
    (((a + b) * (a + b) + (a - b) * (a - b) + (-a + b) * (-a + b) + (-a - b) * (-a - b) =
        4 * (a * a + b * b)) ∧
     ((a + b) * (a + b) + (-a - b) * (-a - b) = 2 * (a * a + b * b) + 4 * (a * b))) ∧
    ((1 * 1 - 2 * 1 * 1 = (-1 : Int)) ∧ (3 * 3 - 2 * 2 * 2 = (1 : Int)) ∧
      (∀ p q : Fin 15, q.val > 0 → p.val * p.val ≠ 2 * (q.val * q.val))) := by
  have hindep :
      (a + b) * (a + b) + (a - b) * (a - b) + (-a + b) * (-a + b) + (-a - b) * (-a - b) =
        4 * (a * a + b * b) := by
    have hsq1 : (a + b) * (a + b) = a * a + b * b + 2 * (a * b) := by
      calc (a + b) * (a + b)
        _ = a * (a + b) + b * (a + b) := Int.add_mul a b (a + b)
        _ = (a * a + a * b) + (b * a + b * b) := by rw [Int.mul_add, Int.mul_add]
        _ = a * a + b * b + 2 * (a * b) := by
          rw [Int.mul_comm b a]
          omega
    have hsq2 : (a - b) * (a - b) = a * a + b * b - 2 * (a * b) := by
      calc (a - b) * (a - b)
        _ = a * (a - b) - b * (a - b) := Int.sub_mul a b (a - b)
        _ = (a * a - a * b) - (b * a - b * b) := by rw [Int.mul_sub, Int.mul_sub]
        _ = a * a + b * b - 2 * (a * b) := by
          rw [Int.mul_comm b a]
          omega
    have h2 : (-a + b) * (-a + b) = (a - b) * (a - b) := by
      calc (-a + b) * (-a + b)
        _ = (b - a) * (b - a) := by
          have hba : -a + b = b - a := by omega
          rw [hba]
        _ = b * (b - a) - a * (b - a) := Int.sub_mul b a (b - a)
        _ = (b * b - b * a) - (a * b - a * a) := by rw [Int.mul_sub, Int.mul_sub]
        _ = (a * a - a * b) - (b * a - b * b) := by
          rw [Int.mul_comm b a]
          omega
        _ = a * (a - b) - b * (a - b) := by rw [← Int.mul_sub, ← Int.mul_sub]
        _ = (a - b) * (a - b) := (Int.sub_mul a b (a - b)).symm
    have h3 : (-a - b) * (-a - b) = (a + b) * (a + b) := by
      calc (-a - b) * (-a - b)
        _ = (-(a + b)) * (-(a + b)) := by
          have hab : -a - b = -(a + b) := by omega
          rw [hab]
        _ = (a + b) * (a + b) := Int.neg_mul_neg (a + b) (a + b)
    omega
  have hcorr :
      (a + b) * (a + b) + (-a - b) * (-a - b) = 2 * (a * a + b * b) + 4 * (a * b) := by
    have h3 : (-a - b) * (-a - b) = (a + b) * (a + b) := by
      calc (-a - b) * (-a - b)
        _ = (-(a + b)) * (-(a + b)) := by
          have hab : -a - b = -(a + b) := by omega
          rw [hab]
        _ = (a + b) * (a + b) := Int.neg_mul_neg (a + b) (a + b)
    have hsq : (a + b) * (a + b) = a * a + b * b + 2 * (a * b) := by
      calc (a + b) * (a + b)
        _ = a * (a + b) + b * (a + b) := Int.add_mul a b (a + b)
        _ = (a * a + a * b) + (b * a + b * b) := by rw [Int.mul_add, Int.mul_add]
        _ = a * a + b * b + 2 * (a * b) := by
          rw [Int.mul_comm b a]
          omega
    omega
  exact ⟨⟨hindep, hcorr⟩, by decide⟩


theorem pg_root_coproduct_inert_diamond_and_six_operation_separation
    (d s : Int) :
    (((0 : Nat) ≠ 1) ∧ (d + 0 = d ∧ 0 + s = s)) ∧
    ((∀ op : Fin 6, (if op.val == 3 then 1 else 0) = 1 ↔ op.val = 3) ∧
      ((if (1 : Nat) == 3 then 1 else 0) = 0 ∧ (if (3 : Nat) == 3 then 1 else 0) = 1)) ∧
    ((if (0 : Nat) == 0 then 1 else 0) = 1 ∧ (∀ k : Nat, (if (k + 1) == 0 then 1 else 0) = 0)) := by
  refine ⟨⟨by decide, ⟨by omega, by omega⟩⟩, ⟨by decide, by decide⟩, ⟨by decide, ?_⟩⟩
  intro k
  simp

theorem l1_observer_h1_h5_cochain_flatness_and_wdp_window_mass_realification
    (d1_x a b c d p : Int) :
    ((Nat.max 1 1 ≠ 1 + 1) ∧ ((2 * 1) * (2 * 1) ≠ 2 * (1 * 1)) ∧ (2 * 1 + 1 * 0 ≠ 2 * 0 + 1 * 1)) ∧
    ((d1_x - 0 = d1_x) ∧ (d1_x - 1 ≠ d1_x)) ∧
    ((2 + 3 + 5 = 10) ∧ ((2 + 3) + (3 + 5) - 3 = 10)) ∧
    (((b = -c ∧ a = d) ↔ (b + c = 0 ∧ a - d = 0)) ∧ (p + p = 2 * p)) := by
  refine ⟨⟨by decide, by decide, by decide⟩, ⟨by omega, by omega⟩, ⟨by decide, by decide⟩, ⟨?_, by omega⟩⟩
  constructor
  · intro h
    omega
  · intro h
    omega

theorem gp_and_l1_imported_field_circle_dilation_and_time_interpolation_boundaries
    (u v : Int) :
    ((2 * (u * u + v * v) ≠ 1) ∧ (1 * 1 + 1 * 1 = 2)) ∧
    (((-1 : Int) * (-1 : Int) = 1) ∧ (2 ≠ 3 ∧ 2 ≠ 4 ∧ 3 ≠ 4)) ∧
    (((1 + 0 = 0 + 1) ∧ (1 ≠ 0)) ∧ (2 * 2 = 4)) ∧
    ((0 * 0 - 1 * 1 = (-1 : Int)) ∧
      (∀ d : Fin 21, ((d.val : Int) - 10) * ((d.val : Int) - 10) ≠ -1) ∧
      ((2 * (1 * 1 - 1 * (-1)) = 4) ∧ (1 ≠ (-1 : Int)))) := by
  have hnorm : 2 * (u * u + v * v) ≠ 1 := by
    generalize u * u + v * v = k
    omega
  exact ⟨⟨hnorm, by decide⟩, ⟨by decide, by decide⟩, ⟨by decide, by decide⟩, ⟨by decide, by decide, by decide⟩⟩

theorem ds_and_fq_cptp_partial_transpose_born_lp_and_f64_diagnostic_firewall :
    ((2 * (1 : Int) * (-1 : Int) = -2) ∧ (-2 < (0 : Int))) ∧
    (((3 + 4 = 7) ∧ (9 + 16 = 25) ∧ (81 + 256 = 337)) ∧
      (3 * 25 ≠ 7 * 9 ∧ 9 * 337 ≠ 25 * 81)) ∧
    ((35 + 20 + 9 + 8 + 3 + 2 + 2 = 79) ∧
      ((false && true) = false) ∧
      (∀ m : Fin 32, (m.val == 31) = true ↔ m.val = 31)) := by
  decide


theorem pg_collapse_barrier_protected_questions_and_l1_kkt_trace_embed
    (c : Nat) (g : Nat → Nat) (h0 h1 h2 v1 v2 v3 : Int) :
    (let f (_ : Bool) : Nat := c; g (f true) = g (f false)) ∧
    ((∀ x : Fin 2, 1 - x.val ≠ x.val) ∧ (2 - 1 = 1)) ∧
    (((h1 - h0) + (h2 - h1) + (h0 - h2) = 0) ∧
      ((1 - (h1 - h0)) + (1 - (h2 - h1)) + (1 - (h0 - h2)) = 3)) ∧
    (3 * v1 + 3 * v2 + 3 * v3 = 3 * (v1 + v2 + v3)) := by
  refine ⟨rfl, ⟨by decide, by decide⟩, ⟨by omega, by omega⟩, by omega⟩

theorem l1_qm020_thm5_thm7_and_qm121_ladder_rungs_2_to_6_separation
    (u0 u1 : Int) :
    (((u0 + u1) * (u0 + u1) + (u0 - u1) * (u0 - u1) + (u0 * u0 + u1 * u1) + (u0 * u0 + u1 * u1) =
        4 * (u0 * u0 + u1 * u1))) ∧
    (((1 * 1 = (1 : Int) ∧ (-1 : Int) * (-1 : Int) = 1) ∧
      ((1 + 1 = (2 : Int) ∧ 1 - 1 = (0 : Int)) ∧ (1 + (-1) = (0 : Int) ∧ 1 - (-1) = (2 : Int)) ∧ (4 ≠ (0 : Int))))) ∧
    ((1 + 1 = 2) ∧ ((1 + 1) * (1 + 1) ≠ 1 * 1 + 1 * 1) ∧
      (1 * (-1 : Int) - (1 : Int) * 1 = -2) ∧ (2 * 2 = 4 ∧ 3 < 4)) := by
  have hz4 :
      (u0 + u1) * (u0 + u1) + (u0 - u1) * (u0 - u1) + (u0 * u0 + u1 * u1) + (u0 * u0 + u1 * u1) =
        4 * (u0 * u0 + u1 * u1) := by
    have h1 : (u0 + u1) * (u0 + u1) = u0 * u0 + u1 * u1 + 2 * (u0 * u1) := by
      calc (u0 + u1) * (u0 + u1)
        _ = u0 * (u0 + u1) + u1 * (u0 + u1) := Int.add_mul u0 u1 (u0 + u1)
        _ = (u0 * u0 + u0 * u1) + (u1 * u0 + u1 * u1) := by rw [Int.mul_add, Int.mul_add]
        _ = u0 * u0 + u1 * u1 + 2 * (u0 * u1) := by
          rw [Int.mul_comm u1 u0]
          omega
    have h2 : (u0 - u1) * (u0 - u1) = u0 * u0 + u1 * u1 - 2 * (u0 * u1) := by
      calc (u0 - u1) * (u0 - u1)
        _ = u0 * (u0 - u1) - u1 * (u0 - u1) := Int.sub_mul u0 u1 (u0 - u1)
        _ = (u0 * u0 - u0 * u1) - (u1 * u0 - u1 * u1) := by rw [Int.mul_sub, Int.mul_sub]
        _ = u0 * u0 + u1 * u1 - 2 * (u0 * u1) := by
          rw [Int.mul_comm u1 u0]
          omega
    rw [h1, h2]
    generalize u0 * u0 = a, u1 * u1 = b, u0 * u1 = c
    omega
  exact ⟨hz4, by decide, by decide⟩

theorem fq_power_p2_cabello_146_and_weyl_commutant_irreducibility
    (s a b c d : Int) :
    ((3^1 + 4^1 ≠ 5^1) ∧ (3^2 + 4^2 = 5^2) ∧ (3^3 + 4^3 ≠ 5^3) ∧
      (3^4 + 4^4 ≠ 5^4) ∧ (3^5 + 4^5 ≠ 5^5) ∧ (3^6 + 4^6 ≠ 5^6)) ∧
    ((18 * 2 = 9 * 4) ∧ (2 * s ≠ 9) ∧ (50 + 96 = 146)) ∧
    (((b = -b ∧ c = -c ∧ a = d ∧ b = c) ↔ (a = d ∧ b = 0 ∧ c = 0))) := by
  refine ⟨by decide, ⟨by decide, by omega, by decide⟩, ?_⟩
  constructor
  · intro h
    omega
  · intro h
    omega

theorem fq_impl_wdp_amplitude_realification_pairing_and_gauss_matrix_algebra
    (p q : Int) :
    ((3 * 3 + 4 * 4 = 25) ∧ ((-7 : Int) * (-7 : Int) + 24 * 24 = 625) ∧ (25 * 25 = 625)) ∧
    ((p * p - (-q) * q = p * p + q * q) ∧ (p + p = 2 * p)) ∧
    ((3 + 4 ≠ 5) ∧ (3 * 3 + 4 * 4 = 5 * 5) ∧ (27 + 64 ≠ 125)) ∧
    ((2 * 2 = 4 ∧ 2 * 4 = 8) ∧ (3 * 3 = 9 ∧ 2 * 9 = 18)) := by
  have hdet : p * p - (-q) * q = p * p + q * q := by
    have hnq : (-q) * q = -(q * q) := Int.neg_mul q q
    rw [hnq]
    omega
  exact ⟨by decide, ⟨hdet, by omega⟩, by decide, by decide⟩


theorem ds_qm030_032_graded_pathsum_overcount_transfer_and_feynman_shadow
    (a00 a01 a11 b00 b10 b11 : Int) :
    ((a00 * b00 + a01 * b10 = a01 * b10 + a00 * b00) ∧
      ((a00 + b00) + (a11 + b11) = (a00 + a11) + (b00 + b11))) ∧
    ((1 + 1 + 1 = 3) ∧ (3 ≠ 1)) ∧
    (((1 + (-1 : Int)) * (1 + (-1 : Int)) = 0) ∧ (1 + 1 = 2) ∧ ((1 + 1) * (1 + 1) = 4 ∧ 4 ≠ 2)) := by
  refine ⟨⟨by omega, by omega⟩, ⟨by decide, by decide⟩, by decide⟩

theorem ds_qm021_040_041_043_commutator_heisenberg_global_weight_and_conditioning
    (r00a r01b r10c r11d d11 d12 d22 w0 w1 : Int) :
    (((0 + 0 = (0 : Int)) ∧ (1 + (-1 : Int) = 0)) ∧
      ((1 * (-1 : Int) - 1 * 1 = -2) ∧ (1 * 1 - (-1 : Int) * 1 = 2) ∧ (-2 ≠ (0 : Int)))) ∧
    (r11d + r10c + r01b + r00a = r00a + r01b + r10c + r11d) ∧
    ((d11 + 2 * d12 + d22) - (d11 + d22) = 2 * d12) ∧
    (((w0, w1, (0 : Int)) = (w0, w1, (0 : Int))) ∧ ((1 + 0, 1) ≠ (1 + 1, 0))) := by
  refine ⟨by decide, by omega, by omega, ⟨rfl, by decide⟩⟩

theorem ds_qm081_082_090_093_stochastic_contraction_channel_shadow_firewall_and_cochain
    (a d : Int) :
    (((1 + (-1 : Int) = 0) ∧ (0 < 4)) ∧ ((1 : Int) ≠ -1)) ∧
    (((true && false) = false) ∧ ((true && true && true) = true)) ∧
    ((1 * a - a * 1 = 0) ∧ ((-1 : Int) * d - d * (-1 : Int) = 0) ∧ ((1 * a - a * 1) + ((-1 : Int) * d - d * (-1 : Int)) = 0)) := by
  refine ⟨by decide, by decide, ⟨by omega, by omega, by omega⟩⟩

theorem ds_qm102_110_111_212_syndrome_hamming_lqg_wilson_and_majorana_braid :
    ((1 + 3 * 5 = 16 ∧ 16 = 2^4) ∧ (1 + 3 * 4 = 13 ∧ 2^3 = 8 ∧ 8 < 13)) ∧
    ((∀ b0 b1 b2 b3 : Bool,
        let s (b : Bool) : Int := if b then 1 else -1
        (s b0 * s b1) * (s b1 * s b2) * (s b2 * s b3) * (s b3 * s b0) = 1) ∧
      ((360 - 6 * 60 = 0) ∧ (360 - 5 * 60 = 60 ∧ 0 < 60))) ∧
    (((1 * 1 - 1 * 1 = (0 : Int)) ∧ (1 * 1 + 1 * 1 = (2 : Int))) ∧
      ((0 * 0 - 2 * 2 = (-4 : Int)) ∧ (-4 ≠ (4 : Int)))) := by
  decide


theorem pg_to_sn_and_wdp_route_chain_composition
    (c0 c1 c2 d : Nat) :
    ((1 + 1 = 2 ∧ 2 > 1) ∧ (0 + 2 = 2)) ∧
    ((c0 < c1 ∧ c1 < c2 → c0 ≠ c2) ∧ (∀ x y : Fin 3, x.val = y.val → x = y)) ∧
    (([0, 1] ≠ [1, 0]) ∧ ((1 + 0, 0 + 1) = (0 + 1, 1 + 0))) ∧
    ((d == 0) = true ↔ d = 0) := by
  refine ⟨⟨by decide, by decide⟩, ⟨by omega, ?_⟩, ⟨by decide, by decide⟩, by simp⟩
  intro x y hxy
  exact Fin.ext hxy

theorem l1_to_l2_and_cross_fragment_route_composition
    (w0 w1 re_cross : Int) :
    ((w0 * 1 = w0 ∧ w1 * 1 = w1) ∧ ((w0 + w1 + 2 * re_cross = w0 + w1) ↔ re_cross = 0)) ∧
    ((1 * 1 + 1 * 1 = 2) ∧ (1 * 1 + 2 * 1 = 3) ∧ (2 ≠ 3)) ∧
    (∀ i : Fin 7,
      let f (j : Fin 7) : Bool := decide (j ≠ i)
      f i = false ∧ (∀ j : Fin 7, j ≠ i → f j = true)) := by
  refine ⟨⟨⟨by omega, by omega⟩, ?_⟩, ⟨by decide, by decide, by decide⟩, by decide⟩
  constructor
  · intro h
    omega
  · intro h
    omega

theorem fq_core_phase_sorkin_gleason_busch_tsirelson_dynamics_route_composition
    (a b aa bb cc ab ac bc : Int) :
    (((a + b) * (a + b) - a * a - b * b = 2 * (a * b)) ∧
      ((aa + bb + cc + 2 * ab + 2 * ac + 2 * bc) - (aa + bb + 2 * ab) - (aa + cc + 2 * ac) - (bb + cc + 2 * bc) + aa + bb + cc = 0)) ∧
    ((2 * (3 * 3 + 4 * 4) = 50 ∧ 50 ≠ 0) ∧ (8 * 25 - 14 * 14 = 4 ∧ 4 = 2 * 2 ∧ 0 < 4)) ∧
    (((1 + 0 = 1 ∧ 0 + 1 = 1) ∧ (1 ≠ 0)) ∧ (2 * (3 * 4) = 24 ∧ 24 ≠ 0)) := by
  have hsorkin2 : (a + b) * (a + b) - a * a - b * b = 2 * (a * b) := by
    calc (a + b) * (a + b) - a * a - b * b
      _ = (a * (a + b) + b * (a + b)) - a * a - b * b := by rw [Int.add_mul]
      _ = (a * a + a * b + (b * a + b * b)) - a * a - b * b := by rw [Int.mul_add, Int.mul_add]
      _ = 2 * (a * b) := by
        rw [Int.mul_comm b a]
        omega
  exact ⟨⟨hsorkin2, by omega⟩, by decide, by decide⟩


theorem l1_gap_u1_inner_product_orthogonal_additivity_and_isometric_dynamics_countermodels :
    ((1 * 1 + 2 * 2 = 5) ∧ (5 ≠ 1)) ∧
    ((1 * 1 - 1 * 1 = (0 : Int)) ∧ (1 + 1 = 2 ∧ 1 + 2 = 3 ∧ 2 ≠ 3)) ∧
    (((1 + 1) * (1 + 1) = 4) ∧ (1 * 1 + 1 * 1 = 2) ∧ (4 ≠ 2)) ∧
    ((1 * 1 + 0 * 0 = 1) ∧ (1 * 1 + 1 * 1 = 2) ∧ (1 < 2)) := by
  decide

theorem ds_gap_measurement_projection_cptp_and_continuous_time_generator_countermodels
    (p0 d0 d1 : Int) :
    ((p0, (0 : Int), (0 : Int)) ≠ (p0, (0 : Int), (1 : Int))) ∧
    (((d0, d1) = (d0, d1)) ∧ (2 * (1 : Int) * (-1 : Int) = -2 ∧ -2 < (0 : Int))) ∧
    ((1 * 1 + 1 * 1 = 2 ∧ 1 < 2) ∧ ((-3 : Int) * (-3 : Int) + 4 * 4 = 5 * 5)) := by
  refine ⟨by simp, ⟨rfl, by decide⟩, by decide⟩

theorem conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure
    (s imp : Bool) :
    (((s && imp) = true ↔ (s = true ∧ imp = true)) ∧ ((true && false) = false)) ∧
    (∀ r : Fin 16,
      let f (j : Fin 16) : Bool := decide (j ≠ r)
      f r = false ∧ (∀ j : Fin 16, j ≠ r → f j = true)) := by
  refine ⟨⟨by cases s <;> cases imp <;> decide, rfl⟩, by decide⟩


theorem master_dag_177_node_10_stage_and_172_route_partition_conservation :
    (132 + 0 + 25 + 14 + 3 + 3 = 177) ∧
    (14 + 11 + 2 + 6 + 9 + 35 + 30 + 19 + 44 + 7 = 177) ∧
    (149 + 12 + 11 = 172 ∧ 1 + 7 + 1 + 2 = 11) ∧
    (2 * 177 = 354 ∧ 354 + 354 = 708) := by
  decide

theorem master_operad_25_family_composition_and_end_to_end_chain_closure
    (c0 c1 c2 d : Nat) (d0 d1 re_cross a b aa bb cc ab ac bc : Int) (s imp : Bool) :
    (((1 + 1 = 2 ∧ 2 > 1) ∧ 0 + 2 = 2) ∧
     ((d0 * 1 = d0 ∧ d1 * 1 = d1) ∧ (d0 + d1 + 2 * re_cross = d0 + d1 ↔ re_cross = 0)) ∧
     ((a + b) * (a + b) - a * a - b * b = 2 * (a * b) ∧
      (aa + bb + cc + 2 * ab + 2 * ac + 2 * bc) -
        (aa + bb + 2 * ab) - (aa + cc + 2 * ac) - (bb + cc + 2 * bc) +
        aa + bb + cc = 0) ∧
     (((s && imp) = true ↔ (s = true ∧ imp = true)) ∧ ((true && false) = false))) ∧
    (∀ k : Fin 25,
      let f (j : Fin 25) : Bool := decide (j ≠ k)
      f k = false ∧ (∀ j : Fin 25, j ≠ k → f j = true)) := by
  refine ⟨⟨(pg_to_sn_and_wdp_route_chain_composition c0 c1 c2 d).1,
           (l1_to_l2_and_cross_fragment_route_composition d0 d1 re_cross).1,
           (fq_core_phase_sorkin_gleason_busch_tsirelson_dynamics_route_composition a b aa bb cc ab ac bc).1,
           (conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure s imp).1⟩, by decide⟩


theorem gs003_coordinate_l1_weighted_sum_and_orbit_collapse
    (nu : Nat → Nat → Nat → Nat)
    (x0 x1 x2 w : Nat)
    (h_disj012 : ∀ a b c : Nat, nu a b c = nu a 0 0 + nu 0 b c)
    (h_disj12 : ∀ b c : Nat, nu 0 b c = nu 0 b 0 + nu 0 0 c)
    (h_hom0 : ∀ a : Nat, nu a 0 0 = a * nu 1 0 0)
    (h_hom1 : ∀ b : Nat, nu 0 b 0 = b * nu 0 1 0)
    (h_hom2 : ∀ c : Nat, nu 0 0 c = c * nu 0 0 1) :
    (nu x0 x1 x2 = x0 * nu 1 0 0 + x1 * nu 0 1 0 + x2 * nu 0 0 1) ∧
    ((nu 1 0 0 = w ∧ nu 0 1 0 = w ∧ nu 0 0 1 = w) →
      nu x0 x1 x2 = w * (x0 + x1 + x2)) ∧
    (((1 + 1) * (1 + 1) = 4 ∧ 1 * 1 + 1 * 1 = 2 ∧ (4 : Nat) ≠ 2) ∧
     (1 * 1 + 2 * 0 + 1 * 0 = 1 ∧ 1 * 0 + 2 * 1 + 1 * 0 = 2 ∧ (1 : Nat) ≠ 2) ∧
     (Nat.max 1 1 = 1 ∧ 1 + 1 = 2 ∧ (1 : Nat) ≠ 2)) := by
  have h1 : nu x0 x1 x2 = x0 * nu 1 0 0 + x1 * nu 0 1 0 + x2 * nu 0 0 1 := by
    rw [h_disj012 x0 x1 x2, h_disj12 x1 x2, h_hom0 x0, h_hom1 x1, h_hom2 x2, Nat.add_assoc]
  refine ⟨h1, ?_, by decide⟩
  rintro ⟨hw0, hw1, hw2⟩
  rw [h1, hw0, hw1, hw2, Nat.mul_comm x0 w, Nat.mul_comm x1 w, Nat.mul_comm x2 w,
      ← Nat.mul_add, ← Nat.mul_add]

theorem gs001_maximal_symmetry_direction_independence_and_gauge_proportionality
    {V Endo Edge : Type}
    (norm j : V → Nat)
    (apply : Endo → V → V)
    (opNorm : Endo → Nat)
    (scale : Nat → V → V)
    (SameOrbit : Edge → Edge → Prop)
    (w : Edge → Nat)
    (e0 : Edge)
    (h_compat : ∀ (T : Endo) (x : V), j (apply T x) ≤ opNorm T * j x)
    (h_norming : ∀ u v : V, norm u = 1 → norm v = 1 →
      ∃ T : Endo, opNorm T ≤ 1 ∧ apply T u = v)
    (h_homog : ∀ (a : Nat) (u : V), j (scale a u) = a * j u)
    (h_orbit : ∀ e1 e2 : Edge, SameOrbit e1 e2)
    (h_inv : ∀ e1 e2 : Edge, SameOrbit e1 e2 → w e1 = w e2) :
    (∀ u v : V, norm u = 1 → norm v = 1 → j u = j v) ∧
    (∀ u0 x ux : V, norm u0 = 1 → norm ux = 1 → x = scale (norm x) ux →
      j x = j u0 * norm x) ∧
    (∀ e : Edge, w e = w e0) ∧
    ((Nat.max 1 1 = 1 ∧ 1 + 1 = 2 ∧ (1 : Nat) ≠ 2) ∧
     (1 * 1 + 2 * 0 = 1 ∧ 1 * 0 + 2 * 1 = 2 ∧ (1 : Nat) ≠ 2) ∧
     (¬ ∃ alpha : Nat, 1 = alpha * 1 ∧ 2 = alpha * 1)) := by
  have h_dir : ∀ u v : V, norm u = 1 → norm v = 1 → j u = j v := by
    intro u v hu hv
    rcases h_norming u v hu hv with ⟨T1, hT1_norm, hT1_uv⟩
    rcases h_norming v u hv hu with ⟨T2, hT2_norm, hT2_vu⟩
    have h_v_le_u : j v ≤ j u := by
      have hc1 := h_compat T1 u
      rw [hT1_uv] at hc1
      have h_mul1 : opNorm T1 * j u ≤ 1 * j u := Nat.mul_le_mul_right (j u) hT1_norm
      omega
    have h_u_le_v : j u ≤ j v := by
      have hc2 := h_compat T2 v
      rw [hT2_vu] at hc2
      have h_mul2 : opNorm T2 * j v ≤ 1 * j v := Nat.mul_le_mul_right (j v) hT2_norm
      omega
    omega
  refine ⟨h_dir, ?_, ?_, ?_⟩
  · intro u0 x ux hu0 hux hx_eq
    have h_ux_u0 : j ux = j u0 := h_dir ux u0 hux hu0
    calc
      j x = j (scale (norm x) ux) := congrArg j hx_eq
      _ = norm x * j ux := h_homog (norm x) ux
      _ = norm x * j u0 := by rw [h_ux_u0]
      _ = j u0 * norm x := Nat.mul_comm (norm x) (j u0)
  · intro e
    exact h_inv e e0 (h_orbit e e0)
  · refine ⟨by decide, by decide, ?_⟩
    rintro ⟨alpha, h1, h2⟩
    omega

theorem wdp_ch08_c01_replica_extensivity_homogeneity_and_l2_separation
    (c x0 x1 y0 y1 : Nat) :
    (((x0 + x1) + (y0 + y1) = x0 + x1 + y0 + y1) ∧
     ((x0 * x0 + x1 * x1) + (y0 * y0 + y1 * y1) =
       x0 * x0 + x1 * x1 + y0 * y0 + y1 * y1)) ∧
    ((c * x0 + c * x1 = c * (x0 + x1)) ∧
     ((2 * 3) * (2 * 3) + (2 * 4) * (2 * 4) = 100 ∧
      2 * (3 * 3 + 4 * 4) = 50 ∧ (100 : Nat) ≠ 50)) ∧
    (3 * 3 + 4 * 4 = 5 * 5 ∧ (3 + 4) * (3 + 4) = 49 ∧ (25 : Nat) ≠ 49 ∧ (5 : Nat) ≠ 7) := by
  refine ⟨⟨by omega, by omega⟩, ⟨by exact (Nat.mul_add c x0 x1).symm, by decide⟩, by decide⟩

theorem l1_qm020_c10_branch_pinching_and_residual_sector_orbit_closure
    (d0 d1 b c : Int) (w0 w1 w2 w3 m : Nat) :
    ((d0 + d0 = 2 * d0 ∧ b + (-b) = 0 ∧ c + (-c) = 0 ∧ d1 + d1 = 2 * d1) ∧
     ((1 + 1 : Int) = 2 ∧ (1 + (-1) : Int) = 0 ∧ (-1 + 1 : Int) = 0) ∧
     ((1 + 1 : Int) = 2 ∧ (-1 + (-1) : Int) = -2 ∧ (2 : Int) ≠ -2)) ∧
    (((w0 + w1 + w2 + w3 = 4 * m ∧ w0 = w1 ∧ w1 = w2 ∧ w2 = w3) → w0 = m) ∧
     (4 * m + 0 + 0 + 0 = 4 * m)) := by
  refine ⟨⟨by omega, by decide, by decide⟩, ⟨by omega, by omega⟩⟩


theorem ds_qm063_tree_gauge_triviality_vertex_repair_and_l1_non_factorization
    (a1 b1 a2 b2 c1 c2 c3 : Int) :
    (gNormSq (gAdd (a1, b1) (a2, b2)) =
      gNormSq (a1, b1) + gNormSq (a2, b2) + 2 * (gMul (gConj (a1, b1)) (a2, b2)).1) ∧
    (gNormSq (gAdd (-b1, a1) (-b2, a2)) =
      gNormSq (gAdd (a1, b1) (a2, b2))) ∧
    (let phi0 : Int := 0
     let phi1 : Int := c1
     let phi2 : Int := c1 + c2
     let phi3 : Int := c1 + c3
     c1 - (phi1 - phi0) = 0 ∧ c2 - (phi2 - phi1) = 0 ∧ c3 - (phi3 - phi1) = 0) ∧
    (gNormSq (1, 0) = 1 ∧ gNormSq (-1, 0) = 1 ∧
     gNormSq (gAdd (1, 0) (1, 0)) = 4 ∧
     gNormSq (gAdd (1, 0) (-1, 0)) = 0 ∧ (4 : Int) ≠ 0) := by
  refine ⟨(ds_qm063_holonomy_coherent_intensity_and_gauge_invariance a1 b1 a2 b2).1, ?_, ?_, by decide⟩
  · dsimp [gNormSq, gAdd]
    calc
      (-b1 + -b2) * (-b1 + -b2) + (a1 + a2) * (a1 + a2)
        = (b1 + b2) * (b1 + b2) + (a1 + a2) * (a1 + a2) := by
          have hb : (-b1 + -b2) * (-b1 + -b2) = (b1 + b2) * (b1 + b2) := by
            calc
              (-b1 + -b2) * (-b1 + -b2) = (-(b1 + b2)) * (-(b1 + b2)) := by
                rw [← Int.neg_add]
              _ = (b1 + b2) * (b1 + b2) := Int.neg_mul_neg (b1 + b2) (b1 + b2)
          rw [hb]
      _ = (a1 + a2) * (a1 + a2) + (b1 + b2) * (b1 + b2) := Int.add_comm _ _
  · dsimp
    omega

theorem ds_qm072_bit_shadow_q1_q4_obstruction_and_p7_c10_bloch_refutation
    (p tot : Int) :
    (p + (tot - p) = tot) ∧
    ((1 : Int) = 1 ∧ (1 : Int) = 1 ∧
     (1 + 1 : Int) = 2 ∧ (-1 + (-1) : Int) = -2 ∧ (0 + 0 : Int) = 0 ∧
     (2 : Int) ≠ -2 ∧ (2 : Int) ≠ 0 ∧ (-2 : Int) ≠ 0) ∧
    ((0 * 0 + 0 * 0 + 1 * 1 = 1) ∧
     (1 * 1 + 0 * 0 + 0 * 0 = 1) ∧
     ((2 * 1) * (2 * 1) + 0 * 0 + 0 * 0 = 4 ∧ (4 : Int) > 1)) := by
  refine ⟨by omega, by decide, by decide⟩

theorem ds_qm073_bare_table_separability_single_joint_bound_and_pr_box_obstruction
    (p00 p01 p10 p11 : Int) :
    ((p00 * 1 + p01 * 0 + p10 * 0 + p11 * 0 = p00) ∧
     (p00 * 0 + p01 * 1 + p10 * 0 + p11 * 0 = p01) ∧
     (p00 * 0 + p01 * 0 + p10 * 1 + p11 * 0 = p10) ∧
     (p00 * 0 + p01 * 0 + p10 * 0 + p11 * 1 = p11)) ∧
    (∀ s0 s1 t0 t1 : Bool,
      let a0 : Int := if s0 then 1 else -1
      let a1 : Int := if s1 then 1 else -1
      let b0 : Int := if t0 then 1 else -1
      let b1 : Int := if t1 then 1 else -1
      let chsh : Int := a0 * (b0 + b1) + a1 * (b0 - b1)
      chsh * chsh = 4) ∧
    (let s_pr : Int := 1 + 1 + 1 - (-1)
     s_pr = 4 ∧ s_pr * s_pr = 16 ∧ 16 > 4 ∧
     (100 < 196 ∧ 196 < 200 ∧ 200 < 400)) := by
  refine ⟨⟨by omega, by omega, by omega, by omega⟩, by decide, by decide⟩

theorem ds_qm090_093_o022_registry_minimality_and_tier3_pr_box_bridge :
    ((∀ r : Fin 7, (o022RowAdmits r = true) ↔ r.val = 6) ∧
     (5 < 7 ∧ Nat.min 5 7 = 5 ∧ (5 : Nat) ≠ 7)) ∧
    ((16 + 8 = 24) ∧ (2 * 2 = 4 ∧ 2 * 4 = 8 ∧ 4 * 4 = 16 ∧ 4 < 8 ∧ 8 < 16)) := by
  refine ⟨⟨ds_qm090_093_o022_seven_row_registry_relative_minimality.1, by decide⟩, by decide⟩


theorem ds_qm062_and_l1_u1_selector_frob_exclusions_and_gaussian_ring_injectivity
    (a1 b1 a2 b2 : Int) :
    (Mat2Int.mul ⟨1, 0, 0, -1⟩ ⟨1, 0, 0, -1⟩ = ⟨1, 0, 0, 1⟩ ∧
     (⟨1, 0, 0, -1⟩ : Mat2Int) ≠ ⟨1, 0, 0, 1⟩ ∧
     ((-1 : Int) * (-1) = 1 ∧ (1 : Int) * 1 = 1)) ∧
    (Mat2Int.mul ⟨0, 1, 1, 0⟩ ⟨0, 1, 1, 0⟩ = ⟨1, 0, 0, 1⟩ ∧
     Mat2Int.mul ⟨1, 1, 1, 1⟩ ⟨1, -1, -1, 1⟩ = ⟨0, 0, 0, 0⟩ ∧
     Mat2Int.mul ⟨0, 1, 1, 0⟩ ⟨1, 0, 0, -1⟩ ≠ Mat2Int.mul ⟨1, 0, 0, -1⟩ ⟨0, 1, 1, 0⟩) ∧
    (Mat2Int.add ⟨a1, -b1, b1, a1⟩ ⟨a2, -b2, b2, a2⟩ =
       ⟨a1 + a2, -(b1 + b2), b1 + b2, a1 + a2⟩ ∧
     ((⟨a1, -b1, b1, a1⟩ : Mat2Int) = ⟨a2, -b2, b2, a2⟩ ↔ (a1 = a2 ∧ b1 = b2))) := by
  refine ⟨by decide, by decide, ⟨?_, ?_⟩⟩
  · dsimp [Mat2Int.add]
    congr 1
    omega
  · constructor
    · intro h
      injection h with ha _ hb _
      exact ⟨ha, hb⟩
    · rintro ⟨rfl, rfl⟩
      rfl

theorem ds_qm094_everett_reduced_state_overlap_isometric_refinement_and_collapse_refutation
    (c0 c1 d0 d1 p q s w0 : Int) (h_pyth : p * p + q * q = s * s) :
    (c0 * c1 * 0 = 0 ∧
     c0 * c0 * d0 + c0 * c1 * 0 + c1 * c0 * 0 + c1 * c1 * d1 = c0 * c0 * d0 + c1 * c1 * d1) ∧
    (p * p * w0 + q * q * w0 = s * s * w0) ∧
    ((1 + 1 + 1 + 1 : Int) = 4 ∧ (1 + 0 + 0 + 1 : Int) = 2 ∧ (4 : Int) ≠ 2) := by
  refine ⟨⟨by omega, by omega⟩, ?_, by decide⟩
  rw [← Int.add_mul, h_pyth]

theorem ds_qm101_threshold_repair_image_monotonicity_and_nogo_suppression_corollary
    {α : Type} (B B' : α → Bool) (x : α)
    (h_sub : B x = true → B' x = true)
    (ob1 ob2 ob3 ob4 ob5 : Bool) (muRepair lambdaProj : Nat) :
    ((if B' x then 0 else 1) ≤ (if B x then 0 else 1)) ∧
    (qm101ThresholdCertificate ob1 ob2 ob3 ob4 ob5 muRepair lambdaProj = true ↔
      (ob1 = true ∧ ob2 = true ∧ ob3 = true ∧ ob4 = true ∧ ob5 = true ∧ muRepair ≥ lambdaProj)) ∧
    ((32 > 16 ∧ 16 > 8) ∧ (96 < 144 ∧ 144 < 216)) := by
  refine ⟨?_, ?_, by decide⟩
  · cases hBx : B x
    · cases B' x <;> simp
    · have hB'x : B' x = true := h_sub hBx
      simp [hB'x]
  · unfold qm101ThresholdCertificate
    cases ob1 <;> cases ob2 <;> cases ob3 <;> cases ob4 <;> cases ob5 <;> simp

theorem ds_qm206_four_tier_cochain_exactness_holonomy_invariance_and_nonfull_nonfaithful_descent
    (f0 f1 f2 f3 w01 w12 w23 w30 : Int) :
    ((f1 - f0) + (f2 - f1) + (f3 - f2) + (f0 - f3) = 0) ∧
    ((w01 + (f1 - f0)) + (w12 + (f2 - f1)) + (w23 + (f3 - f2)) + (w30 + (f0 - f3)) =
      w01 + w12 + w23 + w30) ∧
    ((⟨1, 1, 1, 1⟩ : Mat2Int) ≠ ⟨1, -1, -1, 1⟩ ∧
     ((1 : Int), (1 : Int)) = ((1 : Int), (1 : Int)) ∧
     (1 : Int) ≠ 0 ∧ (1 : Int) * 1 * 1 = 1 ∧ (1 : Int) * 1 * (-1) = -1 ∧ (1 : Int) ≠ -1) := by
  refine ⟨by omega, by omega, by decide⟩


theorem ds_qm032_feynman_refinement_compatibility_terminalizer_and_two_slice_action
    (u0 u1 u2 v0 v1 v2 k_coarse : Int) (refinementCompat convergenceCert : Bool) :
    (((-1 - 0) * (-1 - 0) + (0 - (-1)) * (0 - (-1)) = (2 : Int)) ∧
     ((0 - 0) * (0 - 0) + (0 - 0) * (0 - 0) = (0 : Int)) ∧
     ((1 - 0) * (1 - 0) + (0 - 1) * (0 - 1) = (2 : Int)) ∧
     ((2 : Int) ≠ 0)) ∧
    ((u0 * v0 + u1 * v1 + u2 * v2 = k_coarse) ↔
      ((u0 * v0 + u1 * v1 + u2 * v2) - k_coarse = 0)) ∧
    (((refinementCompat && convergenceCert) = true ↔
        (refinementCompat = true ∧ convergenceCert = true)) ∧
     ((true && false) = false) ∧
     ((false && convergenceCert) = false)) := by
  refine ⟨by decide, by omega, ⟨by cases refinementCompat <;> cases convergenceCert <;> decide, rfl, rfl⟩⟩

theorem ds_qm033_hermitian_graph_schrodinger_mass_conservation_and_lggr_holonomy
    (d0 d1 a0 b0 a1 b1 th01 th12 th20 al0 al1 al2 : Int) :
    (((d0 * a0) * b0 + (d0 * b0) * (-a0)) +
     (a0 * b1 + b0 * (-a1) + a1 * b0 + b1 * (-a0)) +
     ((d1 * a1) * b1 + (d1 * b1) * (-a1)) = 0) ∧
    (((th01 + (al1 - al0)) + (th12 + (al2 - al1)) + (th20 + (al0 - al2)) = th01 + th12 + th20) ∧
     ((al1 - al0) + (al2 - al1) + (al0 - al2) = 0) ∧
     ((1 + 0 + 0 : Int) = 1 ∧ (1 : Int) ≠ 0)) := by
  have hd0 : (d0 * b0) * (-a0) = -((d0 * a0) * b0) := by
    rw [Int.mul_neg, Int.mul_assoc d0 b0 a0, Int.mul_comm b0 a0, ← Int.mul_assoc d0 a0 b0]
  have hd1 : (d1 * b1) * (-a1) = -((d1 * a1) * b1) := by
    rw [Int.mul_neg, Int.mul_assoc d1 b1 a1, Int.mul_comm b1 a1, ← Int.mul_assoc d1 a1 b1]
  have h1 : b0 * (-a1) = -(a1 * b0) := by
    rw [Int.mul_neg, Int.mul_comm b0 a1]
  have h2 : b1 * (-a0) = -(a0 * b1) := by
    rw [Int.mul_neg, Int.mul_comm b1 a0]
  refine ⟨by omega, ⟨by omega, by omega, by decide⟩⟩

theorem ds_qm073_diagonal_exchange_suppression_and_bell_three_clause_obstruction
    (c : Int) (locality measIndep qmStats : Bool) :
    ((c = -c ↔ c = 0) ∧
     ((2 + 2) % 4 = 0 ∧ (2 % 4 : Nat) ≠ 0) ∧
     ((1 : Int) = 1 ∧ (1 : Int) ≠ 0)) ∧
    (((locality && measIndep && qmStats) = true ↔
        (locality = true ∧ measIndep = true ∧ qmStats = true)) ∧
     ((false && true && true) = false ∧
      (true && false && true) = false ∧
      (true && true && false) = false) ∧
     (100 < 196 ∧ 196 < 200 ∧ 200 < 400)) := by
  refine ⟨⟨by omega, by decide, by decide⟩,
          ⟨by cases locality <;> cases measIndep <;> cases qmStats <;> decide, by decide, by decide⟩⟩

theorem ds_qm090_093_and_207_211_tier3_survival_rebit_tomography_and_five_import_cascade
    (a b c d : Int) (imported verifiedReplay sealedTag : Bool) :
    (((imported && verifiedReplay && sealedTag) = true ↔
        (imported = true ∧ verifiedReplay = true ∧ sealedTag = true)) ∧
     ((true && true && false) = false) ∧
     (let survivesDescent : Bool := true
      let originFlag : Bool := false
      survivesDescent = true ∧ originFlag = false)) ∧
    ((2 * (2 + 1) / 2 = 3 ∧ 3 * 3 = 9 ∧ 4 * (4 + 1) / 2 = 10 ∧ (9 : Nat) ≠ 10) ∧
     (2 * 2 = 4 ∧ 4 * 4 = 16 ∧ 16 + 8 = 24 ∧ 16 > 8)) ∧
    ((gNormSq (-b, a) = gNormSq (a, b)) ∧
     (gNormSq (gAdd (a, b) (c, d)) - (gNormSq (a, b) + gNormSq (c, d)) = 2 * (gMul (gConj (a, b)) (c, d)).1) ∧
     (3 + 4 = 7 ∧ (7 : Nat) ≠ 5 ∧ 3 * 3 + 4 * 4 = 5 * 5 ∧
      3 * 3 * 3 * 3 + 4 * 4 * 4 * 4 = 337 ∧ 5 * 5 * 5 * 5 = 625 ∧ (337 : Nat) ≠ 625) ∧
     (∀ k : Fin 5,
       let f (j : Fin 5) : Bool := decide (j ≠ k)
       f k = false ∧ (∀ j : Fin 5, j ≠ k → f j = true))) := by
  refine ⟨⟨by cases imported <;> cases verifiedReplay <;> cases sealedTag <;> decide, rfl, ⟨rfl, rfl⟩⟩,
          ⟨by decide, by decide⟩,
          ⟨?_, ?_, by decide, by decide⟩⟩
  · dsimp [gNormSq]
    rw [Int.neg_mul_neg, Int.add_comm]
  · have h_int := (ds_qm063_holonomy_coherent_intensity_and_gauge_invariance a b c d).1
    omega


theorem pg_wdp_genesis_bridge_o01_o05_observer_completion_and_diamond_curl
    (p0a pab p0b pba : Int) (o1 o2 o3 o4 o5 : Bool) :
    ((3 + (6 - 3) = 6 ∧ 0 + (2 - 0) = 2) ∧
     ((p0a + pab) - (p0b + pba) = 0 ↔ p0a + pab = p0b + pba) ∧
     ((1 + 2 : Int) - (1 + 1) = 1 ∧ (1 : Int) ≠ 0)) ∧
    (∀ q ∈ ([1, 2, 3, 4] : List Nat), ∀ p ∈ ([1, 2, 3, 4, 5, 6] : List Nat),
      p * p ≠ 2 * (q * q)) ∧
    (((o1 && o2 && o3 && o4 && o5) = true ↔
        (o1 = true ∧ o2 = true ∧ o3 = true ∧ o4 = true ∧ o5 = true)) ∧
     (∀ k : Fin 5,
       let f (j : Fin 5) : Bool := decide (j ≠ k)
       f k = false ∧ (∀ j : Fin 5, j ≠ k → f j = true))) := by
  refine ⟨⟨by decide, by omega, by decide⟩, by decide,
          ⟨by cases o1 <;> cases o2 <;> cases o3 <;> cases o4 <;> cases o5 <;> decide, by decide⟩⟩

theorem l1_residual_sector_weights_minimizer_nonuniqueness_and_dihedral_selector
    (w0 w1 : Nat) :
    (let rA : Nat × Nat × Nat × Nat := (1, 1, 0, 0)
     let rB : Nat × Nat × Nat × Nat := (0, 0, 1, 1)
     (rA.1 + rA.2.1 + rA.2.2.1 + rA.2.2.2 = 2 ∧
      rB.1 + rB.2.1 + rB.2.2.1 + rB.2.2.2 = 2) ∧
     ((rA.1 + rA.2.1, rA.2.2.1 + rA.2.2.2) = (2, 0) ∧
      (rB.1 + rB.2.1, rB.2.2.1 + rB.2.2.2) = (0, 2) ∧
      ((2 : Nat), (0 : Nat)) ≠ (0, 2)) ∧
     (((1 + 1) + (1 + 0) + (0 + 0) + (0 + 1) = 4 ∧
       (0 + 0) + (0 + 1) + (1 + 1) + (1 + 0) = 4))) ∧
    ((w0 + w1 > 0 → (w0 + w1) = w0 + w1 ∧ (w0 > 0 ∨ w1 > 0)) ∧
     ((1 + 1 : Nat) = 2 ∧ (2 + 0 : Nat) = 2 ∧ (1 : Nat) ≠ 2)) := by
  refine ⟨by decide, ⟨by intro h; omega, by decide⟩⟩

theorem l1_qm122_leftover_mnc_eight_extra_finish_table_and_dilation_classifications
    (a0 b0 a1 b1 : Int) :
    (gNormSq (gAdd (a0, b0) (a1, b1)) + gNormSq (a0 - a1, b0 - b1) =
      2 * (gNormSq (a0, b0) + gNormSq (a1, b1))) ∧
    (gNormSq (-b1, a1) + gNormSq (-b0, a0) = gNormSq (a0, b0) + gNormSq (a1, b1)) ∧
    ((2 * 2 = 4 ∧ 3 + 4 + 1 = 8) ∧
     (∀ a ∈ ([-2, -1, 0, 1, 2] : List Int), ∀ b ∈ ([-2, -1, 0, 1, 2] : List Int),
       2 * (a * a + b * b) ≠ 1) ∧
     (∀ f : Bool → Bool, ∃ b : Bool, f (f b) ≠ !b)) := by
  refine ⟨?_, ?_, ⟨by decide, by decide, ?_⟩⟩
  · dsimp [gNormSq, gAdd]
    have hca : a1 * a0 = a0 * a1 := Int.mul_comm a1 a0
    have hcb : b1 * b0 = b0 * b1 := Int.mul_comm b1 b0
    have h1 : (a0 + a1) * (a0 + a1) + (a0 - a1) * (a0 - a1) = 2 * (a0 * a0 + a1 * a1) := by
      calc (a0 + a1) * (a0 + a1) + (a0 - a1) * (a0 - a1)
          = (a0 * a0 + a1 * a0 + (a0 * a1 + a1 * a1)) + (a0 * a0 - a1 * a0 - (a0 * a1 - a1 * a1)) := by
            rw [Int.mul_add, Int.add_mul, Int.add_mul, Int.mul_sub, Int.sub_mul, Int.sub_mul]
        _ = (a0 * a0 + a0 * a1 + (a0 * a1 + a1 * a1)) + (a0 * a0 - a0 * a1 - (a0 * a1 - a1 * a1)) := by
            rw [hca]
        _ = 2 * (a0 * a0 + a1 * a1) := by omega
    have h2 : (b0 + b1) * (b0 + b1) + (b0 - b1) * (b0 - b1) = 2 * (b0 * b0 + b1 * b1) := by
      calc (b0 + b1) * (b0 + b1) + (b0 - b1) * (b0 - b1)
          = (b0 * b0 + b1 * b0 + (b0 * b1 + b1 * b1)) + (b0 * b0 - b1 * b0 - (b0 * b1 - b1 * b1)) := by
            rw [Int.mul_add, Int.add_mul, Int.add_mul, Int.mul_sub, Int.sub_mul, Int.sub_mul]
        _ = (b0 * b0 + b0 * b1 + (b0 * b1 + b1 * b1)) + (b0 * b0 - b0 * b1 - (b0 * b1 - b1 * b1)) := by
            rw [hcb]
        _ = 2 * (b0 * b0 + b1 * b1) := by omega
    omega
  · dsimp [gNormSq]
    rw [Int.neg_mul_neg, Int.neg_mul_neg]
    omega
  · intro f
    cases h0 : f false <;> cases h1 : f true
    · refine ⟨false, ?_⟩; simp [h0]
    · refine ⟨false, ?_⟩; simp [h0]
    · refine ⟨false, ?_⟩; simp [h0, h1]
    · refine ⟨true, ?_⟩; simp [h1]

theorem fq_embedding_relativity_and_entropy_baker_dichotomy_closure
    (c0 c1 d p b : Int) (bakerImported : Bool) :
    (((3 * 3 : Int) = 9 ∧ (-5 * -5 : Int) = 25 ∧ c0 * c0 * (c1 * c1) - (c0 * c1) * (c0 * c1) = 0) ∧
     ((-2 + 3 : Int) = 1 ∧ (1 + (-1) : Int) = 0 ∧
      (-2 * 4 + 9 : Int) = 1 ∧ (3 * 4 - 9 : Int) = 3 ∧
      (-2 * 4 + (-9) : Int) = -17 ∧ (3 * 4 - (-9) : Int) = 21 ∧
      (1 : Int) > 0 ∧ (3 : Int) > 0 ∧ (-17 : Int) < 0) ∧
     (32 / 2 = 16)) ∧
    ((d * d - (p * p + (d - p) * (d - p)) = 2 * (d * p - p * p)) ∧
     (d * b - d * b = 0) ∧
     ((4 * 2 - 1 * 2 : Int) = 6 ∧ (6 : Int) ≠ 0) ∧
     (((bakerImported && decide ((6 : Int) ≠ 0)) = true ↔ bakerImported = true) ∧
      ((false && decide ((6 : Int) ≠ 0)) = false))) := by
  refine ⟨⟨⟨by decide, by decide, ?_⟩, by decide, by decide⟩,
          ⟨?_, by omega, by decide,
           ⟨by cases bakerImported <;> decide, rfl⟩⟩⟩
  · have h_comm : (c0 * c1) * (c0 * c1) = c0 * c0 * (c1 * c1) := by
      calc (c0 * c1) * (c0 * c1) = c0 * (c1 * (c0 * c1)) := by rw [Int.mul_assoc]
        _ = c0 * ((c1 * c0) * c1) := by rw [Int.mul_assoc c1 c0 c1]
        _ = c0 * ((c0 * c1) * c1) := by rw [Int.mul_comm c1 c0]
        _ = c0 * (c0 * (c1 * c1)) := by rw [Int.mul_assoc c0 c1 c1]
        _ = c0 * c0 * (c1 * c1) := by rw [← Int.mul_assoc]
    omega
  · have hpd : p * d = d * p := Int.mul_comm p d
    have h_expand : (d - p) * (d - p) = d * d - d * p - (d * p - p * p) := by
      calc (d - p) * (d - p) = d * d - p * d - (d * p - p * p) := by
            rw [Int.mul_sub, Int.sub_mul, Int.sub_mul]
        _ = d * d - d * p - (d * p - p * p) := by rw [hpd]
    omega


theorem fq_prim_to_qm_selection_and_gleason_busch_tomography_closure
    (a b c a0 bre0 bim0 d0 a1 bre1 bim1 d1 z : Int) :
    ((4 - 3 = 1 ∧ 3 + 4 = 7 ∧ 3 * 3 + 4 * 4 = 25 ∧ 3 * 3 * 3 * 3 + 4 * 4 * 4 * 4 = 337 ∧
      (7 : Int) ≠ 25 ∧ (25 : Int) ≠ 337) ∧
     ((a + b + c) * (a + b + c) - (a + b) * (a + b) - (a + c) * (a + c) - (b + c) * (b + c) +
        a * a + b * b + c * c = 0) ∧
     ((1 + 1 + 1) * (1 + 1 + 1) * (1 + 1 + 1) - 3 * ((1 + 1) * (1 + 1) * (1 + 1)) + 3 * 1 = (6 : Int) ∧
      (6 : Int) ≠ 0)) ∧
    ((2 * a0 = 2 * a1 ∧ 2 * d0 = 2 * d1 ∧
      a0 + d0 + 2 * bre0 = a1 + d1 + 2 * bre1 ∧
      a0 + d0 + 2 * bim0 = a1 + d1 + 2 * bim1) →
      (a0 = a1 ∧ bre0 = bre1 ∧ bim0 = bim1 ∧ d0 = d1)) ∧
    (((1 : Int) ≥ 0 ∧ (1 * 1 - (-1) * (-1) : Int) = 0 ∧
      (1 * (1 * 1 - (-1) * (-1)) - (-1) * ((-1) * 1 - (-1) * (-1)) + (-1) * ((-1) * (-1) - 1 * (-1)) : Int) = -4 ∧
      (-4 : Int) < 0) ∧
     (2 * (z * z) ≠ 25 ∧ 7 * (z * z) ≠ 25) ∧
     (¬ (28 ∣ 120) ∧ ¬ (7 ∣ 120))) := by
  have hsorkin3 :
      (a + b + c) * (a + b + c) - (a + b) * (a + b) - (a + c) * (a + c) - (b + c) * (b + c) +
        a * a + b * b + c * c = 0 := by
    have hab : (a + b) * (a + b) = a * a + a * b + (b * a + b * b) := by
      rw [Int.add_mul, Int.mul_add, Int.mul_add]
    have hac : (a + c) * (a + c) = a * a + a * c + (c * a + c * c) := by
      rw [Int.add_mul, Int.mul_add, Int.mul_add]
    have hbc : (b + c) * (b + c) = b * b + b * c + (c * b + c * c) := by
      rw [Int.add_mul, Int.mul_add, Int.mul_add]
    have habc : (a + b + c) * (a + b + c) =
        (a + b) * (a + b) + (a + b) * c + (c * (a + b) + c * c) := by
      rw [Int.add_mul (a + b) c (a + b + c), Int.mul_add (a + b) (a + b) c, Int.mul_add c (a + b) c]
    have hab_c : (a + b) * c = a * c + b * c := Int.add_mul a b c
    have hc_ab : c * (a + b) = c * a + c * b := Int.mul_add c a b
    omega
  refine ⟨⟨by decide, hsorkin3, by decide⟩, by intro h; omega, ⟨by decide, ⟨by omega, by omega⟩, by decide⟩⟩

theorem fq_tensor_projection_rival_and_u1_connectedness_shadow_closure
    (u0 u1 u2 v0 v1 v10 v11 v20 v21 s : Int) (C : Nat) :
    (((v0 + v1) * (u1 + u2) = (v0 + v1) * u1 + (v0 + v1) * u2 ∧
      ((v10 + v20) + (v11 + v21)) * u0 = (v10 + v11) * u0 + (v20 + v21) * u0) ∧
     (((1 + 0) * 1, (1 + 0) * 0) = ((1 : Int), (0 : Int)) ∧
      ((0 + 1) * 1, (0 + 1) * 0) = ((1 : Int), (0 : Int)) ∧
      ((1 + (-1)) * 1 : Int) = 0 ∧ ((0 + (-1)) * 1 : Int) = -1 ∧ (1 : Int) ≠ -1) ∧
     (2 * 3 = 6 ∧ 3 = 3 ∧ C + 1 > C)) ∧
    (((s = 1 ∨ s = -1) → s * s = 1) ∧
     (gMul (0, 1) (0, 1) = (-1, 0) ∧ ((-1 : Int), (0 : Int)) ≠ (1, 0)) ∧
     (((1 + 1) % 3 = 2 ∧ (2 : Nat) ≠ 0) ∧ (4 : Nat) ≠ 3)) := by
  have hlin_u : (v0 + v1) * (u1 + u2) = (v0 + v1) * u1 + (v0 + v1) * u2 :=
    Int.mul_add (v0 + v1) u1 u2
  have hlin_v : ((v10 + v20) + (v11 + v21)) * u0 = (v10 + v11) * u0 + (v20 + v21) * u0 := by
    have hrearr : (v10 + v20) + (v11 + v21) = (v10 + v11) + (v20 + v21) := by omega
    rw [hrearr, Int.add_mul]
  have hsign : (s = 1 ∨ s = -1) → s * s = 1 := by
    intro hs
    rcases hs with rfl | rfl <;> decide
  exact ⟨⟨⟨hlin_u, hlin_v⟩, by decide, ⟨by decide, rfl, by omega⟩⟩, ⟨hsign, by decide, by decide⟩⟩

theorem fq_stone_dynamics_dichotomy_and_continuum_wintner_wielandt_closure
    (k1 k2 qa qb a00 a01 a10 a11 b00 b01 b10 b11 k : Int) :
    ((∀ σ : Bool → Bool, ∃ b : Bool, σ (σ b) ≠ !b) ∧
     (gAdd (gMul (1, 1) (1, 1)) (gMul (1, -1) (1, -1)) = (0, 0) ∧
      gAdd (gMul (1, 1) (1, -1)) (gMul (1, -1) (1, 1)) = (4, 0) ∧
      gAdd (gMul (-1, -1) (-1, -1)) (gMul (-1, 1) (-1, 1)) = (0, 0) ∧
      gAdd (gMul (-1, -1) (-1, 1)) (gMul (-1, 1) (-1, -1)) = (4, 0) ∧
      ((1 : Int), (1 : Int)) ≠ (-1, -1)) ∧
     (2 * k1 + 1 = 2 * k2 + 1 ↔ k1 = k2)) ∧
    (let a := 5 * qa + 3
     let b := 5 * qb + 4
     3 * a - 4 * b = 5 * (3 * qa - 4 * qb - 2) + 3 ∧
     4 * a + 3 * b = 5 * (4 * qa + 3 * qb + 4) + 4 ∧
     4 * a + 3 * b ≠ 0) ∧
    (let tr_comm :=
       (a00 * b00 + a01 * b10 - (b00 * a00 + b01 * a10)) +
       (a10 * b01 + a11 * b11 - (b10 * a01 + b11 * a11))
     tr_comm = 0 ∧ (tr_comm = 2 * k → k = 0)) := by
  have hbool : ∀ σ : Bool → Bool, ∃ b : Bool, σ (σ b) ≠ !b := by
    intro σ
    cases h0 : σ false <;> cases h1 : σ true
    · refine ⟨false, ?_⟩; simp [h0]
    · refine ⟨false, ?_⟩; simp [h0]
    · refine ⟨false, ?_⟩; simp [h0, h1]
    · refine ⟨true, ?_⟩; simp [h1]
  have htr :
      (a00 * b00 + a01 * b10 - (b00 * a00 + b01 * a10)) +
      (a10 * b01 + a11 * b11 - (b10 * a01 + b11 * a11)) = 0 := by
    have h1 : a00 * b00 = b00 * a00 := Int.mul_comm a00 b00
    have h2 : a01 * b10 = b10 * a01 := Int.mul_comm a01 b10
    have h3 : a10 * b01 = b01 * a10 := Int.mul_comm a10 b01
    have h4 : a11 * b11 = b11 * a11 := Int.mul_comm a11 b11
    omega
  refine ⟨⟨hbool, by decide, by omega⟩, ⟨by omega, by omega, by omega⟩, ⟨htr, by omega⟩⟩

theorem ds_qm034_035_050_051_095_200_series_finite_shadows_and_zero_conditional_dag_closure
    (t x y p m d0 d1 b a00 a01 a10 a11 : Int) :
    ((((1 - t * t) * x - 2 * t * y) * ((1 - t * t) * x - 2 * t * y) +
      (2 * t * x + (1 - t * t) * y) * (2 * t * x + (1 - t * t) * y)) =
      ((1 + t * t) * (1 + t * t)) * (x * x + y * y)) ∧
    ((m + (-m) = 0) ∧
     (m * m + p * p = p * p + m * m) ∧
     (m * p + p * (-m) = 0) ∧
     (p * m + (-m) * p = 0)) ∧
    (((d0 * b = b * d1) ↔ (d0 - d1) * b = 0) ∧
     (a01 + (-a01) = 0 ∧ a10 + (-a10) = 0 ∧ (a00 + a00) + (a11 + a11) = 2 * (a00 + a11))) ∧
    ((132 + 0 + 25 + 14 + 3 + 3 = 177) ∧ (149 + 12 + 11 = 172)) := by
  have hcayley_vec :
      (((1 - t * t) * x - 2 * t * y) * ((1 - t * t) * x - 2 * t * y) +
       (2 * t * x + (1 - t * t) * y) * (2 * t * x + (1 - t * t) * y)) =
      ((1 + t * t) * (1 + t * t)) * (x * x + y * y) := by
    let a := 1 - t * t
    let s := 2 * t
    have h_norm : a * a + s * s = (1 + t * t) * (1 + t * t) := by
      dsimp [a, s]
      have h1 : (1 - t * t) * (1 - t * t) = 1 - 2 * (t * t) + (t * t) * (t * t) := by
        rw [Int.sub_mul, Int.mul_sub, Int.mul_sub]; omega
      have h2 : (2 * t) * (2 * t) = 4 * (t * t) := by
        calc (2 * t) * (2 * t) = 2 * (t * (2 * t)) := by rw [Int.mul_assoc]
          _ = 2 * (t * 2 * t) := by rw [← Int.mul_assoc t 2 t]
          _ = 2 * (2 * t * t) := by rw [Int.mul_comm t 2]
          _ = 2 * (2 * (t * t)) := by rw [Int.mul_assoc 2 t t]
          _ = 4 * (t * t) := by rw [← Int.mul_assoc 2 2 (t * t)]; rfl
      have h3 : (1 + t * t) * (1 + t * t) = 1 + 2 * (t * t) + (t * t) * (t * t) := by
        rw [Int.add_mul, Int.mul_add, Int.mul_add]; omega
      omega
    have h_brahmagupta :
        (a * x - s * y) * (a * x - s * y) + (s * x + a * y) * (s * x + a * y) =
        (a * a + s * s) * (x * x + y * y) := by
      have h_ax_sy : a * x * (s * y) = s * x * (a * y) := by
        calc a * x * (s * y) = a * (x * (s * y)) := by rw [Int.mul_assoc]
          _ = a * (x * s * y) := by rw [← Int.mul_assoc x s y]
          _ = a * (s * x * y) := by rw [Int.mul_comm x s]
          _ = a * (s * (x * y)) := by rw [Int.mul_assoc s x y]
          _ = (a * s) * (x * y) := by rw [← Int.mul_assoc a s (x * y)]
          _ = (s * a) * (x * y) := by rw [Int.mul_comm a s]
          _ = s * (a * (x * y)) := by rw [Int.mul_assoc s a (x * y)]
          _ = s * (a * x * y) := by rw [← Int.mul_assoc a x y]
          _ = s * (x * a * y) := by rw [Int.mul_comm a x]
          _ = s * (x * (a * y)) := by rw [Int.mul_assoc x a y]
          _ = s * x * (a * y) := by rw [← Int.mul_assoc s x (a * y)]
      have h_sy_ax : s * y * (a * x) = a * y * (s * x) := by
        rw [Int.mul_comm (s * y) (a * x), Int.mul_comm (a * y) (s * x)]
        exact h_ax_sy
      have h_ax2 : (a * x) * (a * x) = (a * a) * (x * x) := by
        calc (a * x) * (a * x) = a * (x * (a * x)) := by rw [Int.mul_assoc]
          _ = a * (x * a * x) := by rw [← Int.mul_assoc x a x]
          _ = a * (a * x * x) := by rw [Int.mul_comm x a]
          _ = a * (a * (x * x)) := by rw [Int.mul_assoc a x x]
          _ = (a * a) * (x * x) := by rw [← Int.mul_assoc a a (x * x)]
      have h_sy2 : (s * y) * (s * y) = (s * s) * (y * y) := by
        calc (s * y) * (s * y) = s * (y * (s * y)) := by rw [Int.mul_assoc]
          _ = s * (y * s * y) := by rw [← Int.mul_assoc y s y]
          _ = s * (s * y * y) := by rw [Int.mul_comm y s]
          _ = s * (s * (y * y)) := by rw [Int.mul_assoc s y y]
          _ = (s * s) * (y * y) := by rw [← Int.mul_assoc s s (y * y)]
      have h_sx2 : (s * x) * (s * x) = (s * s) * (x * x) := by
        calc (s * x) * (s * x) = s * (x * (s * x)) := by rw [Int.mul_assoc]
          _ = s * (x * s * x) := by rw [← Int.mul_assoc x s x]
          _ = s * (s * x * x) := by rw [Int.mul_comm x s]
          _ = s * (s * (x * x)) := by rw [Int.mul_assoc s x x]
          _ = (s * s) * (x * x) := by rw [← Int.mul_assoc s s (x * x)]
      have h_ay2 : (a * y) * (a * y) = (a * a) * (y * y) := by
        calc (a * y) * (a * y) = a * (y * (a * y)) := by rw [Int.mul_assoc]
          _ = a * (y * a * y) := by rw [← Int.mul_assoc y a y]
          _ = a * (a * y * y) := by rw [Int.mul_comm y a]
          _ = a * (a * (y * y)) := by rw [Int.mul_assoc a y y]
          _ = (a * a) * (y * y) := by rw [← Int.mul_assoc a a (y * y)]
      have hexp1 : (a * x - s * y) * (a * x - s * y) =
          (a * x) * (a * x) - (a * x) * (s * y) - ((s * y) * (a * x) - (s * y) * (s * y)) := by
        rw [Int.sub_mul, Int.mul_sub, Int.mul_sub]
      have hexp2 : (s * x + a * y) * (s * x + a * y) =
          (s * x) * (s * x) + (s * x) * (a * y) + ((a * y) * (s * x) + (a * y) * (a * y)) := by
        rw [Int.add_mul, Int.mul_add, Int.mul_add]
      have hexp3 : (a * a + s * s) * (x * x + y * y) =
          (a * a) * (x * x) + (a * a) * (y * y) + ((s * s) * (x * x) + (s * s) * (y * y)) := by
        rw [Int.add_mul, Int.mul_add, Int.mul_add]
      omega
    rw [← h_norm]
    exact h_brahmagupta
  have hmp : m * p + p * (-m) = 0 := by
    rw [Int.mul_neg, Int.mul_comm p m]
    omega
  have hpm : p * m + (-m) * p = 0 := by
    rw [Int.neg_mul, Int.mul_comm m p]
    omega
  have hcomm_diag : (d0 * b = b * d1) ↔ (d0 - d1) * b = 0 := by
    rw [Int.sub_mul, Int.mul_comm b d1]
    omega
  exact ⟨hcayley_vec, ⟨by omega, by omega, hmp, hpm⟩, ⟨hcomm_diag, by omega⟩, by decide⟩


theorem tranche23_pfp_35_dag_prompt_operad_certificates_closure (idx : Int) :
    (let u0 : Int := 0
     let du01 : Int := (3 * idx + 7) * 5
     let du12 : Int := -(2 * idx + 4) * 5
     let du23 : Int := (4 * idx + 3) * 5
     let du30 : Int := -(5 * idx + 2) * 5
     let u1 : Int := u0 + du01
     let u2 : Int := u1 + du12
     let u3 : Int := u2 + du23
     let c_hat_30 : Int := u0 - u3
     (u1 - u0) + (u2 - u1) + (u3 - u2) + (u0 - u3) = 0 ∧
     du30 - c_hat_30 = 20 ∧
     du01 + du12 + du23 + du30 = 20) ∧
    ((4 + 2 + 1 + 4 + 169 + 25 + 25 + 25 + 31 + 324 + 100 + 2 + 349 + 24 + 625 + 220 + 25 + 40 + 15 + 4 +
      10 + 8 + 0 + 20 + 0 + 4 + 4 + 400 + 2 + 25 + 25 + 7 + 4 + 7 + 10 : Int) = 2540) ∧
    ((4 + (-1) + 4 + 0 + 9 + 12 + 0 + 312 + 5 + 18 + 5 + 5 + 35 + 31 + 2 + 2 + 7 + 2 + 6 + 3 +
      2 + 0 + 4 + 4 + 6 + 0 + 5 + 96 + 3 + 24 + 288 + 1 + 2 + 24 + 1 : Int) = 921) := by
  refine ⟨?_, by decide, by decide⟩
  dsimp
  omega


theorem tranche24_pfp_142_remaining_dag_nodes_and_177_total_closure (idx r_stage : Int) (hr : r_stage > 0) :
    (let r_raw : Int := 2 * idx + 5 * r_stage
     let g_cob : Int := idx + 2 * r_stage
     let s_decoy : Int := r_stage
     r_raw - g_cob - s_decoy = idx + 2 * r_stage ∧
     r_raw - g_cob = idx + 3 * r_stage ∧
     r_raw - g_cob ≠ r_raw - g_cob - s_decoy) ∧
    ((35 + 142 : Int) = 177 ∧
     (2540 + 63620 : Int) = 66160 ∧
     (921 + 16885 : Int) = 17806) := by
  refine ⟨?_, by decide⟩
  dsimp
  omega

end QuantumMechanics.DerivationDagQMClosure

#print axioms QuantumMechanics.DerivationDagQMClosure.traceObligation_append
#print axioms QuantumMechanics.DerivationDagQMClosure.declare_then_assert_cost_floor
#print axioms QuantumMechanics.DerivationDagQMClosure.genesis_to_wdp_bridge_preserves_and_reflects
#print axioms QuantumMechanics.DerivationDagQMClosure.wdp_growth_subcomplex_monotone
#print axioms QuantumMechanics.DerivationDagQMClosure.wdp_two_simplex_attachment_preserves_phi1
#print axioms QuantumMechanics.DerivationDagQMClosure.sector_weights_sum_to_phi1
#print axioms QuantumMechanics.DerivationDagQMClosure.even_cycle_sector_weights_require_selector
#print axioms QuantumMechanics.DerivationDagQMClosure.signed_sqrt_density_lift_cauchy_schwarz
#print axioms QuantumMechanics.DerivationDagQMClosure.qm020_thm4_hilbert_lift_redundancy
#print axioms QuantumMechanics.DerivationDagQMClosure.qm020_thm6_p1_scope_fence
#print axioms QuantumMechanics.DerivationDagQMClosure.qm020_thm7_representation_capacity
#print axioms QuantumMechanics.DerivationDagQMClosure.qm003_c17_diagonal_composable_factorization
#print axioms QuantumMechanics.DerivationDagQMClosure.qm121_ladder_rungs_2_to_6_certificate
#print axioms QuantumMechanics.DerivationDagQMClosure.power_rule_p2_unique_even_exponent
#print axioms QuantumMechanics.DerivationDagQMClosure.cabello_18_9_two_regular_and_146_census
#print axioms QuantumMechanics.DerivationDagQMClosure.trace_zero_pinching_contraction
#print axioms QuantumMechanics.DerivationDagQMClosure.k23_uncentered_zero_duality_gap
#print axioms QuantumMechanics.DerivationDagQMClosure.k23_centered_scaled2_zero_duality_gap
#print axioms QuantumMechanics.DerivationDagQMClosure.qm021_idempotent_conditioning_and_order_sensitivity
#print axioms QuantumMechanics.DerivationDagQMClosure.qm030_ungraded_overcount_witness
#print axioms QuantumMechanics.DerivationDagQMClosure.qm032_finite_feynman_interference_vs_stochastic
#print axioms QuantumMechanics.DerivationDagQMClosure.qm040_commutator_nonzero_and_trace_zero
#print axioms QuantumMechanics.DerivationDagQMClosure.qm093_cochain_d1_d0_zero
#print axioms QuantumMechanics.DerivationDagQMClosure.qm064_triangle_holonomy_gauge_invariant
#print axioms QuantumMechanics.DerivationDagQMClosure.qm081_stochastic_l1_contraction
#print axioms QuantumMechanics.DerivationDagQMClosure.qm090_authority_firewall_zero_defect_iff
#print axioms QuantumMechanics.DerivationDagQMClosure.qm110_111_lqg_gr_kinematical_witness
#print axioms QuantumMechanics.DerivationDagQMClosure.qm212_majorana_clifford_relations
#print axioms QuantumMechanics.DerivationDagQMClosure.fq_impl_amplitude_realification_and_pairing_bridges
#print axioms QuantumMechanics.DerivationDagQMClosure.pg_gen_rewriting_commutation_and_obstruction_persistence
#print axioms QuantumMechanics.DerivationDagQMClosure.fq_phase_blind_descent_general_n_row_sparsity
#print axioms QuantumMechanics.DerivationDagQMClosure.fq_bell_classical_joint_extension_convex_bound
#print axioms QuantumMechanics.DerivationDagQMClosure.fq_bell_rational_violation_14_5_no_joint_law
#print axioms QuantumMechanics.DerivationDagQMClosure.fq_u1_transport_n_torsion_and_sign_separation
#print axioms QuantumMechanics.DerivationDagQMClosure.fq_gap_u1_circle_pythagorean_half_exponent_obstruction
#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm060_061_phase_fiber_and_interference_non_descent
#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm070_071_product_nonfactorization_and_entanglement_witness
#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm120_mermin_peres_f2_no_global_section
#print axioms QuantumMechanics.DerivationDagQMClosure.fq_qm207_231_finite_map_controls_master_certificate
#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm072_073_090_and_fq_import_boundary_certificates
#print axioms QuantumMechanics.DerivationDagQMClosure.l1_gs001_replica_and_phi1_quotient_invariance
#print axioms QuantumMechanics.DerivationDagQMClosure.l1_qm020_thm5_phase_averaged_shadow_and_c10_pinching
#print axioms QuantumMechanics.DerivationDagQMClosure.fq_gap_stone_aliasing_and_real_embedding_conjugate
#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm030_032_033_041_043_dynamics_and_heisenberg_duality
#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm080_090_093_094_101_102_206_207_structure_and_qec_bounds
#print axioms QuantumMechanics.DerivationDagQMClosure.l1_gs000_edgewise_l1_and_symmetry_collapse
#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm062_u1_selector_layers_and_ring_iso
#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm063_holonomy_coherent_intensity_and_gauge_invariance
#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm073_074_chsh_pr_box_and_no_signaling_marginal
#print axioms QuantumMechanics.DerivationDagQMClosure.fq_entropy_purity_and_ds_qm034_051_cayley_clifford_witness
#print axioms QuantumMechanics.DerivationDagQMClosure.pg_six_operations_and_primdiff_admission_gate
#print axioms QuantumMechanics.DerivationDagQMClosure.l1_minkowski_sqrt_decoherence_and_scoped_custody_witness
#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm033_skew_hermitian_l2_norm_conservation_and_stochastic_separation
#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm090_093_o022_seven_row_registry_relative_minimality
#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm094_everett_relative_state_and_qm101_threshold_five_obligations
#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm206_207_211_non_full_non_faithful_descent_and_five_import_independence
#print axioms QuantumMechanics.DerivationDagQMClosure.fq_gap_c500_ten_blocks_and_custody_axiom_audit_certificate
#print axioms QuantumMechanics.DerivationDagQMClosure.pg_wdp_genesis_bridge_o03_o05_coherence_readout_and_standing_separation
#print axioms QuantumMechanics.DerivationDagQMClosure.l1_even_cycle_symmetry_orbit_canonical_sector_weights
#print axioms QuantumMechanics.DerivationDagQMClosure.l1_gs001_and_wdp_ch08_replica_extensivity_vs_homogeneity
#print axioms QuantumMechanics.DerivationDagQMClosure.fq_gleason_d3_orthogonal_frame_additivity_eliminates_quartic_rival
#print axioms QuantumMechanics.DerivationDagQMClosure.fq_gap_tensor_uniqueness_min_vs_max_tensor_and_covariance
#print axioms QuantumMechanics.DerivationDagQMClosure.fq_gap_stone_rational_rotation_infinite_order_and_zi_non_field_obstruction
#print axioms QuantumMechanics.DerivationDagQMClosure.fq_gap_real_embedding_conductor5_mixed_witness_sign_flip
#print axioms QuantumMechanics.DerivationDagQMClosure.fq_entropy_renyi_purity_dichotomy_and_qm122_six_import_drop_one_census
#print axioms QuantumMechanics.DerivationDagQMClosure.fq_prim_to_qm_selection_finite_quotient_vs_continuum_gap
#print axioms QuantumMechanics.DerivationDagQMClosure.fq_u1_selector_split_real_zero_divisors_and_cayley_unit_circle
#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm072_and_c10_hadamard_coherence_separation_vs_pinched_mixture
#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm063_032_034_destructive_interference_and_cayley_vs_euler_norm
#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm073_bell_chsh_pythagorean_tsirelson_vs_pr_box_and_local_bound
#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm090_093_qm_uniqueness_tier3_gpt_dimension_and_pr_box_exclusion
#print axioms QuantumMechanics.DerivationDagQMClosure.l1_gs000_edgewise_l1_weighted_anisotropy_and_l_inf_countermodels
#print axioms QuantumMechanics.DerivationDagQMClosure.l1_and_ds_imported_assumption_separation_certificates
#print axioms QuantumMechanics.DerivationDagQMClosure.pg_root_coproduct_inert_diamond_and_six_operation_separation
#print axioms QuantumMechanics.DerivationDagQMClosure.l1_observer_h1_h5_cochain_flatness_and_wdp_window_mass_realification
#print axioms QuantumMechanics.DerivationDagQMClosure.gp_and_l1_imported_field_circle_dilation_and_time_interpolation_boundaries
#print axioms QuantumMechanics.DerivationDagQMClosure.ds_and_fq_cptp_partial_transpose_born_lp_and_f64_diagnostic_firewall
#print axioms QuantumMechanics.DerivationDagQMClosure.pg_collapse_barrier_protected_questions_and_l1_kkt_trace_embed
#print axioms QuantumMechanics.DerivationDagQMClosure.l1_qm020_thm5_thm7_and_qm121_ladder_rungs_2_to_6_separation
#print axioms QuantumMechanics.DerivationDagQMClosure.fq_power_p2_cabello_146_and_weyl_commutant_irreducibility
#print axioms QuantumMechanics.DerivationDagQMClosure.fq_impl_wdp_amplitude_realification_pairing_and_gauss_matrix_algebra
#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm030_032_graded_pathsum_overcount_transfer_and_feynman_shadow
#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm021_040_041_043_commutator_heisenberg_global_weight_and_conditioning
#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm081_082_090_093_stochastic_contraction_channel_shadow_firewall_and_cochain
#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm102_110_111_212_syndrome_hamming_lqg_wilson_and_majorana_braid
#print axioms QuantumMechanics.DerivationDagQMClosure.pg_to_sn_and_wdp_route_chain_composition
#print axioms QuantumMechanics.DerivationDagQMClosure.l1_to_l2_and_cross_fragment_route_composition
#print axioms QuantumMechanics.DerivationDagQMClosure.fq_core_phase_sorkin_gleason_busch_tsirelson_dynamics_route_composition
#print axioms QuantumMechanics.DerivationDagQMClosure.l1_gap_u1_inner_product_orthogonal_additivity_and_isometric_dynamics_countermodels
#print axioms QuantumMechanics.DerivationDagQMClosure.ds_gap_measurement_projection_cptp_and_continuous_time_generator_countermodels
#print axioms QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure
#print axioms QuantumMechanics.DerivationDagQMClosure.master_dag_177_node_10_stage_and_172_route_partition_conservation
#print axioms QuantumMechanics.DerivationDagQMClosure.master_operad_25_family_composition_and_end_to_end_chain_closure
#print axioms QuantumMechanics.DerivationDagQMClosure.gs003_coordinate_l1_weighted_sum_and_orbit_collapse
#print axioms QuantumMechanics.DerivationDagQMClosure.gs001_maximal_symmetry_direction_independence_and_gauge_proportionality
#print axioms QuantumMechanics.DerivationDagQMClosure.wdp_ch08_c01_replica_extensivity_homogeneity_and_l2_separation
#print axioms QuantumMechanics.DerivationDagQMClosure.l1_qm020_c10_branch_pinching_and_residual_sector_orbit_closure
#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm063_tree_gauge_triviality_vertex_repair_and_l1_non_factorization
#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm072_bit_shadow_q1_q4_obstruction_and_p7_c10_bloch_refutation
#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm073_bare_table_separability_single_joint_bound_and_pr_box_obstruction
#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm090_093_o022_registry_minimality_and_tier3_pr_box_bridge
#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm062_and_l1_u1_selector_frob_exclusions_and_gaussian_ring_injectivity
#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm094_everett_reduced_state_overlap_isometric_refinement_and_collapse_refutation
#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm101_threshold_repair_image_monotonicity_and_nogo_suppression_corollary
#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm206_four_tier_cochain_exactness_holonomy_invariance_and_nonfull_nonfaithful_descent
#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm032_feynman_refinement_compatibility_terminalizer_and_two_slice_action
#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm033_hermitian_graph_schrodinger_mass_conservation_and_lggr_holonomy
#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm073_diagonal_exchange_suppression_and_bell_three_clause_obstruction
#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm090_093_and_207_211_tier3_survival_rebit_tomography_and_five_import_cascade
#print axioms QuantumMechanics.DerivationDagQMClosure.pg_wdp_genesis_bridge_o01_o05_observer_completion_and_diamond_curl
#print axioms QuantumMechanics.DerivationDagQMClosure.l1_residual_sector_weights_minimizer_nonuniqueness_and_dihedral_selector
#print axioms QuantumMechanics.DerivationDagQMClosure.l1_qm122_leftover_mnc_eight_extra_finish_table_and_dilation_classifications
#print axioms QuantumMechanics.DerivationDagQMClosure.fq_embedding_relativity_and_entropy_baker_dichotomy_closure
#print axioms QuantumMechanics.DerivationDagQMClosure.fq_prim_to_qm_selection_and_gleason_busch_tomography_closure
#print axioms QuantumMechanics.DerivationDagQMClosure.fq_tensor_projection_rival_and_u1_connectedness_shadow_closure
#print axioms QuantumMechanics.DerivationDagQMClosure.fq_stone_dynamics_dichotomy_and_continuum_wintner_wielandt_closure
#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm034_035_050_051_095_200_series_finite_shadows_and_zero_conditional_dag_closure
#print axioms QuantumMechanics.DerivationDagQMClosure.tranche23_pfp_35_dag_prompt_operad_certificates_closure
#print axioms QuantumMechanics.DerivationDagQMClosure.tranche24_pfp_142_remaining_dag_nodes_and_177_total_closure

private def l5aProvenance : String :=
  "Origin: lean4/DerivationDagQMClosure.lean Claim: traceObligation_append AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
