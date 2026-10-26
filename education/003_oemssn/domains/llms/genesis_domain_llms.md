# Finite token and precedence examples

AuthorityEffect: None. GenesisEffect: None.

This is an externally designed teaching model. It is not a transcript of the
frozen 19L57G1 experiment or a derivation of this domain from the literal `<>`.
The Python `step_01_admit_root` method inserts a label in its local carrier;
canonical Genesis `Supply` leaves admitted carrier data unchanged. Relating
those operations requires an explicit interpretation rather than identical names.

## Implemented mathematical content

The executable examples manipulate supplied token lists, strict precedence
relations and integer boundary matrices. They do not call an LLM, inspect its
weights, test a language-model benchmark, or establish semantic fidelity of a
produced answer.

For token positions with allowed edges from an earlier position to a later one,
strict index increase along every edge excludes directed cycles. A causal
attention mask may also include the diagonal; diagonal attention is not an edge
of this strict precedence graph. The graph calculation does not compute an
attention distribution or explain a transformer's reasoning.

Continuous derivatives can be represented symbolically and evaluated exactly in
restricted cases. Floating-point arithmetic is a computational choice, not a
logical requirement of differentiation. Whether an output satisfies a task
contract requires a task-specific checker; the parser and precedence graph alone
do not supply one.

## Proof and model boundaries

The [Lean core](lean4/llms_core.lean) proves the elementary implication

\[
(\forall x,\neg r(x,x))\;\land\;r(a,b)\quad\Longrightarrow\quad a\ne b.
\]

Its `Cotrans` declaration is a predicate definition, not a proof that arbitrary
relations satisfy cotransitivity. Additional theorems have the assumptions shown
in their actual statements. Elaborating a file checks those statements; it does
not check the Python implementation or establish a source correspondence.

The former Lean predicate `ContinuousGradientObstruction` was
`∀ f : X → X, f a = a`. This characterizes a singleton carrier: constant functions
show that every element must equal `a`. It therefore cannot certify a claim
about continuum recovery, halting, SQL NULL or gradients. The corrected core
names it `EveryEndomapFixesRoot`, proves its exact meaning, and proves that an
irreflexive witnessed pair refutes it.

Python's `check_gap_obstruction` retains `ContinuousGradientObstruction` as a legacy
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
