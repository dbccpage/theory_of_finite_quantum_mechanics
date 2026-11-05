# Gaussian tomography file review

AuthorityEffect: None. Retention5 is a keep label, not perfection.

| File | Initial | Final | SCORING.md |
|---|---:|---:|---|
| `checks/independent/fq-gleason-qi3-tomography.py` |4|5|L4B|
| `checks/checker_support/gaussian_vector3.py` |new|5|L4B|
| `checks/checker_support/inert_prime_residual.py` |new|5|L4B|
| `checks/checker_support/orthogonal_gaussian_pair.py` |new|5|L4B|
| `checks/checker_support/equatorial_ray_geometry.py` |new|5|L4B|
| `checks/checker_support/hermitian_tomography.py` |new|5|L4B|
| `checks/tests/test_inert_prime_geometry.py` |new|5|L4B|
| `checks/tests/test_tomography_geometry.py` |new|5|L4B|
| `checks/tests/test_gaussian_tomography_controls.py` |new|5|L4B|
| Nine adjacent companions |new|5|Exact-source contracts and assessments|
| `checks/tests/tomography_obligations.json` |new|5|Original guard correspondence|
| `checks/tests/tomography_mutations.json` |new|5|Executed critical fault recipes|

The original970-line checker passed its literal controls. Its defects were in
input admission, claim scope, architecture and verification: boolean integer
coordinates and floating inputs were accepted; a floating Gaussian norm stayed
inexact; integer-primitivity silently truncated fractional coordinates;
Hermitian inner products silently truncated ragged vectors; nonprime/zero
residual parameters were accepted or leaked division-by-zero; the local guard
accepted truthy non-booleans; arithmetic and caller-supplied valuation work had
no declared budget. Its main had maximumCCN148 and cognitive complexity82.
Some labels described sampled epsilon/rotation controls as general continuity
or invariance claims. The exact original source, all probes and passing report
remain archived. No counterexample to its supplied mathematical fixtures was
found in this review.

The repaired application composes five owned domain components: immutable
Gaussian three-vectors, admitted inert-prime residuals, orthogonal pairs,
equatorial geometry and a fixed symbolic Hermitian tomography model. Shared
Gaussian scalar/failure/case infrastructure is reused. Prime-specific residual
implementations and repeated geometry are composed through the same exact
interfaces. Each production file owns one class; private fixed-fixture workers
stay inside the application, public fallible queries return Outcome and CLI
failures return nonzero. Zero-vector conventions are explicit and nonzero-ray
queries reject zero before division. Primitivity requires Gaussian integers.

Stored rational coordinates/norms have4096-bit bounds. Raw rational arithmetic
can temporarily exceed4096bits by a fixed factor; it is not silently clamped.
Primes are actual primes3mod4 up to65535, with bounded trial division and
valuation loops. Vectors and symbolic dimensions are fixed; arbitrary symbolic
expression trees are not admitted. Each contract states its operation bounds
and failure policy. Unexpected exceptions and cancellation propagate.

All65 original static guards are mapped to replacement symbols, with the315-
check original runtime trace retained. The13 symbolic controls remain; the
composed runtime records979 control calls because conjunctions were separated
and cross-prime/frame checks strengthened. An independent recorder verifies
the reported count. All6original frames,33oscillation pairs,3radicalextension
frames and the original Piron/tangent/Kelvin/sandwich/epsilon/symmetry grids
remain. Alloriginal reportdata fields are unchanged. The nine-ray order is now
consistently interleaved, and kernel coefficients were remapped and separately
checked against operator projectors. The source's old unowned procedural
helpers have no external caller; the existing focused consumer calls main.

Independent tests use SymPy vector/projector/Hermitian calculations,
factorization plus finite-field residue membership, generated exact vectors
and rotations, and explicit malformed/resource/cancellation/ownership cases.
Lean definitions and relevant theorem statements were read to check the
formula and hypothesis correspondence; that source review is not a new Lean
build. In particular, the finite epsilon samples are not a pointwise-to-uniform
continuity proof or a general frame-function classification.

The first99-fault campaign recorded89kills,7survivors and3inconclusive30-second
timeouts. Five strictly additive test methods isolate norm-prefix overflow,
coordinate ordering, a negative leading-unit character, complex quarter-turn
conjugation, zero-ray preflight, the explicit Piron formula and a masked mixture
guard. Small fixed Hermitian examples detect three faults that previously
spent their worker budget shrinking generated failures. Allold AST declarations
and fault/test selectors remain. A full final99-case replay kills every fault;
no timeout is counted as a kill. The test-injection harness mistake from the
first quality run is also preserved separately before its correction.

Strict typing and37new groups plus24earlier integration groups pass normally
and under optimization. MaximumproductionCCN is9, cognitive11, nesting3;
all nine files meet the B structure bounds. Source-checkout postflight records
its own exact-source contract/history checks and focused existing consumer.
CI is wired for Python3.12/3.14; only the interpreter in the local receipts has
been run here. No hostedCI, new Lean build, authority or scientific DAG status
promotion is asserted.

The next unreviewed files are the six earlier fq-gap applications, beginning
with `fq-gap-c500-original-targets.py`; they remain explicitly unscored rather
than being skipped by the previous alphabetical cursor.
