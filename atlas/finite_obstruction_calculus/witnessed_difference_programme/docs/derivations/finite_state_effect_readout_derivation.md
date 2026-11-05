# Certified finite states, effects and readout

**Status:** finite conditional derivation with a core-only two-dimensional Lean
model and exact Gaussian-rational replay.

**Purpose:** determine what must be added to the finite Hermitian carrier before
it supports checked state/effect probabilities.  The result constructs one
explicit certificate class.  It does not infer the Born rule or the physical
meaning of a state from Hermitianization alone.

## 1. Inputs and exact scope

Assume the carrier is \(H=\mathbb Q(i)^n\) with its standard Hermitian
form. This presentation is an additional hypothesis: a positive-definite
form over \(\mathbb Q(i)\) need not have an orthonormal basis over that field.
Write \(A^\dagger\) for conjugate transpose and

\[
\|A\|_F^2=\operatorname{tr}(A^\dagger A)
=\sum_{jk}|A_{jk}|^2\in\mathbb Q_{\ge0}.
\]

The chosen presentation is part of the certificate profile.  The previous
Hermitianization theorem supplies a positive Hermitian form after an
observer and compatible complex structure have been specified. Identifying
that form with the standard one over the same exact field is a separate assumption.
This derivation adds a state/effect language and a readout.

The exact scalar field is \(\mathbb Q(i)\).  All matrices below are finite and
all checks use rational arithmetic.

## 2. Gram-factor certificate language

### 2.1 States

A **state-factor certificate** is a nonzero matrix \(B\).  Define

\[
t_B=\|B\|_F^2>0,
\qquad
\rho_B=\frac{B^\dagger B}{t_B}.
\tag{2.1}
\]

Then \(\rho_B\) is positive semidefinite and

\[
\operatorname{tr}\rho_B
=\frac{\operatorname{tr}(B^\dagger B)}{t_B}=1.
\]

The factor is a positive certificate: for every \(x\),

\[
x^\dagger\rho_Bx=\frac{\|Bx\|^2}{t_B}\ge0.
\]

### 2.2 Binary effects

A **binary effect-factor certificate** is a pair \((C,D)\) satisfying

\[
C^\dagger C+D^\dagger D=I.
\tag{2.2}
\]

Set

\[
E_C=C^\dagger C,
\qquad
I-E_C=D^\dagger D.
\]

Both matrices are positive semidefinite, so \(0\le E_C\le I\).  The rejected
factor \(D\) is part of the witness; the checker does not infer positivity of
the complement from floating-point eigenvalues.

For a finite outcome set, the same language uses factors \(C_o\) with

\[
\sum_o C_o^\dagger C_o=I.
\tag{2.3}
\]

The binary theorem below is the minimal nontrivial instance and the one
formalized in the core-only Lean spine.

### 2.3 Coverage boundary

The checker accepts supplied finite rectangular Gram factors over
\(\mathbb Q(i)\). A missing rational square root in a square Cholesky
factor does not establish a coverage gap for this language: for example,
the scalar matrix \((3)\) has rectangular factor \((1,1,1)^\top\).
This result verifies submitted factors; it does not supply a factor-search
algorithm or assert that some positive Gaussian-rational matrix lacks such
a factor. Extensions to other scalar fields require their own exact language.

## 3. Exact probability theorem

Define the accepted and rejected readouts by

\[
p_C(B)=\frac{\|CB^\dagger\|_F^2}{\|B\|_F^2},
\qquad
p_D(B)=\frac{\|DB^\dagger\|_F^2}{\|B\|_F^2}.
\tag{3.1}
\]

`GEN-WDP-64` **Finite conditional theorem (certified state/effect readout).**
For a state factor \(B\ne0\) and a complete binary effect factor \((C,D)\):

\[
\begin{aligned}
p_C(B)&=\operatorname{tr}(\rho_B E_C),\\
p_D(B)&=\operatorname{tr}(\rho_B(I-E_C)),\\
p_C(B)&\ge0,\quad p_D(B)\ge0,\\
p_C(B)+p_D(B)&=1.
\end{aligned}
\tag{3.2}
\]

Consequently \(0\le p_C(B),p_D(B)\le1\).  Every quantity is an exact rational
number.

### Proof: equality to the trace pairing

Cyclicity of the finite trace gives

\[
\begin{aligned}
\operatorname{tr}(\rho_BE_C)
 &=\frac{1}{t_B}\operatorname{tr}(B^\dagger B C^\dagger C)\\
 &=\frac{1}{t_B}\operatorname{tr}(B C^\dagger C B^\dagger)\\
 &=\frac{1}{t_B}\operatorname{tr}
   \bigl((CB^\dagger)^\dagger(CB^\dagger)\bigr)\\
 &=\frac{\|CB^\dagger\|_F^2}{t_B}.
\end{aligned}
\]

The same calculation applies to \(D\).

### Proof: normalization

Using (2.2),

\[
\begin{aligned}
\|CB^\dagger\|_F^2+\|DB^\dagger\|_F^2
 &=\operatorname{tr}\bigl(B(C^\dagger C+D^\dagger D)B^\dagger\bigr)\\
 &=\operatorname{tr}(BB^\dagger)\\
 &=\operatorname{tr}(B^\dagger B)=t_B.
\end{aligned}
\]

Division by the strictly positive \(t_B\) yields (3.2).  Positivity follows
directly from the sums of Gaussian-rational squares.

The finite-outcome version follows by replacing the two-term sum with (2.3).

## 4. Representation invariance and what it establishes

If \(u\in\mathbb Q(i)\) has \(|u|^2=1\), replacing \(B\) by \(uB\) leaves
\(B^\dagger B\), \(\rho_B\), and every probability unchanged.  More generally,
left multiplication of \(B\) by a certified unitary leaves the presented state
unchanged.  These are changes of factor witness, not changes of state.

The WDP transport requirement is therefore:

\[
B\sim B'
\Longrightarrow
\rho_B=\rho_{B'}
\Longrightarrow
p_C(B)=p_C(B')
\]

for the declared factor equivalence.  A hash match or a current numerical
answer is not enough; the actual density and effect maps must commute.

## 5. Readout nonselection

The trace pairing is now constructed and checked, but it has not been derived
as the uniquely physical rule.

For dimension \(n\ge1\) and \(0\le\lambda\le1\), define

\[
p_\lambda(\rho,E)
=\lambda\operatorname{tr}(\rho E)
 +(1-\lambda)\frac{\operatorname{tr}E}{n}.
\tag{5.1}
\]

`GEN-WDP-65` **Finite countermodel (positive normalized readout
nonselection).** For every finite POVM \((E_o)_o\), equation (5.1) is
nonnegative and normalized:

\[
\sum_o p_\lambda(\rho,E_o)=1.
\]

It is phase invariant and affine in both the state and effect arguments. For
\(n\ge2\), a sharp state/effect pair gives
\(p_\lambda=\lambda+(1-\lambda)/n\), which differs from the base value \(1\)
when \(\lambda\ne1\). At \(n=1\), every normalized state is \([1]\), so every
effect \([e]\) gives \(p_\lambda=e\) for all \(\lambda\); there is no readout
distinction in that dimension. In the dimension-two replay fixture,

\[
p_1(|0\rangle\!\langle0|,|0\rangle\!\langle0|)=1,
\qquad
p_{1/2}=\frac34.
\]

### Proof

The second term is the trace pairing with the maximally mixed state \(I/n\).
It is nonnegative on effects.  Since \(\sum_oE_o=I\),

\[
\sum_o\frac{\operatorname{tr}E_o}{n}
=\frac{\operatorname{tr}I}{n}=1.
\]

Convex combination with the base readout preserves positivity and
normalization for every \(n\ge1\). For a rank-one sharp pair,
\(\operatorname{tr}(\rho E)=\operatorname{tr}E=1\), giving the stated formula;
its difference from \(1\) is \(-(1-\lambda)(1-1/n)\). This vanishes for every
\(\lambda\) at \(n=1\), and only for \(\lambda=1\) at \(n\ge2\).

This countermodel does not claim a new fundamental probability law.  It proves
the logical point: positivity, normalization, phase invariance and finite
affinity do not by themselves select the undeformed trace pairing for the
declared state label.  Additional operational axioms such as calibration of
sharp preparations, noncontextuality assumptions, composition/tomography, or
a physical reconstruction theorem must carry that selection.

The earlier amplitude bridge gives a second nonselection control: quadratic
and quartic phase-blind readouts can agree on invariance while differing on
values.  Normalization requirements eliminate some such alternatives but not
the family (5.1).

## 6. Concrete exact fixture

The replay uses

\[
B=\begin{pmatrix}1&1\\0&0\end{pmatrix},
\quad
C=\begin{pmatrix}1&0\\0&0\end{pmatrix},
\quad
D=\begin{pmatrix}0&0\\0&1\end{pmatrix}.
\]

Then

\[
\rho_B=\frac12\begin{pmatrix}1&1\\1&1\end{pmatrix},
\quad
E_C=\begin{pmatrix}1&0\\0&0\end{pmatrix},
\quad
C^\dagger C+D^\dagger D=I,
\]

and the two exact outcomes have probability \(1/2\).  Multiplying \(B\) by
\((3+4i)/5\) leaves its density and readout unchanged.  The checker also
refuses a zero state factor and an incomplete effect pair.

## 7. Certificate and independent checker

The retained receipt contains:

```text
schema
problem_sha256
state:
  factor
  density
  trace
  positive denominator
effect:
  accepted and rejected Gram matrices
  exact identity sum
readout:
  submitted numerator
  accepted and rejected probabilities
  exact sum and trace comparison
phase_control
readout_nonselection
refusals
scope
```

The checker reconstructs every Gram matrix, density, complement and trace from
the submitted factors.  It refuses dimension changes, zero denominators,
incomplete effect factors and receipt mutation.  Replay requires no model
call.

The core-only Lean module
[`FiniteStateEffectReadout.lean`](../../lean4/WitnessedDifference/FiniteStateEffectReadout.lean)
proves the two-by-two Gaussian-rational trace/sum-of-squares identity, frame
partition, rational normalization and sharp basis example.  The executable
reference is in
[`code/state_effect_readout`](../../code/state_effect_readout), with focused tests in
[`test_finite_state_effect_readout.py`](../../code/unit_tests/test_finite_state_effect_readout.py).

## 8. Relation to Bell and quantum computation

This theorem supplies a finite operational interface that the earlier
Hermitian carrier lacked:

\[
\text{certified state}
+\text{ certified effect}
+\text{ admitted trace pairing}
\longrightarrow
\text{exact normalized outcome law}.
\]

For a Bell experiment, the remaining inputs are a declared tensor composite,
local complete effects for each setting, spacelike/commuting locality, and a
state on the composite.  Once those are admitted, the existing finite CHSH
theorems apply.  The present theorem does not derive those physical choices or
Bell's independence assumptions.

For quantum computation, the remaining inputs are certified unitary or
completely positive transformations, sequential composition, measurement
update, classical control, and a gate-generation/approximation statement over
the chosen scalar completion.  A finite exact \(\mathbb Q(i)\) gate set need
not exactly contain gates whose entries require other algebraic numbers, and
approximation requires a topology and error budget.

## 9. Completion boundary and next dependency

This derivation closes the Gram-factorable finite state/effect/readout class.
It leaves open:

1. a uniqueness or physical selection theorem for the trace/Born rule;
2. an implemented, checked factor-construction procedure for arbitrary positive inputs;
3. instrument updates and complete positivity under sequential composition;
4. tensor-local tomography and subsystem realization;
5. Bell-setting freedom, locality and empirical identification;
6. exact versus approximate universal quantum gates;
7. complex/analytic completion and continuum reconstruction;
8. institutional authorization of any real execution.

The next derivation should be a **finite process and computation theorem**:
construct certified Kraus/unitary transformations on these state/effect
objects, prove sequential and tensor composition, bind measurement updates to
the same outcome law, and identify the exact obstruction between a finite
Gaussian-rational gate language and universal complex quantum computation.
