# Next ten small proof requests

Status: REQUESTS ONLY. None of Steps 11-20 is claimed proved by this file. AuthorityEffect: None. User submissions for Steps 1-10 and review corrections are linked in README.md. Prefer a short exact proof, list imported theorems, certify all domains and zero cases, and list reusable operations, relations and composition conditions with every answer.

## 11. Rational positive-semidefinite elimination

For d>=1 and A in Herm_d(Q(i)) positive semidefinite over C, prove there are a permutation matrix P, an invertible unit lower-triangular L over Q(i), and a diagonal D with nonnegative rational entries such that P* A P = L D L*. Give a constructive induction including singular A. Explain why a zero diagonal entry of a PSD matrix forces its entire row and column to vanish. Use no irrational square roots.

## 12. Rational Gram factorization

Using Step 11, prove every rational Hermitian PSD d by d matrix A equals B*B for a rectangular matrix B over Q(i) with at most 4d rows. You may explicitly import Lagrange's integer four-square theorem; show how it gives four rational squares for each nonnegative rational diagonal coefficient. Include A=0. This is rectangular factorization, not a claim about a square rational square root.

## 13. Rational projective dilation of a finite POVM

Let A_1,...,A_m in Herm_d(Q(i)) be PSD, m>=1, and sum A_i=I_d. Using Step 12, construct a rational isometry W:Q(i)^d -> Q(i)^N and pairwise orthogonal rational projections Q_i summing to I_N such that W*Q_i W=A_i. Obtain N<=4md. Prove each identity. A completion of W to a rational unitary is not assumed.

## 14. Derive effect additivity from explicit dilation consistency

Fix input dimension d. For every rational isometry W:Q(i)^d -> Q(i)^N, suppose mu_W maps rational orthogonal projections to nonnegative real numbers, is normalized at I_N, and is additive on orthogonal projections. Assume compression consistency: W*QW=W'*Q'W' implies mu_W(Q)=mu_W'(Q'). Using Step 13, prove p(A)=mu_W(Q) for any dilation of A is well defined, normalized, and additive whenever A,B,A+B are effects. State exactly where compression consistency is used; it is an additional assumption to audit, not a proved physical principle.

## 15. Real-valued probabilities on rational effects

Replace the old codomain Q_{>=0} by R_{>=0}, keeping effects in Herm_d(Q(i)). Prove normalized effect additivity gives a unique complex Hermitian PSD rho with Tr(rho)=1 and p(A)=Tr(rho A) for every rational effect. Identify the changes needed in Steps 1-10. Do not assume rho has rational entries or assume p is linear or continuous.

## 16. Unique extension to all complex effects

For p and rho as in Step 15, prove rational Hermitian effects are dense, in operator norm, in the full complex effect interval [0,I]. Construct approximants that preserve both positivity bounds. Prove p extends uniquely to a nonnegative normalized effect-additive function on all complex effects and that this extension is A -> Tr(rho A). Derive continuity from positivity/additivity rather than imposing it as an extra physical assumption. State the imported real/complex topology explicitly.

## 17. Compression consistency is a separate hypothesis

Construct two rational isometries W_1,W_2 with the same two-dimensional input and normalized, nonnegative, orthogonally additive projection valuations mu_1,mu_2 on their target spaces. Find target projections Q_1,Q_2 with W_1*Q_1W_1=W_2*Q_2W_2 but mu_1(Q_1)!=mu_2(Q_2). This should demonstrate exactly why normalization and orthogonal additivity alone do not imply the consistency assumed in Step 14.

## 18. Explicit qubit projector countermodel

Construct an explicit function f from all rank-one projections in Herm_2(Q(i)) to {0,1} satisfying f(P)+f(I-P)=1. Extend it by f(0)=0 and f(I)=1, and prove additivity on every orthogonal pair of rational projections. Prove no density matrix rho can satisfy f(P)=Tr(rho P) for every such P. Give a deterministic formula, not an appeal to arbitrary choices. No assignment to general effects is required.

## 19. Exact separator from full effect additivity

Set A=diag(1,0) and B=(1/5)[[4,-2],[-2,1]]. Prove A and B are rational rank-one projections and -I/2 <= A-B <= I/2 by exact rational calculations. Construct a projector valuation of the kind in Step 18 with f(A)=1 and f(B)=0. Use Step 3 to show it cannot extend to any normalized nonnegative effect-additive p on [0,I]. Keep the projector and effect domains distinct.

## 20. Composition laws for rational instruments

An instrument has finitely many outcomes i and finite Kraus families K_{i,a}:Q(i)^d -> Q(i)^{e_i}, with sum_{i,a} K_{i,a}*K_{i,a}=I_d. For each branch i, let L_{i,j,b}:Q(i)^{e_i} -> Q(i)^{f_{ij}} be an instrument. Prove the composite families L_{i,j,b} K_{i,a} are normalized. Prove associativity up to explicit finite-index bijections, the singleton identity law, and compatibility with outcome relabeling. For operadic typing, regard input colors as continuation dimensions (e_i) and output color as d; substitution requires matching e_i. Distinguish these algebraic composition laws from a physical justification of instrument dynamics. Record all established colors, operations, relations, and admissible substitutions.

The targets cover exact rational dilation, the extra measurement-consistency assumption, real-valued and full-complex representation, explicit projector obstructions, and instrument composition. They do not by themselves supply an original projective Gleason theorem in dimension >=3 or derive the Hilbert/effect model from the finite-QM ontology.
