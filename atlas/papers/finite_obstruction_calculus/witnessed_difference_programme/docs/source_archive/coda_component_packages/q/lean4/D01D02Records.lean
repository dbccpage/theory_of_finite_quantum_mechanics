/-!
# CODA-Q D01/D02: Core Carrier Records, Descent Packets & Admission Debt

Formalizes:
1. `QuarantineStatus` lifecycle receipts for frontier probes.
2. `ClaimMachineStatus` typed receipts for automated exploration machines.
3. `AuthorityTerminal` disjointness types (`QOrAuthority`, `ClaimMachineOrAuthority`).
4. 5-Field `DescentPacket` structure $(K, E, V, \tau, \Lambda)$.
5. 7-Guard `HaltGuards` conjunction structure ($g_1 \dots g_7$).
6. Proof-relevant `QAdmissionEvidence` and `CompleteAdmissionDebt` predicate.
7. `QHeldAdmissible` and `TerminalWithinScopeAdmissible` status boundaries.

AuthorityEffect: None.
-/

namespace CodaQ

/-- Lifecycle receipt status of a frontier probe. -/
inductive QuarantineStatus where
  | toy_descent
  | partial_descent
  | representation_only
  | obstruction_found
  | no_known_lift
  | survivor
  | refuted
  | do_not_publish_as_claim
  deriving DecidableEq, Repr

/-- Claim-machine outputs are typed receipts, not global truth-oracle answers. -/
inductive ClaimMachineStatus where
  | proven_under_packet
  | refuted_under_packet
  | partial_descent
  | representation_only
  | obstruction_found
  | non_identifiable
  | no_known_lift
  | needs_human_authority
  deriving DecidableEq, Repr

/-- A separate authority lane, intentionally disjoint from Q receipts. -/
inductive AuthorityTerminal where
  | accepted
  deriving DecidableEq, Repr

/-- Disjoint sum separating Q receipts from authority terminals. -/
inductive QOrAuthority where
  | q : QuarantineStatus → QOrAuthority
  | authority : AuthorityTerminal → QOrAuthority
  deriving DecidableEq, Repr

/-- Disjoint sum separating claim-machine statuses from authority terminals. -/
inductive ClaimMachineOrAuthority where
  | claim : ClaimMachineStatus → ClaimMachineOrAuthority
  | authority : AuthorityTerminal → ClaimMachineOrAuthority
  deriving DecidableEq, Repr

/-- 5-Field descent packet (K, E, V, tau, Lambda). -/
structure DescentPacket where
  carrier_k : String
  evaluator_class_e : List String
  verifier_v : String
  terminalizer_tau : String
  discipline_lambda : String
  deriving DecidableEq, Repr

/-- 7-Guard Halt Witness Conjunction: IsAuth(t) <-> BigAnd_{i=1}^7 g_i(t). -/
structure HaltGuards where
  accepted : Bool
  deterministic : Bool
  zero_residual_mass : Bool
  skeleton_preserving : Bool
  exhaustive : Bool
  no_pending_lift : Bool
  no_refusal : Bool
  deriving DecidableEq, Repr

/-- Exact boolean conjunction of the seven halt guards. -/
def HaltGuards.is_auth (g : HaltGuards) : Bool :=
  g.accepted &&
  g.deterministic &&
  g.zero_residual_mass &&
  g.skeleton_preserving &&
  g.exhaustive &&
  g.no_pending_lift &&
  g.no_refusal

/-- The proof-relevant evidence required by the Q admission rule. -/
structure QAdmissionEvidence where
  finite_shadow : Prop
  refinement_relation : Prop
  declared_topology : Prop
  convergence_certificate_route : Prop
  descent_trigger : Prop
  witness_support : Prop

/-- Complete Q admission debt: all 5 mandatory admission debt fields present. -/
def CompleteAdmissionDebt (evidence : QAdmissionEvidence) : Prop :=
  evidence.finite_shadow ∧
  evidence.refinement_relation ∧
  evidence.declared_topology ∧
  evidence.convergence_certificate_route ∧
  evidence.descent_trigger

/-- `QHeld` requires complete finite-shadow admission debt. -/
def QHeldAdmissible (evidence : QAdmissionEvidence) : Prop :=
  CompleteAdmissionDebt evidence

/-- `TerminalWithinScope` additionally requires finite witness support. -/
def TerminalWithinScopeAdmissible (evidence : QAdmissionEvidence) : Prop :=
  QHeldAdmissible evidence ∧ evidence.witness_support

end CodaQ
