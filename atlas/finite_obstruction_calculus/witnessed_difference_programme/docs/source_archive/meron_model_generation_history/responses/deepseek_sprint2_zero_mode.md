# DeepSeek Sprint 2: Leading-Order Analysis of G^{(2)}_{4,1} and Zero Modes

**AuthorityEffect:** None.

## Result
At leading order in $r$:
\[
\boxed{A(p) = B(p) = \frac{1}{4} \quad \text{for every } p \in \{0, \pi/2, \pi, 3\pi/2\}}.
\]
Therefore:
\[
\lambda_+(p) = A(p) + |B(p)| = \frac{1}{2}, \qquad \lambda_-(p) = A(p) - |B(p)| = 0.
\]
$G^{(2)}_{4,1} \succeq 0$ at leading order in $r$, with a flat zero eigenvalue.

---

## Symmetry Protecting the Zero Mode at r = 0

At $r=0$, the shift:
\[
z_{0,x} \mapsto z_{0,x} - \epsilon, \qquad z_{1,x} \mapsto z_{1,x} + \epsilon
\]
leaves $X_{4,1}(z)$ invariant because $D_1 D_0 \mapsto D_1 e^{(\epsilon/2)\sum_x a_x} D_0 e^{-(\epsilon/2)\sum_x a_x} = D_1 D_0$ (the $a_x$ commute). This is a gauge redundancy of the source parametrization at $r=0$, forcing a zero eigenvalue in the temporal block for every spatial mode $p$.

---

## Status of the O(r) Correction

DeepSeek noted that whether the $O(r)$ correction lifts this zero upward ($\lambda_- > 0$, strict positivity) or downward ($\lambda_- < 0$, indefiniteness) remained to be calculated.

*(Subsequent exact rational calculation in `runs/gate_e_exact_counterexample.py` proved that the zero mode is lifted strictly downward: $\lambda_{\min} \sim -\frac{1}{9}r^4 < 0$, refuting finite-$M$ positive semidefiniteness).*
