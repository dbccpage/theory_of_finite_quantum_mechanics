Status: AI-drafted, awaiting human review.

# Three codes on a two-point carrier

AuthorityEffect: None.

## Setup

The carrier has two points, named 0 and 1. Three codes each send a point to a point. The identity-table bit of a code is true when the code sends 0 to 0 and 1 to 1. The code-zero bit is true when the code is 0.

## Arithmetic

Code 0 sends 0 to 0 and 1 to 1, so its identity-table bit is true.
Code 1 sends 0 to 0 and 1 to 1, so its identity-table bit is true.
Code 2 sends 0 to 0 and 1 to 0, so its identity-table bit is false.
The code-zero bit is true at code 0, false at code 1, and false at code 2.

## What is proved

The six behavior entries, the three identity-table bits, and the three code-zero bits.

## What is assumed

Decidable equality of closed terms in Fin 2, Fin 3, and Bool.

## What is open

Rice's theorem for the programs of a Turing-complete language, including any claim that no total computable procedure is sound and complete for a nontrivial extensional property. Mathlib ComputablePred.rice and rice₂ are not instantiated. No semantic property of Nat.Partrec.Code is named. This table does not decide an infinite language.
