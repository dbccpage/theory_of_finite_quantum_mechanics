# QM-208 Quadratic ℓ² Readout and Cross-Term Interference: the Finite Map

**Scope:** research note for `006_finite_qm`; not part of the manuscript, not a claim promotion. Companion to `phase_fiber_holonomy_bridge_finite_map.md`.
**Code:** `python/finite_qm/use_cases/quadratic_readout_control.py`, tests in `tests/e2e/test_e2e_quadratic_readout_control.py` (8 tests).
**Status marks used:** PROVED (argument given here, finite and checkable), COMPUTED (exact arithmetic in Q(ζ₁₂), replayable), IMPORTED (added structure that nothing finite here produces), CONJECTURED (none in this note).

Authority status: none. This note changes no admitted claim.

## 1. The question

QM-208 names the second of the five imports between finite nonnegative weights and complex quantum mechanics: the readout of an amplitude is quadratic, P_v = |c_v|², and two reports that reach one sink combine by adding amplitudes and then squaring, which produces the cross term 2 Re(c₁ conj(c₂)). The task is to research and discover the finite map to this problem.

The answer has the three-layer shape of the QM-207 note. The finite invariant is computed exactly; the completion column is empty for this import; the residual import is the composition rule itself. Section 6 has the table.

## 2. What ℓ¹ provides

Weights w : V → Q≥0 with total W > 0 give probabilities P_v = w_v / W. The readout is linear in the weights. Two reports with weights w₁, w₂ at one sink combine as w₁ + w₂.

**Theorem 2.1 (ℓ¹ readout is additive). PROVED.** For the ℓ¹ readout R(c) = |c| on amplitudes, or directly on weights, I₂(a, b) = R(a + b) − R(a) − R(b) is zero when the two contributions are weights added as nonnegative numbers. COMPUTED: `l1_readout` returns I₂ = 0 on all four fixture pairs (`l1_additive_on_all_pairs`).

So ℓ¹ supplies a single phase-blind datum of degree two in the amplitude, the weight itself, and an additive composition rule. It supplies no cross term.

## 3. The finite invariant

Fix the conductor N = 12. The fiber μ₁₂ acts on an amplitude by c ↦ ζc.

**Theorem 3.1 (phase-blind monomials). PROVED.** The monomial c^a conj(c)^b is invariant under every ζ ∈ μ_N exactly when N divides a − b. For total degree a + b < N this means a = b. Proof: (ζc)^a conj(ζc)^b = ζ^{a−b} c^a conj(c)^b, and ζ^{a−b} = 1 for every ζ ∈ μ_N iff N | a − b. COMPUTED: of the 14 monomials with 1 ≤ a + b ≤ 4, the phase-blind ones are exactly (1, 1) and (2, 2) (`blind_are_exactly_diagonal`). The census refuses a degree bound at or above the conductor, where the statement would fail.

Consequence. A phase-blind polynomial readout of degree at most 4 with R(0) = 0 lies in the two-parameter family R_{α,β}(c) = α|c|² + β|c|⁴.

**Theorem 3.2 (Sorkin selection inside the family). PROVED.** Write I₃[R](a, b, c) = R(a+b+c) − R(a+b) − R(a+c) − R(b+c) + R(a) + R(b) + R(c). Then I₃ is linear in R; I₃[|·|²] vanishes identically, since |x|² = x conj(x) is a quadratic form and the third difference of a quadratic form is zero; and I₃[|·|⁴](1, 1, 1) = 81 − 3·16 + 3 = 36. Hence I₃[R_{α,β}] = β · I₃[|·|⁴] vanishes on every set of triples that contains (1, 1, 1) exactly when β = 0. COMPUTED on the 16-point grid α ∈ {1, 1/2, 0, −3}, β ∈ {0, 1, −1/2, 2} and six triples in Q(ζ₁₂)³: the rows with I₃ ≡ 0 are exactly the rows with β = 0 (`selection_is_exactly_beta_zero`); on (1, 1, 1) the quartic I₃ is 36 and the quadratic I₃ is 9 − 12 + 3 = 0.

**Theorem 3.3 (two-report interference reads the QM-207 cycle invariant). PROVED.** Let p₁, p₂ be two reports from locus u to locus v carrying the same source amplitude a through a U(1) cochain with unit edge values. The transported amplitudes are c_k = a · Hol(p_k), and

I₂ = |c₁ + c₂|² − |c₁|² − |c₂|² = 2 Re(c₁ conj(c₂)) = 2|a|² Re Hol(p₁ p₂⁻¹).

The right side is the real part of the loop holonomy of the QM-207 note, so it is gauge invariant and factorizes through the cycle invariants in Hom(H₁, μ₁₂). COMPUTED on the diamond fixture: I₂ = 1, holonomy exponent 10 (Re ζ₁₂¹⁰ = 1/2), equality with 2|a|² Re Hol, invariance under a locus gauge, factorization through the cycle invariants, all true.

**Theorem 3.4 (three-report term). COMPUTED.** The quadratic I₃ on the three transported reports is 0 (`quadratic_i3_zero`), matching the existing `sorkin_i3` certifier.

Interference census on four amplitude pairs: quadratic I₂ = 2, −2, 0, −√3 (written −2ζ₁₂ + ζ₁₂³ in the power basis), each equal to 2 Re of the cross term; ℓ¹ I₂ = 0 on all four.

Reading. The finite invariant of QM-208 is not a holonomy of its own. It is the inclusion–exclusion identity I₂ ≠ 0, I₃ = 0, and what I₂ reads is the QM-207 cycle invariant through Re. The ℓ¹ readout reads nothing of that invariant.

## 4. Completion step: none needed

**Theorem 4.1 (amplitudes stay algebraic). PROVED.** For rational w ≥ 0, √w lies in Q(√w), an extension of degree at most 2, and Q(ζ_N, √w) is a finite extension of Q. No metric completion enters the readout or its composition rule. COMPUTED: weights 1/4, 9/16, 2, 3/4, 1 have amplitude fields Q, Q, Q(√2), Q(√(3/4)), Q; the element ζ₁₂ + ζ₁₂¹¹ squares to 3, so the weight 3/4 has its amplitude √3/2 inside Q(ζ₁₂) itself (`weight_3_over_4_has_amplitude_in_q_zeta12`).

QM-208 is the one row of the five where the completion column is empty. A continuum of weights would need the metric completion, but that is the positive-weight admission of the manuscript, not a property of the readout.

## 5. Residual import

The add-then-square composition rule. Theorem 3.2 selects the quadratic rule inside the declared family {α|c|² + β|c|⁴} by I₃ = 0; the manuscript's section 11.6 selects p = 2 inside the power family |c|^p by one rational context pair. Both are selections inside a declared family. Neither produces the family, the squaring, or the rule c₁ + c₂ for composing reports. Under ℓ¹ the reports compose as w₁ + w₂; the finite invariant tells the two rules apart (I₂ ≠ 0 against I₂ = 0) and derives neither from the other. The polynomial family itself is also a choice: Theorem 3.1 classifies phase-blind monomials, and nothing finite here says the readout is polynomial.

## 6. Three-layer table

| Layer | Status | Content |
| --- | --- | --- |
| finite invariant | COMPUTED | inside α|c|² + β|c|⁴, Sorkin I₃ ≡ 0 iff β = 0 (16-point grid, six triples); I₂ of two transported reports = 2|a|² Re Hol(p₁ p₂⁻¹), gauge invariant; quadratic I₃ = 0 on three reports; phase-blind monomials of degree ≤ 4 are exactly (1, 1), (2, 2) |
| completion | none needed | √w lies in a finite extension; √3 ∈ Q(ζ₁₂) |
| residual import | IMPORTED | the add-then-square composition rule and the polynomial family it is selected inside |

## 7. Negative controls

- The ℓ¹ readout: I₂ = 0 on every fixture pair, so additivity is the ℓ¹ behaviour and the cross term is the quadratic one.
- The trivial fiber (QM-207 note): with nonnegative amplitudes I₂ = 2ab ≥ 0 on the fixture (+6), so a negative cross term needs the fiber.
- The quartic rule: I₃ = 36 on (1, 1, 1) and nonzero on four of the six triples; the two triples where it vanishes have a zero entry, where I₃ reduces to I₂ of the other two and the quartic I₂ is not tested.
- Refusals: `monomial_readout(0, 0)` (the constant), a census degree bound at or above the conductor, and a conductor not divisible by 12 are refused, not computed.

## 8. What the control does not show

- Sorkin's general characterization, that I₃ = 0 for a wide class of rules forces the quadratic one, is not proved here. Only the phase-blind polynomial family of degree at most 4 is covered. The power family |c|^p with p ∉ {2, 4} is outside it; section 11.6 of the manuscript treats that family by a monotonicity argument.
- No inner product and no Hermitian form on Cⁿ is derived; the readout is per locus and the cross term is per pair of reports.
- Independence from QM-207 is not shown and is in the wrong direction: Theorem 3.3 presupposes the QM-207 fiber. Without it the cross term exists but never cancels.

## 9. Manuscript passages this bears on

Section 13.8, the paragraph that corrects the proposed five-import boundary, and section 11.6. If the catalogue of five were rewritten, the QM-208 row would read: quadratic readout, selected inside the phase-blind polynomial family by I₃ = 0 (computed), with the family and the composition rule imported, and with the cross term reading the QM-207 cycle invariant through its real part. Nothing in the manuscript is edited by this note.

## 10. Claim envelope

- Supports: on Q(ζ₁₂), inside the family α|c|² + β|c|⁴, the quadratic rule is the one with vanishing Sorkin I₃ on the tested triples; the two-report cross term equals 2|a|² Re of the loop holonomy and is gauge invariant; the ℓ¹ readout is additive on every pair; every amplitude of a rational weight lies in a finite extension.
- Does not support: Sorkin's full theorem; any derivation of the quadratic rule outside the declared family; an inner product on Cⁿ; independence of QM-208 from the other imports.
- Narrowest claim: on the declared finite carriers the QM-208 import splits into an exactly computed selection invariant, no completion step, and the imported composition rule.
- Next test: `cd omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm && PYTHONPATH=python python3 -m pytest tests/e2e/test_e2e_quadratic_readout_control.py -q -p no:cacheprovider` (expect 8 passed).
