# Fugu Prompt 3: Strongest Defensible Spacetime Field Theorem for Periodic U=t Meron Chain

Investigate the strongest defensible spacetime field theorem for the same periodic full-Fock U=t Meron chain. Work independently of the proposed discrete covariance proof below; you may state a conditional theorem, but label every condition that remains unproved.

Use even L≥4,
P_x=1/2(n_x+n_{x+1}−2n_x n_{x+1}+c_x†c_{x+1}+c_{x+1}†c_x),
K_L=Σ_x(1/4−P_x), and a_x=(−1)^x(n_x−1/2),
with periodic CAR signs and both parity sectors. Take 0<θ≤1/192. In normalized imaginary time τ∈R/Z, define the thermal time-ordered connected correlation of
a_x(τ)=exp(τθK_L)a_x exp(−τθK_L).
The candidate temporal kernel is the even-L infinite-volume limit of the spatial row sum
K_θ(τ,σ)=lim_{L→∞} Σ_y C_{θ,L}(τ,σ;0,y),
where C is the connected time-ordered thermal two-point function. Do not assume this limit exists: prove it, make it an explicit hypothesis, or falsify it.

Target a precise Gaussian random-distribution construction on the completed spatial circle × imaginary-time circle. For test functions Ψ, the proposed covariance is
Q_θ(Ψ,Χ)=∫_{spatial circle} dx ∫dτ dσ Ψ(τ,x) K_θ(τ,σ) Χ(σ,x).
Determine whether this formula is correct for the actual staggered source and fluctuation scaling L^(−1/2).

Required gates:
1. Prove or refute positive semidefiniteness of Q_θ. A spectral/KMS representation is welcome, but track time ordering, centering, signs, and normalization explicitly. Positivity of a limiting Gaussian covariance does not imply positivity of the finite signed SQL histories.
2. Establish enough bounds to construct the Gaussian field in a named topology, such as H^(−s)(spatial circle × time circle) for a justified s. Show the Fourier or other construction and its finite-dimensional characteristic functional.
3. Determine whether any nonzero temporal Fourier mode survives at θ>0. At θ=0 the source is time-constant and only the zero temporal mode remains. Prove a positive-temperature nonzero-mode statement in an explicit range, or give a rigorous obstruction/counterexample.
4. Explain exactly which estimates would connect this Hamiltonian field to the discrete 2M-step Meron source functional along a joint L,M schedule. Do not assert that connection unless you prove its errors.

The existing static result constructs a spatial white-noise target for the time-averaged source in a high-temperature region. A candidate independent-time-source polymer bound would make connected orders ≥3 vanish under L^(−1/2) scaling, uniformly in M; audit rather than assume it. Your task is the missing covariance, positivity, topology, and temporal content—not a restatement of static Gaussianity.

Return a theorem with full hypotheses and proof, followed by a separate list of OPEN gates. If the proposed field is wrong, identify the first false implication and give the correct replacement. Finite computations may be checks, never the proof.
