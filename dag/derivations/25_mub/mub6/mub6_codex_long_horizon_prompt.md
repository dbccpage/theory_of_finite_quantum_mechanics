# MUB(6) Long-Horizon Execution Directive and Codex Mission Specification

**Target**: Complete the MUB(6) research campaign synthesis, upgrade the manuscript, delineate the definitive derivation DAG, and provide an executive strategic appraisal on continuing MUB work within Omega Engine.  
**Repository Worktree**: `C:\Users\a343o\source\repos\wt-mub6-swarm`  
**Git Branch**: `feat/mub6-woland-swarm`  
**Execution Context**: Autonomous Codex / Teamwork-Preview Long-Horizon Session  
**Discipline**: Strict Landau rigor, fail-closed execution honesty, and adherence to the Claim Hygiene Rule (`RULE[user_global]`).

---

## 1. Executive Context and Checkpoint State

You are inheriting a research campaign that has executed under the Colosseum tournament architecture (32 explore nodes $\to$ 16 merge $\to$ 8 merge $\to$ 5 merge $\to$ 1 root card) and problem decomposition.

### What is 100% Complete and Recorded on Disk:
1. **Phase 1 (Strategy Exploration & Gate Review)**:
   - Root strategy consensus sealed in `.agents/teamwork/strategy_L04_N00/strategy_card.json`.
   - Gate Review certified by 8 independent judges in `.agents/teamwork/gate_level_02_results.json`.
2. **Phase 2 (Problem Decomposition into 7 Subproblems)**:
   - Contracted from Level 0 (8 outliners) $\to$ Level 1 (5 plan mergers) $\to$ Level 2 (1 root consensus master skeleton) sealed in `.agents/teamwork/decomposition_level_02_results.json` via `.agents/teamwork/decomposition_L02_N00/decomposition.json`.
   - Defines the master LaTeX template and the 7-subproblem dependency DAG.
3. **Phase 3, Subproblem 1 (Constructive Lower Bound & Projector Gram Obstruction)**:
   - **100% Sealed** in `.agents/teamwork/subproblem_01_level_02_results.json`.
   - Establishes unconditional lower bound $N(6) \ge 3$ via explicit $\mathbb{C}^2 \otimes \mathbb{C}^3$ Kronecker products ($U_r = A_r \otimes C_r$).
   - Evaluates the $24 \times 24$ rank-1 projector Gram matrix $\mathcal{G} = I_4 \otimes I_6 + \frac{1}{6}(J_4 - I_4) \otimes J_6$, establishing exact spectrum $\{4^{\times 1}, 1^{\\times 20}, 0^{\times 3}\}$ with rank 21 and $\mathcal{G} \succeq 0$, proving that linear operator, frame potential, and Welch bounds cannot detect the dimension-6 obstruction.
4. **Phase 3, Subproblem 2 (Canonical Gauge Fixing, 120-Variable Manifold, and Sporadic Moduli Ceilings)**:
   - **Level 0 (100% Sealed)**: 8 leaf solvers and 8 paired falsers completed in `.agents/teamwork/subproblem_02_level_00_results.json`.
   - **Key Results Established**:
     - *Lie Group vs. Coordinate Codimension*: Continuous column-phase gauge group is $\mathbb{T}^{12} \cong \mathrm{U}(1)^6 \times \mathrm{U}(1)^6$ (12 generators). The 24 real affine constraints $((H_2)_{0k} = 1, (H_3)_{0k} = 1)$ in $\mathbb{R}^{144}$ fix 12 continuous phase parameters and discharge 12 circle unimodularity constraints, leaving exactly $144 - 24 = 120$ active real coordinates across rows 1 to 5.
     - *Transition Balance Laws as Syzygies*: For $W = H_2^\dagger H_3$, row/column sums $\sum_k W_{jk} = 6$ and $\sum_j W_{jk} = 6$ are polynomial syzygies of row-0 gauge fixing and unitarity $H_a H_a^\dagger = 6I_6$. They contribute zero variety codimension.
     - *Sporadic Ceilings & Laurent Invariant*: Literature ceilings exclude Fourier-Diță $F_6(x, y)$ (Jaming et al. 2010 Theorem 1.4), Tao $S_6$ (Brierley & Weigert 2010 ceiling of 2 MUBs), and Haagerup $H_6$ (ceiling of 3 MUBs). Exact evaluation $|F_{\pi(\gamma_1)}(S_6)|^2 = 9$ across all $\binom{6}{3}=20$ permutations confirms violation of Conjecture 2 necessary conditions.
     - *Quarantined Obligations*: Moduli classification hypothesis (Beauchamp-Nicoara five-branch conjecture) is isolated as open **Gap G1**. Continuous affine Karlsson family $A_6(x, y)$ has no literature ceiling and satisfies Conjecture 2 ($G_{A_6} = 0$), remaining an active non-extension obligation.
   - **Level 1 (Staged)**: 5 merge solver assignments recorded in `.agents/teamwork/subproblem_02_level_01_assignments.json`.

---

## 2. Core Missions for Codex

### Mission 1: Complete and Integrate Subproblem 2 into the Master LaTeX Manuscript
1. Synthesize the 5 Level 1 merge perspectives into the definitive Section 2 LaTeX body (budget $\le 120$ lines).
2. Substitute the completed text into `[[SUBPROBLEM_02]]` of the master manuscript defined in `.agents/teamwork/decomposition_L02_N00/decomposition.json`.
3. Seal `.agents/teamwork/subproblem_02_level_01_results.json` and `.agents/teamwork/subproblem_02_level_02_results.json` with exact rational/symbolic verifications.

### Mission 2: Upgrade the MUB(6) Research Manuscript (`paper.md` and LaTeX preprint)
1. Update `omega_engine_projects/mub6/mub6.md` to incorporate:
   - The formal dimensional reduction theorem ($144 \to 120$ real coordinates under $\mathbb{T}^{12}$ column gauge fixing).
   - The exact algebraic syzygy proof demonstrating why the 24 transition balance equations yield zero variety codimension.
   - The Laurent functional invariant $|F_{\pi(\gamma_1)}(S_6)|^2 = 9$ across all 20 permutations on Tao's $S_6$.
   - The machine-checked Lean 4 Curto–Fialkow flat moment equivalence (`ConcreteMubFlatExtension.lean`).
   - The explicit boundary definitions for Gap G1 (Beauchamp–Nicoara) and the continuous Karlsson family $A_6(x, y)$.
2. Maintain strict Landau rigor: no promotional rhetoric, no unearned claims of $N(6)=3$, every section equipped with the 4-part claim scope envelope.

### Mission 3: Detailed Derivation DAG for MUB(6) = 3 or Not
Synthesize an exhaustive, acyclic dependency Directed Acyclic Graph (DAG) detailing the complete mathematical path to deciding whether $N(6)=3$ or a quartet exists in $\mathbb{C}^6$. For each node in the DAG, provide:
1. **Mathematical Statement / Target Lemma**: Exact algebraic or geometric formulation.
2. **Current Epistemic Status**: Proved (with Lean 4/Python receipt), Conditionally Reduced, or Open Conjecture.
3. **Specific Obstruction / Bottleneck**: The precise mathematical barrier preventing trivial closure (e.g., continuous parameters, non-compactness, deltoid cusps, floating-point solver drift).
4. **Required Verification Artifact**: Lean 4 theorem, exact rational Positivstellensatz certificate, or certified outward interval enclosure.

Key sub-branches that must be explicitly mapped in this DAG:
- *Branch A (Sporadic Matrices)*: $F_6(x, y), S_6, H_6$ — status of literature ceilings and transport theorems.
- *Branch B (Two-Circulant Szöllősi Family $B_6(\theta)$)*: Deltoid cusp detachment (real deficit $\ge 1.5$), parameter Jacobian regular arc, and continuous polynomial refutation.
- *Branch C (Continuous Affine Karlsson Family $A_6(x, y)$)*: 2-parameter affine manifold, algebraic non-extension, and why standard Laurent functional checks vanish ($G_{A_6}=0$).
- *Branch D (Classification Completeness - Gap G1)*: Status of Beauchamp–Nicoara 5-branch conjecture and consequences of an unknown isolated 6×6 Hadamard matrix.
- *Branch E (Moment-SOS & Polar-Kernel Compression)*: Degree-two flat extension, $U(2)$ polar compression ($p \le 0.0926$), and dual hyperplane separation.
- *Branch F (Adversarial Counter-Route / Quartet Existence)*: Search for exact algebraic or numerical counterexamples ($N(6) \ge 4$) in $\mathbb{C}^6$.

### Mission 4: Strategic Appraisal — "Is It Worth a Damn to Continue?"
Provide an unsparing, executive-level strategic analysis addressing the fundamental question:
**"Given that the primary objective of Omega Engine is NOT MUB research, is it worth continuing with this problem?"**

Your appraisal must address:
1. **The Nature of the MUB(6) Problem**:
   - Is MUB(6) a tractable milestone for automated reasoning, or is it an open-ended mathematical sinkhole that has consumed decades of human research without yielding to numerical or analytical methods?
2. **Opportunity Cost vs. Scientific Payoff**:
   - What does Omega Engine sacrifice by dedicating compute, tokens, and engineering cycles to MUB(6) instead of its core architectural goals (e.g., general OS kernels, formal verification pipelines, Clean Architecture engines, multi-agent compilers, ROP workflows)?
   - What is the realistic marginal return of pushing from the current state (a world-class formal benchmark with Lean 4 flat extension equivalence and exact syzygies) to attempting an unconditional proof of $N(6)=3$?
3. **The Zenodo Packaging Alternative**:
   - What is the reputational and scientific value of freezing, packaging, and depositing the *existing* artifacts (Lean 4 formalizations, exact rational certifiers, sporadic invariant checks, dimensional reduction theorems) on Zenodo right now?
   - How can this work be published as a clean, highly respectable formal benchmark without incurring further development costs?
4. **Definitive Recommendation**:
   - Deliver a clear, unambiguous recommendation: **FREEZE AND DEPOSIT**, **CONTINUE TARGETED SOLVE**, or **PIVOT**.

---

## 3. Claim Hygiene Rule (`RULE[user_global]`)

You must write with claim discipline.

Default posture:
- Prefer narrow claims over broad claims.
- Prefer “supports,” “suggests,” “demonstrates in this setting,” or “is consistent with” over “proves.”
- Do not use hype verbs unless the evidence is formal and scoped.
- Do not promote speculative ideas into theorems.
- Do not describe toy tests as universal results.
- Do not describe implementation tests as mathematical proofs.
- Do not describe mathematical toy models as empirical evidence about real LLMs.

Forbidden words unless explicitly justified:
- `proves`, `guarantees`, `mathematically verifies`, `fundamentally`, `true intelligence`, `impossible`, `universal`, `flawless`, `perfectly`, `clearly`, `obviously`, `simply`, `merely`, `weaponized`.

Replacement defaults:
- “proves” $\to$ “shows in this model” or “supports”
- “guarantees” $\to$ “guarantees under the declared assumptions”
- “fundamental flaw” $\to$ “failure mode”
- “LLMs cannot” $\to$ “this setup does not show that LLMs can”
- “safe ASI” $\to$ “bounded toy evaluator”
- “mathematically verified” $\to$ “checked by this oracle/test”

When summarizing an artifact, always include the 4-part envelope:
1. What it supports.
2. What it does not support.
3. The narrowest defensible claim.
4. The next test needed.

---

## 4. Key Paths and Environment References

- **Active Worktree**: `C:\Users\a343o\source\repos\wt-mub6-swarm`
- **Git Branch**: `feat/mub6-woland-swarm`
- **Teamwork Directory**: `.agents\teamwork\`
- **Lean 4 Environment**: `lean4\research_programs\mub6\`
  - Pinned Lake toolchain: `leanprover/lean4:v4.33.1`
  - Core files: `ConcreteMubProjectors.lean`, `ConcreteMubMoments.lean`, `ConcreteMubPolynomials.lean`, `FlatMomentProjectorExtraction.lean`, `FlatMomentBasisRelations.lean`, `CommutativeFlatMoments.lean`, `ConcreteMubFlatExtension.lean`.
- **Python Virtual Environment**: `C:\Users\a343o\source\repos\the_symbol_game\.venv\Scripts\python.exe`
- **Manuscripts and Checkpoints**:
  - Master LaTeX Skeleton: `.agents\teamwork\decomposition_L02_N00\decomposition.json` (`decomposition_latex`)
  - Executive Checkpoint: `omega_engine_projects\mub6\papers\mub6_executive_checkpoint_2026-10-10.md`
  - Markdown Paper: `omega_engine_projects\mub6\papers\paper.md`
  - Claim Ledger: `omega_engine_projects\mub6\papers\mub6_claim_ledger.md`
