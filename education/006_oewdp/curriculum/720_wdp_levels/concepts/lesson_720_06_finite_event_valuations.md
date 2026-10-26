---
documentation_contract: symbol-game-documentation/v1
title: "Lesson 720.06: Level 06 Duration, Exactness, Periods, and Clocks Walkthrough"
kind: pedagogical-lesson
track: 720
status: active
maturity: production
claim_status: verified
authority_effect: "None"
---

# Lesson 720.06: Level 06 Duration, Exactness, Periods, and Clocks Walkthrough

**AuthorityEffect:** None.  
**Track:** 720 (WDP Derivation Levels)  
**Topic:** Level 06: Duration, Exactness, Periods, and Clocks

## 1. Pedagogical Objective
Formalize duration as an additive valuation on discrete paths, distinguishing path-independent duration from cyclic period obstructions.

## 2. Invariants
- Additive Valuation: Valuation v: E -> Q assigning exact rational weight to transitions.
- Path Duration: D(p) = sum_{e in p} v(e) for path p.
- Path Independence: D(p1) = D(p2) for all paths p1, p2 with same endpoints iff cycle valuation vanishes.
- Clock Packet: A periodic cycle with non-zero valuation functioning as a discrete reference clock.

## 3. Check for Understanding
- What condition renders duration path-independent on a finite complex?
- How is a discrete clock packet constructed without assuming continuous time?

## 4. Laboratory Workbench
- Companion Workbench: [Interactive Laboratory Notebook](../notebooks/lesson_720_06_finite_event_valuations.ipynb)
