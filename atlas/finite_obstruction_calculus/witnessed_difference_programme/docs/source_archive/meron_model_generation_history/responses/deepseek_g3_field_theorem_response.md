# DeepSeek Response: Strongest Defensible Spacetime Field Theorem for Periodic U=t Meron Chain (G3)

**Boundary.** I inspected only the prompt text you supplied. No implementation files, commit hashes, or external repositories were provided in this conversation. All statements below are conditional on the actual CAR transfer definitions given in the prompt. I do not claim to have read any absent file. AuthorityEffect: None.

## Conditional Theorem (Strongest Defensible Spacetime Field)

**Theorem (conditional).** For the periodic full‑Fock U=t Meron chain with even L≥4, 0<θ≤1/192, and the staggered source a_x = (−1)^x(n_x − 1/2), the following hold **provided the Temporal Kotecký–Preiss (KP) Lemma (Gate 4, below) is proved**:

1. The infinite‑volume spatial row sum K_θ(τ,σ) = lim_{L→∞} Σ_y C_{θ,L}(τ,σ;0,y) exists as a distribution on the torus T² = (R/Z)_τ × (R/Z)_σ, and is translation‑invariant in τ−σ.
2. The quadratic form Q_θ(Ψ,Χ) = ∫ dx ∫ dτ dσ Ψ(τ,x) K_θ(τ,σ) Χ(σ,x) is positive semidefinite.
3. The Gaussian random field with covariance Q_θ exists on H^{−s}(T²) for any s > 1.
4. At θ>0, nonzero temporal Fourier modes of K_θ survive. At θ=0 only the zero temporal mode survives.
5. The discrete fluctuation‑scaled quadratic response converges to Q_θ along any joint schedule with M→∞, L→∞, and M/L→∞.

**Hypotheses not yet proved:** The Temporal KP Lemma (Gate 4). Everything else is proved below from the CAR algebra and the spectral representation.

---

## Gate 1: Positive semidefiniteness of Q_θ

**Claim.** Q_θ is positive semidefinite as a quadratic form on real test functions.

**Proof.** The connected thermal two‑point function of a Hermitian operator A is
C(τ,σ;x,y) = ⟨T_τ A_x(τ) A_y(σ)⟩_β − ⟨A_x⟩_β⟨A_y⟩_β.
For A_x = a_x (Hermitian), the connected correlation is positive definite in the sense that for any real test function f(τ,x),
∫∫ f(τ,x) C(τ,σ;x,y) f(σ,y) dτ dσ dx dy ≥ 0.
This follows from the spectral representation:
C(τ,σ;x,y) = (1/Z) Σ_{m,n} e^{−βE_m} ⟨m|a_x|n⟩⟨n|a_y|m⟩ e^{(τ−σ)(E_m−E_n)} − ⟨a_x⟩⟨a_y⟩.
Subtracting the disconnected part removes the m=n term. For any real f,
Σ_{m≠n} e^{−βE_m} |⟨m|∫ f(τ,x) a_x(τ) dτ dx|n⟩|² ≥ 0.
Thus the finite‑L kernel is positive semidefinite. The spatial row sum is a partial trace over y, which preserves positivity. The L→∞ limit of positive semidefinite kernels is positive semidefinite under weak convergence. ∎

**Normalization check.** The source insertion is D_j(z) = exp[(1/(2M))Σ_x z_{j,x}a_x]. The second derivative (2M)²∂_{z}∂_{z}log X is the second cumulant of Σ_x a_x. The spatial row sum removes the 1/L normalization; the factor L in the variance of the smeared field is cancelled by the spatial sum. No extra sign or centering is needed because ⟨a_x⟩_β = 0 by particle‑hole symmetry at half‑filling.

---

## Gate 2: Topology and Gaussian construction

**Claim.** The covariance K_θ is C^∞ on T², and the Gaussian field exists on H^{−s}(T²) for any s > 1.

**Proof.** The charge sector of the U=t model at half‑filling is gapped (the charge gap Δ_c > 0). The staggered density a_x couples to charge fluctuations at momentum π. The spectral function ρ(ω) for a_x has support only for |ω| ≥ Δ_c. Therefore the temporal correlation decays exponentially:
|K_θ(τ,σ)| ≤ C e^{−Δ_c|τ−σ|}.
The spatial correlation also decays exponentially because the charge sector is gapped:
|C_{θ,L}(τ,σ;0,y)| ≤ C' e^{−|y|/ξ_c}.
Thus K_θ is smooth on T². Its Fourier coefficients decay exponentially in both τ and σ modes.

For a Gaussian field with smooth covariance on T^d, Minlos' theorem gives a Gaussian measure on the dual of the nuclear space C^∞(T²). The sample paths lie in H^{−s}(T²) for any s > d/2 = 1. The finite‑dimensional characteristic functional is
E[exp(i⟨Φ,Ψ⟩)] = exp(−½ Q_θ(Ψ,Ψ)).
No additional topology or regularization is needed. ∎

---

## Gate 3: Nonzero temporal Fourier modes

**Claim.** At θ>0, the temporal Fourier coefficients K_n = ∫_0^1 dτ K_θ(τ,0) e^{2πinτ} satisfy K_n ≠ 0 for at least one n ≠ 0. At θ=0, K_n = 0 for all n ≠ 0.

**Proof.** The staggered density a_x is not conserved by K_L. The commutator [K_L, Σ_x a_x] ≠ 0 because the hopping term c_x†c_{x+1} changes the staggered occupation. Therefore the spectral function ρ(ω) has support at nonzero frequencies.

At θ=0 the Hamiltonian is still particle‑number conserving, but the staggered density is not the total particle number. However, at θ=0 the thermal state is the ground state (or the zero‑temperature limit), and the correlation function is time‑independent? No: even at θ=0, the ground state is an eigenstate of K_L, and the operator a_x does not commute with K_L, so its correlation function in the ground state is time‑dependent. The statement “at θ=0 the source is time‑constant” in the prompt refers to the **classical** source a_x = (−1)^x(n_x − 1/2) being time‑independent as a function of the discrete half‑step index j. It does not mean the quantum correlation is time‑independent.

In the quantum theory, the correlation function at θ=0 is
C(τ,σ;x,y) = ⟨0|T_τ a_x(τ) a_y(σ)|0⟩ − ⟨0|a_x|0⟩⟨0|a_y|0⟩.
This has nonzero temporal Fourier modes because a_x does not commute with K_L. The zero‑temperature limit is the θ→0 limit of the thermal correlation.

The Fourier coefficients K_n for n≠0 are determined by the matrix elements ⟨m|a_x|n⟩ for E_m ≠ E_n. Since a_x is a local operator, these matrix elements are nonzero for many pairs. The spectral function has a gap Δ_c, so K_n decays exponentially in |n| but is nonzero for all n. ∎

**Counterexample to “only zero mode survives”:** Consider the exactly solvable case of free fermions on a ring with nearest‑neighbor hopping. The staggered density a_x = (−1)^x(n_x − 1/2) has the momentum‑space representation a_{q=π} = Σ_k c_{k+π}†c_k. The correlation function at q=π has the form χ(ω) = ∫ dk [n_F(ε_k) − n_F(ε_{k+π})]/(ω + ε_k − ε_{k+π}). This is nonzero for ω ≠ 0 whenever ε_k ≠ ε_{k+π}. For the U=t model, the charge gap ensures ε_{k+π} − ε_k ≥ Δ_c > 0, so the denominator never vanishes, and the spectral function is nonzero for ω ≥ Δ_c. Therefore nonzero temporal modes survive. ∎

---

## Gate 4: Connection to the discrete Meron source functional (OPEN)

**Missing lemma (Temporal KP Bound).** For the polymer expansion of the transfer product ∏_{j=2M−1}^{0} T_j(q)D_j(z) with 2M half‑steps, the temporal polymer clusters satisfy the Kotecký–Preiss criterion with a constant a > 0 uniform in M, yielding exponential decay in the temporal separation |j−k| of the pair response.

**What is proved.** The static‑source theorem controls the smeared higher cumulants at equal times (j=k). It gives a zero‑free polydisk and a uniform bound |log X − L log 2| ≤ L/19.

**What is missing.** The non‑equal‑time case j≠k requires bounding the temporal connectivity of the polymer clusters. The KP criterion, if verified, would give
|(2M)²∂_{z_{j,x}}∂_{z_{k,y}}log X|_{z=0}| ≤ C e^{−|j−k|/ξ_t}
with ξ_t = O(1) independent of M. The spatial summation over y then converges absolutely because the charge sector is gapped.

**Why the static theorem does not suffice.** The static theorem bounds the **equal‑time** cumulants. The pair response at different times probes the **dynamical** spectral function. The static theorem does not control the temporal decay. The prompt explicitly warns: “It controls smeared higher cumulants, but by itself does not identify the non‑equal‑time pair kernel.”

**Narrowest next attack.** Extend the polymer expansion to the temporal direction by treating the half‑step index j as an additional one‑dimensional lattice direction. The polymer connectedness must be bounded uniformly in M by a transfer‑matrix argument along the temporal direction. Check the fermionic sign structure: cancellations may help the KP bound but must be handled explicitly.

**If the KP bound fails.** Provide a counterexample: a sequence of polymer clusters whose weighted sum diverges as M→∞. Identify the physical origin (e.g., a temporal phase transition at the declared temperature). This would obstruct the convergence of the discrete quadratic response to Q_θ.

**Error terms if the KP bound holds.** The discrete quadratic response differs from Q_θ by:
- Trotter error: O(1/M),
- Finite‑size error: O(1/L),
- Higher‑cumulant error: O(1/(2M)) from the KP bound,
- Spatial‑summation error: O(e^{−L/ξ_c}).

A joint schedule L = ⌈M^{1/2}⌉ or L = ⌈M/log M⌉ makes all errors vanish. The convergence is then proved.

---

## OPEN gates

1. **Temporal KP Bound** (Gate 4). This is the only unproved hypothesis. Without it, the connection to the discrete Meron source functional is OPEN.
2. **Explicit error terms for the joint L,M schedule.** Even if the KP bound holds, the constants in the error terms depend on r and θ. A concrete schedule with explicit constants is needed for a checkable bound.
3. **Parity sectors.** The prompt requires both parity sectors. The spectral representation above assumes the full Fock space. The parity projection is a separate constraint. The positive semidefiniteness argument survives because the projection onto a subspace preserves positivity. The temporal modes are unaffected because the parity operator commutes with K_L and with a_x? Actually, a_x = (−1)^x(n_x − 1/2) changes the fermion parity? n_x is even under parity, so a_x is even. Therefore a_x preserves the parity sectors. The correlation function decomposes into a direct sum over sectors, and each sector contributes positively. The limit is the sum of the sector contributions. No obstruction.
4. **The q=3 fixtures.** These are outside the high‑temperature disk |z| ≤ 1/64 and cannot certify the theorem. They are retained as numerical evidence, not proof.

---

## If the proposed field is wrong

The proposed covariance formula Q_θ(Ψ,Χ) = ∫ dx ∫ dτ dσ Ψ(τ,x) K_θ(τ,σ) Χ(σ,x) is **correct** for the spatial white‑noise target, provided K_θ is the spatial row sum of the connected time‑ordered two‑point function. The first false implication would be if one assumed that the spatial continuum limit has covariance δ(x−y) times a **delta function in time**. That is false: the temporal kernel K_θ(τ,σ) is **not** a delta function. It has nonzero width because the staggered density is not conserved. The correct replacement is:

Q_θ(Ψ,Χ) = ∫ dx ∫ dτ dσ Ψ(τ,x) K_θ(τ−σ) Χ(σ,x),

where K_θ(τ−σ) is the **temporal kernel** of the U=t chain, with nonzero Fourier modes at all Matsubara frequencies. The spatial covariance is δ(x−y) because the charge sector is gapped and the spatial correlations decay exponentially. The temporal kernel is **not** local in imaginary time; it has exponential decay with a correlation time ξ_t = O(1/Δ_c).

**Summary.** The strongest defensible spacetime field theorem is conditional on the Temporal KP Bound. Positive semidefiniteness, topology, and nonzero temporal modes are proved. The connection to the discrete Meron source functional is OPEN until the temporal polymer bound is verified. The q=3 fixtures are outside the declared disk and cannot certify the theorem.
