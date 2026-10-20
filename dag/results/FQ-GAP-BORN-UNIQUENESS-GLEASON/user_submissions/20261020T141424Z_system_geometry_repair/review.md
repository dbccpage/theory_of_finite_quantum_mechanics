# System and Jordan-boundary repair review

The old `System` permitted unrelated state sets, hull predicates, capacity and dimension labels. Its unrestricted global Jordan axiom therefore admitted the one-state rank-one dimension-two phantom and yielded `False`. That diagnostic and every older submission remain sealed as historical evidence. None of those old interfaces or axioms is imported by the replacement.

## Concrete interface

`ReconstructionGeometry.System n` has a nonempty compact convex state set in the real Euclidean space of dimension n and requires its affine span to be the full ambient space. Its homogenized dimension is **defined** as n+1. Purity means an actual extreme point. A frame is an injective ordered family of pure states distinguished by bounded affine effects whose sum is one on every state. Capacity is calibrated by a bound on these frames and an attained frame. This declares the full affine-effect convention; it does not derive an effect-restriction postulate.

Reversibles are actual affine equivalences preserving the state set. Identity, inverse and composition preserve states by proof. Spectrality uses real convex hulls of frames; strong symmetry acts on these actual ordered frames. Composites carry separately affine product preparations, affine state-preserving marginals, and both marginal/product laws. The right marginal is onto by fixing any left state. No rank-product or tomography law is silently built into Composite.

`subsingleton_dim_one` rejects a singleton state set with dimension two using full affine span, before any Jordan premise. More strongly, `rank_one_pure` and `rank_one_dim_one` prove that a spectral capacity-one system has dimension one: spectral decompositions have singleton frames, hence every state is extreme; convexity then forces the state space to be a singleton. These are direct regression theorems against the old phantom.

## Safe Jordan boundary and remaining imports

`JordanStateCatalogue` is an explicit **input contract** for concrete real state-space models associated with the existing arithmetic family tags. It requires dimension/capacity calibration, finite convex generation for classical tags, and an actual affine identification with the real three-ball for qubit tags. `Representation` supplies an actual affine equivalence onto a catalogue model and capacity preservation. Dimension preservation is proved from this equivalence; no independent dimension label is trusted.

`JordanBridge catalogue` is an explicit proof argument, guarded by the repaired spectrality and strong-symmetry hypotheses, returning a representation and the simple/classical dichotomy. There is **no global bridge axiom**, no opaque JordanIso predicate, and no supplied instance of this contract. Numeric family tags still do not construct Jordan multiplication. A concrete catalogue, the classification theorem, tensor compatibility/local tomography, complex selection and process equivalence remain outside this repair. The obsolete unrestricted signature has not been made safe by renaming its hypotheses.

## Classical-exclusion chain independently checked

1. Affine maps commute with real convex hulls (Mathlib), so images of finite polytopes are finite polytopes. Empty vertex sets are allowed in this general transport lemma.
2. A section gives the full marginal image. For Composite, nonemptiness of the left state set and the marginal/product law supply that section.
3. The explicit circle points `((1-t²)/(1+t²), 2t/(1+t²), 0)` have norm one and recover their parameter as y/(1+x). The denominator is nonzero. Natural parameters give infinitely many distinct points of the sphere. The support functional at any unit vector uniquely maximizes there, so these are exposed points; strict convexity also proves they are extreme.
4. Extreme points of a convex hull belong to its generating set (Mathlib). A finite polytope has finitely many extreme points. Consequently the real three-ball is not a finite polytope.
5. An affine marginal onto that ball excludes a finite-polytope composite. The System theorem derives the required image from the composite laws. With explicit catalogue representations, a qubit marginal therefore excludes a classical composite tag. Purity of product states is unnecessary.
6. `no_classical_factor_with_qubit` composes the new geometric exclusion with the **unchanged** arithmetic counting lemma for the simple branch. Its dimension-product law, rank lower bound, representations, dichotomy and nontrivial capacity hypothesis are all explicit premises. Dimension multiplication has not been advertised as a proof of operational local tomography.

These proofs discharge the previous elementary classical-composite exclusion **under the concrete geometric interface**. They do not establish the entire reconstruction or instantiate the remaining imported contracts.

## Operation records and evidence boundary

The collected operations carry exact domains, premises, composition admissibility and theorem links. `ConvexSubstitution.lean` proves unit, affine substitution, associativity, and preservation of finite convex generation under substitution. This is a verified unary fragment; no full many-arity operad or complete process theory is claimed.

The accepted arithmetic file is byte-identical to its sealed predecessor. Final compilation receipts refer to frozen source snapshots, the compiler binary hash, local build inventory, stdout/stderr, exit status, and saved compiled artifact bytes. Resolved dependency hashes and package pins are recorded separately. Earlier failed attempts, including elaborator-generated `sorryAx` in failed output, are retained and are **not** accepted proof receipts. The initial helper also encountered a terminal cp1252 rendering error after saving raw compiler output; later runs explicitly render UTF-8.

This is a local review checkpoint. No provider call, publication, commit, push, PR, or merge is performed.
