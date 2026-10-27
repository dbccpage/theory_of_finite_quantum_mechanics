/- Imported so that this repository carries its own Lean evidence.
   Original sha256: 43905002cf5a62655fcd0a088723bc0f7f19f5bc69a101fabb5657c49f79acb2 (bytes as found)
   Imported on    : 2026-10-23
   Module         : Imported.LegacyTopLevel.TerminalizerPolicy
   Reason         : S(n)
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   Renamed        : 2026-10-27, directory and namespace names only (lean4/RENAMES.json).
   AuthorityEffect: None. -/
/-
Does not elaborate on the v4.34.0 package: that package does not depend on
Mathlib. `deriving Fintype` needs `Mathlib.Tactic.DeriveFintype` from the
v4.33.1 pin in `research_programs/mub6`. This file was not typechecked
against that build. Declarations below were not typechecked.
-/
import Mathlib.Tactic.DeriveFintype

/-!
Finite, deterministic terminal routing for PaperER007's concrete policy table.

`ValidatorReport` is a finite tagged union.  Its constructors are disjoint, so
the first applicable table row is represented without ambiguous overlapping
evidence.  Terminal classes are routing statuses only; none carries or creates
authority.
-/

namespace LggrFiniteConsequences

inductive TerminalClass where
  | certificate
  | refusal
  | repair
  | oracleNeeded
  deriving DecidableEq, Repr, Fintype

inductive ValidatorReport where
  | parseError
  | schemaInvalid
  | unsupportedSemantics (allowedOracleRoute : Bool)
  | evidenceCeilingExceeded
  | forbiddenMutation
  | unlicensedStructureMutation
  | tiePolicyMissing
  | terminalMismatch
  | suboptimal
  | missingWitness
  | repairableBoundaryViolation
  | localInvalidNoRepair
  | checked
      (localGreen : Bool) (globalGreen : Bool) (terminalClaimOK : Bool)
      (oracleRouteDeclared : Bool)
  | unmatched (oracleRouteDeclared : Bool)
  deriving DecidableEq, Repr

def allValidatorReports : List ValidatorReport :=
  [ .parseError
  , .schemaInvalid
  , .unsupportedSemantics false
  , .unsupportedSemantics true
  , .evidenceCeilingExceeded
  , .forbiddenMutation
  , .unlicensedStructureMutation
  , .tiePolicyMissing
  , .terminalMismatch
  , .suboptimal
  , .missingWitness
  , .repairableBoundaryViolation
  , .localInvalidNoRepair
  , .checked false false false false
  , .checked false false false true
  , .checked false false true false
  , .checked false false true true
  , .checked false true false false
  , .checked false true false true
  , .checked false true true false
  , .checked false true true true
  , .checked true false false false
  , .checked true false false true
  , .checked true false true false
  , .checked true false true true
  , .checked true true false false
  , .checked true true false true
  , .checked true true true false
  , .checked true true true true
  , .unmatched false
  , .unmatched true ]

theorem validator_report_exhaustive (report : ValidatorReport) :
    report ∈ allValidatorReports := by
  cases report with
  | unsupportedSemantics route =>
      cases route <;> simp [allValidatorReports]
  | checked localGreen globalGreen terminalClaimOK oracleRouteDeclared =>
      cases localGreen <;> cases globalGreen <;> cases terminalClaimOK <;>
        cases oracleRouteDeclared <;> simp [allValidatorReports]
  | unmatched route =>
      cases route <;> simp [allValidatorReports]
  | parseError => simp [allValidatorReports]
  | schemaInvalid => simp [allValidatorReports]
  | evidenceCeilingExceeded => simp [allValidatorReports]
  | forbiddenMutation => simp [allValidatorReports]
  | unlicensedStructureMutation => simp [allValidatorReports]
  | tiePolicyMissing => simp [allValidatorReports]
  | terminalMismatch => simp [allValidatorReports]
  | suboptimal => simp [allValidatorReports]
  | missingWitness => simp [allValidatorReports]
  | repairableBoundaryViolation => simp [allValidatorReports]
  | localInvalidNoRepair => simp [allValidatorReports]

instance : Fintype ValidatorReport :=
  Fintype.ofList allValidatorReports validator_report_exhaustive

/-- The three checked gates required by the certificate row. -/
def CertificateGates : ValidatorReport → Prop
  | .checked localGreen globalGreen terminalClaimOK _ =>
      localGreen = true ∧ globalGreen = true ∧ terminalClaimOK = true
  | _ => False

/-- Reports captured by a refusal row above the certificate row. -/
def RefusalPreemption : ValidatorReport → Prop
  | .parseError
  | .schemaInvalid
  | .forbiddenMutation
  | .unlicensedStructureMutation
  | .localInvalidNoRepair => True
  | _ => False

/-- Reports captured by a repair row above the certificate row. -/
def RepairPreemption : ValidatorReport → Prop
  | .evidenceCeilingExceeded
  | .tiePolicyMissing
  | .terminalMismatch
  | .suboptimal
  | .missingWitness
  | .repairableBoundaryViolation => True
  | _ => False

/--
The concrete first-match table.  Earlier constructors are the table's rows
1--6; `checked` is row 7; the two Boolean fallbacks implement row 8.
-/
def terminalize : ValidatorReport → TerminalClass
  | .parseError
  | .schemaInvalid => .refusal
  | .unsupportedSemantics true => .oracleNeeded
  | .unsupportedSemantics false => .refusal
  | .evidenceCeilingExceeded => .repair
  | .forbiddenMutation
  | .unlicensedStructureMutation => .refusal
  | .tiePolicyMissing
  | .terminalMismatch
  | .suboptimal
  | .missingWitness
  | .repairableBoundaryViolation => .repair
  | .localInvalidNoRepair => .refusal
  | .checked true true true _ => .certificate
  | .checked _ _ _ true => .oracleNeeded
  | .checked _ _ _ false => .refusal
  | .unmatched true => .oracleNeeded
  | .unmatched false => .refusal

theorem terminalizer_total (report : ValidatorReport) :
    ∃ terminal : TerminalClass, terminalize report = terminal :=
  ⟨terminalize report, rfl⟩

theorem terminalizer_deterministic
    (report : ValidatorReport) (left right : TerminalClass)
    (hLeft : terminalize report = left) (hRight : terminalize report = right) :
    left = right := by
  rw [← hLeft, ← hRight]

/-- A certificate cannot bypass any of its three checked gates. -/
theorem certificate_implies_every_gate (report : ValidatorReport)
    (hCertificate : terminalize report = TerminalClass.certificate) :
    CertificateGates report := by
  cases report with
  | unsupportedSemantics route =>
      cases route <;> cases hCertificate
  | checked localGreen globalGreen terminalClaimOK oracleRouteDeclared =>
      cases localGreen <;> cases globalGreen <;> cases terminalClaimOK <;>
        cases oracleRouteDeclared <;> simp [terminalize, CertificateGates] at *
  | unmatched route =>
      cases route <;> cases hCertificate
  | parseError => cases hCertificate
  | schemaInvalid => cases hCertificate
  | evidenceCeilingExceeded => cases hCertificate
  | forbiddenMutation => cases hCertificate
  | unlicensedStructureMutation => cases hCertificate
  | tiePolicyMissing => cases hCertificate
  | terminalMismatch => cases hCertificate
  | suboptimal => cases hCertificate
  | missingWitness => cases hCertificate
  | repairableBoundaryViolation => cases hCertificate
  | localInvalidNoRepair => cases hCertificate

theorem refusal_rows_preempt_certificate (report : ValidatorReport)
    (hRefusal : RefusalPreemption report) :
    terminalize report = TerminalClass.refusal := by
  cases report <;> simp [RefusalPreemption, terminalize] at *

theorem repair_rows_preempt_certificate (report : ValidatorReport)
    (hRepair : RepairPreemption report) :
    terminalize report = TerminalClass.repair := by
  cases report <;> simp [RepairPreemption, terminalize] at *

theorem refusal_or_repair_preempts_certificate (report : ValidatorReport)
    (hPreemption : RefusalPreemption report ∨ RepairPreemption report) :
    terminalize report ≠ TerminalClass.certificate := by
  rcases hPreemption with hRefusal | hRepair
  · rw [refusal_rows_preempt_certificate report hRefusal]
    exact TerminalClass.noConfusion
  · rw [repair_rows_preempt_certificate report hRepair]
    exact TerminalClass.noConfusion

#print axioms LggrFiniteConsequences.validator_report_exhaustive
#print axioms LggrFiniteConsequences.terminalizer_total
#print axioms LggrFiniteConsequences.terminalizer_deterministic
#print axioms LggrFiniteConsequences.certificate_implies_every_gate
#print axioms LggrFiniteConsequences.refusal_rows_preempt_certificate
#print axioms LggrFiniteConsequences.repair_rows_preempt_certificate
#print axioms LggrFiniteConsequences.refusal_or_repair_preempts_certificate

end LggrFiniteConsequences
