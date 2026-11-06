---
documentation_contract: education-documentation/v1
title: "Lesson 720.03: Level 03 Discrete Complex and Cochains Walkthrough"
kind: pedagogical-lesson
track: 720
status: active
maturity: production
claim_status: verified
authority_effect: "None"
---

# Lesson 720.03: Level 03 Discrete Complex and Cochains Walkthrough

**AuthorityEffect:** None.  
**Track:** 720 (WDP Derivation Levels)  
**Topic:** Level 03: Finite Complexes, Cochain Complexes, and Boundary Nilpotency

## 1. Pedagogical Objective
Work through Level 03 to master the formal construction of discrete complexes consisting of vertices $C_0$, edges $C_1$, and faces $C_2$, verifying exact algebraic nilpotency $d_1 \circ d_0 = 0$ over rational coefficients.

## 2. Invariants
- Finite Complex: $K = (V, E, F)$ with oriented edges $(u, v)$ and oriented triangular faces $(u, v, w)$.
- Coboundary Operators:
  - $(d_0 f)(u, v) = f(v) - f(u)$
  - $(d_1 h)(u, v, w) = h(u, v) + h(v, w) - h(u, w)$
- Nilpotency Invariant: $d_1(d_0 f) = 0$ holds identically for every vertex 0-cochain $f$.

## 3. Check for Understanding
- Why is boundary nilpotency ($d^2 = 0$) an algebraic prerequisite for defining cohomology groups?
- How does discrete orientation avoid circularity or topological leakage?

## 4. Laboratory Workbench
- Companion Workbench: [Interactive Laboratory Notebook](../notebooks/lesson_720_03_discrete_complex_cochains.ipynb)
