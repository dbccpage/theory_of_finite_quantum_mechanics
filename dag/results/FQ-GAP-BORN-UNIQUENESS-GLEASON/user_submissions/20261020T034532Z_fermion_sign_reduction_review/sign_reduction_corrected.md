# Model-preserving sign reduction: corrected conditional note

Status: WRITTEN_ARGUMENTS_AND_FINITE_CONTROLS; external theorems cited separately. Not kernel checked. No new interacting-family reduction. Spec item 10: OPEN. AuthorityEffect: None.

## FS1. Exact representation and preservation

Let H=H* act on the finite Fock space of N modes and let beta be real and nonnegative. Then Z=Tr exp(-beta H)>0. Declare observables O and their inserted numerators N_O=Tr(O exp(-beta H)). A representation consists of a measure space, absolutely integrable complex weight w, and integrable inserted functions n_O with integrals Z and N_O. For finite configurations these are arrays. Where n_O=w f_O, f_O is an ordinary estimator. At a zero-weight point with nonzero n_O such an estimator cannot exist. The primitive representation should therefore retain numerators, not discard them during blocking.

A model-preserving change must exhibit a known positive factor c with Z'=cZ and N'_O=cN_O for all declared O. Its construction, evaluation and numerical precision costs are separate obligations. A closed expression is not automatically a polynomial-time algorithm. No cutoff, Trotter error, constraint or omitted sector may silently enter the identities. If the target is a discretized action, say so; exactness for that action does not prove exactness for the original H.

## FS2. Phase taxonomy and a zero-rate counterexample

Suppose W=integral |w| is finite. On the support of |w| put q=|w|/W and s=w/|w|. Then d=E_q s=Z/W is real, 0<d<=1, and E_q(s f_O)/d=N_O/Z whenever the estimator exists. Since |s|=1, equality d=1 implies s=1 q-almost surely: E_q Re(s)=1 and Re(s)<=1. Thus d=1 is equivalent to nonnegative weights almost everywhere, including arbitrary values of s on the ignored zero set.

For a declared sequence (H_N,beta_N,R_N) with V_N=beta_N N tending to infinity define g_N=-log(d_N)/V_N. If g_N tends to g, then

    d_N = exp(-V_N g + o(V_N)).

This is an asymptotic identity. A limit of zero supplies no inverse-polynomial bound.

**Counterexample, full sequence.** At beta_N=1 take d_N=2^(-floor(sqrt(N))) and two weights (1+d_N)/2 and -(1-d_N)/2. Their absolute sum is 1 and their sum is d_N. Then g_N=(floor(sqrt(N))/N) log 2 tends to zero, while d_N^(-2)=4^(floor(sqrt(N))). For every fixed k, log(4^(floor(sqrt(N)))/N^k)=floor(sqrt(N)) log 4-k log N tends to infinity. The phase penalty is superpolynomial. Scaling both weights by 2^N/d_N represents the actual one-body-trivial fermionic family H_N=0 with Z_N=2^N; using f_O=Tr(O)/2^N preserves every declared observable abstractly. This is an existence counterexample, not an efficient estimator construction for arbitrary O.

Use separate tags EXACT_POSITIVE, POLYNOMIAL_PHASE_BOUND, ZERO_EXPONENTIAL_RATE and UNKNOWN. A proved improvement in d or a chosen cost at fixed size is meaningful even if both limiting rates are zero. No rate estimate is supplied by this review.

## FS3. What a phase-cost calculation actually proves

For independent samples and M>=1, the phase mean has exactly

    E |bar(s)-d|^2 / d^2 = (1-d^2)/(M d^2).

Proof: expand the squared norm, use independence to cancel off-diagonal centered terms and E|s-d|^2=1-d^2. This is a denominator variance statement, not a universal observable lower bound.

Let mu=E_q(s f)/d. For the usual ratio estimator, the identity

    bar(s f)/bar(s) - mu = bar(s(f-mu))/bar(s)

holds whenever bar(s) is nonzero. If E|f|^2 is finite, the multivariate iid CLT and Slutsky give an asymptotic Gaussian with covariance obtained by dividing that of s(f-mu) by d^2; the trace of this covariance is E|s(f-mu)|^2/d^2. This is a convergence-in-distribution statement, not a finite-sample error guarantee or automatic convergence of ratio MSE. A finite-sample bound requires denominator control, tails and a confidence parameter. For a Markov chain a suitable CLT and integrated covariance of this residual are needed; no universal worst-case mixing-time equality follows.

Two exact separations:

- If f=1 identically, the ratio equals 1 whenever defined, and its residual is zero even for very small d. This defeats a universal per-observable phase-cost lower bound.
- With positive q=(2^-N,1-2^-N) and f=(2^N,0), the mean is 1 and variance is 2^N-1. Independent sampling removes mixing difficulties, and the displayed rational values have O(N) bits, but the specified sample-mean estimator has exponential variance. This example proves a variance omission, not a hardness theorem against algorithms exploiting the known mean. If a uniform bound on estimator magnitude is available, enter it explicitly.

The ledger must specify the actual algorithm and include construction/search, preprocessing, per-step weight AND estimator evaluation, bit precision, initialization/burn-in, phase or denominator bounds, residual variance/tails, dependence control, accuracy and confidence. UNKNOWN is a valid entry. Neither three certificates nor the claimed four-way independence are established by the submitted witnesses.

## FS4. Observable-aware exact blocking and a genuine composition law

For finite arrays attach each configuration its moment vector v=(w,n_1,...,n_m) in C^(m+1). For any partition into blocks set

    v'_B = sum_(omega in B) v_omega.

This preserves Z and every N_j exactly (c=1). Summation has an identity, is associative and symmetric, and nested partitions obey (r composed with p)_*=r_* composed with p_* by finite-sum rearrangement. Thus these moment arrays form an algebra over the commutative operad: the n-ary operation is componentwise addition, including the zero vector at arity zero. These are explicit mathematical operation laws; no formal operad library or Lean kernel validation is claimed.

The new absolute weight W'=sum_B |w'_B| is at most W by the triangle inequality. Consequently d'=Z/W'>=d. Blocking may fail to improve strictly and may be prohibitively expensive.

Ordinary estimator decoding is partial: n'_j/w'_B is valid on nonzero-weight blocks. A zero-weight block can be omitted only if all its inserted numerators are zero. For w=(1,-1,1) and f=(1,0,0), blocking the first two entries produces weight 0 but numerator 1. Dropping that block changes the observable although Z=1 is preserved. Retaining moment vectors preserves the information; it does not itself furnish a positive-sampling estimator for the lost insertion. This is the reason to retain numerator data throughout staged operations.

Exact phase reweighting is an identity for the same original quantities. Merely replacing w by |w| produces W in place of Z; without retaining the phase correction and necessary normalization it is not a model-preserving positive representation.

## FS5. Determinant positivity: a valid sufficient theorem

**Finite matrix Kramers criterion.** Let B be any complex finite square matrix and T an antiunitary map with T^2=-I and TB=BT. Then det(I+B)>=0, without assuming B Hermitian or diagonalizable.

Proof. T maps the generalized eigenspace E_lambda of B bijectively to E_conjugate(lambda), so nonreal eigenvalues have equal algebraic multiplicities and contribute |1+lambda|^(2m). A real generalized eigenspace is T-invariant. If its complex dimension is m, write T=A conjugation in any basis; T^2=-I yields A conjugate(A)=-I. Determinants give |det A|^2=(-1)^m, so m is even. Each real eigenvalue contributes (1+lambda)^m>=0. If lambda=-1 the determinant is zero. Multiplying these factors proves the claim. An odd-dimensional ambient space cannot admit such a T.

For auxiliary fields this must hold for every admitted B(phi), with nonnegative remaining scalar measure factors and a proved exact HS representation. Reality alone is insufficient. Equal complex factors d*d can be negative (d=i), whereas conjugate factors d*conjugate(d)=|d|^2 are nonnegative. Actual Hubbard parameter/gauge/decoupling hypotheses are not inferred from these matrix controls.

## FS6. Existence, efficiency and obstruction scope

For every finite Hermitian H, a spectral basis has positive weights exp(-beta E_j) and estimator <j|O|j> for every declared O. This proves abstract existence of a positive representation; it does not control the cost of finding or using that basis. Complexity claims must specify deterministic or randomized algorithms, precision, promises and the problem family. The sign-hardness literature constrains efficient algorithms, not this elementary spectral existence statement. [Troyer-Wiese](https://arxiv.org/html/cond-mat/0408370).

Topological and local-basis obstruction imports require the exact class in their hypotheses. In particular, a locally sign-free DQMC exclusion is not an exclusion of arbitrary nonlocal diagonalization or all moment-array resummations. The invariant data and family hypotheses have not been supplied for an example here. [Golan-Smith-Ringel](https://arxiv.org/html/2005.05566).

Continuous changes are not universally prohibited: for the one-mode H=0 (Z=2), take w_t=(4t-2,4-4t), t in [0,1], and constant estimators f_I=1, f_number=1/2. The weights sum to 2 at every t and preserve both observables. At t=0 the weights are (-2,4), d=1/3; at t=1/2 they are (0,2), d=1. This is an elementary exact representation change crossing zero, not a nontrivial lattice sign cure or a counterexample within a protected topological class.

## FS7. Remaining admission obligations

A new interacting-family reduction needs an actual H and parameter/scaling range; declared observables; exact before/after partition and insertion identities; all-field or all-configuration positivity proof if claimed; explicit representation scope; an algorithm with costs, estimator/tail bounds and dependence analysis; and archived evidence. Finite exact controls can detect mistakes. They cannot promote a size fit to an asymptotic theorem or a toy determinant to a full DQMC family.

This corrected note discharges elementary bookkeeping errors and supplies reusable moment operations. It does not resolve item 10 beyond the imported protected/obstructed classes. No sampler data, new theorem of general fermionic curability or native Rust/Python/Lean implementation was created.
