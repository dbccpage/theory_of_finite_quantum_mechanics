# Landau quiz: derive the gauge, repair, and witness

GS-002 v2.0.0 candidate; reviewed 2026-10-02. These are written proof and
counterexample problems. Use the [study guide](study_guide.md) first and
open the [solutions](landau_quiz_solutions.md) after attempting each block.

Each problem is worth five points, for eighty total. A correct formula
without its hypotheses or derivation earns at most two. Retry any gap in
problems 2, 5, 10, 13, or 16 even if the total score is high.

## Local structure

**1. Faithfulness and the unit body.** Explain why a nonnegative, faithful,
absolutely homogeneous, subadditive gauge is a norm. In finite dimension,
identify the missing condition in “closed, convex, balanced, absorbing unit
body.” Give a counterexample when that condition is omitted.

**2. Radial rigidity.** Derive $j(x)=c\|x\|_2$, including $x=0$ and $c>0$,
from sphere transitivity, invariance, faithfulness, and positive homogeneity.
Which norm axioms are unused in this radial proof? For unit planar vectors
$u,v$, give $a,b$ such that $\begin{pmatrix}a&-b\\b&a\end{pmatrix}u=v$.

**3. The one-dimensional boundary.** Explain why absolute homogeneity forces
a faithful gauge on $\mathbb R$ to be $c|t|$. Construct a faithful convex
positively homogeneous gauge that is invariant under $\mathrm{SO}(1)$ but
does not have that form.

**4. A smaller symmetry group.** Show that both $\ell^1$ and $\ell^\infty$
on $\mathbb R^2$ are invariant under signed permutations. Use a 45-degree
rotation to show why this does not imply $\mathrm{SO}(2)$ invariance.

## Aggregation and quotient classes

**5. Separate local and outer symmetry.** Give a faithful convex homogeneous
aggregate that respects independent edge rotations but is not additive on
disjoint supports. Compare two unit edges and two disjoint identical replicas.
Name the assumption needed to obtain the outer $\ell^1$ sum.

**6. Normalize the comparison.** Explain what edge exchange symmetry fixes
and what singleton normalization fixes. With separate weights $a_e,b_e$,
derive the two triangle values. Choose positive weights making them equal.

**7. Quotient behavior.** Prove repair invariance of $\Phi$. Prove
$|\Phi([\omega])-\Phi([\eta])|\le J(\omega-\eta)$ for the same norm and
repair map. State when $\Phi([\omega])=0$.

**8. Construct a repair.** For the directed triangle and
$\omega=((1,0),(0,1),(0,0))$, weights $(3,1,2)$, construct a vertex repair
that puts all circulation on the cheapest edge. Recompute the signed
circulation if the middle edge is stored backwards with data $(0,-1)$.

## Cycle formula and duality

**9. Prove the bottleneck formula.** On one finite cycle with local norm $j$
and positive weights, prove $\Phi=c_{\min}j(S)$ by lower bound and achiever.
Explain what fails as a quotient norm if a weight is zero, and give a failure
example if negative weights are permitted.

**10. Build the dual.** Derive
$c\|r\|_2=\max_{\|z\|_2\le c}\langle z,r\rangle$ and the annihilator
constraint $d_0^*z=0$. Prove weak duality. State the qualification used for
strong duality, and construct an optimal weighted Euclidean cycle witness.

**11. Attainment and uniqueness.** Prove primal residual and dual maximum
attainment in the flat finite-dimensional problem. Explain why attainment
does not imply uniqueness of the vertex repair.

**12. More than one cycle.** For three parallel edges from $0$ to $1$,
identify two independent repair invariants and the dual divergence equation.
Explain why replacing the cycle circulation by $\omega_0+\omega_1+\omega_2$
does not extend the single-cycle formula.

## Closure and evidence

**13. Close the complex.** Distinguish $C^1/\operatorname{im}d_0$ from $H^1$ when faces are present. Prove the mixed closure bound. Give a one-dimensional
linear example in which $d_1d_0\ne0$, the quotient is zero, and the proposed
closure invariant is positive. Explain why $\Gamma/\Phi$ is then unavailable.

**14. Compute a sharp constant.** Derive the scalar-incidence column formula
for $\|d_1\|$ with common vector stalk dimension. For rows $(1,-1,0)$ and
$(0,1,-1)$, edge weights $(2,3,5)$ and face weights $(1,4)$, calculate the
constant and give an attaining cochain. Identify its scope restriction.

**15. Audit the numerical certificate.** A triangle has scalar circulation
$10^{-9}$, edge weights $10^{12}$, and tolerance $10^{-7}$. Can a small
least-squares coordinate residual justify discarding the cycle witness?
Compute the quotient and zero-witness gap. Explain why NaN gauge values,
an empty effective sample, infinite tolerance, and a gap above the declared
tolerance cannot support a passing certificate.

**16. Audit the proof claim.** Classify the evidence for general local
$\mathrm{SO}(k)$ rigidity, planar circle transitivity, strong duality,
cycle exactness, and floating-point zero residuals. Explain what a retained
Lean receipt and notebook execution counts establish, and what fresh release
checks still need to do. Explain why passing archive hashes establishes neither
the mathematical claims nor publication readiness.
