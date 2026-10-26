---
documentation_contract: symbol-game-documentation/v1
title: "MSS-N Level 45: Proof kernel boundary"
kind: grammar-reference
level: 45
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
  row: MSS-46
  relation: declared_research_successor
  lift_status: unlicensed
source_provenance: external_mss_atlas
authority_effect: "None"
source_paths:
  - omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/paper.md
---

# MSS-N Level 45: Proof kernel boundary

**AuthorityEffect:** None.\
**Level:** Level 45 (Epoch III: Linear Resources, Protocols & Proof Kernels)\
**Internal Evaluator Dispatch Offset:** $\operatorname{base}(45) = 128 + 8 \times (45 - 22) = 312$ *(Internal evaluator implementation metadata; never serialized into MSS wire packets)*
**Runtime Pipeline:** `Evaluator::targets.stage_045` | Primary Error: `ERR_PROOF_TERM_DEFECT`\
**Atlas Capabilities:** `proof_term`, `trusted_checker`

---

## Part I: Row Contract

### 1. Architectural Overview & Context

Level 45 resides within **Epoch III: Linear Resources, Protocols & Proof Kernels** in the Minimal Symbol System trans-base operadic hierarchy. While the MSS-N substrate remains domain-agnostic—operating strictly on pure boundary expressions without primitive opcodes or assumed continuum structures—this stage defines the normative packet syntax, capability set, and host verification obligations for stage row $N=45$.

- **Stage Classification:** Finite typed representation of proof kernel boundaries and explicit proof-term verification without self-granting authority.
- **Mathematical Substrate:** The de Bruijn criterion for formal proof kernels:
  - **Pinned Environment:** Cryptographically hashed axioms and primitive inference rules $\mathcal{R}_{\text{pinned}}$.
  - **Concrete Proof-Term Grammar:** Explicit, fully-elaborated proof terms $t$ inhabiting proposition types $T$ in a typed lambda calculus / Martin-Löf type theory ($\Gamma \vdash t : T$).
  - **Independent Deterministic Rechecker:** A minimal, trusted checker artifact that independently recomputes all typing judgments and definitional conversions without heuristic tactics or external network oracles.
- **Verification Discipline:** A claim of verification requires an inspectable proof term and an attested host checker run. Self-reported verification or tactic scripts containing `sorry` are refused.

### 2. Wire Packet Grammar & Mathematical Carrier

The wire packet explicitly declares the pinned axiom/rule hashes, concrete proof-term grammar, candidate proof term, and checker artifact receipt:

```text
<axiom_rule_hashes proof_term_grammar candidate_proof_term checker_artifact>
```

- `axiom_rule_hashes`: SHA-256 digest commitment to the pinned deductive system rules $\mathcal{R}_{\text{pinned}}$.
- `proof_term_grammar`: Explicit BNF / AST specification of admitted proof terms.
- `candidate_proof_term`: Fully elaborated syntax tree $t$ claiming $\Gamma \vdash t : T$.
- `checker_artifact`: Host execution receipt verifying deterministic type checking of $t$.

### 3. Runtime Pipeline Evaluator & Verification Obligation

- **Runtime Pipeline:** `Evaluator::targets.stage_045`
- **Primary Error Code:** `ERR_PROOF_TERM_DEFECT`
- **Atlas Capabilities:** `proof_term`, `trusted_checker`
- **Locally Checkable Verification Obligation:**
  1. **Rule Hash Parity:** Verify that the inference engine matches the pinned cryptographic rule digest $\mathcal{R}_{\text{pinned}}$.
  2. **Proof Term Elaboration:** Check that the candidate term $t$ is fully elaborated and contains zero meta-variables, un-discharged holes, or heuristic stubs (`sorry`).
  3. **Independent Kernel Rechecking:** Execute the deterministic kernel to verify the typing derivation $\Gamma \vdash t : T$ from raw syntax.
- **Falsifier Boundary / Negative Counterexample:**
  - A candidate proof containing unelaborated stubs, undeclared axioms, or ill-typed subterms is rejected with `ERR_PROOF_TERM_DEFECT`.
  - Presenting a self-reported "verified" flag without an inspectable proof term and matching rule hashes is rejected with `ERR_PROOF_TERM_DEFECT`.
- **Boundary Warning:** Level 45 specifies a locally checkable verification obligation; it does not confer ambient authority or self-grant execution privileges.

### 4. Claim Hygiene Quadrant

1. **What this supports:**
   - Formal specification of stage row MSS-45 within Epoch III: Linear Resources, Protocols & Proof Kernels.
   - Locally checkable verification obligation enforcing de Bruijn proof-term checking against pinned deductive rule hashes.
2. **What this does not support:**
   - Does not establish an automatic retraction from MSS-44 or assert meta-theoretic soundness of external SMT solvers.
   - Does not grant autonomous authority elevation (AuthorityEffect: None).
3. **The narrowest defensible claim:**
   - Stage MSS-45 accepts valid fully-elaborated proof terms verified by the pinned host kernel and rejects ungrounded proof claims with `ERR_PROOF_TERM_DEFECT`.
4. **Next test needed:**
   - Execute differential checker verification against stage $N=46$ self-description and termination fixtures using the local CI test harness.

---

## Part II: Lift Record from Predecessor (MSS-44 $\to$ MSS-45)

- **Lift Status:** `unlicensed` (Design-stage specification row; no conservative embedding or retraction proof $r_{45}(u_{45}(x))=x$ has been licensed from MSS-44).
- **Predecessor Stage:** MSS-44 (`level_44_refinement_contracts.md`).
- **Successor Rationale:** When SMT-based refinement contracts (MSS-44) rely on complex black-box solvers without providing minimal, verifiable foundational proof terms, MSS-45 is declared as the specification row providing this capability within the external research atlas.
- **Retraction Status:** Unasserted. (Retraction down-rule $r_{45}(u_{45}(x))=x$ requires an explicit lift receipt certifying repair exhaustion and conservative preimage recovery; it is omitted from the row contract.)
