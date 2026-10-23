# Audit of the Genesis process-comparison campaign unit

AuthorityEffect: None. AI self-review, awaiting human review.

Scope: this final unit only, source commit f34f0b8e6, base
4d50f22373578df83989dc8ec09fdface91289c2. Earlier campaign units have
separate claim reviews and are not covered by this umbrella audit.
Stages run: overclaim, obstruction, symmetry scanner, pattern lint, manual
code-pattern review, and documentation. Agents/skills reviews: not run,
no matching change. No Lean or cargo build was run by this audit; the author
replay receipt records the successful target build.

Result: overclaim 0 FULL, 1 NARROWED, 0 OVERCLAIM for the whole-process
question; automatic hunters 0 HIGH, 3 MEDIUM, 63 LOW. The three documentation
MEDIUM findings are unchanged base links. No node status was raised.

## 1. Claims vs proofs (overclaim-hunter)

# Review of the declared Genesis process comparison

AuthorityEffect: None. AI self-review, awaiting human review.

Scope: PGW-MINIMAL-OR-INITIAL-REFUSED on main 4d50f22373578df83989dc8ec09fdface91289c2.
Method: inspect the defined process objects, morphisms, complete finite-word
readouts, cardinality proof, actual-source replay relation and independent
exact finite orbit audit. Not rebuilt by this review; the authoring campaign
receipt supplies the successful target replay.

Result: 0 FULL, 1 NARROWED, 0 OVERCLAIM for the requested whole-process question.
The declared comparison results below compile; they do not certify the full
Alpha engine's class membership or minimum program/declaration cost. The
historical refusal record and its PROVED_PROSE status remain unchanged.

| Atomic claim | Declaration and exact line | Verdict |
|---|---|---|
| Every finite action word has the same readout after an invisible clock extension | `all_words_agree` (`lean4/CampaignGenesisProcessComparison.lean:164`) | FULL in the declared class |
| No finite-state process maps to its period-(card+1) lift | `no_initial_in_clock_closed_class` (`lean4/CampaignGenesisProcessComparison.lean:175`) | FULL with a chosen action |
| Any self-loop forbids a map to the invisible two-clock lift, without state finiteness | `no_clock_hom_of_self_loop` (`lean4/CampaignGenesisProcessComparison.lean:210`) | FULL |
| Actual optional source runs agree with source replay, including failure | `source_advance_matches` (`lean4/CampaignGenesisProcessComparison.lean:230`), `source_run_matches` (`lean4/CampaignGenesisProcessComparison.lean:243`) | FULL |
| Actual source supply is a self-loop and gives the clock obstruction | `source_supply_self_loop` (`lean4/CampaignGenesisProcessComparison.lean:248`), `no_source_initial_in_clock_closed_class` (`lean4/CampaignGenesisProcessComparison.lean:251`) | FULL for the regime-history interpreter |
| A reachable, behaviorally reduced finite process has minimum state count among same-answer finite models | `all_words_minimum_size` (`lean4/CampaignGenesisProcessComparison.lean:183`) | FULL with explicit reachability/reduction premises |
| Adequacy alone forces minimum state count | `nonminimal_adequate_process` (`lean4/CampaignGenesisProcessComparison.lean:120`) | REFUSED by the concrete control |
| Whole Alpha engine minimum or initiality in an unspecified class | not proved | NOT PROVED; original boundary retained |

The class admits additional unobserved internal state. Morphisms preserve
actual roots, actions and readouts. The finite-state theorem uses a nonempty
action alphabet (a chosen action is explicit). The self-loop theorem drops
state finiteness and applies to the exact actual-source regime interpreter.
Source failure is absorbing, not a no-op. Finite state-cardinality minimality
is a different resource claim from program size, declaration count or the
engine input floor. No conclusion about Alpha runtime/license behavior follows.

Numbers recomputed: 682 unary Boolean-readout processes, 41,764 clock-component
candidate maps, 98,346 exactly behavior-equal pairs, 1,230 valid minimum-size
comparisons, and all sixteen maps into the supply-loop clock countermodel.
SymPy checks the census and the clock target's zero fixed-point trace. Three
explicit missing-premise/morphism controls are checked. Sixteen terminal
axiom audits match the successful replay; no new kernel axiom is introduced.
The general Lean results have no independent-check state bound.

What the scanner cannot decide: which challenge interface and morphisms are
appropriate for the full historical engine, whether it satisfies reduction and
reachability in a finite model, or whether a human accepts the selected class.
The declared class choices are not inferred from a frozen tag or repeated runs.

Corrections to the author's claims: none required within the declared scope.
The whole-engine question remains explicitly unresolved. The strict scanner's
output has four LOW prompts: three inherited tensor prompts and one new
census-number prompt (682, 41764, 98346, 1230). The independent checker
recomputes all four census numbers; it computes rather than hard-codes their
literals. The findings are retained in the campaign checks receipt. The tensor
conclusions are unchanged by this unit. No
historical descriptor numbers were edited by this unit. The process census,
map counts, pair counts, comparisons and controls above were recomputed by the
independent checker in normal and optimized mode. The axiom count was parsed
from the successful final author replay, not from a failed build.

## 2. Obstructions

No automatic obstruction finding (0 HIGH, 0 MEDIUM, 0 LOW).

| Location | Hand review | Limit |
|---|---|---|
| comparison class and LabelledHom | Root, each action and readout preservation are explicit; all-word quantifiers survive in the declarations | No assertion that historical Alpha belongs to a new category |
| all_words_minimum_size | Reachability and behavioral reduction are premises; state count is the concluded resource | No program/declaration minimum or full engine runtime refinement |
| sourceModel | Actual source optional replay and supply self-loop instantiated; failure remains absorbing | Does not model responder, scheduling or license implementation |

No O3 route was flagged; no new node verdict is inferred from a scanner.

## 3. Symmetry breaks

No automatic finding (0 HIGH, 0 MEDIUM, 0 LOW). By-hand rule comparison:
not run, no matching rule, skill, campaign instruction or scanner change.
The author applies the same source-hash and axiom limits to this unit as the
other campaign units.

## 4. Anti-patterns

No automatic finding (0 HIGH, 0 MEDIUM, 0 LOW). Hand review:

| Cards | Result | Evidence / remaining boundary |
|---|---|---|
| AP_LN_001, AP_LN_004, AP_MD_022 | No new admission, custom axiom, unsafe or native decision; final success supplies audits | Committed LF source and sixteen permitted audits in replay receipt; failed attempts are not proof |
| AP_LN_002, AP_MD_006 | Target and imported cache declared separately | Default library, Mathlib and Derivation.Initiality were not rebuilt |
| AP_MATH_006, AP_MATH_011, AP_MATH_022 | Exact arithmetic, explicit bounded census, no authority/status promotion | General Lean all-word theorems are separate from the state-bound-three census |
| AP_PY_001, AP_PY_006, AP_PY_009 | Checker imports no repository code, no machine path; only scoped SymPy typing suppression | Active source/evidence hashes and preserved companion histories verified by campaign finalization |
| AP_PY_019 | Missing-premise controls check actual failures | Root-only map is checked to violate action preservation; hidden-state and unreachable controls have explicit observations |

No AP_MATH finding proposes a new node status. The authorized policy/class
extensions remain choices rather than conclusions from the frozen source.

## 5. Documentation

Worst findings: three MEDIUM broken relative links in generated/aggregate
prose. All three source lines were compared with the base and are unchanged:

| Path and line | Finding | Disposition |
|---|---|---|
| dag/derivations/MASTER_DERIVATION_LEDGER.md:1030 | ../foundations/theory_of_finite_quantum_foundations.md | Existing base link; no repair made by this audit |
| papers/core/finite_quantum_mechanics.md:431 | v | Existing base link; no repair made by this audit |
| papers/core/finite_quantum_mechanics.md:1014 | research/quantum_to_classical_descent/README.md | Existing base link; no repair made by this audit |

The sixty-three LOW findings comprise eight new path::symbol references
that the filesystem-only scanner treats as filenames, and fifty-five inherited
aggregate paths/anchors. All eight new references were checked against actual
Lean declarations and the replay anchors. Inherited paths are not certified
by this unit. Generated README facts are checked by the required campaign gate.
No documentation scanner warning is used as evidence for a theorem.

## 6. Agents and skills

Not run: no matching agent, teamwork, skill or rule change. No learning/pattern
card edit or recursive audit was made.

## What no stage could decide

Human acceptance of the comparison class, membership/reachability/reduction of
the full Alpha engine, engine runtime or license behavior, minimum program or
declaration cost, and initiality under other morphisms. Independent human
review remains pending. The wiki is intentionally unchanged until review and
merge. Repeated-run agreement is not promoted to an engine theorem.
