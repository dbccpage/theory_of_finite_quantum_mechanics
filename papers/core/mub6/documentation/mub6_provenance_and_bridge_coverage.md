# MUB(6) Provenance Delineation & Bridge Coverage Specification

**Document ID:** `DOC-MUB6-PROVENANCE-BRIDGE-001`  
**Bridge Anchor:** `BRIDGE-MUB6-COVERAGE`  
**WDP Anchor:** WDP §21.16 / `WDP-21-16-MUB6`  
**External Anchor:** `EXT-OAI-266`  
**AuthorityEffect:** None.  

---

## 1. Foundational Governance

Results, bounds, and certificates in this estate name the classification domain and the transition slice they use.

---

## 2. Rigorous Delineation: Computer Search vs Exact Rational Certificates

In evaluating the reference materials ingested from OpenAI Family 266 (`omega_engine_library/coda_library/downloads/openai_math/family_266_mub6/`), the mathematical and computational provenance must be rigorously partitioned into two disjoint epistemic categories:

### 2.1 Empirical Branch-and-Bound Floating-Point Search Bound ($N(6) = 3$)
- **Nature of Evidence**: Empirical computer-assisted numerical search.
- **Implementation & Hardware Environment**:
  - Executes via four external C++ branch-and-bound solver pipelines (`covrun`, `arun`, `brun`, `crun`).
  - Compiled with Ubuntu GCC 13.3.0 flags: `-O3 -march=native -ffp-contract=off`.
  - Relies on x86-64 Intel Xeon Platinum 8573C hardware with IEEE 754 binary64 round-to-nearest floating-point arithmetic.
  - Utilizes compiler disassembly verification to ensure `pow(..., 2)` lowers to scalar double `mulsd`.
- **Epistemic Scope**:
  - The $N(6) = 3$ upper bound and the exclusion of 4 arbitrary bases are **not formalized** in the accompanying Lean 4 proof.
  - The repository's own project scope note (`266.md`, lines 10–12) explicitly acknowledges:
    > "The paper claims that at most three mutually unbiased orthonormal bases exist in $\mathbb{C}^6$. The linked formalization proves a weaker family bound: every family in its mutually unbiased bases model has at most five members... The selected statement does not establish the paper's upper bound of three or its computer-assisted exclusion of four arbitrary bases."
  - The empirical bound $N(6) = 3$ is the floating-point search result. The Lean formalization cited above is the weaker family bound.

### 2.2 Formal Exact Rational Fourier Vanishing Certificates ($N(6) \le 5$, Tao Class $T$)
- **Nature of Evidence**: Deductive mathematical theorem with machine-checkable exact certificates over algebraic number fields.
- **Arithmetic Field**: Exact cyclotomic and rational arithmetic over $\mathbb{Q}(\omega_6) = \mathbb{Q}(\zeta_6)$ and $\mathbb{Q}$.
- **Core Theorem**:
  - For every order-6 complex Hadamard matrix $H \in \mathcal{H}(6)$ not equivalent to the isolated Tao matrix $T$ ($H \not\sim T$), the character sum vanishes identically:
    $$g(H, \pi(\alpha)) = 0 \quad \forall \pi \in \operatorname{Sym}(6)$$
  - Across all families in the mutually unbiased bases model, any attainable family satisfies:
    $$N(6) \le 5$$
- **Local Replay & Verification**:
  - Verified in pure Python using exact integer and rational arithmetic (`Fraction`) in `fourier_certificates/verification/run.py` and `verify.py`.
  - Source file `verify.py` matches the printed paper SHA-256 checksum `104a7306205b8544c8f913f6afdb59603f2e04a207c9ac592c383b80eb0e2aa9`.
  - Replay executes with exit code 0, verifying rank tables `8871 909 897` and `46041 3429 2767`, verifying exact rational values $6480 \cdot f = -613302797399911$ and $6480 \cdot v = 179721388988719$, and asserting $f + v < 0$ without floating-point arithmetic.

---

## 3. Bridge Coverage Specification (`BRIDGE-MUB6-COVERAGE`)

Under the Witnessed Difference Programme Goal DAG (`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/plans/goal_dag.jsonl`), node `BRIDGE-MUB6-COVERAGE` defines the integration contract:

### 3.1 Node Attributes
- **Node ID**: `BRIDGE-MUB6-COVERAGE`
- **Kind**: `derivation`
- **Title**: Use MUB6 Fourier vanishing as the §21.16 coverage input
- **Dependencies**: `["EXT-OAI-266", "WDP-21-16-MUB6"]`
- **Statement**: Decide whether the external Fourier vanishing statement, with the Tao class excluded by a separate argument, supplies the exhaustive coverage certificate §21.16 asks for; keep the count of three outside WDP until its code is released and replayed.

### 3.2 Boundary Fences
1. **Fence 1**: WDP keeps MUB6 unresolved until a replayed certificate is admitted.
2. **Fence 2**: An external theorem enters as cited input, not as WDP Lean.
3. **Fence 3**: The count $N(6) = 3$ is strictly excluded from WDP and the sovereign estate; only the exact rational Fourier cancellation and $N(6) \le 5$ certificate are recognized under cited external input.

### 3.3 Mechanized Lean 4 Formalization (`Discrete4DBianchiSpectralContraction.lean`)

Module `lean4/Discrete4DBianchiSpectralContraction.lean` (source monorepo; not shipped in this deposit) formalizes the discrete identities listed below. It does not certify external Fourier vanishing (`EXT-OAI-266`). The proofs are:
1. **Discrete 4D Bianchi Identity**:
   - For any integer 2-cochain field strength $F \in C^2(\Delta^4; \mathbb{Z})$, the alternating coboundary sum around the boundary tetrahedra of the 4-simplex vanishes identically:
     $$d_3 (d_2 F) = 0 \quad (\text{`discrete_4d_bianchi_identity`})$$
   - Higher nilpotency holds for any gauge connection 1-cochain $\omega$: $d_3(d_2(d_1 \omega)) = 0$.
2. **Curvature Closure Defect Vanishing**:
   - The discrete curvature closure defect satisfies $\Gamma_2 = d_2 (d_1 \omega) = 0$ identically on every tetrahedron (`curvature_closure_defect_zero`).
3. **Exact Spectral Contraction Floor**:
   - Feasibility functional $f(v) = 1 - c \sum_i \omega_i^2$ with $c = 6/5$.
   - Under the Invariant-Systems spectral wall $W_{\text{wall}} = 1907/2000 < 1$, the deviation is bounded from below by the exact rational spectral floor:
     $$\sigma_{\text{floor}} = \frac{31}{800} > 0 \quad (\text{`spectral_floor_pos`})$$
   - Enforces $930 \le D_{\text{scaled}}$ (`spectral_contraction_floor_bound`), precluding mutual unbiasedness (`spectral_contraction_precludes_unbiasedness`).
4. **Closed Survivor Status & Zero Closure Ratio**:
   - The closure ratio vanishes identically:
     $$R_{\text{cl}} = \frac{\Gamma_2}{\Phi_1} = \frac{0}{\Phi_1} = 0 \quad (\text{`closure_ratio_eq_zero`})$$
   - Combined with gauge invariance of the circulation ($\Phi_1(\omega + d\alpha) = \Phi_1(\omega) \ge \Gamma = 12133 > 0$), this establishes that the obstruction cannot be relaxed or dissipated by 0-cochain coboundary descent.
5. **Kernel Axiom Audit**:
   - Verified with `#print axioms`: all theorems depend solely on the whitelisted core axioms `{propext, Quot.sound}` or no axioms. Zero non-standard custom axioms and zero `sorry` tokens.


---

## 4. Synthesis & Epistemic Alignment Matrix

| Evaluation Dimension | OpenAI Reference (`family_266_mub6`) | Omega Engine Estate (`omega_engine_atlas/coda_atlas/F004_papers/010_mub6/`) |
| :--- | :--- | :--- |
| **Bound $N(6) \le 5$** | Formalized statement in `MUBSix.lean` (`theorem fourier_and_family_bound`). | Admitted as external cited input under `BRIDGE-MUB6-COVERAGE` pending full Lean kernel replay. |
| **Fourier Vanishing** | Exact rational Nullstellensatz certificates ($g(H, \pi(\alpha)) = 0$ for $H \not\sim T$) verified by `verify.py`. | Fully consistent with estate exact cyclotomic/rational evaluations; reproduces 20/20 symbolic zero checks on affine families. |
| **Tao Class $T$ Isolation** | Separated via custom isolation argument in section 4 of preprint. | Confirmed via exact non-vanishing witness $G_{S_6}(\gamma_1) = 9/1 \ne 0$ in `mub6_g1_variety.rs` and Antibody `#A-G1-001`. |
| **Arithmetic Grounding** | Dual track: binary64 floating-point for search vs exact $\mathbb{Q}$ for Fourier certificates. | Strict mono-track: 100% exact rational ($\mathbb{Q}$) and cyclotomic ($\mathbb{Q}(\zeta_{24})$) arithmetic. Zero float tolerance. |

---

## 4a. LLM-proposer files: exploratory records, not evidence

The files below called hosted language models to propose candidates or to
summarize gaps. Their outputs are kept as exploratory records. No claim in
`papers/paper.md` or the claim ledger rests on them.

| File | Role |
| :--- | :--- |
| `code/mub_verify/openrouter_proposer.py` | Model-call proposer (exploratory) |
| `code/mub_verify/a2_llm_proposer.py` | Model-call proposer (exploratory) |
| `scripts/evaluate_s2_gaps_superbunny_glm.py` | Model-call gap evaluation (exploratory) |
| `scripts/query_superbunny_phase1_r7.py` | Model-call R7 query (exploratory) |
| `artifacts/s2_gaps_superbunny_glm_evaluation.json` | Model output record; not a certificate |
| `artifacts/mub_phase1_r7_superbunny_receipt.json` | Model output record; the word "receipt" in its name is historical and does not make it a certificate |

---

## 5. Claim Hygiene Summary

1. **What this document supports:** Formally delineates the epistemic boundary between external empirical search bounds ($N(6)=3$) and exact rational certificates ($N(6) \le 5$, Fourier vanishing) under `BRIDGE-MUB6-COVERAGE`, enforcing the mandatory firewall line across all documentation.
2. **What this document does not support:** Does not establish that $\text{MUB}(6) = 3$ or $\text{MUB}(6) \le 3$ is proven, nor does it admit external floating-point search routines into the estate's deductive core.
3. **Narrowest defensible claim:** External solvers suggest $N(6)=3$ within declared floating-point search regions, but only $N(6) \le 5$ and exhaustive Fourier vanishing outside Tao's class $T$ possess machine-checkable exact rational certificates over $\mathbb{Q}(\omega_6)$.
4. **Next test needed:** Execution of Milestone M4 Woland reality gate tribunal sequence to verify complete artifact and claim hygiene adherence.
