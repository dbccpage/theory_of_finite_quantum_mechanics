# Polar Deficit Trace Bound and Polar Factor Contraction for (2+4) Block Completions

Type: theorem
Confidence: high
Source: Candidates strategy_L01_N01, strategy_L01_N02, strategy_L01_N03 (Level 1); Candidate strategy_L04_N00 (Level 4)
Relevant to: Parameterizing approximate or perturbed (2+4) block completions of order-6 complex Hadamard matrices onto the compact Lie group U(2) with certified Frobenius distance bounds.

## Statement
Let $H' = \begin{pmatrix} E' & B' \\ C' & D' \end{pmatrix} \in \mathbb{C}^{6 \times 6}$ be any dephased matrix satisfying $H'^\dagger H' = 6 I_6$, with block sizes $2$ and $4$, within seed displacement Frobenius radius $R_s$ from nominal frames $B_0, C_0$:
$$\|\Delta E\|_F^2 + \|\Delta B\|_F^2 + \|\Delta C\|_F^2 \le R_s^2.$$
Let $K_B \in \mathbb{C}^{4 \times 2}$ and $K_C \in \mathbb{C}^{4 \times 2}$ be orthonormal bases for $\ker(B_0)$ and $\ker(C_0^\dagger)$ respectively ($B_0 K_B = 0, C_0^\dagger K_C = 0, K_B^\dagger K_B = I_2, K_C^\dagger K_C = I_2$). Let $P_C = C_0 (C_0^\dagger C_0)^{-1} C_0^\dagger$ and $m_C = \sqrt{4 - |S_C|}$.

Then the compressed $2 \times 2$ block:
$$Y := K_C^\dagger D' K_B \in \mathbb{C}^{2 \times 2}$$
satisfies the exact positive semidefinite deficit identity:
$$6 I_2 - Y^\dagger Y = K_B^\dagger B'^\dagger B' K_B + K_B^\dagger D'^\dagger P_C D' K_B \succeq 0,$$
and its trace satisfies the uniform bound:
$$\operatorname{tr}(6 I_2 - Y^\dagger Y) \le q := R_s^2 \left( 1 + \frac{A_*^2 + 6}{m_C^2} \right),$$
where $A_* = \min(2, \|E_0\|_{\mathrm{op}} + R_s)$.
Whenever $q < 6$, $Y$ is invertible, its unique polar factor $V := Y (Y^\dagger Y)^{-1/2}$ belongs to $U(2)$, and the Frobenius distance satisfies:
$$\|Y - \sqrt{6} V\|_F \le p := \frac{q}{\sqrt{6} + \sqrt{6 - q}}.$$

## Proof
From unitarity $H'^\dagger H' = 6 I_6$, the lower-right $4 \times 4$ block evaluates to:
$$B'^\dagger B' + D'^\dagger D' = 6 I_4.$$
Compressing both sides with the orthonormal frame $K_B$:
$$K_B^\dagger B'^\dagger B' K_B + K_B^\dagger D'^\dagger D' K_B = 6 K_B^\dagger K_B = 6 I_2.$$
Inserting the resolution of the identity $I_4 = K_C K_C^\dagger + P_C$ into the quadratic term in $D'$ yields:
$$K_B^\dagger D'^\dagger D' K_B = (K_C^\dagger D' K_B)^\dagger (K_C^\dagger D' K_B) + K_B^\dagger D'^\dagger P_C D' K_B = Y^\dagger Y + K_B^\dagger D'^\dagger P_C D' K_B.$$
Subtracting $Y^\dagger Y$ gives:
$$6 I_2 - Y^\dagger Y = K_B^\dagger B'^\dagger B' K_B + K_B^\dagger D'^\dagger P_C D' K_B.$$
Both terms on the right-hand side are Gram forms $M^\dagger M$, hence positive semidefinite. Therefore $6 I_2 - Y^\dagger Y \succeq 0$.

For the trace bound, because $B_0 K_B = 0$, we have $B' K_B = (B_0 + \Delta B) K_B = \Delta B K_B$, so $\|B' K_B\|_F \le \|\Delta B\|_F \le R_s$.
Row-column orthogonality $C'^\dagger D' + E'^\dagger B' = 0$ implies $C_0^\dagger D' K_B = - E'^\dagger \Delta B K_B - \Delta C^\dagger D' K_B$.
Because $P_C = C_0 (C_0^\dagger C_0)^{-1} C_0^\dagger$ with $\|(C_0^\dagger C_0)^{-1/2}\|_{\mathrm{op}} = 1/m_C$, and since $\|D'\|_{\mathrm{op}} \le \sqrt{6}$, we bound:
$$\|P_C D' K_B\|_F \le \frac{1}{m_C} (\|E'\|_{\mathrm{op}} \|\Delta B\|_F + \sqrt{6} \|\Delta C\|_F).$$
Cauchy-Schwarz and $\|\Delta B\|_F^2 + \|\Delta C\|_F^2 \le R_s^2$ give $\operatorname{tr}(6 I_2 - Y^\dagger Y) \le q$.
The eigenvalues $\ell_1, \ell_2 \ge 0$ of $6 I_2 - Y^\dagger Y$ satisfy $\ell_1 + \ell_2 \le q < 6$. The singular values of $Y$ are $\sigma_j = \sqrt{6 - \ell_j} > 0$. The unique polar factor $V = Y (Y^\dagger Y)^{-1/2}$ has unit singular values. The scalar difference satisfies:
$$|\sigma_j - \sqrt{6}| = \frac{\ell_j}{\sqrt{6} + \sqrt{6 - \ell_j}} \le \frac{\ell_j}{\sqrt{6} + \sqrt{6 - q}}.$$
Summing in quadrature yields $\|Y - \sqrt{6} V\|_F \le p$.

## Hypotheses / Conditions
1. $H'$ is a $6 \times 6$ matrix satisfying $H'^\dagger H' = 6 I_6$.
2. Nominal seed frames satisfy $|S_B| < 4$ and $|S_C| < 4$ so that $m_C = \sqrt{4 - |S_C|} > 0$.
3. Seed displacement radius $R_s$ satisfies $q = R_s^2 (1 + (A_*^2 + 6)/m_C^2) < 6$.

## How It Applies
This theorem extends the exact polar kernel isometry to perturbed seed balls:
- For $r_s = 0.0320001$, $R_s = 0.201063$, $A_* = 2.0$, and $m_C = 1.0$, $q \approx 0.4447 < 6$ and $p \approx 0.0925$.
- On exact complex Hadamard matrices (such as $F_6$), $|S_C| \le 2$, $m_C^2 \ge 2.0$, and the deficit vanishes identically ($\ell_1 = \ell_2 = 0$).

## Caveats
- The bound $q < 6$ degenerates when $m_C \to 0$, which occurs when $|S_C| \to 4$. For exact Hadamards $|S_C| \le 2$, but near seed ball boundaries care is required.
- While the local contraction to $U(2)$ is mathematically sound, covering the entire moduli space $H_6$ requires accounting for 2D and 3D submanifolds, which cannot be covered by a coarse atlas of 22,379 balls alone.
