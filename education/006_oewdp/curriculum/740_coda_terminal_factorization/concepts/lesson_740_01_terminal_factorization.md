---
documentation_contract: symbol-game-documentation/v1
title: "Lesson 740.01: Terminal Factorization and Dual Witness Certification"
kind: pedagogical-lesson
track: 740_coda_terminal_factorization
status: active
maturity: production
claim_status: verified
authority_effect: "None"
source_paths:
  - omega_engine/crates_rs/omega_wdp/src/coda/coda_gtla.rs
  - omega_engine/crates_rs/omega_wdp/src/coda/layer9_coda_gtla.rs
  - omega_engine/crates_rs/omega_wdp/src/coda/layer1_foc.rs
  - omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/rust/src/foundational_bridges.rs
---

# Lesson 740.01: Terminal Factorization and Dual Witness Certification

**AuthorityEffect:** None. Complete mathematical specification of terminal factorization and dual witness certification; no authorization is conferred.  
**Track:** `740_coda_terminal_factorization`  
**Topic:** GTLA terminal factorization, primal-dual $L_1$ certificates, and exact rational duality-gap receipts.

---

## 1. Pedagogical Objective

Understand how the **Calculus of Obstruction, Descent, and Authority (CODA)** resolves cochain boundary evaluation into three strictly disjoint terminal outcomes $\{T_{\mathrm{exact}}, T_{\mathrm{survivor}}, T_{\mathrm{refusal}}\}$ through sovereign primal-dual linear programming over exact rational fields $\mathbb{Q}$, certifying zero duality gap without unproved continuum or universal authority assumptions.

---

## 2. Disjoint Terminal Factorization: $\{T_{\mathrm{exact}}, T_{\mathrm{survivor}}, T_{\mathrm{refusal}}\}$

Under `omega_wdp::coda::coda_gtla` and `layer9_coda_gtla.rs`, any resolution trajectory must partition into exactly one terminal state:

1. **$T_{\mathrm{exact}}$ (Exact Coboundary Reduction):**
   - Condition: $\Phi_1([x]) = 0$ and $\Gamma_2(x) = 0$.
   - Semantics: The cochain is certified as an exact coboundary $x = d_0 t$. The residual vanishes entirely.
2. **$T_{\mathrm{survivor}}$ (Closed Harmonic Survivor):**
   - Condition: $\Phi_1([x]) > 0$ and $\Gamma_2(x) = 0$.
   - Semantics: The cochain is a closed 1-cocycle spanning a non-trivial homology class. The defect cannot be eliminated by local gauge shifts and is preserved in the persistent harmonic register.
3. **$T_{\mathrm{refusal}}$ (Curvature or Authorization Refusal):**
   - Condition: $\Gamma_2(x) > 0$ (unclosed boundary defect) or invalid context license.
   - Semantics: Fail-closed halting. No structural mutation or lift is admitted.

---

## 3. Primal-Dual Witness Certification over $\mathbb{Q}$

To certify quotient distance without floating-point error, CODA employs exact rational linear programming duality:

- **Primal Problem:**
  $$\Phi_1([x]) = \min_{t \in C^0} \|x - d_0 t\|_1$$
- **Dual Problem:**
  $$\Phi_1^*([x]) = \max \left\{ \langle y, x \rangle : y \in C^1, \|y\|_\infty \le 1, d_0^T y = 0 \right\}$$

By LP strong duality on finite finite-dimensional complexes over $\mathbb{Q}$:
$$\Delta_{\mathrm{duality}} = \Phi_1([x]) - \Phi_1^*([x]) = 0$$

Every terminal receipt contains the primal solution $t$, the dual certificate $y$, and the verified zero duality gap.

---

## 4. Check for Understanding

1. Why must the three terminal variants $\{T_{\mathrm{exact}}, T_{\mathrm{survivor}}, T_{\mathrm{refusal}}\}$ be pairwise mutually exclusive?
2. What role does the dual certificate vector $y \in \ker(d_0^T)$ play in certifying the optimality of $t$?
3. Why does a $T_{\mathrm{exact}}$ receipt explicitly carry `AuthorityEffect: None` rather than an authority grant?

---

## 5. Laboratory Workbench

- Companion Workbench: [Interactive Laboratory Notebook](../notebooks/lesson_740_01_terminal_factorization.ipynb)
