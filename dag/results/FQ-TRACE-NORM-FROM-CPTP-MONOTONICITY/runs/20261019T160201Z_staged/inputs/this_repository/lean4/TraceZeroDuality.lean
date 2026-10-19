



namespace TraceZeroDuality


def iabs (x : Int) : Int :=
  if x < 0 then -x else x

def max2 (a b : Int) : Int :=
  if a < b then b else a

def min2 (a b : Int) : Int :=
  if a < b then a else b

structure Eig2 where
  l1 : Int
  l2 : Int

def spread (L : Eig2) : Int :=
  max2 L.l1 L.l2 - min2 L.l1 L.l2

theorem spread_nonneg (L : Eig2) : 0 ≤ spread L := by
  unfold spread max2 min2
  split <;> omega

structure TraceZeroVec2 where
  x1 : Int
  x2 : Int
  trace_zero : x1 + x2 = 0
  norm_bound : iabs x1 + iabs x2 ≤ 2

theorem trace_zero_vec2_coords (x : TraceZeroVec2) :
    (x.x1 = -1 ∧ x.x2 = 1) ∨ (x.x1 = 0 ∧ x.x2 = 0) ∨ (x.x1 = 1 ∧ x.x2 = -1) := by
  have htz := x.trace_zero
  have hnb := x.norm_bound
  unfold iabs at hnb
  split at hnb <;> split at hnb <;> omega

def pairing (L : Eig2) (x : TraceZeroVec2) : Int :=
  L.l1 * x.x1 + L.l2 * x.x2

theorem pairing_le_spread (L : Eig2) (x : TraceZeroVec2) :
    pairing L x ≤ spread L := by
  have hc := trace_zero_vec2_coords x
  unfold pairing spread max2 min2
  rcases hc with ⟨hx1, hx2⟩ | ⟨hx1, hx2⟩ | ⟨hx1, hx2⟩
  · rw [hx1, hx2]
    split <;> omega
  · rw [hx1, hx2]
    split <;> omega
  · rw [hx1, hx2]
    split <;> omega

def optimalVec2 (L : Eig2) : TraceZeroVec2 :=
  if L.l1 < L.l2 then
    ⟨-1, 1, by omega, by unfold iabs; decide⟩
  else
    ⟨1, -1, by omega, by unfold iabs; decide⟩

theorem optimal_pairing_eq_spread (L : Eig2) :
    pairing L (optimalVec2 L) = spread L := by
  unfold pairing optimalVec2 spread max2 min2
  split <;> dsimp <;> omega

def opNorm (L : Eig2) (c : Int) : Int :=
  max2 (iabs (2 * L.l1 - c)) (iabs (2 * L.l2 - c))

def optimalShift (L : Eig2) : Int :=
  L.l1 + L.l2

theorem optimal_shift_achieves_spread (L : Eig2) :
    opNorm L (optimalShift L) = spread L := by
  unfold opNorm optimalShift spread max2 min2 iabs
  split <;> split <;> split <;> omega

theorem opNorm_ge_spread (L : Eig2) (c : Int) :
    spread L ≤ opNorm L c := by
  unfold opNorm spread max2 min2 iabs
  split <;> split <;> split <;> omega

theorem trace_zero_duality_gap_zero (L : Eig2) :
    pairing L (optimalVec2 L) = opNorm L (optimalShift L) := by
  rw [optimal_pairing_eq_spread, optimal_shift_achieves_spread]



def IsContractive {V : Type} (dist : V → V → Int) (T : V → V) : Prop :=
  ∀ x y, dist (T x) (T y) ≤ dist x y

theorem scaleMetric_monotone {V : Type} (c : Int) (hc : 0 ≤ c)
    (dist : V → V → Int) (T : V → V) (hT : IsContractive dist T) :
    IsContractive (fun x y => c * dist x y) T := by
  intro x y
  exact Int.mul_le_mul_of_nonneg_left (hT x y) hc

theorem monotone_metric_distinct {V : Type} (dist : V → V → Int) (x y : V)
    (hxy : 0 < dist x y) (c1 c2 : Int) (_hc1 : 0 ≤ c1) (_hc2 : 0 ≤ c2) (h_c_diff : c1 ≠ c2) :
    c1 * dist x y ≠ c2 * dist x y := by
  intro h
  have hdist : dist x y ≠ 0 := by omega
  have h_sub : c1 * dist x y - c2 * dist x y = 0 := by omega
  have h_distrib : (c1 - c2) * dist x y = c1 * dist x y - c2 * dist x y := by
    rw [Int.sub_mul]
  rw [← h_distrib] at h_sub
  cases Int.mul_eq_zero.mp h_sub with
  | inl h1 =>
    have : c1 = c2 := by omega
    exact h_c_diff this
  | inr h2 =>
    exact hdist h2



structure CochainComplex (C0 C1 : Type) where
  add0 : C0 → C0 → C0
  add1 : C1 → C1 → C1
  neg0 : C0 → C0
  neg1 : C1 → C1
  zero0 : C0
  zero1 : C1
  d0 : C0 → C1
  d0_add : ∀ a b, d0 (add0 a b) = add1 (d0 a) (d0 b)
  d0_zero : d0 zero0 = zero1
  d0_neg : ∀ a, d0 (neg0 a) = neg1 (d0 a)
  add1_comm : ∀ x y, add1 x y = add1 y x
  add1_assoc : ∀ x y z, add1 (add1 x y) z = add1 x (add1 y z)
  zero1_add : ∀ x, add1 zero1 x = x
  add1_neg : ∀ x, add1 x (neg1 x) = zero1

def CoboundaryEquiv {C0 C1 : Type} (K : CochainComplex C0 C1) (w1 w2 : C1) : Prop :=
  ∃ a : C0, w1 = K.add1 w2 (K.d0 a)

theorem coboundary_equiv_refl {C0 C1 : Type} (K : CochainComplex C0 C1) (w : C1) :
    CoboundaryEquiv K w w := by
  refine ⟨K.zero0, ?_⟩
  rw [K.d0_zero, K.add1_comm, K.zero1_add]

theorem coboundary_equiv_symm {C0 C1 : Type} (K : CochainComplex C0 C1) (w1 w2 : C1)
    (h : CoboundaryEquiv K w1 w2) : CoboundaryEquiv K w2 w1 := by
  rcases h with ⟨a, rfl⟩
  refine ⟨K.neg0 a, ?_⟩
  rw [K.d0_neg, K.add1_assoc, K.add1_neg, K.add1_comm, K.zero1_add]

theorem coboundary_equiv_trans {C0 C1 : Type} (K : CochainComplex C0 C1) (w1 w2 w3 : C1)
    (h12 : CoboundaryEquiv K w1 w2) (h23 : CoboundaryEquiv K w2 w3) :
    CoboundaryEquiv K w1 w3 := by
  rcases h12 with ⟨a, rfl⟩
  rcases h23 with ⟨b, rfl⟩
  refine ⟨K.add0 b a, ?_⟩
  rw [K.d0_add, K.add1_assoc]

theorem coboundary_shift_equiv {C0 C1 : Type} (K : CochainComplex C0 C1) (delta : C1) (alpha : C0) :
    CoboundaryEquiv K (K.add1 delta (K.d0 alpha)) delta := by
  exact ⟨alpha, rfl⟩

theorem quotient_evaluation_invariant {C0 C1 : Type} (K : CochainComplex C0 C1)
    (phi : C1 → Int) (hphi : ∀ w1 w2, CoboundaryEquiv K w1 w2 → phi w1 = phi w2)
    (delta : C1) (alpha : C0) :
    phi (K.add1 delta (K.d0 alpha)) = phi delta := by
  apply hphi
  exact coboundary_shift_equiv K delta alpha

end TraceZeroDuality

private def l5aProvenance : String :=
  "Origin: lean4/TraceZeroDuality.lean Claim: spread_nonneg AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
