# Claim register

This register covers the [paper review](holographic_brain_review.md) and the [discussion](discussion_record.md). A statement's appearance in a publication is evidence of what it says, not evidence that its physical interpretation is correct.

“Conditional” means the calculation follows under the listed assumptions. “Unresolved” means the supplied material does not settle the question. Numerical checks are finite examples unless identified as symbolic identities.

| ID | Claim or issue | Basis | Assessment | Next evidence needed |
|---|---|---|---|---|
| E01 | Appendix A's two gauge conditions and A7 permit nonzero charged density. | A6–A9; vanishing Gauss left side. | Inconsistent as printed. A retained background allows static density. | A consistent scalar-potential or transverse-field reduction. |
| E02 | The Appendix A objection invalidates the numerical scalar potential. | A55 versus A81/A87. | Does not follow; the background potential is retained in Appendix C. | Test Appendix C's own constraint. |
| E03 | A82/A84/A86 preserve matter-only Gauss's law. | Exact divergence identity. | Generally false with the additional response and drive terms. | Total medium/source charge model and constraint residuals. |
| E04 | A70, A76/A78 and A88/A89 agree with their parent equations. | PDF pages 21–22; substitution. | Sign, charge-coefficient and derivative-index discrepancies. | Implementation comparison and rerun. |
| E05 | The resonance condition is $\Omega\ge e^2\bar n/m$. | A13, A29, A47. | Dimensionally inconsistent as printed; require $\Omega^2\ge e^2\bar n/m$. | Mode measure and threshold treatment. |
| S01 | The reduced pulse has a sech envelope. | A40–A46. | Conditional on the stated loss-dominated approximation and parameters. | Biological parameter estimates, dephasing and direct emission predictions. |
| S02 | The displayed ansatz establishes axial guided emission. | A13 and the waveguide discussion. | Not established. | Boundary conditions, material indices and source-to-mode coupling. |
| O01 | Capacity is about 2.5 PB. | Equation 3 with supplied geometry and wavelength. | Arithmetic supported; recomputation gives 2.6 decimal PB. | Usable capacity after noise, losses and readout errors. |
| O02 | A52 contains an object-reconstruction term. | Expansion of $r|r+o|^2$. | Conditional; A51 supplies the density pattern. | A controller that writes that pattern and an optical readout. |
| O03 | The screening parameter 0.045 is an image amplitude. | Local response $T(n)$. | False. Uniform screening reconstructs no object image. | Spatially resolved diffraction and collection model. |
| N01 | Figures 4–6 demonstrate density control. | Published figures and text. | Reported for one displayed configuration; not independently reproduced here. | Corrected implementation, convergence, constraints and uncertainty. |
| N02 | Figure 6 demonstrates erasure. | Reported contrasts 1.3% to 21%. | Not supported; contrast increases over the shown samples. | A specified decoder and a post-write hold experiment. |
| Q01 | Omitting propagator terms is exactly coherent-product reconstruction. | Comparison of reconstruction maps. | Not established; first moments do not determine the marginals. | Explicit state family and projected evolution. |
| Q02 | A nonzero two-site correlation defect proves entanglement. | Separable correlated two-bit example. | False for mixed states. | An entanglement criterion appropriate to the state class. |
| Q03 | Projection bounds certify Figure 6. | Finite-system theorem hypotheses. | Not established. | Cutoff, subsystem decomposition, generator and observable residual bound. |
| R01 | Photon energy above $k_BT\ln2$ guarantees stable storage. | Distinction between reset cost and retention. | Does not follow. | Noise, barriers, readout and error probability versus hold time. |
| R02 | A one-year lifetime requires a 1.2 eV barrier. | Single-barrier Arrhenius calculation. | Conditional on a 1 ps attempt time and a mean-lifetime criterion. | Measured or derived escape mechanism; reliability target. |
| R03 | The 4 meV rotational scale is the memory barrier or simulated mass. | No such identification in the supplied model. | Unresolved; the identification must not be assumed. | Physical calibration. |
| P01 | Equal report values receive equal downstream verdicts. | Composition $E\circ q$. | Supported for the declared report channel and evaluator. | A richer channel if that distinction matters. |
| P02 | Every finite observer must merge states. | Pigeonhole principle. | Requires more admitted states than possible reports. | State/report sets and their sizes. |
| P03 | A simulation matching the full QM likelihood gains evidence from the same data. | Bayes's rule. | Equal positive likelihoods leave the prior odds unchanged. | A different joint prediction or intervention. |
| P04 | Equal single-trial marginals imply equal evidence from repeated observations. | Independent versus copied fair bits. | False without suitable dependence assumptions. | Full joint likelihoods. |
| P05 | The paper supports consciousness rendering unobserved reality. | Paper's scope versus the discussion claim. | No derivation or experiment supplied for that connection. | A defined rendering rule and distinguishing prediction. |
| P06 | An input-to-report association establishes a unique theory of experience. | Identifiability of alternative models. | Does not follow without further assumptions and tests. | A stated report model and competing predictions. |

## Operational definitions

For this review, an observation protocol specifies a state or hypothesis class, an experimental context, a report channel, record retention and a comparison rule. In a deterministic idealization the report is $q_c:X\to P$; noisy experiments use $p(r\mid x,c)$. A measurement additionally supplies a measurand, calibration, units where applicable, uncertainty and provenance.

These are declared conventions for evaluating claims. They do not replace the physical meaning of a detector or imply a theorem about consciousness. Acceptance of a report and authorization to act on it are separate decisions; no additional authority claim is needed for the electromagnetic calculations.

## Verification scope

The [checks](verification/review_checks.py) cover algebraic constraints, the inverse-controller discrepancy, dimensional threshold, finite projection examples, conditional retention arithmetic, report-channel counterexamples and public-reply lengths. They do not measure tissue properties, reproduce the paper's lattice run or compile the repository's Lean files.
