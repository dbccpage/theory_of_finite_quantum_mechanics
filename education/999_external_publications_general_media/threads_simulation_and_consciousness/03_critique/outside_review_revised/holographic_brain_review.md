# Holographic Brain Theory: equations, approximations and empirical tests

Review of A. Nishiyama, S. Tanaka, J. A. Tuszynski and R. Tsenkova, *Holographic Brain Theory: Super-Radiance, Memory Capacity and Control Theory*, IJMS **25**, 2399 (2024), [doi:10.3390/ijms25042399](https://doi.org/10.3390/ijms25042399).

Revised 5 November 2026. Equation numbers refer to the [published paper](ijms-25-02399.pdf). The accompanying [transcription](ijms-25-02399.md) is a reading aid; the PDF governs discrepancies.

## Assessment

The paper combines a conditional superradiance calculation, an ideal holographic capacity estimate, a proposed optical reconstruction and a numerical density-control example. These are useful components of a model. The paper does not demonstrate the complete sequence from light production to writing, retention and optical recall in biological tissue.

The strongest objections concern equations and missing links between those components. Neither the speculative discussion of experience nor the absence of a full many-body calculation invalidates every result. Conversely, the displayed mean-field trajectory does not establish the proposed quantum or cognitive mechanisms.

## 1. Electromagnetic constraints

Appendix A imposes both $A^0=0$ and $\nabla\cdot\mathbf A=0$. Its equation A7 is

$$
\partial^\nu F_{\nu0}=J_0,\qquad J_0=-e|\varphi|^2.
$$

The left side vanishes under the two imposed conditions. For nonzero $e$, A7 therefore requires $|\varphi|^2=0$, contrary to the subsequent nonzero normalization. This is an internal inconsistency in the equations read literally.

Retaining the discarded integration function gives
$$
0=-e|\varphi(t,\mathbf x)|^2+c(\mathbf x).
$$
It permits a static neutralized density, not arbitrary time-dependent charge. A transverse-field approximation can be useful, but the longitudinal electrostatic sector then needs a stated treatment. A static density alone does not exclude every transverse current or every radiative mechanism; the stronger assertion that it forces all two-level coherence to vanish is not established.

Appendix C keeps a background scalar potential. The Appendix A argument does not apply to it unchanged. Instead, let $n=|\bar\varphi|^2$, $\rho_m=-en$, and use the electric-field convention of A83/A85. Equations A82/A84/A86 imply

$$
\partial_t(\nabla\cdot\mathbf E-\rho_m)=
-M^2\nabla\cdot\mathbf A
-\gamma\nabla\cdot(\mathbf E+\nabla A_0)
+v\nabla\cdot(\mathbf A^{(n-1)}+\mathbf A^{(n+1)}).
$$

Thus the added response and drive terms do not, in general, preserve the **matter-only** Gauss constraint. An effective medium may carry additional polarization or external charge. Those contributions must be specified and included in the total constraint before claiming either consistency or physical charge nonconservation. The zero-field, unit-density initial condition also needs a neutralizing charge or a nonzero integration function.

The [constraint note](field_constraints_and_retention.md) derives this identity and its limits.

## 2. Equation discrepancies that affect reproduction

| Location | Discrepancy | Required resolution |
|---|---|---|
| A29 and text after A47 | The printed condition is $\Omega\ge e^2\bar n/m$. A13 instead requires $\Omega^2\ge e^2\bar n/m$ for a real resonant wavevector. | Correct the squared-frequency threshold; state how the threshold case is treated in the mode integral. |
| A31 | $\chi_1$ appears on the right where A25 requires $\chi_0$. | Use the coupled two-level equation; A34 already does so. |
| A52 | The reconstructed response is labelled $\tilde A_i$, previously the input. | Distinguish input and response. |
| A70 | The squared-velocity term has a minus sign. Direct reduction of A63 gives a plus sign, as in A81/A87. | Identify the equation used in computation. |
| A76/A78 | The matter coefficient is $e n/m$; A71/A82/A84 use $e^2n/m$. | Make the coefficient consistent and check charge continuity. |
| A88/A89 | The printed inverse uses $-\partial_1^2u_1$ and $-\partial_2^2u_2$. A82/A84 require $-\partial_2^2u_1$ and $-\partial_1^2u_2$. | Correct the inverse and compare both implementations with Figures 4–6. |

The A88/A89 discrepancy is visible on PDF page 22. For example, with $u_1=\sin x^1,\ u_2=0$, the curl terms in A82 vanish. Its static inverse is $v u_1^{(n-1)}=M^2u_1^{(n)}-v u_1^{(n+1)}$, after the stated omission of the matter term. Printed A88 adds $\sin x^1$, leaving a nonzero residual when substituted back.

For the separated targets, the corrected inverse reduces to $u_{n-1}=2.5u_n-u_{n+1}$. With $u_4=0.1,\ u_5=0$, it gives $u_0=2.13125$. The quoted factor $0.1(2/0.8)^4=3.90625$ omits the backward-coupling subtraction and is not the full recurrence. This comparison does not identify which implementation produced Figure 4.

Duplicated plus signs in A23/A26 are typographical. The discrepancies above cannot all be dismissed as harmless without the implementation.

## 3. Superradiance and optical propagation

The reduced equations yield
$$
\dot\theta=\tau_R^{-1}\sin\theta,\quad
\tau_R=\frac{2\pi}{g^2\Omega N},\quad
\mathcal A(t)=\frac{g\Omega N}{4\pi}
\operatorname{sech}\frac{t-t_d}{\tau_R}.
$$
This solution follows after introducing a radiation-loss term and neglecting the field-envelope derivative relative to that loss. It is a solution of the reduced equation, not an exact solution of every preceding dynamical equation. The initial angle and the parameters $g,\Omega,N,L_3$ are inputs. Their biological values, dephasing rates and wavelength need calibration.

A13 uses carrier wavevectors $(k^1,k^2,0)$ and axial polarization. That ansatz does not derive an axially propagating guided mode. Establishing axial transport requires a boundary-value problem with the lumen, protein wall, surrounding medium and source coupling.

The quoted 21 nm cutoff cannot be interpreted without the waveguide model. For a perfectly conducting circular guide, $\lambda_c\approx1.706d$ and propagation requires $\lambda<\lambda_c$; a 500 nm wave would be below the frequency cutoff. This conditional calculation does not exclude dielectric guiding. A dielectric cylindrical model needs complex refractive indices, geometry, confinement, attenuation and coupling efficiency. Neither a molecular count nor an ideal-guide formula settles transmission through a microtubule.

## 4. Holography, contrast and capacity

Appendix B assumes
$$
n\propto|r+o|^2.
$$
Under its local-response approximation,
$$
A_i\simeq T(n)r,\qquad
T(n)=\frac{M^2}{M^2+e^2n/m}.
$$
The expansion contains a term proportional to $|r|^2o$. That is a conditional reconstruction result. It does not show that the controller produces the required interference pattern or that an object image can be read from the simulated density.

In the dimensionless example, $T(n)=1/(1+0.045n)$. The density change from 1 to 0.79 changes $T$ from 0.95694 to 0.96567: a field-transmission difference of about 0.00873. The number 0.045 is a screening parameter. It is neither an image amplitude nor a diffraction efficiency. Those require a specified spatial pattern, reference field, propagation and collection geometry.

The capacity arithmetic is consistent:
$$
C/A=\frac{4n_rd}{\lambda^3}
=8.32\times10^{10}\ {\rm bit/mm^2},
\qquad C=2.6\times10^{15}\ {\rm bytes}
$$
for the supplied $n_r=1.3,\ d=2$ mm, $\lambda=500$ nm and area $2500\ {\rm cm^2}$. The paper's 2.5 PB is rounding. The comparison value is 31.25 TB at one bit for each of $250\times10^{12}$ synapses.

These are conditional counts. Usable capacity requires distinguishable outputs at a declared error rate, after losses, noise, interference between stored patterns and readout. An optical transmission calculation is needed before applying an ideal volume-hologram estimate to tissue.

## 5. What the mean-field calculation establishes

The numerical equations retain field amplitudes, phase-dependent dynamics and the density-gradient term from the Schrödinger equation. They omit explicit propagator evolution and approximate the response kernel by $M^2$ and $\gamma$. Calling this a mean-field calculation describes its scope. It does not imply that every quantum feature has vanished.

Three distinctions matter:

1. Neglecting fluctuation contributions in an equation does not uniquely specify a coherent-product density operator. Coherent states themselves have vacuum fluctuations.
2. The variables $B_\mu=A_\mu-\partial_\mu\beta/e$ are gauge invariant. Writing equations in $B_\mu$, or choosing a valid gauge with $\beta=0$, need not discard a physical phase. Dropping $\partial_\mu\beta$ while holding the original $A_\mu$ fixed generally changes the state.
3. A four-transverse response tensor can have a spatial longitudinal response. A Ward identity alone does not prohibit it. Nor does the presence of both $M^2$ and the condensate contribution prove double counting; the microscopic definitions must be compared.

The physical scale $m$, material response parameters and layer properties are not calibrated. The 4 meV rotational scale discussed elsewhere is not identified with the simulated mass or a memory barrier. A numerical ablation of the density-gradient term would test its effect on specified outputs; deleting it is not, by itself, a controlled classical limit.

## 6. A valid use of projection bounds

For a specified bipartite state define the correlation defect
$$
D_{ab}=\|\rho_{ab}-\rho_a\otimes\rho_b\|_1.
$$
For any product state $\sigma_a\otimes\sigma_b$,
$$
\begin{aligned}
D_{ab}
&\le\|\rho_{ab}-\sigma_a\otimes\sigma_b\|_1
 +\|\sigma_a\otimes\sigma_b-\rho_a\otimes\rho_b\|_1\\
&\le3\|\rho_{ab}-\sigma_a\otimes\sigma_b\|_1.
\end{aligned}
$$
The second line uses partial-trace contractivity and the tensor-product triangle inequality. Thus $D_{ab}/3$ is a lower bound on error against any product reconstruction. For mixed states, $D_{ab}>0$ need not mean entanglement.

The finite-system theorem in *Projection Obstruction for Factorized States*, §5.1, adds
$$
D_{ab}(t)\ge\nu_{ab}t-24g_{\rm inc}^2t^2,\qquad
g_{\rm inc}=\max_v\sum_{X\ni v}\|h_X\|_\infty,
$$
under its finite-dimensional, one-/two-local Hamiltonian and product-initial-state hypotheses. The half-slope interval is $0<t\le\nu_{ab}/(48g_{\rm inc}^2)$. On-site terms contribute to $g_{\rm inc}$.

Applying this theorem to the paper requires a Hilbert-space decomposition, a controlled bosonic cutoff, explicit interactions and initial state. Discretized matter-current couplings can involve more than two chosen subsystems. A phenomenological damping constant is not a Lindblad generator. The theorem's edgewise Duhamel estimate also assumes a particular marginal-product projected trajectory; it cannot simply be assigned to a different coherent-state or dissipative evolution.

Until these identifications are made, the theorem supplies a possible method, not an error certificate for Figure 6. A density prediction may remain accurate despite substantial state error. The appropriate upper-bound target is the observable used for readout.

## 7. Retention and experience

Figure 6 reports increasing density contrast: 1.3%, 4.5%, 9.1%, 16% and 21% over the displayed times. Its late distortion does not demonstrate erasure. Figure 5 shows decay of the driving field, a different quantity. Retention needs a write-stop time, a later readout and a success criterion.

Landauer's bound concerns entropy removed in a specified information-processing operation. A 500 nm photon has energy about 2.48 eV; this does not establish write fidelity or storage lifetime. Under a supplied single-barrier Arrhenius model,
$$
\tau=\tau_0e^{\Delta E/k_BT}.
$$
At 310 K, a one-year **mean lifetime** requires $\Delta E\approx1.20$ eV if $\tau_0=1$ ps, or 0.461 eV if $\tau_0=1$ s. A reliability requirement changes the bound; neither attempt time nor barrier is established for this model.

The experience discussion does not specify an additional term used in the numerical predictions, a report channel or a quantitative mapping to perceptual reports. A proposed experiment could test such a mapping. Its interpretation would require explicit measurement assumptions; definitions from the Witnessed Difference Programme are useful organizational choices, not additional empirical laws of consciousness.

## 8. Next result worth obtaining

Produce one complete numerical write–hold–read example. Use consistent field equations, a declared effective medium, calibrated units and a known input image. Report constraint residuals, convergence, reconstructed-image error and retention after the drive stops. Compare against a specified classical optical model. This would connect the paper's separate calculations and show which further claims the model can support.

The [research plan](research_plan.md) specifies these tests. The [claim register](claim_register.md) separates calculations, assumptions and unresolved questions. The supplied verification script checks finite algebraic and numerical examples; it does not reproduce Figures 4–6 or certify the full field theory.
