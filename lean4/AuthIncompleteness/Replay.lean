/-
Provenance (recovery, 2026-10-21)
  source    : C:\.ana\coda_university\coda_research\authorization_an_incompleteness_theory\formal\replay_packet_binding_models.lean
  recovered : 2026-10-21
  status    : ported to Lean 4.35.0; statements unchanged
  module    : AuthIncompleteness.Replay
-/
/-!
# Finite replay-packet binding model

Paper key: `authorization_an_incompleteness_theory`

This small model makes a replay boundary structural. A trust root is supplied
outside a submission; a receipt binds that root and the exact submission; and
replay refuses a substituted submission before it treats any self-declared pass
flag as evidence. The terminal policy is deliberately separate from verification.

The equality used here is structural equality, not a cryptographic digest. This
is a finite model of what a real packet must bind. It does not establish hash
collision resistance, verifier soundness, custody, physical independence, or a
production authorization protocol.

AuthorityEffect: None.
-/

namespace AuthorizationIncompleteness.ReplayPacketBindingModels

/-- Version labels are finite stand-ins for schema, checker, and contract
    version bindings. -/
inductive Version where
  | v1
  | v2
  deriving DecidableEq, Repr

/-- The behavior selected by a trusted checker in the finite model. -/
inductive CheckerTag where
  | acceptsTrue
  | acceptsFalse
  deriving DecidableEq, Repr

/-- The Bool-valued contract being checked. -/
inductive ContractTag where
  | requiresTrue
  | requiresFalse
  deriving DecidableEq, Repr

/-- Verification and terminalization remain distinct operations. -/
inductive TerminalPolicy where
  | authorizeOnVerified
  | leaveVerifiedOpen
  deriving DecidableEq, Repr

/-- The externally fixed protocol data. It is an input to verification, not a
    field that a proposal chooses at replay time. -/
structure TrustRoot where
  schemaVersion : Version
  checkerTag : CheckerTag
  checkerVersion : Version
  contractTag : ContractTag
  contractVersion : Version
  policy : TerminalPolicy
  deriving DecidableEq, Repr

/-- The source-controlled submission. `selfPass` is intentionally present but
    ignored by the trusted evaluator. -/
structure Submission where
  payload : Bool
  claimedSchemaVersion : Version
  claimedCheckerTag : CheckerTag
  claimedCheckerVersion : Version
  claimedContractTag : ContractTag
  claimedContractVersion : Version
  selfPass : Bool
  deriving DecidableEq, Repr

/-- Outcomes of the finite deterministic verifier. -/
inductive Verification where
  | bindingRejected
  | checkerMismatch
  | contractRejected
  | verified
  deriving DecidableEq, Repr

/-- A policy effect is intentionally later than the verifier outcome. -/
inductive Terminal where
  | rejected
  | open
  | authorized
  deriving DecidableEq, Repr

/-- The trusted checker semantics in this finite carrier. -/
def checkerResult (tag : CheckerTag) (payload : Bool) : Bool :=
  match tag with
  | .acceptsTrue => payload
  | .acceptsFalse => !payload

/-- The contract semantics in this finite carrier. -/
def contractValid (tag : ContractTag) (payload : Bool) : Bool :=
  match tag with
  | .requiresTrue => payload
  | .requiresFalse => !payload

/-- All replay-relevant identifiers must agree with the externally supplied
    root before the checker result is considered. -/
def bindingsMatch (root : TrustRoot) (submission : Submission) : Bool :=
  (submission.claimedSchemaVersion == root.schemaVersion) &&
    (submission.claimedCheckerTag == root.checkerTag) &&
    (submission.claimedCheckerVersion == root.checkerVersion) &&
    (submission.claimedContractTag == root.contractTag) &&
    (submission.claimedContractVersion == root.contractVersion)

/-- The source's `selfPass` flag has no input position in this evaluation. -/
def verify (root : TrustRoot) (submission : Submission) : Verification :=
  if bindingsMatch root submission then
    if checkerResult root.checkerTag submission.payload ==
        contractValid root.contractTag submission.payload then
      if contractValid root.contractTag submission.payload then
        .verified
      else
        .contractRejected
    else
      .checkerMismatch
  else
    .bindingRejected

/-- Terminal policy consumes a verified local result; it does not redefine the
    result of verification. -/
def terminalize (policy : TerminalPolicy) (verification : Verification) : Terminal :=
  match verification with
  | .verified =>
    match policy with
    | .authorizeOnVerified => .authorized
    | .leaveVerifiedOpen => .open
  | .bindingRejected => .rejected
  | .checkerMismatch => .rejected
  | .contractRejected => .rejected

/-- A receipt binds one root, one exact source submission, and the result that
    the fixed verifier obtained for that pair. -/
structure ReplayReceipt where
  root : TrustRoot
  boundSubmission : Submission
  outcome : Verification
  deriving DecidableEq, Repr

/-- Issuing a receipt is not authorization. It records the local verifier's
    outcome for the exact input pair. -/
def issueReceipt (root : TrustRoot) (submission : Submission) : ReplayReceipt where
  root := root
  boundSubmission := submission
  outcome := verify root submission

/-- The replay surface distinguishes substitution from a changed local outcome. -/
inductive ReplayStatus where
  | bindingRejected
  | outcomeMismatch
  | replayed (outcome : Verification)
  deriving DecidableEq, Repr

/-- Replay first checks the exact bound source submission, then recomputes the
    verifier outcome under the bound root. -/
def replay (receipt : ReplayReceipt) (observed : Submission) : ReplayStatus :=
  if observed = receipt.boundSubmission then
    if verify receipt.root observed == receipt.outcome then
      .replayed receipt.outcome
    else
      .outcomeMismatch
  else
    .bindingRejected

/-- A coherent root for the contract "the payload is true." -/
def authorizeTrueRoot : TrustRoot where
  schemaVersion := .v1
  checkerTag := .acceptsTrue
  checkerVersion := .v1
  contractTag := .requiresTrue
  contractVersion := .v1
  policy := .authorizeOnVerified

/-- The same trusted check can have a policy that keeps its result open. -/
def openTrueRoot : TrustRoot where
  schemaVersion := .v1
  checkerTag := .acceptsTrue
  checkerVersion := .v1
  contractTag := .requiresTrue
  contractVersion := .v1
  policy := .leaveVerifiedOpen

/-- A correctly bound submission. The source does not need to assert success. -/
def validSubmission : Submission where
  payload := true
  claimedSchemaVersion := .v1
  claimedCheckerTag := .acceptsTrue
  claimedCheckerVersion := .v1
  claimedContractTag := .requiresTrue
  claimedContractVersion := .v1
  selfPass := false

/-- An invalid content payload whose source nevertheless asserts `selfPass`. -/
def invalidSelfPassingSubmission : Submission where
  payload := false
  claimedSchemaVersion := .v1
  claimedCheckerTag := .acceptsTrue
  claimedCheckerVersion := .v1
  claimedContractTag := .requiresTrue
  claimedContractVersion := .v1
  selfPass := true

/-- A source tries to replace the trusted checker by one that accepts false. -/
def checkerTamperedSubmission : Submission where
  payload := false
  claimedSchemaVersion := .v1
  claimedCheckerTag := .acceptsFalse
  claimedCheckerVersion := .v1
  claimedContractTag := .requiresTrue
  claimedContractVersion := .v1
  selfPass := true

/-- A source tries to replace the contract version after a receipt is issued. -/
def contractVersionTamperedSubmission : Submission where
  payload := true
  claimedSchemaVersion := .v1
  claimedCheckerTag := .acceptsTrue
  claimedCheckerVersion := .v1
  claimedContractTag := .requiresTrue
  claimedContractVersion := .v2
  selfPass := false

/-- A source tries to replace the schema version after a receipt is issued. -/
def schemaVersionTamperedSubmission : Submission where
  payload := true
  claimedSchemaVersion := .v2
  claimedCheckerTag := .acceptsTrue
  claimedCheckerVersion := .v1
  claimedContractTag := .requiresTrue
  claimedContractVersion := .v1
  selfPass := false

theorem trusted_checker_matches_true_contract (payload : Bool) :
    checkerResult authorizeTrueRoot.checkerTag payload =
      contractValid authorizeTrueRoot.contractTag payload := by
  cases payload <;> rfl

theorem self_pass_cannot_authorize_invalid_content :
    verify authorizeTrueRoot invalidSelfPassingSubmission = .contractRejected := by
  rfl

theorem checker_substitution_is_binding_rejected :
    verify authorizeTrueRoot checkerTamperedSubmission = .bindingRejected := by
  rfl

theorem contract_version_substitution_is_binding_rejected :
    verify authorizeTrueRoot contractVersionTamperedSubmission = .bindingRejected := by
  rfl

theorem schema_version_substitution_is_binding_rejected :
    verify authorizeTrueRoot schemaVersionTamperedSubmission = .bindingRejected := by
  rfl

theorem issued_receipt_replays_exact_submission :
    replay (issueReceipt authorizeTrueRoot validSubmission) validSubmission =
      .replayed .verified := by
  rfl

theorem replay_rejects_payload_substitution :
    replay (issueReceipt authorizeTrueRoot validSubmission)
      invalidSelfPassingSubmission = .bindingRejected := by
  rfl

theorem replayed_status_requires_bound_submission
    (receipt : ReplayReceipt) (observed : Submission) (outcome : Verification) :
    replay receipt observed = .replayed outcome ->
      observed = receipt.boundSubmission := by
  intro replayed
  by_cases h : observed = receipt.boundSubmission
  · exact h
  · unfold replay at replayed
    rw [if_neg h] at replayed
    cases replayed

theorem terminal_policy_is_not_selected_by_verification :
    terminalize authorizeTrueRoot.policy .verified = .authorized ∧
      terminalize openTrueRoot.policy .verified = .open := by
  exact ⟨rfl, rfl⟩

end AuthorizationIncompleteness.ReplayPacketBindingModels

#print axioms
  AuthorizationIncompleteness.ReplayPacketBindingModels.self_pass_cannot_authorize_invalid_content
#print axioms
  AuthorizationIncompleteness.ReplayPacketBindingModels.checker_substitution_is_binding_rejected
#print axioms
  AuthorizationIncompleteness.ReplayPacketBindingModels.contract_version_substitution_is_binding_rejected
#print axioms
  AuthorizationIncompleteness.ReplayPacketBindingModels.schema_version_substitution_is_binding_rejected
#print axioms
  AuthorizationIncompleteness.ReplayPacketBindingModels.issued_receipt_replays_exact_submission
#print axioms
  AuthorizationIncompleteness.ReplayPacketBindingModels.replayed_status_requires_bound_submission
#print axioms
  AuthorizationIncompleteness.ReplayPacketBindingModels.terminal_policy_is_not_selected_by_verification
