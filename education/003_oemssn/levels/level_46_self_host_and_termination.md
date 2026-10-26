---
documentation_contract: symbol-game-documentation/v1
title: "MSS-N Level 46: Self-description & termination certificate"
kind: grammar-reference
level: 46
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
  row: MSS-47
  relation: declared_research_successor
  lift_status: unlicensed
source_provenance: external_mss_atlas
authority_effect: "None"
source_paths:
  - omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/paper.md
---

# MSS-N Level 46: Self-description & termination certificate

**AuthorityEffect:** None.\
**Level:** Level 46 (Epoch III: Linear Resources, Protocols & Proof Kernels)\
**Internal Evaluator Dispatch Offset:** $\operatorname{base}(46) = 128 + 8 \times (46 - 22) = 320$ *(Internal evaluator implementation metadata; never serialized into MSS wire packets)*
**Runtime Pipeline:** `Evaluator::targets.stage_046` | Primary Error: `ERR_SELF_DESCRIPTION_DEFECT`\
**Atlas Capabilities:** `self_description`, `termination_measure`

---

## Part I: Row Contract

### 1. Architectural Overview & Context

Level 46 closes **Epoch III: Linear Resources, Protocols & Proof Kernels** in the Minimal Symbol System trans-base operadic hierarchy. While the MSS-N substrate remains domain-agnostic—operating strictly on pure boundary expressions without primitive opcodes or assumed continuum structures—this stage defines the normative packet syntax, capability set, and host verification obligations for stage row $N=46$.

- **Stage Classification:** Finite typed representation of evaluator self-description and measure-guarded termination certificates without self-granting authority.
- **Mathematical Substrate:** An admitted recursion scheme paired with a declared well-founded measure $(W, \prec)$:
  - **Self-Description:** A typed syntactic self-representation of the symbol evaluation step function $E \colon \text{Expr} \to \text{Expr}$.
  - **Admitted Recursion Scheme:** Recursive evaluation restricted to primitive structural induction or measure-guarded call trees.
  - **Well-Founded Measure:** A declared ranking function $\mu \colon \text{Args} \to W$ mapping arguments to a well-founded set $(W, \prec)$ (such as $(\mathbb{N}, <)$) that strictly decreases on every recursive invocation:
    $$\forall \operatorname{arg}_{\text{rec}} \in \operatorname{Calls}(\operatorname{arg}), \qquad \mu(\operatorname{arg}_{\text{rec}}) \prec \mu(\operatorname{arg})$$
- **Termination Discipline:** Proves termination strictly for the admitted recursion scheme under the declared measure. Level 46 does not claim to decide termination for arbitrary Turing-complete programs (the halting problem barrier). All evaluations require an external host checker; self-certification is refused.

### 2. Wire Packet Grammar & Mathematical Carrier

The wire packet explicitly declares the evaluator self-description, admitted recursion scheme, declared well-founded measure, and termination certificate:

```text
<evaluator_description recursion_scheme well_founded_measure termination_certificate>
```

- `evaluator_description`: Concrete AST representation of the evaluator function $E$.
- `recursion_scheme`: Explicit declaration of recursion discipline (`structural_subterm`, `measure_guarded`).
- `well_founded_measure`: Pinned ranking function $\mu \colon \text{Args} \to \mathbb{N}$ and target order.
- `termination_certificate`: Finite certificate verifying $\mu(\operatorname{arg}_{\text{rec}}) < \mu(\operatorname{arg})$ across all branch paths.

### 3. Runtime Pipeline Evaluator & Verification Obligation

- **Runtime Pipeline:** `Evaluator::targets.stage_046`
- **Primary Error Code:** `ERR_SELF_DESCRIPTION_DEFECT`
- **Atlas Capabilities:** `self_description`, `termination_measure`
- **Locally Checkable Verification Obligation:**
  1. **Well-Foundedness of Target:** Verify that $(W, \prec)$ is a certified well-founded set with no infinite descending chains.
  2. **Strict Measure Decrease:** For every recursive call site in `evaluator_description`, independently verify that the argument strictly decreases under $\mu$.
  3. **External Host Checking:** Require evaluation verification to be performed by the host environment, rejecting any self-granting internal certificates.
- **Falsifier Boundary / Negative Counterexample:**
  - Any recursive definition failing to demonstrate strict decrease under the declared well-founded measure is rejected with `ERR_SELF_DESCRIPTION_DEFECT`.
  - An evaluation packet claiming self-certification without external host validation is refused with `ERR_SELF_DESCRIPTION_DEFECT`.
- **Boundary Warning:** Level 46 specifies a locally checkable verification obligation; it does not confer ambient authority or self-grant execution privileges.

### 4. Claim Hygiene Quadrant

1. **What this supports:**
   - Formal specification of stage row MSS-46 within Epoch III: Linear Resources, Protocols & Proof Kernels.
   - Locally checkable verification obligation enforcing well-founded measure decrease and external host checking for evaluator termination.
2. **What this does not support:**
   - Does not establish an automatic retraction from MSS-45 or claim a general solution to the Turing halting problem.
   - Does not grant autonomous authority elevation (AuthorityEffect: None).
3. **The narrowest defensible claim:**
   - Stage MSS-46 accepts valid measure-guarded termination certificates for admitted recursion schemes and rejects unmeasured loops with `ERR_SELF_DESCRIPTION_DEFECT`.
4. **Next test needed:**
   - Execute differential checker verification against stage $N=47$ Gaussian-rational scalar fixtures using the local CI test harness.

---

## Part II: Lift Record from Predecessor (MSS-45 $\to$ MSS-46)

- **Lift Status:** `unlicensed` (Design-stage specification row; no conservative embedding or retraction proof $r_{46}(u_{46}(x))=x$ has been licensed from MSS-45).
- **Predecessor Stage:** MSS-45 (`level_45_proof_kernel_boundary.md`).
- **Successor Rationale:** When formal proof kernels (MSS-45) evaluate external proof terms without a mechanized self-description of the evaluation function or explicit measure-guarded termination certificates, MSS-46 is declared as the specification row providing this capability within the external research atlas.
- **Retraction Status:** Unasserted. (Retraction down-rule $r_{46}(u_{46}(x))=x$ requires an explicit lift receipt certifying repair exhaustion and conservative preimage recovery; it is omitted from the row contract.)
