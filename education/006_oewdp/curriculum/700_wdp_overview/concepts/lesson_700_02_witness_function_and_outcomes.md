---
documentation_contract: symbol-game-documentation/v1
title: "Lesson 700.02: The Witness Function and Outcome Monad"
kind: pedagogical-lesson
track: 700
status: active
maturity: production
claim_status: verified
authority_effect: "None"
---

# Lesson 700.02: The Witness Function and Outcome Monad

**AuthorityEffect:** None.  
**Track:** 700 (WDP Overview)  
**Topic:** Witness Receipts, Outcome[T], and the Nonclaim Firewall

## 1. Pedagogical Objective
Master the typed distinction between an operation and its verified witness receipt. Learn how Railway-Oriented Programming (ROP) enforces that every computational transition returns an explicit `Outcome[T]` (`Accepted[T]` or `Refused`) carrying `AuthorityEffect.NONE`, preventing silent failures and unearned authority.

## 2. Key Concepts
1. **The Witness Function:** An operation $f: A \to B$ does not confer authority; it yields a record of execution $(x, f(x), \text{proof})$.
2. **The Outcome Monad:** `Accepted(value, authority_effect=AuthorityEffect.NONE)` wraps valid outputs; `Refused(code, detail)` captures failures with typed enumeration codes (`RefusalCode.INVALID_INPUT`, `RefusalCode.SCOPE_VIOLATION`, etc.).
3. **The Nonclaim Rule (`WDP-CH00-N03`):** No computational outcome or witness receipt can be promoted to authority without explicit human signoff.

## 3. Check for Understanding
- Why is an explicit refusal code preferred over throwing a runtime exception?
- How does `AuthorityEffect.NONE` guarantee that execution receipts remain epistemically neutral?

## 4. Laboratory Workbench
- Companion Workbench: [Interactive Laboratory Notebook](../notebooks/lesson_700_02_witness_function_and_outcomes.ipynb)
