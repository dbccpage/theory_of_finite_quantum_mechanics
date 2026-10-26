# Derivation Control: SG-40

**AuthorityEffect:** None.

## Scope and Claim

This finite control (`SG-40`) executes a staged chain-complex repair episode across Stages 0 through 8 on the 3-vertex, 3-edge triangle graph over $\mathbb{Z}$:

$$\partial_1 = \begin{pmatrix} -1 & 0 & 1 \\ 1 & -1 & 0 \\ 0 & 1 & -1 \end{pmatrix}, \quad z = \begin{pmatrix} 1 \\ 1 \\ 1 \end{pmatrix}$$

1. **Before Attachment (`before_receipt`, Stage 5 Host Verifier)**:
   - $\partial_1 z = (0, 0, 0)^T$, $\operatorname{rank}_{\mathbb{Z}}(\partial_1) = 2$, initial 2-cell count $c_2 = 0$, and free $H_1$ rank $3 - 2 - 0 = 1$, witnessing that $z$ is a non-bounding 1-cycle before cell attachment.
2. **Declared Extension & After Attachment (`after_receipt`, Stage 5 Host Verifier)**:
   - Attaching one oriented 2-cell with $\partial_2 = (1, 1, 1)^T$ and witness chain $\beta = (1)$ satisfies $\partial_1 \partial_2 = (0, 0, 0)^T$, $\partial_2 \beta = z$, and updated free $H_1$ rank $3 - 2 - 1 = 0$.
3. **Adversarial & Refusal Controls**:
   - Witness $\beta = (0)$ fails $\partial_2 \beta = z$.
   - Sign-flipped boundary $\partial_2 = (1, 1, -1)^T$ gives $\partial_1 \partial_2 = (-2, 0, 2)^T \neq (0, 0, 0)^T$ and is refused.
   - Any self-issued parser receipt (`issuer != "host_stage_5"`) or undeclared extension contract is refused.

## Non-Claims

- This finite control does not claim general homology computation beyond the declared 3-vertex triangle complex over $\mathbb{Z}$ or live paid provider execution.
