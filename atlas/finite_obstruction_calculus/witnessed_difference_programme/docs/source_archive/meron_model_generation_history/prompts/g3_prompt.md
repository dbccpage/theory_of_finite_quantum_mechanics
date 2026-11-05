# G3: Volume- and Time-Slice-Uniform Mixed-Cumulant Bound for Meron Chain

Work on G3 only: prove or refute a volume- and time-slice-uniform mixed-cumulant bound for the actual full-Fock periodic U=t Meron chain. Do not claim a spacetime limit.

For even L≥4, M≥1, q=1+r/M with 0≤r≤1/192, retain the periodic CAR hop signs, checkerboard transfer layers T_j, and a_x=(-1)^x(n_x-1/2). Use independent half-step sources
Z_{L,M}(z)=q^{-LM/4} Tr ∏_{j=2M-1}^{0}[T_j exp(Σ_x z_{j,x}a_x/(2M))].
The rightmost factor acts first. Its occupation expansion is the signed history sum with the source inserted before each layer. The existing finite checks are algebraic evidence, not a uniform estimate.

Target: exhibit explicit R_*>0 and C<∞ independent of L and M such that Z has a zero-free, consistently branched logarithm for all |z_{j,x}|≤R_* and |log Z(z)-log Z(0)|≤CL. Derive every model-specific premise of the polymer or alternative bound, including the wrapping CAR sign and dependence on independent time labels. Do not import the proved static-source bound as though it covered this polydisk.

Then set Φ_{L,M}(Ψ)=(2M√L)^{-1}Σ_{j,x} Ψ(j/2M,x/L)a_x(s_j). Derive an explicit bound on its mixed cumulants, especially κ_n=O(L^{1-n/2}) for n≥3 for bounded test profiles, uniformly in M. State precisely what your bound does and does not establish about second moments.

Acceptance: displayed definitions, constants and inequalities; a checkable derivation of the uniform bound; and the cumulant deduction. If any step fails, return OPEN with the first missing lemma or a counterexample. Do not claim G2, G4, G5, Gaussian convergence, or a positive probability law for finite signed histories.
