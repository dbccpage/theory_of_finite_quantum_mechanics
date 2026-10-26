---
documentation_contract: education-documentation/v1
title: "Lesson 710.01: The 11 WDP Foundational Bridges"
kind: pedagogical-lesson
track: 710
status: active
maturity: production
claim_status: verified
authority_effect: "None"
---

# Lesson 710.01: The 11 WDP Foundational Bridges

**AuthorityEffect:** None.\
**Track:** 710 (Finite Obstruction Calculus)\
**Topic:** The 11 Core Foundational Bridges connecting Genesis to Measurement

## 1. Pedagogical Objective
Examine how each of the 11 foundational derivation bridges operates with exact rational arithmetic, discrete cochain nilpotency, and zero authority leakage.

## 2. The 11 Bridges
1. **Bridge 1:** Inscription and Structure $\to$ Distinct Admitted Marks. The datum $\langle\rangle$ is opaque; generating marks requires declared constructors and admission laws, where an admitted relation instance $R(a,b)$ plus protected irreflexivity implies distinctness $a \neq b$ (`GEN-WDP-01..02`, retaining `WDP-CH00-N01`).
2. **Bridge 2:** Marks $\to$ Algebra, Cochains, and Quotients ($d_1 \circ d_0 = 0$).
3. **Bridge 3:** Genesis Histories $\to$ Contextual Observers (Transducers and products).
4. **Bridge 4:** Observers $\to$ Probability and Multiplicity (Exact rational distributions).
5. **Bridge 5:** Reports $\to$ Evaluation (`EvaluationStatus`).
6. **Bridge 6:** Evaluation $\to$ Authorization (`AuthorityEffect::None`).
7. **Bridge 7:** Triangle Parity Law (Odd distinct marks parity = 1).
8. **Bridge 8:** Rational $\ell_1$ Attainment on Finite Lists (Computes exact rational $\ell_1$ minimum on non-empty finite rational candidate lists; does not assert unconstrained rational attainment under arbitrary norms).
9. **Bridge 9:** Flat Locus Invariance ($d^2 = 0$).
10. **Bridge 10:** Frustrated All-Edge Anticorrelation (No global binary assignment satisfies $s_i \oplus s_{i+1} = 1$ on an odd cycle, while unconstrained global binary assignments exist).
11. **Bridge 11:** Deterministic Retention and Succession Posets (Strict partial orders of reachability on acyclic graphs, supporting explicit branching forks).

> [!NOTE]
> **Implementation Status:** The enlarged programme is registered in [`docs/genesis_bridge_register.md`](/atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/docs/genesis_bridge_register.md) (`GEN-WDP-01..10`, `GEN-WDP-O01..O05`). The paper contains `code/witnessed_difference/foundational_bridges.py`, `code/rust/src/foundational_bridges.rs` and `lean4/WitnessedDifference/FoundationalBridges.lean`; their statements have their own finite or conditional domains. The eleven survey headings are not eleven canonical bridge-register IDs. This notebook executes the triangle chain equation and the eight-assignment odd-cycle counterexample. The [admission and transport lab](lesson_710_04_admission_and_transport.md) adds the explicit floor, retraction and homotopy examples.

## 3. Check for Understanding
- Why does an odd cycle (e.g. triangle) admit binary assignments generally, but fail to admit any assignment satisfying all-edge anticorrelation ($s_i \oplus s_{i+1} = 1$)?
- Why does generating distinct marks from $\langle\rangle$ require declared constructors and admission laws rather than "difference alone"?

## 4. Laboratory Workbench
- Companion Workbench: [Interactive Laboratory Notebook](../notebooks/lesson_710_01_foundational_bridges.ipynb)
