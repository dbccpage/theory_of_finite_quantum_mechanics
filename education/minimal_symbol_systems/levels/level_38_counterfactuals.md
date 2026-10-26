---
documentation_contract: education-documentation/v1
title: "MSS-N Level 38: Counterfactuals"
kind: grammar-reference
level: 38
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
  row: MSS-39
  relation: declared_research_successor
  lift_status: unlicensed
source_provenance: external_mss_atlas
authority_effect: "None"
source_paths:
  - atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/paper.md
---

# MSS-N Level 38: Counterfactuals

**AuthorityEffect:** None.\
**Level:** Level 38 (Epoch II: Renormalization, Dynamics & Game Theory)\
**Internal Evaluator Dispatch Offset:** $\operatorname{base}(38) = 128 + 8 \times (38 - 22) = 256$ *(Internal evaluator implementation metadata; never serialized into MSS wire packets)*
**Runtime Pipeline:** `Evaluator::targets.stage_038` | Primary Error: `ERR_EXOGENOUS_CONTEXT_DEFECT`\
**Atlas Capabilities:** `exogenous_context`, `twin_model`

---

## Part I: Row Contract

### 1. Architectural Overview & Context

Level 38 resides within **Epoch II: Renormalization, Dynamics & Game Theory** in the Minimal Symbol System trans-base operadic hierarchy. While the MSS-N substrate remains domain-agnostic—operating strictly on pure boundary expressions without primitive opcodes or assumed continuum structures—this stage defines the normative packet syntax, capability set, and host verification obligations for stage row $N=38$.

- **Stage Classification:** Finite typed representation of counterfactual evaluation in twin-world structural models without self-granting authority.
- **Mathematical Substrate:** A finite Structural Causal Model evaluating Pearl's three-step counterfactual logic (Abduction, Action, Prediction) across coupled twin worlds:
  1. **Factual Evidence:** Observed real-world realization $e = (X = x_{\text{obs}}, Y = y_{\text{obs}})$.
  2. **Abduction (Exogenous Context):** The latent exogenous state $U = u$ conditioned on factual evidence $e$, satisfying $x_{\text{obs}} = f_X(\operatorname{PA}_X, u_X)$.
  3. **Action:** Hypothetical intervention $do(X = x')$.
  4. **Prediction:** Counterfactual outcome $Y_{X \leftarrow x'}(u) = y'$.
- **The Twin-World Invariant:**
  Both the factual world and the counterfactual world share the identical realization of exogenous background variables $U = u$. The counterfactual modifies only structural assignments severed by the hypothetical action while locking the background noise.

### 2. Wire Packet Grammar & Mathematical Carrier

The wire packet explicitly carries factual evidence, pinned exogenous context, the hypothetical intervention, and both twin-world evaluation traces:

```text
<factual_evidence exogenous_context intervention_specification factual_world counterfactual_world>
```

- `factual_evidence`: Observed state tuple $e = (X = x_{\text{obs}}, Y = y_{\text{obs}})$.
- `exogenous_context`: Pinned background assignment $U = u$ derived from abduction.
- `intervention_specification`: Hypothetical action $do(X = x')$.
- `factual_world`: Deterministic evaluation trace of factual equations under $U = u$.
- `counterfactual_world`: Deterministic evaluation trace of mutilated equations under identical $U = u$.

### 3. Runtime Pipeline Evaluator & Verification Obligation

- **Runtime Pipeline:** `Evaluator::targets.stage_038`
- **Primary Error Code:** `ERR_EXOGENOUS_CONTEXT_DEFECT`
- **Atlas Capabilities:** `exogenous_context`, `twin_model`
- **Locally Checkable Verification Obligation:**
  1. **Factual World Consistency:** Verify that the factual equations with exogenous values $U = u$ evaluate to the observed factual evidence $e$.
  2. **Twin-World Exogenous Identity:** Verify that the exogenous assignment $u$ used in `counterfactual_world` is bit-for-bit identical to that in `factual_world`.
  3. **Mutilated Prediction Check:** Verify that in `counterfactual_world`, $X$ is pinned to $x'$ and all downstream variables are evaluated according to the mutilated structural assignments.
- **Falsifier Boundary / Negative Counterexample:**
  - A candidate counterfactual evaluation that mutates, resamples, or perturbs the exogenous vector $U$ between factual and counterfactual branches is rejected with `ERR_EXOGENOUS_CONTEXT_DEFECT`.
  - A candidate failing to match factual observations in the un-intervened branch is rejected with `ERR_EXOGENOUS_CONTEXT_DEFECT`.
- **Boundary Warning:** Level 38 specifies a locally checkable verification obligation; it does not confer ambient authority or self-grant execution privileges.

### 4. Claim Hygiene Quadrant

1. **What this supports:**
   - Formal specification of stage row MSS-38 within Epoch II: Renormalization, Dynamics & Game Theory.
   - Locally checkable verification obligation enforcing twin-world exogenous conservation in counterfactual reasoning.
2. **What this does not support:**
   - Does not establish an automatic retraction from MSS-37 or claim un-identifiable counterfactuals without deterministic structural assignments.
   - Does not grant autonomous authority elevation (AuthorityEffect: None).
3. **The narrowest defensible claim:**
   - Stage MSS-38 accepts valid twin-world counterfactual packets with conserved exogenous states and rejects latent resampling with `ERR_EXOGENOUS_CONTEXT_DEFECT`.
4. **Next test needed:**
   - Execute differential checker verification against stage $N=39$ game strategy fixtures using the local CI test harness.

---

## Part II: Lift Record from Predecessor (MSS-37 $\to$ MSS-38)

- **Lift Status:** `unlicensed` (Design-stage specification row; no conservative embedding or retraction proof $r_{38}(u_{38}(x))=x$ has been licensed from MSS-37).
- **Predecessor Stage:** MSS-37 (`level_37_causal_intervention.md`).
- **Successor Rationale:** When population-level causal interventions (MSS-37) cannot evaluate individual-level counterfactual queries ("What would have occurred had $X$ been $x'$ given that we observed $X=x_{\text{obs}}$?"), MSS-38 is declared as the specification row providing this capability within the external research atlas.
- **Retraction Status:** Unasserted. (Retraction down-rule $r_{38}(u_{38}(x))=x$ requires an explicit lift receipt certifying repair exhaustion and conservative preimage recovery; it is omitted from the row contract.)
