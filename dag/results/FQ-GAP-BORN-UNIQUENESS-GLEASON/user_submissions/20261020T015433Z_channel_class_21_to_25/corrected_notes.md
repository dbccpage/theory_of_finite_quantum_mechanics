# Corrected channel claims and constructive notes

## Positivity and normalization

The map X -> 2X has rational Kraus presentation {I,I}. It is CP at every ancilla dimension but maps a normalized state to trace 2. The zero map is CP but gives trace zero. Under a deterministic-channel interpretation, require Tr Phi(rho)=1 for every rational normalized state. The span of rational rank-one states determines trace preservation on Herm_d(K); K-linearity then determines it on all M_d(K). Together with positivity of the maximally entangled test, this yields CPTP by CC-22.

## Exact kernel-composition criterion

Let Psi:M_d -> M_e and Phi:M_e -> M_g, and let Delta_n erase off-diagonal matrix entries in dimension n. On a diagonal input X,

Delta_g Phi Psi(X) - Delta_g Phi Delta_e Psi(X)
 = Delta_g Phi (Id-Delta_e) Psi(X).

Thus S_(Phi after Psi)=S_Phi S_Psi exactly when this linear map vanishes on every diagonal input. Checking E_jj suffices. A sufficient condition is Delta_g Phi=Delta_g Phi Delta_e (no coherence detection); another is Psi Delta_d=Delta_e Psi Delta_d (no coherence creation). Full dephasing covariance of both maps is stronger.

Exact failure: U=(1/5)[[3,-4],[4,3]], Psi=Ad_U, Phi=Ad_U*. Then Phi Psi=id, so its kernel is I_2, whereas S_Phi S_Psi=[[337,288],[288,337]]/625.

Exact success without dephasing covariance of either map: take the same Psi=Ad_U and let Phi(X)=Tr(X) vv*, v=(3/5,4/5)^T. Both create off-diagonal output on E11, hence both fail dephasing covariance. Nevertheless Phi Psi=Phi and S_Phi S_Psi=S_Phi, since the latter has identical stochastic columns. The input coherences are not detected by this Phi.

## Classical lift and identities

For S of shape e by d, set E(S)(X)=diag(S diag(X)). The four-square construction realizes this with rectangular rational Kraus operators. It satisfies E(TS)=E(T) after E(S), but E(I_d)=Delta_d, not the full matrix identity channel when d>1. Its identity interpretation belongs to the classical diagonal state space; do not silently call it an identity-preserving embedding with objects M_d in the ordinary CPTP category.

## Rational unitary completion without a norm-equation search

Let v in K^n have v*v=1. If v=e1 take U=I. Otherwise put w=e1-v, c=1-conjugate(v1), and U=I-ww*/c. Then c!=0: v1=1 would force every other entry to vanish by the unit norm. Also w*e1=c and w*w=c+conjugate(c). Therefore Ue1=v and

U*U = I - ww*/c - ww*/conjugate(c)
       + (w*w) ww*/(c conjugate(c)) = I.

All entries remain in K. Given a rational isometry V:K^d -> K^n, first perform this unitary update on its first column. In U*V the first column is e1, and orthogonality forces the other columns' first coordinates to vanish. Recursively complete the lower (n-1) by (d-1) isometry, then assemble a block unitary. This is a written constructive proof sketch; the next proof request asks for all induction and endpoint details. It requires no imported Witt theorem or new norm-equation solution for a supplied isometry.

## Presentation equality

The normalized families {I} and {3I/5,4I/5} both implement X -> X. Their index sets have cardinalities 1 and 2 and cannot be related by a bijection. Choi/map equality supplies the operational quotient. General composition descends through this quotient because equal linear maps stay equal after composition or tensoring.
