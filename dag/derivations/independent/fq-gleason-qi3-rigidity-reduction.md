Status: AI-drafted, awaiting human review.

# Nine-ray reduction of the remaining Gaussian-rational frame-function problem

AuthorityEffect: None.

This is a paper derivation for `FQ-GLEASON-QI3-FRAME-FUNCTIONS`, not a Lean
proof and not a resolution of its general signed or nonnegative classification.
The independent script `checks/independent/fq-gleason-qi3-tomography.py` checks
the symbolic reconstruction identities and stated algebraic controls. It does
not prove that every frame function has a quadratic representation.

## 1. Carrier and ray invariance

Put K = Q(i), V = K^3, and N(v) = v* v, using conjugate transpose `*`.
A weight-c function is a map f: V minus {0} -> Q satisfying
f(u) + f(v) + f(w) = c on every pairwise orthogonal nonzero triple.
No regularity, boundedness, positivity, or effect additivity is assumed.

Every nonzero v can be completed to such a frame over K without taking square
roots: choose a coordinate vector a outside K v, subtract
v (v* a)/N(v), and solve the two independent orthogonality equations for a
nonzero third vector. The coefficients remain in K. Positive definiteness
gives nonzero positive rational squared norms. Replacing v by lambda v in the
same completion, for any nonzero lambda in K, and subtracting the two frame
equations proves f(lambda v) = f(v). Thus the formulation on vectors already
implies that f is a function on rays.

## 2. Quadratic frame identity without unit-vector normalization

For any Hermitian matrix rho over K, define

    q_rho(v) = (v* rho v) / N(v).

The numerator is fixed by conjugation and hence lies in Q; its denominator is
a positive rational. For a frame, let U have columns u, v, w and let
D = diag(N(u), N(v), N(w)). Orthogonality says U* U = D. The columns are
linearly independent: taking the inner product with each column in a linear
relation kills the other two terms and leaves a nonzero squared norm. Thus U
is invertible and U D^(-1) U* = I. Consequently,

    q_rho(u) + q_rho(v) + q_rho(w)
      = tr(rho U D^(-1) U*) = tr(rho).

This identity applies to frames whose rays have no unit representative in K.

## 3. Unique candidate from nine specified rays

Let e_1, e_2, e_3 be the coordinate vectors, and use these nine rays:

    e_j (1 <= j <= 3),
    e_j + e_k and e_j + i e_k (1 <= j < k <= 3).

For any rational-valued f, set

    d_j = f(e_j),
    a_jk = f(e_j + e_k) - (d_j + d_k)/2,
    b_jk = (d_j + d_k)/2 - f(e_j + i e_k).

Define rho_f by diagonal entries d_j, upper entries a_jk + i b_jk, and lower
entries a_jk - i b_jk. This is a Hermitian matrix over K. Direct substitution
gives

    q_rho(e_j) = d_j,
    q_rho(e_j + e_k) = (d_j + d_k + 2 a_jk)/2,
    q_rho(e_j + i e_k) = (d_j + d_k - 2 b_jk)/2.

Therefore rho_f agrees with f on the nine rays, and these equations uniquely
determine it. If f has weight one, its coordinate frame equation gives
tr(rho_f) = d_1 + d_2 + d_3 = 1.

Define the residual g_f = f - q_rho_f. By Section 2, it is a weight-zero
function, and it vanishes on the nine rays. Conversely any weight-zero
rational-valued g vanishing on these rays gives a weight-one function
f = 1/3 + g. Its candidate is I/3. If g is nonzero, f is not quadratic:
uniqueness of the candidate would force f = q_(I/3) = 1/3.

It follows that **every signed weight-one frame function is quadratic if and
only if every weight-zero rational-valued frame function vanishing on these
nine rays is zero**. This is a reduction; the vanishing assertion is unproved.

## 4. The bounded residual is the exact nonnegative target

Every nonnegative weight-one function satisfies 0 <= f(v) <= 1: complete v
to a frame and use nonnegativity of its other two values.

For a fixed Hermitian rho with the coefficients above, the rational number

    C = sum_j |d_j| + sum_(j<k) (|a_jk| + |b_jk|)

bounds |q_rho(v)| for all nonzero v. Indeed each diagonal contribution is at
most |d_j| N(v). For each off-diagonal pair, its absolute contribution is at
most 2 (|a_jk| + |b_jk|) |v_j| |v_k|, which is at most
(|a_jk| + |b_jk|) N(v), by 2xy <= x^2 + y^2. Dividing their sum by N(v)
proves the bound. Thus a nonnegative f has |g_f(v)| <= 1 + C, a rational
global bound.

In the other direction, suppose |g(v)| <= B for every ray, where B is a
nonnegative rational, and g is weight zero and zero on the nine rays. Put

    epsilon = 1 / (3 (B + 1)),   F(v) = 1/3 + epsilon g(v).

Then F has weight one, is rational-valued, and

    0 < 1 / (3 (B + 1)) <= F(v)
      <= (2 B + 1) / (3 (B + 1)) < 2/3.

These inequalities also cover B = 0; in that case g is zero and F is constant.
For any nonzero g, F is nonquadratic because its nine-ray candidate is I/3
and epsilon is nonzero. A real finite bound can always be enlarged to a
nonnegative rational bound, so the choice of a rational B loses nothing.

Therefore **every nonnegative weight-one frame function is quadratic if and
only if every bounded weight-zero rational-valued frame function vanishing
on the nine rays is zero**. This bounded vanishing assertion is also unproved.
An unbounded signed counterexample alone would not refute the nonnegative
classification.

For completeness, a weight-zero function bounded below by m is bounded above
by -2m, using g(v) = -g(u) - g(w) in a completion. A bound above by M similarly
gives a bound below by -2M. A one-sided global bound therefore suffices here.

## 5. Why a finite rank computation is not the global vanishing theorem

Let E be the free Q-vector space on all K-rays and an extra symbol t. Quotient
by the span of `[u] + [v] + [w] - t` for every frame, obtaining U. A linear
functional L: U -> Q with L(t) = 1 is exactly a signed weight-one frame
function. The projector assignment

    T([v]) = v v* / N(v),   T(t) = I

is a well-defined surjection U -> Herm_3(K), by Section 2 and the nine-ray
reconstruction. Its target has Q-dimension nine.

If T is injective, the nondegenerate rational trace pairing expresses every
L as tr(rho T(-)), giving the quadratic formula. If T has a nonzero kernel
element k, choose a Q-linear functional L with L(k) != 0 by extending a
vector-space basis. Normalize it by

    L' = L + ((1 - L(t))/3) (tr composed with T).

Then L'(t) = 1 and L'(k) = L(k) != 0. Thus L' is a nonquadratic signed frame
function. In particular, the signed classification is equivalent to
injectivity of T. This basis-extension argument asserts no boundedness.

Membership in the relation span uses finite linear combinations. Hence a
proof of injectivity must account for every ray relation, even if each such
relation ultimately has a finite certificate. A finite ray set with only
quadratic solutions settles that finite set; it cannot by itself establish
injectivity on U or bounded residual vanishing on all rays.

## What is proved

The explicit nine-ray reconstruction and the two residual equivalences above
are established as a paper derivation with independent symbolic controls.
The universal quotient formulation gives an equivalent injectivity target
for the signed case. None of these paper arguments is Lean-verified here.

## What is assumed

The stated field, Hermitian form, and all-frame equations are supplied by the
target. The proofs use ordinary rational linear algebra and ordered real
arithmetic for the elementary absolute-value bounds. Section 5 uses algebraic
vector-space basis extension to separate a nonzero kernel element. These are
explicit mathematical proof methods, not added measurement axioms or effect
additivity. No continuum Gleason theorem is used.

## What is open

General signed and nonnegative rigidity, and a global nonquadratic
construction, remain unproved. The next decisive target is global vanishing
of the indicated residual space (bounded for the nonnegative case), or a
nonzero member with its global frame identity proved. A finite rank
calculation alone does not discharge this target.
