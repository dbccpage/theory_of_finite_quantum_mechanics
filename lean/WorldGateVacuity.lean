import PrimitiveDifference

/-!
# W8.10: exact finite gate-vacuity classifier

The DDA D9 target asks whether a Bool-valued gate can emit both outcomes on a
declared finite input family.  This file formalizes exactly that finite
question.  A typed family contains its finite input list and its gate.  The
classifier separates empty scope, nonempty all-pass, nonempty all-fail, and
mixed observations.

For a mixed family, a proof of the scan result yields the existence of one pass
input and one fail input.  Those two inputs form a mixed certificate, and every
mixed declared list has length at least two.  Declared input lists are required
to be duplicate-free, so the explicit two-point family is cardinality-minimal
for certifying non-vacuity at this finite Bool surface.

The gate outcomes also carry a genuine `PrimitiveDifference Bool Bool` from
the shared kernel.  Its difference is exclusive-or and its `ZeroRel` is
exactly equality of outcomes.  The explicit pass/fail pair therefore has a
nonzero difference and is not zero-related.

The eight gates on a fixed three-point carrier are also exhausted exactly: one
is all-pass, one is all-fail, and six are mixed.  A conditional black-box lower
bound shows that any one omitted declared input can conceal a failure while all
queried results agree with the constant-pass gate.  No unrestricted numeric or
exponential query lower bound is claimed.

No external gate implementation is inspected.  No estate sweep, unrestricted
input-independence result, anti-cheat-law promotion, WGOC composition theorem,
or authority transition is claimed.

AuthorityEffect: None.
-/

namespace OmegaWorld
namespace GateVacuityW810

open OmegaCore

universe u

/-- The four exact outcomes of scanning a declared finite Bool gate family. -/
inductive GateClass where
  | emptyScope
  | allPass
  | allFail
  | mixed
  deriving DecidableEq

/--
An executable four-way classifier for a finite list of observed gate results.
`true` is pass and `false` is fail.  The empty case is separated before the
two membership tests, so empty scope is never mislabeled all-pass or all-fail.
-/
def classifyOutcomes (outcomes : List Bool) : GateClass :=
  if outcomes = [] then
    .emptyScope
  else if true ∈ outcomes then
    if false ∈ outcomes then .mixed else .allPass
  else
    .allFail

def EveryPass (outcomes : List Bool) : Prop :=
  outcomes ≠ [] ∧ ∀ outcome : Bool, outcome ∈ outcomes → outcome = true

def EveryFail (outcomes : List Bool) : Prop :=
  outcomes ≠ [] ∧ ∀ outcome : Bool, outcome ∈ outcomes → outcome = false

def HasBothOutcomes (outcomes : List Bool) : Prop :=
  true ∈ outcomes ∧ false ∈ outcomes

/-- Constancy of the observed restriction, including the empty scope. -/
def OutcomeConstant (outcomes : List Bool) : Prop :=
  ∀ left : Bool, left ∈ outcomes →
    ∀ right : Bool, right ∈ outcomes → left = right

theorem all_true_iff_false_not_mem (outcomes : List Bool) :
    (∀ outcome : Bool, outcome ∈ outcomes → outcome = true) ↔
      false ∉ outcomes := by
  constructor
  · intro allTrue falseMember
    have impossible : false = true := allTrue false falseMember
    cases impossible
  · intro noFalse outcome member
    cases outcome with
    | false => exact False.elim (noFalse member)
    | true => rfl

theorem all_false_iff_true_not_mem (outcomes : List Bool) :
    (∀ outcome : Bool, outcome ∈ outcomes → outcome = false) ↔
      true ∉ outcomes := by
  constructor
  · intro allFalse trueMember
    have impossible : true = false := allFalse true trueMember
    cases impossible
  · intro noTrue outcome member
    cases outcome with
    | false => rfl
    | true => exact False.elim (noTrue member)

theorem true_mem_of_nonempty_no_false
    (outcomes : List Bool) (nonempty : outcomes ≠ [])
    (noFalse : false ∉ outcomes) :
    true ∈ outcomes := by
  cases outcomes with
  | nil => exact False.elim (nonempty rfl)
  | cons head tail =>
      cases head with
      | false => exact False.elim (noFalse List.mem_cons_self)
      | true => exact List.mem_cons_self

theorem classify_empty_iff (outcomes : List Bool) :
    classifyOutcomes outcomes = .emptyScope ↔ outcomes = [] := by
  by_cases empty : outcomes = []
  · simp [classifyOutcomes, empty]
  · by_cases hasPass : true ∈ outcomes
    · by_cases hasFail : false ∈ outcomes <;>
        simp [classifyOutcomes, empty, hasPass, hasFail]
    · simp [classifyOutcomes, empty, hasPass]

theorem classify_allPass_membership_iff (outcomes : List Bool) :
    classifyOutcomes outcomes = .allPass ↔
      outcomes ≠ [] ∧ true ∈ outcomes ∧ false ∉ outcomes := by
  by_cases empty : outcomes = []
  · simp [classifyOutcomes, empty]
  · by_cases hasPass : true ∈ outcomes
    · by_cases hasFail : false ∈ outcomes <;>
        simp [classifyOutcomes, empty, hasPass, hasFail]
    · simp [classifyOutcomes, empty, hasPass]

theorem classify_allFail_membership_iff (outcomes : List Bool) :
    classifyOutcomes outcomes = .allFail ↔
      outcomes ≠ [] ∧ true ∉ outcomes := by
  by_cases empty : outcomes = []
  · simp [classifyOutcomes, empty]
  · by_cases hasPass : true ∈ outcomes
    · by_cases hasFail : false ∈ outcomes <;>
        simp [classifyOutcomes, empty, hasPass, hasFail]
    · simp [classifyOutcomes, empty, hasPass]

theorem classify_mixed_iff (outcomes : List Bool) :
    classifyOutcomes outcomes = .mixed ↔ HasBothOutcomes outcomes := by
  by_cases empty : outcomes = []
  · simp [classifyOutcomes, HasBothOutcomes, empty]
  · by_cases hasPass : true ∈ outcomes
    · by_cases hasFail : false ∈ outcomes <;>
        simp [classifyOutcomes, HasBothOutcomes, empty, hasPass, hasFail]
    · simp [classifyOutcomes, HasBothOutcomes, empty, hasPass]

/-- The exact finite D9 vacuity criterion: non-mixed is precisely constant. -/
theorem classify_not_mixed_iff_constant (outcomes : List Bool) :
    classifyOutcomes outcomes ≠ .mixed ↔ OutcomeConstant outcomes := by
  constructor
  · intro notMixed left leftMember right rightMember
    have notBoth : ¬ HasBothOutcomes outcomes := by
      intro both
      exact notMixed ((classify_mixed_iff outcomes).2 both)
    cases left <;> cases right
    · rfl
    · exact False.elim (notBoth ⟨rightMember, leftMember⟩)
    · exact False.elim (notBoth ⟨leftMember, rightMember⟩)
    · rfl
  · intro constant mixedResult
    have both : HasBothOutcomes outcomes :=
      (classify_mixed_iff outcomes).1 mixedResult
    have impossible : true = false :=
      constant true both.1 false both.2
    cases impossible

theorem classify_allPass_iff (outcomes : List Bool) :
    classifyOutcomes outcomes = .allPass ↔ EveryPass outcomes := by
  rw [classify_allPass_membership_iff]
  constructor
  · intro exactMembership
    exact
      ⟨exactMembership.1,
        (all_true_iff_false_not_mem outcomes).2 exactMembership.2.2⟩
  · intro everyPass
    have noFalse : false ∉ outcomes :=
      (all_true_iff_false_not_mem outcomes).1 everyPass.2
    exact
      ⟨everyPass.1,
        true_mem_of_nonempty_no_false outcomes everyPass.1 noFalse,
        noFalse⟩

theorem classify_allFail_iff (outcomes : List Bool) :
    classifyOutcomes outcomes = .allFail ↔ EveryFail outcomes := by
  rw [classify_allFail_membership_iff]
  constructor
  · intro exactMembership
    exact
      ⟨exactMembership.1,
        (all_false_iff_true_not_mem outcomes).2 exactMembership.2⟩
  · intro everyFail
    exact
      ⟨everyFail.1,
        (all_false_iff_true_not_mem outcomes).1 everyFail.2⟩

/-- The executable scan has exactly one of the four declared finite results. -/
theorem classifier_exhaustive (outcomes : List Bool) :
    classifyOutcomes outcomes = .emptyScope ∨
      classifyOutcomes outcomes = .allPass ∨
      classifyOutcomes outcomes = .allFail ∨
      classifyOutcomes outcomes = .mixed := by
  cases classifyOutcomes outcomes <;> simp

/-- Any observed list classified mixed contains at least two entries. -/
theorem mixed_requires_two_outcomes (outcomes : List Bool)
    (mixedResult : classifyOutcomes outcomes = .mixed) :
    2 ≤ outcomes.length := by
  cases outcomes with
  | nil => simp [classifyOutcomes] at mixedResult
  | cons first tail =>
      cases tail with
      | nil =>
          cases first <;> simp [classifyOutcomes] at mixedResult
      | cons second rest =>
          simp

/-- A finite input family together with the Bool gate evaluated on it. -/
structure DeclaredGateFamily (α : Type u) where
  inputs : List α
  inputsNodup : inputs.Nodup
  gate : α → Bool

def observedOutcomes (family : DeclaredGateFamily α) : List Bool :=
  family.inputs.map family.gate

def scanGate (family : DeclaredGateFamily α) : GateClass :=
  classifyOutcomes (observedOutcomes family)

/-- A concrete two-input certificate internal to one declared family. -/
structure MixedCertificate (family : DeclaredGateFamily α) where
  passInput : α
  passMember : passInput ∈ family.inputs
  passOutcome : family.gate passInput = true
  failInput : α
  failMember : failInput ∈ family.inputs
  failOutcome : family.gate failInput = false

theorem certificate_inputs_distinct
    (family : DeclaredGateFamily α)
    (certificate : MixedCertificate family) :
    certificate.passInput ≠ certificate.failInput := by
  intro sameInput
  have impossible : true = false := by
    calc
      true = family.gate certificate.passInput :=
        certificate.passOutcome.symm
      _ = family.gate certificate.failInput :=
        congrArg family.gate sameInput
      _ = false := certificate.failOutcome
  cases impossible

theorem scan_mixed_iff_certificate
    (family : DeclaredGateFamily α) :
    scanGate family = .mixed ↔ Nonempty (MixedCertificate family) := by
  rw [scanGate, classify_mixed_iff]
  constructor
  · intro both
    rcases List.mem_map.mp both.1 with ⟨passInput, passMember, passOutcome⟩
    rcases List.mem_map.mp both.2 with ⟨failInput, failMember, failOutcome⟩
    exact
      ⟨{ passInput := passInput
         passMember := passMember
         passOutcome := passOutcome
         failInput := failInput
         failMember := failMember
         failOutcome := failOutcome }⟩
  · intro certificateExists
    rcases certificateExists with ⟨certificate⟩
    constructor
    · exact List.mem_map.mpr
        ⟨certificate.passInput, certificate.passMember,
          certificate.passOutcome⟩
    · exact List.mem_map.mpr
        ⟨certificate.failInput, certificate.failMember,
          certificate.failOutcome⟩

theorem mixed_family_requires_two_inputs
    (family : DeclaredGateFamily α)
    (mixedResult : scanGate family = .mixed) :
    2 ≤ family.inputs.length := by
  have observedBound : 2 ≤ (observedOutcomes family).length :=
    mixed_requires_two_outcomes (observedOutcomes family) mixedResult
  simpa [observedOutcomes] using observedBound

theorem finite_scan_exhaustion (family : DeclaredGateFamily α) :
    scanGate family = .emptyScope ∨
      scanGate family = .allPass ∨
      scanGate family = .allFail ∨
      scanGate family = .mixed :=
  classifier_exhaustive (observedOutcomes family)

/--
Mathematical constancy on the declared restriction.  It is true on empty scope;
the classifier still reports that case separately as `emptyScope`.  This is
not a predicate for "vacuous on a nonempty scope".
-/
def GateVacuous (family : DeclaredGateFamily α) : Prop :=
  OutcomeConstant (observedOutcomes family)

theorem finite_gate_vacuous_iff_not_mixed
    (family : DeclaredGateFamily α) :
    GateVacuous family ↔ scanGate family ≠ .mixed := by
  exact (classify_not_mixed_iff_constant
    (observedOutcomes family)).symm

/-- The gate that passes every input. -/
def constantPassGate (_input : α) : Bool := true

/-- A comparison gate that fails at exactly one declared input. -/
def failOnlyAt [DecidableEq α] (hidden input : α) : Bool :=
  if input = hidden then false else true

theorem queried_outcomes_agree_when_failure_is_omitted
    [DecidableEq α] (queried : List α) (hidden : α)
    (hiddenOmitted : hidden ∉ queried) :
    queried.map (constantPassGate (α := α)) =
      queried.map (failOnlyAt hidden) := by
  induction queried with
  | nil => rfl
  | cons head tail inductionHypothesis =>
      have headNotHidden : head ≠ hidden := by
        intro headHidden
        apply hiddenOmitted
        rw [headHidden]
        exact List.mem_cons_self
      have hiddenOmittedTail : hidden ∉ tail := by
        intro hiddenInTail
        exact hiddenOmitted (List.mem_cons_of_mem head hiddenInTail)
      simp [constantPassGate, failOnlyAt, headNotHidden,
        inductionHypothesis hiddenOmittedTail]

/--
Conditional black-box lower bound: if a duplicate-free declared carrier has a
hidden input and a distinct control input, omitting the hidden input leaves the
constant-pass and hidden-fail gates observationally identical on every query,
although their full finite classifications are all-pass and mixed.
-/
theorem omitted_input_can_hide_failure
    [DecidableEq α]
    (inputs queried : List α) (inputsNodup : inputs.Nodup)
    (hidden control : α)
    (hiddenMember : hidden ∈ inputs)
    (controlMember : control ∈ inputs)
    (controlNotHidden : control ≠ hidden)
    (hiddenOmitted : hidden ∉ queried) :
    let passFamily : DeclaredGateFamily α :=
      { inputs := inputs
        inputsNodup := inputsNodup
        gate := constantPassGate }
    let hiddenFailFamily : DeclaredGateFamily α :=
      { inputs := inputs
        inputsNodup := inputsNodup
        gate := failOnlyAt hidden }
    queried.map passFamily.gate = queried.map hiddenFailFamily.gate ∧
      scanGate passFamily = .allPass ∧
      scanGate hiddenFailFamily = .mixed := by
  dsimp
  constructor
  · exact queried_outcomes_agree_when_failure_is_omitted
      queried hidden hiddenOmitted
  · constructor
    · rw [scanGate, classify_allPass_iff]
      constructor
      · intro mappedEmpty
        have trueObserved :
            true ∈ inputs.map (constantPassGate (α := α)) :=
          List.mem_map.mpr ⟨hidden, hiddenMember, rfl⟩
        have mappedEmpty' :
            inputs.map (constantPassGate (α := α)) = [] := by
          simpa [observedOutcomes] using mappedEmpty
        simp [mappedEmpty'] at trueObserved
      · intro outcome outcomeMember
        rcases List.mem_map.mp outcomeMember with
          ⟨input, inputMember, inputOutcome⟩
        exact inputOutcome.symm
    · apply (scan_mixed_iff_certificate _).2
      exact
        ⟨{ passInput := control
           passMember := controlMember
           passOutcome := by simp [failOnlyAt, controlNotHidden]
           failInput := hidden
           failMember := hiddenMember
           failOutcome := by simp [failOnlyAt] }⟩

/-- Exclusive-or difference on Bool gate outcomes. -/
def outcomeDelta : Bool → Bool → Bool
  | false, false => false
  | false, true => true
  | true, false => true
  | true, true => false

/--
The lawful shared-kernel Primitive Difference for gate outcomes.  A residual is
zero exactly when the two observed gate results agree.
-/
def gateOutcomePD : PrimitiveDifference Bool Bool where
  δ := outcomeDelta
  Zero := fun residual => residual = false
  zero_refl := by
    intro outcome
    cases outcome <;> rfl
  zero_symm := by
    intro left right zeroLeftRight
    cases left <;> cases right <;> simp_all [outcomeDelta]
  zero_trans := by
    intro left middle right zeroLeftMiddle zeroMiddleRight
    cases left <;> cases middle <;> cases right <;>
      simp_all [outcomeDelta]

theorem gate_outcome_zeroRel_iff (left right : Bool) :
    gateOutcomePD.ZeroRel left right ↔ left = right := by
  cases left <;> cases right <;>
    simp [PrimitiveDifference.ZeroRel, gateOutcomePD, outcomeDelta]

theorem gate_outcome_delta_true_iff_ne (left right : Bool) :
    gateOutcomePD.δ left right = true ↔ left ≠ right := by
  cases left <;> cases right <;> simp [gateOutcomePD, outcomeDelta]

theorem certificate_pair_is_mixed
    (family : DeclaredGateFamily α)
    (certificate : MixedCertificate family) :
    classifyOutcomes
        [family.gate certificate.passInput,
          family.gate certificate.failInput] = .mixed := by
  simp [classifyOutcomes, certificate.passOutcome, certificate.failOutcome]

theorem certificate_difference_nonzero
    (family : DeclaredGateFamily α)
    (certificate : MixedCertificate family) :
    gateOutcomePD.δ
        (family.gate certificate.passInput)
        (family.gate certificate.failInput) = true ∧
      ¬ gateOutcomePD.ZeroRel
        (family.gate certificate.passInput)
        (family.gate certificate.failInput) := by
  constructor
  · simp [certificate.passOutcome, certificate.failOutcome,
      gateOutcomePD, outcomeDelta]
  · rw [gate_outcome_zeroRel_iff]
    simp [certificate.passOutcome, certificate.failOutcome]

/-- The explicit cardinality-two finite family witnessing non-vacuity. -/
inductive TwoPoint where
  | passPoint
  | failPoint
  deriving DecidableEq

def twoPointGate : TwoPoint → Bool
  | .passPoint => true
  | .failPoint => false

def twoPointFamily : DeclaredGateFamily TwoPoint where
  inputs := [.passPoint, .failPoint]
  inputsNodup := by decide
  gate := twoPointGate

def twoPointCertificate : MixedCertificate twoPointFamily where
  passInput := .passPoint
  passMember := List.mem_cons_self
  passOutcome := rfl
  failInput := .failPoint
  failMember :=
    List.mem_cons_of_mem TwoPoint.passPoint List.mem_cons_self
  failOutcome := rfl

theorem two_point_is_mixed : scanGate twoPointFamily = .mixed := by
  exact (scan_mixed_iff_certificate twoPointFamily).2
    ⟨twoPointCertificate⟩

theorem two_point_nonzero_pair :
    gateOutcomePD.δ
        (twoPointGate .passPoint) (twoPointGate .failPoint) = true ∧
      ¬ gateOutcomePD.ZeroRel
        (twoPointGate .passPoint) (twoPointGate .failPoint) :=
  by
    constructor
    · rfl
    · rw [gate_outcome_zeroRel_iff]
      decide

/--
The explicit certificate has two inputs, and no mixed declared family can have
fewer.  This is cardinality minimality, not an exponential lower bound.
-/
theorem two_point_certificate_is_minimal :
    twoPointFamily.inputs.length = 2 ∧
      scanGate twoPointFamily = .mixed ∧
      ∀ (family : DeclaredGateFamily TwoPoint),
        scanGate family = .mixed → 2 ≤ family.inputs.length := by
  constructor
  · rfl
  · constructor
    · exact two_point_is_mixed
    · intro family mixedResult
      exact mixed_family_requires_two_inputs family mixedResult

/-- The fixed duplicate-free three-point carrier used for exact exhaustion. -/
inductive Fin3Point where
  | p0
  | p1
  | p2
  deriving DecidableEq

/-- All eight deterministic Bool gates on the fixed three-point carrier. -/
inductive Fin3GateCode where
  | fff
  | fft
  | ftf
  | ftt
  | tff
  | tft
  | ttf
  | ttt
  deriving DecidableEq

def fin3Gate : Fin3GateCode → Fin3Point → Bool
  | .fff, _ => false
  | .fft, .p0 => false
  | .fft, .p1 => false
  | .fft, .p2 => true
  | .ftf, .p0 => false
  | .ftf, .p1 => true
  | .ftf, .p2 => false
  | .ftt, .p0 => false
  | .ftt, .p1 => true
  | .ftt, .p2 => true
  | .tff, .p0 => true
  | .tff, .p1 => false
  | .tff, .p2 => false
  | .tft, .p0 => true
  | .tft, .p1 => false
  | .tft, .p2 => true
  | .ttf, .p0 => true
  | .ttf, .p1 => true
  | .ttf, .p2 => false
  | .ttt, _ => true

/-- Encode an arbitrary Bool gate by its complete truth table on `Fin3Point`. -/
def fin3CodeOf (gate : Fin3Point → Bool) : Fin3GateCode :=
  match gate .p0, gate .p1, gate .p2 with
  | false, false, false => .fff
  | false, false, true => .fft
  | false, true, false => .ftf
  | false, true, true => .ftt
  | true, false, false => .tff
  | true, false, true => .tft
  | true, true, false => .ttf
  | true, true, true => .ttt

/-- Decoding the truth-table code recovers every Bool gate extensionally. -/
theorem fin3Gate_fin3CodeOf (gate : Fin3Point → Bool) :
    fin3Gate (fin3CodeOf gate) = gate := by
  funext point
  cases h0 : gate .p0 <;>
    cases h1 : gate .p1 <;>
      cases h2 : gate .p2 <;>
        cases point <;>
          simp [fin3CodeOf, fin3Gate, h0, h1, h2]

/-- Encoding a decoded gate recovers its unique code. -/
theorem fin3CodeOf_fin3Gate (code : Fin3GateCode) :
    fin3CodeOf (fin3Gate code) = code := by
  cases code <;> decide

/-- Explicit unique-representation proposition without any enumeration oracle. -/
def HasUniqueFin3Code (gate : Fin3Point → Bool) : Prop :=
  ∃ code : Fin3GateCode,
    fin3Gate code = gate ∧
      ∀ other : Fin3GateCode, fin3Gate other = gate → other = code

/-- Every deterministic Bool gate on `Fin3Point` has exactly one table code. -/
theorem fin3_every_gate_has_unique_code (gate : Fin3Point → Bool) :
    HasUniqueFin3Code gate := by
  refine ⟨fin3CodeOf gate, fin3Gate_fin3CodeOf gate, ?_⟩
  intro code codeRepresentsGate
  calc
    code = fin3CodeOf (fin3Gate code) :=
      (fin3CodeOf_fin3Gate code).symm
    _ = fin3CodeOf gate := congrArg fin3CodeOf codeRepresentsGate

def fin3Family (code : Fin3GateCode) : DeclaredGateFamily Fin3Point where
  inputs := [.p0, .p1, .p2]
  inputsNodup := by decide
  gate := fin3Gate code

def fin3Class (code : Fin3GateCode) : GateClass :=
  scanGate (fin3Family code)

def classIndicator (target observed : GateClass) : Nat :=
  if target = observed then 1 else 0

def fin3ClassCount (target : GateClass) : Nat :=
  classIndicator target (fin3Class .fff) +
  classIndicator target (fin3Class .fft) +
  classIndicator target (fin3Class .ftf) +
  classIndicator target (fin3Class .ftt) +
  classIndicator target (fin3Class .tff) +
  classIndicator target (fin3Class .tft) +
  classIndicator target (fin3Class .ttf) +
  classIndicator target (fin3Class .ttt)

theorem fin3_each_gate_classified_exactly (code : Fin3GateCode) :
    (code = .fff ∧ fin3Class code = .allFail) ∨
      (code = .ttt ∧ fin3Class code = .allPass) ∨
      (code ≠ .fff ∧ code ≠ .ttt ∧ fin3Class code = .mixed) := by
  cases code <;> decide

/-- Exact exhaustion counts for all `2^3 = 8` gates on the Fin3 carrier. -/
theorem fin3_exact_class_counts :
    fin3ClassCount .emptyScope = 0 ∧
      fin3ClassCount .allPass = 1 ∧
      fin3ClassCount .allFail = 1 ∧
      fin3ClassCount .mixed = 6 := by
  decide

/--
The exact code counts are counts of all functions because every function has
one and only one code.
-/
theorem fin3_all_functions_exact_class_counts :
    (∀ gate : Fin3Point → Bool,
      HasUniqueFin3Code gate) ∧
      fin3ClassCount .emptyScope = 0 ∧
      fin3ClassCount .allPass = 1 ∧
      fin3ClassCount .allFail = 1 ∧
      fin3ClassCount .mixed = 6 := by
  exact ⟨fin3_every_gate_has_unique_code, fin3_exact_class_counts⟩

inductive W810AuthorityEffect where
  | none
  deriving DecidableEq

/-- Bundled exact finite result with every unavailable promotion retained false. -/
structure FiniteGateVacuitySurface where
  family : DeclaredGateFamily TwoPoint
  familyIsExact : family = twoPointFamily
  classification : scanGate family = .mixed
  certificate : MixedCertificate family
  certificateClassifies :
    classifyOutcomes
        [family.gate certificate.passInput,
          family.gate certificate.failInput] = .mixed
  certificateDifferenceNonzero :
    gateOutcomePD.δ
        (family.gate certificate.passInput)
        (family.gate certificate.failInput) = true
  certificateNotZeroRelated :
    ¬ gateOutcomePD.ZeroRel
        (family.gate certificate.passInput)
        (family.gate certificate.failInput)
  certificateInputsDistinct :
    certificate.passInput ≠ certificate.failInput
  minimumInputCount : 2 ≤ family.inputs.length
  finiteExhaustion : ∀ (outcomes : List Bool),
    classifyOutcomes outcomes = .emptyScope ∨
      classifyOutcomes outcomes = .allPass ∨
      classifyOutcomes outcomes = .allFail ∨
      classifyOutcomes outcomes = .mixed
  finiteVacuityExact : ∀ (outcomes : List Bool),
    classifyOutcomes outcomes ≠ .mixed ↔ OutcomeConstant outcomes
  fin3AllFunctionsRepresentedUniquely : ∀ gate : Fin3Point → Bool,
    HasUniqueFin3Code gate
  fin3CountsExact :
    fin3ClassCount .emptyScope = 0 ∧
      fin3ClassCount .allPass = 1 ∧
      fin3ClassCount .allFail = 1 ∧
      fin3ClassCount .mixed = 6
  estateSweepClaimed : Bool
  estateSweepOpen : estateSweepClaimed = false
  externalGateSemanticsClaimed : Bool
  externalGateSemanticsOpen : externalGateSemanticsClaimed = false
  unrestrictedInputIndependenceClaimed : Bool
  unrestrictedInputIndependenceOpen :
    unrestrictedInputIndependenceClaimed = false
  exponentialLowerBoundClaimed : Bool
  exponentialLowerBoundOpen : exponentialLowerBoundClaimed = false
  unrestrictedNumericQueryLowerBoundClaimed : Bool
  unrestrictedNumericQueryLowerBoundOpen :
    unrestrictedNumericQueryLowerBoundClaimed = false
  antiCheatLawPromoted : Bool
  antiCheatLawPromotionOpen : antiCheatLawPromoted = false
  wgocCompositionClaimed : Bool
  wgocCompositionOpen : wgocCompositionClaimed = false
  primitiveDifferencePromotedBeyondLocalOutcomes : Bool
  primitiveDifferencePromotionOpen :
    primitiveDifferencePromotedBeyondLocalOutcomes = false
  authorityEffect : W810AuthorityEffect
  authorityNone : authorityEffect = .none

def finiteGateVacuitySurface : FiniteGateVacuitySurface where
  family := twoPointFamily
  familyIsExact := rfl
  classification := two_point_is_mixed
  certificate := twoPointCertificate
  certificateClassifies :=
    certificate_pair_is_mixed twoPointFamily twoPointCertificate
  certificateDifferenceNonzero :=
    (certificate_difference_nonzero
      twoPointFamily twoPointCertificate).1
  certificateNotZeroRelated :=
    (certificate_difference_nonzero
      twoPointFamily twoPointCertificate).2
  certificateInputsDistinct :=
    certificate_inputs_distinct twoPointFamily twoPointCertificate
  minimumInputCount := mixed_family_requires_two_inputs
    twoPointFamily two_point_is_mixed
  finiteExhaustion := classifier_exhaustive
  finiteVacuityExact := classify_not_mixed_iff_constant
  fin3AllFunctionsRepresentedUniquely := fin3_every_gate_has_unique_code
  fin3CountsExact := fin3_exact_class_counts
  estateSweepClaimed := false
  estateSweepOpen := rfl
  externalGateSemanticsClaimed := false
  externalGateSemanticsOpen := rfl
  unrestrictedInputIndependenceClaimed := false
  unrestrictedInputIndependenceOpen := rfl
  exponentialLowerBoundClaimed := false
  exponentialLowerBoundOpen := rfl
  unrestrictedNumericQueryLowerBoundClaimed := false
  unrestrictedNumericQueryLowerBoundOpen := rfl
  antiCheatLawPromoted := false
  antiCheatLawPromotionOpen := rfl
  wgocCompositionClaimed := false
  wgocCompositionOpen := rfl
  primitiveDifferencePromotedBeyondLocalOutcomes := false
  primitiveDifferencePromotionOpen := rfl
  authorityEffect := .none
  authorityNone := rfl

#print axioms classify_empty_iff
#print axioms classify_allPass_iff
#print axioms classify_allFail_iff
#print axioms classify_mixed_iff
#print axioms classify_not_mixed_iff_constant
#print axioms classifier_exhaustive
#print axioms mixed_requires_two_outcomes
#print axioms scan_mixed_iff_certificate
#print axioms certificate_inputs_distinct
#print axioms mixed_family_requires_two_inputs
#print axioms finite_scan_exhaustion
#print axioms finite_gate_vacuous_iff_not_mixed
#print axioms queried_outcomes_agree_when_failure_is_omitted
#print axioms omitted_input_can_hide_failure
#print axioms gate_outcome_zeroRel_iff
#print axioms gate_outcome_delta_true_iff_ne
#print axioms certificate_pair_is_mixed
#print axioms certificate_difference_nonzero
#print axioms two_point_is_mixed
#print axioms two_point_nonzero_pair
#print axioms two_point_certificate_is_minimal
#print axioms fin3Gate_fin3CodeOf
#print axioms fin3CodeOf_fin3Gate
#print axioms fin3_every_gate_has_unique_code
#print axioms fin3_each_gate_classified_exactly
#print axioms fin3_exact_class_counts
#print axioms fin3_all_functions_exact_class_counts
#print axioms finiteGateVacuitySurface

end GateVacuityW810
end OmegaWorld
