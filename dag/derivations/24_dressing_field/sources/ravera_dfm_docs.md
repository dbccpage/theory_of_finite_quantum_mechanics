# Ravera DFM Dossier Documentation & Metadata

## descriptions.md

# Descriptions: The Dressing Field Method on Finite Graphs and Simplicial Complexes

## Short Description

This monograph presents a self-contained nine-pillar finite-to-continuum realization of the Dressing Field Method (DFM) on finite combinatorial graphs, incidence posets, complete bipartite flavor graphs, and four-dimensional piecewise-flat Regge simplicial complexes over the rational numbers Q and Gaussian rationals Q(i). By constructing field-dependent dressing maps algebraically from spanning-tree holonomies, normal-subgroup decompositions, scalar doublets, and local tetrads, the package eliminates local gauge redundancy without differential gauge-fixing equations, Faddeev–Popov ghosts, or spontaneous symmetry breaking narratives, and bridges discrete cohomological invariants to certified rational interval enclosures for continuum quantum field theory observables.

## Pillar-by-Pillar Summary

1. **General Group Spanning-Tree / Chord Factorization and Abelian Symanzik Polynomials (Section 3.1):** For any group G on a finite connected graph Γ = (V, E), an anchored spanning tree T induces an explicit bijection U ↦ (g_T, {W_c}) between link configurations G^E and vertex coordinates on V ∖ {r} paired with dressed fundamental-cycle chord holonomies on E ∖ T (verified over Q and non-Abelian Mat_2(Q)). On the Abelian diamond graph (4 vertices, 5 edges, first Betti number b₁ = 2), residual ambiguity of the second kind under tree changes T → T' acts by unimodular integer matrices in GL(2, Z), preserving the first Symanzik spanning-tree polynomial U_G(α) across all 8 spanning trees and bracketing the imported 1-to-4-loop continuum QED electron anomalous magnetic moment series a_e to 12 decimal digits (0.001159652175).
2. **Non-Abelian Two-Stage Borel Normal-Subgroup Dressing (Section 3.2):** For any semidirect product G = N ⋊ H (exemplified by the upper-triangular Borel group B₂(Q) = N ⋊ T₂(Q)), sequential dressing first by the normal subgroup N and then by the residual quotient H factorizes the full spanning-tree dressing, separates artificial pure-gauge coboundaries from substantial non-Abelian cycle holonomy, and preserves the discrete Bianchi identity on a 2-plaquette prism.
3. **Spanning-Tree Momentum Routing and Zimmermann BPHZ Forest Subtraction (Section 3.3):** Spanning-tree dressing routes external vertex momenta uniquely along tree edges, decoupling the independent loop momenta and reproducing the second Symanzik 2-forest polynomial F_G(α; q, m²) identically across all 8 spanning trees and 10 spanning 2-forests of the diamond graph. Combined with Zimmermann's forest formula, nested and overlapping ultraviolet boundary poles cancel algebraically over Q in the symbolic Feynman-parameter model.
4. **Dressed Dirac Fermion Propagators and the Clifford Ward–Takahashi Identity (Section 3.4):** Pairing lattice spinors with their spanning-tree holonomy tails yields gauge-invariant two-point correlators across all spanning trees. In the 4×4 Clifford algebra Cl₁,₃(Q(i)), the continuum differential Ward–Takahashi identity ∂_μ S_F⁻¹(p) = γ_μ and explicit 4×4 matrix trace identities relate the 1-loop vertex and self-energy ultraviolet counterterms (Z₁ / Z₂ = 1).
5. **Relational Page–Wootters Clock Dressing on Static History Kernels (Section 3.5):** Treating the single-step discrete time-shift operator on a periodic clock-system tensor product as a gauge transformation, the conditional clock-dressing unitary intertwines the static Wheeler–DeWitt history operator (D† W D = (I_C − S_C) ⊗ I_S), so unitary step evolution emerges as a relational observable on the static constraint kernel.
6. **Electroweak SU(2)_L × U(1)_Y → U(1)_EM Doublet Dressing and General-N_c Anomaly Polynomials (Section 3.6):** Extracting the SU(2)_L dressing matrix algebraically from a non-vanishing scalar doublet Φ reduces Φ^u = (0, v)ᵀ, leaves the unbroken electric charge generator Q_EM = T₃ + Y/2 annihilating Φ^u, yields orthogonal rational Weinberg projectors with tree-level custodial ratio ρ_EW = 1, and proves that the one-generation Standard Model gravitational and cubic hypercharge anomaly polynomials 6(N_c − 3) and 9(N_c − 3)(N_c + 3) vanish for positive integer N_c if and only if N_c = 3.
7. **Complete Bipartite Flavor Graph CKM Rephasing Dressing and Jarlskog Cycle Holonomy (Section 3.7):** Quark-field phase redefinitions in U(1)_L^(N_g) × U(1)_R^(N_g) act as vertex coboundaries on the complete bipartite flavor graph K_{N_g,N_g}. Spanning-tree dressing removes 2N_g − 1 artificial phases and projects the CKM matrix onto b₁(K_{N_g,N_g}) = (N_g − 1)² fundamental 4-cycles (Jarlskog plaquettes), explaining why 2 generations have zero physical CP phases (J_CP = 0) whereas 3 generations carry a non-zero dressed cycle holonomy (J_CP = 5184/78125 on an exact Pythagorean SU(3, Q(i)) witness).
8. **Non-Abelian SU(3)_c Spanning-Tree Dressing vs. Discrete Landau Gauge Gribov Copies (Section 3.8):** On the diamond graph, the differential Landau gauge condition ∂* A^g = 0 admits 4^(|V|−1) = 64 anchored Gribov copies in the diagonal Klein 4-subgroup of SU(3, Q), which flip the Faddeev–Popov Hessian quadratic form from positive definite inside the Gribov horizon to indefinite/negative (witnessed by −2 < 0 on δθ = (−1, −1, 0)) outside the horizon. The algebraic spanning-tree dressing projector collapses all 64 Gribov copies to a single unique dressed configuration without Faddeev–Popov ghosts.
9. **Discrete Cartan–Regge Lorentz Tetrad Dressing Around Simplicial 2-Hinges (Section 3.9):** On a 4D piecewise-flat simplicial manifold over Q, the local tetrad e_σ ∈ GL(4, Q) dresses the internal Lorentz spin connection Ω_{σσ'} ∈ SO⁺(1, 3; Q) into the frame-invariant, metric-compatible affine connection Γ_{σσ'} = e_σ⁻¹ Ω_{σσ'} e_{σ'} (satisfying Γ_{σσ'}ᵀ g_σ Γ_{σσ'} = g_{σ'} for g_σ = e_σᵀ η e_σ), separates artificial frame rotations from substantial hinge holonomy (trace 16/3 ≠ 4 in 4D, 10/3 ≠ 2 in the 2D boost plane, and 3D rotational defect trace ≠ 3), and satisfies the non-Abelian discrete Bianchi identity around closed 3-cell boundaries.


## keywords.md

# Keywords

- Dressing Field Method (DFM)
- Finite Gauge Theory
- Artificial vs. Substantial Gauge Symmetry
- Spanning-Tree Cohomological Retraction
- Symanzik Graph Polynomials
- Algebraic BPHZ Forest Renormalization
- Dirac–Kulish–Faddeev Dressed Fermions
- Ward–Takahashi Identity
- Page–Wootters Relational Clock Dressing
- Electroweak Doublet Dressing
- Rational Weinberg Spectral Projectors
- Chiral Anomaly Cancellation
- CKM Bipartite Flavor Graph
- Jarlskog Rephasing Invariant
- Gribov Ambiguity and Gribov Horizon
- Discrete Landau Gauge vs. Spanning-Tree Dressing
- Cartan–Regge Simplicial Gravity
- Lorentz Tetrad Dressing and Hinge Holonomy
- Exact Rational and Cyclotomic Arithmetic
- Lean 4 Formal Verification


## references.md

# References

1. J. François, *Reduction of Gauge Symmetries: A New Geometrical Approach*, PhD Thesis, Aix-Marseille Université (2014).
2. C. Fournel, J. François, S. Lazzarini, and T. Masson, "Gauge invariant composite fields out of connections, with examples," *International Journal of Geometric Methods in Modern Physics* **11**(01), 1450016 (2014).
3. J. Attard, J. François, S. Lazzarini, and T. Masson, "The Dressing Field Method of Gauge Symmetry Reduction, a Review with Examples," in *Foundations of Mathematics and Physics One Century After Hilbert*, Springer (2018), pp. 377–415.
4. J. François, "Artificial versus Substantial Gauge Symmetries: A Criterion and an Application to the Electroweak Model," *Philosophy of Science* **86**(3), 472–496 (2019).
5. P. Berghofer, J. François, S. Friederich, H. Gomes, G. Hetzroni, A. Maas, and L. S.ag, *Gauge Symmetries, Symmetry Breaking, and Gauge-Invariant Approaches*, Cambridge University Press (2023).
6. J. François and L. Ravera, "Cartan geometry, supergravity and the dressing field method," *European Physical Journal C* **84** (2024).
7. L. Ravera and J. François, works on relational gauge symmetry reduction, Cartan connections, supersymmetric dressing, and boundary observables (2021–2025).
8. P. A. M. Dirac, "Gauge-invariant formulation of quantum electrodynamics," *Canadian Journal of Physics* **33**, 650–660 (1955).
9. P. P. Kulish and L. D. Faddeev, "Asymptotic conditions and infrared divergences in quantum electrodynamics," *Theoretical and Mathematical Physics* **4**, 745–757 (1970).
10. W. Zimmermann, "Convergence of Bogoliubov's method of renormalization in momentum space," *Communications in Mathematical Physics* **15**, 208–234 (1969).
11. D. N. Page and W. K. Wootters, "Evolution without evolution: Dynamics described by stationary observables," *Physical Review D* **27**, 2885 (1983).
12. S. Weinberg, "A Model of Leptons," *Physical Review Letters* **19**, 1264–1266 (1967).
13. M. Kobayashi and T. Maskawa, "CP-Violation in the Renormalizable Theory of Weak Interaction," *Progress of Theoretical Physics* **49**, 652–657 (1973).
14. C. Jarlskog, "Commutator of the quark mass matrices in the standard electroweak model and a measure of maximal CP nonconservation," *Physical Review Letters* **55**, 1039 (1985).
15. V. N. Gribov, "Quantization of non-Abelian gauge theories," *Nuclear Physics B* **139**(1–2), 1–19 (1978).
16. I. M. Singer, "Some remarks on the Gribov ambiguity," *Communications in Mathematical Physics* **60**(1), 7–12 (1978).
17. T. Regge, "General relativity without coordinates," *Il Nuovo Cimento* **19**(3), 558–571 (1961).


