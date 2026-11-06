---
documentation_contract: education-documentation/v1
title: "Lesson 710.02: Exact Quotient Obstruction and Dual Certificates"
kind: pedagogical-lesson
track: 710
status: active
maturity: production
claim_status: verified
authority_effect: "None"
---

# Lesson 710.02: Exact Quotient Obstruction and Dual Certificates

**AuthorityEffect:** None.  
**Track:** 710 (Finite Obstruction Calculus)  
**Topic:** Quotient Norm Phi_1([h]), Two-Phase Simplex, and Divergence-Free Dual Circulations

## 1. Pedagogical Objective
Understand how the degree-1 quotient norm $\Phi_1([h]) = \min_f \|h - d_0 f\|_{1,w}$ is computed via exact two-phase simplex over `fractions.Fraction`, and how strong duality certifies the minimal residual using a dual divergence-free circulation $y$ ($d_0^* y = 0$).

## 2. Key Concepts
1. **The Primal Optimization:** Find a vertex potential $f \in C^0$ minimizing the weighted $\ell_1$ distance to the declared edge cochain $h$.
2. **The Dual Certificate:** A dual vector $y \in C_1$ satisfying:
   - Feasibility: $|y_e| \le w_e$ for all edges $e$.
   - Annihilation: $d_0^* y = 0$ (the dual circulation has zero divergence at every vertex).
   - Strong Duality: $\sum_e y_e h_e = \Phi_1([h])$.
3. **Independent Recomputation:** A quotient certificate is accepted only after recomputing the primal residual, dual divergence, and duality equality.

## 3. Check for Understanding
- Why is an $\ell_1$ quotient norm preferred over an $\ell_2$ projection in discrete obstruction calculus?
- What physical interpretation corresponds to the dual circulation $y$ being divergence-free?

## 4. Laboratory Workbench
- Companion Workbench: [Interactive Laboratory Notebook](../notebooks/lesson_710_02_exact_quotient_obstruction.ipynb)
