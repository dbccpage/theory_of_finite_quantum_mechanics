# General written proofs for CC-26 through CC-30

K=Q(i), embedded in C; all physical object dimensions d,e,g are positive integers. Star is adjoint, CP uses complex matrix positivity, and maps are K-linear. These are written algebraic proofs, not Lean certificates. Imports: the earlier reviewed finite Choi/Kraus theorem and Lagrange's integer four-square theorem. Preparations, choice of physical channels and composites remain declared interpretations.

## CC-26: finite exact CPTP criterion

Let D_j=E_jj, R_jk=(e_j+e_k)(e_j+e_k)*/2 and T_jk=(e_j-i e_k)(e_j-i e_k)*/2. These are positive rank-one trace-one matrices in M_d(K). There are d+2 binomial(d,2)=d^2. For j<k,

E_jk = R_jk-i T_jk-(1-i)(D_j+D_k)/2,
E_kj = R_jk+i T_jk-(1+i)(D_j+D_k)/2.

Thus they span all matrix units over K. If each tested output trace equals 1, applying trace Phi to these identities gives trace Phi(E_jk)=0 for j!=k and trace Phi(E_jj)=1. By K-linearity, trace Phi(X)=trace X for every X. Conversely TP implies all these tests. With input-first Choi blocks C_Phi[j,k]=Phi(E_jk), the finite Choi theorem supplies CP iff C_Phi is HERMITIAN PSD. Combining the two conditions gives the requested equivalence, including d=1.

For an exact Gaussian-rational Choi matrix, Hermiticity and nonnegative principal minors decide PSD using rational operations and signs. Necessity follows by restricting a PSD form. For sufficiency, the coefficients of det(A+tI) are sums of principal minors and its leading coefficient is 1, so the determinant is positive for t>0. A negative eigenvalue of Hermitian A would make det(A+tI)=0 at a positive t, contradiction; all eigenvalues are real by the finite Hermitian spectral theorem. This is a finite decision method, potentially exponential. CP alone does not impose TP: A=diag(1,1/2) yields Phi(X)=AXA* and trace Phi(E11)=1/4.

## CC-27: exact classical-kernel obstruction

Write i_d(p)=diag(p) and pi_e(X)=its diagonal column, so Delta_e=i_e pi_e and S_Phi=pi_g Phi i_e. Then

S_(Phi Psi)-S_Phi S_Psi = pi_g Phi (Id-Delta_e) Psi i_d.

This matrix vanishes iff its values on coordinate columns vanish. Since i_g is injective, this is equivalent to Delta_g Phi (Id-Delta_e) Psi Delta_d=0. Sufficient conditions are no creation, (Id-Delta_e)Psi Delta_d=0, and no detection, Delta_g Phi(Id-Delta_e)=0. They are not necessary separately for a particular pair.

The no-detection condition holds iff Phi^dagger(E_mm) is diagonal for every output m: off-diagonal input matrices are Hilbert-Schmidt orthogonal to all diagonal matrices, and the adjoint transfers the pairing. No assumption of dephasing covariance is needed.

The source's rational U followed by U is a failure with the recorded 288/625 defect. The requested U followed by U* is another: their quantum composite is identity, whereas their stochastic product is S_U^T S_U, which is not identity because both transition probabilities in each column are nonzero. The recorded 3D disjoint-coherence example supplies a success with both sufficient factor conditions absent.

## CC-28: rational rectangular classical lift

Let S be an e by d nonnegative rational matrix with column sums one. For each nonzero s_kj=p/q with p,q positive integers, Lagrange gives integers a_1,...,a_4 with pq=sum a_m^2. Set K_kjm=(a_m/q)|k><j| and discard zero coefficients if desired. Then sum_m(a_m/q)^2=p/q. Consequently

sum_(k,j,m) K_kjm* K_kjm = sum_j (sum_k S_kj)E_jj = I_d,
Phi_S(X)=sum K_kjm X K_kjm* = diag(S diag X).

All entries are rational; there are at most 4 times the number of nonzero entries Kraus operators. Rectangular dimensions and zero entries cause no change to the proof. For compatible stochastic T, Phi_T Phi_S(X)=diag(TS diag X)=Phi_(TS)(X). But Phi_(I_d)=Delta_d. Restricting to diagonal algebras gives the usual unital classical functor. Equivalently, take dephased objects (M_d,Delta_d) and morphisms Phi=Delta_e Phi Delta_d, whose identities are Delta_d. On full M_d the normalized identity channel is Id, and the lift is not an identity-preserving functor with the naive object assignment.

The Choi convention is C_(Phi_S)=sum_(j,k) S[k,j] E_jj tensor E_kk, INPUT before OUTPUT. All-zero CP maps are allowed with typed empty Kraus families but are not TP in positive input dimension.

## CC-29: operational quotient and monoidal operations

Input-first Choi equality is equivalent to equality on every matrix unit because each image is one block, hence to map equality by K-linearity. For a Kraus family, C_Phi=sum_a vec(K_a)vec(K_a)*, with vec(K)=sum_j e_j tensor K e_j. Kraus label permutations do not exhaust equal presentations. Any coefficients c_a in K with sum |c_a|^2=1 give identity-channel operators c_a I; the displayed families show different cardinalities. Rational unitary mixing of Kraus indices preserves the same Gram/Choi matrix and supplies the distinct dephasing presentations.

Sequential composition has Kraus L_b K_a; normalization is sum_a K_a*(sum_b L_b*L_b)K_a=I. Tensor composition has Kraus K_a tensor L_b, with normalization I tensor I. Equality of maps is preserved by both operations (use matrix units/simple tensors). The adjoint Phi^dag(Y)=sum K_a* Y K_a depends only on Phi by the nondegenerate Hilbert-Schmidt pairing, and (Phi Psi)^dag=Psi^dag Phi^dag. It is unital when Phi is TP.

Thus positive integer dimensions, K-rational CPTP maps as morphisms, ordinary identity channels, sequential composition, Kronecker tensor and permutation unitaries give a symmetric monoidal category. Its hom-sets are not K-vector spaces: adding two TP maps doubles the trace, and arbitrary complex scaling does not preserve positivity. Rational convex mixtures are available with the appropriate rational Kraus realization; arbitrary real mixing can leave the coefficient carrier.

For A=C_Psi in order (d,e) and B=C_Phi in order (e,g), the composite components are

C_(Phi Psi)[(j,alpha),(k,beta)] = sum_(a,b) A[(j,a),(k,b)] B[(a,alpha),(b,beta)].

Expanding the middle trace proves the link expression Tr_e[(A tensor I_g)(I_d tensor B^(T_e))]. T_e is the transpose on B's input e-leg. Tensoring two Choi matrices first produces legs (d,e,d',e'); the permutation to (d,d',e,e') produces the composite tensor channel's input-first Choi matrix. These formulas follow from index identities, not just the qubit fixture.

## CC-30: rational unitary completion

For a unit vector v in K^n, handle v=e1 by U=I. Otherwise let w=e1-v and c=1-conjugate(v1). If c=0, v1=1 and unit norm makes every other coordinate zero, contradiction. Also w*e1=c and w*w=2-v1-conjugate(v1)=c+conjugate(c). Therefore U=I-ww*/c sends e1 to e1-w=v. Multiplying U*U, its ww* coefficient is

-1/c-1/conjugate(c)+(w*w)/|c|^2 = 0.

Hence U is unitary, with entries in K because c!=0 and K is a field.

For an n by m isometry W, first use U1=house(W[:,1]). The matrix U1* W has first column e1; orthogonality makes the rest of its first row zero. Its lower (n-1) by (m-1) block W' is an isometry. By induction complete W' to a unitary U', then U1 diag(1,U') has first m columns W. Base m=0 returns I_n; the recursive 0 by 0 unit is only a private algebraic base, not a physical zero-dimensional object. This covers n=m, m=1 and first column e1, without new norm solving or Witt extension. The script's added admission checks make the algorithm's preconditions explicit.

## Evidence grade and remaining work

These arguments establish the requested statements as written finite algebra under their declared imports. The replay covers explicit fixtures, not arbitrary dimensions or a formal proof. General Lean implementations, arbitrary physical preparation availability and the original finite-QM reconstruction remain unestablished by this bundle.
