# Everett and many-worlds: measurement, records, and what would refute it

Working notes, 2026-11-02. Every **[D]** claim is checked numerically by the scripts in this folder; every **[L]** claim names a kernel-checked Lean declaration in `lean4/`.

| File | Content |
|---|---|
| [double_slit_measurement_and_interpretation.md](double_slit_measurement_and_interpretation.md) | Two-page public note: double slit, which-path records, decoherence vs collapse (checks: `check_math.py`) |
| [double_slit_research_receipt.md](double_slit_research_receipt.md) | Sources, audited proof status, citations verified for that note |
| [everett_from_weights_math_only.md](everett_from_weights_math_only.md) | Weights → amplitudes → records → relative states; verdict "worlds: not needed, not excluded" (checks: `check_everett.py`) |
| [everett_draft_audit.md](everett_draft_audit.md) | Line-by-line audit of an external draft of the same derivation |
| [marbles_to_everett.md](marbles_to_everett.md) | Classroom version |
| [where_to_contest_multiverse_realism.md](where_to_contest_multiverse_realism.md) | Where Deutsch's multiverse realism can be contested |
| [refuting_everett_assessment.md](refuting_everett_assessment.md) | What a decisive result against Everett would have to be; Deutsch–Wallace core classified by scalar field (checks: `check_conjugate_measure.py`) |
| [referee_report_2026-11-02.md](referee_report_2026-11-02.md) | Independent referee report on revision 2 of the assessment |
| [threads_replies.md](threads_replies.md), [threads_many_worlds.md](threads_many_worlds.md) | Short public replies (≤ 500 characters; counts by `count_*.py`) |
| [test_measurement_boundaries.py](test_measurement_boundaries.py) | Regression witnesses: unequal-weight visibility, exact unitary dilation of dephasing, and coherent reversal of distributed records |

Run checks from this folder with `python -I -X utf8`, e.g. `python -I -X utf8 test_measurement_boundaries.py`. Install NumPy for the numerical scripts and SciPy to include the optional linear-program check in `check_everett.py`: `python -m pip install numpy scipy`. The `everett-checks` workflow runs the seven regression tests and all six existing scripts, including the SciPy check.

The regression checks combine exact rational matrix arithmetic for the dephasing dilation with finite numerical interference and record examples. They do not establish a general Lean theorem or experimental evidence for collapse. In particular, equal record overlap alone does not fix visibility without the path weights; reduced-system dephasing can have a unitary dilation; and environmental decoherence is effectively irreversible when the records cannot be controlled, rather than permanent by a unitary law.
