---
documentation_contract: symbol-game-documentation/v1
title: 'Finite relational joins and protected queries'
kind: application-reference
layer: downstream_application
realizes: null
legacy_level: 21
authority_effect: 'None'
genesis_effect: 'None'
---

# Finite relational joins and protected queries

This is a declared downstream set-relation model. The filename's 21 is a
historical topic locator, not a native S(21) stage. No topology or Genesis
lift follows from executing a join. Begin with the
[relational-query model](../../code/sn_applications.py); its lesson and
notebook were retired on 2026-10-06.

## Join before discarding information

Declare R(A,B)={(a0,b0),(a1,b1)} and
S(B,C)={(b0,c0),(b0,c1),(b1,c1)}. Their natural join has exactly
three tuples: (a0,b0,c0), (a0,b0,c1), (a1,b1,c1). This example uses set
semantics, declared equality and no null values. Bag multiplicity, SQL nulls
and transaction behavior require their own semantics.

Projecting onto A loses a protected question: “is C=c0?” The first two
tuples have the same projected report a0 and opposite answers. Thus no
decoder from the A report alone can recover that question. This is the
[WDP fiber-constancy criterion](../../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/genesis_to_wdp_derivation_programme.md),
with an explicit conflicting fiber. Protecting only “is A=a0?” would allow
the projection. Adequacy depends on the declared question.

## Overlap agreement can miss global inconsistency

On binary columns A,B,C, take AB={(0,0),(1,1)}, BC={(0,0),(1,1)} and
AC={(0,1),(1,0)}. Every overlap projection is {0,1}, yet the triple join is
empty: A=B=C contradicts A≠C. This is a finite relational compatibility
counterexample. A sheaf claim additionally needs an explicit site,
restriction functor, admissible reports and gluing conditions.

Explain the conflicting fiber before running the lab. Then replace the
protected query and predict whether projection becomes adequate. Keep
local agreement, existence of a joint record and physical truth separate.
