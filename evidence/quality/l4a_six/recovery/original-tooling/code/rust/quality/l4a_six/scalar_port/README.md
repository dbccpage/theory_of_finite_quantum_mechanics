# Staged scalar and matrix migration

AuthorityEffect: None. This snapshot was activated by
`20261020T104119Z-scalar-activation`. The live scalar source subsequently regained
nine original contract tests after the integrated replay exposed omitted test
coverage. The source snapshot here remains unchanged for historical receipts.
Fresh integrated assessment is required; activation alone awards no L4A grade.
The staged-development account below retains its original scope and chronology.

The candidate owns a fallible scalar protocol. Native i64 operations use checked
intrinsics; i64 is neither Field nor ExactRing. Rational64 operations widen raw
storage before arithmetic and narrow only a canonical representable result.
Canonical Q admission protects zero queries, arithmetic, inverses and involution.
Public Gaussian components remain immutable and checked at construction/decoding.
External field implementations remain possible; algebraic laws and trustworthy
custom implementations are hypotheses, not conclusions of finite law sampling.

The basic-matrix candidate privately wraps provider storage. Its arithmetic uses
the owned protocol and returns typed scalar errors. There is no Deref or public
provider-storage escape. Raw constructors and decoding are shape-checked
transport; they do not admit a coefficient domain. Arithmetic validates all
inputs, including operands skipped by an empty output. Default arithmetic limits
are 4096 output slots and one million multiply/accumulate calls. Explicit limits
are inclusive. These do not bound bytes, scalar bit growth, validation cost,
process memory or elapsed time. Generic transport into nalgebra stays separate
from exact scalar arithmetic.

The caller migration includes local involution and ordered-field interfaces,
typed error propagation, fallible callback construction, checked row operations,
and full input admission in several matrix predicates and fast paths. Generic
finite fields, Q(i), and Q(sqrt(2)) remain exercised. The external chain-complex
view retains its existing separate admitted Q copies; local matrix storage is
not exposed through that bridge. Provider code was read and pinned, not edited.

`20261020T084429Z-scalar-port-check` passes 403 unit cases, three rank allocation
cases, three new scalar/matrix allocation cases, and twelve doctests. Its source
and dependency checks passed. The new observer detects the real Q output layout
as a positive control and checks both matrix operand roles, vector coefficients,
and budget refusal ordering. This is a current-thread allocation-layout
observation, not a universal allocation bound.

`20261020T084710Z-scalar-port-faults` challenges 27 specific faults against those
exact bytes: 27 killed, no other outcomes, and a passing restored baseline.

The next revision (`20261020T085404Z-scalar-port-check`) passes 404 unit cases,
six allocation cases and twelve doctests. Empty polynomial/outer-product and
tensor-transport inputs are now admitted. Polynomial evaluation starts with its
leading diagonal term, avoiding the old multiplication of the zero accumulator.
A distinct counting scalar checks arithmetic calls against the conservative
work allowance. Validation and zero-query costs are outside that arithmetic
counter. Prototype metrics for the 37 production basic-matrix functions now
have maximum CCN 10, cognitive bound 4 and nesting 2.

The `20261020T085556Z-scalar-port-faults` replay records 32 kills and one survivor,
with no invalid, equivalent, inconclusive or unrun cases and a passing restored
baseline. The survivor inserts one additional polynomial product. That work fits
the conservative allowance on the challenge fixtures; the zero-skipping multiply
also makes the old zero-accumulator product cheaper than a dense cubic estimate.
This outcome remains a survivor, not a retroactive kill or equivalence. The
separate CP24 challenge repeats extra work beyond the allowance; consult its own
receipt rather than adding it to or rewriting the preceding campaign.

Obligations recorded during staged development:

- Refresh targeted faults after any candidate edits. Keep preceding outcomes
  attached to their original bytes.
- Audit API changes and consumer composition. The fallible scalar protocol,
  ordered queries, numeric matrix errors and narrowed convenience surface require
  caller migration; no external consumer compatibility is asserted.
- Complete the broader QM boundary migration. For example, report_fiber imports
  the provider row-reduction trait, Weyl consumers exchange provider matrix types,
  engine_bridge accepts provider density inputs, and GaussianRat/Cyclotomic
  implement the provider scalar traits. The new protocol needs typed, validated
  adapters at those actual boundaries. F5 extensibility tests alone do not
  establish compatibility with those existing callers.
- Check root-module composition using the repository's pinned lockfile and host
  resolution. Initial isolated-manifest attempts selected uncached versions or
  unused web-target dependencies; their failed metadata receipts remain intact.
- Seal the preceding live source/sidecars before activation, then obtain fresh
  integrated metrics, challenges and package baselines before grading.

`base_sources.json`, `homology_origins.json` and the separate provider-origin
record retain origins. Execution receipts retain complete staged source copies.
The candidate files are newer than the earlier standalone scalar prototypes;
copying those prototypes over this directory would discard the caller migration.
