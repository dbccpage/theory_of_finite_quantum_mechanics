---
documentation_contract: symbol-game-documentation/v1
title: "Lesson 730.01: CODA Nine-Layer Stack and Descent Foundations"
kind: pedagogical-lesson
track: 730_coda_foundations
status: active
maturity: production
claim_status: verified
authority_effect: "None"
source_paths:
  - omega_engine/crates_rs/omega_wdp/src/coda/mod.rs
  - omega_engine/crates_rs/omega_wdp/src/coda/coda_gtla.rs
  - omega_engine/crates_rs/omega_wdp/src/coda/layer1_foc.rs
  - omega_engine_education/documentation/006_oewdp/domains/coda/coda_nine_layer_stack_and_descent_foundations.md
---

# Lesson 730.01: CODA Nine-Layer Stack and Descent Foundations

**AuthorityEffect:** None. Complete mathematical and engineering specification of the Nine-Layer CODA Stack and Descent Foundations; no authorization is conferred.  
**Track:** `730_coda_foundations`  
**Topic:** Theoretical foundations, Nine-Layer CODA Stack, $\Phi_1 / \Gamma_2$ cochain trichotomy, and sovereign Rust delegation.

---

## 1. Pedagogical Objective

Understand the structural architecture of the **Calculus of Obstruction, Descent, and Authority (CODA)** across its nine runtime stages, mastering how finite cochain complexes $C^0 \xrightarrow{d_0} C^1 \xrightarrow{d_1} C^2$ produce exact quotient certificates without unproved continuum or universal authority assumptions.

---

## 2. The Nine-Layer CODA Stack

In `omega_wdp::coda`, CODA is structured into nine sequential runtime stages:

| Stage | Name | Role & Invariant | Module |
| :---: | :--- | :--- | :--- |
| **1** | **FOC** | Finite Obstruction Calculus: exact $L_1$ quotient diagnostic $\Phi_1([x])$ and dual witness certification. | `layer1_foc.rs` |
| **2** | **MUR** | Meta & Universal Re-Presentation: section overlap compatibility and transport loss ledger accounting. | `layer2_mur.rs` |
| **3** | **CS** | Continuum Shadow: total projection-table typing; report/query factorization on realized images. | `layer3_cs.rs` |
| **4** | **CS_Q** | Continuum Shadow to Continuum Bridge: legacy overlap collision screening; declared-domain quotient separation. | `layer4_cs_q.rs` |
| **5** | **Q** | The Continuum: rational interval order, diameter bounds, and spectral convergence gates. | `layer5_q.rs`, `q/` |
| **6** | **A** | Anomalon: cokernel projection and persistent typed residual registers. | `layer6_a.rs` |
| **7** | **OR** | Omniversal Re-Presentation: local-to-global gluing and hard refusal sieve. | `layer7_or.rs` |
| **8** | **FDA** | Finite routing firewall: zero defect does not issue an authority token; no external grants. | `layer8_fda.rs` |
| **9** | **CODA_GTLA** | Disjoint local terminal variants: $\{T_{\mathrm{exact}}, T_{\mathrm{survivor}}, T_{\mathrm{refusal}}\}$; non-promotable receipts. | `layer9_coda_gtla.rs`, `coda_gtla.rs` |

---

## 3. The Core Cochain Diagnostics: $\Phi_1$ and $\Gamma_2$

Over the finite cochain complex $C^0 \xrightarrow{d_0} C^1 \xrightarrow{d_1} C^2$ with $d_1 \circ d_0 = 0$:

1. **Primal Quotients:**
   $$\Phi_1([x]) = \min_{t \in C^0} \|x - d_0 t\|_1$$
2. **Curl Invariant:**
   $$\Gamma_2(x) = \|d_1 x\|_1$$
3. **Exact Trichotomy (`omega_policy::trichotomy`):**
   - **Exact (`Exact`):** $\Phi_1 = 0 \land \Gamma_2 = 0$. The cochain is a pure coboundary $x = d_0 t$.
   - **Survivor (`Survivor`):** $\Phi_1 > 0 \land \Gamma_2 = 0$. The cochain is a non-trivial closed 1-cocycle spanning a harmonic loop defect.
   - **Open (`Open`):** $\Gamma_2 > 0$. The boundary condition is violated; the cochain is unclosed.

---

## 4. Check for Understanding

1. Why does Layer 8 (FDA) strictly refuse to issue authority tokens even when $\Phi_1 = 0$ and $\Gamma_2 = 0$?
2. What distinguishes a `Survivor` defect ($\Phi_1 > 0, \Gamma_2 = 0$) from an `Open` defect ($\Gamma_2 > 0$)?
3. How does the primal-dual certificate pair $(x, y)$ certify $\Phi_1([x])$ over $\mathbb{Q}$?

---

## 5. Laboratory Workbench

- Companion Workbench: [Interactive Laboratory Notebook](../notebooks/lesson_730_01_coda_stack_and_descent.ipynb)
