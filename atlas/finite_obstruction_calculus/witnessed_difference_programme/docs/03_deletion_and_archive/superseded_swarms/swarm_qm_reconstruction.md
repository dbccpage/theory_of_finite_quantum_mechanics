# QM reconstruction and composition derivations

AuthorityEffect: None. This note answers the signed operational representation and composition obligations of CH18-O01 and CH19-O02 with explicit no-go statements, a constructive conditional representation theorem, and a sufficient imported quantum composition package. It does not infer a quantum reconstruction or Born selection from W1–W6. Canonical claim statuses remain the responsibility of the manuscript/ledger editor.

## 1. What the existing obligations actually require

CH18-O01 asks for classical representation with signed W3, representation of the actual Chapter 10–13 packets, or a quantum reconstruction exposing additional axioms. Its residual explicitly says that packets admitting arbitrary reportable empirical contexts include contextual images unless W7 is added. Thus proving facts about nonnegative states alone does not discharge it. CH19-O02 requires a principle admitting quantum correlations while excluding PR, and an account of tensor structure. Tagging and no-signalling alone are inadequate; its bilinear positivity clause currently applies only to classical factors.

## 2. Signed full-effect classical representation is impossible

Let `w` be a normalized rational signed valuation on a finite carrier Q. A classical realization preserving a reported indicator `1_i` consists of a nonnegative normalized state `p` on any enlarged finite carrier and an effect `e_i` with entries in [0,1], such that `sum p_j e_i(j) = w_i`. The left-hand side is nonnegative. Therefore any negative reported `w_i` rules out every such realization, regardless of carrier enlargement. Conversely, if all `w_i` are nonnegative, `w` itself is a classical state and preserves every effect. For the complete indicator vocabulary, existence is therefore equivalent to pointwise nonnegativity. The permitted signed W3 instance `(2,-1)` has positive total 1 and fails the necessary condition. A faithful probability interpretation of every signed coordinate cannot be recovered merely by relabeling.

This theorem does not forbid classical realizations of restricted readouts; signed coordinates need not be physically reportable probabilities. That distinction is essential for the actual packet obligation below.

The Jordan decomposition `w = w+ - w-` has disjoint nonnegative parts. Writing `N = sum w-`, their masses are `1+N` and `N`. Every decomposition `w=a-b` with `a,b>=0` has `b_i>=max(-w_i,0)`, so N is the minimal negative mass. For every readout with `|f_i|<=M`,

`|sum w_i f_i| <= M sum |w_i| = M(1+2N)`.

For M>0, `N >= max((|E|/M-1)/2,0)` for any reproduced expectation E. At M=0 all readouts and E vanish; only the undivided inequality applies. The native implementation computes the actual signed expectation, negativity, and bound exactly.

## 3. The actual operational-packet obstruction: PR with a sharp signed section

Enumerate all 16 assignments lambda=(a0,a1,b0,b1), each sign ±1. Put

`S(lambda)=a0 b0+a0 b1+a1 b0-a1 b1`,

which is always ±2, and define

`w(lambda)=(1+S(lambda))/16`.

There are eight assignments of each sign, hence eight weights 3/16 and eight weights -1/16. Their total is 1 and N=1/2. Summing over the two unreported signs gives, for every setting pair (x,y) and outcomes (a,b),

`p(a,b|x,y) = (1 + (-1)^(xy) a b)/4`.

Thus every accepted local outcome table is nonnegative and normalized: it assigns probability 1/2 to each pair with `a b=(-1)^(xy)` and zero otherwise. Both marginals are uniform, so no-signalling holds. Yet the observed CHSH value is 4. Any nonnegative global distribution would average deterministic values ±2 and therefore have absolute expectation at most 2, a contradiction. This gives a fully observable operational no-go, not one resting on a negative hidden outcome. Moreover the Jordan bound gives `N>=1/2`; our signed section attains it exactly. All 16 pairwise outcome marginals are checked in the native test.

By the paper's reportability premise (CH19-P04), this PR empirical table has accepted packet representatives. Therefore the unrestricted claim that all constructed packets satisfy package S/W7 is false. It can be repaired only by restricting packet admission, adding joint runs/W7, or selecting a nonclassical target theory. The countermodel does not select quantum theory: PR is explicitly excluded by the sufficient package below.

## 4. A complete conditional classical report representation, including signed hidden dynamics

Fix a surjective report partition pi:Q→R. Let D be its block-sum map. The following package is sufficient and independently checkable:

1. Finite nonempty carriers and a fixed surjective report map.
2. The full family of normalized signed hidden states w whose report masses `Dw` are nonnegative (or a chosen subfamily explicitly closed under the admitted positive-probability normalized updates).
3. Every admitted outcome map M_o is a rational signed matrix; total row mass across all outcomes is one. For each outcome and every target report r, the sum of entries into block r is constant within each source block. The resulting report maps T_o are nonnegative.
4. Accepted outcome probabilities and post-report states are the masses and normalized positive vectors of the descended maps. Other finite provenance/report tags can be carried as classical auxiliary variables; no calibration validity is thereby established.
5. For simultaneous multi-context classicality, admit only empirical families with a common nonnegative joint table (W7). This is an additional restriction, not a consequence of the previous four clauses.

For any signed row-state w, condition 3 gives `(w M_o)D = (wD)T_o` by rearranging a finite sum. Conversely, testing this equation on each carrier basis vector forces the stated block-row equality; surjectivity makes T_o unique. Nonnegativity of T_o is necessary and sufficient for this quotient outcome map to act positively on every classical report state. Their sum is stochastic because total hidden row mass is one. Iterating the intertwining identity proves every finite outcome-word probability and report-state update agrees with a classical hidden-Markov instrument. No unsigned assumption on hidden w or M_o was used.

The static condition in clause 2 is also necessary and sufficient: block indicators determine the unique probability vector Dw. Complete singleton reports reproduce the full-effect no-go in section 2.

A nontrivial constructed instance has normalized hidden weights `w=(2,-1,1)/2` (total 1), reports `(0,0,1)`, and report state `(1/2,1/2)`. Outcome 0 acts by signed shear `[[2,-1],[1,0]]` within the first fibre and kills the second fibre; outcome 1 keeps the second fibre and kills the first. The native quotient is the binary projective classical instrument. This demonstrates that signed internal structure and an exactly classical restricted report theory can coexist. The theorem is conditional on the declared partition and admitted instruments; it does not assert that unrestricted historical packets meet these clauses.

## 5. A sufficient nonclassical composition principle and PR exclusion

Import finite complex Hilbert local carriers, tensor product composition, PSD trace-one composite states, local Hermitian dichotomic observables `A_x²=B_y²=I`, and the probability pairing `tr(rho effect)`. Local projectors `(I±A_x)/2`, `(I±B_y)/2` define nonnegative normalized outcome probabilities. Local complete instruments do not signal because their summed adjoint effects equal identity. Tensor-basis tagging is injective and therefore consistent with the finite observer architecture. These are exposed quantum assumptions, not consequences of primitive difference or CP's classical bilinear clause.

Define `C_A=[A0,A1]`, `C_B=[B0,B1]` and

`S=A0 tensor(B0+B1)+A1 tensor(B0-B1)`.

Finite multiplication gives `S²=4I-C_A tensor C_B`. The two local positive matrices

`2I±i C_A=(A0±i A1)* (A0±i A1)`

(and similarly for B) imply

`8I-S² = ((2I+iC_A) tensor(2I-iC_B) + (2I-iC_A) tensor(2I+iC_B))/2 >= 0`.

For `s=tr(rho S)`, positivity of `(S-sI)²` yields `s²<=tr(rho S²)<=8`. Thus every finite quantum model satisfying the imported package obeys the squared Tsirelson bound. PR has s=4 and fails it. No irrational root is needed to check the bound.

The exact rational witness uses the Bell density `( |00>+|11> )( <00|+<11| )/2`, `A0=Z`, `A1=X`, `B0=(3Z+4X)/5`, `B1=(3Z-4X)/5`. It has s=14/5>2 and s²=196/25<8: the principle genuinely admits nonclassical quantum correlations while excluding PR. Native code validates the actual local involutions/state, the S² commutator identity, the PSD operator bound, and separate nonnegative variance/operator slacks. Passing the scalar bound alone is not a quantum membership certificate.

## 6. Tensor structure: explicit matrix-algebra classification

To account for tensor structure rather than only assume a chosen Kronecker realization, require two complete commuting unital *-matrix-unit systems `E_ij` (size m) and `F_kl` (size n) acting on the finite Hilbert carrier H. Their products

`G_(i,k),(j,l) = E_ij F_kl`

satisfy all matrix-unit relations, adjoint reversal, and sum of diagonal units equal identity. Every diagonal G is an orthogonal projection of the same rank r, since `G_a0` is an isometric bijection between the reference projection range and the a-th range. Hence `dim H = mn r`. Choose an orthonormal basis `u_t` of the reference range and set `u_(a,t)=G_a0 u_t`. This is an orthonormal basis of H and identifies the local algebra action with

`H ≅ C^m tensor C^n tensor C^r`.

Therefore a no-hidden-multiplicity condition `dim H=mn` selects the Hilbert tensor carrier up to unitary equivalence. Without it, a residual multiplicity factor survives; this is explicitly reported by the certificate rather than hidden. The native matrix-unit classifier verifies all local algebra relations, commutation, integer positive multiplicity, and the dimension identity. Tests distinguish a minimal 2×2 tensor carrier, an extra multiplicity-two carrier, and noncommuting purported factors.

This conditional classification answers what additional composition structure suffices, while exposing the unpaid assumption: complete complex matrix local algebras and minimal multiplicity are stronger than tagging/no-signalling. An orthonormal basis may need irrational coefficients, so the exact Q(i) validator does not promise a Q(i)-valued change-of-basis matrix. Neither this theorem nor the Tsirelson discriminator forces Born pairing from weaker witness axioms.

## 7. Artifacts and validation scope

Native reusable owners:

- `omega_finite_probability/src/signed_representation.rs`: signed no-go witness, Jordan negativity, restricted-state classification, exact instrument quotient descent.
- `omega_quantum_physics/src/composition_quantum_bound.rs`: actual-model squared Tsirelson certificate and complete commuting matrix-algebra/multiplicity classification.
- `omega_wdp/src/reconstruction_classification.rs`: direct thin adapter calls to those owners.

Focused tests are `signed_representation_classification.rs` and `composition_quantum_bound.rs`. Python fixed arithmetic witnesses live in `code/witnessed_difference/reconstruction_classification.py`, with two tests in `code/unit_tests/test_reconstruction_classification.py`. Core-only `lean4/WitnessedDifference/ReconstructionClassification.lean` proves the negative-indicator contradiction, fibre-factorization directions, and exact scaled PR/quantum arithmetic. It does not mechanize the general rational instrument theorem or the operator Tsirelson/tensor-classification proofs; those have the exact prose derivations above plus finite native validation.

Validation completed at this revision: core Lean compilation passed; two focused Python tests passed with repository-wide coverage defaults overridden for this explicitly scoped run. Native production validation details are appended after the final run. No manuscript/ledger status is silently promoted by these artifacts.

## 8. CH19-O03: divisible rational-turn character, gauge descent, and the unpaid readout

Define the additive phase carrier `Q/Z` with canonical rational representative in [0,1). Under a separately declared standard complex embedding, `chi(q)=exp(2 pi i q)` is an injective character into all roots of unity. For q=k/N it is the exact cyclotomic value `zeta_N^k`; changing representatives by an integer does not change it. At any common multiple conductor the existing cyclotomic owner checks multiplication exactly. Every q has an n-th root q/n, so the symbolic phase group and the union of its root-of-unity images are divisible. The selected representative root is not a splitting homomorphism: it need not respect addition across wraparound.

The native symbolic group accepts arbitrary rational denominators. Its actual cyclotomic evaluation respects the existing owner's `MAX_CONDUCTOR=1024`, and rejects unsupported evaluation rather than approximating or claiming a complete executable algebraic closure. Rational-turn phases are periodic and send every integer to 1. Consequently this construction does **not** extend the existing infinite-order Gaussian anchor `u=(3+4i)/5` with `1 -> u`. That anchor's square-root obstruction inside Q(i) remains valid. A scalar extension containing compatible roots of that u for every order would be a different declared branch; no such complete extension is implemented or forced here. Likewise no arbitrary real cochain exponentiation, continuity, or choice of real phase scale is derived.

On an oriented graph with rational turns a_e, a path phase is the signed sum of edge turns. For the gauge action `a'_uv=a_uv+f_v-f_u`, summing a validated path gives

`a'(gamma)=a(gamma)+f(end)-f(start) in Q/Z`.

This follows by cancellation at every intermediate vertex. Applying the declared character makes every path transport acquire the same endpoint factor; closed holonomy is unchanged. Two paths with the same endpoints therefore retain their relative phase, and any common-phase-blind readout descends to the cochain gauge quotient. The native WDP adapter computes both sides from actual validated paths; a concrete triangle has closed phase 5/12 before and after a rational gauge change, and the common-conductor cyclotomic equality is checked.

That quotient does not determine probability readout, even after normalization. For any nonzero finite Gaussian-rational amplitude family z, both rules

`p_i^(2)=N(z_i)/sum_j N(z_j)` and `p_i^(4)=N(z_i)^2/sum_j N(z_j)^2`

are nonnegative, normalized, and invariant under a common unit phase. At amplitudes `(1,2)` they give `(1/5,4/5)` and `(1/17,16/17)`. This is a normalized finite nonselection countermodel, stronger than comparing unnormalized quadratic/quartic intensities alone. It preserves the nonclaim CH19-N01.

An actual operational bridge can be supplied **after paying** the quadratic density/trace pairing: set `rho=|z><z|/sum N(z)` and use the complete basis-projector instrument. The existing exact density/instrument owner validates rho and the Kraus family, and computes `tr(P_i rho)=p_i^(2)`, normalized post-states, and the outcome-forgetting map. This is rational arithmetic even when normalizing z as a ket would need irrational roots. The bridge supplies a concrete effect/readout/instrument instance consistent with gauge descent; it does not claim the quartic alternative obeys the imported linear quantum effect pairing, nor that that pairing was selected by gauge symmetry. Empirical identification with any physical apparatus remains an additional operational hypothesis.

Artifacts: `omega_number_theory/src/rational_turns.rs`, `omega_quantum_physics/src/phase_readout.rs`, `omega_wdp/src/rational_phase_bridge.rs`; targeted tests `rational_turn_character.rs`, `phase_readout_nonselection.rs`, and `rational_phase_gauge.rs`. Fixed Python receipts live in `rational_phase_witness.py`. Lean-distribution core `RationalPhaseBoundary.lean` proves integer path telescoping, closed holonomy invariance, transport of the equality by a declared character, and the explicit normalized-readout cross-product inequality; it does not mechanize the full rational/cyclotomic scalar tower.

A further boundary is necessary: the rational-turn bridge is not faithful on rational cochain classes. On a graph cycle, an integer cochain with cycle sum 1 is not a rational coboundary (all coboundaries have cycle sum zero), but chi maps its cycle phase to 1. Passing to Q/Z therefore introduces integral-period identifications beyond gauge equivalence. The bridge proves descent, not injective reconstruction of the real/rational cochain quotient. The older infinite-order Gaussian integer scale can distinguish all integer exponents; its missing rational roots cannot be repaired merely by switching silently to this periodic scale.

## 9. Original real-cochain bridge: complete conditional analytic theorem

The rational-turn implementation is not a substitute for the REAL cochain interface in the original CH19-O03. The following theorem supplies that interface at the analytic scalar-host level, with every import explicit.

**Declared analytic host.** Fix a finite oriented graph, real edge cochains `a_e`, the standard complex field and modulus, and a declared real scale theta. Define the continuous additive character

`chi_theta(t)=exp(i theta t)`.

The exponential addition identity gives `chi_theta(t+s)=chi_theta(t)chi_theta(s)`, conjugation gives `chi_theta(-t)=overline(chi_theta(t))`, and its modulus is one. To keep the original anchor `u=(3+4i)/5`, choose theta with `exp(i theta)=u`, for example the angle in (0,pi/2) with cosine 3/5 and sine 4/5; every theta differing by 2pi times an integer is another allowed logarithm. This choice is an additional scalar/scale declaration, not a consequence of the primitive cochain system. On the real host, `chi_theta(1/2)` is a square root of u, so the rational-field obstruction is overcome by paying the larger scalar host. No exact transcendental Rust evaluation or formal Lean proof of complex analysis is claimed.

**Path/gauge theorem.** For any finite validated path gamma from s to t, let `A_a(gamma)` be the signed real edge sum and define transport `U_a(gamma)=chi_theta(A_a(gamma))`. Finite addition gives composition of transports, inversion by conjugation, and

`A_(a+d0 f)(gamma)=A_a(gamma)+f(t)-f(s)`

for every real vertex potential f. Hence

`U_(a+d0 f)(gamma)=chi_theta(f(t)) U_a(gamma) overline(chi_theta(f(s)))`.

For a closed path the endpoint factor is one, so holonomy is unchanged. For any finite family of alternative paths with common endpoints and declared complex coefficients c_j, its coherent amplitude

`z_r=sum_j c_j U_a(gamma_(r,j))`

acquires exactly the same common unit phase under gauge transformation. Consequently every common-phase-blind operational readout descends to the REAL cochain quotient by real coboundaries. This proves descent to that quotient, not reconstruction of the quotient from phases.

**Precisely characterized periodic kernel.** If theta=0, the character is constant one and forgets all cochains. If theta is nonzero, `chi_theta(t)=1` exactly when `theta t` is an integer multiple of 2pi. Its kernel is therefore `(2pi/theta) Z`; in particular it is not injective on the real additive group. On a finite graph choose a spanning forest and a fundamental cycle basis. Real cochain classes modulo real coboundaries are identified with their real fundamental-cycle periods. Two phase connections are gauge equivalent exactly when their cycle-period differences lie in the character kernel, i.e. each fundamental-cycle difference is in `(2pi/theta) Z`. Necessity follows by closed-loop cancellation; sufficiency follows by assigning vertex phases along the spanning forest, leaving exactly the fundamental-cycle discrepancies to check. Thus the phase quotient is the real cycle space modulo its full period lattice, not the real cycle space itself.

This loss cannot be removed by demanding some other **continuous additive** faithful character `R→U(1)`: every continuous character is `exp(i theta t)`. To see the classification, use a continuous local argument of the character near zero. The homomorphism law says the failure of local argument additivity is an integer multiple of 2pi; continuity and its zero value at the origin make it zero on a sufficiently small neighborhood. The continuous local Cauchy equation is linear, so the argument is theta times t there. Subdividing any real t into sufficiently small pieces extends the formula globally. Its kernel is as above (all of R when theta=0), proving no continuous character is faithful. This assertion is specifically about continuity; it makes no claim about discontinuous abstract embeddings.

For the original infinite-order anchor u, theta/(2pi) is irrational; otherwise u would have finite order. Therefore the nonzero period `(2pi/theta)` is irrational, and the character's kernel meets Q only at zero. The anchor-preserving analytic branch can distinguish rational scalar exponents while the separate rational-turn branch identifies every integer. Neither fact produces an injective continuous real character.

**A concrete paid instrument interpretation.** Given a nonzero finite detector-amplitude vector z, declare `rho=zz*/(z*z)` and a complete finite Kraus instrument `(K_o)` on the declared complex Hilbert detector carrier. Define `E_o=K_o*K_o`, `p_o=tr(E_o rho)`, and, for p_o>0, the post-state `K_o rho K_o*/p_o`. Positivity and completeness give nonnegative p_o summing to one; these are the same finite algebraic identities as the general instrument derivation. Since a common endpoint phase cancels in rho, all effects, probabilities, and post-states are unchanged by the real cochain gauge action. This fills the effect/readout slots by an explicit specification; it does not derive that specification from the character.

If detector amplitudes have different terminal vertices, their gauge action is a diagonal unitary U_f rather than one common phase. With a declared output gauge V_f, co-transform `rho'=U_f rho U_f*`, `K'_o=V_f K_o U_f*`, and `E'_o=U_f E_o U_f*`. Cyclic trace gives the same p_o and output states related by V_f. Gauge-invariant operational meaning therefore requires these covariant effect/instrument transformations; comparing fixed effects against a transformed non-common-phase state would be a different experiment. Byte-level receipt hashes intentionally bind presentations and need not be equal across gauge-related descriptions; the invariant probabilities and covariant states are the semantic statement.

**Readout still is not forced.** In this very analytic host, the normalized quadratic and quartic detector rules of section 8 remain nonnegative, normalized, and common-phase invariant, and disagree at z=(1,2). If the imported quantum density/linear trace-effect pairing is required, the quadratic table follows by that additional axiom; the quartic rule is not another linear quantum instrument on that same density specification. But gauge descent and normalization alone admit both, so they do not choose Born pairing. One may realize either finite table as a separately declared classical instrument; the discrimination between them is an operational/model assumption, not a theorem of primitive difference.

**Empirical scope.** An operational model additionally declares preparation, accepted detector labels, Kraus realization, calibration/provenance policy, and the meaning of probabilistic trial laws. Finite outcome carriers with real probabilities exist on this analytic host, but arbitrary real/irrational probabilities cannot equal a finite integer-count frequency table exactly. Rational instances (including our witnesses) admit the existing common-denominator packet/run-table construction. For irrational instances, empirical comparison needs a declared sampling/approximation model; no exact finite-frequency representation or physical apparatus identification is inferred here. This is the precise conditional interpretation of the original REAL bridge, with the remaining empirical assumptions exposed rather than replaced by the finite rational-turn example.

## 10. Final production validation receipt

All native tests below ran against the actual repository workspace and owners, with `CARGO_HOME=/workspace/.toolchains/cargo`, `RUSTUP_HOME=/workspace/.toolchains/rustup`, the installed cargo binary, and `-j2`; no scratch surrogate, integrity-gate bypass, or float evaluation is used for these results:

| Owner | Targeted test | Result |
|---|---|---|
| omega_finite_probability | signed_representation_classification | 3 passed |
| omega_quantum_physics | composition_quantum_bound | 3 passed |
| omega_number_theory | rational_turn_character | 1 passed |
| omega_quantum_physics | phase_readout_nonselection | 1 passed |
| omega_wdp | rational_phase_gauge | 1 passed |

The WDP target also production-compiled the thin `reconstruction_classification` module. Two focused reconstruction Python tests and one phase Python test passed under `PYTHONPATH=code`, `-o addopts=''` (overriding whole-package coverage defaults for scoped tests). Both standalone new Lean files compiled using the installed Lean 4.33.1 binary; the phase file imports only the bundled `Lean.Elab.Tactic.Omega`, not Mathlib. General rational-instrument classification, tensor-algebra classification, Tsirelson analysis, and the analytic REAL character theorem have the explicit prose proofs above; the limited Lean kernel coverage is identified in their artifact descriptions. Existing unrelated omega_solvers warnings do not change the exact test outcomes.
