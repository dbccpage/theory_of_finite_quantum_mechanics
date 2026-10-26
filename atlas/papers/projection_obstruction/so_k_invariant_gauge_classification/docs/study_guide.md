# Study guide: SO(k)-invariant gauge rigidity (GS-002)

Companion to the v2.0.0 candidate; reviewed 2026-10-02. Read the paper's
§§3–6 before attempting the [Landau quiz](landau_quiz.md). The
[solutions](landau_quiz_solutions.md) give derivations and grading criteria.

Prerequisites are finite graph incidence, linear algebra, norms, adjoints,
and elementary convex duality. The graph is finite; the real scalar field,
Euclidean inner product, and continuous rotation group are declared inputs.

## 1. Keep four objects distinct

| Object | Definition | What it measures |
|---|---|---|
| Local gauge $j_e$ | $j_e(x)=c_e\|x\|_2$ after local rigidity | One vector defect on one edge |
| Representative cost $J$ | $J(\eta)=\sum_e c_e\|\eta_e\|_2$ | A chosen cochain before optimizing repairs |
| Quotient norm $\Phi$ | $\inf_\alpha J(\omega-d_0\alpha)$ | The best cost in a repair class |
| Closure diagnostic $\Gamma$ | $\|d_1\omega\|_{1,2,u}$, with $d_1d_0=0$ | The class's face defect |

A large $J(\omega)$ need not imply a large $\Phi([\omega])$. A tree can
have nonzero edge data and $\Phi=0$, since every edge cochain is repairable.
The ratio $\Gamma/\Phi$ is used only when $\Phi>0$. The quotient is
$C^1/\operatorname{im}d_0$, which also contains nonclosed cochains. With
faces present it differs from $H^1=\ker d_1/\operatorname{im}d_0$; the
filled triangle can have zero cohomology and still have a nonzero closure
defect and a nonzero quotient cost for nonclosed input.

## 2. Read the argument in three passes

**Local rigidity (§3.2).** Rotations move any Euclidean unit vector to any
other for $k\ge2$. Invariance makes $j$ constant on that sphere. Positive
homogeneity extends that constant radially: $j(x)=c\|x\|_2$. Faithfulness
makes $c>0$. Convexity is not used in this radial step, but norm properties
are used later. The result is relative to the declared Euclidean structure.

**Outer aggregation (§3.3).** The sum across edges is a separate strong
declaration. For two unit edge vectors, the sum is $2$, while
$\sqrt{\sum_e\|\omega_e\|_2^2}=\sqrt2$. Both respect independent edge
rotations. Exact additivity over disjoint supports excludes the latter.
Exchange symmetry equalizes weights on orbits; it does not make the common
weight one. Unit singleton normalization supplies that scale.

**Repair, duality, and closure (§§4–6).** For identity transports,
$(d_0\alpha)_{u\to v}=\alpha(v)-\alpha(u)$. A witness satisfying
$d_0^*z=0$ is unchanged by repairs, and $\|z_e\|_2\le c_e$ bounds its
pairing by every representative's cost. Standard finite-dimensional convex
duality upgrades this lower bound to equality and attainment. Closure uses
a different fact: $d_1d_0=0$ makes $d_1\omega$ invariant under repairs.

For a transport from the source stalk to the target stalk, use
$(d_{0,r}\alpha)_e=\alpha(v)-r_{v,u}\alpha(u)$. Its adjoint, rather than
ordinary divergence, governs dual witnesses. The executable engine and
the untransported cycle formula use identity transports.

## 3. Work the triangle by hand

Take edges $0\to1$, $1\to2$, $2\to0$ and
$\omega=((1,0),(0,1),(0,0))$. The circulation is $S=(1,1)$.

With unit weights, $\Phi_{1,1}=\|S\|_1=2$ and
$\Phi_{2,1}=\|S\|_2=\sqrt2$. These are optimized class costs; the
displayed representative itself has mixed cost $J(\omega)=2$.

Now give both observers edge weights $(3,1,2)$. Put all circulation on the
cheapest edge: $\eta=(0,(1,1),0)$. The repair
$\alpha=((0,0),(1,0),(0,0))$ gives $\omega-d_0\alpha=\eta$.
Its mixed cost is $\sqrt2$. The constant dual witness
$z_e=(1,1)/\sqrt2$ has zero divergence and fits all three balls. Its
pairing with $\omega$ is also $\sqrt2$, certifying the mathematical value.
The coordinate gauge gives $2$ under the same weights.

The general lower bound is
$$
\sum_e c_e j(\eta_e)\ge c_{\min}\sum_e j(\eta_e)
\ge c_{\min}j\left(\sum_e\eta_e\right).
$$
Concentration on a cheapest edge attains it. Equal circulation is equivalent
to an exact repair: partial sums along a spanning path give the vertex
potential, and the closing equation follows from the zero circulation sum.

For reversed stored directions, insert traversal signs $\varepsilon_e$ in
$S=\sum_e\varepsilon_e\omega_e$. A face's signed boundary need not be
the graph's traversal: repeated terms can cancel. The cycle solver derives
its traversal from the graph.

## 4. Leave the single-cycle setting carefully

On the theta graph, three indexed parallel edges join vertices $0$ and $1$.
A repair subtracts the same vector from every edge. Two independent
invariants are $\omega_0-\omega_1$ and $\omega_1-\omega_2$; the raw sum
of all edge data is not repair-invariant. The one-cycle bottleneck formula
does not apply. The mixed primal is a weighted geometric-median problem in
the common repair difference, and the dual requires $z_0+z_1+z_2=0$.

For face rows $(1,-1,0)$ and $(0,1,-1)$, edge weights $(2,3,5)$, and face
weights $(1,4)$, the scalar-incidence operator norm is
$$
\max\left\{\frac12,\frac53,\frac45\right\}=\frac53.
$$
A unit vector on the middle edge has $J=3$ and $\Gamma=5$ and attains
the operator ratio. The abstract closure theorem allows more general face
dimensions; this explicit column formula uses equal-dimensional stalks and
scalar signed incidence.

## 5. Read the evidence with its scope

| Evidence | What it establishes | Remaining boundary |
|---|---|---|
| Prose radial proof | Local rigidity under the stated hypotheses | Euclidean structure and general sphere transitivity are declared |
| Lean planar rotation construction | Algebraic unit-circle transitivity | Not a full general-$k$ rotation formalization |
| Lean radial kernel | Collapse for a native norm with sphere constancy | The Euclidean group-to-norm bridge remains explicit |
| Lean cycle kernel | Anchored zero-sum repair algebra and norm cost bounds | Ordinary graph incidence is identified in prose |
| Lean dual kernel | Repair-invariant weak-duality lower bound | Strong-duality equality/attainment is imported convex analysis |
| Floating-point solver | Reported feasibility and gap pass a finite tolerance | No exact or interval-arithmetic proof |
| Random invariance audit | Tested samples pass or provide a counterexample | A pass is not unbounded invariance |
| Manifest/archive checks | Exact file custody and deterministic packaging | No mathematical truth or publication approval |

A tiny coordinate residual is not necessarily a tiny weighted cost. On a
triangle with circulation $10^{-9}$ and weights $10^{12}$, the quotient is
$10^3$. A zero dual witness leaves that full gap. Similarly, a NaN-valued
function is not a gauge and must never pass an audit through comparisons
with NaN. The regression suite checks these failures explicitly.

`is_optimal`, `is_zero_gap`, and `certified_quotient_value` are numerical
terms qualified by tolerance. `is_exact_repair` reports a computed zero
residual cost; it does not prove exact membership in the repair image.
Notebook execution counts and retained Lean receipts are historical evidence
unless a fresh replay/build binds them to the current sources. See
[publication_review.md](publication_review.md) for this review's results.

## 6. Finish with derivations

Attempt the quiz without code. State each hypothesis before using it,
construct the repair and witness, and distinguish a theorem from a sampled
check. Then rerun the examples and compare the signed gap, divergence, and
edge-ball violations with the declared tolerance. A failed numerical
certificate can indicate a solver limitation without refuting the theorem.
