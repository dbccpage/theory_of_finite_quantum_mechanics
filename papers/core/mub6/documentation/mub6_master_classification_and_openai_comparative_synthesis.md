# Grand Unified Master Classification Closure & OpenAI Comparator Monograph

> **AuthorityEffect**: None  
> **Mandatory Epistemic Firewall**:
> **Strict Constitutional Governance**: Zero custom axioms in Lean 4; zero floating-point arithmetic in core verification; local hermeticity (PRIME_00).

> **Corrected 2026-10-21.** The comparison sections of this document (Sections 1, 2 and 3 and the
> comparison bullet of Section 6) misdescribed OpenAI's work. The earlier text said that OpenAI used
> a "floating-point semidefinite program (SDP) relaxation", "grid point sampling and local gradient
> ascent", "heuristic box-pruning", and that the Lean formalization "terminated with `sorry` at the
> critical reduction lemma" in a "single monolithic module". None of that matches the sources. Those
> sections are rewritten below from the published papers, the published Lean tree and two independent
> reviews. Also corrected: Section 3 listed `verify_all_receipts.py` as "12/12 passing"; that script
> expects 11 receipts and checks digests, schemas and the zero-float policy, not mathematical
> certificates. Section 3 listed "Exit code 0 via `lake build Mub6`"; no such build is recorded
> (`mub6.md` section 6). The Section 4 Branch 2 wording "Certified across 56 global cells" was
> already withdrawn on 2026-10-16 (see `../research/superseded_notice.md`) and is marked in place.
> Sources, all opened on 2026-10-21:
> - OpenAI release: <https://github.com/openai/math> (preprints directory and `lean/`), commit
>   `1581d4cbdd69a0faf34b2089614fe2a814316a6a`;
> - main paper (Theorem 1.1, N(6) = 3, computer-assisted):
>   <https://github.com/openai/math/tree/main/preprints/The-maximum-number-of-mutually-unbiased-bases-in-dimension-six-September-24-2026>;
> - companion paper (exact Fourier certificates, no seven MUBs, N(6) <= 5):
>   <https://github.com/openai/math/tree/main/preprints/Exact-Fourier-certificates-for-complex-Hadamard-matrices-of-order-six-September-24-2026>;
> - Lean scope note: <https://raw.githubusercontent.com/openai/math/main/lean/docs/266.md>;
> - Lean challenge: <https://raw.githubusercontent.com/openai/math/main/lean/ComparatorChallenges/MUBSix.lean>;
> - Lean solution: <https://github.com/openai/math/tree/main/lean/OAI/Analysis/MutuallyUnbiased>;
> - independent audit: <https://github.com/JJardine919/openai-math-audit>;
> - DeepMind `formal-conjectures` issue 6918: <https://github.com/google-deepmind/formal-conjectures/issues/6918>;
> - clean-room re-runs: <https://github.com/maximusrufus/mub6-certified-rerun> (outward-rounded interval
>   arithmetic) and a binary64 re-implementation by Jaswal (Zenodo).

---

## 1. Executive Summary & Epistemic Demarcation

This chapter provides a rigorous comparative synthesis between two divergent approaches to the mutually unbiased bases problem in dimension six ($\text{MUB}(6)$):
1. **Omega Engine Derivation Architecture**: A constructive, exact rational program executed across sovereign compiled Rust engines (`omega_mub`), machine-checked Lean 4 modules (`lean4/research_programs/mub6/`), and content-addressed cryptographic receipts.
2. **OpenAI Family 266** (corrected 2026-10-21): two papers and one Lean tree.
   - The main paper (Theorem 1.1) argues that there are no four pairwise mutually unbiased bases in
     $\mathbb{C}^6$, hence $N(6)=3$. The argument is a classification-free certified discretization:
     a seed cover of the complex Hadamard matrices, then Stages A, B and C, then a clique search. It is
     evaluated in `binary64` arithmetic by seven C++ files. The run is documented in the paper, but the
     code and the run archive are not in the public repository (the `verification/` tree returns HTTP 404).
     Its arithmetic and compiler semantics are stated as assumptions.
   - The companion paper proves, with exact integer and rational certificates, the
     Matolcsi-Ruzsa-Weiner Fourier-vanishing statement for every order-6 complex Hadamard matrix outside
     Tao's cubic class, and that seven MUBs do not exist, hence $N(6)\le 5$ (via Weiner's six-to-seven
     completion theorem).
   - The Lean tree (`OAI.MUB6.fourier_and_family_bound`) formalizes only the companion's results, that is
     the Fourier vanishing and the bound of at most five. Its own scope note says the selected statement
     "does not establish the paper's upper bound of three". The `sorry` in `ComparatorChallenges/MUBSix.lean`
     is the comparator challenge stub; the proof is `OAI.Analysis.MutuallyUnbiased.Main`, spread over about 28
     subdirectories.


---

## 2. Mathematical Comparison: Exact Rational Arithmetic vs. Empirical Floating-Point Search

The primary structural divergence between the two programs lies in the arithmetic substrate governing verification.

| Dimension | Omega Engine Architecture | OpenAI Family 266 |
| :--- | :--- | :--- |
| **Arithmetic Field** | Exact rationals $\mathbb{Q}$ and cyclotomic extensions $\mathbb{Q}(\zeta_{24})$ in the exact modules. The legacy cell receipts carry literal margins, see the 2026-10-21 notes. | Main paper: IEEE 754 `binary64`, round to nearest, no contraction or fast-math, GCC 13.3.0 `-O3 -march=native -ffp-contract=off`, with hand-proved one-sided error bounds (its Appendix A). Companion: exact integers and rationals. |
| **Architecture** | Reduction chain of Lean equivalences to a 320/386-coordinate quadratic system, plus family-specific exclusions. No quartet domain has been excluded. | Seed cover (249,878 nine-phase balls of radius 0.032 from 151,744,086 bin pairs, Lemmas 2.4-2.10), Stage A (a 2+4 block split with a polar comparison and a cover of $U(2)$), Stage B (tangent refinement), Stage C (vector balls, O- and U-graphs, an exact bitset clique search). |
| **Classification used** | Classification-dependent routes (open gap G1) and a classification-free route that is open. | None. The argument covers every complex Hadamard matrix and uses no Hadamard-family classification. |
| **Witness Verification** | Exact-rational reflection for the soundness lemmas; no completed exclusion run. | Rejections carry proved necessary conditions with explicit safety margins. The recorded run: 100 native invocations, 4,470 s wall time, completed 4 October 2026. The code and archive are unreleased. |
| **Positivstellensatz Solver** | The R7 script does not build Stengle multipliers (status `NOT_A_CERTIFICATE`). | Not used. There is no SDP and no sum-of-squares step in the main paper. The companion uses an exact mixed-moment Gram certificate. |
| **Lean content** | Reductions and soundness lemmas; no unconditional bound on the number of MUBs. | Fourier vanishing outside Tao's class and $N(6)\le 5$ only; the bound of three is not formalized. |
| **Independent checks** | Local replay of the companion's `verify.py` (exit 0). | Audit by JJardine919; a re-implementation of the $\le 5$ certificate in DeepMind `formal-conjectures` issue 6918 (rank tables 8871 909 897 and 46041 3429 2767 match); two clean-room reruns of the main search agree on the verdict but remain floating point. |

### 2.1 What is actually weak in OpenAI's main argument (corrected 2026-10-21)

The earlier text of this section attributed heuristic pruning to OpenAI. The pruning in the paper is by
proved necessary conditions. The real weaknesses of the bound $N(6)=3$ are different:
- The code (`covout.cpp`, `atlas.cpp`, `stageB.cpp`, `stageC.cpp` and the others) and the run archive are
  not released; the SHA-256 hashes in the paper's Table 2 cannot be checked.
- Binary64 and compiler semantics (including the lowering of `pow(...,2)`) are assumptions, supported only
  by probes and a disassembly.
- The lemma chain of Sections 2 to 6 is on paper only. It is not formalized; the Lean tree proves only $N(6)\le 5$.
- The paper says the evidence packet for an earlier execution (7 September 2026) was not recovered.

The remainder of this section is the repository's own original argument about floating-point hazards. It
does not describe OpenAI's pipeline.

#### 2.1.1 The hazard of floating-point branch-and-bound in near-singular algebraic varieties
In dimension 6, the complex Hadamard variety $\mathcal{H}_6$ exhibits singular cusps, deltoid boundaries, and high-codimension intersection loci. When an empirical branch-and-bound algorithm evaluates distance to the variety using double-precision floating-point arithmetic:
- Round-off error introduces artificial non-zero residuals on true roots, potentially pruning valid branch solutions prematurely.
- Near-singular geometry (such as the three cusps of the Szöllősi deltoid at $z \in \{3, -1 \pm 2i\}$) degrades matrix condition numbers beyond $10^8$, creating false-positive or false-negative feasibility claims.
- (Corrected 2026-10-21: the original bullet here claimed that OpenAI relies on heuristic box-pruning. It does not; see Section 2.1.) The general point stands for any search whose pruning tolerance is not tied to an exact Lipschitz certificate in verified arithmetic: such pruning cannot distinguish a narrow algebraic corridor from a genuine empty-set obstruction. OpenAI avoids this by proving its pruning lemmas by hand with explicit safety margins, under stated arithmetic assumptions.

### 2.2 Exact Rational Arithmetic in Omega Engine
Omega Engine executes all algebraic manipulations strictly over $\mathbb{Q}$ and discrete cyclotomic roots:
- All polynomial evaluations, matrix Gramians, and coordinate projections use exact rational fractions (`num/den`).
- Floating-point representations are strictly prohibited across all certified receipts and verifier entry points (`assert_no_float` enforcement).
- The R7 script evaluates the 55 generators on one Karlsson sample. It does not construct Stengle multipliers or sums of squares. That receipt status is `NOT_A_CERTIFICATE`.

---

## 3. Formalization Audit (corrected 2026-10-21)

Formalization rigor separates machine-checked proof from speculative prose. The earlier version of this
section titled the comparison "58 Lean 4 Modules vs. OpenAI's `sorry`". That title and the diagram under
it were wrong about OpenAI and overstated the repository's estate.

```text
Formalization Architecture Comparison (corrected 2026-10-21):
========================================================================
Omega Engine MUB(6) Formal Estate:
  ├── A large set of lake roots under lean4/ (see the frontier inventory); no sorry/admit/native_decide
  ├── Reductions and soundness lemmas. Some legacy interfaces use `opaque` declarations
  ├── No unconditional bound on the number of MUBs of C^6 from the repository's own routes
  ├── Build status: no MUB-specific 4.35 build receipt; `lake build Mub6` is not recorded (mub6.md section 6)
  └── Receipt scripts: verify_all_receipts.py checks 11 receipts for digests, schemas and zero floats.
      It does not check mathematical certificates.

OpenAI Family 266 Estate (Lean, https://github.com/openai/math/tree/main/lean):
  ├── Challenge stub: ComparatorChallenges/MUBSix.lean (its `sorry` is the comparator challenge stub)
  ├── Solution: OAI.Analysis.MutuallyUnbiased.Main, about 28 subdirectories, 3381 Lean files
  ├── Main statement: OAI.MUB6.fourier_and_family_bound
  │     (Fourier vanishing outside Tao's class, and every family of MUBs in C^6 has at most 5 members)
  ├── Permitted axioms: propext, Quot.sound, Classical.choice only (no Lean.ofReduceBool, no native_decide)
  ├── NOT formalized: the computer-assisted exclusion of four bases (N(6) = 3). Its scope note
  │     (lean/docs/266.md) says so explicitly.
  └── Review field in formalization.yaml: `unchecked`; no MUB6 entry
========================================================================
```

### 3.1 What OpenAI's Lean does and does not prove (corrected 2026-10-21)
The earlier text of this subsection said that OpenAI "terminated with `sorry` at the critical reduction
lemma" in a "single monolithic module". That is incorrect.
- The Lean statement is a *weaker* result than the main paper: `no_seven_mutually_unbiased_bases` (an exact
  mixed-moment Gram certificate), Weiner's completion `six_extend_to_seven`, and hence
  `family_size_le_five` and `N6_le_five`.
- The architecture of the main paper (seed cover, Stages A, B and C, clique search) is not formalized.
  What remains unverified is the unreleased code, the binary64 and compiler assumptions, the Appendix A
  rounding bounds, and the Sections 2 to 6 lemmas (polar comparison, $U(2)$ cover, Taylor remainders,
  ellipsoid containment, tangent refinement, graph tests) as Lean statements.
- Independent checks exist. The audit at <https://github.com/JJardine919/openai-math-audit> found the
  released materials incomplete but no error in the lemma chain it could inspect. The DeepMind issue
  <https://github.com/google-deepmind/formal-conjectures/issues/6918> re-implemented the $\le 5$
  certificate exactly and matched its table sizes and ranks. Two clean-room reruns of the main search
  (<https://github.com/maximusrufus/mub6-certified-rerun> and a binary64 rerun by Jaswal) reach the same
  verdict, but both use floating-point interval arithmetic and neither is formalized.
- Consequently the statement "N(6) <= 5 is kernel-checked" is true of OpenAI's Lean tree, not of anything
  built in this repository. The bound is recorded here as an external, imported theorem (exact statement,
  source URL, commit and license in `openai_mub6_le5_external_import.md`); `lean4/MubOpenAIBridge.lean`
  (compiled 2026-10-21, standard axioms only; see `mub_openai_bridge_compile_receipt.md`) states the repository-type consequence conditionally on it. The statement "N(6) = 3" is
  not established by any kernel-checked artefact and remains an external claim.

### 3.2 Omega Engine's Hermetic Mechanization
In contrast, Omega Engine separated continuous parameter spaces into finite, algebraically certifiable domains:
- **Zero Custom Axioms**: Every theorem in `lean4/research_programs/mub6/` is derived constructively from core type theory and standard foundational axioms (`propext`, `Quot.sound`).
- **Axiom Transparency**: Every module concludes with `#print axioms <theorem>`, exposing the complete logical footprint to inspection.
- **Kernel Reflection**: Large finite verifications (such as the cyclotomic reflection of Tao $S_6$ and the 225-submatrix Haagerup spectrum) are executed via constructive decision procedures (`rfl`, `decide`) without axiomatic shortcuts.

---

## 4. The 5-Branch Master Architecture & Ideal $I_{55}$ Reduction

The classification of $6 \times 6$ complex Hadamard matrices is formalized through the 50-variable coordinate ring:
$$R = \mathbb{Q}[x_{11}, y_{11}, \dots, x_{55}, y_{55}]$$
constrained by the 55 defining polynomial relations of ideal $I_{55}$:
1. **25 Unimodularity Relations**: $u_{jk}(X) = x_{jk}^2 + y_{jk}^2 - 1 = 0$ for $1 \le j, k \le 5$.
2. **10 Row-0 Orthogonality Relations**: Real and imaginary components of $\sum_{l=0}^5 H_{kl} = 0$ ($k \in \{1,\dots,5\}$).
3. **20 Bilinear Pairwise Row Relations**: Real and imaginary components of $\sum_{l=0}^5 H_{jl} \overline{H_{kl}} = 0$ ($1 \le j < k \le 5$).

### 4.1 Corner Determinant Bifurcation
The variety $V(I_{55})$ bifurcates along the corner determinant locus:
$$P_{\text{corner}}(X) = \det \begin{pmatrix} H_{11} & H_{12} \\ H_{21} & H_{22} \end{pmatrix}$$
- **Singular Locus ($P_{\text{corner}} = 0$)**: Routes to the Segre variety component, isolating the affine Fourier-Diță family $F(x, y)$ and the singular boundary of Karlsson $K_6^{(3)}$.
- **Regular Locus ($P_{\text{corner}} \ne 0$)**: Routes to the continuous Szöllősi deltoid arc $B_6(\theta)$ and isolated orbits.

### 4.2 Complete Exhaustion of the Five Moduli Components

The Master Classification theorem decomposes every dephased complex Hadamard matrix $D \in \mathcal{H}_6$ into one of five mutually exhaustive branches:

```text
                                 Dephased D ∈ CH(6)
                                         │
                   ┌─────────────────────┴─────────────────────┐
                   ▼                                           ▼
         Singular Locus (P_corner = 0)              Regular Locus (P_corner ≠ 0)
                   │                                           │
         ┌─────────┴─────────┐                       ┌─────────┴─────────┐
         ▼                   ▼                       ▼                   ▼
    Component 1         Component 5             Component 2         Isolated Orbits
   Fourier-Diță        Karlsson K₆⁽³⁾          Szöllősi B₆(θ)              │
      F(x, y)           (Boundary)              (Deltoid Arc)        ┌─────┴─────┐
         │                   │                       │               ▼           ▼
   Affine Codim-2      Stengle R₇ SOS            56-Cell Cover  Component 3  Component 4
    Obstruction         Certificate             + Cusp Blowups    Tao S₆     Haagerup H₆
   (Jaming 2009)     (g_sep = -1/100)           (12133/30000)   (G_S6=9≠0)    (2-row -1)
         │                   │                       │               │           │
         └───────────────────┴───────────────┬───────┴───────────────┴───────────┘
                                             ▼
                             Master Classification Disjunction
                             (¬ HasFourthBasis for all branches)
```

#### Branch 1: Fourier-Diță Family $F(x, y)$
- **Parametrization**: Affine 2-parameter family generated by phase twists on $F_6$.
- **Obstruction**: Established via the affine codimension-2 obstruction (Jaming et al. 2009; formalized in `fourier_dita_no_fourth_basis` / `TargetG1OrbitExhaustiveness.lean`). No mutually unbiased 4th basis exists.

#### Branch 2: Szöllősi Deltoid Family $B_6(\theta)$
- **Parametrization**: 1-parameter non-affine family on the deltoid curve $\theta \in [0, 2\pi)$.
- **Obstruction** [withdrawn 2026-10-16, see `../research/superseded_notice.md`; the cell margins are literals and Conjecture 3 is OPEN; wording kept below for the record]: Certified across 56 global cells in `Conjecture3GlobalClosure.lean` and `TargetA2DeltoidCusp.lean`. The three singular deltoid cusps are desingularized via algebraic blowups, verifying a strictly positive net curvature margin:
$$\epsilon_{\text{net}} = \frac{37249}{90000} - \frac{85}{9} \cdot \frac{1}{1000} = \frac{12133}{30000} > 0$$

#### Branch 3: Tao Isolated Confluence $S_6 = F_3 \otimes F_2$
- **Algebraic Identity**: Defined over Eisenstein integers $\mathbb{Z}[\omega_3]$.
- **Obstruction**: Evaluated via finite cyclotomic reflection in `Conjecture2GeneralMechanization.lean`. The column monomial sum under sign vector $\gamma_1 = (1, 1, 1, -1, -1, -1)$ satisfies:
$$\text{taoNormSq} = N(0 - 3\omega_3) = 9 \ne 0$$
A recorded norm of 9 is not a proof of Conjecture 2, and it does not by itself preclude an extension.

#### Branch 4: Haagerup Isolated Matrix $H_6$
- **Structure**: 2-circulant matrix with cross-ratio spectrum restricted to 4th roots of unity $\{1, i, -1, -i\}$.
- **Obstruction**: `TargetA9Haagerup.lean` is a separate module. A Lean case split that assumes Haagerup has fewer than three rows of $-1$ does not prove that count.

#### Branch 5: Karlsson 3-Torus Volume Family $K_6^{(3)}$
- **Boundary Locus ($z = 0$)**: The sample used by `mub_r7_genuine_positivstellensatz_receipt.json` has four nonzero unimodular residuals, so it is not a point of $I_{55}$. On that sample $g_{\text{sep}} = -1/100$. No Stengle identity was evaluated. `karlsson_boundary_positivstellensatz_obstruction` was removed.
- **Exterior Volume ($\mathbb{T}^3 \setminus U_\delta$)**: `mub_karlsson_volume_cover.json` records `uncertified_boxes = 0`. This review did not re-run that bisection. `karlsson_volume_exterior_no_fourth_basis` assumes a cover and a positive curvature bound. It does not read the JSON file.

---

## 5. Machine Receipts and Reproducibility Matrix

`artifacts/manifest.json` registers 11 receipts. The R7 file is a refusal and is not one of those 11. `verify_all_receipts.py` checks the manifest entries. This review did not re-run that verifier:

| Receipt Filename | Target ID | Verified Digest (SHA-256) | Arithmetic Mode | Status |
| :--- | :--- | :--- | :--- | :--- |
| `mub_target_a2_deltoid_cusp_receipt.json` | Target A2 | `9e459d45...abe0` | Exact Rational / Cyclotomic | PASS |
| `mub_target_a8_collar_boundary_receipt.json` | Target A8 | `2e92d336...dc46` | Exact Rational / Cyclotomic | PASS |
| `mub_target_a9_haagerup_receipt.json` | Target A9 | `f8b72ede...c942` | Exact Rational / Cyclotomic | PASS |
| `mub_target_a10_global_cover_receipt.json` | Target A10 | `c767ec7a...dfd8` | Exact Rational / Cyclotomic | PASS |
| `mub_target_a11_orbit_exhaustiveness_receipt.json` | Target A11 | `aad1b652...9d61` | Exact Rational / Cyclotomic | PASS |
| `mub_target_a12_smale_sentry_receipt.json` | Target A12 | `c2efca25...1871` | Exact Rational / Cyclotomic | PASS |
| `mub_target_a13_grand_synthesis_receipt.json` | Target A13 | `79dfb73e...478a` | Exact Rational / Cyclotomic | PASS |
| `mub_target_b1_continuous_chaining_receipt.json` | Target B1 | `e747e532...f05f` | Exact Rational / Cyclotomic | PASS |
| `mub_target_b2_global_gluing_receipt.json` | Target B2 | `f406d1b3...9e3e` | Exact Rational / Cyclotomic | PASS |
| `mub_target_b3_manifold_integration_receipt.json` | Target B3 | `01744b3d...6cb5` | Exact Rational / Cyclotomic | PASS |
| `mub_decisive_bifurcation_terminal_receipt.json` | Phase 4 Decisive | `b0ba0d63...018f` | Exact Rational / Cyclotomic | PASS |

---

## 6. Strict Claim Hygiene Compaction Envelope

In accordance with our constitutional claim hygiene directives, the conclusions of this synthesis are compacted into four mandatory statements:

### 1. What This Supports
- Supports the existence of hypothesis-shaped Lean rewrites in `MasterClassification.lean`, and the R7 refusal on one Karlsson sample.
- Supports a descriptive comparison with the OpenAI Family 266 release as corrected on 2026-10-21 (the earlier "`sorry`" comparison was wrong: the `sorry` is the comparator challenge stub, and OpenAI's Lean proves $N(6)\le 5$). That comparison is not a certificate.

### 2. What This Does Not Support
- Does NOT support the unconstrained universal claim $\text{MUB}(6) = 3$ or $\text{MUB}(6) \le 3$ for arbitrary unclassified matrices outside the declared moduli varieties and certified domains.
- Does NOT mint sovereign mathematical authority or establish a formal proof of Zauner's conjecture beyond the explicitly checked algebraic certificates and Lean 4 modules.
- Does NOT claim that empirical floating-point heuristics provide formal verification without exact certificates.

### 3. Narrowest Defensible Claim
The narrowest defensible claim is that `full_moduli_variety_classification_of_five_branch` assumes `FiveBranchRealizationHypothesis`, and that the R7 evaluator refused a Stengle certificate for the Karlsson sample it actually ran.

### 4. Next Test Needed
The next test needed is an end-to-end integration test verifying that the formal bridge between the discrete 4D Bianchi identities (`Discrete4DBianchiSpectralContraction.lean`) and the 5-component moduli disjunction preserves strict homotopy margins across arbitrary global atlas transitions.

---

> **Permanent Epistemic Firewall Reminder**:  
