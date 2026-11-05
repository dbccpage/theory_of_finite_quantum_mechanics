# Comments on "Holographic Brain Theory: Super-Radiance, Memory Capacity and Control Theory"

**Paper.** A. Nishiyama, S. Tanaka, J. A. Tuszynski and R. Tsenkova, *Int. J. Mol. Sci.* 25(4):2399 (2024), doi:10.3390/ijms25042399.
**Date.** 5 November 2026.
**From.** [name, contact]

Dear Dr. Nishiyama, Dr. Tanaka, Dr. Tuszynski and Dr. Tsenkova,

We have read your paper and its three appendices and re-derived the main steps. We are writing because several results depend on steps that do not hold as printed. Most of them can be repaired, and we say how. Each point names the equation it concerns, says what we find, and says what would settle it. Equation numbers are yours. Every computation below is replayed by one script that accompanies this letter (`8_checks.py`, Python with sympy and numpy). Where we have misread you, we would be glad to be corrected, and we will publish the correction.

## Summary of our reading

The paper contains four calculations:

1. a Maxwell–Bloch superradiant pulse from two-level charged emitters (Appendix A);
2. holographic screening of an external wave (Appendix B);
3. an optical storage count (Section 3);
4. a control simulation on a four-layer lattice (Section 4, Appendix C).

Sections 5 and 6 then interpret these as memory and subjective experience. Our main findings are:

- Calculation 1 is inconsistent with the gauge conditions it imposes.
- Calculation 4 does not conserve Gauss's law, and its drive formula is misprinted.
- Calculation 2 assumes the hologram rather than producing it.
- Calculation 3 is correct as arithmetic, but its size comes from one assumption.
- None of the interpretive steps in Section 5 corresponds to a variable or an equation in the model.

## A. Points that change a result

**A1. The conditions $A^0 = 0$ and $\nabla_i A_i = 0$ freeze the charge, so (A38) has no source.**

You adopt $A^0 = 0$ and $\nabla_i A_i = 0$ before (A2) and call the pair the Coulomb gauge. The Coulomb gauge is the second condition alone. $A^0$ is then fixed by Poisson's equation and is not zero when $J_0 \neq 0$.

With both conditions, $F_{i0} = -\partial_0 A_i$. So $\partial^\nu F_{\nu 0}$ is a multiple of $\partial_0(\nabla_i A_i)$, which vanishes. Equation (A7) then reads $J_0 = -e|\varphi|^2 = 0$. Keeping the time-independent term that the text after (A7) sets to zero, it reads $\partial_0|\varphi|^2 = 0$.

In the two-level expansion (A8)–(A12), the density contains the cross term
$2\,\mathrm{Re}\big(\chi_0^*\chi_1\,e^{-i\Omega x^0}\,\phi_0^*\phi_1\big)$,
which oscillates at $\Omega$. A density that is constant in time forces $\chi_0^*\chi_1 = 0$ wherever $\phi_0^*\phi_1 \neq 0$. That sets $R = 2\chi_0^*\chi_1$ to zero in (A38), and the pulse (A45) has no source.

*Repair.* Keep $\nabla_i A_i = 0$ and let $A^0$ solve Poisson's equation. The charge can then move. The price is the electrostatic term $eA^0\varphi$ in (A2), which must be shown small on the time scale $\tau_R$.

**A2. Appendix C does not conserve Gauss's law.**

From (A82), (A84) and (A86), with $J^0 = -e|\bar\varphi|^2$ from (A66), the $e^2$ terms cancel exactly against the continuity equation. What remains is

$$\partial_0\big(\nabla_i E_i - J^0\big) = -M^2\,\nabla_i A_i \;-\; \gamma\,\nabla_i\big(E_i + \partial_i A_0\big) \;+\; v\,\nabla_i\big(A_i^{(n-1)} + A_i^{(n+1)}\big).$$

None of the three terms vanishes for your drive. The targets (10)–(11) are curl-free, so the drive is purely longitudinal and $\nabla_i A_i \neq 0$. The boson number is conserved, as you report ($10^{-6}\,\%$). What drifts is $\nabla_i E_i - J^0$.

We reran the simulation at your parameters, measuring $\nabla_i E_i - J^0 - e$. The constant $e$ is the uniform background needed for the initial data $|\bar\varphi| = 1$, $E = 0$ to satisfy (A68). Along the run, this residual is 1.1 to 2.3 times the change in charge density that the run produces. Our rerun reproduces your density dips to within about 10 %, but we have not compared it with your code.

*Repair.* Either declare a medium charge whose evolution compensates these terms and give its equation, or use a damping and mass term that respects the constraint.

**A3. The drive amplitude: (A88)–(A89) carry the wrong second derivative.**

Take (A82), drop the time derivatives and solve for $A_1^{(n-1)}$. The result is

$$u_1^{(n-1)} = \frac{-\partial_2^2 u_1^{(n)} + \partial_1\partial_2 u_2^{(n)} + M^2 u_1^{(n)}}{v} - u_1^{(n+1)}.$$

(A88) prints $-\partial_1^2 u_1$, and (A89) correspondingly prints $-\partial_2^2 u_2$. Your Section 4 text says that the $\partial_2^2 u_1$ and $\partial_1\partial_2 u_2$ terms vanish for target (10). That is true of the corrected formula, not of the printed one.

For targets (10)–(11), the corrected recursion has no derivative terms at all:
$u^{(n-1)} = (M^2/v)\,u^{(n)} - u^{(n+1)} = 2.5\,u^{(n)} - u^{(n+1)}$.
Starting from $u^{(N)} = 0.1$ and $u^{(N+1)} = 0$ with $N = 4$, it gives $\max|u_1^{(0)}| = 2.13$. The text quotes $0.1 \times 2^4/0.8^4 = 3.9$, which omits the $-u^{(n+1)}$ term, and also says "approximately 3".

*Request.* State which input amplitude was used for Figures 4–6.

**A4. The hologram is assumed, not produced (Appendix B).**

(A51) sets $|\varphi|^2 \propto |r + o|^2$. No equation in the paper produces this pattern, and the object wave $o$ has no source.

In (A48), the external wave enters only through $M^2\tilde A_i$. At $M^2 = 0$ it has no effect, and at large $M^2$ the medium no longer imprints on it. The response is set by the screening number $e^2|\varphi|^2/(M^2 m)$, which is 0.045 at your Section 4 values.

Given (A51), the screened wave (A52) contains $|r|^2 o$, which is correct. It also contains the twin term $r^2 o^*$, and nothing in the model selects the image from the twin.

*Request.* Supply a write process that produces $|r+o|^2$ from an object, and a read rule that returns the object with an error rate.

**A5. Retention is not addressed, and the Landauer paragraph does not bear on it.**

$k_BT\ln 2$ (18.5 meV at 310 K; the text says 20 meV) is the minimum heat released when one bit is *erased*. It does not set how long a written pattern survives.

In your model the record is a density pattern in $\varphi$, not a photon. Its lifetime depends on the barrier that holds it. For a single barrier with attempt time $\tau_0$, a one-year mean lifetime needs $\Delta E = k_BT\ln(1\,\mathrm{yr}/\tau_0)$. That is 1.20 eV for $\tau_0 = 1$ ps and 0.46 eV for $\tau_0 = 1$ s. The paper gives no barrier.

The 60 µm "maximum wavelength" is the wavelength whose photon energy equals $k_BT\ln 2$ (67 µm at 18.5 meV). It is a unit conversion, not a limit on holography. The photon energy at 500 nm is 2.48 eV, not 2.4 eV.

**A6. The petabyte figure is a depth assumption.**

$4n_r d/\lambda^3$ with $n_r = 1.3$, $d = 2$ mm and $\lambda = 500$ nm gives $8.32\times 10^{10}$ bit/mm². Over 2500 cm² that is 2.6 PB (2.5 PB in the text). The synaptic comparison is 31.25 TB (30 TB in the text).

A surface hologram over the same area holds $4/\lambda^2 \times 2500\ \mathrm{cm^2} = 0.5$ TB. The factor that makes it petabytes is $n_r d/\lambda = 5200$, which assumes the tissue resolves depth at the wavelength scale. Nothing in the model writes or reads by depth.

The wavelength is also chosen, not derived. The model's own emission frequency $\Omega$ is never computed. At the 4 meV scale you quote for water, $\lambda = 310$ µm and the same formula gives 11 MB.

## B. Points that limit a result

**B1. The pulse rests on three unstated inputs.**

- **The seed $\theta_0$.** It is used in (A41), (A44) and (A47), and in $\tau_0 = -\tau_R\ln\tan(\theta_0/2)$ in Section 2, which says "definition of $\theta_0$ is in Appendix A". Appendix A uses $\theta_0$ but does not define it. At $\theta_0 = 0$, $\tau_0$ is infinite and there is no pulse.
- **The emitter-size condition.** The condition before (A24) needs emitters within one wavelength of each other. The Section 3 slab is $2\,\mathrm{mm}/500\,\mathrm{nm} = 4000$ wavelengths deep and about $10^6$ wavelengths across.
- **The loss term.** The sech shape needs the loss $L_3$ added by hand in (A42), with the field following the loss instantly (before (A43)). Without it, (A36)–(A38) conserve the energy (A39) and the Bloch length $Z^2 + R^2$, and the system oscillates.

*Request.* Give $g$, $\Omega$, $N$, $L_3$, $\theta_0$ and a dephasing time $T_2$, with $\tau_R = 2\pi/(g^2\Omega N) < T_2$.

**B2. The mechanism of the density dip in Figure 6.**

In (A86) the density moves with velocity $(e/m)A_i$, so the dip is first order in $e$. Inside the target box, the drive's divergence is $\nabla_i A_i = -(0.1/N_1 + 0.1/N_2) = -0.0083$.

A first-order estimate takes $A$ at the target and decaying as $e^{-\gamma_2 x^0}$. It gives a dip of $(e/m)\,|\nabla_i A_i|\,(1 - e^{-\gamma_2 x^0})/\gamma_2 = 0.25\,(1 - e^{-0.01\,x^0})$. That is 1.2, 4.5, 8.2, 15.8 and 21.6 % at $mx^0$ = 5, 20, 40, 100 and 200, close to your 1.3, 4.5, 9.1, 16 and 21 %.

In our rerun, halving $e$ from 0.3 to 0.15 reduces the dip at $mx^0 = 20$ by a factor of 1.7, and halving it again, to 0.075, reduces it by 1.9. A mechanism quadratic in $e$ would give 4.

So the pattern is the fluid carried by the longitudinal part of the drive. Its step shape is the shape of $\nabla_i A_i$ for piecewise-linear targets. It grows while the drive is on, and it is a continuous depth, not a binary value. Once the drive is off, nothing in (A86) moves the fluid back. But the model has no thermal noise either, so this says nothing about retention at 310 K (A5).

*Request.* Say whether this direct transport is the intended mechanism.

**B3. The only quantum term is called a distortion.**

After the truncations of (A62)–(A75), Appendix C is a classical charged fluid: (A69) and (A70) are the Madelung pair, plus Maxwell's equations with the added $M^2$ and $\gamma$. The only term carrying $\hbar$ is the $\nabla^2|\bar\varphi|/|\bar\varphi|$ term in (A70), (A81) and (A87). Section 5 attributes the "slight distortions" of Figure 6f to it.

*Request.* Run the same simulation with that term removed. Any difference in Figures 5 and 6 measures what is quantum in the result.

**B4. The waveguide sentence in Section 5.**

For a hollow conducting guide, a 21 nm cutoff passes only wavelengths *shorter* than 21 nm, so 500 nm light does not propagate. Treated as a dielectric rod of radius 12.5 nm with indices 1.5 and 1.33, the guide has $V = (2\pi a/\lambda)\sqrt{n_1^2 - n_2^2} \approx 0.11$ at 500 nm, and most of the mode lies outside the rod. Either way, "guide light from strong ultra-violet to near-infrared" does not follow from the 21 nm figure.

**B5. Section 5 has no variables for what it describes.**

The model's variables are $\varphi$ and $A_\mu$, with one unspecified fixed potential $U(x)$. No term takes a sensory input. No rule reads the stored pattern back. No term drives an action, and no variable stands for an experience.

The four steps you list (register, decipher, decide, encode) are a correct statement of what such an account must supply, and the paper itself calls the first of them "yet another mystery altogether". "One-to-one correspondence between holograms ... and our subjective experiences" needs two sets and a map; the paper has one set. The only reader of a pattern named in the paper is the external headset.

## C. Misprints

| Where | As printed | Should be |
|---|---|---|
| (A31) | $\chi_1$ on the right | $\chi_0$, as in (A34) |
| after (A47) | $\Omega \ge e^2 n/m$ | $\Omega^2 \ge e^2 n/m$, so $\Omega \ge 0.3\,m$ at the Section 4 values |
| (A52) | response labelled $\tilde A_i$ | the screened response, not the input $\tilde A_i$ |
| (A70) | $-\frac{e}{2m}(A_i - \partial_i\beta/e)^2$ | $+$, as in (A81), (A87) and the derivation; the free plane wave satisfies only the $+$ form |
| (A76), (A78) | $e\lvert\bar\varphi\rvert^2/m$ | $e^2\lvert\bar\varphi\rvert^2/m$, as in (A71) and (A82); with $e$, the continuity terms no longer cancel in A2 |
| (A88), (A89) | $-\partial_1^2 u_1$, $-\partial_2^2 u_2$ | $-\partial_2^2 u_1$, $-\partial_1^2 u_2$ (A3) |
| Section 3 | 2.5 PB, 30 TB, 20 meV, 2.4 eV | 2.6 PB, 31.25 TB, 18.5 meV, 2.48 eV |
| Section 6 | "celebrospinal" | "cerebrospinal" |

## D. What would make the results stand

In order:

1. a consistent set of field equations, with the gauge repaired (A1), the charge accounted for (A2) and the misprints corrected;
2. values of $g$, $\Omega$, $N$, $L_3$, $\theta_0$, $T_2$ and the mass scale $m$ for the proposed medium;
3. a write process for $|r+o|^2$, a read rule with an error rate, and a barrier that holds the pattern for a stated time;
4. the ablation run in B3;
5. only then, a mapping from patterns to reports, and the experiment your final sentence proposes.

## How to check this letter

`python 8_checks.py` replays every derivation and number above in about two minutes. `python 8_checks.py --rerun` repeats the Appendix C simulation and the Gauss-law measurement, which takes about 30 minutes. The paper's text, with every equation re-typeset, is `3_paper.md`.

With thanks for a paper that states its equations fully enough to be checked,

[name]
