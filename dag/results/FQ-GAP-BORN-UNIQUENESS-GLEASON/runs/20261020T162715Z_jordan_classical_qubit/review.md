# Mathematical review and construction boundaries

The new work constructs actual state Systems under the already declared real-field interface. It does not replace an unknown geometry by rank/dimension labels.

## Classical family

`ClassicalModel.system n` is the convex hull of an affine basis of n+1 points in real Euclidean dimension n. The affine basis is fixed by `Classical.choice` applied to Mathlib's proved finite-dimensional basis-existence theorem. This is an explicit noncomputable coordinate choice, not a physical postulate, a canonical rational coordinate formula, or an executable enumeration guarantee. The state chart maps onto the entire standard probability simplex, and the coordinate reconstruction theorem supplies its inverse on normalized coordinates.

The coordinate effects are nonnegative, bounded by one, normalized and distinguish the vertices. Each vertex is extreme because its coordinate functional has a unique maximum. Every extreme point of a finite convex hull belongs to its generating set; therefore an injective pure frame has at most n+1 elements. The displayed vertex frame attains that bound. Rank and homogenized dimension n+1 are thus calibrated by actual geometry. n=0 means one outcome, not an empty state space. Spectrality is proved using the full vertex frame.

## Qubit/spin state model

`QubitModel.system` is the actual unit ball in real Euclidean dimension three. Its pure points are exactly the sphere. Unit antipodal pairs are pure frames, distinguished by the explicit effects (1+inner(u,x))/2 and (1-inner(u,x))/2. For an arbitrary normalized affine measurement, reflection gives e(-x)+e(x)=2e(0). An effect attaining one therefore has e(0)>=1/2. Summing over outcomes proves every distinguishable frame has at most two elements. This capacity proof does not presuppose a rank label, Jordan representation or purity theorem.

The ball is nonempty, compact, convex and full in its ambient space. The attained antipodal frame gives rank two, and the interface fixes homogenized dimension four. Spectral decomposition treats the centre separately and normalizes by the norm only when the vector is nonzero. Its diameter coefficients (1+norm(x))/2 and (1-norm(x))/2 are admissible even at the sphere boundary.

## Explicit real algebra and state cones

`ConcreteJordanProducts` gives coordinatewise multiplication on real finite tuples and the spin product (a,x) circle (b,y)=(ab+inner(x,y), a*y+b*x). Commutativity, unit, left additivity/scalar compatibility and the Jordan identity are proved; right bilinearity follows by commutativity. Spin multiplication is always the named operation `spinMul`. The raw pair type is not endowed here with a new global multiplication instance, so ordinary inherited `*` must not be advertised as this product.

Both positive cones are proved equal to their Jordan-square cones. The spin proof separates a zero vector, then uses real square roots of t+norm(v) and t-norm(v). No positivity or uniqueness theorem about the square-root witness itself is claimed. Classical states in barycentric coordinates are trace-one squares; spin states of trace one are exactly (1/2,x/2) with norm(x)<=1. These links are checked again in `CatalogueApplications`. No complex Hermitian-matrix map or Pauli/PSD equivalence is proved here.

## Supported catalogue and genuine gaps

`SupportedJordanCatalogue.Entry J` contains an actual System and proofs of the reviewed rank, dimension, classical-polytope and qubit-chart contract. `classicalEntry` works for every arithmetic tag list satisfying IsClassical; `qubitEntry` works for the two singleton qubit spellings. Predicate-specific impossible clauses are discharged using the proved rank-one versus rank-two mismatch. No unsupported family receives a default model.

`entry J supported` constructs an entry on exactly the supported subset. The complexHerm2 arithmetic tag is assigned the constructed ball state model; this is **not** a proof identifying the algebra of 2x2 complex Hermitian matrices with the spin algebra. Such an identification remains required for a matrix-algebra interpretation of that tag.

`completeCatalogue remaining` is a proved assembly operation **requiring** an entry for every unsupported tag. No `remaining` value, complete JordanStateCatalogue, or JordanBridge instance is supplied. The new models' spectrality is proved; their full ordered-frame strong symmetry is not yet formalized. Bundled Euclidean Jordan typeclass instances, trace-inner-product associativity, the complex matrix identification, other matrix/spin/exceptional families, nonclassical direct sums, tensor compatibility, classification and full process equivalence remain separate work.

## Evidence and operation ceiling

Original arithmetic and interface sources are copied byte-for-byte. Existing sealed bundles are preserved. Each compile attempt reads a frozen source snapshot, captures exact output and dependencies, and saves its binary artifact only on success. Failed attempts and passing-but-superseded snapshots are retained. Only the accepted-module map certifies final sources; generated `sorryAx` in failed elaboration output is never accepted.

Stage ledgers were collected after the corresponding successful checks. Final operation records include exact exported types and the conditional extension argument. The products have a Jordan relation, not general associativity. These are scoped typed operations and relations; no complete many-arity operad or global reconstruction theorem is asserted.

The real field, Euclidean topology, full affine-effect convention and pinned Mathlib cache remain declared foundations. Finite data have not been used to derive completion or select complex scalars. No provider inference or Git publication is performed in this review-stop run.
