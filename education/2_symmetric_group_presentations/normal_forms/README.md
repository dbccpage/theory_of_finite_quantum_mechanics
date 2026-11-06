---
documentation_contract: education-documentation/v1
title: "Normal Forms & Canonical Form Contracts — S(n) — Survivor Sequence"
kind: normal-form-index
status: active
maturity: research
evidence_grades:
  named: true
  syntax: true
  computed: false
  Lean: false
  gated: false
authority_effect: "None"
canonical_source: omega_engine_education/documentation/014_normal_forms/contracts_normal_forms/
last_verified: 2026-09-29
---

# Normal Forms & Canonical Form Contracts — S(n) Survivor Sequence

**AuthorityEffect:** None.\
**Canonical Source:** [`omega_engine_education/documentation/014_normal_forms/contracts_normal_forms/`](../../014_normal_forms/contracts_normal_forms)

---

These YAML files specify intended contracts. `sn_audit.py` checks their schema
shape; it does not execute their replay, cost, authorization or mathematical
proof obligations. “Verification required” is a requirement on an eventual
consumer, not evidence that the consumer exists.

## Architectural Taxonomy: True Normal Forms vs. Extended Form Contracts

In accordance with [`standard.yaml`](../../014_normal_forms/contracts_nf_standards/standard.yaml), contracts in the $S(n)$ domain are evaluated against the four foundational pillars of normalization:

1. **Relational Database Normal Forms (`qualifies_as_true_normal_form: true`):**
   - Strictly satisfy relational project-join decomposition or functional/multivalued dependency preservation theorems (1NF–6NF, BCNF, ETNF).
   - Decompositions must guarantee lossless natural join reconstruction without spurious tuples.
   - *Note on Mathematical Parity:* Abstract term rewriting and polygraphs possess their own distinct normal forms (via confluence and termination). The flag `qualifies_as_true_normal_form: false` here denotes specifically that reconstruction is not a relational project-join, not that term rewriting lacks normal forms.

2. **Extended / Canonical Form Contracts (`qualifies_as_extended_form: true`, `qualifies_as_true_normal_form: false`):**
   - Provide concrete domain normalization: **anomaly exclusion**, **canonicalization**, **invariant preservation**, and **typed terminal routing decisions**.
   - Model derivations, epistemic state observers, and folds where reconstruction is defined via replay, sequence fold, or quotient presentation rather than flat relational project-join theorems.
   - All eight contracts in this $S(n)$ survivor sequence domain declare `qualifies_as_true_normal_form: false`; they operate as draft extended form contracts.

---

## Contracts in This Domain

| ID | Name | Short | Form Category | Family | Relevance & Invariant |
|---|---|---|---|---|---|
| [`nf.derivation.pdnf`](./nf.derivation.pdnf.yaml) | Primitive Difference Normal Form | PDNF | Extended Form Contract | derivation | $S(n)$ witnessed irreflexive relation: specifies that every difference claim has a positive witness count and no self-difference ($a \neq b$). |
| [`nf.derivation.rpnf`](./nf.derivation.rpnf.yaml) | Replay Provenance Normal Form | RPNF | Extended Form Contract | derivation | $S(n)$ regime definition: $\text{regime} = \operatorname{fold}(\text{genesis}, \text{history})$. Specifies deterministic replay equivalence from quiescent genesis. |
| [`nf.derivation.scnf`](./nf.derivation.scnf.yaml) | Separation Cost Normal Form | SCNF | Extended Form Contract | derivation | $S(n)$ survivor counts & transition costs: minimizers require explicit cost measure, grammar, and isomorphism relations without silent tie-breaking. |
| [`nf.derivation.sernf`](./nf.derivation.sernf.yaml) | Split Extension-Retraction Normal Form | SERNF | Extended Form Contract | derivation | $S(n)$ presentation tower: section lift $u_N$ and retraction down-map $r_N$ satisfy split identity $r_N(u_N(x)) = x$ on base carrier. |
| [`nf.derivation.obnf`](./nf.derivation.obnf.yaml) | Obstruction Relativization Normal Form | OBNF | Extended Form Contract | derivation | $S(n)$ Boxed Law 1: collisions are obstructions only relative to a declared protected law; $S(n+1)$ admits only structure forced by unresolved $S(n)$ obstructions. |
| [`nf.epistemic.nar_nf`](./nf.epistemic.nar_nf.yaml) | Non-Authoritative Realization Normal Form | NAR-NF | Extended Form Contract | epistemic | $S(n)$ Boxed Law 2: representation arrow $S(n) \to R(S(n))$ is strictly one-way; external realizations possess zero authority to extend Genesis. |
| [`nf.epistemic.state`](./nf.epistemic.state.yaml) | State Normal Form | StNF | Extended Form Contract | epistemic | Tracks the regime/epoch state of each $S(n)$ level transition with explicit state digest separation. |
| [`nf.epistemic.pvnf`](./nf.epistemic.pvnf.yaml) | Provenance Normal Form | PvNF | Extended Form Contract | epistemic | Provenance versioning and hash chain integrity for $S(n)$ level snapshots. |

---

## Domain-Specific Rationale

### `nf.derivation.pdnf` — Primitive Difference Normal Form
$S(n)$ begins with a witnessed irreflexive relation (CODA-01). PDNF specifies that every difference claim has a positive witness count and no self-difference, preserving distinctness on carrier sets.

### `nf.derivation.rpnf` — Replay Provenance Normal Form
$S(n)$ defines $\text{regime} = \operatorname{fold}(\text{genesis}, \text{history})$. RPNF specifies that a regime is certified only when it equals the fold of its declared history from quiescent genesis.

### `nf.derivation.scnf` — Separation Cost Normal Form
$S(n)$ transition costs (distinct from survivor counts) must name their measure explicitly. SCNF prevents cost minima reported without the measure that made them minimal.

### `nf.derivation.sernf` — Split Extension-Retraction Normal Form
Specifies the split retraction invariant $r_N(u_N(x)) = x$ for presentation tower extensions, eliminating broken down-maps and ensuring losslessly recoverable predecessor levels.

### `nf.derivation.obnf` — Obstruction Relativization Normal Form (Boxed Law 1)
Specifies Boxed Law 1: a collision is an obstruction only relative to an explicitly declared protected law, ensuring $S(n+1)$ contains only structure forced by an unresolved obstruction at $S(n)$.

### `nf.epistemic.nar_nf` — Non-Authoritative Realization Normal Form (Boxed Law 2)
Specifies Boxed Law 2: external mathematical realizations $R(S(n))$ have no authority to extend $S(n)$; the representation arrow $S(n) \xrightarrow{\rho} R(S(n))$ is strictly one-way and non-generative in reverse.

### `nf.epistemic.state` — State Normal Form
Tracks the regime/epoch state of each $S(n)$ level transition, preventing unverified state mutations.

### `nf.epistemic.pvnf` — Provenance Normal Form
Provenance versioning for $S(n)$ level snapshots, asserting cryptographic hash custody across derivations.

---

## Genesis Core Stage to Normal Form Invariant Mapping

| Stage | Name | Key Invariant & Obstruction | Governing Extended Form Contract |
| :--- | :--- | :--- | :--- |
| **S(0)** | Ground Zero | Empty carrier, quiescent genesis token `<>`, no-op action | [`nf.derivation.rpnf`](./nf.derivation.rpnf.yaml) (Quiescent genesis anchor) |
| **S(1)** | Supply | Lone mark admitted, demand for non-vacuous action | [`nf.epistemic.state`](./nf.epistemic.state.yaml) (Regime state transition) |
| **S(2)** | Retention & Collapse | Two inscriptions observationally collapsed under $S_2$ symmetry | [`nf.derivation.pdnf`](./nf.derivation.pdnf.yaml) (Witnessed irreflexive difference) |
| **S(3)** | Required Separation | Separation floor cost 2, unclosed orbit demand | [`nf.derivation.scnf`](./nf.derivation.scnf.yaml) (Explicit separation cost measure) |
| **S(4)** | Orbit Closure | Full automorphism closure, `terminal_all_separated` | [`nf.derivation.obnf`](./nf.derivation.obnf.yaml) & [`nf.epistemic.state`](./nf.epistemic.state.yaml) |
| **S(5)** | External Continuation | Endogenous fixpoint, external continuation demand | [`nf.epistemic.nar_nf`](./nf.epistemic.nar_nf.yaml) (Boxed Law 2 boundary) & [`nf.epistemic.pvnf`](./nf.epistemic.pvnf.yaml) |
| **S(6)** | Extension & Descent | Section lift $u_N$, retraction down-map $r_N$ ($r_N(u_N(x))=x$) | [`nf.derivation.sernf`](./nf.derivation.sernf.yaml) (Split Retraction) & [`nf.derivation.scnf`](./nf.derivation.scnf.yaml) |

---

## Claim Hygiene Quadrant

1. **What these contracts support:**
   - Formal anomaly exclusion, replay-certified state progression, and typed terminal routing across $S(n)$ derivation stages.
2. **What they do not support:**
   - Do not claim relational project-join decomposition (`qualifies_as_true_normal_form: false`).
   - Do not grant operational execution authority (`AuthorityEffect: None`).
3. **The narrowest defensible claim:**
   - Each extended form contract describes a structural anomaly and required data invariants relative to explicitly declared parameters (such as `history_fold`, `cost_measure`, or `irreflexive_witness`).
4. **Next test needed:**
   - Execute [`sn_audit.py contracts`](../code/sn_audit.py) to cross-validate all contracts against canonical `standard.yaml` and `normal_form_contract_schema.yaml`.
