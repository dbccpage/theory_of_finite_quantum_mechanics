# HL Hilbert-completion review

AuthorityEffect: None. Original chat transcribed as UTF-8/LF, not original-message byte custody. Status: ACCEPTED CONSTRUCTIONS UNDER EXPANDED HYPOTHESES; several submitted claims rejected. No full continuum bridge, dynamics theorem or new Lean certificate is established by this review. Function-valued cochains are the primary convention; the density convention is translated explicitly.

## 1. Algebraic closure is useful, but does not contain all finite evolution

Define K0^+ as the fixed field of the involution, and choose an ordering/real embedding. Its real closure is identified with R_alg at that embedding because it is algebraic over Q; adjoining i gives a conjugation-compatible algebraic closure Qbar. The real closure is unique up to unique order-preserving isomorphism over the ordered base. Its extension to an algebraic closure is not a uniquely labeled field embedding. Extending the archimedean embedding supplies a standard absolute-value norm on the chosen Qbar; its metric completion is C. None of these topologies follows from field operations alone.

The finite Hermitian spectral theorem over R(i), R real closed, is correct. Artin-Schreier makes R(i) algebraically closed. An eigenpair Av=lambda v has lambda=(v*Av)/(v*v) in R, and v*v>0. Normalize using square roots in R and induct on the invariant orthogonal complement. Thus algebraic Hermitian matrices have algebraic eigenvalues and an algebraic unitary eigenbasis. Inverses require nonsingularity; a PSD square root stays Hermitian/PSD. K0 was already a field, so inverses alone do not require algebraic closure.

The claim that EVERY finite stage's unitary evolution lies in Qbar is FALSE. A one-dimensional algebraic Hamiltonian H=[1] at t=1 gives exp(-i), transcendental by Hermite-Lindemann. The physically nontrivial qubit version H=diag(0,1) gives relative phase diag(1,exp(-i)), likewise outside Qbar. Finite matrix algebra and algebraic spectral diagonalization do not include the transcendental exponential functional calculus. Special algebraic unitary samples may be declared separately; an exact real-time group needs the additional time/analytic structure already recorded in DT. Finite dimension does not remove this issue.

## 2. Places, coherent roots and the incorrect numerical comparison

Coherent primitive-root choices correspond to embeddings only after fixing reference root labels; they distinguish an embedding from its conjugate. A complex ARCHIMEDEAN PLACE forgets conjugation. On this cyclotomic field it corresponds to an ordering of the totally real fixed field, and its parameter space is a torsor modeled on profinite units modulo +/-1 after choosing a reference embedding. A two-way orientation or choice of i does not determine a place: it leaves infinitely many choices on higher cyclotomic fields. A coherent choice at every conductor is much more than such an orientation.

The two seventh-root quantities are unnormalized squared magnitudes, not probabilities until normalized as part of an experiment. Their order does depend on the place, but the supplied second embedding does NOT reverse it. Put t=zeta+zeta^-1, so A=2+t, B=t^2 and A-B=(2-t)(t+1). At embeddings zeta -> exp(2pi ik/7):

- k=1 gives t in (1,2), hence A>B.
- k=2 gives t in (-1,0), hence A>B again. Here A is about 1.555 and B about 0.198, not a reversal.
- k=3 gives t in (-2,-1), hence A<B. This is a valid reversal.

No decimal approximations are used as proof in the replay. The values t are roots of t^3+t^2-2t-1 and can be isolated by rational intervals (1,3/2), (-1/2,0), (-2,-3/2). A finite collection of algebraic weight comparisons depends on only one finite conductor. Each nonempty finite-comparison fiber therefore still contains infinitely many places of the full cyclotomic union. The full place is a declared infinite coherence datum, not pinned by finitely many observed comparisons.

## 3. Norm and refinement data must be specified

Jordan-von Neumann characterizes norms induced by an inner product via the universal parallelogram law. A two-cell l1 counterexample disproves Hilbert isometry: for the coordinate unit vectors the two sides are 8 and 4. Completion cannot repair that norm. For the specified growth/refinement maps its l1 completions are weighted l1/L1. A single successful finite sample does not certify a universal identity, and arbitrary norm presentations do not have an automatic decision algorithm. A rational Gram matrix gives an effective certificate for its declared quadratic norm; no general all-stages decision procedure follows.

The weighted diagonal Hermitian form is a valid declared choice. Its uniqueness requires an explicit locality/orthogonality assumption on distinct cells, not just the phrase 'respects cell structure'. Even the positive definite swap-invariant matrix [[2,1],[1,2]] gives a different form if disjoint-cell orthogonality is not required. Choosing an inner product from a presumed Born quadratic form would be circular in a route intended to derive that form. Declare the pre-Hilbert structure independently.

For growth, zero extension is isometric when old cell weights are stable. It does NOT automatically commute with coboundaries: grow a single vertex to one edge with a new endpoint; the old value 1 extends to (1,0), whose new-edge difference is -1, while the old zero edge cochain extends to 0. Operator compatibility is an additional condition, not a property of every subcomplex growth system.

For subdivision, specify a countable nested sequence of finite partitions of a fixed total space, surjective parent maps, positive weights of finite fixed total, and FUNCTION pullback f(child)=f(parent). That pullback is isometric iff each parent weight is the sum of its children's weights. Under DENSITY/MASS coordinates a_c=w_c f_c the isometric map is a_child=(w_child/w_parent)a_parent and the norm is sum |a_c|^2/w_c. Constant-copying these density coordinates is generally not isometric. Other renormalized transition maps can be isometric without additive weights; the 'iff' concerns the specified pullback only.

## 4. Correct Stone-measure construction

Under the preceding subdivision hypotheses, the union Boolean algebra is countable. Its Stone space S is compact metrizable and is the inverse limit of the finite partition sets. Compatible finite weights define a finite positive charge on clopens. For a disjoint countable clopen family whose union is clopen, compactness yields a finite subcover, so only finitely many nonempty members occur. This is precisely the premeasure condition on the algebra, not a claim that every open union is clopen. Caratheodory gives the unique finite extension to the sigma algebra generated by clopens; countability makes that the BOREL algebra. These details validate the construction here. For an arbitrary nonmetrizable Stone space the sigma algebra generated by clopens need not be all Borel sets.

Finite-stage functions identify with locally constant functions; their closure is L2(S,mu), modulo null sets. Rational/algebraic coefficients are dense only after the chosen scalar embedding/completion. Countability gives separability. The growth version similarly yields weighted l2 over the cell union. Neither construction makes a profinite space a spatial manifold.

Abstract Hilbert space isomorphism erases more than geometry but retains field and dimension. The classification applies to infinite-dimensional separable spaces over a fixed complete field; a finite atomic measure could instead give finite dimension. To retain geometry record the multiplication representation of the cell/event algebra, embeddings and domains as well as differential operators. A spectrum or Laplacian alone does not generally reconstruct geometry.

## 5. State convergence and normalization

Increasing orthogonal projections P_n converge strongly to I when their ranges have dense union. This is valid for the stated constructions. For common-carrier functions x,y, the submitted inequality is valid even for complex amplitudes:

||x|^2-|y|^2| = |Re(conj(x-y)(x+y))| <= |x-y||x+y|,

then weighted/integral Cauchy-Schwarz yields the bound. For normalized x,y the density measures are probabilities and conventional total variation is HALF their L1 distance, hence <=||x-y||. Coarse-graining cannot increase TV. P_n x need not be normalized: its total squared mass is ||P_n x||^2. Either discuss subprobabilities, add the missing-mass event, or normalize P_n x when nonzero. Normalized projections converge to a unit x once their norms tend to 1. Do not silently compare incomplete mass vectors as probability distributions.

## 6. Operators: bounded extension versus closed-form realization

Compatible uniformly bounded delta_n extend uniquely by continuity to a bounded delta on the completed Hilbert spaces. For a graph differential f(head)-f(tail), with edges counted once and the stated vertex/edge norms, the valid estimate is ||delta||^2<=2 sup_v (sum_(e incident v) w_e)/w_v. General higher-degree cellular differentials require the corresponding incidence estimate. The graph constant is not universal for arbitrary complexes.

The submitted 'otherwise' is false without domain hypotheses. On finitely supported sequences in l2 define T x=sum_(n>=1) n x_n in C. Its finite-stage maps commute with zero extension, but x^(n)=e_n/n tends to zero while Tx^(n)=1. Thus T is NOT closable. The nonnegative form q(x)=|Tx|^2 is not closable either: differences of these x^(n) have q=0 but q(x^(n))=1. The formal T*T is not defined on the entire colimit: its adjoint domain is {0}. This is a countermodel to the broad compatible-finite-linear-map inference, not a claim that every locally finite graph differential behaves this way.

Instead assume/prove delta is densely defined and closable (local graph hypotheses can supply it), then use D=closure(delta) and the closed form q(x)=||Dx||^2 on Dom(D). It yields A=D*D>=0 self-adjoint. Alternatively, first construct a densely defined semibounded symmetric L0 and take its Friedrichs extension. A mere formal expression is insufficient. Boundary/core choices select a realization; Friedrichs is not the only possible self-adjoint boundary condition. In higher cochain degrees delta*delta is one term of a full Hodge Laplacian, which may also contain the adjacent-degree term.

## 7. Convergence: Galerkin forms, domains and the correct topology

A precise sufficient hypothesis is a closed nonnegative form q on H with self-adjoint operator A, nested finite-dimensional V_n subset Dom(q), and union V_n dense in the FORM norm ||x||_q^2=||x||^2+q(x). Define A_n by <u,A_n v>=q(u,v) on V_n. These are FORM/GALERKIN restrictions. They equal operator compressions P_n A|V_n only when V_n subset Dom(A). Form-core membership alone does not imply that inclusion.

For example the triangular hat u(x)=min(x,1-x) on (0,1) is in the Dirichlet Laplacian form domain H0^1 but not its operator domain H^2 intersect H0^1. It has q(u)=1 and ||u||^2=1/12. The one-dimensional Galerkin operator has coefficient 12, while Au is not an L2 function. Thus the literal compression is undefined.

There is a direct variational proof of the desired resolvent limit. For f in H, u=(A+1)^-1 f solves a(u,v)=<f,v> with a=q+<.,.>. Its Galerkin solution u_n solves the same relation for v in V_n, so a(u-u_n,v)=0. Form-core density implies ||u-u_n||_q ->0. Therefore j_n(A_n+1)^-1 P_n -> (A+1)^-1 strongly. To use ordinary same-space strong resolvent language define Atilde_n=A_n direct-sum 0 on V_n^perp; the additional complementary resolvent term tends strongly to zero. The standard self-adjoint unitary-group convergence theorem then gives exp(-it A_n)P_n -> exp(-itA) strongly, uniformly on compact time intervals for each fixed state. It is NOT operator-norm convergence or an error rate. At t=0 the projected expression is P_n, whose operator-norm distance from I is 1 while V_n is proper.

If different stage energies, spaces or boundary conditions are used, prove their actual Mosco/variational or suitable form convergence. Naming Simon 1978 does not verify hypotheses: the paper also treats nondense forms and nonclosable limits. Its precise monotonicity direction and domains must be matched, not asserted from the word 'compression'.

## Declared inputs and status

There are more than two inputs: scalar embedding/order and completion; chosen positive pre-Hilbert norm; specified stable growth or partition/refinement system; compatible weights and transition maps; compatible differential with boundedness or closability/domain proof; chosen closed form/boundary realization; actual Galerkin restrictions and a form-core proof; and real-time spectral calculus for dynamics. Some may be derivable in a concrete model, but they are not discharged by this proposal. Corrected Lemma 7.1 states a sufficient conditional package in separate parts. No original continuum-Hilbert gap is marked closed.
