<div align="center">

# Discrete Deformation Calculus

A Finite Trace Calculus for Obstruction Handling

**Author:** Jeremy H. Carroll **Version:** 1.0.3
**Date:** 2026-10-03

Text: CC BY 4.0 · Code: PolyForm Noncommercial 1.0.0

</div>

## Abstract

The Discrete Deformation Calculus (DDC) records what a finite computation did
to a declared obstruction. Each step emits one letter from
$\mathcal{A}_{\mathrm{DDC}} = \{E, R, C, I, \Lambda, D, M, T\}$: exact repair,
residual projection, context exposure, integration, licensed lift, descent,
typed refusal and terminalization. A step carries a receipt, and a tape is the
hash-chained sequence of receipts. Diagnostics come from CODA-FOC: $\Phi_1$ is
the weighted $\ell^1$ distance of a residual to the image of $d_0$, and
$\Gamma_2 = \lVert d_1 x \rVert_1$ is its face-closure defect.

This version states the letter laws as a finite-control transition system over unbounded data and proves its
tape results in Lean 4 without Mathlib. Every proved or computed claim is
bound to a Lean declaration, a Python test or a written proof shipped in this
package; the rest are typed as open problems or positioning. The main results are these. Only a
descent with a loss ledger or a licensed lift can lower $\Phi_1$ or $\Gamma_2$.
Consequently an open obstruction ($\Gamma_2 > 0$) never reaches a terminal
without such a priced move. The tape C·R·E·D·I·T is lawful exactly when each
of its six steps satisfies its law. A lawful one starts from
$\Phi_1 = \Gamma_2 = 0$, and without a loss ledger at D it is not lawful.
Every step the paper admits satisfies the deposited historical comparison
laws on the same abstract state; no deployed-runtime equivalence is claimed. A lawful tape is replay
evidence; it is never authority.

## 0. Scope and nonclaims

```text
DDC does not prove that reality is discrete or that the universe is a cochain complex.
DDC does not prove quantum mechanics, continuum physics, consciousness, semantic truth,
autonomous self-modification, or global topology.

DDC is not authority. A DDC tape is replay evidence; a receipt is bounded verification
data; a terminal is a routing terminal. No authorization is conferred.

"All problems are obstruction problems" is a programme thesis, not a theorem.
"The universe is not very creative" is motivation, not runtime mathematics.
```

Every diagnostic in this paper is taken on a declared finite carrier with a
declared detector. Claims about trace equivalence, normal forms, detector
adequacy in general, and lift minimality remain open (§13).

## Part I — The calculus

## 1. Definition

**Definition 1.1** (OE010-09). A *DDC regime* is a finite carrier, declared
coboundary maps $d_0, d_1$ with $d_1 d_0 = 0$, a detector that measures
$\Phi_1$ and $\Gamma_2$, and a terminal policy. A *step* is a letter from
$\mathcal{A}_{\mathrm{DDC}}$, the state after it, and the witnesses it carries.
A *tape* is a finite sequence of steps; it is *lawful* when every step
satisfies its letter's step law (§7) and the control laws (§10).

Carrier, ZeroRel, Observer, Witness, Residual, Quotient, CompletionLaw and
AuthorityEffect are used in their CODA sense; this paper relies only on the
ones it defines in this section and in §3 (OE010-02).

The letters classify the role a step played in the life of an obstruction:

```text
context exposure · exact repair · residual projection · integration
licensed lift · descent · typed refusal · terminalization
```

## 2. Core invariant

DDC does not only classify obstruction states. It classifies what each
computation did to an obstruction:

$$\boxed{\text{DDC is a typed calculus of what a computation did to an obstruction.}}$$

A status system says *pass*, *fail* or *unknown*. DDC asks which finite
operation occurred: did it expose a carrier, repair a defect, project a
residual, integrate a receipt, license a lift, descend with loss, refuse, or
terminalize? This lets error handling be compared across domains without
claiming that the domains share an ontology.

## 3. Cochain window and diagnostics

When a cochain regime is declared, every execution window is

$$C^0 \xrightarrow{d_0} C^1 \xrightarrow{d_1} C^2, \qquad d_1 \circ d_0 = 0.$$

| Object | Runtime reading |
|--|------|
| $C^0$ | vertex variables, potentials, repair parameters |
| $C^1$ | edge defects, claim gaps, local residuals |
| $C^2$ | face and loop closure defects |

The convention is adapter-conditional: a prompt, a patch or an agent trace does
not have $C^\bullet$, $d_0$, $d_1$, $\Phi_1$ or $\Gamma_2$ until a carrier, a
comparison map, a repair image and a detector have been declared.

**Definition 3.1** (FOC diagnostics). For a residual $x \in C^1$ with positive
edge weights $w$,
$\Phi_1(x) = \min_{\varphi} \sum_e w_e \lvert x_e - (d_0\varphi)_e \rvert$ and
$\Gamma_2(x) = \lVert d_1 x \rVert_1$. The class of $x$ is *ActiveClosureFailure*
when $\Gamma_2 > 0$, otherwise *ExactRepair* when $\Phi_1 = 0$, otherwise
*ClosedResidual*. A positive $\Gamma_2$ dominates (witness dominance).

**Proposition 3.2** (DDC-TAPE-11). On a finite graph, $\Phi_1$ is attained
at a potential determined by a spanning forest whose edges are all tight.
Enumerating spanning forests therefore computes $\Phi_1$ exactly.

*Proof.* Fix one vertex potential to zero in each connected component.
Positive weights bound each edge difference on an objective sublevel set;
paths in a spanning forest then bound every remaining potential. Apply
compactness to the real extension; a minimum is attained. The objective is
piecewise linear on finitely many polyhedral regions. The minimizing face in
one such region is nonempty and bounded, so it contains a vertex of that
region. At such a vertex, independent
tight constraints $x_e = \varphi_v - \varphi_u$ fix $\varphi$. Independent
incidence rows form a forest, and fixing $\varphi$ needs one spanning each
component. A minimizing vertex determined by a spanning forest has rational
coordinates, so the optimum is also attained over the rationals. $\square$

`cochain.phi1` implements the enumeration and refuses as `BUDGET_UNKNOWN` above a
declared subset budget; `test_cochain.py::test_phi1_is_gauge_invariant_and_matches_brute_force_on_small_grids`
checks it against an integer search. `cochain.phi1_certificate` also returns a
dual witness: a flow $y$ with $d_0^{\top} y = 0$ and $\lvert y_e \rvert \le w_e$
whose value $\langle y, x \rangle$ equals the primal objective. Dual vertices
set $y_e = \pm w_e$ off a spanning forest and solve the forest edges by
conservation, so the same enumeration finds them, and strong duality is
checked rather than assumed
(`test_cochain.py::test_phi1_certificates_close_the_duality_gap_exactly`).
Every $\Phi_1$ in the demos is measured through this certificate.

A fixed forest representative need not minimize this objective. For the
complete graph on $a<b<c<d$, orient all six edges increasingly and put $-1$
on each. The forest rooted at $a$ leaves the three other edges at $-1$, so
the recorded residual norm is 3, while $\Phi_1=2$. Both representatives have
the same quotient class. Chapter 2 distinguishes these quantities.

**Theorem 3.3** (OE010-01, DDC-TAPE-10). Over $\mathbb{Q}$ with the standard
inner product, $C^1 = \operatorname{im} d_0 \oplus \operatorname{im} d_1^{\top}
\oplus \mathcal{H}^1$ with $\mathcal{H}^1 = \ker d_1 \cap \ker d_0^{\top}$.
Write $x = x_E + x_C + x_H$. Then $\Gamma_2(x) > 0$ exactly when $x_C \neq 0$,
and $\Phi_1(x) = 0$ exactly when $x_C = 0$ and $x_H = 0$.

*Proof.* Set $U=\operatorname{im}d_0$ and $V=\operatorname{im}d_1^{\top}$.
The chain law gives $U\perp V$, and
$(U\oplus V)^\perp=\ker d_0^{\top}\cap\ker d_1=\mathcal H^1$.
Finite-dimensional positive definiteness gives the unique orthogonal direct
sum $C^1=U\oplus V\oplus\mathcal H^1$. The defining linear systems have
rational coefficients, so their unique projected vectors are rational.
Now $d_1$ kills $x_E$ because $d_1 d_0 = 0$ and kills $x_H$ by definition.
On $\operatorname{im} d_1^{\top}$ it is injective: $d_1 d_1^{\top}\psi = 0$
implies $\lVert d_1^{\top}\psi \rVert^2 = \langle \psi, d_1 d_1^{\top}\psi
\rangle = 0$. So $d_1 x = d_1 x_C$ vanishes only when $x_C = 0$. $\Phi_1(x) = 0$
means $x \in \operatorname{im} d_0$, which by the direct sum means
$x_C = x_H = 0$. $\square$

The subscripts name Hodge components, not letters. The letter E acts on the
exact component; the co-exact component is what $\Gamma_2$ sees; the harmonic
component is the closed residual. `cochain.hodge_split` computes the split
exactly and `test_cochain.py::test_hodge_split_is_orthogonal_and_matches_the_classes`
checks the theorem on four complexes.

## 4. The alphabet

Every state transition or structural modification in a DDC regime emits
exactly one letter.

| Letter | Name | Runtime meaning | Must not claim |
|---|----|--------|--------|
| `E` | Exact repair | removes a defect that lies in $\operatorname{im} d_0$ | semantic truth, global correctness, authority |
| `R` | Residual projection | records the residual class; keeps $\Phi_1$ and $\Gamma_2$ | resolution |
| `C` | Context exposure | declares or splits the carrier, window or boundary | repair or authority |
| `I` | Integration | appends a receipt to the hash-chained tape | promotion |
| `Λ` | Structural lift | extends the carrier under a licence | arbitrary growth or automatic promotion |
| `D` | Descent | re-indexes or coarsens with a declared loss ledger | lossless transport unless witnessed |
| `M` | Typed refusal | refuses an invalid, unwitnessed or out-of-budget request | failure of the product |
| `T` | Terminalization | closes the tape on a routing terminal | authority |

```text
DDC records how an obstruction was handled, not whether the world is true.
```

## 5. Step receipts

Every admitted abstract step produces a deterministic record of the supplied
states, carrier labels and witness flags, linked to the previous record.
These flags are hypotheses about evidence presence; they do not authenticate
a receipt, a loss ledger, a licence or detector adequacy. Direct construction
of `State` likewise does not certify its diagnostics.

`measure` computes exact diagnostics. Passing a carrier map to `run_tape`
recomputes the initial and successor diagnostics, checks that R changes the
cochain by a coboundary, and binds topology and positive weights into the
tape genesis digest. Without that map, replay checks only the abstract laws.
The Lean theorems concern those laws, not an authenticated runtime. The record is:

```json
{
  "step_index": 2,
  "before_digest": "sha256 of the canonical before-state",
  "after_digest": "sha256 of the canonical after-state",
  "carrier_before": "two_triangles",
  "carrier_after": "two_triangles",
  "class_before": "ExactRepair",
  "class_after": "ExactRepair",
  "phi_before": "0", "phi_after": "0",
  "gamma_before": "0", "gamma_after": "0",
  "witness": {
    "receipt": false,
    "loss_ledger": false,
    "lift_licence": false,
    "reason": null
  },
  "control_after": "Open",
  "routing_terminal": null,
  "authority_effect": "None"
}
```

The integration tape chains receipts as
$h_{t+1} = \mathrm{SHA256}(t : h_t : \alpha : \mathrm{json}(r_t))$ with canonical
JSON (sorted keys, exact rationals as strings, floats refused). Production
receipts add a trace identifier, detector and terminalizer versions, protected
distinctions, and references to loss ledgers and lift requests. No receipt
stores raw user text by default. Tamper evidence assumes the collision
resistance of SHA-256 and an independently retained head and length (DDC-I-02).
Unanchored replay checks internal consistency only; a rewritten or truncated
history can remain internally consistent.

## 6. Diagnostic and runtime crosswalk

| DDC term | Runtime term | Diagnostic meaning | Routing |
|----|---|----|------|
| closure defect | $\Gamma_2$ | $d_1 x \neq 0$ | `Repair` or `Refusal`; never `CheckPassed` |
| irreducible residual | $\Phi_1$ | quotient mass, $\Phi_1 > 0$ | `RequiresLift` or residual terminal |
| exact class | `ExactRepair` | $\Phi_1 = 0$, $\Gamma_2 = 0$ | `CheckPassed` within the declared scope |
| open defect | `ActiveClosureFailure` | $\Gamma_2 > 0$ | `Repair` or `Refusal` |
| stabilized survivor | `ClosedResidual` | $\Phi_1 > 0$, $\Gamma_2 = 0$ | residual terminal or `RequiresLift` |

The four axes stay separate:

```text
DiagnosticClass ≠ RoutingTerminal ≠ ExtensionStatus ≠ AuthorityStatus.
```

Letters are not terminals. `CheckPassed` on the routing axis is not a licence:
this package adopts `F_term: REFUSED` as its explicit unlicensed-terminal
policy. This is a policy definition, not an application of an external theorem.

## 7. The laws

The eight candidate laws of the first draft are now step and control laws of
a finite-control transition system (Definition 10.1). The comparison
columns below refer exclusively to the deposited `engineLaw` and
`engine_violations` specifications, retained from repository commit
`e4a1214bb3e47570b0f74ecc9117c98f27a26b5e`. Their names are historical.
No theorem here establishes parity with a deployed Rust implementation;
claims about later runtime changes require a separate pinned conformance check.

1. **Trace typing** (OE010-03). Every letter carries its input class, output
   class, required witness and refusal condition, and every lawful step
   satisfies its letter's step law (`Ddc.well_typed_step`).
2. **Terminal absorption** (OE010-10). After `T` no letter is admitted, so `T`
   is the last letter of a lawful tape (`Ddc.lawful_T_is_last`).
3. **Refusal absorption unless lifted** (DDC-TAPE-01). After `M` only `C`
   (changed scope), `Λ` (licensed lift) or `T` may follow.
4. **Lift trigger.** `Λ` needs a licence and a trigger: the state before it is
   a `ClosedResidual` or its detector is inadequate. A trigger is not a licence.
5. **Integration requires a receipt.** `I` without a receipt is refused.
6. **Descent requires a loss ledger.** `D` without a loss ledger is refused.
7. **Exact repair discharges.** `E` needs an exact class before it, leaves the
   carrier unchanged, and leaves $\Phi_1 = \Gamma_2 = 0$ and a zero defect after
   it. A gauge repair cannot cross classes (Chapter 1), so `E` is never a
   disguised class change.
8. **Context exposure is not repair.** `C` changes the carrier and never lowers
   $\Phi_1$ or $\Gamma_2$. Hiding an obstruction by re-scoping has to be priced
   as `D` or `Λ`.

The step laws, compared with the deposited historical specification:

| Letter | Step law | Deposited comparison | Additional paper law |
|--|------|------|------|
| `E` | same carrier; after $\Phi_1 = \Gamma_2 = 0$ | yes (`ExactRepairLeftResidual`) | before class exact; zero defect after; adequate detector |
| `R` | same carrier; $\Phi_1$ unchanged | yes (`ResidualProjectionChangedMass`) | $\Gamma_2$ unchanged; adequate detector |
| `C` | carrier changes | yes (`CarrierUnchangedUnderRestructure`) | $\Phi_1$ and $\Gamma_2$ do not fall (Law 8) |
| `I` | state unchanged | yes (`InertOpMutatedState`) | receipt present (Law 5) |
| `Λ` | carrier changes | yes | licence and trigger (Law 4) |
| `D` | carrier changes | yes | loss ledger (Law 6) |
| `M` | state unchanged | yes | reason from the closed vocabulary |
| `T` | state unchanged; $\Gamma_2 = 0$ | yes (`TerminalizedOpenResidual`) | adequate detector |

**Theorem 7.1** (DDC-TAPE-03). Every step admitted by the paper laws satisfies
the deposited comparison laws, represented on the abstract state (`engineLaw` in
Lean, `engine_violations` in Python). The comparison is defined by the local source bytes; the theorem
does not execute Rust or assert correspondence with its current version. Lean:
`Ddc.paper_refines_engine`; Python:
`test_automaton.py::test_paper_laws_refine_the_engine_laws_on_every_step`.

## 8. Five minimal demos

Each demo is measured on a declared complex and replayed through the laws by
`code/ddc/demos.py`. Unlawful variants are kept as falsifiers.
`test_fsm_and_demos.py::test_every_demo_reaches_its_stated_verdict` pins every
verdict below.

**Demo 1 — boundary cancellation** (two triangles sharing an edge). An exact
defect is registered, repaired and sealed: `C·R·E·T`, routing `CheckPassed`.
A defect with circulation around one face ($\Gamma_2 = 1$) ends in a typed
refusal: `C·R·M`. Its falsifier `C·R·E·T` is refused at `E`, because the class
before `E` is not exact.

**Demo 2 — local green, global red** (a filled triangle with value 1 on every
edge). Each edge is locally consistent, yet $d_1 x = 3$, so $\Gamma_2 = 3$ and
$\Phi_1 = 3$. The lawful tape is `C·R·M`. Appending `T` is refused
(`TerminalizedOpenResidual`): a refusal does not license a seal.

**Demo 3 — stabilized survivor** (a hollow square with a unit defect on one
edge; $\Phi_1 = 1$, $\Gamma_2 = 0$). `C·R·T` seals on the residual terminal. A
licensed lift that adds capacity away from the cycle, `C·R·Λ·T`, re-measures
$\Phi_1 = 1$: the survivor persists, as Chapter 5 proves it must. Without a
licence the record is `C·R·M·T` with `REFUSED_REQUIRES_LIFT`. Two falsifiers:
a lift without a licence is refused, and a lift that attaches a face bounding
the cycle turns the survivor into $\Gamma_2 = 1$, after which `T` is refused.

**Demo 4 — detector collapse** (a constant detector reports zero on the
survivor). The lawful tape is `C·M` with `REFUSED_DETECTOR_INADEQUATE`; `C·M·T`
is refused (`BlindDetector`), because a collapsing detector is how false green
enters. A licensed detector lift, `C·Λ·T`, re-measures $\Phi_1 = 1$ and seals
honestly on the residual terminal.

**Demo 5 — descent with loss** (a path of four edges carrying
$(1, 2, \tfrac{3}{2}, \tfrac{1}{4})$, coarsened to two edges). With a loss ledger
the tape `D·I·T` books loss $\tfrac{7}{4}$ and seals. Without one, `D` is
refused (`MissingLossLedger`), and the lawful record is `M·T` with
`REFUSED_MISSING_LOSS_LEDGER`.

## 9. Runtime context and verification ceiling

The Rust crate `omega_discrete_deformation_calculus` is related runtime
context. Names in `docs/claim_code_map.yaml` are informational pointers, not
self-contained evidence of current engine conformance. This deposit proves
refinement only of its own historical comparison specification. It supplies
no authenticated licence evaluator and no test of the deployed Rust system.

## Part II — The eight letters

| Chapter | Letter | Central result |
|---|---|------------|
| [1](chapters/01_e_exact_repair.md) | `E` | gauge repair discharges an exact defect and cannot cross classes |
| [2](chapters/02_r_residual_projection.md) | `R` | projection keeps the class, with one coordinate per independent cycle |
| [3](chapters/03_c_context_exposure.md) | `C` | exposure changes the carrier and never lowers the diagnostics |
| [4](chapters/04_i_integration.md) | `I` | the receipt tape only grows and every letter enters the chain |
| [5](chapters/05_lambda_structural_lift.md) | `Λ` | a lift preserves norms; an extending lift cannot exactify a non-exact residual |
| [6](chapters/06_d_descent.md) | `D` | a descent is lossless exactly when the dropped tail is zero |
| [7](chapters/07_m_typed_refusal.md) | `M` | a refusal leaves the state unchanged and names a reason |
| [8](chapters/08_t_terminalization.md) | `T` | the abstract seal needs $\Gamma_2 = 0$ and adequate detection; continuation policy is a separate guard |

## Part III — Tapes

## 10. The tape automaton

**Definition 10.1.** A tape runs from a control state `Open`, `Refused` or
`Terminalized` and an abstract data state. A step is admitted when the control
admits its letter and the letter's step law holds. `T` moves the control to
`Terminalized`, `M` to `Refused`, and `C` or `Λ` after a refusal back to
`Open`. `Terminalized` admits nothing; `Refused` admits only `C`, `Λ` and `T`.
Replay stops at the first unlawful step, which is not recorded. The Python
automaton is `code/ddc/automaton.py`; the Lean one is `Ddc.run` in
`lean4/Ddc/Law.lean`. They state the same laws. The Lean model represents supplied
$\Phi_1, \Gamma_2$ by $\mathbb{N}$ values; the laws use only equality, order and zero
tests, which the non-negative rationals of the Python model share.

## 11. Tape theorems

Every theorem below is proved in `lean4/` with no axiom outside
{`propext`, `Quot.sound`} (`lean4/axiom_report.txt`) and checked on examples
in `code/tests/`.

**Theorem 11.1** (OE010-03, composition). If replay of $t_1$ succeeds,
replaying $t_1 t_2$ equals replaying $t_2$ from that successful endpoint.
If $t_1$ fails, the concatenated replay fails as well. The empty tape is the identity
(`Ddc.run_append`, `Ddc.lawful_append`, `Ddc.lawful_nil`). Lawful tapes
therefore form the morphisms of a category whose objects are control-state
pairs.

**Theorem 11.2** (OE010-10, terminal absorption). No step is admitted after
`T` (`Ddc.terminal_absorbing`, `Ddc.lawful_T_is_last`).

**Theorem 11.3** (DDC-TAPE-01, refusal absorption). After `M` only `C`, `Λ` or
`T` is admitted (`Ddc.refusal_absorbing`).

**Theorem 11.4** (DDC-TAPE-02, well-typed steps). Every step of a lawful tape
satisfies its letter's step law at the state it was taken from
(`Ddc.well_typed_step`).

**Theorem 11.5** (OE010-04, no authority). Every receipt a replay emits
carries `AuthorityEffect.none`, although the type has a second value
(`Ddc.authority_effect_none`); the receipt tape only grows
(`Ddc.receipts_prefix`).

**Theorem 11.6** (OE010-17, no free decrease). If a lawful step lowers
$\Phi_1$ or $\Gamma_2$, its letter is `D` or `Λ` (`Ddc.no_free_decrease`).

*Proof sketch.* `E` starts from $\Phi_1 = \Gamma_2 = 0$; `R` keeps both; `C`
cannot lower either; `I`, `M` and `T` leave the state unchanged. $\square$

**Theorem 11.7** (DDC-TAPE-04, open obstructions need a priced move). From a
state with $\Gamma_2 > 0$ and a non-terminal control, a lawful tape with no `D`
and no `Λ` keeps $\Gamma_2 > 0$ and never terminalizes
(`Ddc.open_needs_priced_move`). This is witness dominance at the level of
tapes: an open obstruction reaches a seal only through a booked loss or a
licensed lift. `test_automaton.py::test_open_obstruction_is_never_sealed_without_a_priced_move`
checks it by exhaustive reachability on a 32-state abstraction.

**Theorem 11.8** (CREDIT). The mnemonic "CREDIT" names the tape
C·R·E·D·I·T; it is only a mnemonic.

- (DDC-TAPE-05) CREDIT is lawful iff each of its six steps satisfies its law
  (`Ddc.credit_lawful_iff`).
- (DDC-TAPE-06) A lawful CREDIT starts from $\Phi_1 = \Gamma_2 = 0$
  (`Ddc.credit_starts_exact`): `E` needs an exact class, `R` keeps the
  diagnostics and `C` cannot lower them, so the residual was exact before `C`.
- (DDC-TAPE-07) Without a loss ledger at `D` it is not lawful
  (`Ddc.credit_needs_ledger`).
- (DDC-TAPE-08) It is realizable (`Ddc.credit_realizable`; Python:
  `demos.credit`, an exact defect on a hollow triangle repaired and then
  booked down to one edge).

CREDIT is therefore the exact-repair tape with a booked descent. It is not a
route for dissolving an obstruction.

**Theorem 11.9** (OE010-16, driver soundness). The §12 driver never proposes
`T` on an open or blind state, proposes `E` only on an exact class, and
proposes `Λ` only with a Law 4 trigger (`Ddc.driver_never_seals_open`,
`Ddc.driver_repairs_only_exact`, `Ddc.driver_lift_trigger`).

## 12. The §23 driver

The first draft generated tapes with a state machine whose table swapped two
classes: it tagged `ActiveClosureFailure` with $\Phi_1 > 0$ and
`ClosedResidual` with $\Gamma_2 > 0$. The corrected driver (OE010-16) proposes:

| Class of the current state | Letters the driver may propose |
|------|------|
| `ExactRepair` ($\Phi_1 = 0$, $\Gamma_2 = 0$) | `E` then `T`; `I` |
| `ClosedResidual` ($\Phi_1 > 0$, $\Gamma_2 = 0$) | `R`, `Λ` (Law 4), `T` to the residual terminal; `I` |
| `ActiveClosureFailure` ($\Gamma_2 > 0$) | `R`, `C`, `D`, `M`; `I`; never `T` |
| detector inadequate | `Λ`, `M`, `C`; `I` |

The four drivers of the first draft read as follows under the laws.
`C·R·E·I·T` (autopoietic) is lawful on an exact defect. `C·R·M·T` (refusal) is
lawful when the refused state has $\Gamma_2 = 0$; on an open state the lawful
record is `C·R·M`. `C·R·Λ·I·T` (self-examination) is lawful from a closed
survivor with a licence when the lifted state has $\Gamma_2 = 0$. `D·I·T`
(allopoietic) is lawful with a loss ledger when the target has $\Gamma_2 = 0$.
The residual-progress guard of the first draft is Theorem 11.6.

## 13. Open laws

These remain open. Bounded checks are recorded as computed fixtures, never as
proofs.

- **Trace equivalence** (DDC-OPEN-01). When do two tapes denote the same
  handling: same terminal, same diagnostic effect, same receipts, same loss
  ledger, same carrier endpoint? No equivalence is defined here.
- **Normal forms** (DDC-OPEN-02). Whether finite tapes reduce to forms such as
  `C·R·E·I·T`, `C·R·M·T`, `C·R·Λ·I·T` and `D·I·T`. No universal normal form is
  assumed.
- **Detector adequacy in general.** Demo 4 covers the constant detector; the
  empty carrier, acyclic collapse, shape-only verifiers and all-green or
  all-open terminalizers remain future fixtures, not results.
- **Separation from rewriting logic**, **lift minimality** and **universal
  obstruction completeness** are research questions (Part IV).

Composition (Theorem 11.1) and the non-authority invariant (Theorem 11.5),
open in the first draft, are now proved.

## 14. Deformations of the window

**Proposition 14.1** (OE010-05). A deformation
$d_i \mapsto d_i + \mu_i$ keeps the window a complex iff
$(d_1 + \mu_1)(d_0 + \mu_0) = 0$, i.e. iff
$d_1 \mu_0 + \mu_1 d_0 + \mu_1 \mu_0 = 0$ (the Maurer–Cartan condition).

*Proof.* Expand and use $d_1 d_0 = 0$. $\square$

`cochain.deformation_obstruction` computes the left-hand side exactly;
`test_cochain.py::test_maurer_cartan_obstruction_detects_unlawful_deformations`
shows a zero deformation passing and a single-entry bump failing.

## Part IV — Positioning

Part IV maps the research neighbourhood. Its statements are positioning, not
verified literature conclusions; no external citation is upgraded to a result.

## 15. Research agenda

Six modules steer further work, each recast as a directed attack rather than
a validation request.

| Module | Question | Relevance to DDC |
|---|------|------|
| A. Higher categories and operads | Which structures model finite control loops without unpriced coherence? | may supply composition laws for tapes; not proof that DDC is an operad |
| B. Sparse $\ell^1$ cochains | How stable are quotient obstructions under perturbation? | diagnostic engines for $\Phi_1$ and $\Gamma_2$ |
| C. Sheaf obstruction | Which Čech or cellular frameworks separate local consistency from global coherence? | detectors for local-green, global-red failures, once covers are declared |
| D. Verified rewriting | How can compiler passes be receipt-preserving operations? | concrete software examples for `E`, `D`, `M`, `T` |
| E. Finite shadows of continua | How can infinite objects be admitted only through finite shadows or oracles? | continuum claims route to `OracleNeeded` |
| F. Prior art and negative results | Has anyone typed the role a computation plays in an obstruction's life? | tests the novelty statement |

Every result from these modules is to be classified as an established
finite-hypothesis theorem, a plausible formalization target, an analogy, a
likely category error, or unsupported; with the exact construction, the
missing adapter data, the smallest demo and the likely counterexample.

## 16. Prior art and the rewriting-logic objection

Five traditions are closest (DDC-POS-01).

- **Rewriting logic and Maude** is the strongest computational neighbour: it
  specifies systems by labelled, potentially conditional rules $t \to t'$
  modulo equations. Such a specification can include obstruction diagnostics,
  witness conditions and receipt fields. DDC supplies one declared combination
  of these choices; this paper proves no separation in expressive power.
- **Constructor Theory** states physics through possible and impossible
  transformations; it is a philosophical analogy with no operation ledger or
  cochain quotient.
- **Structural realism** aligns with the representation-first stance but is
  not mathematical support by itself.
- **Hypergraph rewriting** treats evolution as rule application; its physical
  claim is empirical, not runtime verification.
- **Coalgebra** gives behaviour and observation semantics, a promising target
  for trace semantics, without a cochain obstruction calculus.

Adjacent fields supply candidate law sources: trace monoids and abstract
rewriting (normal forms, confluence), operational semantics and effect
systems (typed letters), provenance semirings and proof-carrying code
(receipts), event structures (concurrency), double categories and string
diagrams (transport), cellular sheaves and chain homotopy (trace
equivalence), discrete Morse theory (cancellation), CEGAR and abstract
interpretation (detector adequacy), and equality saturation (repair search).

The sharpest objection is "DDC is rewriting logic with labels". The concrete
contribution evaluated here is the selected policy: obstruction diagnostics
(§3), typed step guards (§7), chained records (§5), declared licence and ledger
conditions (Laws 4 and 6), refusal control (Theorem 11.3), and terminal
absorption (Theorem 11.2). Theorem 11.5 proves that emitted receipt fields say
`none`; authorization remains outside the model. These choices do not prove
that rewriting logic cannot express DDC. A formal translation and a prior-art
review of the combination remain open.

## 17. Novelty statement

Unsafe: "DDC is a theory of everything", "every process is obstruction
elimination", "representation is all that exists".

Defensible programme claim (DDC-POS-02): DDC formalizes a finite operation
ledger in which every structure-creating, obstruction-exposing,
obstruction-eliminating, obstruction-carrying or obstruction-refusing event is
a typed step with a replayable record that confers no authorization. What may be
distinctive is the combination of six parts:

1. finite cochain diagnostics;
2. typed letters recording what a step did to an obstruction;
3. replayable receipts;
4. proof-assistant and runtime counterparts;
5. machine-readable governance boundaries;
6. a firewall that stops successful representation becoming trusted action.

This stays a programme claim until the prior-art review of Module F is
complete.

## 18. Risks and fences

| Risk | Fence |
|---|--------|
| Universality becomes tautology | an obstruction needs a declared carrier, protected distinction, detector, witness or refusal rule, and terminalizer; DDC must say when it returns `NoRule`, `DetectorInadequate` or `OracleNeeded` |
| "The universe is not creative" needs a negative result | DDC tests whether domains reuse the same letters; it does not prove that no new structure exists |
| The word "algebra" overclaims | the constructed object is a typed trace calculus with proved tape laws; equivalence and normal forms stay open |
| Continuum smuggling | continuum objects need finite shadows, completion receipts or oracle interfaces, else `OracleNeeded` |
| Authority laundering | receipts record conditional decisions; authorization is outside this model. Theorem 11.5 establishes only the constant receipt field |
| Detector inadequacy | a blind detector cannot seal (`BlindDetector`); authority-sensitive uses need a declared adequacy record |

## 19. Prior-art questions

The standing question for literature search: *has any theory defined an
operation alphabet whose symbols classify the role a finite computation played
in an obstruction's life, rather than recording that a transition occurred?*
Compare against rewriting logic, trace monoids, operational semantics, effect
systems, proof-carrying code, provenance semirings, event structures, double
categories, string diagrams, cellular sheaves, chain homotopy, deformation
complexes, discrete Morse theory, process calculi, higher rewriting,
coalgebra, Constructor Theory, hypergraph rewriting and ontic structural
realism. For each, classify and return the construction, the finite
hypotheses, the missing adapter data, the smallest demo and the likely
counterexample. If DDC is rewriting logic with labels, say exactly why; if
not, name the minimal formal object that separates them.

## 20. Final position

DDC is a finite typed trace calculus for obstruction-handling operations. Its
product value is that it records what kind of finite operation was performed
on an obstruction, not only whether a system passed. Its research value is a
possible substrate-independent operation ledger linking cochain obstruction,
rewriting, proof-carrying traces, provenance and authority firewalls. The
warning stands: do not sell the universe; prove trace equivalence, detector
adequacy and the separation from rewriting logic first.

```text
DDC tape = replay evidence · DDC receipt = bounded verification data
DDC terminal = routing terminal · DDC authority = None
```

## 21. Residuals

| ID | Residual | Route |
|--|--------|-----|
| R-DDC-01 | This version's new mathematics: the tape automaton and Part III | discharged here |
| R-DDC-02 | The historical comparison model's `E` law admits class-crossing edits; the paper requires an exact class before `E` | historical comparison gap; resolved in governance contracts; Rust parity separate |
| R-DDC-03 | The historical comparison model's `R` law does not fix $\Gamma_2$ | historical comparison gap; resolved in governance contracts; Rust parity separate |
| R-DDC-04 | The historical comparison model does not enforce Law 8 (no scope laundering by `C`) | historical comparison gap; resolved in governance contracts; Rust parity separate |
| R-DDC-05 | The historical comparison model does not check Laws 3–6, the refusal vocabulary or detector adequacy at step level | historical comparison gap; resolved in governance contracts; Rust parity separate |
| R-DDC-06 | $\Phi_1$ needed a dual witness, not only a primal potential | discharged here: `cochain.phi1_certificate` |
| R-DDC-07 | Proposition 3.2 and Theorem 3.3 have written proofs only; mechanizing them needs linear algebra beyond core Lean | Lean: a later version |

## References

See [`docs/references.md`](docs/references.md).
