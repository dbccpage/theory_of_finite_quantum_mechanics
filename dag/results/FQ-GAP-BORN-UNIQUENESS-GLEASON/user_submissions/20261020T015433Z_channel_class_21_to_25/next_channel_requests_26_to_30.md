# Channel-class follow-ups CC-26 through CC-30

Requested proofs only, not completion certificates. This CC namespace is independent of the BR Born/tomography numbering. Use K=Q(i), d,e,g>=1, complex PSD, star for adjoint. Earlier reviewed results may be cited with their recorded corrections. State physical assumptions separately from algebra and list reusable operations, relations, zero cases and admissible compositions.

## CC-26. Finite exact test for a deterministic CPTP map

Let Phi:M_d(K)->M_e(K) be K-linear. Prove Phi is CPTP iff its Choi matrix is PSD and Tr Phi(R)=1 for the following d^2 normalized rational rank-one states: E_jj, and for each j<k the projectors onto e_j+e_k and e_j-i e_k, each divided by its squared norm 2. Show these normalization tests force trace preservation on every matrix. Explain that CP alone does not normalize states. Separate the assumption that these preparations and deterministic output normalization are physically available from the algebraic equivalence.

## CC-27. Exact condition for multiplication of classical kernels

For Psi:M_d->M_e and Phi:M_e->M_g CPTP, define Delta_n to erase off-diagonal entries. Prove S_(Phi after Psi)=S_Phi S_Psi iff Delta_g Phi (Id-Delta_e) Psi Delta_d=0. Derive the sufficient no-detection and no-creation conditions. Give one exact rational failure using a rotation and its inverse, and one success where neither map is dephasing covariant. Dephasing covariance is not to be assumed necessary.

## CC-28. Rectangular classical lift and its identity

For a rational e by d stochastic matrix S, define E(S)(X)=diag(S diag X). Construct normalized rational e by d Kraus operators and prove E(TS)=E(T) after E(S). Show E(I_d)=Delta_d, and explain why this is the identity on classical diagonal states but not the identity channel on the full matrix algebra when d>1. Formulate the resulting composition statement with the correct objects and identities.

## CC-29. Equality of channels versus equality of presentations

Prove two rational Kraus families define the same channel iff their Choi matrices agree. Show sequential composition, tensor product and dual effect transport are well-defined after quotienting by this equality. Exhibit normalized families of different cardinalities defining the identity channel. Keep this operational quotient distinct from index-permutation equivalence. State which symmetric monoidal category is being constructed; its CPTP hom-sets are not K-vector spaces.

## CC-30. Constructive rational unitary completion

Let v in K^n satisfy v*v=1. For v!=e1 set w=e1-v, c=1-conjugate(v1), and U=I-ww*/c; for v=e1 take U=I. Prove c!=0, U*U=I and Ue1=v. Then use induction to complete any rational isometry V:K^d->K^n to a rational unitary whose first d columns equal V. Include n=d, d=1 and the v=e1 branch. No new norm-equation solver or imported Witt theorem is required.
