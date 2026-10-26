---
documentation_contract: symbol-game-documentation/v1
title: "MSS-N Level 40: Equilibrium evidence"
kind: grammar-reference
level: 40
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
  row: MSS-41
  relation: declared_research_successor
  lift_status: unlicensed
source_provenance: external_mss_atlas
authority_effect: "None"
source_paths:
  - omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/paper.md
---

# MSS-N Level 40: Equilibrium evidence

**AuthorityEffect:** None.\
**Level:** Level 40 (Epoch II: Renormalization, Dynamics & Game Theory)\
**Internal Evaluator Dispatch Offset:** $\operatorname{base}(40) = 128 + 8 \times (40 - 22) = 272$ *(Internal evaluator implementation metadata; never serialized into MSS wire packets)*
**Runtime Pipeline:** `Evaluator::targets.stage_040` | Primary Error: `ERR_BEST_RESPONSE_DEFECT`\
**Atlas Capabilities:** `best_response`, `deviation_witness`

---

## Part I: Row Contract

### 1. Architectural Overview & Context

Level 40 closes **Epoch II: Renormalization, Dynamics & Game Theory** in the Minimal Symbol System trans-base operadic hierarchy. While the MSS-N substrate remains domain-agnostic—operating strictly on pure boundary expressions without primitive opcodes or assumed continuum structures—this stage defines the normative packet syntax, capability set, and host verification obligations for stage row $N=40$.

- **Stage Classification:** Finite typed representation of pure-strategy Nash equilibrium evidence without self-granting authority.
- **Mathematical Substrate:** Given a finite normal-form game $\Gamma = (N, (A_i)_{i \in N}, (u_i)_{i \in N})$ with rational payoffs, candidate profile $a^* = (a_1^*, \dots, a_n^*) \in \prod_i A_i$ is a **Pure-Strategy Nash Equilibrium (PNE)** if no player has a profitable unilateral deviation:
  $$\forall i \in N, \quad \forall a_i' \in A_i \setminus \{a_i^*\}, \qquad u_i(a_i^*, a_{-i}^*) - u_i(a_i', a_{-i}^*) \ge 0$$
- **Explicit Pure-Strategy Scope:**
  Level 40 explicitly checks pure-strategy Nash equilibria. (Mixed-strategy equilibria require rational probability distributions, convex polytope supports, and expected payoff integrals; candidate mixed profiles require explicit distribution arrays).

### 2. Wire Packet Grammar & Mathematical Carrier

The wire packet explicitly declares the game reference, candidate pure profile, unilateral deviation ledger, and best-response witness:

```text
<game_reference candidate_pure_profile unilateral_deviation_ledger best_response_witness>
```

- `game_reference`: Identifier and hash of the underlying finite normal-form game $\Gamma$ (MSS-39).
- `candidate_pure_profile`: Action tuple $a^* = (a_1^*, \dots, a_n^*)$.
- `unilateral_deviation_ledger`: Complete enumeration of all $\sum_i (|A_i| - 1)$ alternate action profiles $(a_i', a_{-i}^*)$ and their corresponding rational payoff differences $\Delta u_i = u_i(a^*) - u_i(a_i', a_{-i}^*)$.
- `best_response_witness`: Certificate proving $\Delta u_i \ge 0$ for all unilateral deviations.

### 3. Runtime Pipeline Evaluator & Verification Obligation

- **Runtime Pipeline:** `Evaluator::targets.stage_040`
- **Primary Error Code:** `ERR_BEST_RESPONSE_DEFECT`
- **Atlas Capabilities:** `best_response`, `deviation_witness`
- **Locally Checkable Verification Obligation:**
  1. **Profile Well-Typedness:** Verify that $a_i^* \in A_i$ for every player $i \in N$.
  2. **Exhaustive Deviation Check:** For every player $i$ and every alternate action $a_i' \in A_i$, recompute the rational utility difference:
     $$\Delta u_i(a_i') = u_i(a_1^*, \dots, a_i^*, \dots, a_n^*) - u_i(a_1^*, \dots, a_i', \dots, a_n^*)$$
  3. **Nonnegativity Verification:** Verify that $\Delta u_i(a_i') \ge 0$ for all evaluated deviations.
- **Falsifier Boundary / Negative Counterexample:**
  - Any candidate profile exhibiting a profitable unilateral deviation ($\Delta u_i(a_i') < 0$ for some player $i$ and action $a_i'$) is rejected with `ERR_BEST_RESPONSE_DEFECT`.
  - An incomplete deviation ledger omitting any valid unilateral deviation is rejected with `ERR_BEST_RESPONSE_DEFECT`.
- **Boundary Warning:** Level 40 specifies a locally checkable verification obligation; it does not confer ambient authority or self-grant execution privileges.

### 4. Claim Hygiene Quadrant

1. **What this supports:**
   - Formal specification of stage row MSS-40 within Epoch II: Renormalization, Dynamics & Game Theory.
   - Locally checkable verification obligation enforcing exhaustive unilateral deviation checks for pure-strategy Nash equilibrium.
2. **What this does not support:**
   - Does not establish an automatic retraction from MSS-39 or assert universal existence of pure equilibria in arbitrary games.
   - Does not grant autonomous authority elevation (AuthorityEffect: None).
3. **The narrowest defensible claim:**
   - Stage MSS-40 accepts certified pure-strategy Nash equilibrium packets and rejects profitable deviation candidates with `ERR_BEST_RESPONSE_DEFECT`.
4. **Next test needed:**
   - Execute differential checker verification against stage $N=41$ linear resource fixtures using the local CI test harness.

---

## Part II: Lift Record from Predecessor (MSS-39 $\to$ MSS-40)

- **Lift Status:** `unlicensed` (Design-stage specification row; no conservative embedding or retraction proof $r_{40}(u_{40}(x))=x$ has been licensed from MSS-39).
- **Predecessor Stage:** MSS-39 (`level_39_game_strategies.md`).
- **Successor Rationale:** When uncoordinated game strategy profiles (MSS-39) cannot verify stability, mutual best-responses, or equilibrium certificates, MSS-40 is declared as the specification row providing this capability within the external research atlas.
- **Retraction Status:** Unasserted. (Retraction down-rule $r_{40}(u_{40}(x))=x$ requires an explicit lift receipt certifying repair exhaustion and conservative preimage recovery; it is omitted from the row contract.)
