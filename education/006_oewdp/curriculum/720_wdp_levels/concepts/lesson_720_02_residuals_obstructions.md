---
documentation_contract: symbol-game-documentation/v1
title: "Lesson 720.02: Level 02 Residuals and Obstructions Walkthrough"
kind: pedagogical-lesson
track: 720
status: active
maturity: production
claim_status: verified
authority_effect: "None"
---

# Lesson 720.02: Level 02 Residuals and Obstructions Walkthrough

**AuthorityEffect:** None.  
**Track:** 720 (WDP Derivation Levels)  
**Topic:** Level 02: Residual Vectors, Obstruction Norms, and Farkas Certificates

## 1. Pedagogical Objective
Work through Level 02 to understand how the discrepancy between a target field and an exact boundary gradient is measured as a residual vector $r = \delta - d_0 f$, and certified by an exact dual witness.

## 2. Invariants
- Residual Formula: $r = \delta - d_0 f$.
- $\ell_1$ Metric: $\|r\|_{1,w} = \sum_e w_e |r_e|$.
- Dual Bound: Dual circulation $y$ with $|y_e| \le w_e$ satisfying $d_0^* y = 0$ achieves $\sum_e y_e \delta_e = \|r\|_{1,w}$.
- Non-Repair Invariant: Detecting a non-zero residual does not automatically repair or rewrite the complex.

## 3. Check for Understanding
- Why is a non-zero residual vector described as an "obstruction"?
- How does the dual certificate prove that no potential $f$ can achieve a smaller residual?

## 4. Laboratory Workbench
- Companion Workbench: [Interactive Laboratory Notebook](../notebooks/lesson_720_02_residuals_obstructions.ipynb)
