# Finite relations and simplicial examples

AuthorityEffect: None. GenesisEffect: None.

This is an externally designed teaching model. It is not a transcript of the
frozen 19L57G1 experiment or a derivation of this domain from the literal `<>`.
The Python `step_01_admit_root` method inserts a label in its local carrier;
canonical Genesis `Supply` leaves admitted carrier data unchanged. Relating
those operations requires an explicit interpretation rather than identical names.

## Implemented mathematical content

The executable model stores admitted labels and directed pairs. Its simplicial
helper constructs integer edge and triangle boundaries and multiplies the
boundary matrices. These are concrete finite calculations under the chosen
simplicial interpretation. The three `step_01`–`step_03` methods do not implement
the former document's advertised sixteen-step derivation.

For an oriented triangle, the cancellation is

\[
\partial_1\partial_2[a,b,c]
=(c-b)-(c-a)+(b-a)=0.
\]

This identity applies to the declared boundary operators; an arbitrary pair of
matrices of matching shape need not satisfy it. Integral homology additionally
needs the actual boundary maps and a valid quotient computation. Stored Betti
numbers and invariant factors in a Lean fixture do not perform that reduction.

The larger `mathematics_kernel.py` and `smith_normal_form.py` files contain finite
example implementations with their own tests. This note does not assert that
all their algorithms have been formally proved correct.

## Proof and model boundaries

The [Lean core](lean4/mathematics_core.lean) proves the elementary implication

\[
(\forall x,\neg r(x,x))\;\land\;r(a,b)\quad\Longrightarrow\quad a\ne b.
\]

Its `Cotrans` declaration is a predicate definition, not a proof that arbitrary
relations satisfy cotransitivity. Additional theorems have the assumptions shown
in their actual statements. Elaborating a file checks those statements; it does
not check the Python implementation or establish a source correspondence.

The former Lean predicate `UncountableContinuumObstruction` was
`∀ f : X → X, f a = a`. This characterizes a singleton carrier: constant functions
show that every element must equal `a`. It therefore cannot certify a claim
about continuum recovery, halting, SQL NULL or gradients. The corrected core
names it `EveryEndomapFixesRoot`, proves its exact meaning, and proves that an
irreflexive witnessed pair refutes it.

Python's `check_gap_obstruction` retains `UncountableContinuumObstruction` as a legacy
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
