---
documentation_contract: symbol-game-documentation/v1
title: "MSS-N Level 85: Agent task routing"
kind: grammar-reference
level: 85
status: active
maturity: research
atlas_status: specified
syntax_status: verified
checker_status: verified
mathematical_status: computed
successor_status: declared
lift_status: unproved
source_provenance: external_mss_atlas
authority_effect: "None"
source_paths:
  - omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/paper.md
---

# MSS-N Level 85: Agent task routing

**AuthorityEffect:** None.\
**Level:** Level 85 (Epoch VIII: Scoped Authorization, Provenance & Multi-Agent Tracing)\
**Internal Evaluator Dispatch Offset:** $\operatorname{base}(85) = 128 + 8 \times (85 - 22) = 632$ *(Internal evaluator implementation metadata; never serialized into MSS wire packets)*\
**Runtime Pipeline:** `Evaluator::targets.stage_085` | Primary Error: `ERR_TASK_SCOPE_DEFECT`\
**Atlas Capabilities:** `principal_identity`, `delegate_identity`, `grant_expiry`, `delegated_scope`, `principal_scope`

---

## 1. Architectural Overview & Context

Level 85 resides within **Epoch VIII: Scoped Authorization, Provenance & Multi-Agent Tracing** (Authorization Scopes & Execution Traces) in the Minimal Symbol System trans-base operadic hierarchy. While the MSS-N substrate remains domain-agnostic—operating strictly on pure boundary expressions without primitive opcodes or assumed continuum structures—this stage defines the normative packet syntax, capability set, and host verification obligations for stage row $N=85$.

- **Stage Classification:** Finite typed representation of agent task routing without self-granting authority.
- **Conditional Lift Obligation:** Any accepted lift record into MSS-85 must provide $u_{85}, r_{85}$ satisfying $r_{85}(u_{85}(x)) = x$. No accepted predecessor lift is currently claimed (`lift_status: unproved`). Novel terms lacking prior preimage return typed `NON_DESCENT`.

---

## 2. Wire Packet Grammar & Successor Rationale

- **Meaning:** Finite typed representation of agent task routing without self-granting authority.
- **Declared Successor Rationale:** When previous stage capacities lack primitives to articulate agent task routing without ambiguity, MSS-85 is declared as the specification row providing this capability within the external research atlas. (Actual transition requires an accepted lift record; lift status is unproved.)
- **Wire Packet(s):**

```text
  <task_routing <principal_identity principal_id> <delegate_identity delegate_id> <grant_expiry grant_id expiry_epoch> <delegated_scope sub_scope> <principal_scope parent_scope>>
```

---

## 3. Runtime Pipeline Evaluator & Mathematical Core

- **Runtime Pipeline:** `Evaluator::targets.stage_085`
- **Primary Error Code:** `ERR_TASK_SCOPE_DEFECT`
- **Atlas Capabilities:** `principal_identity`, `delegate_identity`, `grant_expiry`, `delegated_scope`, `principal_scope`
- **Mathematical Core & Boundary:** Ruling D4: Counted in apparatus column (A) and atlas specification coverage ($C_{\rm atlas}$), never in object-language mathematical capability coverage ($C_{\rm object}$); object-language witness owed. A future licensed lift must discharge the retraction obligation $r_{85}(u_{85}(x))=x$; undefined terms return `NON_DESCENT`. AuthorityEffect: None.

---

## 4. Verification Obligation & Falsifier Boundary

- **Verification Obligation:** Verify strict scope containment (delegated scope ⊆ principal scope) with valid principal identity, delegate identity, and active unexpired grant identifier.
- **Negative Counterexample:** An agent expanding its authorization beyond principal scope, or acting under an unverified, expired, or forged delegation grant, is refused.
- **Boundary Warning:** Level 85 records machine-checked finite verification receipts; it does not confer ambient authority or self-grant execution privileges.

---

## 5. Claim Hygiene Quadrant

1. **What this supports:**
   - Formal specification of stage row MSS-85 within Epoch VIII: Scoped Authorization, Provenance & Multi-Agent Tracing.
   - Machine-checked verification obligation enforcing `ERR_TASK_SCOPE_DEFECT` upon invalid candidate proposals.
2. **What this does not support:**
   - Does not establish un-mechanized continuum properties or heuristic physics models.
   - Does not grant autonomous authority elevation (AuthorityEffect: None).
3. **The narrowest defensible claim:**
   - Stage MSS-85 accepts valid boundary packets and rejects negative counterexamples with `ERR_TASK_SCOPE_DEFECT`.
4. **Next test needed:**
   - Execute differential checker verification against stage $N=86$ fixtures using the local CI test harness.
