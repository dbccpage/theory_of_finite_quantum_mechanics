# GS-000 — Coordinate-Wise Additivity and Local ℓ¹ Gauge Selection

**Author:** Jeremy H. Carroll  
**Canonical Publication:** `v6.1.1` (2026-06-16), DOI `10.5281/zenodo.20723753`

**Repository State:** unpublished post-v6.1.1 draft (2026-10-02); no later version or DOI assigned

**Paper Identity:** `GS-000`  
**Legacy File Identity:** `009_coordinate_wise_additivity.md`  

**Status:** Step 1 of the Gauge Selection Programme (purely finite coordinate-separable base theorem).

**Authority:** none. This paper may diagnose, price, route, or construct structure inside a declared obstruction regime. It does not mint authority. Any authority-bearing use requires a separate CODA-FDA / GTLA descent packet, terminalizer, evidence ceiling, replay witness, and `IsAuth` guard.

**Scope:** finite graph-cochain seminorm classification under coordinate-separable observer assumptions, with Lean4 support for exact finite helpers: CE1–CE4 arithmetic witnesses, a narrower CE5 arithmetic witness, Theorem 1 finite real cores, declared-orbit cores for Theorems 2–3, the Theorem 3 edge-uniformity collapse, and primitive-difference quotient-boundary helpers. CE5 as stated in prose and the real-cochain LGGR reading in §3.5 remain `OPEN / NOT_VERIFIED`; the narrower executable helpers do not promote them. PL-004-2 was recorded discharged 2026-06-20 only for its declared finite formulation; the observer-class hypotheses remain conditional. Mechanization scope, and the steps that remain assumed rather than derived in Lean, are itemized in the GTOC / GTLA Compliance Note.

**Main claim:** edge locality + coordinate permutation symmetry + disjoint-coordinate additivity + seminorm absolute homogeneity force coordinatewise $\ell^1$ on each edge; graph invariance gives orbit-weighted $\ell^1$; unweighted global $\ell^1$ requires edge-transitivity or explicit uniformity.

**Non-claim:** no finite-structural $\ell^1$, no claim about non-coordinate-separable observers, no unweighted global scalar without edge-uniformity, no Banach/dynamical result proved in this paper.

```{=latex}
\begin{nonclaim}
This paper does not claim finite-structural $\ell^1$ geometry, physical norm selection, Banach-presheaf rigidity, projection-obstruction dynamics, or unweighted global $\ell^1$ without edge-transitivity or explicit edge-uniformity. It shows in this model only the finite combinatorial base case: inside the coordinate-separable, edge-local, disjoint-additive observer class, the edgewise seminorm is coordinatewise $\ell^1$, and graph invariance gives orbit-weighted aggregation.
\end{nonclaim}

```

**Lean status.** The local `PaperGS003` Lean module ([`lean4/gs003_coordinate_l1.lean`](lean4/gs003_coordinate_l1.lean)) machine-checks CE1–CE4 arithmetic witnesses, an exact scoped helper named `ce5_lp_not_homogeneous`, Theorem 1 finite real scalar-witness/norm-positive cores, Theorem 2 declared-orbit aggregation cores, Theorem 3 orbit-uniform and edge-uniform collapse bridges, and finite `Nat`-valued primitive-difference quotient helpers. The CE5 helper does not verify the full prose counterexample, and the finite quotient helpers do not verify the real-cochain LGGR reading in §3.5. Both broader claims remain `OPEN / NOT_VERIFIED`. The global proof ledger marks PL-004-2 discharged only for the declared finite orbit-action formulation; the prose theorem still retains H1–H5 plus edge-transitivity or explicit uniformity as hypotheses.

**Read "cores" and "bridges" strictly.** Each Lean artifact supports only the exact finite statement it mechanizes. Theorem 1's real core is genuinely derived — $\nu$ is an opaque field, not assumed to be $w\lVert x\rVert_1$ — but the Theorem 2 and Theorem 3 artifacts **assume** their load-bearing steps (fiber isometry, weight factorization, uniformity) rather than deriving them, H2 is not modelled as a permutation action, and no graph, automorphism group, or derived orbit appears in the Lean at all. Per-theorem mechanization scope, and what "declared finite orbit-action formulation" excludes, are itemized in the Claim-Type Ledger and the GTOC / GTLA Compliance Note.

Lean reproducibility:

* `lake build PaperGS003` — green (exit 0) from a clean, short-path replay on 2026-09-28.
* The refreshed [`lean4/axiom_report.txt`](lean4/axiom_report.txt) covers all 43 declared `#print axioms` targets. Each exact Lean declaration depends only on subsets of `{propext, Classical.choice, Quot.sound}`.
* A clean build and axiom census establish only compilation and the dependency set of the exact Lean declarations. They do not promote CE5 or the manuscript-level §3.5 LGGR reading from `OPEN / NOT_VERIFIED`.
* File path: [`lean4/gs003_coordinate_l1.lean`](lean4/gs003_coordinate_l1.lean).
* The receipt is bound to the source digests listed in [`lean4/PROVENANCE.md`](lean4/PROVENANCE.md) and to the release manifest.

## Abstract

For finite graph cochains with coordinate-valued edge defects, any edge-local seminorm that is coordinate-permutation symmetric and additive over disjoint coordinate supports is forced to be a nonnegative scalar multiple of coordinatewise $\ell^1$ edgewise; positive weights require faithfulness/normhood; across edges the sharp conclusion is orbit-weighted $\ell^1$, with unweighted global $\ell^1$ requiring edge-transitivity or explicit uniformity. The additivity assumption is justified only for coordinate-separable, replica-extensive observers. Relaxing those assumptions yields alternative obstruction geometries.

**Conventions.** Norms are denoted $\lVert \cdot \rVert$ with appropriate subscripts; scalar absolute values are denoted $|\cdot|$.

**Why a researcher should care.** Many finite diagnostic systems decompose observations into coordinate channels: graph total variation, componentwise residuals, finite constraint violations, sparse defect fields, and coordinate-separable model-evaluation errors all have this form. This paper shows in this model that if those coordinate channels are treated as independent replicas and their disjoint supports must add exactly, then $\ell^1$ is not an arbitrary choice — it is forced inside that observer class. The result also says what is not forced: $\ell^2$, $\ell^\infty$, cross-edge cancellation, coordinate-weighted $\ell^1$, and orbit-weighted edge sums all reappear when the corresponding assumptions are removed.

## 1. Introduction

This paper is the first step in a sequence analyzing projection-induced defects on presheaf coboundaries through progressively richer structural settings:

* **This paper** establishes that coordinate-wise additivity and symmetry on finite graph cochains select coordinatewise $\ell^1$ geometry within the coordinate-separable observer class. The result is purely combinatorial and requires no functional-analytic or dynamical structure.
* **The M-compatible Banach-presheaf paper** [7] extends the classification under a different observer class: maximal bounded-linear local symmetry fixes the native stalk norm edgewise, and edge-additive aggregation then yields a weighted $\ell^1$ edge sum.
* **The projection-obstruction paper** [6] applies this rigidity in a setting that imports evolution and a projection map, and reports coboundary defects measured by a conditional $\ell^1$ diagnostic. Both the dynamics and the projection are imported representation structures relative to the present paper; nothing here derives them, and the $\ell^1$ measurement is forced there only under that paper's own declared hypotheses, not as an unconditional necessity.

The current package is `009_coordinate_wise_additivity` (legacy Paper 003 / Paper 004), and is logically prior to the Banach-presheaf and projection-obstruction papers. The numbering reflects repository order, not dependency order.

The purpose of the present paper is to isolate the minimal combinatorial realization of the replica-extensive, coordinate-separable observer class behind this rigidity. In the broader M-compatible framework, this corresponds to the case where coordinate channels are required to aggregate independently. Other symmetry classes yield different admissible gauges. Rather than beginning with Banach space assumptions or dynamical systems, we show that $\ell^1$ geometry is selected for finite graph cochains under coordinate-separable, replica-extensive evaluation.

A central modeling vulnerability is treating the summation of independent measurement channels as an ad hoc assumption ($L^2$ root-sum-squares assume an entirely different aggregation). We isolate that assumption rather than hiding it. When independent observations are required to compose additively over disjoint coordinate supports, the finite seminorm argument below forces linear absolute-value summation. Without that observer boundary, the conclusion does not follow.

**Falsifiability.** A proposed use of this classification fails if it cannot specify the finite graph, coordinate dimension $k$, edge-local decomposition, coordinate permutation action, disjoint-coordinate additivity condition, seminorm homogeneity, graph-isomorphism action, and any edge-uniformity assumption used to pass from orbit-weighted to unweighted $\ell^1$. The theorem would be falsified by a seminorm satisfying all stated hypotheses but not representable as $\sum_{\mathcal O}w_{\mathcal O}\sum_{e\in\mathcal O}\|\delta_e\|_1$.

---

## 1.1 Related Work and Positioning

This paper is closest to five bodies of work:

1. **Finite-dimensional norm and seminorm classification.** The proof is a finite-coordinate seminorm classification: disjoint-coordinate additivity plus homogeneity forces linear absolute-value summation. This paper differs by applying that elementary classification edgewise to graph cochains.

2. **Graph total variation and discrete coarea.** For $k=1$, the classified $\ell^1$ edge diagnostic matches graph total variation and connects to coarea and cut interpretations. This paper differs by making the observer assumptions selecting that diagnostic explicit.

3. **Max-flow / min-cut duality.** Under scalar boundary conditions, $\ell^1$-type graph total variation is related to cut problems. This paper differs by proving a norm-selection result, not a new max-flow theorem.

4. **Banach-space ($L^1$) / abstract ($L$)-space characterizations.** The finite result is a combinatorial analogue of $L^1$-type additivity over disjoint supports. This paper differs by staying entirely finite and graph-cochain based.

5. **M-compatible gauge classification and later obstruction papers.** Later papers replace coordinate-separability with Banach-presheaf functoriality or dynamical projection hypotheses. This paper is the finite combinatorial base case, not the Banach or dynamical theorem itself.

These are positioning anchors. The cited external results are used only for background context unless explicitly invoked in a theorem.

### 1.2 Notation

| Symbol               | Meaning                             |
| -------------------- | ----------------------------------- |
| $G=(V,E)$            | finite directed graph               |
| $C^1(G,\mathbb R^k)$ | edge cochain space                  |
| $\delta_e$           | vector value on edge $e$            |
| $\nu_G$              | global diagnostic seminorm          |
| $\nu_e$              | edge-local seminorm                 |
| $w_e$                | edge weight                         |
| $\mathcal O$         | edge orbit                          |
| $\alpha$             | global scalar under edge-uniformity |

## 2. The $\ell^1$ Characterization Proofs

Theorems 1–3 are finite elementary prose proofs. Lean mechanization is a reproducibility-hardening target, not a condition for the paper-level result.

### 2.1 Setup

### Genesis-Bias Fence — No Prior Host

This paper does not begin with a substrate that hosts the graph, a possibility domain that
contains the cochains, an ambient geometry that pre-selects a norm, a physical system the edges
represent, or an observer standing outside the comparison. It begins with **declared,
packet-local finite data**: an index set of edges $E$, an index set of coordinates
$\{1,\dots,k\}$, a declared scalar specialization $\mathbb R$, and a declared comparison scope
(the axioms H1–H5 below).

$G=(V,E)$, $k$, and the coordinate fiber are **declared**, not derived and not antecedent. The
graph is not a prior container from which cochains issue; it is the finite index data the
declared comparison ranges over. `[DEFINITION]` below records that declaration — it does not
report a discovery about a pre-existing space.

The "observer" of this paper is a **declared-comparison scope** (charter convention K6): the
bundle H1–H5 and nothing more. It carries no privilege, no standpoint outside the differences it
compares, and no authority. Where the prose says a geometry is "forced" or "selected", the
scope of that force is exactly this declared bundle.

**Pricing the stronger readings.** $\mathbb R$ is a **declared scalar specialization**, not a
derived one — absolute homogeneity over $\mathbb R$ is admitted here, not earned. $\bigoplus_e
\mathbb R^k$ is a declared finite carrier, not a finite-structural state space. Neither the graph nor the
fiber is claimed to be prior to, or to explain, the differences the diagnostic measures.

> **GENESIS-BIAS AUDIT.** Does this section explain $\ell^1$ selection by presupposing a prior
> container, substrate, state-space, law, observer, temporal order, possibility domain, sample
> space, Hilbert space, physical system, or authority source? If so, declare and price that
> antecedent, replace it with packet-local data, or stop with an OBSTRUCTION. — Answer: the
> graph, the coordinate fiber, and the scalar field are declared and priced above as
> packet-local index data and a declared scalar specialization. No prior host is claimed.
>

Let $G=(V,E)$ be a finite directed graph and $k\ge1$ an integer, declared as above, and

**[DEFINITION]**
$$
C^1(G,\mathbb R^k)=\bigoplus_{e\in E}\mathbb R^k.
$$

An element $\delta\in C^1(G,\mathbb R^k)$ assigns to every edge $e\in E$ a vector

$$
\delta_e=(\delta_{e,1},\ldots,\delta_{e,k})\in\mathbb R^k.
$$

Let

$$
\nu_G:C^1(G,\mathbb R^k)\to\mathbb R_{\ge0}
$$

be a seminorm satisfying the assumptions below. In H1, the local terms
$\nu_e:\mathbb R^k\to\mathbb R_{\ge0}$ are nonnegative maps. Evaluating H1
on the zero cochain gives $\sum_e\nu_e(0)=0$, hence every $\nu_e(0)=0$.
Restricting $\nu_G$ to cochains supported on one edge then gives exactly
$\nu_e$, so each local term inherits seminormhood. Equivalently, one can
declare the local seminorms at the outset.

If $E=\varnothing$, the global carrier is zero-dimensional and its unique
seminorm is zero; orbit statements are vacuous and one may take $\alpha=0$.
The basis and positivity arguments below use $k\ge1$; edge-transitivity is
used on a nonempty edge set. The $k=0$ case is excluded because it has no first
basis vector and its scalar weight is not identifiable.

The observer assumptions are:

1. **[AXIOM / DEFINITION OF OBSERVER CLASS] (H1) Edge locality**

$$
\nu_G(\delta)=\sum_{e\in E}\nu_e(\delta_e).
$$

2. **[AXIOM / OBSERVER ASSUMPTION] (H2) Coordinate permutation symmetry**

For every permutation $\sigma\in S_k$,

$$
\nu_e(x_{\sigma(1)},\ldots,x_{\sigma(k)}) = \nu_e(x_1,\ldots,x_k).
$$

3. **[AXIOM / OBSERVER ASSUMPTION] (H3) Disjoint-coordinate additivity**

If $\operatorname{supp}(x)\cap\operatorname{supp}(y)=\varnothing$, then

$$
\nu_e(x+y)=\nu_e(x)+\nu_e(y).
$$

Here “replica-extensive” means exact additivity over declared disjoint coordinate supports. It is an observer assumption, not a property of all diagnostics or all physical systems.

4. **[AXIOM / OBSERVER ASSUMPTION] (H4) Graph isomorphism invariance**

If $\phi:G\to G'$ is a graph isomorphism, then

$$
\nu_{G'}(\phi_*\delta)=\nu_G(\delta).
$$

Here $\phi_*$ relabels edges; if a nontrivial action on the coordinate fiber $\mathbb R^k$ is declared, it is assumed to act by (possibly signed) coordinate permutations, hence $\ell^1$-isometrically. This explicit fiber hypothesis is what Theorem 2 uses when comparing edge weights across an orbit.

5. **[AXIOM / OBSERVER ASSUMPTION] (H5) Seminorm absolute homogeneity**

Carried by the standing assumption that $\nu_G$, and hence each $\nu_e$, is a seminorm:

$$
\nu_e(cx)=|c|\,\nu_e(x)\qquad(c\in\mathbb R).
$$

Listed explicitly because the status claims in the front matter and the Lean bridges quantify over it. Absolute homogeneity is admitted over the **declared scalar specialization** $\mathbb R$ (Genesis-Bias fence above); it is not derived here.

**Hypothesis register.** H1 edge locality; H2 coordinate permutation symmetry; H3 disjoint-coordinate additivity; H4 graph-isomorphism invariance with $\ell^1$-isometric (signed-permutation) fiber action; H5 seminorm absolute homogeneity. Every "[PROVEN, CONDITIONAL]" tag in this paper is conditional on the subset of H1–H5 named at the theorem, and on nothing else.

### 2.2 **[PROVEN, CONDITIONAL] Theorem 1 — Coordinatewise Additivity Forces a Nonnegative Scalar Multiple of Coordinatewise $\ell^1$ Edgewise; Positive Weights Require Faithfulness/Normhood**

**Statement:**

For each edge $e$, there exists a scalar $w_e\ge0$ such that

$$
\nu_e(x)=w_e\|x\|_1 = w_e\sum_{i=1}^k |x_i|
$$

for all $x\in\mathbb R^k$.

If $\nu_e$ is a norm, then $w_e>0$. The scalar is unique because $k\ge1$ and $w_e=\nu_e(e_1)$.

**Proof:**

Let

$$
x=(x_1,\ldots,x_k)\in\mathbb R^k.
$$

Write $e_i$ for the $i$-th standard coordinate vector. Then

$$
x=\sum_{i=1}^k x_i e_i.
$$

The vectors $x_i e_i$ have pairwise disjoint coordinate support. Therefore, by disjoint-coordinate additivity,

$$
\nu_e(x) = \nu_e\left(\sum_{i=1}^k x_i e_i\right) = \sum_{i=1}^k \nu_e(x_i e_i).
$$

Since $\nu_e$ is a seminorm, it is absolutely homogeneous:

$$
\nu_e(x_i e_i)=|x_i|\nu_e(e_i).
$$

By coordinate permutation symmetry, all coordinate basis vectors have the same seminorm value:

$$
\nu_e(e_1)=\nu_e(e_2)=\cdots=\nu_e(e_k).
$$

Set

$$
w_e:=\nu_e(e_1).
$$

Then

$$
\nu_e(x) = \sum_{i=1}^k |x_i|w_e = w_e\sum_{i=1}^k |x_i| = w_e\|x\|_1.
$$

The scalar is nonnegative since $\nu_e(e_1)\ge0$, and positive under normhood since $e_1\ne0$. Thus each edge seminorm is coordinatewise $\ell^1$, up to its unique edge weight. $\square$

### 2.3 **[PROVEN, CONDITIONAL] Theorem 2 — Orbit-Weighted Global Aggregation**

**Statement:**

Let the automorphism group of the graph, or the declared admissible graph-isomorphism action, partition the edge set $E$ into edge orbits

$$
E=\bigsqcup_{\mathcal O} \mathcal O.
$$

Then there exist weights $w_{\mathcal O}\ge0$, constant on edge orbits, such that

$$
\nu_G(\delta) = \sum_{\mathcal O} w_{\mathcal O} \sum_{e\in\mathcal O} \|\delta_e\|_1.
$$

Orbit weights may be zero for seminorms. If the global diagnostic is required to be faithful on each edge orbit, the corresponding orbit weights are positive.

**Proof:**

By Theorem 1, for each edge $e$,

$$
\nu_e(\delta_e)=w_e\|\delta_e\|_1.
$$

By edge locality,

$$
\nu_G(\delta) = \sum_{e\in E}\nu_e(\delta_e) = \sum_{e\in E}w_e\|\delta_e\|_1.
$$

Now let $e,e'\in E$ lie in the same edge orbit. Then there exists a graph automorphism $\phi:G\to G$ such that

$$
\phi(e)=e'.
$$

Take a cochain $\delta$ supported only on edge $e$, with value $u\in\mathbb R^k$:

$$
\delta_e=u,\qquad \delta_f=0\quad(f\ne e).
$$

Then

$$
\nu_G(\delta)=w_e\|u\|_1.
$$

The pushed-forward cochain $\phi_*\delta$ is supported only on $e'$, with the same coordinate value $u$ up to the declared coordinate action — which, being a (signed) coordinate permutation by Axiom 4, preserves $\|u\|_1$. By graph invariance,

$$
\nu_G(\phi_*\delta)=\nu_G(\delta).
$$

Thus

$$
w_{e'}\|u\|_1=w_e\|u\|_1.
$$

Choose $u\ne0$. Then $\|u\|_1>0$, so

$$
w_{e'}=w_e.
$$

Therefore edge weights are constant on edge orbits. Write the common value on orbit $\mathcal O$ as $w_{\mathcal O}$. Hence

$$
\nu_G(\delta) = \sum_{\mathcal O} w_{\mathcal O} \sum_{e\in\mathcal O} \|\delta_e\|_1.
$$

$\square$

### 2.4 **[PROVEN, CONDITIONAL + edge-transitivity or explicit uniformity] Theorem 3 — Edge-Uniformity Reduces to Unweighted Global $\ell^1$**

**Statement:**

If the graph action is edge-transitive, or if one imposes an explicit edge-uniformity/naturality axiom forcing all edge weights to agree, then there exists a single scalar $\alpha\ge0$ such that

$$
\nu_G(\delta) = \alpha\sum_{e\in E}\|\delta_e\|_1.
$$

If $\alpha=1$, this is exactly the standard unweighted $\ell^1$ norm on

$$
E\times\{1,\ldots,k\}.
$$

**Proof:**

From Theorem 2,

$$
\nu_G(\delta) = \sum_{\mathcal O} w_{\mathcal O} \sum_{e\in\mathcal O} \|\delta_e\|_1.
$$

If the graph action is edge-transitive, then $E$ consists of a single orbit:

$$
E=\mathcal O.
$$

Therefore

$$
\nu_G(\delta)=w_{\mathcal O}\sum_{e\in E}\|\delta_e\|_1.
$$

Set

$$
\alpha:=w_{\mathcal O}.
$$

Then

$$
\nu_G(\delta)=\alpha\sum_{e\in E}\|\delta_e\|_1.
$$

Alternatively, if there are several edge orbits but an explicit edge-uniformity axiom imposes

$$
w_{\mathcal O}=\alpha
$$

for every orbit $\mathcal O$, then

$$
\nu_G(\delta) = \sum_{\mathcal O} \alpha \sum_{e\in\mathcal O} \|\delta_e\|_1 = \alpha \sum_{e\in E} \|\delta_e\|_1.
$$

Finally,

$$
\sum_{e\in E}\|\delta_e\|_1 = \sum_{e\in E}\sum_{i=1}^k |\delta_{e,i}| = \|\delta\|_{\ell^1(E\times\{1,\ldots,k\})}.
$$

Thus the edge-uniform case is the standard finite $\ell^1$ norm, up to scalar normalization. $\square$

### Worked Replay — Orbit-Weighted Coordinatewise $\ell^1$

Let $G$ have two directed edges $e_1,e_2$, with $k=2$. Suppose the admissible graph action fixes the two edges separately, so they lie in distinct edge orbits. Let
$$
\delta_{e_1}=(3,-4),\qquad \delta_{e_2}=(1,2).
$$
By Theorem 1, each edge term is coordinatewise $\ell^1$. With orbit weights $w_{e_1}=1,\ w_{e_2}=2$,
$$
\nu_G(\delta) = 1(|3|+|-4|)+2(|1|+|2|) = 7+6 = 13.
$$
If edge-uniformity is imposed with $\alpha=1$, the same cochain has
$$
\|\delta\|_1=(|3|+|-4|)+(|1|+|2|)=10.
$$
Thus graph invariance alone permits orbit-weighted $\ell^1$; the unweighted value requires the additional uniformity assumption.

Minimal replay:

```python
d1 = (3, -4)
d2 = (1, 2)
w1, w2 = 1, 2

def l1(x):
    return sum(abs(t) for t in x)

orbit_weighted = w1*l1(d1) + w2*l1(d2)
unweighted = l1(d1) + l1(d2)

print(orbit_weighted)
print(unweighted)

```

Expected output:

```text
13
10

```

### 2.5 Counterexamples

CE1–CE3 witness the roles of H3, H2, and H1, respectively; CE4 witnesses the
extra edge-uniformity assumption, which is not one of H1–H5. CE1 and CE2 use
$k\ge2$. For CE2 and CE3, take trivial fiber transport so that H4 does not
impose an additional coordinate action. CE5 must weaken the standing
seminorm premise as well as H5: homogeneity cannot be removed while still
calling the map a seminorm. Its full matching formalization remains open.

The Lean CE1 and CE3 declarations are narrower arithmetic models: a quadratic
function on $\mathbb N^2$ and a coupled polynomial on $\mathbb N^2$,
respectively. They are not formal proofs that the real $\ell^2$ norm or
$|a+b|$ satisfies all retained observer assumptions.

#### **[PROVEN BY COUNTEREXAMPLE] Counterexample 1 — If Coordinate Additivity Is Removed, $\ell^2$ Is Allowed**

Define, on each edge,

$$
\nu_e(x)=\|x\|_2 = \left(\sum_{i=1}^k x_i^2\right)^{1/2}.
$$

Then $\nu_e$ is a norm. It is coordinate permutation symmetric:

$$
\|(x_{\sigma(1)},\ldots,x_{\sigma(k)})\|_2=\|x\|_2.
$$

It is absolutely homogeneous and subadditive.

But for disjointly supported vectors $x=(1,0)$ and $y=(0,1)$,

$$
\nu_e(x+y)=\|(1,1)\|_2=\sqrt2,
$$

while

$$
\nu_e(x)+\nu_e(y)=1+1=2.
$$

So

$$
\nu_e(x+y)\ne\nu_e(x)+\nu_e(y).
$$

Thus without coordinate additivity, the conclusion $\nu_e=w_e\|x\|_1$ fails.

> **Coordinate symmetry alone does not force $\ell^1$.**
>

#### **[PROVEN BY COUNTEREXAMPLE] Counterexample 2 — If Coordinate Symmetry Is Removed, Weighted Coordinate $\ell^1$ Is Allowed**

Define

$$
\nu_e(x)=\sum_{i=1}^k a_i |x_i|
$$

with positive but unequal weights $a_i>0$. For example, in $\mathbb R^2$,

$$
\nu_e(x_1,x_2)=|x_1|+2|x_2|.
$$

This is a norm. It is additive on disjoint supports:

$$
\nu_e(x+y)=\nu_e(x)+\nu_e(y)
$$

whenever $\operatorname{supp}(x)\cap\operatorname{supp}(y)=\varnothing$.

But it is not coordinate permutation symmetric. Indeed,

$$
\nu_e(1,0)=1,
$$

while

$$
\nu_e(0,1)=2.
$$

Therefore the conclusion becomes coordinate-weighted $\ell^1$, not scalar coordinatewise $\ell^1$.

> **Without coordinate symmetry, additivity gives weighted $\ell^1$, not uniform coordinate $\ell^1$.**
>

#### **[PROVEN BY COUNTEREXAMPLE] Counterexample 3 — If Edge Locality Is Removed, Cross-Edge Coupling Is Allowed**

Let $G$ have two edges $e_1,e_2$, and take $k=1$. A cochain is

$$
\delta=(a,b)\in\mathbb R^2.
$$

Define

$$
\nu_G(\delta)=|a+b|.
$$

This is a seminorm on $C^1(G,\mathbb R)$.

It is not edge-local because it cannot be written as

$$
\nu_G(\delta)=\nu_{e_1}(a)+\nu_{e_2}(b)
$$

for edgewise seminorms $\nu_{e_1},\nu_{e_2}$.

To see this, take $(a,b)=(1,0)$ and $(0,-1)$. If edge locality held, then

$$
\nu_G(1,0)=\nu_{e_1}(1)+\nu_{e_2}(0)=1,
$$

and

$$
\nu_G(0,-1)=\nu_{e_1}(0)+\nu_{e_2}(-1)=1.
$$

So locality would imply

$$
\nu_G(1,-1)=2.
$$

But actually

$$
\nu_G(1,-1)=|1-1|=0.
$$

Contradiction.

Thus without edge locality, cancellation between edges is possible. The global seminorm need not be an edge-sum of $\ell^1$ terms.

> **Without edge locality, cross-edge cancellation destroys edgewise $\ell^1$ aggregation.**
>

#### **[PROVEN BY COUNTEREXAMPLE] Counterexample 4 — If Edge-Uniformity Is Removed, Orbit-Weighted $\ell^1$ Need Not Reduce to Unweighted $\ell^1$**

Let $G$ be a directed path with two edges $e_1,e_2$, and suppose the admissible graph automorphism group fixes the two edges separately, so they lie in distinct edge orbits.

Define, for $k=1$,

$$
\nu_G(\delta)=|\delta_{e_1}|+2|\delta_{e_2}|.
$$

This satisfies edge locality. It also satisfies coordinate symmetry vacuously since $k=1$, and disjoint-coordinate additivity is vacuous on each scalar edge.

It is graph-invariant under the trivial automorphism group.

But it is not proportional to the unweighted $\ell^1$ norm

$$
|\delta_{e_1}|+|\delta_{e_2}|.
$$

Indeed,

$$
\nu_G(1,0)=1,
$$

while

$$
\nu_G(0,1)=2.
$$

No single scalar $\alpha$ satisfies both

$$
\alpha=\nu_G(1,0)=1
$$

and

$$
\alpha=\nu_G(0,1)=2.
$$

Thus the best general theorem is orbit-weighted $\ell^1$, not globally unweighted $\ell^1$.

> **Graph invariance alone gives orbit weights; edge-uniformity is an extra axiom.**
>

#### **[OPEN / NOT_VERIFIED] Counterexample 5 — A Nonlinear Gauge Candidate after Weakening the Seminorm Premise**

Replace the seminorm premise by a nonnegative, zero-at-zero, subadditive gauge, and retain coordinate symmetry and disjoint-coordinate additivity. The candidate on $\mathbb R^k$ is

$$
\Phi(x)=\sum_{i=1}^k |x_i|^p
$$

for $0<p<1$. This range makes $0^p=0$ and permits subadditivity. The broader earlier range $p\ne1$ was insufficient: $p\le0$ causes a zero-coordinate problem, while $p>1$ loses subadditivity as well as homogeneity.

This is coordinate permutation symmetric and additive over disjoint coordinate support:

$$
\Phi(x+y)=\Phi(x)+\Phi(y)
$$

when supports are disjoint.

But

$$
\Phi(cx)=|c|^p\Phi(x),
$$

not

$$
|c|\Phi(x).
$$

For $0<p<1$, the scalar inequality $|a+b|^p\le |a|^p+|b|^p$ gives subadditivity after summing coordinates. Nevertheless the scaling above fails H5 for a nonzero vector and, for example, $c=2$. At $p=1$ the family becomes the $\ell^1$ norm. The shipped Lean helper fixes $p=2$ and checks only a natural-number scaling inequality; that helper also lies outside the subadditive candidate range.

The shipped Python and Lean helpers verify narrower, fixed arithmetic witnesses
of non-homogeneity. They do not establish the full parameter range and every
hypothesis asserted by this prose construction. Therefore CE5 remains
`OPEN / NOT_VERIFIED`; the equations above state the intended candidate, not a
promoted paper result.

> **Disjoint additivity plus symmetry without homogeneity does not force $\ell^1$ scaling.**
>

### 2.6 **[PROVEN, CONDITIONAL] Final Consolidated Theorem**

Under the full assumptions:

* Edge locality
* Coordinate permutation symmetry
* Disjoint-coordinate additivity
* Seminorm homogeneity
* Graph isomorphism invariance

one obtains:

$$
\nu_G(\delta) = \sum_{\mathcal O} w_{\mathcal O} \sum_{e\in\mathcal O} \|\delta_e\|_1.
$$

Under edge-transitivity or explicit edge-uniformity:

$$
\nu_G(\delta) = \alpha \sum_{e\in E} \sum_{i=1}^k |\delta_{e,i}|.
$$

And the counterexamples show:

* **Remove coordinate additivity** $\to$ $\ell^2$ / $\ell^\infty$ / mixed gauges allowed
* **Remove coordinate symmetry** $\to$ coordinate-weighted $\ell^1$ allowed
* **Remove edge locality** $\to$ cross-edge coupling/cancellation allowed

* **Remove edge-uniformity** $\to$ orbit-weighted $\ell^1$ is the sharp result
* **Weaken the seminorm premise and remove homogeneity** $\to$ nonlinear separable gauges are a candidate (`OPEN / NOT_VERIFIED`, CE5)

#### **[INTERPRETIVE / OPEN] Connection to Projection-Congruence Core ($ENC-0209$)**

A failure of H1 or H3 invalidates this classification. It does not, by itself,
prove a returning projection obstruction or prevent an unrelated quotient
from existing. A PCC application must separately specify its state carrier,
projection, transition rule, congruence relation, and a theorem connecting
that structure to these cochain diagnostics. No such bridge is proved or
packaged here; the `PCC.adequacy` connection is a programme motivation only.


## 3. Structural Consequences

### 3.1 Coarea Duality ($k = 1$)

**[STANDARD + elementary finite proof] Fact 3.1 (Weighted Discrete Coarea).**
For a scalar vertex signal $v:V\to\mathbb R$ and fixed weights $w_e\ge0$, set

$$
\operatorname{TV}_w(v)=\sum_{e=(m,n)\in E}w_e|v_n-v_m|,
\qquad V_t=\{m:v_m>t\}.
$$

Then

$$
\operatorname{TV}_w(v)=\int_{-\infty}^{\infty}
\sum_{e=(m,n)\in E}w_e
|\mathbf1_{V_t}(n)-\mathbf1_{V_t}(m)|\,dt.
$$

For each edge the indicator difference has absolute value one on the interval
between its two endpoint values and zero elsewhere; its integral is therefore
$|v_n-v_m|$. Multiply by $w_e$ and sum finitely. At $w_e=1$, the integrand
counts boundary-crossing edges. This is the finite graph specialization of
coarea background [2,3]; see also the explicit graph proof in [10, Appendix B].

**Orientation convention.** Each declared edge is counted once regardless of
its orientation. Opposite directed edges, if both are listed, both contribute.
This absolute-value TV yields the cut of the underlying undirected weighted
multigraph, not a one-way directed-cut objective.

**[STANDARD + finite threshold argument] Cut specialization.** For distinct
vertices $a,b$, minimize $\operatorname{TV}_w(v)$ with $v_a=1$, $v_b=0$.
Clipping to $[0,1]$ cannot increase any edge difference. Each threshold
$0<t<1$ gives a cut containing $a$ and excluding $b$, so coarea bounds the
minimum below by the minimum such cut capacity. Conversely, the indicator of
a minimum cut is feasible and has TV equal to that capacity. Thus a binary
minimizer exists; the boundary values alone do not force every minimizer to be
binary. Max-flow/min-cut [5] applies to the undirected capacitated network, or
its replacement by two opposite equal-capacity arcs for each edge.

**[PROVEN, CONDITIONAL] Remark 3.2.** For $k>1$, the weighted diagnostic of a
vertex coboundary is $\sum_{i=1}^k\operatorname{TV}_w(v_i)$, so coarea applies
coordinate by coordinate. This specialization concerns coboundaries of vertex
signals; an arbitrary edge cochain need not be a coboundary.

### 3.2 The Geometry of the Defect Field

The explicit inclusion of **Coordinate Additivity** formally captures the declared independence of distinct observed coordinates. Permutation symmetry and absolute homogeneity alone permit alternative norms such as $\ell^\infty$ or $\ell^2$. The strict structural requirement that isolated defect channels accumulate their structural signatures linearly thereby determines the $\ell^1$ stalk geometry under these constraints.

Thus, the seminorm compatible with the stated local coordinate-additivity and coordinate-symmetry constraints is coordinatewise $\ell^1$ on each edge. Uniform $\ell^1$ over the product index set requires the additional edge-uniformity assumption stated in Theorem 3.

Conceptually, our theorem establishes (cf. [4]) that:
**[PROVEN, CONDITIONAL + uniform weights + $\alpha>0$]** As a normed diagnostic space under the selected uniform $\ell^1$ diagnostic with $\alpha>0$, $C^1(G,\mathbb R^k)$ is isometric to the finite $L^1$ space on $E\times\{1,\dots,k\}$. The strict positivity is load-bearing: on a nonzero carrier, $\alpha=0$ gives an identically zero seminorm, not a norm. Its separated quotient is the zero space. For $\alpha>0$, the map $\delta\mapsto\alpha\delta$ is an isometry to the standard counting-measure $L^1$ space; equivalently, the identity map uses mass $\alpha$ at each point. This identification is a **measure-theoretic import** used for identification only; no measure, proportion, or probability semantics is derived here (see the Import / Oracle boundary). More generally the result is a finite weighted $L^1$ geometry. **[INTERPRETIVE / STANDARD BACKGROUND + citation]** This serves as a finite combinatorial analogue of Kakutani's (1941) concrete characterization of abstract $L$-spaces [1]. Local additivity across independent structural components selects $\ell^1$-type geometry over the relevant finite measure. Defect fields in the uniform scalar case behave as discrete 1-forms whose absolute total variation tracks graph cuts and sparse obstructions [3].

### 3.3 Role in the Broader Classification Program

The result obtained here isolates the combinatorial origin of $\ell^1$-type geometry as a consequence of coordinate-wise and edge-wise separability. In subsequent work, this principle is generalized. In particular, when the cochain spaces are replaced by Banach presheaves and coordinate additivity is replaced by structural compatibility in the form of functoriality under bounded linear maps [7], the same weighted $\ell^1$ edge-sum structure is recovered, with uniformity requiring additional symmetry or normalization.

The present theorem should not be interpreted as asserting universality of $\ell^1$ across all observers. Rather, it identifies the unique geometry compatible with coordinate-wise independence and replica-extensive aggregation. In the general M-compatible classification, relaxing coordinate additivity admits alternative geometries such as $\ell^2$ and mixed norms. The present theorem therefore provides the minimal combinatorial base case from which the more general Banach [7] and dynamical [6] results can be understood as specific structural extensions.

### 3.4 Conditional Characterization of $\ell^1$

**[INTERPRETIVE / PROVEN, CONDITIONAL if formalized] Formalizing this compressed characterization requires PL-004-1: definitions of refinement-invariant and regular, plus the proof that the resulting scalar function satisfies $\psi(t)=C|t|$.**

> **Status divergence (recorded, not resolved).** The global proof ledger records PL-004-1 as **DISCHARGED 2026-06-20** (ENC-0526, CONDITIONAL→PROVED-PROSE, tier T3; `lean_status: NOT-STARTED`), for the corrected conditional statement given below. This section retains `[INTERPRETIVE]` pending the explicit theorem-ledger mapping and adversary acceptance required by the formalization-status firewall. The status is **deliberately not upgraded here**; a hygiene pass does not promote claims. Reconciling this divergence is an open obligation.
>

A compressed form of the result is the following. If a diagnostic $\Phi$ is coordinate-separable, refinement-invariant, homogeneous, and additive across independent coordinates, then it has the form

$$
\Phi(x)=\sum_i \psi(x_i)
$$

with one **even** scalar branch $\psi$, and with either (a) $\psi$ absolutely homogeneous, or (b) $\psi$ additive and regular **on each sign half-line**. Hence $\psi(t)=C|t|$ with $C\ge0$, and

$$
\Phi(x)=C\sum_i |x_i|.
$$

**The evenness / sign-reflection hypothesis is load-bearing and was omitted in earlier revisions of this section.** Without it the compressed statement is false, in both directions: additivity of a *nonnegative* $\psi$ across all of $\mathbb R$ forces $\psi(t)+\psi(-t)=\psi(0)=0$ with both terms $\ge0$, hence $\psi\equiv0$; while regular additivity on each half-line without sign reflection admits distinct positive and negative slopes, which is not $C|t|$. The corrected conditional form above is the one recorded in the encyclopedia at ENC-0526.

Thus $\ell^1$ is selected by coordinate separability, additive aggregation, an even branch, and regularity. Relaxing any of these assumptions admits alternative geometries. This compressed statement should be read as a heuristic summary of the finite theorem unless the terms ‘refinement-invariant’ and ‘regular’ are formally defined here.

### 3.5 Quotient Boundaries and the **[OPEN / NOT_VERIFIED]** LGGR Interpretation

Three distinct comparisons must be kept separate. The elementary factorization
facts below correct the earlier fixed-profile non-descent assertion; they do
not claim the broader cross-graph LGGR specialization is mechanized.

**Fixed graph and fixed weights.** Define $D_w(\delta)=(w_e\|\delta_e\|_1)_e$
and $\delta\sim_w\delta'$ iff $D_w(\delta)=D_w(\delta')$. Then

$$
\nu_G(\delta)=\sum_e D_w(\delta)_e.
$$

Thus $\nu_G$ factors through $D_w$, and equal per-edge diagnostics force equal
global totals for every fixed profile, including nonuniform and zero weights.
The pairing $\delta\mapsto(D_w(\delta),w)$ also factors through this relation
because $w$ is constant on the carrier. The same conclusion holds when the
fixed-profile relation records the unweighted per-edge values instead.

**Coarser total-only relation.** Let $U(\delta)=\sum_e\|\delta_e\|_1$ and
identify cochains only when $U(\delta)=U(\delta')$. For fixed weights $(1,2)$,
edge magnitude profiles $(7,3)$ and $(3,7)$ both have $U=10$, but weighted
totals $13$ and $17$. This witnesses failure of factorization through $U$,
not through the per-edge relation. Uniformity makes $\nu_G=\alpha U$; if
$E\ne\varnothing$ and $k\ge1$, testing each unit-edge cochain shows that a
representation $\nu_G=f\circ U$ requires all edge weights to agree.

**Varying-profile record carrier.** On records $(\delta,w)$, suppose the
relation records only the unweighted per-edge values and forgets $w$.
The same cochain with magnitudes $(7,3)$ and profiles $(1,2)$ or $(2,2)$ gives
totals $13$ or $20$. A weight-sensitive total or pairing therefore need not
descend. A fixed declared profile repairs that loss; only requiring each
record's profile to be uniform does not, unless the scalar is shared across
the comparison. The shipped finite `Nat` record helpers permit weights to
vary in this way. They are not a theorem about two real cochains under one
fixed diagnostic.

**Programme boundary.** Identifying a specified cross-graph comparison with
LGGR [8,9] remains `OPEN / NOT_VERIFIED`. It requires an explicit real carrier,
relation, graph transport, and claim-to-formalization map. Nonuniform weights
alone do not create a failure of descent through per-edge diagnostics.

### 3.6 **[INTERPRETIVE]** Connection to EPK (Epistemic Primacy of the Kernel)

The classification depends on the full observer bundle, not on a linear kernel
alone. On $\mathbb R^k$ with $k\ge2$, the $\ell^1$ and $\ell^2$ norms both have
kernel $\{0\}$ but differ geometrically. Even the equality relation of an
observable does not fix its numeric scale: multiplying a diagnostic by any
positive scalar leaves that relation unchanged.

For the classified edge sum, its linear kernel is exactly the set of cochains
supported on zero-weight edges. H3, H2, and H5 determine the coordinate form;
H4 constrains orbit weights; edge-uniformity constrains the global form.
These are stronger data than the kernel. A coordinate-compatible vertex
coboundary $d_0$ may be supplied in an extension, but its kernel is determined
by that operator and graph, and is not derived from norm selection.

The EPK connection is therefore an interpretive reminder to state which
distinctions an observer preserves and which data a quotient forgets. This
paper establishes no general claim that a kernel uniquely selects a norm.

**Generalization frontier.** When coordinate-separability is relaxed:

* Replacing coordinate permutation symmetry with $SO(k)$ invariance is the standard route toward $\ell^2$. **This paper does not establish that route, and Counterexample 1 does not establish it either.** CE1 shows only that $\ell^2$ *is permitted* once disjoint-coordinate additivity is dropped — it exhibits $\ell^2$ as $SO(k)$-invariant and not disjoint-additive. It does **not** show that $SO(k)$ invariance *forces* $\ell^2$; that converse is a separate classification claim, not proved here and not implied by CE1. **[OPEN / IMPORTED]** Obtaining $\ell^2$ requires importing an inner product (or an equivalent quadratic/rotation-invariant structure) at this degree. That import is not earned anywhere in this paper: nothing here derives an inner product, and the $\ell^2$ readout is Q-gated in the surrounding series. What is available here is the negative half only — $\ell^2$ is excluded by H3, per CE1.
* Replacing coordinate-separable boundaries with general Banach-presheaf functoriality gives the M-compatible gauge classification [7] (see ENC-0652).
* Replacing the finite carrier with an infinite-dimensional one requires functional-analytic hypotheses (Kakutani's theorem [1]).

The finite theorem selects a diagnostic form inside the declared observer class. It does not remove the freedom to choose another class or a permitted weight profile.

---

## Claim-Type Ledger

| Result | Type | Lean4 Status |
|---|---|---|
| Main abstract claim | [PROVEN, CONDITIONAL] | Prose proof in Theorems 1–3; Lean4 support partial |
| $C^1(G,\mathbb R^k)$ setup | [DEFINITION] | N/A |
| Edge locality | [AXIOM / DEFINITION] | N/A |
| Coordinate permutation symmetry | [AXIOM / OBSERVER] | N/A |
| Disjoint-coordinate additivity | [AXIOM / OBSERVER] | N/A |
| Graph isomorphism invariance | [AXIOM / OBSERVER] | N/A |
| Theorem 1 | [PROVEN, CONDITIONAL] | **[MECHANIZED-PARTIAL]** — real finite-coordinate core genuinely derived (`coord_real_l1_weighted_sum`, `coord_real_l1_scalar_sum_succ`, `coord_real_l1_exists_scalar_succ` for $w\ge0$, `coord_real_l1_norm_scalar_positive_succ` for $w>0$): $\nu$ is an opaque field, not assumed to be $w\lVert x\rVert_1$. **Gap:** H2 is not modelled as a permutation action; it enters only as its consequence, the `basis_equal` field. The exact declarations are covered by the refreshed receipt. |
| Theorem 2 | [PROVEN, CONDITIONAL] | **[MECHANIZED-PARTIAL]** — `orbit_weight_eq_of_isometric_single_edge_invariance` shows in this model weight equality under an **assumed** fiber-isometry hypothesis; `orbit_weighted_l1_aggregation` **assumes** the weight factorization (`hfactor`) that the prose Theorem 2 derives. **Gap:** no graph, no $\mathrm{Aut}(G)$, no derived orbits — `orbit : E → O` is an arbitrary declared classifier; the ℓ¹ form is baked into `edgeWeightedL1Total` rather than composed from Theorem 1's witness. The exact declarations are covered by the refreshed receipt. |
| Theorem 3 | [PROVEN, CONDITIONAL] | **[MECHANIZED-PARTIAL]** — `orbit_uniform_l1_collapse` / `edge_uniform_l1_collapse` **assume** uniformity (`huniform`) and collapse in two lines; `edge_uniformity_collapses_finite_l1` and the two-edge core are receipt-covered. The uniformity axiom itself is not derived in Lean, consistent with the prose. |
| Counterexamples 1-4 | [PROVEN BY COUNTEREXAMPLE, PROSE] | **[MECHANIZED-PARTIAL]** — exact arithmetic helpers are receipt-covered. CE1 uses a natural-number quadratic rather than the real Euclidean norm; CE3 uses a coupled polynomial rather than the real cancellation seminorm. These helpers do not check every retained prose hypothesis. |
| Counterexample 5 | **[OPEN / NOT_VERIFIED]** | `ce5_lp_not_homogeneous` is a narrower arithmetic witness and does not promote the full prose claim. |
| Final consolidated theorem | [PROVEN, CONDITIONAL] | Pending |
| Weighted discrete coarea and undirected cut specialization | [STANDARD + finite prose derivation] | No new Lean claim; §3.1 includes the edgewise proof and orientation convention |
| Max-flow/min-cut statement | [STANDARD + citation] | N/A |
| Remark 3.2 for $k>1$ | [PROVEN, CONDITIONAL] | Pending |
| Defect-space identification | [PROVEN, CONDITIONAL] | Pending |
| Kakutani analogy | [INTERPRETIVE / STANDARD] | N/A |
| Conditional characterization §3.4 | [INTERPRETIVE / PROVEN, CONDITIONAL] | N/A |
| LGGR reading (§3.5) | **[OPEN / NOT_VERIFIED]** | Finite `Nat`-valued quotient helpers are receipt-covered over `OmegaCore.PrimitiveDifference` [9], but they are not the real-cochain manuscript claim. |
| EPK observer audit (§3.6) | [INTERPRETIVE] | **[MECHANIZED-PARTIAL]** for the finite `Nat`-model kernel-refinement artifacts only; the §3.6 principle itself is interpretive and is not mechanized. |
| $SO(k)\Rightarrow\ell^2$ route (§3.6) | **[OPEN / IMPORTED]** | N/A — not proved here; requires an unearned inner-product import. CE1 gives only the negative half ($\ell^2$ excluded by H3). |

## Support Ledger

* **S1 — Finite coordinate decomposition lemma (easy).** For $x\in\mathbb R^k$, the coordinate vectors $x_i e_i$ have pairwise disjoint supports and sum to $x$. If $\nu_e$ is additive over disjoint coordinate supports, then $\nu_e(x)=\sum_i\nu_e(x_i e_i)$.
* **S2 — Coordinate symmetry weight-equality lemma (easy).** If $\nu_e$ is invariant under coordinate permutations, then $\nu_e(e_i)=\nu_e(e_j)$ for all $i,j$.
* **S3 — Edge-orbit weight lemma (easy).** If graph-isomorphism invariance sends edge $e$ to edge $e'$, then the edge weights obtained from Theorem 1 satisfy $w_e=w_{e'}$.
* **S4 — Edge-uniformity collapse lemma (easy).** If all edge orbits share the same weight $\alpha$, either by edge-transitivity or explicit uniformity, then the orbit-weighted diagnostic collapses to $\nu_G(\delta)=\alpha\sum_{e\in E}\|\delta_e\|_1$. The PL-004-2 formal bridge for the declared finite orbit-action formulation is discharged by `PaperGS003.orbit_uniform_l1_collapse` and `PaperGS003.edge_uniform_l1_collapse`; the edge-uniformity hypothesis remains load-bearing.
* **S5 — Counterexample independence ledger (easy/moderate).** CE1–CE4 verify the scoped failures for disjoint-coordinate additivity, coordinate symmetry, edge locality, and edge-uniformity. The corresponding full homogeneity-independence construction is CE5 and remains `OPEN / NOT_VERIFIED`.
* **S6 — Finite $L^1$ identification lemma (easy).** Under uniform edge weights and coordinatewise $\ell^1$, the diagnostic norm on $C^1(G,\mathbb R^k)$ is isometric to the finite $L^1$ norm on the finite measure space $E\times\{1,\dots,k\}$ with counting measure, up to scalar $\alpha$.
* **S7 — Scalar coarea import boundary (easy).** For scalar graph total variation, the discrete coarea formula and min-cut relation are imported standard results and are not required to prove Theorems 1–3.
* **S8 — Functional-equation summary lemma (moderate).** If a scalar function $\psi:\mathbb R\to\mathbb R_{\ge0}$ is absolutely homogeneous and used in a coordinate-separable disjoint-additive diagnostic, then $\psi(t)=C|t|$. If instead one wants a Cauchy-equation proof from additivity and regularity, the exact regularity assumption must be stated.
* **S9 — Dependency-name consistency lemma (easy).** Cross-paper references should use current paper titles or current logical roles rather than stale internal sequence numbering when numbering has changed across the corpus.
* **S10 — Quotient relation audit (elementary).** A fixed-profile weighted total descends through per-edge diagnostic equality. Non-descent occurs in the examples only after coarsening to unweighted-total equality or enlarging the carrier to records whose weights vary (§3.5). The broader LGGR interpretation remains open.
* **S11 — EPK observer audit (interpretive).** Kernel data alone do not determine norm geometry. The finite classification uses the full declared observer bundle; alternative symmetry classes require separate hypotheses and classification proofs (§3.6).

---

## GTOC / GTLA Compliance Note

*Added by the GTOC/GTLA compliance pass of 2026-07-17. No version bump, no status upgrade, and no theorem statement or proof was widened by that pass.*

**Role:** finite combinatorial base case for the gauge-classification program. Classifies edge-local seminorms on declared finite graph cochains under a declared coordinate-separable observer class. Diagnostic only.

**Degree:** the edge-cochain degree $C^1(G,\mathbb R^k)=\bigoplus_{e\in E}\mathbb R^k$, over the declared scalar specialization $\mathbb R$ and declared finite index sets $E$ and $\{1,\dots,k\}$.

**Consumes:** the declared observer bundle H1–H5 (§2.1); declared finite index data $G=(V,E)$, $k$; the declared scalar specialization $\mathbb R$.

**Produces:** (i) Theorem 1 — edgewise $\nu_e=w_e\lVert\cdot\rVert_1$, $w_e\ge0$, with $w_e>0$ under normhood; (ii) Theorem 2 — orbit-weighted aggregation; (iii) Theorem 3 — unweighted global $\ell^1$ **only** under edge-transitivity or an explicit uniformity axiom; (iv) CE1–CE4 — verified independence witnesses; (v) CE5 and the §3.5 LGGR reading — `OPEN / NOT_VERIFIED` candidates with narrower executable helpers.

**Does not produce:** authority of any kind; finite-structural or observer-independent $\ell^1$; $\ell^2$ or any inner-product geometry; probability, proportion, or measure semantics; physical norm selection; Banach-presheaf rigidity; dynamical or projection-obstruction results; unweighted global $\ell^1$ absent edge-transitivity or explicit uniformity; any claim about non-coordinate-separable observers or infinite-dimensional carriers.

**Authority status:** **none.** See the front-matter firewall. Nothing here is a descent packet; nothing here terminalizes; no `IsAuth` guard is discharged. The classification is regime-relative to H1–H5 and diagnoses only inside that declared regime.

**GTOC regime declaration.**

| Slot | This paper |
|---|---|
| `ObstructionRegime(k)` | Declared: edge-cochain degree $C^1(G,\mathbb R^k)$. |
| `C^k, C^{k+1}, C^{k+2}` | **Not declared.** This paper classifies a seminorm *on* $C^1$; it does not route a cochain complex. |
| `d_k, d_{k+1}` | **Not used.** $d_0$ appears once (§3.6) as a hypothetical coordinate-compatible boundary; no result depends on it. |
| `d_{k+1}\circ d_k=0` | **Not used and not asserted.** No exactness claim is made or needed. |
| `ZeroRel` / local sameness | Declared at §3.5: $\delta\sim\delta'$ iff $\nu_e(\delta_e)=\nu_e(\delta'_e)$ for every edge $e$. |
| Observer / gauge / norm | H1–H5 — a **declared-comparison scope** (charter K6), carrying no privilege and no standpoint outside the compared differences. |
| Lift policy | No general lift is claimed. Fixed-profile aggregation descends through the per-edge relation; the separate coarser-total and varying-profile examples lose data (§3.5). |
| Terminal policy | **Refused.** No terminalization is attempted or available at this degree. |

**GTOC classification boundary.** No fixed-profile closure failure is established by nonuniform weights: the weighted aggregate is already determined by per-edge diagnostics. Loss of descent in §3.5 belongs to its separately declared coarser relation or varying-profile carrier. A shared uniform scalar repairs the total-only example; declaring the profile repairs the varying-profile example. Any broader GTOC classification remains interpretive until its exact carrier and relation are supplied.

**GTLA boundary.** GTOC routes and diagnoses; it mints no authority. Authority type, `IsAuth`, and descent-packet data are owned by CODA-FDA; terminalization discipline and non-promotion rules are owned by GTLA. This paper touches none of them. A diagnostic that classifies cleanly, replays finitely, and mechanizes in Lean is still not authority-bearing.

**Import / Oracle boundary.** Any use of Hilbert space, Born uniqueness, phase, continuum, probability semantics, dynamics, physical interpretation, tensor composition, or empirical realization is an imported representation structure unless explicitly constructed at this paper's declared degree. Imported structures are not DDA operations and do not produce authority. This paper's registered imports:

| Import | Where | Status |
|---|---|---|
| $\mathbb R$ as scalar carrier; absolute homogeneity over $\mathbb R$ | §2.1 (H5), throughout | **Declared scalar specialization.** Admitted, not derived. The classification is stated for this specialization only. |
| Continuum coarea integral $\int_{-\infty}^{\infty}\lvert\partial V_t\rvert\,dt$ | Fact 3.1, §3.1 | **IMPORTED (continuum).** Standard, cited [2,3]. Integral notation is imported; the finite edgewise identity is shown in §3.1 and is **not used to prove Theorems 1–3** (see S7). The paper's "purely combinatorial / entirely finite" self-description refers to Theorems 1–3 and the counterexamples; it does not extend to this imported fact. |
| Max-flow / min-cut | §3.1 | **IMPORTED.** Standard, cited [5]. Background only. |
| Counting measure; finite $L^1$ space on $E\times\{1,\dots,k\}$ | §3.2, S6 | **IMPORTED (measure-theoretic).** Used for identification only. |
| Kakutani (1941): abstract $L$-spaces, mean ergodic theorem | §3.2, §3.6, ref [1] | **IMPORTED / INTERPRETIVE.** Cited as a finite analogue. The ergodic content is **not** invoked; no source model, no ergodicity, no stochastic reading is imported with it. |
| Inner product / $SO(k)$-invariance route to $\ell^2$ | §3.6 | **OracleNeeded / Q-gated.** Not earned here. See the §3.6 `[OPEN / IMPORTED]` block. |
| Infinite-dimensional carrier | §3.6 | **OracleNeeded.** Requires functional-analytic hypotheses; correctly priced in-place. |
| Dynamics, linear evolution, projection onto a manifold | §1, ref [6] | **IMPORTED.** Belongs to [6] under [6]'s hypotheses; nothing here derives it. |
| Banach-presheaf functoriality | §1, §3.3, ref [7] | **IMPORTED.** Belongs to [7]. |

**Probability: not imported, and not available.** This paper contains no probability semantics, and none is smuggled: it performs no normalization to unit sum, constructs no weight profile summing to one, and never reads a weight as a proportion, frequency, chance, or measure of belief. The words "normalization" (§2.4, §3.3) refer **only** to the scaling constant $\alpha$, not to a unit-sum condition. The weights $w_e,w_{\mathcal O},\alpha$ are **finite non-negative scalars** attached to declared edges — nothing more. The finite-$L^1$/counting-measure identification of §3.2 is a measure-theoretic *identification*, not a probability structure: no normalized measure is constructed. Should a later adapter wish to read a normalized weight profile as a probability distribution, it must first supply the normalization **and** the adapter; **this paper supplies neither, and no result here depends on or licenses that reading.** Weight, proportion, and normalization at the $\delta_2$ degree are the subject of the separate series paper on weight and proportion, not of this one.

**Formalization-status firewall.** Any Lean, Rust, or replay artifact cited here supports only the exact finite statement it mechanizes. It does not automatically discharge PL-GTOC, Q, continuum, physical-realization, or GTLA authority obligations. A status upgrade requires an explicit theorem-ledger mapping, hypotheses check, build receipt, axiom/sorry audit, and adversary acceptance. Concretely, for this paper: the Lean mechanizes Theorem 1's real finite-coordinate core **genuinely** ($\nu$ is an opaque field, not assumed to be $w\lVert x\rVert_1$), but the Theorem 2 and Theorem 3 artifacts **assume** their load-bearing steps — the fiber isometry, the weight factorization `hfactor`, and uniformity `huniform` — rather than deriving them; H2 is never modelled as a permutation action; and no graph, automorphism group, or derived orbit appears anywhere in the Lean, where `orbit : E → O` is an arbitrary declared classifier. "PL-004-2 discharged **for the declared finite orbit-action formulation**" means exactly that and nothing broader. See the Claim-Type Ledger for the per-theorem scope.

**Detector adequacy warning.** A replayable detector/profile is not automatically adequate for a claim. A collapsing detector can make every profile exact. This paper contains a live instance: $\nu_G$ is a **seminorm**, so $w_e\ge0$ admits $w_e\equiv0$ — under which $\nu_G\equiv0$ satisfies H1–H5 and reads **every** cochain as exact. The paper notes the vanishing case (§2.3) and blocks it where it matters by requiring faithfulness/normhood for $w_e>0$ (Theorem 1) and $\alpha>0$ (§3.2). Any authority-bearing use would require a separate `DetectorAdequacy` certificate naming the protected distinctions, adversarial cases, and blind spots — none is supplied here, and none is needed, because this paper mints no authority.

**Remaining open obligations.**

1. **PL-004-1 status divergence** — global ledger records DISCHARGED 2026-06-20 (ENC-0526); §3.4 retains `[INTERPRETIVE]`. Not reconciled here; a hygiene pass does not promote.
2. **CE5 and LGGR scope** — match CE5 to the weakened gauge premise and $0<p<1$ range; match any LGGR interpretation to an explicit real record carrier or coarser relation. Keep the broader formalization obligations open; finite probes and the $p=2$ helper do not close them.
3. **Lean H2** — model coordinate permutation symmetry as an actual permutation action and derive `basis_equal`, rather than assuming it.
4. **Lean Theorem 2** — model the graph, an automorphism group, and genuine orbits; derive the weight factorization instead of assuming `hfactor`.
5. **Lean composition** — compose Theorem 1's $\exists w$ witness into the edge-total definitions, so that the ℓ¹ form is derived rather than baked into `edgeWeightedL1Total`.
6. **§3.6 $\ell^2$ route** — either price the inner-product import explicitly or leave it `[OPEN / IMPORTED]`.

---

## Acknowledgments

No external funding. No conflicts of interest.

---

## References

1. Kakutani, S. (1941). *Concrete representation of abstract $(L)$-spaces and the mean ergodic theorem*. Annals of Mathematics, 42(2), 523-537.
2. Fleming, W. H., & Rishel, R. (1960). *An integral formula for total gradient variation*. Archiv der Mathematik, 11(1), 218-222.
3. Chambolle, A., Caselles, V., Novaga, M., Cremers, D., & Pock, T. (2010). *An introduction to total variation for image analysis.* In: Theoretical Foundations and Numerical Methods for Sparse Recovery. De Gruyter. Author manuscript: <https://cvai.cit.tum.de/_media/spezial/bib/chambolle_et_al_10.pdf>.
4. Rockafellar, R. T. (1970). *Convex Analysis.* Princeton University Press.
5. Ford, L. R., & Fulkerson, D. R. (1956). *Maximal flow through a network.* Canadian Journal of Mathematics, 8, 399-404.
6. Carroll, J. H. (2026). *Projection Obstruction for Factorized States: Nonlinear Dynamics, Conditional ℓ1 Diagnostics, and Finite-Time Defect Bounds* Zenodo. <https://zenodo.org/records/20650922>
7. Carroll, J. H. (2026). *M-Compatible Gauge Classification for Banach Presheaf Coboundaries: The ℓ¹ Maximal-Symmetry Endpoint* Zenodo. <https://zenodo.org/records/20564214>
8. Carroll, J. H. (2026). *Primitive Axiomatics of Finite Obstruction Calculus* Zenodo. <https://zenodo.org/records/20651224>
9. Carroll, J. H. (2026). *Representation Abundance Is Not Physical Authority*. Programme reference; no verified record identifier is supplied here. The exact imported finite quotient code is packaged as [`lean4/primitive_difference.lean`](lean4/primitive_difference.lean), with provenance in [`lean4/PROVENANCE.md`](lean4/PROVENANCE.md).
10. van Gennip, Y., Guillen, N., Osting, B., & Bertozzi, A. L. (2013). *Mean curvature, threshold dynamics, and phase field theory on finite graphs*. Author manuscript, Appendix B. <https://www.math.ucla.edu/~bertozzi/papers/graph_curve.pdf>.

---

## Appendix: Zenodo Description

This preprint shows in this model a finite combinatorial classification theorem for coordinate-valued graph cochain diagnostics. Under edge locality, coordinate permutation symmetry, disjoint-coordinate additivity, and seminorm homogeneity, each edge-local seminorm is a nonnegative scalar multiple of coordinatewise $\ell^1$. Graph isomorphism invariance gives orbit-weighted $\ell^1$; a single unweighted global $\ell^1$ diagnostic requires edge-transitivity or explicit edge-uniformity. The result is conditional on a coordinate-separable observer class and does not claim finite-structural $\ell^1$ geometry.

This paper supplies the finite combinatorial base case for later obstruction-calculus papers on Banach presheaf coboundaries, M-compatible gauge classification, and projection-induced defects in factorized-state dynamics.

**Keywords:** coordinate-wise additivity; seminorm classification; finite graph cochains; $\ell^1$ norm; weighted $\ell^1$; disjoint supports; permutation symmetry; edge locality; edge orbits; edge transitivity; graph total variation; formal verification.
