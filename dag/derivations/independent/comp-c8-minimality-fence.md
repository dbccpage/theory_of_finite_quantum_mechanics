Status: AI-drafted, awaiting human review.

# COMP-C8-MINIMALITY-FENCE

Node status stays OPEN. This note records one closed tape. It does not simulate a machine, and it does not state a minimality sentence.

## The closed tape

Mark A is the number 1. Mark B is the number 2. The blank is the number 0.

Appending one blank cell to a word writes that word and then the blank. On the word mark A then mark B, the result is the list whose entries are 1, then 2, then 0. That list has length 3.

The blank number is different from 1 and different from 2, so it differs from mark A and from mark B.

## What is proved

The three number identities, the one appended list, its length 3, and the two differences.

## What is assumed

The two marks and the blank are these three numbers. Appending a cell is list concatenation. AuthorityEffect is None. No package is imported.

## What is open

Simulation of a machine over a coded alphabet by a machine over the two marks and a blank stays open. A sentence that composite machine M0 is not a smallest general-purpose machine stays open. Small-machine records stay literature only. The letter-by-letter code of a finite alphabet stays on the sibling record COMP-C8-BINARY-CODING.
