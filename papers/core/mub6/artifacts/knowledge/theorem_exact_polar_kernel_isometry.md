# Exact Polar Kernel Isometry for (2+4) Block Completions

Type: theorem
Confidence: high
Source: Candidates strategy_L00_N02, strategy_L00_N06 (Level 0)
Relevant to: Parameterizing candidate completions of order-6 complex Hadamard matrices onto the compact Lie group U(2).

## Statement
Let $H \in \mathbb{C}^{6 \times 6}$ be a dephased complex Hadamard matrix ($|H_{jk}| = 1$, $H H^\dagger = 6 I_6$, with first row and first column equal to 1). Partition $H$ into blocks of sizes $2$ and $4$:
$$H = \begin{pmatrix} E & B \\ C & D \end{pmatrix},$$
where $E \in \mathbb{C}^{2 \times 2}$, $B \in \mathbb{C}^{2 \times 4}$, $C \in \mathbb{C}^{4 \times 2}$, and $D \in \mathbb{C}^{4 \times 4}$.
Let $V_B \in \mathbb{C}^{4 \times 2}$ be an orthonormal basis of $\ker B$ ($B V_B = 0$ and $V_B^\dagger V_B = I_2$), and let $V_C \in \mathbb{C}^{4 \times 2}$ be an orthonormal basis of $\ker C^\dagger$ ($C^\dagger V_C = 0$ and $V_C^\dagger V_C = I_2$).
Then the compressed $2 \times 2$ block:
$$W := V_C^\dagger D V_B \in \mathbb{C}^{2 \times 2}$$
satisfies the exact isometry identity:
$$W^\dagger W = 6 I_2.$$
Consequently, $U := \frac{1}{\sqrt{6}} W \in U(2)$, and the completion block $D$ admits the exact decomposition:
$$D = D_{\operatorname{det}} + \sqrt{6} V_C U V_B^\dagger,$$
where $D_{\operatorname{det}} = - C (C^\dagger C)^{-1} E^\dagger B - C E^\dagger (B B^\dagger)^{-1} B + C (C^\dagger C)^{-1} C^\dagger C E^\dagger (B B^\dagger)^{-1} B$ is uniquely determined by $E, B, C$.

## Proof
Consider the matrix $\begin{pmatrix} 0 \\ V_B \end{pmatrix} \in \mathbb{C}^{6 \times 2}$. Applying the top row block of $H$:
$$\begin{pmatrix} E & B \end{pmatrix} \begin{pmatrix} 0 \\ V_B \end{pmatrix} = B V_B = 0.$$
Because $H H^\dagger = 6 I_6$, the row space of the bottom block $\begin{pmatrix} C & D \end{pmatrix}$ spans the orthogonal complement of the first two rows. Therefore, there exists a unique matrix $X \in \mathbb{C}^{4 \times 2}$ such that:
$$\begin{pmatrix} 0 \\ V_B \end{pmatrix} = \begin{pmatrix} C^\dagger \\ D^\dagger \end{pmatrix} X.$$
The top block identity gives $C^\dagger X = 0$, meaning the columns of $X$ lie in $\ker C^\dagger$. Because $V_C$ is an orthonormal basis of $\ker C^\dagger$, there exists $Y \in \mathbb{C}^{2 \times 2}$ such that $X = V_C Y$.
The bottom block identity then yields $V_B = D^\dagger X = D^\dagger V_C Y$.
Computing the norm:
$$I_2 = V_B^\dagger V_B = X^\dagger (C C^\dagger + D D^\dagger) X = 6 X^\dagger X = 6 Y^\dagger V_C^\dagger V_C Y = 6 Y^\dagger Y.$$
Hence $Y^\dagger Y = \frac{1}{6} I_2$.
Now consider $W = V_C^\dagger D V_B$. Substituting $V_B = D^\dagger V_C Y$:
$$W = V_C^\dagger (D D^\dagger) V_C Y.$$
From $H H^\dagger = 6 I_6$, we have $C C^\dagger + D D^\dagger = 6 I_4$. Since $V_C^\dagger C = 0$, we have $V_C^\dagger (D D^\dagger) V_C = 6 V_C^\dagger V_C = 6 I_2$.
Therefore $W = 6 Y$.
Consequently:
$$W^\dagger W = 36 Y^\dagger Y = 36 \left(\frac{1}{6} I_2\right) = 6 I_2.$$
This shows $W / \sqrt{6} \in U(2)$. Decomposing $D$ into projections onto $\operatorname{ran}(B^\dagger)$, $\operatorname{ran}(C)$, and the kernel frames yields the decomposition.

## Hypotheses / Conditions
1. $H$ is a $6 \times 6$ matrix satisfying $H H^\dagger = 6 I_6$.
2. The off-diagonal blocks $B \in \mathbb{C}^{2 \times 4}$ and $C \in \mathbb{C}^{4 \times 2}$ have full rank 2, which holds whenever the inner product sum $|S| \le 2 < 4$.

## How It Applies
This algebraic identity parameterizes the 16 entries of the completion block $D$ in terms of the compact 4-dimensional Lie group $U(2)$ and the 9 seed phases of $E, B, C$.
- What it supports: Supports an exact parameterization of $D$ via $U(2)$ across all complex Hadamard matrices.
- What it does not support: Does not support a finite grid refutation at coarse mesh sizes ($\sim 10^5$ cells) due to high-dimensional interval expansion.
- Narrowest defensible claim: For any dephased complex Hadamard matrix, the compressed block $V_C^\dagger D V_B$ has singular values equal to $\sqrt{6}$.
- Next test needed: Test whether isolated candidate representatives (such as Tao or Haagerup) admit certified local Taylor enclosures on $U(2)$.

## Caveats
While the algebraic identity is exact, using it to cover all complex Hadamard matrices by grid discretization on $[0, 2\pi)^9 \times U(2)$ encounters extreme dimensional complexity ($\sim 10^{19}$ cells needed for exclusion).
