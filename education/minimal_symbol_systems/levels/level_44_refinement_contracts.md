---
documentation_contract: education-documentation/v1
title: "MSS-N Level 44: Refinement contracts"
kind: grammar-reference
level: 44
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
  row: MSS-45
  relation: declared_research_successor
  lift_status: unlicensed
source_provenance: external_mss_atlas
authority_effect: "None"
source_paths:
  - atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/paper.md
---

# MSS-N Level 44: Refinement contracts

**AuthorityEffect:** None.\
**Level:** Level 44 (Epoch III: Linear Resources, Protocols & Proof Kernels)\
**Internal Evaluator Dispatch Offset:** $\operatorname{base}(44) = 128 + 8 \times (44 - 22) = 304$ *(Internal evaluator implementation metadata; never serialized into MSS wire packets)*
**Runtime Pipeline:** `Evaluator::targets.stage_044` | Primary Error: `ERR_PREDICATE_REFINEMENT_DEFECT`\
**Atlas Capabilities:** `predicate_refinement`, `prepost_contract`

---

## Part I: Row Contract

### 1. Architectural Overview & Context

Level 44 resides within **Epoch III: Linear Resources, Protocols & Proof Kernels** in the Minimal Symbol System trans-base operadic hierarchy. While the MSS-N substrate remains domain-agnostic—operating strictly on pure boundary expressions without primitive opcodes or assumed continuum structures—this stage defines the normative packet syntax, capability set, and host verification obligations for stage row $N=44$.

- **Stage Classification:** Finite typed representation of predicate refinement contracts scoped to decidable theories without self-granting authority.
- **Mathematical Substrate:** Refinement types $\{x : T \mid \phi(x)\}$ and pre/postcondition contracts $(P, Q)$ scoped strictly to a declared decidable theory $\mathcal{T}$ (e.g., Quantifier-Free Presburger Arithmetic QF-PA or Quantifier-Free Linear Rational Arithmetic QF-LRA).
- **Verification Condition & Solver Witness:**
  For an operation $y = f(x)$, the verification condition is:
  $$\operatorname{VC}(f) \equiv \forall x, \quad P(x) \implies Q(x, f(x))$$
  Validity is discharged by an explicit checkable solver certificate (e.g., Farkas lemma rational dual vector for linear inequalities or an unsatisfiable core resolution DAG).
- **The Pending Invariant:** Unwitnessed assertions remain pending. No assertion is accepted as valid based on syntactic plausibility alone; without an independently checkable solver witness, the contract is refused.

### 2. Wire Packet Grammar & Mathematical Carrier

The wire packet explicitly declares the decidable theory fragment, precondition, postcondition, solver certificate, and verified contract status:

```text
<decidable_theory precondition postcondition solver_certificate contract_status>
```

- `decidable_theory`: Identifier for the formal theory fragment (e.g., `QF_LRA`, `QF_PA`).
- `precondition`: First-order formula $P(x)$ in $\mathcal{T}$.
- `postcondition`: First-order formula $Q(x, y)$ in $\mathcal{T}$.
- `solver_certificate`: Exact certificate artifact (e.g., rational Farkas dual coefficients witnessing $\neg(P \implies Q)$ is unsatisfiable).
- `contract_status`: Verified claim token (`certified` vs. `pending`).

### 3. Runtime Pipeline Evaluator & Verification Obligation

- **Runtime Pipeline:** `Evaluator::targets.stage_044`
- **Primary Error Code:** `ERR_PREDICATE_REFINEMENT_DEFECT`
- **Atlas Capabilities:** `predicate_refinement`, `prepost_contract`
- **Locally Checkable Verification Obligation:**
  1. **Decidable Fragment Check:** Verify that all predicate formulas belong strictly to the declared decidable theory $\mathcal{T}$ (no unquantified non-linear terms or higher-order logic).
  2. **Certificate Recomputation:** Independently evaluate the solver certificate (e.g., check that the Farkas linear combination yields a contradictory positive/negative rational bound).
  3. **Refusal of Unwitnessed Claims:** Ensure that any contract lacking a complete certificate remains strictly flagged as `pending` and is rejected from certified status.
- **Falsifier Boundary / Negative Counterexample:**
  - A candidate contract claiming certified status without an accompanying checkable solver certificate is rejected with `ERR_PREDICATE_REFINEMENT_DEFECT`.
  - A candidate where the solver certificate fails recomputation or the negated verification condition is satisfiable is rejected with `ERR_PREDICATE_REFINEMENT_DEFECT`.
- **Boundary Warning:** Level 44 specifies a locally checkable verification obligation; it does not confer ambient authority or self-grant execution privileges.

### 4. Claim Hygiene Quadrant

1. **What this supports:**
   - Formal specification of stage row MSS-44 within Epoch III: Linear Resources, Protocols & Proof Kernels.
   - Locally checkable verification obligation enforcing solver-witnessed refinement contracts within declared decidable theories.
2. **What this does not support:**
   - Does not establish an automatic retraction from MSS-43 or assert general undecidable program verification (Turing halting barrier).
   - Does not grant autonomous authority elevation (AuthorityEffect: None).
3. **The narrowest defensible claim:**
   - Stage MSS-44 accepts valid solver-certified refinement contract packets and leaves unwitnessed assertions pending with `ERR_PREDICATE_REFINEMENT_DEFECT`.
4. **Next test needed:**
   - Execute differential checker verification against stage $N=45$ proof kernel boundary fixtures using the local CI test harness.

---

## Part II: Lift Record from Predecessor (MSS-43 $\to$ MSS-44)

- **Lift Status:** `unlicensed` (Design-stage specification row; no conservative embedding or retraction proof $r_{44}(u_{44}(x))=x$ has been licensed from MSS-43).
- **Predecessor Stage:** MSS-43 (`level_43_effect_and_capability.md`).
- **Successor Rationale:** When discrete capability lattices (MSS-43) cannot express fine-grained algebraic data invariants (such as array bounds, sortedness, or arithmetic inequalities), MSS-44 is declared as the specification row providing this capability within the external research atlas.
- **Retraction Status:** Unasserted. (Retraction down-rule $r_{44}(u_{44}(x))=x$ requires an explicit lift receipt certifying repair exhaustion and conservative preimage recovery; it is omitted from the row contract.)
