# Claim Ledger — Paper QM_122: Finite Hilbert Boundary from Primitive Difference

**Paper key:** `003_quantum_foundations/122_finite_hilbert_boundary_from_primitive_difference`
**Date:** 2026-08-20
**Version:** v0.1.16
**AuthorityEffect:** None

This ledger records the Hilbert walk (CODA PR #56), the
shared-frame follow-up, the carrier-thread follow-up, the
sign-exclusion extra, the two-level Gauss-integer matrix
recovery, the finite-\(n\) Gauss-integer matrix recovery, the
Gleason dim-2 obstruction, the remaining \(M_n(\mathbb{C})\) extras, the drop-one of that frozen extra list,
the one-carrier thread with H014 obstruction, and the
same-host combining-systems rival. Prose does not add theorems. Lean file tags such as
`H006` are locators.

Lean root: `lean4/genx/_work_review_queue/fable_hilbert_walk_20260819/`
Baseline receipt: `evidence/BUILD_RECEIPT.md`
Frame-additivity delta: `evidence/FRAME_ADDITIVITY_DELTA_RECEIPT.md`
Carrier-thread delta: `evidence/CARRIER_THREAD_DELTA_RECEIPT.md`
Same-contract delta: `evidence/SAME_CONTRACT_DELTA_RECEIPT.md`
Open list: paper §7

## Claim index

| ID | Type | Statement | Status | Where |
|---|---|---|---|---|
| QM-122-C0 | THEOREM_DEFINITION | This paper does not derive quantum mechanics, Hilbert space, uniqueness of the Born square, uniqueness of tensor product, channels, or continuous time. It mints no authority. | scope fence | refusal box, §6 |
| QM-122-C1 | LEAN4_PROOF | A finite presented carrier uses the report-fiber primitive difference. Finiteness is an extra assumption. | proved | `H000` |
| QM-122-C2 | LEAN4_PROOF | Nonnegative integer weights at a declared scale exist. This is not the rational simplex. | proved | `H001` |
| QM-122-C3 | LEAN4_PROOF | Pushing those weights along any report update preserves total mass. Descent from an ambient update still requires preserving report fibers. Checking only selected representatives is not enough. | proved | `H002` |
| QM-122-C4 | LEAN4_PROOF | Determinism does not imply reversibility. | proved | `H003.collapse_not_reversible` |
| QM-122-C5 | LEAN4_PROOF | Formal linear combinations need an imported coefficient pack. The trunk does not choose the pack. | proved | `H004` |
| QM-122-C6 | LEAN4_PROOF | A declared orthonormal inner product is extra structure, not unique. | proved | `H005.gram_not_unique` |
| QM-122-C7 | LEAN4_PROOF | Every reversible report update extends to a form-preserving isometry with two-sided inverse. Over the integers, with a positive-definite form, it is an isometric automorphism. Not a Hilbert unitary. Strictly smaller than the isometry group. | proved | `H006` |
| QM-122-C8 | LEAN4_PROOF | The same pipeline runs over the integers; the complex numbers are not selected. (Asked over the reals; this host has no reals.) | proved, host-weakened | `H007.real_pipeline_complete` |
| QM-122-C9 | LEAN4_PROOF | Phase-blind squares: \((1,1)\) and \((1,-1)\) have equal weights. Global phase stays in the fiber; relative phase need not. | proved | `H008`, `H009` |
| QM-122-C10 | LEAN4_PROOF | Mixing separates that fiber. No function of the phase-blind weights reproduces the mixed readout. The leftover runs over the integers with only plus and minus one. | proved | `H010` |
| QM-122-C11 | LEAN4_PROOF | The leftover does not select the circle group or the complex numbers. Under the named extra that the phase carrier is not of exponent two, \(\{+1,-1\}\) is excluded. Gaussian units and a three-cycle meet the extra. The circle stays an import. | proved + imported | `H011Circle.sign_fails_connectedness_shadow`, `H011Circle.sign_excluded_circle_still_imported`; paper §7.1 item 3 |
| QM-122-C12 | LEAN4_PROOF | A bilinear pairing exists. A positive fourth-power readout is not a rescaling of the square. `H013Frame.fourth_power_dies_under_frame_additivity` proves the fourth-power candidate violates the formal scale-2 frame-total constraint. The square agrees (10 and 10) only on the two exhibited frames; global frame additivity is not proved. Gleason’s hypotheses remain imported. | proved + open | `H013`, `H013Frame.fourth_power_dies_under_frame_additivity`, `evidence/FRAME_ADDITIVITY_DELTA_RECEIPT.md`; §7.1 item 2 |
| QM-122-C13 | LEAN4_PROOF | The product host has a non-product vector. The direct-sum host is exhausted by its parts. On Bool × Bool, a bilinear integer-homogeneous Kronecker-normalized map equals the pointwise product. A weaker same-host combining interface has a rival. Hilbert-tensor uniqueness is not proved. | proved | `H014`, `H014Bilin.embed_eq_tensor`, `H014Interface.two_combinings_share_interface_and_disagree`; paper §7.1 item 4 |
| QM-122-C14 | LEAN4_PROOF | Collapse has no same-basis isometry. Two reversible dilations can share one reduction. Continuous interpolants after complex coefficients exist at scale 4 and are not unique. The two-state toggle has no report-level square root. | proved | `H015`, `H016` |
| QM-122-C15 | LEAN4_PROOF | The assembly theorem is the conjunction of the selected witnesses, not one implication about a single carrier. | proved | `H017`; §3.4 |
| QM-122-C16 | THEOREM_DEFINITION | Remaining work is paper §7 and docs/STACK.md. | open | §7 |
| QM-122-C17 | LEAN4_PROOF | Superposition is the phase-blind fiber on the H000 report set. Adapter QM_060. Not a circle group. | proved | `HWCarrierThread.superposition_is_the_phase_blind_fiber`; §8 |
| QM-122-C18 | LEAN4_PROOF | Entanglement needs a tensor host: a correlated integer vector is not a product. Adapter QM_070/QM_071. | proved | `HWCarrierThread.entanglement_needs_a_tensor_host`; §8 |
| QM-122-C19 | THEOREM_DEFINITION | SUSY is unassigned. No leftover on this walk selects supercharges. | scope fence | §8 |
| QM-122-C20 | THEOREM_DEFINITION | SU(3)×SU(2)×U(1) is unassigned. The circle is still an import. | scope fence | §8 |
| QM-122-C21 | LEAN4_PROOF | Amplitudes on the H000 presented carrier ride along that carrier’s presentation. Same-report points agree. Pushing phase-blind weights back recovers twice the report-level weight. Mixing leftover is that report end’s leftover. Not the whole walk on one object. | proved | `HWCarrierThread.one_carrier_through_mixing_leftover`; §7.1 item 1 |
| QM-122-C22 | LEAN4_PROOF | On Bool × Bool, any bilinear integer-homogeneous Kronecker-normalized product map equals the pointwise product. Cartesian product of report sets is imported. Direct sum is a different host. | proved | `H014Bilin.embed_eq_tensor`; §7.1 item 4 |
| QM-122-C23 | LEAN4_PROOF | The declared dual pairing and the report-swapped pairing of the same quadratic weights share every unit-effect total, are nonnegative on nonnegative effects, and disagree on the false-indicator at amplitudes (2,1). Gleason uniqueness is not this theorem. | proved | `H013Contract.two_effect_rules_share_unit_total_and_disagree`; §7.1 item 5 |
| QM-122-C24 | LEAN4_PROOF | Under the extra “not of exponent two”, the sign group is excluded. Gaussian units and a three-cycle meet the extra. Mixing leftover still runs on plus-and-minus-one without the extra. Continuity of a one-parameter phase group remains a hypothesis. The circle is not constructed. | proved + imported | `H011Circle.sign_excluded_circle_still_imported`; §7.1 item 3 |
| QM-122-C25 | LEAN4_PROOF | Under named extras (GaussInt coefficients, two-point Bool reports, additive homogeneous endomorphisms), End of that module is \(M_2(\mathbb{Z}[i])\). Composition is matrix product. Conjugate transpose is the pairing adjoint. Ordinary Pauli X, Y, Z live here; Y is not an integer matrix. This is not \(M_n(\mathbb{C})\). | proved | `H017Matrix.two_level_gauss_matrix_algebra`; §7.2 |
| QM-122-C29 | LEAN4_PROOF | Under named extras (GaussInt coefficients, a finite enumeration of a report set Q, additive homogeneous endomorphisms), End of that module is \(M_n(\mathbb{Z}[i])\) with \(n = |Q|\). The matrix is unique. Composition is matrix product. Conjugate transpose is the pairing adjoint. Instantiated at \(n = 2\) and \(n = 4\). This is not \(M_n(\mathbb{C})\). | proved | `H017Fin.finite_gauss_matrix_algebra`; §7.2 |
| QM-122-C30 | LEAN4_PROOF | A three-label cardinality surrogate (`3 ≤ \|Q\|`) is false on Bool, and there is no three-element orthonormal report-basis frame. That is not a bridge to `GleasonPack`. Born uniqueness under the full Gleason package (R7) stays imported. | proved + imported | `H017Gleason.two_label_host_not_gleason_dimension`, `H017Gleason.gleason_pack_uniqueness_still_imported`; §7.2 |
| QM-122-C31 | LEAN4_PROOF | Obstruction evidence on this host, not a requirements interface for ordinary \(M_n(\mathbb{C})\): GaussInt is not a field; a self-adjoint GaussInt matrix need not have a GaussInt eigenvalue; the cardinality surrogate fails on Bool; the toggle has no report-level square root; the sign-exclusion extra does not select the circle; a same-host combining interface has a rival; Pauli Y is not an integer matrix. Completeness of \(\mathbb{C}\), CPTP, unique Hilbert tensor, the circle, continuous time, and Gleason at \(n \ge 3\) are not conjuncts. Not a drop-one count and not \(M_n(\mathbb{C})\). | proved + open | `H017Extras.remaining_extras_for_ordinary_mnC`; §7.2 |
| QM-122-C38 | COMPUTATION | Python dual of named existing Lean theorems (collapse not reversible; two Bool reversibles; exhaustive classifications of four identity dilations and four collapse dilations; exact mod-two obstruction showing \(1+i\) is not a unit; dumpRight ≠ tensor; no report half-step; mix doubles total on the two witnesses). Not Gleason. Not \(M_n(\mathbb{C})\). Not a Lean theorem. | computed | `qm122_lib/qm122_dual.py`, `tests/test_qm122_dual.py`; `H017Finish.finish_pythonDual_outside_lean` |
| QM-122-C37 | THEOREM_DEFINITION + LEAN4_PROOF | Declared finish table for the eight frozen extras, paired with narrower proved host facts: field \(\mathbb{C}\), spectral extra, and continuous time refused on this host; CPTP, Gleason uniqueness, Hilbert-tensor uniqueness, and the circle imported; Python dual outside Lean. Collapse non-reversibility and failure of a same-basis isometry are not CPTP obstructions. The table is not a requirements or necessity theorem. SUSY and \(\mathrm{SU}(3)\times\mathrm{SU}(2)\times\mathrm{U}(1)\) unassigned. Historical drop-one OPEN verdicts untouched. Not \(M_n(\mathbb{C})\). | declared metadata + proved facts | `H017Finish.remaining_import_list`; `H017Finish.finish_is_not_ordinary_mnC` |
| QM-122-C36 | LEAN4_PROOF | Under the declared convention that the ancilla is prepared at false, exactly four two-sided-invertible maps on Bool × Bool send the prepared slice to collapse on the report coordinate. Not CPTP. Not identity dilations. Convention is declared, not derived. | proved | `H015CollapseDilations.four_reversible_dilations_of_collapse`; FRONTIER R6b |
| QM-122-C35 | LEAN4_PROOF | At two labels, a reversible report map is identity or toggle, and its permutation lift is identity or coordinate-swap. The Gaussian-integer isometry that multiplies a swap by \(i\) is outside that pair. Not a Hilbert unitary group. Not a count of all linear isometries of \((\mathbb{Z}[i])^2\). | proved | `H006Envelope.two_permutation_lifts_envelope_strict`; FRONTIER R4 |
| QM-122-C34 | LEAN4_PROOF | For every GaussInt amplitude vector on Bool, mixing doubles total weight. The two-witness check is the special case. Not a probability interpretation. Not uniqueness of the quadratic readout. | proved | `H010Scale.mix_doubles_total_any`; FRONTIER R1 |
| QM-122-C33 | LEAN4_PROOF | Exactly four two-sided-invertible maps on Bool × Bool that are the identity on the report coordinate. Classified by whether each report fiber flips its ancilla. `H015.dil1` and `H015.dil2` are two of them. Not CPTP. Not dilations of collapse. | proved | `H015DilationCount.four_reversible_dilations_of_report_identity`; FRONTIER R6a |
| QM-122-C32 | LEAN4_PROOF | Declared census of the frozen extra list at merge SHA `dba1434b`: eight extras, no duplicates, every extra appears. Three extras are classified lost with current-host obstruction evidence (GaussInt is not a field; a self-adjoint GaussInt matrix need not have a GaussInt eigenvalue; the toggle has no report-level square root). Necessity of Gleason uniqueness at \(n \ge 3\), CPTP, uniqueness of Hilbert tensor, the circle group, and a Python dual is OPEN. Not an assumption-removal interface. Completeness of \(\mathbb{C}\) is not the invertibility theorem. Not \(M_n(\mathbb{C})\). No Python dual. | proved + open | `H017ExtrasDropone.drop_one_count`, `H017ExtrasDropone.drop_one_is_not_ordinary_mnC`; §7.2 |
| QM-122-C26 | LEAN4_PROOF | From one H000 presented carrier, the report-end walk through H016 is an implication about that carrier. The H014 correlation vector is not a report of that carrier: it splits a same-report fiber. The missing extra is a second presented carrier whose reports are a product of two label sets. H017 remains a conjunction. | proved | `HWFullThread.from_one_presented_carrier`, `HWFullThread.bell_not_along_presentation`; §7.1 item 1 |
| QM-122-C27 | LEAN4_PROOF | On this host, a combining-systems interface (bilinear, each pair of report-basis vectors occupies some composite report) is inhabited by the pointwise product and by a dump-the-right-report map that disagrees. Direct sum is not used. Injectivity of the tagging recovers the pointwise product along the tagging. Hilbert-tensor uniqueness is not this theorem. | proved | `H014Interface.two_combinings_share_interface_and_disagree`, `H014Interface.injective_tag_recovers_product`; §7.1 item 4 |
| QM-122-C28 | LEAN4_PROOF | Exact fractions as integer pairs modulo cross-multiplication form a commutative *-ring pack without classical choice. Half plus half is one. Half is neither zero nor one. Stock Lean.Rat remains choice-tainted. Not Lean.Rat, not a real field, not uniqueness of the mass carrier. | proved | `H001Rats.choice_free_fractional_weights`, `H001Rats.fracPack`; §7.1 item 6 |

## Audit

The assembly is a conjunction, stated as such. The envelope is an isometry, not a Hilbert unitary. The fourth-power readout is not uniqueness of the Born square. The bilinear Kronecker uniqueness on Bool × Bool is not uniqueness of tensor product as a way to combine systems. Two pairings that share a unit-effect total are not Gleason non-uniqueness. The three-lift uniqueness check is a toy, not a theorem of this Lean target. The finite Gauss-integer matrix algebra is not \(M_n(\mathbb{C})\). A three-label cardinality surrogate failing on Bool is not a Gleason theorem and is not discharge of R7. Host obstruction facts are not a requirements interface for ordinary \(M_n(\mathbb{C})\). A drop-one count with five OPEN necessity verdicts is not \(M_n(\mathbb{C})\). Two permutation lifts at n=2 are not the isometry group of \((\mathbb{Z}[i])^2\). Four reversible collapse dilations under a declared ancilla convention are not CPTP.

## Remaining work (English names; details in §7)

| Need | Blocks a later revision? |
|---|---|
| One carrier through mixing leftover (presentation consumed) | closed |
| One carrier through the whole walk (implication plus H014 obstruction) | closed |
| Fourth-power rival vs shared-frame totals (this rival, this host) | closed |
| Rule out plus-or-minus-one under “not of exponent two”; circle stays an import | closed for the extra; circle still imported |
| Bilinear Kronecker product unique on Bool × Bool | closed |
| Combining-system uniqueness beyond that interface | closed for this interface (rival); Hilbert tensor still extra |
| Born pairing under positivity and unit-effect total | closed |
| Three-label cardinality surrogate on Bool | closed as obstruction; not GleasonPack |
| Gleason uniqueness under the full package (R7) | yes (imported) |
| Rational weights without classical choice (exact fractions) | closed for this pack; stock Rat still priced |
| Two-level Gauss-integer matrix algebra with Pauli generators | closed for \(M_2(\mathbb{Z}[i])\) |
| Finite enumerated Gauss-integer matrix algebra | closed for \(M_n(\mathbb{Z}[i])\), \(n = |Q|\) |
| Drop-one of the frozen extra list (eight extras; three lost named properties, five OPEN) | closed as a counted list; five extras still OPEN on necessity; not \(M_n(\mathbb{C})\) |
| Reversible dilations of the report-identity on Bool × Bool | closed: exactly four |
| Mixing scale law for every GaussInt amplitude vector on Bool (R1) | closed |
| Permutation lifts at two labels (R4) | closed: identity and coordinate-swap; swapI sits outside |
| Reversible dilations of collapse under prepared-ancilla-false (R6b) | closed: exactly four; not CPTP |
| Finish table for remaining extras (refuse / imported / dual-outside-Lean) | closed as a table; not \(M_n(\mathbb{C})\) |
| Ordinary \(M_n(\mathbb{C})\) | yes (not recovered) |
