# Pairwise Column Sign Cancellation for the Displayed Two-Phase Affine Ansatz

**Date**: 2026-09-28

**AuthorityEffect**: None


## Source and scope boundary

The matrix checked here is the explicit two-phase affine ansatz named
`karlssonMatrix` in
[`MasterClassification.lean`](../../../../lean4/research_programs/mub6/MasterClassification.lean).
That source explicitly says that `karlssonMatrix` is a legacy component name and
does **not** establish equivalence to the complete named Karlsson family, its
parameter dimension, or an exhaustive catalog. Accordingly, this note makes no
claim about the full Karlsson family from the literature.

## Pairwise column sign-cancellation lemma

Let $M$ be an entrywise-nonzero $6 \times 6$ complex matrix. Suppose its
columns partition into three pairs $(C_{2p}, C_{2p+1})$ and there is a fixed
three-element row set $R \subset \{0,1,2,3,4,5\}$ such that

$$
M_{k,2p+1} =
\begin{cases}
M_{k,2p} & k \notin R,\\
-M_{k,2p} & k \in R.
\end{cases}
$$

For an odd positive integer $n$, let
$\gamma=(s_0,\ldots,s_5)$ contain three entries $+n$ and three entries $-n$,
and define the signed Laurent sum

$$F_\gamma(M)=\sum_{j=0}^{5}\prod_{k=0}^{5}M_{k,j}^{s_k}.$$

Then $F_\gamma(M)=0$. Entrywise nonzero is required because negative
components of $\gamma$ denote Laurent powers. On unit-modulus entries this is
equivalent to the usual conjugate-power convention.

### Derivation

Fix a column pair and let $m$ be the number of rows in $R$ whose exponent is
$+n$. The sign relating the two column products is

$$
(-1)^\beta,\qquad
\beta=m n+(3-m)(-n)=n(2m-3).
$$

Both $n$ and $2m-3$ are odd, so $\beta$ is odd and $(-1)^\beta=-1$.
Therefore the two products cancel. Summing the three independently cancelling
column pairs gives $F_\gamma(M)=0$.

## Application to the repository ansatz

The displayed matrix is

$$
A_6(x,y)=\begin{pmatrix}
1 & 1 & 1 & 1 & 1 & 1 \\
1 & -1 & x & -x & y & -y \\
1 & 1 & \omega & \omega & \omega^2 & \omega^2 \\
1 & -1 & \omega x & -\omega x & \omega^2 y & -\omega^2 y \\
1 & 1 & \omega^2 & \omega^2 & \omega & \omega \\
1 & -1 & \omega^2 x & -\omega^2 x & \omega y & -\omega y
\end{pmatrix}.
$$

For $R=\{1,3,5\}$, columns $(0,1)$, $(2,3)$, and $(4,5)$ have exactly the
sign relation required by the lemma. Hence the signed Laurent sum vanishes for
all 20 distinct row permutations of $\gamma_1=(1,1,1,-1,-1,-1)$ and of
$\gamma_2=(3,3,3,-3,-3,-3)$. Under `KarlssonDomain`, the Lean theorem
`karlssonMatrix_isCH6` separately establishes that this displayed ansatz is a
complex Hadamard matrix.

This application is limited to the displayed ansatz. It does not identify that
ansatz with the full literature Karlsson family, classify other families, or
establish any bound on MUB(6).

## Exact symbolic corroboration

[`test_karlsson_conj2.py`](test_karlsson_conj2.py) uses exact symbolic Laurent
arithmetic and the algebraic value
$\omega=(-1+\sqrt{-3})/2$. It checks all 20 distinct sign patterns for each of
$\gamma_1$ and $\gamma_2$. The script is corroboration of the finite symbolic
identities above; it is not a Lean kernel proof and does not expand the stated
scope.
