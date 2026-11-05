# Field constraints and retention

Technical note accompanying the [review](holographic_brain_review.md). References A1–A91 and Figures 4–6 are to the [published paper](ijms-25-02399.pdf).

## 1. Gauss's law in the two appendices

Appendix A imposes $A^0=0$ and $\nabla\cdot\mathbf A=0$. Consequently $\partial^\nu F_{\nu0}=0$. Combining this with A6–A7 gives
$$
0=-e|\varphi|^2.
$$
This contradicts the subsequent normalization to a nonzero population. Restoring the discarded integration function yields $e|\varphi|^2=c(\mathbf x)$, allowing a static background cancellation. It does not permit an arbitrary evolving density.

This finding concerns the simultaneous equations as printed. It does not exclude radiation from divergence-free currents, or a reduced transverse-field theory in which electrostatic interactions have been treated separately. In particular, a static-density condition alone is insufficient to prove that every coherence amplitude vanishes.

Appendix C retains the background scalar potential. Write
$$
\begin{aligned}
n&=|\bar\varphi|^2,& \rho_m&=-en,\\
\dot n&=\frac em\nabla\cdot(n\mathbf A),&
\dot{\mathbf A}&=\mathbf E+\nabla A_0,\\
\dot{\mathbf E}
&=\nabla^2\mathbf A-\nabla(\nabla\cdot\mathbf A)
-\frac{e^2n}{m}\mathbf A+\mathbf S,&
\mathbf S&=-M^2\mathbf A-\gamma(\mathbf E+\nabla A_0)
+v(\mathbf A^-+\mathbf A^+).
\end{aligned}
$$
Here $\mathbf A^\pm$ denotes adjacent layers. With the paper's field convention,
$$
\dot G_m
=\partial_t(\nabla\cdot\mathbf E-\rho_m)
=\nabla\cdot\mathbf S.
$$
The curl terms cancel identically, as do the matter-current terms. Replacing $e^2n/m$ by printed $en/m$ adds
$$
\frac{e^2-e}{m}\nabla\cdot(n\mathbf A)
$$
to this residual.

For an effective medium, the relevant constraint is
$$
G_{\rm tot}=\nabla\cdot\mathbf E-\rho_m-\rho_{\rm med}-\rho_{\rm ext}.
$$
Its preservation requires the corresponding response and source charges, including
$\partial_t(\rho_{\rm med}+\rho_{\rm ext})=\nabla\cdot\mathbf S$ in this convention. They should follow from a constitutive or dynamical model, rather than be fitted after the fact to cancel a residual.

The initial data $\mathbf E=\mathbf A=0,\ n=1$ has $G_m=e$. A neutralizing background $+e$ removes that initial discrepancy but does not cancel a general time-dependent $\nabla\cdot\mathbf S$.

**Test:** report $G_{\rm tot}$ in $L^2$ and $L^\infty$, total charge and charge flux, using the same discrete derivatives as the evolution. Verify the discrete divergence-of-curl identity. Constraint error should converge under refinement. Number conservation alone is insufficient.

## 2. The Madelung sign and the inverse controller

Set $\bar\varphi=R e^{i\beta}$, $R>0$, and neglect the fluctuation terms as stated in the paper. The real part of A63 gives
$$
A_0-\frac{\dot\beta}{e}
=-\frac{\nabla^2R}{2meR}
+\frac e{2m}\left(\mathbf A-\frac{\nabla\beta}{e}\right)^2.
$$
Thus A70 has the wrong sign in its last term; A81/A87 have the consistent sign.

For the static inverse used by the controller, after the stated removal of the matter term,
$$
\begin{aligned}
v u_1^{(n-1)}
&=-\partial_2^2u_1^{(n)}
+\partial_1\partial_2u_2^{(n)}
+M^2u_1^{(n)}-v u_1^{(n+1)},\\
v u_2^{(n-1)}
&=-\partial_1^2u_2^{(n)}
+\partial_1\partial_2u_1^{(n)}
+M^2u_2^{(n)}-v u_2^{(n+1)}.
\end{aligned}
$$
A88/A89 interchange the Laplacian directions. Substitution of a nonconstant target into A82/A84 distinguishes the two versions. A constant target would miss the error.

**Test:** use a longitudinal target, a transverse target and a mixed target. Check the static residual first; then restore the omitted matter contribution and measure the controller's resulting bias.

## 3. Energy, writing and retention

At $T=310$ K,
$$
k_BT=26.714\ {\rm meV},\quad
k_BT\ln2=18.517\ {\rm meV},\quad
E_\gamma(500\,{\rm nm})=2.480\ {\rm eV}.
$$
For a symmetric binary memory reset against a thermal bath, the familiar $k_BT\ln2$ cost corresponds to removing one full bit of unknown information without usable retained side information. Copying onto a known blank can be logically reversible; resetting one of two identical copies can use the other copy. This is an ideal information-theoretic distinction, not a promise of zero dissipation in a laboratory device. See [Bennett, 2003](https://arxiv.org/abs/physics/0210005).

The equilibrium photon occupation at 500 nm is about $4.86\times10^{-41}$. This bounds that particular thermal background. It does not bound absorption, scattering, molecular motion, chemical noise or write errors. Comparing a photon energy with Landauer's bound supplies no retention guarantee.

For a supplied single-barrier escape model,
$$
\tau=\tau_0\exp(\Delta E/k_BT),\qquad
P(\text{failure by }T_h)=1-\exp(-T_h/\tau).
$$
The condition $P(\text{failure by }T_h)\le p$ requires
$$
\Delta E\ge
k_BT\ln\!\left(\frac{T_h}{\tau_0[-\ln(1-p)]}\right).
$$
If the right side is negative, a nonnegative barrier already satisfies this model's inequality.

| Assumed attempt time | Barrier for a one-year mean lifetime | Barrier for at most 1% failure over one year |
|---|---:|---:|
| $1$ ps | $1.199$ eV | $1.322$ eV |
| $1$ s | $0.461$ eV | $0.584$ eV |

These are conditional calculations. Neither the attempt time nor a barrier for the proposed record has been measured or derived here. The paper's 4 meV rotational scale is not such a barrier. A mean lifetime of one year allows about 63% probability of failure within that year; it is not a one-year reliability specification.

## 4. A retention measurement

Choose a finite message set, a write map, a stopping time $t_w$, and a readout $r$. Declare success by either a decoding error probability or a distance tolerance:
$$
P_{\rm err}(T_h)=
P\!\left[r(M(t_w+T_h))\ne b_{\rm written}\right].
$$
Measure this after the writing drive stops, over independent noise realizations and multiple stored patterns. Include optical readout disturbance. The increasing density contrast in Figure 6 is evidence about the displayed write trajectory; it is not a retention measurement.

For a driven, damped calculation, test an energy balance including input work, dissipation and the chosen medium's stored energy. A74 is a conserved energy for an earlier undriven approximation; it should not be required to stay constant after adding arbitrary drive, damping and inter-layer coupling.
