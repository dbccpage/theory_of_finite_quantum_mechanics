# Change Log: The Dressing Field Method on Finite Graphs and Simplicial Complexes

## v0.2.1 (October 2026) — Review Remediation & Scope Alignment

- **Lean 4 & Code Parity Upgrades (`lean4/RaveraDfmFiniteToContinuum.lean`, `rust/ravera_dfm_finite_to_continuum.rs`, `code/ravera_dfm_dossier_replay.py`):**
  - Extended `lean4/RaveraDfmFiniteToContinuum.lean` to 16 zero-`sorry` theorems over `Rat`:
    * Added `spanning_tree_nonabelian_mat2_factorization` proving non-Abelian $2 \times 2$ matrix spanning-tree and chord reconstruction $U_{(x,y)} = g_x W_c g_y^{-1}$ with non-commuting link variables.
    * Added `sm_anomaly_polynomials_general_nc` proving the polynomial factorizations $6 A_{\mathrm{grav}}(N_c) = 6(N_c - 3)$ and $36 A_{Y^3}(N_c) = 9(N_c - 3)(N_c + 3)$ for arbitrary integer $N_c$.
    * Upgraded `su3_diagonal_klein_four_landau_gribov_copies` with the explicit negative Faddeev–Popov quadratic form witness `fp_hessian_plane (-1) (-1) = -2 < 0`.
  - Updated `code/ravera_dfm_dossier_replay.py` and `rust/ravera_dfm_finite_to_continuum.rs` to verify non-Abelian $2\times 2$ spanning-tree reconstruction across all 8 spanning trees of the diamond graph, general-$N_c$ anomaly polynomial factorizations, 3D Regge hinge angle defects alongside 2D boost-plane traces, and exact discrete Bianchi product boundaries.
- **Manuscript Corrections (`ravera_dfm_finite_to_continuum_dossier.md`):**
  - Repaired the tree-reconstruction formula in Theorem 3.1 ($g_x = U_{\gamma(r \to x)}^{-1}$ so $g_x U_e g_y^{-1} = 1_G$ on tree edges), the matrix/vector coboundary dimensions in Theorem 3.2, the general normal-subgroup factorization in Theorem 3.3, the symbolic continuum Feynman-parameter / Dirac-trace scope in Theorem 3.4, the single-step discrete shift scope in Theorem 3.5, and the 3D hinge vs. 4D simplicial Bianchi distinction in Theorem 3.9.

## v0.2.0 (October 2026)

- **Self-Contained Local Code & Formalization Bundle:**
  - Added standalone Lean 4 package under `lean4/` (`lean4/RaveraDfmFiniteToContinuum.lean`, `lean4/lakefile.lean`, `lean4/lean-toolchain`) with zero-sorry theorems over `Rat`.
  - Added local Rust verification module at `rust/ravera_dfm_finite_to_continuum.rs`.
  - Rewrote `code/ravera_dfm_dossier_replay.py` as a 100% self-contained exact-rational Python module (`fractions.Fraction`) implementing all nine pillars with zero external/parent imports.
  - Stripped all internal project codes and external repository paths from the manuscript and documentation so every citation references local package files.
- **Theorem 3.8 ($SU(3)_c$ Spanning-Tree Dressing vs. Discrete Landau Gribov Copies):**
  - Implemented and proved the exact comparison between non-Abelian $SU(3, \mathbb{Q}(i))$ spanning-tree dressing and the $4^{|V|-1} = 64$ anchored diagonal Klein 4-group Gribov copies in $SU(3, \mathbb{Q})$ satisfying $\partial^* A^g = 0$ with negative Faddeev–Popov Hessian eigenvalues outside the Gribov horizon.
- **Theorem 3.9 (Discrete Cartan–Regge Lorentz Frame/Tetrad Dressing Around Simplicial 2-Hinges over $\mathbb{Q}$):**
  - Implemented and proved local $SO^+(1,3;\mathbb{Q})$ invariance of the tetrad-dressed simplex metric $g_\sigma = e_\sigma^T \eta e_\sigma$ and affine connection $\Gamma_{\sigma\sigma'} = e_\sigma^{-1}\Omega_{\sigma\sigma'} e_{\sigma'}$, metric compatibility $\Gamma_{\sigma\sigma'}^T g_\sigma \Gamma_{\sigma\sigma'} = g_{\sigma'}$, substantial hinge deficit-boost holonomy ($\mathrm{Tr} = 16/3 \neq 4$ in 4D, $10/3 \neq 2$ in the 2D boost plane), and the non-Abelian discrete Bianchi identity around a closed 3-cell boundary.

## v0.1.0 (October 2026)

- Initial release covering Theorems 3.1 through 3.7 (Abelian spanning-tree dressing, Symanzik polynomials $U_G$ and $F_G$, two-stage Borel normal-subgroup dressing, dressed Dirac propagator and Clifford Ward–Takahashi identity $Z_1 = Z_2$, Page–Wootters relational clock dressing, electroweak $SU(2)_L \times U(1)_Y \to U(1)_{\mathrm{EM}}$ doublet dressing, and bipartite flavor graph $K_{N_g,N_g}$ CKM Jarlskog cycle holonomy).
