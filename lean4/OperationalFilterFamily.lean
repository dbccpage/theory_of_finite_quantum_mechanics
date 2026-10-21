import OperationalTomography

/-!
Selective test followed by preparation gives a rank-one outcome filter.
Positivity, sequential admission, global separation, and spanning are explicit
operational hypotheses. Product-test resets descend, but their irreducibility
is equivalent to tomography. Global reset descent contains the missing
separation claim. No primitive-to-QM or unconditional tomography claim is made.
AuthorityEffect: None.
-/
namespace OperationalFilterFamily
open OperationalTomography

variable {K V C I J G : Type*} [Field K]
  [AddCommGroup V] [Module K V] [AddCommGroup C] [Module K C]

def reset (p : V) (e : V →ₗ[K] K) : V →ₗ[K] V := e.smulRight p

def preparation (p : V) : K →ₗ[K] V := (LinearMap.id : K →ₗ[K] K).smulRight p

theorem reset_is_sequential (p : V) (e : V →ₗ[K] K) :
    reset p e = (preparation p).comp e := by
  ext x
  rfl

/-- Admission of a test followed by a preparation is an operational closure rule,
separate from mathematical positivity of the resulting linear map. -/
structure SequentialAdmission (K V : Type*) [Field K]
    [AddCommGroup V] [Module K V] where
  preparations : Set (K →ₗ[K] V)
  tests : Set (V →ₗ[K] K)
  processes : Set (V →ₗ[K] V)
  sequential : ∀ P ∈ preparations, ∀ e ∈ tests, P.comp e ∈ processes

theorem reset_admitted (A : SequentialAdmission K V) (p : V) (e : V →ₗ[K] K)
    (hp : preparation p ∈ A.preparations) (he : e ∈ A.tests) :
    reset p e ∈ A.processes := by
  rw [reset_is_sequential]
  exact A.sequential _ hp _ he

/-- An ordered rational carrier. Cone and normalization are supplied data. -/
structure OrderedModel (V : Type*) [AddCommGroup V] [Module ℚ V] where
  positive : Set V
  zero_mem : (0 : V) ∈ positive
  add_mem : ∀ x ∈ positive, ∀ y ∈ positive, x + y ∈ positive
  smul_mem : ∀ a : ℚ, 0 ≤ a → ∀ x ∈ positive, a • x ∈ positive
  unit : V →ₗ[ℚ] ℚ
  unit_nonneg : ∀ x ∈ positive, 0 ≤ unit x

section Ordered
variable {W : Type*} [AddCommGroup W] [Module ℚ W]

def OutcomeFilter (O : OrderedModel W) (T : W →ₗ[ℚ] W) : Prop :=
  (∀ x ∈ O.positive, T x ∈ O.positive) ∧
  (∀ x ∈ O.positive, O.unit (T x) ≤ O.unit x)

theorem reset_outcome_filter (O : OrderedModel W) (p : W) (e : W →ₗ[ℚ] ℚ)
    (hp : p ∈ O.positive) (hn : O.unit p = 1)
    (he : ∀ x ∈ O.positive, 0 ≤ e x ∧ e x ≤ O.unit x) :
    OutcomeFilter O (reset p e) := by
  constructor
  · intro x hx
    exact O.smul_mem (e x) (he x hx).1 p hp
  · intro x hx
    simpa [reset, hn] using (he x hx).2

theorem outcome_filter_comp (O : OrderedModel W) (T S : W →ₗ[ℚ] W)
    (hT : OutcomeFilter O T) (hS : OutcomeFilter O S) :
    OutcomeFilter O (T.comp S) := by
  constructor
  · intro x hx
    exact hT.1 _ (hS.1 x hx)
  · intro x hx
    exact (hT.2 _ (hS.1 x hx)).trans (hS.2 x hx)
end Ordered

/-- Separating GLOBAL effects and spanning preparations suffice for reset
irreducibility. They are not assumed to be product effects/preparations. -/
theorem resets_irreducible (p : I → V) (e : J → V →ₗ[K] K)
    (span : Submodule.span K (Set.range p) = ⊤)
    (separate : ∀ x : V, (∀ j, e j x = 0) → x = 0) :
    OperationalTomography.Irreducible (fun ij : I × J => reset (p ij.1) (e ij.2)) := by
  intro W hW
  by_cases hz : W = ⊥
  · exact Or.inl hz
  right
  obtain ⟨x, hxW, hx⟩ := Submodule.exists_mem_ne_zero_of_ne_bot hz
  have hex : ∃ j, e j x ≠ 0 := by
    by_contra h
    exact hx (separate x (fun j => not_not.mp (not_exists.mp h j)))
  obtain ⟨j, hj⟩ := hex
  have hp : ∀ i, p i ∈ W := by
    intro i
    have h := W.smul_mem ((e j x)⁻¹) (hW (i,j) x hxW)
    simpa [reset, smul_smul, hj] using h
  have hs : Submodule.span K (Set.range p) ≤ W := by
    apply Submodule.span_le.mpr
    rintro _ ⟨i,rfl⟩
    exact hp i
  rw [span] at hs
  exact top_unique hs

/-- One family satisfies admission, the outcome bound, and irreducibility under
explicit global operational premises. Product descent is deliberately separate. -/
theorem admitted_reset_family {W P E : Type*} [AddCommGroup W] [Module ℚ W]
    (O : OrderedModel W) (A : SequentialAdmission ℚ W)
    (p : P → W) (e : E → W →ₗ[ℚ] ℚ)
    (hp : ∀ i, p i ∈ O.positive ∧ O.unit (p i) = 1 ∧ preparation (p i) ∈ A.preparations)
    (he : ∀ j, e j ∈ A.tests ∧ ∀ x ∈ O.positive, 0 ≤ e j x ∧ e j x ≤ O.unit x)
    (span : Submodule.span ℚ (Set.range p) = ⊤)
    (separate : ∀ x : W, (∀ j, e j x = 0) → x = 0) :
    (∀ ij : P × E, reset (p ij.1) (e ij.2) ∈ A.processes ∧
      OutcomeFilter O (reset (p ij.1) (e ij.2))) ∧
    OperationalTomography.Irreducible (fun ij : P × E => reset (p ij.1) (e ij.2)) := by
  constructor
  · intro ij
    exact ⟨reset_admitted A _ _ (hp ij.1).2.2 (he ij.2).1,
      reset_outcome_filter O _ _ (hp ij.1).1 (hp ij.1).2.1 (he ij.2).2⟩
  · exact resets_irreducible p e span separate

/-- Normalized positive states span a generating ordered carrier when only
zero has zero normalization. No tomography or local frame is used. -/
theorem normalized_preparations_span {W : Type*} [AddCommGroup W] [Module ℚ W]
    (O : OrderedModel W) (generating : Submodule.span ℚ O.positive = ⊤)
    (faithful : ∀ x ∈ O.positive, O.unit x = 0 → x = 0) :
    Submodule.span ℚ {p : W | p ∈ O.positive ∧ O.unit p = 1} = ⊤ := by
  apply top_unique
  rw [← generating]
  apply Submodule.span_le.mpr
  intro x hx
  by_cases hz : x = 0
  · rw [hz]; exact Submodule.zero_mem _
  have hu : O.unit x ≠ 0 := fun h => hz (faithful x hx h)
  have hp : (O.unit x)⁻¹ • x ∈ O.positive :=
    O.smul_mem _ (inv_nonneg.mpr (O.unit_nonneg x hx)) _ hx
  have hn : O.unit ((O.unit x)⁻¹ • x) = 1 := by simp [hu]
  have hm := (Submodule.span ℚ {p : W | p ∈ O.positive ∧ O.unit p = 1}).smul_mem
    (O.unit x) (Submodule.subset_span (show (O.unit x)⁻¹ • x ∈
      {p : W | p ∈ O.positive ∧ O.unit p = 1} from ⟨hp,hn⟩))
  simpa [smul_smul, hu] using hm

/-- Bounded globally separating effects force faithful normalization on the
positive cone; this is derived rather than an additional family hypothesis. -/
theorem normalization_faithful {W E : Type*} [AddCommGroup W] [Module ℚ W]
    (O : OrderedModel W) (e : E → W →ₗ[ℚ] ℚ)
    (bounded : ∀ j x, x ∈ O.positive → 0 ≤ e j x ∧ e j x ≤ O.unit x)
    (separate : ∀ x : W, (∀ j, e j x = 0) → x = 0) :
    ∀ x ∈ O.positive, O.unit x = 0 → x = 0 := by
  intro x hx hu
  apply separate x
  intro j
  have h := bounded j x hx
  exact le_antisymm (hu ▸ h.2) h.1

/-- Canonical normalized preparations with separating admitted global effects
construct an admitted positive subnormalized irreducible reset family. Only
sequential admission, cone generation, bounded global effects and global
separation are supplied here; product-test descent remains a separate issue. -/
theorem normalized_reset_family {W E : Type*} [AddCommGroup W] [Module ℚ W]
    (O : OrderedModel W) (A : SequentialAdmission ℚ W)
    (generating : Submodule.span ℚ O.positive = ⊤)
    (prepare_available : ∀ p ∈ O.positive, O.unit p = 1 → preparation p ∈ A.preparations)
    (e : E → W →ₗ[ℚ] ℚ)
    (he : ∀ j, e j ∈ A.tests ∧ ∀ x ∈ O.positive, 0 ≤ e j x ∧ e j x ≤ O.unit x)
    (separate : ∀ x : W, (∀ j, e j x = 0) → x = 0) :
    let P := {p : W // p ∈ O.positive ∧ O.unit p = 1}
    (∀ ij : P × E, reset (ij.1 : W) (e ij.2) ∈ A.processes ∧
      OutcomeFilter O (reset (ij.1 : W) (e ij.2))) ∧
    OperationalTomography.Irreducible (fun ij : P × E => reset (ij.1 : W) (e ij.2)) := by
  let P := {p : W // p ∈ O.positive ∧ O.unit p = 1}
  have hr : Set.range (fun p : P => (p : W)) = {p : W | p ∈ O.positive ∧ O.unit p = 1} := by
    ext x
    constructor
    · rintro ⟨p,rfl⟩; exact p.property
    · intro hx; exact ⟨⟨x,hx⟩,rfl⟩
  apply admitted_reset_family O A (fun p : P => (p : W)) e
  · intro p
    exact ⟨p.property.1,p.property.2,prepare_available _ p.property.1 p.property.2⟩
  · exact he
  · rw [hr]
    exact normalized_preparations_span O generating
      (normalization_faithful O e (fun j => (he j).2) separate)
  · exact separate

/-- Product-observable tests give descent for arbitrary output preparations. -/
theorem reset_pullback (M : V →ₗ[K] C) (p : V) (f : C →ₗ[K] K) (x : V) :
    M (reset p (f.comp M) x) = reset (M p) f (M x) := by
  simp [reset]

theorem reset_kills_hidden (M : V →ₗ[K] C) (p : V) (f : C →ₗ[K] K)
    (x : V) (hx : M x = 0) : reset p (f.comp M) x = 0 := by
  simp [reset, hx]

/-- If one output preparation is visibly normalized, descent of its reset
is equivalent to factorization of the input effect through product observation.
This is the precise circularity boundary for global measure-and-prepare. -/
theorem reset_descent_iff_effect_factor (M : V →ₗ[K] C) (p : V)
    (q : C →ₗ[K] K) (visible : q (M p) = 1) (e : V →ₗ[K] K) :
    (∃ L : C →ₗ[K] C, ∀ x, M (reset p e x) = L (M x)) ↔
    ∃ f : C →ₗ[K] K, e = f.comp M := by
  constructor
  · rintro ⟨L,hL⟩
    refine ⟨q.comp L, ?_⟩
    ext x
    have h := congrArg q (hL x)
    simpa [reset, visible] using h
  · rintro ⟨f,rfl⟩
    exact ⟨reset (M p) f, reset_pullback M p f⟩

/-- For a separating global effect family, assuming all these resets descend
is already equivalent to tomography. No irreducibility hypothesis is needed. -/
theorem global_reset_descent_iff_tomography (D : Calibrated K V C) (p : V)
    (q : C →ₗ[K] K) (visible : q (D.observe p) = 1)
    (e : J → V →ₗ[K] K)
    (separate : ∀ x : V, (∀ j, e j x = 0) → x = 0) :
    (∀ j, ∃ L : C →ₗ[K] C, ∀ x, D.observe (reset p (e j) x) = L (D.observe x)) ↔
    Function.Injective D.observe := by
  constructor
  · intro descent
    apply LinearMap.ker_eq_bot.mp
    apply eq_bot_iff.mpr
    intro x hx
    change x = 0
    apply separate x
    intro j
    obtain ⟨f,hf⟩ := (reset_descent_iff_effect_factor D.observe p q visible (e j)).mp (descent j)
    rw [hf]
    change f (D.observe x) = 0
    rw [show D.observe x = 0 from hx, map_zero]
  · intro tomography j
    refine ⟨D.observe.comp ((reset p (e j)).comp D.prepare), ?_⟩
    intro x
    simp only [LinearMap.comp_apply]
    rw [D.tomography_iff_reconstruction.mp tomography x]

/-- Algebraic closure includes more maps than physically admitted filters.
Consequently its hidden-kernel invariant also applies to any admitted subset.
Arbitrary sums/scalars are not asserted to preserve the outcome bound. -/
inductive Circuit (ops : G → V →ₗ[K] V) : (V →ₗ[K] V) → Prop
  | identity : Circuit ops LinearMap.id
  | generator (g : G) : Circuit ops (ops g)
  | add {T S} : Circuit ops T → Circuit ops S → Circuit ops (T + S)
  | scale (a : K) {T} : Circuit ops T → Circuit ops (a • T)
  | comp {T S} : Circuit ops T → Circuit ops S → Circuit ops (T.comp S)

theorem circuits_preserve_hidden (M : V →ₗ[K] C) (ops : G → V →ₗ[K] V)
    (loc : G → C →ₗ[K] C) (descent : ∀ g x, M (ops g x) = loc g (M x))
    {T : V →ₗ[K] V} (hT : Circuit ops T) :
    ∀ x, M x = 0 → M (T x) = 0 := by
  induction hT with
  | identity => intro x hx; exact hx
  | generator g => intro x hx; rw [descent, hx, map_zero]
  | add hT hS ihT ihS => intro x hx; simp [ihT x hx, ihS x hx]
  | scale a hT ihT => intro x hx; simp [ihT x hx]
  | comp hT hS ihT ihS => intro x hx; exact ihT _ (ihS x hx)

def lift (D : Calibrated K V C) (L : C →ₗ[K] C) : V →ₗ[K] V :=
  D.prepare.comp (L.comp D.observe)

theorem lift_descent (D : Calibrated K V C) (L : C →ₗ[K] C) (x : V) :
    D.observe (lift D L x) = L (D.observe x) := D.calibration _

theorem lift_comp (D : Calibrated K V C) (L N : C →ₗ[K] C) :
    (lift D L).comp (lift D N) = lift D (L.comp N) := by
  ext x
  simp [lift, D.calibration]

theorem lift_irreducible (D : Calibrated K V C) (ops : G → C →ₗ[K] C)
    (irr : OperationalTomography.Irreducible ops) (tomography : Function.Injective D.observe) :
    OperationalTomography.Irreducible (fun g => lift D (ops g)) := by
  intro W hW
  let W' : Submodule K C := W.comap D.prepare
  have inv : Invariant ops W' := by
    intro g c hc
    change D.prepare (ops g c) ∈ W
    have h := hW g (D.prepare c) hc
    simpa [lift, D.calibration] using h
  rcases irr W' inv with h | h
  · left
    apply eq_bot_iff.mpr
    intro x hx
    change x = 0
    have hc : D.observe x ∈ W' := by
      change D.prepare (D.observe x) ∈ W
      rwa [D.tomography_iff_reconstruction.mp tomography x]
    rw [h] at hc
    apply tomography
    simpa using hc
  · right
    apply top_unique
    intro x _
    have hc : D.observe x ∈ W' := by rw [h]; trivial
    change D.prepare (D.observe x) ∈ W at hc
    rwa [D.tomography_iff_reconstruction.mp tomography x] at hc

/-- Coordinate matrix units give a finite calibrated reset family. Global
irreducibility of this family is exactly tomography, not a weaker replacement. -/
theorem product_resets_irreducible_iff [Fintype I] [DecidableEq I] [Nonempty I]
    (D : Calibrated K V (I → K)) :
    OperationalTomography.Irreducible (fun ij : I × I => lift D (matrixUnit ij.1 ij.2)) ↔
    Function.Injective D.observe := by
  constructor
  · intro irr
    exact calibrated_tomography D _ _ (fun ij => lift_descent D _) irr
  · intro tomography
    exact lift_irreducible D _ matrix_units_irreducible tomography

def basisVector [DecidableEq I] (i : I) : I → K := fun k => if k = i then 1 else 0

theorem product_reset_formula [DecidableEq I] (D : Calibrated K V (I → K))
    (i j : I) : lift D (matrixUnit i j) =
    reset (D.prepare (basisVector i)) ((LinearMap.proj j).comp D.observe) := by
  ext x
  change D.prepare (matrixUnit i j (D.observe x)) = (D.observe x j) • D.prepare (basisVector i)
  rw [← map_smul]
  congr 1
  ext k
  by_cases h : k = i <;> simp [matrixUnit, basisVector, h]

theorem product_test_pullback [DecidableEq I] (D : Calibrated K V (I → K))
    (i j k : I) (x : V) :
    D.observe (lift D (matrixUnit i j) x) k = if k = i then D.observe x j else 0 := by
  rw [lift_descent]
  rfl

theorem doubled_reset_kills_hidden :
    reset ((1/2,1/2) : ℚ × ℚ) doubled.observe (1,-1) = 0 := by
  norm_num [reset, doubled]

theorem doubled_protected_reset_no_descent :
    ¬ ∃ L : ℚ →ₗ[ℚ] ℚ, ∀ x : ℚ × ℚ,
      doubled.observe (reset (1,0) (LinearMap.fst ℚ ℚ ℚ) x) = L (doubled.observe x) := by
  intro h
  have hv : (LinearMap.id : ℚ →ₗ[ℚ] ℚ) (doubled.observe (1,0)) = 1 := by norm_num [doubled]
  obtain ⟨f,hf⟩ := (reset_descent_iff_effect_factor doubled.observe (1,0) LinearMap.id hv
    (LinearMap.fst ℚ ℚ ℚ)).mp h
  apply protected_question_cannot_descend
  refine ⟨f, fun x => ?_⟩
  exact (LinearMap.congr_fun hf x).symm

end OperationalFilterFamily

#print axioms OperationalFilterFamily.reset_is_sequential
#print axioms OperationalFilterFamily.reset_admitted
#print axioms OperationalFilterFamily.reset_outcome_filter
#print axioms OperationalFilterFamily.outcome_filter_comp
#print axioms OperationalFilterFamily.resets_irreducible
#print axioms OperationalFilterFamily.reset_pullback
#print axioms OperationalFilterFamily.reset_kills_hidden
#print axioms OperationalFilterFamily.reset_descent_iff_effect_factor
#print axioms OperationalFilterFamily.global_reset_descent_iff_tomography
#print axioms OperationalFilterFamily.circuits_preserve_hidden
#print axioms OperationalFilterFamily.lift_descent
#print axioms OperationalFilterFamily.lift_comp
#print axioms OperationalFilterFamily.lift_irreducible
#print axioms OperationalFilterFamily.product_resets_irreducible_iff
#print axioms OperationalFilterFamily.product_reset_formula
#print axioms OperationalFilterFamily.product_test_pullback
#print axioms OperationalFilterFamily.doubled_reset_kills_hidden
#print axioms OperationalFilterFamily.doubled_protected_reset_no_descent

#print axioms OperationalFilterFamily.admitted_reset_family

#print axioms OperationalFilterFamily.normalized_preparations_span
#print axioms OperationalFilterFamily.normalized_reset_family

#print axioms OperationalFilterFamily.normalization_faithful
