import SzollosiGaugedCover
import SzollosiNativeReflection
import SzollosiRectangularReflection

/-!
# Added native coefficients and one semantic candidate-box exclusion

AuthorityEffect: None.

All added coefficient rows and all input bounds are kernel checked.
The selected image is derived from the actual transition balance identity.
Other images and the generic Rust/JSON runtime are not verified here.
No complete family/cusp cover or curvature closure is asserted.
-/

namespace MUB.SzollosiGaugedReflection
open SzollosiGaugedCover SzollosiGaugedExecutable SzollosiNativeReflection
open SzollosiColumnGauge SzollosiQuadraticSystem SzollosiTwoCirculant
open SzollosiExecutableSystem SzollosiTermExpansion SzollosiIntervalExclusion

set_option maxRecDepth 30000
set_option maxHeartbeats 10000000

-- Native inspection SHA-256: bbd5513313a63d73e3410be0ef14c45a3b96198d7eb0a81272d442a275dc5bce
-- Native exclusion SHA-256: 2fc7836d2661bb697144cec194b994d8c5f5ff829678cbdcf240c38103c4ea66
-- Native parent SHA-256: 9eb8596b1122df8f389c3b8d48e54e2fa3dd142311e4d7cf1ea3a0c92c5040b8
-- Lean coefficient SHA-256: f9fffc4d7664fc3a31fe9eee6ee0032a08271ed41184b08310ede5b21411ad44

def extraTerms : List (List CodedTerm) := [
  [((-1),[]),((1),[80])],
  [((1),[81])],
  [((-1),[]),((1),[82])],
  [((1),[83])],
  [((-1),[]),((1),[84])],
  [((1),[85])],
  [((-1),[]),((1),[86])],
  [((1),[87])],
  [((-1),[]),((1),[88])],
  [((1),[89])],
  [((-1),[]),((1),[90])],
  [((1),[91])],
  [((-1),[]),((1),[152])],
  [((1),[153])],
  [((-1),[]),((1),[154])],
  [((1),[155])],
  [((-1),[]),((1),[156])],
  [((1),[157])],
  [((-1),[]),((1),[158])],
  [((1),[159])],
  [((-1),[]),((1),[160])],
  [((1),[161])],
  [((-1),[]),((1),[162])],
  [((1),[163])],
  [((-6),[]),((1),[368]),((1),[370]),((1),[372]),((1),[374]),((1),[376]),((1),[378])],
  [((1),[369]),((1),[371]),((1),[373]),((1),[375]),((1),[377]),((1),[379])],
  [((-6),[]),((1),[380]),((1),[382]),((1),[384]),((1),[386]),((1),[388]),((1),[390])],
  [((1),[381]),((1),[383]),((1),[385]),((1),[387]),((1),[389]),((1),[391])],
  [((-6),[]),((1),[392]),((1),[394]),((1),[396]),((1),[398]),((1),[400]),((1),[402])],
  [((1),[393]),((1),[395]),((1),[397]),((1),[399]),((1),[401]),((1),[403])],
  [((-6),[]),((1),[404]),((1),[406]),((1),[408]),((1),[410]),((1),[412]),((1),[414])],
  [((1),[405]),((1),[407]),((1),[409]),((1),[411]),((1),[413]),((1),[415])],
  [((-6),[]),((1),[416]),((1),[418]),((1),[420]),((1),[422]),((1),[424]),((1),[426])],
  [((1),[417]),((1),[419]),((1),[421]),((1),[423]),((1),[425]),((1),[427])],
  [((-6),[]),((1),[428]),((1),[430]),((1),[432]),((1),[434]),((1),[436]),((1),[438])],
  [((1),[429]),((1),[431]),((1),[433]),((1),[435]),((1),[437]),((1),[439])],
  [((-6),[]),((1),[368]),((1),[380]),((1),[392]),((1),[404]),((1),[416]),((1),[428])],
  [((1),[369]),((1),[381]),((1),[393]),((1),[405]),((1),[417]),((1),[429])],
  [((-6),[]),((1),[370]),((1),[382]),((1),[394]),((1),[406]),((1),[418]),((1),[430])],
  [((1),[371]),((1),[383]),((1),[395]),((1),[407]),((1),[419]),((1),[431])],
  [((-6),[]),((1),[372]),((1),[384]),((1),[396]),((1),[408]),((1),[420]),((1),[432])],
  [((1),[373]),((1),[385]),((1),[397]),((1),[409]),((1),[421]),((1),[433])],
  [((-6),[]),((1),[374]),((1),[386]),((1),[398]),((1),[410]),((1),[422]),((1),[434])],
  [((1),[375]),((1),[387]),((1),[399]),((1),[411]),((1),[423]),((1),[435])],
  [((-6),[]),((1),[376]),((1),[388]),((1),[400]),((1),[412]),((1),[424]),((1),[436])],
  [((1),[377]),((1),[389]),((1),[401]),((1),[413]),((1),[425]),((1),[437])],
  [((-6),[]),((1),[378]),((1),[390]),((1),[402]),((1),[414]),((1),[426]),((1),[438])],
  [((1),[379]),((1),[391]),((1),[403]),((1),[415]),((1),[427]),((1),[439])]
]

def nativeBounds : List (Rat × Rat) := [
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((1),(1)),
  ((0),(0)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((1),(1)),
  ((0),(0)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((1),(1)),
  ((0),(0)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((1),(1)),
  ((0),(0)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((1),(1)),
  ((0),(0)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((1),(1)),
  ((0),(0)),
  ((1),(1)),
  ((0),(0)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(-1)),
  ((0),(0)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((1),(1)),
  ((0),(0)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(-1)),
  ((0),(0)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((1),(1)),
  ((0),(0)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(-1)),
  ((0),(0)),
  ((1),(1)),
  ((0),(0)),
  ((1),(1)),
  ((0),(0)),
  ((1),(1)),
  ((0),(0)),
  ((1),(1)),
  ((0),(0)),
  ((1),(1)),
  ((0),(0)),
  ((1),(1)),
  ((0),(0)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((1),(1)),
  ((0),(0)),
  ((1),(1)),
  ((0),(0)),
  ((1),(1)),
  ((0),(0)),
  ((1),(1)),
  ((0),(0)),
  ((1),(1)),
  ((0),(0)),
  ((1),(1)),
  ((0),(0)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-1),(1)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-1/2),(1/2)),
  ((-3),(3)),
  ((-1/2),(1/2)),
  ((-3),(3)),
  ((-1/2),(1/2)),
  ((-3),(3)),
  ((-1/2),(1/2)),
  ((-3),(3)),
  ((-1/2),(1/2)),
  ((-3),(3)),
  ((-1/2),(1/2)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3)),
  ((-3),(3))
]

def nativeImage : Bounds := ⟨(7/2),(17/2)⟩

def nativeWitnessValues : List Rat := [(1),(0),(-1),(0),(1),(0),(0),(1),(1),(0),(0),(0),(0),(0),(1),(0),(0),(0),(0),(0),(0),(0),(1),(0),(0),(0),(0),(0),(1),(0),(0),(0),(0),(0),(0),(0),(1),(0),(0),(0),(0),(0),(1),(0),(1),(0),(0),(0),(0),(0),(-1),(0),(0),(0),(0),(0),(0),(0),(1),(0),(0),(0),(0),(0),(-1),(0),(0),(0),(0),(0),(0),(0),(1),(0),(0),(0),(0),(0),(-1),(0),(1),(0),(1),(0),(1),(0),(1),(0),(1),(0),(1),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(1),(0),(1),(0),(1),(0),(1),(0),(1),(0),(1),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0),(0)]

def extraCoefficientCheck : Bool := tableKeys extraTerms ==
  tableKeys (extraExpressions.map normalizedExpr)

theorem extra_coefficients_checked : extraCoefficientCheck = true := by decide +kernel

theorem extra_terms_match : extraTerms = extraExpressions.map normalizedExpr :=
  table_keys_injective (beq_iff_eq.mp extra_coefficients_checked)

def augmentedNativeTerms : List (List CodedTerm) := nativeTerms ++ extraTerms

theorem augmented_native_terms_match :
    augmentedNativeTerms = augmentedExpressions.map normalizedExpr := by
  simp only [augmentedNativeTerms,augmentedExpressions,List.map_append,List.map_map,
    native_terms_match,extra_terms_match]
  rfl

def nativeLower (v : Variable) : Rat := ((nativeBounds[variableCode v]?).getD (0,0)).1
def nativeUpper (v : Variable) : Rat := ((nativeBounds[variableCode v]?).getD (0,0)).2

def nativeBoundCheck : Bool := allVariables.all fun v =>
  decide (lowRowLower v ≤ nativeLower v) && decide (nativeUpper v ≤ lowRowUpper v)

theorem native_bounds_checked : nativeBoundCheck = true := by decide +kernel

def InNativeBox (r : Variable → ℝ) : Prop :=
  ∀ v, (nativeLower v : ℝ) ≤ r v ∧ r v ≤ (nativeUpper v : ℝ)

theorem native_box_in_low_row (r : Variable → ℝ) (hb : InNativeBox r) : InLowRowBox r := by
  intro v
  have hv := List.all_eq_true.mp native_bounds_checked v (variables_complete v)
  simp only [Bool.and_eq_true,decide_eq_true_iff] at hv
  have hl : lowRowLower v ≤ nativeLower v := hv.1
  have hu : nativeUpper v ≤ lowRowUpper v := hv.2
  have hlr : (lowRowLower v : ℝ) ≤ nativeLower v := by exact_mod_cast hl
  have hur : (nativeUpper v : ℝ) ≤ lowRowUpper v := by exact_mod_cast hu
  exact ⟨hlr.trans (hb v).1,(hb v).2.trans hur⟩

theorem native_image_separated :
    decide (nativeUpper (rowVariable 0) < nativeImage.lo) = true := by decide +kernel

/-- The selected emitted image encloses the coordinate of every contained zero. -/
theorem native_image_semantics (r : Variable → ℝ) (h : AllExpressionsZero r)
    (hb : InNativeBox r) : nativeImage.Contains (r (rowVariable 0)) := by
  have hi := balanced_row_image r h (native_box_in_low_row r hb)
  norm_num [nativeImage,Bounds.Contains] at hi ⊢
  exact hi

theorem native_box_exclusion (r : Variable → ℝ) (h : AllExpressionsZero r)
    (hb : InNativeBox r) : False :=
  low_row_box_empty r h (native_box_in_low_row r hb)

def nativeWitness (v : Variable) : Rat := (nativeWitnessValues[variableCode v]?).getD 0

def witnessCheck : Bool := allVariables.all fun v =>
  decide (nativeLower v ≤ nativeWitness v) && decide (nativeWitness v ≤ nativeUpper v)

theorem native_witness_checked : witnessCheck = true := by decide +kernel

theorem native_witness_contains : InNativeBox (fun v => (nativeWitness v : ℝ)) := by
  intro v
  change (nativeLower v : ℝ) ≤ (nativeWitness v : ℝ) ∧ (nativeWitness v : ℝ) ≤ (nativeUpper v : ℝ)
  have hv := List.all_eq_true.mp native_witness_checked v (variables_complete v)
  simp only [Bool.and_eq_true,decide_eq_true_iff] at hv
  constructor
  · exact_mod_cast (hv.1 : nativeLower v ≤ nativeWitness v)
  · exact_mod_cast (hv.2 : nativeWitness v ≤ nativeUpper v)

theorem witness_parameters_eq :
    parameters (fun v => (nativeWitness v : ℝ)) = encodeParameters ![1,-1,1,Complex.I] := by
  funext q
  rcases q with ⟨i,b⟩
  fin_cases i <;> cases b <;>
    norm_num [parameters,nativeWitness,nativeWitnessValues,variableCode,bit,encodeParameters]

theorem witness_parameter_equations :
    ∀ e, MvPolynomial.eval (parameters (fun v => (nativeWitness v : ℝ)))
      (parameterPolynomial e) = 0 := by
  rw [witness_parameters_eq]
  apply (parameter_equations_iff _).mpr
  simpa [decode_encode] using boundary_parameter_point

/-- This box meets the admissible phase domain; the witness is not a quartet. -/
theorem native_box_has_admissible_phase_point :
    ∃ r : Variable → ℝ, InNativeBox r ∧
      ∀ e, MvPolynomial.eval (parameters r) (parameterPolynomial e) = 0 :=
  ⟨fun v => (nativeWitness v : ℝ),native_witness_contains,witness_parameter_equations⟩

def parentBounds : Variable → Bounds
  | .inr (.inr (a,i,j,b)) => if a = 2 ∧ i = 0 ∧ b = false then ⟨-3,3⟩
      else ⟨nativeLower (.inr (.inr (a,i,j,b))),nativeUpper (.inr (.inr (a,i,j,b)))⟩
  | v => ⟨nativeLower v,nativeUpper v⟩

def parentBoundCheck : Bool := allVariables.all fun v =>
  let b := SzollosiRectangularReflection.nativeRetainedBox (variableCode v)
  decide ((parentBounds v).lo ≤ max b.lo (gaugeLower v)) &&
    decide (min b.hi (gaugeUpper v) ≤ (parentBounds v).hi)

theorem parent_bounds_checked : parentBoundCheck = true := by decide +kernel

theorem augmented_solution_in_parent (r : Variable → ℝ) (h : AllExpressionsZero r) :
    ∀ v, (parentBounds v).Contains (r v) := by
  have hs := (augmented_zeros_iff r).mp h
  have hg := gauged_solution_in_box r hs.1 hs.2
  intro v
  have hb := SzollosiRectangularReflection.solution_in_native_retained r hs.1
    (variableCode v) (variableCode_lt v)
  rw [coded_point_code] at hb
  have hv := List.all_eq_true.mp parent_bounds_checked v (variables_complete v)
  simp only [Bool.and_eq_true,decide_eq_true_iff] at hv
  have hl : ((parentBounds v).lo : ℝ) ≤
      max ((SzollosiRectangularReflection.nativeRetainedBox (variableCode v)).lo : ℝ)
        (gaugeLower v : ℝ) := by exact_mod_cast hv.1
  have hu : min ((SzollosiRectangularReflection.nativeRetainedBox (variableCode v)).hi : ℝ)
      (gaugeUpper v : ℝ) ≤ (parentBounds v).hi := by exact_mod_cast hv.2
  exact ⟨hl.trans (max_le hb.1 (hg v).1),(le_min hb.2 (hg v).2).trans hu⟩

def nativeChartBounds (j : Fin 6) (v : Variable) : Bounds :=
  ⟨if v = rowVariable j then 1 else (parentBounds v).lo,(parentBounds v).hi⟩

def InNativeChart (r : Variable → ℝ) (j : Fin 6) : Prop :=
  ∀ v, (nativeChartBounds j v).Contains (r v)

theorem native_chart_cover (r : Variable → ℝ) (h : AllExpressionsZero r) :
    ∃ j, InNativeChart r j := by
  have hb := augmented_solution_in_parent r h
  obtain ⟨j,hj⟩ := augmented_solution_six_charts r h
  rw [row_coordinate] at hj
  refine ⟨j,fun v => ⟨?_,(hb v).2⟩⟩
  by_cases hv : v = rowVariable j
  · simpa [nativeChartBounds,hv] using hj
  · simpa [nativeChartBounds,hv] using (hb v).1

theorem native_chart_quartet_iff (p : ParameterCoord → ℝ)
    (hp : ∀ e, MvPolynomial.eval p (parameterPolynomial e) = 0) :
    (∃ r, parameters r = p ∧ AllExpressionsZero r ∧ ∃ j, InNativeChart r j) ↔
      ∃ U V, SzollosiQuartetSystem.Quartet
        (SzollosiQuartetSystem.bases (SzollosiQuartetSystem.parameterMatrix p) U V) := by
  rw [← augmented_exists_with_parameters_iff p hp]
  constructor
  · rintro ⟨r,hr,hz,_⟩
    exact ⟨r,hr,hz⟩
  · rintro ⟨r,hr,hz⟩
    exact ⟨r,hr,hz,native_chart_cover r hz⟩

def nativeChartJson : Lean.Json := .arr (((List.finRange 6).map fun j =>
  Lean.Json.mkObj [("chart",natJson j.val),("bounds",.arr ((allVariables.map fun v =>
    Lean.Json.mkObj [("index",natJson (variableCode v)),
      ("lo",.str (rationalText (nativeChartBounds j v).lo)),
      ("hi",.str (rationalText (nativeChartBounds j v).hi))]).toArray))]).toArray)

#print axioms parent_bounds_checked
#print axioms augmented_solution_in_parent
#print axioms native_chart_cover
#print axioms native_chart_quartet_iff

#print axioms augmented_native_terms_match
#print axioms native_bounds_checked
#print axioms native_image_semantics
#print axioms native_box_exclusion
#print axioms native_box_has_admissible_phase_point
end MUB.SzollosiGaugedReflection

