# QM-217 Finite-Map Note: Exact Algebraic Bound-State Spectra ($\mathfrak{su}(2)$ Kravchuk Harmonic Oscillator & $\mathfrak{so}(4)$ Pauli–Runge–Lenz Hydrogen Spectrum)

## Scope and Three-Layer Decomposition

This note records the finite-to-continuum decomposition of canonical textbook bound-state spectra—the 1D harmonic oscillator and the 3D Coulomb / Hydrogen atom together with its $n = 2$ ($2S_{1/2}$ vs. $2P_{1/2}$) Lamb-shift degeneracy lifting (`QM-217`)—into:

1. **Exact Finite Algebraic Spine ($\mathbb{Q}$):**
   - **$\mathfrak{su}(2)$ Kravchuk Finite Harmonic Oscillator ($N = 2j \in \{1, 2, 3, 4\}$):** On the $(2j+1)$-dimensional binomial weight space $\mathbb{Q}^{2j+1}$ with rational ladder matrices $(J_+)_{n+1, n} = 2j - n$, $(J_-)_{n, n+1} = n + 1$, and $(J_z)_{n,n} = n - j$, the $\mathfrak{sl}(2, \mathbb{Q})$ commutation brackets
     $$[J_z, J_\pm] = \pm J_\pm, \qquad [J_+, J_-] = 2 J_z,$$
     the quadratic Casimir identity
     $$C_2 = J_z^2 + \frac{1}{2}(J_+ J_- + J_- J_+) = j(j+1) I_{2j+1},$$
     and $G$-metric adjointness
     $$J_+^{\mathsf{T}} G = G J_-, \qquad G = \operatorname{diag}\!\left(\binom{2j}{0}^{-1}, \binom{2j}{1}^{-1}, \dots, \binom{2j}{2j}^{-1}\right)$$
     hold over $\mathbb{Q}$ without square roots. Shifting $J_z$ produces the exact equidistant oscillator spectrum
     $$H_{\mathrm{osc}} = J_z + \left(j + \frac{1}{2}\right) I_{2j+1} = \operatorname{diag}\!\left(\frac{1}{2}, \frac{3}{2}, \dots, 2j + \frac{1}{2}\right)$$
     with adjacent level spacing $\Delta E_n = 1$. In the ground state $|0\rangle$, the scaled quadratures $Q = (J_+ + J_-)/(2\sqrt{2j})$ and $P = (J_+ - J_-)/(2i\sqrt{2j})$ have rational second moments $\langle Q^2 \rangle_0 = \langle P^2 \rangle_0 = \frac{1}{4}$ and saturate the discrete Robertson–Schrödinger uncertainty relation
     $$\langle Q^2 \rangle_0 \langle P^2 \rangle_0 = \frac{1}{16} = \frac{1}{4}\left|\left\langle \frac{J_z}{2j} \right\rangle_0\right|^2$$
     at every finite $N = 2j \ge 1$. Moreover, the discrete Kravchuk polynomials
     $$K_k(x; N) = \sum_{j=0}^k (-1)^j \binom{x}{j}\binom{N-x}{k-j} \in \mathbb{Z}$$
     satisfy exact binomial orthogonality
     $$\sum_{x=0}^N \binom{N}{x} K_k(x; N) K_{k'}(x; N) = 2^N \binom{N}{k} \delta_{k,k'}$$
     and the 3-term difference eigenvalue equation
     $$(N-x)K_k(x+1; N) - N K_k(x; N) + x K_k(x-1; N) = -2k\,K_k(x; N).$$
   - **$\mathfrak{so}(4) \cong \mathfrak{su}(2)_A \oplus \mathfrak{su}(2)_B$ Pauli–Runge–Lenz 3D Hydrogen Spectrum ($n \in \{1, 2, 3, 4\}$):** On the $n$-th bound-state shell $\mathcal{H}_n = V_j \otimes V_j$ with $n = 2j + 1$ ($\dim \mathcal{H}_n = n^2 \in \{1, 4, 9, 16\}$), the orbital angular momentum $\mathbf{L} = \mathbf{A} + \mathbf{B}$ and scaled Runge–Lenz vector $\mathbf{K} = \mathbf{A} - \mathbf{B}$ satisfy $[A_\alpha, B_\beta] = 0$, the $\mathfrak{so}(4)$ commutation relations
     $$[L_x, L_y] = -L_z, \qquad [L_x, K_y] = -K_z, \qquad [K_x, K_y] = -L_z,$$
     the Pauli orthogonality constraint
     $$\mathbf{L} \cdot \mathbf{K} = \mathbf{A}^2 - \mathbf{B}^2 = (j(j+1) - j(j+1)) I_{n^2} = 0$$
     (which fails on the asymmetric negative-control representation $V_{1/2} \otimes V_1$ where $\mathbf{L} \cdot \mathbf{K} = -\frac{5}{4} I_6 \neq 0$), and the $\mathfrak{so}(4)$ Casimir identity
     $$C_2(\mathfrak{so}_4) = \mathbf{L}^2 + \mathbf{K}^2 = 2(\mathbf{A}^2 + \mathbf{B}^2) = 4j(j+1) I_{n^2} = (n^2 - 1) I_{n^2}.$$
     Pauli's algebraic Hamiltonian therefore evaluates on $\mathcal{H}_n$ to the exact rational Balmer–Rydberg spectrum
     $$\frac{H_{\mathrm{H}}}{E_{\mathrm{Ryd}}} = -\bigl(C_2(\mathfrak{so}_4) + I_{n^2}\bigr)^{-1} = -\frac{1}{n^2} I_{n^2} \in \left\{-1, -\frac{1}{4}, -\frac{1}{9}, -\frac{1}{16}\right\}$$
     with Lyman-$\alpha$ jump $E_2 - E_1 = \frac{3}{4} E_{\mathrm{Ryd}}$, Balmer-$\alpha$ jump $E_3 - E_2 = \frac{5}{36} E_{\mathrm{Ryd}}$, and orbital angular-momentum trace
     $$\operatorname{tr}_{\mathcal{H}_n}(\mathbf{L}^2) = \sum_{l=0}^{n-1} (2l+1)l(l+1) = \frac{n^2(n^2-1)}{2} \in \{0, 6, 36, 120\}.$$
   - **$n = 2$ ($2S$ vs. $2P$) Projectors & Relativistic / Radiative Degeneracy Lifting:** On $\mathcal{H}_2 = V_{1/2} \otimes V_{1/2}$ ($\dim = 4$), the polynomial projectors
     $$\Pi_{2S} = I_4 - \frac{1}{2}\mathbf{L}^2 \quad (\operatorname{tr} = 1), \qquad \Pi_{2P} = \frac{1}{2}\mathbf{L}^2 \quad (\operatorname{tr} = 3)$$
     satisfy $\Pi_{2S}^2 = \Pi_{2S}$, $\Pi_{2P}^2 = \Pi_{2P}$, $\Pi_{2S}\Pi_{2P} = 0$, $\Pi_{2S} + \Pi_{2P} = I_4$, commute with orbital rotations $[\Pi_{2S}, L_\alpha] = 0$, and fail to commute with the Runge–Lenz ladder $[\Pi_{2S}, K_z] \neq 0$. The leading Dirac fine-structure coefficient
     $$C_{\mathrm{FS}}(n, j_{\mathrm{tot}}) = -\frac{1}{2n^3}\left(\frac{1}{j_{\mathrm{tot}} + 1/2} - \frac{3}{4n}\right)$$
     leaves $2S_{1/2}$ and $2P_{1/2}$ degenerate ($C_{\mathrm{FS}}(2, 1/2) = -\frac{5}{128}$ vs. $C_{\mathrm{FS}}(2, 3/2) = -\frac{1}{128}$, fine-structure splitting $\frac{1}{32}$), while the 1-loop QED radiative contact coefficient from `QM-216`,
     $$C_{\mathrm{contact}}(2S_{1/2} - 2P_{1/2}) = \left(\frac{19}{30} + \frac{1}{8}\right) - \left(-\frac{1}{5}\right) = \frac{67}{120},$$
     lifts the $2S_{1/2}$–$2P_{1/2}$ degeneracy by breaking the $\mathfrak{so}(4)$ Runge–Lenz symmetry.

2. **Certified Rational Interval Bridge (`RationalInterval` / `BigInterval`):**
   - Encloses $\pi \in [\frac{31415926535897932384626433}{10^{25}}, \frac{31415926535897932384626434}{10^{25}}]$ together with the gross Hydrogen Lyman-$\alpha$ transition frequency
     $$\nu_{\mathrm{Ly}\alpha}^{\mathrm{gross}} = \frac{3}{8}\,\alpha^2\,\frac{m_e c^2}{h} = 2467.381467264629\ldots\,\mathrm{THz}$$
     and the 1-loop non-logarithmic QED contact splitting between $2S_{1/2}$ and $2P_{1/2}$
     $$\Delta E_{\mathrm{contact}}(2S_{1/2} - 2P_{1/2}) = \frac{91}{120}\,\frac{\alpha^5}{\pi}\,\frac{m_e c^2}{h} = 617.179215588248\ldots\,\mathrm{MHz}$$
     to $12$ certified decimal places with interval width $< 10^{-14}$.

3. **Irreducible Continuum / External Import Boundary:**
   - The fine-structure constant $\alpha^{-1}$, the electron Compton frequency $m_e c^2 / h$, and the state-dependent relativistic Bethe logarithm $\ln k_0(n, l)$ remain declared external inputs.

## Verification Anchors

- **Python reference use case:** `sources/atlas/papers/finite_quantum_mechanics/python/finite_qm/use_cases/algebraic_bound_state_spectra_control.py` (`evaluate_algebraic_bound_state_spectra_control`)
- **Python e2e test suite:** `sources/atlas/papers/finite_quantum_mechanics/tests/e2e/test_e2e_algebraic_bound_state_spectra_control.py` (`6 passed`)
- **Rust compiled implementation & unit test:** `omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps/algebraic_bound_state_spectra.rs` (`evaluate_qm217_algebraic_bound_state_spectra`, `test_qm217_algebraic_bound_state_spectra_control`), re-exported from `quantum_import_finite_maps`
