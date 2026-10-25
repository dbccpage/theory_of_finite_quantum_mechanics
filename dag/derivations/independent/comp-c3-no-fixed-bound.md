Status: AI-drafted, awaiting human review.

# COMP-C3-NO-FIXED-BOUND

## One letter and no rewrite step

The alphabet has one letter, written 0. A word is a finite list of that letter. There is no rewrite step. Bounded reachability at this stage is the reflexive relation: a word reaches a word exactly when the two lists are equal.

## The bound

The declared length bound is 1. The start word (0) has length 1, so it lies inside the bound, and it reaches itself. The empty word has length 0, so it also lies inside the bound, and (0) does not reach it. The word (0, 0) has length 2, so it lies outside the bound, and (0) does not reach it.

## What is proved

With no rewrite step, reachability is equality. At bound 1 the start word (0) reaches itself, does not reach the empty word, and does not reach (0, 0). The lengths are 1, 0 and 2.

## What is assumed

Lists and their lengths are the ambient data. No machine encoding is used.

## What is open

A computable map from an input to a start word, one bound that contains every halting start word, and a clash with normal-form reachability stay open.
