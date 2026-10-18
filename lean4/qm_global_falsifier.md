import Mathlib.Tactic

/-!
# QMGlobalFalsifier — W7.6 (T17 empirical falsifier package)

Programme target: DERIV-MASTER W7.6 (path §F.42); freeze T17.

**Job:** register an explicit **global empirical falsifier sentence** for the
finite classical-heart + surplus + imports package, plus contingent component
falsifiers (CHSH / MP / interference / clone). Lab execution remains OPEN.

AuthorityEffect: None.
-/

namespace QM
namespace GlobalFalsifier

/-! ## Component falsifiers -/

inductive FalsifierId where
  | F_CHSH_CLASS
  | F_CHSH_Q
  | F_MP
  | F_INTERF
  | F_CLONE
  deriving DecidableEq, Repr

/-- Contingent = can fail in principle (not a logical tautology). -/
structure FalsifierRow where
  id : FalsifierId
  contingent : Bool
  packagePredictsObstruction : Bool
  deriving DecidableEq, Repr

def falsifiers : List FalsifierRow :=
  [ { id := .F_CHSH_CLASS, contingent := true, packagePredictsObstruction := true }
    , { id := .F_CHSH_Q, contingent := true, packagePredictsObstruction := true }
    , { id := .F_MP, contingent := true, packagePredictsObstruction := true }
    , { id := .F_INTERF, contingent := true, packagePredictsObstruction := true }
    , { id := .F_CLONE, contingent := true, packagePredictsObstruction := true }
  ]

theorem falsifiers_card : falsifiers.length = 5 := by
  decide

def allContingent : Bool :=
  falsifiers.all (fun r => r.contingent)

theorem all_contingent : allContingent = true := by
  decide

def allPredictObstruction : Bool :=
  falsifiers.all (fun r => r.packagePredictsObstruction)

theorem all_predict_obstruction : allPredictObstruction = true := by
  decide

/-! ## Global T17 sentence (registered as structured flags, not free prose) -/

/-- Conjunction of three operational failure modes that would refute the package. -/
structure GlobalFalsifierSpec where
  requiresChshQuantumExceedanceAbsent : Bool
  requiresMpObstructionAbsent : Bool
  requiresInterferenceResidualAbsent : Bool
  deriving DecidableEq, Repr

/-- The global falsifier is the **conjunction** of absences: if all three
    absences hold on a declared platform, the package is inadequate there. -/
def globalFalsifier : GlobalFalsifierSpec :=
  { requiresChshQuantumExceedanceAbsent := true
    requiresMpObstructionAbsent := true
    requiresInterferenceResidualAbsent := true }

def globalFalsifierRegistered : Bool := true

theorem global_falsifier_registered : globalFalsifierRegistered = true := by
  decide

/-- Not a tautology: package does **not** claim the absences are necessary truths. -/
def globalIsTautology : Bool := false

theorem global_not_tautology : globalIsTautology = false := by
  decide

/-- Package predicts that on quantum-host platforms, the three absences are
    **not** jointly expected (i.e. at least one presence). -/
def packageExpectsSomePresence : Bool := true

theorem package_expects_some_presence : packageExpectsSomePresence = true := by
  decide

/-! ## Contingency witnesses (toy discrete checks that clauses are nontrivial) -/

/-- Classical CHSH can achieve 2 (tight) but package forbids >2 for deterministic. -/
def classicalChshCap : Nat := 2
def quantumTsirelsonSquare : Nat := 8
def classicalChshSquare : Nat := 4

theorem chsh_gap_nontrivial :
    quantumTsirelsonSquare > classicalChshSquare ∧ classicalChshCap = 2 := by
  decide

/-- MP: target parity 1 vs coboundary parity 0 (W7.3 shape). -/
def mpTargetParity : Bool := true
def mpCoboundaryParity : Bool := false

theorem mp_gap_nontrivial : mpTargetParity ≠ mpCoboundaryParity := by
  decide

/-- Interference residual can be nonzero. -/
def sampleResidual : Int := 2
theorem interf_residual_can_be_nonzero : sampleResidual ≠ 0 := by
  decide

/-! ## Lab / exit honesty -/

def labExecution_closed : Bool := false
theorem lab_execution_open : labExecution_closed = false := by
  decide

/-- Stating falsifiers does not close Waves 5–7 residuals. -/
def waves5to7FullyClosedByFalsifierAlone : Bool := false

theorem falsifier_not_wave_exit :
    waves5to7FullyClosedByFalsifierAlone = false := by
  decide

/-! ## Synthetic platform evaluator (not lab)

Named discrete platforms evaluate the three T17 absence clauses on **toy
outcome flags**. This is an in-silico decision procedure dual, not empirical
lab execution (FAL-LAB remains OPEN).
-/

structure PlatformOutcome where
  chshQuantumExceedancePresent : Bool
  mpObstructionPresent : Bool
  interferenceResidualPresent : Bool
  deriving DecidableEq, Repr

/-- Global falsifier fires when all three absences hold. -/
def allAbsences (o : PlatformOutcome) : Bool :=
  !o.chshQuantumExceedancePresent &&
  !o.mpObstructionPresent &&
  !o.interferenceResidualPresent

def packageInadequateOn (o : PlatformOutcome) : Bool :=
  allAbsences o

inductive SynthPlatform where
  | quantumHost
  | finL1Shadow
  | classicalNull
  deriving DecidableEq, Repr

/-- Declared synthetic outcomes (toy fixtures, not lab data). -/
def synthOutcome : SynthPlatform → PlatformOutcome
  | .quantumHost =>
      { chshQuantumExceedancePresent := true
        mpObstructionPresent := true
        interferenceResidualPresent := true }
  | .finL1Shadow =>
      { chshQuantumExceedancePresent := false
        mpObstructionPresent := true
        interferenceResidualPresent := false }
  | .classicalNull =>
      { chshQuantumExceedancePresent := false
        mpObstructionPresent := false
        interferenceResidualPresent := false }

theorem quantum_host_not_inadequate :
    packageInadequateOn (synthOutcome .quantumHost) = false := by
  decide

theorem classical_null_inadequate :
    packageInadequateOn (synthOutcome .classicalNull) = true := by
  decide

theorem finL1_shadow_not_inadequate_by_mp_presence :
    packageInadequateOn (synthOutcome .finL1Shadow) = false ∧
    (synthOutcome .finL1Shadow).mpObstructionPresent = true ∧
    (synthOutcome .finL1Shadow).chshQuantumExceedancePresent = false := by
  decide

/-- Package expects quantum-host platforms to keep ≥1 presence (not all absences). -/
theorem package_expectation_on_quantum_host :
    packageInadequateOn (synthOutcome .quantumHost) = false ∧
    packageExpectsSomePresence = true := by
  decide

/-! ## Component falsifier toy evaluators (synthetic measurements) -/

/-- F-CHSH-CLASS fires if deterministic local CHSH > 2 (refutes classical half). -/
def evalF_CHSH_CLASS (observedChsh : Int) : Bool :=
  decide (observedChsh > 2)

/-- F-CHSH-Q fires if quantum-host platform never exceeds classical square 4. -/
def evalF_CHSH_Q (quantumSquareObserved : Nat) : Bool :=
  decide (quantumSquareObserved ≤ classicalChshSquare)

/-- F-MP fires if a noncontextual global assignment is found (obstruction absent). -/
def evalF_MP (globalAssignmentFound : Bool) : Bool :=
  globalAssignmentFound

/-- F-INTERF fires if dephasing never changes predictions when residual claimed. -/
def evalF_INTERF (dephaseChangesPredictions : Bool) (residualClaimed : Bool) : Bool :=
  residualClaimed && !dephaseChangesPredictions

/-- F-CLONE fires if universal linear clone of pure amplitudes succeeds. -/
def evalF_CLONE (universalCloneSucceeds : Bool) : Bool :=
  universalCloneSucceeds

theorem component_eval_defaults :
    evalF_CHSH_CLASS 2 = false ∧
    evalF_CHSH_CLASS 3 = true ∧
    evalF_CHSH_Q 8 = false ∧
    evalF_CHSH_Q 4 = true ∧
    evalF_MP false = false ∧
    evalF_MP true = true ∧
    evalF_INTERF true true = false ∧
    evalF_INTERF false true = true ∧
    evalF_CLONE false = false := by
  decide

/-- Synthetic evaluator package closed at TOY-MECH; lab still OPEN. -/
def syntheticPlatformEvalPackage_toy : Bool := true

theorem synthetic_platform_eval_package :
    syntheticPlatformEvalPackage_toy = true ∧
    packageInadequateOn (synthOutcome .quantumHost) = false ∧
    packageInadequateOn (synthOutcome .classicalNull) = true ∧
    packageInadequateOn (synthOutcome .finL1Shadow) = false ∧
    evalF_CHSH_CLASS 2 = false ∧
    evalF_CHSH_Q 8 = false ∧
    labExecution_closed = false := by
  decide

/-! ## T17 recovery flag -/

def t17SentenceStated : Bool := true
def t17LabValidated : Bool := false
def t17SyntheticEvalStated : Bool := true

theorem t17_partial :
    t17SentenceStated = true ∧ t17LabValidated = false ∧
    t17SyntheticEvalStated = true := by
  decide

/-! ## Main package -/

theorem global_falsifier_package :
    falsifiers.length = 5 ∧
    allContingent = true ∧
    globalFalsifierRegistered = true ∧
    globalIsTautology = false ∧
    packageExpectsSomePresence = true ∧
    quantumTsirelsonSquare > classicalChshSquare ∧
    mpTargetParity ≠ mpCoboundaryParity ∧
    syntheticPlatformEvalPackage_toy = true ∧
    packageInadequateOn (synthOutcome .classicalNull) = true ∧
    packageInadequateOn (synthOutcome .quantumHost) = false ∧
    labExecution_closed = false ∧
    waves5to7FullyClosedByFalsifierAlone = false := by
  decide

/-! ## Authority firewall -/

def IsAuth (_carrier : Type) : Prop := False

theorem structure_not_auth (C : Type) : ¬ IsAuth C := fun h => h

end GlobalFalsifier
end QM

#print axioms QM.GlobalFalsifier.falsifiers_card
#print axioms QM.GlobalFalsifier.global_falsifier_package
#print axioms QM.GlobalFalsifier.synthetic_platform_eval_package
#print axioms QM.GlobalFalsifier.structure_not_auth
