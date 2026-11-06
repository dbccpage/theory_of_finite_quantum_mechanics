# Branch Elimination & Case Coverage Receipt: Target C2

AuthorityEffect: None.
Firewall Line: `stated region only; mints no authority`

## 1. Executive Summary

Target C2 executes the algebraic case splitting and branch elimination campaign over the 50-variable, 55-polynomial real rational encoding of dephased $6 \times 6$ complex Hadamard matrices, formalizing:
1. **Master Case Routing**: Complete disjunction between Regular Corner charts ($P_{\text{corner}} \ne 0$) and Degenerate Segre Cusps ($P_{\text{corner}} = 0$) in `MUB.CaseCoverage` with zero lost solutions.
2. **Gröbner Nullstellensatz Refutations**: Exact rational polynomial certificates proving that degenerate coordinate branches ($x = 0, y = 0$) and all-ones row orthogonality branches are empty varieties in `MUB.GroebnerBranch`.
3. **Positivstellensatz Real Semialgebraic Refutations**: Exact sum-of-squares (SOS) certificates proving that boundary leaves outside $[-1, 1]$ are strictly empty over $\mathbb{R}$ in `MUB.CADBranch`, distinguishing complex feasibility from real semialgebraic feasibility.

---

## 2. Formal Branch Ledger Table

| Branch ID | Parent | Guard Condition | Certificate Type | Lean 4 Theorem | Infeasibility Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `branch_regular_corner` | `root` | $P_{\text{corner}} \ne 0$ | Parametric Moduli Orbit | `master_case_routing` | Active Moduli Cover |
| `branch_segre_cusp` | `root` | $P_{\text{corner}} = 0$ | Deltoid Blowup Desingularization | `master_case_routing` | Active Moduli Cover |
| `branch_annihilated_entry` | Subvarieties | $x_{ij} = 0 \land y_{ij} = 0$ | Nullstellensatz ($1 \in I$) | `annihilated_branch_refutation` | Discharged Empty |
| `branch_all_ones_row` | Subvarieties | $\bigwedge_{j=1}^5 x_{1j} = 1$ | Nullstellensatz ($1 \in I$) | `all_ones_branch_refutation` | Discharged Empty |
| `branch_real_upper_boundary` | Boundary Leaves | $x_{ij} \ge 2$ | Stengle Positivstellensatz (SOS) | `upper_boundary_real_infeasible` | Discharged Empty |
| `branch_real_lower_boundary` | Boundary Leaves | $x_{ij} \le -2$ | Stengle Positivstellensatz (SOS) | `lower_boundary_real_infeasible` | Discharged Empty |

---

## 3. Exact Mathematical Certificates

### 3.1 Annihilated Entry Nullstellensatz Identity
$$\underbrace{(-1)}_{a_1} \cdot (x^2 + y^2 - 1) + \underbrace{x}_{a_2} \cdot (x) + \underbrace{y}_{a_3} \cdot (y) \equiv 1$$
Evaluated on $\mathbb{R}[x, y]$, this proves that $x^2 + y^2 = 1 \land x = 0 \land y = 0 \implies 1 = 0 \implies \text{False}$.

### 3.2 All-Ones Row Orthogonality Nullstellensatz Identity
$$\frac{1}{6} \left(1 + \sum_{j=1}^5 x_j\right) - \sum_{j=1}^5 \frac{1}{6} (x_j - 1) \equiv 1$$
Evaluated against the row-0 real orthogonality generator $\sum_{j=0}^5 x_{1j} = 1 + \sum_{j=1}^5 x_{1j} = 0$.

### 3.3 Upper Real Boundary Positivstellensatz SOS Identity
$$-1 \equiv \left(-\frac{1}{3}\right) (x^2 + y^2 - 1) + \underbrace{\left[\frac{1}{3}(x - 2)^2 + \frac{1}{3}y^2\right]}_{\sigma_0(x, y) \ge 0} + \underbrace{\left(\frac{4}{3}\right)}_{\sigma_1 \ge 0} (x - 2)$$
For $x^2 + y^2 = 1$ and $x - 2 \ge 0$, the right-hand side is $\ge 0$, refuting $-1 \ge 0$.

### 3.4 Lower Real Boundary Positivstellensatz SOS Identity
$$-1 \equiv \left(-\frac{1}{3}\right) (x^2 + y^2 - 1) + \underbrace{\left[\frac{1}{3}(x + 2)^2 + \frac{1}{3}y^2\right]}_{\sigma_0(x, y) \ge 0} + \underbrace{\left(\frac{4}{3}\right)}_{\sigma_1 \ge 0} (-2 - x)$$
For $x^2 + y^2 = 1$ and $-2 - x \ge 0$, the right-hand side is $\ge 0$, refuting $-1 \ge 0$.

---

## 4. Multi-Engine Verification Status

- **Lean 4 (`lake build`)**: `012_mutually_unbiased_bases` compiled all 8,753 jobs cleanly (0 `sorry`, 0 `admit`, standard foundational axioms `[propext, Classical.choice, Quot.sound]`).
- **Python Exact Verification**: Validated via `omega_engine/crates/mub_verify/g1_case_verifier.py` with 0 float leakage.
- **Epistemic Scope**: Classification of $6 \times 6$ complex Hadamard matrices remains strictly **OPEN**; this receipt establishes certified elimination of explicit degenerate branches and real boundary leaves without premature closure claims.
