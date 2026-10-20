# Next ten proof requests: 21-30

These are requested proof units, not claims of new formal completion. Some fill omitted details or make the host review sketches precise; others extend the results. Earlier reviewed Steps 1-20 may be used with the corrections in review.md. All general Lean certificates are pending. AuthorityEffect: None.

Standing conventions: K=Q(i), d,e>=1, star is conjugate transpose, Hermitian order is the usual complex PSD order, probabilities may be real. Each answer should state assumptions/imports, domains, zero cases, reusable operations/identities and permitted substitutions. A physical interpretation is an assumption to state, not a consequence of the matrix algebra.

## 21. Affine effect probes and tomography

For j<k let S_jk=E_jk+E_kj and T_jk=i(E_jk-E_kj). Prove E_jj, G_jk=(I+S_jk)/2 and H_jk=(I+T_jk)/2 are rational effects. For normalized effect-additive p, derive rho_jj=p(E_jj), Re rho_jk=p(G_jk)-1/2 and Im rho_jk=p(H_jk)-1/2. Prove these d^2 probe values determine rho. Do not claim positive scaling alone turns the indefinite S_jk,T_jk into effects.

## 22. Supply the explicit positivity converse

Let rho be any complex Hermitian PSD matrix and A any rational Hermitian PSD matrix. Use rational Gram factorization A=B*B to prove Tr(rho A)>=0 by expanding Tr(B rho B*) into nonnegative quadratic forms. Deduce that Tr rho=1 gives a normalized nonnegative effect-additive p on rational effects. Prove the bound p(A)<=1 for 0<=A<=I. Avoid importing a complex matrix square root for this argument.

## 23. Exact admission criterion for finite probe data

Assign real numbers a_j, g_jk, h_jk to the probes in 21. Construct the Hermitian matrix rho from those data. Prove the data extend to a normalized nonnegative effect-additive p on all rational effects if and only if sum_j a_j=1 and rho is PSD; prove uniqueness. State what follows for rational-valued data. Use exact equalities and inequalities, not tolerance-based admissibility.

## 24. Compression consistency is equivalent to one common input state

In the setting of 14, prove (C) is equivalent to existence of a single density matrix rho on the input space such that mu_W(Q)=Tr(W rho W* Q) for every rational isometry W and rational target projection Q. You may use 13-15. Derive mu_W(WW*)=1 and zero probability for projections orthogonal to ran W. Distinguish the operator pullback W*QW from the state pushforward W rho W*; separate maps or states for each W do not suffice.

## 25. One rational informationally complete measurement

Construct, for every d>=1, a POVM consisting of exactly d^2 rational PSD effects summing to I whose probabilities determine every complex density matrix. Give an explicit rational smallness bound in a construction from a rational traceless Hermitian basis. Prove fewer than d^2 outcomes cannot determine every density matrix using one fixed POVM. Handle d=1. A suggested construction is I/d^2 plus small traceless perturbations, with the last effect cancelling their sum.

## 26. Fixed-profile colored instrument operad

For profile (e_1,...,e_m;d), retain ordered outcome slots and rational Kraus families K_i,a:K^d -> K^{e_i}, with sum K* K=I_d. Quotient only by bijections of Kraus indices within each slot. Define substitution into a specified slot by operator multiplication and prove well-definedness, normalization, identities, associativity and permutation equivariance. Outcome permutations transport profiles and slots. State explicitly the canonical index bijections used in the laws.

## 27. Coarse-graining with its correct substitution conditions

For the instruments in 26, merge outcomes only when their output dimensions agree, using disjoint union of their Kraus families. Prove normalization and addition of effects, and associativity of repeated coarse-graining. Prove coarse-graining commutes with subsequent substitution when the merged outcomes receive the same continuation instrument; exhibit why this condition matters. Explain why deleting a zero outcome changes the profile, whereas deleting zero Kraus operators within a fixed outcome can be allowed under CP-map equality.

## 28. State-effect duality and sequential probabilities

For a density matrix rho and instrument K, define the unnormalized branch state sigma_i=sum_a K_i,a rho K_i,a*. Prove sigma_i is PSD, Tr sigma_i=Tr(rho A_i), and the branch traces sum to one. Under a subsequent instrument L_i, prove joint probabilities are nonnegative and have the correct marginals, using cyclic trace. Define the normalized conditional state only when Tr sigma_i>0, and prove sigma_i=0 when its trace is zero. No collapse postulate should be inferred from these algebraic statements.

## 29. Rational Choi test and rational Kraus realization

Let Phi:M_d(K)->M_e(K) be K-linear and let its complex-linear extension be star-preserving. Define J(Phi)=sum_ab E_ab tensor Phi(E_ab). Prove the following are equivalent: J(Phi) is PSD; the complex extension is completely positive; Phi(X)=sum_alpha K_alpha X K_alpha* with rational K_alpha and at most 4de Kraus operators. Use 12 for the constructive direction, fixing a vectorization convention and all transpose/conjugation signs. Prove trace preservation is equivalent to Tr_output J(Phi)=I_d.

## 30. Operational quotient of the instrument operad

Within a fixed ordered outcome profile, declare two rational Kraus instruments equivalent exactly when their CP maps agree separately at each outcome. Prove this is equivalent to equality of their outcome Choi matrices, and that substitution, identities, relabeling and dimension-compatible coarse-graining descend to this quotient. Prove zero Kraus branches may be removed within a slot while zero outcome slots remain part of the profile. Do not identify this quotient with Kraus-index permutations alone or assume a rational unitary gauge between all presentations.

These targets develop a usable finite operational algebra. They still leave the derivation of the matrix/effect model, the chosen physical equivalence and the additional compression-consistency assumption explicit. They do not assert original projective Gleason uniqueness from orthogonal-frame additivity alone.
