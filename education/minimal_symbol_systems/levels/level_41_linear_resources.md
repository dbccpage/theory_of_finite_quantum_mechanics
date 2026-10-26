---
documentation_contract: education-documentation/v1
title: "MSS-N Level 41: Linear resources"
kind: grammar-reference
level: 41
status: active
maturity: research
atlas_status: specified
evidence_grades:
  named: true
  syntax: true
  computed: true
  Lean: false
  gated: true
successor:
  row: MSS-42
  relation: declared_research_successor
  lift_status: unlicensed
source_provenance: external_mss_atlas
authority_effect: "None"
source_paths:
  - atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/paper.md
---

# MSS-N Level 41: Linear resources

**AuthorityEffect:** None.\
**Level:** Level 41 (Epoch III: Linear Resources, Protocols & Proof Kernels)\
**Internal Evaluator Dispatch Offset:** $\operatorname{base}(41) = 128 + 8 \times (41 - 22) = 280$ *(Internal evaluator implementation metadata; never serialized into MSS wire packets)*
**Runtime Pipeline:** `Evaluator::targets.stage_041` | Primary Error: `ERR_RESOURCE_TOKEN_DEFECT`\
**Atlas Capabilities:** `resource_token`, `tensor_compose`

---

## Part I: Row Contract

### 1. Architectural Overview & Context

Level 41 opens **Epoch III: Linear Resources, Protocols & Proof Kernels** in the Minimal Symbol System trans-base operadic hierarchy. While the MSS-N substrate remains domain-agnostic—operating strictly on pure boundary expressions without primitive opcodes or assumed continuum structures—this stage defines the normative packet syntax, capability set, and host verification obligations for stage row $N=41$.

- **Stage Classification:** Finite typed representation of substructural linear resource tokens without self-granting authority.
- **Mathematical Substrate:** Multiplicative Intuitionistic Linear Logic (MILL) resource accounting:
  - **Linear Invariant:** Resource tokens $A$ are linear by default: every token must be consumed exactly once.
  - **No Contraction:** Structural duplication $A \vdash A \otimes A$ is strictly prohibited for un-annotated tokens.
  - **No Weakening:** Structural discarding $A \vdash \mathbf{1}$ is strictly prohibited for un-annotated tokens.
  - **Exponential Modality ($!A$):** Contraction and weakening are permitted if and only if the resource token carries an explicit exponential modality annotation $!A$ declaring licensed reuse.

### 2. Wire Packet Grammar & Mathematical Carrier

The wire packet explicitly declares the resource multiset, tensor composition structure, exponential modality annotations, and the exact consumption balance ledger:

```text
<resource_multiset tensor_expression modality_annotation consumption_balance>
```

- `resource_multiset`: Finite multiset of linear tokens $\Delta = \{A_1^{k_1}, \dots, A_m^{k_m}\}$.
- `tensor_expression`: Substructural algebraic expression combining tokens via tensor product $\otimes$.
- `modality_annotation`: Dictionary mapping tokens to substructural status (`linear` vs. `exponential_reuse_permitted`).
- `consumption_balance`: Exact ledger tracking input tokens, consumed tokens, and residual multiset.

### 3. Runtime Pipeline Evaluator & Verification Obligation

- **Runtime Pipeline:** `Evaluator::targets.stage_041`
- **Primary Error Code:** `ERR_RESOURCE_TOKEN_DEFECT`
- **Atlas Capabilities:** `resource_token`, `tensor_compose`
- **Locally Checkable Verification Obligation:**
  1. **Multiset Conservation:** Verify that for all un-annotated tokens, the count of consumed tokens exactly matches the input multiset count ($\Delta_{\text{in}} = \Delta_{\text{consumed}}$).
  2. **Contraction Firewall:** Verify that no linear token is duplicated ($k_{\text{consumed}} > k_{\text{in}}$) unless annotated with $!$.
  3. **Weakening Firewall:** Verify that no linear token is dropped ($k_{\text{consumed}} < k_{\text{in}}$) without explicit disposal modality.
- **Falsifier Boundary / Negative Counterexample:**
  - Any derivation that duplicates a protected linear token without an exponential annotation $!A$ is rejected with `ERR_RESOURCE_TOKEN_DEFECT`.
  - Discarding an unconsumed linear resource token without explicit authorization is rejected with `ERR_RESOURCE_TOKEN_DEFECT`.
- **Boundary Warning:** Level 41 specifies a locally checkable verification obligation; it does not confer ambient authority or self-grant execution privileges.

### 4. Claim Hygiene Quadrant

1. **What this supports:**
   - Formal specification of stage row MSS-41 within Epoch III: Linear Resources, Protocols & Proof Kernels.
   - Locally checkable verification obligation enforcing substructural linear resource conservation and exponential firewalling.
2. **What this does not support:**
   - Does not establish an automatic retraction from MSS-40 or assert classical unrestricted copying/garbage collection.
   - Does not grant autonomous authority elevation (AuthorityEffect: None).
3. **The narrowest defensible claim:**
   - Stage MSS-41 accepts valid linear resource accounting receipts and rejects unauthorized contraction or weakening with `ERR_RESOURCE_TOKEN_DEFECT`.
4. **Next test needed:**
   - Execute differential checker verification against stage $N=42$ session protocol fixtures using the local CI test harness.

---

## Part II: Lift Record from Predecessor (MSS-40 $\to$ MSS-41)

- **Lift Status:** `unlicensed` (Design-stage specification row; no conservative embedding or retraction proof $r_{41}(u_{41}(x))=x$ has been licensed from MSS-40).
- **Predecessor Stage:** MSS-40 (`level_40_equilibrium_evidence.md`).
- **Successor Rationale:** When strategic equilibrium models (MSS-40) assume infinitely copyable payoff scalars and unrestricted state inspection, MSS-41 is declared as the specification row introducing substructural resource linearity and conservation constraints into the external research atlas.
- **Retraction Status:** Unasserted. (Retraction down-rule $r_{41}(u_{41}(x))=x$ requires an explicit lift receipt certifying repair exhaustion and conservative preimage recovery; it is omitted from the row contract.)
