Status: AI-drafted, awaiting human review.

# Derivation Note: FSP-HUBBARD-PROTECTED-REPRESENTATIONS

**AuthorityEffect:** None.
**Target:** `FSP-HUBBARD-PROTECTED-REPRESENTATIONS` (Rank 8, score 28).
**Outcome Class:** `Narrowed`.

---

## 1. Statement and Problem Context

The node statement in `dag/derivation_dag.json` reads:
> "Hubbard determinant positivity is restricted to the package stated half-filled bipartite or attractive spin-balanced hypotheses; exact negative fields outside those protections remain distinct witnesses."

In continuous and discrete quantum Monte Carlo calculations for interacting fermionic systems, determinant positivity is essential to avoid the numerical fermion sign problem. In the Hubbard model on a finite lattice graph $G = (V, E)$, the grand canonical partition function is represented via a discrete Hubbard–Stratonovich auxiliary field $s \in \{-1, +1\}^{|V| \times M}$ across $M$ discrete imaginary-time slices:
$$Z = \sum_{s} C(s) \, d_\uparrow(s) \, d_\downarrow(s),$$
where $d_\sigma(s) = \det(I + P_\sigma(s))$ is the single-particle fermion determinant for spin sector $\sigma \in \{\uparrow, \downarrow\}$, and $P_\sigma(s) = B_\sigma(M-1) \cdots B_\sigma(0)$ is the time-ordered product of single-time-step transfer operators $B_\sigma(t) = T \cdot V_\sigma(t)$.

Here:
1. $T$ is the kinetic single-particle transfer matrix on $\mathbb{R}^{|V|}$, defined as a symmetric palindromic product of bond exponentials $R_{xy}(r)$ for bonds in $E$, with parameter $r = \exp(\delta\tau \, t / 2) > 0$.
2. $V_\sigma(t) = \text{diag}(v_{\sigma, 0}(t), \dots, v_{\sigma, |V|-1}(t))$ is the diagonal auxiliary-field potential at time slice $t$.

The goal of this derivation is to verify the exact boundary of determinant positivity:
- To derive the algebraic pairing identities that make determinant weights non-negative under the declared symmetry hypotheses (attractive spin-balanced and half-filled bipartite particle-hole symmetric representations).
- To recompute exact rational negative determinant product weights outside those protections, establishing that unconditional positivity fails.

---

## 2. Derivation of Protected Non-Negative Determinant Pairings

### 2.1 Attractive Spin-Balanced Hypothesis
In the attractive Hubbard model ($U = -|U| < 0$), both spin sectors couple identically to the discrete auxiliary field $s$:
$$v_{\uparrow, i}(t) = z \, h^{s_{i,t}}, \qquad v_{\downarrow, i}(t) = z \, h^{s_{i,t}},$$
where $z = \exp(\delta\tau \, \mu) > 0$ is the fugacity and $\cosh \lambda = (h + h^{-1})/2 = \exp(\delta\tau |U| / 2) \ge 1$ with $h \ge 1$.

Because $V_\uparrow(t) = V_\downarrow(t)$ at every time slice $t$:
$$P_\uparrow(s) = P_\downarrow(s) \implies I + P_\uparrow(s) = I + P_\downarrow(s).$$
Consequently, the spin determinants are identical:
$$d_\uparrow(s) = d_\downarrow(s) = d(s) \in \mathbb{R}.$$
The determinant product is an algebraic square:
$$d_\uparrow(s) \, d_\downarrow(s) = [d(s)]^2 \ge 0.$$
With the field-dependent prefactor $C(s) = h^{-\sum_{i,t} s_{i,t}} > 0$, the total auxiliary field weight is:
$$W(s) = C(s) \, [d(s)]^2 \ge 0.$$
This nonnegativity holds for any lattice graph $G$ (including frustrated or non-bipartite graphs such as triangles) and at any chemical potential $\mu$ / fugacity $z$.

In Lean 4 (`lean4/CampaignFspHubbardProtected.lean`), this is formalized as `attractive_pairing_sq_nonneg` and `attractive_weight_nonneg`.

### 2.2 Half-Filled Bipartite Hypothesis (Repulsive Particle-Hole Protection)
In the repulsive Hubbard model ($U > 0$) at half filling ($\mu = 0$, so $z = 1$) on a bipartite graph $G$ (with bipartition $V = A \cup B$):
Define the diagonal sublattice sign operator $\eta$ by $\eta_{ii} = +1$ for $i \in A$ and $\eta_{ii} = -1$ for $i \in B$.
Because every bond connects an $A$-site to a $B$-site, $\eta$ anticommutes with the hopping generator, so $\eta \, R_{xy}(r) \, \eta = R_{xy}(r)^{-1}$.
The palindromic bond product gives:
$$\eta \, T \, \eta = T^{-1}.$$
For repulsive interactions at $z = 1$, the down-spin potential is $v_{\downarrow, i}(t) = h^{-s_{i,t}} = [v_{\uparrow, i}(t)]^{-1}$. Because $\eta$ is diagonal:
$$\eta \, V_\downarrow(t) \, \eta = [V_\uparrow(t)]^{-1}.$$
Multiplying time steps in reverse order yields the relation:
$$\eta \, P_\downarrow \, \eta = (P_\uparrow^T)^{-1}.$$
Therefore:
$$M_\downarrow = I + P_\downarrow = \eta \, [I + (P_\uparrow^T)^{-1}] \, \eta = \eta \, (P_\uparrow^T + I) \, (P_\uparrow^T)^{-1} \, \eta.$$
Taking the determinant of both sides (since $\det \eta = \pm 1$ and $(\det \eta)^2 = 1$):
$$\det M_\downarrow = \frac{\det(I + P_\uparrow^T)}{\det(P_\uparrow^T)} = \frac{\det(I + P_\uparrow)}{\det(P_\uparrow)} = \frac{d_\uparrow}{\det(P_\uparrow)}.$$
Since $\det T = 1$, the determinant of $P_\uparrow$ is simply the product of the diagonal potentials:
$$\det(P_\uparrow) = \prod_{t=0}^{M-1} \prod_{i \in V} (z \, h^{s_{i,t}}) = z^{|V|M} \, h^{\sum_{i,t} s_{i,t}}.$$
At half filling $z = 1$, so $\det(P_\uparrow) = h^{\sum s} > 0$.
The determinant product is therefore:
$$W(s) = d_\uparrow(s) \, d_\downarrow(s) = \frac{[d_\uparrow(s)]^2}{\det(P_\uparrow)} = \frac{[d_\uparrow(s)]^2}{h^{\sum s}} \ge 0.$$
In Lean 4, this is formalized as `half_filled_bipartite_weight_eq` and `half_filled_bipartite_weight_nonneg`.

---

## 3. Explicit Negative Determinant Witnesses Outside Protection

When either the bipartite condition or the half-filling condition is omitted, the symmetry relations $\eta T \eta = T^{-1}$ and $\eta V_\downarrow \eta = V_\uparrow^{-1}$ break down. Without an algebraic pairing identity, individual auxiliary-field configurations can acquire opposite signs ($d_\uparrow > 0$ and $d_\downarrow < 0$), resulting in strictly negative determinant product weights $W(s) < 0$.

Two concrete rational witnesses from `papers/core/fsp/docs/sql_meron_hubbard.md` §5 and `code/python/src/fsp/sign_sql/exact_models.py` have been independently recomputed using SymPy and plain Python (zero repository imports):

### 3.1 Witness 1: Doped 4-Site Ring (Broken Half-Filling)
- **Geometry:** 4-site periodic ring ($|V|=4$, bonds $(0,1), (1,2), (2,3), (0,3)$), 4 time slices ($M=4$).
- **Parameters:** Repulsive $U$, $r = 2$, $h = 8$, fugacity $z = 2 \ne 1$ (doped away from half-filling).
- **Field mask:** $15721 = 0011110101101001_2$.
- **Exact Spin Determinants:**
  $$d_\uparrow = \frac{11072073737867929807204939234025}{2305843009213693952} > 0,$$
  $$d_\downarrow = \frac{-1034021712177776419381618902295}{147573952589676412928} < 0.$$
- **Product Weight:**
  $$W(15721) = d_\uparrow \, d_\downarrow = \frac{-11448764643788789633389299083665210593647227349065798614587375}{340282366920938463463374607431768211456} < 0.$$

### 3.2 Witness 2: Frustrated 3-Site Triangle (Broken Bipartiteness)
- **Geometry:** 3-site triangular lattice ($|V|=3$, bonds $(0,1), (1,2), (0,2)$), 4 time slices ($M=4$).
- **Parameters:** Repulsive $U$, $r = 2$, $h = 8$, fugacity $z = 1$ (half-filled, but non-bipartite).
- **Field mask:** $1281 = 010100000001_2$.
- **Exact Spin Determinants:**
  $$d_\uparrow = \frac{2661572208368287551525625}{9223372036854775808} > 0,$$
  $$d_\downarrow = \frac{-323903084369592224375}{35184372088832} < 0.$$
- **Product Weight:**
  $$W(1281) = d_\uparrow \, d_\downarrow = \frac{-862091447562875338563475227905478168562109375}{324518553658426726783156020576256} < 0.$$

The determinants and products above are recomputed exactly by the standalone check script `checks/independent/fsp-hubbard-protected-representations.py`, and independently by a second exact-`Fraction` script written for the review (bonds applied in lexicographic order, then reversed: the ring is $(0,1),(0,3),(1,2),(2,3)$; with the listed order $(0,1),(1,2),(2,3),(0,3)$ the numbers differ). The denominators are $2^{61}, 2^{67}, 2^{128}$ (ring) and $2^{63}, 2^{45}, 2^{108}$ (triangle). Lean 4 (`CampaignFspHubbardProtected.lean`, `witness_doped_ring_weight_neg`, `witness_triangle_weight_neg`) states only that the stored rational pairs have a negative product. It does not derive those pairs from the matrices.

The same field mask 15721 on the ring at $z = 1$ satisfies $d_\downarrow = d_\uparrow/\det P_\uparrow$ and has $W \ge 0$, so the sign change at $z = 2$ is due to leaving half filling. On the triangle at $z=1$ and mask 1281 the pairing relation fails (odd cycle).

---

## 4. What is proved

Sections 2.1 and 2.2 are prose derivations (a mathematician can check them by hand); they are not formalized in Lean. What the Lean module states is narrower, and is listed first.

**In Lean 4 (arithmetic only):**
1. For $C \ge 0$ in an ordered commutative ring, $C\,(d \cdot d) \ge 0$ (`attractive_pairing_sq_nonneg`, `attractive_weight_nonneg`). The equality $d_\uparrow = d_\downarrow$ is not a hypothesis or a conclusion of this theorem; it is built into the form $d \cdot d$.
2. In an ordered field, if $d_\downarrow = d_\uparrow / \det P_\uparrow$ and $\det P_\uparrow > 0$, then $d_\uparrow d_\downarrow = d_\uparrow^2/\det P_\uparrow \ge 0$ (`half_filled_bipartite_weight_eq`, `half_filled_bipartite_weight_nonneg`). The pairing relation is a hypothesis.
3. Two stored rational pairs (masks 15721 and 1281) have $d_\uparrow > 0 > d_\downarrow$, hence a negative product (`witness_doped_ring_weight_neg`, `witness_triangle_weight_neg`).
4. $\neg (\forall p : \text{DeterminantPair}\ \mathbb{Q},\ 0 \le p.\text{weight})$ (`not_unconditional_positivity`). Any pair with opposite signs refutes it, so by itself it says nothing about Hubbard fields.

**Exact computation (not Lean):**
5. The pairing relation $d_\downarrow = d_\uparrow/h^{\sum s}$ holds, and $W \ge 0$, on all 256 fields of the 4-site ring at two slices with $r = 3/2$, $h = 2$, $z = 1$. The attractive relation $d_\uparrow = d_\downarrow$ holds on all 64 fields of the triangle at two slices with $r=3/2$, $h=2$, $z=3/2$.
6. The determinants and products of Section 3 for masks 15721 and 1281.

**By prose derivation only:**
7. $\eta T \eta = T^{-1}$ and hence the pairing relation for every bipartite graph at $z=1$; equality $P_\uparrow = P_\downarrow$ in the attractive case; $\det P_\uparrow = z^{|V|M} h^{\sum s}$.

**Outcome classification:** `Narrowed`. The status of the node stays `CONDITIONAL`.

---

## 5. What is assumed

0. **In the Lean module:** the half-filled bipartite pairing relation $d_\downarrow = d_\uparrow/\det P_\uparrow$ with $\det P_\uparrow>0$ (a hypothesis), the square form $C\,d\cdot d$ for the attractive case, and the two stored rational witness pairs. None of these is derived from the transfer matrices in Lean.

1. **Finite Trotter/Suzuki discretization:** The single-particle transfer matrix $T$ is given by the palindromic product of bond exponentials $R_{xy}(r)$, and imaginary time is discretized into $M$ slices.
2. **Discrete auxiliary-field transformation:** The discrete Hubbard–Stratonovich decomposition with single-site binary fields $s_{i,t} \in \{-1, +1\}$ is used.
3. **Declared symmetries:**
   - Attractive channel assumes identical spin coupling ($V_\uparrow = V_\downarrow$).
   - Repulsive half-filled bipartite channel assumes particle-hole symmetry ($\mu = 0$, $z = 1$) and bipartiteness of the hopping graph ($V = A \cup B$).

---

## 6. What is open

1. **Other auxiliary-field representations:** The explicit negative witnesses disprove pointwise determinant positivity for this specific discrete auxiliary-field representation. They do not exclude the possible existence of alternative representations (e.g., continuous Gaussian fields, Majorana fermion representations, or loop cluster algorithms) that might be sign-free for specific non-protected parameter regimes.
2. **Trotter limit ($\delta\tau \to 0$, $M \to \infty$):** The derivations establish finite discrete matrix identities; convergence bounds and continuum limits of the partition sum remain outside the finite discrete scope.
3. **Monte Carlo sampling and mixing bounds:** Determinant nonnegativity $W(s) \ge 0$ does not imply polynomial-time mixing of Markov-chain Monte Carlo updates over auxiliary field configurations.

---

## 7. Claim Hygiene Assessment

- **What it supports:** Supports the restriction of Hubbard auxiliary-field determinant positivity to half-filled bipartite or attractive spin-balanced representations, and provides certified rational countermodels outside those protections.
- **What it does not support:** Does not support unconditional sign-free Monte Carlo simulation for generic Hubbard models, and does not establish that all possible fermion representations are obstructed.
- **Narrowest defensible claim:** For the discrete Trotter Hubbard–Stratonovich determinant representation, the determinant product is nonnegative under the pairing relations (half-filled bipartite: $d_\downarrow = d_\uparrow/\det P_\uparrow$ with $\det P_\uparrow>0$; attractive spin-balanced: equal spin determinants), by the prose derivation of Section 2 and an arithmetic Lean statement; and at two exact fields (mask 15721 on the 4-site ring at $z=2$, mask 1281 on the 3-site triangle at $z=1$) the product is strictly negative, by exact computation. Positivity is not shown to fail on all or generic fields outside the protections (the same mask 15721 at $z = 1$ is nonnegative).
- **Next test needed:** Formalize the multi-slice Suzuki product and sublattice conjugation $\eta T \eta = T^{-1}$ directly within Lean 4 matrix algebra, and evaluate the witness determinants $\det(I+P_\sigma)$ of the ring and triangle matrices in Lean, so that the stored pairs are derived rather than stored.
