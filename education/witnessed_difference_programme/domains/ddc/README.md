---
documentation_contract: education-documentation/v1
title: "0_ddc: Discrete Deformation Calculus (DDC): Operational Alphabet, Runtime Laws & Finite Demos"
kind: mathematical-reference
audience:
  - engineers
  - researchers
  - coding-agents
status: active
maturity: production
claim_status: source-grounded
authority_effect: "None"
source_paths:
  - atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/docs/source_archive/discrete_deformation_calculus_package/discrete_deformation_calculus.md
  - atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/docs/source_archive/discrete_deformation_calculus_package/chapters/
  - atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/docs/source_archive/discrete_deformation_calculus_package/docs/
aliases:
  - ddc
  - 140_discrete_deformation_calculus_ddc
related:
  - ../README.md
last_verified: 2026-10-10
---

# 0_ddc: Discrete Deformation Calculus (DDC): Operational Alphabet, Runtime Laws & Finite Demos

**AuthorityEffect:** None. Complete mathematical and engineering documentation suite for the Discrete Deformation Calculus; no authorization is conferred.

This directory serves as the canonical navigational entry point, architectural overview, and chapter-by-chapter mathematical reference for the **Discrete Deformation Calculus (DDC)**, its 8-letter operational trace alphabet, eight runtime laws, five minimal finite verification demos, and complete claim ledger.

---

## 1. Documentation Index

The DDC educational and mathematical documentation is structured into foundational chapters, operational level guides, and normal form contracts:

### Core Chapters (0, 1, 2, 3)

| Document | Title & Focus | Primary Content & Mechanization |
| :--- | :--- | :--- |
| [**00: Foundations**](00_discrete_deformation_calculus_foundations.md) | DDC Foundations & Core Invariants | Cochain window ($C^0 \to C^1 \to C^2$), FOC diagnostics ($\Phi_1, \Gamma_2$), spanning forest duality over $\mathbb{Q}$, discrete Hodge decomposition, and four-axis separation. |
| [**01: Runtime Laws & Theorems**](01_runtime_laws_and_tape_theorems.md) | Runtime Laws, Tape Theorems & Verification Demos | The 8 runtime laws, refinement of historical comparison models, tape automaton, Lean 4 tape theorems, C·R·E·D·I·T sequence analysis, and five minimal finite demos. |
| [**02: Claim Ledger & Maps**](02_ddc_claim_ledger_and_mechanization_map.md) | Complete Claim Ledger & Mechanization Map | Complete census of all DDC claims, epistemic status classifications, Lean 4 theorems (`lean4/Ddc/`), and Python test bindings (`code/tests/`). |
| [**03: Simplicial Semantics & Rust Delegation**](03_ddc_simplicial_semantics_and_rust_delegation.md) | Simplicial Semantics, Runes & Sovereign Rust Delegation | Homotopy retraction semantics for runes, eight classical algebraic invariants, and native Rust math crate delegation (`omega_discrete_deformation_calculus`). |

### Deep Level Guides & Normal Forms

| Catalog | Focus | Link |
| :--- | :--- | :---: |
| **Operational Levels Index** | Deep specifications for all 8 operational runes ($E, R, C, I, \Lambda, D, M, T$) | [Levels Register](../../levels/ddc/README.md) |
| **DDC Normal Forms** | The 8 canonical normal forms (HCNF, TMNF, CBNF, LLNF, RRNF, TPNF, LNLF, DWNF) | [Normal Forms](../../normal_forms/README.md) |

---

## 2. Core Thesis & Epistemic Posture

The Discrete Deformation Calculus is a typed algebra of what a finite computation did to a declared obstruction:

$$\boxed{\textbf{DDC is a typed calculus of what a computation did to an obstruction.}}$$

> **The DDC Epistemic Posture:**
> 1. DDC records **how a computation handled an obstruction**, not whether external prose, model output, or code is true.
> 2. It tracks state transformations through deterministic, machine-verifiable step receipts committed to cryptographic Merkle tapes.
> 3. An obstruction cannot be wished away, renamed, or ignored; it must be transformed through lawful operational letters.
> 4. A lawful tape provides replay evidence; it confers no authority (`AuthorityEffect: None`).

---

## 3. The 8-Letter Operational Alphabet ($\mathcal{A}_{\mathrm{DDC}}$)

Every valid DDC state transition is typed by exactly one operational letter from the canonical alphabet:

$$\mathcal{A}_{\mathrm{DDC}} = \{C, R, E, I, \Lambda, D, M, T\}$$

Detailed mathematical definitions, transition fences, wire receipts, and falsifiers for each letter reside in the [`levels/ddc/`](../../levels/ddc/README.md) directory:

| Rune | Operational Name | Formal Function & Meaning | Level Guide | Diagram |
| :---: | :--- | :--- | :---: | :---: |
| **`C`** | **Context Exposure** | Declares or exposes boundary complexes, chains, and windows ($C^0 \xrightarrow{d_0} C^1 \xrightarrow{d_1} C^2$). Does not reduce residual mass. | [Level 03](../../levels/ddc/level_03_c_context_exposure.md) | [SVG](../../_images/ddc_03_c_context_exposure.svg) |
| **`R`** | **Residual Projection** | Projects unresolved boundary discrepancies into quotient tracking ($\Phi_1([x]) > 0$). | [Level 02](../../levels/ddc/level_02_r_residual_projection.md) | [SVG](../../_images/ddc_02_r_residual_projection.svg) |
| **`E`** | **Exact Repair** | Eliminates local coboundary tension under declared rewrite rules ($\Delta_E \in \mathrm{im}(d_0)$). | [Level 01](../../levels/ddc/level_01_e_exact_repair.md) | [SVG](../../_images/ddc_01_e_exact_repair.svg) |
| **`I`** | **Integration** | Appends a cryptographically verified transition to the Merkle execution tape with a deterministic receipt. | [Level 04](../../levels/ddc/level_04_i_integration.md) | [SVG](../../_images/ddc_04_i_integration.svg) |
| **`Λ`** | **Structural Lift** | Extends carrier capacity under a Licensed Context Extension (LCE) when local repair is impossible ($\Phi_1 > 0, \Gamma_2 = 0$). | [Level 05](../../levels/ddc/level_05_lambda_structural_lift.md) | [SVG](../../_images/ddc_05_lambda_structural_lift.svg) |
| **`D`** | **Descent** | Scale descent lowering from rich to coarse representations, recording forgotten data into an explicit loss ledger. | [Level 06](../../levels/ddc/level_06_d_descent.md) | [SVG](../../_images/ddc_06_d_descent.svg) |
| **`M`** | **Typed Refusal** | Mutation block halting untyped, unwitnessed, out-of-budget, or illegal operational moves. | [Level 07](../../levels/ddc/level_07_m_typed_refusal.md) | [SVG](../../_images/ddc_07_m_typed_refusal.svg) |
| **`T`** | **Terminalization** | Closes execution trace under a declared routing terminal, absorbing further mutation. | [Level 08](../../levels/ddc/level_08_t_terminalization.md) | [SVG](../../_images/ddc_08_t_terminalization.svg) |

---

## 4. The Eight Runtime Laws

The operational trace must strictly obey the eight candidate runtime laws:

1. **Law 1 (Receipt Determinism):** Every transition generates a deterministic, machine-verifiable step receipt binding SHA-256 digests of input state, output state, carrier context, and dual witness.
2. **Law 2 (Terminal Absorption):** Once a trace reaches terminal state `T`, no further mutation may touch the active trace (`Ddc.terminal_absorbing`).
3. **Law 3 (Refusal Absorption):** Retrying a refused operation `M` without new evidence, altered scope, or Licensed Context Extension is strictly forbidden; only $\{C, \Lambda, T\}$ may follow (`Ddc.refusal_absorbing`).
4. **Law 4 (Lift Trigger Law):** Structural lift `Λ` may be proposed only from a verified `ClosedResidual` state ($\Phi_1 > 0, \Gamma_2 = 0$) or `DetectorInadequate` with an explicit discrete licence.
5. **Law 5 (Integration Requires Receipt):** Step integration `I` requires an explicit, cryptographically valid receipt; without a receipt, it routes unconditionally to typed refusal `M`.
6. **Law 6 (Descent Requires Loss Ledger):** Scale descent `D` must declare all dropped coordinates and forgotten topological phases in an explicit `LossLedger` $L_{\text{adapter}}$.
7. **Law 7 (Exact Repair Monotonicity):** Exact repair `E` must strictly decrease or preserve $(\Gamma_2, \Phi_1)$ defect mass under the declared detector scope.
8. **Law 8 (Context Exposure Is Not Repair):** Declaring or exposing a boundary `C` does not reduce residual mass or mint authority.

---

## 5. The Five Minimal Finite Demos

The DDC test suite validates the runtime engine against five minimal finite benchmark scenarios:

- **Demo 1 (Boundary Cancellation):** Two adjacent triangles sharing an edge. Exact defect is registered, repaired, and sealed ($C \to R \to E \to T \implies \text{CheckPassed}$). Open defect is refused ($C \to R \to M$).
- **Demo 2 (Local Green, Global Red):** Filled triangle with value 1 on all three boundary edges ($\Gamma_2 = 3, \Phi_1 = 3$). Trace is $C \to R \to M$; attempting to seal with `T` is refused (`TerminalizedOpenResidual`).
- **Demo 3 (Stabilized Survivor):** Hollow square with unit defect on one edge ($\Phi_1 = 1, \Gamma_2 = 0$). Lawfully sealed on residual terminal ($C \to R \to T$) or lifted under licence ($C \to R \to \Lambda \to T$).
- **Demo 4 (Detector Collapse):** Constant zero detector masking boundary discrepancy. Lawfully halted as $C \to M$ (`REFUSED_DETECTOR_INADEQUATE`); attempting to seal with `T` is refused (`BlindDetector`).
- **Demo 5 (Scale Descent With Loss):** Coarsening 4-edge path to 2-edge path. Lawfully committed with loss ledger ($D \to I \to T$, loss = $7/4$); descent without ledger is rejected as `MissingLossLedger`.

---

## 6. Claim Hygiene Quadrant

1. **What this supports:**
   - Formal specification of the Discrete Deformation Calculus 8-letter operational trace alphabet $\mathcal{A}_{\mathrm{DDC}}$.
   - Operational enforcement of the eight candidate runtime laws and five minimal finite demos.
   - Cryptographic step receipt generation and loss ledger accounting on Merkle tapes.
2. **What this does not support:**
   - Does not establish continuum limits, real phase embeddings, or unbounded search termination.
   - Does not license unverified authority escalation from finite step receipts.
3. **The narrowest defensible claim:**
   - DDC provides a deterministic, typed finite state machine for logging and validating obstruction transformations under `AuthorityEffect: None`.
4. **Next test needed:**
   - Execute the targeted test suite:
     `py -3.12 -m pytest atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/docs/source_archive/discrete_deformation_calculus_package/code/tests/test_automaton.py --basetemp=scratch/pytest_tmp`


## Curriculum Tracks & Interactive Laboratories

- [**Curriculum Master Index**](../../curriculum/ddc_reading_route.md): Interactive laboratory notebooks, concept lessons, narration scripts, and media assets.
