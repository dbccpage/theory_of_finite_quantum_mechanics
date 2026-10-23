# WDP-APPW-EXTINCTION-POSITIVITY

Goal id: WDP-APPW-EXTINCTION-POSITIVITY

Selected scope for WDP-APPW-EXTINCTION-POSITIVITY is recorded in this note.

The plan statement is that an extinction or positivity claim that is not the one-point Trotter-response verification record stays open. This note records the finite constant-profile schedule that the locality checker stores, and it records why that schedule is not the open claim. No fresh Python replay, Lean kernel run, or congruence was executed for this note. The plan entry has an empty `depends_on` list and no fence on the reading.

## Selected scope

Finite carrier only: L=4 periodic CAR, Fock dimension 16, constant profile ψ_x(τ)=1, θ=1/10, bounds B=1 and D=0. Rational majorants E_4=(80/79)^32 and E_16=(20/19)^32. Margin m=79^32/(4·80^32). Numerator A=4·(30·(θ+θ^2)·E_16+2·θ·E_4). Recorded strict threshold M_0=415. Not the Gate E matrix at M=1, not other profiles, not L≠4, not positivity of G_M, and not a field-limit extinction theorem.

## Hypotheses

H1. Appendix W §1 fixes L=4 and the 16-dimensional Fock space, with a_x=(−1)^x(n_x−I/2), bond projections P_x, and H=Σ_x P_x. The response G_M has order LN=8M. The normalized quadratic is q_M(ψ)=ψ^T G_M ψ/(L N^2), with N=2M.

H2. For the constant profile, B=1 and D=0, so the T1 constant in W §4 specializes to A_θ=4·(30(θ+θ^2)e^{16θ}+2θ e^{4θ}). The same section gives ∥H∥≤4. No spatial quadrature is taken: the site index stays on these four sites.

H3. The rational schedule replaces e^{kθ} by E_k=(1−kθ/32)^{−32} for k∈{4,16}; W §5 also names k=8. W §5 invokes −log(1−u)≥u to get E_k≥e^{kθ} on 0≤θ≤1. That comparison is written in the monograph. It was not re-executed here.

H4. The same section gives Q_θ≥Tr(A^2)/(L Z)≥1/(4e^{4θ}) for ψ_x(τ)=1, using Tr(A^2)=16, L=4, thermal mean zero, and Z≤16e^{4θ}. The mean-zero step is the unitary cyclic site translation, which preserves H and sends A to −A. The second inequality is the dimension-16 bound coming from H≥0 and ∥H∥≤4. `tests/test_replay.py` asserts Tr(A^2)=16 and a real orthogonal u with u^T u=I, uHu^T=H, and uAu^T=−A. Those matrix assertions were read, not re-executed. The test does not evaluate the thermal expectation.

## Derivation

### 1. The rational majorant at θ=1/10

At θ=1/10, θ/8=1/80 and θ/2=1/20, so

E_4=(1−θ/8)^{−32}=(80/79)^32, E_16=(1−θ/2)^{−32}=(20/19)^32,

and m=1/(4 E_4)=79^32/(4·80^32). The code binds the same quantities: `exponential_envelope` returns (1−kθ/32)^{−32}, and `time_consistency_constant` at spatial length 4, amplitude 1, and derivative 0 returns 4·(30(θ+θ^2)E_16+2θ E_4). `replay.check` rebuilds that numerator as `a_bound` and the margin as `1/(4*e4)`, then requires the stored `time_limit` object to equal that recomputation.

`examples.json` stores `strict_M0` 415 and the positive margin

5297450670659957549009604563595170759963655420038456036451841 / 316912650057057350374175801344 followed by 32 zeros.

The prefix 316912650057057350374175801344 is 2^98, so the denominator is 2^98·10^32. Since 80^32=2^96·10^32, that denominator is 4·80^32. The stored numerator has 61 digits and ends in 51841. Successive squaring gives 79^2≡6241, 79^4≡50081, 79^8≡06561, 79^16≡46721, and 79^32≡51841 (mod 100000), and 32 log10(79) lies between 60 and 61, so 79^32 is a 61-digit integer with the same last five digits. The full numerator was not expanded by hand. Equality of the stored fraction with 79^32/(4·80^32) is what `replay.check` is written to require. That check was not run for this note.

`positive_threshold` and `replay.check` set M_0=max(1,⌊A/m⌋+1) and require M_0·m>A. The companion test also requires (M_0−1)·m≤A. That is an exact rational comparison on this labelled schedule. The product 415·m was not expanded by hand here. 415 is the recorded output of that floor formula.

### 2. What the written comparison gives on this profile

Under H2–H4, the monograph's comparison is |q_M−Q_θ|≤A_θ/M. Granting the written majorant E_k≥e^{kθ}, one has A_θ≤A and 1/(4e^{4θ})≥m, hence Q_θ≥m and |q_M−Q_θ|≤A/M. The recorded threshold then gives A/M<m≤Q_θ for every integer M≥415, and therefore q_M>0 for this constant profile only. The step E_k≥e^{kθ} remains written-only. Nothing here recomputes the CAR trace, the thermal covariance, or the product 415·m.

`TrotterObservableFiltering.lean` states `margin_positivity` for three rationals: if |approx−limit|≤err and err<limit, then approx>0. `uniform_envelope_positive` is the same lemma with err=numerator/time. The file header says these are finite certificate consequences, not Python, and that the analytic CAR product estimate and Lehmann positivity are written proofs. The lemma does not build this CAR trace.

The schedule is not the one-point Trotter-response verification record. For the constant profile the staggered compression of W §3 is a different object: a time-independent profile has mean zero against v_(j,x)=(−1)^j, so that one compressed channel vanishes exactly. W §3 says the rank-one bound does not prove positivity of the full q_M.

### 3. The one-point record is not this margin

W.8 copies, and does not rerun, the Gate E receipt: L=4, M=1, r=1/10, eigenvalue −1/706440, test vector (−1,−1,−1,−1,+1,+1,+1,+1), quadratic value −1/88305, and `is_positive_semidefinite` false. The point lies outside r≤1/192. The relation 8·(−1/706440)=−1/88305 is that record's Rayleigh identity, because 8·88305=706440. It is not reused as m, and the one-dimensional eigenvalue is not summed into an 8M-dimensional quadratic. `gate_e_exact_refutation.md` says the receipt does not record λ_min∼−r^4/9 and does not record indefiniteness for every finite M. `four_source_inventory.md` lists Gate G, mode extinction, as open and says not to rename the missing estimate.

The separate one-period evaluation λ_1(r)=−r^4/(4(r+2)(r^2+4r+8)) equals −1/87426958080 at r=1/192. Clearing the denominator gives 4(r+2)(r^2+4r+8)=455348740/192^3, and 192·455348740=87426958080. The value is negative, so the edge r=1/192 is not a positivity certificate. `test_replay.py` asserts the same rational value for the symbolic M=1 eigenvalue. That assertion was read, not re-executed. W §5 does not assign the constant-profile margin to other fields.

### 4. Why this does not close the open claim

W.8 says an extinction or positivity claim that is not the one-point record stays open. It names the unfinished model-response estimates: a uniform infinite-volume bound, a joint spacetime limit, and a general extinction or positivity claim. The rank-one bound |q_{v,M}|≤(E+E^2)D^2/(16M^2) is extinction of one compressed channel. T2 is Q_θ≥0 on the declared real sources for this fixed Hamiltonian. T3 is eventual strict positivity of q_M only after an independent margin is supplied, and the constant-profile lower bound is tied to ψ_x=1. GEN-WDP-57 records those fixed-carrier theorems and leaves joint spatial limits, Gaussianity, and all-M inertia separate. Reusing the one-point value, the rank-one bound, or T2/T3 does not supply the estimate W.8 says is missing.

M_0=415 is only the recorded constant-profile threshold at θ=1/10 and L=4. It does not prove positivity of G_M, extinction of every mode, any non-constant profile, or the W.8 field-limit obligation. A finite schedule does not establish a continuum limit, a physical law, or a closed theorem outside this scope.

## Claims this note does not make

- It does not close the W.8 obligation. An extinction or positivity claim other than the one-point Trotter-response verification record stays open.
- It does not claim positivity of the matrix G_M, extinction of every mode, or q_M>0 for any profile other than the constant profile ψ_x(τ)=1 at θ=1/10, L=4, B=1, D=0.
- It does not treat the recorded threshold 415 as a hand expansion of 415·m. It does not treat a run of `replay.check` as having been repeated here. It does not expand the stored 61-digit numerator beyond the terminal-digit check and the checker's written comparison.
- It does not re-prove E_k≥e^{kθ}. That comparison is the written use of −log(1−u)≥u. Without it, the exponential envelope A_θ is not identified with the rational numerator A.
- It does not treat `margin_positivity` as a construction of the CAR trace, the thermal covariance, or an infinite-M spectrum. It does not treat the sign-reversal test as an evaluation of the thermal mean.
- It does not reuse v^T G v=−1/88305, the eigenvalue −1/706440, or λ_1(1/192)=−1/87426958080 as the margin m. The edge r=1/192 is negative, so it is not a positivity certificate. The receipt does not record λ_min∼−r^4/9 or indefiniteness for every finite M.
- It does not treat the rank-one limit, T2, or T3 as Gate G, as Gaussianity, as a uniform infinite-volume bound, as a joint spacetime limit, or as a physical quantum reconstruction. It does not assign this margin to other fields, other temperatures, or other L.
- It does not claim a continuum limit, a physical law, or a closed theorem outside the selected scope.
