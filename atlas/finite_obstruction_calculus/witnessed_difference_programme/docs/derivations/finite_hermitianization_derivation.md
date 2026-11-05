# Finite Hermitianization of witnessed-difference carriers

**Status:** finite conditional derivation with core-only Lean and exact rational
replay.

**Purpose:** continue the derivation from primitive typed histories through
signed differences, tensor composition, dagger and observer geometry to an
actual complex algebraic carrier.  The construction identifies the precise new
datum: a checked complex structure.  It does not infer that datum from the
initial mark, the additive carrier, the dagger or positivity.

## 1. Input boundary

The preceding derivations supply the following chain after declarations have
been admitted:

1. a typed signature and its finite histories;
2. a contextual quotient for a declared family of questions;
3. the free commutative alternative carrier and its signed completion;
4. the algebraic tensor object for independent biadditive composition;
5. a supplied involution on generators and its additive extension;
6. a supplied additive observer
   \(L:A_{\mathbb Z}\to\mathbb Z^m\), with Gram form
   \(g_L(a,b)=L(a)^T L(b)\).

The observer theorem gives

\[
\operatorname{Rad}(g_L)=\ker L,
\qquad
A_{\mathbb Z}/\ker L\cong\operatorname{im}L.
\]

The realized quotient is torsion-free because it embeds in \(\mathbb Z^m\).
Its rationalization

\[
V=\bigl(A_{\mathbb Z}/\ker L\bigr)\otimes_{\mathbb Z}\mathbb Q
\]

therefore retains the realized distinctions.  Equivalently, one may work
directly in the rational span of \(\operatorname{im}L\).  The Gram form extends
uniquely to a rational symmetric positive-definite form on this realized
space.  If the unreduced presentation is retained, the same statement is
positive semidefinite and its radical remains the rationalized observer
kernel.

None of this supplies multiplication by \(i\).  That is the next admission.

## 2. Exact admission contract for complex structure

Let \(V\) be a finite-dimensional rational vector space with symmetric
bilinear form \(g\).  A **compatible complex-structure certificate** is a
rational linear map \(J:V\to V\) satisfying

\[
J^2=-I,
\qquad
g(Jx,Jy)=g(x,y).
\tag{2.1}
\]

Because \(J^{-1}=-J\), the second equation is equivalent to skew-adjointness:

\[
g(Jx,y)=-g(x,Jy).
\tag{2.2}
\]

For a matrix presentation with Gram matrix \(G\), the independent checker
tests

\[
J^2=-I,
\qquad
J^T G=-GJ,
\qquad
J^T GJ=G.
\tag{2.3}
\]

The last two equations are mathematically redundant once \(J^2=-I\) and one
of them hold, but checking both is a useful corruption detector.  If the form
is observer-induced, the checker also recomputes \(G=L^TL\) from the supplied
observer rather than accepting a detached Gram matrix.

Equation \(J^2=-I\) already implies that \(\dim_{\mathbb Q}V\) is even.  A
rank-one realized carrier therefore cannot pass this gate.  More generally,
the existence of some positive form does not select a particular \(J\).

## 3. The Gaussian-rational scalar action

Write

\[
\mathbb Q(i)=\{a+ib:a,b\in\mathbb Q\},
\quad
(a+ib)(c+id)=(ac-bd)+i(ad+bc),
\quad
\overline{a+ib}=a-ib.
\]

Given an admitted \(J\), define

\[
(a+ib)\cdot x=ax+bJx.
\tag{3.1}
\]

`GEN-WDP-62` **Finite conditional theorem (Gaussian-rational carrier).** If
\(J\) is rational linear and \(J^2=-I\), equation (3.1) makes \(V\) a vector
space over \(\mathbb Q(i)\).

### Proof

Additivity in the scalar and vector arguments follows from rational
linearity.  The unit law is

\[
(1+0i)\cdot x=x,
\]

and \(i\cdot x=Jx\).  For associativity, let
\(z=a+ib\), \(w=c+id\).  Then

\[
\begin{aligned}
z\cdot(w\cdot x)
 &=a(cx+dJx)+bJ(cx+dJx)\\
 &=acx+adJx+bcJx+bdJ^2x\\
 &=(ac-bd)x+(ad+bc)Jx\\
 &=(zw)\cdot x.
\end{aligned}
\]

This proves the scalar action without choosing coordinates or importing a
completion.  The corresponding Lean theorem is `complexSmul_mul`.

## 4. Hermitianization theorem

Define

\[
h(x,y)=g(x,y)+i\,g(Jx,y).
\tag{4.1}
\]

We use the convention that the first slot is conjugate linear and the second
slot is linear.

`GEN-WDP-63` **Finite conditional theorem (sharp Hermitianization).** Let
\((V,g,J)\) satisfy the admission contract of Section 2, with
\(g(x,x)\ge0\).  Then (4.1) is a positive-semidefinite Hermitian form over
\(\mathbb Q(i)\).  More precisely:

\[
\begin{aligned}
h(x_1+x_2,y)&=h(x_1,y)+h(x_2,y),\\
h(zx,y)&=\bar z\,h(x,y),\\
h(x,zy)&=z\,h(x,y),\\
h(y,x)&=\overline{h(x,y)},\\
h(x,x)&=g(x,x)\in\mathbb Q_{\ge0},\\
\operatorname{Rad}(h)&=\operatorname{Rad}(g).
\end{aligned}
\tag{4.2}
\]

If \(g\) is the observer Gram form, then

\[
h(x,x)=0
\iff
g(x,x)=0
\iff
Lx=0,
\tag{4.3}
\]

so quotienting by the Hermitian radical removes exactly the distinctions that
the supplied observer cannot see.

### Proof: isometry and conjugate symmetry

Skew-adjointness and \(J^2=-I\) imply

\[
g(Jx,Jy)=-g(x,J^2y)=g(x,y).
\]

By symmetry and skew-adjointness,

\[
g(Jy,x)=g(x,Jy)=-g(Jx,y).
\]

Thus

\[
h(y,x)=g(x,y)-i g(Jx,y)=\overline{h(x,y)}.
\]

### Proof: first-slot conjugate linearity

For \(z=a+ib\),

\[
\begin{aligned}
h(zx,y)
 &=g(ax+bJx,y)+i g(J(ax+bJx),y)\\
 &=a g(x,y)+b g(Jx,y)
   +i\bigl(a g(Jx,y)-b g(x,y)\bigr)\\
 &=(a-ib)\bigl(g(x,y)+i g(Jx,y)\bigr)\\
 &=\bar z\,h(x,y).
\end{aligned}
\]

The second-slot law follows directly from right bilinearity,
skew-adjointness and \(J\)-isometry, or from conjugate symmetry and the first
law.

### Proof: diagonal and radical

Symmetry and skew-adjointness give

\[
g(Jx,x)=g(x,Jx)=-g(Jx,x).
\]

The characteristic is zero, so \(g(Jx,x)=0\), hence
\(h(x,x)=g(x,x)\ge0\).

If \(x\in\operatorname{Rad}(h)\), taking real parts gives
\(g(x,y)=0\) for every \(y\).  Conversely, if \(g(x,-)=0\), then

\[
g(Jx,y)=-g(x,Jy)=0
\]

for every \(y\), so \(h(x,-)=0\).  This proves equality of radicals.  For an
observer Gram form, the sum-of-squares identity proves (4.3).

## 5. Constructive finite class

The two-dimensional rational plane provides the minimal faithful example.
For \(x=(x_0,x_1)\), set

\[
J(x_0,x_1)=(-x_1,x_0),
\qquad
g(x,y)=x_0y_0+x_1y_1.
\]

Then \(J^2=-I\), \(J^TG=-GJ\), and

\[
h(x,y)
=(x_0-ix_1)(y_0+iy_1).
\]

The map \((x_0,x_1)\mapsto x_0+ix_1\) is therefore an exact
\(\mathbb Q(i)\)-linear identification.  This is proved by
`plane_complex_action_is_multiplication` and
`plane_hermitian_is_standard` in Lean.

The replay uses a four-coordinate presentation with

\[
J=\begin{pmatrix}
0&-1&0&0\\
1&0&0&0\\
0&0&0&-1\\
0&0&1&0
\end{pmatrix},
\qquad
L=\begin{pmatrix}
1&0&0&0\\
0&1&0&0
\end{pmatrix}.
\]

Here the second complex coordinate is observer-blind.  The exact checker
verifies that its two-dimensional kernel is also the Hermitian radical.  On
the enumerated cube \(\{-1,0,1\}^4\), all 81 diagonal values are real and
nonnegative, and self-nullity agrees exactly with membership in \(\ker L\).
This enumeration is a replay fixture; the general equality is proved
symbolically in Lean.

## 6. Nonselection and refusal examples

### 6.1 Opposite orientation

The same plane form is compatible with both \(J\) and \(-J\).  They give

\[
h_J(e_0,e_1)=i,
\qquad
h_{-J}(e_0,e_1)=-i.
\]

Both pass positivity, skew-adjointness and \(J^2=-I\).  Therefore the positive
observer geometry does not select a complex orientation.  The selection of
\(J\), or an equivalence class of acceptable choices, belongs to the declared
mathematical/physical profile.

### 6.2 Incompatible observer geometry

Take

\[
G=\begin{pmatrix}1&0\\0&4\end{pmatrix},
\qquad
J=\begin{pmatrix}0&-1\\1&0\end{pmatrix}.
\]

Although \(J^2=-I\), one has \(J^TGJ\ne G\).  The replay refuses this package
rather than constructing a false Hermitian certificate.  A complex structure
and positive form are not enough separately; their compatibility is an
independent obligation.

### 6.3 Rank-one obstruction

The previous derivation proves that no rank-one integer endomorphism squares
to \(-I\).  Rationalization does not repair this: no \(q\in\mathbb Q\) has
\(q^2=-1\).  A realized rank-one observer carrier must be enlarged, paired
with another direction, or refused at the complex-structure gate.

## 7. Tensor compatibility

For Hermitianized carriers \(V,W\), the complex tensor product must impose the
balance relation

\[
(J_Vx)\otimes y=x\otimes(J_Wy).
\tag{7.1}
\]

The earlier complex-tensor balancing derivation proves the exact coefficient
quotient that enforces (7.1). As additional structure, admit multiplicativity
of the Hermitian pairing on pure tensors:

\[
h_{V\otimes W}(x\otimes u,y\otimes v)
=h_V(x,y)h_W(u,v),
\tag{7.2}
\]

There is a unique sesquilinear extension of this supplied rule: pure tensors
span the tensor product, so sesquilinearity determines its values on all finite
sums. The rule descends through the balance relations in both arguments; in
the first argument, (7.1) is respected because

\[
h_V(J_Vx,y)h_W(u,v)
=-i\,h_V(x,y)h_W(u,v)
=h_V(x,y)h_W(J_Wu,v).
\]

The second-argument check follows by Hermitian symmetry. Balance alone does
not select (7.2). For \(V=W=\mathbb Q(i)\), identify
\(V\otimes_{\mathbb Q(i)}W\) with \(\mathbb Q(i)\) by multiplication. Both
\(\overline z w\) and \(2\overline z w\) are positive Hermitian pairings on
this balanced tensor product, but the squared norm of \(1\otimes1\) is
respectively \(1\) and \(2\). The second form fails the supplied
multiplicativity rule for the usual unit pairings. Thus uniqueness here is
conditional on (7.2), not a consequence of balance alone.

For finite positive forms, positivity of the tensor form follows after
factoring each carrier by its radical and choosing a finite Gram realization.
This is an algebraic finite tensor construction.  It does not yet assert a
chosen physical subsystem factorization or an infinite completed tensor
product.

## 8. WDP, CODA, LGGR and projection-obstruction roles

- **LGGR** owns the separation between local generating data and a globally
  compatible realized carrier.  Hermitianization starts only after the
  relevant additive global carrier has been specified.
- **Projection Obstruction** identifies the information lost by the observer.
  The equality \(\operatorname{Rad}(h)=\ker L\) says that Hermitianization adds
  complex structure without reviving observer-erased distinctions.
- **WDP** binds the original task, the observer, \(J\), the form, the submitted
  witness and the derived certificate.  A result is conditional if any of
  those bindings change.
- **CODA/Prime** keeps proposal of \(J\), exact admission of (2.3), evaluation
  of the Hermitian laws and authorization of subsequent use as separate
  operations.
- **DDC** may search for or repair a candidate \(J\), but a decrease in a
  closure diagnostic cannot replace the exact equations in (2.3).

This is the first point in the foundational chain at which amplitude-like
complex cancellation is available on the constructed carrier.  It is not yet
a quantum theory.

## 9. Evidence and certificate format

The executable receipt binds:

```text
schema
problem_sha256
admission:
  dimension
  complex_square
  gram_symmetric
  skew_adjoint
  isometry
pairing:
  submitted exact Gaussian-rational values
  left and right scalar-law comparisons
  diagonal value
radical:
  blind report
  basis pairings
  enumerated self-null/kernel comparison
orientation_nonselection:
  J and -J comparison
incompatible_control:
  rejected anisotropic form
scope:
  derived
  not_derived
```

The checker reconstructs \(G=L^TL\), rechecks every matrix identity and
recomputes the receipt.  It does not trust a claimed Hermitian value.  Replay
requires no model call.

The core-only Lean module
[`FiniteHermitianization.lean`](../../lean4/WitnessedDifference/FiniteHermitianization.lean)
proves the Gaussian-rational multiplication laws, the scalar action,
conjugate symmetry, both scalar laws, positivity, radical equality, the
concrete plane and the orientation counterexample.  The Python reference is
[`code/hermitianization`](../../code/hermitianization), with adversarial tests in
[`test_finite_hermitianization.py`](../../code/unit_tests/test_finite_hermitianization.py).

## 10. Exact completion boundary

This derivation closes the finite algebraic step

\[
\text{observer Gram carrier}
+\text{ admitted }J
\longrightarrow
\text{finite }\mathbb Q(i)\text{-Hermitian carrier}.
\]

It leaves the following independent:

1. selection or empirical justification of \(J\);
2. extension of scalars from \(\mathbb Q(i)\) to \(\mathbb C\);
3. analytic norm completion where an infinite carrier requires it;
4. positive normalized state and effect cones;
5. the Born pairing and operational probability interpretation;
6. unitary or completely positive dynamics;
7. subsystem factorization, spacelike locality and Bell measurement choices;
8. continuum or field reconstruction.

The next derivation should therefore be a **finite state/effect cone and
readout admission theorem**: determine the exact extra conditions under which
the Hermitian carrier supports independently checked positive normalized
states, effects and a compositional probability pairing, while preserving the
observer radical and refusing a Born rule inferred from phase invariance
alone.
