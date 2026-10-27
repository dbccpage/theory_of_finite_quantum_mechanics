Status: AI-drafted, awaiting human review.

# Derivation Note: `PGW-SN-E08-WEIGHTED-L1-DUALITY` (`TFQ-0522`)

**Target Node:** `PGW-SN-E08-WEIGHTED-L1-DUALITY` (Stage `MSSN_SN`, Record `TFQ-0522`, UUID `22fb4fa2-a611-5082-b8b2-06de96d712fc`)  
**Record status:** `SOURCE_RECORD` (unchanged)  
**DAG status:** `CONDITIONAL` $\to$ `PROVED_LEAN` (discharging the external LP strong-duality assumption over $\mathbb{Q}$ via Fourier–Motzkin elimination)  
**Campaign outcome class:** Discharged LP strong-duality import (`imports: []`); source-record fence on `AdjunctionCochain` preserved  
**AuthorityEffect:** None.  
**Lean module:** `lean4/WeightedL1Duality.lean`  
**Independent check:** `checks/independent/pgw-sn-e08-weighted-l1-duality.py`

---

## 1. Problem Statement and Mathematical Formulation

Given finite index sets $V$ (0-cells) and $E$ (1-cells), a linearly ordered field $K$ (in particular $K = \mathbb{Q}$), a coboundary matrix $D : E \times V \to K$ ($d_0 : C^0 \to C^1$), nonnegative edge weights $w : E \to K$ ($0 \le w_e$), and a measured 1-cochain $h : E \to K$:

1. **Primal gauge-repair problem**:
   $$\min_{x \in K^V} \mathrm{cost}(D, w, h, x), \qquad \mathrm{cost}(D, w, h, x) := \sum_{e \in E} w_e \,\bigl|h_e - \sum_{v \in V} D_{e,v} x_v\bigr|.$$
2. **Dual divergence-free bounded flow problem**:
   $$\max_{y \in K^E} \sum_{e \in E} y_e h_e \quad \text{subject to} \quad \forall v \in V,\; \sum_{e \in E} D_{e,v} y_e = 0 \quad \text{and} \quad \forall e \in E,\; |y_e| \le w_e.$$

Example E08 (`TFQ-0522`) previously carried an unproved assumption importing strong duality for finite feasible bounded linear programs over $\mathbb{Q}$. This derivation eliminates that assumption by establishing Farkas' lemma (`farkas`, `farkas_fintype`) over an arbitrary linearly ordered field $K$ by induction on the variable dimension via Fourier–Motzkin elimination, deriving general linear programming strong duality (`lp_strong_duality`), and specializing to weighted $\ell^1$ cochain approximation (`weighted_l1_strong_duality`, `e08_rational`).

---

## 2. Derivation of Strong Duality via Fourier–Motzkin Elimination

### 2.1 Weak Duality and Optimality Certificates

For any primal potential $x : V \to K$ and any dual-feasible flow $y : E \to K$ satisfying $D^T y = 0$ and $|y_e| \le w_e$:
$$\sum_{e \in E} y_e \Bigl(\sum_{v \in V} D_{e,v} x_v\Bigr) = \sum_{v \in V} \Bigl(\sum_{e \in E} D_{e,v} y_e\Bigr) x_v = 0,$$
and therefore
$$\sum_{e \in E} y_e h_e = \sum_{e \in E} y_e \Bigl(h_e - \sum_{v \in V} D_{e,v} x_v\Bigr) \le \sum_{e \in E} |y_e| \,\bigl|h_e - (Dx)_e\bigr| \le \sum_{e \in E} w_e \,\bigl|h_e - (Dx)_e\bigr| = \mathrm{cost}(D, w, h, x).$$
Consequently, any primal-dual pair $(x, y)$ with $\mathrm{DualFeasible}(D, w, y)$ and $\mathrm{cost}(D, w, h, x) = \sum_e y_e h_e$ certifies both $\mathrm{cost}(D, w, h, x) \le \mathrm{cost}(D, w, h, x')$ for all $x'$ and $\sum_e y'_e h_e \le \sum_e y_e h_e$ for all dual-feasible $y'$ (`certificate_optimal`).

### 2.2 Fourier–Motzkin Elimination and Farkas' Lemma

To avoid external convex-analysis or real-closure imports, `farkas` establishes the theorem of the alternatives for $A \in K^{m \times n}$ and $b \in K^m$ by induction on $n$:
- **Base case ($n = 0$)**: Either $0 \le b_i$ for all $i \in \mathrm{Fin}\,m$ (so the unique vector in $K^0$ satisfies $A x \le b$), or there exists $z \in \mathrm{Fin}\,m$ with $b_z < 0$ (so the unit basis vector $u = e_z \ge 0$ satisfies $u^T A = 0$ and $u^T b = b_z < 0$).
- **Inductive step ($n + 1$)**: To eliminate the last coordinate $t = x_n$ from $\sum_{j < n} A_{i,j} x_j + A_{i,n} t \le b_i$, form the $m^2 \times m$ nonnegative combination matrix $W$ indexed by pairs $(p, q) \in \mathrm{Fin}\,m \times \mathrm{Fin}\,m$:
  - On diagonal pairs $(p, p)$ with $A_{p,n} = 0$, row $(p, p)$ of $W$ is $e_p^T$.
  - On off-diagonal pairs $(p, q)$ with $A_{p,n} < 0 < A_{q,n}$, row $(p, q)$ of $W$ is $A_{q,n} e_p^T + (-A_{p,n}) e_q^T$.
  - On all other pairs, row $(p, q)$ of $W$ is $0$.
  By construction, $W \ge 0$ (`hW_nonneg`) and $(W A)_{r, n} = 0$ (`hW_ann`). Applying the induction hypothesis to the $n$-variable system $(W A_{\cdot, <n}) x_0 \le W b$:
  - If a solution $x_0 \in K^n$ exists, then every zero-coefficient constraint has $0 \le d_z := b_z - (A_{\cdot, <n} x_0)_z$ and every negative/positive pair $(p, q)$ satisfies $d_p / A_{p,n} \le d_q / A_{q,n}$. By `exists_between_finset` and `fm_feasibility_of_eliminated`, there exists $t \in K$ satisfying $A_{i,n} t \le d_i$ for all $i$, extending $x_0$ to $\mathrm{snoc}(x_0, t) \in K^{n+1}$.
  - If a dual certificate $v \ge 0$ exists for the reduced system with $v^T W A_{\cdot, <n} = 0$ and $v^T W b < 0$, then $u := W^T v \ge 0$ satisfies $u^T A = 0$ and $u^T b < 0$.

### 2.3 Strong LP Duality and Weighted $\ell^1$ Specialization

In `lp_strong_duality`, given primal-feasible $\max_y c^T y$ subject to $G y \le g$ and dual-feasible $\min_{u \ge 0} g^T u$ subject to $G^T u = c$, `farkas_fintype` is applied to the combined block system asserting primal feasibility, dual feasibility, and $g^T u - c^T y \le 0$. A Farkas infeasibility witness $(u', s, y^+, y^-, t) \ge 0$ produces $y' = y^+ - y^-$ with $G^T u' = t c$, $G y' \le t g$, and $g^T u' < c^T y'$; if $t > 0$, bilinear pairing $t(c^T y') = u'^T G y' \le t(g^T u')$ contradicts $g^T u' < c^T y'$, and if $t = 0$, pairing $u'$ with a primal-feasible $y_0$ and $y'$ with a dual-feasible $u_0$ yields $0 \le g^T u' < c^T y' \le 0$, again a contradiction.

In `weighted_l1_strong_duality`, the E08 dual flow problem ($\max_y h^T y$ subject to $D y \le 0$, $-D y \le 0$, $y \le w$, $-y \le w$) is encoded as the LP primal:
- Primal feasibility holds at $y_0 = 0$ since $0 \le w_e$.
- Dual feasibility holds at $x^+ = x^- = 0$, $u^+_e = \max(h_e, 0) \ge 0$, $u^-_e = \max(-h_e, 0) \ge 0$.
- From an optimal LP pair $(y, (x^+, x^-, u^+, u^-))$, setting $x_v := x^+_v - x^-_v$ yields $h_e - (D x)_e = u^+_e - u^-_e$, so $|h_e - (D x)_e| \le u^+_e + u^-_e$ and $\mathrm{cost}(D, w, h, x) \le \sum_e w_e (u^+_e + u^-_e) = \sum_e y_e h_e \le \mathrm{cost}(D, w, h, x)$.

### 2.4 Oriented 3-Cycle Witnesses and Adjunction Separation

On the oriented 3-cycle (`cycD`) with unit weights `cycW = (1, 1, 1)` and measured cochain `cycH = (1, 0, 0)`:
- Both `cycX1 = (0, 0, 0)` (residual `(1, 0, 0)`) and `cycX2 = (0, 1, 1)` (residual `(0, 0, 1)`) achieve weighted $\ell^1$ cost `1`, matching the dual circulation `cycY = (1, 1, 1)` (`cyc_optimum`), while their optimal residuals differ (`cyc_residuals_differ`).
- The harmonic potential `cycXHarm = (0, 2/3, 1/3)` yields the divergence-free $\ell^2$ residual `(1/3, 1/3, 1/3)`, which differs from both $\ell^1$-optimal residuals (`cyc_harmonic`).
- `AdjunctionTriangleData` records the algebraic unit-counit triangle laws, `adjunctionCochain_section_retraction` records that the `sn_realizations.py` map pair `(x ↦ (x, 0), (x, y) ↦ x)` is a product section-retraction, and `adjunctionCochain_not_cycD_transpose` shows that $(d_0, d_0^T)$ does not satisfy $d_0^T(d_0 x) = x$.

---

## 3. What is proved

All Lean declarations in `lean4/WeightedL1Duality.lean` compile under Lean 4.35.0 using only standard axioms (`propext`, `Classical.choice`, `Quot.sound`):

1. `weak_duality` and `certificate_optimal`: weak duality for weighted $\ell^1$ cochain approximation and mutual global optimality of zero-gap primal-dual pairs over any linearly ordered field $K$.
2. `farkas` and `farkas_fintype`: Farkas' lemma over any linearly ordered field $K$, proved by induction on the variable dimension via Fourier–Motzkin elimination.
3. `lp_weak_duality` and `lp_strong_duality`: weak and strong linear programming duality over any linearly ordered field $K$.
4. `weighted_l1_strong_duality` and `e08_rational`: existence of a primal potential $x$ and a dual-feasible flow $y$ achieving equal objective values $\mathrm{cost}(D, w, h, x) = \sum_e y_e h_e$ over $K$ and over $\mathbb{Q}$.
5. `cyc_dual_feasible`, `cyc_optimum`, `cyc_residuals_differ`, and `cyc_harmonic`: exact 3-cycle witnesses establishing optimal cost $1$, non-unique $\ell^1$ residuals, and separation from the $\ell^2$ harmonic residual $(1/3, 1/3, 1/3)$.
6. `AdjunctionTriangleData`, `adjunctionCochain_section_retraction`, and `adjunctionCochain_not_cycD_transpose`: separation between the product section-retraction in `AdjunctionCochain` and the coboundary transpose pair $(d_0, d_0^T)$.

## 4. What is assumed

1. Finite index sets `[Fintype V]` and `[Fintype E]` and nonnegative edge weights `∀ e, 0 ≤ w e` in a linearly ordered field $K$ (or $K = \mathbb{Q}$).
2. No external LP duality theorem or real-analytic Hahn–Banach import is assumed; `imports` on `TFQ-0522` is empty (`[]`).

## 5. What is open

1. In the external `S(n)` educational strand (`the_symbol_game`), `AdjunctionCochain` in `sn_realizations.py` remains a product section and first-coordinate projection rather than a linear-program solver or a full categorical functor/natural-transformation adjunction.
2. Constructive polynomial-time LP solver complexity bounds (interior-point or simplex pivot bounds) are not formalized in Lean; `farkas` uses finite $m \mapsto m^2$ Fourier–Motzkin elimination.
