import FiniteWignerSimilarity

/-!
Conditional operational routes and countermodels for transition-probability preservation.
AuthorityEffect: None. The Gaussian-rational carrier and Born readout are supplied.
No hypothesis below is TpPreserving. Finite calibration requires a separately supplied
linear lift; the nonlinear two-sector countermodel explains why that requirement matters.
-/
namespace CampaignTransitionProbability

open Matrix BornFable BornFable.HermitianCarrier BornFable.HermitianPsd
  WignerFable.Kernel WignerFable.Theorem

abbrev Vec (n : ℕ) := Fin n → GaussRat
variable {n : ℕ}

/-- Static Born rule, with no constraint on dynamics. -/
def BornRule (readout : Vec n → Vec n → ℚ) : Prop :=
  ∀ x y, readout x y = hf (P x) y / vnorm y

theorem born_rule : BornRule (tp (n := n)) := tp_eq_born

def Nonvanishing (T : Vec n → Vec n) : Prop := ∀ x, x ≠ 0 → T x ≠ 0
def Reversible (T : Vec n → Vec n) : Prop := Function.Bijective T
def Orthogonality (T : Vec n → Vec n) : Prop :=
  ∀ x y, ip (T x) (T y) = 0 ↔ ip x y = 0
def BasisStatistics (T : Vec n → Vec n) : Prop :=
  ∀ x i, tp (e i) (T x) = tp (e i) x
def NormPreserving (T : Vec n → Vec n) : Prop := ∀ x, vnorm (T x) = vnorm x
/-- Superposition compatibility is an extra structural assumption. -/
def LinearLift (T : Vec n → Vec n) : Prop :=
  ∃ F : Matrix (Fin n) (Fin n) GaussRat, ∀ x, T x = F *ᵥ x
/-- Only a finite family of zero-probability tests; no general probability equalities. -/
structure OrthogonalCalibration (T : Vec n → Vec n) : Prop where
  basis : ∀ i j, i ≠ j → ip (T (e i)) (T (e j)) = 0
  balanced : ∀ i j, i ≠ j → ip (T (e i + e j)) (T (e i - e j)) = 0

def NonzeroAnchor (T : Vec n → Vec n) (i : Fin n) : Prop := T (e i) ≠ 0

theorem ip_sub_left (x y z : Vec n) : ip (x - y) z = ip x z - ip y z := by
  simp [ip, star_sub, sub_dotProduct]

theorem ip_sub_right (x y z : Vec n) : ip x (y - z) = ip x y - ip x z := by
  simp [ip, dotProduct_sub]

theorem calibration_norms {F : Matrix (Fin n) (Fin n) GaussRat}
    (h : OrthogonalCalibration (fun x => F *ᵥ x)) (i j : Fin n) :
    vnorm (F *ᵥ e i) = vnorm (F *ᵥ e j) := by
  by_cases hij : i = j
  · rw [hij]
  · have hp := h.balanced i j hij
    rw [mulVec_add, mulVec_sub, ip_sub_right, ip_add_left, ip_add_left,
      h.basis i j hij, h.basis j i (Ne.symm hij), add_zero, zero_add] at hp
    have hr := congrArg GaussRat.re hp
    simp only [GaussRat.re_sub, GaussRat.re_zero, ip_self_re] at hr
    linarith

/-- A finite orthogonality calibration fixes the Gram matrix of a supplied linear lift. -/
theorem calibration_similarity {F : Matrix (Fin n) (Fin n) GaussRat}
    (h : OrthogonalCalibration (fun x => F *ᵥ x)) (i₀ : Fin n) :
    Similarity F (vnorm (F *ᵥ e i₀)) := by
  have hc : colMatrix (fun i => F *ᵥ e i) = F := by
    apply Matrix.ext
    intro r i
    change (F *ᵥ e i) r = F r i
    simp [e]
  have hs := similarity_colMatrix h.basis (fun i => calibration_norms h i i₀)
  rwa [hc] at hs

/-- Sufficient route, with every additional premise visible. -/
theorem linear_calibration_tpPreserving {T : Vec n → Vec n} (i₀ : Fin n)
    (hl : LinearLift T) (hc : OrthogonalCalibration T) (ha : NonzeroAnchor T i₀) :
    TpPreserving T := by
  obtain ⟨F, hF⟩ := hl
  have he : T = fun x => F *ᵥ x := funext hF
  subst T
  have hs := calibration_similarity hc i₀
  have hd : vnorm (F *ᵥ e i₀) ≠ 0 := vnorm_ne_zero ha
  exact ⟨fun _ hx => hs.mulVec_ne_zero hd hx, fun x y _ _ => hs.tp_mulVec hd x y⟩

theorem orthogonality_calibration {T : Vec n → Vec n} (h : Orthogonality T) :
    OrthogonalCalibration T where
  basis i j hij := (h _ _).mpr (ip_e_e_of_ne hij)
  balanced i j hij := (h _ _).mpr (by
    rw [ip_add_left, ip_sub_right, ip_sub_right, ip_e_e_of_ne hij,
      ip_e_e_of_ne hij.symm, ip_self_eq, ip_self_eq, vnorm_e, vnorm_e]
    simp)

/-- The linear route composes with the existing exact Wigner theorem. -/
theorem linear_calibration_wigner {T : Vec n → Vec n} (i₀ : Fin n)
    (hl : LinearLift T) (hc : OrthogonalCalibration T) (ha : NonzeroAnchor T i₀) :
    ∃ (F : Matrix (Fin n) (Fin n) GaussRat) (d ε : ℚ), 0 < d ∧
      Similarity F d ∧ (ε = 1 ∨ ε = -1) ∧
      ∀ x, x ≠ 0 → ∃ μ : GaussRat, μ ≠ 0 ∧ T x = μ • (F *ᵥ twist ε x) :=
  finite_wigner i₀ (linear_calibration_tpPreserving i₀ hl hc ha)

/-! A global nonlinear countermodel on Q(i)^2. -/

def Balanced (x : Vec 2) : Prop := GaussRat.normSq (x 0) = GaussRat.normSq (x 1)
instance (x : Vec 2) : Decidable (Balanced x) := inferInstanceAs (Decidable (_ = _))

def conditionalConjugation (x : Vec 2) : Vec 2 := if Balanced x then star x else x

theorem balanced_star (x : Vec 2) : Balanced (star x) ↔ Balanced x := by
  simp [Balanced, normSq_star]

theorem conditionalConjugation_involutive : Function.Involutive conditionalConjugation := by
  intro x
  by_cases h : Balanced x
  · simp [conditionalConjugation, h, (balanced_star x).mpr h]
  · simp [conditionalConjugation, h]

theorem conditionalConjugation_reversible : Reversible conditionalConjugation :=
  conditionalConjugation_involutive.bijective

theorem conditionalConjugation_norm : NormPreserving conditionalConjugation := by
  intro x
  unfold conditionalConjugation
  split_ifs <;> simp [vnorm_star]

theorem conditionalConjugation_nonvanishing : Nonvanishing conditionalConjugation := by
  intro x hx hz
  have hn := conditionalConjugation_norm x
  rw [hz, vnorm_zero] at hn
  exact hx ((vnorm_eq_zero_iff x).mp hn.symm)

theorem conditionalConjugation_coordinate_norm (x : Vec 2) (i : Fin 2) :
    GaussRat.normSq (conditionalConjugation x i) = GaussRat.normSq (x i) := by
  unfold conditionalConjugation
  split_ifs <;> simp [normSq_star]

theorem conditionalConjugation_basis : BasisStatistics conditionalConjugation := by
  intro x i
  rw [tp_e_left, tp_e_left, conditionalConjugation_norm,
    conditionalConjugation_coordinate_norm]

theorem normSq_neg_local (z : GaussRat) : GaussRat.normSq (-z) = GaussRat.normSq z := by
  simp [GaussRat.normSq]

/-- Orthogonal nonzero vectors in two sectors are either both balanced or both unbalanced. -/
theorem balanced_of_orthogonal {x y : Vec 2} (hx : x ≠ 0) (hb : Balanced x)
    (ho : ip x y = 0) : Balanced y := by
  have he : star (x 0) * y 0 = -(star (x 1) * y 1) := by
    have h := ho
    rw [ip_eq_sum, Fin.sum_univ_two] at h
    exact eq_neg_of_add_eq_zero_left h
  have hn := congrArg GaussRat.normSq he
  simp only [GaussRat.normSq_mul, normSq_star, normSq_neg_local] at hn
  have hp : GaussRat.normSq (x 1) ≠ 0 := by
    intro hz
    apply hx
    funext i
    fin_cases i
    · exact (GaussRat.normSq_eq_zero_iff _).mp (hb.trans hz)
    · exact (GaussRat.normSq_eq_zero_iff _).mp hz
  rw [hb] at hn
  exact mul_left_cancel₀ hp hn

theorem conditionalConjugation_orth_forward {x y : Vec 2} (ho : ip x y = 0) :
    ip (conditionalConjugation x) (conditionalConjugation y) = 0 := by
  by_cases hx : x = 0
  · subst x
    simp [conditionalConjugation, Balanced, ip]
  by_cases hy : y = 0
  · subst y
    simp [conditionalConjugation, Balanced, ip]
  have he : Balanced x ↔ Balanced y :=
    ⟨fun hb => balanced_of_orthogonal hx hb ho, fun hb =>
      balanced_of_orthogonal hy hb (by rw [← star_ip, ho, star_zero])⟩
  by_cases hb : Balanced x
  · simp [conditionalConjugation, hb, he.mp hb, ip_star_star, ho]
  · simp [conditionalConjugation, hb, mt he.mpr hb, ho]

theorem conditionalConjugation_orthogonality : Orthogonality conditionalConjugation := by
  intro x y
  constructor
  · intro h
    have hh := conditionalConjugation_orth_forward h
    rwa [conditionalConjugation_involutive x, conditionalConjugation_involutive y] at hh
  · exact conditionalConjugation_orth_forward

def witnessA : Vec 2 := ![1, GaussRat.I]
def witnessB : Vec 2 := ![1, 2 * GaussRat.I]

theorem witnessA_ne : witnessA ≠ 0 := by
  intro h
  have := congrFun h 0
  norm_num [witnessA] at this

theorem witnessB_ne : witnessB ≠ 0 := by
  intro h
  have := congrFun h 0
  norm_num [witnessB] at this

theorem countermodel_probabilities :
    tp witnessA witnessB = 9 / 10 ∧
    tp (conditionalConjugation witnessA) (conditionalConjugation witnessB) = 1 / 10 := by
  norm_num [tp, ip_eq_sum, vnorm, Fin.sum_univ_two, witnessA, witnessB,
    conditionalConjugation, Balanced, GaussRat.normSq]

theorem conditionalConjugation_not_tpPreserving : ¬ TpPreserving conditionalConjugation := by
  intro h
  have he := h.tp_eq _ _ witnessA_ne witnessB_ne
  rw [countermodel_probabilities.1, countermodel_probabilities.2] at he
  norm_num at he


/-! Ray quotient: the countermodel acts on all rays, not just test vectors. -/
def SameRay (x y : Vec n) : Prop := ∃ c : GaussRat, c ≠ 0 ∧ y = c • x

theorem sameRay_refl (x : Vec n) : SameRay x x := ⟨1, one_ne_zero, (one_smul _ _).symm⟩

theorem sameRay_symm {x y : Vec n} : SameRay x y → SameRay y x := by
  rintro ⟨c, hc, rfl⟩
  exact ⟨c⁻¹, inv_ne_zero hc, by rw [smul_smul, inv_mul_cancel₀ hc, one_smul]⟩

theorem sameRay_trans {x y z : Vec n} : SameRay x y → SameRay y z → SameRay x z := by
  rintro ⟨c, hc, rfl⟩ ⟨d, hd, rfl⟩
  exact ⟨d * c, mul_ne_zero hd hc, smul_smul _ _ _⟩

abbrev NonzeroVec (n : ℕ) := {x : Vec n // x ≠ 0}

def raySetoid (n : ℕ) : Setoid (NonzeroVec n) where
  r x y := SameRay x.val y.val
  iseqv := ⟨fun x => sameRay_refl x.val, fun h => sameRay_symm h,
    fun h₁ h₂ => sameRay_trans h₁ h₂⟩

abbrev Ray (n : ℕ) := Quotient (raySetoid n)

def RayCompatible (T : Vec n → Vec n) : Prop :=
  ∀ x y, SameRay x y → SameRay (T x) (T y)

def rayMap (T : Vec n → Vec n) (hn : Nonvanishing T) (hc : RayCompatible T) : Ray n → Ray n :=
  Quotient.map (fun x : NonzeroVec n => ⟨T x.val, hn x.val x.property⟩)
    (fun x y h => hc x.val y.val h)

def involutiveRayEquiv (T : Vec n → Vec n) (hn : Nonvanishing T) (hc : RayCompatible T)
    (hi : Function.Involutive T) : Ray n ≃ Ray n where
  toFun := rayMap T hn hc
  invFun := rayMap T hn hc
  left_inv q := by
    induction q using Quotient.inductionOn with
    | h x =>
      apply congrArg (Quotient.mk (raySetoid n))
      apply Subtype.ext
      exact hi x.val
  right_inv q := by
    induction q using Quotient.inductionOn with
    | h x =>
      apply congrArg (Quotient.mk (raySetoid n))
      apply Subtype.ext
      exact hi x.val

theorem balanced_smul {c : GaussRat} (hc : c ≠ 0) (x : Vec 2) :
    Balanced (c • x) ↔ Balanced x := by
  unfold Balanced
  simp only [Pi.smul_apply, smul_eq_mul, GaussRat.normSq_mul]
  exact mul_right_inj' (fun h => hc ((GaussRat.normSq_eq_zero_iff c).mp h))

theorem conditionalConjugation_rayCompatible : RayCompatible conditionalConjugation := by
  rintro x y ⟨c, hc, rfl⟩
  by_cases hb : Balanced x
  · refine ⟨star c, star_ne_zero.mpr hc, ?_⟩
    simp [conditionalConjugation, hb, (balanced_smul hc x).mpr hb, star_smul]
  · refine ⟨c, hc, ?_⟩
    simp [conditionalConjugation, hb, mt (balanced_smul hc x).mp hb]

def countermodelRayEquiv : Ray 2 ≃ Ray 2 :=
  involutiveRayEquiv conditionalConjugation conditionalConjugation_nonvanishing
    conditionalConjugation_rayCompatible conditionalConjugation_involutive

/-- Covariance under the nontrivial relabelling of two report sectors. -/
def reportSwap (x : Vec 2) : Vec 2 := ![x 1, x 0]

def ReportSwapCovariant (T : Vec 2 → Vec 2) : Prop :=
  ∀ x, T (reportSwap x) = reportSwap (T x)

theorem balanced_reportSwap (x : Vec 2) : Balanced (reportSwap x) ↔ Balanced x := by
  simp [Balanced, reportSwap, eq_comm]

theorem conditionalConjugation_reportSwap : ReportSwapCovariant conditionalConjugation := by
  intro x
  by_cases hb : Balanced x
  · simp only [conditionalConjugation, ite_eq_left hb, ite_eq_left ((balanced_reportSwap x).mpr hb)]
    funext i
    fin_cases i <;> rfl
  · simp [conditionalConjugation, hb, mt (balanced_reportSwap x).mp hb]

/-- These weaker conditions hold together, while the transition law fails. -/
theorem insufficient_operational_package :
    BornRule (tp (n := 2)) ∧ Reversible conditionalConjugation ∧
    Nonvanishing conditionalConjugation ∧ RayCompatible conditionalConjugation ∧
    NormPreserving conditionalConjugation ∧ BasisStatistics conditionalConjugation ∧
    ReportSwapCovariant conditionalConjugation ∧ Orthogonality conditionalConjugation ∧
    OrthogonalCalibration conditionalConjugation ∧ ¬ TpPreserving conditionalConjugation :=
  ⟨born_rule, conditionalConjugation_reversible, conditionalConjugation_nonvanishing,
    conditionalConjugation_rayCompatible, conditionalConjugation_norm,
    conditionalConjugation_basis, conditionalConjugation_reportSwap,
    conditionalConjugation_orthogonality,
    orthogonality_calibration conditionalConjugation_orthogonality,
    conditionalConjugation_not_tpPreserving⟩


/-! Fixed-frame tomography: finitely many effects, but every nonzero state. -/
structure ProbeStatistics (x y : Vec n) : Prop where
  basis : ∀ i, tp (e i) x = tp (e i) y
  realPair : ∀ i j, j ≠ i → tp (p i j) x = tp (p i j) y
  imagPair : ∀ i j, j ≠ i → tp (qs i 1 j) x = tp (qs i 1 j) y

def TomographicStatistics (T : Vec n → Vec n) : Prop :=
  ∀ x, x ≠ 0 → ProbeStatistics x (T x)

/-- Equality of this finite probe family separates all nonzero Gaussian-rational rays. -/
theorem tomography_sameRay {x y : Vec n} (hx : x ≠ 0) (hy : y ≠ 0)
    (h : ProbeStatistics x y) : SameRay x y := by
  classical
  obtain ⟨i₀, hxi⟩ : ∃ i, x i ≠ 0 := by
    exact not_forall.mp (fun h => hx (funext h))
  have hyi : y i₀ ≠ 0 := by
    intro hz
    have hb := h.basis i₀
    rw [tp_e_left, tp_e_left, hz] at hb
    have hn0 : GaussRat.normSq (0 : GaussRat) = 0 := by simp [GaussRat.normSq]
    rw [hn0, zero_div] at hb
    rcases div_eq_zero_iff.mp hb with hn | hn
    · exact hxi ((GaussRat.normSq_eq_zero_iff _).mp hn)
    · exact vnorm_ne_zero hx hn
  let u := (x i₀)⁻¹ • x
  let v := (y i₀)⁻¹ • y
  have hu : u i₀ = 1 := by simp [u, hxi]
  have hv : v i₀ = 1 := by simp [v, hyi]
  have hun : u ≠ 0 := smul_ne_zero (inv_ne_zero hxi) hx
  have hvn : v ≠ 0 := smul_ne_zero (inv_ne_zero hyi) hy
  have he : ∀ i, tp (e i) u = tp (e i) v := by
    intro i
    simpa only [u, v, tp_smul_right (inv_ne_zero hxi),
      tp_smul_right (inv_ne_zero hyi)] using h.basis i
  have hN : vnorm v = vnorm u := by
    have hh := he i₀
    rw [tp_e_left, tp_e_left, hu, hv, normSq_one] at hh
    have := vnorm_ne_zero hun
    have := vnorm_ne_zero hvn
    field_simp at hh
    linarith
  have hvec : v = u := by
    funext j
    by_cases hj : j = i₀
    · subst j
      rw [hu, hv]
    · have hp : tp (p i₀ j) u = tp (p i₀ j) v := by
        simpa only [u, v, tp_smul_right (inv_ne_zero hxi),
          tp_smul_right (inv_ne_zero hyi)] using h.realPair i₀ j hj
      have hq : tp (qs i₀ 1 j) u = tp (qs i₀ 1 j) v := by
        simpa only [u, v, tp_smul_right (inv_ne_zero hxi),
          tp_smul_right (inv_ne_zero hyi)] using h.imagPair i₀ j hj
      have hh := coord_rigidity (s := 1) hj hu hv hN (Or.inl rfl)
        (he j) hp hq
      simpa only [tw_one] using hh
  refine ⟨y i₀ * (x i₀)⁻¹, mul_ne_zero hyi (inv_ne_zero hxi), ?_⟩
  calc y = y i₀ • v := by simp [v, smul_smul, hyi]
    _ = y i₀ • u := by rw [hvec]
    _ = (y i₀ * (x i₀)⁻¹) • x := smul_smul _ _ _

/-- This route requires no linear lift. It actually forces every ray to be fixed. -/
theorem tomography_tpPreserving {T : Vec n → Vec n} (hn : Nonvanishing T)
    (ht : TomographicStatistics T) : TpPreserving T where
  ne_zero := hn
  tp_eq x y hx hy := by
    obtain ⟨a, ha, hax⟩ := tomography_sameRay hx (hn x hx) (ht x hx)
    obtain ⟨b, hb, hby⟩ := tomography_sameRay hy (hn y hy) (ht y hy)
    rw [hax, hby, tp_smul_left ha, tp_smul_right hb]

theorem tomography_identity : TomographicStatistics (id : Vec n → Vec n) :=
  fun _ _ => ⟨fun _ => rfl, fun _ _ _ => rfl, fun _ _ _ => rfl⟩

/-! Subspace-lattice preservation without orthogonality is also insufficient. -/
def stretch : Vec 2 ≃ₗ[GaussRat] Vec 2 where
  toFun x := ![x 0, 2 * x 1]
  invFun x := ![x 0, (2 : GaussRat)⁻¹ * x 1]
  map_add' x y := by
    funext i
    fin_cases i <;> simp [mul_add]
  map_smul' c x := by
    funext i
    fin_cases i <;> simp
    ring
  left_inv x := by
    funext i
    fin_cases i <;> simp
  right_inv x := by
    funext i
    fin_cases i <;> simp

def SubspaceLatticeLift (T : Vec n → Vec n) : Prop :=
  ∃ E : Submodule GaussRat (Vec n) ≃o Submodule GaussRat (Vec n),
    ∀ x, E (Submodule.span GaussRat {x}) = Submodule.span GaussRat {T x}

def stretchLattice : Submodule GaussRat (Vec 2) ≃o Submodule GaussRat (Vec 2) :=
  Submodule.orderIsoMapComap stretch

theorem stretch_lattice : SubspaceLatticeLift stretch := by
  refine ⟨stretchLattice, fun x => ?_⟩
  change Submodule.map stretch.toLinearMap (Submodule.span GaussRat {x}) = _
  rw [Submodule.map_span, Set.image_singleton]
  rfl

def linearRayEquiv (E : Vec n ≃ₗ[GaussRat] Vec n) : Ray n ≃ Ray n where
  toFun := rayMap E (fun x hx h => hx (E.injective (h.trans E.map_zero.symm))) (by
    rintro x y ⟨c, hc, rfl⟩
    exact ⟨c, hc, E.map_smul c x⟩)
  invFun := rayMap E.symm (fun x hx h => hx (E.symm.injective (h.trans E.symm.map_zero.symm))) (by
    rintro x y ⟨c, hc, rfl⟩
    exact ⟨c, hc, E.symm.map_smul c x⟩)
  left_inv q := by
    induction q using Quotient.inductionOn with
    | h x =>
      apply congrArg (Quotient.mk (raySetoid n))
      apply Subtype.ext
      exact E.symm_apply_apply x.val
  right_inv q := by
    induction q using Quotient.inductionOn with
    | h x =>
      apply congrArg (Quotient.mk (raySetoid n))
      apply Subtype.ext
      exact E.apply_symm_apply x.val

def stretchRayEquiv : Ray 2 ≃ Ray 2 := linearRayEquiv stretch

theorem stretch_probabilities :
    tp (e (0 : Fin 2)) ![1, 1] = 1 / 2 ∧
    tp (stretch (e 0)) (stretch ![1, 1]) = 1 / 5 := by
  norm_num [tp, ip_eq_sum, vnorm, Fin.sum_univ_two, stretch, e, Pi.single_apply,
    GaussRat.normSq]

theorem stretch_not_tpPreserving : ¬ TpPreserving stretch := by
  intro h
  have hv : (![1, 1] : Vec 2) ≠ 0 := by
    intro hz
    have hh := congrFun hz 0
    norm_num at hh
  have he := h.tp_eq _ _ (e_ne_zero 0) hv
  rw [stretch_probabilities.1, stretch_probabilities.2] at he
  norm_num at he


/-! Boundaries and independent premises. -/
def RealProbeStatistics (T : Vec n → Vec n) : Prop :=
  ∀ x i j, tp (p i j) (T x) = tp (p i j) x

theorem conditionalConjugation_realProbes : RealProbeStatistics conditionalConjugation := by
  intro x i j
  have hs : star (p i j) = p i j := by simp [p, e, Pi.star_single]
  by_cases hb : Balanced x
  · rw [conditionalConjugation, ite_eq_left hb, ← hs, tp_star_star, hs]
  · rw [conditionalConjugation, ite_eq_right hb]

theorem imaginary_probe_probabilities :
    tp (qs (0 : Fin 2) 1 1) witnessA = 1 ∧
    tp (qs (0 : Fin 2) 1 1) (conditionalConjugation witnessA) = 0 := by
  norm_num [tp, ip_eq_sum, vnorm, Fin.sum_univ_two, witnessA, qs, e, Pi.single_apply,
    conditionalConjugation, Balanced, GaussRat.normSq]

theorem conditionalConjugation_not_linearLift : ¬ LinearLift conditionalConjugation := by
  intro hl
  exact conditionalConjugation_not_tpPreserving
    (linear_calibration_tpPreserving 0 hl
      (orthogonality_calibration conditionalConjugation_orthogonality)
      (conditionalConjugation_nonvanishing _ (e_ne_zero 0)))

theorem conditionalConjugation_not_tomographic : ¬ TomographicStatistics conditionalConjugation := by
  intro ht
  exact conditionalConjugation_not_tpPreserving
    (tomography_tpPreserving conditionalConjugation_nonvanishing ht)

theorem identity_calibration : OrthogonalCalibration (id : Vec n → Vec n) :=
  orthogonality_calibration (fun _ _ => Iff.rfl)

theorem identity_linearLift : LinearLift (id : Vec n → Vec n) :=
  ⟨1, fun x => (one_mulVec x).symm⟩

theorem identity_nonvanishing : Nonvanishing (id : Vec n → Vec n) := fun _ hx => hx

theorem stretch_linearLift : LinearLift stretch := by
  refine ⟨Matrix.diagonal ![1, 2], fun x => ?_⟩
  funext i
  fin_cases i <;> simp [stretch, mulVec_diagonal]

theorem insufficient_lattice_package :
    BornRule (tp (n := 2)) ∧ LinearLift stretch ∧ Reversible stretch ∧
    SubspaceLatticeLift stretch ∧ ¬ TpPreserving stretch :=
  ⟨born_rule, stretch_linearLift, stretch.bijective, stretch_lattice, stretch_not_tpPreserving⟩

/-- The one-sector boundary has a single nonzero ray. -/
theorem oneSector_sameRay {x y : Vec 1} (hx : x ≠ 0) (hy : y ≠ 0) : SameRay x y := by
  have hxi : x 0 ≠ 0 := by
    intro hz
    apply hx
    funext i
    fin_cases i
    exact hz
  have hyi : y 0 ≠ 0 := by
    intro hz
    apply hy
    funext i
    fin_cases i
    exact hz
  refine ⟨y 0 / x 0, div_ne_zero hyi hxi, ?_⟩
  funext i
  fin_cases i
  simp [div_mul_cancel₀ _ hxi]

theorem oneSector_tpPreserving {T : Vec 1 → Vec 1} (hn : Nonvanishing T) :
    TpPreserving T where
  ne_zero := hn
  tp_eq x y hx hy := by
    rw [(tp_eq_one_iff (hn x hx) (hn y hy)).mpr (oneSector_sameRay (hn x hx) (hn y hy)),
      (tp_eq_one_iff hx hy).mpr (oneSector_sameRay hx hy)]

end CampaignTransitionProbability

#print axioms CampaignTransitionProbability.Vec
#print axioms CampaignTransitionProbability.BornRule
#print axioms CampaignTransitionProbability.born_rule
#print axioms CampaignTransitionProbability.Nonvanishing
#print axioms CampaignTransitionProbability.Reversible
#print axioms CampaignTransitionProbability.Orthogonality
#print axioms CampaignTransitionProbability.BasisStatistics
#print axioms CampaignTransitionProbability.NormPreserving
#print axioms CampaignTransitionProbability.LinearLift
#print axioms CampaignTransitionProbability.OrthogonalCalibration
#print axioms CampaignTransitionProbability.NonzeroAnchor
#print axioms CampaignTransitionProbability.ip_sub_left
#print axioms CampaignTransitionProbability.ip_sub_right
#print axioms CampaignTransitionProbability.calibration_norms
#print axioms CampaignTransitionProbability.calibration_similarity
#print axioms CampaignTransitionProbability.linear_calibration_tpPreserving
#print axioms CampaignTransitionProbability.orthogonality_calibration
#print axioms CampaignTransitionProbability.linear_calibration_wigner
#print axioms CampaignTransitionProbability.Balanced
#print axioms CampaignTransitionProbability.conditionalConjugation
#print axioms CampaignTransitionProbability.balanced_star
#print axioms CampaignTransitionProbability.conditionalConjugation_involutive
#print axioms CampaignTransitionProbability.conditionalConjugation_reversible
#print axioms CampaignTransitionProbability.conditionalConjugation_norm
#print axioms CampaignTransitionProbability.conditionalConjugation_nonvanishing
#print axioms CampaignTransitionProbability.conditionalConjugation_coordinate_norm
#print axioms CampaignTransitionProbability.conditionalConjugation_basis
#print axioms CampaignTransitionProbability.normSq_neg_local
#print axioms CampaignTransitionProbability.balanced_of_orthogonal
#print axioms CampaignTransitionProbability.conditionalConjugation_orth_forward
#print axioms CampaignTransitionProbability.conditionalConjugation_orthogonality
#print axioms CampaignTransitionProbability.witnessA
#print axioms CampaignTransitionProbability.witnessB
#print axioms CampaignTransitionProbability.witnessA_ne
#print axioms CampaignTransitionProbability.witnessB_ne
#print axioms CampaignTransitionProbability.countermodel_probabilities
#print axioms CampaignTransitionProbability.conditionalConjugation_not_tpPreserving
#print axioms CampaignTransitionProbability.SameRay
#print axioms CampaignTransitionProbability.sameRay_refl
#print axioms CampaignTransitionProbability.sameRay_symm
#print axioms CampaignTransitionProbability.sameRay_trans
#print axioms CampaignTransitionProbability.NonzeroVec
#print axioms CampaignTransitionProbability.raySetoid
#print axioms CampaignTransitionProbability.Ray
#print axioms CampaignTransitionProbability.RayCompatible
#print axioms CampaignTransitionProbability.rayMap
#print axioms CampaignTransitionProbability.involutiveRayEquiv
#print axioms CampaignTransitionProbability.balanced_smul
#print axioms CampaignTransitionProbability.conditionalConjugation_rayCompatible
#print axioms CampaignTransitionProbability.countermodelRayEquiv
#print axioms CampaignTransitionProbability.reportSwap
#print axioms CampaignTransitionProbability.ReportSwapCovariant
#print axioms CampaignTransitionProbability.balanced_reportSwap
#print axioms CampaignTransitionProbability.conditionalConjugation_reportSwap
#print axioms CampaignTransitionProbability.insufficient_operational_package
#print axioms CampaignTransitionProbability.ProbeStatistics
#print axioms CampaignTransitionProbability.TomographicStatistics
#print axioms CampaignTransitionProbability.tomography_sameRay
#print axioms CampaignTransitionProbability.tomography_tpPreserving
#print axioms CampaignTransitionProbability.tomography_identity
#print axioms CampaignTransitionProbability.stretch
#print axioms CampaignTransitionProbability.SubspaceLatticeLift
#print axioms CampaignTransitionProbability.stretchLattice
#print axioms CampaignTransitionProbability.stretch_lattice
#print axioms CampaignTransitionProbability.linearRayEquiv
#print axioms CampaignTransitionProbability.stretchRayEquiv
#print axioms CampaignTransitionProbability.stretch_probabilities
#print axioms CampaignTransitionProbability.stretch_not_tpPreserving
#print axioms CampaignTransitionProbability.RealProbeStatistics
#print axioms CampaignTransitionProbability.conditionalConjugation_realProbes
#print axioms CampaignTransitionProbability.imaginary_probe_probabilities
#print axioms CampaignTransitionProbability.conditionalConjugation_not_linearLift
#print axioms CampaignTransitionProbability.conditionalConjugation_not_tomographic
#print axioms CampaignTransitionProbability.identity_calibration
#print axioms CampaignTransitionProbability.identity_linearLift
#print axioms CampaignTransitionProbability.identity_nonvanishing
#print axioms CampaignTransitionProbability.stretch_linearLift
#print axioms CampaignTransitionProbability.insufficient_lattice_package
#print axioms CampaignTransitionProbability.oneSector_sameRay
#print axioms CampaignTransitionProbability.oneSector_tpPreserving
