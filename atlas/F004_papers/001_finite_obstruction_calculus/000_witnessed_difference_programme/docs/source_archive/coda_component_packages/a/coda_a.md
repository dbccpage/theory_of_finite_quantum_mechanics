<div align="center">

# CODA-A: Residuals of Projections, Kernels, and Cokernels

**Subtitle:** The Anomalon as a Typed Leftover

**Author:** Jeremy H. Carroll

**Date:** 2026-09-27

**Version:** v0.1.0 Pre-Print

**Status:** release candidate

**License:** Creative Commons Attribution 4.0 International (CC-BY-4.0)

</div>

## CODA Architecture & Layers

CODA stands for the Calculus of Obstruction, Descent, and Authorization. It is an exact, finite mathematical apparatus that enforces strict claim discipline by separating linear repairs, transport certificates, and finite descent from ungrounded authority claims. The system comprises eight operational layers governed by a single overarching authority architecture (GTLA).

| Layer | Abbreviation | Layer / Component Name & Scope |
| :---: | :--- | :--- |
| 1 | **FOC** | Finite Obstruction Calculus |
| 2 | **MUR** | Meta & Universal Re-Presentation (what presentations exist) |
| 3 | **CS** | Continuum Shadow (what continuum presentation may descend to a finite calculus system) |
| 4 | **CS_Q** | Continuum Shadow to Continuum Bridge (how continuum presentations descend) |
| 5 | **Q** | The Continuum (continuum presentations via completion and enclosure) |
| 6 | **A** | Anomalon (global residuals not removed and typed instead) |
| 7 | **OR** | Omniversal Re-Presentation (what presentations can transport) |
| 8 | **FDA** | Finite Descent Authority (what presentation may descend to evaluation and authorization) |
| 9 | **GTLA** | Layered Authority Architecture for CODA |

## Abstract

A linear correction $C$ applied to a vector $x$ leaves $\mathrm{residual}(C,x)=x-Cx$. That leftover is zero if and only if $Cx=x$. When $C$ is a projection, the leftover lies in the kernel of $C$, and applying the leftover map a second time does nothing. A linear map that commutes with two such corrections carries leftovers to leftovers. Two vectors have the same leftover if and only if they differ by a vector in the image of $C$; those leftover classes are the cokernel of the idempotent. A leftover is not a decision and not an origin story. A named toy constructible witness recorded in a companion Lean file demonstrates existence within the declared finite taxonomy without extra unproved axioms.

## Introduction

It is easy to treat a leftover as a verdict. You apply a correction, something remains, and you talk as if the remainder decided the original claim, or as if it explained where the difference came from. The remainder is a vector. This paper computes that vector.

Within the discrete cochain classification setting of this apparatus (Layer 9), "Anomalon" is a project-specific name strictly denoting the `ClosedResidual` terminal state ($d_1 x = 0$ with positive quotient distance against the declared repair subspace). It is not a synonym for every vector $x - Cx$, nor for every nonzero residual of an endomorphism or projection. This terminology makes no claim about the historical nuclear-physics use of "anomalon" or about particle physics.

A picture. Work in the plane, with coordinates written as columns. Let $C$ keep the first coordinate and kill the second:

$$
C\begin{pmatrix}a\\b\end{pmatrix}
=
\begin{pmatrix}a\\0\end{pmatrix}.
$$

Then $C\circ C=C$, so $C$ is a projection (Axler 2015; Jacobson 1985). The vector $(3,4)$ is sent to $(3,0)$. The leftover is

$$
(3,4)-(3,0)=(0,4).
$$

Applying $C$ to that leftover gives $(0,0)$. Applying the leftover map again to $(0,4)$ gives $(0,4)$. Stretching both coordinates by $2$ commutes with $C$ and stretches the leftover to $(0,8)$. Replacing $(3,4)$ by $(5,4)$ changes the vector by $(-2,0)$, which lies in the image of $C$; the leftover is still $(0,4)$. Replacing $(3,4)$ by $(3,5)$ changes the second coordinate, which $C$ cannot produce; the leftover becomes $(0,5)$.

The theory is refuted by:

1. **Mathematical counterexamples to Theorems A-T1–A-T7:**
   - a leftover that is nonzero while $Cx=x$, or vice versa (falsifying A-T1);
   - a projection whose leftover does not lie in the kernel (falsifying A-T2);
   - a projection whose leftover map fails to be idempotent on some vector (falsifying A-T3);
   - a projection with an image vector that is not fixed or a fixed vector not in its image (falsifying A-T4a);
   - a projection for which the direct-sum splitting $V = \operatorname{im} C \oplus \ker C$ fails (falsifying A-T4b);
   - a linear map that commutes with the two corrections but fails to carry leftovers to leftovers (falsifying A-T5);
   - two vectors that differ by an image vector of a projection and yet have different leftovers, or vice versa (falsifying A-T6); or
   - a linear map $f$ vanishing on $R = \ker(\pi)$ that fails to have a unique linear factorisation $g \circ \pi = f$ through the quotient $V/R$ with surjective $\pi$ (falsifying A-T7).

2. **Scope violations:**
   - a leftover treated as an authorization, rejection, or policy verdict; or
   - a leftover treated as an origin story or causal provenance of the difference it records.

## Notation

For A-T1–A-T7, $K$ is a field and $V,W$ are modules over $K$ (Axler 2015; Jacobson 1985). In the examples, $K=\mathbb{Q}$ and the modules are finite-dimensional coordinate spaces. In the companion, every matrix entry is an exact rational. A-T9 is restricted to finite rational coordinate spaces with their coordinate $\ell^1$ norm.

- $C:V\to V$ is a linear endomorphism: a linear correction of $V$.
- $D:W\to W$ is a linear correction of $W$.
- $T:V\to W$ is a linear map of carriers.
- $\mathrm{residual}(C,x):=x-Cx$.
- $C$ is a *projection* when $C\circ C=C$. That is the same as $C$ being idempotent as an endomorphism.
- $T$ *commutes* with $(C,D)$ when $T\circ C=D\circ T$.
- $\operatorname{im} C=\{Cy:y\in V\}$ is the image. $\ker C=\{v:Cv=0\}$ is the kernel.
- $V/\operatorname{im} C$ is the cokernel of $C$ as a map $V\to V$ (Mac Lane 1998).

A **leftover** of $C$ at $x$ is the vector $\mathrm{residual}(C,x)$. It is the output of a linear formula. It is not a policy.

## 1. Residual of a linear map

### Definition A-D1 — residual

For a linear endomorphism $C:V\to V$ and a vector $x\in V$, set

$$
\mathrm{residual}(C,x)
:=
x-Cx.
$$

The Lean definition is `Coda.A.residual`. Always, whether or not $C$ is a projection,

$$
x
=
Cx
+
\mathrm{residual}(C,x).
$$

That is an identity of vectors (Lean `Coda.A.decomposition`), not a claim about decisions.

### Theorem A-T1 — leftover zero if and only if fixed

$$
\mathrm{residual}(C,x)=0
\quad\text{if and only if}\quad
Cx=x.
$$

**Proof.** $x-Cx=0$ rearranges to $Cx=x$. This is Lean `Coda.A.residual_zero_iff`. □

In the picture, $C(3,0)=(3,0)$, so the leftover of $(3,0)$ is zero. $C(3,4)=(3,0)\neq(3,4)$, so the leftover of $(3,4)$ is not zero. The companion function `residual` returns the exact column $x-Cx$.

A non-instance, not a counterexample: if one writes "leftover zero" to mean "the first coordinate vanished," Theorem A-T1 is being misread. The theorem compares $Cx$ with $x$, not $Cx$ with $0$. For this $C$, $C(3,4)=(3,0)\neq 0$, and the leftover is $(0,4)$, not $(3,4)$.

## 2. When the correction is a projection

### Definition A-D2 — projection

A linear endomorphism $C:V\to V$ is a projection when $C\circ C=C$ (Axler 2015). The companion predicate `is_projection` returns true exactly on square matrices with $CC=C$.

Not every linear correction is a projection. The nilpotent example

$$
N
=
\begin{pmatrix}0&1\\0&0\end{pmatrix}
$$

satisfies $N^2=0\neq N$. For $x=(0,1)$ one has $Nx=(1,0)$ and leftover $(-1,1)$, and $N$ applied to that leftover is $(1,0)\neq 0$. Kernel and idempotence statements below therefore assume $C\circ C=C$.

### Theorem A-T2 — a projection eats the leftover

If $C\circ C=C$, then

$$
C\bigl(\mathrm{residual}(C,x)\bigr)=0.
$$

**Proof.** Linearity gives $C(x-Cx)=Cx-C(Cx)$. Idempotence gives $C(Cx)=Cx$, so the difference is zero. This is Lean `Coda.A.residual_in_kernel`. □

In the picture, $C(0,4)=(0,0)$. The leftover already has first coordinate zero, which is the only coordinate $C$ keeps.

### Theorem A-T3 — leftover of a leftover

If $C\circ C=C$, then

$$
\mathrm{residual}\bigl(C,\ \mathrm{residual}(C,x)\bigr)
=
\mathrm{residual}(C,x).
$$

**Proof.** Write $r=\mathrm{residual}(C,x)$. Then $\mathrm{residual}(C,r)=r-Cr$. Theorem A-T2 says $Cr=0$, so this is $r$. This is Lean `Coda.A.residual_idempotent`. □

Doing the leftover map twice does not produce a new leftover. On the nilpotent $N$ above, the leftover of $(-1,1)$ is $(-2,1)$, which is not $(-1,1)$. Idempotence of the leftover map uses that $C$ is a projection.

### Theorem A-T4 — image of a projection is the fixed set

If $C\circ C=C$, then $x\in\operatorname{im} C$ if and only if $Cx=x$.

**Proof.** If $x=Cy$, then $Cx=C(Cy)=Cy=x$. If $Cx=x$, then $x=Cx$, so $x$ lies in the image. This is Lean `Coda.A.range_fixed_iff`. □

Together with Theorem A-T1: for a projection, leftover zero, being fixed, and lying in the image are the same condition.

The identity $x=Cx+\mathrm{residual}(C,x)$ is then a splitting of $V$ as $\operatorname{im} C\oplus\ker C$ (Axler 2015). The first summand is the corrected part; the second is the leftover. The two summands meet only at $0$: if $v=Cy$ and $Cv=0$, then $v=C(Cy)=Cv=0$.

## 3. Moving leftovers with a linear map

Let $C:V\to V$ and $D:W\to W$ be linear corrections, and let $T:V\to W$ be linear.

### Theorem A-T5 — a commuting map transports leftovers

If $T\circ C=D\circ T$, then for every $x\in V$,

$$
T\bigl(\mathrm{residual}(C,x)\bigr)
=
\mathrm{residual}\bigl(D,\ Tx\bigr).
$$

**Proof.** $T(x-Cx)=Tx-T(Cx)=Tx-D(Tx)$. This is Lean `Coda.A.residual_transport`. □

The commuting hypothesis is used exactly once, as $T(Cx)=D(Tx)$. No further naturality is required.

In the picture, let $T$ be scaling by $2$ on the same plane, and let $D=C$. Scaling commutes with $C$:

$$
T\bigl(C(a,b)\bigr)=T(a,0)=(2a,0)=C(2a,2b)=C\bigl(T(a,b)\bigr).
$$

The leftover $(0,4)$ is sent to $(0,8)$, which is the leftover of $(6,8)$.

A non-instance. Let $S$ swap coordinates, $S(a,b)=(b,a)$, and keep $D=C$. Then $S(C(3,4))=S(3,0)=(0,3)$, while $C(S(3,4))=C(4,3)=(4,0)$. The two routes disagree, so Theorem A-T5 does not apply. Directly: $S$ of the leftover $(0,4)$ is $(4,0)$, while the leftover of $S(3,4)=(4,3)$ is $(0,3)$. Leftovers are not transported by an arbitrary linear map.

The companion predicate `maps_commute` checks $TC=DT$ on exact rational matrices. The notebooks compute both sides of Theorem A-T5 and compare them.

## 4. Leftover classes and the cokernel

Fix a projection $C:V\to V$. The cokernel of $C$, as an endomorphism, is the quotient module $V/\operatorname{im} C$ (Mac Lane 1998). Two vectors $x,y$ determine the same class in that quotient exactly when $x-y$ lies in the image.

### Theorem A-T6 — leftover classes match the cokernel

If $C\circ C=C$, then

$$
x-y\in\operatorname{im} C
\quad\text{if and only if}\quad
\mathrm{residual}(C,x)=\mathrm{residual}(C,y).
$$

**Proof.** By Theorem A-T4, $x-y$ lies in the image if and only if $C(x-y)=x-y$. Linearity rewrites the right-hand side as $Cx-Cy=x-y$, which rearranges to $x-Cx=y-Cy$. This is Lean `Coda.A.quotient_residual_iff`. □

In the picture, $(3,4)-(5,4)=(-2,0)=C(-2,0)$, and both leftovers are $(0,4)$. $(3,4)-(3,5)=(0,-1)$ does not lie in the image, and the leftovers are $(0,4)$ and $(0,5)$.

The representative $\mathrm{residual}(C,x)$ of the class of $x$ lies in $\ker C$ by Theorem A-T2. Different leftover vectors are different classes. Because $r = I-C$ vanishes on $\operatorname{im} C$, it induces a canonical representative map $s : V / \operatorname{im} C \to V$, defined by $s([x]) = x-Cx$, whose image lies in $\ker C$. If $q : V \to V / \operatorname{im} C$ is the quotient map, then $q \circ s = \mathrm{id}$. Thus the induced residual representative map is a section of $q$, and it identifies $V / \operatorname{im} C$ canonically with $\ker C$ (Lean `Coda.A.quotient_section`). In Lean 4, this structure is mechanized over additive commutative groups with additive homomorphisms (`Coda.A.LinearMap`), proving well-definedness and uniqueness without requiring field scalars for these projection identities.

### Theorem A-T7 — unique induced map on the quotient

Let $R\subseteq V$ be a submodule and $f:V\to W$ a linear map with $R\subseteq\ker f$. Then there exists a unique linear map $g:V/R\to W$ such that $g\circ\pi=f$, where $\pi:V\to V/R$ is the quotient map.

**Proof.** Existence is the ordinary factorisation of a linear map through a quotient on which it vanishes (Mac Lane 1998): $g(\pi(x))=f(x)$ is well-defined because $\pi(x)=\pi(x')$ implies $x-x'\in R\subseteq\ker f$, so $f(x)=f(x')$. Uniqueness: every class in $V/R$ is $\pi(x)$ for some $x$, so $g$ is determined on every class by $f(x)$. Linearity follows from $g([x]+[y])=f(x+y)=f(x)+f(y)$ and $g(a[x])=f(ax)=af(x)$. Lean `Coda.A.quotient_universal` establishes existence and uniqueness of the underlying function on a set quotient for additive groups. Its quotient carries no formalized scalar action, so the scalar-linearity assertion is proved here in prose; `quotient_universal_factor` checks finite rational matrix instances. □

Applied to $R=\operatorname{im} C$ and to a linear $f$ that vanishes on the image, the unique $g$ reads leftover classes. Theorem A-T6 says that those classes are the same data as the leftover vectors of a projection. In the computational companion, `quotient_universal_factor` requires $\pi$ to be surjective onto the declared quotient space ($\operatorname{rank}(\pi) = \operatorname{rows}(\pi)$) and verifies the absence of free parameters, preventing underdetermined non-unique factors.

The companion function `difference_in_image` decides $x-y\in\operatorname{im} C$ by an exact image-membership certificate, not by a floating-point rank.

## 5. A leftover is not a decision

The theorems above compute a vector, compare it with zero, place it in a kernel, transport it, and identify its class with a cokernel. None of those operations selects an action. In particular:

- leftover zero means $Cx=x$. It does not mean "accept $x$," "reject $x$," or "the original claim is settled";
- leftover nonzero means $Cx\neq x$. It does not mean "repair further," "halt," or "the original claim is false";
- a closed leftover in the sense of the discrete companion classifier of Section 6 is a vector whose next-stage image is zero and whose $\ell^1$ leftover against a declared repair subspace is positive (Carroll 2026, CODA-FOC). That is a diagnosis of a cochain. It is not a licence to treat the leftover as a source of the difference it records.

Residue is posterior to applying $C$. The formula $x-Cx$ mentions $C$ and $x$. It does not construct $x$, and it does not explain why $x$ was present before $C$ was applied. Calling the leftover an origin story confuses a difference computed after a correction with a generator of that difference.

### Scope fence A-S1 — residual data are not decision or provenance data

The value $\mathrm{residual}(C,x)$, the predicate $\mathrm{residual}(C,x)=0$, and the class of $x$ in $V/\operatorname{im} C$ do not inhabit a decision record, and they do not supply an origin of $x$.

**Explication.** Definition A-D1 is a vector. Theorem A-T1 is an equality of vectors. Theorem A-T6 is an equality of classes in a quotient. None of those mathematical types is a decision record (Carroll 2026, CODA-FDA). The formula $x-Cx$ is defined only after $C$ and $x$ are given, so it is not a construction of $x$. Definitions A-D1–A-D2 and Theorems A-T1–A-T7 supply no decision map and no origin map.

The Lean file `T03ToyAnomalonWitness.lean` formalizes a constructible pure-residual toy witness (`toy_anomalon_exists`) within the declared finite taxonomy. That witness is constructible by direct definition in the toy model; it is not an unproved foundational axiom and does not claim an independently constructed cofiber or physical particle.

## 5.1. Declared boundary and finite cokernel retention

### Declared commitment A-T8 — The Anomalon Boundary

A-T8 is a declared ontological commitment, not a theorem. Its formula is
$\mathrm{Real}_0=\text{Primitive Difference}\cup\text{Structure}$.
Here Primitive Difference names a nonzero declared obstruction, and Structure
names what persists, composes, stabilizes, or records it. This vocabulary supplies
no additional mathematical hypothesis or proof. The former theorem label was
withdrawn on 2026-09-23; no external implementation is offered as evidence.

### Theorem A-T9 — finite cokernel retention

Let $V=\mathbb Q^n$ and $W=\mathbb Q^m$ for finite nonnegative integers $n,m$,
with the coordinate $\ell^1$ norm on $V$. Let $d_0:W\to V$ be a rational linear
map and define $\Phi_1([x])=\min_{f\in W}\|x-d_0f\|_1$.
Let $C:V\to V$ be rational linear with $C^2=C$ and
$\operatorname{im}C=\operatorname{im}d_0$. Then:

1. $\Phi_1([x])>0\iff x\notin\operatorname{im}d_0\iff x-Cx\ne0$.
2. For every $f\in W$, $\mathrm{residual}(C,x-d_0f)=\mathrm{residual}(C,x)$
   and $\Phi_1([x-d_0f])=\Phi_1([x])$.
3. Under the isomorphism $\ker C\cong V/\operatorname{im}C$, the class of $x$
   corresponds to $x-Cx$.

If $d_1d_0=0$, $d_1x=0$, and $\Phi_1([x])>0$, this is a closed leftover in
the finite cochain classification of Section 6.

**Proof.** Minimizing the finite coordinate $\ell^1$ norm is a feasible rational
linear program bounded below by zero: introduce variables $t_i$ with
$-t_i\le(x-d_0f)_i\le t_i$ and minimize $\sum_i t_i$.
A finite rational linear program with a finite optimum attains that optimum at
a rational solution. Thus the minimum is zero exactly when $x=d_0f$ for some
$f\in\mathbb Q^m$; otherwise it is positive. By A-T4 and the equality of the
images, $x\in\operatorname{im}d_0$ exactly when $Cx=x$. For (2),
$Cd_0f=d_0f$ makes the residual of $d_0f$ vanish, and translation by $f$ only shifts the representative without altering the residual while reindexing all repairs in the minimization. Part (3) is A-T6. □

The earlier A-T9 was withdrawn on 2026-09-23 because it omitted
$\operatorname{im}C=\operatorname{im}d_0$ and claimed invariance under arbitrary
optimization. Its counterexample is $V=W=\mathbb Q$, $C=I$, $d_0=d_1=0$,
$x=1$: the quotient distance is $1$ but $x-Cx=0$. Also, $\ker C$ is related
to the quotient by an isomorphism, not a literal inclusion.

**Evidence scope.** `code/tests/test_a_t9_retention.py` checks this counterexample,
the running example, and seeded finite rational instances. A-T9 has a prose
proof and finite computational checks, with no single Lean declaration.
Register storage and administrative terminal routing are additional application
policies and are not conclusions of A-T9.

## 6. Computational companion

The companion module `code/coda_a_core.py` computes $\mathrm{residual}(C,x)$ on exact rational matrices, tests $CC=C$, tests $TC=DT$, and decides image membership of $x-y$ by an exact certificate. Arithmetic is exact rational; floats and booleans in scalar position raise `TypeError`.

On the running example,

$$
C=\begin{pmatrix}1&0\\0&0\end{pmatrix},\qquad
x=\begin{pmatrix}3\\4\end{pmatrix},\qquad
\mathrm{residual}(C,x)=\begin{pmatrix}0\\4\end{pmatrix}.
$$

Scaling by $2$ commutes with $C$ and sends the leftover to $(0,8)$. The swap map does not commute, and the two leftover computations disagree as in Section 3.

The same module also classifies a finite cochain leftover against a declared repair matrix $d_0$ and an optional next map $d_1$, using the exact $\ell^1$ quotient solver of the companion obstruction calculus (Carroll 2026, CODA-FOC). Prior to mathematical classification, the classifier computes the exact $\ell^1$ quotient distance (`LinearRepairProblem.quotient_l1_distance`) against the declared coboundary subspace; it never reports hardcoded or sentinel numbers. For administrative states (`RefusedClosure`, `LiftRequired`), `quotient_distance` is strictly absent (`None`). That classifier returns one of five labels: absorbed (quotient distance $0$), closed leftover ($d_1x=0$ and strictly positive distance), open leftover ($d_1x\neq 0$ and strictly positive distance), a pending-lift flag (distance `None`), or an explicit refusal (distance `None`). Those labels are a discrete diagnosis. They are not Theorems A-T1–A-T7, and they are not a decision. Substituting an $\ell^2$ projection leftover for the $\ell^1$ quotient, or substituting $x+Cx$ for $x-Cx$, is a fault the tests are written to kill.

Lean files in `lean4/`:

- `Foundations.lean` — factor and fiber foundation lemmas;
- `A.lean` — core mechanization of Theorems A-T1–A-T7, internal direct-sum splitting $V = \operatorname{im} C \oplus \ker C$ (`direct_sum_decomposition`, `direct_sum_unique`), and induced quotient section;
- `D01D02Records.lean` — records for a discrete leftover/absorbed/open taxonomy;
- `T01AnomalonTerminal.lean` — taxonomy properties of the anomalon terminal;
- `T02ResidualNonCreation.lean` — toy-level residual non-creation firewall;
- `T03ToyAnomalonWitness.lean` — constructible toy witness within the finite taxonomy;
- `Algebra.lean` — wraps reconstruction Theorems A-T1–A-T7, splitting, and quotient section;
- `Core.lean` — re-exports the files above and checks axioms.

The declarations and their precise scope are listed in `docs/lean_claim_map.md`. `lean4/axiom_report.txt` records the current named-declaration census, not an assertion that its results prove broader prose claims. Replay `lake build` and the entrypoint axiom queries with the pinned toolchain for the current sources. Standard kernel axioms such as `propext` and `Quot.sound` are distinguished from unproved custom axioms.

Adversarial tests include: leftover $(0,4)$ on the running projection; a nilpotent correction whose leftover is not killed; a commuting scale and a non-commuting swap; two vectors with the same leftover class and two with different classes; float rejection; and cochain condition $d_1 d_0 = 0$ validation.

## 7. Limitations

A-T1–A-T7 are dimension-independent algebraic statements; the Lean quotient result for A-T7 establishes the underlying unique function, while scalar linearity is established in prose. A-T9 and the Python quotient-distance solver require finite rational coordinate spaces with the coordinate $\ell^1$ norm. A-T8 is a commitment without a mathematical proof.

A cofiber of a closure functor is not constructed. Bicategories, higher simplicial duality, and an independent physical anomalon are not proved here. The toy witness in `T03ToyAnomalonWitness.lean` establishes existence only by construction within the finite toy taxonomy.

A leftover is a vector. Each additional statement uses the hypotheses displayed with it.

## References

1. S. Axler, *Linear Algebra Done Right*, 3rd ed., Springer, 2015. [doi:10.1007/978-3-319-11080-6](https://doi.org/10.1007/978-3-319-11080-6)
2. S. Mac Lane, *Categories for the Working Mathematician*, 2nd ed., Springer, 1998. [doi:10.1007/978-1-4757-4721-8](https://doi.org/10.1007/978-1-4757-4721-8)
3. J. H. Carroll, *The Finite Obstruction Calculus: Exact quotient diagnostics, dual witnesses, two-stage coherence, and transport (CODA-FOC)*, 2026. [versioned repository source](https://github.com/dbccpage/the_symbol_game/blob/44aff3782df7aa58a7ffc88e063a5643fd26a428/omega_engine_atlas/coda_atlas/F005_coda/foc/coda_foc.md)
4. J. H. Carroll, *Finite Descent Authority: Packets, Pipelines, and Seven Halt Guards: A proposal is not a decision (CODA-FDA)*, 2026. [versioned repository source](https://github.com/dbccpage/the_symbol_game/blob/44aff3782df7aa58a7ffc88e063a5643fd26a428/omega_engine_atlas/coda_atlas/F005_coda/fda/coda_fda.md)
5. N. Jacobson, *Basic Algebra I*, 2nd ed., W. H. Freeman, 1985. [https://www.worldcat.org/isbn/0716714809](https://www.worldcat.org/isbn/0716714809)
