# Corrected statements and added proof bridges

Status: written mathematics with exact finite controls; NOT KERNEL-CHECKED.
K is Q or Q(i), embedded in C with the usual involution. Dimensions are positive unless an empty Kraus index set is explicitly admitted. The earlier Choi/CP and finite rational Kraus-factorization results are declared imports, not newly discharged here.

## CC-26: normalization by field-appropriate probes

For K=Q(i), use D_j, rho+_jk, rho-_jk from the submission. The inversion formulas show that these d² states form a K-basis of M_d(K). Thus a K-linear Phi is CPTP iff J(Phi)>=0 and Tr Phi(rho)=1 on all probes.

For K=Q, use only D_j and rho+_jk. These d(d+1)/2 states form a Q-basis of Sym_d(Q). Under CP, A=Phi†(I) is real symmetric, since a Kraus representation gives A=sum K_i^T K_i. If Tr Phi(rho)=1 on these probes, Tr((A-I)rho)=0 on their symmetric span. Diagonal probes give (A-I)_jj=0, and plus probes give (A-I)_jk=0. Thus A=I. Hence Tr Phi(X)=Tr X for every real matrix X, including the skew part. This is not a claim that real density matrices span all real matrices.

Qualified minimality: fix normalized-state scalar trace queries, permit all CP maps into a nonzero output dimension, and assume no prior trace-nonincreasing or other normalization restriction. Let h=d² over Q(i), h=d(d+1)/2 over Q, the rational dimension of the Hermitian effect space. Fewer than h queries leave a nonzero Hermitian H with Tr(H rho_l)=0, by rational linear algebra. Choose a nonzero rational epsilon small enough that A=I+epsilon H is positive definite. For a fixed rank-one trace-one output projector P0, Phi_A(X)=Tr(AX)P0 has Choi A^T tensor P0, is CP, passes every specified query, and is not TP because A!=I. This also defeats fewer than h adaptive queries on the path giving only output 1: construct H after fixing those queries. This lower bound is for this query model, not arbitrary matrix-valued queries.

Under the additional promise A<=I, one faithful state rho>0 suffices: B=I-A>=0 and Tr(B rho)=0 imply B=0. This prevents overclaiming the preceding minimality.

For input-first J, Tr_out J=(Phi†(I))^T; the normalized equation is Tr_out J=I. Q/Q(i)-valued CP maps allow nonnegative rational scaling, and CPTP maps allow rational convex mixing; composition and tensor have their usual dimension checks. Arbitrary real coefficients require extending the carrier.

## CC-27: exact image-annihilation criterion

Let C_Psi=im((Id-Delta_e) Psi Delta_d), a K-linear subspace of the off-diagonal matrices. Then

    S_(Phi Psi)=S_Phi S_Psi iff (Delta_g Phi)|_(C_Psi)=0.

Proof: subtract Delta_g Phi Delta_e Psi Delta_d from Delta_g Phi Psi Delta_d. Their difference is Omega. Since Omega factors through Delta_d, equality of the diagonal kernels is equivalent to the full obstruction map vanishing. Image-annihilation is precisely the same assertion.

Annihilating every matrix unit occurring in the support of C_Psi suffices but is not necessary. The U,V cancellation counterexample in review.md gives a strict separation even for Gaussian-rational unitary channels. In the submitted 3D example, replace the detected value by (12/25)(E11-E22). Matrix multiplication is associative; this criterion concerns preservation of composition by the shadow map.

## CC-28: corrected classical category

For rational column-stochastic S define E(S)(X)=diag(S diag X). A decomposition S_kj=sum_m a_kjm² over Q, with at most four squares per nonzero entry, gives Kraus a_kjm E_kj, so E(S) is rational CPTP. E(TS)=E(T)E(S), E(I_d)=Delta_d, and S_E(S)=S.

Define the target objects to be (M_d(K),Delta_d), with arrows CPTP Phi satisfying Phi=Delta_e Phi Delta_d. Their identities are Delta_d. Each such arrow is determined by its rational stochastic matrix S_Phi and equals E(S_Phi). Thus E is full and faithful on these hom sets. In the ambient full channel category it is a composition-preserving, nonunital assignment, not an ordinary functor. For e=1, E(S)=Tr. Scalar mixtures inside this category have rational coefficients.

## CC-29: equality and the adjoint class

J is a linear bijection with inverse Phi(X)=Tr_in[(X^T tensor I)J]. Hence equality of Choi matrices is equality of maps and descends through typed composition and tensor product. Kraus presentations are identified by their common map, not index permutations.

All CP classes are closed under the HS adjoint: its Kraus operators are K_i*. TP of Phi is equivalent to unitality of Phi†. Phi† is TP iff Phi is unital. Thus an adjoint stays CPTP only when the original CPTP map is also unital (with the appropriate input/output identities). The reset example separates these conditions.

## Added bridge: equal-Gram unitary over K without normalization roots

Lemma A. If a,b in K^N satisfy a*a=b*b and a!=b, let w=a-b and c=w*a. Then c+conj(c)=w*w>0, so c!=0. The matrix T=I-ww*/c is unitary, sends a to b, and fixes every x with w*x=0.

Proof. Expand w*w=a*a-a*b-b*a+b*b. Equal norms give c+conj(c)=2 a*a-b*a-a*b=w*w. Consequently

    T*T=I-ww*(1/c+1/conj(c))+w(w*w)w*/(c conj(c))=I.

Also Ta=a-w(w*a)/c=b. If w*x=0, Tx=x. All entries are obtained by field operations and conjugation. For a=b, including a=b=0, choose T=I instead. No division by a norm or square root is used.

Lemma B. If A,B in K^(M x R) satisfy AA*=BB*, there is a K-unitary U of size R such that B=AU.

Proof. Let a_j=A[j,:]* and b_j=B[j,:]* be conjugate row columns. Their Gram matrices agree. Start T=I and match these columns in order. Assume T a_i=b_i for i<j. Put a'_j=T a_j. For each matched b_i,

    b_i* a'_j = a_i* a_j = b_i* b_j.

Thus b_i*(a'_j-b_j)=0. Lemma A applied to a'_j,b_j gives a unitary update fixing all earlier b_i and matching the next vector (or the identity if already equal). Replace T by update times T. At the end T a_j=b_j for all rows, so B=A T*. Put U=T*. Dependent, zero, and empty rows cause no problem; R=0 gives the empty identity. This proof works for any conjugation-closed subfield of C.

Kraus consequence. Vectorize input-first, take A's columns vec(K_i) and B's columns vec(L_j), and append zero columns so both have R=max(r,s). Equality of Choi matrices is AA*=BB*. Lemma B gives B=AU and therefore L_j=sum_i K_i U_ij. With row-index mixing notation V=U^T, L_j=sum_i V_ji K_i; V is unitary as well. This proves rational unitary mixing after common zero-padding. It avoids assuming rational orthonormal bases of arbitrary subspaces.

## CC-30: completion remains a distinct lemma

For an already given W in K^(n x m) with W*W=I_m, the submission's unit-vector rank-one update and induction extend W to a K-unitary. Handle v=e1 separately before division by 1-conj(v1). The proof preserves K and needs no square roots. The equal-Gram bridge above proves existence of an intertwiner for CC-29; CC-30 separately completes prescribed orthonormal columns. Both are useful, with distinct inputs.

No argument above selects a physical channel class, completes the scalars to C, or proves original Born-rule uniqueness. General formal verification remains pending.
