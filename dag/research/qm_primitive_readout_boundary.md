# A cochain carrier does not select its quantum readout

2026-10-11. Research correction and exact finite control. AuthorityEffect: None.

GAP-FQM-021 remains open. Direct packet consumption is useful integration
evidence, but does not derive the packet, scalar field or readout from primitive
distinction. GAP-FQM-005's executable model walk remains intact.

## Source audit

The audit starts from repository commit
`33e3fea65c4800aa8064b400292df8ecfa4ae777`.
The then-named
`TestDirectCochainPacketWalkE2E.test_complete_continuous_walk_from_difference_to_predictions`
computed `D(10.0, 10.0 + pi/2)` and checked that scalar against `pi/2`.
Its later triangle, three-slit and glued-simplex packets, Cayley parameter
`1/3`, cyclotomic weights, and detector were supplied independently; the
scalar was not used to construct them. The current test is named
`test_declared_packet_models_produce_predictions` and checks those same model
outputs without the disconnected scalar prelude.

In [the reference engines](../tests/legacy/e2e/conftest.py),
`probability_quadratic_from_complex` forms a weighted path sum and calls
`norm_sq`. Its third-order cancellation therefore checks the consequence of
an explicitly chosen square. The [legacy cochain implementation](../../majorana/code/tests/support/finite_qm/use_cases/cochain.py)
itself says that it neither derives the packet nor selects the weights. Its
obstruction classifier uses a floating-point LP with tolerance `1e-9`.
The exact rational/cyclotomic engine calculations and the numerical classifier
have different evidence scopes.

The earlier closure entry is retained in `closure_history` within the reopened
[gap row](../claims/gap_register.yaml). Historical receipts, source archives
and changelog assertions are unchanged. The current manuscript and test
documentation carry the corrected interpretation.

## Same carrier, three readouts

Fix the five vertices `source, a, b, c, sink`, the six directed edges
`source→a, source→b, source→c, a→sink, b→sink, c→sink`, and the three closed
face walks `source→a→sink→b→source`, `source→b→sink→c→source`, and
`source→c→sink→a→source`. Each slit path consists of its two forward edges.
The unit detector cochain pairs with each path to give 2. With the common
declared amplitude factor `1/6`, each path contributes `1/3`.

For an open-slit subset $S\subseteq\{a,b,c\}$, keep the packet, paths,
weights and additive amplitude $A(S)=|S|/3$ fixed. Define

$$P_1(S)=A(S),\qquad P_2(S)=A(S)^2,\qquad P_4(S)=A(S)^4.$$

All three are nonnegative, at most one, zero at the empty subset and one at
the full subset. Each gives a normalized binary distribution
$(P_j(S),1-P_j(S))$ at every declared slit setting. This is a finite family
of experiments; no compatible full operational theory is asserted for the
rival rules.

For a symmetric table define

$$I_3(P)=P(abc)-3P(ab)+3P(a)-P(\varnothing).$$

Direct substitution gives the following exact values.

| Readout | One slit | Two slits | Three slits | $I_3$ |
| --- | ---: | ---: | ---: | ---: |
| $P_1$ | $1/3$ | $2/3$ | $1$ | $0$ |
| $P_2$ | $1/9$ | $4/9$ | $1$ | $0$ |
| $P_4$ | $1/81$ | $16/81$ | $1$ | $4/9$ |

Thus $d_1d_0=0$, the declared path pairing, nonnegativity and endpoint
normalization do not force the quadratic rule. Even adding $I_3=0$ on this
family leaves the linear rule: its second-order term is zero, whereas the
quadratic rule gives $2/9$. This does not refute a reconstruction with stronger
operational hypotheses; it identifies hypotheses that the integration test
does not supply.

More generally, the third finite difference of a polynomial of degree at
most two vanishes. Expanding a squared additive complex amplitude into its
single-path and pair terms proves third-order cancellation; each term
depends on at most two slit indicators, so inclusion–exclusion cancels it.
That proof starts with a square and does not select the square.

## Protected questions and the Genesis bridge

Let the admitted model class contain the two explicitly declared choices
$(C,P_2)$ and $(C,P_4)$ above, and let $q$ forget the readout choice, retaining
only the common carrier data $C$. The single-slit prediction differs by
$1/9-1/81=8/81$ on one fiber of $q$. Hence it cannot factor through $q$.
For any carrier-only prediction $x$, the triangle inequality gives

$$\max\{|x-1/9|,|x-1/81|\}\ge 4/81.$$

The midpoint $x=5/81$ attains this bound on the two-model class. Likewise the
third-order question has exact minimax error $2/9$ because its two values are
$0$ and $4/9$. These are sharp uncertainty bounds about an omitted model
choice, not experimental error estimates for a chosen quantum theory.

This is the [WDP protected-question fiber criterion](../../finite_obstruction_calculus/witnessed_difference_programme/docs/genesis_bridge_register.md)
(GEN-WDP-03) applied to declared mathematical realizations. Retaining a
readout tag repairs this particular loss but does not determine which tag
nature uses. Excluding the quartic and linear alternatives requires stated
premises with an independent justification.

The [S(n)/MSS-N architecture](../../finite_obstruction_calculus/symmetric_groups_and_minimal_symbol_systems/README.md)
does not permit a property of a chosen realization to create a native Genesis
stage. This control consequently supports GEN-WDP-O04's open reconstruction
obligation. It neither admits a carrier from the opaque `<>` inscription nor
derives complex scalars, reversible history quotients, state/effect spaces,
tensor composition or physical process availability. The conditional positive
trace and central purification results in
[PO-000 Appendix E](../../projection_obstruction/projection_obstruction_paper/projection_obstruction.md)
can be used after their respective algebraic and operational premises are
supplied; they do not remove this earlier bridge obligation.

## Native check and verification scope

The new test
`quadratic_readout_interference::the_same_three_slit_packet_admits_distinct_readout_degrees`
in [the sovereign physics suite](../../../../../omega_engine/crates_rs/tests/omega_quantum_physics/synthesis/quadratic_readout_interference.rs)
uses `omega_solvers::finite_cochain_packet`, the shared exact inner product,
`omega_number_theory` rational/Gaussian scalars, and the existing
`gaussian_frame_readout::readout`. It checks $d_1d_0$ on every coordinate
basis potential, the three path pairings, all eight slit settings and the
table above. The existing quadratic `sorkin_interference` independently
agrees with the quadratic inclusion–exclusion value.

From `omega_engine/crates_rs`, run:

```sh
cargo test -j 1 --offline --locked -p omega_quantum_physics --test synthesis quadratic_readout_interference::the_same_three_slit_packet_admits_distinct_readout_degrees -- --exact
```

This test is a finite counterexample under the stated weak premises. The
general fiber and minimax arguments above are written proofs, not new Lean
formalizations. The execution receipt records the actual toolchain, result
and source hashes; no whole-suite pass or external publication is claimed.
