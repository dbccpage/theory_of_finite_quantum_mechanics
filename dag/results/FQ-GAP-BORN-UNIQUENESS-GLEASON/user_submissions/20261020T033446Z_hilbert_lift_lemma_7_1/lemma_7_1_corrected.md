# Corrected Lemma 7.1 (conditional Hilbert lift)

Status: written mathematical argument with named imports; NOT KERNEL-CHECKED. No physical continuum, Born uniqueness or generator-selection claim is proved here.

## Data

Fix a conjugation-compatible embedding iota:K0=Q(mu_infinity)->C, or a normalized archimedean place with a choice of its conjugate embedding. If an unnormalized absolute value v is supplied, record v=|iota(.)|^s and use the ordinary complex modulus for Hilbert norms. Let K0^+=Fix(*), with the ordering induced by iota, and let R be its real closure at this ordering.

Take a countable directed system of finite-dimensional K0 spaces V_alpha with positive Hermitian forms h_alpha and coherent isometric transitions. In graded applications give these data in each degree. Put W_alpha=V_alpha tensor_iota C. The norm used below is explicitly ||x||²=iota(h_alpha(x,x)), extended sesquilinearly. Arbitrary alternative norms require their own parallelogram test and need not reproduce h_alpha.

For the operator conclusion, use either:

- (I) compatible stage differentials with j delta_alpha=delta_beta j and a closable induced operator delta on the dense algebraic union; or
- (II) a separately defined densely defined closable global differential delta0 whose domain contains the stage union, which is a core for its closure, and define stage energies as restrictions of ||closure(delta0)x||².

Case (II) is the applicable repair for ordinary graph exhaustion when zero extension fails the forward intertwining identity. Its stage operators need not be internal finite-subgraph Laplacians.

## (a) Scalars and finite algebra

The chosen archimedean completion of K0 is topologically C; after normalization its modulus is standard. The involution extends to conjugation, since it agrees on roots of unity and those generate K0. R identifies with the real algebraic numbers at the chosen ordering, and R(i) is an algebraic closure. Finite positive Hermitian spaces over R(i) admit orthonormal bases and Hermitian spectral diagonalization with real algebraic eigenvalues. These are algebraic operations. Complexification and real-time exponentials are subsequent analytic operations; no claim that every finite-stage exponential is algebraic is made.

Positivity extends to W_alpha: the embedded Gram matrix is semidefinite by continuity and density of iota(K0). A nonzero radical would have a nonzero vector over K0 because the Gram equations have K0 coefficients; that contradicts positivity on V_alpha. Hence the form is positive definite.

## (b) Hilbert criterion and completion

For any compatible family of complex norms, the completion is isometrically Hilbert iff the parallelogram law holds on every stage. Its polarized form, antilinear in the first argument, is

    g(x,y)=1/4 sum_(k=0)^3 i^(-k) ||x+i^k y||².

For the explicitly chosen quadratic norms g=h. Without that agreement, g and a previously declared h need not be equal. The two-cell l1 norm fails the law (8 versus 4).

The directed colimit W has a well-defined positive inner product. Its completion H is unique up to a unitary fixing W. It is separable, and the orthogonal stage projections P_alpha converge strongly to I. To reduce nets to sequences, enumerate the countable directed set and repeatedly choose an upper bound for the previous element and the next enumerated element; the resulting sequence is increasing and cofinal.

## (c) Concrete function models

Growth: stable positive weights and zero extension identify H with l2(X_infinity,w). This claim concerns the normed spaces and does not assert compatibility of internal coboundaries.

Subdivision: finite cell sets with coherent surjective parent maps and additive positive weights define a countable Boolean colimit B. Its Stone space S is the compact metrizable inverse limit of the finite sets. The compatible charge on clopens is a finite premeasure: a disjoint countable clopen union that is clopen reduces to a finite union by compactness. Caratheodory gives the unique finite Borel measure mu. Stage-constant functions are isometrically embedded and dense in L2(S,mu).

S is homeomorphic to Cantor space only if it is nonempty and B is atomless. For this system, atomlessness is equivalent to every stage cell eventually splitting into at least two descendants. Infinitely many splits somewhere in the system do not suffice.

## (d) Born measures and coordinate transport

In either concrete function model define nu_x=|x|² mu (weighted counting measure in growth), of mass ||x||². For a subdivision cell C set b_alpha,C(x)=nu_x(C). For growth use the singleton cell weights at the available coordinates. For a stage vector the coefficient formula is w_C|x_C|². Subdivision marginals sum over child fibers; growth weights restrict to earlier cell sets instead.

For all x,y in the same L2 carrier,

    ||nu_x-nu_y||variation <= ||x-y|| (||x||+||y||).

Indeed pointwise ||x|²-|y|²|<=|x-y|(|x|+|y|); integrate and apply Cauchy--Schwarz. Every cell partition/restriction contracts the variation norm, so this estimate is uniform over stages. Taking y=P_beta x proves uniform convergence of the corresponding weight vectors. For normalized vectors probability TV distance is half the variation norm; projections need not preserve normalization.

Mass coordinates on a stage are a_C=w_C f_C with norm sum |a_C|²/w_C and refinement a_child=(w_child/w_parent)a_parent. Transport all operators by the same isometries. For arbitrary x, integral_C x gives the projected amplitude mass, not the actual Born mass nu_x(C) in general.

## (e) Closed operator and form

In case (I), compatibility defines delta on W. Uniform boundedness sup ||delta_alpha||<infinity gives the unique bounded extension. Otherwise retain the explicit closability hypothesis. Compatibility of stage adjoints is a sufficient condition for closability: for any y in a target stage, its compatible stage adjoint is a fixed vector representing x-><delta x,y> on every later stage and therefore on W. Thus the global adjoint has dense domain.

This does not imply that every graph-growth construction satisfies forward compatibility. For the standard locally finite graph, define the global finitely supported incidence differential first, use the finitely supported divergence domain to prove closability, and use case (II) with boundary-edge energy included. With edges counted once, its boundedness estimate, when finite, is

    ||delta||² <= 2 sup_v (sum_(e incident v) w_e)/w_v.

Let D be the closure in either case. Then A=D*D is nonnegative self-adjoint. The closed form q(x,y)=<Dx,Dy> has domain Dom(D), and W is a form core by the stipulated core property (automatic for the closure of delta on W in case (I)). The spectral theorem supplies e^(-itA). This constructs an analytic group, not a justification that A is the physical Hamiltonian.

## (f) Galerkin convergence: direct proof

Choose a cofinal increasing sequence of stages W_n. Define the finite self-adjoint A_n by <x,A_n y>=q(x,y) on W_n. Under case (I) this is precisely delta_n*delta_n; under case (II) it is the global-energy Galerkin operator and can differ from the internal subgraph expression. Literal operator compression requires W_n subset Dom(A), which is not required for form restrictions.

Let a(x,y)=<x,y>+q(x,y), an inner product on Dom(D). For f in H, u=(A+1)^(-1)f satisfies a(v,u)=<v,f> for every v in Dom(D). The stage solution u_n=(A_n+1)^(-1)P_n f satisfies the same identity for v in W_n. Hence u-u_n is a-orthogonal to W_n and

    ||u-u_n||_a <= inf_(v in W_n) ||u-v||_a -> 0,

by form-core density. This proves projected strong resolvent convergence. For ordinary same-space notation take Atilde_n=A_n on W_n and zero on W_n^perp. Then

    (Atilde_n+1)^(-1)=(A_n+1)^(-1)P_n+(I-P_n),

so its resolvents converge strongly as well. The resolvent identity or continuous functional calculus gives the usual nonreal-resolvent formulation.

For f in C0([0,infinity)), define g(s)=f(1/s-1) on s>0 and g(0)=0. Uniform polynomial approximation on [0,1] applied to the positive contractions (Atilde_n+1)^(-1) yields strong convergence of f(Atilde_n); the complement term f(0)(I-P_n) vanishes strongly. Thus f(A_n)P_n->f(A).

For unitary groups first cut off the spectrum by a continuous compactly supported chi equal to one on a sufficiently large interval. Strong convergence of chi(Atilde_n) controls spectral tails on a fixed vector. On the compact support, t->exp(-it lambda)chi(lambda) is uniformly continuous in the sup norm for t in a fixed compact interval. A finite time mesh and the previous functional-calculus convergence give uniform strong convergence of the cutoff dynamics; the tails are uniformly small. Removing the complementary projection gives

    exp(-itA_n)P_n x -> exp(-itA)x

uniformly on compact time intervals for each fixed x. This is not operator-norm convergence, uniform convergence over unit vectors, or an error rate.

For lambda in Spec(A), choose a continuous compactly supported bump near lambda with f(A)!=0. Projected strong convergence implies f(A_n)!=0 eventually. Thus every neighborhood of lambda meets Spec(A_n) eventually, permitting eigenvalues approaching lambda. The reverse inclusion may fail: the mixed-pair construction in review.md has stage eigenvalue 2 but limiting spectrum {1,3}. If forward and adjoint stage compatibility both hold, finite stages instead reduce A and their eigenvalues are already genuine global eigenvalues.

## Scope retained after the lift

The scalar field, finite-dimensional stage data, norm, transition maps, differential realization and analytic completion are declared/imported structures until derived in a concrete program. Keep the event-algebra/multiplication representation, embeddings, weights and domains alongside D and A. Abstract separable infinite-dimensional Hilbert isomorphism does not identify those structures, a manifold, or a physical time generator.
