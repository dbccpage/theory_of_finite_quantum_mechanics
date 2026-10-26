# WDP-21-16-MUB6

Goal id: WDP-21-16-MUB6

Selected scope for WDP-21-16-MUB6 is recorded in this note.

## Selected scope

Labelled finite carriers only, not the order-6 complex Hadamard moduli.

1. The recorded Tao phase table `phaseTable`, with `gamma_1 = (1, 1, 1, -1, -1, -1)`: the six column exponents modulo 3 and the Eisenstein norm `x^2 - xy + y^2`.
2. The partition index `m` in `{0, 1, 2, 3}`, with `alpha_2(m) = 6m - 9` and `paritySign`.
3. The synthetic directed weights `canonicalNerveOmega` on `Fin 5` and the single label triple `(0, 1, 2)`.
4. The five-constructor `ModuliClass` row-count table.

These equalities are not summed onto one another. No fresh Lean kernel run, test replay, or matrix enumeration was performed for this note. The twenty-mask check and the Haagerup and Karlsson matrix counts were not re-executed.

## Hypotheses

H1. In the Witnessed Difference Programme, `Phi_1` is the quotient residual mass on a declared finite window. `WDP-CH04-D02` sets `Q^1 = C^1 / im d_0` and `Phi_1([h]) = Phi_J([h])` once a norm `J` is declared. `WDP-CH04-P04` uses `d_1 d_0 = 0` and the norm hypothesis of §§4.9–4.11, and under those hypotheses concludes `Phi_1([h]) = 0` if and only if `[h] = 0`. No opened window in that definition has the complex Hadamard moduli as its carrier.

H2. The nerve sum below is the directed cycle sum of a synthetic integer table on chart labels. It is not taken from a Hadamard matrix, a collar witness, or transition data.

H3. The five-constructor row table is a lookup on an inductive type. It is not a classification of `CHM(6)`.

H4. Section 21.16 asks whether regional circulation `Phi_1 > 0` extends to an exhaustive coverage certificate on the full complex Hadamard moduli, including the remaining non-slice boundary and Stengle certificates. That question is not a register obligation of this note. The arithmetic below does not answer it.

## Derivation

The checked equalities stay on their own carriers. None of them is a value of the WDP quotient mass on the order-6 complex Hadamard moduli.

### 1. Recorded Tao phase table

In `Conjecture2GeneralMechanization.lean`, row 0 of `phaseTable` is identically 0. Rows 1 through 5 and columns 0 through 5 are

```
1: 0 0 1 1 2 2
2: 0 1 0 2 2 1
3: 0 1 2 0 1 2
4: 0 2 2 1 0 1
5: 0 2 1 2 1 0
```

with `gamma_1 = (1, 1, 1, -1, -1, -1)`. The six column sums of `gamma_1` times these entries are `0, -4, -4, 0, 2, 0`. Their nonnegative residues modulo 3 are `(0, 2, 2, 0, 2, 0)`, because `-4 = -2·3 + 2`. The counts are `(n0, n1, n2) = (3, 0, 3)`. Then

```
x = n0 - n2 = 0,
y = n1 - n2 = -3,
x^2 - xy + y^2 = 0 - 0·(-3) + (-3)^2 = 9.
```

This is the integer identity stated by `tao_normSq_eq_nine`. The same file states `column_exponents` and `exponent_counts` by `decide`. It also states `tao_all_balanced_masks`: every 3-plus mask on this phase table has Eisenstein norm 9, again by `decide`. That twenty-mask check was not re-executed here. The file says those statements are not a necessary condition for arbitrary MUB triples.

The value 9 is an Eisenstein norm of one recorded phase table. The G1 receipt `mub_target_g1_matolcsi_conjecture2_receipt.json` records the Tao maximum `max_g1_mod_sq_rat` as `9/1` and sets `ideal_membership_verdict` to `REFUSED_NON_MEMBERSHIP_TAO_WITNESS`. That receipt does not record a `Phi_1` cover. The integer 9 is not the WDP quotient mass `Phi_1`.

### 2. Four partition indices

`alpha_2(m) = 6m - 9` equals `-9, -3, 3, 9` on `m = 0, 1, 2, 3`. Each value is odd, so the ordinary sign is `-1` and

```
1 + (-1)^{alpha_2(m)} = 0.
```

`qubit_parity_sum_zero` records the same integer identity on `Fin 4`, and the module header says these identities do not prove that `G_H` vanishes on matrices. The paired sum `w + (-1)^{alpha_2(m)} w = 0` in `qubit_odd_parity_polynomial_vanishing` is conditional on that exponent formula. Vanishing of a paired integer weight is not a positive circulation obstruction, and it is not a value of `Phi_1` on a Hadamard matrix.

### 3. Synthetic directed weights on five labels

`canonicalNerveOmega` assigns `4045, 4044, 4044` on the ordered pairs `(0, 1)`, `(1, 2)`, `(2, 0)` and `4045` on every other directed pair. `nervePhi1` is the directed cycle sum `ω(i, j) + ω(j, k) + ω(k, i)`. On the label triple `(0, 1, 2)`,

```
4045 + 4044 + 4044 = 12133,
```

which is `deltoid_corner_nervePhi1_eq_gamma` with `circulation_gamma_val = 12133`. The coboundary is `(nerveCoboundary α)(u, v) = α(v) - α(u)`. On any directed 3-cycle the three terms telescope to 0, so the cycle sum is unchanged by an integer vertex potential. The source states that this table is synthetic, not taken from a collar witness or transition data, not antisymmetric, and not a cohomological or geometric obstruction. The comment on `NerveFace2` says the finite relation alone does not establish geometric triple intersection.

Reusing `12133`, or the rescalings `12133/5000` and `12133/30000` that appear as hardcoded margins in opened Lean comments and tests, as a `Phi_1` summed over the Hadamard moduli is refused. `closure_ratio_eq_zero` assumes `0 < phi1` and returns `integer_closure_ratio 0 phi1 = 0`. It does not derive `phi1` from a Hadamard matrix. The spectral identity

```
(1 - 1907/2000) / (6/5) = (93/2000)·(5/6) = 31/800
```

is an identity of the declared rationals `spectral_wall_frac`, `spectral_normalizer_frac`, and `spectral_floor_frac`. The same file says `spectral_contraction_precludes_unbiasedness` does not identify `D_scaled` with a mutually unbiased basis vector.

### 4. Five-constructor row-count table

`proposition_4_2_moduli_reduction` decides a declared table of minus-one row counts: FourierDita 3, Szollosi 3, TaoS6 0, Haagerup 1, KarlssonGeneric 2. The file says this is not a matrix proof. An `AnalyticCubeSliceCertificate` implies confinement to FourierDita or Szollosi only after a caller supplies a row bound of at least 3 that the class meets. Under those hardcoded counts, `tao_admits_no_analytic_certificate`, `haagerup_admits_no_analytic_certificate`, and `karlsson_generic_admits_no_analytic_certificate` say Tao, Haagerup, and KarlssonGeneric admit no such certificate. That is a refusal inside the lookup, not a count of entries of a matrix.

The opened failed-approach category `category_unproved_hadamard_moduli_bridge.md` instead records Haagerup with five minus-one rows and outside `F(x, y) ∪ B_6(θ)`, and records the displayed affine Karlsson ansatz as evading that same confinement. The companion observation notes state those row counts. Those matrix counts were not recomputed here. The disagreement blocks any use of the five-constructor table as a classification of `CHM(6)`.

### 5. The four carriers do not cover the moduli

Section 21.16 poses the full-moduli question and then leaves open whether `Phi_1 > 0` and Stengle certificates cover the remaining non-slice boundary. `WDP-CH04-D02` and `WDP-CH04-P04` make `Phi_1 > 0` a statement inside one declared finite window, under `d_1 d_0 = 0` and the norm hypothesis. No opened window has the complex Hadamard moduli as its carrier. No Stengle certificate on that boundary was opened. The R6 receipt `mub_subgap_r6_closure_receipt.json` has status `NOT_A_CERTIFICATE`. The bridge note states that `Discrete4DBianchiSpectralContraction.lean` does not certify external Fourier vanishing.

Therefore the regional circulation obstruction is not admitted as an exhaustive certificate on the full moduli. The row-count table, the `Fin 4` parity zero, the Tao norm 9, and the synthetic cycle sum 12133 do not supply that carrier. A finite model does not establish a continuum limit, a physical law, or a closed theorem outside the selected scope. This finite case is not a continuum limit, a classification of `CHM(6)`, or a bound on `N(6)`.

## Claims this note does not make

- It does not claim that `Phi_1 > 0` on a declared finite window, the integer 9, the parity identity `1 + (-1)^{alpha_2(m)} = 0`, or the synthetic sum 12133 is an exhaustive coverage certificate on the order-6 complex Hadamard moduli.
- It does not claim that the non-slice boundary is a declared finite semi-algebraic set, and it does not open or certify a Stengle identity on that boundary.
- It does not treat `tao_all_balanced_masks` as re-executed, or as a necessary condition for arbitrary MUB triples.
- It does not treat `proposition_4_2_moduli_reduction` as a matrix proof or as a classification of `CHM(6)`. It does not recompute the Haagerup or Karlsson row counts recorded in the failed-approach notes, and it does not adopt either count as a theorem of this note.
- It does not identify `12133`, `12133/5000`, or `12133/30000` with a quotient mass summed over Hadamard classes. `closure_ratio_eq_zero` assumes a positive denominator; it does not derive that denominator from a Hadamard matrix.
- It does not identify `31/800` or `D_scaled` with a mutually unbiased vector.
- It does not read the G1 receipt's Tao maximum `9/1`, or its refused ideal membership, as a `Phi_1` cover. It does not change the R6 status `NOT_A_CERTIFICATE`.
- It does not certify external Fourier vanishing, and it does not admit the floating-point search count `N(6) = 3`, or the statements `MUB(6) = 3` and `MUB(6) ≤ 3`.
- It does not select the complex field or `U(1)`. Chapter 22 refuses that Tier-4 selection, and the later evidence boundary says there is no claim that MUB6 is resolved.
- It does not close section 21.16. The question stays open outside the four labelled carriers named above.
