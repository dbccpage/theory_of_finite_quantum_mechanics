# The Symbol Game as an Epistemic Immune System: Empirical Findings & Architectural Protocol

**Estate**: `omega_engine_projects/mub6/research`
**Date**: 2026-09-27
**Status**: EMPIRICAL_SUMMARY
**EvidenceScope**: Aggregate results only; raw generations and billing receipts are not included in this change.
**AuthorityEffect**: None
**Firewall**: `stated region only; mints no authority`

---

## 1. Executive Summary & Research Motivation

A major operational bottleneck in automated mathematical research is the prohibitive financial and temporal cost of running frontier models (e.g. 70B–405B+ parameters or proprietary frontier endpoints) continuously for months across deep combinatorial proof search spaces.

The **Symbol Game** addresses this failure mode by operating as a **Three-Layer Sovereign Host** (L1 discrete projection governor, L2 simplicial boundary divergence, L3 defect descent and weak duality certification) paired with an **Epistemic Immune System**. Instead of relying on raw parametric scale or conversational trust, the architecture:
1. Employs untrusted, low-cost proposer models (e.g. 8B parameter models) to explore proof trajectories and generate candidate reductions/lifts.
2. Mines the proposer's errors, invalid deductions, and boundary hallucinations into formal, typed **Antibodies (Antimorphisms)**.
3. Re-injects these accumulated antibodies into subsequent proposer iterations to narrow the search space.
4. Enforces step-level intermediate reasoning via **Topological/Algebraic Scratchpads**.
5. Employs a fail-closed, exact host governor (implemented in Rust using native cyclotomic $\mathbb{Q}(\zeta_{24})$ and exact rational arithmetic) to certify invariant satisfaction with zero floating-point slop.

This document records the empirical results of this protocol on the **Matolcsi-Weiner Conjecture 2 (arXiv:2503.14752)** derivation challenge for Mutually Unbiased Bases in dimension 6 ($\text{MUB}(6)$).

---

## 2. Mathematical Benchmark Target: Matolcsi-Weiner Conjecture 2

### 2.1 The Conjecture Definition
For any complex Hadamard matrix $H \in \mathcal{H}_6$ arising as a transition matrix within a MUB triplet in $\mathbb{C}^6$:
- **Part (a)**: $G_H(\pi(\gamma_1)) = 0$ for all $\pi \in S_6$, where $\gamma_1 = (1, 1, 1, -1, -1, -1)$.
- **Part (b)**: $G_H(\pi(\gamma_2)) \cdot G_{H^*}(\pi(\gamma_2)) = 0$ for all $\pi \in S_6$, where $\gamma_2 = (3, 3, 3, -3, -3, -3)$.

Here the defect functional is defined as:
$$G_H(\gamma) = \left| \sum_{j=0}^{5} \prod_{k=0}^{5} H_{k, j}^{\gamma_k} \right|^2$$

### 2.2 Ground-Truth Machine Verification
Prior to LLM testing, the identity was solved algebraically and verified over exact arithmetic:
- **Theorem (Exact Qubit Sign Cancellation)**: For any $U(\phi) = \frac{1}{\sqrt{2}} \begin{pmatrix} 1 & 1 \\ e^{i\phi} & -e^{i\phi} \end{pmatrix}$ and any entrywise-nonzero $3 \times 3$ matrix $V$, the tensor product $H = U \otimes V$ satisfies $F_s(H) = 0$ for all permutations of $\gamma_1$.
- **Proof Mechanism**: Under flat index $r = 3i + j$, the sum factorizes as:
  $$F_s = \left(\sum_{k=0}^1 \left(\frac{U_{0k}}{U_{1k}}\right)^\alpha\right) \left(\sum_{l=0}^2 W_l(s)\right)$$
  where $\alpha = \sum_{j=0}^2 s_j = 2m - 3$ for $m \in \{0, 1, 2, 3\}$. Thus $\alpha \in \{-3, -1, 1, 3\}$ is odd, and:
  $$\left(\frac{U_{00}}{U_{10}}\right)^\alpha + \left(\frac{U_{01}}{U_{11}}\right)^\alpha = e^{-i\alpha\phi} + (-e^{-i\phi})^\alpha = e^{-i\alpha\phi}(1 + (-1)^\alpha) = 0$$
- **Checks**: The symbolic script reduces all 20 $\gamma_1$ permutations to zero. Separately, the native Rust verifier checks both conjecture clauses on 7 catalog MUB triples using 840 permutation checks and 1,260 exact Cyc24 evaluations of $G$, with zero failures. This finite check is not a proof of Conjecture 2(b).

---

## 3. Experiment 1: Iterative Antibody Mining (Hallucination Extraction)

### 3.1 Protocol
Proposers were prompted to prove or disprove the $\gamma_1$ identity for $H = U \otimes V$ with entrywise-nonzero $V$. Responses were evaluated by the Host on a 4-point rubric:
1. Correct verdict (`PROVED`).
2. Correct constraint on $V$ (entrywise nonzero, with no unitarity or invertibility requirement).
3. Identification of the odd-exponent parity cancellation mechanism.
4. Correct factorization into $U$-dependent and $V$-dependent terms.

When a proposer failed any rubric item, a typed **Antibody** was minted containing the explicit algebraic obstruction and injected into the prompt of the subsequent round.

### 3.2 Quantitative Results

| Proposer Model | Round 1 Score | Round 2 Score | Round 3 Score | Status | Total Rounds | Total Cost |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Llama 3.1 8B Instruct** | 3/4 | 0/4 | **4/4** | **CONVERGED** | 3 | **$0.000250** |
| **Llama 3.1 70B Instruct** | 3/4 | 2/4 | **4/4** | **CONVERGED** | 3 | **$0.002148** |

### 3.3 Key Findings
1. **Model Parity via Antimorphism**: The 8B model reached perfect 4/4 convergence in the exact same number of iterations (3 rounds) as the 70B model, at **8.6× lower total financial cost** ($0.00025 vs $0.00215).
2. **Intermediate Cognitive Regression**: The 8B model exhibited a transient collapse in Round 2 (dropping from 3/4 to 0/4) due to context restructuring from the newly injected antibody payload, before synthesizing the correct proof in Round 3. The 70B model degraded more gracefully (3/4 to 2/4).
3. **Retrieval vs Reasoning Boundary**: In these runs, Round 3 incorporated the supplied antibody formulation and reached the rubric maximum. The small experiment does not establish a general convergence guarantee.

---

## 4. Experiment 2: Scratchpad Ablation (Structured Decoding Controls)

### 4.1 Protocol
To evaluate the isolated effect of intermediate scratchpad structuring without iterative antibody feedback, we conducted a paired ablation trial across 5 independent trials per arm ($N=20$ total generations, temperature $T=0.4$):
- **Arm A (Freeform Baseline)**: Direct request for proof verdict, key mechanism, and constraints on $V$.
- **Arm B (Mandatory 4-Step Scratchpad)**: Proposer was strictly required to populate four sequential intermediate calculation slots before emitting the verdict:
  - Step 1: Expansion of tensor entry products.
  - Step 2: Collection of $U_{0k}$ and $U_{1k}$ powers in terms of $\alpha = s_0 + s_1 + s_2$.
  - Step 3: Explicit evaluation of $\sum_k (U_{0k}/U_{1k})^\alpha$ using the ratio $U_{01}/U_{11} = -U_{00}/U_{10}$.
  - Step 4: Parity enumeration showing $\alpha = 2m - 3 \in \{-3, -1, 1, 3\}$ is always odd.

### 4.2 Quantitative Results

| Model | Arm A (Freeform) Mean Score | Arm A Perfect Rate | Arm B (Scratchpad) Mean Score | Arm B Perfect Rate | Empirical Score Lift | Perfect Rate Delta |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Llama 3.1 8B Instruct** | 2.20 / 4 | 0 / 5 (0%) | 3.40 / 4 | 2 / 5 (40%) | **+1.20 pts** | **+40%** |
| **Llama 3.1 70B Instruct** | 2.60 / 4 | 0 / 5 (0%) | **4.00 / 4** | **5 / 5 (100%)** | **+1.40 pts** | **+100%** |

### 4.3 Key Findings
1. **Zero Unassisted Perfection**: Under freeform prompting, neither model achieved a perfect score in these trials (0/5 for both 8B and 70B). Responses imposed unneeded unitarity or Hadamard constraints on $V$; only entrywise nonzero is required for the Laurent powers.
2. **Observed 5/5 on 70B**: With the mandatory scratchpad, the 70B model scored 4/4 in all five observed trials. This is a small-sample result at nonzero temperature, not deterministic proof-system accuracy.
3. **Significant Lift on 8B**: The 8B model experienced a +1.20 point lift, achieving a 40% perfect pass rate and raising its mean score from 2.20 to 3.40.
4. **Limits**: The study covers one algebraic task, two models, and 20 generations. It does not establish cross-task reliability, statistical significance, or autonomous theorem-proving capability.

---

## 5. Architectural Implications for the Symbol Game Pipeline

```
+-----------------------------------------------------------------------------------+
|                            UNTRUSTED PROPOSER POOL                                |
|  - Low-cost models (Llama 8B, Gemini Flash, etc.)                                 |
|  - Mandatory 4-Phase Topological Scratchpad Input                                 |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          | Proposes CUT / Certificate
                                          v
+-----------------------------------------------------------------------------------+
|                        TRUSTED HOST GOVERNOR (Rust/Cyc24)                         |
|  - Layer 1: L1 Discrete Projection Defect Norm D(s)                               |
|  - Layer 2: Simplicial Coboundary B^T z = 0                                       |
|  - Layer 3: Weak Duality Pairing <z, r> == ||r||_{1,w}                            |
|  - Exact Cyclotomic Evaluation (Zero Float Tolerance)                             |
+-------------------+-------------------------------------------+-------------------+
                    |                                           |
         [PASS: Defect Descent]                       [FAIL: Obstruction]
                    v                                           v
+---------------------------------------+   +---------------------------------------+
|        EVIDENCE DAG EMISSION          |   |       ANTIBODY MINING & RE-FEED       |
|  - VerifiedEvent with SHA-256 link    |   |  - Extract typed antimorphism         |
|  - DDC 8-letter trace (E->R->C->I)    |   |  - Commit to Cemetery DAG             |
|  - State digest update                |   |  - Prepend to Proposer context        |
+---------------------------------------+   +---------------------------------------+
```

### 5.1 The Cost-Reduction Thesis
A hypothetical unassisted 405B run lasting 18 months over millions of branches would be costly; this study did not run that comparison. Within the reported benchmark:
- **Scratchpad structuring** coincided with a +1.40 mean-score lift for the 70B model and 5/5 rubric-perfect observed trials.
- **Antibody accumulation** coincided with a rubric-perfect 8B response in round 3 at the reported cost.
- The results motivate broader testing of low-tier proposers under exact host rejection; they do not establish that most combinatorial search can already be offloaded safely.

---

## 6. Next Experimental Trajectories

1. **Cross-Domain Antibody Transfer**: Test whether antibodies mined from finite quantum mechanics (e.g. qubit tensor sign cancellation) transfer effectively when presented as abstract group-character lemmas in graph-theoretic or combinatorial challenges.
2. **Cemetery DAG Autonomous Indexing**: Implement automated vector/FTS5 retrieval over historical failed receipts in `_intelligence/_woland/runs/` to inject relevant prior antibodies without manual intervention.
3. **Lean 4 Mechanization**: Formalize the algebraic theorem corroborated by `conj2_tensor_product_proof.py` in `lean4/research_programs/mub6/` to seek zero-sorry proof-kernel closure.
