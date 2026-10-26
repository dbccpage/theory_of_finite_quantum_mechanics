---
documentation_contract: education-documentation/v1
title: "Lesson 720.05: Level 05 Recurrence, Succession, and Constitutive Order Walkthrough"
kind: pedagogical-lesson
track: 720
status: active
maturity: production
claim_status: verified
authority_effect: "None"
---

# Lesson 720.05: Level 05 Recurrence, Succession, and Constitutive Order Walkthrough

**AuthorityEffect:** None.  
**Track:** 720 (WDP Derivation Levels)  
**Topic:** Level 05: Recurrence, Succession, and Constitutive Order

## 1. Pedagogical Objective
Master the distinction between bare recurrence and constitutive succession, formalizing strict partial orders on reachability DAGs without assuming an external clock.

## 2. Invariants
- Succession Order: Strict partial order (X, <) on event occurrences.
- DAG Reachability: Event b succeeds a iff there exists a finite chain of elementary transitions from a to b.
- No External Clock: Succession is constitutive to the event DAG, not referenced to an ambient scalar time.
- Fork Branching: Branching points preserve partial ordering without forcing total order linearization.

## 3. Check for Understanding
- Why is bare recurrence insufficient to establish succession?
- How does a strict partial order avoid circular time paradoxes in discrete complexes?

## 4. Laboratory Workbench
- Companion Workbench: [Interactive Laboratory Notebook](../notebooks/lesson_720_05_retention_discrete_succession.ipynb)
