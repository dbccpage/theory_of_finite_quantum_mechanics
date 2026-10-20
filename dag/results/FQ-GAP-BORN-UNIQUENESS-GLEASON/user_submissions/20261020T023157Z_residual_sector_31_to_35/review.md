# Residual-sector RS-31 through RS-35: review and corrections

AuthorityEffect: None. Original attachment preserved byte for byte. Status: REVISED WRITTEN RESULTS; no new Lean theorem. RS numbering preserves the submitted 31-35 labels without treating these as answers to the separate pending BR-31 through BR-40 instrument requests.

## Main finding: common signs make all mass maps affine

The proposal correctly distinguishes the cochain d1 omega from a scalar quotient distance and identifies a canonical set of allowed masses. Its central measure-selector characterization needs repair. In this weighted l1 problem all optimal residuals have the same weak sign at each edge. Consequently the finest mass map is an affine injection, its image is already convex, and every coherent residual-faithful mass assignment has a unique deterministic repair representative. A measure on repairs is an optional ensemble representation, generally nonunique, not additional necessary structure.

Let A=omega+im(d0) over R, w_e>0, and Phi=min_(r in A) sum w_e|r_e|. Existence follows from closedness of A and boundedness of a norm sublevel set; rational LP data give a rational optimal value and rational vertices. If r,s are minimizers, (r+s)/2 is feasible, so

Phi <= ||(r+s)/2||_(1,w) <= (||r||+||s||)/2 = Phi.

Each coordinate triangle gap is nonnegative, and all weights are positive, so each gap vanishes. Thus r_e s_e>=0 for every edge and every pair of minimizers. Choose sigma_e in {+1,-1} agreeing with any nonzero minimizer coordinate; choose either sign on an identically zero coordinate. Then |r_e|=sigma_e r_e for all minimizers. It follows that

M = {r in A: sigma_e r_e>=0 for all e, sum w_e sigma_e r_e=Phi},

and, for Phi>0,

L(r)_e=w_e sigma_e r_e/Phi,
r_e=Phi sigma_e L(r)_e/w_e.

The diagonal map is invertible and rational. Therefore P_edges=L(M) is a rational polytope affinely isomorphic to M. Every sector map is the linear coarse-graining of this polytope. This proof is general written mathematics; replayed fixtures below only check its explicit examples.

## Carrier correction before optimization

The submission sets C^i=Q^(cells), but invokes real intervals, continuous polytope measures and real entropy maximizers. Separate M_R, the real rational-data polytope, from M_Q=M_R intersect Q^E. The rational and real optima agree by rational LP theory, and their optimal values are rational. Sector endpoint extrema occur at rational vertices. The masses of rational repairs form the rational points of P_R: linear fibers with rational data have rational solutions, or use the explicit inverse at the finest level. Thus a sector interval means [a,b] intersect Q in the rational-only program. Arbitrary real mixing or real measures are declared scalar extensions; finite rational mixtures stay within Q. Empty edges imply Phi=0, so no normalized edge probability exists in that case.

## RS-31: invariant cochain, scalar norm and regime

d1(omega-d0 alpha)=d1 omega is correct. Normalized face masses depend on the cochain, declared positive face weights and declared partition, not on the bare fact that d1 is a map. A zero face norm has no normalized face masses. Distinguish the cochain Gamma_vec=d1 omega from Gamma_norm=||d1 omega||_(1,wF); the live Python campaign uses the scalar convention, so no API renaming or silent identification is made here.

M(omega+d0 beta)=M(omega), M(c omega)=c M(omega) for c>0, and the normalized sector set is invariant under these changes. Phi=0 iff omega is exact; by d1d0=0 exact implies closed. This justifies the stated trichotomy in this finite positive-weight model. The full quotient class and weights determine M, whereas the two scalar diagnostics (Phi,Gamma_norm) generally do not. Do not alternate these meanings of 'the residual'. A selected closest closed representative is another declared optimization/choice. Its normalized masses can be undefined if that representative has Phi=0. Class-preserving moves are sufficient invariances, not the only permitted moves: scaling already supplies another.

## RS-32: exact LPs, convexity and structural cases

The polytope claim and point criterion hold with the carrier qualification above. A projected optimal LP face is bounded because ||r||=Phi; potentials alpha can remain unbounded by gauge freedom without making the residual polytope unbounded. Positive weights force s=|r| on the joint feasible face

r in omega+im(d0), s>=r, s>=-r, sum w_e s_e<=Phi.

Every feasible point has Phi<=sum w|r|<=sum ws<=Phi. Thus BOTH sector extrema are ordinary linear programs on this one face, minimizing/maximizing sum_(e in S) w_e s_e, divided by Phi. No sign-pattern enumeration is necessary. Sector maps are affine on M by the sign lemma, so P_S is itself a polytope, not merely a nonconvex set whose convex hull must be added.

Component-separated sectors are a sufficient case of constant sector masses, not the only structural case. In a connected triangle with a pendant bridge, every minimizer makes the bridge residual zero: varying the leaf potential changes only that edge and otherwise strictly lowers cost. With unit circulation on the triangle the triangle sector has mass 1, the bridge sector mass 0, even though neither sector is a union of whole connected components and M is non-singleton. This is an exact counterexample to the exclusivity claim.

The consistently oriented n-cycle example, no faces, unit weights and omega=e1, correctly gives M_R=the simplex and its rational points for M_Q. Two nonempty sectors range over [0,1]. It is an example, not a proven minimality theorem over unspecified graph categories. A unique least-weight edge gives a unique repair ON THIS CYCLE. More generally, nonuniqueness does not require equal individual weights: parallel edges with omega=(0,0,1), weights=(1,2,3), have every common potential t in [0,1] optimal with cost 3. All three weights are distinct. The coarse-grained interval inclusion in the proposal is correct and can be strict; marginal intervals do not capture all joint constraints.

## RS-33: coherence chooses a mass point, not a unique measure

Normalization and coarse-graining over all partitions yield a single edge distribution mu, provided the assignments also respect block labels/partition reindexing. Residual-faithfulness at the finest partition means mu in P_edges, since this set is already convex. The affine inverse above yields a UNIQUE r* in M with L(r*)=mu. It is rational iff mu is rational. Residual-faithfulness for other partitions follows by the linear pushforward. Therefore one deterministic repair suffices for all admitted partitions; the choice itself remains undetermined unless the admissible mass set is a point.

For a Borel probability measure nu on M_R, define rbar=int r dnu. Compact convexity gives rbar in M_R, and affinity gives int L(r)dnu=L(rbar). A finite rational ensemble gives the same statement without measures or real scalar extension. Distinct ensembles usually have identical outputs: on the four-parallel-edge example, delta_(r(1/2)) and (delta_(r(0))+delta_(r(1)))/2 have identical masses at every partition, but are different measures. In particular coarse-graining does not recover nu, and a fixed coarse partition with constant masses does not force nu. If M itself is a singleton then its probability measure is indeed forced. The Caratheodory representation bound is valid but unnecessary: a single atom suffices for this model after replacing the ensemble by its barycenter.

The analogous distinction in quantum theory is a state versus a nonunique ensemble decomposition, not a theorem identifying a state with a unique measure over preparations.

## RS-34: what the selector example proves

For the four parallel edges the written values are correct: Phi=3, t in [0,1], vertex-mean t=1/2 gives sector masses (1/3,2/3); squared-norm minimizer t=3/4 gives (1/2,1/2); edge-entropy maximizer t=2/3 gives (4/9,5/9). The entropy stationarity equation t^2=(1-t)(2-t) is correct. These rules can be defined globally equivariantly under relabeling and orientation changes: average all residual vertices, minimize the invariant positive quadratic cost, or maximize permutation-invariant entropy of edge masses. Thus naturality ALONE does not select one rule. Merely checking one automorphism of one example would be weaker than this global argument.

The stronger title 'no residual-intrinsic principle selects nu' is false as an unrestricted impossibility claim: vertex mean is already an intrinsic function of the entire rational polytope M. The point is that the stated axioms do not require that rule. A positive rational secondary quadratic cost has a unique rational minimizer, by the active-face rational linear equations and strict convexity. Natural cost data suffice for equivariance; the proposed 'iff' is too strong because different costs can induce the same minimizer (e.g. common positive rescaling). Specify which vertex mean or relative-volume centroid is chosen; do not identify a measure with its mean. If a finite symmetry group acts transitively on the vertices, every invariant POINT equals their mean, but invariant MEASURES need not agree (uniform vertices versus a Dirac mass at their mean).

Entropy can leave Q; that does not make every exact replay impossible. For six unit-weight parallel edges omega=(0,0,0,1,2,3), Phi=6 and t in [0,1]. The maximizing t solves

2t^3-6t^2+11t-6=0.

The polynomial has derivative 6(t-1)^2+5>0 and changes sign between 4/5 and 5/6. Its only possible rational roots in (0,1), by the rational-root theorem, are 1/2 (not a root); hence its maximizer is irrational. Nevertheless the polynomial plus a rational isolating interval specifies an exact real-algebraic number, usable by a declared algebraic-number replay engine. It is outside a rational-only engine. No logarithm was numerically evaluated or an entropy solver claimed here; strict concavity and the written derivative prove the example.

## RS-35: diagonal representation and its precise fiber

For a real distribution mu with nonempty E, diag(mu) is a complex density matrix; if mu is rational it is in Herm(Q(i)). The diagonal sector projections commute, sum to I over a partition, and Tr(diag(mu)Q_S)=sum_(e in S)mu_e. For all partitions, any other density matrix reproduces these probabilities iff its diagonal is mu. Its off-diagonal entries are NOT arbitrary: Hermiticity and full PSD still apply; |rho_ij|^2<=mu_i mu_j is necessary, and all principal constraints are needed in higher dimensions. Zero diagonal entries force the corresponding rows/columns to vanish. For example mu=(1/2,1/2) admits off-diagonal 0 or 1/2, but not 1. The latter matrix has determinant -3/4 and a negative quadratic form on (1,-1).

If mu has only one nonzero coordinate, PSD forces the unique diagonal pure state; otherwise different admissible off-diagonal completions exist. The diagonal probabilities do not select a nonzero coherence. Choosing zero off-diagonals is a valid declared classical embedding, not a derivation of general quantum dynamics. For rational-carrier claims require the selected mu entries in K; a genuinely irrational entropy distribution need not define a matrix over Q(i).

The proposed reason 'every quantity in 31-34 is a function of |r|' is also too broad: those sections use d1 omega, the affine repair set and signed residual witnesses. The non-identifiability conclusion follows precisely because all stated sector OBSERVATIONS factor through the diagonal. It does not follow from discarding every signed or cochain datum in the construction.

## Scope of saved verification

The local exact replay uses the existing public L1Seminorm certificate verifier with rational primal/dual certificates for the cycle, four-edge selector example, distinct-weight degeneracy and triangle-plus-bridge countermodel. Additional Fraction checks cover affine mass mixing, selector values, the irrational algebraic entropy example and PSD counterexamples. Normal and optimized Python runs and rejected mutations are recorded separately. These are bounded fixtures, not an LP solver, no general Lean certificate, and no closure of the original residual-to-Hilbert gap. Rust/Python/Lean live implementations and frozen gap rows are unchanged.
