# Finite relational and SQL examples

AuthorityEffect: None. GenesisEffect: None.

This is an externally designed teaching model. It is not a transcript of the
frozen 19L57G1 experiment or a derivation of this domain from the literal `<>`.
The Python `step_01_admit_root` method inserts a label in its local carrier;
canonical Genesis `Supply` leaves admitted carrier data unchanged. Relating
those operations requires an explicit interpretation rather than identical names.

## Implemented mathematical content

The package contains relational schemas, boundary-matrix computations, determinant
examples, and separately scoped SQL fixtures. A SQL/Python comparison checks the
submitted instances. A general bisimulation theorem would need a state relation
and preservation and reflection of every declared transition.

SQL NULL is handled by a chosen three-valued truth table. That table is finite;
it is not an obstruction to finite representation or a continuum problem.
Query transformations need explicit treatment of NULL, duplicate rows and
aggregation. Recursive queries need a termination argument or a declared bound.

The [former bisimulation receipt](bisimulation_receipt.md) records withdrawals.
The [physics cleanup](../../physics_claim_cleanup.md) governs removed anyon,
braiding and physical-recovery claims. Retained matrix arithmetic remains useful
without promoting a fixture comparison to a theorem about all SQL programs.

## Proof and model boundaries

The [Lean core](lean4/ansi_sql_core.lean) proves the elementary implication

\[
(\forall x,\neg r(x,x))\;\land\;r(a,b)\quad\Longrightarrow\quad a\ne b.
\]

Its `Cotrans` declaration is a predicate definition, not a proof that arbitrary
relations satisfy cotransitivity. Additional theorems have the assumptions shown
in their actual statements. Elaborating a file checks those statements; it does
not check the Python implementation or establish a source correspondence.

The former Lean predicate `ThreeValuedNullObstruction` was
`∀ f : X → X, f a = a`. This characterizes a singleton carrier: constant functions
show that every element must equal `a`. It therefore cannot certify a claim
about continuum recovery, halting, SQL NULL or gradients. The corrected core
names it `EveryEndomapFixesRoot`, proves its exact meaning, and proves that an
irreflexive witnessed pair refutes it.

Python's `check_gap_obstruction` retains `ThreeValuedNullObstruction` as a legacy
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
