# Tests and research directions

The immediate target is a complete, reproducible write–hold–read calculation. It should connect the light source, medium, controller and optical decoder, with units and error criteria fixed before interpreting the result.

## 1. Tests to run next

| Priority | Test | Procedure | Decisive output |
|---|---|---|---|
| 1 | Complete memory cycle | Write several known patterns; stop the drive; hold for declared intervals; illuminate with a specified reference; decode the reconstructed image. Include a no-write control and a phase-scrambled reference. | Reconstruction error and bit-error rate versus hold time, with uncertainty across noise realizations. Specify the tolerated error before the run. |
| 1 | Charge consistency | Derive the total charge/current of the condensate, medium and external drive. Initialize Gauss's law consistently and monitor it with the evolution's own discrete operators. | $L^2$ and $L^\infty$ constraint residuals that decrease with refinement; a conserved total charge or accounted boundary flux. |
| 1 | Controller reproduction | Compare printed A88/A89 with the inverse derived from A82/A84. Test longitudinal, transverse and mixed targets, then the published rectangle. | Static residuals and reconstructed Figures 4–6 for each equation choice. Identify which implementation matches the published result. |
| 1 | Numerical convergence | Use at least three spatial resolutions at fixed physical size and separate time-step refinements. Preserve the same physical target rather than its cell count. | Observed convergence order for contrast, image error and constraint residuals. Include number balance, density positivity and driven energy balance. |
| 2 | Optical transport | Solve the cylindrical Maxwell boundary problem with complex material response and an explicit emitter. Include lumen, wall and exterior. | Propagation constant, confinement, attenuation length and source-to-mode coupling over wavelength. |
| 2 | Physical units | Give the interpretation and value of $m$, effective charge, density, $M^2,\gamma,v$, layer thicknesses and boundary conditions. | One consistent table converting lattice length, run duration and drive strength to physical units. |
| 2 | Retention and noise | Start from a written state and propagate with a specified bath/noise model after the drive stops. Test several patterns and noise strengths. | Failure probability versus hold time. Fit an Arrhenius law only if its assumptions and fit are supported. |
| 2 | Observable error from mean field | Define a finite quantum model and cutoff; compare exact and reduced evolution on small systems; increase the cutoff and cluster size. | Error bounds or convergence evidence for the actual readout observable, alongside state/correlation diagnostics. |
| 2 | Discriminating quantum prediction | Specify a classical optical/stochastic baseline with comparable parameters. Select an observable the two models predict differently. | A predicted separation larger than model and measurement uncertainty; intensity matching alone is insufficient. |
| 3 | Empirical report mapping | Once a physical mechanism is established, define the intervention, report choices, blinding and competing predictions. | A held-out input-to-report confusion matrix and evidence distinguishing the proposed mechanism from alternatives. |

The first four tests should precede larger capacity claims. A negative result is useful if it identifies a specific failed link: field delivery, pattern formation, retention or decoding.

## 2. Lines of reasoning worth pursuing

### A. Replace geometric capacity with operational capacity

Let $B$ denote the written message and $Y_T$ the decoded observation after hold time $T$. Estimate the transition probabilities $p(Y_T\mid B)$. For a declared set of admissible writes, define
$$
C_{\rm op}(T)=\max_{p(B)} I(B;Y_T).
$$
This is a capacity for the specified channel, alphabet, resource constraints and hold time. A finite tested alphabet gives evidence about that tested channel; it does not certify all possible encodings.

This separates the number of ideal optical modes from information recoverable under noise. It also gives a direct role to the retention and report maps: differences count as stored information only to the extent that the decoder can resolve them.

### B. Test whether the reduced state predicts its own future

For a proposed report $q$ and full evolution $T_t$, ask whether
$$
q(x)=q(y)\quad\Longrightarrow\quad q(T_t x)=q(T_t y).
$$
If this fails, the chosen report is insufficient for autonomous reduced dynamics. Density-only evolution already fails this test when phase gradients change the current. Repeat it for density plus gauge-invariant velocity, then for additional correlations.

In a noisy model the analogous requirement concerns conditional future distributions, not just mean trajectories. Seek the smallest additional observable that restores predictive accuracy at a stated tolerance. This is a concrete connection to observer completion.

### C. Derive a consistent effective medium

Start from a conserved total current or a gauge-invariant effective action, then derive the scalar, longitudinal and transverse response together. Determine whether $M^2$ describes a condensate contribution, an independent ionic response or an approximation to a frequency-dependent kernel.

Compare the full kernel with the local mass-and-damping approximation on the frequencies used for writing and readout. If a bath is invoked at a stated temperature, specify its associated fluctuations as well as its damping. This resolves the charge-accounting question and gives a physical noise model for retention.

### D. Bound the observable that makes the memory useful

A large state-space error need not spoil a particular image measurement. Conversely, a visually small density error can cross a decoding threshold. Use the readout operator or reconstruction functional to define the error target first.

For finite Hamiltonian models, derive a residual bound for the actual approximate trajectory. Use edgewise projection bounds only when the decomposition and projected evolution satisfy their hypotheses. Track cutoff error separately from dynamical approximation and numerical integration error.

### E. Identify a prediction unique to the proposed mechanism

Compare explicit models, not labels such as “quantum” and “classical.” Possible observables include emitted-field correlations, dependence on phase preparation, collective scaling and response to dephasing. Which of these distinguishes the models depends on the baseline; none is automatically a quantum witness.

Likewise, a cognitive interpretation needs a prediction beyond “an intervention changes reports.” A report association can establish an operational map while leaving several physical or interpretive explanations compatible with it.

## 3. Naming conventions

Use descriptive names for the mathematical object, experiment or document purpose. Keep revision dates in document metadata and history rather than filenames.

| Purpose or current expression | Recommended name | Reason |
|---|---|---|
| Main paper critique | `holographic_brain_review.md` | Names the subject and function. |
| Electromagnetic and thermal calculations | `field_constraints_and_retention.md` | Names the two technical topics. |
| Review objections and counterexamples | `assumption_counterexamples.md` | Makes the reusable content easy to find. |
| Claims ledger | `claim_register.md` | Stable claim IDs can link prose to checks. |
| Scope analysis | `scope_analysis.md` | Separates the public claim from the paper's results. |
| Historical exchange | `discussion_record.md` | Distinguishes quotations from proposed replies. |
| Public drafts | `public_replies.md`, `public_reply_variants.md` | Makes intended use clear. |
| “Entanglement defect” on mixed states | **Correlation defect** | A separable state can have a nonzero value. |
| “Coherent projection” without a map | **First-moment report** or **coherent-state reconstruction** | Distinguishes information extraction from state assignment. |
| “Memory capacity” from geometry alone | **Ideal holographic capacity estimate** | Identifies the assumptions behind the number. |
| Density pattern during writing | **Written density pattern** | Retention and retrieval remain separate tests. |
| Demonstrated storage and retrieval | **Operational memory**, with alphabet, decoder and hold time | States what has actually been demonstrated. |
| “Observer” in a test protocol | **Observation protocol** or **report channel**, as appropriate | Avoids conflating a person, detector, rule and experience. |
| “Binary hologram” before threshold/readout validation | **Density mask** or **transmission mask** | Describes the computed object without claiming successful decoding. |

Keep established programme names, including Witnessed Difference Programme and Projection Obstruction, when referring to those bodies of work. Expand them at first use. Do not introduce a new programme acronym for this case study.

## 4. Verification discipline

Use descriptive test names tied to claim IDs, explicit assumptions and numerical tolerances. A missing fixture, dependency or required result must fail the run. Test a known failing example as well as passing examples. Preserve source equations separately from proposed corrections.

The supplied [verification script](verification/review_checks.py) implements the finite checks available from these documents. The full lattice reproduction, material calibration, noise simulation and experimental tests above remain proposed work.
