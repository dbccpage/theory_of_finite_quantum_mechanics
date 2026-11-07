# Electroweak doublet checker review

AuthorityEffect: None.

The repaired application and independent suite receive retention label 5 and
completed L4B assessments. Their adjacent companions bind the exact source and
retain prior histories. Label 5 is a retention judgment, not perfection.

The former duplicated Gaussian implementation and normalization exception are
composed into the shared independent-checker GaussianRational, Violation and
Outcome infrastructure. This removes two local classes and their arithmetic
maintenance surface. ElectroweakDoublet is the sole production class: it owns
two immutable Gaussian components and exposes Railway norm, scaling,
normalization and unit-action operations. Matrix helpers retain their four-entry
formats. No external Python callers of the removed local classes/methods or
changed control signatures were found in the consumer audit.

Malformed components, doublets and matrices previously could escape through
attribute errors or tuple-unpacking paths. All are now explicitly admitted
before arithmetic. Scalars exclude bool/float/foreign objects. Gaussian stored
components, squared norms, norm sums, root squares and returned components have
4096-bit rational budgets. Intermediate overflow is refused, even when a later
operation might reduce it. Phase enumeration is an owned snapshot of at most
64 unit phases, with at most 4226 obligations. Immutable component ownership,
preflight ordering, maximum-size inputs and typed resource failures are tested.

Normalization requires a supplied positive rational root and retains the
zeroNorm, nonpositiveScale and mismatchedSquare domain distinctions. This is not
a root-finding routine, and a rational root need not exist for every doublet.
The algebraic Lean division operation is total at zero; this executable's
division API deliberately requires a nonzero denominator. The checked
normalization API is the narrower positive-root portion of the Lean origin.

The old prose-only run did not count all its executed obligations and used
SystemExit throughout its internals. The new typed CLI reports 761 obligations:
738 normalization/action, 10 negative-input, 2 unnormalized and 11 witness checks.
The 3/5+4/5i witness and z=2 own-root counterexample remain. Failure injection
checks both the refusal controls and actual executable exit status.

The 15-group suite uses independent SymPy matrix/norm calculations, rational
unit-sphere generation, explicit nonreal fixtures and 80 deterministic examples
per generated property. It also tests ownership, error order, resource limits,
import restoration, cancellation and programming-error propagation. Strict
pinned typing and both this suite and the existing 24-group integration suite
pass normal and optimized Python. CCN/cognitive/nesting maxima are 7/7/3; each
reviewed source has one class.

All 39 critical mutation candidates are retained and detected. The original
run detected 35, retained one invalid-only test-selector survivor and three
property-shrinking timeouts. One additional deterministic nonreal matrix and
doublet fixture detects all four promptly. The original outcomes, initial
suite/quality record, exact additive amendment and follow-up baseline/output
remain separate. No timeout is counted as a kill without that follow-up.

The full Lean origin and current consumers were read. The finite executable
checks exact supplied-root normalization and residual covariance. It does not
construct continuum fields or electroweak dynamics. Shared code remains within
the independent-checking context; it is not the production scientific model
used as an oracle. No new Lean build, hosted CI or scientific DAG promotion is
claimed, and historical receipts retain their original source hashes.
