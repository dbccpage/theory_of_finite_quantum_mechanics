# Next ten small proof requests BR-31 through BR-40

Requests only, not completion certificates. Some formalize corrections already sketched by the host; others extend the current written results. Earlier BR/CC results may be used with their recorded corrections. K=Q(i), star is adjoint, positive integer dimensions, PSD over C. Rational probes/instruments and real probabilities/complex states are distinct carriers. State assumptions, domains, zero cases, operations/relations and admissible compositions in each answer.

## BR-31. Typed branch-state semantics

For an instrument with output dimensions e_i, define its output state as the tuple (sigma_i)_i, sigma_i=sum_a K_i,a rho K_i,a*. Prove positivity and sum_i Tr(sigma_i)=1. Embed this as a tagged direct-sum density matrix and prove nested instruments act by the typed component maps. Derive scalar marginals without summing matrices of different dimensions. At trace zero retain the zero unnormalized state; define conditional normalization only at positive trace.

## BR-32. Choi/effect duality with every transpose explicit

Under input-first vec, prove Phi*(I_e)=(Tr_output C_Phi)^T. For a scalar-output map Phi_A(X)=Tr(A X), prove C_Phi=A^T and A=Phi_A*(1). Derive the corrected identification of trace instruments with rational POVMs. Give an imaginary off-diagonal effect for which A differs from its transpose. Explain why the identity-normalization condition is unaffected.

## BR-33. Precise merge/continuation compatibility

Prove the same-continuation coarse-graining identity with all outcome reindexing explicit. Show equal continuations are sufficient uniformly but not necessary for a fixed instrument, using outer slots E11,E22 and continuations I,diag(-1,1). At CP-map level, state the exact factorization condition for the merge-after-continuations map to have a common merge-first continuation. Separate disjoint merges, overlapping coarsenings and zero-slot profile changes.

## BR-34. Rational mixing and carrier scope

Prove rational Choi instrument tuples are closed under rational convex weights and exhibit an irrational mixture leaving K. Construct a normalized rational Kraus realization of a rational mixture without assuming sqrt(weight) lies in K. State precisely when branch states and normalized conditional states stay rational, and when arbitrary real probe values require complex rho entries. Do not assert that all probabilities and states lie in K.

## BR-35. Certifying rational PSD admission algorithm

For any rational Hermitian matrix A, give a terminating exact pivot algorithm returning either (i) a rational PSD LDL* certificate, or (ii) a nonzero vector v in K^d with v* A v<0. Cover negative diagonals, positive pivots, zero-diagonal nonzero blocks and singular PSD inputs. Prove correctness and witness transport through congruences. State which representation/sign procedures would additionally be required for real-algebraic inputs; arbitrary real-oracle comparisons are not automatically computable.

## BR-36. Explicit qubit probability-admission region

Use BR-25 at d=2 with probes E11, G12, H12, lambda=1/3, outcomes M1=E11/3, M2=G12/3, M3=H12/3 and M0=I-M1-M2-M3. Derive the inverse from q0,q1,q2,q3 to rho and an exact necessary/sufficient inequality for these probabilities to come from a density matrix. Include boundary/zero cases and the nonzero lower bound on q0. No tolerances or parameter fitting.

## BR-37. Operadic composition directly in Choi coordinates

Let A=C_Phi for Phi:M_d->M_e and B=C_Psi for Psi:M_e->M_g. Derive C_(Psi after Phi)[(j,alpha),(k,beta)]=sum_ab A[(j,a),(k,b)] B[(a,alpha),(b,beta)]. Prove the equivalent partial-trace link-product formula, declaring every tensor order and partial transpose. Show this gives the BR-30 slot composition without choosing Kraus representatives and preserves the appropriate summed instrument normalization.

## BR-38. Rational unitary equivalence after zero padding

Let A in K^(N by r), B in K^(N by s) satisfy AA*=BB*. Pad to R=max(r,s) columns. Prove there is a rational unitary U on K^R with B_padded=A_padded U. A possible route: for equal-norm vectors a!=b, set w=a-b, c=w*a and prove I-ww*/c is unitary and maps a to b. Match the equal-Gram row-vector families one by one, fixing the already matched vectors. Include zero/dependent vectors and all conjugation conventions. Apply this to Kraus vectorizations without assuming minimal rational Kraus count equals Choi rank.

## BR-39. Parallel composition compatible with the operad

For instruments K_i,a:K^d->K^{e_i} and L_j,b:K^{d'}->K^{f_j}, use Kraus operators K_i,a tensor L_j,b with ordered outcome pairs (i,j). Prove normalization, the tensor unit and swap laws. Show simultaneous continuation substitution commutes with tensoring up to explicit outcome/branch index bijections. Prove this structure descends to the CP-map quotient. Keep the tensor/composite physical interpretation an explicit input.

## BR-40. Rational dilation of a full typed instrument

For normalized rational Kraus slots K_i,a:K^d->K^{e_i}, set E=sum_i e_i and R=sum_i |A_i|. Construct a rational isometry V:K^d->K^E tensor K^R and orthogonal environment pointer projections Q_i whose outcome states, after discarding the environment, equal J_i Phi_i(rho) J_i*, where J_i embeds K^{e_i} in the i-th direct-sum block. Prove the state-update identity, not just the effect probabilities. Retain zero outcome labels; normalization ensures R>=1. State finite size bounds and all physical assumptions separately.
