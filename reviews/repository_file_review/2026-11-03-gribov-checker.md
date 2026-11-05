# Finite Gribov weighted-trace checker review

AuthorityEffect: None.

The application and independent suite receive retention label 5 and completed
L4B assessments in adjacent source-bound contracts. Label 5 is not a claim of
perfection. Prior contract histories, where present, remain intact.

The original helpers assumed 3x3 inputs but did not validate shape or entry
types before indexing and multiplication. They accepted arbitrary iterables,
lacked arithmetic budgets, and used SystemExit for verification failures.
The repaired boundary admits exactly three owned rows of three exact rational
entries, excluding bool/float/foreign values. Every row's shape is checked before
entry conversion. Multiplication is composed into the existing independent
RationalMatrix instead of maintained as duplicate arithmetic. Each input,
product, accumulation, trace prefix and final difference stays within a
4096-bit rational numerator/denominator budget.

TraceQuadraticForm is the sole production class. It owns the supplied weight and
provides Railway value and difference operations for Tr(weight*H^2). Both
difference operands are admitted before arithmetic. A zero value/difference is
a successful mathematical result; domain/resource refusal is a typed failure.
The weight and generator need not be symmetric, and positivity is not claimed.
The retained fixed witnesses have weights I and diag(1,-1,-1), generators H23
and H12, and form values 2, -2 and 0.

The original combined predicates are now ten separately counted obligations:
two generator squares, the weight square and diagonal determinant, two traces,
three form values and their difference. The CLI emits a JSON count and returns
a nonzero exit code on failure. Exact/mat/mul/trace/diag helper names and detached
row-tuple formats remain. No external Python consumer of the former prose
receipt was found.

The 11-group independent suite compares generated exact 3x3 matrices against
SymPy, with 80 deterministic examples per property. A fixed nonsymmetric fixture
detects order and transpose faults hidden by the original symmetric examples.
Tests also cover snapshot ownership, full scalar budgets, conservative prefix
refusal despite later cancellation, shape preflight, typed Railway failures,
actual executable exits, cancellation and unexpected programming errors.
Strict typing and this suite plus the 24-group integration suite pass normal
and optimized Python. Each source contains at most one class and satisfies the
B structural limits recorded in the quality receipt.

All 30 critical mutation candidates are retained and detected. The initial run
detected 29: the matrix-transpose mutant survived its selected fixed test because
that test did not call mat. The generated helper suite already covered mat.
One exactly additive call makes the deterministic selector cover constructor
preservation as well; its baseline, failure output, original outcome and initial
test/quality snapshots are retained separately.

The full Lean origin and current consumers were read. They establish finite
rational matrix identities; no continuum operator, Gribov region or gauge-fixing
construction follows. The shared matrix implementation belongs to independent
checker infrastructure, and separate symbolic calculations provide the oracle.
No new Lean build, hosted CI or scientific DAG promotion is claimed.
