# Fugu Prompt 4: Time-Resolved Spacetime Covariance Limit for Periodic U=t Meron Chain

Derive or rigorously obstruct a time-resolved spacetime covariance limit for the actual periodic U=t Meron chain. I need an infinite-family argument, not a finite numerical demonstration.

For even L≥4, use the full 2^L CAR Fock space, with y=x+1 modulo L,
P_x = 1/2(n_x+n_y−2n_x n_y+c_x†c_y+c_y†c_x),
K_L=H_L/t=Σ_x(1/4−P_x),
a_x=(−1)^x(n_x−1/2).
Keep the periodic hopping CAR sign and both parity sectors.

Let q=1+r/M, 0≤r≤1/192, and form the original alternating even/odd transfer product with 2M half-steps. Insert independent sources before the layers:
D_j(z)=exp[(1/(2M))Σ_x z_{j,x}a_x],
X_{L,M}(z)=q^(−LM/4) Tr ∏_{j=2M−1}^{0}[T_j(q)D_j(z)].
The rightmost factor acts first. Do not replace this with a sign-stripped, open-chain, or equal-time model.

A candidate polymer argument gives a zero-free polydisk |z_{j,x}|≤1/64 and |log X−L log 2|≤L/19 uniformly in L,M. Its 3ML factor labels have norm ≤1/(256M) and overlap degree ≤7M−1. Audit this claim; do not assume it merely because the static-source theorem holds. It controls smeared higher cumulants, but by itself does not identify the non-equal-time pair kernel.

Your target is:
1. Derive the exact source/history identity, including the q^(−LM/4) factor and periodic CAR signs.
2. Prove a spatially summable, M-uniform bound on the naturally rescaled pair response
   (2M)^2 ∂_{z_{j,x}}∂_{z_{k,y}} log X_{L,M}(z)|_{z=0},
   including coincident labels. State its dependence on periodic spatial distance.
3. Identify the corresponding infinite-volume, continuous-imaginary-time kernel of K_L, and prove convergence of the discrete pair response to it. Supply explicit error terms or another checkable bound that yields a concrete joint L,M schedule.
4. For fixed bounded Lipschitz spacetime test profiles Ψ, show convergence of the fluctuation-scaled quadratic response of
   Φ_{L,M}(Ψ)=(1/(2M√L))Σ_{j,x} Ψ(j/(2M),x/L)a_x(s_j).
   State precisely whether the spatial continuum limit has covariance δ(x−y) times a temporal kernel, and identify that kernel.

A valid solution must name every imported theorem and verify its hypotheses for this CAR transfer. It must distinguish the finite signed-history functional from a probability measure. The q=3 fixtures are outside the declared high-temperature disk and cannot certify this theorem.

If a step fails, return an OPEN result: give the exact missing lemma or a counterexample, preserve all proved bounds, and propose the narrowest next attack. Do not call a proposed topology, a finite script, or a source-free partition identity a spacetime limit.
