# code: continuum checks on the paper

The checks here use the paper's own equations: full calculus, with fields on the continuum.

| Script | What it checks |
|---|---|
| `adversarial_review_checks.py` | 1a: Appendix C keeps Gauss's law in the pure Maxwell part, and M², γ and v break it. 1b: the e/m misprint in (A76)/(A78). 1c: the initial data and the uniform background. 1d: the targets (10)–(11) are curl-free. 2: Landauer numbers and the energy barrier needed for one-year retention. 3: capacity arithmetic. |

Run with `python code/adversarial_review_checks.py` from the folder above. It needs sympy.

The deeper continuum critique of the paper is being built in a separate thread, and its scripts will land here.
