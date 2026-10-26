---
title: "Lesson 720.24: Which edits preserve balance?"
kind: pedagogical-lesson
track: 720
status: active
claim_status: scoped
authority_effect: "None"
---

# Lesson 720.24: Which edits preserve balance?

**AuthorityEffect:** None.

## Predict before calculating

Take four terms and the filled directed triangle 012. Begin with zero excess.
Predict what happens when you add one R assertion on 01, add it on 10, add a
term, or identify 0 with 3. Then ask whether your answer holds for every old
balanced input. An experiment with the zero table cannot answer that question.

## The rules and their reasons

[Proved] The written general proof is Appendix P.7 of the WDP manuscript:
growth retains old faces; an assertion update must avoid all marked directed
arcs; a merge must leave no surviving face touching its merged vertex; a new
filling equation must lie in the rational row span of existing equations.
Negative universal answers have legal raw counterstates. Selected Lean cycle
and tetrahedron laws check only part of this full written proof.

[Pinned] These rules use the canonical Source-25 kernel, independent directed
arc counts, nonnegative R/S multiplicities and its actual enablement rules.
They are not a change to those source semantics.

[Declared] Balance preservation and gradient-quotient descent are different
protected questions. A particular input/output answer is different again.

[Open] General covers, coherent higher fillers and physical interpretation
still need arguments. None of these diagnostics authorizes a Genesis extension.

## A useful falsifier

Fill 013, 023 and 123, and set only excess 20 to one. The new 012 equation
fails, despite the other three balances. Reverse arcs are independent.
Using seven directed face equations supplies the missing implication through
an eight-term identity, without assuming antisymmetry.

## Laboratory and explanation

Run the [companion notebook](../notebooks/lesson_720_24_balance_preserving_edits.ipynb).
It executes the native Rust example, including a disabled event refusal.
Set `CARGO_TARGET_DIR` to an external build cache first; Cargo dependencies and
the tracked lockfile must already be available for offline execution.
Explain why the particular zero-excess identification survives while its
universal verdict fails. The [storyboard](../scripts/lesson_720_24_balance_preserving_edits.md)
is a proposed recording, not evidence of a recorded video or a learner study.
