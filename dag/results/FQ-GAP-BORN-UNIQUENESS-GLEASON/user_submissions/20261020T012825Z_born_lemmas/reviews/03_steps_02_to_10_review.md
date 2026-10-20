# Review of submitted Steps 2-10

The core arguments establish the stated conditional rational-matrix representation on ordinary mathematical review. Steps 2-3 use only the standing interval assumptions and Step 1. Steps 4-7 explicitly add an order unit. Steps 8-10 explicitly specialize to Herm_d(Q(i)), d>=1, with the usual complex PSD order. The rational trace-basis signs in Step 9 are correct. Step 10 explicitly uses real/complex continuity and density of rational complex vectors; those are imported mathematical background, not consequences of a finite physical ontology. No part has a new Lean certificate.

Corrections and proof details (original source retained unchanged):

1. Step 3 reusable halving claim: epsilon<=1 is sufficient to ensure C=(B+epsilon*u)/2 lies in E uniformly for B in E. It is not necessary for a particular B. Counterexample: V=Q, u=1, B=0, epsilon=3/2 gives C=3/4 in E. The main proof already assumes epsilon<=1 and is unaffected.
2. Step 3 seminorm scope: before the order-unit assumption, do not assert a finite seminorm on all of V. The sandwich inequality is proved for effect differences. Once u is an order unit, define the real infimum over nonnegative rational bounds and call it a seminorm, potentially degenerate without an Archimedean/separation condition. For epsilon>1 the effect probability bounds already give the needed inequality; take infima to obtain the 1-Lipschitz statement on effects.
3. Step 8 maximum/basis indexing assumes d>=1, as in the request. Add that condition explicitly when extracting the theorem into a standalone file.
4. Step 10 converse needs an explicit standard matrix lemma: rho,A PSD implies Tr(rho*A)>=0. Then Tr(rho*(I-A))>=0 gives the upper bound and trace linearity gives additivity. This was asserted rather than proved in the submitted converse. Proposed next tasks include a rational Gram factorization to supply a self-contained exact proof. The forward representation argument does not depend on this converse.
5. The reusable rank-one rescaling by 1/||v||^2 is for v!=0. The v=0 case is the zero effect. No division is allowed there.
6. Rational-valued p restricts the representing density matrix to Q(i) entries. Real-valued probabilities on rational effects require a separate codomain-generalized representation theorem and can give arbitrary complex density matrices.

Acceptance: forward Steps 2-10 accepted as reviewed written arguments with these stated assumptions and corrections. Converse positivity detail pending explicit proof. No full projective Gleason theorem, no derivation of effect additivity from operational axioms, no kernel certificate, and no publication claim.
