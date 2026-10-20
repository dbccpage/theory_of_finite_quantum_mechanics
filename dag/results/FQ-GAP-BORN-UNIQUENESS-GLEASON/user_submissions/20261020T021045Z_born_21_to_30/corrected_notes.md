# Corrected statements and witnesses

## Effect readout domain and affine normalization

F(X)=Tr(rho X) is defined on every Hermitian matrix. Its restriction p to [0,I] satisfies p(A+B)=p(A)+p(B) only when A+B also lies in [0,I]. For example A=B=I has sum 2I outside the effect domain. Nonnegativity can still be discussed for F on the whole positive cone.

The map (I+S)/2 is a standard affine normalization. It is not an absolute minimum shift among all nonconstant affine effect maps: (I+S)/4 is also an effect, with a smaller shift. If the slope is fixed to 1/2, the +/-1 eigenvalues force the shift to be 1/2.

## Positive support

Let sigma be PSD, trace one, and P an orthogonal projection with Tr(sigma P)=1. Set Q=I-P. The PSD matrix Q sigma Q has trace zero, hence is zero by the zero-diagonal argument. The positive quadratic-form Cauchy-Schwarz inequality implies sigma q=0 for q in ran Q; thus sigma Q=Q sigma=0 and sigma=P sigma P. For P=WW*, sigma=W(W* sigma W)W*. No assumption that all per-W input states coincide follows until common compression consistency is imposed.

## The constructed remainder is strictly positive

Write N=d^2-1 for d>=2. Among the listed probes are G_12 and H_12. On their selected block, (7/4)I-G_12-H_12 has diagonal 3/4 and off-diagonal -(1+i)/2; its determinant is 1/16 and both diagonal entries are positive. On the other coordinates it is (3/4)I. Therefore G_12+H_12 <= (7/4)I. All other N-2 probes are <=I, so sum_i A_i <= (N-1/4)I. It follows that M_0=I-(sum A_i)/N >= I/(4N)>0. The source's main nonnegative bound was valid; its singular-remainder possibility is not realized by this construction.

## Exact PSD decision scope

The criterion for arbitrary real data is mathematical. An executable test requires a representation with effective equality/order, such as rational data or represented real-algebraic numbers with specified real embeddings. A complete rational pivot procedure can return either a PSD LDL* certificate or a rational vector of negative quadratic value; this is a next proof target.

A trace-one rational matrix can pass every diagonal and 2x2 principal-minor quick check yet fail PSD:

rho=(1/3)[[1,-1,-1],[-1,1,-1],[-1,-1,1]].

All 2x2 principal determinants are zero; for v=(1,1,1), v* rho v=-1. Its probe data x_j=1/3, g_jk=1/6, h_jk=1/2 are individually in [0,1] but are not jointly admissible.

## Explicit block permutation and nullary convention

Let q_i,n(j)=j for j<i and j+n-1 for j>i. The expanded outer permutation sends the old position q_i,n(j), j!=i, to q_tau(i),n(tau(j)); and sends i+l-1 to tau(i)+l-1 for 1<=l<=n. This specifies the block transport without conflating input colors with physical propagation direction. The ordinary identity/composition laws for permutations follow by reindexing the original labeled slot set. Branch-product associators and bijections implement nested associativity.

For positive output color d, a nullary normalized operation would require 0=I_d. Thus Ins(;d) is empty. Empty branch sets in individual slots are allowed within a normalized positive-arity instrument.

## Different continuations can still permit a common merge-first realization

Take d=e=2, outer Kraus slots K_1=E11 and K_2=E22. They are normalized together. Let the continuations be L_1=I and L_2=Z=diag(-1,1). Their CP maps differ (Ad_Z(E12)=-E12), but L_1 K_1=K_1 and L_2 K_2=K_2. Applying the common continuation I after merging yields exactly the same Kraus family. Thus equal continuations are sufficient for a general distributivity identity, but not necessary for a given instrument. Agreement on the reached branch ranges can be enough.

## Heterogeneous output states

For input density [1], use a continuation with K_1=[3/5]:K->K and K_2=[4/5,0]^T:K->K^2. It is normalized. Its branch states are [9/25] and [[16/25,0],[0,0]], of different sizes. Their matrix sum is undefined. Their trace probabilities sum to one. Their tagged direct sum is a 3x3 PSD trace-one state. For a general instrument use the outcome-indexed tuple or the direct-sum output algebra; summing matrices requires equal output spaces.

At a zero-probability branch, sigma=0 and all subsequent unnormalized states are defined and zero. Conditional normalized states alone are undefined.

## Scalar-output Choi matrices are transposed effects

For input-first vec and Phi_A(X)=Tr(A X), C_Phi has entry (j,k)=Phi_A(E_jk)=A_kj, so C_Phi=A^T. Equivalently A=Phi_A*(1)=C_Phi^T. Example A=(1/2)[[1,i],[-i,1]] is a rational effect; its scalar-output Choi matrix is (1/2)[[1,-i],[i,1]], which is different. Trace instruments identify with POVMs THROUGH this transpose. In general Phi*(I)=(Tr_output C_Phi)^T; identity normalization remains unchanged under transpose.

## Rational convexity

The Choi tuple set with K entries is closed under rational convex weights, using rational Gram re-realization. It need not be closed under irrational real weights: an irrational mixture of the identity and dephasing qubit Choi matrices has an irrational real off-diagonal entry. The ambient complex-channel spectrahedron is real-convex; its rational points are rationally convex. Arbitrary real probe values likewise produce complex rho entries, not necessarily K entries.
