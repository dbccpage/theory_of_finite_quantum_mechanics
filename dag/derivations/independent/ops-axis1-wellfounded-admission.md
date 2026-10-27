Status: AI-drafted, awaiting human review.

# Finite admission chain

The node stays IMPORTED_ASSUMPTION. This note records one chain of three candidates. The Genesis theorem collapsed_of_no_insts is cited by name and is not re-run.

## Predecessors

Candidate 0 has no predecessor. Candidate 1 names candidate 0. Candidate 2 names candidate 1.

## Admission

Let b assign a boolean bit to each candidate. Admission of candidate 0 equals b at 0. Admission of candidate 1 equals the disjunction of b at 1 with admission of candidate 0. Admission of candidate 2 equals the disjunction of b at 2 with admission of candidate 1.

Unfolding the predecessor, admission of candidate 1 is the disjunction of b at 1 with b at 0, and admission of candidate 2 is the disjunction of b at 2 with that value.

## Two closed assignments

The assignment that is false at each candidate admits none of the three: each disjunction of false bits is false.

The assignment that is true at candidate 0 and false at candidate 1 and at candidate 2 admits all three. Candidate 0 reads the true bit. Candidate 1 reads a false bit disjoined with that true admission. Candidate 2 reads a false bit disjoined with the true admission of candidate 1.

## What is proved

The predecessor table, the three admission equations for every base assignment, the three bits of each closed assignment, and the three admission bits of each closed assignment. The Lean declarations are pred0, pred1, pred2, adm0, adm1, adm2, none0, none1, none2, zb0, zb1, zb2, zero0, zero1 and zero2 in lean4/ObserverPresheafAxis1WellfoundedAdmission.lean. The independent script recomputes the same equations on all eight base assignments.

## What is assumed

The three-candidate predecessor table and boolean disjunction, stated as definitions. No new axiom is declared. The node status stays IMPORTED_ASSUMPTION.

## What is open

The Genesis theorem collapsed_of_no_insts is not re-run. No source in this graph relates that theorem to the admission-gate node. Other shapes of admission stay outside this chain.
