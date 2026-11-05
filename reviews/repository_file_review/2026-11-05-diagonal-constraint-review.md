# Diagonal constraint and kernel-projector review

AuthorityEffect is None.

The original fixed-matrix calculation agrees with ConstraintKernelProjector.lean.
The original application and companion are preserved byte for byte. The original
script lacked an admitted reusable operator boundary and independent challenges.

DiagonalConstraint now owns three rational coefficients and provides exact matrix,
kernel basis/projector, spectrum, rank, sign classification, application, projection,
membership and quadratic queries. The common rational matrix backend enforces
stored-value, product and dot-prefix budgets before later cancellation. Membership
uses zero-coordinate logic without arithmetic that could exceed those budgets.
Quadratic evaluation applies H first, including the zero-operator boundary.

The application retains the original integer fixture, all 125 vectors, symbolic
residual orthogonality and exact CLI output. Its default 638 guard calls are
independently counted. The radius admits native integers 0..4, with 729 vectors
and 3658 guards at the cap. All 64 candidate triples over {-1,0,1,2} are challenged;
only the declared operator passes the fixture contract.

Two sets of 80 deterministic rational property examples use independent SymPy
matrices and nullspaces. The projector oracle forms B(B^T B)^-1 B^T from the
nullspace. All 27 zero/sign patterns, multiplicities and full/zero rank cases are
covered. Tests include shape preflight, exact domains, input and intermediate
budgets, cancellation, ownership, immutable controls, typed failure, CLI status,
quiet imports, repeatability and RuntimeError/KeyboardInterrupt/SystemExit propagation.

Strict typing, 11 new test groups and 24 prior integration groups pass normally
and optimized. All 45 critical fault recipes are killed against final source
hashes, including shared term/prefix budgets and corrupted oracle/refusal helpers.
The earlier typing failure and its exact test bytes remain recorded.

The source correspondence covers the declared diagonal integer model. Python's
reusable rational family has its separate finite resource contract. This does
not supply a general Wheeler-DeWitt operator or a continuum construction.
The full cited Lean source was read; fresh Lean builds and hosted CI have their
own evidence. The three sources have retention 5 and completed L4B records.
The next file is fsp-hubbard-protected-representations.py.
