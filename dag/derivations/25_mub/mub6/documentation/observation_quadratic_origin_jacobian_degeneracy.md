# Jacobian Degeneracies and Gauge Nullspace Obstructions in Lifted Quadratic MUB Formulations

Type: observation
Confidence: high
Source: Candidates strategy_L00_N00, strategy_L00_N01, strategy_L00_N04, strategy_L00_N05, strategy_L00_N07, strategy_L00_N28, strategy_L00_N31, strategy_L01_N06, strategy_L01_N07 (Level 0 and Level 1 falser reports)
Relevant to: Rectangular Krawczyk operator design, preconditioner synthesis, coordinate projection, and choice of expansion centers in Route A.

## Statement
In the 440-variable, 666-equation formulation of candidate MUB quartets, the system exhibits severe structural rank deficiencies across all attempted expansion centers:
1. **Origin derivative vanishing**: At the coordinate origin $x_0 = 0$, every constraint governing candidate basis coordinates and auxiliary transition variables is purely quadratic or bilinear with zero constant and linear terms. All partial derivatives with respect to candidate coordinates vanish identically, yielding a Jacobian nullity of at least 126. Preconditioners evaluated at $x_0 = 0$ have zero rows for these coordinates, forcing $(I - A J(0))_{kk} = 1$ and precluding contraction.
2. **Torus gauge nullspace eigenvalue obstruction**: Even at non-zero basepoints $c$ situated on the complex torus $\mathbb{T}^{36}$, fixing only 24 first-row coordinates leaves residual continuous phase gauge degrees of freedom. The resulting Jacobian $J_F(c) \in \mathbb{R}^{666 \times 440}$ has column rank at most 416 (nullspace dimension $\ge 24$). For any $v \in \ker(J_F(c))$, $(I - A J_F(c)) v = v$, which forces $\lambda = 1$ to be an eigenvalue of multiplicity at least 24. Consequently, $\rho(I - A J_F(c)) \ge 1$, making strict contraction $\|I - A J_F(c)\|_\infty < 1$ mathematically impossible on the unprojected 440-variable system.
3. **Uniform rational center rank collapse**: At off-origin rational centers with uniform phase coordinates across rows 1..5 (such as $c = (3/5, 4/5)$), row-unitarity gradients become linearly dependent, causing the candidate basis Jacobian to drop rank to 35 out of 60 variables (nullity 25, minimum singular value $\approx 8 \times 10^{-17}$). Consequently, no exact rational left inverse $A$ satisfying $A J_F(c) = I_{440}$ exists at such points.
4. **Rational box midpoint derivative vanishing**: At box midpoints $c = (l+u)/2$ where free candidate basis variables in rows 1..5 have symmetric bounds $[-1, 1]$ (midpoint $c = 0$), in the defining relation $Z_{12} - H_1^\dagger H_2 = 0$, $Z_{12}$ appears linearly with coefficient 1 and does not multiply basis coordinates. Thus all partial derivatives with respect to candidate basis variables vanish identically at midpoint $c$, leaving basis directions in the nullspace and reproducing zero contraction.
5. **Bilinear constraint propagation stagnation**: Forward-backward interval constraint propagation (HC4-revise) across the bilinear coupling relations achieves exactly $0.0\%$ contraction on candidate basis variables from transition coordinate intervals, providing zero resistance to $2^{368}$ leaf explosion.

## Evidence
1. Symbolic differentiation in SymPy executed across falser audits (N00, N04, N05, N07) confirms that formal partial derivatives of all 666 equations with respect to candidate coordinates in rows 1..5 evaluate to zero at $x = 0$.
2. SVD analysis of the $666 \times 440$ Jacobian at the box center $x_0 = 0$ reveals exactly 126 zero singular values.
3. Native execution in `mub_szollosi_rectangular_native_receipt.json` records that exactly 0 candidate coordinates contracted and 0 separated when expanding at $c = 0$.
4. SVD and spectral radius probe on rank-416 Jacobians in $\mathbb{R}^{666 \times 440}$ (tested in N28 and N31 falser reports) confirms that $\rho(I - A J) \ge 1.0$ identically due to the 24-dimensional gauge nullspace.
5. Code probe in strategy_L01_N06_falser confirmed that the candidate basis Jacobian $J_U(c)$ at $c = (3/5, 4/5)$ drops rank to 35/60 with nullity 25.
6. Code probe in strategy_L01_N07_falser confirmed that all candidate basis derivatives vanish at midpoint $c = (l+u)/2$, and HC4-revise across $x_{0,0} = 1 + \sum_{m=1}^{10} A_m B_m$ leaves all $A_m \in [-1, 1]$ with $0.0\%$ contraction.

## Implications
- **What it supports**: Explains why origin-centered, uniform off-origin, midpoint-centered, and naive unprojected torus-centered Krawczyk contractors all return `CONTRACTED_UNRESOLVED_BOX`.
- **What it does not support**: Does not mean that the rectangular Krawczyk method is intrinsically flawed; rather, candidate basis variables cannot be contracted through auxiliary bilinear transition matrices without high-dimensional subdivision or algebraic variable elimination.
- **Narrowest defensible claim**: At $x_0 = 0$ and at symmetric midpoints $c$, candidate basis Jacobian columns vanish; at uniform rational centers, rank collapses to 35/60; and at torus basepoints with rank 416, the 24D gauge nullspace forces $\rho(I - A J) \ge 1$, precluding strict $L_\infty$ contraction.
- **Next test needed**: Evaluate rectangular Krawczyk contraction on an algebraically reduced system ($\le 72$ variables) where auxiliary transition variables $Z_{ab}$ are eliminated.

## Caveats
Even after eliminating auxiliary transition variables, high-dimensional interval derivative variation across boxes of radius 1-3 can yield operator norms $\rho_\infty \gg 1$ unless candidate coordinates are finely subdivided.
