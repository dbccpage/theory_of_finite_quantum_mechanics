import BornGaussianFiniteModel

/-!
# Continuum-Shadow Model and Explicit Bridge for Gleason over `ℚ(i)³`

AuthorityEffect: None.

This module formalizes Phase 3 of the Gleason campaign: the explicit continuum-shadow model and the
bridge between finite rational ray/frame observations and continuum Born-rule claims on `ℂ³`.

## Main Components and Crosswalk to the `FOC / MUR / CS / CS_Q / Q / A / OR / FDA` Spine

1. **Abstract Continuum-Shadow Observation & Descent (`FOC`, `MUR`, `CS`)**
   * `ObservationProfile`: finite or stage-indexed observation map `p : X → Obs`.
   * `FibreConstant` and `FactorsThroughOnRange`: exact descent of a query `q : X → Val` to the
     realized observation image `Set.range p` (`fibreConstant_iff_factorsThroughOnRange`,
     `descendOnRange`, `descendOnRange_spec`, `descendOnRange_unique`).
   * `extendFromRange_nonunique_outside_range`: explicit separation between canonical uniqueness on
     the realized observation image `Set.range p` and non-uniqueness of total extensions `Obs → Val`
     on unrealized observation labels `o₀ ∉ Set.range p`.

2. **Approximate Decoder Collision Bounds & Pseudometric Separation (`CS_Q`, `Q`)**
   * `ApproxDecodes p q D ε`: uniform `ε`-decoding `|q x - D (p x)| ≤ ε`.
   * `approxDecodes_query_diff_le`: `|q x - q y| ≤ |D (p x) - D (p y)| + 2 * ε`.
   * `approxDecodes_collision_bound`: observation collision `p x = p y` forces `|q x - q y| ≤ 2 * ε`.
   * `approxDecodes_ne_of_gap_gt_two_eps`: a query gap `|q x - q y| > 2 * ε` forces distinct finite
     observations `p x ≠ p y`.
   * `profileL1Dist`: exact rational `ℓ¹` pseudometric on finite vector-valued observation profiles,
     with `profileL1Dist_eq_zero_iff : profileL1Dist p x y = 0 ↔ p x = p y` and
     `profileL1Dist_zero_not_eq_of_collision` separating zero profile pseudometric distance from
     state or off-support query equality.

3. **Directed Stage Refinement Compatibility (`FOC`, `CS`, `FDA`)**
   * `stageRayProfile` and `stageRefinement`: restriction along finite ray-subset inclusions
     `S ⊆ T`, satisfying `stageRefinement_stageRayProfile` and `stageRefinement_trans`, with
     monotonicity of exact descent (`fibreConstant_mono_stage`).

4. **Nine-Ray Tomography Shadow, Restricted Exact Factorization, and Nonquadratic Aliasing (`CS`, `CS_Q`, `Q`)**
   * `anchorRay`, `nineRayProfile`, and `decodeNineRayProfile`: the 9-ray tomography profile map and
     its linear Hermitian-form decoder ` (Fin 9 → ℚ) → HermForm3`.
   * `nineRayProfile_quadRay_tomographyForm` and `nineRayProfile_quadRay_decode`: exact section
     property showing that `nineRayProfile ∘ quadRay ∘ decodeNineRayProfile = id` on all profiles
     `Fin 9 → ℚ` and that `quadRay (tomographyForm f)` matches `f` on all 9 anchor rays for every
     `f : GVec → ℚ`.
   * `IsQuadraticRayFunction`, `IsNormalizedQuadraticRayFunction`,
     `quadratic_ray_eq_decodeNineRayProfile`, and `quadratic_fibreConstant_nineRayProfile`: exact
     factorization and uniqueness on the restricted quadratic state class.
   * `exoticQi3_aliases_maximallyMixed_on_witness_111` and `s3_aliases_zero_on_witness_111`:
     explicit nonquadratic frame-function aliasing witnesses with `profileL1Dist = 0` on
     `nineRayProfile` that diverge at `witness_111 = (1, 1, 1)`.

5. **Quantitative Stability of Nine-Ray Tomography (`CS_Q`, `Q`, `A`)**
   * `NineRayClose f g ε`: anchorwise `ℓ^∞` perturbation hypothesis `|f (anchorRay i) - g (anchorRay i)| ≤ ε`.
   * `tomography_diag_error_le`, `tomography_offdiag_error_le`, `tomography_coeffNorm_sub_le`:
     entrywise bounds `≤ ε` (diagonal) and `≤ 2 * ε` (off-diagonal), summing to
     `(subForm (tomographyForm f) (tomographyForm g)).coeffNorm ≤ 27 * ε`.
   * `tomography_quadRay_error_le`: uniform ray-probability stability
     `|quadRay (tomographyForm f) v - quadRay (tomographyForm g) v| ≤ 27 * ε` on all nonzero
     `v ∈ ℚ(i)³`.
   * `tomography_trace_error_le`: trace stability `|(tomographyForm f).tr - (tomographyForm g).tr| ≤ 3 * ε`.
   * `tomography_approx_nonneg_of_nineRayClose`: approximate positivity lower bound `≥ -27 * ε`.
   * `nineRayClose_trans` and `tomography_quadRay_error_trans`: additive error accumulation across
     composed observation stages.

6. **Quantitative Rayleigh-Quotient Continuity & Constructive Rational Modulus (`A`, `OR`, `FDA`)**
   * `abs_Qc_le_coeffNorm_mul_nsq`: `|Qc ρ v| ≤ (ρ.coeffNorm : ℝ) * nsq v` for all `v ∈ ℂ³` by
     topological density of `ι : ℚ(i)³ → ℂ³`.
   * `sq_Qc_sub_le` and `abs_Qc_sub_le`: exact Hermitian polarization difference bound
     `(Qc ρ x - Qc ρ y)² ≤ (ρ.coeffNorm : ℝ)² * nsq (x - y) * nsq (x + y)` for all `x, y ∈ ℂ³`.
   * `sq_quadRay_sub_le`, `sq_quadRay_sub_le_eight`, and `abs_quadRay_sub_le_sqrt`: quantitative
     projective Rayleigh-quotient continuity
     `(quadRay ρ u - quadRay ρ v)² ≤ 4 * ρ.coeffNorm² * raySinSq u v ≤ 8 * ρ.coeffNorm² * raySinSq u v`
     and `|(quadRay ρ u : ℝ) - (quadRay ρ v : ℝ)| ≤ 2 * (ρ.coeffNorm : ℝ) * √(raySinSq u v)`.
   * `rationalRayModulus B ε := if B ≤ 0 then 1 else ε² / (8 * B²)`: explicit rational uniform
     continuity modulus Handling degenerate `B ≤ 0` and `ρ.coeffNorm = 0` cases, yielding a purely
     algebraic proof `isUniformlyRayContinuous_quadRay_constructive` of `IsUniformlyRayContinuous (quadRay ρ)`.
-/

namespace BornFinite.ContinuumShadow

open BornFinite BornFinite.GaussRat BornFinite.GaussianFrames BornFinite.GaussianTomography
open BornFinite.GleasonBridge BornFinite.BornCompletion BornFinite.GaussianFiniteModel
open GleasonComplex Complex ComplexConjugate Matrix
open scoped BigOperators

/-! ### 1. Abstract Continuum-Shadow Observation & Descent (`FOC`, `MUR`, `CS`) -/

/-- A finite or stage-indexed observation profile map from carrier `X` to observation space `Obs`. -/
abbrev ObservationProfile (X Obs : Type*) := X → Obs

/-- A query `q : X → Val` is fibre-constant over an observation profile `p : X → Obs` when equal
observations force equal query values. -/
def FibreConstant {X Obs Val : Type*} (p : X → Obs) (q : X → Val) : Prop :=
  ∀ x y : X, p x = p y → q x = q y

/-- A query `q : X → Val` factors through the realized observation image `Set.range p` when there
exists a decoder `D : Set.range p → Val` such that `q x = D ⟨p x, ⟨x, rfl⟩⟩` for all `x`. -/
def FactorsThroughOnRange {X Obs Val : Type*} (p : X → Obs) (q : X → Val) : Prop :=
  ∃ D : Set.range p → Val, ∀ x : X, q x = D ⟨p x, ⟨x, rfl⟩⟩

/-- A query `q : X → Val` factors through the ambient observation type `Obs` when there exists a
total decoder `D : Obs → Val` such that `q x = D (p x)` for all `x`. -/
def FactorsThroughTotal {X Obs Val : Type*} (p : X → Obs) (q : X → Val) : Prop :=
  ∃ D : Obs → Val, ∀ x : X, q x = D (p x)

/-- Canonical descent of a query `q : X → Val` to the realized observation image `Set.range p`. -/
noncomputable def descendOnRange {X Obs Val : Type*} (p : X → Obs) (q : X → Val)
    (y : Set.range p) : Val :=
  q y.2.choose

/-- When `q` is fibre-constant over `p`, `descendOnRange p q` reproduces `q` on every state `x`. -/
theorem descendOnRange_spec {X Obs Val : Type*} {p : X → Obs} {q : X → Val}
    (h : FibreConstant p q) (x : X) :
    descendOnRange p q ⟨p x, ⟨x, rfl⟩⟩ = q x := by
  unfold descendOnRange
  have hx : p (⟨p x, ⟨x, rfl⟩⟩ : Set.range p).2.choose = p x :=
    (⟨p x, ⟨x, rfl⟩⟩ : Set.range p).2.choose_spec
  exact h _ x hx

/-- Any two decoders on the realized observation image `Set.range p` that factor `q` are equal. -/
theorem descendOnRange_unique {X Obs Val : Type*} {p : X → Obs} {q : X → Val}
    (D₁ D₂ : Set.range p → Val)
    (h₁ : ∀ x : X, q x = D₁ ⟨p x, ⟨x, rfl⟩⟩)
    (h₂ : ∀ x : X, q x = D₂ ⟨p x, ⟨x, rfl⟩⟩) :
    D₁ = D₂ := by
  funext ⟨o, x, hox⟩
  subst hox
  rw [← h₁ x, ← h₂ x]

/-- Exact descent characterization on the realized image: `q` is fibre-constant over `p` if and only
if `q` factors through `Set.range p`. -/
theorem fibreConstant_iff_factorsThroughOnRange {X Obs Val : Type*}
    (p : X → Obs) (q : X → Val) :
    FibreConstant p q ↔ FactorsThroughOnRange p q := by
  constructor
  · intro h
    exact ⟨descendOnRange p q, fun x => (descendOnRange_spec h x).symm⟩
  · rintro ⟨D, hD⟩ x y hxy
    have hsub : (⟨p x, ⟨x, rfl⟩⟩ : Set.range p) = ⟨p y, ⟨y, rfl⟩⟩ :=
      Subtype.ext hxy
    rw [hD x, hD y, hsub]

/-- Total factorization through `Obs` implies factorization on `Set.range p`. -/
theorem factorsThroughOnRange_of_factorsThroughTotal {X Obs Val : Type*}
    {p : X → Obs} {q : X → Val} (h : FactorsThroughTotal p q) :
    FactorsThroughOnRange p q := by
  rcases h with ⟨D, hD⟩
  exact ⟨fun y => D y.1, fun x => hD x⟩

/-- Explicit separation between canonical descent on `Set.range p` and extension to all of `Obs`:
whenever an observation label `o₀ : Obs` is outside `Set.range p` and `v₁ ≠ v₂`, there exist two
distinct total decoders `D₁ ≠ D₂ : Obs → Val` that both factor `q` on all of `X`. -/
theorem extendFromRange_nonunique_outside_range {X Obs Val : Type*} [DecidableEq Obs]
    (p : X → Obs) (q : X → Val) (D : Obs → Val) (hD : ∀ x : X, q x = D (p x))
    {o₀ : Obs} (ho₀ : o₀ ∉ Set.range p) {v₁ v₂ : Val} (hv : v₁ ≠ v₂) :
    ∃ D₁ D₂ : Obs → Val,
      (∀ x : X, q x = D₁ (p x)) ∧
      (∀ x : X, q x = D₂ (p x)) ∧
      D₁ o₀ = v₁ ∧ D₂ o₀ = v₂ ∧ D₁ ≠ D₂ := by
  let D₁ : Obs → Val := fun o => if o = o₀ then v₁ else D o
  let D₂ : Obs → Val := fun o => if o = o₀ then v₂ else D o
  refine ⟨D₁, D₂, ?_, ?_, ?_, ?_, ?_⟩
  · intro x
    have hne : p x ≠ o₀ := fun h => ho₀ ⟨x, h⟩
    simp [D₁, hne, hD x]
  · intro x
    have hne : p x ≠ o₀ := fun h => ho₀ ⟨x, h⟩
    simp [D₂, hne, hD x]
  · simp [D₁]
  · simp [D₂]
  · intro h12
    have hval : D₁ o₀ = D₂ o₀ := congrFun h12 o₀
    simp [D₁, D₂] at hval
    exact hv hval

/-! ### 2. Approximate Decoder Collision Bounds & Pseudometric Separation (`CS_Q`, `Q`) -/

/-- A decoder `D : Obs → ℚ` approximately decodes query `q : X → ℚ` from profile `p : X → Obs`
within uniform error `ε` when `|q x - D (p x)| ≤ ε` for every `x : X`. -/
def ApproxDecodes {X Obs : Type*} (p : X → Obs) (q : X → ℚ) (D : Obs → ℚ) (ε : ℚ) : Prop :=
  ∀ x : X, |q x - D (p x)| ≤ ε

/-- Quantitative query difference bound under `ε`-decoding:
`|q x - q y| ≤ |D (p x) - D (p y)| + 2 * ε`. -/
theorem approxDecodes_query_diff_le {X Obs : Type*} {p : X → Obs} {q : X → ℚ}
    {D : Obs → ℚ} {ε : ℚ} (h : ApproxDecodes p q D ε) (x y : X) :
    |q x - q y| ≤ |D (p x) - D (p y)| + 2 * ε := by
  have hx := h x
  have hy := h y
  have hrew : q x - q y = (q x - D (p x)) + (D (p x) - D (p y)) + (D (p y) - q y) := by ring
  have h1 := abs_add_le ((q x - D (p x)) + (D (p x) - D (p y))) (D (p y) - q y)
  have h2 := abs_add_le (q x - D (p x)) (D (p x) - D (p y))
  have h3 : |D (p y) - q y| = |q y - D (p y)| := abs_sub_comm _ _
  rw [hrew]
  linarith

/-- Approximate decoder collision bound: if two states `x, y` produce the same finite observation
profile `p x = p y`, any `ε`-decoder forces `|q x - q y| ≤ 2 * ε`. -/
theorem approxDecodes_collision_bound {X Obs : Type*} {p : X → Obs} {q : X → ℚ}
    {D : Obs → ℚ} {ε : ℚ} (h : ApproxDecodes p q D ε) {x y : X} (hp : p x = p y) :
    |q x - q y| ≤ 2 * ε := by
  have hdiff := approxDecodes_query_diff_le h x y
  rw [hp, sub_self, abs_zero, zero_add] at hdiff
  exact hdiff

/-- Contrapositive separation criterion: if `|q x - q y| > 2 * ε`, no `ε`-decoder can exist unless
the finite observation profile separates `x` and `y` (`p x ≠ p y`). -/
theorem approxDecodes_ne_of_gap_gt_two_eps {X Obs : Type*} {p : X → Obs} {q : X → ℚ}
    {D : Obs → ℚ} {ε : ℚ} (h : ApproxDecodes p q D ε) {x y : X}
    (hgap : 2 * ε < |q x - q y|) :
    p x ≠ p y := by
  intro hp
  linarith [approxDecodes_collision_bound h hp]

/-- Exact rational `ℓ¹` pseudometric induced by a finite `k`-component observation profile. -/
def profileL1Dist {X : Type*} {k : ℕ} (p : X → Fin k → ℚ) (x y : X) : ℚ :=
  ∑ i : Fin k, |p x i - p y i|

theorem profileL1Dist_nonneg {X : Type*} {k : ℕ} (p : X → Fin k → ℚ) (x y : X) :
    0 ≤ profileL1Dist p x y :=
  Finset.sum_nonneg fun i _ => abs_nonneg (p x i - p y i)

theorem profileL1Dist_self {X : Type*} {k : ℕ} (p : X → Fin k → ℚ) (x : X) :
    profileL1Dist p x x = 0 := by
  simp [profileL1Dist]

theorem profileL1Dist_comm {X : Type*} {k : ℕ} (p : X → Fin k → ℚ) (x y : X) :
    profileL1Dist p x y = profileL1Dist p y x := by
  unfold profileL1Dist
  refine Finset.sum_congr rfl fun i _ => abs_sub_comm (p x i) (p y i)

theorem profileL1Dist_triangle {X : Type*} {k : ℕ} (p : X → Fin k → ℚ) (x y z : X) :
    profileL1Dist p x z ≤ profileL1Dist p x y + profileL1Dist p y z := by
  unfold profileL1Dist
  rw [← Finset.sum_add_distrib]
  refine Finset.sum_le_sum fun i _ => ?_
  have hrew : p x i - p z i = (p x i - p y i) + (p y i - p z i) := by ring
  rw [hrew]
  exact abs_add_le _ _

/-- Zero `ℓ¹` profile distance is equivalent to observation-profile equality `p x = p y`, not
carrier equality `x = y`. -/
theorem profileL1Dist_eq_zero_iff {X : Type*} {k : ℕ} (p : X → Fin k → ℚ) (x y : X) :
    profileL1Dist p x y = 0 ↔ p x = p y := by
  unfold profileL1Dist
  rw [Finset.sum_eq_zero_iff_of_nonneg (fun i _ => abs_nonneg (p x i - p y i))]
  constructor
  · intro h
    funext i
    exact sub_eq_zero.mp (abs_eq_zero.mp (h i (Finset.mem_univ i)))
  · intro h i _
    rw [h, sub_self, abs_zero]

/-- Explicit pseudometric vs. metric separation: when `p x = p y` but `q x ≠ q y`, the observation
pseudometric distance `profileL1Dist p x y` is `0` even though `q x ≠ q y` and `x ≠ y`. -/
theorem profileL1Dist_zero_not_eq_of_collision {X : Type*} {k : ℕ}
    (p : X → Fin k → ℚ) (q : X → ℚ) {x y : X}
    (hp : p x = p y) (hq : q x ≠ q y) :
    profileL1Dist p x y = 0 ∧ q x ≠ q y ∧ x ≠ y := by
  refine ⟨(profileL1Dist_eq_zero_iff p x y).mpr hp, hq, ?_⟩
  intro hxy
  exact hq (congrArg q hxy)

/-! ### 3. Directed Stage Refinement & Observation Compatibility (`FOC`, `CS`, `FDA`) -/

/-- Finite stage observation profile restricting `f : GVec → ℚ` to a finite ray subset `S`. -/
def stageRayProfile (S : Finset GVec) (f : GVec → ℚ) : S → ℚ :=
  fun v => f v.1

/-- Canonical restriction map between finite observation stages `S ⊆ T`. -/
def stageRefinement {S T : Finset GVec} (hST : S ⊆ T) (pT : T → ℚ) : S → ℚ :=
  fun v => pT ⟨v.1, hST v.2⟩

/-- Stage refinement commutes strictly with stage observation profiles (`p_S = r_{S,T} ∘ p_T`). -/
theorem stageRefinement_stageRayProfile {S T : Finset GVec} (hST : S ⊆ T) (f : GVec → ℚ) :
    stageRefinement hST (stageRayProfile T f) = stageRayProfile S f :=
  rfl

/-- Functorial transitivity of stage refinement along `R ⊆ S ⊆ T`. -/
theorem stageRefinement_trans {R S T : Finset GVec} (hRS : R ⊆ S) (hST : S ⊆ T) (pT : T → ℚ) :
    stageRefinement hRS (stageRefinement hST pT) = stageRefinement (hRS.trans hST) pT :=
  rfl

/-- If a query `q` is fibre-constant at a coarser stage `S`, it remains fibre-constant at any finer
stage `T ⊇ S`. -/
theorem fibreConstant_mono_stage {S T : Finset GVec} (hST : S ⊆ T)
    {q : (GVec → ℚ) → ℚ} (hS : FibreConstant (stageRayProfile S) q) :
    FibreConstant (stageRayProfile T) q := by
  intro f g hT
  apply hS
  rw [← stageRefinement_stageRayProfile hST f, ← stageRefinement_stageRayProfile hST g, hT]

/-! ### 4. Nine-Ray Tomography Shadow, Restricted Exact Factorization, and Nonquadratic Aliasing -/

/-- Enumeration of the 9 Gaussian-rational tomography anchor vectors in `ℚ(i)³`. -/
def anchorRay : Fin 9 → GVec
  | ⟨0, _⟩ => tomo_e1
  | ⟨1, _⟩ => tomo_e2
  | ⟨2, _⟩ => tomo_e3
  | ⟨3, _⟩ => tomo_e12
  | ⟨4, _⟩ => tomo_e13
  | ⟨5, _⟩ => tomo_e23
  | ⟨6, _⟩ => tomo_e12i
  | ⟨7, _⟩ => tomo_e13i
  | ⟨8, _⟩ => tomo_e23i

/-- Every tomography anchor vector in `anchorRay` is nonzero. -/
theorem anchorRay_nonZero (i : Fin 9) : (anchorRay i).NonZero := by
  fin_cases i
  · exact tomo_e1_nonZero
  · exact tomo_e2_nonZero
  · exact tomo_e3_nonZero
  · exact tomo_e12_nonZero
  · exact tomo_e13_nonZero
  · exact tomo_e23_nonZero
  · exact tomo_e12i_nonZero
  · exact tomo_e13i_nonZero
  · exact tomo_e23i_nonZero

/-- The 9-ray tomography observation profile `Fin 9 → ℚ` of a ray function `f : GVec → ℚ`. -/
def nineRayProfile (f : GVec → ℚ) : Fin 9 → ℚ :=
  fun i => f (anchorRay i)

/-- Explicit linear decoder reconstructing a `3 × 3` rational Hermitian form from a 9-ray profile. -/
def decodeNineRayProfile (p : Fin 9 → ℚ) : HermForm3 where
  d1 := p 0
  d2 := p 1
  d3 := p 2
  a12 := p 3 - (p 0 + p 1) / 2
  a13 := p 4 - (p 0 + p 2) / 2
  a23 := p 5 - (p 1 + p 2) / 2
  b12 := (p 0 + p 1) / 2 - p 6
  b13 := (p 0 + p 2) / 2 - p 7
  b23 := (p 1 + p 2) / 2 - p 8

/-- Decoding the 9-ray profile of `f` produces `tomographyForm f`. -/
theorem decodeNineRayProfile_nineRayProfile (f : GVec → ℚ) :
    decodeNineRayProfile (nineRayProfile f) = tomographyForm f :=
  rfl

/-- `tomographyForm f` depends only on `nineRayProfile f`. -/
theorem tomographyForm_eq_of_nineRayProfile_eq {f g : GVec → ℚ}
    (h : nineRayProfile f = nineRayProfile g) :
    tomographyForm f = tomographyForm g := by
  rw [← decodeNineRayProfile_nineRayProfile f, ← decodeNineRayProfile_nineRayProfile g, h]

/-- Exact section property on all functions `f : GVec → ℚ`: the Rayleigh quotient of
`tomographyForm f` has the exact same 9-ray profile as `f`. -/
theorem nineRayProfile_quadRay_tomographyForm (f : GVec → ℚ) :
    nineRayProfile (quadRay (tomographyForm f)) = nineRayProfile f := by
  have hm := tomography_matches_nine_rays f
  funext i
  fin_cases i
  · exact hm.1
  · exact hm.2.1
  · exact hm.2.2.1
  · exact hm.2.2.2.1
  · exact hm.2.2.2.2.1
  · exact hm.2.2.2.2.2.1
  · exact hm.2.2.2.2.2.2.1
  · exact hm.2.2.2.2.2.2.2.1
  · exact hm.2.2.2.2.2.2.2.2

/-- Every profile `p : Fin 9 → ℚ` is realized by the Rayleigh quotient of `decodeNineRayProfile p`
(`nineRayProfile` is surjective onto `Fin 9 → ℚ` with right inverse `quadRay ∘ decodeNineRayProfile`). -/
theorem nineRayProfile_quadRay_decode (p : Fin 9 → ℚ) :
    nineRayProfile (quadRay (decodeNineRayProfile p)) = p := by
  funext i
  fin_cases i <;>
    simp [nineRayProfile, anchorRay, decodeNineRayProfile,
      quadRay_tomo_e1, quadRay_tomo_e2, quadRay_tomo_e3,
      quadRay_tomo_e12, quadRay_tomo_e13, quadRay_tomo_e23,
      quadRay_tomo_e12i, quadRay_tomo_e13i, quadRay_tomo_e23i] <;>
    ring

/-- Left-inverse property on `HermForm3`: decoding the 9-ray profile of `quadRay ρ` recovers `ρ`. -/
theorem decodeNineRayProfile_quadRay (ρ : HermForm3) :
    decodeNineRayProfile (nineRayProfile (quadRay ρ)) = ρ := by
  rw [decodeNineRayProfile_nineRayProfile, tomographyForm_quadRay]

/-- A ray function `f : GVec → ℚ` belongs to the restricted quadratic state class when it agrees on
all nonzero vectors with `quadRay ρ` for some `ρ : HermForm3`. -/
def IsQuadraticRayFunction (f : GVec → ℚ) : Prop :=
  ∃ ρ : HermForm3, ∀ v : GVec, v.NonZero → f v = quadRay ρ v

/-- A ray function `f : GVec → ℚ` belongs to the normalized quadratic state class when it agrees on
all nonzero vectors with `quadRay ρ` for some trace-one `ρ : HermForm3`. -/
def IsNormalizedQuadraticRayFunction (f : GVec → ℚ) : Prop :=
  ∃ ρ : HermForm3, ρ.tr = 1 ∧ ∀ v : GVec, v.NonZero → f v = quadRay ρ v

/-- If `f` is a quadratic ray function represented by `ρ`, then `decodeNineRayProfile (nineRayProfile f) = ρ`. -/
theorem decodeNineRayProfile_eq_of_isQuadratic {f : GVec → ℚ} {ρ : HermForm3}
    (hρ : ∀ v : GVec, v.NonZero → f v = quadRay ρ v) :
    decodeNineRayProfile (nineRayProfile f) = ρ := by
  have hp : nineRayProfile f = nineRayProfile (quadRay ρ) := by
    funext i
    exact hρ (anchorRay i) (anchorRay_nonZero i)
  rw [hp, decodeNineRayProfile_quadRay]

/-- Restricted exact factorization theorem: for any `f` in the quadratic ray class, `f v` on every
nonzero ray `v ∈ ℚ(i)³` is uniquely determined by and factors through `nineRayProfile f`. -/
theorem quadratic_ray_eq_decodeNineRayProfile {f : GVec → ℚ}
    (hf : IsQuadraticRayFunction f) {v : GVec} (hv : v.NonZero) :
    f v = quadRay (decodeNineRayProfile (nineRayProfile f)) v := by
  rcases hf with ⟨ρ, hρ⟩
  rw [decodeNineRayProfile_eq_of_isQuadratic hρ, hρ v hv]

/-- Fibre constancy on the restricted quadratic state class: two quadratic ray functions with the
same 9-ray profile agree on every nonzero ray in `ℚ(i)³`. -/
theorem quadratic_fibreConstant_nineRayProfile {v : GVec} (hv : v.NonZero)
    {f g : GVec → ℚ} (hf : IsQuadraticRayFunction f) (hg : IsQuadraticRayFunction g)
    (hp : nineRayProfile f = nineRayProfile g) :
    f v = g v := by
  rw [quadratic_ray_eq_decodeNineRayProfile hf hv,
      quadratic_ray_eq_decodeNineRayProfile hg hv, hp]

/-- The maximally mixed `3 × 3` rational Hermitian form `(1/3) I₃`. -/
def maximallyMixedForm3 : HermForm3 where
  d1 := 1 / 3
  d2 := 1 / 3
  d3 := 1 / 3
  a12 := 0
  a13 := 0
  a23 := 0
  b12 := 0
  b13 := 0
  b23 := 0

theorem maximallyMixedForm3_tr : maximallyMixedForm3.tr = 1 := by
  unfold HermForm3.tr maximallyMixedForm3
  norm_num

theorem quadRay_maximallyMixedForm3 {v : GVec} (hv : v.NonZero) :
    quadRay maximallyMixedForm3 v = 1 / 3 := by
  have hpos := normSqVec_ne_zero_of_nonZero hv
  have hnum : quadNum maximallyMixedForm3 v = (1 / 3) * normSqVec v := by
    simp only [quadNum, normSqVec, maximallyMixedForm3]
    ring
  rw [quadRay, hnum, mul_div_cancel_right₀ (1 / 3) hpos]

/-- `VanishesOnNineRays g` is equivalent to `nineRayProfile g = 0`. -/
theorem vanishesOnNineRays_iff_nineRayProfile_eq_zero (g : GVec → ℚ) :
    VanishesOnNineRays g ↔ nineRayProfile g = 0 := by
  constructor
  · intro h
    funext i
    fin_cases i
    · exact h.1
    · exact h.2.1
    · exact h.2.2.1
    · exact h.2.2.2.1
    · exact h.2.2.2.2.1
    · exact h.2.2.2.2.2.1
    · exact h.2.2.2.2.2.2.1
    · exact h.2.2.2.2.2.2.2.1
    · exact h.2.2.2.2.2.2.2.2
  · intro h
    exact ⟨congrFun h 0, congrFun h 1, congrFun h 2, congrFun h 3, congrFun h 4,
           congrFun h 5, congrFun h 6, congrFun h 7, congrFun h 8⟩

/-- The zero-weight 3-adic frame function `s3` has identically zero 9-ray profile. -/
theorem nineRayProfile_s3_eq_zero : nineRayProfile s3 = 0 :=
  (vanishesOnNineRays_iff_nineRayProfile_eq_zero s3).mp s3_vanishes_on_nine_rays

/-- Explicit signed aliasing witness: `s3` and the zero function `0` have `profileL1Dist = 0` on
`nineRayProfile`, yet `s3 witness_111 = 1 ≠ 0`. -/
theorem s3_aliases_zero_on_witness_111 :
    nineRayProfile s3 = nineRayProfile (fun _ => 0) ∧
    profileL1Dist nineRayProfile s3 (fun _ => 0) = 0 ∧
    s3 witness_111 = 1 ∧
    s3 witness_111 ≠ (fun _ : GVec => (0 : ℚ)) witness_111 := by
  have hp : nineRayProfile s3 = nineRayProfile (fun _ => 0) := nineRayProfile_s3_eq_zero
  refine ⟨hp, (profileL1Dist_eq_zero_iff nineRayProfile s3 (fun _ => 0)).mpr hp,
    s3_witness_111, by rw [s3_witness_111]; norm_num⟩

theorem exoticQi3_witness_111_eq_two_thirds : exoticQi3 witness_111 = 2 / 3 := by
  simp only [exoticQi3, s3_witness_111]
  norm_num

/-- The nonnegative frame function `exoticQi3` has the exact same 9-ray profile as the maximally
mixed Born state `quadRay maximallyMixedForm3`. -/
theorem nineRayProfile_exoticQi3_eq_maximallyMixed :
    nineRayProfile exoticQi3 = nineRayProfile (quadRay maximallyMixedForm3) := by
  funext i
  simp only [nineRayProfile, exoticQi3]
  have hs3 : s3 (anchorRay i) = 0 := congrFun nineRayProfile_s3_eq_zero i
  have hmax : quadRay maximallyMixedForm3 (anchorRay i) = 1 / 3 :=
    quadRay_maximallyMixedForm3 (anchorRay_nonZero i)
  rw [hs3, hmax]
  ring

/-- Explicit nonnegative aliasing witness: `exoticQi3` is a `[0, 1]`-valued frame function whose
9-ray profile coincides with `quadRay maximallyMixedForm3` (`profileL1Dist = 0`), while on
`witness_111 = (1, 1, 1)` it evaluates to `2 / 3 ≠ 1 / 3`. -/
theorem exoticQi3_aliases_maximallyMixed_on_witness_111 :
    IsNonnegFrameFunction exoticQi3 ∧
    nineRayProfile exoticQi3 = nineRayProfile (quadRay maximallyMixedForm3) ∧
    profileL1Dist nineRayProfile exoticQi3 (quadRay maximallyMixedForm3) = 0 ∧
    exoticQi3 witness_111 = 2 / 3 ∧
    quadRay maximallyMixedForm3 witness_111 = 1 / 3 ∧
    exoticQi3 witness_111 ≠ quadRay maximallyMixedForm3 witness_111 := by
  have hp := nineRayProfile_exoticQi3_eq_maximallyMixed
  have hw := quadRay_maximallyMixedForm3 witness_111_nonZero
  refine ⟨exoticQi3_isNonnegFrameFunction, hp,
    (profileL1Dist_eq_zero_iff nineRayProfile exoticQi3 (quadRay maximallyMixedForm3)).mpr hp,
    exoticQi3_witness_111_eq_two_thirds, hw, ?_⟩
  rw [exoticQi3_witness_111_eq_two_thirds, hw]
  norm_num

/-! ### 5. Quantitative Stability of Nine-Ray Tomography (`CS_Q`, `Q`, `A`) -/

/-- Two ray functions `f, g : GVec → ℚ` are `ε`-close on the 9 tomography anchors when
`|f (anchorRay i) - g (anchorRay i)| ≤ ε` for all `i : Fin 9`. -/
def NineRayClose (f g : GVec → ℚ) (ε : ℚ) : Prop :=
  ∀ i : Fin 9, |f (anchorRay i) - g (anchorRay i)| ≤ ε

/-- Entrywise difference of two `3 × 3` rational Hermitian forms. -/
def subForm (ρ σ : HermForm3) : HermForm3 where
  d1 := ρ.d1 - σ.d1
  d2 := ρ.d2 - σ.d2
  d3 := ρ.d3 - σ.d3
  a12 := ρ.a12 - σ.a12
  a13 := ρ.a13 - σ.a13
  a23 := ρ.a23 - σ.a23
  b12 := ρ.b12 - σ.b12
  b13 := ρ.b13 - σ.b13
  b23 := ρ.b23 - σ.b23

theorem quadNum_subForm (ρ σ : HermForm3) (v : GVec) :
    quadNum (subForm ρ σ) v = quadNum ρ v - quadNum σ v := by
  simp only [quadNum, subForm]
  ring

theorem quadRay_subForm (ρ σ : HermForm3) (v : GVec) :
    quadRay (subForm ρ σ) v = quadRay ρ v - quadRay σ v := by
  simp only [quadRay, quadNum_subForm, sub_div]

theorem tr_subForm (ρ σ : HermForm3) :
    (subForm ρ σ).tr = ρ.tr - σ.tr := by
  simp only [HermForm3.tr, subForm]
  ring

/-- Diagonal coefficient stability of 9-ray tomography: `|Δ.d_i| ≤ ε`. -/
theorem tomography_diag_error_le {f g : GVec → ℚ} {ε : ℚ} (h : NineRayClose f g ε) :
    |(tomographyForm f).d1 - (tomographyForm g).d1| ≤ ε ∧
    |(tomographyForm f).d2 - (tomographyForm g).d2| ≤ ε ∧
    |(tomographyForm f).d3 - (tomographyForm g).d3| ≤ ε :=
  ⟨h 0, h 1, h 2⟩

private lemma offdiag_a_bound {x1 x2 x12 y1 y2 y12 ε : ℚ}
    (h1 : |x1 - y1| ≤ ε) (h2 : |x2 - y2| ≤ ε) (h12 : |x12 - y12| ≤ ε) :
    |(x12 - (x1 + x2) / 2) - (y12 - (y1 + y2) / 2)| ≤ 2 * ε := by
  rcases abs_le.mp h1 with ⟨h1l, h1u⟩
  rcases abs_le.mp h2 with ⟨h2l, h2u⟩
  rcases abs_le.mp h12 with ⟨h12l, h12u⟩
  exact abs_le.mpr ⟨by linarith, by linarith⟩

private lemma offdiag_b_bound {x1 x2 x12i y1 y2 y12i ε : ℚ}
    (h1 : |x1 - y1| ≤ ε) (h2 : |x2 - y2| ≤ ε) (h12i : |x12i - y12i| ≤ ε) :
    |((x1 + x2) / 2 - x12i) - ((y1 + y2) / 2 - y12i)| ≤ 2 * ε := by
  rcases abs_le.mp h1 with ⟨h1l, h1u⟩
  rcases abs_le.mp h2 with ⟨h2l, h2u⟩
  rcases abs_le.mp h12i with ⟨h12il, h12iu⟩
  exact abs_le.mpr ⟨by linarith, by linarith⟩

/-- Off-diagonal coefficient stability of 9-ray tomography: `|Δ.a_ij| ≤ 2 * ε` and `|Δ.b_ij| ≤ 2 * ε`. -/
theorem tomography_offdiag_error_le {f g : GVec → ℚ} {ε : ℚ} (h : NineRayClose f g ε) :
    |(tomographyForm f).a12 - (tomographyForm g).a12| ≤ 2 * ε ∧
    |(tomographyForm f).a13 - (tomographyForm g).a13| ≤ 2 * ε ∧
    |(tomographyForm f).a23 - (tomographyForm g).a23| ≤ 2 * ε ∧
    |(tomographyForm f).b12 - (tomographyForm g).b12| ≤ 2 * ε ∧
    |(tomographyForm f).b13 - (tomographyForm g).b13| ≤ 2 * ε ∧
    |(tomographyForm f).b23 - (tomographyForm g).b23| ≤ 2 * ε :=
  ⟨offdiag_a_bound (h 0) (h 1) (h 3),
   offdiag_a_bound (h 0) (h 2) (h 4),
   offdiag_a_bound (h 1) (h 2) (h 5),
   offdiag_b_bound (h 0) (h 1) (h 6),
   offdiag_b_bound (h 0) (h 2) (h 7),
   offdiag_b_bound (h 1) (h 2) (h 8)⟩

/-- Total `coeffNorm` stability of 9-ray tomography:
`(subForm (tomographyForm f) (tomographyForm g)).coeffNorm ≤ 27 * ε`
(`3 * ε` from the three diagonal entries plus `6 * (2 * 2 * ε) = 24 * ε` from the six off-diagonal
components). -/
theorem tomography_coeffNorm_sub_le {f g : GVec → ℚ} {ε : ℚ} (h : NineRayClose f g ε) :
    (subForm (tomographyForm f) (tomographyForm g)).coeffNorm ≤ 27 * ε := by
  obtain ⟨hd1, hd2, hd3⟩ := tomography_diag_error_le h
  obtain ⟨ha12, ha13, ha23, hb12, hb13, hb23⟩ := tomography_offdiag_error_le h
  unfold HermForm3.coeffNorm subForm
  linarith

/-- Quantitative Rayleigh-quotient stability of 9-ray tomography: if `f` and `g` are `ε`-close on
the 9 anchor rays, their reconstructed Rayleigh quotients differ by at most `27 * ε` on every
nonzero ray `v ∈ ℚ(i)³`. -/
theorem tomography_quadRay_error_le {f g : GVec → ℚ} {ε : ℚ} (h : NineRayClose f g ε)
    {v : GVec} (hv : v.NonZero) :
    |quadRay (tomographyForm f) v - quadRay (tomographyForm g) v| ≤ 27 * ε := by
  rw [← quadRay_subForm]
  exact (abs_quadRay_le (subForm (tomographyForm f) (tomographyForm g)) hv).trans
    (tomography_coeffNorm_sub_le h)

/-- Trace stability of 9-ray tomography: `|(tomographyForm f).tr - (tomographyForm g).tr| ≤ 3 * ε`. -/
theorem tomography_trace_error_le {f g : GVec → ℚ} {ε : ℚ} (h : NineRayClose f g ε) :
    |(tomographyForm f).tr - (tomographyForm g).tr| ≤ 3 * ε := by
  obtain ⟨hd1, hd2, hd3⟩ := tomography_diag_error_le h
  rcases abs_le.mp hd1 with ⟨h1l, h1u⟩
  rcases abs_le.mp hd2 with ⟨h2l, h2u⟩
  rcases abs_le.mp hd3 with ⟨h3l, h3u⟩
  unfold HermForm3.tr
  exact abs_le.mpr ⟨by linarith, by linarith⟩

/-- Approximate positivity preservation under `NineRayClose`: if `tomographyForm f` has nonnegative
Rayleigh quotient on all nonzero rays in `ℚ(i)³` and `NineRayClose f g ε`, then
`quadRay (tomographyForm g) v ≥ -27 * ε` on all nonzero rays `v ∈ ℚ(i)³`. -/
theorem tomography_approx_nonneg_of_nineRayClose {f g : GVec → ℚ} {ε : ℚ}
    (h : NineRayClose f g ε)
    (hpos : ∀ v : GVec, v.NonZero → 0 ≤ quadRay (tomographyForm f) v)
    {v : GVec} (hv : v.NonZero) :
    -(27 * ε) ≤ quadRay (tomographyForm g) v := by
  have herr := (abs_le.mp (tomography_quadRay_error_le h hv)).2
  have hf := hpos v hv
  linarith

/-- Additive composition of anchorwise perturbations across intermediate approximation stages. -/
theorem nineRayClose_trans {f g h : GVec → ℚ} {ε₁ ε₂ : ℚ}
    (h₁ : NineRayClose f g ε₁) (h₂ : NineRayClose g h ε₂) :
    NineRayClose f h (ε₁ + ε₂) := by
  intro i
  have hrew : f (anchorRay i) - h (anchorRay i) =
      (f (anchorRay i) - g (anchorRay i)) + (g (anchorRay i) - h (anchorRay i)) := by ring
  rw [hrew]
  exact (abs_add_le _ _).trans (add_le_add (h₁ i) (h₂ i))

/-- Composed Rayleigh-quotient error bound across two approximation stages (`≤ 27 * (ε₁ + ε₂)`). -/
theorem tomography_quadRay_error_trans {f g h : GVec → ℚ} {ε₁ ε₂ : ℚ}
    (h₁ : NineRayClose f g ε₁) (h₂ : NineRayClose g h ε₂)
    {v : GVec} (hv : v.NonZero) :
    |quadRay (tomographyForm f) v - quadRay (tomographyForm h) v| ≤ 27 * (ε₁ + ε₂) :=
  tomography_quadRay_error_le (nineRayClose_trans h₁ h₂) hv

/-! ### 6. Quantitative Rayleigh-Quotient Continuity & Constructive Rational Modulus (`A`, `OR`, `FDA`) -/

noncomputable section

/-- Topological density extension of `abs_quadNum_le`: for every rational Hermitian form `ρ` and
every complex vector `v ∈ ℂ³`, `|Qc ρ v| ≤ (ρ.coeffNorm : ℝ) * nsq v`. -/
theorem abs_Qc_le_coeffNorm_mul_nsq (ρ : HermForm3) (v : Fin 3 → ℂ) :
    |Qc ρ v| ≤ (ρ.coeffNorm : ℝ) * nsq v := by
  refine isClosed_property denseRange_ι
    (isClosed_le (continuous_abs.comp (continuous_Qc ρ))
      (continuous_const.mul continuous_nsq))
    (fun g => ?_) v
  show |Qc ρ (ι g)| ≤ (ρ.coeffNorm : ℝ) * nsq (ι g)
  rw [Qc_ι, nsq_ι]
  exact_mod_cast abs_quadNum_le ρ g

/-- On every nonzero complex vector `v ∈ ℂ³ \ {0}`, `|QcRay ρ v| ≤ (ρ.coeffNorm : ℝ)`. -/
theorem abs_QcRay_le_coeffNorm (ρ : HermForm3) {v : Fin 3 → ℂ} (hv : v ≠ 0) :
    |QcRay ρ v| ≤ (ρ.coeffNorm : ℝ) := by
  have hpos : 0 < nsq v := nsq_pos hv
  rw [QcRay, abs_div, abs_of_pos hpos, div_le_iff₀ hpos]
  exact abs_Qc_le_coeffNorm_mul_nsq ρ v

lemma nsq_add_eq (x y : Fin 3 → ℂ) :
    nsq (x + y) = nsq x + 2 * (dotC x y).re + nsq y := by
  simp only [nsq, dotC, Pi.add_apply, Complex.normSq_apply, Complex.add_re, Complex.add_im,
    Complex.mul_re, Complex.conj_re, Complex.conj_im]
  ring

/-- Parallelogram identity for `nsq` on `ℂ³`. -/
theorem nsq_parallelogram (a b : Fin 3 → ℂ) :
    nsq (a + b) + nsq (a - b) = 2 * nsq a + 2 * nsq b := by
  rw [nsq_add_eq, nsq_sub_eq]
  ring

/-- Real polarization identity for `Qc ρ`:
`Qc ρ (a + b) - Qc ρ (a - b) = 4 * Re ⟨a, toMatrix ρ *ᵥ b⟩`. -/
theorem Qc_add_sub (ρ : HermForm3) (a b : Fin 3 → ℂ) :
    Qc ρ (a + b) - Qc ρ (a - b) = 4 * (dotC a (toMatrix ρ *ᵥ b)).re := by
  have hHer := toMatrix_isHermitian ρ
  have hba : (dotC b (toMatrix ρ *ᵥ a)).re = (dotC a (toMatrix ρ *ᵥ b)).re := by
    rw [dotC_conj_symm (toMatrix ρ *ᵥ a) b, dotC_mulVec_left, hHer.eq, Complex.conj_re]
  unfold Qc
  simp only [Matrix.mulVec_add, Matrix.mulVec_sub, dotC_add_left, dotC_add_right,
    dotC_sub_left, dotC_sub_right, Complex.add_re, Complex.sub_re]
  linarith

/-- Exact difference identity for a Hermitian quadratic form:
`Qc ρ x - Qc ρ y = Re ⟨x - y, toMatrix ρ *ᵥ (x + y)⟩`. -/
theorem Qc_sub_eq_re_dotC_sub_add (ρ : HermForm3) (x y : Fin 3 → ℂ) :
    Qc ρ x - Qc ρ y = (dotC (x - y) (toMatrix ρ *ᵥ (x + y))).re := by
  have hpol := Qc_add_sub ρ (x - y) (x + y)
  have hsum : (x - y) + (x + y) = (2 : ℂ) • x := by ext i; simp; ring
  have hdiff : (x - y) - (x + y) = (-2 : ℂ) • y := by ext i; simp; ring
  have h2 : normSq (2 : ℂ) = 4 := by norm_num [Complex.normSq]
  have hm2 : normSq (-2 : ℂ) = 4 := by norm_num [Complex.normSq]
  rw [hsum, hdiff, Qc_smul, Qc_smul, h2, hm2] at hpol
  linarith

/-- One-parameter scaled polarization inequality for `Qc ρ`: for every real `t : ℝ`,
`4 * t * (Qc ρ x - Qc ρ y) ≤ (ρ.coeffNorm : ℝ) * (2 * t² * nsq (x - y) + 2 * nsq (x + y))`. -/
theorem Qc_scaled_polar_bound (ρ : HermForm3) (x y : Fin 3 → ℂ) (t : ℝ) :
    4 * t * (Qc ρ x - Qc ρ y) ≤
      (ρ.coeffNorm : ℝ) * (2 * t ^ 2 * nsq (x - y) + 2 * nsq (x + y)) := by
  set a : Fin 3 → ℂ := (t : ℂ) • (x - y) with ha_def
  set b : Fin 3 → ℂ := x + y with hb_def
  have hpol := Qc_add_sub ρ a b
  have hsmul : (dotC a (toMatrix ρ *ᵥ b)).re = t * (Qc ρ x - Qc ρ y) := by
    rw [ha_def, hb_def, dotC_smul_left, Complex.conj_ofReal, Complex.re_ofReal_mul,
        ← Qc_sub_eq_re_dotC_sub_add]
  have h4t : 4 * t * (Qc ρ x - Qc ρ y) = Qc ρ (a + b) - Qc ρ (a - b) := by
    linarith
  have hab1 := (le_abs_self (Qc ρ (a + b))).trans (abs_Qc_le_coeffNorm_mul_nsq ρ (a + b))
  have hab2 := (neg_le_abs (Qc ρ (a - b))).trans (abs_Qc_le_coeffNorm_mul_nsq ρ (a - b))
  have hpar := nsq_parallelogram a b
  have hnsqa : nsq a = t ^ 2 * nsq (x - y) := by
    rw [ha_def, nsq_smul, Complex.normSq_ofReal, sq]
  have hpar_mul :
      (ρ.coeffNorm : ℝ) * nsq (a + b) + (ρ.coeffNorm : ℝ) * nsq (a - b) =
        (ρ.coeffNorm : ℝ) * (2 * t ^ 2 * nsq (x - y) + 2 * nsq b) := by
    linear_combination (ρ.coeffNorm : ℝ) * hpar + 2 * (ρ.coeffNorm : ℝ) * hnsqa
  linarith

/-- Squared polarization difference bound on `ℂ³`:
`(Qc ρ x - Qc ρ y)² ≤ (ρ.coeffNorm : ℝ)² * nsq (x - y) * nsq (x + y)`. -/
theorem sq_Qc_sub_le (ρ : HermForm3) (x y : Fin 3 → ℂ) :
    (Qc ρ x - Qc ρ y) ^ 2 ≤ (ρ.coeffNorm : ℝ) ^ 2 * nsq (x - y) * nsq (x + y) := by
  set C : ℝ := (ρ.coeffNorm : ℝ) with hC_def
  set A : ℝ := nsq (x - y) with hA_def
  set B : ℝ := nsq (x + y) with hB_def
  set Δ : ℝ := Qc ρ x - Qc ρ y with hΔ_def
  have hC0 : 0 ≤ C := by rw [hC_def]; exact_mod_cast coeffNorm_nonneg ρ
  have hA0 : 0 ≤ A := nsq_nonneg (x - y)
  by_cases hCA : C * A = 0
  · rcases mul_eq_zero.mp hCA with hC | hA
    · have hx0 : |Qc ρ x| ≤ 0 := by
        have h1 := abs_Qc_le_coeffNorm_mul_nsq ρ x
        rw [← hC_def, hC, zero_mul] at h1
        exact h1
      have hy0 : |Qc ρ y| ≤ 0 := by
        have h1 := abs_Qc_le_coeffNorm_mul_nsq ρ y
        rw [← hC_def, hC, zero_mul] at h1
        exact h1
      have hqx : Qc ρ x = 0 := abs_nonpos_iff.mp hx0
      have hqy : Qc ρ y = 0 := abs_nonpos_iff.mp hy0
      have hΔ : Δ = 0 := by rw [hΔ_def, hqx, hqy, sub_self]
      rw [hΔ, hC]
      norm_num
    · have hxy : x - y = 0 := by
        by_contra hne
        exact (nsq_pos hne).ne' hA
      have hxy_eq : x = y := sub_eq_zero.mp hxy
      have hΔ : Δ = 0 := by rw [hΔ_def, hxy_eq, sub_self]
      rw [hΔ, hA]
      norm_num
  · have hCA_pos : 0 < C * A := lt_of_le_of_ne (mul_nonneg hC0 hA0) (Ne.symm hCA)
    have hC_ne : C ≠ 0 := left_ne_zero_of_mul hCA
    have hA_ne : A ≠ 0 := right_ne_zero_of_mul hCA
    have hbound := Qc_scaled_polar_bound ρ x y (Δ / (C * A))
    rw [← hC_def, ← hA_def, ← hB_def, ← hΔ_def] at hbound
    have hmul := mul_le_mul_of_nonneg_left hbound hCA_pos.le
    have hident1 : C * A * (4 * (Δ / (C * A)) * Δ) = 4 * Δ ^ 2 := by
      field_simp [hC_ne, hA_ne]
    have hident2 : C * A * (C * (2 * (Δ / (C * A)) ^ 2 * A + 2 * B)) =
        2 * Δ ^ 2 + 2 * (C ^ 2 * A * B) := by
      field_simp [hC_ne, hA_ne]
    linarith

/-- Square-root polarization difference bound on `ℂ³`:
`|Qc ρ x - Qc ρ y| ≤ (ρ.coeffNorm : ℝ) * √(nsq (x - y)) * √(nsq (x + y))`. -/
theorem abs_Qc_sub_le (ρ : HermForm3) (x y : Fin 3 → ℂ) :
    |Qc ρ x - Qc ρ y| ≤
      (ρ.coeffNorm : ℝ) * Real.sqrt (nsq (x - y)) * Real.sqrt (nsq (x + y)) := by
  have hC0 : 0 ≤ (ρ.coeffNorm : ℝ) := by exact_mod_cast coeffNorm_nonneg ρ
  have hA0 : 0 ≤ nsq (x - y) := nsq_nonneg (x - y)
  have hB0 : 0 ≤ nsq (x + y) := nsq_nonneg (x + y)
  have hrhs_nonneg : 0 ≤ (ρ.coeffNorm : ℝ) * Real.sqrt (nsq (x - y)) * Real.sqrt (nsq (x + y)) :=
    mul_nonneg (mul_nonneg hC0 (Real.sqrt_nonneg _)) (Real.sqrt_nonneg _)
  have hsq := sq_Qc_sub_le ρ x y
  have hrhs_sq :
      ((ρ.coeffNorm : ℝ) * Real.sqrt (nsq (x - y)) * Real.sqrt (nsq (x + y))) ^ 2 =
        (ρ.coeffNorm : ℝ) ^ 2 * nsq (x - y) * nsq (x + y) := by
    calc ((ρ.coeffNorm : ℝ) * Real.sqrt (nsq (x - y)) * Real.sqrt (nsq (x + y))) ^ 2
        = (ρ.coeffNorm : ℝ) ^ 2 * (Real.sqrt (nsq (x - y)) ^ 2) * (Real.sqrt (nsq (x + y)) ^ 2) := by ring
      _ = (ρ.coeffNorm : ℝ) ^ 2 * nsq (x - y) * nsq (x + y) := by
          rw [Real.sq_sqrt hA0, Real.sq_sqrt hB0]
  rw [← Real.sqrt_sq_eq_abs, ← Real.sqrt_sq hrhs_nonneg, hrhs_sq]
  exact Real.sqrt_le_sqrt hsq

/-- Nonnegativity of `raySinSq u v` for nonzero vectors `u, v ∈ ℚ(i)³` (via Lagrange's cross-product
identity `normSqVec_cross`). -/
theorem raySinSq_nonneg_of_nonZero {u v : GVec} (hu : u.NonZero) (hv : v.NonZero) :
    0 ≤ raySinSq u v := by
  have hnu := normSqVec_pos_of_nonZero hu
  have hnv := normSqVec_pos_of_nonZero hv
  have hcr := normSqVec_nonneg (cross u v)
  rw [normSqVec_cross] at hcr
  unfold raySinSq
  rw [sub_nonneg, div_le_one (mul_pos hnu hnv)]
  linarith

/-- Exact rational squared Rayleigh-quotient continuity bound: for all nonzero `u, v ∈ ℚ(i)³`,
`(quadRay ρ u - quadRay ρ v)² ≤ 4 * ρ.coeffNorm² * raySinSq u v`. -/
theorem sq_quadRay_sub_le (ρ : HermForm3) {u v : GVec} (hu : u.NonZero) (hv : v.NonZero) :
    (quadRay ρ u - quadRay ρ v) ^ 2 ≤ 4 * ρ.coeffNorm ^ 2 * raySinSq u v := by
  have hx : ι u ≠ 0 := ι_ne_zero hu
  have hy : ι v ≠ 0 := ι_ne_zero hv
  set z := dotC (GleasonBridge.normalize (ι u)) (GleasonBridge.normalize (ι v)) with hzdef
  obtain ⟨c, hc1, hcz⟩ := exists_phase z
  have hc0 : c ≠ 0 := Complex.normSq_pos.mp (by rw [hc1]; exact one_pos)
  have hnorm_u : nsq (GleasonBridge.normalize (ι u)) = 1 := nsq_normalize hx
  have hnorm_cv : nsq (c • GleasonBridge.normalize (ι v)) = 1 := by
    rw [nsq_smul, hc1, nsq_normalize hy, mul_one]
  have hz : normSq z = 1 - (raySinSq u v : ℝ) := by
    rw [hzdef, normSq_dotC_normalize hx hy, raySinSq_cast]; ring
  have hzn : normSq z = ‖z‖ ^ 2 := Complex.normSq_eq_norm_sq z
  have hsub : nsq (GleasonBridge.normalize (ι u) - c • GleasonBridge.normalize (ι v)) = 2 - 2 * ‖z‖ := by
    rw [nsq_sub_eq, dotC_smul_right, ← hzdef, hcz, Complex.ofReal_re, hnorm_u, hnorm_cv]
    ring
  have hadd : nsq (GleasonBridge.normalize (ι u) + c • GleasonBridge.normalize (ι v)) = 2 + 2 * ‖z‖ := by
    rw [nsq_add_eq, dotC_smul_right, ← hzdef, hcz, Complex.ofReal_re, hnorm_u, hnorm_cv]
    ring
  have hprod :
      nsq (GleasonBridge.normalize (ι u) - c • GleasonBridge.normalize (ι v)) *
      nsq (GleasonBridge.normalize (ι u) + c • GleasonBridge.normalize (ι v)) =
      4 * (raySinSq u v : ℝ) := by
    rw [hsub, hadd]
    linear_combination -4 * hz + 4 * hzn
  have ha : ((1 / Real.sqrt (nsq (ι u)) : ℝ) : ℂ) ≠ 0 := by
    exact_mod_cast (one_div_pos.mpr (Real.sqrt_pos.mpr (nsq_pos hx))).ne'
  have hb : ((1 / Real.sqrt (nsq (ι v)) : ℝ) : ℂ) ≠ 0 := by
    exact_mod_cast (one_div_pos.mpr (Real.sqrt_pos.mpr (nsq_pos hy))).ne'
  have e1 : Qc ρ (GleasonBridge.normalize (ι u)) = (quadRay ρ u : ℝ) := by
    have h1 : QcRay ρ (GleasonBridge.normalize (ι u)) = (quadRay ρ u : ℝ) := by
      rw [GleasonBridge.normalize, QcRay_smul ρ _ ha, QcRay_ι ρ u]
    rw [QcRay, hnorm_u, div_one] at h1
    exact h1
  have e2 : Qc ρ (c • GleasonBridge.normalize (ι v)) = (quadRay ρ v : ℝ) := by
    have h1 : QcRay ρ (c • GleasonBridge.normalize (ι v)) = (quadRay ρ v : ℝ) := by
      rw [QcRay_smul ρ _ hc0, GleasonBridge.normalize, QcRay_smul ρ _ hb, QcRay_ι ρ v]
    rw [QcRay, hnorm_cv, div_one] at h1
    exact h1
  have hsq := sq_Qc_sub_le ρ (GleasonBridge.normalize (ι u)) (c • GleasonBridge.normalize (ι v))
  rw [e1, e2, mul_assoc, hprod] at hsq
  have hsqR : (((quadRay ρ u - quadRay ρ v) ^ 2 : ℚ) : ℝ) ≤
      ((4 * ρ.coeffNorm ^ 2 * raySinSq u v : ℚ) : ℝ) := by
    push_cast
    linarith
  exact_mod_cast hsqR

/-- Consequence with factor `8`: `(quadRay ρ u - quadRay ρ v)² ≤ 8 * ρ.coeffNorm² * raySinSq u v`. -/
theorem sq_quadRay_sub_le_eight (ρ : HermForm3) {u v : GVec} (hu : u.NonZero) (hv : v.NonZero) :
    (quadRay ρ u - quadRay ρ v) ^ 2 ≤ 8 * ρ.coeffNorm ^ 2 * raySinSq u v := by
  have h4 := sq_quadRay_sub_le ρ hu hv
  have hsin : 0 ≤ raySinSq u v := raySinSq_nonneg_of_nonZero hu hv
  have hsq : 0 ≤ ρ.coeffNorm ^ 2 := sq_nonneg ρ.coeffNorm
  nlinarith

/-- Real square-root Rayleigh-quotient continuity bound:
`|(quadRay ρ u : ℝ) - (quadRay ρ v : ℝ)| ≤ 2 * (ρ.coeffNorm : ℝ) * √(raySinSq u v)`. -/
theorem abs_quadRay_sub_le_sqrt (ρ : HermForm3) {u v : GVec} (hu : u.NonZero) (hv : v.NonZero) :
    |(quadRay ρ u : ℝ) - (quadRay ρ v : ℝ)| ≤
      2 * (ρ.coeffNorm : ℝ) * Real.sqrt (raySinSq u v : ℝ) := by
  have hC0 : 0 ≤ (ρ.coeffNorm : ℝ) := by exact_mod_cast coeffNorm_nonneg ρ
  have hsin0 : 0 ≤ (raySinSq u v : ℝ) := by exact_mod_cast raySinSq_nonneg_of_nonZero hu hv
  have hrhs0 : 0 ≤ 2 * (ρ.coeffNorm : ℝ) * Real.sqrt (raySinSq u v : ℝ) := by positivity
  have hsq : ((quadRay ρ u : ℝ) - (quadRay ρ v : ℝ)) ^ 2 ≤
      (2 * (ρ.coeffNorm : ℝ) * Real.sqrt (raySinSq u v : ℝ)) ^ 2 := by
    have h4 : (((quadRay ρ u - quadRay ρ v) ^ 2 : ℚ) : ℝ) ≤
        ((4 * ρ.coeffNorm ^ 2 * raySinSq u v : ℚ) : ℝ) := by
      exact_mod_cast sq_quadRay_sub_le ρ hu hv
    push_cast at h4
    calc ((quadRay ρ u : ℝ) - (quadRay ρ v : ℝ)) ^ 2
        ≤ 4 * (ρ.coeffNorm : ℝ) ^ 2 * (raySinSq u v : ℝ) := h4
      _ = (2 * (ρ.coeffNorm : ℝ)) ^ 2 * (Real.sqrt (raySinSq u v : ℝ)) ^ 2 := by
          rw [Real.sq_sqrt hsin0]; ring
      _ = (2 * (ρ.coeffNorm : ℝ) * Real.sqrt (raySinSq u v : ℝ)) ^ 2 := by ring
  rw [← Real.sqrt_sq_eq_abs, ← Real.sqrt_sq hrhs0]
  exact Real.sqrt_le_sqrt hsq

/-- Explicit rational uniform continuity modulus for any rational Hermitian form with
`ρ.coeffNorm ≤ B`: returns `1` in the degenerate regime `B ≤ 0` and `ε² / (8 * B²)` when `B > 0`. -/
def rationalRayModulus (B ε : ℚ) : ℚ :=
  if B ≤ 0 then 1 else ε ^ 2 / (8 * B ^ 2)

/-- For every `ε > 0` and every `B : ℚ` (including `B ≤ 0`), `rationalRayModulus B ε > 0`. -/
theorem rationalRayModulus_pos {B ε : ℚ} (hε : 0 < ε) :
    0 < rationalRayModulus B ε := by
  unfold rationalRayModulus
  split_ifs with hB
  · exact one_pos
  · have hBpos : 0 < B := lt_of_not_ge hB
    positivity

/-- Constructive uniform ray-continuity guarantee with explicit modulus `rationalRayModulus B ε`:
whenever `ρ.coeffNorm ≤ B`, `ε > 0`, and `raySinSq u v < rationalRayModulus B ε`, we have
`|quadRay ρ u - quadRay ρ v| < ε`. -/
theorem quadRay_sub_lt_of_raySinSq_lt_modulus (ρ : HermForm3) {B ε : ℚ}
    (hB : ρ.coeffNorm ≤ B) (hε : 0 < ε) {u v : GVec}
    (hu : u.NonZero) (hv : v.NonZero)
    (huv : raySinSq u v < rationalRayModulus B ε) :
    |quadRay ρ u - quadRay ρ v| < ε := by
  have hC0 : 0 ≤ ρ.coeffNorm := coeffNorm_nonneg ρ
  unfold rationalRayModulus at huv
  split_ifs at huv with hB0
  · have hC_zero : ρ.coeffNorm = 0 := le_antisymm (hB.trans hB0) hC0
    have hsq := sq_quadRay_sub_le ρ hu hv
    rw [hC_zero] at hsq
    have hdiff0 : quadRay ρ u - quadRay ρ v = 0 := by nlinarith
    rw [hdiff0, abs_zero]
    exact hε
  · have hBpos : 0 < B := lt_of_not_ge hB0
    have hCB_sq : ρ.coeffNorm ^ 2 ≤ B ^ 2 := by nlinarith
    have hsin0 : 0 ≤ raySinSq u v := raySinSq_nonneg_of_nonZero hu hv
    have hsq8 := sq_quadRay_sub_le_eight ρ hu hv
    have hsqB : (quadRay ρ u - quadRay ρ v) ^ 2 ≤ 8 * B ^ 2 * raySinSq u v :=
      hsq8.trans (by nlinarith)
    have h8B_pos : 0 < 8 * B ^ 2 := by positivity
    have hlt_eps_sq : 8 * B ^ 2 * raySinSq u v < ε ^ 2 :=
      (lt_div_iff₀' h8B_pos).mp huv
    have hsq_lt : (quadRay ρ u - quadRay ρ v) ^ 2 < ε ^ 2 :=
       lt_of_le_of_lt hsqB hlt_eps_sq
    have habs_sq : |quadRay ρ u - quadRay ρ v| ^ 2 < ε ^ 2 := by
      rwa [sq_abs]
    nlinarith [abs_nonneg (quadRay ρ u - quadRay ρ v)]

/-- Purely algebraic, constructive proof that `quadRay ρ` is uniformly continuous on rays for every
`ρ : HermForm3`, using the explicit rational modulus `rationalRayModulus ρ.coeffNorm ε` rather than
compactness of the complex unit sphere. -/
theorem isUniformlyRayContinuous_quadRay_constructive (ρ : HermForm3) :
    IsUniformlyRayContinuous (quadRay ρ) := by
  intro ε hε
  refine ⟨rationalRayModulus ρ.coeffNorm ε, rationalRayModulus_pos hε, ?_⟩
  intro u v hu hv huv
  exact quadRay_sub_lt_of_raySinSq_lt_modulus ρ le_rfl hε hu hv huv

end

end BornFinite.ContinuumShadow
