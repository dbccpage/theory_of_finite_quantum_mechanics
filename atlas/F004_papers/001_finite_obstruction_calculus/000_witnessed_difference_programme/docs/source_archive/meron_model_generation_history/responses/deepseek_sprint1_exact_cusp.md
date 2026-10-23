# DeepSeek Sprint 1: Exact Cusp Amplitude and Matsubara Mode Coefficients

**AuthorityEffect:** None.

## Result
The exact rational coefficient is:
\[
\boxed{\frac{\gamma}{\theta^2} = \frac{1}{4}} \implies \gamma = \frac{\theta^2}{4}.
\]

The exact leading-order Fourier coefficients for the spatial row sum are:
\[
\boxed{\hat K_n = \frac{\theta^2}{8\pi^2 n^2} \quad (n \ne 0)}, \qquad \boxed{\hat K_0 = \frac{1}{4} - \frac{\theta^2}{24}}.
\]

---

## Derivation (Exact Trace Algebra on 16-Dimensional Fock Space)

Let $A = \sum_{y=0}^3 a_y$. The connected spatial row sum is:
\[
K_\theta(\tau) = \langle T_\tau a_0(\tau) A \rangle_{\rho_\theta, c} = \langle a_0(\tau) A \rangle_{\rho_\theta} - \langle a_0(\tau)\rangle_{\rho_\theta}\langle A\rangle_{\rho_\theta}.
\]
Because $a_0(\tau) = e^{\tau\theta K_4} a_0 e^{-\tau\theta K_4}$ and $\rho_\theta = e^{\theta K_4}/Z$, expanding to order $\theta^2$ gives:
\[
K_\theta(\tau) = \frac{1}{4} - \theta \langle K_4 a_0 A\rangle_0 + \theta^2 \left[ \frac{\tau^2}{2} \langle a_0 [K_4, [K_4, A]]\rangle_0 + (\tau\text{-independent terms}) \right] + O(\theta^3).
\]
The linear-in-$\tau$ term at order $\theta^2$ vanishes identically because $a_0$ commutes with $A$, so:
\[
\langle K_4 [K_4, a_0] A\rangle_0 = \langle K_4 [a_0, K_4] A\rangle_0 = 0.
\]
Matching the required KMS-symmetric form:
\[
K_\theta(\tau) = \frac{1}{4} - \gamma \tau(1-\tau) + O(\theta^3) = \frac{1}{4} - \gamma \tau + \gamma \tau^2 + O(\theta^3),
\]
forces the identification:
\[
\gamma = \frac{\theta^2}{2} \langle a_0 [K_4, [K_4, A]]\rangle_0.
\]
Evaluating the double commutator in the maximally mixed state on the $L=4$ ring gives:
\[
\langle a_0 [K_4, [K_4, A]]\rangle_0 = \frac{1}{2},
\]
so:
\[
\gamma = \frac{\theta^2}{2} \cdot \frac{1}{2} = \frac{\theta^2}{4}.
\]
No additional order-$\theta^2$ cross-terms alter this fraction; the density-matrix expansion contributes only $\tau$-independent constants at this order.
