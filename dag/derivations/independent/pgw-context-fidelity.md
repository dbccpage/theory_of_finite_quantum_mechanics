Status: AI-drafted, awaiting human review.

# PGW-CONTEXT-FIDELITY narrowed boundary

AuthorityEffect: None.

The node stays OPEN. The census below is one two-code model. It is not a reading of Trial 2.

## Two codes

The stale declared context is the code 0. The replayed context is the code 1. These codes differ.

The empty-claim step holds at a code exactly when that code is 0. It holds at 0 and fails at 1.

The binding check accepts a declared code and a replayed code exactly when the two codes are equal. It refuses the pair (0, 1) and accepts the pair (1, 1). It also accepts (0, 0) and refuses (1, 0).

The four ordered pairs drawn from {0, 1} are (0, 0), (0, 1), (1, 0), and (1, 1). Exactly two of them are accepted, and those two are the pairs in which the codes agree.

## What is proved

The integer facts in the two-code model: 0 differs from 1, the empty-claim step holds at 0 and fails at 1, and the equality binding accepts 2 of the 4 ordered pairs.

## What is assumed

Integer equality and the two definitions in the model. The codes are not read from a trial log.

## What is open

Trial 2 Result 15, Prompt 12, Prompt 17, and a general ValidTrace semantics. A verifier that reconstructs a history and accepts a declared context only when it equals that replay stays open. The node status stays OPEN.
