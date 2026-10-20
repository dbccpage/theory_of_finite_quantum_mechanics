# Corrections and exact witnesses

## Affine tomography effects

For j<k, S=E_jk+E_kj and T=i(E_jk-E_kj) have eigenvalues +1,-1 on the selected two-dimensional block. No nonzero positive scaling makes them effects. Instead G_S=(I+S)/2 and G_T=(I+T)/2 are rational effects, since -I<=S,T<=I. For the derived unital linear extension F,

F(S)=2p(G_S)-1; F(T)=2p(G_T)-1;
rho_jj=p(E_jj); Re(rho_jk)=p(G_S)-1/2; Im(rho_jk)=p(G_T)-1/2.

There are d+2 choose(d,2)=d^2 such probes. Their diagonal probabilities sum to one. Their values need not be independently specifiable; PSD of the reconstructed rho is the consistency condition to prove in a later task.

## One common compression map

(C) implies a single p by rational dilation (Step 14), hence a single rho by Step 15. Cyclic trace gives mu_W(Q)=Tr(rho W*QW)=Tr(W rho W* Q). Conversely this formula with fixed rho immediately gives (C). Separate per-W factorization does not imply a common p.

A stronger independence example than the submitted one: W=I_2 and W'=[I_2;0_2] into K^4. Choose sigma_W=E11 in K^2 and sigma_W'=E22 in K^4. Both state supports lie in their respective isometry ranges, so mu_W(WW*)=mu_W'(W'W'*)=1. Nevertheless Q=E11 and Q'=E11 have the same compressed effect E11 and probabilities 1 and 0. Thus even range normalization and separate factorization through compression do not imply shared consistency.

## Three axes versus four directions

The Hermitian trace-one matrix H=(I+sigma_x+sigma_y+sigma_z)/2 has Bloch vector (1,1,1). It gives value 1 at all three positive coordinate-axis projections and 0 at their antipodes. It is not PSD (det H=-1/2). At n=(3/5,0,4/5), it gives (1+3/5+4/5)/2=6/5, whereas the submitted selector gives 1. Thus the actual four-direction argument is valid; the stronger three-axis affine claim is not.

## Every binary qubit selector is obstructed

Distinct rank-one qubit projections have distance <=1, with equality exactly for complementary projections. If Q is not complementary to P, their distance is <1; choose rational epsilon strictly between that distance and 1. Step 3 forces equal values for any binary-valued effect-extendible selector. For Q=I-P, choose a rational rank-one R different from P and I-P; E11 works unless those two are E11,E22, in which case (1/2)[[1,1],[1,1]] works. Then both edges P-R and R-Q have distance <1, so their values must agree too. Hence the selector is constant, contradicting complement normalization. This is a written proof under the usual complex norm/order facts, not a claim that a finite replay proves the universal statement.

## Outcome quotient is incompatible with an untransported fixed-slot graft

All colors below are dimension 1 and every outcome has one scalar Kraus operator. K=(3/5,4/5) and K'=(4/5,3/5) are equal if outcome permutation is quotiented. Substitute L=(3/5,4/5) into the first slot and identity into the second slot.

K yields the Kraus multiset {9/25,12/25,20/25};
K' yields {12/25,16/25,15/25}.

Both are normalized (squared amplitudes sum to 1), but no outcome/branch bijection equates the multisets. A well-defined slot graft must retain slot identity, or transport the continuation along the chosen outcome bijection. In a colored symmetric operad keep a fixed ordered profile (e_1,...,e_m;d), allow per-slot Kraus-index bijections, and treat outcome permutations as profile-transport operations. The general repaired operad construction is a next proof target.

## Zero outcomes

The one-outcome identity instrument {I_d} and the two-outcome instrument {I_d,0} have different arities. There is no bijection of their outcome sets. Removing zero Kraus branches inside a fixed outcome preserves its CP map under a map-based quotient; removing an entire zero outcome changes the profile. These two operations must remain distinct.
