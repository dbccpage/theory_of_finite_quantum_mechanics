# Landau quiz solutions and grading

GS-002 v2.0.0 candidate; reviewed 2026-10-02. Each numbered solution is
worth five points. Award three for the derivation and two for the stated
hypotheses, boundary, or counterexample. Numerical agreement alone is not a
proof of a quantified statement.

**1.** The four properties are exactly nonnegativity, definiteness, absolute
homogeneity, and the triangle inequality. The missing body condition is
boundedness. $B=\mathbb R^k$ has the listed four geometric properties, but
$j_B(x)=0$ for every $x$. A faithful finite-dimensional norm has a bounded
unit ball by norm equivalence. Conversely, if $j_B(x)=0$ for $x\ne0$, the
arbitrarily large points $x/\lambda$ belong to $B$ as $\lambda\downarrow0$,
contradicting boundedness. The source statement remains an imported result.

**2.** Choose a unit vector $u$. Invariance and transitivity give $j(v)=j(u)=c$
for all unit $v$. For nonzero $x$, write $x=\|x\|_2(x/\|x\|_2)$ and apply
positive homogeneity. Faithfulness and nonnegativity give $c>0$, and
homogeneity at zero gives $j(0)=0$. Convexity and subadditivity are unused.
In the plane take $a=u_1v_1+u_2v_2$ and $b=u_1v_2-u_2v_1$; expansion gives
$a^2+b^2=(u_1^2+u_2^2)(v_1^2+v_2^2)=1$ and $Ru=v$. The inner product
and unit sphere are declared; the argument does not construct them.

**3.** Absolute homogeneity gives $j(t)=|t|j(1)$, including negative $t$.
For the counterexample let $j(t)=2\max(t,0)+\max(-t,0)$. This is faithful,
convex, and positively homogeneous, but $j(1)=2\ne1=j(-1)$. The group
$\mathrm{SO}(1)=\{1\}$ imposes no sign symmetry. Absolute homogeneity
supplies precisely the missing condition.

**4.** Changing signs or permuting coordinates preserves both the sum and
maximum of absolute coordinates. Rotating $(1,0)$ to
$(1/\sqrt2,1/\sqrt2)$ changes the $\ell^1$ value from $1$ to $\sqrt2$
and the $\ell^\infty$ value from $1$ to $1/\sqrt2$. A smaller symmetry
group therefore leaves several norm choices.

**5.** Use $A(\omega)=(\sum_e\|\omega_e\|_2^2)^{1/2}$. It is a norm
and respects independent edge rotations. Two disjoint unit edge inputs
have individual values $1,1$ and combined value $\sqrt2$, violating
disjoint additivity. Two identical disjoint replicas likewise give
$\sqrt2 A(\omega)$ rather than $2A(\omega)$. Strong edgewise summability,
or the separately proved finite disjoint-support splitting hypotheses,
supplies the outer sum; local rotations do not.

**6.** Exchange symmetry makes $c_e$ constant on declared edge orbits. Unit
singleton normalization makes that constant one on each normalized type.
The triangle formulas are $2\min_e a_e$ and $\sqrt2\min_e b_e$. Take all
$a_e=1$ and all $b_e=\sqrt2$ to make both values $2$. The canonical
$2$ versus $\sqrt2$ comparison presupposes common unit normalization.

**7.** Replacing $\omega$ by $\omega+d_0\beta$ only translates the repair
variable. For any $\alpha$,
$J(\omega-d_0\alpha)\le J(\omega-\eta)+J(\eta-d_0\alpha)$.
Taking infima and exchanging $\omega,\eta$ yields the Lipschitz bound.
The normed quotient is zero exactly when $\omega\in\operatorname{im}d_0$,
because that image is closed in finite dimension. A candidate residual
cost before optimization need not equal the quotient norm.

**8.** Let $\eta=(0,(1,1),0)$ and $\alpha=((0,0),(1,0),(0,0))$.
Then $d_0\alpha=((1,0),(-1,0),(0,0))$ and $\omega-d_0\alpha=\eta$.
The mixed cost is $\sqrt2$ on the weight-one middle edge. If that edge is
stored backwards, traversal signs $(1,-1,1)$ and data
$((1,0),(0,-1),(0,0))$ still give $S=(1,1)$. Both data and incidence
must follow the same orientation convention.

**9.** For every representative of circulation $S$,
$\sum_e c_e j(\eta_e)\ge c_{\min}\sum_e j(\eta_e)\ge c_{\min}j(S)$.
Put $S$ on a cheapest edge for equality. Equal circulation permits that
representative because the difference has an exact path-sum repair.
A zero-weight edge lets every cycle class have zero cost, losing quotient
faithfulness. With all weights $-1$, put $tv,-tv,0$ on a triangle of zero
circulation; the cost tends to $-\infty$. Positive weights keep a norm.

**10.** Cauchy–Schwarz gives $\langle z,r\rangle\le c\|r\|_2$ for
$\|z\|_2\le c$; equality uses $z=cr/\|r\|_2$ when $r\ne0$ and $z=0$
at zero. The repair term is $-\langle d_0^*z,\alpha\rangle$, whose
infimum is finite only when $d_0^*z=0$. A feasible witness then has the
same pairing on all representatives and bounds each cost, proving weak
duality. Full-domain continuity of the finite norm supplies the usual
Fenchel–Rockafellar qualification for equality. On a signed Euclidean
cycle use $z_e=\varepsilon_e c_{\min}S/\|S\|_2$ for $S\ne0$, and zero
otherwise. Its pairing is $c_{\min}\|S\|_2$. Strong duality is not a
consequence of a successful solver run.

**11.** The affine residual class $\omega-\operatorname{im}d_0$ is closed.
Intersect it with a norm sublevel set containing $\omega$; the intersection
is nonempty and compact, so a residual minimizer exists. It has a preimage
repair. The dual intersection of edge balls and the adjoint kernel is also
nonempty compact, so the linear pairing attains its maximum. Adding a
constant vector on a connected component leaves $d_0\alpha$ unchanged;
vertex repair uniqueness requires extra gauge fixing and may still need
additional assumptions.

**12.** A repair subtracts $a=\alpha(1)-\alpha(0)$ from all three edge
vectors. Thus $\omega_0-\omega_1$ and $\omega_1-\omega_2$ are independent
invariants, and the dual constraint is $z_0+z_1+z_2=0$. The sum of edge
data changes by $-3a$, so it is not a quotient invariant. This graph has
two independent cycle directions and requires a different optimization
problem from a single directed cycle.

**13.** The quotient used here allows all edge cochains; $H^1$ restricts to $\ker d_1$ before quotienting. Nilpotency gives $d_1(\omega-d_0\alpha)=d_1\omega$.
The operator norm bounds $\Gamma$ by $\|d_1\|J(\omega-d_0\alpha)$ for
every $\alpha$; taking the infimum gives the result. For a counterexample
take $C^0=C^1=C^2=\mathbb R$, $d_0=d_1=I$, and $\omega=1$. The quotient
is zero, but $\|d_1\omega\|=1$, which changes under repairs and is not a
quotient invariant. Division by $\Phi=0$ is undefined. In the actual
complex, $\Phi=0$ implies $\Gamma=0$, but the ratio is still unused.

**14.** For scalar incidence $A$, weighted face triangle inequalities give
$\|Ah\|_{1,2,u}\le\sum_e(\sum_f u_f|A_{fe}|)\|h_e\|_2$.
Divide each coefficient by $c_e$ and maximize. A vector supported on a
maximizing edge attains the upper bound. The three ratios are $1/2,5/3,4/5$,
so the constant is $5/3$. Put a unit vector on edge 1: $J=3$ and
$\Gamma=1+4=5$. Common stalk dimension and scalar incidence are essential
to this column formula; a general block linear operator needs its own norm.

**15.** The quotient is $10^{12}\cdot10^{-9}=10^3$. A least-squares repair
can leave approximately $10^{-9}/3$ on each edge, below the coordinate
tolerance but with total weighted cost $10^3$. A zero witness has dual
value zero and gap $10^3$, so it cannot pass tolerance $10^{-7}$. Keep the
nonzero cycle witness. NaN values can evade ordinary comparisons; reject
them before auditing. An empty effective sample is vacuous. Infinite
tolerance accepts arbitrary finite errors. A finite declared tolerance
must govern feasibility and the gap consistently, including the smoothed
solver path. These are executable-contract issues, not counterexamples to
the exact mathematical cycle theorem.

**16.** General local rigidity has the stated prose proof; Lean supplies a
native-norm radial theorem under sphere constancy and a separate planar
rotation construction. General-$k$ transitivity and their full Euclidean
bridge are not mechanized here. Strong duality/attainment is a standard
finite-dimensional convex-analysis step; Lean mechanizes weak-duality
kernels. Cycle exactness has an anchored finite algebraic kernel, while
ordinary graph incidence is connected to it in prose. A floating-point
zero residual is a computed diagnostic, not an exact membership proof.
A historical Lean receipt records a past build and must match source hashes;
a fresh release build must reproduce its axiom census. Execution counts
record stored notebook outputs; fresh kernel replay must execute current
sources and assertions. Sequential Python cell replay is a narrower check.
Manifests and deterministic ZIP checks establish file custody only.
