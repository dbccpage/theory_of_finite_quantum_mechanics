# Conditional Hilbert Lifts of ℓ¹ Sector Weights and Born Normalization Redundancy

## GTOC Foundations — Quantum Contact Series (qm_020_born_normalization_and_conditional_hilbert_lift)

**Date:** 2026-07-29 · **Version:** v1.0  
**License:** Creative Commons Attribution 4.0 International (CC-BY-4.0)  
**Status:** RELEASED  
**Authority:** `AuthorityEffect::None`  

## Mechanism inventory

| Slot | Value / Description |
| --- | --- |
| **Primitive Differences** | $\delta c = \text{{defect mass}}$ |
| **Carriers / Structure** | Finite Graph 0-Cochain / Hilbert Space |
| **Cochain complex** | $C^0 \to C^1 \to C^2$ |
| **Coboundary maps** | $\delta^0, \delta^1$ |
| **ZeroRel** | Preserved under $L_1$ quotient |
| **Licensed repairs** | None |
| **Quotient / Q1** | Banach Quotient |
| **Residuals** | $\delta c \neq 0$ boundary defect |
| **Witnesses** | Replayable Python / Rust Certifiers |
| **Observers / profiles** | Operational Observer |
| **Anomalons** | None |
| **CompletionLaw** | Finite Cochain Completion |
| **Terminal / route** | Route to 003 Quantum Foundations |
| **AuthorityEffect** | None |

**Version:** v3.0.2 Pre-Print

> **Status / demotion (per corpus audit):** Born normalization and the Hilbert
> lift in this paper are **not** derivations of quantum mechanics.
>
> - **✅ Core (narrow algebra):** Theorems 1 and 4 establish only a normalization
>   *redundancy* — given nonnegative additive sector weights, the optional Hilbert
>   lift reproduces the same finite normalized weight law. These narrow algebraic lemmas stand.
> - **⚠️ Conjecture (self-quarantined):** the Born-rule/ontology claim. Born
>   *uniqueness* and the Hilbert lift are conditional on imported representation
>   assumptions (Theorem 6) and are otherwise UNPROVEN as ontology.
>   Branch-localization / many-worlds remarks are quarantined conjectures.
>   Downstream citations must not present Born normalization or the Hilbert lift
>   as established physical results or as core results.

```{=latex}
\begin{nonclaim}
This paper does not derive quantum mechanics from ℓ¹ structure, does not claim the Born rule as ontology, and does not claim Born uniqueness from additive sector weights alone — Born uniqueness is conditional on imported Hilbert, projection, and Gleason-type assumptions (Theorem 6). Branch-localization and many-worlds remarks are quarantined conjectures, not theorems.
\end{nonclaim}
```

> **Role in the program (significance, not a claim upgrade — 2026-07-15).** The
> demotion box above is exact and stands: this paper derives no quantum
> mechanics. Its *significance*, however, is **architectural, not proof-deep**,
> and should not be read off the modesty of its one-line proofs. Within the
> corpus this redundancy result is **rung 1 of the QM reconstruction ladder**
> (QM_121): it is the finite statement that the *finite ℓ¹ proportion* half of the
> quantum picture — the first summand of the
> $L^1(E)\oplus\mathrm{Fiber}_{L^2}(E)$ decomposition — is a **free re-encoding**
> of already-given $\ell^1$ sector weights (Theorems 1, 4), while everything
> phase/interference/dynamics-valued is the *priced* second summand. The probability reading belongs to a later adapter. Theorem 6
> is the canonical home of the program's **Born-uniqueness $=$ `OracleNeeded`
> firewall** (GTOC-spine obligation GTOC-8): Born-quadratic uniqueness is one of
> the whole stack's small set of irreducible imports, and this is where that
> import is *named and fenced*, not smuggled. The GTOC $\delta 2$ probability
> paper defers to Theorems 1/4 for its entire Born treatment
> (`002_probability` §7.1) and to Theorem 2 for its
> $\ell^1$-vs-$\ell^p$ aggregation exclusion (§6.3). **The value of this paper is
> the line it draws** — free normalization on one side, imported uniqueness on
> the other — not the difficulty of the algebra; a one-line identity can be a
> keystone. This note adds no authority and upgrades no theorem (Authority
> Firewall: representation $\ne$ ontology; coherence organizes, descent
> authorizes).


**Abstract:**

**Main result (informal).** Given nonnegative additive sector weights $w_\gamma$, the finite normalized weight law $P(\gamma)=w_\gamma/\sum_\eta w_\eta$ is already fixed; the optional Hilbert lift $c_\gamma=\sqrt{w_\gamma}\,e^{i\theta_\gamma}$ reproduces *the same* law through the Born formula. Born normalization is therefore a redundant encoding, while Born *uniqueness* (the quadratic form) requires separately imported Hilbert/projection assumptions and is not forced by $\ell^1$ additivity.

This paper studies the relationship between nonnegative $\ell^1$ sector weights and Born-style probability normalization. It does not derive quantum mechanics from $\ell^1$ structure. Instead, it proves a narrow redundancy result: once gauge-reduced, additive, nonnegative sector weights are already supplied, direct normalization gives a unit-sum weight profile, and an optional Hilbert lift $c_\gamma=\sqrt{w_\gamma}e^{i\theta_\gamma}$ reproduces the same law through the Born formula. The paper separates this Layer A normalization result from conditional representation assumptions involving Hilbert space, unitary dynamics, phase averaging, and measurement descent. Speculative claims about branch localization and many-worlds interpretations are quarantined as graph-support conjectures, not theorems about quantum ontology.

**Why a researcher should care.** It is tempting to read "the Born rule drops out of $\ell^1$ weights" as a derivation of quantum probability. This paper draws the line precisely: the *normalization* is redundant (a one-line algebra identity), but *uniqueness* of the quadratic form is not forced by additive weights — it needs a complex Hilbert representation, orthogonal-sector additivity, and Gleason-type structure. Separating the cheap identity from the expensive uniqueness claim is what keeps an $\ell^1$ obstruction framework from silently overclaiming a foundations-of-quantum-mechanics result.

In Local-Green/Global-Red terms: the local algebraic normalization checks are green, but the global Born-rule/ontology conclusion stays red unless the imported Hilbert, projection, and frame-function assumptions are explicitly supplied.

```text
GTOC role:

  * finite normalized weight law from declared ℓ¹ sector weights
  * ℓ¹ additivity boundary
  * phase-blind descent / LGGR witness
  * Born uniqueness = OracleNeeded

GTLA role:

  * no authority minted
  * no physical Born ontology terminal
  * any use of Hilbert/Born uniqueness requires a declared import/oracle packet
```


1. The Redundancy and Conditional Lift Proofs


### 1.1 Setup

Let $\Gamma$ be a finite set of residual sectors.

Let each sector carry a nonnegative weight:

$$
w_\gamma\ge0, \qquad \gamma\in\Gamma.
$$

Assume not all weights vanish:

$$
W:=\sum_{\eta\in\Gamma}w_\eta>0.
$$

These weights are already supplied by the declared $\ell^1$, disjoint-additive observer structure. The question is not how to derive quantum mechanics. The question is:

> **Given additive nonnegative sector weights, what finite normalized weight law and optional Hilbert encoding follow?**

### 1.2 Theorem 1 — Direct Normalization **[PROVEN]**

**Statement:**

Let $\Gamma$ be finite and let $w_\gamma\ge0$, not all zero. Define:

$$
P_{\ell^1}(\gamma) = \frac{w_\gamma}{\sum_{\eta\in\Gamma}w_\eta}.
$$

Then $P_{\ell^1}$ is a unit-sum weight profile on $\Gamma$. A later probabilistic adapter may read this unit-sum profile as a probability distribution; this paper does not supply that adapter.

**Proof:**

Since each $w_\gamma\ge0$, and $W=\sum_\eta w_\eta>0$,

$$
P_{\ell^1}(\gamma)=\frac{w_\gamma}{W}\ge0.
$$

Also,

$$
\sum_{\gamma\in\Gamma}P_{\ell^1}(\gamma) = \sum_{\gamma\in\Gamma}\frac{w_\gamma}{W} = \frac{1}{W}\sum_{\gamma\in\Gamma}w_\gamma = \frac{W}{W} = 1.
$$

Thus $P_{\ell^1}$ is a normalized finite weight law.

> **No Hilbert space is needed for this normalization.**

The Lean hardening also records the finite rational scale-invariance of this
normalization: for any nonzero $a\in\mathbb Q$,

$$
\frac{a w_\gamma}{\sum_\eta a w_\eta}
=
\frac{w_\gamma}{\sum_\eta w_\eta}.
$$

Thus direct normalization depends only on the nonzero ray of weights. This is a
bookkeeping invariance, not a Born-rule uniqueness principle.

**Primitive-Difference registry.** This paper uses two distinct quotient
relations and does not identify them. The scalar-ray relation belongs only to
normalization. The phase-blind relation
$\delta_{\mathrm{phase}}(c,c')_i=c_i^2-(c_i')^2$ belongs to squared-coordinate
descent and is the `ZeroRel` used by the mixing obstruction. The
$\ell^1$ additivity defect is a third diagnostic, not either equivalence
relation. Any downstream adapter must name which relation it consumes.

Lean also packages this as a `PrimitiveDifference` quotient statement:
finite rational direct normalization factors through the scalar-ray quotient
that identifies weight vectors differing by a nonzero global scalar. In other
words, normalization is a well-defined observable on ray classes of finite
weights.

Conversely, on the nonzero-total locus, Lean proves that the fibers of direct
normalization are exactly those scalar-ray classes: two finite rational weight
vectors have the same normalized distribution iff one is a nonzero scalar
multiple of the other. This is an exact quotient classifier for normalization
bookkeeping, not a uniqueness theorem for physical probability.

The same finite algebra preserves support when $W\ne0$:

$$
P_{\ell^1}(\gamma)=0 \quad\Longleftrightarrow\quad w_\gamma=0.
$$

For the nonnegative case of the theorem, where $W>0$, Lean also proves the
positive-support form:

$$
P_{\ell^1}(\gamma)>0 \quad\Longleftrightarrow\quad w_\gamma>0.
$$

Finally, under the same nonnegative positive-total hypotheses, Lean proves the
unit-interval bound:

$$
0\le P_{\ell^1}(\gamma)\le1.
$$

It also proves the finite rational order law: for any two sectors $\gamma,\eta$,
positive-total normalization preserves weak order, strict order, and ties:

$$
P_{\ell^1}(\gamma)\le P_{\ell^1}(\eta)\Longleftrightarrow w_\gamma\le w_\eta,
$$

$$
P_{\ell^1}(\gamma)< P_{\ell^1}(\eta)\Longleftrightarrow w_\gamma<w_\eta,
\qquad
P_{\ell^1}(\gamma)=P_{\ell^1}(\eta)\Longleftrightarrow w_\gamma=w_\eta.
$$

Lean also proves idempotence:

$$
P_{\ell^1}(P_{\ell^1}(w))_\gamma=P_{\ell^1}(w)_\gamma.
$$

After a nonzero finite weight vector has been normalized, applying the same
normalization again changes nothing. Normalization is therefore a projection
onto the sum-one slice of the finite rational weight space.

Normalization changes scale, not which sectors are present or active.

$\square$

### 1.3 Theorem 2 — Nonlinear Aggregation for $p>1$

**Theorem 2a — finite rational ℓ¹ additivity defect kernel [MECHANIZED / finite]**
**Theorem 2b — real ℓᵖ strict subadditivity for p>1 [STANDARD / imported real-analysis fact]**

**Statement:**

For disjoint positive sectors, the $\ell^1$ norm is exactly additive:

$$
\|x\oplus y\|_1=\|x\|_1+\|y\|_1.
$$

For $p>1$, if $x,y\neq0$ have disjoint support, then:

> **$\|x\oplus y\|_p<\|x\|_p+\|y\|_p.$**

Thus $\ell^p$ with $p>1$ introduces nonlinear aggregation over disjoint sectors.

**Proof:**

Let $x,y$ have disjoint support.

For $p=1$,

$$
\|x\oplus y\|_1 = \sum_i|x_i|+\sum_j|y_j| = \|x\|_1+\|y\|_1.
$$

The Lean hardening mechanizes this finite additivity kernel over rational-valued functions: if $x$ and $y$ have disjoint support, then

$$
\sum_i |x_i+y_i|=\sum_i |x_i|+\sum_i |y_i|.
$$

It also proves the finite rational $\ell^1$ ambient norm laws used around this
equality: $\sum_i |x_i|\ge0$ and
$\sum_i |x_i+y_i|\le\sum_i |x_i|+\sum_i |y_i|$, together with the zero-norm
criterion $\sum_i |x_i|=0$ iff every coordinate of $x$ is zero. Thus
the positive-norm form also follows: $\sum_i |x_i|>0$ iff some coordinate of
$x$ is nonzero. Disjoint-support additivity is therefore recorded as the
exact-equality case of the finite $\ell^1$ triangle inequality, not as an
isolated arithmetic coincidence.

Lean also packages the triangle slack as a finite obstruction:

$$
D_1(x,y)=\|x\|_1+\|y\|_1-\|x+y\|_1.
$$

It proves $D_1(x,y)\ge0$, proves $D_1(x,y)=0$ exactly when the $\ell^1$
triangle inequality is sharp, and proves that disjoint support forces
$D_1(x,y)=0$. This is the Theorem 2 Local-Green certificate: disjoint-sector
gluing is green precisely because the $\ell^1$ additivity defect vanishes.

Lean further decomposes this obstruction into coordinatewise local defects:

$$
D_{1,i}(x,y)=|x_i|+|y_i|-|x_i+y_i|.
$$

It proves each $D_{1,i}(x,y)\ge0$ and

$$
D_1(x,y)=\sum_i D_{1,i}(x,y).
$$

Therefore the global $\ell^1$ additivity defect vanishes iff every local
coordinate defect vanishes. This is the finite sheaf-style reading: local
coordinate gluing certificates assemble exactly into the global additivity
certificate.

Lean also identifies the local certificate explicitly over rational
coordinates:

$$
D_{1,i}(x,y)=0 \quad\Longleftrightarrow\quad x_i y_i\ge0.
$$

Thus global zero defect is equivalent to pointwise sign compatibility. The
disjoint-support case used in the theorem is one clean sufficient condition:
if one of $x_i,y_i$ is zero at every coordinate, then $x_i y_i=0$ locally and
the global $\ell^1$ defect vanishes.

Lean also packages this disjoint-support green case as a single certificate:
exact $\ell^1$ additivity, zero global defect, zero coordinate defects, and
zero coordinate products all hold together. The helper
`disjointSupport_mul_eq_zero` records that support separation is not a sign
convention; it makes every local cross-product vanish.

Equivalently, Lean proves the exact finite rational additivity locus:

$$
\|x+y\|_1=\|x\|_1+\|y\|_1
\quad\Longleftrightarrow\quad
\forall i,\ x_i y_i\ge0.
$$

So $\ell^1$ additivity is not mysterious: it is precisely the no-local-sign-
cancellation condition. Disjoint positive-sector aggregation is the special
case where compatibility is guaranteed by support separation.

The strict obstruction is equally local. Lean proves

$$
D_{1,i}(x,y)>0 \quad\Longleftrightarrow\quad x_i y_i<0
$$

and therefore

$$
D_1(x,y)>0 \quad\Longleftrightarrow\quad \exists i,\ x_i y_i<0.
$$

So the global $\ell^1$ defect is red exactly when some coordinate contains
local sign cancellation.

It also mechanizes the corresponding positive natural-power identity $\sum_i |x_i+y_i|^n=\sum_i |x_i|^n+\sum_i |y_i|^n$ for $n>0$, which is the finite algebraic content of the disjoint-support step below. The same Lean kernel proves nonnegativity of finite rational power sums, strict positivity when the block has a nonzero coordinate, and for $n>0$ the exact zero/positive criteria: the power sum is zero iff all coordinates are zero, equivalently positive iff some coordinate is nonzero. These are the finite rational witnesses for the $a,b>0$ premise used next.

Lean now also proves the finite witness-root version of the strict step: for
natural exponents $p\ge2$, if positive rational witnesses $a,b$ satisfy

$$
a^p=\sum_i |x_i|^p,\qquad b^p=\sum_i |y_i|^p,
$$

then disjoint support implies

$$
\sum_i |x_i+y_i|^p < (a+b)^p.
$$

This mechanizes the algebraic bridge from disjoint power-sum additivity to
strict aggregation below; the arbitrary real-root norm statement remains the
standard prose step.

Now let $p>1$. Define:

$$
a=\|x\|_p>0, \qquad b=\|y\|_p>0.
$$

Since supports are disjoint,

$$
\|x\oplus y\|_p^p = \|x\|_p^p+\|y\|_p^p = a^p+b^p.
$$

Therefore:

$$
\|x\oplus y\|_p = (a^p+b^p)^{1/p}.
$$

For $a,b>0$ and $p>1$, set $t=a/(a+b)\in(0,1)$. Then

$$
\frac{a^p+b^p}{(a+b)^p}=t^p+(1-t)^p< t+(1-t)=1.
$$

Hence $(a^p+b^p)^{1/p}<a+b$.

Thus:

$$
\|x\oplus y\|_p<\|x\|_p+\|y\|_p.
$$

$\square$

**Consequence:**

> **$\ell^1$ is the unique $\ell^p$ bookkeeping norm with exact additive aggregation on disjoint positive sectors.**

This does not make $\ell^1$ universal. It makes it canonical for observers requiring exact disjoint-sector additivity.

### 1.4 Theorem 3 — Strict Row-Sparsity of Descent-Compatible Linear Maps **[PROVEN, CONDITIONAL on chosen sector basis + imported linear representation]**

**Statement:**

Let $U:\mathbb C^\Gamma\to\mathbb C^{\Gamma'}$ be linear.

Define phase-blind descent equivalence:

$$
c\sim c' \iff |c_i|^2=|c_i'|^2 \quad \forall i\in\Gamma.
$$

In the Lean hardening, the finite rational version of this relation is represented as the zero relation of a primitive difference:

$$
\delta(c,c')_i=c_i^2-(c_i')^2.
$$

Thus phase-blind descent is explicitly a quotient-by-zero-difference discipline, not an extra physical postulate.

Suppose $U$ is descent-compatible:

$$
c\sim c' \Rightarrow U(c)\sim U(c').
$$

Then each output row of $U$ has at most one nonzero entry.

Equivalently, each output coordinate $U(c)_j$ depends on at most one input coordinate.

**Proof:**

Fix an output coordinate $j$. It has the form:

$$
U(c)_j=\sum_{i\in\Gamma}U_{ji}c_i.
$$

Suppose for contradiction that row $j$ contains two distinct nonzero entries:

$$
U_{ji}\neq0, \qquad U_{jk}\neq0, \qquad i\neq k.
$$

Choose an input $c$ supported only on coordinates $i,k$, with:

$$
c_i=r_i>0, \qquad c_k=r_k>0.
$$

Now define a phase-rotated input $c^{(\theta)}$ by:

$$
c_i^{(\theta)}=r_i, \qquad c_k^{(\theta)}=r_k e^{i\theta},
$$

with all other coordinates zero.

For every $\theta$,

$$
|c_i^{(\theta)}|^2=r_i^2, \qquad |c_k^{(\theta)}|^2=r_k^2.
$$

Therefore:

$$
c^{(\theta)}\sim c^{(0)}.
$$

By descent compatibility, we must have:

$$
|U(c^{(\theta)})_j|^2 = |U(c^{(0)})_j|^2
$$

for all $\theta$.

But:

$$
U(c^{(\theta)})_j = U_{ji}r_i+U_{jk}r_ke^{i\theta}.
$$

Then:

$$
|U(c^{(\theta)})_j|^2 = |U_{ji}r_i|^2 + |U_{jk}r_k|^2 + 2\operatorname{Re} \left( U_{ji}r_i\overline{U_{jk}r_k}e^{-i\theta} \right).
$$

Since $U_{ji}r_i\neq0$ and $U_{jk}r_k\neq0$, the cross term depends on $\theta$. Therefore the output modulus varies with the relative phase.

This contradicts descent compatibility.

Hence each row has at most one nonzero entry.

> **Phase-blind descent-compatible linear maps cannot generically mix input coordinates.**

The Lean hardening mechanizes the finite rational sign-phase shadow of this argument: for a finite row $a:\iota\to\mathbb Q$, if

$$
\sum_i a_i x_i
$$

has squared output invariant under all input sign changes preserving each $x_i^2$, then for any distinct $i\ne k$ one has $a_i a_k=0$. Thus no two distinct row coefficients can both be nonzero. This is the finite-row algebraic kernel of the complex phase-rotation proof above.

Lean also packages the same finite rational conclusion as a support statement:
if two coefficients in a descent-compatible row are both nonzero, then their
indices are equal. Equivalently, the nonzero support of such a row is
subsingleton.

Lean now proves the converse in the same finite rational sign-phase model:
the zero row is descent-compatible, any row supported at one coordinate is
descent-compatible, and a finite row is descent-compatible iff its nonzero
support is subsingleton. Thus the mechanized rational shadow is a classification
of compatible rows, while the complex Hilbert phase-rotation theorem remains the
prose-standard argument for the full statement.

Lean also proves the quotient form of this finite rational classification:
the squared row-output observable factors through the `PrimitiveDifference`
residual quotient exactly when the row support is subsingleton. In
Local-Green/Global-Red terms, squared-coordinate equality is locally green for
the quotient only for row-sparse observables; generic mixing remains globally
red after phase-blind descent.

Lean further lifts this from a single row to a finite rational matrix. For
$M:\kappa\to(\iota\to\mathbb Q)$, the matrix-level squared-output observable
factors through the same phase-blind `PrimitiveDifference` quotient exactly
when every output row has subsingleton support. Thus the mechanized finite
shadow now matches the paper's row-by-row statement: descent compatibility is
a per-output-row condition, not a hidden global cancellation among rows.

This is a basis-relative result for the declared sector decomposition. Changing the sector basis changes the descent equivalence relation and therefore changes which linear maps are descent-compatible.

$\square$

**Consequence:**

If $U$ is additionally unitary and descent-compatible in this phase-blind sector category, then row-sparsity forces $U$ to be a monomial unitary: a permutation of sectors followed by phases. Generic unitaries therefore do not commute with phase-blind descent.

They may still be used as lifted pre-descent dynamics, but they do not commute with phase-blind descent for all phase-equivalent inputs.

### 1.5 Theorem 4 — Hilbert-Lift Redundancy **[PROVEN]**

**Statement:**

Let $\Gamma$ carry nonnegative weights $w_\gamma\ge0$, not all zero.

Define a Hilbert lift:

$$
c_\gamma=\sqrt{w_\gamma}e^{i\theta_\gamma}.
$$

Then the Born normalization of the lifted vector recovers the direct $\ell^1$ normalization:

> **$P_{\mathrm{Born}}(\gamma) = \frac{|c_\gamma|^2}{\sum_\eta |c_\eta|^2} = \frac{w_\gamma}{\sum_\eta w_\eta} = P_{\ell^1}(\gamma).$**

**Proof:**

By definition:

$$
c_\gamma=\sqrt{w_\gamma}e^{i\theta_\gamma}.
$$

For sectors with $w_\gamma=0$, the phase is irrelevant because $c_\gamma=0$.

Therefore:

$$
|c_\gamma|^2 = |\sqrt{w_\gamma}|^2 |e^{i\theta_\gamma}|^2 = w_\gamma\cdot1 = w_\gamma.
$$

Similarly:

$$
\sum_{\eta}|c_\eta|^2 = \sum_\eta w_\eta.
$$

Therefore:

$$
P_{\mathrm{Born}}(\gamma) = \frac{|c_\gamma|^2}{\sum_\eta |c_\eta|^2} = \frac{w_\gamma}{\sum_\eta w_\eta} = P_{\ell^1}(\gamma).
$$

$\square$

**Finite Lean certificate.** The finite rational kernel is mechanized in
`PaperQF002.L010_01_BornRedundancy.bornNormalization_redundant_certificate`.
First, the historical theorem
`bornProbFromNormSq_probability_certificate` proves that any finite rational
squared-norm weight function with nonnegative entries and positive total
normalizes to a nonnegative unit-sum weight profile. Reading that profile as a
probability law requires a separately declared probability adapter. Then, given
rational functions `w` and `normSq`, a pointwise
identity `normSq = w`, nonnegativity of `w`, and `0 < totalWeight w`, Lean
packages the redundancy as a certificate:

1. every Born-normalized weight is nonnegative;
2. the Born-normalized weights sum to one;
3. the Born-normalized weights agree pointwise with direct $\ell^1$
   normalization.

Lean also proves the associated normalization bookkeeping law: multiplying all
finite rational squared-norm weights by the same positive rational scalar does
not change `bornProbFromNormSq`. More generally, using its pointwise equality
with direct normalization, Lean proves that finite rational squared-norm
normalization factors through the same scalar-ray `PrimitiveDifference`
quotient, and on the nonzero-total locus its fibers are exactly scalar-ray
classes. It also proves that squared-norm normalization preserves support
exactly: under positive total squared norm,
`bornProbFromNormSq normSq γ = 0` iff `normSq γ = 0`, and
`0 < bornProbFromNormSq normSq γ` iff `0 < normSq γ`. Under the redundancy
hypothesis `normSq = w`, the same zero/positive support statement transfers
pointwise to the direct $\ell^1$ weights. The same finite rational algebra
preserves ranking and ties: weak order, strict order, and equality between two
normalized squared-norm coordinates are exactly the corresponding order or
equality relations between their squared norms; under `normSq = w`, this is
the same ranking as the direct $\ell^1$ weights. Finally, Lean proves that
squared-norm normalization is idempotent: normalizing an already normalized
finite rational squared-norm weight vector changes no coordinate.

This is a finite algebra certificate for normalization and redundancy only. It
neither derives a Hilbert representation nor upgrades the conditional
Born-uniqueness claim of Theorem 6.

**Consequence:**

The Hilbert lift adds no new information to the normalized sector-weight profile itself:

> **Born normalization is redundant once nonnegative additive sector weights are already given.**

It may add representation capacity for phase, interference, and reversible lifted dynamics, but those are imported structure, not consequences of $\ell^1$ weights alone.

### 1.6 Theorem 5 — Phase-Averaged Shadow Theorem **[PROVEN, CONDITIONAL on chosen Hilbert lift + Haar phase measure + independence adapter]**

**Statement:**

Let:

$$
|\psi(\theta)\rangle = \sum_{\gamma\in\Gamma} \sqrt{w_\gamma}e^{i\theta_\gamma} |\gamma\rangle.
$$

Let:

$$
|u\rangle=\sum_{\gamma\in\Gamma}u_\gamma|\gamma\rangle.
$$

Assume the phases $\theta_\gamma$ are independent Haar-uniform on $U(1)$. Then:

> **$\mathbb E_\theta \left[ |\langle u,\psi(\theta)\rangle|^2 \right] = \sum_{\gamma\in\Gamma}|u_\gamma|^2w_\gamma.$**

**Proof:**

Using the standard complex inner product convention,

$$
\langle u,\psi(\theta)\rangle = \sum_{\gamma} \overline{u_\gamma} \sqrt{w_\gamma} e^{i\theta_\gamma}.
$$

Therefore:

$$
|\langle u,\psi(\theta)\rangle|^2 = \left( \sum_{\gamma} \overline{u_\gamma} \sqrt{w_\gamma} e^{i\theta_\gamma} \right) \left( \sum_{\eta} u_\eta \sqrt{w_\eta} e^{-i\theta_\eta} \right).
$$

Expand:

$$
|\langle u,\psi(\theta)\rangle|^2 = \sum_{\gamma,\eta} \overline{u_\gamma}u_\eta \sqrt{w_\gamma w_\eta} e^{i(\theta_\gamma-\theta_\eta)}.
$$

Take expectation over independent Haar phases.

For $\gamma=\eta$,

$$
e^{i(\theta_\gamma-\theta_\eta)}=1.
$$

For $\gamma\ne\eta$,

$$
\mathbb E[e^{i(\theta_\gamma-\theta_\eta)}] = \mathbb E[e^{i\theta_\gamma}] \mathbb E[e^{-i\theta_\eta}] = 0\cdot0 = 0.
$$

Therefore all off-diagonal terms vanish and only diagonal terms remain:

$$
\mathbb E_\theta |\langle u,\psi(\theta)\rangle|^2 = \sum_{\gamma} \overline{u_\gamma}u_\gamma w_\gamma = \sum_\gamma |u_\gamma|^2w_\gamma.
$$

The Lean hardening mechanizes the finite two-sign algebraic kernel of this cancellation:

$$
\frac{(A+B)^2+(A-B)^2}{2}=A^2+B^2.
$$

It also mechanizes the independent two-sign rational analogue:

$$
\frac{(A+B)^2+(A-B)^2+(-A+B)^2+(-A-B)^2}{4}=A^2+B^2.
$$

Lean now also proves the finite list version for independent rational sign
choices. If $A=(A_1,\ldots,A_n)$ and the average ranges over all
$s\in\{\pm1\}^n$, then:

$$
\frac{1}{2^n}\sum_{s\in\{\pm1\}^n}\left(\sum_i s_i A_i\right)^2
=\sum_i A_i^2.
$$

These are finite rational analogues of averaging away off-diagonal cross
terms. The full theorem still imports the chosen complex Hilbert lift and
independent Haar-uniform phase assumptions.

This theorem uses the unnormalized lifted vector. If the normalized vector $|\tilde\psi\rangle = W^{-1/2}|\psi\rangle$ is used instead, the right-hand side becomes

$$
\sum_\gamma |u_\gamma|^2 w_\gamma / W.
$$

$\square$

**Consequence:**

Phase averaging converts the lifted quadratic expression into a phase-blind weighted sector shadow.

This is a theorem about the chosen Hilbert lift plus Haar phase averaging. It is not a derivation of quantum measurement from $\ell^1$ alone.

The Haar-phase expectation is a property of the chosen random-phase lift. It is not a measurement postulate and does not identify a physical ensemble unless such an ensemble is separately declared.

### Worked Replay — Born Redundancy, Disjoint Aggregation, and the Phase-Averaged Shadow

Take three sectors with weights $w=(2,1,1)$, so $W=4$ and the direct law is $P_{\ell^1}=(0.5,0.25,0.25)$. Pick *any* phases, e.g. $\theta=(0.3,1.1,2.7)$, and form $c_\gamma=\sqrt{w_\gamma}\,e^{i\theta_\gamma}$. Then $|c_\gamma|^2=w_\gamma$ and

$$
P_{\mathrm{Born}}(\gamma)=\frac{|c_\gamma|^2}{\sum_\eta|c_\eta|^2}=(0.5,0.25,0.25)=P_{\ell^1}(\gamma)
$$

to machine precision — the phases cancel exactly (Theorem 4).

Disjoint-support aggregation (Theorem 2): for unit blocks $\|x\|_p=\|y\|_p=1$ with $p=2$, $\|x\oplus y\|_2=\sqrt{1^2+1^2}=\sqrt2\approx1.414<2=\|x\|_2+\|y\|_2$, whereas $p=1$ gives exact additivity $1+1=2$.

Phase-averaged shadow (Theorem 5): with $u=(1,-0.5,0.25)$ and Haar-uniform phases, a $3\times10^5$-sample Monte-Carlo estimate of $\mathbb E_\theta|\langle u,\psi(\theta)\rangle|^2$ returns $\approx2.313$, matching the predicted $\sum_\gamma|u_\gamma|^2 w_\gamma=2.3125$.

```python
import numpy as np
w = np.array([2., 1, 1])
c = np.sqrt(w) * np.exp(1j * np.array([0.3, 1.1, 2.7]))   # arbitrary phases
print(np.abs(c)**2 / (np.abs(c)**2).sum())   # [0.5 0.25 0.25] == w / w.sum()
print(np.sqrt(1 + 1))                        # 1.4142... < 2  (disjoint l2 aggregation)
```

Expected output: `[0.5 0.25 0.25]`, `1.4142135...`.

### 1.7 Theorem 6 — Conditional Quadratic/Born Uniqueness Requires Imported Representation Assumptions **[Part 1: PROVEN / SCOPE FENCE; Part 2: STANDARD + citation [1,2] (Gleason route), CONDITIONAL on the imported assumptions 1–7]**

**Statement:**

The quadratic Born form

$$
F(\psi)_\gamma\propto |\psi_\gamma|^2
$$

is not forced by $\ell^1$ additive weights alone.

It is selected only after importing additional representation assumptions, such as:

1. finite additive nonnegative sector weights;
2. complex linear Hilbert representation;
3. phase-blind positive descent map;
4. orthogonal additivity over disjoint sectors;
5. reversible lifted dynamics by linear isometries;
6. interference represented by bilinear cross terms;
7. projection-measure or frame-function structure, if invoking Gleason-type uniqueness.

Under those imported assumptions, the quadratic form is conditionally selected.

**Proof:**

**Part 1 — $\ell^1$ weights alone do not force Hilbert space**

A finite nonnegative weight vector

$$
w\in\mathbb R_{\ge0}^{\Gamma}
$$

already defines a probability distribution by Theorem 1.

Nothing in this datum uniquely specifies:

- a complex vector space;
- an inner product;
- phases;
- unitary dynamics;
- projectors;
- POVMs;
- interference;
- or a measurement lattice.

For the same weights $w_\gamma$, one could choose:

$$
c_\gamma=\sqrt{w_\gamma}e^{i\theta_\gamma}
$$

in complex Hilbert space, or choose a purely classical representation:

$$
p_\gamma=\frac{w_\gamma}{W},
$$

or choose real signed amplitudes, quaternionic amplitudes, nonlinear embeddings, or redundant encodings.

Thus $\ell^1$ additive weights alone do not force Hilbert structure.

**Part 2 — Quadratic form follows after Hilbert/frame assumptions**

Now assume a complex Hilbert space representation with sectors represented by orthogonal basis states $|\gamma\rangle$.

Assume the probability assignment is:

- phase-blind,
- positive,
- continuous,
- additive over orthogonal sectors,
- normalized on complete decompositions.

Then the assignment is a frame function on the projective Hilbert space.

For Hilbert dimension $\ge3$, the Gleason-type route implies that such a probability measure has the form:

$$
P(\Pi)=\operatorname{Tr}(\rho\Pi)
$$

for a positive trace-one operator $\rho$.

For a pure state

$$
\rho=|\psi\rangle\langle\psi|,
$$

and a sector projector

$$
\Pi_\gamma=|\gamma\rangle\langle\gamma|,
$$

this gives:

$$
P(\gamma) = \operatorname{Tr}\bigl(|\psi\rangle\langle\psi|\,|\gamma\rangle\langle\gamma|\bigr) = |\langle\gamma,\psi\rangle|^2 = |\psi_\gamma|^2.
$$

Thus the quadratic Born form is selected under the imported Hilbert/projection-measure assumptions. The Gleason route requires a probability assignment over projectors / closed subspaces across all relevant orthogonal decompositions, not merely additivity over one fixed sector basis.

For dimension $2$, ordinary Gleason assumptions do not suffice; one must explicitly import a POVM Gleason variant, continuity/context assumptions, or another strengthening.

Therefore:

> **Born quadratic uniqueness is conditional on imported representation structure, not a theorem of $\ell^1$ additivity alone.**

$\square$

### 1.8 Theorem 7 — Hilbert-Lift Redundancy Does Not Eliminate Lifted Dynamics **[PROVEN — representation-capacity observation]**

**Statement:**

Although the Hilbert lift is redundant for reproducing sector probabilities, it is not redundant as a representation for phase-sensitive dynamics.

**Proof:**

By Theorem 4, the probability law:

$$
P(\gamma)=\frac{w_\gamma}{\sum_\eta w_\eta}
$$

is already recovered directly from the weights.

The lifted vector:

$$
c_\gamma=\sqrt{w_\gamma}e^{i\theta_\gamma}
$$

contains additional phase data $\theta_\gamma$ not present in $w_\gamma$.

A unitary transformation $U$ can mix amplitudes:

$$
c\mapsto Uc.
$$

The descended weights after the lifted transformation are:

$$
w_\gamma' = |(Uc)_\gamma|^2.
$$

These weights can depend on relative phases in $c$. Therefore the Hilbert lift can represent interference and reversible redistribution before descent.

The Lean hardening records the finite rational witness behind this point: the sign-phase lifts $(1,1)$ and $(1,-1)$ have identical squared sector weights, but the two-row mixing shadow $((x+y)^2,(x-y)^2)$ sends them to $(4,0)$ and $(0,4)$ respectively. This is a representation-capacity witness, not a derivation of the imported Hilbert/unitary structure.

Lean also proves the parametric form of the same two-sector witness: for any
rational pair $(x,y)$ with $xy\ne0$, the sign flip $(x,y)\mapsto(x,-y)$
preserves local squared weights but changes the mixed output weights. Thus the
LGGR obstruction is exactly the nonzero cross term, not a special feature of
the unit example.

Lean also packages the same witness as a `PrimitiveDifference` quotient
statement. The squared-weight observable

$$
(x,y)\mapsto (x^2,y^2)
$$

is invariant under the phase-blind quotient and therefore factors through it.
The two-row mixing observable

$$
(x,y)\mapsto ((x+y)^2,(x-y)^2)
$$

does not factor through that quotient. This is the two-sector LGGR certificate:
local squared weights are quotient-stable, while global phase-sensitive mixing
is not determined by the local phase-blind shadow.

The obstruction survives post-mix normalization. Lean defines the direct
two-output normalization

$$
N(a,b)=\left(\frac{a}{a+b},\frac{b}{a+b}\right)
$$

For the same $xy\ne0$ hypothesis used in the sign-flip witness, Lean proves
that $N((x+y)^2,(x-y)^2)$ is a finite probability pair: both coordinates are
nonnegative and their sum is one.

and proves that, for $xy\ne0$,

$$
N((x+y)^2,(x-y)^2)\ne N((x-y)^2,(x+y)^2).
$$

For the concrete sign pair, Lean computes the fully normalized witness:

$$
N(1^2,1^2)=N(1^2,(-1)^2)=\left(\frac12,\frac12\right),
$$

while

$$
N((1+1)^2,(1-1)^2)=(1,0),\qquad
N((1+(-1))^2,(1-(-1))^2)=(0,1).
$$

Equivalently, the normalized mixed-probability observable still has no
factorization through the phase-blind `PrimitiveDifference` quotient.
Lean sharpens this into an exact classifier: the sign flip
$(x,y)\mapsto(x,-y)$ swaps the two normalized mixed coordinates, and the
normalized mixed probabilities agree after sign flip if and only if $xy=0$.
Thus the finite normalized LGGR obstruction is exactly the nonzero cross term.
Equivalently, if $\Delta(a,b)=a-b$, then Lean proves the normalized imbalance
formula

$$
\Delta\!\left(N((x+y)^2,(x-y)^2)\right)=\frac{2xy}{x^2+y^2}
$$

for $xy\ne0$; sign flip negates this imbalance.
Lean also defines the algebraic squared distance
$d_2^2((a,b),(c,d))=(a-c)^2+(b-d)^2$. With this finite rational measure,
local normalized squared weights have zero distance under sign flip, while
normalized mixed probabilities have strictly positive squared distance whenever
$xy\ne0$. Lean computes the obstruction size exactly:

$$
d_2^2\!\left(N((x+y)^2,(x-y)^2),N((x-y)^2,(x+y)^2)\right)
=\frac{8x^2y^2}{(x^2+y^2)^2}
$$

for $xy\ne0$. Lean also proves the associated zero-obstruction classifier:
this normalized mixed squared distance is zero exactly when $xy=0$.

By contrast, local direct-normalized squared weights do descend. Lean defines

$$
(x,y)\mapsto N(x^2,y^2)
$$

and proves that this observable is invariant under the phase-blind quotient and
therefore factors through it. For any nonzero local pair, Lean also proves that
$N(x^2,y^2)$ is a finite probability pair: both coordinates are nonnegative
and their sum is one. For the same local observable, Lean proves

$$
\Delta\!\left(N(x^2,y^2)\right)=\frac{x^2-y^2}{x^2+y^2}
$$

and proves that sign flip preserves this local normalized imbalance. This is
the normalized Local-Green/Global-Red split: local normalized squared weights
are valid quotient-stable probabilities, with quotient-stable imbalance, but
normalized probabilities after phase-sensitive mixing are not quotient-stable.
Lean makes the separation explicit: for $xy\ne0$, the two sign-equivalent
inputs cannot both have their normalized mixed outputs identified with their
local normalized squared-weight probabilities. Equivalently, at least one side
of the sign-flip pair must exhibit a normalized local-vs-mixed mismatch.
Lean also classifies the single-branch equality locus: for
$x^2+y^2\ne0$, the positive mixed branch equals the local normalized output
exactly when $2xy=x^2-y^2$, while the sign-flipped branch equals its local
normalized output exactly when $-2xy=x^2-y^2$. Hence, away from the zero pair,
the two sign-related mixed outputs cannot both be locally explained.
Lean gives the corresponding one-branch squared-distance formulas:

$$
d_2^2\!\left(N((x+y)^2,(x-y)^2),N(x^2,y^2)\right)
=\frac{(x^2-y^2-2xy)^2}{2(x^2+y^2)^2}
$$

and

$$
d_2^2\!\left(N((x-y)^2,(x+y)^2),N(x^2,(-y)^2)\right)
=\frac{(x^2-y^2+2xy)^2}{2(x^2+y^2)^2}.
$$

Thus each one-branch obstruction vanishes exactly at its corresponding
quadratic balance.
Lean also quantifies the partition: for every nonzero local pair
($x^2+y^2\ne0$), the two squared distances from the local normalized
squared-weight output to the two sign-related normalized mixed outputs add to
one,

$$
d_2^2\!\left(N((x+y)^2,(x-y)^2),N(x^2,y^2)\right)
+d_2^2\!\left(N((x-y)^2,(x+y)^2),N(x^2,(-y)^2)\right)=1
$$

Consequently, at least one sign-related branch has squared distance at least
$1/2$ from the local normalized output. In this finite witness, the local
green explanation cannot make both sign-related global branches simultaneously
small.

Lean also proves the endpoint classifiers:

$$
d_2^2\!\left(N((x+y)^2,(x-y)^2),N(x^2,y^2)\right)=1
\quad\Longleftrightarrow\quad
-2xy=x^2-y^2
$$

and

$$
d_2^2\!\left(N((x-y)^2,(x+y)^2),N(x^2,(-y)^2)\right)=1
\quad\Longleftrightarrow\quad
2xy=x^2-y^2.
$$

Thus exact local explanation of one sign-related branch forces maximal
squared-distance failure on the opposite branch.

Finally, Lean packages the split as a PrimitiveDifference diagnostic. The
combined map

$$
p\longmapsto\left(N(p_1^2,p_2^2),
N((p_1+p_2)^2,(p_1-p_2)^2)\right)
$$

has a green first projection: the local normalized squared-weight component
factors through the phase-blind quotient. The full paired diagnostic has no
factor through that same quotient, because the mixed component separates
phase-blind-equivalent sign choices. This is the formal local-green/global-red
statement used here.
The quotient obstruction is now mechanized through a reusable
`PrimitiveDifference` product-diagnostic theorem: a paired diagnostic descends
exactly when both projections descend. In this instance, the local projection
descends and the mixed projection does not, so the pair cannot descend.
The no-factor steps use the core quotient law directly: any diagnostic that is
not invariant on zero-related inputs has no residual-quotient factor.
Lean also packages this as a reusable LGGR obstruction theorem: one invariant
projection supplies the local quotient factor, while one non-invariant
projection blocks quotient descent of the paired diagnostic.
The Q-level bridge is now explicit: `QM.QLevelLGGRBridge.density_lggr_is_q_level_primitive_nonpromotion`
reuses `Paper_Q.primitive_continuum_lggr_nonpromotion` to identify this
residual-density pattern as a Level-Q PrimitiveDifference non-promotion
instance. The theorem says only that a local density-like profile can descend
while a paired hidden/global coordinate cannot; it is not a Born-rule
derivation and does not grant authority. The declared-equivalence extension,
`QM.QLevelLGGRBridge.density_mod_lggr_is_q_level_primitive_nonpromotion`,
adds the Q-packet version: even when the density diagnostic descends only
modulo a declared output equivalence, a hidden/global or authority coordinate
that remains separated modulo its own declared equivalence still blocks paired
modulo descent. The density-side coarsening theorem,
`QM.QLevelLGGRBridge.density_mod_lggr_persists_under_density_coarsening`,
then records the admissible weakening: a fine density equivalence may be lowered
to a coarser density equivalence without promoting a still-separated hidden or
authority coordinate. The product-composition theorem,
`QM.QLevelLGGRBridge.local_pair_mod_lggr_is_q_level_primitive_nonpromotion`,
adds the multi-diagnostic closure: two local green visible diagnostics may be
paired into a larger visible green packet, but the augmented packet with a
still-separated hidden/global or authority coordinate remains red. The readout-closure theorem,
`QM.QLevelLGGRBridge.diagnostic_readout_mod_lggr_is_q_level_primitive_nonpromotion`,
then records the report layer: equivalence-respecting summaries of a green
diagnostic stay green, while a hidden/global or authority readout that still
separates the zero witness keeps the augmented report red.
The converse/certificate-obligation theorem,
`QM.QLevelLGGRBridge.local_pair_mod_factor_implies_hidden_quotient_compatible`,
adds the reverse audit: if an augmented visible product or readout packet really
descends through the residual quotient, then the hidden/global coordinate, or
the hidden readout being reported, was already quotient-compatible. Red cannot
be hidden inside a larger local-green report without proving its own quotient
compatibility.
The augmented-certificate criterion,
`QM.QLevelLGGRBridge.local_pair_mod_factor_iff_hidden_quotient_compatible`,
then closes the audit: once the visible side is already green, augmented product
or readout descent is equivalent to quotient compatibility of the hidden/global
coordinate or hidden readout.
The componentwise paired-descent theorem,
`QM.ResidualDensityBridge.factorsThroughResidualMod_pair_iff_component_factors`,
records the general algebra behind this audit: a paired residual diagnostic
descends modulo a product equivalence exactly when each component descends
modulo its own declared equivalence.
The red-coordinate monotonicity theorem,
`QM.ResidualDensityBridge.pair_mod_no_factor_of_left_not_factor`,
adds the contrapositive audit rule: if either component fails its residual
descent obligation, then the paired diagnostic cannot descend modulo the
product equivalence.
The nested-triple theorem,
`QM.ResidualDensityBridge.factorsThroughResidualMod_triple_iff_component_factors`,
extends the audit to three-coordinate packets: descent of
$((d_1,d_2),d_3)$ modulo the nested product equivalence is equivalent to the
three component descent obligations, and any one non-descending coordinate
blocks the whole triple.
The witness-backed form records all four facts at once: local equality, paired
diagnostic inequality, local quotient descent, and paired quotient obstruction.
Lean also gives the explicit parametric witness: when $xy\ne0$, the pair
$(x,y)$ and its sign flip $(x,-y)$ are zero-related in the phase-blind
PrimitiveDifference, their local projections agree, and their paired
local/global diagnostics differ.

However, that capacity comes from the imported complex linear representation and unitary dynamics. It does not alter the direct normalization theorem.

Thus:

> **Hilbert lift is probability-redundant but dynamics-capable.**

$\square$

### 1.9 Final Consolidated Result

For finite nonnegative sector weights $w_\gamma$:

> **$P_{\ell^1}(\gamma) = \frac{w_\gamma}{\sum_\eta w_\eta}$**

is already a normalized nonnegative weight profile. It becomes a probability
law only under a separately declared probability interpretation.

The optional Hilbert lift:

> **$c_\gamma=\sqrt{w_\gamma}e^{i\theta_\gamma}$**

satisfies:

> **$P_{\mathrm{Born}}(\gamma) = \frac{|c_\gamma|^2}{\sum_\eta |c_\eta|^2} = P_{\ell^1}(\gamma).$**

The descent-compatible linear maps are row-sparse:

> **$c\sim c'\Rightarrow Uc\sim Uc' \quad\Longrightarrow\quad \text{each row of }U\text{ has at most one nonzero entry.}$**

Phase averaging gives:

> **$\mathbb E_\theta \left[ |\langle u,\psi(\theta)\rangle|^2 \right] = \sum_\gamma |u_\gamma|^2w_\gamma.$**

And the main firewall is:

> **$\ell^1$ weights alone do not derive Hilbert space, unitarity, quantum measurement, or the Born rule as ontology.**

The exact claim is:

> **Born normalization is a redundant Hilbert encoding of already-given additive sector weights, while Born uniqueness requires imported Hilbert/projection assumptions.**


Falsifiability

The redundancy claim (Theorem 4) is falsified by any nonnegative weight vector $w$ and phase choice for which $|c_\gamma|^2/\sum_\eta|c_\eta|^2\ne w_\gamma/\sum_\eta w_\eta$. The conditional-uniqueness claim is falsified only by a phase-blind, positive, normalized, orthogonally additive frame-function assignment over projectors / closed subspaces across the declared Hilbert representation, satisfying the imported assumptions of Theorem 6, that is not of the form $\operatorname{Tr}(\rho\Pi)$. The row-sparsity claim (Theorem 3) is falsified by any descent-compatible linear map with a two-nonzero output row.

Related Work and Positioning

1. **Gleason's theorem** [1] and POVM / frame-function variants [2]: this paper invokes Gleason-type uniqueness *as an imported hypothesis* (Theorem 6), not as a result derived from $\ell^1$ weights.
2. **Derivations of the Born rule** (envariance, decision-theoretic) [3, 4]: the paper deliberately does **not** claim a Born derivation; it isolates the narrow normalization redundancy from the ontological claim.
3. **Strict convexity / Minkowski inequality for $\ell^p$, $p>1$** [5]: Theorem 2's disjoint-support strict subadditivity is the elementary $\ell^p$ fact, used to single out $\ell^1$ as the additive bookkeeping norm.
4. **Companion corpus papers** 006 / 007 ($\ell^1$ selection and quotient norm) [6].

References

[1] A. M. Gleason, "Measures on the closed subspaces of a Hilbert space," *J. Math. Mech.* **6** (1957), 885–893.

[2] P. Busch, "Quantum states and generalized observables: a simple proof of Gleason's theorem," *Phys. Rev. Lett.* **91** (2003), 120403.

[3] W. H. Zurek, "Environment-assisted invariance, entanglement, and probabilities in quantum physics," *Phys. Rev. Lett.* **90** (2003), 120404.

[4] D. Wallace, *The Emergent Multiverse*, Oxford University Press, 2012.

[5] G. H. Hardy, J. E. Littlewood, and G. Pólya, *Inequalities*, Cambridge University Press, 1934.

[6] J. H. Carroll, "L1-Native Cohomology of Defect Fields: Quotient Norms, Dual Circulations, and Hodge Inflation" (<https://zenodo.org/uploads/20186523>); "An L1 Obstruction Framework for Coboundary Defects" (<https://zenodo.org/uploads/20186809>). Zenodo, 2026.

Changelog

### v3.0.2 (2026-06-13)

- Added Lean hardening references for PL-010-1:
  `PaperQF002.L010_01_BornRedundancy` mechanizes direct normalization
  plus nonzero rational rescaling invariance, zero/positive support preservation,
  unit-interval bounds, and order/tie preservation
  (Theorem 1), squared-norm normalization plus Born-normalization redundancy,
  finite nonnegativity, unit-interval, sum-one, pointwise-equality certificate,
  positive rational squared-norm scale-invariance, squared-norm support
  preservation, and order/tie preservation
  (Theorem 4), plus partial kernels for finite
  $\ell^1$ nonnegativity, zero/positive norm criteria, triangle inequality, exact finite
  disjoint-support $\ell^1$ additivity, positive
  natural-power disjoint-support additivity, finite power-sum nonnegativity
  plus zero/positive criteria, strict positive two-block integer-exponent
  $p\ge2$ aggregation (Theorem 2), and the sign-phase finite-row row-sparsity
  obstruction (Theorem 3).

- Represented the finite rational phase-blind descent relation as the zero
  relation of a primitive difference
  $\delta(c,c')_i=c_i^2-(c_i')^2$, aligning Theorem 3 with the OmegaCore
  quotient-by-zero-difference discipline.

- Added the finite rational quotient-factorization form for Theorem 3:
  the squared row-output observable factors through the
  `PrimitiveDifference` residual quotient iff the row support is subsingleton.

- Added the finite rational matrix-level quotient-factorization form for
  Theorem 3: the squared output vector factors through the phase-blind
  `PrimitiveDifference` residual quotient iff every output row has
  subsingleton support.

- Added a finite rational Lean witness for Theorem 7: sign-phase lifts with
  identical squared sector weights can descend to different mixed output
  weights after a two-row mixing operation. This is recorded as a
  representation-capacity witness, not a derivation of Hilbert/unitary
  structure.

- Generalized the Theorem 7 witness: any rational two-sector pair with nonzero
  product has the same local squared weights after a sign flip but different
  mixed output weights.

- Strengthened the Theorem 7 witness as a `PrimitiveDifference` quotient
  certificate: squared sector weights factor through the phase-blind quotient,
  while the two-row mixing observable has no factorization through that
  quotient. This is the finite two-sector LGGR witness.

- Strengthened the Theorem 7 witness after post-mix direct normalization:
  `twoRowMixWeights_normalized_no_factor_through_phaseBlindQuotient` proves
  that normalized mixed probabilities still do not factor through the
  phase-blind quotient.

- Added the exact normalized sign-flip classifier:
  `twoRowMixWeights_normalized_sign_flip_swap` proves that sign flip swaps the
  normalized mixed coordinates, and
  `twoRowMixWeights_normalized_sign_flip_eq_iff_mul_eq_zero` proves equality
  iff the cross term vanishes.

- Added the exact normalized imbalance formula:
  `twoRowMixWeights_normalized_imbalance_formula` proves the imbalance is
  `2*x*y/(x^2+y^2)`, and
  `twoRowMixWeights_normalized_imbalance_sign_flip` proves sign flip negates it.

- Added the normalized squared-distance LGGR certificate:
  `pairSquaredDirectProb_sign_flip_squaredDistance_eq_zero` proves zero local
  squared distance under sign flip, while
  `twoRowMixWeights_squaredDistance_normalized_sign_flip_pos` proves strictly
  positive normalized mixed squared distance under `x*y != 0`; Lean also proves
  the exact finite obstruction formula in
  `twoRowMixDistance_normalized_sign_flip_formula` and the zero-obstruction
  classifier in `twoRowMixDistance_zero_iff_crossTerm_zero`.

- Added a finite probability certificate for the normalized two-row mixed
  witness: `twoRowMixWeights_normalized_probability_certificate` proves
  nonnegative coordinates and total mass one.

- Added the local normalized side of the same LGGR certificate:
  `pairSquaredDirectProb_factor_exists` proves that direct-normalized local
  squared weights do factor through the phase-blind quotient.

- Added the finite probability certificate for the local normalized side:
  `pairSquaredDirectProb_probability_certificate` proves nonnegative
  coordinates and total mass one for any nonzero local pair.

- Added the exact local normalized imbalance certificate:
  `pairSquaredDirectProb_imbalance_formula` proves the imbalance is
  `(x^2-y^2)/(x^2+y^2)`, and
  `pairSquaredDirectProb_imbalance_sign_flip` proves sign flip preserves it.

- Added the normalized local-vs-mixed separation certificate:
  `twoRowMixWeights_normalized_not_local_on_sign_flip_pair` proves that the
  two sign-equivalent mixed outputs cannot both be identified with local
  normalized squared weights under `x*y != 0`, and
  `twoRowMixWeights_normalized_exists_local_mismatch_of_mul_ne_zero` extracts
  the resulting mismatch alternative.

- Added the normalized local-vs-mixed equality-locus classifiers:
  `twoRowMixLocalEq_iff_crossTermBalance` and
  `twoRowMixLocalFlipEq_iff_crossTermBalance` identify the exact quadratic
  balances for each sign branch, while `twoRowMixLocalBoth_ne_of_nonzero`
  strengthens the two-branch exclusion to every nonzero local pair.

- Added the normalized local-vs-mixed one-branch distance formulas:
  `twoRowMixLocalDistance_formula` and
  `twoRowMixLocalFlipDistance_formula` give the exact squared distances, while
  `twoRowMixLocalDistance_zero_iff` and
  `twoRowMixLocalFlipDistance_zero_iff` identify their zero loci.

- Added the normalized local-vs-mixed distance partition certificate:
  `twoRowMixLocalDistSum_one_nonzero` proves that the two sign-related
  normalized local-vs-mixed squared distances add to one for every nonzero
  local pair, and `twoRowMixLocalDistances_sum_eq_one` records the earlier
  nonzero-cross-term corollary.

- Added the normalized local-vs-mixed half-distance certificate:
  `twoRowMixLocalOneDist_ge_half` proves that at least one sign-related
  branch has squared distance at least `1/2` from the local normalized output.

- Added normalized local-vs-mixed endpoint classifiers:
  `twoRowMixLocalDistance_eq_one_iff_flipCrossTermBalance` and
  `twoRowMixLocalFlipDistance_eq_one_iff_crossTermBalance` prove that exact
  local explanation of one sign-related branch is paired with maximal
  squared-distance failure on the opposite branch.

- Added a PrimitiveDifference local-green/global-red diagnostic:
  `pairLocalGlobalDiagnostic_local_projection_factor_exists` proves the local
  projection factors through the phase-blind quotient, while
  `pairLocalGlobalDiagnostic_no_factor_through_phaseBlindQuotient` proves the
  paired local/global diagnostic does not.

- Added the product-diagnostic quotient criterion instance:
  `pairLocalGlobalDiagnostic_factor_exists_iff_components_invariant` proves the
  paired diagnostic descends exactly when both projections are invariant.

- Routed the phase-blind no-factor proofs through the reusable
  `PrimitiveDifference` no-factor theorem:
  `invariantFactor_no_factor_of_not_invariant`.

- Added the reusable PrimitiveDifference LGGR obstruction instance:
  `pairLocalGlobalDiagnostic_lggr_quotient_obstruction` packages local quotient
  descent together with failure of paired quotient descent.

- Added the witness-backed PrimitiveDifference LGGR certificate:
  `pairLocalGlobalDiagnostic_sign_flip_witness_and_quotient_obstruction`
  packages local equality, paired diagnostic inequality, local quotient
  descent, and paired quotient obstruction for the sign-flip witness.

- Added the explicit PrimitiveDifference LGGR sign-flip witness:
  `pairLocalGlobalDiagnostic_sign_flip_lggr_of_mul_ne_zero` proves zero-related
  sign-flip inputs have equal local projections but different paired
  local/global diagnostics whenever the cross term is nonzero.

- Added the concrete normalized unit LGGR witness:
  `normalized_unit_lggr_witness` proves that `(1,1)` and `(1,-1)` have the
  same local normalized squared weights `(1/2,1/2)` while their normalized
  mixed outputs are `(1,0)` and `(0,1)`.

- Strengthened the finite rational Theorem 3 row-sparsity kernel with a Lean
  support-subsingleton theorem: two nonzero coefficients in a compatible row
  must have the same index.

- Strengthened the finite rational Theorem 3 row-sparsity kernel with the
  converse direction: zero rows and one-coordinate-supported rows are
  descent-compatible, and finite-row descent compatibility is equivalent to
  the nonzero support being subsingleton in the rational sign-phase model.

- Strengthened the Theorem 2 finite power-sum kernel with Lean zero/positive
  criteria for positive natural exponents, and strengthened Theorem 4 with
  squared-norm support preservation and redundancy-support certificates.

- Added a finite $\ell^1$ additivity-defect object for Theorem 2:
  `l1AdditivityDefect` is nonnegative, vanishes exactly when the triangle
  inequality is sharp, and vanishes on disjoint supports.

- Packaged the disjoint-support Theorem 2 green certificate:
  `l1LocalGreenCertificate_of_disjointSupport` records exact additivity, zero
  global defect, zero local defects, and zero local cross-products together.

- Added the finite local-to-global decomposition of the $\ell^1$ additivity
  defect: the global defect is the sum of nonnegative coordinate defects, so
  it vanishes iff every local coordinate defect vanishes.

- Added the finite rational local sign-compatibility criterion:
  a coordinate $\ell^1$ defect vanishes iff the coordinate product is
  nonnegative; hence global zero defect is equivalent to pointwise
  sign-compatibility.

- Added the exact finite rational $\ell^1$ additivity locus:
  $\|x+y\|_1=\|x\|_1+\|y\|_1$ iff all coordinate products are nonnegative.

- Added the strict finite rational $\ell^1$ obstruction locus:
  the global additivity defect is positive iff some coordinate product is
  negative.

- Added the finite rational witness-root strict aggregation theorem:
  for $p\ge2$, disjoint-support power sums are strictly below $(a+b)^p$
  whenever $a^p$ and $b^p$ witness the two nonzero block power sums.

- Strengthened direct and squared-norm normalization with Lean unit-interval
  certificates: every normalized finite nonnegative coordinate lies in
  $[0,1]$ under positive total mass.

- Strengthened direct and squared-norm normalization with Lean order/tie
  preservation certificates: positive-total normalization preserves weak
  order, strict order, and equality of finite rational coordinates.

- Strengthened direct and squared-norm normalization with Lean idempotence
  certificates: after total mass is normalized to one, re-normalization is the
  identity coordinatewise.

- Added scalar-ray `PrimitiveDifference` quotient certificates: direct
  normalization and squared-norm normalization factor through the quotient that
  identifies finite rational weight vectors differing by a nonzero scalar.

- Added scalar-ray fiber classifier certificates: on the nonzero-total locus,
  equality of normalized finite rational weights is equivalent to membership
  in the same nonzero scalar ray.

- Added a finite rational Lean witness for Theorem 5's off-diagonal
  cancellation kernel:
  `((A+B)^2+(A-B)^2)/2 = A^2+B^2`. The full Haar phase-average theorem
  remains conditional on the chosen Hilbert lift and independent Haar phases.

- Added a finite-list rational sign-average Lean witness:
  `finite_rademacher_sign_average_square_identity`, proving that averaging
  `(\sum_i s_i A_i)^2` over all independent signs leaves exactly
  `\sum_i A_i^2`.

- Re-stated the Local-Green/Global-Red firewall: local normalization lemmas are
  green; global Born-rule ontology remains red without the imported
  representation assumptions of Theorem 6.

### v3.0.1 (2026-06-09)

- Improver hygiene pass (Stage 1). Part A rubric verified present (informal main result, why-care, related work, worked replay, falsifiability; the status/demotion box serves as the non-claims fence). Claim-typed all seven theorem headers.
- Resolved the two `[VERIFY record ids]` tags: reference [6] now lists the two companion papers by title with Zenodo records 20186523 and 20186809 (both verified HTTP 200 against the corpus registry).
- Fixed the Theorem 6 trace display typo ($\operatorname{Tr}(\rho,\Pi)$ comma → operator product).
- Lineage note: the "v007 Audit Note" below uses the long-form draft's internal numbering (its "Proposition 8.3" does not exist in this condensed version); the header version (v3.0 → v3.0.1) is canonical.
- Created sibling claim ledger `010_Born_Normalization_Claim_Ledger`; registered Paper 010 in `proof_ledger_20260609` (no genuine open obligations; PL-010-1 Lean hardening only).

v007 Audit Note

This version removes three overclaims:

1. $\ell^1$ weights alone do not force Hilbert space; the quadratic lift requires explicit representation assumptions.
2. Noncommuting lifted operators are not equivalent to observable order mismatch after descent; only the one-way implications in Proposition 8.3 are valid without faithfulness.
3. Decoherence removes phase-sensitive interference under a fixed pointer-basis restriction; it does not make arbitrary post-decoherence dynamics commutative.


GTOC / GTLA Compliance Note

*(Added 2026-07-17, GTOC/GTLA corpus cleanup pass)*

**Role:** Finite L¹ / Born import-boundary paper. Names and fences the normalization redundancy; draws the line between the free finite result and the imported uniqueness claim.

**Degree:** δ2 import-boundary

**Consumes:** Finite ℓ¹ weights, unit-sum normalization (Paper 000 / GTOC δ1), chosen Hilbert lift (imported), Haar-uniform phase assumption (imported), independence adapter (imported), Gleason/frame-function theorem (imported, Theorem 6).

**Produces:** Born normalization redundancy theorem (free, finite); ℓ¹-vs-ℓᵖ split (Theorem 2a=MECHANIZED/finite, 2b=STANDARD/imported real-analysis); Phase-averaged shadow theorem (Theorem 5, PROVEN CONDITIONAL); Born uniqueness = OracleNeeded firewall (Theorem 6).

**Does not produce:** Born rule derivation; Hilbert space from ℓ¹ weights alone; quantum dynamics; authority.

**Authority status:** None. Normalization redundancy does not confer authority.

**Declared imports:**

- Hilbert space (complex): `OracleNeeded (Q1)`
- Born uniqueness: `OracleNeeded (Gleason/frame-function), Theorem 6`
- Haar phase measure + independence adapter: `OracleNeeded, Theorem 5`
- Real-analysis ℓᵖ subadditivity (p>1): `STANDARD, Theorem 2b`

**OracleNeeded / Q-gated items:** Born uniqueness, Hilbert lift, Haar phase measure, independence adapter, quantum dynamics, continuum.

**GTLA boundary:** No terminalization or governance obligations in this paper. All GTLA obligations downstream.

**Mechanization status:** Theorem 2a: MECHANIZED (finite rational). Theorem 1/4/7: MECHANIZED (finite rational). Theorem 3: MECHANIZED (finite rational, row-sparsity kernel). Theorem 5: PROVEN CONDITIONAL (finite kernel only mechanized). Theorem 6: SCOPE FENCE + STANDARD citation.

**Remaining open obligations:** PL-010-1 (Lean hardening of continuous/full Theorem 5 remains conditional). Theorem 5 must not be upgraded to PROVEN without full Hilbert + Haar discharge.

<!-- claim-id-body-index:begin -->

Claim-ID body index (packaging)

| ID | Home |
|---|---|
| `C1` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `020:C1`) |
| `C2` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `020:C2`) |
| `C3` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `020:C3`) |
| `C4` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `020:C4`) |
| `C5` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `020:C5`) |
| `C6` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `020:C6`) |
| `C7` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `020:C7`) |
| `C8` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `020:C8`) |
| `C9` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `020:C9`) |
| `C10` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `020:C10`) |
| `Role` | [`../finite_quantum_mechanics/finite_quantum_mechanics_source_notes.md`](../finite_quantum_mechanics/finite_quantum_mechanics_source_notes.md) (§11.11) |
| `GTOC-8` | [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (ID `020:GTOC-8`) |

<!-- claim-id-body-index:end -->


## 2026-10-20 Supplement — Effect-Additive Born Representation & 4D Hermitian $\mathbb{Q}(i)$ Carrier (`FQ-GAP-BORN-UNIQUENESS-GLEASON`, `U1ChebyshevCauchyBridge.lean`)

1. **Effect-additive Born representation vs. bare ortho-frame non-uniqueness (`FQ-GAP-BORN-UNIQUENESS-GLEASON`):** Over $\mathbb{Q}^2$ and $\mathbb{Q}^3$, bare per-context frame additivity admits discontinuous $\{0,1\}$-valued countermodels (`lean4/GleasonRationalPlane.lean`, `no_quadratic_representation`) and non-quadratic degree-4 power laws (`lean4/QuarticRivalSeparation.lean`), whereas linearity across the operator effect cone uniquely forces the Frobenius trace form $f(E) = \operatorname{tr}(W E)$.
2. **4D Hermitian $\mathbb{Q}(i)$ Born carrier (`lean4/U1ChebyshevCauchyBridge.lean`, `HermitianMat2Qi`):** Extending the 3D real-symmetric matrix carrier ($b_i = 0$) by the imaginary Pauli-$Y$ basis matrix $\sigma_y = \begin{psmallmatrix}0 & -i \\ i & 0\end{psmallmatrix}$ yields the 4D $\mathbb{Q}$-vector space `HermitianMat2Qi` of $2\times 2$ Hermitian matrices over $\mathbb{Q}(i)$. Every $\mathbb{Q}$-linear effect functional $f : \mathrm{Herm}_2(\mathbb{Q}(i)) \to \mathbb{Q}$ is uniquely represented as $f(H) = \operatorname{tr}(W_f H)$ (`linear_functional_is_frobeniusTrace`, `frobeniusTrace_weight_unique`), $\sigma_y$ is Frobenius-orthogonal to the 3D real-symmetric subspace (`sigmaY_orthogonal_to_realSym`), and rank-1 Gaussian-rational kets $\psi, \phi \in \mathbb{Q}(i)^2$ satisfy $\det(|\psi\rangle\langle\psi|) = 0$ and $\operatorname{tr}(|\psi\rangle\langle\psi|\,|\phi\rangle\langle\phi|) = |\langle\psi|\phi\rangle|^2$ (`frobeniusTrace_rankOneKet_eq_inner_mod_sq`). `AuthorityEffect: None`.
