/-!
# Campaign TFQ-0003: one 3-cycle obstruction signature

Finite carrier: integer 1-cochains `(z0, z1, z2)` on the oriented 3-cycle.
Comparison: the three integer entries.
Coboundary: `(d0 h) = (h1 - h0, h2 - h1, h0 - h2)`.
Quotient: cochains modulo the image of `d0`, decided by the holonomy `z0 + z1 + z2`.
`Phi1` is the absolute value of that holonomy. It is the minimum of the unweighted L1 norm
on the cohomology class, attained by the classical residual `(hol, 0, 0)` and also by
`(0, hol, 0)`. `Gamma2` in this module means the holonomy, not a sum of squares.

This is one unweighted 3-cycle. It does not identify a Python or Rust witness, and it does
not complete a pass from Genesis into the obstruction calculus.

AuthorityEffect: None
-/

namespace CampaignTfq0003FiniteObstruction

/-- Integer 1-cochain on the three oriented edges of the 3-cycle. -/
structure Z3Cochain where
  z0 : Int
  z1 : Int
  z2 : Int
deriving DecidableEq, Repr

/-- Coboundary of a vertex cochain, edges `0→1`, `1→2`, `2→0`. -/
def d0 (h : Z3Cochain) : Z3Cochain where
  z0 := h.z1 - h.z0
  z1 := h.z2 - h.z1
  z2 := h.z0 - h.z2

/-- Holonomy, the class invariant. -/
def hol (c : Z3Cochain) : Int :=
  c.z0 + c.z1 + c.z2

/-- Unweighted L1 norm. -/
def l1 (c : Z3Cochain) : Nat :=
  c.z0.natAbs + c.z1.natAbs + c.z2.natAbs

/-- Entrywise difference. -/
def subCo (c d : Z3Cochain) : Z3Cochain where
  z0 := c.z0 - d.z0
  z1 := c.z1 - d.z1
  z2 := c.z2 - d.z2

/-- Gauge action `c - d0 h`. -/
def gauge (c h : Z3Cochain) : Z3Cochain :=
  subCo c (d0 h)

/-- `Gamma2` in this finite case is the holonomy. -/
def gamma2 (c : Z3Cochain) : Int :=
  hol c

/-- `Phi1` is the absolute value of the holonomy. -/
def phi1 (c : Z3Cochain) : Nat :=
  (hol c).natAbs

/-- Classical residual: the whole holonomy on the first edge. -/
def residualEdge0 (s : Int) : Z3Cochain where
  z0 := s
  z1 := 0
  z2 := 0

/-- Second L1 minimizer: the whole holonomy on the second edge. -/
def residualEdge1 (s : Int) : Z3Cochain where
  z0 := 0
  z1 := s
  z2 := 0

/-- Explicit primitive of a holonomy-zero cochain: `h = (0, c0, c0 + c1)`. -/
def preimageOfHolZero (c : Z3Cochain) : Z3Cochain where
  z0 := 0
  z1 := c.z0
  z2 := c.z0 + c.z1

/-- Two 1-cochains lie in the same `d0` coset. -/
def SameClass (c r : Z3Cochain) : Prop :=
  ∃ h : Z3Cochain, r = gauge c h

/-- `c` is a coboundary. -/
def IsCoboundary (c : Z3Cochain) : Prop :=
  ∃ h : Z3Cochain, c = d0 h

theorem cochain_ext {c r : Z3Cochain} (h0 : c.z0 = r.z0) (h1 : c.z1 = r.z1) (h2 : c.z2 = r.z2) :
    c = r := by
  cases c
  cases r
  subst h0
  subst h1
  subst h2
  rfl

theorem hol_d0 (h : Z3Cochain) : hol (d0 h) = 0 := by
  simp only [hol, d0]
  omega

theorem hol_gauge (c h : Z3Cochain) : hol (gauge c h) = hol c := by
  simp only [hol, gauge, subCo, d0]
  omega

theorem gamma2_gauge (c h : Z3Cochain) : gamma2 (gauge c h) = gamma2 c := by
  unfold gamma2
  exact hol_gauge c h

theorem d0_preimage_of_hol_zero (c : Z3Cochain) (hzero : hol c = 0) :
    d0 (preimageOfHolZero c) = c := by
  apply cochain_ext
  · simp only [d0, preimageOfHolZero]
    omega
  · simp only [d0, preimageOfHolZero]
    omega
  · simp only [d0, preimageOfHolZero, hol] at hzero ⊢
    omega

theorem coboundary_iff_hol_zero (c : Z3Cochain) : IsCoboundary c ↔ hol c = 0 := by
  constructor
  · intro hb
    cases hb with
    | intro h heq =>
      subst heq
      exact hol_d0 h
  · intro hz
    exact ⟨preimageOfHolZero c, (d0_preimage_of_hol_zero c hz).symm⟩

theorem hol_subCo (c r : Z3Cochain) : hol (subCo c r) = hol c - hol r := by
  simp only [hol, subCo]
  omega

theorem gauge_cancels_diff (c r : Z3Cochain)
    (hd : d0 (preimageOfHolZero (subCo c r)) = subCo c r) :
    gauge c (preimageOfHolZero (subCo c r)) = r := by
  have hd0 := congrArg Z3Cochain.z0 hd
  have hd1 := congrArg Z3Cochain.z1 hd
  have hd2 := congrArg Z3Cochain.z2 hd
  apply cochain_ext
  · simp only [gauge, subCo] at hd0 ⊢
    omega
  · simp only [gauge, subCo] at hd1 ⊢
    omega
  · simp only [gauge, subCo] at hd2 ⊢
    omega

theorem sameClass_of_equal_hol (c r : Z3Cochain) (h : hol r = hol c) : SameClass c r := by
  have hdiff : hol (subCo c r) = 0 := by
    rw [hol_subCo]
    omega
  exact ⟨preimageOfHolZero (subCo c r),
    (gauge_cancels_diff c r (d0_preimage_of_hol_zero (subCo c r) hdiff)).symm⟩

theorem sameClass_iff_hol (c r : Z3Cochain) : SameClass c r ↔ hol r = hol c := by
  constructor
  · intro hs
    cases hs with
    | intro h heq =>
      subst heq
      exact hol_gauge c h
  · exact sameClass_of_equal_hol c r

theorem natAbs_hol_le_l1 (c : Z3Cochain) : (hol c).natAbs ≤ l1 c := by
  unfold hol l1
  have h1 := Int.natAbs_add_le c.z0 c.z1
  have h2 := Int.natAbs_add_le (c.z0 + c.z1) c.z2
  omega

theorem phi1_lower_bound (c r : Z3Cochain) (hs : SameClass c r) : phi1 c ≤ l1 r := by
  have hr := (sameClass_iff_hol c r).mp hs
  simp only [phi1]
  rw [← hr]
  exact natAbs_hol_le_l1 r

theorem hol_edge0 (s : Int) : hol (residualEdge0 s) = s := by
  simp only [hol, residualEdge0]
  omega

theorem l1_edge0 (s : Int) : l1 (residualEdge0 s) = s.natAbs := by
  simp only [l1, residualEdge0, Int.natAbs_zero]
  omega

theorem hol_edge1 (s : Int) : hol (residualEdge1 s) = s := by
  simp only [hol, residualEdge1]
  omega

theorem l1_edge1 (s : Int) : l1 (residualEdge1 s) = s.natAbs := by
  simp only [l1, residualEdge1, Int.natAbs_zero]
  omega

theorem phi1_attained_edge0 (c : Z3Cochain) :
    SameClass c (residualEdge0 (hol c)) ∧ l1 (residualEdge0 (hol c)) = phi1 c := by
  refine ⟨sameClass_of_equal_hol c (residualEdge0 (hol c)) (hol_edge0 (hol c)), ?_⟩
  simp only [phi1]
  rw [l1_edge0]

theorem phi1_attained_edge1 (c : Z3Cochain) :
    SameClass c (residualEdge1 (hol c)) ∧ l1 (residualEdge1 (hol c)) = phi1 c := by
  refine ⟨sameClass_of_equal_hol c (residualEdge1 (hol c)) (hol_edge1 (hol c)), ?_⟩
  simp only [phi1]
  rw [l1_edge1]

theorem minimizers_differ (c : Z3Cochain) (hne : hol c ≠ 0) :
    residualEdge0 (hol c) ≠ residualEdge1 (hol c) := by
  intro heq
  have hz0 := congrArg Z3Cochain.z0 heq
  unfold residualEdge0 residualEdge1 at hz0
  exact hne hz0

/-- The concrete cochain named in the node statement. -/
def sample : Z3Cochain where
  z0 := 1
  z1 := -2
  z2 := 4

theorem sample_signature :
    hol sample = 3 ∧ phi1 sample = 3 ∧ l1 sample = 7 ∧ phi1 sample < l1 sample := by
  decide

theorem sample_not_classical_residual : sample ≠ residualEdge0 (hol sample) := by
  intro heq
  have hz1 := congrArg Z3Cochain.z1 heq
  simp only [sample, residualEdge0, hol] at hz1
  omega

end CampaignTfq0003FiniteObstruction

#print axioms CampaignTfq0003FiniteObstruction.hol_d0
#print axioms CampaignTfq0003FiniteObstruction.hol_gauge
#print axioms CampaignTfq0003FiniteObstruction.gamma2_gauge
#print axioms CampaignTfq0003FiniteObstruction.d0_preimage_of_hol_zero
#print axioms CampaignTfq0003FiniteObstruction.coboundary_iff_hol_zero
#print axioms CampaignTfq0003FiniteObstruction.sameClass_iff_hol
#print axioms CampaignTfq0003FiniteObstruction.natAbs_hol_le_l1
#print axioms CampaignTfq0003FiniteObstruction.phi1_lower_bound
#print axioms CampaignTfq0003FiniteObstruction.phi1_attained_edge0
#print axioms CampaignTfq0003FiniteObstruction.phi1_attained_edge1
#print axioms CampaignTfq0003FiniteObstruction.minimizers_differ
#print axioms CampaignTfq0003FiniteObstruction.sample_signature
#print axioms CampaignTfq0003FiniteObstruction.sample_not_classical_residual
