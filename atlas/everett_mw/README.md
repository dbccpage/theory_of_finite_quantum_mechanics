# Everett and many-worlds: measurement, records, and what would refute it

Working notes, 2026-11-02. Every **[D]** claim is checked numerically by the scripts in this folder; every **[L]** claim names a kernel-checked Lean declaration in `lean4/`.

| File | Content |
|---|---|
| [double_slit_measurement_and_interpretation.md](double_slit_measurement_and_interpretation.md) | Two-page public note: double slit, which-path records, decoherence vs collapse (checks: `check_math.py`) |
| [double_slit_research_receipt.md](double_slit_research_receipt.md) | Sources, audited proof status, citations verified for that note |
| [everett_from_weights_math_only.md](everett_from_weights_math_only.md) | Weights → amplitudes → records → relative states; verdict "worlds: not needed, not excluded" (checks: `check_everett.py`) |
| [everett_draft_audit.md](everett_draft_audit.md) | Line-by-line audit of an external draft of the same derivation |
| [Two printable sheets on Everett](../../education/l1_to_many_worlds/codex_primitive_to_hamilton_noether/everett/README.md) | A two-route experiment with a reversible record and Everett’s reading of it |
| [marbles_to_everett.md](marbles_to_everett.md) | Classroom version |
| [where_to_contest_multiverse_realism.md](where_to_contest_multiverse_realism.md) | Where Deutsch's multiverse realism can be contested |
| [refuting_everett_assessment.md](refuting_everett_assessment.md) | What a decisive result against Everett would have to be; Deutsch–Wallace core classified by scalar field (checks: `check_conjugate_measure.py`) |
| [referee_report_2026-11-02.md](referee_report_2026-11-02.md) | Independent referee report on revision 2 of the assessment |
| [threads_replies.md](threads_replies.md), [threads_many_worlds.md](threads_many_worlds.md) | Short public replies (≤ 500 characters). Draft counters reject oversized or malformed posts. `threads_replies.md` is kept as posted; `threads_many_worlds.md` is a draft |
| [review_2026-11-02.md](review_2026-11-02.md) | Pre-publication review of every file in this folder: findings and what changed |
| [test_measurement_boundaries.py](test_measurement_boundaries.py) | Regression witnesses: unequal-weight visibility, exact unitary dilation of dephasing, and coherent reversal of distributed records |
| [test_post_counters.py](test_post_counters.py) | Counter regressions: complete multiline posts, malformed or missing sections, duplicate posts, count mismatches, Unicode, and EOF |

Run checks from this folder with `python -I -X utf8`, e.g. `python -I -X utf8 test_measurement_boundaries.py`. Install NumPy for the numerical scripts and SciPy to include the optional linear-program check in `check_everett.py`: `python -m pip install numpy scipy`. The `everett-checks` workflow runs both regression suites and all six existing scripts, including the SciPy check.

The draft counters use Python `len()` on the complete post body, retaining internal line breaks and blank paragraphs with LF line endings. Numbered posts end at the next heading; the final sources section is excluded. The memo and pocket posts are selected by their section headings; quote markers and the separate trailing count annotation are excluded. Both counters verify the stated count and the 500-character limit, and reject missing or malformed sections. Keep annotations on their own line, separated from the post by a blank line.

The regression checks combine exact rational matrix arithmetic for the dephasing dilation with finite numerical interference and record examples. They do not establish a general Lean theorem or experimental evidence for collapse. In particular, equal record overlap alone does not fix visibility without the path weights; reduced-system dephasing can have a unitary dilation; and environmental decoherence is effectively irreversible when the records cannot be controlled, rather than permanent by a unitary law.
