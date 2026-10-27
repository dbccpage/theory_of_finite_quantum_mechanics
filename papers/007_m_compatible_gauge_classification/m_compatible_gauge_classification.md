# M-Compatible Gauge Classification for Banach Presheaf Coboundaries: The ℓ¹ Maximal-Symmetry Endpoint

**Author:** Jeremy H. Carroll  

**Date:** 2026-09-20  

**Version:** v4.7  

**License:** Creative Commons Attribution 4.0 International (CC-BY-4.0)  

---

## Abstract

For Banach-presheaf coboundaries over a finite poset, any faithful edge-additive diagnostic compatible with all bounded linear endomorphisms of each stalk has the weighted $\ell^1$ form over native stalk norms; the global unweighted $\ell^1$ form follows only under edge-uniformity or explicit normalization. $\ell^1$ here is not finite-structural — it is the maximal-symmetry, edge-additive endpoint. Specifically, let $P$ be a finite partially ordered set and $F$ a Banach presheaf over $P$. As a vector space, $C^1(P,F)$ is the finite direct sum of the edge stalks; the $\ell^1$ structure on it is selected under the observer axioms, not installed as an ambient cross-norm. Maximal bounded-linear local symmetry implies native-stalk proportionality edgewise. Edge-wise additivity then gives a weighted $\ell^1$ edge sum. Unweighted $\ell^1$ requires edge-uniformity, single orbit, or normalization.

The **M-Compatible Algebraic Diagnostics** taxonomy records that the local gauge is rigid only when the active transformation monoid $M$ is the complete set of bounded maps ($M_{All}$). The result is conditional: maximal bounded-linear local symmetry yields native stalk norms and, with edge-additive aggregation, weighted $\ell^1$ over edges; weaker monoids yield larger convex-body families. In particular, CPTP monotonicity alone does not uniquely force the trace norm; the trace norm is selected only after adding the usual operational distinguishability axioms.

In short: *Any additive, faithful diagnostic on Banach presheaf coboundaries that is functorial under arbitrary bounded linear maps (i.e., maximal local symmetry) must be a weighted $\ell^1$ sum of native stalk norms. Uniform $\ell^1$ requires an additional edge-uniformity or normalization assumption. This result characterizes the maximal-symmetry observer class when aggregation satisfies edge-decomposability and exact disjoint additivity. Relaxing these conditions admits alternative obstruction geometries.*

The maximal case $M=\mathrm{End}_b(V)$ is intentionally strong. It is a maximal-symmetry observer, not a default physical assumption. Many physical, computational, or operational observers use smaller monoids and therefore admit more gauges.

> **What this does not claim.** This paper does not claim that physics universally selects $\ell^1$, that all observer diagnostics are additive, that CPTP monotonicity uniquely selects the trace norm, that weaker monoids collapse to native stalk norms, or that global unweighted $\ell^1$ follows without edge-uniformity or normalization. It says only that, inside the faithful edge-additive observer class and under maximal bounded-linear local symmetry $M_e = \mathrm{End}_b(F(a_e))$, each local gauge is proportional to the native stalk norm and the global diagnostic is weighted $\ell^1$ over edges.
>
**Why a researcher should care.** Many finite obstruction systems measure local mismatch across edges: presheaf gluing failures, constraint violations, projection defects, distributed-consistency errors, and model-evaluation residuals all share this shape. The choice of diagnostic norm is not harmless — $\ell^1$, $\ell^2$, max, trace, and Orlicz gauges select different residual geometry. This paper identifies the stated observer regime in which weighted $\ell^1$ follows from the hypotheses: edge-additive aggregation plus maximal bounded-linear local symmetry. The result separates one maximal-symmetry observer class from explicit non-claims about finite-structural physics or finite-structural norm selection.

**Conventions.** Norms are denoted $\lVert \cdot \rVert$ with appropriate subscripts; scalar absolute values are denoted $|\cdot|$.

---

1. Setup

### 1.1 Banach Presheaves over Finite Posets

> **Structure Definition:** The input structure is formally defined as a **covering-edge Banach diagram** (matching PO-000). Where contravariant presheaf language $\mathcal{F} : \mathcal{P}^{\mathrm{op}}  o \mathbf{Ban}_1$ is used, path coherence (path-independent composition $F(b  o a) \circ F(c  o b) = F(c  o a)$) is strictly enforced.
>
Let $(P, \leq)$ be a finite partially ordered set. The **covering relations** are the edges of the Hasse diagram:
$$E_{\text{cov}}(P) = \{e = (a, b) : a < b,\; \nexists\, c \text{ with } a < c < b\}.$$

A **Banach presheaf** $F$ over $P$ assigns:

* To each $x \in P$, a Banach space $(F(x), \|\cdot\|_{F(x)})$.
* To each $e = (a, b) \in E_{\text{cov}}$, a bounded linear **restriction map** $r_{b,a}: F(b) \to F(a)$ with $\|r_{b,a}\|_{\text{op}} \leq 1$.

A **section** of $F$ is a family $s = (s(x))_{x \in P}$ with $s(x) \in F(x)$.

### 1.2 The 1-Cochain Space

For each edge $e = (a, b)$, the **coboundary defect** is:
$$\delta_e(s) = r_{b,a}(s(b)) - s(a) \in F(a).$$

As a vector space, the 1-cochain space is the finite product of edge stalks,
$$C^1(P,F) \;=\; \bigoplus_{e\in E_{\mathrm{cov}}} F(a_e),$$
the **ambient** space in which coboundary vectors $(\delta_e(s))_e$ live. The set of coboundary vectors is $\operatorname{im}(d_0)\subseteq C^1(P,F)$, in general a proper subspace — $C^1$ is the cochain space, not the image of $d_0$. We do **not** equip $C^1$ with an $\ell^1$ cross-norm by fiat: the $\ell^1$ structure is the object *selected* by Theorem 4.2 under the observer axioms. (That the $\ell^1$ direct sum is the coproduct in the category of Banach spaces with contractive linear maps is a standard fact, recorded here as downstream positioning, not as the defining norm.)

The $\ell^1$ coboundary norm of a section $s$ is:
$$I(s) = \sum_{e \in E_{\text{cov}}} \|\delta_e(s)\|_{F(a_e)} = \|(\delta_e(s))_e\|_1.$$

### Genesis-Bias Fence — No Prior Banach Host Is Earned Here

**The audit below is answered`YES`, and the antecedent is declared rather than denied.**

§1.1 admits a finite poset $P$, a Banach space $F(x)$ *with its native norm* at every point, and the
restriction maps — and only then does this section define $\delta_e(s) = r_{b,a}(s(b)) - s(a)$. The central
object of this paper is therefore a **subtraction of two completed sections inside a prior container**. That
is host-before-difference: the container, its stalks, and their norms are laid down first, and the difference
is exhibited inside them. This paper does **not** derive that host, and nothing here should be read as
deriving it.

**Declared antecedent (admitted, not derived).** The tuple $\bigl(P,\ E_{\mathrm{cov}},\ \{F(x),\lVert\cdot\rVert_{F(x)}\},\ \{r_{b,a}\}\bigr)$
is this paper's **declared regime data**. It is the admitted input of a regime-relative classification. It is
not constructed at this paper's degree, and it carries the continuum imports registered in the Import / Oracle
boundary below (Banach completeness, $\mathbb{R}_{\geq 0}$ as the gauge codomain, Hahn–Banach).

**Priced stronger readings — all refused.**

* *"The paper derives the norm."* **No.** The native stalk norms $\lVert\cdot\rVert_{F(a_e)}$ are **installed by fiat** at §1.1 and are the *input*. Proportionality to them is the *output*. What Theorem 4.2 establishes is non-trivial but narrower than "derivation": the maximal-symmetry gauge class **collapses to a single ray** through the already-declared native norm. Selecting among gauges given a declared norm is not deriving a norm.
* *"The $\ell^1$ structure is likewise assumed."* **No — and this distinction is real.** The **cross-norm** across edges genuinely is *selected* (Theorem 4.2), not installed; see the paragraph above on $C^1$. The asymmetry is deliberate: stalk norms in, cross-norm out.
* *"The poset/presheaf is a neutral ambient."* **No.** It is a declared, priced import. A different admitted regime yields a different classification, and this paper says nothing about which regime is licensed.
* *"$\delta_e$ is a primitive difference."* **No.** It is a coboundary defect computed between completed sections in a declared host. It is not the root-level admitted cut, and it must not be read as one.

> **GENESIS-BIAS AUDIT.** Does this section explain coboundary-diagnostic geometry by presupposing a prior container, substrate, state-space, law, observer, temporal order, possibility domain, sample space, Hilbert space, physical system, or authority source? **Yes — a finite poset, Banach stalks, and native stalk norms.** That antecedent is declared and priced above and in the Import / Oracle boundary; it is not replaced with packet-local data, and no result here is claimed to hold independently of it.
>
#### Cat_Res morphism binding (cross-reference) — HANDOFF-003 contact

**Canonical residual-handoff carrier.** Typed residual handoffs live in $\mathbf{Cat}_{\mathrm{Res}}$ (Foundations VIII / HANDOFF-003): objects are layer packets $P_i=(K_i,Z_i,J_i,W_i,R_i,Q_i,L_i,A_i)$ with $A_i=\texttt{AuthorityEffect.None}$; morphisms are inter-layer handoffs $F\colon P_i\to P_{i+1}$ that preserve carrier scope, price ZeroRel loss, map $R_i\mapsto R_{i+1}$, record a loss ledger $L_{i,i+1}$, and preserve authority non-promotion. Live path:

* [`008_residual_handoff_category.md`](../../008_engine_runtime/008_residual_handoff_category.md) under`published/008_engine_runtime/`(canonical after 2026-07-27 relocation).
* Historical dual-path label`100_mathematical_foundations/008_residual_handoff_category.md`is **not** a live file on this tree; do not resolve against it.

**GS-001 packet sketch (declared regime, not ambient genesis).** Under the §1.1–§1.2 inputs, a residual-honest reading of this paper as a layer packet is:

| Packet slot | GS-001 declared value | Residual note |
|---|---|---|
| $K$ (carrier) | Covering-edge Banach diagram $(P,E_{\mathrm{cov}},F,\{r_{b,a}\})$ | Host-before-difference; not derived |
| $Z$ (ZeroRel) | Edgewise zero defect $\delta_e=0$ / gauge ray through native stalk norm | Regime-relative |
| $J$ (observer) | Faithful edge-additive $M_e$-compatible gauges (P1–P3) | Maximal $M_e=\mathrm{End}_b$ is one observer class |
| $W$ (witness) | Lean`PaperGS001`maximal-symmetry / weighted-$\ell^1$ kernels where cited | Finite statements only |
| $R$ (residual) | Coboundary defects $(\delta_e)_e\in C^1$; non-native gauges when $M$ is smaller | Typed residual class, not authority |
| $Q$ (quotient / selected structure) | Weighted $\ell^1$ cross-norm selected under maximal monoid (Thm 4.2) | Stalk norms in; cross-norm out |
| $L$ (loss ledger) | Continuum imports (Banach, HB), edge-uniformity debt for unweighted $\ell^1$, CPTP→trace only after quotient/ops axioms | Explicit non-claims |
| $A$ (authority) |`None`| Diagnostic classifier only |

**Morphism cross-reference $F_{\mathrm{GS001}}\colon P_{\mathrm{host}}\to P_{\mathrm{gauge}}$.** Read the passage from declared host (§1.1) to $M$-compatible gauge selection (Thms 4.2 / edge sum) as a residual-honest handoff morphism in the $\mathbf{Cat}_{\mathrm{Res}}$ sense:

$$
F_{\mathrm{GS001}}
\colon
P_{\mathrm{host}}
\longrightarrow
P_{\mathrm{gauge}},
\qquad
\mathbf{R}_{\mathrm{host}}
\bigl(\delta_e(s)\bigr)_e
\;\longmapsto\;
\mathbf{R}_{\mathrm{gauge}}
\bigl(\nu_e(\delta_e)\bigr)_e
\;\text{(}M_e\text{-compatible local gauges)},
$$

with loss ledger $L_{\mathrm{host},\mathrm{gauge}}$ recording at least: (i) Banach-presheaf antecedent not constructed here; (ii) Hahn–Banach import for norming functionals; (iii) unweighted scalar $\ell^1$ remains debt unless edge-uniformity / single orbit / normalization is declared; (iv) no FuncDiffAdapter is minted from $\delta_e$ alone (coboundary defect $\neq$ primitive $\Delta$).

**Binding contract (what this cross-reference does and does not do).**

| Contract field (HANDOFF-003) | GS-001 status |
|---|---|
| preserves_carrier_scope | **Yes** — same finite poset / edge set; no free ambient enlargement claimed |
| preserves_zero_rel_or_prices_loss | **Yes** — zero residual stays $\delta_e=0$; non-zero priced by selected $\nu_e$ |
| maps_residual_to_typed_residual | **Yes (diagnostic)** — defects $\mapsto$ $M$-compatible gauge values; not a CODA-FDA authority residual |
| records_loss_ledger | **Yes** — Import / Oracle + Genesis-Bias fence + non-claim box |
| preserves_authority_effect | **Yes** — remains `None` |
| Full $\mathbf{Cat}_{\mathrm{Res}}$ identity/associativity calculus | **Not claimed** — this is a published cross-reference and packet sketch, not a completed adapter-category proof |
| Derives ambient Banach host / stalk norms | **Refused** — conditional on declared inputs only |

. Weighted $\ell^1$ selection is not a residual handoff *certificate* and is not a GlobalGreen claim.

### CPTP Trace-Norm Rigidity Theorem & Monoid Reachability

> **Theorem (CPTP Trace-Norm Rigidity):** Let $H_n^0 = \{X \in M_n : X = X^\dagger, \operatorname{Tr}X = 0\}$ be the space of trace-zero Hermitian operators. Any homogeneous norm $j$ on $H_n^0$ contractive under all CPTP channels $\Lambda : M_n \to M_n$ (i.e. $j(\Lambda X) \le j(X)$) is strictly proportional to the trace norm:
> $$j(X) = c \|X\|_1.$$
>
*Proof:* For any $X, Y \in H_n^0$ with equal trace norm $\|X\|_1 = \|Y\|_1 = 2t$, decompose $X = X_+ - X_-$, $Y = Y_+ - Y_-$ with $\operatorname{Tr}X_+ = \operatorname{Tr}X_- = \operatorname{Tr}Y_+ = \operatorname{Tr}Y_- = t$. Let $P$ project onto $\operatorname{supp}X_+$, $\rho = Y_+/t$, $\sigma = Y_-/t$. The measure-and-prepare CPTP channel $\Lambda(A) = \operatorname{Tr}(PA)\rho + \operatorname{Tr}((I-P)A)\sigma$ maps $X \mapsto Y$. By CPTP contractivity, $j(Y) = j(\Lambda X) \le j(X)$. Reversing roles yields $j(X) = j(Y)$. Hence $j$ is constant on every trace-norm sphere, forcing $j(X) = c\|X\|_1$. $\blacksquare$

> **Organizing Principle (Bidirectional Sphere-Reachability Criterion):**
> $$\boxed{\text{Gauge rigidity is controlled by monoid reachability classes.}}$$
> If, for every pair of native unit vectors $(u,v)$, the monoid contains contractions $(T,S)$ with $Tu=v$ and $Sv=u$, then every compatible faithful homogeneous gauge is $c\|\cdot\|$.
>
### 1.3 Seminorms on 1-Cochains

> **Definition 1.1.** A **seminorm on 1-cochains** is a function $\nu: C^1(P, F) \to \mathbb{R}_{\geq 0}$ satisfying $\nu(cx) = |c|\nu(x)$ and $\nu(x+y) \leq \nu(x) + \nu(y)$ for all $x,y \in C^1(P, F)$ and scalars $c$.
>
We consider four properties:

**(P1) Edge-wise additivity.** $\nu$ decomposes as
$$\nu((\delta_e)_e) = \sum_{e \in E_{\text{cov}}} \nu_e(\delta_e)$$
where each $\nu_e: F(a_e) \to \mathbb{R}_{\geq 0}$ is itself a seminorm on $F(a_e)$.

**(P2) Faithfulness.** For each $e$: $\nu_e(\delta) = 0 \iff \delta = 0$.

**(P3) Functoriality under M-Compatible Subsets (Contractive Monotonicity).** The function $\nu_e$ is compatible with the underlying Banach geometry restricted by an admissible monoid evaluated on the stalk, $M_e \subset \mathrm{End}_b(F(a_e))$. Specifically, for a bounded linear transformation evaluated in this monoid:
$$\nu_e(\varphi(\delta)) \leq \|\varphi\|_{F(a_e)\to F(a_e)} \cdot \nu_e(\delta) \quad \forall \varphi \in M_e.$$
*(Note: When $M_e = \mathrm{End}_b(F(a_e))$, this is a maximal-symmetry observer assumption. It is strong and unusual: it imposes absolute direction independence, giving proportionality to the native stalk norm. On trace-zero space $H_n^0$, contractivity under full CPTP quantum channels strictly selects the Schatten-1 trace norm $c \|\cdot\|_1$.)*

**(P4) Edge-Diagram Isomorphism Invariance & Single-Edge Locality.** For any single-edge excision $\delta_e$, $\nu_e$ is determined locally. For any fiberwise isometric edge-diagram isomorphism $\pi: \tilde{E} \to E$ between edge covering diagrams, $\nu_{\tilde{P}}(\pi^*(\delta_e)_e) = \nu_P((\delta_e)_e)$, preserving edge norm weights $w_e = w_{\pi(e)}$ within each orbit of $\text{Aut}(E_{\text{cov}}(P))$.

### 1.4 Relation to the Combinatorial Classification

The present classification may be viewed as a functional-analytic companion to the finite-dimensional result established in "Coordinate-Wise Additivity and the L1 Norm on Finite Graph Cochains" [4]. In that setting, $\ell^1$ arises from local additivity over disjoint coordinate supports and edge separability alone, with no Banach space structure required. Here, coordinate additivity is replaced by structural compatibility in the form of functoriality under bounded linear maps on Banach spaces (P3). The comparison with [4] is positioning only: the present theorem is the Banach-stalk maximal-symmetry endpoint under P1--P3, not a claim that all finite-coordinate conclusions transfer automatically.

This diagnostic classification is logically prior to downstream projection-obstruction applications that use it.

**Scope note.** The convex-body taxonomy in Sections 2--3 is stated first for finite-dimensional stalks. The maximal-symmetry endpoint in Sections 4--5 applies to Banach stalks using Hahn--Banach. Infinite-dimensional convex-body classifications require the usual topological qualifications and are not claimed in full generality here.

**Falsifiability.** A proposed use of this classification fails if it cannot specify the finite poset, edge stalks, native stalk norms, declared transformation monoids $M_e$, the edge-additivity assumption, the faithfulness condition, and the edge-uniformity or normalization assumption used to pass from weighted to unweighted $\ell^1$. It also fails if a claimed non-$\ell^1$ diagnostic satisfies all stated hypotheses (P1)–(P3) with $M_e = \mathrm{End}_b(F(a_e))$.

## 1.5 Related Work and Positioning

This paper is closest to five bodies of work:

1. **Banach-space geometry and Hahn–Banach norm classification** (standard Banach-space tools, Megginson [2]; related norm-uniqueness results, Pestov [1]). The maximal-symmetry endpoint uses a Hahn–Banach rank-one operator argument to obtain direction independence. This paper differs by applying that mechanism edgewise to Banach-presheaf coboundary diagnostics.
2. **Finite direct sums and cross-norms.** The finite $\ell^1$ direct sum is the coproduct in Banach spaces with contractive linear maps. This paper differs by treating that finite-structural property as a *diagnostic-selection* constraint for obstruction cochains rather than as an ambient assumption.
3. **Convex-body / Minkowski-functional classification.** $M$-compatible gauges correspond to invariant or contractive symmetric convex bodies under a declared transformation monoid. This paper differs by organizing those bodies as observer-dependent obstruction geometries.
4. **Sheaf and presheaf gluing obstruction.** Presheaf coboundaries measure local-to-global mismatch. This paper differs by classifying the diagnostic geometry placed on those coboundaries, not by proving a new sheaf-cohomology theorem.
5. **Quantum distinguishability and CPTP monotonicity** (Helstrom [8]). The CPTP discussion is a boundary example: contractivity alone does not uniquely select the trace norm; additional operational discrimination assumptions are needed.

These references are background anchors. Do not read them as direct dependence unless a theorem is explicitly imported.

---

2. General M-Compatible Gauge Classification

---

### 2.1 Definition

Let $V$ be a finite-dimensional normed vector space and let
$$M \subset \mathrm{End}_b(V)$$
be an admissible transformation monoid. The operator norm $\|T\|$ is taken with respect to a fixed ambient Banach norm $\|\cdot\|_V$ on $V$. Thus the M-compatible classification depends on the pair $(M, \|\cdot\|_V)$, not on $M$ alone.

A gauge $j: V \to \mathbb{R}_{\geq 0}$ is **M-compatible** if:

1. $j(x) = 0 \iff x = 0$
2. $j(\lambda x) = |\lambda| j(x)$
3. $j(x + y) \leq j(x) + j(y)$
4. $j(T x) \leq \|T\|_{\|\cdot\|_V\to\|\cdot\|_V} j(x) \quad \forall T \in M$

---

### 2.2 **[STANDARD / PROVEN, CONDITIONAL finite-dimensional] Theorem 2.2 — M-Compatible Gauge / Convex Body Correspondence**

Let
$$B_j := \{x \in V : j(x) \leq 1\}.$$
In finite dimension, $j$ is a faithful gauge iff $B_j$ is a closed, convex, balanced, absorbing, bounded neighborhood of $0$. Equivalently, $B_j$ is the unit ball of a norm. The $M$-compatibility condition is exactly
$$
T(B_j) \subseteq \|T\|_{\|\cdot\|_V\to\|\cdot\|_V} B_j \quad \forall T \in M.
$$
Conversely, any such $M$-contractive body defines an $M$-compatible faithful gauge by its Minkowski functional:
$$j_B(x) := \inf\{\lambda > 0 : x \in \lambda B\}.$$

Thus:
$$\text{Gauge}(V, M) \cong \{\text{M-contractive symmetric convex bodies in } V\}.$$

**What`$\cong$`denotes here, and what §2.3 actually checks.** The displayed`$\cong$`is the **standard
Minkowski correspondence**, cited [2], not an equivalence proved in this paper. §2.3 checks exactly the two
*well-definedness* directions: Necessity, that $j \mapsto B_j$ lands in the body class; and Sufficiency, that
$B \mapsto j_B$ lands in the gauge class. It does **not** check the round-trips $j_{B_j} = j$ and $B_{j_B} = B$,
which are what upgrade a pair of assignments to a bijection. Both round-trips are classical for closed bodies in
finite dimension and are **imported with the`[STANDARD]`tag**, not re-proved here. Read`$\cong$`as that cited
bijection; nothing downstream of §2 relies on more than the two directions §2.3 checks. (Likewise the
"neighbourhood of $0$" clause follows from absorbing + convex + balanced in finite dimension and is cited rather
than checked in §2.3.)

---

### 2.3 Proof of Theorem 2.2

**Necessity.** Let $j$ be an $M$-compatible faithful gauge on $V$.

1. *Closedness:* Since $j$ is subadditive and absolutely homogeneous, it is a seminorm on the finite-dimensional space $V$, hence continuous. The unit ball $B_j = j^{-1}([0, 1])$ is the preimage of a closed set, hence closed.
2. *Convexity:* For $x, y \in B_j$ and $t \in [0, 1]$, subadditivity and homogeneity yield $j(tx + (1-t)y) \leq t j(x) + (1-t)j(y) \leq t + 1 - t = 1$, so $tx + (1-t)y \in B_j$.
3. *Balancedness:* For any scalar $\lambda$ with $|\lambda| \leq 1$ and $x \in B_j$, $j(\lambda x) = |\lambda| j(x) \leq 1$, so $\lambda x \in B_j$.
4. *Absorbing:* For any $x \in V$, if $x = 0$, $x \in B_j$. If $x \neq 0$, then since $j(x) < \infty$, we have $x / j(x) \in B_j$, meaning $x \in \lambda B_j$ for $\lambda = j(x)$.
5. *Boundedness:* Since $j$ is a faithful seminorm on finite-dimensional $V$, it is a norm. All norms on finite-dimensional $V$ are equivalent, so there exists $c>0$ with $j(x)\ge c\|x\|_V$. Hence $B_j\subseteq \{x:\|x\|_V\le 1/c\}$, so $B_j$ is bounded.
6. *M-Contractive Inclusion:* For any $x \in B_j$ and $T \in M$, compatibility implies $j(T x) \leq \|T\| j(x) \leq \|T\|$. If $\|T\|=0$, then $T=0$ and $T(B_j)=\{0\}\subseteq 0\cdot B_j$. If $\|T\|>0$, then for $x\in B_j$, compatibility gives $j(Tx)\le \|T\|$, hence $Tx/\|T\|\in B_j$, so $Tx\in \|T\|B_j$. Therefore $T(B_j)\subseteq \|T\|B_j$ in all cases.

**Sufficiency.** Let $B \subset V$ satisfy the geometric conditions. Define the Minkowski functional $j_B(x) = \inf\{\lambda > 0 : x \in \lambda B\}$.

1. *Seminorm properties:* Balancedness and convexity of $B$ imply $j_B$ is a seminorm (homogeneity and subadditivity).
2. *Faithfulness:* If $j_B(x)=0$, then $x\in \lambda B$ for every $\lambda>0$. Equivalently, $x/\lambda\in B$ for every $\lambda>0$. If $x\neq0$, the set $\{x/\lambda:\lambda>0\}$ is unbounded as $\lambda\to0^+$, contradicting boundedness of $B$. Hence $x=0$. Conversely, $j_B(0)=0$. Thus $j_B$ is faithful.
3. *M-Compatibility:* Let $T \in M$. For any $x \in V$ and $\epsilon > 0$, we have $x \in (j_B(x) + \epsilon) B$. Applying $T$:
   $$T x \in (j_B(x) + \epsilon) T(B) \subseteq (j_B(x) + \epsilon) \|T\| B.$$
   By definition of the Minkowski functional, this implies $j_B(T x) \leq \|T\| (j_B(x) + \epsilon)$. Since this holds for all $\epsilon > 0$, we conclude $j_B(T x) \leq \|T\| j_B(x).$ $\square$

---

### 2.4 Corollaries

The following four corollaries refine Theorem 2.2. Each is stated here and checked in §2.5.

> **[PROVEN] Corollary 1 (Order Reversal / Monotonicity of the Gauge Class).** Let $M_1 \subseteq M_2 \subseteq \mathrm{End}_b(V)$. Then $\mathrm{Gauge}(V, M_2) \subseteq \mathrm{Gauge}(V, M_1)$: enlarging the transformation monoid can only shrink the admissible gauge class. *(Weak reduction; strict containment requires an explicit separating gauge.)*
>
> **[PROVEN, CONDITIONAL + Hahn–Banach, native ambient norm] Corollary 2 (Maximal-Symmetry Endpoint).** Let $M = \mathrm{End}_b(V)$ with operator norm induced by the ambient norm $\|\cdot\|_V$. If $j$ is an $M$-compatible faithful gauge, then there exists $c > 0$ such that $j(x) = c\,\|x\|_V$ for all $x \in V$.
>
> **[STANDARD / PROVEN, CONDITIONAL + compact isometry group, normalized Haar measure] Corollary 3 (Compact-Group Construction).** Let $G \subset \mathrm{GL}(V)$ be compact and act by isometries for $\|\cdot\|_V$, and let $q$ be any norm on $V$. Then $j_G(x) = \int_G q(gx)\,dg$ (with $dg$ the normalized Haar measure) is a faithful $G$-invariant norm. Hence a $G$-compatible gauge exists for every compact isometry group.
>
> **[PROVEN, CONDITIONAL + transitive isometric sphere action] Corollary 4 (Transitive Sphere Action).** Let $G \subset \mathrm{GL}(V)$ act transitively and isometrically on the native unit sphere $S_V = \{x : \|x\|_V = 1\}$. Then any $G$-invariant norm $j$ satisfies $j(x) = c\,\|x\|_V$ for some $c > 0$. In particular, for $V = \mathbb{R}^k$ and $G = \mathrm{SO}(k)$ this gives $j(x) = c\,\|x\|_2$; under replica-extensive edge aggregation with edge-uniformity the global diagnostic is $J(\delta) = c\,\ell^1(E;\ell^2)$. *("Replica-extensive" (RE) aggregation is imported terminology from the RE1–RE5 axioms of [3]; wherever it is used in this paper it means exactly the (P1) edge-wise additivity declared in §1.3, and it is that declared hypothesis — not an additional one — that is doing the work.)*
>
### 2.5 Proof of Corollaries

**Proof of Corollary 1 (Order Reversal).** Let $j \in \text{Gauge}(V, M_2)$. Then by definition, $j(T x) \leq \|T\| j(x)$ for all $T \in M_2$. Since $M_1 \subseteq M_2$, this inequality holds for all $T \in M_1$. Thus $j$ is also $M_1$-compatible, meaning $j \in \text{Gauge}(V, M_1).$ $\square$

**Proof of Corollary 2 (Maximal Symmetry Endpoint).** Let $M = \mathrm{End}_b(V)$ and let $j$ be $M$-compatible. Let $u, v \in V$ be arbitrary vectors with $\|u\|_V = \|v\|_V = 1$. By the Hahn-Banach theorem, there exists a bounded linear functional $f \in V^*$ such that $f(u) = 1$ and $\|f\|_{V^*} = 1$. Define the rank-one operator $T: V \to V$ by $T(x) = f(x) v$.
The operator $T(x)=f(x)v$ satisfies $\|T\|_{\text{op}}\le \|f\|\,\|v\|=1$. Since $T(u)=v$, compatibility gives $j(v)=j(Tu)\le \|T\|_{\text{op}}j(u)\le j(u)$.
By swapping the roles of $u$ and $v$ and constructing a corresponding rank-one operator sending $v$ to $u$, we obtain $j(u) \leq j(v)$. Thus $j(u) = j(v)$ for all $u, v$ on the unit sphere of $(V, \|\cdot\|_V)$. Let this constant value be $c$. Since $j$ is faithful, $c > 0$. For any nonzero $x \in V$, absolute homogeneity yields:
$$j(x) = j\left(\|x\|_V \frac{x}{\|x\|_V}\right) = \|x\|_V j\left(\frac{x}{\|x\|_V}\right) = c \|x\|_V.$$
For $x = 0$, $j(0) = c \|0\|_V = 0$. Thus $j(x) = c \|x\|_V$ for all $x \in V.$ $\square$

**Proof of Corollary 3 (Compact Group Construction).** Let $G \subset \text{GL}(V)$ be compact, acting by isometries. Let $q$ be any norm on $V$. Define $j_G(x) = \int_G q(gx) \, dg$, where $dg$ is the normalized Haar measure on $G$.

1. *Subadditivity and Homogeneity:* These follow directly from the linearity of the integral and the properties of the norm $q$.
2. *Faithfulness:* Since $q$ is a norm, $q(gx) \geq 0$, and since the Haar measure is positive and $q(gx) > 0$ for $x \neq 0$, we have $j_G(x) > 0$ for all $x \neq 0$.
3. *G-Invariance:* For any $T \in G$:
   $$j_G(T x) = \int_G q(g T x) \, dg.$$
   By the right-translation invariance of the Haar measure ($d(gT) = dg$), we have:
   $$j_G(T x) = \int_G q(h x) \, dh = j_G(x).$$
   Since $G$ acts by isometries, $\|T\| = 1$, so $j_G(T x) = j_G(x) = \|T\| j_G(x).$ $\square$

**Proof of Corollary 4 (Transitive Sphere Action).** Let $G \subset \text{GL}(V)$ act transitively on the native unit sphere $S_V = \{x \in V : \|x\|_V = 1\}$. Let $j$ be any $G$-invariant norm. For any $u, v \in S_V$, transitivity implies there exists $g \in G$ such that $g u = v$.
Since $g \in G$ preserves the unit sphere, it is an isometry, so $\|g\| = 1$. $G$-invariance of $j$ yields $j(v) = j(g u) \leq \|g\| j(u) = j(u)$. Similarly, $g^{-1} v = u$ and $\|g^{-1}\| = 1$ yield $j(u) \leq j(v)$.
Thus $j(u) = j(v)$ for all $u, v \in S_V$. Let this constant value be $c > 0$. Homogeneity yields $j(x) = c \|x\|_V$ for all $x \in V$.
For the specific case of $V = \mathbb{R}^k$ with $M = \mathrm{SO}(k)$, the group acts transitively on the Euclidean sphere $S^{k-1}$. Thus any compatible norm must satisfy $j(x) = c \|x\|_2$. Under replica-extensive edge aggregation, the global diagnostic is the sum of these local norms: $J(\delta) = \sum_e c_e \|\delta_e\|_2$. Under edge-uniformity, $c_e = c$, yielding $J = c \ell^1(E; \ell^2).$ $\square$

3. Specific M-Invariant Convex Body Classifications

---

**Standing ambient-norm hypothesis (§3).** Each example below uses the bound $j(Tx)\le \lVert T\rVert_{\lVert\cdot\rVert_V\to\lVert\cdot\rVert_V}\, j(x)$. Any claim that a generator $T\in M$ has operator norm $1$ therefore requires $T$ to be an **isometry for the declared ambient norm** $\lVert\cdot\rVert_V$. The ambient norm is stated per example (Euclidean for $SO(k)$, $\ell^p$/signed-permutation-invariant for signed permutations, $\ell^\infty$ for diagonal contractions).

### 3.1 $M = \mathrm{SO}(k)$ on $\mathbb{R}^k$

**[PROVEN, CONDITIONAL + Euclidean ambient norm] Theorem 3.1 — Rotational Symmetry Implies Euclidean Balls.** Let $V=\mathbb{R}^k$ and let $M=\mathrm{SO}(k)$. If $j$ is an $M$-compatible norm, then $j(x)=c\|x\|_2$ for some $c > 0$. Equivalently, the only $\mathrm{SO}(k)$-contractive symmetric convex bodies are Euclidean balls $B=c B_2^k$.

*Proof.* The special orthogonal group $\mathrm{SO}(k)$ acts transitively on the unit sphere $S^{k-1} = \{x \in \mathbb{R}^k : \|x\|_2 = 1\}$. For any $x, y \in S^{k-1}$, there exists an $R \in \mathrm{SO}(k)$ such that $R x = y$. Since $R$ is an orthogonal matrix, its operator norm with respect to the Euclidean norm is $\|R\| = 1$. The compatibility condition for $T = R$ yields:
$$j(y) = j(R x) \leq \|R\| j(x) = j(x).$$
Applying the same argument with $R^{-1} \in \mathrm{SO}(k)$ yields $j(x) = j(R^{-1} y) \leq \|R^{-1}\| j(y) = j(y)$. Thus $j(x) = j(y)$ for all $x, y \in S^{k-1}$. Let $c = j(e_1)$. Since $j$ is a norm, $c > 0$. For any nonzero $x \in \mathbb{R}^k$, write $x = \|x\|_2 u$ where $u = x/\|x\|_2 \in S^{k-1}$. Then $j(x) = \|x\|_2 j(u) = c \|x\|_2$. $\square$

---

### 3.2 Signed permutation group on $\mathbb{R}^k$

Let $M = \mathcal{H}_k$ be the signed permutation group on $\mathbb{R}^k$, generated by coordinate permutations and coordinate reflections $x_i \mapsto -x_i$.

**[PROVEN, CONDITIONAL + signed-permutation-invariant ambient norm] Theorem 3.2 — Signed Permutations Classify Symmetric Unconditional Bodies.** A norm $j$ is $M$-compatible if and only if it is a symmetric unconditional norm:
$$j(x_1, \dots, x_k) = j(|x_1|, \dots, |x_k|) \quad \text{and} \quad j(x_1, \dots, x_k) = j(x_{\pi(1)}, \dots, x_{\pi(k)}) \quad \forall \pi \in \mathcal{S}_k.$$
Equivalently, the $M$-contractive symmetric convex bodies are exactly permutation-invariant, unconditional convex bodies.

*Proof.* Assume the ambient norm is signed-permutation invariant (for example, any $\ell^p$ norm). Then the generators of $M$ are isometries with operator norm $1$, and $M$-compatibility for the signed-permutation group is equivalent to invariance under signs and coordinate permutations.

1. Let $T_i$ be the reflection $T_i(x_1, \dots, x_i, \dots, x_k) = (x_1, \dots, -x_i, \dots, x_k)$. Since $T_i \in M$ and $\|T_i\| = 1$, compatibility requires $j(T_i x) \leq j(x)$ and $j(x) = j(T_i(T_i x)) \leq j(T_i x)$, giving $j(T_i x) = j(x)$. By composition, $j(x) = j(|x|)$, which is the unconditionality condition.
2. Let $P_\pi$ be the permutation operator $P_\pi(x)_i = x_{\pi(i)}$. Since $P_\pi \in M$ and $\|P_\pi\| = 1$, we have $j(P_\pi x) \leq j(x)$ and $j(x) = j(P_{\pi^{-1}} P_\pi x) \leq j(P_\pi x)$, giving $j(P_\pi x) = j(x)$.
Conversely, any symmetric unconditional norm is invariant under the generators of $M$, hence $M$-compatible. $\square$

---

### 3.3 Diagonal contractions on $\mathbb{R}^k$

Let $M = \mathcal{D}_{\leq 1}$ be the monoid of diagonal matrices $T = \mathrm{diag}(a_1, \dots, a_k)$ with $|a_i| \leq 1$. The operator norm is computed with respect to the $\ell^\infty$ norm: $\|T\| = \max_i |a_i| \leq 1$.

**[PROVEN, CONDITIONAL + $\ell^\infty$ ambient norm] Theorem 3.3 — Diagonal Contractions Classify Monotone Unconditional Bodies.** A norm $j$ is $M$-compatible if and only if it is coordinatewise monotone:
$$|x_i| \leq |y_i| \quad \forall i \implies j(x) \leq j(y).$$

*Proof.* Let $j$ be $M$-compatible. Suppose $|x_i| \leq |y_i|$ for all $i$. Define $a_i = x_i / y_i$ if $y_i \neq 0$, and $a_i = 0$ otherwise. Then $|a_i| \leq 1$. The diagonal matrix $T = \mathrm{diag}(a_1, \dots, a_k)$ lies in $M$ and $\|T\| \leq 1$. Since $x = T y$, compatibility yields:
$$j(x) = j(T y) \leq \|T\| j(y) \leq j(y).$$
Conversely, let $j$ be coordinatewise monotone. For any $T = \mathrm{diag}(a_1, \dots, a_k) \in M$, we have $|(Tx)_i| = |a_i x_i| \leq \max_j |a_j| \cdot |x_i| = \|T\| \cdot |x_i|$ for all $i$. Monotonicity and homogeneity yield:
$$j(T x) \leq j(\|T\| \cdot x) = \|T\| j(x).$$
Thus $j$ is $M$-compatible. $\square$

---

### 3.4 Positive diagonal contractions and positive cone maps

Let $K = \mathbb{R}^k_{\geq 0}$ with the coordinatewise order. Let $M_{\mathrm{diag}}^+$ be the monoid of positive diagonal contractions
$$
T=\mathrm{diag}(a_1,\dots,a_k),
\qquad
0\le a_i\le1.
$$

**[PROVEN, CONDITIONAL + positive-diagonal monoid] Theorem 3.4 (Positive diagonal contractions classify coordinatewise order-compatible cone gauges).** A faithful cone gauge $j_K:K\to\mathbb R_{\ge0}$ is $M_{\mathrm{diag}}^+$-compatible if and only if it is monotone with respect to the positive cone:
$$0 \leq x \leq y \text{ in } K \implies j(x) \leq j(y).$$

*Proof.* Let $j_K$ be $M_{\mathrm{diag}}^+$-compatible. Let $0 \leq x \leq y$ in $K$. Define $T=\mathrm{diag}(a_1,\dots,a_k)$ by $a_i=x_i/y_i$ when $y_i>0$ and $a_i=0$ when $y_i=0$. Since $0\le x_i\le y_i$, each $a_i$ lies in $[0,1]$, so $T\in M_{\mathrm{diag}}^+$ and $x=Ty$. Compatibility gives $j_K(x)=j_K(Ty)\le j_K(y)$.

Conversely, assume $j_K$ is monotone on $K$. For any $T=\mathrm{diag}(a_1,\dots,a_k)\in M_{\mathrm{diag}}^+$ and $x\in K$, one has $0\le Tx\le x$ coordinatewise. Monotonicity gives $j_K(Tx)\le j_K(x)$, which is exactly compatibility for positive diagonal contractions. $\square$

**Boundary note.** The equivalence above is deliberately stated for positive diagonal contractions on the cone. For arbitrary positive linear maps $T(K)\subseteq K$, coordinatewise monotonicity alone does not imply $0\le Tx\le \|T\|x$ coordinatewise; positive maps can mix coordinates. General positive-map compatibility is therefore the stronger condition
$$
j_K(Tx)\le \|T\|\,j_K(x)
\qquad
(x\in K,\ T(K)\subseteq K),
$$
and classifies order-compatible gauges only relative to the declared cone, ambient norm, and positive-map monoid. No simple coordinatewise monotonicity iff is claimed for arbitrary positive maps.

---

### 3.5 Unitary conjugation on matrices

Let $V = M_n(\mathbb{C})$ and let $M = \{X \mapsto U X U^\dagger : U \in \mathrm{U}(n)\}$.

**[STANDARD + citation / SKETCH] Theorem 3.5 — Unitary Conjugation and Spectral Boundary Example.** A norm $j$ is $M$-compatible iff it is invariant under unitary conjugation. In the Hermitian finite-dimensional case, a conjugation-invariant norm is determined by a permutation-invariant norm/function of the eigenvalue vector, with the usual norm symmetries. This is weaker than the singular-value symmetric-gauge classification, which applies to two-sided unitary invariance X ↦ UXV.

*Proof.* The map $T_U(X) = U X U^\dagger$ is a linear operator on $V$. Under any unitarily invariant ambient norm (such as the Frobenius or operator norm), $\|T_U\| = 1$.

1. If $j$ is $M$-compatible, then $j(U X U^\dagger) \leq j(X)$ and $j(X) = j(U^\dagger(U X U^\dagger) U) \leq j(U X U^\dagger)$, giving $j(U X U^\dagger) = j(X)$ for all unitaries $U$.
2. For any Hermitian matrix $X$, there exists $U \in \mathrm{U}(n)$ such that $U X U^\dagger = \Lambda = \mathrm{diag}(\lambda_1, \dots, \lambda_n)$ where $\lambda_i$ are the eigenvalues of $X$. Thus $j(X) = j(\Lambda)$.
3. If $\pi \in \mathcal{S}_n$ is a permutation, there exists a permutation matrix $P_\pi \in \mathrm{U}(n)$ such that $P_\pi \Lambda P_\pi^\dagger$ permutes the diagonal elements. Thus $j(\Lambda) = j(P_\pi \Lambda P_\pi^\dagger)$ is symmetric under permutations of the eigenvalues. This checks only the Hermitian/eigenvalue sketch needed for the boundary example. The general singular-value classification is a standard two-sided-unitary-invariance result and is cited rather than reproved here. $\square$

---

### 3.6 CPTP-compatible gauges on Hermitian trace-class differences

Let $V$ be the space of trace-zero Hermitian operators and let $M$ be the monoid of CPTP maps restricted to $V$.

**[INTERPRETIVE / BOUNDARY EXAMPLE + citation] Example 3.6 — CPTP-Compatible Distinguishability Monotones.** A gauge $j$ is CPTP-compatible precisely when it satisfies the defining compatibility inequality
$$
j(\Lambda X)\le j(X)
\qquad
\text{for all CPTP maps }\Lambda.
$$
This is a compatibility condition, not a uniqueness theorem.

The trace norm is the standard example. CPTP maps $\Lambda$ are contractive under the trace norm:
$$
\|\Lambda(X)\|_1 \leq \|X\|_1
$$
for Hermitian trace-class differences $X$. The customary reading of this inequality — that *physical processes
cannot increase operational distinguishability* — is an **imported physical interpretation carried by the CPTP
formalism**. It is not a result of this paper, and this paper constructs neither "physical process" nor
"distinguishability" at its declared degree. The inequality itself is the mathematical content; the physical
gloss is`IMPORTED`.

1. The trace norm $j(X) = \|X\|_1$ satisfies the compatibility condition $j(\Lambda X) \leq j(X)$ because CPTP maps have operator norm $\| \Lambda \|_{\|\cdot\|_1 \to \|\cdot\|_1} \leq 1$.
2. CPTP monotonicity alone is treated here as a compatibility condition, not a uniqueness theorem. The full CPTP observer geometry and the trace-norm selection problem are developed in [9]. The operational role of trace norm should be cited through an exact binary-discrimination / Helstrom source [8]: the maximal success probability of distinguishing two states $\rho,\sigma$ under equal priors is

$$
P_{\mathrm{succ}}(\rho,\sigma)=\frac12\left(1+\frac12\|\rho-\sigma\|_1\right)
$$
and this operational theorem selects trace norm for that discrimination task; it is not derived from CPTP monotonicity alone.

   *Import note.* The probability semantics in this display — "success probability", "equal priors", and the
   state pair $\rho,\sigma$ — is **imported wholesale with [8]**. This paper declares no probability adapter and
   constructs no chance semantics at its declared degree; $P_{\mathrm{succ}}$ is quoted as an external
   operational theorem, is confined to this boundary example, and is not load-bearing for Theorem 4.2.

Thus:
$$
\boxed{
\text{CPTP monotonicity alone does not force trace norm.}
}
$$

> **Resolution of the CPTP Monotonicity Boundary via PCC-20260730:**  
> While CPTP monotonicity alone does not uniquely select the trace norm on arbitrary unquotiented state spaces $X$, passing to the **minimal adequate congruence-core quotient state space** $\widehat{X} = X / \text{Core}_C(\text{ker } o)$ (Lean 4 formalizations`PCC.Adequate`/`PCC.adequate_iff`[B4] and`PCC.qo_minimal_adequate`/`PCC.minimal_iso`[B5–B6] in [`004_pcc_adequacy.lean`](`Lean package path (see claim ledger / lake target; monorepo path omitted for release)`)) eliminates all unobservable gauge redundancy. On $\widehat{X}$, maximal-monoid rigidity holds natively, resolving the Red-Team CPTP distinguishability blocker without introducing ungrounded ambient norms or genesis bias.
>
> The unitary and CPTP examples are boundary examples for the M-compatible taxonomy. They are not load-bearing for Theorem 4.2.
>
---

### 3.7 Trivial monoid

Let $M = \{I\}$.

**[PROVEN] (trivial) Theorem 3.7 (Trivial monoid admits all gauges).** Every norm $j$ on $V$ is compatible with $M = \{I\}$.

*Proof.* The monoid contains only the identity operator $I$, which has operator norm $\|I\| = 1$. The compatibility condition $j(I x) \leq \|I\| j(x)$ reduces to the identity $j(x) \leq j(x)$, which is trivially satisfied by all gauges. $\square$

4. The Maximal Symmetry Endpoint

---

The theorem in this section classifies diagnostics inside the edge-additive observer class only. Without (P1), no $\ell^1$ conclusion follows; mixed, max-type, and cross-edge-coupled diagnostics remain admissible.

We first isolate a primary structural lemma.

> **[PROVEN, CONDITIONAL + Hahn–Banach] Lemma 4.1 (Direction Independence under Maximal Symmetry).** If $\nu_e$ satisfies (P3) with $M_e = \mathrm{End}_b(F(a_e))$, then for any $v, w \in F(a_e)$ with $\|v\| = \|w\| \neq 0$, we have $\nu_e(v) = \nu_e(w)$.
>
> *Proof.* By the Hahn--Banach theorem, there exists $f_v \in F(a_e)^*$ with $\|f_v\|_{\text{op}} = 1$ and $f_v(v) = \|v\|$. Define $\Phi: F(a_e) \to F(a_e)$ by $\Phi(x) = f_v(x) \frac{w}{\|w\|}$. Because $\Phi$ is a bounded linear endomorphism of $F(a_e)$, (P3) applies directly here because $M_e = \mathrm{End}_b(F(a_e))$. Then $\Phi(v)=w$ and $\|\Phi\|_{\text{op}}\le 1$, so $\nu_e(w)=\nu_e(\Phi v)\le \|\Phi\|_{\text{op}}\nu_e(v)\le \nu_e(v)$ by (P3). By symmetry, constructing $\Psi(x) = f_w(x) \frac{v}{\|v\|}$ gives $\nu_e(v) \leq \nu_e(w)$, giving equality. $\square$
>
Lean support for the Hahn--Banach discharge:`PaperGS001.norming_functional_from_hahn_banach`,`PaperGS001.direction_independence_hahn_banach`, and`PaperGS001.gauge_proportional_hahn_banach`in
[index:index:L002_09_HahnBanachDischarge.lean](`estate index (see claim ledger; monorepo path omitted for release)`). The Lean
proof uses Mathlib's`exists_dual_vector`corollary of Hahn--Banach to remove
the previously explicit norming-functional hypothesis from`L002_06_MaximalSymmetry.lean`.

> **[PROVEN, CONDITIONAL + P1–P3; uniformity needs P4 / single orbit / normalization] Theorem 4.2 (Maximal-Symmetry $\ell^1$ Endpoint).** Let $\nu$ be a seminorm on $C^1(P, F)$ satisfying (P1), (P2), and (P3) with $M_e = \mathrm{End}_b(F(a_e))$ for all edges $e$. Then for each edge $e$, there exists $w_e > 0$ such that
> $$\nu_e(\delta) = w_e \cdot \|\delta\|_{F(a_e)} \quad \text{for all } \delta \in F(a_e).$$
>
> If additionally (P4) holds and all edge presheaf data lie in a single isomorphism orbit (or an explicit cross-edge normalization is imposed), then $w_e = \alpha$ is independent of $e$, and
> $$\nu((\delta_e)_e) = \alpha \sum_{e} \|\delta_e\|_{F(a_e)} = \alpha \cdot I(s).$$
>
In other words: maximal local functoriality gives native-stalk proportionality, and the edge-additivity hypothesis gives a weighted $\ell^1$ coboundary norm. The unweighted $\ell^1$ coboundary norm is unique up to positive scalar only under the additional edge-uniformity hypothesis.

---

5. Proof of the Maximal Theorem

---

The proof proceeds in three stages.

### Stage 1: Direction Independence

This is Lemma 4.1: for any two vectors $v, w \in F(a_e)$ with $\|v\| = \|w\| \neq 0$, we have $\nu_e(v) = \nu_e(w)$.

### Stage 2: Each $\nu_e$ is proportional to $\|\cdot\|$

Fix an edge $e$ and let $V = F(a_e)$. By Lemma 4.1, all unit vectors in $V$ have the same $\nu_e$-value: there exists $w_e \geq 0$ such that $\nu_e(v) = w_e$ for all $v$ with $\|v\| = 1$. By (P2), $w_e > 0$.

For any $\delta \in V$ with $\delta \neq 0$, the absolute homogeneity of $\nu_e$ gives:
$$\nu_e(\delta) = \|\delta\| \cdot \nu_e\!\left(\frac{\delta}{\|\delta\|}\right) = \|\delta\| \cdot w_e = w_e \|\delta\|.$$

Since $\nu_e(0) = 0$ by the seminorm property, we conclude $\nu_e(\delta) = w_e \|\delta\|$ for all $\delta \in V$. $\square$ (Stage 2)

### Stage 3: Isomorphism invariance implies uniform weights within declared edge orbits

Stage 3 uses the additional locality/naturality convention that the per-edge diagnostic $\nu_e$ is determined by the single-edge presheaf data $(F(a_e),F(b_e),r_{b,a})$, not by unrelated ambient-poset context. Under this convention, P4 identifies weights across isomorphic edge-presheaf orbits. Without this locality convention, P4 gives only the invariances explicitly declared for the diagnostic family.

By Stages 1--2, $\nu_e(\delta_e) = w_e \|\delta_e\|$ for some $w_e > 0$. Since $w_e$ depends only on the isomorphism class of the single-edge presheaf $(P_e, F_e)$, it remains to show all such presheaves yield the same weight.

Let $e_1 = (a_1, b_1)$ and $e_2 = (a_2, b_2)$ be any two covering edges with the same stalk spaces $F(a_{e_1}) \cong F(a_{e_2})$ and $F(b_{e_1}) \cong F(b_{e_2})$, and compatible restriction maps under the induced isomorphism. The single-edge posets $P_{e_1} = \{a_1 < b_1\}$ and $P_{e_2} = \{a_2 < b_2\}$ admit a unique order-preserving bijection $\pi: P_{e_1} \to P_{e_2}$. By (P4), $\nu_{P_{e_1}}(\pi^*(\delta_{e_2})) = \nu_{P_{e_2}}((\delta_{e_2}))$, which gives $w_{e_1} = w_{e_2}$.

Thus all covering edges in the same edge-presheaf isomorphism orbit share the same weight. If the paper additionally assumes a single edge orbit or a global normalization identifying all edge types, set $\alpha=w$ and obtain $\nu=\alpha\cdot I$. Without that extra assumption the correct conclusion is the orbit-weighted form
$$
\nu((\delta_e)_e)=\sum_{\mathcal O} w_{\mathcal O}\sum_{e\in\mathcal O}\|\delta_e\|.
$$
$\square$ (Theorem 4.2)

---

## Numerical Illustration — Weighted vs Unweighted $\ell^1$ Across Two Maximally-Symmetric Edges

Let $P$ have two covering edges $e_1,e_2$, with stalks $V=\mathbb{R}^2$ under the Euclidean norm and maximal local symmetry $M_{e_1}=M_{e_2}=\mathrm{End}_b(\mathbb{R}^2)$.

The load-bearing step is **Lemma 4.1** (Hahn–Banach direction independence): under maximal symmetry each per-edge gauge is proportional to the native norm $\lVert\cdot\rVert_2$. The numbers below illustrate the weighted/unweighted boundary *downstream* of that local result — they do not themselves establish it. Given the local result, Theorem 4.2 gives a faithful edge-additive diagnostic of the form
$$\nu(\delta_1,\delta_2) \;=\; w_1\lVert\delta_1\rVert_2 + w_2\lVert\delta_2\rVert_2.$$

Take $w_1=2,\ w_2=3$ and defects $\delta_1=(3,4),\ \delta_2=(1,0)$. Then $\lVert\delta_1\rVert_2=5$, $\lVert\delta_2\rVert_2=1$, so
$$\nu(\delta_1,\delta_2) = 2\cdot 5 + 3\cdot 1 = 13.$$
With edge-uniform normalization $w_1=w_2=1$ the same defects give
$$I(\delta_1,\delta_2) = 5 + 1 = 6.$$
Maximal local symmetry implies the native stalk norm edgewise, but does **not** imply a global unweighted scalar unless edge-uniformity or normalization is added.

```python
import math
delta1, delta2 = (3, 4), (1, 0)
w1, w2 = 2, 3
def l2(x): return math.sqrt(sum(t*t for t in x))
print(w1*l2(delta1) + w2*l2(delta2))   # 13.0
print(l2(delta1) + l2(delta2))         # 6.0
```---

6. Necessity of Each Property and Two-Sided Characterization (S9b)

---

| Dropped property | Target diagnostic | Violated property | Satisfied remaining properties | Structural consequence |
|---|---|---|---|---|
| **(P1) Additivity** | $\nu_{\max} = \max_e \|\delta_e\|$ | Fails P1 (additivity) | Satisfies P2, P3, P4 | Admits $\ell^\infty$-type bottleneck aggregation across edges |
| **(P2) Faithfulness** | $\nu_{\text{zero}} \equiv 0$ | Fails P2 (faithfulness) | Satisfies P1, P3, P4 | Admits degenerate zero seminorms discarding all defects |
| **(P3) Maximal Symmetry** | $\nu_{\text{aniso}}(x_1, x_2) = \|x_1\| + 2\|x_2\|$ | Fails P3 ($M_e$-functoriality) | Satisfies P1, P2, P4 | Admits anisotropic direction-dependent gauges |
| **P4 (Edge-Uniformity)** | $\nu_{\text{weighted}} = \sum_e w_e \|\delta_e\|$ ($w_e \neq w_{e'}$) | Fails P4 (unweighted scalar collapse) | Satisfies P1, P2, P3 | Admits orbit-dependent / non-uniform weighted $\ell^1$ sums |

Each row above is a verified two-sided independence witness: the target diagnostic fails the dropped property while explicitly satisfying all remaining axioms. This upgrades Theorem 4.2 into a non-redundant, two-sided characterization of the maximal-symmetry observer class.

> **[PROVEN, CONDITIONAL] Two-Sided Independence (S9b Completed).** Theorem 4.2 is non-redundant: no proper subset of the hypotheses (P1)--(P3) forces native stalk norm proportionality, and P4 is non-redundant for unweighted scalar collapse. Each dropped hypothesis strictly expands the admissible diagnostic class to include non-$\ell^1$ geometries.
>

7. Structural Uniqueness

---

Rather than defining artificial categories to encapsulate simple scaling relations, we formulate the finite-structural structure directly:

> **[PROVEN, CONDITIONAL + P1–P4 / single orbit] Proposition 7.1 (Normalized Uniqueness).** In the maximal-local-symmetry setting $M_e=\mathrm{End}_b(F(a_e))$, the weighted $\ell^1$ coboundary norm is the unique additive diagnostic satisfying properties (P1)--(P3). Adding edge-uniformity or single-orbit isomorphism invariance reduces the weighted form to $\alpha\cdot I(s)$ for some positive scalar $\alpha$.
>
> *Proof.* Let $\nu$ be any seminorm on $C^1(P, F)$ satisfying (P1)--(P3). By (P1), $\nu$ decomposes as $\nu((\delta_e)_e) = \sum_e \nu_e(\delta_e)$ where each $\nu_e$ is a seminorm on $F(a_e)$.
> By (P3), each $\nu_e$ is compatible with $M_e = \mathrm{End}_b(F(a_e))$, which by Corollary 2 gives $\nu_e(\delta) = w_e \|\delta\|_{F(a_e)}$ for some $w_e \geq 0$.
> By (P2), faithfulness requires $\nu_e(\delta) > 0$ for all $\delta \neq 0$, which gives $w_e > 0$. Thus, $\nu$ must be of the weighted $\ell^1$ form $\nu((\delta_e)_e) = \sum_e w_e \|\delta_e\|_{F(a_e)}$.
> If we assume single-orbit isomorphism invariance (P4), then all edges in the same isomorphism orbit share the same weight. If all edges lie in a single orbit, then $w_e = \alpha$ for all $e$, yielding $\nu((\delta_e)_e) = \alpha \sum_e \|\delta_e\| = \alpha I(s).$ $\square$
>
Lean support for the weighted-to-unweighted transition:`PaperGS001.weighted_sum_eq_scalar_l1_of_uniform_weights`and`PaperGS001.weighted_sum_eq_scalar_l1_of_single_orbit_weights`in
[index:index:L002_08_WeightedToUnweightedTransition.lean](`estate index (see claim ledger; monorepo path omitted for release)`).

> **[PROVEN, CONDITIONAL] Corollary 7.2 (Commutative Factorization).** For any seminorm $\nu$ satisfying (P1)--(P4) and any admitted bounded linear map $\varphi$ acting stalkwise with the declared operator-norm bound, the evaluation functional factors predictably. For a stalkwise map $\varphi=(\varphi_e)_e$, equip the weighted $\ell^1$ edge sum with the induced block operator norm $\|\varphi\|_{\text{op}} := \max_e \|\varphi_e\|_{\text{op}}$. Then:
>
> $$\nu(\varphi_*(\delta)) \leq \|\varphi\|_{\text{op}} \cdot \nu(\delta),$$
>
> and, in the maximal-local-symmetry endpoint, the weighted $\ell^1$ coboundary norm is unique among faithful edge-wise additive diagnostics satisfying P3 with $M_e = \mathrm{End}_b(F(a_e))$. The unweighted scalar form is recovered only after edge-uniformity or normalization.
>
> *Proof.* Let $\varphi = (\varphi_e)_e$ act stalkwise on the cochains. By Proposition 7.1, $\nu((\delta_e)_e) = \sum_e w_e \|\delta_e\|$. Applying $\varphi$ stalkwise:
> $$\nu(\varphi_*(\delta)) = \sum_e w_e \|\varphi_e(\delta_e)\| \leq \sum_e w_e \|\varphi_e\|_{\text{op}} \|\delta_e\| \leq \left(\max_e \|\varphi_e\|_{\text{op}}\right) \sum_e w_e \|\delta_e\| = \|\varphi\|_{\text{op}} \nu(\delta).$$
> The uniqueness follows because any deviation from the weighted $\ell^1$ form violates at least one declared hypothesis: an $\ell^p$ edge aggregation with $p>1$ violates exact edge-wise additivity (P1), while non-proportional local seminorms violate maximal local functoriality (P3) by Lemma 4.1. It is **not** the case that all non-$\ell^1$ alternatives fail contractivity — an $\ell^2$ aggregation across edges is contractive under block-diagonal maps yet fails additivity ($\sqrt{1^2+1^2}=\sqrt2\neq 1+1$). The exclusion is by additivity or functoriality, not by contractivity. $\square$
>
8. Discussion

---

### 8.1 What This Paper Shows Under Its Hypotheses

This paper isolates a structural constraint on how coboundary defects in Banach presheaf systems can be measured: maximal bounded-linear local symmetry gives native-stalk proportionality edgewise. Edge-wise additivity then gives a weighted $\ell^1$ edge sum. Unweighted $\ell^1$ requires edge-uniformity, single orbit, or normalization.

Crucially, this uniqueness is tightly bounded by the choice of the transformation monoid $M_e$. The classification does not claim that physics universally employs $\ell^1$. Rather, restricting to a narrower class of transformations generates the **M-Compatible Diagnostics** via the explicit partial order of monoids:

$$\{e\} \;\subset\; \mathbb{Z}_2^n \rtimes S_n \;\subset\; \mathbf{Diag}_{>0} \;\subset\; \mathrm{End}_b(V)$$

* **Trivial Monoid $M_e = \{e\}$:** Admits all Minkowski functionals of closed, convex, balanced, absorbing unit bodies (full infinite-dimensional convex body taxonomy).
* **Signed Permutations $M_e = \mathbb{Z}_2^n \rtimes S_n$:** Admits all symmetric Orlicz gauges / coordinate-symmetric unconditional norms.
* **Positive Diagonal $M_e = \mathbf{Diag}_{>0}$:** Admits weighted $\ell^\infty$ / weighted coordinate bounds.
* **Full Linear Monoid $M_e = \mathrm{End}_b(V)$ (Maximal Case):** Collapses the admissible local gauge space to a single ray through the native stalk norm $\nu_e(v) = w_e |v|_{F(a_e)}$.

Specific monoids determine specific convex-body families. Maximal bounded-linear symmetry reduces the admissible local body class to the native Banach ball, yielding a weighted edge-$\ell^1$ sum of native local norms under edge-additive aggregation. Rotational symmetry reduces vector stalks to Euclidean balls, yielding $\ell^1(E; \ell^2)$ under the separate edge-additivity assumption. Signed-permutation and diagonal-contraction monoids retain large families of unconditional bodies, producing $\ell^p$, $\ell^\infty$, Orlicz, and polyhedral gauges. Unitary conjugation produces spectral convex bodies and Schatten-type norms. CPTP monotonicity produces quantum distinguishability monotones, with trace norm becoming unique only under additional operational discrimination axioms. Thus the M-framework is not a norm-selection slogan; it is a convex-body classification program.

### 8.2 Relation to Other Work

The Hahn--Banach factoring argument used in Stage 1 is analogous to classical norm classification techniques in Banach space theory, where linear functionals are used to reduce geometric constraints to one-dimensional analysis (see Megginson 1998 [2] for Banach geometric tools, and Pestov 2006 [1] for related uniqueness results for norms). The key structural observation is that functoriality under all bounded linear endomorphisms, combined with Hahn--Banach, implies direction independence. This mechanism parallels the uniqueness proof for the operator norm.

The result is a presheaf version of a classical additive-sum principle in Banach space theory. More precisely, $C^1(P, F)=\bigoplus_e^{\ell^1}F(a_e)$ is the coproduct of the edge stalks in the category of Banach spaces and contractive linear maps: any family of contractive maps $T_e:F(a_e)\to Y$ induces the contractive map $(x_e)_e\mapsto\sum_eT_e x_e$. When a measurement on this finite edge family must satisfy edge-wise additivity and strict compatibility with the underlying norms on each component, the weighted $\ell^1$ form is the resulting geometry. Cross-edge $\ell^2$ aggregation fails exact edge-wise additivity because
$$
\|(v,w)\|_2\neq \|v\|+\|w\|.
$$
This does not exclude local $\ell^2$ stalk gauges such as $\ell^1(E;\ell^2)$; it excludes $\ell^2$ aggregation across independent edges under P1. The $\ell^\infty$ norm fails because $\max(\|v\|, \|w\|)$ discards summation. **[INTERPRETIVE / positioning]** This positions the $\ell^1$ coboundary norm as the additive edge-sum geometry on $C^1(P,F)$ under the stated constraints.

We note that the coboundary defects $\delta_e(s) = r_{b,a}(s(b)) - s(a)$ measure the failure of local data to glue consistently across the covering relations of the poset. The distinction in our framework is conditional: under the structural axioms (P1)--(P4), the admissible diagnostic is an orbit-weighted $\ell^1$ coboundary norm, with a global scalar only after an additional edge-uniformity assumption.

### 8.3 Strategic Place in the Overall Program

In the logical dependency order, this paper supplies the maximal-symmetry gauge-classification input used by later projection and Hodge-style obstruction papers. It sits near the start of the sequence establishing conditional $\ell^1$ rigidity for additive, structure-preserving measurements of local defects across progressively richer structural settings:

1. **Coordinate-Wise Additivity** [4]: Local additivity over disjoint coordinate supports on finite graph cochains selects $\ell^1$ geometry within the stated observer class. This is the purely combinatorial core.
2. **M-Compatible Gauge Classification** (this paper): An analogous $\ell^1$ endpoint holds in the Banach-presheaf setting only under the stronger maximal-local-symmetry and edge-additivity hypotheses of this paper. Combined with the broader M-compatible classification, this identifies weighted $\ell^1$ as the maximal-monoid endpoint in a hierarchy of admissible obstruction geometries.
3. **Single Obstruction Theory** [3]: Dynamical retractions produce intrinsic coboundary defects measured by the selected $\ell^1$ diagnostic in the replica-extensive observer class, and these defects persist with non-vanishing density over finite-time intervals protected by Lieb--Robinson bounds.
4. **$\ell^1$ Quotient Cohomology** [5]: The fixed $\ell^1$ cochain geometry induces the standard quotient norm on $H^1(G)$. This is not the unique possible norm on cohomology; it is the quotient norm compatible with the chosen $\ell^1$ cochain geometry.

### 8.4 Connection to Observer Theory and Contextual Congruence

The M-compatible gauge classification developed here determines the **diagnostic geometry** of the obstruction calculus. The general finite obstruction framework [6] adds a complementary **governance layer** that determines what authority that geometry carries.

#### Observer Passivity and Gauge Choice

In the general framework, an observer is a repair-compatible quotient map $\mathcal O: Q^1 \to Q^1_{\mathcal O}$ with induced norm $\Phi_{\mathcal O}(y) = \inf_{\mathcal O(r)=y} \Phi(r)$. The no-creation theorem (O1 in [6]) shows $\Phi_{\mathcal O}(\mathcal O(q)) \le \Phi(q)$: observers cannot create obstruction.

The gauge choice studied here — the selection of local norms via the M-compatible classification — determines *how* the quotient obstruction $\Phi$ is computed. The observer passivity theory then constrains *what happens when that diagnostic is further processed*. Specifically:

* A maximal-symmetry observer ($M=\mathrm{End}_b(V)$ with operator norm induced by the native norm) computes $\Phi$ using the weighted $\ell^1$ coboundary norm. Any further observer quotient can only reduce $\Phi$.
* An SO(k)-observer computes $\Phi$ using the mixed $\ell^1(E; \ell^2)$ norm. The observer passivity bound applies with respect to this geometry.
* A CPTP observer computes $\Phi$ using trace-norm-based diagnostics only after trace norm has been selected by the relevant operational assumptions. The same passivity bound then holds relative to that declared geometry.

Thus the M-compatible classification and the observer passivity theory are complementary: the former selects the geometry, the latter constrains epistemic processing within that geometry.

#### Contextual Congruence and Lift Triggers

The general framework shows that the lift trigger is not obstruction mass ($\Phi > 0$) alone but **context-visible non-congruence**: a witness $w = (x,y,c)$ with $p(x) = p(y)$ but $p(\rho(c)x) \neq p(\rho(c)y)$. The $\Phi$ computed by the M-selected gauge determines whether the residual is nonzero, but the witness structure determines whether a lift is licensed.

For Banach presheaf systems, this means that even when the M-compatible diagnostic detects a nonzero quotient obstruction, the lift is licensed only when that obstruction is exposed by a declared context. The M-classification tells us *what geometry to use*; contextual congruence tells us *when to act on it*.

### 8.5 Scope Boundary and Companion Works

This manuscript establishes the sharp, maximal-symmetry endpoint under $M_e = \mathrm{End}_b(F(a_e))$. Further extensions are partitioned into dedicated companion works:

1. **Weaker-Monoid Gauge Classification:** Classifying non-$\ell^1$ gauge families when $M_e \subsetneq \mathrm{End}_b(V)$.
2. **Higher-Degree Cochain Gauge Rigidity:** Extension lifting maximal symmetry from $C^1$ to higher cochains ($C^2$) and Postnikov-style cochain towers.
3. **Residual Oracles and Lattice Scaling:** Computational application demonstrating the forced weighted-$\ell^1$ diagnostic as the residual signal for solver pruning and complexity reduction.
4. **Observer-Relative Regimes:** Framework positioning observer gauge choices as the mechanism rendering finite and infinite obstruction regimes observer-relative.

#### Reflective Completion

Under the admissibility hypotheses H1--H5 of [6] (finite witness enumeration, finite generator search class, well-founded termination, deterministic minimality certificates, no-silent-mutation discipline), the general framework formulates conditions under which iterative resolution of context witnesses is intended to produce a congruence-complete system. In [6], this reflective-completion claim remains **[CONJECTURE, CONDITIONAL]** pending the initiality-to-reflection lemma; the derivation of Theorem 4.2 here does not rely on that conjectural completion. The diagnostic computed by the M-selected gauge feeds into this completion procedure: each witness exposes a nonzero quotient residual, and the selected norm determines the quantitative obstruction mass used in minimality certificates.

#### Sheaf Gluing Obstruction

The Banach presheaf coboundary $\delta_e(s) = r_{b,a}(s(b)) - s(a)$ studied here is exactly the local-to-global defect that appears in the sheaf gluing obstruction theorem (L3 in [6]). A compatible local family $a \in \ker(d_1)$ that does not come from a global section defines a nonzero quotient obstruction $q_a \in H^1$. The M-compatible classification determines the norm on the cochain space in which this gluing obstruction is measured.

### 8.6 Norm Choice and Obstruction Geometry

Let
$$\Phi(\omega) = \inf_f \|\omega - d_0 f\|_J$$
be the observer-induced obstruction functional.

The choice of norm $J$ determines the geometry of residuals. An $\ell^2$ norm produces orthogonal projections onto $(\mathrm{im}\, d_0)^\perp$, distributing residual mass globally. An $\ell^1$ norm produces extremal solutions on the feasible affine set $\omega - \mathrm{im}(d_0)$, preserving sparse or localized structure. The admissible residuals satisfy an affine constraint determined by $\omega$ and $\mathrm{im}(d_0)$, independent of the norm.

Under additional maximal-observer assumptions — (i) additivity on disjoint support, (ii) refinement invariance, (iii) regularity, (iv) maximal bounded-linear local functoriality, and (v) edge-uniformity or explicit normalization — the functional $\Phi$ reduces to the unweighted $\ell^1$ endpoint:
$$\Phi(\omega) = C \sum_e |h_{1,e}|.$$

Without (v), the correct conclusion is the weighted or orbit-weighted $\ell^1$ form established above. These assumptions are observer-dependent and not universally imposed.

### 8.7 Connection to Dynamical Obstruction Theory

The classification result here is purely structural: it identifies the weighted $\ell^1$ form of any diagnostic satisfying the stated additivity, functoriality, and symmetry assumptions on presheaf coboundaries. Its significance becomes more apparent when combined with dynamical settings in which such coboundary defects are generated.

In the companion work "Projection Obstruction Theory" [3], projection of linear many-body dynamics onto a nonlinear manifold is shown to produce intrinsic coboundary defects that cannot be removed by linearization and that persist with non-vanishing density over finite time intervals. The present result implies that any local, additive measurement of such defects satisfying the same structural constraints has the corresponding weighted $\ell^1$ form. Thus, the $\ell^1$ diagnostic appearing in that analysis is not an unconstrained modeling choice; it is selected by the stated observer and symmetry assumptions.

$\ell^1$ is not finite-structural; it is the maximal-symmetry, edge-additive endpoint.

---

### Publication-Safe Thesis

The result should be read as a maximal-symmetry endpoint theorem: maximal bounded-linear compatibility fixes the local native norm, while edge-additive aggregation produces a weighted $\ell^1$ edge diagnostic. It does not say that all observers, all physical systems, or all quantum distinguishability measures must use this geometry.

## Acknowledgments

No external funding. No conflicts of interest.

---

## GTOC / GTLA Compliance Note

**Role:** Diagnostic gauge-classification inside a declared Banach-presheaf obstruction regime. This paper selects *which norm geometry* a coboundary diagnostic may carry under a declared observer monoid. It is not a foundations paper, not an authority paper, and not a governance paper.

**Degree:** Degree 1. The objects are 1-cochains $C^1(P,F)=\bigoplus_{e\in E_{\mathrm{cov}}}F(a_e)$ and the coboundary defects $\delta_e(s)=r_{b,a}(s(b))-s(a)$ over a **declared** finite poset $P$ with Banach stalks (§1.1–1.2). $\operatorname{im}(d_0)\subseteq C^1$ is referenced (§1.2, §8.5) and $\ker(d_1)$ is referenced (§8.4), but **neither $d_0$, $d_1$, nor the complex condition $d_1\circ d_0=0$ is constructed or proved here** — they are imported from [6]. No $C^2$ result is claimed.

**Consumes:** the declared regime tuple $\bigl(P,\ E_{\mathrm{cov}},\ \{F(x),\lVert\cdot\rVert_{F(x)}\},\ \{r_{b,a}\}\bigr)$ (§1.1; admitted, not derived — see the Genesis-Bias Fence); the observer axioms (P1) edge-wise additivity, (P2) faithfulness, (P3) $M$-compatibility, (P4) isomorphism invariance (§1.3); a declared transformation monoid $M_e\subset\mathrm{End}_b(F(a_e))$ together with a declared ambient norm — the classification depends on the **pair** $(M,\lVert\cdot\rVert_V)$, not on $M$ alone (§2.1).

**Produces:** (a) a convex-body classification of $M$-compatible gauges (§2–§3, finite-dimensional); (b) the maximal-symmetry endpoint — under (P3) with $M_e=\mathrm{End}_b(F(a_e))$, each local gauge is a positive multiple of the *already-declared* native stalk norm (Lemma 4.1, Cor 2); (c) with (P1), the weighted $\ell^1$ edge sum (Thm 4.2); (d) the unweighted scalar $\ell^1$ **only** under edge-uniformity, a single edge orbit, or explicit normalization.

**Does not produce:** a finite-structural $\ell^1$; a derivation of any norm from nothing (stalk norms are input, not output — see the Genesis-Bias Fence); trace-norm uniqueness from CPTP monotonicity; a global unweighted scalar without edge-uniformity or normalization; a claim that weaker monoids collapse to native stalk norms; any statement about physics, physical systems, or which observer regime is licensed; any lift license; any terminal; a completed $\mathbf{Cat}_{\mathrm{Res}}$ identity/associativity calculus or residual handoff *certificate* (the §1.2 $F_{\mathrm{GS001}}$ block is a published cross-reference and packet sketch only).

**Authority status:** **none.** See the authority firewall in the front matter. §8.4 already concedes that the governance layer determining what authority a geometry carries belongs to [6], not here. A classification is a diagnostic; it does not mint authority.

**Declared imports:** see the Import / Oracle boundary below.

**OracleNeeded / Q-gated items:** the §3.5 unitary-conjugation and §3.6 CPTP material — $\mathrm{U}(n)$, density operators / states $\rho,\sigma$, CPTP maps, trace-class operators, the trace norm, and the Helstrom binary-discrimination probability — is`Q-gated`imported representation structure. It is a boundary example and is explicitly **not load-bearing for Theorem 4.2** (§3.6). The trace-norm *selection* problem is`OracleNeeded`here and is deferred to [9]; this paper records only the refusal that CPTP monotonicity alone does not force it.

**GTLA boundary:** this paper is a GTOC-side diagnostic. It declares no`ContractAuthority`, no`VerifierScopedAuthority`, and no`SemanticAuthority`; it supplies no`SpecificationIdentity`,`DetectorAdequacy`,`ExhaustionWitness`,`EvidenceCeiling`,`ReplayWitness`,`Terminalizer`, or`IsAuth`. A nonzero $\Phi$ computed in the geometry selected here **triggers** nothing by itself: §8.4 routes the lift trigger to context-visible non-congruence in [6], and this paper licenses no lift and no terminal.

**Mechanization status:**`[MECHANIZATION CLAIMED; ARTIFACT NOT INCLUDED]`overall. The green build receipt, axiom audit, per-theorem scope, and the declared Lean-vs-paper gaps are recorded in the companion claim ledger. The Hahn–Banach discharge (PL-002-1) is genuinely closed; the necessity table (PL-002-2) is partial; Banach presheaves, the convex-body taxonomy, §3.5/§3.6, and (P4) are **not** mechanized.

**Remaining open obligations:** **S9b / PL-002-2 (partial)** — the satisfied-property half of the necessity table. **PL-002-3 / S10** — the initiality-to-reflection lemma, an inherited`[CONJECTURE, CONDITIONAL]`dependency from [6]; §8.4's reflective-completion material rests on it and Theorem 4.2 does not. **Prose-only, not mechanized:** (P4) and the §5 Stage-3 locality convention. **Imported, not proved here:** $d_1\circ d_0=0$.

### Import / Oracle boundary

**Import / Oracle boundary.** Any use of Hilbert space, Born uniqueness, phase, continuum, probability semantics, dynamics, physical interpretation, tensor composition, or empirical realization is an imported representation structure unless explicitly constructed at this paper's declared degree. Imported structures are not DDA operations and do not produce authority.

Concretely: this is a **finite** calculus — finite poset, finite edge set, finite direct sum — standing on an imported continuum ambient. The register:

| Import | Where | Status | Load-bearing? |
|---|---|---|---|
| **Hahn–Banach** (choice-dependent;`Classical.choice`appears in every cited Lean theorem) | Cor 2 (§2.5); Lemma 4.1 (§4); §8.2 |`IMPORTED`| **Yes — it is the engine of the paper's own load-bearing lemma.** |
| **Banach stalks / completeness** | §1.1 and throughout |`IMPORTED`| **Yes** — the declared ambient. (The Lean statement needs only a *normed* space; completeness is not used there.) |
| $\mathbb{R}_{\geq 0}$ **as the gauge codomain** | Def 1.1 (§1.3); §2.1 |`IMPORTED`| **Yes** — a continuum value domain for every diagnostic in this finite calculus. |
| **Haar measure / integration over a compact group** | Cor 3 (§2.4–2.5) |`IMPORTED`| No — construction corollary only; unused by Thm 4.2. |
| **$\mathrm{U}(n)$, CPTP maps, density operators, trace-class operators, trace norm** | §3.5, §3.6, §8.1 |`Q-gated`| No — fenced boundary examples (§3.6). |
| **Probability semantics** ("success probability", "equal priors", state pair $\rho,\sigma$) | §3.6, via Helstrom [8] |`IMPORTED`— **no probability adapter is declared here** | No. |
| **"Physical processes cannot increase operational distinguishability"** | §3.6 |`IMPORTED`physical interpretation | No. |
| **Observer passivity / no-creation (O1); $d_0$, $d_1$, $d_1\circ d_0=0$; contextual congruence; reflective completion** | §8.4, §8.5 |`IMPORTED`from [6] — internal-corpus import, *not* settled external mathematics | No — positioning only; Thm 4.2 rests on none of them. |

None of these are constructed at this paper's declared degree, and none of them produce authority.

## References

[1] V. Pestov, "Dynamics of infinite-dimensional groups and Ramsey-type phenomena," *Publicacoes Matematicas do IMPA*, 2006.
[2] R. E. Megginson, *An Introduction to Banach Space Theory*, Springer, 1998.
[3] J. H. Carroll, "Projection Obstruction for Factorized States: Nonlinear Dynamics, Conditional ℓ1 Diagnostics, and Finite-Time Defect Bounds," Zenodo, 2026. <https://zenodo.org/records/20650922>
[4] J. H. Carroll, "Coordinate-Wise Additivity and the L1 Norm on Finite Graph Cochains," Zenodo, 2026. <https://zenodo.org/records/20173236>
[5] J. H. Carroll, "L1-Native Cohomology of Defect Fields: Quotient Norms, Dual Circulations, and Hodge Inflation," Zenodo, 2026. <https://zenodo.org/uploads/20186523>
[6] J. H. Carroll, "Primitive Axiomatics of Finite Obstruction Calculus," Zenodo, 2026. <https://zenodo.org/records/20651224>
[7] J. von Neumann, “Some matrix inequalities and metrization of matric space,” *Mitt. Forschungsinst. Math. Mech. Kujbyschew-Univ. Tomsk* **1**, 286–300, 1937.
[8] C. W. Helstrom, *Quantum Detection and Estimation Theory*, Academic Press, 1976.
[9] J. H. Carroll, "CPTP-Invariant Obstruction Theory Trace-Norm Geometry and Quantum Dual Witnesses," Zenodo, 2026. <https://zenodo.org/records/20550459>
