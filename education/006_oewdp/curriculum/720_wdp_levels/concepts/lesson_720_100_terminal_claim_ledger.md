---
documentation_contract: symbol-game-documentation/v1
title: "Lesson 720.100: Level 100 Terminal Open Horizon Claim Ledger Walkthrough"
kind: pedagogical-lesson
track: 720
status: active
maturity: production
claim_status: verified
authority_effect: "None"
---

# Lesson 720.100: Level 100 Terminal Open Horizon Claim Ledger Walkthrough

**AuthorityEffect:** None.  
**Track:** 720 (WDP Derivation Levels)  
**Topic:** Level 100: Terminal Open Horizon Claim Ledger & Receipt Gate

## 1. Pedagogical Objective
Examine the terminal claim ledger gate, verifying raw byte-level SHA-256 digests against Git object IDs with zero authority assertion.

## 2. Invariants
- Terminal Gate: Raw SHA-256 file digests verified against framed Git object IDs.
- Zero Authority: Terminal gate asserts no external authority; pure cryptographic verification.
- Open Horizon: Unproven generality left explicitly open.
- Hermetic Parity: Bit-for-bit repository checksum parity.

## 3. Check for Understanding
- Why is the distinction between raw SHA-256 byte sums and framed Git object IDs essential?
- How does Level 100 enforce zero authority assertion at the terminal gate?

## 4. Laboratory Workbench
- Companion Workbench: [Interactive Laboratory Notebook](../notebooks/lesson_720_100_terminal_claim_ledger.ipynb)
