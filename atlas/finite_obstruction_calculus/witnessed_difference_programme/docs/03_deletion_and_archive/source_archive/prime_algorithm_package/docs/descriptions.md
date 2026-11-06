# Descriptions

AuthorityEffect: None.

## Abstract

The Omega Engine Algorithm Prime Triad formalizes bounded candidate intake, adapter descent, and continuation control across discrete reasoning loops. Prime 000 establishes a two-phase protocol separating candidate packet admission from execution and measurement; an unadmitted candidate packet cannot be measured, preventing premature metric evaluation. Prime 001 establishes adapter descent soundness across representations, requiring an explicit loss ledger whenever operations or distinctions are lost. Prime 002 establishes the master continuation predicate CanContinue, reconciling the canonical nine conjuncts with three-condition and eleven-condition representations, governed by six anti-cheat halting laws that enforce bounded operational termination (#ops ≤ ⌊B_tot / δ_control⌋). The core theorems are mechanized in Lean 4 without Mathlib using only propext and Quot.sound axioms.

## One line

A finite, exactly computed, Lean-checked operational calculus establishing admission-before-measurement, adapter descent, and anti-cheat continuation control for discrete reasoning systems.
