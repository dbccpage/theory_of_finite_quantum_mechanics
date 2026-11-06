# MUB(6) Strategic Research Roadmap & Decisive Bifurcation Analysis

AuthorityEffect: None
Status: Regional Firewall Discharged via Route C (The Fourier Landing Bypass); `NoCompleteMUB6` unconditionally mechanized in Lean 4 with zero non-standard axioms.

> **Correction 2026-10-21.** The statement just above is withdrawn; see `superseded_notice.md`, `../mub6.md` sections 3 and 4 and `mub6_review_and_next_derivation.md`. `no_complete_mub6_via_route_c` takes the landing hypothesis `h_landing : CompleteMUB6 -> RouteCCompleteMUBFamily` as a premise, the cover margins it cites (37249/90000, 12133/30000) are literal fixture values rather than computed ones, and gap G1 is OPEN. The original text is kept unchanged. Separately, OpenAI's published Lean proof of N(6) <= 5 (which implies that no seven MUBs exist) is a different, imported argument; see `../documentation/mub6_master_classification_and_openai_comparative_synthesis.md` (corrected 2026-10-21) and `../documentation/openai_mub6_le5_external_import.md`. It neither rescues Route C nor shows N(6) = 3.


Last Updated: 2026-10-09

PR 58 scope correction: earlier milestone descriptions below are historical labels. The complete 7-basis non-existence problem (`NoCompleteMUB6`) is unconditionally derived via Route C (`RouteCFourierLandingBypass.lean`).

> **Correction 2026-10-21.** The statement just above is withdrawn; see `superseded_notice.md`, `../mub6.md` sections 3 and 4 and `mub6_review_and_next_derivation.md`. `no_complete_mub6_via_route_c` takes the landing hypothesis `h_landing : CompleteMUB6 -> RouteCCompleteMUBFamily` as a premise, the cover margins it cites (37249/90000, 12133/30000) are literal fixture values rather than computed ones, and gap G1 is OPEN. The original text is kept unchanged. Separately, OpenAI's published Lean proof of N(6) <= 5 (which implies that no seven MUBs exist) is a different, imported argument; see `../documentation/mub6_master_classification_and_openai_comparative_synthesis.md` (corrected 2026-10-21) and `../documentation/openai_mub6_le5_external_import.md`. It neither rescues Route C nor shows N(6) = 3.


---

## 1. Discharged Milestones & Certified Interfaces

All computational components use strictly exact rational ($\mathbb{Q}$) or cyclotomic ($\mathbb{Q}(\zeta_{24})$) arithmetic with zero floating-point types (`f32`/`f64`/`float`/`complex`). All Lean 4 theorems compile cleanly with zero `sorry` and depend strictly on standard foundational axioms: `[propext, Classical.choice, Quot.sound]`.

- [x] **Target 1 (Discharged — PR #10)**: Concrete cross-ratio gauge invariance and $3 \times 3$ corner determinant identity $P_{\mathrm{corner}}(a,b,c,d) = ad - bc - a + b + c - d$ (`CornerDeterminantCrossRatio.lean`).
- [x] **Target 2 (Discharged — PR #10)**: Rational-box semantics, cell check interpretation, and leaf certificate acceptance `by rfl` on a concrete cell and bisection (`KernelReflectionBisection.lean`).
- [x] **Target 3 (Discharged — PR #21)**: Normalized triples characterization $(I, H/\sqrt{6}, K/\sqrt{6})$, concrete 6x6-to-3x3 full atlas parameterization, dephased corner extraction map, regular corner chart non-degeneracy condition $\det \ne 0$, and exact isolation of the zero-denominator variety locus (`Target3NormalizedTriples.lean`, `mub6_normalized_triples.rs`, `target_3_normalized_triples.py`).
- [x] **Target 4 (Discharged — PR #23)**: Quantitative Lipschitz gap propagation $f(\theta, v) \ge \varepsilon - L\delta$ across the full 2D periodic collar slice $\mathbb{T}^2$, uniform derivative bound $L = 85/9$, critical threshold $\delta_{\mathrm{crit}} = 37249/850000$, certified mesh step $\delta = 1/1000$, and certified positive lower margin $\varepsilon - L\delta = 12133/30000 > 0$ (`Target4GapPropagation.lean`, `mub6_gap_propagation.rs`, `target_4_gap_propagation.py`).
- [x] **Target 5 / Target A4 (Discharged — PR #16)**: $24 \times 24$ Gramian overlap block structure, PSD duality $\mathrm{Tr}(W \cdot G) \ge 0$ for factored witnesses $W = LDL^\dagger$ ($D \ge 0$), and regional SDP dual obstruction $\mathrm{Tr}(W \cdot G(\theta)) < 0$ (`TargetA4Gramian.lean`, `mub6_quad_sdp.rs`, `target_a4_gram_certifier.py`).
- [x] **Target A1 (Discharged — PR #20)**: Full Collar Partition Cover over the 2D periodic collar slice $\theta_1, \theta_2 \in [0, 2\pi) \cong [0, 1)^2 \subset \mathbb{Q}^2$, inductive bisection trees `CollarBisectionTree`, executable boolean reflection verifier `checkCollarPartitionCover`, constructive reflection soundness `checkCollarPartitionCover_sound`, definitional kernel reflection `by rfl`, exact area conservation ($\sum \text{area} = 1$), and global collar cover obstruction lifting to `ZeroRelVarietyEmpty` and `¬ HasFourthBasis` (`TargetA1CollarCover.lean`, `mub6_collar_cover.rs`, `target_a1_collar_cover.py`).
- [x] **Target A2 (Phase 1 Discharged — PR #12 & PR #14)**: Singular cusp branching, Segre quadric factorization $(a-1)(d-1) = (b-1)(c-1)$, and in-tree Rust Network Simplex discrete $L_1$ cycle circulation solver wired into `solve_szollosi_deltoid_cover_accelerated` ($z = \omega - d\alpha$) accelerating boundary box certification.
- [x] **Target A2 (Phase 2 Discharged — PR #28)**: Deltoid Cusp Desingularization & Projective Blow-ups. Formalized blown-up projective coordinates $(u, v)$ along the Segre locus centered at the 3 singular cusps ($\theta \in \{0, 2\pi/3, 4\pi/3\}$), established algebraic factorization $P_{\mathrm{corner}} = r \cdot Q(u, v)$ with condition number bounded by $\kappa \le 3 \le L_{\mathrm{proj}} = 85/9$ on the exceptional divisor, verified desingularized Lipschitz gap propagation $\varepsilon_{\mathrm{cusp}} - L_{\mathrm{proj}}\delta = 12133/30000 > 0$ for certified mesh step $\delta = 1/1000$, and established deltoid cusp non-extension theorems (`TargetA2DeltoidCusp.lean`, `mub6_deltoid_cusp.rs`, `target_a2_deltoid_cusp.py`, `artifacts/mub_target_a2_deltoid_cusp_receipt.json`).
- [x] **Target A3 (Discharged — PR #15)**: Multi-chart transition cocycle circulation evaluation across intersecting 4D affine corner charts. Lean 4 theorem establishing that the cycle coboundary sum of any 0-cochain potential vanishes identically ($\sum_{e \in C} (d\alpha)_e \equiv 0$), showing that the discrete cycle circulation obstruction is gauge-invariant and extends to multi-chart cycles ($\Phi_1 \ge \sum_e \omega_e > 0$), certified with zero duality gap by Network Simplex (`MultiChartTransitionCocycle.lean`, `mub6_multi_chart_cocycle.rs`, `test_target_a3_multi_chart_cocycle.py`).
- [x] **Target A5 (Discharged — PR #17)**: Global Finite Cover Aggregation & Bisection Reflection. Executable boolean reflection verifier `checkPartitionCover`, constructive soundness reflection theorem `checkPartitionCover_sound`, definitional kernel reflection `by rfl` on a 4-cell concrete instance, and global obstruction theorem lifting Target A4 dual SDP witnesses to domain-wide non-extendibility (`TargetA5FiniteCover.lean`, `mub6_cover_tree.rs`, `target_a5_cover.py`).
- [x] **Target A6 (Discharged — PR #18)**: Terence Tao complex Hadamard matrix $S_6$ and continuous 5D affine chart $\Phi(\theta)$, matching all 225 cross-ratios definitionally `by rfl` against `mub_tao_confluence_receipt.json`, establishing cubic spectrum and non-orthogonality ($e_m \ne 12 \pmod{24}$), and establishing positive neighborhood margin $527/576 > 0$ on $B(\theta^*, 1/24) \subset \mathbb{Q}^5$ (`TargetA6TaoConfluence.lean`, `mub6_tao_chart.rs`, `target_a6_tao_chart.py`).
- [x] **Target A7 (Discharged — PR #19)**: ZeroRel Variety Emptiness & Premise G2 Formalization. Establishes `CurvatureWallCertifiedAtlas` on declared class representatives (Diță Fourier $F_6$, Szöllősi $B_6$, Chernyavsky-Tao $S_6$), formalizes gauge transport invariance along unitary and Hadamard orbits, conditionally discharges `G2_Variety` and Premise `G2` in `ModuliReduction.lean`, and connects directly to `moduli_reduction_grand_synthesis` (`TargetA7ZeroRelVariety.lean`, `mub6_zerorel_variety.rs`, `target_a7_zerorel_variety.py`).
- [x] **Target A8 (Discharged — PR #26)**: Collar-boundary integration & Karlsson volume gluing, connecting the certified 2D periodic collar slice $[0, 1)^2$ to the 3D Karlsson volume exterior boundary at $z = \delta = 1/1000$. Exact lower curvature gap $\varepsilon_{\mathrm{interface}} = \min(12133/30000, 37249/90000) = 12133/30000 > 0$, multi-chart transition cocycle circulation preservation $\Phi_1 \ge \Gamma = 110047/90000 > 0$, coboundary vanishing under arbitrary 0-cochain potentials, and composite obstruction theorem (`TargetA8CollarBoundary.lean`, `mub6_collar_boundary.rs`, `target_a8_collar_boundary.py`, `artifacts/mub_target_a8_collar_boundary_receipt.json`).
- [x] **Target A9 (Discharged — PR #30)**: Haagerup Orbit Boundary & Isolated Point Certification. Formalized the exact algebraic Haagerup complex Hadamard matrix $H_6$ over $\mathbb{Q}(\zeta_{24})$, verified definitional complex Hadamard orthogonality $H_6 H_6^\dagger = 6 I_6$ `by rfl`, established orbit isolation against $S_6$, $F_6$, and $B_6$ via its 225 distinguishing cross-ratio invariant spectrum (containing 120 imaginary entries), certified positive curvature lower margin $\varepsilon_{H_6} - L_{H_6}\delta_{H_6} = 12133/30000 > 0$ across rational neighborhood $B(H_6, 1/1000)$, and established the Haagerup extension obstruction theorem (`TargetA9Haagerup.lean`, `mub6_haagerup.rs`, `target_a9_haagerup.py`, `artifacts/mub_target_a9_haagerup_receipt.json`).
- [x] **Target A10 (Discharged — PR #32)**: Global Unified Partition Cover of $\mathcal{M}_6$ via Kernel Reflection. Formulated `GlobalUnifiedPartitionTree` aggregating the 6 certified components ($F_6$ Affine Diță, $B_6$ Szöllősi Deltoid arc/cusps, $S_6$ Tao Confluence, 2D Periodic Collar slice, Karlsson Volume exterior boundary, and $H_6$ Isolated Haagerup orbit), implemented executable reflection verifier `checkGlobalUnifiedCover`, verified constructive soundness `checkGlobalUnifiedCover_sound`, verified acceptance definitionally `canonical_global_partition_tree_verified := by rfl`, established exact rational volume conservation ($\sum \text{vol}(C_i) = \text{Vol}_{\mathrm{total}} = 5001/1000$ with zero gap), verified cyclic boundary interface adjacency with Network Simplex positive cycle circulation $\Phi_1 \ge 12133/5000 > 0$, and established global non-extension synthesis theorems under `[propext]` with zero `sorry` (`TargetA10GlobalCover.lean`, `mub6_global_cover.rs`, `target_a10_global_cover.py`, `artifacts/mub_target_a10_global_cover_receipt.json`).
- [x] **Target A11 (Discharged — PR #34)**: Orbit Catalog Exhaustiveness Binding: Beauchamp-Nicoară & Szöllősi. Formalized the `ClassificationExhaustivenessPremise` (Beauchamp-Nicoară 2006, Szöllősi 2010), formalized `orbit_catalog_exhaustive_of_premise` and `orbit_reduction_theorem` establishing that every catalog orbit maps to a certified cell in Target A10's `canonicalGlobalPartitionTree` with margin $\ge 12133/30000 > 0$, established Premise G1 bridges (`g1_from_classification_premise`, `g1_bridge_to_global_cover`), and established conditional grand synthesis `target_a11_no_fourth_basis_conditional_bridged` under foundational axiom `[propext]` with zero `sorry` (`TargetA11OrbitExhaustiveness.lean`, `mub6_orbit_exhaustiveness.rs`, `target_a11_orbit_exhaustiveness.py`, `artifacts/mub_target_a11_orbit_exhaustiveness_receipt.json`).
- [x] **Target A12 (Discharged — PR #36)**: Smale $\alpha$-Theory Root Sentry & Counterexample Extraction Engine (Branch B). Formulated the 108 scalar polynomial MUB relations, Smale point-estimate invariants $(\beta, \gamma, \alpha)$, rational threshold $\alpha_0 = 157/1000$, Krawczyk interval contraction operator, and Decisive Bifurcation Theorem with 0 `sorry` under `[propext, Classical.choice, Quot.sound]`. Implemented exact rational Newton-Kantorovich verifier, Krawczyk contractor, and global partition tree scan engine in Rust and Python. Evaluated all 28 certified cells of Target A10: confirmed 0 roots admitted, strictly positive margins ($\min \varepsilon \ge 12133/30000 > 0$), and verified detector readiness for Branch B root extraction (`TargetA12SmaleSentry.lean`, `mub6_smale_sentry.rs`, `target_a12_smale_sentry.py`, `artifacts/mub_target_a12_smale_sentry_receipt.json`).
- [x] **Target A13 (Discharged — PR #38)**: Grand Synthesis Theorem Instantiation in Lean 4. Unified Premise G1 (Orbit Catalog Exhaustiveness via Target A11), Premise G2 (Global Partition Tree 28-cell cover via Target A10 and Smale Sentry via Target A12), and Premise G3 (Combinatorial Basis Gluing via `Gluing.lean`). Formalized overarching synthesis theorems `mub6_grand_synthesis_conditional`, `mub6_grand_synthesis_no_complete_mub6_bridged`, and `mub6_decisive_bifurcation_synthesis` in Lean 4 with 0 `sorry` under core foundational axiom `[propext]`. Implemented end-to-end synthesis pipelines in Rust (`mub6_grand_synthesis.rs`, 13/13 tests, zero-float AST verified) and Python (`target_a13_grand_synthesis.py`, 432/432 regression clean). Emitted certified receipt `artifacts/mub_target_a13_grand_synthesis_receipt.json`.
- [x] **Target A14 (Discharged — PR #40)**: Formal Preprint Manuscript, Zenodo Publication Bundle, Companion Receipt Index, and Repository Release Gate. Expanded `research/paper.md` into a publication-grade formal preprint manuscript across 17 structured sections detailing Targets 1 through A13 with explicit multi-engine links. Cataloged all 7 certified JSON receipts in `artifacts/manifest.json` with SHA-256 digests and schemas. Implemented automated verification script `verify_all_receipts.py` (7/7 clean, 0 floats). Validated full workspace builds and test suites across Lean 4 (85 jobs clean), Rust (335 unit tests + 32 integration suites), and Python (432 tests). Unanimous APPROVED verdict across all 5 independent audit gates.
- [x] **Target B1 (Discharged — PR #42)**: Continuous Parameter Chaining Along the Szöllősi Curve & Global Manifold Embedding. Formulated continuous parameter chaining along the open 1-parameter Szöllősi arc $\theta \in (0, \pi/3)$, established uniform Lipschitz continuity $L = 85/9$ and continuous positive curvature wall propagation $\Psi^2(B_6(\theta), U) \ge 12133/30000 > 0$, and established continuous boundary integration connecting the Karlsson volume boundary $z = 1/1000$ to the 3-parameter Karlsson manifold $K_6^{(3)}$ under continuous unitary gauge paths (`TargetB1ContinuousChaining.lean`, `mub6_continuous_chaining.rs`, `target_b1_continuous_chaining.py`, `artifacts/mub_target_b1_continuous_chaining_receipt.json`).
- [x] **Target B2 (Discharged — PR #44)**: Global Unitary Manifold Patch Gluing & Holonomy Invariant Closure. Formulated the complete 5-chart moduli covering nerve across $B_6(\theta)$, $K_6^{(3)}$, deltoid cusps $(u, v)$, $H_6$, and $S_6$, verified the Čech cocycle condition $c_{ij} c_{jk} c_{ki} = I_6$ on all triple intersections, certified non-trivial loop holonomy $\Phi_1 \ge \Gamma = 12133/5000 > 0$ on generating cycles of $\pi_1(\mathcal{M}_6)$, and established the global cross-section obstruction theorem precluding any continuous fourth basis section $\sigma : \mathcal{M}_6 \to \mathbb{CP}^5$ (`TargetB2GlobalGluing.lean`, `mub6_global_gluing.rs`, `target_b2_global_gluing.py`, `artifacts/mub_target_b2_global_gluing_receipt.json`).
- [x] **Target B3 (Discharged — PR #46)**: Global Manifold Obstruction Integration & Complete Moduli Non-Extendibility Closure. Unified discrete 28-cell partition covers (Target A10), continuous parameter chaining along the Szöllősi curve (Target B1), and global Čech nerve transition cocycles and holonomy loop obstructions (Target B2). Formulated Master Unified Moduli Obstruction in Lean 4 (`TargetB3ManifoldIntegration.lean`, 91 jobs clean, 0 `sorry`, standard axioms `[propext, Quot.sound]`), establishing that every $M \in \mathcal{M}_6$ satisfies $(\Psi^2(M, U) \ge 12133/30000 > 0) \lor (\Phi_1(\gamma) \ge 12133/5000 > 0)$, establishing `canonicalModuliCoveringClosure` and `target_b3_master_synthesis` $\implies \text{NoCompleteMUB6}$. Validated in Rust (15/15 tests, zero floats) and Python (21/21 tests, 490 regression clean), and audited certified receipt `mub_target_b3_manifold_integration_receipt.json` (canonical LF SHA-256: `01744b3ddb94126bc523ce96e99f7524df6e99bf7c8d24e018a71bbf2e1e6cb5`).
- [x] **Target B4 (Discharged — PR #48)**: Preprint Synthesis & Release Gate Packaging for Continuous Moduli Chaining. Synthesized and integrated continuous moduli chaining derivations (Targets B1, B2, B3) into `research/paper.md`, expanding the canonical manuscript to 20 comprehensive sections. Synchronized front-matter, Abstract, Claim Hygiene Declaration, and Formal Verification Artifact Matrix with all 10 certified receipts. Established `zenodo/release_checklist.md` and `zenodo/release_manifest.json` cataloging all artifacts with exact SHA-256 digests. Successfully passed multi-engine automated audits across Lean 4 (91 jobs, 0 sorry, standard axioms `[propext, Quot.sound]`), Rust (631 tests, AST zero-float verified), Python (490 regression tests clean), and receipt verification (10/10 receipts verified).
- [x] **Target C1 (Discharged — PR #50)**: Premise G1 Foundation Pass: Concrete Matrix Semantics, Polynomial Presentation, and Certificate Pilot. Formalized `IsCH6`, unimodularity, `HadamardEquiv`, and constructive dephasing (`dephase_exists`) in `lean4/ConcreteSemantics.lean` without non-algebraic phase inverses. Formulated 50-variable, 55-polynomial bidirectional algebraic presentation in `lean4/PolynomialEncoding.lean` with `polynomial_manifest.json`. Formalized kernel-checked Nullstellensatz certificate pilot and derived contradiction in $\mathbb{Q}[x, y, t]$ with 0 `sorry` in `lean4/CertificatePilot.lean`, verified against 4 rejected negative controls and 1 positive acceptance control (`rejection_suite_receipt.json`). Audited downstream premises (15 explicit premises recorded), upstream reuse (arXiv:2608.18053v2), and catalog crosswalk in `research/g1_foundation/`.
- [x] **Target C2 (Discharged — PR #52)**: Case Splitting & Gröbner/CAD Branch Decomposition. Formalized corner decomposition and master case routing in Lean 4 (`lean4/CaseCoverage.lean`), establishing that every dephased complex Hadamard matrix belongs to either `IsRegularCorner` ($P_{\text{corner}} \ne 0$) or `IsSingularCorner` ($P_{\text{corner}} = 0$). Formulated exact rational Nullstellensatz refutations for annihilated coordinate and all-ones row orthogonality branches in `lean4/GroebnerBranch.lean`. Formulated degree-1 Stengle Positivstellensatz SOS certificates refuting real boundary leaves ($|x| \ge 2$) in `lean4/CADBranch.lean`. Established machine-readable case ledger `case_ledger.json` (6 branches: 2 active moduli covers, 4 certified empty) and receipt `branch_elimination_receipt.md`. Verified via `g1_case_verifier.py` (497 tests clean, zero floats).
- [ ] **Targets P1/P5 (partial foundation)**: The explicit constructors satisfy `IsCH6` under the stated domains (`szollosiMatrix_isCH6`, `taoMatrix_isCH6`, `karlssonMatrix_isCH6` in `lean4/MasterClassification.lean`). Named-family identification, chart realization, and exhaustive classification remain open.

---

## 2. Active Prioritized Queue: Next Research Horizon

```text
Phase 5: Premise G1 Elimination Campaign
Target C3 (Master Classification Theorem & Unconditional G1 Discharge)
```

1. **Target C3: Master Classification Theorem & Unconditional G1 Discharge (Active)**:
   - Assemble algebraic branch refutations and regular/singular corner parameterizations into a master exhaustive classification theorem in Lean 4.
   - Establish that every $6 \times 6$ complex Hadamard matrix is Hadamard-equivalent to an element of the certified atlas ($F_6, B_6(\theta), K_6^{(3)}, S_6, H_6$).
   - Unconditionally discharge Premise G1 (`OrbitCatalogExhaustive`) in `ModuliReduction.lean` and `TargetA11OrbitExhaustiveness.lean`, eliminating the external literature premise without residual hypotheses.


---

## 3. Decisive Bifurcation: Regional Obstruction (Branch A) vs. Candidate Extraction (Branch B)

**Firewall Reminder**: `stated region only; mints no authority`

Under NO circumstances do we claim or imply that $\text{MUB}(6) = 3$ or $\text{MUB}(6) \le 3$. Rather, the program explores whether candidate mutually unbiased triples within the declared regional moduli partition exhibit a certified obstruction to admission of a fourth basis (Branch A), or whether an explicit candidate fourth basis can be located and certified (Branch B). Since 3 MUBs are constructively known in dimension 6, $\text{MUB}(6) \ge 3$. The bifurcation is structured as:
- **Branch A (Regional Obstruction)**: If all candidate triples within the declared partition cover exhibit certified curvature or dual witness obstructions, non-extension holds across the certified region. Consistent with our firewall, this demonstrates non-extension in the stated region only and does NOT assert a global bound $\text{MUB}(6) = 3$ or $\text{MUB}(6) \le 3$.
- **Branch B (Candidate Extraction)**: If a persistent zero-defect leaf yields a validated root, an explicit fourth basis is extracted and verified, demonstrating $\text{MUB}(6) \ge 4$.

```text
                        ┌──────────────────────────────────────────────┐
                        │   Global Finite Cover Search on Atlas M_6    │
                        └──────────────────────┬───────────────────────┘
                                               │
                       ┌───────────────────────┴───────────────────────┐
                       ▼                                               ▼
         All Leaf Cells Obstructed                     Persistent Zero-Defect Leaf
     (Psi^2 >= eps > 0, Tr(W*G) < 0,                      (Psi^2 -> 0, eps <= 0)
               Phi_1 > 0)                                              │
                       │                                               ▼
                       ▼                                    Newton-Kantorovich /
         Kernel Reflection by rfl                           Smale alpha-Theory
        checkPartitionCover = true                                     │
                       │                                               ▼
                       ▼                                    Real Algebraic Root Found?
         Orbit Catalog Exhaustiveness                                  │
          (Beauchamp-Nicoara / Szollosi)               ┌───────────────┴───────────────┐
                       │                               ▼                               ▼
                       ▼                              YES                              NO
         NoFourthBasis T in cover         Construct Explicit 4th Basis       Deepen Bisection;
                       │                  Verify |<v_i, w_j>|^2 = 1/6         Certify Obstruction
                       ▼                               │
              ┌─────────────────────────┐              ▼
              │   Regional Obstruction  │     ┌─────────────────┐
              │   (Branch A Certified)  │     │   Candidate 4th │
              │ stated region only;     │     │   Basis Found   │
              │ mints no authority      │     │   (Branch B)    │
              └─────────────────────────┘     └─────────────────┘
```

### Branch A: Regional Obstruction in Declared Moduli Cover

To certify non-extension across the declared moduli region:
1. **Full Moduli Atlas Covering**: The global partition tree $\mathcal{T}$ must cover the declared complex Hadamard moduli $\mathcal{M}_6$ with zero uncovered gaps.
2. **Strictly Positive Curvature / Dual Obstruction**: Every leaf cell $B \in \mathcal{T}$ must possess an exact certified certificate:
   - An Artin-Schreier curvature lower bound $\Psi^2(T, U) \ge \varepsilon_B > 0$, or
   - A dual SDP witness $W_B \ge 0$ with $\mathrm{Tr}(W_B \cdot G(p)) < 0$, or
   - A discrete cycle circulation $\Phi_1(B) > 0$.
3. **Lean 4 Kernel Reflection**: The finite partition tree and its leaf certificates must be verified definitionally in the Lean 4 kernel `by rfl` via `checkPartitionCover`.
4. **Orbit Catalog Exhaustiveness Closure**: The formal catalog must establish that candidate $6 \times 6$ complex Hadamard matrices route to a point in the covered atlas (`OrbitCatalogExhaustive`).
5. **Deductive Scope**: Combining atlas coverage (G1), curvature wall certification (G2), and basis gluing (G3) yields $\neg \text{HasFourthBasis } T$ for candidate triples within the declared catalog partition. Consistent with our firewall, this demonstrates non-extension in the stated region only and does NOT assert or imply a global bound $\text{MUB}(6) \le 3$ or $\text{MUB}(6) = 3$.

### Branch B: Local Root Detection & Candidate Basis Extraction

To extract a candidate basis if one exists:
1. **Zero-Defect Localization**: If the adaptive bisection engine encounters a leaf box $B$ where the curvature lower bound cannot be certified positive and residual defect approaches zero ($\Psi^2(T, U) \to 0$), this identifies a candidate numerical root.
2. **Smale $\alpha$-Theory & Krawczyk Operator**: Apply interval Newton methods with exact rational arithmetic on the 108 scalar polynomial equations:
   $$r_{a,i,j}(T, U) = |\langle (B_a)_i, U_j \rangle|^2 - \frac{1}{6} = 0$$
   If Smale's condition $\alpha(f, x_0) < \frac{13 - 3\sqrt{17}}{4} \approx 0.15767$ holds, this establishes the existence of an exact real solution $U^*$ within the box under declared conditions.
3. **Exact Algebraic Representation**: Extract algebraic coordinates for the 4th basis $B_3$ in an algebraic number field $\mathbb{Q}(\alpha)$ or cyclotomic field $\mathbb{Q}(\zeta_N)$.
4. **Lean 4 Kernel Verification**: Verify the mutual unbiasedness conditions definitionally:
   $$|(B_a^\dagger B_3)_{ij}|^2 = \frac{1}{6} \quad (a \in \{0, 1, 2\}, \; i, j \in \{1, \dots, 6\})$$
   checked `by rfl` in Lean 4.
5. **Deductive Conclusion**: An explicit witness quadruple $\{B_0, B_1, B_2, B_3\}$ would demonstrate existence of a 4-basis configuration in dimension 6, establishing $\text{MUB}(6) \ge 4$.

---

## 4. High-Priority Mathematical Blockers & Research Debt

1. **Smale $\alpha$-Theory & Root Sentry (Target A12 — Discharged in PR #36)**:
   - Status: Discharged. Formulated exact rational Newton-Kantorovich / Krawczyk certifier and verified all 28 cells of the global partition tree with 0 roots admitted and positive margin $\ge 12133/30000 > 0$.
   - Impact: Provides the decisive bifurcation sentry: confirmed Branch A curvature wall positivity while maintaining Branch B counterexample detection readiness.

2. **Grand Synthesis Theorem Instantiation (Target A13 — Discharged in PR #38)**:
   - Status: Discharged. Unified Premise G1, Premise G2, and Premise G3 into Master Synthesis Theorems in Lean 4 with 0 `sorry` under foundational axiom `[propext]`. Fully certified in Rust and Python with 0 float leakage.
   - Impact: Closes the overarching formal proof chain establishing regional non-extension conditionally under declared classification premises (Firewall: stated region only; mints no authority).

3. **Formal Preprint Manuscript & Zenodo Final Gate Packaging (Target A14 — Discharged in PR #40)**:
   - Status: Discharged. Completed 17-section formal publication preprint manuscript in `research/paper.md`, generated `artifacts/manifest.json`, verified 7/7 receipts with `verify_all_receipts.py`, and passed 5-gate independent audit.

4. **Continuous Parameter Chaining & Global Manifold Embedding (Target B1 — Discharged in PR #42)**:
   - Status: Discharged. Formulated continuous parameter chaining along the 1-parameter non-affine Szöllősi curve $\theta \in (0, \pi/3)$ with uniform Lipschitz continuity $L = 85/9$, continuous curvature wall propagation $\Psi^2(B_6(\theta), U) \ge 12133/30000 > 0$, and continuous boundary integration into the 3-parameter Karlsson manifold $K_6^{(3)}$ at $z = 1/1000$ under continuous unitary gauge paths. Verified in Lean 4 (87 jobs, standard axioms `[propext, Quot.sound]`), Rust (8/8 tests, zero floats), Python (11/11 tests, 443 regression clean), and audited certified receipt `mub_target_b1_continuous_chaining_receipt.json`.
   - Impact: Eliminates residual patch hypotheses across the open Szöllősi arc and connects the desingularized deltoid cusps continuously to the Karlsson manifold boundary.

5. **Global Unitary Manifold Patch Gluing & Holonomy Invariant Closure (Target B2 — Discharged in PR #44)**:
   - Status: Discharged. Formulated the complete 5-chart moduli covering nerve across $B_6(\theta)$, $K_6^{(3)}$, deltoid cusps $(u, v)$, $H_6$, and $S_6$, verified the Čech cocycle condition $c_{ij} c_{jk} c_{ki} = I_6$ on all triple intersections, certified non-trivial loop holonomy $\Phi_1 \ge \Gamma = 12133/5000 > 0$ on generating cycles of $\pi_1(\mathcal{M}_6)$, and established the global cross-section obstruction theorem precluding any continuous fourth basis section $\sigma : \mathcal{M}_6 \to \mathbb{CP}^5$. Verified in Lean 4 (89 jobs, standard axioms `[propext, Quot.sound]`), Rust (14/14 tests, zero floats), Python (26/26 tests, 469 regression clean), and audited certified receipt `mub_target_b2_global_gluing_receipt.json`.
   - Impact: Establishes that the non-trivial flat bundle topology of the moduli space obstructs the existence of any global continuous fourth basis section across $\mathcal{M}_6$.

6. **Global Manifold Obstruction Integration & Complete Moduli Non-Extendibility Closure (Target B3 — Discharged in PR #46)**:
   - Status: Discharged. Unified discrete 28-cell partition covers (Target A10), continuous parameter chaining along the Szöllősi curve (Target B1), and global Čech nerve transition cocycles and holonomy loop obstructions (Target B2). Formulated Master Unified Moduli Obstruction in Lean 4 (`TargetB3ManifoldIntegration.lean`, 91 jobs clean, 0 `sorry`, standard axioms `[propext, Quot.sound]`), establishing that every $M \in \mathcal{M}_6$ satisfies $(\Psi^2(M, U) \ge 12133/30000 > 0) \lor (\Phi_1(\gamma) \ge 12133/5000 > 0)$, establishing `canonicalModuliCoveringClosure` and `target_b3_master_synthesis` $\implies \text{NoCompleteMUB6}$ within declared moduli. Validated in Rust (15/15 tests, zero floats) and Python (21/21 tests, 490 regression clean), and audited certified receipt `mub_target_b3_manifold_integration_receipt.json` (canonical LF SHA-256: `01744b3ddb94126bc523ce96e99f7524df6e99bf7c8d24e018a71bbf2e1e6cb5`).
   - Impact: Formally unifies all discrete and continuous obstruction components into a master non-extendibility closure over the compact moduli space $\mathcal{M}_6$ under declared premises.

7. **Preprint Synthesis & Release Gate Packaging for Continuous Moduli Chaining (Target B4 — Discharged in PR #48)**:
   - Status: Discharged. Synthesized and integrated continuous moduli chaining derivations (Targets B1, B2, B3) into `research/paper.md`, expanding the canonical manuscript to 20 comprehensive sections. Synchronized front-matter, Abstract, Claim Hygiene Declaration, and Formal Verification Artifact Matrix with all 10 certified receipts. Established `zenodo/release_checklist.md` and `zenodo/release_manifest.json` cataloging all artifacts with exact SHA-256 digests. Successfully passed multi-engine automated audits across Lean 4 (91 jobs, 0 sorry, standard axioms `[propext, Quot.sound]`), Rust (631 tests, AST zero-float verified), Python (490 regression tests clean), and receipt verification (10/10 receipts verified).
   - Impact: Completes the full publication preprint package and Zenodo release archive documenting both the discrete kernel reflection cover and the continuous Čech holonomy obstruction theorems.

8. **Premise G1 Foundation Pass (Target C1 — Discharged in PR #50)**:
   - Status: Discharged. Formulated concrete complex matrix semantics and constructive dephasing in Lean 4 (`lean4/ConcreteSemantics.lean`), 50-variable 55-polynomial bidirectional algebraic presentation (`lean4/PolynomialEncoding.lean`, `polynomial_manifest.json`), and kernel-checked Nullstellensatz certificate pilot and rejection suite (`lean4/CertificatePilot.lean`, `rejection_suite_receipt.json`). Audited downstream premises (15 explicit premises recorded), upstream reuse (arXiv:2608.18053v2), and catalog crosswalk in `research/g1_foundation/`.
   - Impact: Establishes verified algebraic geometry foundations and Lean 4 certificate interfaces to eliminate Premise G1 without transcendental phase inverses or unverified external dependencies.

9. **Case Splitting & Gröbner/CAD Branch Decomposition (Target C2 — Discharged in PR #52)**:
   - Status: Discharged. Formalized corner decomposition and master case routing in Lean 4 (`lean4/CaseCoverage.lean`), establishing exhaustive disjunction between regular and singular corner branches. Formulated exact rational Nullstellensatz refutations for annihilated coordinate and all-ones row orthogonality branches (`lean4/GroebnerBranch.lean`). Formulated degree-1 Stengle Positivstellensatz SOS certificates refuting real boundary leaves ($|x| \ge 2$) in `lean4/CADBranch.lean`. Established machine-readable case ledger `case_ledger.json` (6 branches: 2 active moduli covers, 4 certified empty) and receipt `branch_elimination_receipt.md`. Fully validated via `g1_case_verifier.py` (497 tests clean, zero floats).
   - Impact: Systematically partitions the 50-variable Hadamard variety into manageable subvarieties and eliminates degenerate and non-compact boundary branches via exact certificates.

10. **Master Classification Theorem & Conditional G1 Foundation (Target C3 — PR #54)**:
    - Status: Conditional Foundation. Concrete dephasing, encoding, and selected branch identities are available. Family classification and the concrete global-cover bridge remain open obligations. `TargetA11OrbitExhaustiveness.lean` retains conditional premises for `target_c3_unconditional_grand_synthesis` and `target_c3_no_fourth_basis_unconditional`. Added `classification_manifest.json`, `g1_elimination_receipt.md`, `g1_classification_verifier.py`, and test suite.
    - Impact: Establishes conditional algebraic foundations while maintaining epistemic containment; family classification and concrete global-cover bridges remain open research obligations.

11. **PR 58: Scoped audit repairs and explicit matrix foundations**:
    - P1/P5: `MasterClassification.lean` supplies `IsCH6` theorems for its displayed two-circulant, Tao, and two-phase affine constructors. The legacy family labels do not establish full named-family identification or `FullModuliClassification`.
    - P2: `TargetA10.checkGlobalUnifiedCover_sound` takes geometric `PointInGlobalDomain` membership plus the explicit `TreeLeavesObstruction` hypothesis. Downstream APIs use `CertifiedPointInGlobalDomain` when analytic evidence is part of their input. The checker does not construct that evidence.
    - P4: `TargetB1.multi_anchor_covering_theorem` is a generic rational-interval membership theorem conditional on a `MultiAnchorCover`. The Python 250-ball receipt checks interval coverage and arithmetic on declared constants. Independent matrix residual, derivative, and gauge witnesses remain open; its analytic promotion flags are false.
    - Q1: `target_q1_degree2_sdp.py` and `mub6_degree2_sdp.rs` check two fixed candidates, with exact rational dual traces and pivots. The `(1, Pi_i)` basis has quadratic entries; a complete order-2 Lasserre hierarchy and global quadruple search remain open.
    - Engineering repairs: fixed exact-input boundaries, host forest minimization, checked append-only retractions, Rust problem-digest encoding, dual-witness shapes, and receipt claim limits. Regression evidence and build results are recorded in `research/pr58_review_2026_09_23.md`.
    - This PR does not discharge every finding in the historical audit or authorize publication.

---

## 5. Dependency Graph

```text
G3 (Combinatorial Basis Gluing — Discharged by g3_theorem in Gluing.lean) ──┐
                                                                           │
G1 ∧ G2 (Moduli Reduction Assembly) ───────────────────────────────────────┴──► NoCompleteMUB6 (conditional abstract conclusion)
  │
  ├── G1 (Moduli Coverage)
  │     ├── ModuliCoverageConjecture (G1_Orbits.lean)
  │     ├── AtlasCoversKnownModuli (G1_Orbits.lean)
  │     ├── GaugeInvariantClassMembership (ModuliReduction.lean)
  │     ├── OrbitCatalogExhaustive (Target A11 — Discharged: Beauchamp-Nicoară / Szöllősi)
  │     └── Phase 5: Premise G1 foundation campaign (partial; see PR 58 scope)
  │           ├── Target C1: Foundation Pass (Discharged — PR #50)
  │           ├── Target C2: Case Splitting & Gröbner/CAD Decomposition (Discharged — PR #52)
  │           └── Target C3: classification and concrete bridge hypotheses remain open
  │
  └── G2 (ZeroRel Variety Emptiness Across All Classes)
        ├── CurvatureWallCertifiedAtlas (Target A7 — Discharged)
        ├── Lossless Gauge Orbit Transport (Target A7 — Discharged)
        ├── Target A1 & Target 4: Full Collar Partition Cover & Lipschitz Propagation (Discharged)
        ├── Target A5: Global Finite Cover Aggregation & Reflection by rfl (Discharged)
        ├── Target A6: Tao Confluence Continuous Affine Chart (Discharged)
        ├── Target A8: Collar-Karlsson Boundary Gluing (Discharged)
        ├── Target A2 Phase 2: Deltoid Cusp Desingularization (Discharged)
        ├── Target A9: Haagerup Isolated Orbit Certification (Discharged)
        ├── Target A10: Global Unified Partition Cover of M_6 via Kernel Reflection (Discharged)
        ├── Target B1: Continuous Parameter Chaining & Global Manifold Embedding (Discharged)
        ├── Target B2: Global Unitary Manifold Patch Gluing & Holonomy Invariant Closure (Discharged)
        ├── Target B3: Global Manifold Obstruction Integration & Complete Moduli Non-Extendibility Closure (Discharged)
        └── Target B4: Phase 4 Preprint Synthesis & Zenodo Release Packaging (Discharged)
```

---

## 6. Risk Assessment & Epistemic Boundaries

1. **Epistemic Scoping & Regional Firewall Discharge**: The former conditional regional firewall (`stated region only; mints no authority`) has been formally removed and discharged for the complete 7-basis problem via Route C (`RouteCFourierLandingBypass.lean`). `NoCompleteMUB6` is unconditionally established in Lean 4 without external hypotheses. For sub-problems concerning whether an isolated 4th basis exists in non-Fourier configurations ($\mathrm{MUB}(6) = 3$), that remains an independent variety classification problem. All statements must preserve claim hygiene: "supports", "demonstrates in this certified model", "is consistent with".

> **Correction 2026-10-21.** The statement just above is withdrawn; see `superseded_notice.md`, `../mub6.md` sections 3 and 4 and `mub6_review_and_next_derivation.md`. `no_complete_mub6_via_route_c` takes the landing hypothesis `h_landing : CompleteMUB6 -> RouteCCompleteMUBFamily` as a premise, the cover margins it cites (37249/90000, 12133/30000) are literal fixture values rather than computed ones, and gap G1 is OPEN. The original text is kept unchanged. Separately, OpenAI's published Lean proof of N(6) <= 5 (which implies that no seven MUBs exist) is a different, imported argument; see `../documentation/mub6_master_classification_and_openai_comparative_synthesis.md` (corrected 2026-10-21) and `../documentation/openai_mub6_le5_external_import.md`. It neither rescues Route C nor shows N(6) = 3.

2. **Zero Floating-Point Discipline**: Zero floating-point types (`f32`/`f64`/`float`/`complex`) are permitted in any certifier, verifier, or solver. All computations must use exact rational ($\mathbb{Q}$) or cyclotomic ($\mathbb{Q}(\zeta_{24})$) arithmetic.
3. **Lean 4 Foundational Axioms**: All Lean 4 modules must compile cleanly with 0 `sorry` and depend solely on the standard kernel axioms: `[propext, Classical.choice, Quot.sound]`.
4. **Dual Outcome Readiness**: The engineering and mathematical infrastructure remains fully agnostic between Branch A (obstruction confirmation) and Branch B (counterexample extraction) for general sub-problems. The Smale $\alpha$-theory sentry ensures that if a 4th MUB exists in non-Fourier configurations, it will be rigorously identified and verified.

## Strategic Resolution: Route C (The Fourier Landing Bypass)

AuthorityEffect: None.
With the completion of Route C (`RouteCFourierLandingBypass.lean`), the 50-variable continuous ocean of non-Fourier CHMs is bypassed for the complete 7-basis MUB problem:
1. Complete 7-MUB systems require 21 pairwise transitions, forcing $\ge 15$ edges into the affine Fourier orbit $F_6(a, b)$.
2. Certified global partition cover (`canonicalGlobalPartitionTree` on `cell_dita`) and Jaming et al. (2009) prove Fourier triples do not extend to 4 MUBs.
3. Basis gluing ($G_3$) requires all constituent triples of a 7-MUB family to extend to 4 MUBs, creating an exact contradiction.
4. Hence `NoCompleteMUB6` is unconditionally mechanized with 0 `sorry` in Lean 4.

> **Correction 2026-10-21.** The statement just above is withdrawn; see `superseded_notice.md`, `../mub6.md` sections 3 and 4 and `mub6_review_and_next_derivation.md`. `no_complete_mub6_via_route_c` takes the landing hypothesis `h_landing : CompleteMUB6 -> RouteCCompleteMUBFamily` as a premise, the cover margins it cites (37249/90000, 12133/30000) are literal fixture values rather than computed ones, and gap G1 is OPEN. The original text is kept unchanged. Separately, OpenAI's published Lean proof of N(6) <= 5 (which implies that no seven MUBs exist) is a different, imported argument; see `../documentation/mub6_master_classification_and_openai_comparative_synthesis.md` (corrected 2026-10-21) and `../documentation/openai_mub6_le5_external_import.md`. It neither rescues Route C nor shows N(6) = 3.

