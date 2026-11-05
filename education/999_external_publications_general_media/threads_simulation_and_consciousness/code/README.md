# code: continuum checks on the paper

The checks here use the paper's own equations: full calculus, with fields on the continuum.

| Script | What it checks |
|---|---|
| `adversarial_review_checks.py` | 1a: Appendix C keeps Gauss's law in the pure Maxwell part, and M², γ and v break it. 1b: the e/m misprint in (A76)/(A78). 1c: the initial data and the uniform background. 1d: the targets (10)–(11) are curl-free. 2: Landauer numbers and the energy barrier needed for one-year retention. 3: capacity arithmetic. |

| `retest_checks.py` | R1: reruns the Section 4 / Appendix C simulation at the paper's parameters and measures the Gauss-law residual against the density change (numerical, floating point). R2: the Appendix A transition current is not divergence-free. R3: equal reports with Bayes factor 2. R4: a finite observer with \|P\| = \|X\| separates every state. Used in `../retest_log.md`. |

Run with `python code/adversarial_review_checks.py` from the folder above. It needs sympy. `python code/retest_checks.py [t_end] [input_max]` also needs numpy. The default run, to m x0 = 40, takes about 30 minutes.

The deeper continuum critique of the paper is being built in a separate thread, and its scripts will land here.
