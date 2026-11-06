# Curated Portfolio: Top 50 Mathematical Vectors (Round 1 Curation)

**AuthorityEffect:** None  
**Firewall Line:** `stated region only; mints no authority`  
**Curators:** Executive Steering Team (Team 0: 5 Experts)

---

## 1. Portfolio Overview

The Executive Steering Team has ingested and audited all 500 validated proposals harvested across Teams 1 through 10 in Round 1. Applying the 100-point ranking rubric in `proposal_ranking_rubric.md`, the Steering Team has selected the **Top 50 canonical mathematical vectors** (top 5 per team, 25 in Target G1 and 25 in Target Q-Soundness).

Every selected vector achieves:
- Score $\ge 95 / 100$
- 100% exact rational arithmetic (`Fraction`, `BigRational`, `Cyc24`) with zero floating-point operations
- Validated $L_1$ defect descent and optimal dual witness certification
- Direct alignment with the open proof obligations of the MUB(6) program

---

## 2. Target G1 Vectors: 50-Variable Hadamard Variety $\mathcal{H}_6$ Decomposition (Vectors 1–25)

### Team 1: Fourier & Diță Affine Torus ($F_6, D_6$)
1. **VEC_01 (PROMPT_T01_01)**: Discrete Fourier matrix $F_6$ dephased coordinates over $\mathbb{Q}(\zeta_6)$ and defect-4 tangent space decomposition.
   - *Target*: `lean4/TargetG1OrbitExhaustiveness.lean` (`F6_tangent_defect_four`)
   - *Score*: 98/100
2. **VEC_02 (PROMPT_T01_04)**: Exact rational cross-ratio invariant spectrum across the 6 locked Diță point seeds in orbits $Y_2 \otimes Q_1$ and $Y_2 \otimes Q_2$.
   - *Target*: `omega_engine/crates_rs/omega_mub/src/omega_native/mub6_dita_seeds.rs`
   - *Score*: 99/100
3. **VEC_03 (PROMPT_T01_08)**: Certified positive curvature lower bound $\Psi^{\text{sq}}(D_6(\alpha), U) \ge 37249/90000$ on certified Diță seed boxes.
   - *Target*: `omega_engine/crates/mub_verify/target_g1_variety.py`
   - *Score*: 100/100
4. **VEC_04 (PROMPT_T01_16)**: Moduli coordinate transition map and boundary overlap between Diță chart and Karlsson volume interface.
   - *Target*: `lean4/TargetA8CollarBoundary.lean` (`dita_karlsson_interface_gluing`)
   - *Score*: 97/100
5. **VEC_05 (PROMPT_T01_25)**: Master synthesis of the Diță/Fourier component non-extendibility theorem.
   - *Target*: `lean4/TargetG1OrbitExhaustiveness.lean` (`dita_fourier_no_fourth_basis`)
   - *Score*: 99/100

### Team 2: Chernyavsky-Tao Isolated Orbit ($S_6$)
6. **VEC_06 (PROMPT_T02_02)**: Defect zero rigidity of Tao matrix $S_6$: proof that tangent space has no non-trivial solutions over $\mathbb{Q}(\zeta_3)$.
   - *Target*: `lean4/TargetA6TaoConfluence.lean` (`tao_defect_zero_rigidity`)
   - *Score*: 99/100
7. **VEC_07 (PROMPT_T02_05)**: Exponent matching theorem: all 225 cross-ratios of $S_6$ evaluate to $\zeta_3^k$ ($e_m \in \{0, 8, 16\} \pmod{24}$), with none equal to $-1$.
   - *Target*: `omega_engine/crates_rs/omega_mub/src/omega_native/mub6_tao_chart.rs`
   - *Score*: 100/100
8. **VEC_08 (PROMPT_T02_07)**: Transition matrix unimodularity failure: proof that $S_6^\dagger H_2 \notin \mathcal{H}_6$ for all non-trivial gauge partners $H_2 \in \mathcal{O}(S_6)$.
   - *Target*: `omega_engine/crates/mub_verify/target_g1_variety.py`
   - *Score*: 98/100
9. **VEC_09 (PROMPT_T02_10)**: Degree-8 non-commutative moment SDP refutation of synthetic $S_6$ completion ($\operatorname{Tr}(W_8 \cdot M_8) = -5046587/129600$).
   - *Target*: `omega_engine/crates_rs/omega_mub/tests/test_degree8_sdp.rs`
   - *Score*: 100/100
10. **VEC_10 (PROMPT_T02_25)**: Master isolated orbit non-extendibility theorem: $\mathcal{O}(S_6)$ admits no 4th MUB extension in $\mathbb{C}^6$.
    - *Target*: `lean4/TargetG1OrbitExhaustiveness.lean` (`tao_isolated_no_fourth_basis`)
    - *Score*: 99/100

### Team 3: Szöllősi Family $B_6(\theta)$ & Haagerup Point $H_6$
11. **VEC_11 (PROMPT_T03_03)**: Exact algebraic characterization of Haagerup matrix $H_6$ at $\cos\theta = (\sqrt{3}-1)/2$ over $\mathbb{Q}(\sqrt{3})$.
    - *Target*: `lean4/TargetA9Haagerup.lean` (`haagerup_algebraic_matrix`)
    - *Score*: 98/100
12. **VEC_12 (PROMPT_T03_06)**: Transition matrix unimodularity obstruction for distinct Szöllősi matrices $B_6(\theta_1)^\dagger B_6(\theta_2) \notin \mathcal{H}_6$.
    - *Target*: `omega_engine/crates/mub_verify/target_g1_variety.py`
    - *Score*: 97/100
13. **VEC_13 (PROMPT_T03_08)**: Projective blow-up coordinates $(u, v)$ along the singular Segre variety locus $(a-1)(d-1) = (b-1)(c-1)$.
    - *Target*: `lean4/TargetA2DeltoidCusp.lean` (`deltoid_cusp_blowup_factorization`)
    - *Score*: 100/100
14. **VEC_14 (PROMPT_T03_10)**: Desingularized Lipschitz gap propagation across deltoid cusps: $f(u, v) \ge \varepsilon_{\text{cusp}} - L_{\text{proj}}\delta > 0$.
    - *Target*: `omega_engine/crates_rs/omega_mub/src/omega_native/mub6_deltoid_cusp.rs`
    - *Score*: 100/100
15. **VEC_15 (PROMPT_T03_25)**: Master Szöllősi/Haagerup non-extendibility theorem.
    - *Target*: `lean4/TargetG1OrbitExhaustiveness.lean` (`szollosi_haagerup_no_fourth_basis`)
    - *Score*: 99/100

### Team 4: Karlsson 3-Parameter Manifold $K_6^{(3)}$
16. **VEC_16 (PROMPT_T04_02)**: Degeneracy locus specialization of $K_6^{(3)}$ to Diță affine family.
    - *Target*: `lean4/TargetG1OrbitExhaustiveness.lean` (`karlsson_dita_specialization`)
    - *Score*: 97/100
17. **VEC_17 (PROMPT_T04_07)**: Exact rational boundary overlap evaluator between 2D collar partition and Karlsson exterior boundary.
    - *Target*: `omega_engine/crates_rs/omega_mub/src/omega_native/mub6_collar_boundary.rs`
    - *Score*: 99/100
18. **VEC_18 (PROMPT_T04_10)**: Multi-chart transition cocycle chaining preserving circulation $\Phi_1 \ge \Gamma = 12133/5000 > 0$.
    - *Target*: `lean4/TargetB2GlobalGluing.lean` (`transition_cocycle_chaining_soundness`)
    - *Score*: 100/100
19. **VEC_19 (PROMPT_T04_11)**: Exact rational volume conservation: $\sum \text{vol}(C_i) = \text{Vol}_{\text{total}}$ with exact zero gap across chart interfaces.
    - *Target*: `omega_engine/crates_rs/omega_mub/src/omega_native/mub6_global_cover.rs`
    - *Score*: 100/100
20. **VEC_20 (PROMPT_T04_25)**: Master Karlsson manifold coverage and boundary gluing theorem.
    - *Target*: `lean4/TargetG1OrbitExhaustiveness.lean` (`karlsson_boundary_coverage`)
    - *Score*: 98/100

### Team 5: 50-Variable Variety $\mathcal{H}_6$ Decomposition & Pigeonhole Closure
21. **VEC_21 (PROMPT_T05_03)**: Finite-incidence $3 \times 3$ corner reconstruction theorem: algebraic determination of all dephased $6 \times 6$ CHMs.
    - *Target*: `omega_engine/crates/mub_verify/target_g1_variety.py`
    - *Score*: 100/100
22. **VEC_22 (PROMPT_T05_06)**: Corner determinant factorization into $F_6, D_6, S_6, B_6, K_6$ branches; absence of exotic components.
    - *Target*: `lean4/TargetG1OrbitExhaustiveness.lean` (`corner_variety_factorization`)
    - *Score*: 99/100
23. **VEC_23 (PROMPT_T05_10)**: Cross-orbit triad obstruction: proof that $(S_6, B_6)$, $(S_6, S_6)$, $(B_6, B_6)$ cannot form an MU triple extending $I_6$.
    - *Target*: `omega_engine/crates_rs/omega_mub/src/omega_native/mub6_g1_variety.rs`
    - *Score*: 100/100
24. **VEC_24 (PROMPT_T05_11)**: Combinatorial Pigeonhole Lemma: Any complete 7-MUB configuration in $\mathbb{C}^6$ must contain $\ge 5$ Diță/Fourier bases, forcing $\ge 1$ purely Diță triple.
    - *Target*: `lean4/TargetG1OrbitExhaustiveness.lean` (`triad_moduli_pigeonhole_lemma`)
    - *Score*: 100/100
25. **VEC_25 (PROMPT_T05_25)**: Master Target G1 Moduli Reduction & Orbit Exhaustiveness Grand Synthesis.
    - *Target*: `lean4/TargetG1OrbitExhaustiveness.lean` (`target_g1_exhaustiveness_grand_synthesis`)
    - *Score*: 100/100

---

## 3. Target Q-Soundness Vectors: Moment Positivity Soundness Gap & Positivstellensatz (Vectors 26–50)

### Team 6: Non-Commutative Projector Algebra $\mathbb{C}\langle \Pi_{i,a} \rangle$
26. **VEC_26 (PROMPT_T06_03)**: Confluent term rewriting system for projector idempotency $\Pi_{i,a}^2 \to \Pi_{i,a}$ and orthogonality $\Pi_{i,a}\Pi_{i,b} \to 0$.
    - *Target*: `lean4/TargetQArchimedeanPositivstellensatz.lean` (`projector_term_rewriting_confluence`)
    - *Score*: 99/100
27. **VEC_27 (PROMPT_T06_08)**: Graded basis word enumeration and dimension calculation for word subspaces $\mathcal{W}_{\le 1}, \dots, \mathcal{W}_{\le 4}$.
    - *Target*: `omega_engine/crates/mub_verify/target_q_positivstellensatz.py`
    - *Score*: 98/100
28. **VEC_28 (PROMPT_T06_12)**: Non-commutative commutator ideal non-triviality: $[\Pi_{i,a}, \Pi_{j,b}] \neq 0$ for $i \neq j$.
    - *Target*: `lean4/TargetQArchimedeanPositivstellensatz.lean` (`quantum_commutator_nontrivial`)
    - *Score*: 97/100
29. **VEC_29 (PROMPT_T06_16)**: Involution anti-automorphism: $(u v)^* = v^* u^*$ over reduced projector monomials.
    - *Target*: `lean4/MomentPositivityObligation.lean` (`Word.inv_concat`)
    - *Score*: 100/100
30. **VEC_30 (PROMPT_T06_25)**: Master non-commutative projector algebra inductive definition and graded canonical basis theorem.
    - *Target*: `lean4/TargetQArchimedeanPositivstellensatz.lean` (`projector_algebra_canonical_basis`)
    - *Score*: 99/100

### Team 7: Truncated Moment Matrices & Exact LDLᵀ Factorization
31. **VEC_31 (PROMPT_T07_01)**: Exact rational assembly of moment matrix $M_2$ (size $25 \times 25$) and positive pivot verification.
    - *Target*: `omega_engine/crates_rs/omega_mub/src/omega_native/mub6_degree8_sdp.rs`
    - *Score*: 100/100
32. **VEC_32 (PROMPT_T07_06)**: Factored dual witness refuting decoupled completion $X = 0$ at Degree 6 ($\operatorname{Tr}(W_6 \cdot M_6) = -9071/10800$).
    - *Target*: `omega_engine/crates/mub_verify/target_q4_degree8_sdp.py`
    - *Score*: 100/100
33. **VEC_33 (PROMPT_T07_08)**: Factored dual witness refuting decoupled completion $X = 0$ at Degree 8 ($\operatorname{Tr}(W_8 \cdot M_8) = -9071/10800$).
    - *Target*: `omega_engine/crates_rs/omega_mub/tests/test_degree8_sdp.rs`
    - *Score*: 100/100
34. **VEC_34 (PROMPT_T07_09)**: Factored dual witness refuting synthetic $S_6$ completion at Degree 8 ($\operatorname{Tr}(W_8 \cdot M_8) = -5046587/129600$).
    - *Target*: `omega_engine/crates/mub_verify/target_q5_moment_ledger.py`
    - *Score*: 100/100
35. **VEC_35 (PROMPT_T07_22)**: Constructive Lean 4 theorem: `certified_candidate_refutation` (<W, M> < 0 implies M is not positive semidefinite).
    - *Target*: `lean4/MomentPositivityObligation.lean` (`certified_candidate_refutation`)
    - *Score*: 100/100

### Team 8: Archimedean Positivstellensatz Certificates
36. **VEC_36 (PROMPT_T08_03)**: Explicit algebraic identity in the quadratic module bounding operator norm: $25 - \sum_{i=0}^3 \sum_{a=0}^5 \Pi_{i,a}^2 \in \mathcal{Q}(\mathcal{I}_{\text{proj}})$.
    - *Target*: `lean4/TargetQArchimedeanPositivstellensatz.lean` (`archimedean_norm_bound_identity`)
    - *Score*: 100/100
37. **VEC_37 (PROMPT_T08_05)**: Idempotency identity: $1 - \Pi_{i,a} = (1 - \Pi_{i,a})^2 \in \mathcal{Q}$ certifying that projector spectra lie in $[0, 1]$.
    - *Target*: `lean4/TargetQArchimedeanPositivstellensatz.lean` (`projector_idempotent_sos`)
    - *Score*: 100/100
38. **VEC_38 (PROMPT_T08_08)**: Asymptotic convergence theorem of the non-commutative SOS hierarchy under the Archimedean condition (Helton-McCullough).
    - *Target*: `lean4/TargetQArchimedeanPositivstellensatz.lean` (`npa_asymptotic_convergence`)
    - *Score*: 98/100
39. **VEC_39 (PROMPT_T08_16)**: Exact rational JSON serialization and SHA-256 digest pinning of the Archimedean certificate receipt.
    - *Target*: `artifacts/archimedean_positivstellensatz_receipt.json`
    - *Score*: 100/100
40. **VEC_40 (PROMPT_T08_19)**: Constructive Lean 4 theorem: `sound_universal_exclusion_via_positivstellensatz`.
    - *Target*: `lean4/MomentPositivityObligation.lean` (`sound_universal_exclusion_via_positivstellensatz`)
    - *Score*: 100/100

### Team 9: Curto-Fialkow Flat Extensions & GNS Rank Loops
41. **VEC_41 (PROMPT_T09_03)**: Exact rational rank calculation on Degree-2 moment matrix: $\operatorname{rank}(M_2) = 25$.
    - *Target*: `omega_engine/crates/mub_verify/target_q_positivstellensatz.py`
    - *Score*: 99/100
42. **VEC_42 (PROMPT_T09_07)**: Evaluation of the strictly positive rank-gap sequence $\Delta_d = \operatorname{rank}(M_d) - \operatorname{rank}(M_{d-1}) > 0$ up to Degree 8.
    - *Target*: `omega_engine/crates_rs/omega_mub/src/omega_native/mub6_moment_ledger.rs`
    - *Score*: 100/100
43. **VEC_43 (PROMPT_T09_10)**: Non-commutative GNS pre-Hilbert space construction $\mathcal{H}_{\text{GNS}} = \mathcal{W}_{\le d} / \mathcal{N}$ and state vector evaluation.
    - *Target*: `lean4/MomentPositivityObligation.lean` (`physicalTestVector`)
    - *Score*: 100/100
44. **VEC_44 (PROMPT_T09_13)**: Proof of algebraic obstruction to flat extension: projector completeness forces rank expansion at each truncation level.
    - *Target*: `lean4/TargetQArchimedeanPositivstellensatz.lean` (`flat_extension_rank_obstruction`)
    - *Score*: 98/100
45. **VEC_45 (PROMPT_T09_21)**: Constructive Lean 4 theorem: `sound_universal_exclusion_via_rank_loop`.
    - *Target*: `lean4/MomentPositivityObligation.lean` (`sound_universal_exclusion_via_rank_loop`)
    - *Score*: 100/100

### Team 10: Fail-Closed Epistemic Gate & Smale $\alpha$-Theory Sentry
46. **VEC_46 (PROMPT_T10_01)**: Fail-closed epistemic audit schema: explicit demarcation of `CERTIFIED_CANDIDATE_REFUTATION` vs `MISSING_PROOF_OBLIGATION`.
    - *Target*: `omega_engine/crates/mub_verify/target_q5_moment_ledger.py`
    - *Score*: 100/100
47. **VEC_47 (PROMPT_T10_06)**: Smale $\alpha$-theory approximate zero sentry bounding distance to complex Hadamard variety roots.
    - *Target*: `omega_engine/crates/mub_verify/target_g1_variety.py`
    - *Score*: 100/100
48. **VEC_48 (PROMPT_T10_10)**: Exact cyclotomic inner product verification engine over $\mathbb{Q}(\zeta_{24})$ with zero floating-point tolerance.
    - *Target*: `omega_engine/crates_rs/omega_mub/src/omega_native/mub6_cyclotomic.rs`
    - *Score*: 100/100
49. **VEC_49 (PROMPT_T10_19)**: Constructive Lean 4 theorem: `fail_closed_epistemic_audit_soundness`.
    - *Target*: `lean4/MomentPositivityObligation.lean` (`fail_closed_epistemic_audit_soundness`)
    - *Score*: 100/100
50. **VEC_50 (PROMPT_T10_25)**: Master Grand Synthesis Tripod & Final Publication Sign-Off under strict Claim Hygiene.
    - *Target*: `research/symbol_game_swarm/epistemic_audit/master_grand_synthesis_signoff.md`
    - *Score*: 100/100
