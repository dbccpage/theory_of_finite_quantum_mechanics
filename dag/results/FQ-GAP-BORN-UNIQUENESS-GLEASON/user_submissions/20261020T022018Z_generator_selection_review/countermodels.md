# Exact symbolic witnesses and conditional lemmas

All statements below have written-review status; no new kernel or numerical exponential certificate is claimed. Fix tau>0 and a nonzero complex Hilbert space.

## Coherent dyadic roots with no continuous interpolation

For n>=0 put a_n=sum_(0<=2j<n) 2^(2j), and z_n=exp(2pi i a_n/2^n). Then a_0=0, z_0=1 and a_(n+1)-a_n is either 0 or 2^n. Hence z_(n+1)^2=z_n. Define V(k tau/2^n)=z_n^k; compatibility makes this a well-defined unitary scalar homomorphism on tau Z[1/2].

For n=2m, m>=1, a_(2m)=(4^m-1)/3, so a_(2m)/2^(2m)=(1-4^(-m))/3 lies in [1/4,1/3). Thus |z_(2m)-1|>=sqrt(2), even while tau/2^(2m)->0. The dyadic representation has no strongly continuous extension to R. Algebraic root consistency alone is insufficient.

## Correct extension principle

Let V:tau Z[1/2]->U(H) be a homomorphism that is strongly continuous at zero in the inherited real-time topology. For t in R choose dyadic q_n->t. For any xi,

||V(q_n)xi-V(q_m)xi||=||(V(q_n-q_m)-I)xi|| ->0.

Hilbert completeness gives an isometric strong limit U(t), independent of the approximants. The limits along -q_n also exist; strong multiplication on uniformly bounded unitary sequences gives mutually inverse limits. Therefore U(t) is unitary. The same approximation gives the group law and strong continuity. Density forces uniqueness. Stone supplies the unique self-adjoint generator. This uses Hilbert completeness and the stated continuity assumption, not root consistency alone.

## Degenerate sample, uncountably many groups

For any rank-one P on C^2, exp(-i tau (2pi/tau)P)=I+(exp(-2pi i)-1)P=I. The family P_x=(1+x^2)^(-1)[[1,x],[x,x^2]], x real, is injectively parameterized by x (read off the off-diagonal/upper-diagonal ratio). H_P=2pi P/tau therefore gives uncountably many logarithms of I_2. They have the same two energies 0,2pi/tau but different energy eigenspaces. A scalar-valued integer function of H_0=0 cannot describe these nonscalar logs.

## Finite-depth aliases and restrictions that do not suffice

For a grid through depth N, H'=H+(2pi 2^N/tau)I agrees with H at every k tau/2^N. Both yield strongly continuous groups. On a finite lattice, H=0 and H'=(2pi/tau)P_j for a one-site projection are both strictly local, bounded below by zero, and have the same sample I. Symmetry alone cannot remove arbitrary integer-period identity shifts. A selection rule must actually have a proved uniqueness property for its specified admissible class.

## Two incommensurate times

Suppose two strongly continuous groups agree at tau and sigma, with tau/sigma irrational. They agree on all k tau+l sigma by the group law. This subgroup is dense in R, so continuity makes the groups identical and Stone makes their generators identical. Existence is separate: in dimension one, samples U(1)=1 and U(sqrt(2))=-1 cannot both come from exp(-ith), since h=2pi k and 2k sqrt(2) would have to be odd. This uniqueness result assumes exact real timing and exact operator samples.

## Markov obstruction and nonuniqueness

Use column-stochastic convention: rate matrices have nonnegative off-diagonals and zero column sums. The flip S=[[0,1],[1,0]] is stochastic but cannot equal exp(tau Q) for real Q, since det S=-1 while det exp(tau Q)=exp(tau Tr Q)>0. The same flip is complex-unitarily embeddable using H=(pi/tau)(I-S)/2.

For nonunique Markov embedding take a cyclic 3x3 permutation C, s=2pi/(sqrt(3)tau), Q_+=s(C-I), Q_-=s(C^2-I). They are distinct rate matrices. On the constant subspace both have eigenvalue zero; on its complement their tau-scaled eigenvalues are -sqrt(3)pi +/- i pi, exchanged between them. Thus their exponentials coincide:

P=(1+r)J/3-rI, r=exp(-sqrt(3)pi),

where J is the all-ones matrix. Here 0<r<1/2, so P has positive diagonal (1-2r)/3, positive off-diagonal (1+r)/3 and column sums one. This is an analytic real-rate example; it is not a claim that all rates or probabilities lie in Q(i).

## Logarithm branches in finite dimension

If U=sum_lambda exp(-i theta_lambda) P_lambda, then self-adjoint H with exp(-i tau H)=U commute with U and decompose each P_lambda into spectral subprojections P_lambda,k at energies (theta_lambda+2pi k)/tau. Conversely every such decomposition gives a log. A fixed half-open energy band of one period permits one value per phase, making H a unique function of U. Without that restriction, degenerate phase eigenspaces permit additional continuous projector choices. Infinite-dimensional endpoint spectral support needs the additional qualification recorded in review.md.
