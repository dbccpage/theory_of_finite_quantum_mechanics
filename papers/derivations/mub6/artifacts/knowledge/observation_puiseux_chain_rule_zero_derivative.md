# Vanishing Derivative Artifact in Cusp Puiseux Reparameterization

Type: observation
Confidence: high
Source: Candidates L01_N12, L00_N05, L00_N20
Relevant to: Deltoid cusp blowing-up, parameter preconditioning, Krawczyk branch-and-bound

## Statement
Applying a quadratic Puiseux substitution $\theta(t) = \theta_0 + t^2$ to desingularize a deltoid cusp at $\theta = \theta_0$ induces an identically vanishing partial derivative with respect to $t$ at the cusp center $t = 0$:
$$\left.\frac{\partial F}{\partial t}\right|_{t=0} = \left.\frac{\partial F}{\partial \theta}\right|_{\theta_0} \cdot (2 \cdot 0) = 0$$
This generates an all-zero Jacobian column at the branch center.

## Evidence
By the chain rule, differentiating $F(x, \theta(t))$ with respect to $t$ gives $\frac{\partial F}{\partial t} = \frac{\partial F}{\partial \theta} \frac{d\theta}{dt} = 2t \frac{\partial F}{\partial \theta}$. At the expansion center $t = 0$, this derivative evaluates to 0 regardless of whether $\frac{\partial F}{\partial \theta}$ vanishes or not. In rectangular Krawczyk interval preconditioning, the column corresponding to $t$ in the midpoint Jacobian $J(x_0, 0)$ is identically zero, dropping the column rank and making the normal matrix non-invertible.

## Implications
Quadratic Puiseux blowing-up does not yield a non-singular midpoint Jacobian at $t = 0$. Preconditioners evaluated at the cusp center face an artificial null direction along the parameter axis. To use fractional powers effectively in interval analysis, the expansion center must either be offset ($t_0 > 0$) or the algebraic relations must be reformulated without smooth chain-rule substitution at the origin.

## Caveats
Puiseux series remain a valid algebraic representation for the curve branches; the obstruction is specific to evaluating numerical and interval Jacobian preconditioners at the coordinate origin $t = 0$.
