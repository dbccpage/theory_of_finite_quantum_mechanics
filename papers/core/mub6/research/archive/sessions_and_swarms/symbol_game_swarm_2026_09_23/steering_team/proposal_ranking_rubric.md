# Proposal Ingestion and Ranking Rubric (500 Proposals -> Top 50 Portfolio)

**AuthorityEffect:** None  
**Firewall Line:** `stated region only; mints no authority`  
**Authors:** Executive Steering Team (Team 0: 5 Experts)

---

## 1. Automated Scoring Rubric (100-Point Scale)

Every proposal submitted by an execution team is evaluated across five objective, verifiable dimensions:

| Dimension | Points | Evaluation Criteria & Exact Requirements |
|---|---|---|
| **D1: Mathematical Exactness & Zero-Float Purity** | 25 | **25 pts**: 100% exact rational (`Fraction`, `BigRational`, `Cyc24`) or exact cyclotomic arithmetic. Zero floating-point types (`float`, `f32`, `f64`, `Complex`) anywhere in weights, claims, coordinates, or proofs.<br>**0 pts**: Any floating-point leakage detected by recursive `assert_no_float`. |
| **D2: Symbol Game Compliance & L1 Defect Descent** | 25 | **25 pts**: Conforms strictly to `$TAU_SG_V1`. Uses 4-move vocabulary (`ASSERT`, `CUT`, `VERIFY`, `RETRACT`). Defect norm $\|\Phi_1\|_{L_1}$ is non-increasing ($\Delta \|\Phi_1\| \le 0$). Dual witness satisfies: (1) divergence $B^T z = 0$, (2) weight bounds $\|z_e\| \le w_e$, (3) zero duality gap $\langle z, r \rangle = \|r\|_{1,w}$.<br>**0 pts**: Unlicensed claim mutation, defect increase, or duality gap violation. |
| **D3: Mathematical Leverage & Obligation Alignment** | 25 | **25 pts**: Directly addresses Target G1 (irreducible variety decomposition, corner determinant factorization, triad pigeonhole lemma) or Target Q-Soundness (Archimedean Positivstellensatz in the quadratic module, rank-loop flat extension, fail-closed barrier).<br>**10–15 pts**: Addresses intermediate or local lemmas without closing a global bridge.<br>**0 pts**: Irrelevant or trivial identity. |
| **D4: Cross-Runtime Verifiability & Falsifiability** | 15 | **15 pts**: Replay script passes with negative control suite (detects mutated weights, perturbed matrices, or sign flips). Bit-for-bit reproducible SHA-256 state hash.<br>**5–10 pts**: Verified in one runtime without full negative control suite.<br>**0 pts**: Unreproducible or unverified claims. |
| **D5: Claim Hygiene & Epistemic Firewalls** | 10 | **10 pts**: Zero forbidden hype words ("proves", "guarantees", "mathematically verifies", "fundamentally", "universal"). Explicitly includes `AuthorityEffect: None` and mandatory firewall line: `stated region only; mints no authority`.<br>**0 pts**: Any premature or unconditioned claim of $\text{MUB}(6) = 3$ or $\text{MUB}(6) \le 3$. |

**Minimum Acceptance Threshold for Round 1 Winning Proposal**: Score $\ge 85 / 100$.

---

## 2. Ingestion & Selection Protocol

1. **Per-Run Culling**:
   - Each execution team executes 25 symbolic game runs.
   - For each run, the team evaluates all candidate moves and extracts the **Top 2 winning proposals** that achieve the lowest defect $\|\Phi_1\|_{L_1}$ and highest rubric score ($25 \times 2 = 50$ proposals per team).
2. **Registry Aggregation**:
   - All $10 \times 50 = 500$ harvested proposals are compiled into `round_1_manifest_500.json`.
   - Each entry records: `proposal_id`, `team_id`, `run_id`, `target`, `defect_before`, `defect_after`, `dual_witness_hash`, `rubric_score`, and `sha256_digest`.
3. **Steering Team Portfolio Curation (Top 50)**:
   - Team 0 filters and clusters the 500 proposals into the **Top 50 canonical mathematical vectors** (top 5 per team).
   - The Top 50 portfolio allocates 5 high-depth prompts per team for Round 2 deep-dive formalization in Lean 4 and exact Rust/Python solvers.
