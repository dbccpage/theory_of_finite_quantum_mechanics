# From the inert mark to a general-purpose evaluator: how far Genesis supports computation

**AuthorityEffect:** None.

**Scope.** This paper extends the derivation from the edge of the current Genesis derivation "to the right", toward a Turing-complete rewriting regime, starting from the primitive inert mark `<>`. It records, step by step (C1 to C8), what is kernel-checked in Lean 4 (v4.35.0, Mathlib v4.35.0), what is checked by exact finite computation in Rust and Python, what is imported from Mathlib, and what is declared or open. It stops where honest support stops.

**Fences.**

- `<>` is inert. Nothing here derives the identity convention (`TFQ-0423`, `PGW-IDENTITY-CONVENTION-UNDECIDABLE`), the existence of an alphabet beyond the declared construction, or an unbounded supply of fresh marks. Each is a declared input and is named as one.
- Finite instances are not general theorems; every finite instance below states its instance.
- Mathlib's computability theory (`Nat.Partrec.Code`, `Turing.TM0`, `TM1`, `TM2`, their simulations, `ComputablePred.halting_problem`) is IMPORTED infrastructure. It is cited, not re-derived.
- No physical Church-Turing claim is made, and no smallest general-purpose machine is claimed.

## 1. Where Genesis ends

The reading order is `dag/derivations/PREGENESIS_TO_WDP_ROUTE.md`. The facts used here, with the records that carry them:

| Fact | Record | Status in the DAG |
|---|---|---|
| `<>` is an inert inscription, supplied or mentioned, with no object-language job | `PG-INERT-DIAMOND`, `TFQ-0000` | `DEFINITION` |
| Six distinct operations; only Admit changes the admitted state | `PG-SIX-OPERATIONS` | `DEFINITION` |
| An exhibited cut needs a law; endpoints are apart | `PG-ADMISSION-FLOOR` | `PROVED_LEAN` (external twin) |
| Free monoids on finite alphabets of different sizes are not isomorphic | `PG-FREE-MONOID-NONISO`, `TFQ-0373` | `PROVED_LEAN` (external twin) |
| First separation of two marks has item cost two inside the declared grammar | `PG-GEN-COLLAPSE-AND-FIRST-SEPARATION` (node), `TFQ-0381` (source record) | `PROVED_LEAN` (external twin); the Lean twin of the cost-two minimum is absent from this checkout |
| Irreflexive relation forces distinct endpoints | `PG-GEN-IRREFLEXIVE-DISTINCT` | `PROVED_LEAN` |
| Contexts with holes and plugging profiles | `TFQ-0433` | `DEFINITION` |
| Context count `(n+1)^a - n^a` per form of arity `a` | `TFQ-0436` | `PROVED_LEAN` (external twin) |
| Changes commute with injective rewriting of terms | `PG-GEN-REWRITING-COMMUTATION` | `PROVED_LEAN` (external twin) |
| Supply alone is a no-op; only admission changes the regime | `TFQ-0379`, `PG-GEN-SUPPLY-NO-OP` | staged Lean copy in this checkout |
| Closed Genesis saturates: at most `n(n-1)/2` rounds, then any further requirement needs a fresh datum (external supply) or a new requirement kind (external goal) | `TFQ-0451` (`PGW-NO-ENDOGENOUS-DEMAND-GENERATOR`), `TFQ-0487` | `PROVED_PROSE` and source record; Lean twins external |
| Leftover feedback gives unbounded sequence lengths, not an unbounded set of results | `TFQ-0482` | `PROVED_LEAN` (external twin) |
| Demand accounting `s_next = s - d + b` | `PG-DEMAND-ACCOUNTING`, `TFQ-0369` | external twin |
| The freeze-endpoint ledger and its open obligations `TFQ-0496` to `TFQ-0504` | `TFQ-0486` | `SOURCE_RECORD` |

Most Genesis Lean sources are external (`external:` paths under `the_symbol_game/...`). The one Genesis event semantics that is present in this checkout is the staged copy `dag/results/PG-GEN-SUPPLY-ERASURE/runs/20261019T215447Z_staged/inputs/the_symbol_game/omega_engine_education/documentation/001_oegen/primitives/lean4/SupplyErasure.lean` (its `BEGIN COPY` block holds `Regime`, `Event`, `stepE`, `replayE` from the sealed derivation `19L57G1`). The Genesis `Step3` and `Reach3` source is only partly present: `dag/results/PG-GEN-REWRITING-COMMUTATION/runs/20261019T215447Z_staged/inputs/the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/Second/Rename.lean` (lines 1 to 130 are read), which imports `Second.Cost` (not staged).

The decisive observation for this paper is `TFQ-0451` and `TFQ-0487`: the closed Genesis system is bounded. Everything beyond the bound is paid for from outside. That is the Genesis form of the bounded-regime obstruction (C3), and it is why the unbounded supply is recorded as a declared import (C4).

## 2. The chain and its status

| Step | Content | Status | Lean (module::name) |
|---|---|---|---|
| C1 | Alphabet from separation | Fixed instance computed; general canonical alphabets proved for a mirror definition; identity convention declared | `GenesisComputation::first_separation_replay`, `canonicalRegime_pairwise`, `separated_marks_not_collapsed` |
| C2 | Words, contexts, rewriting | `Step`/`Reach`, letter-renaming commutation proved; one-hole contexts related to Genesis contexts; Genesis `Step3` NOT shown to be a word step | `Step.map`, `Reach.map`, `Reach.of_map`, `oneHole_iff_split`, `plug1_ofSplit` |
| C3 | Bounded-regime obstruction | Proved: decider, finite configuration space, sound three-valued verdict; unbounded need shown on a concrete machine | `reachB_iff`, `decideReachB_iff`, `card_wordsLE`, `verdict_*`, `runner_unbounded` |
| C4 | Unbounded supply | Genesis `stepE` has no cap (proved); the supply itself is a DECLARED IMPORT | `replay_admitDatum_replicate`, `genesis_unbounded_admission`, `not_closed_of_unbounded`, `supply_growth` |
| C5 | TM0 as a rewriting regime | Proved: step simulation both directions, closures, halting equivalence; tested on small machines | `step_fwd`, `step_bwd`, `reaches_fwd`, `reach_bwd`, `halts_iff` |
| C6 | General-purpose evaluator | Proved: one fixed TM2 machine and one fixed composite TM0 machine, halting equivalent to `Code.eval`; finite mark set; output form at TM0 level OPEN | `universal_code`, `tm2_computes_eval`, `halts_iff_eval_dom`, `used_marks_finite` |
| C7 | Undecidability | Proved for the explicit family of start words of the fixed regime; the reduction over encoded instances is CONDITIONAL | `halting_not_computable`, `reach_irreducible_not_computable`, `nfReach_not_computable`, `reach_problem_not_computable` |
| C8 | Binary coding fence | Proved: injective fixed-width binary coding of any finite alphabet with a decoder | `decode_encode`, `encodeWord_injective`, `encodeMarks_injective` |

The axioms used by every headline theorem are among `propext`, `Classical.choice`, `Quot.sound`; the full list is `dag/research/genesis_to_universal_computation.axioms.txt` (81 declarations, none outside the allowed set, none using `sorryAx` or `ofReduceBool`).

## 3. The steps in detail

### 3.1 C1. Alphabet from separation

The mirror of the sealed events is copied byte for byte into `lean4/GenesisComputation.lean` (lines 60 to 110, namespace `GenesisCopy`), with its custody note. On it:

- `first_separation_replay`: the history `[admitDatum, admitDatum, admitForm 1, admitInst 0 [0], impose 0 1]` replays from the empty regime to the regime with two data, one unary form, the instance `(0,[0])` and the demand `(0,1)`. This is a fixed instance, checked by `decide`. It is the cost-two SHAPE (one form, one instance); the cost-two minimum itself is `TFQ-0381`, whose Lean twin is not in this checkout.
- `UnarySep` (line 123) is a mirror, defined here, of the hole-only unary case of the Genesis `separable` (`TFQ-0433`) with derivability by instance membership. It is not the external definition. It is decidable (`unarySep_iff` and the `Decidable` instances), and so are `Collapsed` and `PairwiseSeparated`.
- `first_separation_pairwise`: the two marks of the first-separation regime are told apart. `Mark2` is the two-mark type with `mark0 := <>` and `mark1 := its first separated successor` (`Mark2.toDatum_bijective`). That `mark0` is `<>` is a declared labelling.
- `canonicalRegime_pairwise`: for every `n`, the canonical regime on `n` marks (`n` data, `n - 1` unary forms, the instances `(i,[i])`) is pairwise separated. This generalises the first separation to any finite alphabet size at the cost of `2(n-1)` items, as a statement about the mirror `UnarySep`.
- `two_marks_without_forms_collapsed`: with no form at all, two admitted marks are collapsed (decided). Under the opaque identity convention they are one internal class; under the exact-inscription convention they are two inscriptions. `separated_marks_not_collapsed` shows that on a pairwise separated alphabet the two conventions give the same marks. Blank, state and end marks of a machine must therefore be admitted as separated marks, or the convention must be declared.

**Declared input:** the identity convention. It is recorded as the inductive type `IdentityConvention` (`opaqueConv`, `exactInscription`) and is never used to derive anything.

### 3.2 C2. Words, contexts, rewriting

- Words are `List α`, the free monoid on the letters (`PG-FREE-MONOID-NONISO` is the Genesis statement that alphabets of different sizes give non-isomorphic free monoids; it is cited, not re-proved here).
- A rule is a pair of words, a one-hole context is a pair `(u, v)`, and `Step R w w'` holds when `w = u ++ l ++ v` and `w' = u ++ r ++ v` for a rule `l -> r` (lines 261 to 272). `step_iff_plug` states this as "a rule applied under a one-hole context". `Reach` is the reflexive-transitive closure.
- Commutation with letter renaming, the analogue of `Step.rename` and `Reach.rename` of `PG-GEN-REWRITING-COMMUTATION`: `Step.map` and `Reach.map` for every letter map, and `Reach.of_map` (with `Step.exists_of_map`) for an injective letter map, where the converse needs the observation that a step from a renamed word stays in the image.
- Genesis contexts versus word contexts. A Genesis context of arity `a` is a tuple of slots, each a datum or a hole, and plugging fills every hole with one datum (`TFQ-0433`). `GCtx`, `plug1`, `holes` mirror this. `oneHole_iff_split` shows that the contexts with exactly one hole are exactly `ofSplit u v`, `ofSplit_injective` that the split is unique, and `plug1_ofSplit` that plugging `d` gives `u ++ d :: v`. So the one-hole Genesis contexts are the word contexts `(u, v)` with `|u| + |v| = a - 1`, and a word rule plugs a word where Genesis plugs one datum.
- Finite checks of the counts: for `n = 2`, `a = 3`, `19 = 3^3 - 2^3` contexts with a hole and `12 = 3 * 2^2` with exactly one hole (`genesis_context_count_n2_a3`, `genesis_one_hole_count_n2_a3`, by `decide`); Rust checks `n` from 0 to 4 and `a` from 1 to 5, Python `n` from 0 to 3 and `a` from 1 to 4.

**Where Genesis `Step3` is narrower.** `Step3` is a relation on states `(T, A, a, b)`: a finite set of terms (natural numbers), a finite set of assertions (pairs of terms) and two named terms, with three moves (add a fresh term, add an assertion, identify two terms by merging). It has no order on terms, its `identify` is a non-injective merge, and it has no user-supplied rule list. It is a different object from a semi-Thue step. No embedding of `Step3` into word rewriting is proved here, and none is claimed. What is proved is the same commutation law for letter renaming on the word side. This is an OPEN correspondence with an exact statement: construct a word encoding of `St` under which each of the three moves is a word step, or show that none exists.

### 3.3 C3. The bounded-regime obstruction

Let `α` be a finite alphabet and `RL` a finite rule list.

- `succList` computes all one-step rewrites by scanning the positions; `mem_succList` states that `w' ∈ succList RL w ↔ Step (inRules RL) w w'`. So `Step` is decidable for a finite rule list (this is the rewriting analogue of enumerating contexts).
- `StepB RL L`, `ReachB RL L`: steps and reachability with every word of length at most `L`. The configuration space is `wordsLE α L`, with exactly `1 + k + ... + k^L` words (`card_wordsLE`, `k = |α|`).
- `reachB_iff` and `decideReachB_iff`: `ReachB` is decided by an explicit breadth-first closure of at most `|wordsLE α L|` rounds (`rtg_iff_mem_reachN_card`), with `reachSet_card_le` bounding the reachable set. This is a `Fintype` decision procedure.
- Three-valued verdict `verdict`: `reachable`, `unreachable`, `boundExceeded`. `verdict_reachable_sound` and `verdict_unreachable_sound` show that the first two answers are correct for the UNBOUNDED relation (the second because a closed bounded search, `Closed`, cannot miss a longer path: `closed_reach`), and `verdict_boundExceeded_witness` returns a step that leaves the bound. `Reach.exists_bound` shows that unbounded reachability is the directed union of the decidable bounded relations (hence, informally, semi-decidable; this is not formalised).
- `not_closed_of_unbounded`, `closed_bounds_reach`: a regime that reaches arbitrarily long words is never closed at any bound, and a closed bounded search has only words of length at most `L` reachable.

**What this answers of `TFQ-0497`.** `TFQ-0497` asks for a decision procedure for collapse and separability over the well-formed contexts of a finite regime. What is built here is (a) the decision of `Step` and bounded `Reach` for word rewriting, and (b) the decision of the unary, hole-only mirror `UnarySep`/`Collapsed`/`PairwiseSeparated` on a finite regime. The procedure over all Genesis contexts of the sealed regime (including uniform rules and higher arity), and its use to decide `Y-2`, `T-1`, holding two and exhaustion, is NOT built. `TFQ-0497` stays OPEN in that form.

**Universality needs unbounded space.** The right-running machine (`runner`, one state, moves right forever) reaches words of every length (`runner_unbounded`), so its regime is never closed (`runner_not_closed`); the bounded decider returns `boundExceeded` for it at every bound. This is the concrete instance. The general sentence "no fixed bound suffices for a general-purpose regime" is CONDITIONAL in the form in which it can be stated here: if `x -> startWord x` were computable, a bound `L` that witnessed every halting start word would make `nfReach` decidable, contradicting `nfReach_not_computable`. The computability of `startWord` is not proved (see C7).

### 3.4 C4. Unbounded supply as an explicit import

- `replay_admitDatum_replicate`: `k` copies of `admitDatum` replay to `data := base.data + k`. `genesis_unbounded_admission`: for every `n` a history reaches at least `n` data. `stepE_data_mono`: no event lowers the number of data. So the Genesis event semantics `stepE` itself has no cap: unbounded admission is PERMITTED. This is a statement about the copied `stepE`.
- It is not DERIVED. Every `admitDatum` is a host event. `TFQ-0451` and `TFQ-0487` record that a closed run saturates and that any further requirement needs a fresh datum from outside, and `TFQ-0504` (OB-1) records that no endogenous demand generator exists. `TFQ-0482` does not supply space: it gives unbounded SEQUENCE lengths from two-change cycles over a bounded state ("unbounded lengths of sequences reaching a result, not an unbounded set of results"). Time without space cannot build the configurations that a general-purpose machine needs.
- `supply_growth`: in the demand accounting `s_next = s - d + b` (`PG-DEMAND-ACCOUNTING`), if every round has strictly more births than discharges, the active count is at least `s 0 + n` after `n` rounds. The births are an input; Genesis does not derive them.
- `UnboundedSupply RL a` is the declared form of the import for a rewriting regime: for every `L` a word longer than `L` is reachable from `a`.

**Declared import (named):** *unbounded admission of fresh blank marks*, supplied by host events. It is the same import as `TFQ-0451`'s "external supply" and is not smuggled in.

### 3.5 C5. Turing machines as rewriting regimes

`lean4/GenesisCompTM.lean`. A Mathlib `Turing.TM0.Machine Γ Λ` is encoded on configuration words over `Sym Γ Λ` (end markers `lend`, `rend`, state marks `st q`, tape marks `sym a`): `lend · (left cells, far to near) · q · a · (right cells, near to far) · rend` (`cfgWord`). `Rep c w` says that `w` represents `c`, with arbitrary blank padding at the far ends. The rule set `Rules M` has five shapes (write, right, right-end, left, left-end). The two end rules write a fresh blank mark exactly when the head leaves the written part of the tape; this is the only place where words grow.

- `step_fwd`: if `TM0.step M c = some c'` and `Rep c w`, then a step of `Rules M` takes `w` to a word `w'` with `Rep c' w'`.
- `step_bwd`: if `Rep c w` and `Step (Rules M) w w'`, then `TM0.step M c = some c'` with `Rep c' w'`. So the rewriting is deterministic on represented words, and a halted configuration has no rewrite.
- `rep_exists`, `rep_unique`: every configuration is represented and a word represents at most one configuration.
- `reaches_fwd`, `reach_bwd`: the same for the closures. `halts_iff`: the machine halts from `c` iff some word reachable from a representing word is irreducible.
- `card_sym`: the mark budget is `|Γ| + |Λ| + 2`. All of these marks must be admitted and separated, which `canonicalRegime_pairwise` provides for any finite count; the enumeration of marks by `Fintype.equivFin` is a declared choice.
- `ruleList` and `mem_ruleList`: for a finite machine the rule set is the finite list `ruleList M`, so the bounded decider of C3 applies. `reach_ruleList_iff` transfers `Reach`.
- Lean instance: `writeOne_halts` (a machine that writes a one and halts).
- Finite computations (not general theorems): Rust `incrementer_matches_machine_for_all_small_inputs` (a binary incrementer, inputs 0 to 40 with 0 to 2 padding cells, step count `2c + 1` for `c` trailing ones, tape value `n + 1`), `busy_beaver_2_matches_machine` (the two-state two-symbol champion in the TM0 form, 12 steps, 4 ones), `step_simulation_holds_on_every_small_configuration` (3150 configurations: 7 states, 2 symbols, tapes of length at most 3 on each side), `right_runner_is_refused_by_every_bounded_decider` (bounds 4 to 24 all return `BoundExceeded`). Python `test_all_two_state_two_symbol_machines_step_simulation` checks all 6561 machines with two states and two symbols in the TM0 form for 20 steps, with a different tape representation (a dictionary of cells and a position-free canonical form).

### 3.6 C6. A general-purpose evaluator

`lean4/GenesisCompUniv.lean`. Imported from Mathlib (names verified in the installed v4.35.0; the module names differ from earlier Mathlib: there is no `Mathlib.Computability.TMToPartrec` or `Mathlib.Computability.TuringMachine` file, the files are `Mathlib/Computability/TuringMachine/{Tape,PostTuringMachine,StackTuringMachine,Config,ToPartrec,Computable}.lean`): `Nat.Partrec.Code.eval`, `eval_part`, `exists_code`; `Turing.ToPartrec.Code.exists_code`; `Turing.PartrecToTM2.tr`, `init`, `tr_eval`, `tr_supports`, `codeSupp`; `Turing.TM2to1.tr`, `tr_respects`, `tr_supports`; `Turing.TM1to0.tr`, `tr_respects`, `tr_supports`; `StateTransition.tr_eval_dom`, `mem_eval`; `ComputablePred.halting_problem`.

New here:

- `universal_code`: one fixed code `u` with `eval u (pair (encode c) n) = eval c n` for all codes `c` and inputs `n`; `univCode_exists`: a fixed `ToPartrec.Code` computing the same function on one natural number.
- `tm2_computes_eval`: the fixed TM2 machine `PartrecToTM2.tr`, started on `init univCode [pair (encode c) n]`, evaluates to `halt <$> (pure <$> Code.eval c n)`.
- The composite fixed TM0 machine `M0 = TM1to0.tr (TM2to1.tr PartrecToTM2.tr)` and the explicit family `initCfg0 x`. `trCfg_init_gen` is the initial-configuration relation for an arbitrary starting label (adapted from the Mathlib proof for the default label). `dom_chain` and `halts_iff_eval_dom`: `M0` halts from `initCfg0 (pair (encode c) n)` iff `Code.eval c n` is defined.
- `used_state_marks_finite`, `used_marks_finite`, `card_G1`: any word reachable from a start word uses marks from the finite set `markSet`: the two end markers, the 1250 tape marks (`G1 = Bool x (K' -> Option Γ')`, `2 * 5^4`), and the state marks of the finite set `S0` (built from Mathlib's `tr_supports` chain). The size of `S0` is not computed: it depends on the code chosen by `Classical.choose`.

**Composition with C5.** C5 and `halts_iff_eval_dom` give: the rewriting regime `Rules M0`, started at a represented start word, reaches an irreducible word iff the evaluation halts (`reach_irreducible_iff`). This is the statement "there is a fixed rewriting regime, over a finite set of marks, whose normal-form reachability is the halting of the general-purpose evaluator", with unbounded growth of the word (C4) as the declared supply.

**OPEN in C6:** the output form at the TM0 level (the tape of the halting TM0 configuration encodes the value of `Code.eval c n`). Mathlib's `TM2to1.tr_eval` gives the output only existentially; the exact statement to prove is `v ∈ Code.eval c n ↔ (halting configuration of M0 from initCfg0 reads v on the output tape)`. The TM2 level output form is proved (`tm2_computes_eval`).

### 3.7 C7. Undecidability on the Genesis side

- `halting_not_computable`: for each `n`, the predicate `c ↦ Halts M0 (initCfg0 (pair (encode c) n))` is not computable (from `halts_iff_eval_dom` and `ComputablePred.halting_problem`).
- `reach_irreducible_not_computable` and `nfReach_not_computable`: the predicate "the start word of the input reaches an irreducible word under the fixed regime `Rules M0`" is not computable, as a predicate of the code or of the natural number input. This is the negative half of the context-decision-procedure obligation, for the explicit family of start words.
- `reach_problem_not_computable` (CONDITIONAL): if `Sym G1 (TM1to0.Λ' M1)` has a `Primcodable` structure and `startWord` is computable, then the normal-form reachability problem on words is not a computable predicate. The hypothesis is the OPEN lemma `startWord_computable`: it needs a `Primcodable` structure on a mark type that contains the infinite type `TM1to0.Λ' M1` (only a finite subset, `S0`, is used), and a computability proof for the paired-input encoding `trList`, `initL`, `addBottom`. Mathlib does not provide it.
- OPEN: undecidability of `Reach` to a FIXED target word. It requires adding erasing rules so that every halting word reduces to one fixed word; the statement is `Reach R0' (startWord x) target ↔ (univFun x).Dom` for the extended rule set `R0'`.

### 3.8 C8. Minimality fence

- `encodeWord`, `decodeWord`, `decode_encode`, `encodeWord_injective`, `encodeWord_append`: for any finite alphabet with `k = clog 2 |α| + 1` digits per letter (`codeWidth`), the letter-by-letter binary code is injective on words, is a monoid homomorphism, and has the explicit decoder `decodeWord` (`bits_injective` is the digit lemma). `encodeMarks`, `decodeMarks`, `encodeMarks_injective`, `encodeMarks_append` express this in `List Mark2`, the free monoid on the two separated marks.
- So words over any finite alphabet embed into words over two separated marks. A tape with a blank gives three symbols. Mathlib's alphabet-reduction `Turing.TM1to1` is imported infrastructure and is not used here; the Lean here does not prove that a machine over the coded alphabet simulates the machine over the original alphabet.
- Rust `binary_coding_roundtrips_and_is_injective` (alphabet sizes 1 to 9, words of length at most 3) and Python `test_binary_coding_roundtrip_and_injective` check the same code.
- **Not claimed:** the smallest general-purpose machine. The composite machine `M0` is large (1250 tape marks and a state set of unknown size) and is an existence statement. Small-machine records are literature only and are not used.

## 4. Where honest support stops, and the next lemma

The chain is established, with the declared inputs, up to this statement: *a fixed rewriting regime over a finite set of marks exists whose normal-form reachability from a family of start words is the halting of the general-purpose evaluator, and that reachability is not decidable; bounded versions are decidable and cannot reach it.* What stops it from being a derivation from `<>`:

1. The unbounded supply of fresh marks is host-supplied (C4). The next lemma on the Genesis side is an endogenous source of unboundedly many admitted data (`TFQ-0504`), or an explicit statement that it stays exogenous.
2. The identity convention and the labelling of `mark0` as `<>` are declared (C1).
3. Genesis `Step3` is not shown to be a word rewriting step (C2). The next lemma is an encoding of `St` under which `addTerm`, `addAssertion` and `identify` are word steps, or a proof that none exists.
4. `TFQ-0497` in its full form (collapse and separability over all Genesis contexts of the sealed regime) is not built (C3).
5. `startWord_computable`, the TM0-level output form, and fixed-target undecidability are open (C6, C7). The first is the next lemma for the encoded-instance form of the undecidability.

## 5. Verification record

Commands and results (this checkout, branch `comp-utm`):

- `lake build GenesisComputation GenesisCompTM GenesisCompUniv`: build completed, no `sorry`, `admit` or `native_decide`; `#print axioms` for 81 declarations in `dag/research/genesis_to_universal_computation.axioms.txt`.
- `cargo test --offline -p tfqm_genesis_tm`: 18 tests pass (the file `code/rust/src/wdp/genesis_tm.rs` is also the module `genesis_tm` of the `tfqm_wdp` crate; the standalone crate is `code/rust/src/genesis_tm`).
- `pytest code/python/tests/test_genesis_tm.py`: 112 tests pass.
- `scripts/contract_scores.py check`, `dag/validate_derivation_dag.py --no-files`, and the three DAG sync `--check` commands are recorded in the commit report.

## 6. Source map

- Lean: `lean4/GenesisComputation.lean` (C1 to C4, C8), `lean4/GenesisCompTM.lean` (C5), `lean4/GenesisCompUniv.lean` (C6, C7).
- Rust: `code/rust/src/wdp/genesis_tm.rs` (engine, bounded decider, TM0 encoding, Genesis event mirror, contexts, binary coding), `code/rust/src/genesis_tm/Cargo.toml`.
- Python: `code/python/src/qm/genesis_tm.py`, `code/python/tests/test_genesis_tm.py`.
- Axioms: `dag/research/genesis_to_universal_computation.axioms.txt`.
