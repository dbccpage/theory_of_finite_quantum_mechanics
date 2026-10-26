---
documentation_contract: education-documentation/v1
title: "Lesson 600.01: the base seed"
kind: pedagogical-lesson
authority_effect: "None"
claim_status: verified
last_verified: 2026-10-08
---

# Lesson 600.01: the base seed

**AuthorityEffect:** None.

**Pin:** `dbccpage/H3V7N5QF@5d9488324ce976817987bd83a28d901371cfc073`.

This track is not the front door.

## Read this

- Read `prompt/seed_prompt.md` and `code/xry/state.py` in the pinned package.
- `given(False, Sameness.ANCHORED)` asserts `arb` and leaves `bra` out. `given(True, Sameness.ANCHORED)` asserts both.
- Ledger D2 says these are the two legal states on the given terms that contain `arb`.

## Check

Why does `given` take a Boolean for `bra`?

The answers are in the pinned files cited above, and in the companion notebook.

## Notebook

[Companion notebook](../notebooks/lesson_600_01_genesis_ongoing_architecture.ipynb)
