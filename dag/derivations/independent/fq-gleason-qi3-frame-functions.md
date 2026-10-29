Status: AI-drafted, awaiting human review.

# FQ-GLEASON-QI3-FRAME-FUNCTIONS: two obstructions and the remaining rigidity problem

AuthorityEffect: None.

Baseline: `83667d6f0bd3a52898b915a0e68dcbadf443b6c1`. The original target remains
`OPEN`. Its signed and nonnegative quadratic-rigidity questions are not settled
by the results below. The binary-valued and specified-extension questions have
finite obstruction certificates.

## 1. Carrier and scope

Let (K=\mathbb Q(i)), with inner product
\(\langle u,v\rangle=\sum_j\overline{u_j}v_j\). A frame consists of three
nonzero pairwise orthogonal vectors. A frame function takes rational values and
sums to one on every frame. Positivity, continuity and dependence on residue
classes are not part of this definition.

The Lean carrier is `BornFinite.GaussianFrames.GVec`; `IsFrame` and
`IsFrameFunction` express exactly these conditions. A total function on `GVec`
has an unconstrained value at zero, which plays no role. This is equivalent to
the target's function on nonzero vectors. Existing `frameFunction_smul` in
`BornGaussianFrameRays.lean` proves constancy on nonzero scalar multiples.
Neither obstruction below needs to assume that property separately.

| Question in the original target | Result of this work | Evidence |
|---|---|---|
| Must every signed rational frame function be quadratic? | Unresolved; reduced to a zero-weight residual problem | [Reduction note](fq-gleason-qi3-rigidity-reduction.md), prose only |
| Must every nonnegative rational frame function be quadratic? | Unresolved; equivalent to vanishing of bounded residuals | Same reduction note, prose only |
| Does a \(\{0,1\}\)-valued frame function exist? | No | `NoColouring.no_zero_one_frame_function` |
| Does the repository's specified exotic \(\mathbb Q^3\) function extend? | No, even allowing signed values | `GaussianExtension.no_exotic_extension` |

Lean names in the table have prefix `BornFinite.GaussianFrames` for
`NoColouring`, and prefix `BornFinite` for `GaussianExtension`. The
[replay receipt](../../research/campaign_fq-gleason-qi3-frame-functions_lean_replay.json)
records the actual build and axiom audit; a table entry alone is not a replay.

## 2. Binary values are impossible

Take all primitive integer triples in \([-2,2]^3\), selecting the representative
whose first nonzero coordinate is positive. There are 49 such rays, 138
orthogonal pairs and 26 orthogonal triples entirely inside this set. The
[independent checker](../../../checks/independent/fq-gleason-qi3-frame-functions.py)
enumerates these sets using integer gcd and dot products.

Write \(c_j=f(v_j)\). Every internal triple imposes
\(c_a+c_b+c_c=1\). Every orthogonal pair also imposes
\(c_a+c_b\leq1\): the nonzero integer cross product
\(w=v_a\times v_b\) completes the pair to a frame, and \(f(w)\geq0\)
follows from the binary-value hypothesis. The completing vector need not be
inside the box. Omitting these additional pair constraints is an error:
the internal-triples-only system has a binary solution.

The resulting finite binary system is inconsistent. The checker proves this
by exhaustive branching with unit propagation. A value one forces all
orthogonal neighbours to zero; a triple with two zero values forces its last
value to one; a triple already containing one forces its other values to zero.
Conflicting assignments close a branch. Otherwise the algorithm branches on
both values of an unassigned variable, so each branch strictly decreases the
number of unassigned variables and all assignments are covered. It also
independently verifies satisfying assignments for the triples-only and
pairs-only negative controls and compares small instances with direct
exhaustive enumeration.

`BornGaussianRationalNoColouring.lean` checks the concrete nonzero vectors and
orthogonality equations, derives the pair inequalities from actual frame
equations, and replays a finite binary case split using rational linear
arithmetic. Its theorem quantifies over every frame function on (K^3).
All vectors used are real, so the same finite argument also rules out a binary
frame function on all rational real rays. This does not contradict results
about the smaller rational unit sphere: a rational ray need not have a rational
unit representative.

## 3. The specified real exotic has no signed extension

For a primitive real integer vector, the existing exotic is
\(E(v)=(1+s(v))/3\). If precisely two coordinates are odd, \(s(v)=-1\)
when those two are congruent modulo four and \(s(v)=1\) otherwise.
In every other parity pattern, \(s(v)=0\). This is the function defined in
`BornRationalRayObstruction.lean`, not an arbitrary nonquadratic real frame
function.

Suppose an extension (f) existed and set \(g(v)=3f(v)-1\). Every frame
then has \(g(u)+g(v)+g(w)=0\), and every real prescribed ray has
\(g(v)=s(v)\). The
[certificate](../../../checks/independent/data/fq_gleason_qi3_extension.json)
lists 277 nonzero Gaussian-integer vectors, 210 orthogonal frames, and 19 real
prescribed values, together with integer coefficients.

For each frame row (t=(a,b,c)), let its coefficient be \(\lambda_t\);
for each prescribed real ray (j), let its coefficient be \(\mu_j\).
The certificate has the exact identities

\[
 \sum_{t:\,k\in t}\lambda_t+\mu_k=0\quad\text{for every listed vector }k,
 \qquad \sum_j\mu_j s(v_j)=32,
\]

where \(\mu_k=0\) outside the prescribed real rows. Taking this linear
combination of the frame and value equations gives \(0=32\), a contradiction.
All cancellation uses the actual listed vectors; no identification of distinct
vectors or symmetry assumption about (f) is needed.

The [independent checker](../../../checks/independent/fq-gleason-qi3-extension.py)
recomputes Hermitian orthogonality, nonzero-ness, the real parity values, and
every coefficient sum using integers. It uses no search solver or repository
imports. The Lean theorem `no_prescribed_frame_function` checks those actual
frame equations and combines them with the prescribed values.
`no_exotic_extension` derives the required real values directly from the
repository's `exotic` definition. No nonnegativity hypothesis occurs, so the
conclusion excludes both signed and nonnegative extensions of this example.

This certificate was discovered using permutation and conjugation orbits,
then expanded and reduced to equations on individual vectors. Discovery
symmetries are absent from the final proof. A finite consistent system, such
as the earlier smaller-box probe, never implied that an extension existed.

## 4. The remaining question

The [supplemental derivation](fq-gleason-qi3-rigidity-reduction.md) constructs
the unique Hermitian trace-one candidate from the values on
\(e_j\), \(e_j+e_k\), and \(e_j+i e_k\). Subtracting its quadratic
frame function leaves a zero-weight frame function vanishing on those nine
rays. Signed rigidity asks whether every such residual vanishes everywhere;
nonnegative rigidity asks the same for bounded residuals. The supplement
proves these equivalences in prose and checks its algebra symbolically.
It does not prove either vanishing assertion in Lean or in prose.

## What is proved

- The exact finite binary obstruction excludes \(\{0,1\}\)-valued frame
  functions on all (K^3) rays, and the same real witness applies to
  \(\mathbb Q^3\).
- The exact linear certificate excludes any signed extension of the specified
  real exotic to (K^3).
- The supplemental prose gives precise signed and bounded residual reductions.

## What is assumed

The supplied Gaussian-rational vector space, its standard Hermitian form,
and frame normalization are the setting. Binary values are assumed only for
the binary obstruction. Agreement with the specified exotic is assumed only
for the extension obstruction. Neither proof assumes continuity or a residue
class ansatz. These results do not derive the carrier from earlier DAG nodes.

## What is open

- General signed quadratic rigidity or a signed nonquadratic counterexample
  on (K^3).
- General nonnegative quadratic rigidity or a nonnegative nonquadratic
  counterexample on (K^3).
- Formalization of the supplemental residual-reduction equivalences.

Consequently the full target and its incoming gap route retain their original
statuses. No result here establishes continuum Gleason or the whole Born-rule
derivation.
