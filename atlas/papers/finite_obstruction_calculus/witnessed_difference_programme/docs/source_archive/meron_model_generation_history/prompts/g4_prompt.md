# G4: Continuous-Time Two-Point Function and High-Temperature Thermodynamic Limit

Solve G4 independently of Grok’s cumulant task. Use the actual full-Fock periodic U=t chain, not a free-field or spin-chain replacement. For even L≥4 let
P_x=(n_x+n_{x+1}-2n_xn_{x+1}+c_x†c_{x+1}+c_{x+1}†c_x)/2,
G_L=Σ_x P_x, a_x=(-1)^x(n_x-1/2), and
A_L(F)=L^{-1/2}Σ_x F(x/L)a_x.
Retain the periodic CAR boundary sign.

For τ≥σ in [0,1], start with the finite continuous-time ordered two-point function
C_{L,θ}(τ,σ;F,G)=
Tr[e^{(1-τ)θG_L} A_L(F) e^{(τ-σ)θG_L} A_L(G) e^{σθG_L}]
/Tr[e^{θG_L}],
with the insertion order reversed when σ>τ. Prove the one-point term vanishes or subtract it explicitly.

Target: identify and prove the L→∞ limit in the declared high-temperature region θ≤1/192 for Lipschitz F,G. A convergent linked-cluster series with a quantitative tail bound counts as an explicit kernel. Determine whether the limit is k_θ(τ-σ)∫F G, a two-sublattice kernel, or something else; do not assume its form. Prove or disprove positive semidefiniteness for real spacetime test functions and a strictly nonzero regime. Check that the double time integral reproduces the already derived static susceptibility χ(θ). Determine whether any nonzero temporal Fourier mode survives at θ>0.

A finite-L spectral formula alone does not close G4. If uniform spatial summability or the time-continuum passage cannot be proved, return OPEN with the exact missing estimate and the strongest finite theorem you can establish. Do not infer a Gaussian spacetime field or a joint (L,M) schedule.
