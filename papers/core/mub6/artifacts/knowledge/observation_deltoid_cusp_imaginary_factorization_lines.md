# Zero-Residual Factoring Lines and Deficit Separation at Deltoid Boundary Cusps

Type: observation
Confidence: high
Source: Falser report strategy_L02_N04 (Level 2); Candidate strategy_L03_N03 and Falser report strategy_L03_N03 (Level 3); Candidate strategy_L04_N00 (Level 4)
Relevant to: Deltoid cusp desingularization, Puiseux collars, and Szöllősi variety B_6(theta).

## Statement
At the three singular boundary cusps of the Szöllősi parameter variety on $\mathbb{T}^4$, the imaginary defining constraint:
$$\operatorname{Im}(\phi(\alpha, \beta)) = \sin\alpha + \sin\beta - \sin(\alpha+\beta)$$
admits an exact trigonometric product factorization:
$$\operatorname{Im}(\phi(\alpha, \beta)) = 4 \sin\left(\frac{\alpha}{2}\right) \sin\left(\frac{\beta}{2}\right) \sin\left(\frac{\alpha+\beta}{2}\right).$$
Consequently:
1. $\operatorname{Im}(\phi(\alpha, \beta))$ vanishes identically to all orders along three continuous lines passing directly through the cusp $(0, 0)$: $\alpha = 0$, $\beta = 0$, and $\alpha + \beta = 0$.
2. The leading cubic Taylor expansion $\frac{1}{2}\alpha\beta(\alpha+\beta)$ changes sign across quadrants (satisfying $C(-\alpha, -\beta) = -C(\alpha, \beta)$) and evaluates to zero on the three lines, providing zero collar lower bound.
3. Because $\operatorname{range}(\operatorname{Re}\phi) = [-1.5, 3.0]$ on $\mathbb{T}^2$, at the cusp point $\phi_1 = 3$, the Szöllősi defining relation $\phi_1 + \phi_2 = 0$ requires $\operatorname{Re}\phi_2 = -3$. This lies strictly outside the range of $\operatorname{Re}\phi$ with a positive deficit of $1.5$ ($|-1.5 - (-3)| = 1.5$), proving that the candidate variety does not intersect the cusps.

## Evidence
1. **Trigonometric Identity**:
   Using sum-to-product identities:
   $$\sin\alpha + \sin\beta = 2 \sin\left(\frac{\alpha+\beta}{2}\right) \cos\left(\frac{\alpha-\beta}{2}\right),$$
   $$\sin(\alpha+\beta) = 2 \sin\left(\frac{\alpha+\beta}{2}\right) \cos\left(\frac{\alpha+\beta}{2}\right).$$
   Subtracting gives:
   $$2 \sin\left(\frac{\alpha+\beta}{2}\right) \left[ \cos\left(\frac{\alpha-\beta}{2}\right) - \cos\left(\frac{\alpha+\beta}{2}\right) \right] = 4 \sin\left(\frac{\alpha}{2}\right) \sin\left(\frac{\beta}{2}\right) \sin\left(\frac{\alpha+\beta}{2}\right).$$
   Symbolic differentiation and simplification in SymPy confirmed identity residual is identically zero.
2. **Evaluation on Factoring Lines**:
   Evaluating $\operatorname{Im}(\phi(\alpha, 0)) = \sin\alpha + 0 - \sin\alpha = 0$ identically for all $\alpha$. The infimum of $|\operatorname{Im}(\phi)|$ on any deleted collar neighborhood $B((0, 0), \epsilon) \setminus \{(0, 0)\}$ is exactly $0$.
3. **Deficit Computation (Level 3 Formalization)**:
   Critical points of $\operatorname{Re}\phi(\alpha, \beta) = \cos\alpha + \cos\beta + \cos(\alpha+\beta)$ on $[0, 2\pi)^2$ occur at $(\alpha, \beta) \in \{(0, 0), (2\pi/3, 2\pi/3), (4\pi/3, 4\pi/3), (\pi, \pi)\}$, with values in $\{-1.5, 3.0\}$.
   At cusp $\phi_1 = 3 + 0i$, $\phi_1 + \phi_2 = 0 \implies \phi_2 = -3$. But $\min \operatorname{Re}\phi = -1.5$, leaving a minimum deficit $\min \operatorname{Re}(\phi_1 + \phi_2) = 3.0 - 1.5 = 1.5 > 0$.

## Implications
1. Claims that a third-order cubic Taylor expansion $\frac{1}{2}\alpha\beta(\alpha+\beta)$ provides a collar lower bound isolating the deltoid cusps are mathematically false.
2. Because $\phi_1 + \phi_2 = 0$ requires $\operatorname{Re}\phi_2 = -3$, the candidate variety is detached from the cusps by an exact real deficit of $1.5$, establishing that parameter Jacobian rank collapse and cusp collisions do not occur on the feasible variety.
3. However, as established in Falser report L03_N03, proving deltoid cusp detachment only establishes that the variety avoids boundary cusps; it provides zero evidence that candidate quartets do not exist on the smooth, regular 120-variable arc of $B_6(\theta)$.

## Claim Hygiene Summary
- **What it supports**: Supports that $\operatorname{Im}(\phi)$ factors into three sine terms and vanishes along three rays, and supports that the variety $\phi_1 + \phi_2 = 0$ has an analytic real deficit of at least $1.5$ from the deltoid cusps.
- **What it does not support**: Does not support that cubic Taylor expansion isolates deltoid cusps, nor that candidate quartets are excluded on the smooth regular arc of $B_6(\theta)$.
- **Narrowest defensible claim**: $\operatorname{Im}(\phi(\alpha, \beta)) = 4 \sin(\alpha/2) \sin(\beta/2) \sin((\alpha+\beta)/2)$ on $\mathbb{R}^2$, and $\min_{\alpha,\beta} \operatorname{Re}(\phi(\alpha,\beta)) = -1.5$, ensuring $\min \operatorname{Re}(\phi_1 + \phi_2) \ge 1.5 > 0$ when one factor is at a cusp.
- **Next test needed**: Investigate whether candidate quartets on the smooth regular arc of $B_6(\theta)$ can be excluded via algebraic symmetry reduction.

