/-!
GOMC-13: obstruction branch search is proposal structure, not authority.

The Rust engine `omega_engines::obstruction_branch_search` evaluates finite
candidate transitions by lexicographic obstruction descent `(Phi_1, Gamma_2,
Xi)` and mirrors positive improvement mass into a branch-density diagnostic.
This Lean target captures the firewall: strict descent proposals, branch ranks,
and proposal masses do not mint authority unless the separate descent terminal
gate closes.
-/

namespace QM

namespace GOMC13

inductive AuthorityEffect
  | none
  | certified
deriving DecidableEq, Repr

inductive ImprovementTier
  | phi1
  | gamma2
  | xi
  | none
deriving DecidableEq, Repr

/-- One candidate branch in an obstruction search report. -/
structure BranchCandidate where
  label : Nat
  strictDescent : Bool
  proposalMass : Nat
  rank : Nat
  improvementTier : ImprovementTier
  authorityEffect : AuthorityEffect
deriving DecidableEq, Repr

def CandidateDiagnosticOnly (c : BranchCandidate) : Prop :=
  c.authorityEffect = AuthorityEffect.none

def AllCandidatesDiagnosticOnly : List BranchCandidate -> Prop
  | [] => True
  | c :: rest =>
      CandidateDiagnosticOnly c ∧ AllCandidatesDiagnosticOnly rest

/-- A finite search trace plus the separate terminal authority gate. -/
structure BranchSearchTrace where
  candidates : List BranchCandidate
  descentGateClosed : Bool
  terminalAuthority : Bool
deriving DecidableEq, Repr

def SearchDiagnosticOnly (t : BranchSearchTrace) : Prop :=
  AllCandidatesDiagnosticOnly t.candidates ∧ t.descentGateClosed = false

def DescentAuthority (t : BranchSearchTrace) : Prop :=
  t.descentGateClosed = true ∧ t.terminalAuthority = true

def ReportAuthority (t : BranchSearchTrace) : AuthorityEffect :=
  if t.descentGateClosed && t.terminalAuthority then
    AuthorityEffect.certified
  else
    AuthorityEffect.none

/--
GOMC-13 firewall: a branch-search trace whose candidates are diagnostic-only
and whose descent gate is closed cannot be a descent authority terminal.
-/
theorem searchDiagnosticOnly_no_descentAuthority
    {t : BranchSearchTrace} (h : SearchDiagnosticOnly t) :
    ¬ DescentAuthority t := by
  intro hAuth
  exact Bool.noConfusion (h.2.symm.trans hAuth.1)

/--
Even a strict descent proposal remains non-authority when its candidate record
has authority effect `none`.
-/
theorem strictDescentProposal_not_authority
    {c : BranchCandidate}
    (hDiag : CandidateDiagnosticOnly c)
    (_hStrict : c.strictDescent = true) :
    c.authorityEffect ≠ AuthorityEffect.certified := by
  intro hCert
  rw [CandidateDiagnosticOnly] at hDiag
  rw [hDiag] at hCert
  contradiction

/--
Branch ranking/proposal mass is irrelevant to authority while the terminal gate
is closed: replacing the ranked candidate list preserves the authority-null
report.
-/
theorem replacingRankedCandidates_preserves_closedGateFirewall
    (xs ys : List BranchCandidate) :
    ReportAuthority
        { candidates := xs, descentGateClosed := false, terminalAuthority := false } =
      ReportAuthority
        { candidates := ys, descentGateClosed := false, terminalAuthority := false } := by
  rfl

def strictDescentProposal : BranchCandidate where
  label := 0
  strictDescent := true
  proposalMass := 3
  rank := 1
  improvementTier := ImprovementTier.phi1
  authorityEffect := AuthorityEffect.none

def rejectedProbe : BranchCandidate where
  label := 1
  strictDescent := false
  proposalMass := 0
  rank := 0
  improvementTier := ImprovementTier.none
  authorityEffect := AuthorityEffect.none

def branchSearchWitness : BranchSearchTrace where
  candidates := [strictDescentProposal, rejectedProbe]
  descentGateClosed := false
  terminalAuthority := false

theorem strictDescentProposal_is_diagnostic :
    CandidateDiagnosticOnly strictDescentProposal := by
  rfl

theorem rejectedProbe_is_diagnostic :
    CandidateDiagnosticOnly rejectedProbe := by
  rfl

theorem branchSearchWitness_is_diagnosticOnly :
    SearchDiagnosticOnly branchSearchWitness := by
  constructor
  · exact ⟨strictDescentProposal_is_diagnostic,
      rejectedProbe_is_diagnostic, True.intro⟩
  · rfl

theorem strictBranchSearchWitness_no_authority :
    ¬ DescentAuthority branchSearchWitness := by
  exact searchDiagnosticOnly_no_descentAuthority
    branchSearchWitness_is_diagnosticOnly

end GOMC13

end QM

#print axioms QM.GOMC13.searchDiagnosticOnly_no_descentAuthority
#print axioms QM.GOMC13.strictDescentProposal_not_authority
#print axioms QM.GOMC13.replacingRankedCandidates_preserves_closedGateFirewall
#print axioms QM.GOMC13.strictBranchSearchWitness_no_authority
