# Master Prompt Space: 250 Mathematical Attack Prompts (Teams 1–10)

**AuthorityEffect:** None  
**Firewall Line:** `stated region only; mints no authority`  
**Authors:** Executive Steering Team (Team 0: 5 Experts)

---

## Overview

The master prompt space establishes $10 \times 25 = 250$ distinct mathematical attack prompts divvied across Teams 1 through 10.
Each team consists of:
- 1 Quantum Information Expert
- 1 Abstract Algebra Expert

Every prompt defines:
1. Target mathematical subproblem
2. Constraint graph topology & redex positions
3. Allowed 4-move transitions (`ASSERT`, `CUT`, `VERIFY`, `RETRACT`)
4. Terminal acceptance condition (zero defect $\|\Phi_1\|_{L_1} = 0$ or certified obstruction $\Phi_1 \ge \varepsilon > 0$)
5. Strict zero-float rational arithmetic contract

---

## Part I: Target G1 — Hadamard Variety $\mathcal{H}_6$ Decomposition & Orbit Exhaustiveness (Teams 1–5)

### Team 1: Fourier Component & Affine Diță Torus Desingularization ($F_6, D_6$)
- **PROMPT_T01_01**: Discrete Fourier matrix $F_6 \cong F_2 \otimes F_3$ character table dephased coordinates over $\mathbb{Q}(\zeta_6)$ and affine tangent space defect $d(F_6) = 4$.
- **PROMPT_T01_02**: Diță 2-parameter affine phase family $D_6(\alpha, \beta) = \begin{pmatrix} F_3 & D(\alpha, \beta)F_3 \\ F_3 & -D(\alpha, \beta)F_3 \end{pmatrix}$ orthogonality relations.
- **PROMPT_T01_03**: 1-parameter slice $D_6(\alpha, 0)$ algebraic reduction to $T^1$.
- **PROMPT_T01_04**: 6 locked Diță point seeds in orbits $Y_2 \otimes Q_1$ and $Y_2 \otimes Q_2$ over $\mathbb{Q}(\zeta_{24})$.
- **PROMPT_T01_05**: Phase difference holonomy around Diță 3-cycle faces in the collar partition.
- **PROMPT_T01_06**: Exact rational cross-ratio invariants $cr_{ij,kl}(D_6(\alpha, \beta))$ across all 225 submatrices.
- **PROMPT_T01_07**: Desingularization of the boundary collision locus $(\alpha, \beta) \to (0, 0)$ (Fourier confluence).
- **PROMPT_T01_08**: ZeroRel curvature lower bound $\Psi^{\text{sq}}(D_6(\alpha), U) \ge \varepsilon > 0$ on certified Diță seed boxes.
- **PROMPT_T01_09**: Elimination of candidate 4th basis vectors in the Diță affine chart via exact rational Gröbner bases.
- **PROMPT_T01_10**: Invariance of the Diță cycle defect under diagonal phase gauge shifts.
- **PROMPT_T01_11**: Smale $\alpha$-theory approximate zero exclusion on the Diță 2-torus.
- **PROMPT_T01_12**: Exact cyclotomic representation of $D(\alpha, \beta)$ for rational angles $\alpha, \beta \in 2\pi \cdot \mathbb{Q}$.
- **PROMPT_T01_13**: Evaluation of the 108 ZeroRel polynomials on the boundary of the Diță seed enclosures.
- **PROMPT_T01_14**: Bounded-depth rational bisection on $D_6(\alpha, \beta)$ parameter cells.
- **PROMPT_T01_15**: Cycle circulation $\Phi_1 > 0$ verification across Diță grid boundaries using Network Simplex.
- **PROMPT_T01_16**: Moduli coordinate transition from Diță chart to Karlsson chart.
- **PROMPT_T01_17**: Obstruction of circulant symmetric Hadamard extensions within the Diță orbit.
- **PROMPT_T01_18**: Non-extendibility of $(I_6, F_6, D_6(\alpha))$ to a 4-MUB set for all $\alpha \in [0, 2\pi)$.
- **PROMPT_T01_19**: Nullstellensatz certificate for emptiness of $V_{\mathbb{R}}(\text{ZeroRel}_{T_{\text{Dita}}})$.
- **PROMPT_T01_20**: Topological triviality of the tangent bundle over the interior of the Diță torus.
- **PROMPT_T01_21**: Exact rational interval bounds on Diță gradient variations.
- **PROMPT_T01_22**: Uniform derivative bounds $L_{\text{Dita}} \le 85/9$ across the 2D affine patch.
- **PROMPT_T01_23**: Rejection of floating-point perturbation in Diță phase matrices.
- **PROMPT_T01_24**: Verification of $F_6^\dagger D_6(\alpha, \beta) \in \mathcal{H}_6$ iff $\alpha = \beta = 0 \pmod{2\pi/3}$.
- **PROMPT_T01_25**: Master synthesis of the Diță/Fourier component obstruction certificate.

### Team 2: Chernyavsky-Tao Isolated Point $S_6$, Defect Zero Rigidity, & Non-Extendibility
- **PROMPT_T02_01**: Construction of Tao matrix $S_6$ over $\mathbb{Q}(\zeta_3)$ from spectral sets in $\mathbb{Z}_3 \times \mathbb{Z}_3$.
- **PROMPT_T02_02**: Exact rational proof that defect $d(S_6) = 0$ (tangent space orthogonality has no non-trivial solutions).
- **PROMPT_T02_03**: Topological isolation of $S_6$: proof that $\mathcal{H}_6 \cap B(S_6, r) = \mathcal{O}(S_6)$ for $r = 1/10$.
- **PROMPT_T02_04**: Evaluation of all 225 cross-ratios of $S_6$ showing $e_m \in \{0, 8, 16\} \pmod{24}$.
- **PROMPT_T02_05**: Proof that no cross-ratio of $S_6$ equals $-1$ (no $2 \times 2$ submatrix is row/column orthogonal).
- **PROMPT_T02_06**: Evaluation of transition matrix $H_{12} = S_6^\dagger (D_1 P_1 S_6 P_2 D_2)$ across all permutation cosets.
- **PROMPT_T02_07**: Proof that $H_{12} \notin \mathcal{H}_6$ for all non-trivial gauge transformations: no internal MU pairs in $\mathcal{O}(S_6)$.
- **PROMPT_T02_08**: ZeroRel curvature evaluation $\Psi^{\text{sq}}(S_6, U) \ge 12133/30000 > 0$ over candidate bases.
- **PROMPT_T02_09**: Exact rational sum-of-squares certificate for $V_{\mathbb{R}}(\text{ZeroRel}_{S_6}) = \emptyset$.
- **PROMPT_T02_10**: Non-commutative moment SDP refutation of synthetic $S_6$ completion ($\operatorname{Tr}(W_8 \cdot M_8) = -5046587/129600$).
- **PROMPT_T02_11**: Invariant polynomial spectrum distinguishing $\mathcal{O}(S_6)$ from continuous families.
- **PROMPT_T02_12**: Smale $\alpha$-theory certification bounding distance to nearest complex Hadamard manifold.
- **PROMPT_T02_13**: Proof that $(I_6, S_6)$ cannot extend to an MU triple $(I_6, S_6, B_2)$ with $B_2 \in \mathcal{O}(S_6)$.
- **PROMPT_T02_14**: Evaluation of cross-orbit pairing $(I_6, S_6, D_6(\alpha))$: transition matrix unimodularity failure.
- **PROMPT_T02_15**: Exact rational $LDL^T$ certificate of curvature matrix at $S_6$ basepoint.
- **PROMPT_T02_16**: Simplicial 1-cocycle circulation $\Phi_1(S_6) \ge 12133/5000 > 0$ on triangular boundary nerve.
- **PROMPT_T02_17**: Rejection of near-Tao perturbation candidates under 100% exact rational check.
- **PROMPT_T02_18**: Gröbner basis decomposition of $S_6$ local dephased ideal in 50 real variables.
- **PROMPT_T02_19**: Flat extension obstruction: proof that $M_4(S_6)$ admits no rank-preserving extension $M_5$.
- **PROMPT_T02_20**: Projective blow-up of the singular intersection between $S_6$ and the Karlsson closure.
- **PROMPT_T02_21**: Proof that $\mathcal{O}(S_6)$ supports at most 3 MUBs in $\mathbb{C}^6$.
- **PROMPT_T02_22**: Network Simplex dual witness on the Tao isolated neighborhood graph.
- **PROMPT_T02_23**: Elimination of real Hadamard sub-configurations within $\mathcal{O}(S_6)$.
- **PROMPT_T02_24**: Lean 4 formalization of $S_6$ algebraic matrix and dephased form.
- **PROMPT_T02_25**: Master synthesis of the Tao isolated orbit non-extendibility theorem.

### Team 3: Szöllősi Non-Affine Family $B_6(\theta)$, Haagerup Point $H_6$, & 2-Circulant Intersections
- **PROMPT_T03_01**: Parameterization of Szöllősi 1-parameter family $B_6(\theta)$ for $\theta \in [0, \pi]$.
- **PROMPT_T03_02**: Algebraic phase equations for $B_6(\theta)$ derived from 2-circulant core blocks.
- **PROMPT_T03_03**: Exact algebraic identification of Haagerup matrix $H_6$ at $\cos\theta = (\sqrt{3}-1)/2$.
- **PROMPT_T03_04**: Generic defect calculation $d(B_6(\theta)) = 1$ for $\theta \in (0, \pi) \setminus \{\theta_H\}$.
- **PROMPT_T03_05**: Evaluation of transition matrix $H_{12} = B_6(\theta_1)^\dagger B_6(\theta_2)$ showing non-unimodularity.
- **PROMPT_T03_06**: Proof that no two distinct Szöllősi matrices form an MU triple with $I_6$.
- **PROMPT_T03_07**: Desingularization of the deltoid cusp singularities at $\theta \in \{0, 2\pi/3, 4\pi/3\}$.
- **PROMPT_T03_08**: Projective blow-up coordinates $(u, v)$ along the Segre variety locus $(a-1)(d-1) = (b-1)(c-1)$.
- **PROMPT_T03_09**: Factored corner determinant on blow-up chart: $P_{\text{corner}} = r \cdot \tilde{P}(u, v)$ with bounded condition number.
- **PROMPT_T03_10**: Desingularized Lipschitz gap propagation: $f(u, v) \ge \varepsilon_{\text{cusp}} - L_{\text{proj}}\delta > 0$.
- **PROMPT_T03_11**: Exact rational interval enclosure of Haagerup point $H_6$ over $\mathbb{Q}(\sqrt{3})$.
- **PROMPT_T03_12**: ZeroRel curvature lower bound across the Haagerup rational ball $B(H_6, 1/100)$.
- **PROMPT_T03_13**: Cross-ratio invariant spectrum of $H_6$ verifying orbit isolation against $F_6, D_6, S_6$.
- **PROMPT_T03_14**: Bounded-depth rational bisection on Szöllősi arc parameter cells.
- **PROMPT_T03_15**: Cycle circulation $\Phi_1 > 0$ across the composite Szöllősi deltoid partition.
- **PROMPT_T03_16**: Connecting the Szöllősi family boundary to the Karlsson 3-parameter manifold.
- **PROMPT_T03_17**: Evaluating pairing between $B_6(\theta)$ and Diță family $D_6(\alpha)$: triad incompatibility.
- **PROMPT_T03_18**: Nullstellensatz certificate for emptiness of $V_{\mathbb{R}}(\text{ZeroRel}_{B_6(\theta)})$ along the arc.
- **PROMPT_T03_19**: Network Simplex dual witness certification on blown-up cusp cells.
- **PROMPT_T03_20**: Non-existence of 4-MUB sets containing a Szöllősi matrix and a Tao matrix.
- **PROMPT_T03_21**: Exact rational representation of algebraic roots of $B_6(\theta)$ via minimal polynomials.
- **PROMPT_T03_22**: Uniform derivative bounds on the Szöllősi arc away from cusps.
- **PROMPT_T03_23**: Rejection of non-unitary / non-unimodular perturbations along $B_6(\theta)$.
- **PROMPT_T03_24**: Lean 4 verification of Szöllősi deltoid cusp desingularization.
- **PROMPT_T03_25**: Master synthesis of the Szöllősi / Haagerup orbit non-extendibility theorem.

### Team 4: Karlsson 3-Parameter Manifold $K_6^{(3)}$, Boundary Strata, & Degeneracy Loci
- **PROMPT_T04_01**: Parameterization of Karlsson 3-parameter continuous family $K_6^{(3)}(x, y, z)$.
- **PROMPT_T04_02**: Degeneracy locus where $K_6^{(3)}$ specializes to the Diță affine family $D_6(\alpha, \beta)$.
- **PROMPT_T04_03**: Boundary stratum where $K_6^{(3)}$ connects to the Szöllősi family $B_6(\theta)$.
- **PROMPT_T04_04**: Generic defect analysis $d(K_6^{(3)}) = 3$, jumping to 4 on Diță sub-manifold.
- **PROMPT_T04_05**: Evaluation of transition matrix $H_1^\dagger H_2$ for internal pairs in $K_6^{(3)}$.
- **PROMPT_T04_06**: Proof that internal MU pairs in $K_6^{(3)}$ exist only within the embedded Diță stratum.
- **PROMPT_T04_07**: Exterior boundary interface between Karlsson volume and the 2D periodic collar slice.
- **PROMPT_T04_08**: Exact rational boundary overlap evaluator between collar partition and Karlsson boundary.
- **PROMPT_T04_09**: Positive curvature margin $\varepsilon_{\text{interface}} > 0$ on the Karlsson-collar boundary.
- **PROMPT_T04_10**: Multi-chart transition cocycle chaining across the Karlsson boundary interface.
- **PROMPT_T04_11**: Volume conservation certification: $\sum \text{vol}(C_i) = \text{Vol}_{\text{total}}$ with exact zero gap.
- **PROMPT_T04_12**: Network Simplex acceleration confirming $\Phi_1 > 0$ across all composite Karlsson loops.
- **PROMPT_T04_13**: Elimination of candidate 4th bases across the Karlsson volume via branch-and-bound.
- **PROMPT_T04_14**: Algebraic characterization of the Karlsson non-affine phase relations.
- **PROMPT_T04_15**: Bounded-depth rational bisection on 3D Karlsson interval boxes.
- **PROMPT_T04_16**: Rejection of gapped boundary interfaces between Karlsson and Diță charts.
- **PROMPT_T04_17**: Exact cyclotomic evaluations on rational Karlsson grid points.
- **PROMPT_T04_18**: Smale $\alpha$-theory sentry verifying absence of roots on the Karlsson boundary.
- **PROMPT_T04_19**: Nullstellensatz certificate for emptiness of $V_{\mathbb{R}}(\text{ZeroRel}_T)$ on Karlsson volume.
- **PROMPT_T04_20**: Proof that no putative MUB quadruple extends across the Karlsson volume boundary.
- **PROMPT_T04_21**: Invariant cross-ratio mapping across the 3 parameters of $K_6^{(3)}$.
- **PROMPT_T04_22**: Uniform gradient bounds on the Karlsson interior.
- **PROMPT_T04_23**: AST zero-float linting on Karlsson exact rational evaluator.
- **PROMPT_T04_24**: Lean 4 formalization of the Karlsson volume boundary interface.
- **PROMPT_T04_25**: Master synthesis of the Karlsson manifold coverage and boundary gluing theorem.

### Team 5: 50-Variable Variety $\mathcal{H}_6$ Decomposition, Corner Minors, & Pigeonhole Triad Obstruction
- **PROMPT_T05_01**: Formulation of the 55 polynomial equations in 50 real variables defining $\mathcal{H}_6$.
- **PROMPT_T05_02**: Elimination ideal of the $3 \times 3$ corner submatrix: 9 complex variables (18 real variables).
- **PROMPT_T05_03**: Finite-incidence algebraic corner reconstruction theorem (Cárdenes Wuttig & Tindall 2026).
- **PROMPT_T05_04**: Proof that every dephased $6 \times 6$ CHM is algebraically determined by a $3 \times 3$ corner.
- **PROMPT_T05_05**: Irreducible component decomposition of the corner variety $V(I_{\text{corner}})$.
- **PROMPT_T05_06**: Proof that all viable corner determinants factor into $F_6, D_6, S_6, B_6, K_6$ branches.
- **PROMPT_T05_07**: Absence of exotic isolated points: proof that defect zero implies $S_6$ equivalence.
- **PROMPT_T05_08**: Formulation of the Triad Compatibility Variety $V_{\text{triple}} \subset \mathcal{H}_6 \times \mathcal{H}_6$.
- **PROMPT_T05_09**: Proof that $H_1^\dagger H_2 \in \mathcal{H}_6$ forces both $H_1$ and $H_2$ to lie in compatible orbits.
- **PROMPT_T05_10**: Cross-orbit triad obstruction: proof that $(S_6, B_6)$, $(S_6, S_6)$, $(B_6, B_6)$ cannot form an MU triple with $I_6$.
- **PROMPT_T05_11**: Combinatorial Pigeonhole Lemma: Any complete 7-MUB configuration contains $\ge 5$ Diță/Fourier bases.
- **PROMPT_T05_12**: Proof that $\ge 5$ Diță/Fourier bases force $\ge 1$ purely Diță/Fourier triple.
- **PROMPT_T05_13**: Connecting the Pigeonhole Lemma to the certified Diță moduli atlas.
- **PROMPT_T05_14**: Formal discharge of Premise $G_1$ without continuum cover of the non-Diță continuum.
- **PROMPT_T05_15**: Exact rational Gröbner basis computation on the 18-variable corner ideal.
- **PROMPT_T05_16**: Real radical ideal computation $\sqrt[\mathbb{R}]{I(\mathcal{H}_6)}$.
- **PROMPT_T05_17**: Degree bounds on the Nullstellensatz certificates for the corner variety.
- **PROMPT_T05_18**: Network Simplex dual witness certifying non-extendibility of cross-orbit triples.
- **PROMPT_T05_19**: Exact rational certifier verifying corner reconstruction in Python and Rust.
- **PROMPT_T05_20**: Negative control test suite rejecting corrupted or perturbed corner matrices.
- **PROMPT_T05_21**: Lean 4 formalization of the 50-variable variety equations in `TargetG1OrbitExhaustiveness.lean`.
- **PROMPT_T05_22**: Lean 4 proof of the Triad Compatibility Hadamard equivalence (`mu_triple_hadamard_transition`).
- **PROMPT_T05_23**: Lean 4 proof of `TriadModuliPigeonhole` lemma.
- **PROMPT_T05_24**: Axiom audit of the Target G1 Lean formalization: strictly `[propext, Quot.sound]`.
- **PROMPT_T05_25**: Master synthesis of Target G1 Foundation & Orbit Exhaustiveness Closure.

---

## Part II: Target Q-Soundness — Moment Positivity Soundness Gap & Positivstellensatz (Teams 6–10)

### Team 6: Non-Commutative Projector Algebra $\mathbb{C}\langle \Pi_{i,a} \rangle$ Ideals & Word Reduction
- **PROMPT_T06_01**: Generation of the free unital $*$-algebra on 24 formal symbols $\Pi_{i, a}$ ($i \in \{0..3\}, a \in \{0..5\}$).
- **PROMPT_T06_02**: Formalization of the self-adjoint involution $w \mapsto w^*$ by word reversal.
- **PROMPT_T06_03**: Canonical term rewriting system for idempotency $\Pi_{i, a}^2 \to \Pi_{i, a}$.
- **PROMPT_T06_04**: Canonical term rewriting for intra-basis orthogonality $\Pi_{i, a} \Pi_{i, b} \to 0$ ($a \neq b$).
- **PROMPT_T06_05**: Resolution of identity reduction $\sum_{a=0}^5 \Pi_{i, a} \to \mathbf{1}$ (eliminating $\Pi_{i, 5}$).
- **PROMPT_T06_06**: Confluence and termination of the non-commutative term rewriting system (Bergman Diamond Lemma).
- **PROMPT_T06_07**: Basis monomial enumeration for word lengths $d \in \{1, 2, 3, 4\}$.
- **PROMPT_T06_08**: Dimension count of the truncated word subspace $\mathcal{W}_{\le d}$ for $d=1$ (25 dimensions).
- **PROMPT_T06_09**: Dimension count of $\mathcal{W}_{\le 2}$ (projector pairs, NPA Level 2).
- **PROMPT_T06_10**: Dimension count of $\mathcal{W}_{\le 3}$ (projector triples, NPA Level 3).
- **PROMPT_T06_11**: Dimension count of $\mathcal{W}_{\le 4}$ (projector quadruples, NPA Level 4 / Lasserre).
- **PROMPT_T06_12**: Mutual unbiasedness trace condition $\operatorname{Tr}(\Pi_{i, a} \Pi_{j, b}) = 1/6$ in the reduced algebra.
- **PROMPT_T06_13**: Representation of the quadratic module $\mathcal{M}(\mathcal{I}_{\text{proj}})$ generated by projector axioms.
- **PROMPT_T06_14**: Exact rational polynomial arithmetic over reduced words in Python (`Fraction`).
- **PROMPT_T06_15**: Exact rational polynomial arithmetic over reduced words in Rust (`BigRational`).
- **PROMPT_T06_16**: Verification of involution preservation under multiplication: $(u v)^* = v^* u^*$.
- **PROMPT_T06_17**: Characterization of the non-commutative commutator ideal $[\Pi_{i, a}, \Pi_{j, b}]$.
- **PROMPT_T06_18**: Non-triviality of the commutator ideal for $i \neq j$ (quantum non-commutativity).
- **PROMPT_T06_19**: Truncated test vector representation $c : \mathcal{W}_{\le d} \to \mathbb{Q}$.
- **PROMPT_T06_20**: Exact inner product $\langle u, v \rangle = \tilde{\mathbb{E}}[u^* v]$ on reduced words.
- **PROMPT_T06_21**: Negative control testing: rejecting unreduced words with adjacent identical projectors.
- **PROMPT_T06_22**: Lean 4 formalization of the reduced word inductive type in `TargetQArchimedeanPositivstellensatz.lean`.
- **PROMPT_T06_23**: Lean 4 proof of involution anti-automorphism: $(w_1 \cdot w_2)^* = w_2^* \cdot w_1^*$.
- **PROMPT_T06_24**: Axiom audit on algebraic word reduction: zero non-standard axioms.
- **PROMPT_T06_25**: Master synthesis of the non-commutative projector algebra foundation.

### Team 7: Truncated Moment Matrices (Degrees 2, 4, 6, 8) & Exact Rational LDLᵀ Pivot Signatures
- **PROMPT_T07_01**: Construction of Degree-2 moment matrix $M_2$ (size $25 \times 25$) over $\mathbb{Q}$.
- **PROMPT_T07_02**: Exact rational $LDL^T$ decomposition of $M_2$ verifying pivot positivity ($D_i > 0$).
- **PROMPT_T07_03**: Construction of Degree-4 moment matrix $M_4$ incorporating projector pairs.
- **PROMPT_T07_04**: Exact rational $LDL^T$ decomposition of $M_4$ and pivot spectrum analysis.
- **PROMPT_T07_05**: Construction of Degree-6 moment matrix $M_6$ incorporating projector triples.
- **PROMPT_T07_06**: Evaluation of candidate completion $X = 0$ on $M_6$: $\operatorname{Tr}(W_6 \cdot M_6) = -9071/10800 < 0$.
- **PROMPT_T07_07**: Construction of Degree-8 moment matrix $M_8$ incorporating projector quadruples.
- **PROMPT_T07_08**: Evaluation of candidate completion $X = 0$ on $M_8$: $\operatorname{Tr}(W_8 \cdot M_8) = -9071/10800 < 0$.
- **PROMPT_T07_09**: Evaluation of synthetic $S_6$ candidate completion on $M_8$: $\operatorname{Tr}(W_8 \cdot M_8) = -5046587/129600 < 0$.
- **PROMPT_T07_10**: Factored dual witness representation $W = \sum D_k c^{(k)} (c^{(k)})^T$ with $D_k \ge 0$.
- **PROMPT_T07_11**: Constructive proof that $\operatorname{Tr}(W \cdot M) < 0$ refutes pseudo-expectation positivity.
- **PROMPT_T07_12**: Bit-for-bit SHA-256 fingerprint agreement for $M_2, M_4, M_6, M_8$ between Python and Rust.
- **PROMPT_T07_13**: Pivot signature verification: confirming zero negative pivots in valid Gramians.
- **PROMPT_T07_14**: Cross-runtime fixture validation in `test_target_q4_degree8_sdp.py`.
- **PROMPT_T07_15**: Native Rust release-mode test suite in `test_degree8_sdp.rs`.
- **PROMPT_T07_16**: Negative control suite: rejecting non-symmetric matrices and indefinite pivots.
- **PROMPT_T07_17**: AST-level zero-float verification on Rust moment matrix builders.
- **PROMPT_T07_18**: Recursive `assert_no_float` on all Python moment matrix entries.
- **PROMPT_T07_19**: Unified diagnostic ledger API for multi-degree SDP moments.
- **PROMPT_T07_20**: Separation between candidate refutation and global search refusal.
- **PROMPT_T07_21**: Lean 4 formalization of factored dual witness and trace inner product.
- **PROMPT_T07_22**: Lean 4 constructive theorem: `certified_candidate_refutation`.
- **PROMPT_T07_23**: Lean 4 constructive theorem: `dual_witness_trace_nonneg_of_moment_positivity`.
- **PROMPT_T07_24**: Axiom audit of Lean 4 moment matrix theorems: strictly `[propext, Quot.sound]`.
- **PROMPT_T07_25**: Master synthesis of the multi-degree moment SDP hierarchy ledger.

### Team 8: Archimedean Positivstellensatz Certificates in the Projector Quadratic Module
- **PROMPT_T08_01**: Formulation of the quadratic module $\mathcal{Q}(\mathcal{I}_{\text{proj}})$ generated by projector identities.
- **PROMPT_T08_02**: Definition of the Archimedean property: $\exists R \in \mathbb{Q}$ such that $R^2 - \sum_{i,a} \Pi_{i,a}^2 \in \mathcal{Q}$.
- **PROMPT_T08_03**: Construction of explicit exact rational Archimedean certificate for rank-1 projectors.
- **PROMPT_T08_04**: Bound radius calculation: proving $R = \sqrt{24} \le 5$ (exact bound $25 - \sum \Pi_{i,a}^2 \in \mathcal{Q}$).
- **PROMPT_T08_05**: Algebraic identity: $1 - \Pi_{i,a} = (1 - \Pi_{i,a})^2 \in \mathcal{Q}$ by idempotency and self-adjointness.
- **PROMPT_T08_06**: Sum-of-squares decomposition of the norm bound in the projector algebra.
- **PROMPT_T08_07**: Helton-McCullough non-commutative Positivstellensatz application to projector algebras.
- **PROMPT_T08_08**: Proof of asymptotic convergence of the NPA / Lasserre hierarchy under the Archimedean condition.
- **PROMPT_T08_09**: Bridging pseudo-expectations to true states: Gelfand-Naimark-Segal (GNS) state construction.
- **PROMPT_T08_10**: Proof that an Archimedean certificate transforms dual refutations into operator norm bounds.
- **PROMPT_T08_11**: Exact rational certificate generator in Python for the Archimedean identity.
- **PROMPT_T08_12**: Exact rational certificate verifier in Rust with zero float leakage.
- **PROMPT_T08_13**: Evaluation of degree bounds for Archimedean Positivstellensatz certificates.
- **PROMPT_T08_14**: Connecting Archimedean Positivstellensatz to the Artin-Schreier ZeroRel curvature mass $\Psi^{\text{sq}}$.
- **PROMPT_T08_15**: Negative control suite: rejecting perturbed or non-SOS quadratic module elements.
- **PROMPT_T08_16**: Exact rational certificate serialization into JSON schema format.
- **PROMPT_T08_17**: Cryptographic SHA-256 digest pinning of the Archimedean certificate receipt.
- **PROMPT_T08_18**: Lean 4 formalization of `ArchimedeanPositivstellensatzCertificate` structure.
- **PROMPT_T08_19**: Lean 4 proof: `sound_universal_exclusion_via_positivstellensatz`.
- **PROMPT_T08_20**: Lean 4 proof that physical quantum realizations always induce positive states.
- **PROMPT_T08_21**: Discharging the open proof obligation `Q_OBLIGATION_POSITIVSTELLENSATZ`.
- **PROMPT_T08_22**: Axiom audit on Positivstellensatz theorems: strictly `[propext, Quot.sound]`.
- **PROMPT_T08_23**: Boundary check: distinguishing between asymptotic convergence and finite-degree termination.
- **PROMPT_T08_24**: Integration of Archimedean Positivstellensatz with the master verification pipeline.
- **PROMPT_T08_25**: Master synthesis of the Archimedean Positivstellensatz Soundness Bridge.

### Team 9: Curto-Fialkow Flat Extensions, Non-Commutative GNS Extraction, & Rank Loops
- **PROMPT_T09_01**: Formulation of the non-commutative flat extension condition: $\operatorname{rank}(M_d) = \operatorname{rank}(M_{d-1})$.
- **PROMPT_T09_02**: Curto-Fialkow flat extension theorem adapted to non-commutative polynomial algebras.
- **PROMPT_T09_03**: Rank calculation on Degree-2 moment matrix $M_2$: $\operatorname{rank}(M_2) = 25$.
- **PROMPT_T09_04**: Rank calculation on Degree-4 moment matrix $M_4$: checking $\operatorname{rank}(M_4) > \operatorname{rank}(M_2)$.
- **PROMPT_T09_05**: Rank calculation on Degree-6 moment matrix $M_6$: checking $\operatorname{rank}(M_6) > \operatorname{rank}(M_4)$.
- **PROMPT_T09_06**: Rank calculation on Degree-8 moment matrix $M_8$: checking $\operatorname{rank}(M_8) > \operatorname{rank}(M_6)$.
- **PROMPT_T09_07**: Evaluation of the rank-gap sequence $\Delta_d = \operatorname{rank}(M_d) - \operatorname{rank}(M_{d-1})$.
- **PROMPT_T09_08**: Proof that $\Delta_d > 0$ across all evaluated levels: flat extension is not achieved at degree $\le 8$.
- **PROMPT_T09_09**: Exact rational spectral analysis of the non-commutative GNS kernel $\mathcal{N} = \{ u : \tilde{\mathbb{E}}[u^* u] = 0 \}$.
- **PROMPT_T09_10**: Construction of the GNS pre-Hilbert space $\mathcal{H}_{\text{GNS}} = \mathcal{W}_{\le d} / \mathcal{N}$.
- **PROMPT_T09_11**: GNS operator representation: $\pi(w)[u] = [w u]$.
- **PROMPT_T09_12**: Well-definedness of GNS representation iff flat extension condition holds.
- **PROMPT_T09_13**: Algebraic obstruction to flat extension: proof that projector completeness forces rank growth.
- **PROMPT_T09_14**: Exact rational rank evaluation algorithm over $\mathbb{Q}$ using Gaussian row reduction.
- **PROMPT_T09_15**: Rust implementation of exact rational rank evaluator over `BigRational`.
- **PROMPT_T09_16**: Python implementation of exact rational rank evaluator over `Fraction`.
- **PROMPT_T09_17**: Negative control suite: rejecting rank over-claims or near-zero pivot misclassifications.
- **PROMPT_T09_18**: Proof that finite rank closure $\operatorname{rank}(M_d) = \operatorname{rank}(M_{d-1})$ implies finite-dimensional Hilbert space realization.
- **PROMPT_T09_19**: Dimension bound: if flat extension holds, $\dim(\mathcal{H}) = \operatorname{rank}(M_{d-1}) \ge 6$.
- **PROMPT_T09_20**: Lean 4 formalization of `RankLoopClosure` structure.
- **PROMPT_T09_21**: Lean 4 constructive theorem: `sound_universal_exclusion_via_rank_loop`.
- **PROMPT_T09_22**: Lean 4 proof of the Soundness Gap: `moment_positivity_soundness_gap`.
- **PROMPT_T09_23**: Axiom audit on rank-loop theorems: strictly `[propext, Quot.sound]`.
- **PROMPT_T09_24**: Integration of rank-loop diagnostics into the unified moment ledger API.
- **PROMPT_T09_25**: Master synthesis of the Rank-Loop Flat Extension & GNS Extraction analysis.

### Team 10: Fail-Closed Epistemic Gate, Smale $\alpha$-Theory Sentry, & Master Verification Synthesis
- **PROMPT_T10_01**: Formulation of the fail-closed epistemic audit schema: `SDPStatus`.
- **PROMPT_T10_02**: Definition of status `CERTIFIED_CANDIDATE_REFUTATION` for fixed candidate matrices.
- **PROMPT_T10_03**: Definition of status `MISSING_PROOF_OBLIGATION` for universal search claims without bridge.
- **PROMPT_T10_04**: Python implementation of `MissingProofObligationError` in `target_q5_moment_ledger.py`.
- **PROMPT_T10_05**: Rust implementation of `MomentSdpStatus::MissingProofObligation` in `mub6_moment_ledger.rs`.
- **PROMPT_T10_06**: Smale $\alpha$-theory sentry for complex polynomial systems over $\mathbb{C}^{50}$.
- **PROMPT_T10_07**: Calculation of Smale invariant $\alpha(x) = \beta(x) \gamma(x)$ for candidate 4th MUBs.
- **PROMPT_T10_08**: Proof that $\alpha(x) < (13 - 3\sqrt{17})/4 \approx 0.15767$ guarantees quadratic convergence to a true root.
- **PROMPT_T10_09**: Smale $\alpha$-theory rejection sentry: certifying that candidate completions have $\alpha > 1/2$ (no nearby zero).
- **PROMPT_T10_10**: Exact cyclotomic inner product verification engine over $\mathbb{Q}(\zeta_{24})$.
- **PROMPT_T10_11**: Rejection of approximate or floating-point unitary matrices by the exact cyclotomic sentry.
- **PROMPT_T10_12**: Master CLI verifier in Python: `mub6_verify_all.py` validating 24/24 certification steps.
- **PROMPT_T10_13**: Master native release binary in Rust: `omega_mub_verify_all.rs`.
- **PROMPT_T10_14**: Bit-for-bit SHA-256 digest matching across all canonical receipts in `artifacts/manifest.json`.
- **PROMPT_T10_15**: Full text claim hygiene regex audit across all project documentation and source code.
- **PROMPT_T10_16**: Verification of zero forbidden hype terms ("proves", "guarantees", "mathematically verifies", "fundamentally", "universal").
- **PROMPT_T10_17**: Verification of mandatory firewall line: `stated region only; mints no authority`.
- **PROMPT_T10_18**: Verification of `AuthorityEffect: None` in every emitted artifact, receipt, and transcript.
- **PROMPT_T10_19**: Lean 4 formalization of `fail_closed_epistemic_audit_soundness`.
- **PROMPT_T10_20**: Lean 4 formalization of `universal_exclusion_requires_bridge`.
- **PROMPT_T10_21**: Full Lean 4 package build audit: `lake build` with 0 sorry and standard foundational axioms.
- **PROMPT_T10_22**: Full Python regression suite verification: `python -m pytest tests/mub_verify -n 8`.
- **PROMPT_T10_23**: Full Rust test suite verification: `cargo test -p omega_mub --release`.
- **PROMPT_T10_24**: Reproducible release archive generation: `zenodo/mub6_formal_archive_v1.0.tar.gz`.
- **PROMPT_T10_25**: Master Grand Synthesis & Epistemic Gate Final Sign-Off.
