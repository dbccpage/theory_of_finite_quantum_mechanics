---
documentation_contract: education-documentation/v1
title: "MSS-N Level 37: Causal intervention"
kind: grammar-reference
level: 37
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
  row: MSS-38
  relation: declared_research_successor
  lift_status: unlicensed
source_provenance: external_mss_atlas
authority_effect: "None"
source_paths:
  - atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/paper.md
---

# MSS-N Level 37: Causal intervention

**AuthorityEffect:** None.\
**Level:** Level 37 (Epoch II: Renormalization, Dynamics & Game Theory)\
**Internal Evaluator Dispatch Offset:** $\operatorname{base}(37) = 128 + 8 \times (37 - 22) = 248$ *(Internal evaluator implementation metadata; never serialized into MSS wire packets)*
**Runtime Pipeline:** `Evaluator::targets.stage_037` | Primary Error: `ERR_STRUCTURAL_EQUATION_DEFECT`\
**Atlas Capabilities:** `structural_equation`, `do_operator`

---

## Part I: Row Contract

### 1. Architectural Overview & Context

Level 37 resides within **Epoch II: Renormalization, Dynamics & Game Theory** in the Minimal Symbol System trans-base operadic hierarchy. While the MSS-N substrate remains domain-agnostic—operating strictly on pure boundary expressions without primitive opcodes or assumed continuum structures—this stage defines the normative packet syntax, capability set, and host verification obligations for stage row $N=37$.

- **Stage Classification:** Finite typed representation of causal interventions in acyclic Structural Causal Models without self-granting authority.
- **Mathematical Substrate:** A finite Structural Causal Model (SCM) $\mathcal{M} = (V, U, \mathcal{F}, P(U))$:
  - Endogenous variables $V = \{X_1, \dots, X_n\}$, exogenous variables $U = \{U_1, \dots, U_m\}$.
  - Structural assignments $X_i := f_i(\operatorname{PA}_i, U_i)$ where $\operatorname{PA}_i \subseteq V \setminus \{X_i\}$.
  - Causal graph $G = (V, E)$ where $(X_j, X_i) \in E \iff X_j \in \operatorname{PA}_i$. Mandatory invariant: $G$ is a strict Directed Acyclic Graph (DAG).
- **Pearleian $do$-Intervention:**
  An intervention $do(X_k = x_k^*)$ replaces the structural function $f_k(\operatorname{PA}_k, U_k)$ with the constant assignment $X_k := x_k^*$. In the mutilated graph $G_{\overline{X_k}}$, all incoming arrows into $X_k$ are deleted, severing $X_k$ from its parents $\operatorname{PA}_k$ while preserving all downstream functional dependencies.

### 2. Wire Packet Grammar & Mathematical Carrier

The wire packet explicitly declares the causal DAG, intervention target, assigned value, altered structural equation, and resulting mutilated DAG:

```text
<scm_dag intervention_target intervention_value altered_assignment mutilated_dag>
```

- `scm_dag`: Strict topological adjacency matrix of causal DAG $G = (V, E)$.
- `intervention_target`: Endogenous node identifier $X_k \in V$.
- `intervention_value`: Pinned intervention value $x_k^*$.
- `altered_assignment`: Replaced structural equation $X_k := x_k^*$.
- `mutilated_dag`: Modified graph $G_{\overline{X_k}}$ with all incoming edges into $X_k$ removed.

### 3. Runtime Pipeline Evaluator & Verification Obligation

- **Runtime Pipeline:** `Evaluator::targets.stage_037`
- **Primary Error Code:** `ERR_STRUCTURAL_EQUATION_DEFECT`
- **Atlas Capabilities:** `structural_equation`, `do_operator`
- **Locally Checkable Verification Obligation:**
  1. **Strict DAG Acyclicity:** Verify that $G$ possesses a valid topological sort (no directed cycles).
  2. **Intervention Graph Mutilation:** Check that in $mutilated_dag$, the in-degree of $X_k$ is zero and that for all $j \neq k$, $\operatorname{PA}_j$ in $G_{\overline{X_k}}$ is identical to $\operatorname{PA}_j$ in $G$.
  3. **Assignment Replacement:** Verify that the equation for $X_k$ is substituted with the constant $x_k^*$ without modifying $f_j$ for $j \neq k$.
- **Falsifier Boundary / Negative Counterexample:**
  - Any SCM candidate containing a directed cycle is rejected with `ERR_STRUCTURAL_EQUATION_DEFECT`.
  - Conflating observational conditioning $P(Y \mid X=x)$ with causal intervention $P(Y \mid do(X=x))$, or failing to delete incoming edges to the intervention target, is rejected with `ERR_STRUCTURAL_EQUATION_DEFECT`.
- **Boundary Warning:** Level 37 specifies a locally checkable verification obligation; it does not confer ambient authority or self-grant execution privileges.

### 4. Claim Hygiene Quadrant

1. **What this supports:**
   - Formal specification of stage row MSS-37 within Epoch II: Renormalization, Dynamics & Game Theory.
   - Locally checkable verification obligation enforcing acyclicity, graph mutilation, and assignment substitution in finite SCMs.
2. **What this does not support:**
   - Does not establish an automatic retraction from MSS-36 or assert causal discovery from purely observational data without unconfoundedness assumptions.
   - Does not grant autonomous authority elevation (AuthorityEffect: None).
3. **The narrowest defensible claim:**
   - Stage MSS-37 accepts valid acyclic SCM intervention packets with correctly mutilated graphs and rejects cyclic or un-mutilated graphs with `ERR_STRUCTURAL_EQUATION_DEFECT`.
4. **Next test needed:**
   - Execute differential checker verification against stage $N=38$ counterfactual fixtures using the local CI test harness.

---

## Part II: Lift Record from Predecessor (MSS-36 $\to$ MSS-37)

- **Lift Status:** `unlicensed` (Design-stage specification row; no conservative embedding or retraction proof $r_{37}(u_{37}(x))=x$ has been licensed from MSS-36).
- **Predecessor Stage:** MSS-36 (`level_36_bayesian_updates.md`).
- **Successor Rationale:** When observational Bayesian conditioning (MSS-36) cannot distinguish between statistical correlation and directed causal mechanisms (the causal hierarchy gap), MSS-37 is declared as the specification row providing this capability within the external research atlas.
- **Retraction Status:** Unasserted. (Retraction down-rule $r_{37}(u_{37}(x))=x$ requires an explicit lift receipt certifying repair exhaustion and conservative preimage recovery; it is omitted from the row contract.)
