---
documentation_contract: symbol-game-documentation/v1
title: "Lesson 720.14: Level 14 Authority is a Separate Layer Walkthrough"
kind: pedagogical-lesson
track: 720
status: active
maturity: production
claim_status: verified
authority_effect: "None"
---

# Lesson 720.14: Level 14 Authority is a Separate Layer Walkthrough

**AuthorityEffect:** None.  
**Track:** 720 (WDP Derivation Levels)  
**Topic:** Level 14: Authority is a Separate Layer

## 1. Pedagogical Objective
Separate typed authority packets from verification, observation, and status layers, enforcing cryptographic provenance receipts.

## 2. Invariants
- Layer Separation: Authority != Verification != Observation != Status.
- Authority Packet: Auth = (Grantor, Jurisdiction, Scope, Signature).
- Immutable Receipt: Provenance receipts append-only with hash-chain integrity.
- No Auto-Escalation: Verification receipts never auto-promote into authority grants.

## 3. Check for Understanding
- Why must authority be maintained as a separate layer from verification?
- How do hash-chain provenance receipts prevent unauthorized status escalation?

## 4. Laboratory Workbench
- Companion Workbench: [Interactive Laboratory Notebook](../notebooks/lesson_720_14_traceability_provenance_receipts.ipynb)
