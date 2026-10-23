# Spacetime response of the periodic full-Fock U=t chain

Status: OPEN

Revision: 8b9e7d3704723a80f4927bd24375c55f0d63632e

## Carrier

The transport header binds the carrier, Hamiltonian, boundary condition, and query to the full-Fock periodic U=t chain of meron_time_and_volume_refinement.md, and it asserts no spatial scaling limit, no general Meron character theorem, and no new Lean credit.

Refinement §1 states that the source sums the full 2^L occupation basis, with even periodic L>=4, checkerboard repetitions M, and rational q>=1. On that carrier, y=x+1 mod L and

P_x=(1/2)(n_x+n_y-2 n_x n_y+c_x^* c_y+c_y^* c_x), H_L/t=sum_x(I/4-P_x).

Spatial SG-2 states: "The brackets are the original normalized signed SQL history sum. They are not reclassified as a probability law." Transport §1 states: "Taking two unrestricted spin traces doubles the carrier and loses the model." No free field, unrestricted spin trace, or complex Gaussian measure is substituted.

## Insertions that are written

Spatial §1 writes one repeated diagonal on the original transfers:

X_{L,M}(z)=q^{-LM/4} Tr[T_odd(q) D_z T_even(q) D_z]^M, D_z=exp[sum_x z_x a_x/(2M)], q=1+r/M.

Transport §3 writes one repeated insertion, F_{L,M}(lambda)=Tr prod_{t=K-1}^{0}(T_t e^{lambda A}), and states that the occupation expansion gives the signed history weight multiplied by exp(lambda Q), where Q=sum_t A(state_t).

Source-field §3 writes one D=v^{A_L} and states: "the original signed graph/orientation sum with weight v^Q equals this trace."

Analytic (AR-1) is one common z on every half step. The factor q^{-LM/4} is retained there. In a normalized ratio that scalar cancels. It remains in the partition. That cancellation is not a non-equal-time kernel.

A search of meron_spin_and_observable_transport.md, meron_analytic_response.md, meron_spatial_gaussian_source.md, and meron_source_field_response.md finds no D_j, no z_{j,x}, no phi_{L,M}(Psi), and no occurrence of the word cumulant.

The distinct half-step formula is absent as a displayed equation from those four notes. The finite identity below supplies it for every even L at least 2 and every integer M at least 1. It supplies no logarithm for independent labels, no modulus, no schedule, and no kernel on T×T. A continuum reading of z_{j,x}=u L^{-1/2} Psi(x/L, j/(2M)) remains outside this assignment.

Analytic §1 fixes the complex logarithm by continuation from zero coupling and zero source on the one-z curve. A proved logarithm for fully time-dependent labels is absent. Spatial §1 centers every real time-independent profile by c_x -> (-1)^x c_x^*, preserving every P_x and each transfer layer and reversing every a_x. Vanishing of an unequal-time bracket is not a separate written theorem. A particle-hole proof is absent from meron_analytic_response.md. Analytic §6 only invokes the name of that symmetry so that first derivatives vanish.

## Written disk

Analytic §1 states: "Declare 0<=theta<=1/192 and the complex-source radius R=1/64. These are sufficient constants from the proof below, not a maximal temperature range." It takes r>=rho>=0, r+rho<=1/192, and q=1+r/M. Spatial §1 uses the same Theta=1/192 and R=1/64 for time-independent z_x with every |z_x|<=R. That disk is not a proved time-dependent polydisk.

Analytic §7 states: "The familiar q=3,M=2 fixture has theta_hat=2 log 3 and lies outside this region. Its exact finite response remains valid; AR-9 supplies no continuum certificate for it."

## Objects that are not a spacetime kernel

Spatial §5 states that for any s>1/2 the expected negative-Sobolev squared norm is chi[1+2 sum_{n>=1}(1+n^2)^{-s}], finite, and "defines a Gaussian random distribution on H^{-s}(T). This explicitly constructs the static white-noise field target." The same section gives 1/8<=chi(theta)<=3/8 at theta<=2^{-20}, for chi(theta)=p''(theta,0) only.

Spatial §6 states: "A physical coupling renormalization, critical continuum limit, propagation law, nontrivial spacetime correlations, or interacting field action has not been derived."

Transport §4 displays (KO) as the integrated scalar K_L(theta) at fixed L. It states that (KT), for fixed L, bounded r, M tending to infinity and rho tending to zero, vanishes, and: "Its exponential-in-L bound does not close a growing-volume correlation limit."

Source-field §6 states: "A future import must still handle the actual parity-dependent periodic boundary and prove uniform imaginary-time connected-correlation control or another valid derivative argument. The one-bond pressure bound does not automatically control second derivatives." The same section says a spatial continuum profile needs an explicitly chosen convergence topology. That import is unmet and supplies no kernel bound.

Analytic §6 (AR-9) uses L=4k^4, M=L^2, epsilon=R/(4k) for the one-z intensive error |f_{L,M}''(0)-p''(theta,0)|. Spatial §4 reuses that schedule only for one time-independent F. No joint (L,M) schedule for time-dependent Psi is stated.

Kotecký–Preiss enters only as Fernandez–Procacci, arXiv:math-ph/0605041v2, equations (2.10), (2.14), and (2.15), with AR-2 through AR-5 as model premises (analytic §4). It is not a spacetime bound.

Spatial §2 states: "These are source-response kernels; finite signed time histories have not been assumed to have positive covariance matrices." The kernel there is kappa_{L,M}(x,y), the mixed derivative of log X_{L,M} at zero source. It is not a non-equal-time covariance on T×T.

If Psi(s,xi)=F(xi), the finite weight would reduce to the written static weight exp[u sqrt(a) Q_F/(2M)] of spatial §4. Any future continuum claim in that special case would still have to reproduce spatial §§4–5, from ell(u;F) to (1/2) u^2 chi(theta) integral_T F^2. That obligation constrains only the full time average of an unknown kernel. It is not itself a kernel.

## Where "register §14" is absent

genesis_bridge_register.md has no numbered §14. Its only section heading is "Selected closure of the Source-25 balance-edit question". GEN-WDP-14 in that file is the row "PROVED COUNTERMODELS" about AddTerm and Identify, not a Meron confinement. Chapter 14 of witnessed_difference_programme.md is "Self-reference and the awareness boundary".

Static confinement that is present sits in spatial §§4–6, GEN-WDP-33, GEN-WDP-34, monograph O.9, and cs_q_presentation_completion.md §13. That last section is headed "Circle completion now carries a static spatial source limit" and states that the construction does not "identify an interacting spacetime quantum field." GEN-WDP-34 names H^{-s}(T) for s>1/2 and the same static chi window, and says this is distinct from an interacting quantum field.

This is not the static spatial limit, a partition cancellation, or an assumed continuum remainder.

## Finite identity

This section is the G1 assignment. The packet status stays OPEN.

Let L be an even integer, L≥2, and let M be an integer, M≥1. Let q≥1. Write K=2M and number the half-steps by j=0,...,K-1. Let a_x=(-1)^x(n_x-1/2). For each half-step j and site x let z_{j,x} be an independent scalar, and set

$$
D_j=\exp\left(\sum_{x=0}^{L-1} z_{j,x} a_x/(2M)\right),
$$

diagonal in the occupation basis. Let T_j be the checkerboard layer of parity j mod 2: the product, in increasing starting site, of the local blocks I+(q-1)P_x. The hop sign in each block is the source sign. It is −1 exactly when the occupied modes strictly between the two endpoints have odd parity, read on the occupation that enters that bond.

The ordered product, with the rightmost factor acting first, is

$$
\Pi=T_{K-1} D_{K-1}\cdots T_1 D_1 T_0 D_0.
$$

Both sides carry the same factor q^{-LM/4}:

$$
q^{-LM/4}\operatorname{Tr}(\Pi)
=q^{-LM/4}\sum_{s_0,\ldots,s_{K-1}}
\prod_{j=0}^{K-1}
\langle s_{j+1}|T_j|s_j\rangle
\exp\left(\sum_{j,x} z_{j,x} a_x(s_j)/(2M)\right),
$$

where s_K=s_0 and the sum runs over the full 2^L occupation basis at every half-step. The bracket is the signed layer weight. The exponential is the source weight on the occupation before the layer, which is the occupation on which D_j acts.

### Insertion order

Transport §3 writes F_{L,M}(λ)=Tr ∏_{t=K-1}^{0}(T_t e^{λ A}), with an insertion before each layer. The product above is that order: D_0 acts first, then T_0, then D_1, then T_1. Specializing z_{j,x}=2M λ for every j and every x recovers e^{λ A} in every slot, because A=∑_x a_x. Then q^{-LM/4} Tr(Π)=q^{-LM/4} F_{L,M}(λ).

Spatial §1 repeats one diagonal, X_{L,M}(z)=q^{-LM/4} Tr[T_odd D_z T_even D_z]^M. That formula is the case in which every even half-step carries the same D_z and every odd half-step carries the same D_z. Independent values z_{j,x} remain independent until that repetition is imposed.

### Periodic fermion signs

Refinement §1 states that on each mixed two-mode sector, P_x has matrix [[1,s],[s,1]]/2, and that s is −1 precisely when the occupied modes strictly between the endpoints have odd parity. This includes the periodic bond. The local block I+(q-1)P_x therefore has diagonal (q+1)/2 on a mixed bond, off-diagonal s(q-1)/2, and weight 1 on an equal-occupation bond. Transport §3 records the same breakup: vertical weight 1, horizontal weight (q-1)/2 times the CAR sign, and mixed diagonal 1+(q-1)/2.

Adjacent bonds have an empty open interval, so their hop sign is +1 on every occupation. The wrap bond is (L-1, 0). It occurs on odd layers. Its sign is (−1) raised to the number of occupied modes in {1,...,L-2}. For L=2 that interval is empty, so the wrap sign is +1 on every occupation. A comparison that strips signs needs L≥4. The L=2 check in the finite note is an unscaled identity.

Refinement §1 states that disjoint even CAR polynomials commute, and that disjoint odd ones commute. Transport §3 states that disjoint interior hops preserve the number of spectators inside the periodic Jordan-Wigner string, so the sign computed from the before-layer occupation agrees with the multiplication order. The sequential sign on the state entering each bond is the sign on the layer-input occupation. Replacing every hop sign by +1 builds a different layer.

### The factor q^{-LM/4}

meron_transfer_trace returns the unscaled trace. Inside the SQL ceiling, the SQL signed partition is that same unscaled sum. The database metadata names the removed factor q^{-LM/4}. Refinement §1 removes that factor from Z_{L,M}(q) and restores it in the physical log-density as −M log(q)/4. The identity multiplies the trace and the history sum by this common factor. The factor is a common prefactor. Cancelling it in a ratio does not produce a time-dependent kernel.

When 4 divides LM and q is rational, the factor is rational. When 4 does not divide LM, the checker compares the two unscaled sides, and this statement keeps the common prefactor in front of both.

### Expansion

D_j is diagonal, so ⟨s_{j+1}|T_j D_j|s_j⟩=⟨s_{j+1}|T_j|s_j⟩ D_j(s_j), and D_j(s_j)=exp(∑_x z_{j,x} a_x(s_j)/(2M)). Expand Tr(Π) in the occupation basis. Each closed tuple (s_0,...,s_{K-1}) contributes the product of those matrix elements, and the trace retains the tuples with s_K=s_0. Multiplying by q^{-LM/4} gives the displayed equality.

At zero source every D_j is the identity. The unscaled trace then equals meron_transfer_trace(L,M,q) for every even L≥2 and every integer M≥1: both multiply the same bond blocks in the same site order. Inside the SQL ceiling L∈{4,6} and LM≤12, transport §3 identifies that trace with the original graph-and-orientation sum. On each zero-source row the finite note executes, the checker requires reconstruction in meron_summary, together with equality of signed_partition and meron_transfer_trace. Those executed rows do not exhaust the ceiling. The SQL constructor does not store z_{j,x}. The sourced weight is the occupation factor above.

The source notes state their later estimates for L≥4. The bond matchings used here are defined for every even L≥2.

### Two distinct times

Fix zero source, two half-steps j≠k, and two sites x and y. Insert the diagonal a_x into slot j and the diagonal a_y into slot k, and multiply by q^{-LM/4}. Call the result N_{j,x;k,y}(q). The same expansion gives

$$
N_{j,x;k,y}(q)
=q^{-LM/4}\sum_s W(s)\, a_x(s_j)\, a_y(s_k),
$$

where W(s)=∏_j ⟨s_{j+1}|T_j|s_j⟩. Differentiating the sourced partition once in z_{j,x} and once in z_{k,y} brings a_x(s_j)/(2M) from D_j and a_y(s_k)/(2M) from D_k. At zero source every exponential equals 1, so

$$
(2M)^2 \partial_{z_{j,x}}\partial_{z_{k,y}} Z(0) = N_{j,x;k,y}(q).
$$

This is a finite mixed numerator on one chain. A covariance kernel, a cumulant bound, and a limit remain separate assignments.

This is not the static spatial limit, a partition cancellation, or an assumed continuum remainder.

## Gate ledger

The spacetime limit remains open. The finite identity in the preceding section is the G1 assignment. G2, G3, G4, and G5 remain open.

- G1. The finite identity equates the ordered product to the signed occupation-history sum for every even L≥2, every integer M≥1, and independent half-step sources. The insertion order, the periodic hop signs, and the common factor q^{-LM/4} are pinned in that section. The two-time numerator is the corollary there. The four source notes still do not display the formula. The finite note records the exact checks. The identity is a finite chain equality. Topology, cumulants, the spacetime kernel, and the joint schedule remain open.
- G2. OPEN. No spacetime topology is identified. T×T is only the name of the withdrawn cylinder test domain. A negative-Sobolev index on that cylinder is absent. The only named negative-Sobolev space in these sources is the static H^{-s}(T), s>1/2. Transport §4 is fixed-L (KO). Source-field §6 leaves the convergence topology unmet. Analytic §7 stops at a fixed lattice. The time/volume target is the scalar f(theta), not a cylinder space.
- G3. OPEN. No uniform bound on mixed imaginary-time connected correlations, and no bound on cumulants of order greater than two, is written for distinct half-step labels. The word cumulant is absent from the four notes. Source-field §6 leaves that control as a future import. AR-3 and AR-8 control one repeated z. SG-5, SG-7, the static field, cancellation of q^{-LM/4}, and the finite insertion identity are different statements.
- G4. OPEN. No non-equal-time covariance kernel on T×T, and no positive nonzero regime for one, is written for the original signed SQL ensemble. Spatial §2 defines only kappa_{L,M}(x,y) and does not assume positive covariance matrices for finite signed histories. The window 1/8<=chi(theta)<=3/8 at theta<=2^{-20} bounds only chi(theta)=p''(theta,0). (KO) is a fixed-L integrated scalar.
- G5. OPEN. No joint (L,M) schedule for time-dependent Psi has a quantitative error tending to zero. The schedule candidate is absent. AR-9 and spatial §4 schedule one z and one time-independent F. Transport (KT) vanishes only at fixed L. A logarithm for independent half-step labels is absent, so there is no cumulant error to send to zero. SG-8, cancellation of q^{-LM/4}, and an assumed cylinder remainder are not this schedule.
- G6. The finite note records an in-disk rational fixture, a changed-source refusal, and a sign-stripped refusal for the finite identity. The four notes still do not name those refusals as a cylinder-kernel test. Transport §3 records that at L=4, M=2, q=3 the numerator 36864 gives 48/19 and the equal-time numerator 2384 gives 149/57, and states: "The time-integrated query cannot be replaced by an equal-time readout with the same name." meron_spin_and_observable.rs asserts second()==36864 and mean_square()==48/19. meron_observable_adapter.rs asserts partition 912 and second()==36864. The numerator 2384 is absent from both tests. The reading guides ask for an explanation of 2384/912=149/57 or of the 5/57 gap. That split remains a different statement from a cylinder falsifier. The finite checks do not close G2, G3, G4, or G5.
