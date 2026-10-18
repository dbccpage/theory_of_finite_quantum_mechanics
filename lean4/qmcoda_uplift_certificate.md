/-!
# qmcoda_uplift_certificate

Formal Lean 4 definitions for the Nine Up-Lift Certificate Conditions
(U_k : MSS-k -> MSS-(k+1)) and the Real0 Carrier vs Residual Structure Firewall.

Schema-only module (no Mathlib / cochain imports required).

**Honesty (schema binding, not a completed uplift proof):**
Nine conditions use typed witness records carrying bound `HostReceipt` payloads
(receipt_id, kind, payload_digest, authority_effect) plus status flags.
A bare all-true boolean conjunction without nonempty receipt ids / kind match /
`authority_effect = "None"` cannot satisfy `allSatisfied`.

**OPEN residual:** binding these schema slots to **runtime host** receipts
(`omega_trace`, `omega_self_review`, host exhaustion/conservativity/replay
artifacts, etc.) remains **OPEN**. This module is schema binding only —
`payload_digest` is a placeholder hash string, not cryptographic authority.
`example_fixture_*` constructors are diagnostic fixtures, **not** a production
uplift proof.

AuthorityEffect: None — type definitions + schema validity only; uplift is not proved.
-/

namespace SharedKernel.QMCODA

/-- Certified Derivational Stage (MSS-k) -/
structure MssStage where
  stage_id : Nat
  grammar_id : String
  alphabet_finite : Bool
  equality_decidable : Bool
  deriving Repr

/-- Witnessed Primitive Difference -/
structure PrimitiveDifferenceWitness where
  delta_0_id : Nat
  is_non_contractible : Bool
  deriving Repr

/--
Minimal host-shaped receipt bound into each witness slot.

- `kind`: slot label, e.g. `"exhaustion" | "conservativity" | "replay" | ...`
- `payload_digest`: blake/placeholder hash string; **not** crypto authority
- `authority_effect`: must be `"None"` for schema validity in this module

Runtime host binding (omega_trace, self_review, …) remains **OPEN**.
-/
structure HostReceipt where
  receipt_id : String
  kind : String
  payload_digest : String
  authority_effect : String
  deriving Repr

/-- Canonical kind labels for the nine certificate slots. -/
def receiptKind.exhaustion : String := "exhaustion"
def receiptKind.refusal : String := "refusal"
def receiptKind.traceability : String := "traceability"
def receiptKind.preservation : String := "preservation"
def receiptKind.conservativity : String := "conservativity"
def receiptKind.obstruction_resolution : String := "obstruction_resolution"
def receiptKind.minimality : String := "minimality"
def receiptKind.replay : String := "replay"
def receiptKind.authority_fence : String := "authority_fence"

/-- Nonempty receipt id. -/
def HostReceipt.idNonempty (r : HostReceipt) : Bool :=
  decide (r.receipt_id.length > 0)

/-- Kind matches the expected slot label. -/
def HostReceipt.kindMatch (r : HostReceipt) (expected : String) : Bool :=
  decide (r.kind = expected)

/-- Authority fence: must be exactly `"None"`. -/
def HostReceipt.authorityNone (r : HostReceipt) : Bool :=
  decide (r.authority_effect = "None")

/--
Schema validity for a receipt in a named slot:
nonempty id, kind match, authority_effect = "None".
-/
def HostReceipt.schemaValid (r : HostReceipt) (expectedKind : String) : Bool :=
  r.idNonempty && r.kindMatch expectedKind && r.authorityNone

/-- 1. Exhaustion of same-level repairs (bound host receipt) -/
structure ExhaustionTrace where
  receipt : HostReceipt
  exhausted : Bool
  deriving Repr

def ExhaustionTrace.valid (w : ExhaustionTrace) : Bool :=
  HostReceipt.schemaValid w.receipt receiptKind.exhaustion && w.exhausted

/-- 2. Refusal / non-contractibility witness -/
structure RefusalWitness where
  receipt : HostReceipt
  refused : Bool
  deriving Repr

def RefusalWitness.valid (w : RefusalWitness) : Bool :=
  HostReceipt.schemaValid w.receipt receiptKind.refusal && w.refused

/-- 3. Generator traceability to obstruction -/
structure TraceabilityWitness where
  receipt : HostReceipt
  obstruction_id : String
  generator_id : String
  traced : Bool
  deriving Repr

def TraceabilityWitness.valid (w : TraceabilityWitness) : Bool :=
  HostReceipt.schemaValid w.receipt receiptKind.traceability &&
  decide (w.obstruction_id.length > 0) && decide (w.generator_id.length > 0) && w.traced

/-- 4. Preservation of prior stage judgments -/
structure PreservationWitness where
  receipt : HostReceipt
  preserved : Bool
  deriving Repr

def PreservationWitness.valid (w : PreservationWitness) : Bool :=
  HostReceipt.schemaValid w.receipt receiptKind.preservation && w.preserved

/-- 5. Conservativity of MSS-(k+1) over MSS-k -/
structure ConservativityWitness where
  receipt : HostReceipt
  conservative : Bool
  deriving Repr

def ConservativityWitness.valid (w : ConservativityWitness) : Bool :=
  HostReceipt.schemaValid w.receipt receiptKind.conservativity && w.conservative

/-- 6. Obstruction resolution / refinement (cochain evidence) -/
structure ObstructionResolutionWitness where
  receipt : HostReceipt
  resolved_or_refined : Bool
  deriving Repr

def ObstructionResolutionWitness.valid (w : ObstructionResolutionWitness) : Bool :=
  HostReceipt.schemaValid w.receipt receiptKind.obstruction_resolution &&
  w.resolved_or_refined

/-- 7. Generator minimality -/
structure MinimalityWitness where
  receipt : HostReceipt
  generator_id : String
  minimal : Bool
  deriving Repr

def MinimalityWitness.valid (w : MinimalityWitness) : Bool :=
  HostReceipt.schemaValid w.receipt receiptKind.minimality &&
  decide (w.generator_id.length > 0) && w.minimal

/-- 8. Replay / deterministic evaluation receipt -/
structure ReplayReceipt where
  receipt : HostReceipt
  replay_checked : Bool
  deterministic : Bool
  deriving Repr

def ReplayReceipt.valid (w : ReplayReceipt) : Bool :=
  HostReceipt.schemaValid w.receipt receiptKind.replay &&
  w.replay_checked && w.deterministic

/-- 9. Evidence level remains AuthorityEffect::None (bound fence receipt) -/
structure AuthorityFenceWitness where
  receipt : HostReceipt
  deriving Repr

def AuthorityFenceWitness.valid (w : AuthorityFenceWitness) : Bool :=
  HostReceipt.schemaValid w.receipt receiptKind.authority_fence

/--
The Nine Up-Lift Certificate Conditions (U_k : MSS-k -> MSS-(k+1)).

Typed witness slots — each carries a bound `HostReceipt`, not bare booleans alone.
-/
structure NineCertificateConditions (src dst : MssStage) where
  exhaustion : ExhaustionTrace
  refusal : RefusalWitness
  traceability : TraceabilityWitness
  preservation : PreservationWitness
  conservativity : ConservativityWitness
  obstruction_resolution : ObstructionResolutionWitness
  generator_minimality : MinimalityWitness
  replay : ReplayReceipt
  authority_fence : AuthorityFenceWitness

/-- All nine conditions satisfied (receipt schema + status flags) -/
def NineCertificateConditions.allSatisfied {src dst : MssStage}
    (c : NineCertificateConditions src dst) : Bool :=
  c.exhaustion.valid &&
  c.refusal.valid &&
  c.traceability.valid &&
  c.preservation.valid &&
  c.conservativity.valid &&
  c.obstruction_resolution.valid &&
  c.generator_minimality.valid &&
  c.replay.valid &&
  c.authority_fence.valid

/-- Status-bit projection only (does **not** check receipt schema — prefer `allSatisfied`) -/
def NineCertificateConditions.statusBits {src dst : MssStage}
    (c : NineCertificateConditions src dst) : List Bool :=
  [c.exhaustion.exhausted, c.refusal.refused, c.traceability.traced,
   c.preservation.preserved, c.conservativity.conservative,
   c.obstruction_resolution.resolved_or_refined, c.generator_minimality.minimal,
   c.replay.replay_checked && c.replay.deterministic,
   c.authority_fence.receipt.authorityNone]

/-- Collect the nine bound receipts (diagnostic / export surface). -/
def NineCertificateConditions.receipts {src dst : MssStage}
    (c : NineCertificateConditions src dst) : List HostReceipt :=
  [c.exhaustion.receipt, c.refusal.receipt, c.traceability.receipt,
   c.preservation.receipt, c.conservativity.receipt,
   c.obstruction_resolution.receipt, c.generator_minimality.receipt,
   c.replay.receipt, c.authority_fence.receipt]

/-- Real0 Firewall Boundary: Primitive Difference (+) Residual Structure -/
inductive Real0Structure
  | primitiveDifference (witness : PrimitiveDifferenceWitness)
  | residualCore (survivor_id : String)

/-!
## Diagnostic fixtures (NOT a production uplift proof)

`example_fixture_*` build a fully schema-valid `NineCertificateConditions`
with nine placeholder receipts. Host binding remains OPEN.
-/

/-- Diagnostic: build a placeholder host receipt for a named kind. -/
def example_fixture_hostReceipt (receiptId kind digest : String) : HostReceipt where
  receipt_id := receiptId
  kind := kind
  payload_digest := digest
  authority_effect := "None"

def example_fixture_mss_src : MssStage where
  stage_id := 0
  grammar_id := "fixture.mss.0"
  alphabet_finite := true
  equality_decidable := true

def example_fixture_mss_dst : MssStage where
  stage_id := 1
  grammar_id := "fixture.mss.1"
  alphabet_finite := true
  equality_decidable := true

/--
Diagnostic fixture: nine schema-valid receipts + status flags all true.

**Not** a production uplift proof. Digests are placeholders; no host runtime
binding. AuthorityEffect remains None at the schema layer only.
-/
def example_fixture_nineCertificate :
    NineCertificateConditions example_fixture_mss_src example_fixture_mss_dst where
  exhaustion := {
    receipt := example_fixture_hostReceipt
      "fix-exhaustion-001" receiptKind.exhaustion "digest:fixture:exhaustion"
    exhausted := true
  }
  refusal := {
    receipt := example_fixture_hostReceipt
      "fix-refusal-001" receiptKind.refusal "digest:fixture:refusal"
    refused := true
  }
  traceability := {
    receipt := example_fixture_hostReceipt
      "fix-traceability-001" receiptKind.traceability "digest:fixture:traceability"
    obstruction_id := "obstruction.fixture.0"
    generator_id := "generator.fixture.0"
    traced := true
  }
  preservation := {
    receipt := example_fixture_hostReceipt
      "fix-preservation-001" receiptKind.preservation "digest:fixture:preservation"
    preserved := true
  }
  conservativity := {
    receipt := example_fixture_hostReceipt
      "fix-conservativity-001" receiptKind.conservativity "digest:fixture:conservativity"
    conservative := true
  }
  obstruction_resolution := {
    receipt := example_fixture_hostReceipt
      "fix-obstruction-resolution-001" receiptKind.obstruction_resolution
      "digest:fixture:obstruction_resolution"
    resolved_or_refined := true
  }
  generator_minimality := {
    receipt := example_fixture_hostReceipt
      "fix-minimality-001" receiptKind.minimality "digest:fixture:minimality"
    generator_id := "generator.fixture.0"
    minimal := true
  }
  replay := {
    receipt := example_fixture_hostReceipt
      "fix-replay-001" receiptKind.replay "digest:fixture:replay"
    replay_checked := true
    deterministic := true
  }
  authority_fence := {
    receipt := example_fixture_hostReceipt
      "fix-authority-fence-001" receiptKind.authority_fence "digest:fixture:authority_fence"
  }

/-- Fixture is schema-valid under `allSatisfied` (diagnostic only). -/
theorem example_fixture_nineCertificate_allSatisfied :
    example_fixture_nineCertificate.allSatisfied = true := by
  native_decide

/-!
## Negative schema lemmas (empty id / wrong authority fail validity)

Concrete decisions via `native_decide` — schema refuse shapes, not host proofs.
-/

/-- Empty `receipt_id` fails `HostReceipt.schemaValid` (kind/authority otherwise ok). -/
theorem HostReceipt.schemaValid_empty_id_fails :
    HostReceipt.schemaValid
      { receipt_id := ""
        kind := receiptKind.exhaustion
        payload_digest := "digest:empty"
        authority_effect := "None" }
      receiptKind.exhaustion = false := by
  native_decide

/-- Empty receipt_id fails `ExhaustionTrace.valid` even when exhausted. -/
theorem ExhaustionTrace.valid_empty_receipt_id_fails :
    ExhaustionTrace.valid
      { receipt := {
          receipt_id := ""
          kind := receiptKind.exhaustion
          payload_digest := "digest:empty"
          authority_effect := "None"
        }
        exhausted := true } = false := by
  native_decide

/-- Wrong `authority_effect` fails `HostReceipt.schemaValid`. -/
theorem HostReceipt.schemaValid_wrong_authority_fails :
    HostReceipt.schemaValid
      { receipt_id := "rx-001"
        kind := receiptKind.exhaustion
        payload_digest := "digest:x"
        authority_effect := "Some" }
      receiptKind.exhaustion = false := by
  native_decide

/--
Wrong authority_effect on any slot fails `allSatisfied`.

Near-fixture certificate whose exhaustion receipt claims
`authority_effect := "Some"`; conjunction is false.
-/
def example_fixture_nineCertificate_badAuthority :
    NineCertificateConditions example_fixture_mss_src example_fixture_mss_dst where
  exhaustion := {
    receipt := {
      receipt_id := "fix-exhaustion-bad-auth"
      kind := receiptKind.exhaustion
      payload_digest := "digest:fixture:exhaustion"
      authority_effect := "Some"
    }
    exhausted := true
  }
  refusal := example_fixture_nineCertificate.refusal
  traceability := example_fixture_nineCertificate.traceability
  preservation := example_fixture_nineCertificate.preservation
  conservativity := example_fixture_nineCertificate.conservativity
  obstruction_resolution := example_fixture_nineCertificate.obstruction_resolution
  generator_minimality := example_fixture_nineCertificate.generator_minimality
  replay := example_fixture_nineCertificate.replay
  authority_fence := example_fixture_nineCertificate.authority_fence

theorem example_fixture_nineCertificate_badAuthority_not_allSatisfied :
    example_fixture_nineCertificate_badAuthority.allSatisfied = false := by
  native_decide

/-- Wrong kind label fails schema validity for the exhaustion slot. -/
theorem ExhaustionTrace.valid_wrong_kind_fails :
    ExhaustionTrace.valid
      { receipt := {
          receipt_id := "rx-001"
          kind := "replay"
          payload_digest := "digest:x"
          authority_effect := "None"
        }
        exhausted := true } = false := by
  native_decide

end SharedKernel.QMCODA
