Status: AI-drafted, awaiting human review.

# Independent Derivation Note: `FSP-THETA-TERM-COMPLEX-WEIGHT` (`TFQ-1198` / `FSP-DERIV-034`)

AuthorityEffect: None.

## 1. What This Derivation Supports

1. **Lattice Chiral Index $Q_{\mathrm{top}} = n_+ - n_-$ and CP Antisymmetry**:
   For chiral zero-mode counts $n_+, n_- \in \mathbb{N}$ (matching `CdtTopologicalChargeEvaluator` in `code/python/src/fsp/cdt_topological_charge_evaluator.py`), the integer lattice topological charge $Q_{\mathrm{top}}(n_+, n_-) = n_+ - n_-$ is antisymmetric under chirality / CP reversal $Q_{\mathrm{top}}(n_-, n_+) = -Q_{\mathrm{top}}(n_+, n_-)$ and vanishes on balanced configurations $n_+ = n_-$ (`lattice_chiral_index_cp_antisymmetry`).
2. **Rational $\theta/\pi$ Divisibility Criterion and CP-Conjugate Pair Reduction**:
   For a rational vacuum angle $\theta = (p/q)\pi$ ($q > 0$), $\theta Q_{\mathrm{top}} \in \pi \mathbb{Z}$ holds if and only if $q \mid p \cdot Q_{\mathrm{top}}$ (`rational_pi_theta_real_weight_iff_divisible`), so generic $\theta \neq 0$ produces non-real Boltzmann phase factors $\exp(-i\theta Q_{\mathrm{top}})$. Combining CP-conjugate sectors $+Q$ and $-Q$ with equal gauge weight $w > 0$ cancels the imaginary sine components and leaves $2 w \cos(\theta Q)$ (`cp_conjugate_pair_cancels_imaginary_boltzmann_phase`), which becomes strictly negative whenever the cosine factor is negative ($c < 0$, e.g. $\pi/2 < |\theta Q| \le \pi$, `cp_conjugate_pair_negative_real_weight_at_obtuse_phase`).
3. **$\theta = \pi$ Parity Homomorphism, Two-Sector Cancellation, and Instanton Susceptibility**:
   At $\theta = \pi$, the real topological sign character $\sigma_\pi(Q) = (-1)^Q \in \{+1, -1\}$ is multiplicative under charge addition $\sigma_\pi(Q_1 + Q_2) = \sigma_\pi(Q_1)\sigma_\pi(Q_2)$ (`theta_pi_alternating_sector_sign_homomorphism`). In a two-sector ensemble ($Q = 0$ weight $w_0 > 0$, $|Q| = 1$ weight $w_1 > 0$), the signed partition sum satisfies $Z(\pi) = w_0 - w_1 < Z_{\mathrm{pq}} = w_0 + w_1$ (`two_sector_theta_pi_partition_cancellation_and_average_sign`, `su2_vortex_action_gap_sector_weight_ordering`), while in a CP-symmetric 3-sector ensemble $Q \in \{-1, 0, +1\}$, the mean charge vanishes and the second moment $\sum_Q Q^2 w_Q = 2 w_1 > 0$ is strictly positive (`topological_susceptibility_second_moment_positivity`).

## 2. What This Derivation Does Not Support (`GIN-C9` Scope Fences)

1. **Historical `GIN-C9` Fixture Fence**:
   As shown in `gin_c9_su2_action_gap_fixture_scope_fence`, the historical inequality `w0 != w0 + deltaS` for `deltaS > 0` in `su2_lattice_gauge.py` is elementary arithmetic on natural numbers and does not establish physical $SU(2)$ Yang-Mills confinement or $\theta = \pi$ phase transition theorems.
2. **Phenomenological Severity Fence (`IMPORTED_ASSUMPTION` Preserved)**:
   As shown in `theta_term_phenomenology_scope_fence`, the algebraic non-reality of $\exp(-i\theta Q_{\mathrm{top}})$ for $\theta Q_{\mathrm{top}} \notin \pi \mathbb{Z}$ and the finite two-sector cancellation identities do not determine the thermodynamic severity of the $\theta$-term sign problem in continuum gauge theories.

## 3. Narrowest Defensible Claim

For integer lattice topological charge $Q_{\mathrm{top}} = n_+ - n_-$, the Boltzmann phase $\exp(-i\theta Q_{\mathrm{top}})$ at $\theta = (p/q)\pi$ is non-real whenever $q \nmid p Q_{\mathrm{top}}$, CP-conjugate pairing reduces the weight to $2 w \cos(\theta Q_{\mathrm{top}})$ (which is negative for obtuse phases), $\theta = \pi$ induces the multiplicative parity sign $(-1)^{Q_{\mathrm{top}}}$ with $Z(\pi) = w_0 - w_1 < w_0 + w_1$, and the node remains `IMPORTED_ASSUMPTION` under `GIN-C9`.

## 4. Next Test Needed

Couple an explicit 2D/4D compact lattice gauge action with a geometric or overlap topological charge density and measure the scaling of the phase-quenched reweighting factor $\langle \cos(\theta Q_{\mathrm{top}}) \rangle_{\theta=0}$ across lattice volumes.
