# Finite transition and fuel examples

AuthorityEffect: None. GenesisEffect: None.

This is an externally designed teaching model. It is not a transcript of the
frozen 19L57G1 experiment or a derivation of this domain from the literal `<>`.
The Python `step_01_admit_root` method inserts a label in its local carrier;
canonical Genesis `Supply` leaves admitted carrier data unchanged. Relating
those operations requires an explicit interpretation rather than identical names.

## Implemented mathematical content

The executable model includes finite graph transitions and a tape machine with
explicit fuel. A successful nonterminal step spends one unit of fuel. In the
Lean model this follows from the pattern match on a successor natural number;
it is not a theorem that every program terminates.

A repeated full configuration of a deterministic, unchanged transition system
establishes a cycle if every transition along the repeated segment is nonhalting.
The full configuration includes control state, head location and tape contents;
repeating a label or an observation alone is insufficient. A fuel limit with no
halt and no witnessed cycle yields unknown behavior beyond that bound.

Unbounded finite tape extension is enough for the usual Turing-machine model;
a preallocated infinite physical tape is not a necessary admission. Rice's theorem
concerns nontrivial semantic properties of partial computable functions, not a
blanket statement that all truth is uncomputable.

The Lean `BisimulationMapping` record is an injective relation-preserving and
relation-reflecting map onto its image. No transition-system back-and-forth law or
surjectivity onto a database model is supplied by that name.

## Proof and model boundaries

The [Lean core](lean4/computation_core.lean) proves the elementary implication

\[
(\forall x,\neg r(x,x))\;\land\;r(a,b)\quad\Longrightarrow\quad a\ne b.
\]

Its `Cotrans` declaration is a predicate definition, not a proof that arbitrary
relations satisfy cotransitivity. Additional theorems have the assumptions shown
in their actual statements. Elaborating a file checks those statements; it does
not check the Python implementation or establish a source correspondence.

The former Lean predicate `HaltingIncompletenessObstruction` was
`∀ f : X → X, f a = a`. This characterizes a singleton carrier: constant functions
show that every element must equal `a`. It therefore cannot certify a claim
about continuum recovery, halting, SQL NULL or gradients. The corrected core
names it `EveryEndomapFixesRoot`, proves its exact meaning, and proves that an
irreflexive witnessed pair refutes it.

Python's `check_gap_obstruction` retains `HaltingIncompletenessObstruction` as a legacy
scenario label. It returns declared scope metadata, not the result of an
impossibility proof. No mathematical independence claim follows from that label
or from setting `gap_detected`.

## Reproduction and next connection

The [tests](tests/) exercise the actual local methods. Run individual test files
in separate processes where domain packages reuse top-level module names.
The [publication review](../../publication_review.md) records which checks were
run for the current corrections. A model bridge should map explicit source
states and transitions, then prove preservation of its chosen operations and
questions. These finite examples are useful inputs to that work.
