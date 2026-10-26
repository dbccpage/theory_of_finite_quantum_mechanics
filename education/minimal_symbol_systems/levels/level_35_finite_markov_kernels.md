---
documentation_contract: education-documentation/v1
title: "MSS-N Level 35: Finite Markov kernels"
kind: grammar-reference
level: 35
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
  row: MSS-36
  relation: declared_research_successor
  lift_status: unlicensed
source_provenance: external_mss_atlas
authority_effect: "None"
source_paths:
  - atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/paper.md
---

# MSS-N Level 35: Finite Markov kernels

**AuthorityEffect:** None.\
**Level:** Level 35 (Epoch II: Renormalization, Dynamics & Game Theory)\
**Internal Evaluator Dispatch Offset:** $\operatorname{base}(35) = 128 + 8 \times (35 - 22) = 232$ *(Internal evaluator implementation metadata; never serialized into MSS wire packets)*
**Runtime Pipeline:** `Evaluator::checks.check_markov, targets.stage_035` | Primary Error: `ERR_STOCHASTIC_KERNEL_DEFECT`\
**Atlas Capabilities:** `stochastic_kernel`, `transition_measure`

---

## Part I: Row Contract

### 1. Architectural Overview & Context

Level 35 resides within **Epoch II: Renormalization, Dynamics & Game Theory** in the Minimal Symbol System trans-base operadic hierarchy. While the MSS-N substrate remains domain-agnostic—operating strictly on pure boundary expressions without primitive opcodes or assumed continuum structures—this stage defines the normative packet syntax, capability set, and host verification obligations for stage row $N=35$.

- **Stage Classification:** Finite typed representation of discrete Markov transition kernels without self-granting authority.
- **Mathematical Substrate:** A transition probability kernel over a finite state space $S = \{s_1, \dots, s_m\}$, represented as an $m \times m$ matrix $P \in \mathbb{Q}^{m \times m}$.
- **Stochasticity Invariants:**
  1. **Nonnegativity:** $P_{ij} \ge 0$ for all $i, j \in \{1, \dots, m\}$.
  2. **Row Stochasticity:** For every source state $i \in \{1, \dots, m\}$, the total exit probability sums to 1:
     $$\sum_{j=1}^m P_{ij} = 1$$

### 2. Wire Packet Grammar & Mathematical Carrier

The wire packet explicitly declares the finite state space, rational transition matrix, and exact row sum witnesses:

```text
<state_space transition_matrix row_sum_witness>
```

- `state_space`: Enumerated finite set $S = \{s_1, \dots, s_m\}$.
- `transition_matrix`: Rational $m \times m$ matrix $P$ where each entry $P_{ij} \in \mathbb{Q}$.
- `row_sum_witness`: Rational summation receipt certifying $\sum_{j=1}^m P_{ij} = 1$ for each row $i$.

### 3. Runtime Pipeline Evaluator & Verification Obligation

- **Runtime Pipeline:** `Evaluator::checks.check_markov, targets.stage_035`
- **Primary Error Code:** `ERR_STOCHASTIC_KERNEL_DEFECT`
- **Atlas Capabilities:** `stochastic_kernel`, `transition_measure`
- **Locally Checkable Verification Obligation:**
  1. **Dimension Match:** Verify that $P$ is an $m \times m$ matrix matching the cardinality $|S| = m$.
  2. **Nonnegative Rational Entries:** Check that $P_{ij} \ge 0$ for all $1 \le i, j \le m$.
  3. **Row Sum Normalization:** Check that $\sum_{j=1}^m P_{ij} = 1$ holds exactly in $\mathbb{Q}$ for every row $i \in \{1, \dots, m\}$.
- **Falsifier Boundary / Negative Counterexample:**
  - Any matrix candidate containing a negative entry ($P_{ij} < 0$) is rejected with `ERR_STOCHASTIC_KERNEL_DEFECT`.
  - Any matrix candidate whose row sum deviates from 1 (e.g., summing to $3/2$ or $0$) is rejected with `ERR_STOCHASTIC_KERNEL_DEFECT`.
- **Boundary Warning:** Level 35 specifies a locally checkable verification obligation; it does not confer ambient authority or self-grant execution privileges.

### 4. Claim Hygiene Quadrant

1. **What this supports:**
   - Formal specification of stage row MSS-35 within Epoch II: Renormalization, Dynamics & Game Theory.
   - Locally checkable verification obligation enforcing row stochasticity and nonnegativity of rational Markov matrices.
2. **What this does not support:**
   - Does not establish an automatic retraction from MSS-34 or assert ergodicity or convergence to stationary distributions.
   - Does not grant autonomous authority elevation (AuthorityEffect: None).
3. **The narrowest defensible claim:**
   - Stage MSS-35 accepts valid finite stochastic kernel packets and rejects non-stochastic matrices with `ERR_STOCHASTIC_KERNEL_DEFECT`.
4. **Next test needed:**
   - Execute differential checker verification against stage $N=36$ Bayesian update fixtures using the local CI test harness.

---

## Part II: Lift Record from Predecessor (MSS-34 $\to$ MSS-35)

- **Lift Status:** `unlicensed` (Design-stage specification row; no conservative embedding or retraction proof $r_{35}(u_{35}(x))=x$ has been licensed from MSS-34).
- **Predecessor Stage:** MSS-34 (`level_34_statistical_manifolds.md`).
- **Successor Rationale:** When statistical manifolds (MSS-34) require discrete state transition dynamics, Markov jump processes, and stochastic propagation operators, MSS-35 is declared as the specification row providing this capability within the external research atlas.
- **Retraction Status:** Unasserted. (Retraction down-rule $r_{35}(u_{35}(x))=x$ requires an explicit lift receipt certifying repair exhaustion and conservative preimage recovery; it is omitted from the row contract.)
