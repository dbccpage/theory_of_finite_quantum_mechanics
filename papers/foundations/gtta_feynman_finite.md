# 032 Gtta Feynman Finite Shadow Histories

## GTOC Foundations — Quantum Contact Series (qm_032_gtta_feynman_finite_shadow_histories)

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

CODA-A-Feynman-1: Declared Continuum Path-Category Limit from Finite-Shadow Histories
===================================================================================

**Author:** Jeremy H. Carroll
**Version:** v0.1 (Pre-Print)
**Date:** 2026-06-17

> **Lead result.** A Feynman path integral, in this framework, is *not* a primitive: it is
> reconstructed only as the limit of **finite, replayable** sum-over-histories shadows, and the
> continuum kernel is **admitted as checked continuum evidence only when a declared topology and convergence certificate are
> supplied** — absent which the construction returns a typed residual, never a continuum object.
> The finite shadow ($K_\lambda$ = normalized finite sum over a finite history set) is the
> certified substrate; the continuum limit $K=\lim_\lambda K_\lambda$ is a *non-forced lift*, and
> the promotion "finite shadow $\Rightarrow$ continuum integral" is explicitly **refused** without
> the certificate.

**Why a researcher should care.** Anyone who writes "$\int \mathcal D x\, e^{iS/\hbar}$" is
invoking an object whose measure-theoretic existence is, for most actions, an open or false
analytic question. This paper isolates the part of the path integral that *is* finitely
constructible and replayable — the time-sliced, finite-carrier sum over histories — from the part
that must be *imported* under an external convergence oracle. For numerical path-integral practice
(lattice field theory, Monte-Carlo histories, transfer-matrix methods) this draws an explicit fence
between what a finite computation certifies and what it merely approximates, and it states exactly
what extra data (refinement maps, a topology, a convergence certificate) a continuum claim owes.

**Related work.** This sits between several literatures and differs from each in a precise way.
**(1) Lattice / time-sliced path integrals** (Feynman–Hibbs time-slicing; lattice field theory):
those *take* the continuum limit as the object of interest; here the finite slice is the certified
object and the limit is a fenced, non-forced lift. **(2) Transfer-matrix / Chapman–Kolmogorov
methods**: the finite propagator $K_\lambda$ is, up to the declared normalization $Z_\lambda$, a
transfer-matrix entry (the finite path-sum of [ENC-1128] / ****QM_111** / **QM_042**** (finite matrix-power/path-sum identity)), but this paper adds the CODA-A
closure-residual terminalizer on top.
**(3) Rigorous constructive / Euclidean path integrals** (Glimm–Jaffe; Wiener-measure imaginary-time
constructions): those *build* a measure; this paper does **not** — it refuses the continuum object
absent a supplied certificate and never claims a measure exists. **(4) Categorical / "infinity"
limits of finite approximations** (pro-objects, cofinal-system limits): the "infinity path category"
here is a declared limit of a refinement system, existing *only* when cofinality + coarse-graining
functors + a topology are declared, otherwise replaced by a finite shadow ledger. **(5) The GTLA
authority firewall** (QM_110 finite weighted transport; QM_090 continuum non-promotion; QM_081
finite descent): this paper is the path-integral instance of that firewall — it mints no authority
and imports the continuum.

Status Packet

```text
Claim:
  CODA-A wraps the CODA-CS finite-shadow Feynman construction as a residual-safe
  closure discipline over finite path shadows.

Authority:
  conditional theorem / derivation target.

Not claiming:
  QED derived,
  Standard Model derived,
  physics proven from CODA-CS,
  continuum-evidence admission without finite shadows.

First target:
  nonrelativistic finite time-sliced mechanical systems.
```

*Claim type of the Status Packet:* `[SCOPE FENCE]` — the "Not claiming" block is the
load-bearing fence; the "Claim" line is `[PROVEN, CONDITIONAL]` for the finite shadow and
`[PROVEN, CONDITIONAL + convergence oracle]` for the continuum limit, which terminalizes at
`OracleNeeded(Convergence)` absent the certificate (see the typed Theorem below).

**Notation.** This paper uses the GTLA tower vocabulary. `CODA-CS` = the tower's continuum-shadow
discipline (a continuum object is authorized only by certified finite shadows); `CODA-A` = the
tower's closure/transport-evidence layer (the residual-closure terminalizer wrapping a finite
construction); $\Lambda_F$ = the declared CODA-A closure discipline; `cofib` = the cofiber of the
closure unit (the typed residual); $q_\lambda$ = the finite-shadow projection of a candidate
continuum object; $\chi_{\lambda\lambda'}$ / $\rho_{\lambda\lambda'}$ = declared coarse-graining /
comparison maps under refinement; $\tau_{\mathrm{res}}$ = the residual terminalizer;
$\mathsf{Imported}/\mathsf{StructureDerived}/\mathsf{IsAuth}$ = the authority-firewall types. For the
canonical definitions see **QM_110** (finite weighted transport calculus synthesis), QM_090 (continuum non-promotion), and
the encyclopedia `quantum` layer view `paper_qm030`.

Status Overview

| Operation | Status |
|---|---|
| **finite combinatorics** | exact |
| **phase evaluation** | symbolic / interval / scoped |
| **refinement compatibility** | conditional |
| **continuum convergence** | oracle / certificate |
| **authority** | none |

Theorem

**CODA-A-Feynman-1.** `[PROVEN, CONDITIONAL]` — split by part below.

**(i)** `[PROVEN]` (finite shadow; MECHANIZED via ENC-1072 FEYNMAN-001). Given a finite time
partition λ, finite carrier X_λ, declared endpoints a,b, declared discrete Lagrangian L_λ,
declared normalization Z_λ, and declared numeric policy, the finite shadow propagator K_λ is
replayable by finite enumeration.

**(ii)** `[PROVEN, CONDITIONAL + convergence oracle]`. If the family {K_λ} is compatible under
declared refinement maps χ_{λλ′} and converges under declared topology Τ, then the limit K is
imported as a certified limit, not authorized as primitive. **The continuum object is not constructed
here; it is imported under the declared convergence certificate** — absent the certificate the
output is `OracleNeeded(Convergence)` and no continuum kernel is produced. The *gating* discipline
(no certificate ⇒ `OracleNeeded` / no continuum kernel; with certificate ⇒ promotion allowed) is
MECHANIZED as ENC-1078 (CONTINUUM-001); the analytic convergence of any *particular* family is the
imported oracle, not proven here.

**(iii)** `[DEFINITION / OPERATIONAL RULE]` (the CODA-A terminalizer). If CODA-A closure discipline Λ_F
absorbs the residual of this finite-shadow system, K terminalizes as ClosureAbsorbed /
Certificate(K). Otherwise the construction returns a typed residual. (This is the *definition* of
the closure terminalizer's output, not a separately proven theorem; the proven content is parts
(i)–(ii).)

CODA-A Wrapper `[DEFINITION / OPERATIONAL RULE]`

The Feynman construction is wrapped as a CODA-A closure attempt:

```text
K_candidate
  -> Close_{Lambda_F}(K_candidate)
  -> R_{Lambda_F}(K_candidate)
  -> tau_res(R_{Lambda_F})
```

where `Lambda_F` contains:

```text
finite time partitions lambda
finite path-shadow categories Path_lambda^L(a,b)
action-phase functors A_lambda
finite sum terminalizers Sigma_lambda
refinement comparison maps chi_lambda_lambda'
declared topology Tau
residual terminalizer tau_res
```

The CODA-A residual is:

```text
R_{Lambda_F}(K_candidate)
  = cofib(c_{Lambda_F,K}: K_candidate -> Close_{Lambda_F}(K_candidate))
```

Terminalization is:

| Condition | CODA-A terminal |
|---|---|
| All finite kernels replay, refinements commute, and convergence is certified | `ClosureAbsorbed` / `Certificate(K)` |
| A finite shadow cannot be replayed | `OpenResidual(NonReplayableShadow)` |
| Refinement compatibility fails | `OpenResidual(RefinementTear)` |
| Topology or convergence oracle is missing | `OracleNeeded(Convergence)` |
| Shadow family is not cofinal/exhaustive | `BudgetUnknown` |
| Lagrangian, carrier, normalization, or numeric policy is undeclared | `RefusedClosure` |

This is the CODA-A point: the continuum object is not trusted because it is elegant. It is trusted only if the closure residual vanishes through finite, replayable shadows.

CODA-CS Finite-Shadow Evidence Rule `[SCOPE FENCE]` (firewall; MECHANIZED via ENC-1078, ENC-1063)

CODA-CS does not grant authority to continuum objects. A continuum claim is eligible for this bounded evidence check only through declared finite shadows:

```text
q_lambda(X)
```

and by certified compatibility across refinement:

```text
lambda <= lambda'  implies  q_lambda(X) = chi_lambda_lambda'(q_lambda'(X))
```

where `chi_lambda_lambda'` is the declared coarse-graining or comparison map.

For this bounded replay, finite shadows are required evidence carriers rather than optional approximations. They are not an authority substrate.

Declared Continuum Path-Category Limit

Let `Part(T)` be the refinement category of finite partitions of the interval `[t_a,t_b]`.

```text
objects: finite partitions lambda
morphisms: lambda -> lambda' when lambda' refines lambda
```

For each partition `lambda`, define the finite path-shadow category:

```text
Path_lambda^L(a,b)
```

with:

```text
objects:
  finite histories gamma = (x_0,...,x_n), x_0=a, x_n=b

1-morphisms:
  declared finite path rewrites, refinements, or identity transports

k-morphisms:
  declared k-dimensional coherence witnesses between lower path rewrites
```

If no rewrite/coherence data is declared, `Path_lambda^L(a,b)` is the discrete finite category on the history set.

For every refinement `lambda <= lambda'`, declare a coarse-graining functor:

```text
rho_lambda_lambda' : Path_lambda'^L(a,b) -> Path_lambda^L(a,b)
```

The **infinity path category** is the CODA-A/CODA-CS shadow limit `[DEFINITION / SCOPE FENCE]` — it is a
*declared* limit, not a primitive, and does not exist without its declaration data:

```text
Path_lim^L(a,b) is not primitive.
It exists only when the refinement system, coarse-graining functors,
cofinality certificate, and limit construction are declared.
Otherwise CODA-A returns the finite shadow ledger NAbs(Path_infty^L).
```

When this limit is declared and certified, operationally, an object of `Path_lim^L(a,b)` is a compatible family:

```text
(gamma_lambda)_lambda
such that rho_lambda_lambda'(gamma_lambda') = gamma_lambda
```

for every declared refinement `lambda <= lambda'`.

If the limit is unavailable, CODA-A does not pretend the infinity path category exists. It returns the shadow attempt ledger:

```text
NAbs(Path_infty^L)
  = { (Path_lambda^L, rho_lambda, residual_lambda, tau_lambda) }_lambda
```

with global status `BudgetUnknown` unless the finite shadow family is proven cofinal.

The finite action-phase functor is:

```text
A_lambda : Path_lambda^L(a,b) -> Amp
A_lambda(gamma) = exp(i S_lambda(gamma) / hbar)
```

The finite propagator is the finite categorical sum:

```text
K_lambda(b,a)
  = Sigma_lambda(A_lambda)
```

The continuum propagator is not defined as an unguarded sum over a raw continuum. It is authorized as:

```text
K(b,a) = lim_lambda K_lambda(b,a)
```

only after CODA-A verifies finite replay, refinement compatibility, and declared convergence.

Finite Time-Sliced Mechanical System

Fix:

```text
lambda = (t_0 < t_1 < ... < t_n)
Delta t_k = t_{k+1} - t_k
```

A finite history from endpoint `a` to endpoint `b` is:

```text
gamma = (x_0, x_1, ..., x_n)
x_0 = a
x_n = b
```

Assume a finite declared position carrier for the shadow:

```text
X_lambda = {declared finite position states at slice lambda}
```

The finite carrier model is a lattice/shadow approximation,
not the usual continuum configuration space.

Then the finite history set is:

```text
Hist_lambda(a,b)
  = {gamma in X_lambda^(n+1) : gamma_0 = a, gamma_n = b}
```

This set is finite, so every sum below is replayable by enumeration.

Declared Discrete Action

Let `L` be the declared Lagrangian evaluator for adjacent time-slice data:

```text
L_lambda(x_k, x_{k+1}; Delta t_k)
```

The finite-shadow action is:

```text
S_lambda(gamma)
  = sum_{k=0}^{n-1} L_lambda(x_k, x_{k+1}; Delta t_k) Delta t_k
```

The phase weight is:

```text
A_lambda(gamma)
  = exp(i S_lambda(gamma) / hbar)
```

The finite-shadow propagator is:

```text
K_lambda(b,a)
  = Z_lambda^{-1}
    sum_{gamma in Hist_lambda(a,b)}
      exp(i S_lambda(gamma) / hbar)
```

where `Z_lambda` is a declared normalization factor.

Replayable Packet `[DEFINITION]`

The finite-shadow packet is:

```text
gttc<
  q<histories>
  shadow<time_slice lambda>
  endpoints<a,b>
  carrier<X_lambda>
  path<gamma:x_0..x_n>
  lagrangian<L_lambda>
  action<S_lambda=sum L Delta t>
  amp<exp(i S_lambda / hbar)>
  sum<K_lambda=sum amp over gamma:a->b>
  normalize<Z_lambda>
>
```

A host validator can replay:

1. Endpoint validity: `x_0 = a`, `x_n = b`.
2. Carrier membership: every `x_k in X_lambda`.
3. Slice validity: every `Delta t_k > 0`.
4. Lagrangian evaluation: every local `L_lambda(x_k, x_{k+1}; Delta t_k)` is declared.
5. Action evaluation: the finite sum equals `S_lambda(gamma)`.
6. Phase evaluation: the phase equals `exp(i S_lambda(gamma) / hbar)` under declared numeric policy.
7. History enumeration: every finite history is included exactly once.
8. Normalization: `Z_lambda` is the declared normalization for `lambda`.
9. Kernel assembly: `K_lambda(b,a)` equals the normalized finite sum.

Thus `K_lambda` is not certified by explanation. It is certified by finite replay.

Proof

*Typing.* Part 1 is `[PROVEN]` (finite, elementary; MECHANIZED via ENC-1072). Part 2 is
`[PROVEN, CONDITIONAL]` on the declared comparison maps. Part 3 is `[PROVEN, CONDITIONAL +
convergence oracle]` — its conclusion *imports* the limit object under the supplied certificate and
does **not** construct it (the non-promotion direction is MECHANIZED via ENC-1078). Part 4 is
`[DEFINITION / OPERATIONAL RULE]` — it records how the CODA-A terminalizer disposes of the residual,
not a separately proven theorem.

### Part 1: Finite Shadows Produce Replayable Propagators

Fix a finite time partition `lambda`, finite carrier `X_lambda`, endpoints `a,b in X_lambda`, declared discrete Lagrangian `L_lambda`, declared `hbar`, and declared normalization `Z_lambda`.

Since `X_lambda` is finite and `lambda` has finitely many time slices, the history set

```text
Hist_lambda(a,b)
```

is finite.

For every history `gamma in Hist_lambda(a,b)`, the action

```text
S_lambda(gamma)
  = sum_{k=0}^{n-1} L_lambda(x_k, x_{k+1}; Delta t_k) Delta t_k
```

is a finite sum of declared local evaluations. Therefore `S_lambda(gamma)` is replayable.

The amplitude

```text
A_lambda(gamma)
  = exp(i S_lambda(gamma) / hbar)
```

is replayable under the declared numeric policy for complex exponentiation.

The propagator

```text
K_lambda(b,a)
  = Z_lambda^{-1} sum_{gamma in Hist_lambda(a,b)} A_lambda(gamma)
```

is a finite normalized sum over a finite, declared, enumerable set. Therefore `K_lambda` is replayable.

This proves the first claim.

### Part 2: Refinement Compatibility Defines a CODA-CS System

Let `lambda <= lambda'` mean that `lambda'` refines `lambda`. Suppose the system declares comparison maps:

```text
chi_lambda_lambda' : K_lambda' -> K_lambda
```

or, more generally, maps that compare refined kernels to coarse kernels in the declared observation space.

The compatibility hypothesis states:

```text
chi_lambda_lambda'(K_lambda') = K_lambda
```

for every declared refinement pair `lambda <= lambda'`.

Therefore the family:

```text
{K_lambda}_lambda
```

forms a compatible finite-shadow family.

In CODA-CS terms, this is exactly the finite evidence required for a candidate continuum object to have coherent finite projections.

### Part 3: Declared Convergence Authorizes the Limit Object

Assume the packet declares a topology or convergence structure `Tau`, and assume:

```text
K_lambda -> K
```

under `Tau`.

By the CODA-CS evidence-admission rule, a continuum object is admitted when:

1. its finite shadows are declared,
2. those shadows are replayable,
3. those shadows are compatible under refinement,
4. the proposed limit exists under the declared topology.

Part 1 proves replayability of each `K_lambda`.
Part 2 gives refinement compatibility.
The convergence hypothesis gives the limit object `K`.

Therefore `K` is imported as the CODA-CS finite-shadow limit under convergence certificate.

### Part 4: CODA-A Residual Closure

Now place the construction inside CODA-A. The candidate continuum propagator `K_candidate` is subjected to the closure discipline `Lambda_F`.

The closure target `Close_{Lambda_F}(K_candidate)` is the compatible family of finite path-shadow kernels:

```text
{K_lambda}_lambda
```

equipped with the declared comparison maps `chi_lambda_lambda'` and convergence structure `Tau`.

If every finite `K_lambda` replays, every refinement comparison commutes, and the family converges to `K`, then the closure residual vanishes:

```text
R_{Lambda_F}(K) = cofib(c_{Lambda_F,K}) ~= 0
```

Therefore:

```text
tau_res(R_{Lambda_F}(K)) = ClosureAbsorbed
```

and `K` is authorized as the CODA-A limit object.

If any obligation fails, the residual is nonzero or ill-typed and CODA-A terminalizes it as `OpenResidual`, `BudgetUnknown`, `OracleNeeded`, or `RefusedClosure`. No failed branch authorizes the continuum propagator.

This proves CODA-A-Feynman-1.

### Numeric Policy and Exactness

Finite enumeration is exact at the combinatorial level. Amplitude evaluation is exact only if the declared phase policy is symbolic or interval-certified. Decimal evaluation terminalizes as scoped numerical evidence.

| Phase Policy | Terminal |
|---|---|
| exact symbolic root | `Certificate(K_lambda-symbolic)` |
| certified interval  | `Certificate(K_lambda-interval, epsilon)` |
| decimal float       | `ApproxQuantumReplay(epsilon)` |
| undeclared          | `NumericUndecidable` |

Free Particle Target

For the first concrete model, use the nonrelativistic free particle with mass `m`.

The continuum Lagrangian is:

```text
L(x, v) = (m / 2) v^2
```

The time-sliced discrete Lagrangian can be declared as:

```text
L_lambda(x_k, x_{k+1}; Delta t_k)
  = (m / 2) ((x_{k+1} - x_k) / Delta t_k)^2
```

Then:

```text
S_lambda(gamma)
  = sum_{k=0}^{n-1}
      (m / 2) ((x_{k+1} - x_k)^2 / Delta t_k)
```

and:

```text
K_lambda(b,a)
  = Z_lambda^{-1}
    sum_{gamma:a->b}
      exp((i / hbar) S_lambda(gamma))
```

This is the first useful CODA-A-Feynman bridge because all finite-shadow claims are locally replayable:

```text
finite carrier
finite histories
finite action sum
finite complex phase sum
declared refinement maps
declared convergence topology
```

### Worked example (exact algebraic finite shadow) `[WORKED EXAMPLE]`

To ensure finite replay is fully exact, declare weights in $\{\pm 1, \pm i\}$. Consider a discrete 2-slice random walk where $a=0, b=0$ and the midpoint $x_1 \in \{-1, 1\}$.
Let the phase be $+1$ for returning to origin and $i$ for moving away.

* History $(0, 1, 0)$: weight $i \cdot i = -1$
* History $(0, -1, 0)$: weight $i \cdot i = -1$
$K_\lambda(0,0) = -1 + (-1) = -2$.
This computation is completely exact algebraically (`Certificate(K_lambda-symbolic)`) and requires no transcendental functions or decimal approximations.

### Worked example (hand-replayable two-slice free particle) `[WORKED EXAMPLE]`

A fully numeric finite shadow a reader can check by hand. Declare:

```text
m = 1, hbar = 1, Z_lambda = 1
n = 2 slices, t_0 = 0 < t_1 = 1 < t_2 = 2, so Delta t_0 = Delta t_1 = 1
endpoints a = x_0 = 0, b = x_2 = 0
finite carrier of the midpoint x_1 in X_lambda = {-1, 0, 1}
```

There are exactly **three** finite histories γ = (0, x_1, 0), one per midpoint. With the free-particle
discrete action $S_\lambda(\gamma)=\tfrac{m}{2}\big[(x_1-x_0)^2/\Delta t_0+(x_2-x_1)^2/\Delta t_1\big]
=\tfrac12\big[x_1^2+x_1^2\big]=x_1^2$:

```text
x_1 = -1:  S = 1,  amp = exp(i)
x_1 =  0:  S = 0,  amp = exp(0) = 1
x_1 =  1:  S = 1,  amp = exp(i)
```

so the finite-shadow propagator is the finite sum
$$
K_\lambda(0,0)=Z_\lambda^{-1}\sum_{x_1\in\{-1,0,1\}}e^{iS_\lambda}=1+2\,e^{i}
= (1+2\cos 1)+2\,i\sin 1 \approx 2.0806 + 1.6829\,i .
$$
Every step — endpoint validity, carrier membership, the three actions, the three phases, the sum, the
trivial normalization — is replayed by finite enumeration over a 3-element set; nothing here invokes a
continuum, a measure, or a limit. This decimal evaluation terminalizes as scoped numerical evidence (`ApproxQuantumReplay(epsilon)`), not an exact algebraic certificate. Refining
`X_lambda` to `{-1,-0.5,0,0.5,1}` or adding a third slice yields a *different* finite shadow; whether
the family $\{K_\lambda\}$ converges as the mesh refines is **not** decided by this computation — it is
the `OracleNeeded(Convergence)` obligation, and is exactly the lift this paper refuses to take for free.

**Reproducibility pointer.** The finite path-sum / Feynman-shadow replay underlying part (i) is
mechanized as **ENC-1072** (FEYNMAN-001 / LT-R, MECHANIZED, axiom-audited) — Lean
`QM.FiniteFeynmanShadow` and `FinitePathSumReplay` — and the
finite-shadow $\not\Rightarrow$ continuum non-promotion of part (ii) is **ENC-1078** (CONTINUUM-001 /
LT-S, MECHANIZED) — Lean `QM.ContinuumNonPromotion`. The finite
path-sum = transfer-matrix identity is **ENC-1128** (**QM_111** / **QM_042**). See the encyclopedia `quantum` view
`paper_qm030`.

**Falsifiability.** This construction fails if (1) some finite shadow $K_\lambda$ cannot be replayed by
finite enumeration over the declared finite carrier (it is a finite normalized sum, so failure means an
undeclared/ill-typed packet); (2) a refined shadow does *not* coarse-grain to the declared coarse
kernel, $\chi_{\lambda\lambda'}(K_{\lambda'})\ne K_\lambda$ (a `RefinementTear`); or (3) someone exhibits
a continuum path-integral object constructed from a finite-shadow family **without** a declared topology
and convergence certificate — which would refute the CODA-CS non-promotion fence (ENC-1078). It is **not**
falsified by the absence of a continuum limit: that absence is the typed `OracleNeeded` terminal, not an
error.

Terminalization `[DEFINITION / OPERATIONAL RULE]`

The finite-shadow path-sum packet terminalizes as:

*Note: A finite-shadow validator will only be vendored into the publication tree once the numeric policy for transcendental phase evaluation is fully explicit and typed.*

| Status | Condition |
|---|---|
| `Certificate(K_lambda)` | Finite history enumeration, action evaluation, phase evaluation, normalization, and kernel sum replay successfully. |
| `Repair` | Packet has fixable endpoint, carrier, shape, or normalization mismatch. |
| `Refusal` | Lagrangian, carrier, topology, numeric policy, or refinement law is undeclared. |
| `OracleNeeded` | Continuum convergence, analytic closed form, or external theorem proof is required but not available in-process. |
| `Certificate(K)` | Compatibility and convergence are certified under declared topology, authorizing the CODA-CS finite-shadow limit and CODA-A closure-absorbed object. |
| `OpenResidual(RefinementTear)` | A refined shadow does not coarse-grain to the declared coarse kernel. |
| `BudgetUnknown` | The finite shadow family is not proven cofinal/exhaustive. |
| `RefusedClosure` | Required CODA-A closure data is undeclared or ill-typed. |

What This Does Not Prove

This theorem does not prove:

```text
QED,
the Standard Model,
physical correctness of a chosen Lagrangian,
existence of every continuum path integral,
continuum-evidence admission without finite shadows,
convergence without a declared topology,
compatibility without declared refinement maps.
```

The theorem proves only the CODA-CS evidence-admission shape:

```text
finite histories first
finite action phases second
finite propagator by replayable sum third
continuum propagator only by compatible convergent limit
```

In particular, **"finite shadow ⇒ continuum integral" is not a theorem of this paper** — the
finite shadow is certified, the continuum is a *non-forced lift* gated by an external convergence
oracle (ENC-1078). And per the GTLA firewall, $\mathsf{StructureDerived}\not\Rightarrow\mathsf{IsAuth}$:
no part of this construction mints tower authority; the continuum object, when authorized, is
**imported** under its certificate, never derived from the finite shadows alone (ENC-1063).

Implementation Sketch `[DEFINITION / OPERATIONAL RULE]` (type signatures only; not load-bearing)

```rust
pub struct TimeSlice {
    pub t0: Rational,
    pub t1: Rational,
}

pub struct TimePartition {
    pub slices: Vec<TimeSlice>,
}

pub struct FiniteCarrier<X> {
    pub states: Vec<X>,
}

pub struct History<X> {
    pub points: Vec<X>,
}

pub trait DiscreteLagrangian<X> {
    fn eval(&self, x0: &X, x1: &X, dt: Rational) -> Result<Rational, LagrangianError>
}

pub struct FeynmanShadowPacket<X, L> {
    pub partition: TimePartition,
    pub carrier: FiniteCarrier<X>,
    pub start: X,
    pub end: X,
    pub lagrangian: L,
    pub hbar: Rational,
    pub normalization: ComplexRational,
    pub numeric_policy: NumericPolicy,
}

pub struct FinitePropagator {
    pub value: ComplexDecimal,
    pub history_count: usize,
    pub certificate: ReplayCertificate,
}

pub trait RefinementCompatible {
    fn check_refinement(&self, coarse: &Self, map: &RefinementMap) -> ValidationReport
}

pub trait DeclaredConvergence {
    type Limit
    fn check_convergence(
        family: &[FinitePropagator],
        topology: &TopologyId,
    ) -> Result<Self, OracleNeeded>
}

pub struct FinitePathCategory<X> {
    pub partition: TimePartition,
    pub objects: Vec<History<X>>,
    pub morphisms: Vec<PathMorphism>,
    pub coherence: Vec<PathCoherenceCell>,
}

pub struct InfinityPathCategory<X> {
    pub index: RefinementCategory,
    pub finite_shadows: Vec<FinitePathCategory<X>>,
    pub coarse_grainings: Vec<CoarseGrainingFunctor>,
    pub cofinality_certificate: Option<CofinalityCertificate>,
}

pub enum FeynmanResidual {
    NonReplayableShadow(PacketId),
    RefinementTear(RefinementPair),
    MissingTopology,
    DivergentFamily,
    NonCofinalShadowFamily,
    RefusedClosure(RefusalReason),
}
```

Validator outline:

```text
parse packet
check finite carrier
enumerate Hist_lambda(a,b)
evaluate S_lambda(gamma)
evaluate exp(i S_lambda / hbar)
sum amplitudes
apply Z_lambda
emit Certificate(K_lambda)
if refinement family supplied:
  check chi_lambda_lambda'(K_lambda') = K_lambda
if convergence oracle supplied:
  certify K as CODA-CS finite-shadow limit
wrap in Lambda_F:
  if residual vanishes:
    emit ClosureAbsorbed / Certificate(K)
  else:
    emit typed CODA-A residual
```

Final Line

Feynman is not the starting authority. In CODA-A, the path-integral form appears when finite compatible histories are terminalized through an action-phase observer, checked as an infinity path category of finite shadows, and then admitted, if possible, as checked evidence for a declared continuum limit. No such admission constructs authority.


Changelog

Version Note: v1.0-audit (2026-06-21):** pipeline pass
Version Note: v1.0-hygiene:** standard release cleanup

<!-- claim-id-body-index:begin -->

Claim-ID body index (packaging)

| ID | Home |
|---|---|
| `QM-032-C1` | sibling `qm_032_gtta_feynman_finite_shadow_histories_claim_ledger.md` |
| `QM-032-C2` | sibling `qm_032_gtta_feynman_finite_shadow_histories_claim_ledger.md` |
| `QM-032-C3` | sibling `qm_032_gtta_feynman_finite_shadow_histories_claim_ledger.md` |
| `QM-032-C4` | sibling `qm_032_gtta_feynman_finite_shadow_histories_claim_ledger.md` |
| `QM-032-C5` | sibling `qm_032_gtta_feynman_finite_shadow_histories_claim_ledger.md` |
| `QM-032-C6` | sibling `qm_032_gtta_feynman_finite_shadow_histories_claim_ledger.md` |
| `QM-032-C7` | sibling `qm_032_gtta_feynman_finite_shadow_histories_claim_ledger.md` |
| `QM-032-C8` | sibling `qm_032_gtta_feynman_finite_shadow_histories_claim_ledger.md` |
| `QM-032-C9` | sibling `qm_032_gtta_feynman_finite_shadow_histories_claim_ledger.md` |
| `QM-032-C10` | sibling `qm_032_gtta_feynman_finite_shadow_histories_claim_ledger.md` |
| `QM-032-C11` | sibling `qm_032_gtta_feynman_finite_shadow_histories_claim_ledger.md` |
| `QM-032-C12` | sibling `qm_032_gtta_feynman_finite_shadow_histories_claim_ledger.md` |
| `QM-032-C13` | sibling `qm_032_gtta_feynman_finite_shadow_histories_claim_ledger.md` |
| `QM-032-C14` | sibling `qm_032_gtta_feynman_finite_shadow_histories_claim_ledger.md` |
| `QM-032-C15` | sibling `qm_032_gtta_feynman_finite_shadow_histories_claim_ledger.md` |

<!-- claim-id-body-index:end -->
