Status: AI-drafted, awaiting human review.

# COMP-C6-TM0-OUTPUT-FORM-OPEN one blank cell

The node stays OPEN. This note records one writer and one constant evaluator. It does not read the tape of M0.

## The cell

A cell is a pair `(halted, value)`. A blank cell is `(false, 0)`.

## The writer

`writeHalt v` leaves a halted cell unchanged. On a cell that has not halted, it returns `(true, v)`.

From a blank cell the result is `(true, v)`.

## The evaluator

`evalConst v n` ignores `n` and returns `v`. That return value is the value in the cell produced from the blank cell.

## What is proved

- For every natural number `v`, writing `v` into the blank cell `(false, 0)` yields `(true, v)`.
- For every natural number `n`, `evalConst v n` equals `v`.
- The value in that written cell equals `evalConst v n`.

The Lean declarations are `writeHaltFromBlank`, `evalConstReturns`, and `constAgrees` in `lean4/CampaignCompC6Tm0OutputFormOpen.lean`.

## What is assumed

Boolean conditionals and natural-number equality in the Lean kernel. No new axiom is declared. The node status stays OPEN.

## What is open

A natural number `v` lying in `Code.eval c n` exactly when `M0` halts from `initCfg0` with the encoded `v` on its output tape is not given here.
