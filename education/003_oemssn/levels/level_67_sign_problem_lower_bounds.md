---
documentation_contract: symbol-game-documentation/v1
title: "MSS-N Level 67: Sign problem lower bounds"
kind: grammar-reference
level: 67
status: active
maturity: research
atlas_status: specified
evidence_grades:
  named: true
  syntax: true
  computed: true
  Lean: false
  gated: true
successor_status: declared
successor:
  row: MSS-68
  relation: declared_research_successor
  lift_status: unlicensed
lift_status: unlicensed
lift_proof_status: absent
lift_license_status: unlicensed
source_provenance: external_mss_atlas
authority_effect: "None"
source_paths:
  - omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/paper.md
---

# MSS-N Level 67: Sign problem lower bounds

**AuthorityEffect:** None.\
**Level:** Level 67 (Epoch VI: Hardness, Real Numbers & Continuum Fences)\
**Internal Evaluator Dispatch Offset:** $\operatorname{base}(67) = 128 + 8 \times (67 - 22) = 488$ *(Internal evaluator implementation metadata; never serialized into MSS wire packets)*\
**Runtime Pipeline:** `Evaluator::targets.stage_067` | Primary Error: `ERR_COMPLEXITY_REDUCTION_DEFECT`\
**Atlas Capabilities:** `problem_family`, `complexity_reduction`

---

## Part I: Row Contract

### 1. Architectural Overview & Context

Level 67 resides within **Epoch VI: Hardness, Real Numbers & Continuum Fences** in the Minimal Symbol System trans-base operadic hierarchy. While the MSS-N substrate remains domain-agnostic—operating strictly on pure boundary expressions without primitive opcodes or assumed continuum structures—this stage defines the normative packet syntax, capability set, and host verification obligations for stage row $N=67$.

- **Stage Classification:** Finite typed representation of computational complexity lower bounds, formal reductions, and parameter scaling for declared sign-problem families without self-granting authority.
- **Complexity Binding Discipline:**
  A hardness result is strictly relative to a declared problem family and formal reduction. Level 67 strictly prohibits turning a hardness proof for a specific Hamiltonian class into an unqualified sweeping claim that "the sign problem is NP-hard".
- **Six Mandatory Reduction Bindings:**
  1. **Source Hard Problem $\mathcal{P}_{\text{hard}}$:** Pinned NP-hard/complete problem (e.g. 3-SAT, MAX-CUT).
  2. **Target Problem Family $\Pi$:** Explicitly scoped sign problem class (e.g. partition function evaluation for 2D frustrated non-stoquastic local Hamiltonians).
  3. **Instance Encoding:** Typed representation format mapping instances into discrete finite bitstrings or rational matrices.
  4. **Reduction Type:** Formal reduction classifier (`KARP_MANY_ONE`, `LEVIN_SEARCH`, or `COOK_TURING`).
  5. **Complexity Resource Model:** Step-count and space bounds on a deterministic classical Turing machine.
  6. **Parameter Scaling Bound:** Exact polynomial bounds $|f(x)| \le p(|x|)$ and $T(|x|) \le q(|x|)$ with explicit rational coefficients.

### 2. Wire Packet Grammar & Mathematical Carrier

The wire packet explicitly binds all six reduction facets and the bidirectional truth-preservation receipt:

```text
<source_problem target_family instance_encoding reduction_type complexity_resource parameter_scaling reduction_witness>
```

- `source_problem`: Identifier of pinned source hard problem $\mathcal{P}_{\text{hard}}$.
- `target_family`: Formal identifier and parameters of target sign-problem instance family $\Pi$.
- `instance_encoding`: Specification of input/output instance serialization formats.
- `reduction_type`: Tagged classification (`KARP_MANY_ONE`, `LEVIN_SEARCH`, `COOK_TURING`).
- `complexity_resource`: Resource model (e.g. deterministic Turing machine time bound).
- `parameter_scaling`: Exact polynomial bound $p(|x|) \in \mathbb{Q}[x]$ bounding instance size expansion.
- `reduction_witness`: Mathematical proof receipt certifying $x \in \mathcal{P}_{\text{hard}} \iff f(x) \in \Pi$.

### 3. Runtime Pipeline Evaluator & Verification Obligation

- **Runtime Pipeline:** `Evaluator::targets.stage_067`
- **Primary Error Code:** `ERR_COMPLEXITY_REDUCTION_DEFECT`
- **Atlas Capabilities:** `problem_family`, `complexity_reduction`
- **Locally Checkable Verification Obligation:**
  1. **Reduction Well-Formedness:** Verify that reduction algorithm $f$ maps every valid instance of $\mathcal{P}_{\text{hard}}$ to a syntactically valid instance of $\Pi$ under `instance_encoding`.
  2. **Polynomial Growth Check:** Verify that instance size $|f(x)|$ respects the declared polynomial bound $p(|x|)$.
  3. **Truth Preservation:** Verify the bidirectional equivalence witness $x \in \mathcal{P}_{\text{hard}} \iff f(x) \in \Pi$.
  4. **Scoped Claim Fence:** Verify that the hardness conclusion is strictly qualified to target family $\Pi$.
- **Falsifier Boundary / Negative Counterexample:**
  - Claiming NP-hardness without an explicit, checkable reduction binding (omitting source problem, encoding, or parameter scaling) is rejected with `ERR_COMPLEXITY_REDUCTION_DEFECT`.
  - Generalizing hardness for a specific family into an unqualified claim that "the sign problem is universally NP-hard" is rejected with `ERR_COMPLEXITY_REDUCTION_DEFECT`.
- **Boundary Warning:** Level 67 records computed/gated verification receipts; it does not confer ambient authority or self-grant execution privileges.

### 4. Claim Hygiene Quadrant

1. **What this supports:**
   - Formal specification of stage row MSS-67 within Epoch VI: Hardness, Real Numbers & Continuum Fences.
   - Computed/gated verification receipts enforcing formal polynomial reductions and qualified scope for computational hardness claims.
2. **What this does not support:**
   - Does not establish an automatic retraction from MSS-66 or claim that every physical sign problem is intractable without reduction.
   - Does not grant autonomous authority elevation (AuthorityEffect: None).
3. **The narrowest defensible claim:**
   - Stage MSS-67 accepts valid polynomial-time reduction packets establishing lower bounds for declared problem families and rejects unqualified or un-reduced hardness claims with `ERR_COMPLEXITY_REDUCTION_DEFECT`.
4. **Next test needed:**
   - Execute differential checker verification against stage $N=68$ interval arithmetic fixtures using the local CI test harness.

---

## Part II: Lift Record from Predecessor (MSS-66 $\to$ MSS-67)

- **Lift Status:** `unlicensed` (lift_license_status: unlicensed, lift_proof_status: absent; design-stage specification row; no conservative embedding or retraction proof $r_{67}(u_{67}(x))=x$ has been licensed from MSS-66).
- **Predecessor Stage:** MSS-66 (`level_66_signed_sum_models.md`).
- **Successor Rationale:** When evaluating signed sums (MSS-66) suffers from exponential variance in Monte Carlo estimators, MSS-67 is declared as the specification row providing formal computational complexity lower bounds for declared problem families within the external research atlas.
- **Conditional Lift Obligation:** Any future accepted lift into MSS-67 must exhibit $(u_{67}, r_{67})$ satisfying $r_{67}(u_{67}(x)) = x$. No predecessor lift is currently claimed (`lift_status: unlicensed`, `lift_proof_status: absent`).
