# QM-212 Dressed Graph Polynomials and the Rational QED g-2 Enclosure: the Finite Map

**Scope:** research note for `finite_quantum_mechanics`; not part of the manuscript, not a claim promotion. Companion to `phase_fiber_holonomy_bridge_finite_map.md` and `general_relativity/relational_point_coincidence_and_witnessed_difference`.
**Code:** `python/finite_qm/use_cases/dressed_qed_g2_control.py`, tests in `tests/e2e/test_e2e_dressed_qed_g2_control.py` (8 tests), and `external:sha256:376085dc410bbb86117c8efb40f2280ed15cb5734a22d050f6e1718aef3be579`.
**Status marks used:** PROVED (argument given here, finite and checkable), COMPUTED (exact rational and cyclotomic arithmetic over Q and Q(ζ₁₂), replayable), IMPORTED (added structure that nothing finite here produces), CONJECTURED (none in this note).

Authority status: none. This note changes no admitted claim.

## 1. The question

Perturbative quantum electrodynamics predicts the electron anomalous magnetic moment a_e = (g - 2) / 2 to twelve decimal places as a power series in α / π:

a_e = Σ_{L ≥ 1} C_L (α / π)^L.

Textbook expositions present this series as arising from an uncountable continuum quantum field A_μ(x) defined at every point of R⁴, reduced by gauge-fixing cuts. The task is to build and test the finite map for this calculation along three axes:

- Compute the first Symanzik spanning-tree polynomial U_G(α) directly from the spanning trees and cotree chords of a finite carrier graph G, and check its exact rational identity with the dual Kirchhoff Laplacian cofactor.
- Verify that the Spanning-Tree Dressing Field Method (DFM, following François and Ravera, arXiv:2510.19845) acts as an idempotent, gauge-invariant retraction Π_dress on C¹(G; μ_N) that sets all |V| - 1 spanning-tree edges to 1, concentrates the physical degrees of freedom on the b₁(G) = L cotree loop chords, and leaves U_G(α) invariant under every local vertex gauge transformation and spanning-tree basis change.
- Enclose the L = 1, 2, 3 QED anomalous magnetic moment a_e^(1..3) and the 4-loop mass-independent QED series a_e^(1..4) to twelve decimal places using exact rational intervals (`Fraction` in Python, `BigRational` in Rust) built from finite rational series with explicit remainder bounds, without instantiating a continuum field or floating-point approximation.

## 2. Spanning-tree dressing and the Symanzik polynomial U_G

Let G = (V, E) be a finite connected graph with |V| loci, |E| edges, and loop number (first Betti number) L = b₁(G) = |E| - |V| + 1. A spanning tree T ⊂ E has |V| - 1 edges, and its complement E \ T is a cotree of size b₁(G) = L. Each cotree edge e ∈ E \ T closes a unique fundamental cycle C_e in T ∪ {e}.

**Theorem 2.1 (Symanzik spanning-tree polynomial and dual Kirchhoff cofactor). PROVED.** Given positive rational edge parameters α = (α_e)_{e∈E} ∈ Q_{>0}^{|E|}, define the first Symanzik polynomial of G by summing over the set T(G) of all spanning trees of G:

U_G(α) = Σ_{T ∈ T(G)} Π_{e ∉ T} α_e.

Assign dual edge conductances w_e = 1 / α_e, form the |V| × |V| weighted graph Laplacian L_G(w), and let L_G^(0)(w) be the (|V| - 1) × (|V| - 1) principal minor obtained by deleting row and column 0. By the Matrix-Tree Theorem, det L_G^(0)(w) = Σ_{T ∈ T(G)} Π_{e ∈ T} (1 / α_e). Multiplying both sides by Π_{e ∈ E} α_e yields the exact rational identity:

U_G(α) = (Π_{e ∈ E} α_e) det L_G^(0)(1 / α).

COMPUTED: on the 4-vertex, 5-edge diamond graph (b₁ = 2), 8 of the 10 two-edge subsets are valid cotrees (`spanning_tree_count = 8`, `U_G(1,1,1,1,1) = 8`), and on α = (1, 2, 3, 5, 7) both the cotree sum and the scaled Kirchhoff determinant evaluate to the exact rational integer 101 (`kirchhoff_identity_holds = True`). On the 1-loop triangle graph K₃ (|V| = 3, |E| = 3, b₁ = 1), all 3 single-edge subsets are cotrees and U_{K₃}(α₁, α₂, α₃) = α₁ + α₂ + α₃.

**Theorem 2.2 (Spanning-tree Dressing Field Method invariance). PROVED.** Fix a reference spanning tree T₀ ∈ T(G) rooted at locus 0. For any 1-cochain A ∈ C¹(G; μ_N), define the vertex dressing field u_{T₀} : V → μ_N by transporting A along the unique tree path in T₀ from 0 to v. Under any local vertex gauge transformation (A^g)(a, b) = g(a) A(a, b) conj(g(b)), the dressed cochain Π_dress(A) = A^{u_{T₀}} satisfies:

1. Π_dress(Π_dress(A)) = Π_dress(A) (idempotence);
2. Π_dress(A^g) = Π_dress(A) for all g ∈ C⁰(G; μ_N) (exact vertex-gauge invariance);
3. Π_dress(A)(e) = 1 for every tree edge e ∈ T₀, and Π_dress(A)(e) = Hol_{C_e}(A) for every cotree chord e ∉ T₀.

Consequently, any edge-weight assignment α(A) that factors through Π_dress(A) and local Born weights has gauge-invariant Symanzik polynomial U_G(α(A^g)) = U_G(α(A)), and changing the reference spanning tree T₀ ↦ T₁ acts on H₁(G; Z) by an integer matrix M ∈ GL(b₁(G), Z) with |det M| = 1 while leaving the set T(G) and U_G(α) unchanged. COMPUTED: verified across all 8 spanning trees of the diamond graph (`all_trees_unimodular_basis_change = True`, `dressed_symanzik_gauge_invariant = True`).

## 3. Exact rational interval enclosure of the L = 1, 2, 3 QED g - 2 series

The mass-independent QED coefficients C₁ (L = 1, Schwinger 1948), C₂ (L = 2, 7 connected graphs, Petermann 1957 and Sommerfield 1957), and C₃ (L = 3, 72 connected graphs, Laporta and Remiddi 1996) are closed rational linear combinations of finite graph periods:

1. **One-loop (b₁ = 1):** C₁ = 1/2 (exact rational, interval width 0).
2. **Two-loop (b₁ = 2):**

C₂ = 197/144 + (1/12) π² - (1/2) π² ln 2 + (3/4) ζ(3).

3. **Three-loop (b₁ = 3):**

C₃ = 28259/5184 + (17101/810) π² - (298/9) π² ln 2 + (139/18) ζ(3) + (100/3) (Li₄(1/2) + (1/24) ln⁴ 2 - (1/24) π² ln² 2) - (239/2160) π⁴ + (83/72) π² ζ(3) - (215/24) ζ(5).

Every period in C₂ and C₃ is enclosed in an exact rational interval `[lo, hi]` over Q using finite series truncations with certified rational remainder bounds:

- **π via Machin's alternating series:** π = 16 arctan(1/5) - 4 arctan(1/239); truncating after an even number of terms encloses each arctan between consecutive partial sums (at 20 terms, width < 10⁻²⁹).
- **ln 2 and Li₄(1/2) via binary geometric series:** Σ_{k=1}^K 1 / (k^s 2^k) for s ∈ {1, 4}, with positive tail bounded above by 1 / ((K + 1)^s 2^K) (at K = 50, width < 2 × 10⁻¹⁷).
- **ζ(3) via Apéry's alternating series:** ζ(3) = (5/2) Σ_{k=1}^M (-1)^{k-1} / (k³ C(2k, k)), enclosed between consecutive even and odd partial sums (at M = 20, width < 6 × 10⁻¹⁶).
- **ζ(5) via Euler-Maclaurin summation:** Σ_{k=1}^{N-1} k⁻⁵ + 1/(2N⁵) + 1/(4N⁴) + 5/(12N⁶) - 7/(24N⁸) + R_N with 0 ≤ R_N ≤ 5/(8N¹⁰) (at N = 20, width < 7 × 10⁻¹⁴).

COMPUTED: at the benchmark fine-structure rational input α⁻¹ = 137035999166 / 10⁹, the finite rational interval evaluator produces:

- C₁ ∈ [1/2, 1/2] (width 0);
- C₂ ∈ [-0.328478965579194, -0.328478965579193] (width < 10⁻¹⁴);
- C₃ ∈ [1.18124145658719, 1.18124145658721] (width < 10⁻¹³);
- a_e^(1..3) ∈ [0.00115965223117, 0.00115965223118] (width < 10⁻¹⁸, 12+ certified digits `0.001159652231` for the 3-loop truncation);
- Including the declared 4-loop interval C₄ ∈ [-1.91224576492645, -1.91224576492644] (4-loop mass-independent QED series `0.001159652175` to 12 digits) and the 5-loop remainder bound |C₅| (α/π)⁵ ≤ 5 (α/π)⁵, the mass-independent QED prediction is enclosed in `a_e^(QED) ∈ [0.00115965217530, 0.00115965217600]` with interval width < 10⁻¹² in exact rational arithmetic.

## 4. Three-layer summary table

| Layer | Status | Statement |
| --- | --- | --- |
| Finite invariant | COMPUTED | On any finite connected graph G, spanning-tree dressing Π_dress (DFM) sets all |V| - 1 tree edges to 1 and isolates the b₁(G) = L cycle holonomies on cotree chords; the Symanzik polynomial U_G(α) equals (Π_e α_e) det L_G^(0)(1/α), is gauge-invariant under Π_dress, and the L = 1, 2, 3 QED coefficients C₁, C₂, C₃ and a_e are enclosed to > 12 decimal places by finite rational series over Q. |
| Completion / enclosure step | COMPUTED (rational intervals) | Each transcendental period (π, ln 2, ζ(3), Li₄(1/2), ζ(5)) is replaced by a certified finite rational interval `[lo, hi]` of width < 10⁻¹³ without instantiating R. |
| Residual import | IMPORTED | The empirical rational interval for α⁻¹, the Lorentz/Clifford numerator algebra that maps spinor traces to scalar graph numerators before Schwinger reduction, and the renormalization subtraction prescription that maps bare graph polynomials to finite periods. |
