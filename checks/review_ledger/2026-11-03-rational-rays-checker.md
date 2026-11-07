# Rational-ray obstruction checker review

AuthorityEffect: None.

The repaired application and independent test source receive retention **5**
and completed **L4B** assessments with adjacent contracts, bringing the
current distinct completed total to 80. The original source had no companion
and remains byte-archived. Label 5 is a retention decision, not perfection.

Initial probes show that the old raw function accepted floats, booleans and
the zero vector; its dot product silently ignored a fourth coordinate.
Its helper for two odd coordinates accepted even inputs. Import executed the
entire search, mutated global counters and exited the process. Arithmetic and
enumeration had no explicit input budget. Its prose described every triple
in a box, while its actual algorithm completed pairs with a cross product
that could leave the box.

`IntegerRay3` now owns an exact nonzero integer triple normalized by its gcd
and the sign of its first nonzero coordinate. Equality and hashing identify
the represented rational ray. Even representatives are normalized before
evaluation; the old raw parity formula is not applied to them. All input,
product, term and prefix integers have a 4096-bit budget. Fallible operations
return typed outcomes; unexpected programming errors and interruptions
propagate. Imports are quiet and every verification run has its own counter.

The box radius is admitted in 1–6 before enumeration. Projective duplicates
are removed, leaving 865 rays and 5,502 orthogonal pairs at radius six. Each
pair gets three checks: both completion dot products and the exotic frame
sum. Completing rays may lie outside the box. All 64 parity-admitted tuples
modulo four replace repeated integer samples; 32 satisfy the required modular
orthogonality. The old private Gaussian elimination is composed with the
shared inverse verifier: a six-equation basis determines the quadratic
coefficients, the seventh equation contradicts them, and a separate left-null
certificate annihilates all six columns while pairing to -2 with the target.
Explicit witnesses exercise all three exotic values.

The new count is **20,872**, comprising 3×5,502 geometric/frame checks,
5×865 value/scaling checks, 33 congruence/census checks and eight obstruction
checks. The historical 46,328-condition receipt remains unchanged. Independent
tests compare every original 1,854 admitted radius-six vector with a residue
oracle and compare projective pair coverage against raw enumeration in boxes
of radii 1–3. Generated projective coordinates, symbolic cross products and
quadratic polynomials use 80 deterministic examples each. A separate symbolic
rank/nullspace calculation confirms ranks six and seven for the coefficient
and augmented systems.

All five final quality commands pass: strict pinned typing and the 12-group
new suite plus the 24-group regression harness in ordinary and optimized
Python. Application CCN/cognitive/nesting maxima are 6/6/3; test maxima are
12/14/2. Both sources have one class and no production assertions.

The first 41-fault campaign killed 36. One additive test isolates an oversized
dot product hidden by a prior prefix, an oversized cross difference with
fitting products, and nonorthogonal distinct rays whose cross product is not
zero. Final replay kills 39. Two surviving removals of scaling guards are
equivalent within the declared native API: the constructor repeats zero and
product-size checks before normalization, preserving the result or typed
refusal category. Their original raw outcomes, explicit scope/proofs and 120
paired API comparisons remain recorded; the guards remain in production.
No invalid, inconclusive or unrun mutation is omitted. Initial tests,
manifest, quality result and campaign remain preserved.

The complete Lean origin and existing derivation note were read. All current
declarations map to requirements and tests; both original path consumers
remain valid. No external caller of the old internal scalar helpers was
found. Source-checkout replay is recorded separately after guarded copying.
This review does not rebuild Lean, claim hosted CI, promote scientific DAG
status or extend the real rational-ray obstruction to Gaussian rays or the
continuum. Work continues with `fq-gleason-qi3-extension.py`, then the rest of
`checks` before `code`.
