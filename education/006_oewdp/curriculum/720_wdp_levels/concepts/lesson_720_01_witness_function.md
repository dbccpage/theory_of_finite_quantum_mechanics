---
documentation_contract: symbol-game-documentation/v1
title: "Lesson 720.01: Level 01 Witness Function Walkthrough"
kind: pedagogical-lesson
track: 720
status: active
maturity: production
claim_status: verified
authority_effect: "None"
---

# Lesson 720.01: Level 01 Witness Function Walkthrough

**AuthorityEffect:** None.  
**Track:** 720 (WDP Derivation Levels)  
**Topic:** Level 01: The Witness Function and Nonclaim Firewall

## 1. Pedagogical Objective
Examine how Level 01 formalizes the witness function, creating an immutable `WitnessReceipt` that records interactions and registrations without conferring authority standing (`WDP-CH02-N01`).

## 2. Invariants
- Distinction $\neq$ Authority: A witness records an interaction; it never confers permission.
- Immutable Receipt: `WitnessReceipt(registration, interaction, authority_effect=AuthorityEffect.NONE)`.
- Verified Separation: Evaluator status (`Accept`, `Reject`, `Refuse`) is isolated from the witness registration.

## 3. Check for Understanding
- Why is an execution witness prohibited from carrying authority?
- How does the witness function preserve non-learning and non-authority boundaries?

## 4. Laboratory Workbench
- Companion Workbench: [Interactive Laboratory Notebook](../notebooks/lesson_720_01_witness_function.ipynb)
