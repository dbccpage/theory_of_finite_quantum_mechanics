# Genesis-Ongoing inventory (dbccpage/H3V7N5QF)

Read-only clone: `C:\Users\a343o\AppData\Local\Temp\fable-src\H3V7N5QF`, commit `9da20199101160aadf0aa3f66ec51e6652cdc008` (`Merge pull request #55 from dbccpage/add-apache-2-0-license`). Lean was not built. Axiom dependence is taken from the committed `evidence/**/lean_axioms.txt` reports. Comparison object language: `dbccpage/19L57G1` at `85a83ae7ce64dc2123ff218568a4ecd37e566d33` (`lean4/Derivation/Basic.lean`), not copied into this file's repository.

## Layout

The four directories named in the brief are present. Nothing named there is missing.

| Path | Role |
|---|---|
| `lean4/` | Lake package for the base seed `H3V7N5QF` and derivations Second through Twentyfirst. Toolchain file `lean4/lean-toolchain`. |
| `lean4_core/` | Separate Lake package for Twentysecond, Twentythird, Twentyfourth, Twentyfifth. No modules of those four sit under `lean4/`. |
| `evidence/` | One `summary.json` and one `lean_axioms.txt` for the base and for each numbered derivation, plus the base exploration tables. |
| `research/` | `notes.md`, `reading_the_seed.md`, `identification_only.py`, and per-derivation reading notes. `research/notes.md` says those notes are not cited as evidence. |

Also present, and not part of the four named directories: `code/`, `tests/`, `paper/`, `prompt/`, `ci/`, `meta/`, `.github/`, `.claude/`. There is no top-level `README.md`. `meta/README.md` fences `meta/` off the derivations: its Genesis vocabulary is not an input, and a claim there is not an inherited theorem.

## What is new relative to the 19L57G1 object language

`19L57G1`'s object language, in `lean4/Derivation/Basic.lean`, is a regime: counts of admitted data, form arities, instances `Inst`, all-tuples rules, and separation requirements. Admission events are `supply`, `admitDatum`, `admitForm`, `admitInst`, `admitRuleAll`, and `impose`. Observation is a context with holes (`Ctx`), plugged uniformly, with `derivable`, `collapsed`, and `separable`. The two Challenge-3 regimes are `R2L` and `R2F`. Later modules in that repository add, still inside that language, a transition codebook, primitive candidates, refusal frontiers, and a higher-cell boundary rule. This continuation does not import those modules and does not declare `Regime`, `Event`, `Inst`, or `Ctx`.

`H3V7N5QF` adds a different sealed language, starting from `prompt/seed_prompt.md`: terms, an assertion written `xry`, the given `arb`, a ban on `xrx`, and exactly four changes (identify two terms, remove an assertion, add a term, add an assertion). Obstruction, refusal, and "build structure" are a protocol around those four changes. Later seeds change that language. They do not add the regime events above. `meta/immune_system/genesis_correspondence.md`, which is outside the seal and pinned to `19L57G1` at `89fc568a61eb22100edf4070d40eb1449c350ed4`, records the 4 local change kinds and the 13 presentation classes as different, and records an isomorphism of the declared alphabets as refuted.

Pre-Genesis, S(n), and MSS-N do not occur as declarations, seeds, or ledger claims in this clone. A search of `*.lean`, `*.md`, `*.py`, `*.json`, and `*.txt` found no `Pre-Genesis`, `pregenesis`, `MSS-N`, `MSSN`, or `S(n)`.

## Data types

Each row is a carrier the continuation adds. `Reach` / `ReachN` inductives are finite change-sequences, listed with the primitives, not as a separate path object.

- `H3V7N5QF:lean4/H3V7N5QF/Finite.lean::St` — proved in Lean (module `lean4/H3V7N5QF/Finite.lean`; fields `T`, `A`, `a`, `b`; boolean membership, no multiplicity; axioms of the module's theorems are in `evidence/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/State.lean::MSt` — proved in Lean (module `lean4/Fourth/State.lean`; fields `T`, `M : ℕ × ℕ → ℕ`, `a`, `b`; multiplicity)
- `H3V7N5QF:lean4/Seventh/State.lean::NSt` — proved in Lean (module `lean4/Seventh/State.lean`; fields `T`, `M`; names dropped; empty beginning)
- `H3V7N5QF:lean4/Eighth/State.lean::Rel` — proved in Lean (module `lean4/Eighth/State.lean`; `abbrev Rel := Bool`, the two relations `r` and `s`)
- `H3V7N5QF:lean4/Eighth/State.lean::DSt` — proved in Lean (module `lean4/Eighth/State.lean`; fields `T`, `M : Rel → ℕ × ℕ → ℕ`, names `a`, `b`)
- `H3V7N5QF:lean4/Ninth/State.lean::NDSt` — proved in Lean (module `lean4/Ninth/State.lean`; fields `T`, `M : Rel → ℕ × ℕ → ℕ`; empty beginning)
- `H3V7N5QF:lean4/Tenth/State.lean::LeftOver` — proved in Lean (module `lean4/Tenth/State.lean`; a leftover is not an assertion)
- `H3V7N5QF:lean4/Tenth/State.lean::Tagged` — proved in Lean (module `lean4/Tenth/State.lean`; a ninth state plus a leftover tag)
- `H3V7N5QF:lean4/Eleventh/State.lean::Labeled` — proved in Lean (module `lean4/Eleventh/State.lean`; a writing that may give two terms one letter)
- `H3V7N5QF:lean4/Twelfth/State.lean::LoopTag` — proved in Lean (module `lean4/Twelfth/State.lean`)
- `H3V7N5QF:lean4/Twelfth/State.lean::IdentRecord` — proved in Lean (module `lean4/Twelfth/State.lean`; which assertions of two terms become one, per relation)
- `H3V7N5QF:lean4/Twelfth/State.lean::Recorded` — proved in Lean (module `lean4/Twelfth/State.lean`; a state kept with that record)
- `H3V7N5QF:lean4/Fourteenth/State.lean::LeftWriting` — proved in Lean (module `lean4/Fourteenth/State.lean`; a leftover written neither `xry` nor `xsy`)
- `H3V7N5QF:lean4/Fourteenth/State.lean::Tagged` — proved in Lean (module `lean4/Fourteenth/State.lean`; distinct from the tenth `Tagged`)
- `H3V7N5QF:lean4/Fifteenth/State.lean::Admission` — proved in Lean (module `lean4/Fifteenth/State.lean`; constructors `notAdmitted`, `admitted`; neither is an assertion)
- `H3V7N5QF:lean4/Fifteenth/State.lean::Tagged` — proved in Lean (module `lean4/Fifteenth/State.lean`; unchosen reading C-A2: `NDSt` plus `Admission`)
- `H3V7N5QF:lean4/Sixteenth/State.lean::RSt` — proved in Lean (module `lean4/Sixteenth/State.lean`; fields `st : NDSt` and `L : ℕ × ℕ → ℕ`, unadmitted leftover counts)
- `H3V7N5QF:lean4/Second/Carry.lean::Carries` — proved in Lean (module `lean4/Second/Carry.lean`; a term map carrying assertions)
- `H3V7N5QF:lean4/Third/Contain.lean::Contains` — proved in Lean (module `lean4/Third/Contain.lean`)
- `H3V7N5QF:lean4/Fourth/Contain.lean::Contains4` — proved in Lean (module `lean4/Fourth/Contain.lean`)
- `H3V7N5QF:lean4/Seventh/Cost.lean::Contains7` — proved in Lean (module `lean4/Seventh/Cost.lean`)
- `H3V7N5QF:lean4_core/Twentysecond/Basic.lean::Rel` — proved in Lean (module `lean4_core/Twentysecond/Basic.lean`; inductive, not the eighth `abbrev`)
- `H3V7N5QF:lean4_core/Twentysecond/Basic.lean::Atom` — proved in Lean (module `lean4_core/Twentysecond/Basic.lean`; fields `q : Rel`, `x`, `y`)
- `H3V7N5QF:lean4_core/Twentysecond/State.lean::St` — proved in Lean (module `lean4_core/Twentysecond/State.lean`; the twenty-second state, not base `St`)
- `H3V7N5QF:lean4_core/Twentyfourth/Basic.lean::FSt` — proved in Lean (module `lean4_core/Twentyfourth/Basic.lean`; fields `G : St`, `F : Nat → Bool`)
- `H3V7N5QF:lean4_core/Twentyfifth/Fill.lean::Tri` — proved in Lean (module `lean4_core/Twentyfifth/Fill.lean`; fields `x`, `y`, `z`)
- `H3V7N5QF:lean4_core/Twentyfifth/Fill.lean::FSt` — proved in Lean (module `lean4_core/Twentyfifth/Fill.lean`; twenty-second state plus a list of filled triples; distinct from twenty-fourth `FSt`)

Python carriers used by the explorers (`code/xry/state.py` and the later `code/<n>/state.py` modules) are the computational side of these types. They are not a second object language.

## Primitives

The base seed's primitives are not the regime events of `19L57G1`.

- `H3V7N5QF:prompt/seed_prompt.md::xry` — stated in prose only (an assertion has two term places; `arb` and `bra` are not the same sentence)
- `H3V7N5QF:lean4/H3V7N5QF/Finite.lean::addTerm` — proved in Lean (module `lean4/H3V7N5QF/Finite.lean`; one new term, no new assertion)
- `H3V7N5QF:lean4/H3V7N5QF/Finite.lean::addAssertion` — proved in Lean (module `lean4/H3V7N5QF/Finite.lean`)
- `H3V7N5QF:lean4/H3V7N5QF/Finite.lean::remove` — proved in Lean (module `lean4/H3V7N5QF/Finite.lean`)
- `H3V7N5QF:lean4/H3V7N5QF/Finite.lean::identify` — proved in Lean (module `lean4/H3V7N5QF/Finite.lean`; both terms are replaced by one term in every assertion)
- `H3V7N5QF:lean4/H3V7N5QF/Finite.lean::Step` — proved in Lean (constructors `addTerm`, `addAssertion`, `remove`, `identify`; a performed step is unobstructed by construction of those constructors)
- `H3V7N5QF:lean4/H3V7N5QF/Cost.lean::Reach` — proved in Lean (module `lean4/H3V7N5QF/Cost.lean`; finite sequences of `Step`)

Per-derivation change to that primitive list. Each seed is `prompt/<name>/seed_prompt.md` unless noted.

| Derivation | What the seed changes | Change relation |
|---|---|---|
| Second | Removal is not a change. Three kinds remain. | `H3V7N5QF:lean4/Second/Step.lean::Step3` |
| Third | Only adding a term and adding an assertion. | `H3V7N5QF:lean4/Third/Step.lean::Step2` |
| Fourth | Multiplicity. Additions only. `arb` has multiplicity one. | `H3V7N5QF:lean4/Fourth/Step.lean::Step4` |
| Fifth | Multiplicity, and the four kinds, with the `xrx` ban and the answer protocol kept. | `H3V7N5QF:lean4/Fifth/Step.lean::Step5` |
| Sixth | Multiplicity and the four kinds. The `xrx` ban and the obstruction paragraph are absent. | `H3V7N5QF:lean4/Sixth/Step.lean::Step6` |
| Seventh | Sixth, with nothing given at the start. | `H3V7N5QF:lean4/Seventh/Step.lean::Step7` |
| Eighth | Two relations `r` and `s`, multiplicity, given `arb` at multiplicity one. | `H3V7N5QF:lean4/Eighth/Step.lean::Step8` |
| Ninth | Eighth with an empty beginning. | `H3V7N5QF:lean4/Ninth/Step.lean::Step9` |
| Tenth | After each change, record a leftover that is not an assertion. The four kinds stay `Step9`. | `H3V7N5QF:lean4/Tenth/Compare.lean::StepTagged` |
| Eleventh | A writing may assign one letter to two terms. Steps stay `Step9`. | `H3V7N5QF:lean4/Eleventh/Step.lean::Step11` (imported alias; see below) |
| Twelfth | Identification stores `IdentRecord` on the result. Steps stay `Step9`. | `H3V7N5QF:lean4/Twelfth/Step.lean::Step12` (imported alias) |
| Thirteenth | A coarser writing forgets `r` versus `s`. Steps stay `Step9`. | `H3V7N5QF:lean4/Thirteenth/Step.lean::Step13` (imported alias) |
| Fourteenth | A leftover is written neither `xry` nor `xsy`, and is not an answer. Steps stay `Step9`. | `H3V7N5QF:lean4/Fourteenth/Step.lean::Step14` (imported alias) |
| Fifteenth | Reaching does not admit. Admission is not a fifth kind under the chosen reading. | `H3V7N5QF:lean4/Fifteenth/Step.lean::Step15` (imported alias); `H3V7N5QF:lean4/Fifteenth/Compare.lean::StepTagged` for the tagged reading |
| Sixteenth | A recorded leftover `xℓy` may be admitted into `r` or into `s`. | `H3V7N5QF:lean4/Sixteenth/Step.lean::Step16` constructors `addTerm`, `addAssertion`, `remove`, `admitLeftover`, `identify` |
| Seventeenth | The sentence forbidding `xrx` is struck. Obstruction remains. `Reach17` keeps only unobstructed steps; `ReachAll` does not. | `H3V7N5QF:lean4/Seventeenth/Step.lean::Step17` |
| Eighteenth | Two results that differ only in writing are different results, not the same result. | No new step inductive. `H3V7N5QF:lean4/Eighteenth/Writing.lean::braWritten` and `swappedGiven` are two writings of one boolean assertion pattern. |
| Nineteenth | Identification rewrites one chosen assertion, not every assertion. | `H3V7N5QF:lean4/Nineteenth/Partial.lean::PStep` constructors `rewriteOne`, `addTerm`, `addAssertion`, `remove` |
| Twentieth | Attempt order is fewest total changes, not fewest additions. The four kinds are unchanged. | No new step inductive. |
| Twentyfirst | An obstructed change is refused. It is not performed. | `H3V7N5QF:lean4/Twentyfirst/Refusal.lean::identify_given_refused` uses base `Step` |
| Twentysecond | Empty start, two relations, multiplicity. Sameness also identifies a state with the state that has both `xry` and `xsy`. | `H3V7N5QF:lean4_core/Twentysecond/State.lean::Step` |
| Twentythird | Sameness also allows raising a term: add `xry` and `ysx` once for every other term `y`. Raising is not a fifth change kind. | `H3V7N5QF:lean4_core/Twentythird/Same.lean::Gen3` |
| Twentyfourth | Fifth kind: fill one term. A filled term `x` balances when `xrx` and `xsx` have equal multiplicity. | `H3V7N5QF:lean4_core/Twentyfourth/Basic.lean::Step24` constructor `fill` |
| Twentyfifth | Fifth kind: fill three different terms. Balance is equality of `r` and `s` counts around the triple. | `H3V7N5QF:lean4_core/Twentyfifth/Fill.lean::Step25` constructor `fill` |

Answer records in the base (refuse, remove the obstruction, build by standing in for the obstructed change) are fixed in `paper/paper.md` as chosen reading C7, not as extra change kinds. `H3V7N5QF:lean4/H3V7N5QF/Answers.lean::build_answer` is the Lean statement that a build is a sequence of unobstructed changes.

## Admission rules

These are the continuation's own admission rules. They are not `admitDatum` or `admitInst`. A declaration that is printed again in a census below is counted once, on the census line.

- `H3V7N5QF:lean4/H3V7N5QF/Finite.lean::identify_legal_iff` — proved in Lean (module `lean4/H3V7N5QF/Finite.lean`; identifying `u`,`v` is unobstructed exactly when neither `urv` nor `vru` is asserted; axioms: `propext, Classical.choice, Quot.sound`, recorded in `evidence/lean_axioms.txt`)
- `H3V7N5QF:lean4/H3V7N5QF/Finite.lean::addAssertion_legal_iff` — proved in Lean (same module and axiom report; adding `xry` is unobstructed exactly when `x ≠ y`)
- `H3V7N5QF:lean4/H3V7N5QF/Finite.lean::adding_xrx_always_obstructed` — proved in Lean (same; adding `xrx` is obstructed in every state)
- `H3V7N5QF:lean4/H3V7N5QF/Finite.lean::remove_legal` — proved in Lean (same; removal is never obstructed)
- `H3V7N5QF:lean4/H3V7N5QF/Finite.lean::addTerm_legal` — proved in Lean (same; adding a term is never obstructed)
- `H3V7N5QF:lean4/Fifteenth/State.lean::Admission` — proved in Lean (constructors `notAdmitted` and `admitted`)
- `H3V7N5QF:lean4/Fifteenth/Step.lean::reaching_does_not_admit` — proved in Lean (axioms: none, recorded in `evidence/fifteenth/lean_axioms.txt`; the chosen record of a reached result is `notAdmitted`)
- `H3V7N5QF:lean4/Fifteenth/Step.lean::admission_not_assertion` — proved in Lean (same report)
- `H3V7N5QF:lean4/Fifteenth/Step.lean::admission_not_a_kind` — proved in Lean (same report)
- `H3V7N5QF:lean4/Fifteenth/Compare.lean::every_reached_can_be_admitted` — proved in Lean (same report; exhibits a tagged copy, which the ledger says is the C-A2 constructor, not a proof that reaching implies admissibility)
- `H3V7N5QF:lean4/Sixteenth/State.lean::admitLeftover` — proved in Lean (raises one multiplicity and lowers the leftover count of that pair)
- `H3V7N5QF:lean4/Sixteenth/Step.lean::Step16` — proved in Lean (constructor `admitLeftover` requires the leftover count to be nonzero)
- `H3V7N5QF:lean4/Sixteenth/State.lean::remove_admit_same` — proved in Lean (remove, then admit the leftover into the same relation, returns the same state; axioms in `evidence/sixteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Twentyfirst/Refusal.lean::identify_given_refused` — proved in Lean (module `lean4/Twentyfirst/Refusal.lean`; identifying the two given names is not a `Step`; axioms in `evidence/twentyfirst/lean_axioms.txt`)
- `H3V7N5QF:lean4/Twentyfirst/Refusal.lean::refusal_continues_by_a_term` — proved in Lean (same module; a refusal does not stop the other unobstructed changes)
- `H3V7N5QF:prompt/twentyfirst/seed_prompt.md::refused` — stated in prose only (an obstructed change is refused, recorded, and changes nothing)

Further cited theorems whose names contain `admit` or `refus` are listed under Admission theorems below and are not repeated in the general census.

## Invariants

Base preservation, all proved in Lean in `lean4/H3V7N5QF/Finite.lean` and `lean4/H3V7N5QF/Cost.lean`, axioms `propext, Classical.choice, Quot.sound` unless the report says otherwise (`evidence/lean_axioms.txt`):

- `H3V7N5QF:lean4/H3V7N5QF/Finite.lean::Legal` — proved in Lean (`def Legal`: no pair `(x,x)` is asserted)
- `H3V7N5QF:lean4/H3V7N5QF/Finite.lean::WF` — proved in Lean (assertions and the names `a`,`b` sit on terms that are present)
- `H3V7N5QF:lean4/H3V7N5QF/Finite.lean::Step.legal` — proved in Lean
- `H3V7N5QF:lean4/H3V7N5QF/Finite.lean::Step.wf` — proved in Lean
- `H3V7N5QF:lean4/H3V7N5QF/Finite.lean::Step.nonempty` — proved in Lean (no step deletes the last term)
- `H3V7N5QF:lean4/H3V7N5QF/Finite.lean::Step.names_stay_merged` — proved in Lean
- `H3V7N5QF:lean4/H3V7N5QF/Cost.lean::Reach.legal` — proved in Lean
- `H3V7N5QF:lean4/H3V7N5QF/Cost.lean::Reach.wf` — proved in Lean
- `H3V7N5QF:lean4/H3V7N5QF/Cost.lean::Reach.nonempty` — proved in Lean
- `H3V7N5QF:lean4/H3V7N5QF/Cost.lean::Reach.names_stay_merged` — proved in Lean
- `H3V7N5QF:lean4/H3V7N5QF/Cost.lean::Reach.arb_gone_for_good` — proved in Lean (after `a` and `b` are one term, `arb` is not asserted again)
- `H3V7N5QF:lean4/H3V7N5QF/Finite.lean::obstruction_persists` — proved in Lean (one step; the ledger's O6 says the sequence case is not this theorem)
- `H3V7N5QF:lean4/H3V7N5QF/Basic.lean::given_distinct` — proved in Lean (axioms: none; `a` and `b` are two terms because `arb` is not `xrx`)

Second seed, where removal is absent: `H3V7N5QF:lean4/Second/Carry.lean::Reach3.arb_persists`, `Reach3.bra_persists`, `Reach3.names_apart`, `Reach3.two_terms`, `Reach3.obstruction_persists`, `Reach3.split_mono` — proved in Lean (axioms in `evidence/second/lean_axioms.txt`).

Seventeenth: `LoopFree` is the imported abbreviation below, not a new predicate. `Reach17` preserves loop-freeness only along unobstructed steps. Twenty-fourth `Reach24.hasFilled` is in the invariant census (a filled term is not deleted under the chosen identification reading).

Every other cited theorem whose short name is one of `legal`, `wf`, `nonempty`, `names_stay_merged`, `arb_gone_for_good`, `names_apart`, `two_terms`, `arb_persists`, `bra_persists`, `obstruction_persists`, `split_mono`, `hasFilled`, `loopFree_out`, `identify_keeps_apart`, `loop_survives_replacement`, `loop_survives_additions`, `only_removal_restores` is listed in the invariant census and not again below.

## Imported

These names are aliases or a predicate abbreviation. The defining relation is an earlier declaration, not a new proof.

- `H3V7N5QF:lean4/Tenth/Step.lean::Step10` — imported (`abbrev` of `Step9`)
- `H3V7N5QF:lean4/Tenth/Step.lean::Reach10` — imported (`abbrev` of `Reach9`)
- `H3V7N5QF:lean4/Eleventh/Step.lean::Step11` — imported (`abbrev` of `Step9`)
- `H3V7N5QF:lean4/Eleventh/Step.lean::Reach11` — imported (`abbrev` of `Reach9`)
- `H3V7N5QF:lean4/Twelfth/Step.lean::Step12` — imported (`abbrev` of `Step9`)
- `H3V7N5QF:lean4/Twelfth/Step.lean::Reach12` — imported (`abbrev` of `Reach9`)
- `H3V7N5QF:lean4/Thirteenth/Step.lean::Step13` — imported (`abbrev` of `Step9`)
- `H3V7N5QF:lean4/Thirteenth/Step.lean::Reach13` — imported (`abbrev` of `Reach9`)
- `H3V7N5QF:lean4/Fourteenth/Step.lean::Step14` — imported (`abbrev` of `Step9`)
- `H3V7N5QF:lean4/Fourteenth/Step.lean::Reach14` — imported (`abbrev` of `Reach9`)
- `H3V7N5QF:lean4/Fifteenth/Step.lean::Step15` — imported (`abbrev` of `Step9`)
- `H3V7N5QF:lean4/Fifteenth/Step.lean::Reach15` — imported (`abbrev` of `Reach9`)
- `H3V7N5QF:lean4/Seventeenth/State.lean::LoopFree` — imported (`abbrev` of base `Legal`)
- `H3V7N5QF:lean4/Sixteenth/State.lean::record` — imported (the leftover count is viewed as a seventh `NSt`; the seventh's lemmas are not re-proved)

No declaration in `lean4/` or `lean4_core/` imports a module from `19L57G1`.

## Invariant census

Count: 101. Each line is proved in Lean. Axioms are as recorded, not rebuilt.

- `H3V7N5QF:lean4/Eighth/Step.lean::names_stay_merged` — proved in Lean (module `lean4/Eighth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/Step.lean::nonempty` — proved in Lean (module `lean4/Eighth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/Step.lean::wf` — proved in Lean (module `lean4/Eighth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/Step.lean::names_stay_merged` — proved in Lean (module `lean4/Eighth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/Step.lean::nonempty` — proved in Lean (module `lean4/Eighth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/Step.lean::wf` — proved in Lean (module `lean4/Eighth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/Step.lean::arb_gone_for_good` — proved in Lean (module `lean4/Fifth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/Step.lean::legal` — proved in Lean (module `lean4/Fifth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/Step.lean::names_stay_merged` — proved in Lean (module `lean4/Fifth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/Step.lean::nonempty` — proved in Lean (module `lean4/Fifth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/Step.lean::wf` — proved in Lean (module `lean4/Fifth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/Step.lean::legal` — proved in Lean (module `lean4/Fifth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/Step.lean::names_stay_merged` — proved in Lean (module `lean4/Fifth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/Step.lean::nonempty` — proved in Lean (module `lean4/Fifth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/Step.lean::wf` — proved in Lean (module `lean4/Fifth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/Contain.lean::arb_persists` — proved in Lean (module `lean4/Fourth/Contain.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/Contain.lean::bra_persists` — proved in Lean (module `lean4/Fourth/Contain.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/Step.lean::legal` — proved in Lean (module `lean4/Fourth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/Contain.lean::names_apart` — proved in Lean (module `lean4/Fourth/Contain.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/Step.lean::nonempty` — proved in Lean (module `lean4/Fourth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/Contain.lean::obstruction_persists` — proved in Lean (module `lean4/Fourth/Contain.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/Contain.lean::split_mono` — proved in Lean (module `lean4/Fourth/Contain.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/Contain.lean::two_terms` — proved in Lean (module `lean4/Fourth/Contain.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/Step.lean::wf` — proved in Lean (module `lean4/Fourth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/Step.lean::legal` — proved in Lean (module `lean4/Fourth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/Step.lean::nonempty` — proved in Lean (module `lean4/Fourth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/Step.lean::wf` — proved in Lean (module `lean4/Fourth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)
- `H3V7N5QF:lean4/H3V7N5QF/Finite.lean::identify_keeps_apart` — proved in Lean (module `lean4/H3V7N5QF/Finite.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/lean_axioms.txt`)
- `H3V7N5QF:lean4/H3V7N5QF/Basic.lean::loop_survives_additions` — proved in Lean (module `lean4/H3V7N5QF/Basic.lean`; axioms: none; recorded in `evidence/lean_axioms.txt`)
- `H3V7N5QF:lean4/H3V7N5QF/Basic.lean::loop_survives_replacement` — proved in Lean (module `lean4/H3V7N5QF/Basic.lean`; axioms: none; recorded in `evidence/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/Step.lean::nonempty` — proved in Lean (module `lean4/Ninth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/Step.lean::wf` — proved in Lean (module `lean4/Ninth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/Step.lean::nonempty` — proved in Lean (module `lean4/Ninth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/Step.lean::wf` — proved in Lean (module `lean4/Ninth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/H3V7N5QF/Finite.lean::obstruction_persists` — proved in Lean (module `lean4/H3V7N5QF/Finite.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/lean_axioms.txt`)
- `H3V7N5QF:lean4/H3V7N5QF/Basic.lean::only_removal_restores` — proved in Lean (module `lean4/H3V7N5QF/Basic.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/lean_axioms.txt`)
- `H3V7N5QF:lean4/H3V7N5QF/Cost.lean::arb_gone_for_good` — proved in Lean (module `lean4/H3V7N5QF/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/lean_axioms.txt`)
- `H3V7N5QF:lean4/H3V7N5QF/Cost.lean::legal` — proved in Lean (module `lean4/H3V7N5QF/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/lean_axioms.txt`)
- `H3V7N5QF:lean4/H3V7N5QF/Cost.lean::names_stay_merged` — proved in Lean (module `lean4/H3V7N5QF/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/lean_axioms.txt`)
- `H3V7N5QF:lean4/H3V7N5QF/Cost.lean::nonempty` — proved in Lean (module `lean4/H3V7N5QF/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/lean_axioms.txt`)
- `H3V7N5QF:lean4/H3V7N5QF/Cost.lean::wf` — proved in Lean (module `lean4/H3V7N5QF/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/lean_axioms.txt`)
- `H3V7N5QF:lean4/Second/Carry.lean::arb_persists` — proved in Lean (module `lean4/Second/Carry.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/second/lean_axioms.txt`)
- `H3V7N5QF:lean4/Second/Carry.lean::bra_persists` — proved in Lean (module `lean4/Second/Carry.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/second/lean_axioms.txt`)
- `H3V7N5QF:lean4/Second/Step.lean::legal` — proved in Lean (module `lean4/Second/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/second/lean_axioms.txt`)
- `H3V7N5QF:lean4/Second/Carry.lean::names_apart` — proved in Lean (module `lean4/Second/Carry.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/second/lean_axioms.txt`)
- `H3V7N5QF:lean4/Second/Step.lean::nonempty` — proved in Lean (module `lean4/Second/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/second/lean_axioms.txt`)
- `H3V7N5QF:lean4/Second/Carry.lean::obstruction_persists` — proved in Lean (module `lean4/Second/Carry.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/second/lean_axioms.txt`)
- `H3V7N5QF:lean4/Second/Carry.lean::split_mono` — proved in Lean (module `lean4/Second/Carry.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/second/lean_axioms.txt`)
- `H3V7N5QF:lean4/Second/Carry.lean::two_terms` — proved in Lean (module `lean4/Second/Carry.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/second/lean_axioms.txt`)
- `H3V7N5QF:lean4/Second/Step.lean::wf` — proved in Lean (module `lean4/Second/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/second/lean_axioms.txt`)
- `H3V7N5QF:lean4/Second/Step.lean::legal` — proved in Lean (module `lean4/Second/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/second/lean_axioms.txt`)
- `H3V7N5QF:lean4/Second/Step.lean::nonempty` — proved in Lean (module `lean4/Second/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/second/lean_axioms.txt`)
- `H3V7N5QF:lean4/Second/Step.lean::wf` — proved in Lean (module `lean4/Second/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/second/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventeenth/Step.lean::names_stay_merged` — proved in Lean (module `lean4/Seventeenth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventeenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventeenth/Step.lean::nonempty` — proved in Lean (module `lean4/Seventeenth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventeenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventeenth/Step.lean::wf` — proved in Lean (module `lean4/Seventeenth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventeenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventeenth/Step.lean::names_stay_merged` — proved in Lean (module `lean4/Seventeenth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventeenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventeenth/Step.lean::nonempty` — proved in Lean (module `lean4/Seventeenth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventeenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventeenth/Step.lean::wf` — proved in Lean (module `lean4/Seventeenth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventeenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventeenth/Step.lean::loopFree_out` — proved in Lean (module `lean4/Seventeenth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventeenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventeenth/Step.lean::names_stay_merged` — proved in Lean (module `lean4/Seventeenth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventeenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventeenth/Step.lean::nonempty` — proved in Lean (module `lean4/Seventeenth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventeenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventeenth/Step.lean::wf` — proved in Lean (module `lean4/Seventeenth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventeenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventh/Step.lean::nonempty` — proved in Lean (module `lean4/Seventh/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventh/Step.lean::wf` — proved in Lean (module `lean4/Seventh/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventh/Step.lean::nonempty` — proved in Lean (module `lean4/Seventh/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventh/Step.lean::wf` — proved in Lean (module `lean4/Seventh/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixteenth/Step.lean::nonempty` — proved in Lean (module `lean4/Sixteenth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixteenth/Step.lean::nonempty` — proved in Lean (module `lean4/Sixteenth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixteenth/Step.lean::wf` — proved in Lean (module `lean4/Sixteenth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixth/Step.lean::names_stay_merged` — proved in Lean (module `lean4/Sixth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixth/Step.lean::nonempty` — proved in Lean (module `lean4/Sixth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixth/Step.lean::wf` — proved in Lean (module `lean4/Sixth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixth/Step.lean::names_stay_merged` — proved in Lean (module `lean4/Sixth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixth/Step.lean::nonempty` — proved in Lean (module `lean4/Sixth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixth/Step.lean::wf` — proved in Lean (module `lean4/Sixth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/H3V7N5QF/Finite.lean::legal` — proved in Lean (module `lean4/H3V7N5QF/Finite.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/lean_axioms.txt`)
- `H3V7N5QF:lean4/H3V7N5QF/Finite.lean::names_stay_merged` — proved in Lean (module `lean4/H3V7N5QF/Finite.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/lean_axioms.txt`)
- `H3V7N5QF:lean4/H3V7N5QF/Finite.lean::nonempty` — proved in Lean (module `lean4/H3V7N5QF/Finite.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/lean_axioms.txt`)
- `H3V7N5QF:lean4/H3V7N5QF/Finite.lean::wf` — proved in Lean (module `lean4/H3V7N5QF/Finite.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/lean_axioms.txt`)
- `H3V7N5QF:lean4/Third/Contain.lean::arb_persists` — proved in Lean (module `lean4/Third/Contain.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)
- `H3V7N5QF:lean4/Third/Contain.lean::bra_persists` — proved in Lean (module `lean4/Third/Contain.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)
- `H3V7N5QF:lean4/Third/Step.lean::legal` — proved in Lean (module `lean4/Third/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)
- `H3V7N5QF:lean4/Third/Contain.lean::names_apart` — proved in Lean (module `lean4/Third/Contain.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)
- `H3V7N5QF:lean4/Third/Step.lean::nonempty` — proved in Lean (module `lean4/Third/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)
- `H3V7N5QF:lean4/Third/Contain.lean::obstruction_persists` — proved in Lean (module `lean4/Third/Contain.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)
- `H3V7N5QF:lean4/Third/Contain.lean::split_mono` — proved in Lean (module `lean4/Third/Contain.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)
- `H3V7N5QF:lean4/Third/Contain.lean::two_terms` — proved in Lean (module `lean4/Third/Contain.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)
- `H3V7N5QF:lean4/Third/Step.lean::wf` — proved in Lean (module `lean4/Third/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)
- `H3V7N5QF:lean4/Third/Step.lean::legal` — proved in Lean (module `lean4/Third/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)
- `H3V7N5QF:lean4/Third/Step.lean::nonempty` — proved in Lean (module `lean4/Third/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)
- `H3V7N5QF:lean4/Third/Step.lean::wf` — proved in Lean (module `lean4/Third/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Fill.lean::wf` — proved in Lean (module `lean4_core/Twentyfifth/Fill.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Fill.lean::wf` — proved in Lean (module `lean4_core/Twentyfifth/Fill.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Basic.lean::hasFilled` — proved in Lean (module `lean4_core/Twentyfourth/Basic.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Basic.lean::wf` — proved in Lean (module `lean4_core/Twentyfourth/Basic.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Same.lean::hasFilled` — proved in Lean (module `lean4_core/Twentyfourth/Same.lean`; axioms: none; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Basic.lean::hasFilled` — proved in Lean (module `lean4_core/Twentyfourth/Basic.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Basic.lean::wf` — proved in Lean (module `lean4_core/Twentyfourth/Basic.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/State.lean::wf` — proved in Lean (module `lean4_core/Twentysecond/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/State.lean::wf` — proved in Lean (module `lean4_core/Twentysecond/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

## Admission theorems

Count: 21. Headline rules are also named in the admission section above; this list is every cited theorem whose name contains `admit` or `refus`.

- `H3V7N5QF:lean4/Fifteenth/Rename.lean::admission_swap_admitted` — proved in Lean (module `lean4/Fifteenth/Rename.lean`; axioms: none; recorded in `evidence/fifteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifteenth/Step.lean::admitted_is_admitted` — proved in Lean (module `lean4/Fifteenth/Step.lean`; axioms: none; recorded in `evidence/fifteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifteenth/Compare.lean::every_reached_can_be_admitted` — proved in Lean (module `lean4/Fifteenth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifteenth/Step.lean::first_change_does_not_admit` — proved in Lean (module `lean4/Fifteenth/Step.lean`; axioms: none; recorded in `evidence/fifteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifteenth/Step.lean::reaching_does_not_admit` — proved in Lean (module `lean4/Fifteenth/Step.lean`; axioms: none; recorded in `evidence/fifteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifteenth/Step.lean::reaching_ne_admitted` — proved in Lean (module `lean4/Fifteenth/Step.lean`; axioms: none; recorded in `evidence/fifteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifteenth/Compare.lean::step_reaches_not_admitted` — proved in Lean (module `lean4/Fifteenth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventeenth/Answers.lean::refusal_does_not_enter` — proved in Lean (module `lean4/Seventeenth/Answers.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventeenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixteenth/Reach.lean::admit_remove_unbounded` — proved in Lean (module `lean4/Sixteenth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixteenth/Compare.lean::admitted_leftover_is_the_assertion` — proved in Lean (module `lean4/Sixteenth/Compare.lean`; axioms: propext, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixteenth/State.lean::mass_admit` — proved in Lean (module `lean4/Sixteenth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixteenth/State.lean::potential_admit` — proved in Lean (module `lean4/Sixteenth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixteenth/Compare.lean::r_leftover_admitted_into_s` — proved in Lean (module `lean4/Sixteenth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixteenth/Reach.lean::reach16_admit_all` — proved in Lean (module `lean4/Sixteenth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixteenth/State.lean::remove_admit_other_ne` — proved in Lean (module `lean4/Sixteenth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixteenth/State.lean::remove_admit_other_ne_direct` — proved in Lean (module `lean4/Sixteenth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixteenth/State.lean::remove_admit_other_st` — proved in Lean (module `lean4/Sixteenth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixteenth/State.lean::remove_admit_same` — proved in Lean (module `lean4/Sixteenth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Twentyfirst/Refusal.lean::identify_given_refused` — proved in Lean (module `lean4/Twentyfirst/Refusal.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/twentyfirst/lean_axioms.txt`)
- `H3V7N5QF:lean4/Twentyfirst/Refusal.lean::refusal_continues_by_a_term` — proved in Lean (module `lean4/Twentyfirst/Refusal.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/twentyfirst/lean_axioms.txt`)
- `H3V7N5QF:lean4/Twentyfirst/Refusal.lean::refusal_continues_by_removal` — proved in Lean (module `lean4/Twentyfirst/Refusal.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/twentyfirst/lean_axioms.txt`)

## Computed (exact)

Ledger rows whose status is computed, or whose identifier starts with `K`. The files named in each ledger regenerate under the derivation's generator. This inventory did not re-run them.

- `H3V7N5QF:paper/claim_ledger.md::K1` — computed (exact) (status: computed; evidence: `evidence/counts.csv`, `evidence/summary.json`; cross-checked by listing for 1–3 terms (`tests/test_orbits.py`) and by the exploration for 1–5 / 1–4 terms)
- `H3V7N5QF:paper/claim_ledger.md::K2` — computed (exact) (status: computed; evidence: `evidence/rounds_*.csv`, `evidence/summary.json`)
- `H3V7N5QF:paper/claim_ledger.md::K3` — computed (exact) (status: computed from D8; evidence: `evidence/rounds_*.csv` (last column); agreement with the exploration in rounds `0 … N − 2` (`rounds_agreeing_with_unbounded_formula`))
- `H3V7N5QF:paper/claim_ledger.md::K4` — computed (exact) (status: computed; evidence: `evidence/rounds_*.csv`, `evidence/frontier_*.csv`, `evidence/summary.json`)
- `H3V7N5QF:paper/claim_ledger.md::K5` — computed (exact) (status: computed; evidence: `evidence/added_*.csv`, `evidence/results_*.csv`)
- `H3V7N5QF:paper/claim_ledger.md::K6` — computed (exact) (status: computed; evidence: `evidence/follows_*.csv`)
- `H3V7N5QF:paper/claim_ledger.md::K7` — computed (exact) (status: computed; evidence: `python code/generate.py --check`; `tests/test_evidence.py::test_command_line` (the check itself, on a small plan); `evidence/MANIFEST.sha256`)
- `H3V7N5QF:paper/claim_ledger.md::K8` — computed (exact) (status: computed; evidence: `python -m pytest`; `python code/xry/gate.py <coverage.json>`; `python -m mypy`)
- `H3V7N5QF:paper/eighteenth/claim_ledger.md::D1` — computed (exact) (status: computed; evidence: `orbit_splits_factorial` on every reached state (`orbit_formula_fails` empty on all four runs))
- `H3V7N5QF:paper/eighteenth/claim_ledger.md::D3` — computed (exact) (status: computed + derived; evidence: `summary.json` `rounds_above_the_base_cost` = 0 and `rounds_below_the_base_cost` empty on both named runs; base Lean `fewest_changes_lower_A`, `fewest_changes_lower_B`)
- `H3V7N5QF:paper/eighteenth/claim_ledger.md::D4` — computed (exact) (status: computed; evidence: `summary.json` `rounds_below_the_base_cost` empty, `rounds_above_the_base_cost`, `greatest_excess_over_the_base_cost`)
- `H3V7N5QF:paper/eighteenth/claim_ledger.md::K1` — computed (exact) (status: computed; evidence: `summary.json`)
- `H3V7N5QF:paper/eighteenth/claim_ledger.md::K2` — computed (exact) (status: computed; evidence: `summary.json` `answers_on_an_unreached_writing` = 0)
- `H3V7N5QF:paper/eighteenth/claim_ledger.md::K3` — computed (exact) (status: computed; evidence: `python code/run_eighteenth.py --check`)
- `H3V7N5QF:paper/eighth/claim_ledger.md::K1` — computed (exact) (status: computed; evidence: `summary.json`, `results_*.csv`, `counts.csv`)
- `H3V7N5QF:paper/eighth/claim_ledger.md::K2` — computed (exact) (status: computed; evidence: `rounds_*.csv`, `summary.json`)
- `H3V7N5QF:paper/eighth/claim_ledger.md::K3` — computed (exact) (status: computed; evidence: `rounds_*.csv`, `summary.json`)
- `H3V7N5QF:paper/eighth/claim_ledger.md::K4` — computed (exact) (status: computed; evidence: `attempts_bound2_rounds3_*.jsonl`, `summary.json` (`attempts_in_full_logs`))
- `H3V7N5QF:paper/eighth/claim_ledger.md::K5` — computed (exact) (status: computed; evidence: `frontier_*.csv`, `summary.json`)
- `H3V7N5QF:paper/eighth/claim_ledger.md::K6` — computed (exact) (status: computed; evidence: `added_*.csv`)
- `H3V7N5QF:paper/eighth/claim_ledger.md::K7` — computed (exact) (status: computed; evidence: `follows_*.csv`, `results_*.csv`, `summary.json`)
- `H3V7N5QF:paper/eighth/claim_ledger.md::K8` — computed (exact) (status: computed; evidence: `reach_bound2_rounds4_*.csv`, `summary.json` (`reachability`))
- `H3V7N5QF:paper/eighth/claim_ledger.md::K9` — computed (exact) (status: computed; evidence: `python code/generate_eighth.py --check`; the seven earlier `--check`s and Lean reports (`change_log.md` item 13))
- `H3V7N5QF:paper/eighth/claim_ledger.md::K10` — computed (exact) (status: computed; evidence: `python -m pytest`; `python code/xry/gate.py coverage.json`; `python -m mypy`; `python ci/check_prose_watchlist.py`)
- `H3V7N5QF:paper/eleventh/claim_ledger.md::D12` — computed (exact) (status: computed (two results; cost) + illustrated in Lean; evidence: `labeled_of` gives two results; `labeled.json`. Lean `labeled_extra` only shows two `Labeled` records with different letter functions differ (not up to renaming); `labeled_cost_is_size` is `rfl` (definition unfold))
- `H3V7N5QF:paper/eleventh/claim_ledger.md::K1` — computed (exact) (status: computed; evidence: `given.json` `r_collision_not_s`, `identify_drops_a_term`)
- `H3V7N5QF:paper/eleventh/claim_ledger.md::K2` — computed (exact) (status: computed; evidence: `writing_verdicts`; `writing_statements_holding_of_every_writing` empty in the committed 2-term 8-round run (`summary_bound2_rounds8.json`))
- `H3V7N5QF:paper/eleventh/claim_ledger.md::K3` — computed (exact) (status: computed; evidence: `labeled.json`)
- `H3V7N5QF:paper/fifteenth/claim_ledger.md::K1` — computed (exact) (status: computed; evidence: `given.json`)
- `H3V7N5QF:paper/fifteenth/claim_ledger.md::K2` — computed (exact) (status: computed; evidence: `admission_verdicts`; `admission_statements_holding_of_every_result`)
- `H3V7N5QF:paper/fifteenth/claim_ledger.md::K3` — computed (exact) (status: computed; evidence: `tagged.json`)
- `H3V7N5QF:paper/fifth/claim_ledger.md::K1` — computed (exact) (status: computed; evidence: `summary.json`, `results_*.csv`, `counts.csv`)
- `H3V7N5QF:paper/fifth/claim_ledger.md::K2` — computed (exact) (status: computed; evidence: `rounds_*.csv`, `summary.json`)
- `H3V7N5QF:paper/fifth/claim_ledger.md::K3` — computed (exact) (status: computed; evidence: `rounds_*.csv`, `summary.json` (`attempts_equal_formula`, `obstructed_equal_formula`, `changes_raising_the_round`, `changes_keeping_the_round`, `changes_lowering_the_round`))
- `H3V7N5QF:paper/fifth/claim_ledger.md::K4` — computed (exact) (status: computed; evidence: `summary.json` (`answers_*`), `attempts_bound2_rounds4_*.jsonl`)
- `H3V7N5QF:paper/fifth/claim_ledger.md::K5` — computed (exact) (status: computed; evidence: `frontier_*.csv`, `summary.json`)
- `H3V7N5QF:paper/fifth/claim_ledger.md::K6` — computed (exact) (status: computed; evidence: `added_*.csv`, `summary.json` (`results_with_fewer_terms_or_assertions_than_given`))
- `H3V7N5QF:paper/fifth/claim_ledger.md::K7` — computed (exact) (status: computed; evidence: `follows_*.csv`, `results_*.csv`, `summary.json`)
- `H3V7N5QF:paper/fifth/claim_ledger.md::K8` — computed (exact) (status: computed; evidence: `reach_bound3_rounds6_*.csv`, `summary.json` (`reachability`))
- `H3V7N5QF:paper/fifth/claim_ledger.md::K9` — computed (exact) (status: computed; evidence: `python code/generate_fifth.py --check`; `python code/generate.py --check`; `python code/generate_second.py --check`; `python code/generate_third.py --check`; `python code/generate_fourth.py --check`; the four earlier Lean reports)
- `H3V7N5QF:paper/fifth/claim_ledger.md::K10` — computed (exact) (status: computed; evidence: `python -m pytest`; `python code/xry/gate.py coverage.json`; `python -m mypy`; `python ci/check_prose_watchlist.py`)
- `H3V7N5QF:paper/fourteenth/claim_ledger.md::K1` — computed (exact) (status: computed; evidence: `given.json`)
- `H3V7N5QF:paper/fourteenth/claim_ledger.md::K2` — computed (exact) (status: computed; evidence: `leftover_verdicts`; `leftover_statements_holding_of_every_change` does not contain `leaves_nothing` at 4 or more rounds)
- `H3V7N5QF:paper/fourteenth/claim_ledger.md::K3` — computed (exact) (status: computed; evidence: `tagged.json`)
- `H3V7N5QF:paper/fourth/claim_ledger.md::K1` — computed (exact) (status: computed; evidence: `summary.json` (`results`, `results_by_terms`, `results_asserting_nothing_twice`, `explored_equals_independent_count`), `results_*.csv`, `counts.csv`)
- `H3V7N5QF:paper/fourth/claim_ledger.md::K2` — computed (exact) (status: computed; evidence: `rounds_*.csv`, `summary.json` (`last_round_with_a_new_result`, `rounds_agreeing_with_unbounded_formula`))
- `H3V7N5QF:paper/fourth/claim_ledger.md::K3` — computed (exact) (status: computed; evidence: `rounds_*.csv` (`changes_attempted_so_far`, `of_which_obstructed`), `summary.json` (`attempts_equal_formula_1_plus_n_squared`, `obstructed_equal_formula_n`))
- `H3V7N5QF:paper/fourth/claim_ledger.md::K4` — computed (exact) (status: computed; evidence: `frontier_*.csv`, `summary.json` (`frontier_*`, `results_of_the_last_round_whose_changes_await`, `changes_awaiting`))
- `H3V7N5QF:paper/fourth/claim_ledger.md::K5` — computed (exact) (status: computed; evidence: `added_*.csv`, `summary.json` (`additions_never_negative`))
- `H3V7N5QF:paper/fourth/claim_ledger.md::K6` — computed (exact) (status: computed; evidence: `follows_*.csv`, `summary.json` (`statements_holding_in_every_result`, `statements_that_do_not_follow`))
- `H3V7N5QF:paper/fourth/claim_ledger.md::K7` — computed (exact) (status: computed; evidence: `results_*.csv` (`sequences_of_changes`), `summary.json` (`sequences_of_changes_total`, `results_reached_by_one_sequence`, `two_term_sequences_equal_binomial`, `same_sequence_counts_as_third_derivation`), `tests/test_fourth_explore.py`)
- `H3V7N5QF:paper/fourth/claim_ledger.md::K8` — computed (exact) (status: computed; evidence: `reach_bound3_rounds6_*.csv`, `summary.json` (`reachability`, `results_that_reach_what_is_given`))
- `H3V7N5QF:paper/fourth/claim_ledger.md::K9` — computed (exact) (status: computed (the third's `--check`: not re-run); evidence: `python code/generate_fourth.py --check`; `python code/generate.py --check`; `python code/generate_second.py --check`; `tests/test_fourth_evidence.py::test_command_line`; to complete: `python code/generate_third.py --check`, `python code/lean_report.py`, `python code/lean_report_second.py`, `python code/lean_report_third.py`)
- `H3V7N5QF:paper/fourth/claim_ledger.md::K10` — computed (exact) (status: computed; evidence: `python -m pytest`; `python code/xry/gate.py coverage.json`; `python -m mypy`; `python ci/check_prose_watchlist.py`)
- `H3V7N5QF:paper/nineteenth/claim_ledger.md::N9` — computed (exact) (status: computed; evidence: `evidence/nineteenth/summary.json`)
- `H3V7N5QF:paper/nineteenth/claim_ledger.md::N10` — computed (exact) (status: computed; evidence: `obstruction_not_between`, `removal_answer_outside`)
- `H3V7N5QF:paper/ninth/claim_ledger.md::K1` — computed (exact) (status: computed; evidence: `summary.json`, `results_*.csv`, `counts.csv`)
- `H3V7N5QF:paper/ninth/claim_ledger.md::K2` — computed (exact) (status: computed; evidence: `rounds_*.csv`, `summary.json`)
- `H3V7N5QF:paper/ninth/claim_ledger.md::K3` — computed (exact) (status: computed; evidence: `rounds_*.csv`, `summary.json`)
- `H3V7N5QF:paper/ninth/claim_ledger.md::K4` — computed (exact) (status: computed; evidence: `attempts_bound2_rounds3.jsonl`, `summary.json` (`attempts_in_full_log`))
- `H3V7N5QF:paper/ninth/claim_ledger.md::K5` — computed (exact) (status: computed; evidence: `frontier_*.csv`, `summary.json`)
- `H3V7N5QF:paper/ninth/claim_ledger.md::K6` — computed (exact) (status: computed; evidence: `added_*.csv`)
- `H3V7N5QF:paper/ninth/claim_ledger.md::K7` — computed (exact) (status: computed; evidence: `follows_*.csv`, `results_*.csv`, `summary.json`)
- `H3V7N5QF:paper/ninth/claim_ledger.md::K8` — computed (exact) (status: computed; evidence: `reach_bound3_rounds5.csv`, `summary.json` (`reachability`))
- `H3V7N5QF:paper/ninth/claim_ledger.md::K9` — computed (exact) (status: computed; evidence: `python code/generate_ninth.py --check` (matched))
- `H3V7N5QF:paper/ninth/claim_ledger.md::K10` — computed (exact) (status: computed; evidence: `python -m pytest`; `python code/xry/gate.py coverage.json`; `python -m mypy`; `python ci/check_prose_watchlist.py`; paper §10)
- `H3V7N5QF:paper/second/claim_ledger.md::K1` — computed (exact) (status: computed; evidence: `evidence/second/counts.csv`, `summary.json` (`independent_counts`); cross-checked by listing for 1–3 terms (`tests/test_second_orbits.py`) and by the explorations)
- `H3V7N5QF:paper/second/claim_ledger.md::K2` — computed (exact) (status: computed; evidence: `evidence/second/rounds_*.csv`, `summary.json`)
- `H3V7N5QF:paper/second/claim_ledger.md::K3` — computed (exact) (status: computed from D8, D9; evidence: `evidence/second/rounds_*.csv` (last column), `summary.json` (`rounds_agreeing_with_unbounded_formula`))
- `H3V7N5QF:paper/second/claim_ledger.md::K4` — computed (exact) (status: computed; evidence: `evidence/second/rounds_*.csv`, `frontier_*.csv`, `summary.json`)
- `H3V7N5QF:paper/second/claim_ledger.md::K5` — computed (exact) (status: computed; evidence: `evidence/second/added_*.csv`, `results_*.csv`)
- `H3V7N5QF:paper/second/claim_ledger.md::K6` — computed (exact) (status: computed; evidence: `evidence/second/follows_*.csv`, `summary.json`)
- `H3V7N5QF:paper/second/claim_ledger.md::K7` — computed (exact) (status: computed; evidence: `evidence/second/reach_bound3_*.csv`, `summary.json` (`reachability`, `results_that_reach_what_is_given`))
- `H3V7N5QF:paper/second/claim_ledger.md::K8` — computed (exact) (status: computed; evidence: `summary.json` (`fewest_classes_checked_on`, `fewest_classes_lowered_by`))
- `H3V7N5QF:paper/second/claim_ledger.md::K9` — computed (exact) (status: computed; evidence: `python code/generate_second.py --check`; `python code/generate.py --check`; `python code/lean_report.py`; `tests/test_second_evidence.py::test_command_line`)
- `H3V7N5QF:paper/second/claim_ledger.md::K10` — computed (exact) (status: computed; evidence: `python -m pytest`; `python code/xry/gate.py coverage.json`; `python -m mypy`)
- `H3V7N5QF:paper/seventeenth/claim_ledger.md::K1` — computed (exact) (status: computed; evidence: `evidence/seventeenth/summary.json`; `tests/test_seventeenth_core.py`)
- `H3V7N5QF:paper/seventeenth/claim_ledger.md::K2` — computed (exact) (status: terms`) and 400 results first reached in round 6, whose changes the round bound left unattempted (`\; evidence: rounds`; per run in `unexpanded_by_run`); and the attempt log at 2 terms and 3 rounds)
- `H3V7N5QF:paper/seventeenth/claim_ledger.md::K3` — computed (exact) (status: computed; evidence: `python code/run_seventeenth.py --check`; `evidence/seventeenth/MANIFEST.sha256`)
- `H3V7N5QF:paper/seventeenth/claim_ledger.md::K4` — computed (exact) (status: computed; evidence: `evidence/seventeenth/lean_axioms.txt`; `tests/test_seventeenth_leanreport.py` fails if a cited theorem of `lean4/Seventeenth/` has no line there)
- `H3V7N5QF:paper/seventeenth/claim_ledger.md::K5` — computed (exact) (status: computed; evidence: `evidence/seventeenth/results_bound3_rounds6.csv`)
- `H3V7N5QF:paper/seventh/claim_ledger.md::K1` — computed (exact) (status: computed; evidence: `summary.json`, `results_*.csv`, `counts.csv`)
- `H3V7N5QF:paper/seventh/claim_ledger.md::K2` — computed (exact) (status: computed; evidence: `rounds_*.csv`, `summary.json`)
- `H3V7N5QF:paper/seventh/claim_ledger.md::K3` — computed (exact) (status: computed; evidence: `rounds_*.csv`, `summary.json`)
- `H3V7N5QF:paper/seventh/claim_ledger.md::K4` — computed (exact) (status: computed; evidence: `attempts_bound2_rounds4.jsonl`, `summary.json` (`attempts_in_full_log`))
- `H3V7N5QF:paper/seventh/claim_ledger.md::K5` — computed (exact) (status: computed; evidence: `frontier_*.csv`, `summary.json`)
- `H3V7N5QF:paper/seventh/claim_ledger.md::K6` — computed (exact) (status: computed; evidence: `added_*.csv`)
- `H3V7N5QF:paper/seventh/claim_ledger.md::K7` — computed (exact) (status: computed; evidence: `follows_*.csv`, `results_*.csv`, `summary.json`)
- `H3V7N5QF:paper/seventh/claim_ledger.md::K8` — computed (exact) (status: computed; evidence: `reach_bound3_rounds6.csv`, `summary.json` (`reachability`))
- `H3V7N5QF:paper/seventh/claim_ledger.md::K9` — computed (exact) (status: computed; evidence: `python code/generate_seventh.py --check`; the six earlier `--check`s and Lean reports (`change_log.md` item 12))
- `H3V7N5QF:paper/seventh/claim_ledger.md::K10` — computed (exact) (status: computed; evidence: `python -m pytest`; `python code/xry/gate.py coverage.json`; `python -m mypy`; `python ci/check_prose_watchlist.py`)
- `H3V7N5QF:paper/sixteenth/claim_ledger.md::D6` — computed (exact) (status: computed (the criterion against search); necessity derived through the mass, sufficiency from the empty state and by admitting every leftover; evidence: `code/sixteenth/reach.py` `carries`; `reach_bound3_rounds5.csv`, `summary.json` `reachability` (`criterion_agrees_with_search` on 27 889 pairs; 17 624 pairs the ninth admits and this seed refuses; none the reverse; 4 227 pairs the two invariants admit and the criterion refuses); Lean `Reach16.mass_le`, `reach16_by_additions`, `reach16_admit_all`)
- `H3V7N5QF:paper/sixteenth/claim_ledger.md::D7` — computed (exact) (status: computed (closed form checked against the exploration and the series in every run); evidence: `code/sixteenth/orbits.py` `one_term_round_count`; `one_term_rounds_equal_closed_form` true in every run; `counts.csv`)
- `H3V7N5QF:paper/sixteenth/claim_ledger.md::D14` — computed (exact) (status: computed; evidence: `alternatives.json` (`same_relation_identity_failures` 10 / 0; `reachability`); `given.json` `set_reading`)
- `H3V7N5QF:paper/sixteenth/claim_ledger.md::K1` — computed (exact) (status: computed; evidence: `summary.json`, `results_*.csv`, `counts.csv`)
- `H3V7N5QF:paper/sixteenth/claim_ledger.md::K2` — computed (exact) (status: computed; evidence: `rounds_*.csv`, `summary.json`)
- `H3V7N5QF:paper/sixteenth/claim_ledger.md::K3` — computed (exact) (status: computed; evidence: `summary.json` (`records`))
- `H3V7N5QF:paper/sixteenth/claim_ledger.md::K4` — computed (exact) (status: computed; evidence: `attempts_bound2_rounds3.jsonl`)
- `H3V7N5QF:paper/sixteenth/claim_ledger.md::K5` — computed (exact) (status: computed; evidence: `frontier_*.csv`, `summary.json`)
- `H3V7N5QF:paper/sixteenth/claim_ledger.md::K6` — computed (exact) (status: computed; evidence: `reach_bound3_rounds5.csv`, `summary.json` (`reachability`))
- `H3V7N5QF:paper/sixteenth/claim_ledger.md::K7` — computed (exact) (status: computed; evidence: `results_*.csv`, `summary.json`)
- `H3V7N5QF:paper/sixteenth/claim_ledger.md::K8` — computed (exact) (status: computed; evidence: `follows_*.csv`, `summary.json`)
- `H3V7N5QF:paper/sixteenth/claim_ledger.md::K9` — computed (exact) (status: computed; evidence: `python code/generate_sixteenth.py --check`)
- `H3V7N5QF:paper/sixteenth/claim_ledger.md::K10` — computed (exact) (status: computed; evidence: `python -m pytest`; `python code/xry/gate.py coverage.json`; `python -m mypy`; `python ci/check_prose_watchlist.py`; `python ci/check_vacuous_checks.py`; `python ci/check_definitional_citations.py`; `python ci/check_mutation_bite.py`)
- `H3V7N5QF:paper/sixth/claim_ledger.md::K1` — computed (exact) (status: computed; evidence: `summary.json`, `results_*.csv`, `counts.csv`)
- `H3V7N5QF:paper/sixth/claim_ledger.md::K2` — computed (exact) (status: computed; evidence: `rounds_*.csv`, `summary.json`)
- `H3V7N5QF:paper/sixth/claim_ledger.md::K3` — computed (exact) (status: computed; evidence: `rounds_*.csv`, `summary.json` (`attempts_equal_formula`, `xrx_making_equal_formula`, `changes_raising_the_round`, `changes_keeping_the_round`, `changes_lowering_the_round`))
- `H3V7N5QF:paper/sixth/claim_ledger.md::K4` — computed (exact) (status: computed; evidence: `attempts_bound2_rounds3_*.jsonl`, `summary.json` (`attempts_in_full_logs`))
- `H3V7N5QF:paper/sixth/claim_ledger.md::K5` — computed (exact) (status: computed; evidence: `frontier_*.csv`, `summary.json`)
- `H3V7N5QF:paper/sixth/claim_ledger.md::K6` — computed (exact) (status: computed; evidence: `added_*.csv`, `summary.json` (`results_with_fewer_terms_or_assertions_than_given`))
- `H3V7N5QF:paper/sixth/claim_ledger.md::K7` — computed (exact) (status: computed; evidence: `follows_*.csv`, `results_*.csv`, `summary.json`)
- `H3V7N5QF:paper/sixth/claim_ledger.md::K8` — computed (exact) (status: computed; evidence: `reach_bound3_rounds4_*.csv`, `summary.json` (`reachability`))
- `H3V7N5QF:paper/sixth/claim_ledger.md::K9` — computed (exact) (status: computed; evidence: `python code/generate_sixth.py --check`; the five earlier `--check`s and Lean reports (`change_log.md` item 15))
- `H3V7N5QF:paper/sixth/claim_ledger.md::K10` — computed (exact) (status: computed; evidence: `python -m pytest`; `python code/xry/gate.py coverage.json`; `python -m mypy`; `python ci/check_prose_watchlist.py`)
- `H3V7N5QF:paper/tenth/claim_ledger.md::K1` — computed (exact) (status: computed; evidence: `given.json` `three_outcomes_inhabited`; leftovers of the 2-term 8-round run)
- `H3V7N5QF:paper/tenth/claim_ledger.md::K2` — computed (exact) (status: computed; evidence: the 2-term 8-round run (`summary_bound2_rounds8.json`): all three outcomes inhabited (`leftovers.three_outcomes_inhabited`), so each of the three statements holds of some change and fails of some, and `leftover_statements_holding_of_every_change` is empty; `tests/test_tenth_follows.py` at 2 terms and 4 rounds)
- `H3V7N5QF:paper/tenth/claim_ledger.md::K3` — computed (exact) (status: computed; evidence: `tagged.json`)
- `H3V7N5QF:paper/third/claim_ledger.md::K1` — computed (exact) (status: computed; evidence: `evidence/third/counts.csv`, `summary.json` (`independent_counts`); the explorations agree within the bounds)
- `H3V7N5QF:paper/third/claim_ledger.md::K2` — computed (exact) (status: computed; evidence: `evidence/third/rounds_*.csv`, `summary.json`)
- `H3V7N5QF:paper/third/claim_ledger.md::K3` — computed (exact) (status: computed from D8, D9; evidence: `evidence/third/rounds_*.csv` (last two columns), `summary.json` (`rounds_agreeing_with_unbounded_formula`, `same_results_rounds_and_attempts_as_second_derivation_without_identifications`))
- `H3V7N5QF:paper/third/claim_ledger.md::K4` — computed (exact) (status: computed; evidence: `evidence/third/rounds_*.csv`, `frontier_*.csv`, `summary.json`)
- `H3V7N5QF:paper/third/claim_ledger.md::K5` — computed (exact) (status: computed; evidence: `evidence/third/added_*.csv`, `results_*.csv`)
- `H3V7N5QF:paper/third/claim_ledger.md::K6` — computed (exact) (status: computed; evidence: `evidence/third/follows_*.csv`, `summary.json`)
- `H3V7N5QF:paper/third/claim_ledger.md::K7` — computed (exact) (status: computed; evidence: `evidence/third/results_*.csv`, `summary.json` (`sequences_of_changes_total`, `results_reached_by_one_sequence`); `tests/test_third_explore.py::test_sequences_are_counted_and_the_witnesses_differ` (asserts the totals 393 and 66 and their equality))
- `H3V7N5QF:paper/third/claim_ledger.md::K8` — computed (exact) (status: computed; evidence: `evidence/third/reach_bound3_*.csv`, `summary.json` (`reachability`, `results_that_reach_what_is_given`))
- `H3V7N5QF:paper/third/claim_ledger.md::K9` — computed (exact) (status: computed; evidence: `python code/generate_third.py --check`; `python code/generate.py --check`; `python code/generate_second.py --check`; `python code/lean_report.py`; `python code/lean_report_second.py`; `tests/test_third_evidence.py::test_command_line`)
- `H3V7N5QF:paper/third/claim_ledger.md::K10` — computed (exact) (status: computed; evidence: `python -m pytest`; `python code/xry/gate.py coverage.json`; `python -m mypy`; `python ci/check_prose_watchlist.py`)
- `H3V7N5QF:paper/thirteenth/claim_ledger.md::K1` — computed (exact) (status: computed; evidence: `given.json`)
- `H3V7N5QF:paper/thirteenth/claim_ledger.md::K2` — computed (exact) (status: computed; evidence: `coarse_verdicts`; `coarse_statements_holding_of_every_result` empty in the committed `summary_bound2_rounds8.json`. The exchange statement counts a result different from its exchange up to writing (`not same`), not merely differing `r`/`s` tuples (corrected at review))
- `H3V7N5QF:paper/thirteenth/claim_ledger.md::K3` — computed (exact) (status: computed; evidence: `coarse.json`)
- `H3V7N5QF:paper/twelfth/claim_ledger.md::D12` — computed (exact) (status: computed; evidence: `recorded.json` (six on `1::)
- `H3V7N5QF:paper/twelfth/claim_ledger.md::K1` — computed (exact) (status: computed; evidence: `given.json` `r_record_not_s`, `identify_drops_a_term`, `two_term_empty_restored`)
- `H3V7N5QF:paper/twelfth/claim_ledger.md::K2` — computed (exact) (status: computed; evidence: `record_verdicts`; `record_statements_holding_of_every_identification` is `['determined']` in the committed `summary_bound2_rounds8.json`)
- `H3V7N5QF:paper/twelfth/claim_ledger.md::K3` — computed (exact) (status: computed; evidence: `recorded.json`)
- `H3V7N5QF:paper/twentyfifth/claim_ledger.md::K1` — computed (exact) (status: computed; evidence: `summary.json` `runs`, `disagreements`)
- `H3V7N5QF:paper/twentyfifth/claim_ledger.md::K2` — computed (exact) (status: computed; evidence: paper K2; `frontier_*.csv`; the independent count)
- `H3V7N5QF:paper/twentyfifth/claim_ledger.md::K3` — computed (exact) (status: computed; evidence: `summary.json` `map_back`)
- `H3V7N5QF:paper/twentyfifth/claim_ledger.md::K4` — computed (exact) (status: computed; evidence: `summary.json` `twentythird_derivation`, `embed_mismatch` empty)
- `H3V7N5QF:paper/twentyfifth/claim_ledger.md::K5` — computed (exact) (status: computed; evidence: `summary.json` `the_twentythird_record`, `records_*.csv`)
- `H3V7N5QF:paper/twentyfifth/claim_ledger.md::K6` — computed (exact) (status: computed; evidence: `summary.json` `told_or_not`)
- `H3V7N5QF:paper/twentyfifth/claim_ledger.md::K7` — computed (exact) (status: computed; evidence: `reach_bound3_rounds5.csv`)
- `H3V7N5QF:paper/twentyfifth/claim_ledger.md::K8` — computed (exact) (status: computed; evidence: `readings.json`)
- `H3V7N5QF:paper/twentyfifth/claim_ledger.md::K9` — computed (exact) (status: computed; evidence: `summary.json` `changes`)
- `H3V7N5QF:paper/twentyfifth/claim_ledger.md::K10` — computed (exact) (status: computed; evidence: `decide.csv`, `unseen.csv`, `summary.json`)
- `H3V7N5QF:paper/twentyfifth/claim_ledger.md::K11` — computed (exact) (status: computed; evidence: `MANIFEST.sha256`, `lean_axioms.txt`)
- `H3V7N5QF:paper/twentyfifth/claim_ledger.md::N10` — computed (exact) (status: computed; evidence: `follows_*.csv`)
- `H3V7N5QF:paper/twentyfourth/claim_ledger.md::D17` — computed (exact) (status: computed; evidence: `follows_*.csv`)
- `H3V7N5QF:paper/twentyfourth/claim_ledger.md::K1` — computed (exact) (status: computed; evidence: `results_*.csv`, `rounds_*.csv`, `summary.json`)
- `H3V7N5QF:paper/twentyfourth/claim_ledger.md::K2` — computed (exact) (status: derived; computed; evidence: paper K2; `shortest24`; `frontier_*.csv`)
- `H3V7N5QF:paper/twentyfourth/claim_ledger.md::K3` — computed (exact) (status: computed; evidence: `summary.json`)
- `H3V7N5QF:paper/twentyfourth/claim_ledger.md::K4` — computed (exact) (status: computed; evidence: `summary.json` (`twentythird`))
- `H3V7N5QF:paper/twentyfourth/claim_ledger.md::K5` — computed (exact) (status: computed; evidence: `given.json`)
- `H3V7N5QF:paper/twentyfourth/claim_ledger.md::K6` — computed (exact) (status: computed; evidence: `follows_*.csv`)
- `H3V7N5QF:paper/twentyfourth/claim_ledger.md::K7` — computed (exact) (status: computed; evidence: `reach_bound2_rounds4.csv`, `summary.json`)
- `H3V7N5QF:paper/twentyfourth/claim_ledger.md::K8` — computed (exact) (status: computed; evidence: `readings.json`)
- `H3V7N5QF:paper/twentyfourth/claim_ledger.md::K9` — computed (exact) (status: computed; evidence: `summary.json`)
- `H3V7N5QF:paper/twentysecond/claim_ledger.md::K1` — computed (exact) (status: computed; evidence: `summary.json` `runs`, `disagreements`)
- `H3V7N5QF:paper/twentysecond/claim_ledger.md::K2` — computed (exact) (status: computed; evidence: `summary.json` `seventh_derivation`, `seventh_mismatch` empty)
- `H3V7N5QF:paper/twentysecond/claim_ledger.md::K3` — computed (exact) (status: computed; evidence: `summary.json`)
- `H3V7N5QF:paper/twentysecond/claim_ledger.md::K4` — computed (exact) (status: computed; evidence: `summary.json` `ninth_derivation`, `ninth_mismatch` empty)
- `H3V7N5QF:paper/twentysecond/claim_ledger.md::K5` — computed (exact) (status: computed; evidence: `results_*.csv`)
- `H3V7N5QF:paper/twentysecond/claim_ledger.md::K6` — computed (exact) (status: computed; evidence: `follows_*.csv`)
- `H3V7N5QF:paper/twentysecond/claim_ledger.md::K7` — computed (exact) (status: computed; evidence: `reach_bound3_rounds4.csv`, `summary.json`)
- `H3V7N5QF:paper/twentysecond/claim_ledger.md::K8` — computed (exact) (status: computed; evidence: `readings.json`)
- `H3V7N5QF:paper/twentysecond/claim_ledger.md::K9` — computed (exact) (status: computed; evidence: `MANIFEST.sha256`, `lean_axioms.txt`)
- `H3V7N5QF:paper/twentysecond/claim_ledger.md::N9` — computed (exact) (status: computed; evidence: `results_*.csv`)
- `H3V7N5QF:paper/twentysecond/claim_ledger.md::N10` — computed (exact) (status: computed; evidence: `follows_*.csv`)
- `H3V7N5QF:paper/twentythird/claim_ledger.md::K1` — computed (exact) (status: computed; evidence: `summary.json` `runs`, `disagreements`)
- `H3V7N5QF:paper/twentythird/claim_ledger.md::K2` — computed (exact) (status: computed; evidence: paper K2; `frontier_*.csv`)
- `H3V7N5QF:paper/twentythird/claim_ledger.md::K3` — computed (exact) (status: computed; evidence: `summary.json` `map_back`)
- `H3V7N5QF:paper/twentythird/claim_ledger.md::K4` — computed (exact) (status: computed; evidence: `summary.json` `ninth_derivation`, `ninth_mismatch` empty)
- `H3V7N5QF:paper/twentythird/claim_ledger.md::K5` — computed (exact) (status: computed; evidence: `summary.json` `twentysecond_derivation`)
- `H3V7N5QF:paper/twentythird/claim_ledger.md::K6` — computed (exact) (status: computed; evidence: `follows_*.csv`)
- `H3V7N5QF:paper/twentythird/claim_ledger.md::K7` — computed (exact) (status: computed; evidence: `reach_bound3_rounds4.csv`)
- `H3V7N5QF:paper/twentythird/claim_ledger.md::K8` — computed (exact) (status: computed; evidence: `readings.json`)
- `H3V7N5QF:paper/twentythird/claim_ledger.md::K9` — computed (exact) (status: computed; evidence: `MANIFEST.sha256`, `lean_axioms.txt`)
- `H3V7N5QF:paper/twentythird/claim_ledger.md::N10` — computed (exact) (status: computed; evidence: `follows_*.csv`)

## Stated in prose only

Derived, refuted, or negative ledger rows whose evidence cell does not name a Lean file. Open rows are not listed here; they are unmet. A row that only cites an earlier claim ID has the mark of this row as its ledger wording; the Lean declaration, when one exists, is the census entry for that earlier claim. A row whose evidence names `summary.json`, `counts.csv`, or an orbits module, and no Lean declaration, is a paper argument plus an exact file. The mark stays stated in prose only because there is no Lean declaration; the file was not re-run.

- `H3V7N5QF:paper/claim_ledger.md::D12` — stated in prose only (derived + computed. Within the bound the exploration is complete, rounds equal fewest changes without bound, and the frontier is exact Evidence: paper §4 (D12); `evidence/summary.json`, `evidence/counts.csv`, `evidence/frontier_*.csv`, `frontier_entries_are_1_plus_2N_per_state_with_N_terms`)
- `H3V7N5QF:paper/claim_ledger.md::R1` — stated in prose only (refuted. `a` and `b` are one term to begin with Evidence: D1)
- `H3V7N5QF:paper/claim_ledger.md::R2` — stated in prose only (refuted. Some answer makes adding `xrx` performable Evidence: D4)
- `H3V7N5QF:paper/claim_ledger.md::R4` — stated in prose only (refuted. Some sequence of changes reaches a state without terms Evidence: D6 (`Reach.nonempty`))
- `H3V7N5QF:paper/claim_ledger.md::R5` — stated in prose only (refuted. After `a`, `b` are identified, some changes tell them apart or assert `arb` again Evidence: D7)
- `H3V7N5QF:paper/claim_ledger.md::R6` — stated in prose only (refuted. Some answer reaches a result that unobstructed changes do not reach Evidence: D10)
- `H3V7N5QF:paper/claim_ledger.md::N3` — stated in prose only (do not follow (computed witnesses: the two beginnings). Never both ways; passing on; every term first; always both ways Evidence: `evidence/follows_anchored_*.csv`)
- `H3V7N5QF:paper/claim_ledger.md::N4` — stated in prose only (do not follow for results (computed witnesses). `arb` stays asserted; `a`, `b` stay two; exactly two terms; something asserted Evidence: `evidence/follows_*.csv` (first rounds 1, 2, 1, 1 without `bra`; 1, 3, 1, 2 with it))
- `H3V7N5QF:paper/claim_ledger.md::N5` — stated in prose only (does not follow (derived from D9). Any statement about the asserting that holds in one finite legal state and fails in another Evidence: D9)
- `H3V7N5QF:paper/claim_ledger.md::N6` — stated in prose only (does not follow (derived from D3, D4, D5, D10). Which answer an obstructed change gets Evidence: as cited)
- `H3V7N5QF:paper/claim_ledger.md::N7` — stated in prose only (does not follow (witnesses: what is given, which adds no term, and a result one change away that adds one); that every result is finite is derived (D6). Growth: that terms must be added Evidence: `evidence/added_*.csv`)
- `H3V7N5QF:paper/eighteenth/claim_ledger.md::R1` — stated in prose only (refuted. Two writings of one base result are one result Evidence: D2, K1, K2)
- `H3V7N5QF:paper/eighteenth/claim_ledger.md::R2` — stated in prose only (refuted. The changes reach a last result with no bound on terms Evidence: the frontier is non-empty; adding a term is never obstructed (base `addTerm_legal`))
- `H3V7N5QF:paper/eighth/claim_ledger.md::D10` — stated in prose only (derived (paper §4) + computed. Within the bound the exploration is complete; the independent count with two multiplicities per cycle certifies it; the count is not the product of the single-relation counts for `n ≥ 2` and is for `n = 1`; the frontier is one entry per res... Evidence: `code/eighth/orbits.py`; `summary.json` (`explored_equals_independent_count`, `count_exceeds_product_for_two_or_more_terms`, `product_equals_count_for_one_term`, `frontier_entries_are_1_per_state_with_N_terms`, `results_with_exact_sequence_count`, `rounds_agreeing_with_unbounded_formula`), `counts.csv`, `tests/test_eighth_orbits.py` (counts against listing every writing))
- `H3V7N5QF:paper/eighth/claim_ledger.md::D11` — stated in prose only (derived (paper §4) + computed. Two terms, names kept: the results of round `r` are the sixth's two-term kinds convolved with the `s` states (`C(r − k + 3, 3)`) plus the one-term states; the shortest sequences to a result with the names apart are a multinomial with eight ... Evidence: `code/eighth/orbits.py` (`two_term_round_count`), `code/eighth/evidence.py` (`two_term_multinomial`), `summary.json` (`two_term_rounds_equal_closed_form`, `two_term_sequences_equal_multinomial` true on both ANCHORED two-term runs), `tests/test_eighth_explore.py`)
- `H3V7N5QF:paper/eighth/claim_ledger.md::D14` — stated in prose only (derived (from D5) + computed. Exactly "at least one term" (on either part) holds in every result Evidence: `follows_*.csv`, `summary.json` (`statements_holding_in_every_result`))
- `H3V7N5QF:paper/eighth/claim_ledger.md::D15` — stated in prose only (derived (paper §4). The unchosen reading of identification (the larger of the two, per relation) gives the same results and reachability, and the same cost without `bra` Evidence: paper §4 D15)
- `H3V7N5QF:paper/eighth/claim_ledger.md::R1` — stated in prose only (refuted. `a` and `b` one term to begin with Evidence: D1 (`givenA8_a`, `givenA8_b`))
- `H3V7N5QF:paper/eighth/claim_ledger.md::R2` — stated in prose only (refuted. An attempt that is refused, or obstructed Evidence: D3; `given.json` (`of_which_obstructed: 0`); `summary.json` (`given.attempts_not_performed: 0`))
- `H3V7N5QF:paper/eighth/claim_ledger.md::R3` — stated in prose only (refuted. Telling `a` and `b` apart again after identifying them, in either relation; reaching what is given from a one-term state Evidence: D2)
- `H3V7N5QF:paper/eighth/claim_ledger.md::R4` — stated in prose only (refuted. A sequence of changes to a result shorter than its cost Evidence: D4 (`fewest_changes8_lower_A`, `_B`))
- `H3V7N5QF:paper/eighth/claim_ledger.md::R5` — stated in prose only (refuted. A well-formed state with a term that is not a result; a pair of well-formed parts on the same terms that is not Evidence: D5 (`result8_iff_A`, `results_pair`))
- `H3V7N5QF:paper/eighth/claim_ledger.md::R6` — stated in prose only (refuted. A change that keeps the cost, or the round, where it was Evidence: D4(v) (`Reach8.size_parity`; `changes_keeping_the_round: 0`))
- `H3V7N5QF:paper/eighth/claim_ledger.md::R7` — stated in prose only (refuted. Two results with the names apart, or with the same `r` part, that do not reach each other; two results neither of which reaches the other Evidence: D8, D9 (`reach8_symm`, `same_r_part_mutual`, `reach8_total`))
- `H3V7N5QF:paper/eighth/claim_ledger.md::R8` — stated in prose only (refuted. A given `s` assertion; an `s` assertion destroyed along a shortest sequence Evidence: D4, D13 (`s_costs_its_total`; the cost-raising rule))
- `H3V7N5QF:paper/eighth/claim_ledger.md::R9` — stated in prose only (refuted. A rewriting of one relation that is not a rewriting of the other Evidence: D7 (`proj_rename8`: one rewriting, both parts))
- `H3V7N5QF:paper/eighth/claim_ledger.md::R10` — stated in prose only (refuted. The count of results as the product of the single-relation counts, for two or more terms Evidence: D10 (`count_exceeds_product_for_two_or_more_terms`; 20 against 16, 8 against 4))
- `H3V7N5QF:paper/eighth/claim_ledger.md::N1` — stated in prose only (do not follow (derived from D5; computed witnesses). Anything about the asserting, in either relation or jointly, other than "at least one term" (fifty statements tested) Evidence: `follows_*.csv`, `summary.json` (`statements_that_do_not_follow`))
- `H3V7N5QF:paper/eighth/claim_ledger.md::N3` — stated in prose only (does not follow (derived: D5, `results_pair`; computed witnesses on the given terms). That the `s` part determines anything about the `r` part, or the converse Evidence: `results_*.csv`)
- `H3V7N5QF:paper/eighth/claim_ledger.md::N5` — stated in prose only (does not follow (D3: 10 for `a b; nothing asserted`, 12 for `a b; arb asb`). That results of one round with equally many terms have equally many changes Evidence: column `changes` of `results_*.csv`)
- `H3V7N5QF:paper/eighth/claim_ledger.md::N6` — stated in prose only (refuted (witnesses; `changes_lowering` in every run). That a multiplicity, the number of terms, either total, the size or the fewest classes in either relation never falls; that no `xrx`, or no `xsx`, stays asserted Evidence: `summary.json`; `tests/test_eighth_follows_invariants.py`)
- `H3V7N5QF:paper/eighth/claim_ledger.md::N9` — stated in prose only (refuted for `n ≥ 2`, holds for `n = 1` (D10). That the number of results with `n` terms is the product of the single-relation counts Evidence: `counts.csv`, `summary.json`)
- `H3V7N5QF:paper/eleventh/claim_ledger.md::D10` — stated in prose only (derived (identity) + computed. C-W1 results, rounds, sequences and count are the ninth's; count not a product for `n ≥ 2` Evidence: the C-W1 exploration wraps the ninth's, so `same_results`, rounds and sequences agree by construction; the one independent check is `explored_equals_independent_count` (the ninth's orbit count); 9:D10 for the non-product)
- `H3V7N5QF:paper/eleventh/claim_ledger.md::R1` — stated in prose only (refuted. Writing is identifying Evidence: G16 "remain two terms"; D8)
- `H3V7N5QF:paper/eleventh/claim_ledger.md::R2` — stated in prose only (refuted. Writing is a third multiplicity Evidence: G16 a writing of terms; D6)
- `H3V7N5QF:paper/fifteenth/claim_ledger.md::D10` — stated in prose only (derived (identity) + computed. C-A1 results, rounds, sequences and count are the ninth's; count not a product for `n ≥ 2` Evidence: the C-A1 exploration wraps the ninth's, so `same_results`, rounds and sequences agree by construction; the one independent check is `explored_equals_independent_count` (the ninth's orbit count); 9:D10 for the non-product)
- `H3V7N5QF:paper/fifth/claim_ledger.md::D14` — stated in prose only (derived (paper §4) + computed. Within the bound (terms and rounds) the exploration is complete; the independent count by (terms, total, destroyed givens) certifies it; the frontier is exact in both parts; the shortest-sequence counts are exact for results with fewer term... Evidence: `code/fifth/orbits.py`; `summary.json` (`explored_equals_independent_count`, `frontier_entries_are_1_plus_2N_per_state_with_N_terms`, `rounds_agreeing_with_unbounded_formula`, `results_with_exact_sequence_count`), `counts.csv`, `tests/test_fifth_orbits.py` (counts against listing every writing))
- `H3V7N5QF:paper/fifth/claim_ledger.md::D17` — stated in prose only (derived (paper §4) + computed. Two terms, names kept: results of round `r` are `1, 3, 5, 6` then `2r` (no `bra`), `1, 4, 6, 7` then `2r` (`bra`); on results with no destroyed given the shortest sequences are `C(i + j, i)` Evidence: `code/fifth/evidence.py` (`two_term_round_count`), `summary.json` (`two_term_rounds_equal_closed_form`, `two_term_sequences_equal_binomial` true on all 100 rounds), `rounds_bound2_rounds100_*.csv`, `tests/test_fifth_explore.py::test_two_terms_all_rounds`)
- `H3V7N5QF:paper/fifth/claim_ledger.md::D18` — stated in prose only (derived + computed. Every state has a two-change cycle; no change keeps the round; the two ANCHORED explorations no longer correspond round by round Evidence: D13, D8(v); `summary.json` (`results` differ: 14 061 / 17 240))
- `H3V7N5QF:paper/fifth/claim_ledger.md::D19` — stated in prose only (derived (paper §4). The unchosen reading of identification (the larger of the two multiplicities) gives the same results, the same cost and the same reachability criterion Evidence: paper §3 C5″, §4 D19: the proofs of D8, D9, D12 use only "a merged multiplicity is at least each part" and "an identification lowers the size by at least one", or identify terms with nothing asserted between the merged pairs)
- `H3V7N5QF:paper/fifth/claim_ledger.md::R1` — stated in prose only (refuted. `a` and `b` one term to begin with Evidence: D1)
- `H3V7N5QF:paper/fifth/claim_ledger.md::R2` — stated in prose only (refuted. An answer that makes adding `xrx` performable Evidence: D4)
- `H3V7N5QF:paper/fifth/claim_ledger.md::R3` — stated in prose only (refuted. Clearing an obstructed identification by any change but the removal of the obstruction Evidence: D5 (`obstruction_persists5`))
- `H3V7N5QF:paper/fifth/claim_ledger.md::R4` — stated in prose only (refuted. A state without terms Evidence: D6 (`Reach5.nonempty`))
- `H3V7N5QF:paper/fifth/claim_ledger.md::R5` — stated in prose only (refuted. Telling `a` and `b` apart again, or asserting `arb` again, after identifying them; reaching what is given from the one-term state Evidence: D7)
- `H3V7N5QF:paper/fifth/claim_ledger.md::R6` — stated in prose only (refuted. An answer that reaches a result unobstructed changes do not reach Evidence: D10)
- `H3V7N5QF:paper/fifth/claim_ledger.md::R7` — stated in prose only (refuted. `bra` together with passing on in one legal state Evidence: D15 (`passing_on_refutes_bra`))
- `H3V7N5QF:paper/fifth/claim_ledger.md::R8` — stated in prose only (refuted. A sequence of changes to a result shorter than its cost Evidence: D8 (`fewest_changes5_lower_A`, `_B`))
- `H3V7N5QF:paper/fifth/claim_ledger.md::R9` — stated in prose only (refuted. A legal state with at least one term that is not a result Evidence: D9)
- `H3V7N5QF:paper/fifth/claim_ledger.md::R10` — stated in prose only (refuted. A change that keeps the cost, or the round, where it was Evidence: D8(v) (`Reach5.size_parity`; `changes_keeping_the_round: 0`))
- `H3V7N5QF:paper/fifth/claim_ledger.md::R11` — stated in prose only (refuted. A third one-term build for an obstructed `xrx` Evidence: 4:D10, 4:R15 (about additions; computed on the beginnings))
- `H3V7N5QF:paper/fifth/claim_ledger.md::R12` — stated in prose only (refuted. Two results with the names apart that do not reach each other; two results neither of which reaches the other Evidence: D13 (`reach5_symm`, `reach5_total`))
- `H3V7N5QF:paper/fifth/claim_ledger.md::R13` — stated in prose only (refuted. Under the unchosen reading of identification, a result or a fewest-changes count differing from the chosen reading's Evidence: D19)
- `H3V7N5QF:paper/fifth/claim_ledger.md::N3` — stated in prose only (do not follow (derived from D9; computed witnesses). Any statement about the asserting other than "no `xrx`" and "at least one term" (twenty-one tested) Evidence: `follows_*.csv`, `summary.json` (`statements_that_do_not_follow`))
- `H3V7N5QF:paper/fifth/claim_ledger.md::N4` — stated in prose only (does not follow (computed witnesses: what is given; add a term; the one-term state). Exactly two terms Evidence: `follows_*.csv`)
- `H3V7N5QF:paper/fifth/claim_ledger.md::N5` — stated in prose only (do not follow (computed witnesses, first failing rounds 1, 2, 1). That what is given survives: `arb` asserted; `a`, `b` two terms; something asserted Evidence: `follows_*.csv`)
- `H3V7N5QF:paper/fifth/claim_ledger.md::N6` — stated in prose only (does not follow (derived from D3, D5, D10). Which answer an obstructed change gets Evidence: as cited)
- `H3V7N5QF:paper/fifth/claim_ledger.md::N7` — stated in prose only (does not follow (witnesses: what is given; one change each way). Growth: that terms, or assertions, must be added or must stay Evidence: `added_*.csv`)
- `H3V7N5QF:paper/fifth/claim_ledger.md::N9` — stated in prose only (does not follow (D3: 6 for `a b; nothing asserted`, 8 for `a b; arb bra`). That results of one round with equally many terms have equally many attempts Evidence: column `changes` of `results_*.csv`)
- `H3V7N5QF:paper/fifth/claim_ledger.md::N10` — stated in prose only (do not follow (computed witnesses). Nothing twice; `arb` once; all asserted equally often; both ways equally often Evidence: `follows_*.csv`)
- `H3V7N5QF:paper/fifth/claim_ledger.md::N11` — stated in prose only (does not follow (derived D9; computed: the same lists). That the two beginnings differ in what they reach or in which statements are independent Evidence: `summary.json`)
- `H3V7N5QF:paper/fourteenth/claim_ledger.md::D10` — stated in prose only (derived (identity) + computed. C-F1 results, rounds, sequences and count are the ninth's; count not a product for `n ≥ 2` Evidence: the C-F1 exploration wraps the ninth's, so `same_results`, rounds and sequences agree by construction; the one independent check is `explored_equals_independent_count` (the ninth's orbit count); 9:D10 for the non-product)
- `H3V7N5QF:paper/fourth/claim_ledger.md::D14` — stated in prose only (derived + computed. Within the bound (terms and rounds) the exploration is complete; the independent count by series certifies it; the frontier is exact in both parts; the sequence counts are exact; the number of results per round without bound is given by the... Evidence: paper §4; `code/fourth/orbits.py`; `summary.json` (`explored_equals_independent_count`, `rounds_agreeing_with_unbounded_formula`, `frontier_entries_are_1_plus_2N_per_state_with_N_terms`), `frontier_*.csv`, `counts.csv`, `tests/test_fourth_orbits.py` (counts against listing every writing))
- `H3V7N5QF:paper/fourth/claim_ledger.md::D17` — stated in prose only (derived (paper §4) + computed. Two terms: results of round `r` are `r + 1` (names kept, with or without `bra`), `⌊(r + 1)/2⌋ + 1` (FREE, no `bra`), `⌊r/2⌋ + 1` (FREE, `bra`); sequences to `(1 + i, j)` are `C(i + j, i)`; `2^r` per round; `2^101 − 1` in 100 rounds Evidence: `rounds_bound2_rounds100_*.csv`, `results_bound2_rounds100_*.csv`, `summary.json` (`two_term_sequences_equal_binomial`, `sequences_of_changes_total`), `tests/test_fourth_explore.py::test_two_terms_all_rounds`, `tests/test_fourth_orbits.py::test_two_term_counts_in_closed_form`)
- `H3V7N5QF:paper/fourth/claim_ledger.md::D18` — stated in prose only (derived (paper §4) + computed. Names kept, adding `bra` once is a one-to-one correspondence between the results of the beginning without `bra` and those of the beginning with it, round by round, commuting with every change; so the two ANCHORED explorations have the same ... Evidence: `summary.json` (equal `results`, `results_by_terms`, `sequences_of_changes_total`, attempts in the three ANCHORED pairs of runs and the census))
- `H3V7N5QF:paper/fourth/claim_ledger.md::R1` — stated in prose only (refuted. `a` and `b` one term to begin with Evidence: D1)
- `H3V7N5QF:paper/fourth/claim_ledger.md::R2` — stated in prose only (refuted. An answer that makes adding `xrx` performable Evidence: D4)
- `H3V7N5QF:paper/fourth/claim_ledger.md::R3` — stated in prose only (refuted. Removing the obstruction of any obstructed change; any change lowering a multiplicity Evidence: D7 (`Reach4.mult_le`, `no_change_asserts_xrx4`))
- `H3V7N5QF:paper/fourth/claim_ledger.md::R4` — stated in prose only (refuted. A result with fewer than two terms; the one-term state Evidence: D6, `oneTerm_unreachable4_A`, `oneTerm_unreachable4_B`)
- `H3V7N5QF:paper/fourth/claim_ledger.md::R5` — stated in prose only (refuted. Identifying `a` and `b`, or lowering the multiplicity of `arb`, ever Evidence: D6 (`Reach4.names_apart`, `Reach4.arb_mult_le`))
- `H3V7N5QF:paper/fourth/claim_ledger.md::R6` — stated in prose only (refuted. An answer that reaches a result additions do not reach Evidence: D10)
- `H3V7N5QF:paper/fourth/claim_ledger.md::R7` — stated in prose only (refuted. `bra` together with passing on; with `bra` given, passing on in any result Evidence: D15)
- `H3V7N5QF:paper/fourth/claim_ledger.md::R8` — stated in prose only (refuted. The beginning with `bra` reaching the beginning without Evidence: D2 (`givenB4_never_givenA4`))
- `H3V7N5QF:paper/fourth/claim_ledger.md::R9` — stated in prose only (refuted. A result that does not contain what is given (multiplicities included) Evidence: D9)
- `H3V7N5QF:paper/fourth/claim_ledger.md::R10` — stated in prose only (refuted. A sequence of changes to a result whose length is not the size difference Evidence: D8)
- `H3V7N5QF:paper/fourth/claim_ledger.md::R11` — stated in prose only (refuted. A change that lowers the fewest classes Evidence: D13 (`Reach4.split_mono`))
- `H3V7N5QF:paper/fourth/claim_ledger.md::R12` — stated in prose only (refuted. A change that lowers the number of terms, the total multiplicity or any multiplicity, or that leaves the size where it was or raises it by more than one Evidence: D6, D8)
- `H3V7N5QF:paper/fourth/claim_ledger.md::R13` — stated in prose only (refuted. A result returned to after being left; any result other than what is given reaching what is given Evidence: D13)
- `H3V7N5QF:paper/fourth/claim_ledger.md::R14` — stated in prose only (refuted. Two different results reachable from each other Evidence: D13)
- `H3V7N5QF:paper/fourth/claim_ledger.md::R15` — stated in prose only (refuted. A third one-term build for an obstructed `xrx`; a one-term build asserting `xrt` and `trx` both, or copying an assertion of `x` Evidence: D10 (paper §4; `is_build_of`, enumeration in `tests/test_fourth_changes.py`))
- `H3V7N5QF:paper/fourth/claim_ledger.md::N3` — stated in prose only (do not follow (computed witnesses). Never both ways; passing on; every term first; always both ways (from the beginning without `bra`) Evidence: `follows_*.csv`)
- `H3V7N5QF:paper/fourth/claim_ledger.md::N4` — stated in prose only (does not follow (computed witnesses: what is given; add a term). Exactly two terms Evidence: `follows_*.csv`)
- `H3V7N5QF:paper/fourth/claim_ledger.md::N5` — stated in prose only (does not follow (derived from D9). Any statement about the asserting that holds in one legal state containing what is given and fails in another Evidence: D9)
- `H3V7N5QF:paper/fourth/claim_ledger.md::N6` — stated in prose only (does not follow (derived from D3, D7, D10). Which answer an obstructed change gets Evidence: as cited)
- `H3V7N5QF:paper/fourth/claim_ledger.md::N7` — stated in prose only (does not follow (witnesses: what is given; a result one change away of each kind). Growth: that terms, or assertions, must be added Evidence: `added_*.csv`)
- `H3V7N5QF:paper/fourth/claim_ledger.md::N8` — stated in prose only (does not follow (computed witnesses: `a b c; arb`, `a b; arb bra`, `a b; arb(2)`, round 1, none contains another). That any two results are comparable (one reaches the other) Evidence: `reach_bound3_rounds6_anchored_without_bra.csv`)
- `H3V7N5QF:paper/fourth/claim_ledger.md::N10` — stated in prose only (does not follow (D3: `1 + n²`; 10 for `a b c; arb`, 5 for `a b; arb bra`); for results with equally many terms it does follow. That results of one round have equally many attempts Evidence: column `changes` of `results_*.csv`)
- `H3V7N5QF:paper/fourth/claim_ledger.md::N12` — stated in prose only (do not follow (computed witnesses: what is given and `a b; arb bra` hold, `a b; arb(2) bra` fails). That all asserted assertions are asserted equally often; that `xry` and `yrx`, when both asserted, are asserted equally often Evidence: `follows_*.csv` (`same_multiplicity`, `both_ways_equal`))
- `H3V7N5QF:paper/nineteenth/claim_ledger.md::N1` — stated in prose only (given. The changed sentence, and the rest of the base seed Evidence: `prompt/nineteenth/seed_prompt.md`)
- `H3V7N5QF:paper/nineteenth/claim_ledger.md::N2` — stated in prose only (chosen. P1: one pair that mentions at least one of the two terms; the terms stay; an unchanged pair is not a change; a loop is refused Evidence: `code/nineteenth/changes.py`)
- `H3V7N5QF:paper/nineteenth/claim_ledger.md::N3` — stated in prose only (chosen + computed. P2, only a pair naming both terms, is kept and reaches the same results while performing none Evidence: `evidence/nineteenth/summary.json` (`cooccur_performed` 0, equal closures))
- `H3V7N5QF:paper/nineteenth/claim_ledger.md::N4` — stated in prose only (derived. Rewriting one pair leaves the terms Evidence: `performPartial_terms`)
- `H3V7N5QF:paper/nineteenth/claim_ledger.md::N5` — stated in prose only (derived. A pair naming both terms becomes a loop Evidence: `cooccur_is_loop`)
- `H3V7N5QF:paper/nineteenth/claim_ledger.md::N6` — stated in prose only (derived. A one-sided rewrite can be legal, and it is not the base identification Evidence: `side_partial_eq`, `side_partial_legal`, `side_not_identify`)
- `H3V7N5QF:paper/nineteenth/claim_ledger.md::N7` — stated in prose only (derived. The base identification of what is given has fewer terms Evidence: `identify_smaller`)
- `H3V7N5QF:paper/nineteenth/claim_ledger.md::N8` — stated in prose only (derived. No sequence of these changes reaches the one-term state Evidence: `PStep.card_ge`, `PReach.card_ge`, `oneTerm_unreachable`)
- `H3V7N5QF:paper/nineteenth/claim_ledger.md::N11` — stated in prose only (refuted. Global identification is recovered by iterating partial ones Evidence: N8, N9)
- `H3V7N5QF:paper/nineteenth/claim_ledger.md::N12` — stated in prose only (derived. Adding a term is never obstructed, so there is no last result Evidence: base `addTerm_legal`; the frontier counts in N9)
- `H3V7N5QF:paper/nineteenth/claim_ledger.md::N13` — stated in prose only (derived. No sequence that adds a fourth term returns inside the bound, so the closure inside 3 terms is every result with at most 3 terms Evidence: `PStep.card_ge`, `PReach.card_ge` (over a superset of the seed's changes))
- `H3V7N5QF:paper/ninth/claim_ledger.md::D10` — stated in prose only (derived (paper §4) + computed. Within the bound the exploration is complete; the independent count with the empty state added certifies it; the count is not the product of the seventh's for `n ≥ 2` and is for `n ≤ 1`; the frontier is one entry per result at the bound; th... Evidence: `code/ninth/orbits.py`; `summary.json` (`explored_equals_independent_count`, `count_exceeds_product_for_two_or_more_terms`, `product_equals_count_for_at_most_one_term`, `frontier_entries_are_1_per_state_with_N_terms`, `results_with_exact_sequence_count = results`, `rounds_agreeing_with_unbounded_formula` all true), `counts.csv`, `tests/test_ninth_orbits.py`)
- `H3V7N5QF:paper/ninth/claim_ledger.md::D11` — stated in prose only (derived (paper §4) + computed. With at most two terms the results of round `r` are `[r = 0] + [r ≥ 1]·r + [r ≥ 2]·(C(r+5, 7) + [r even]·C(r/2+2, 3))/2`; one-term results asserting `ara` `p` times and `asa` `q` times have `C(p + q, p)` shortest sequences; the results with... Evidence: `code/ninth/orbits.py` (`two_term_count`, `two_term_round_count`, `one_term_sequences`, `agreeing_count`), `summary.json` (`two_term_rounds_equal_closed_form` true on all 12 rounds, `two_term_closed_form_mismatches` empty, `one_term_results_follow_the_binomial`, `relations_agreeing_equal_closed_form` true), `tests/test_ninth_orbits.py`)
- `H3V7N5QF:paper/ninth/claim_ledger.md::D14` — stated in prose only (derived (from D5) + computed. No statement about the asserting holds in every result; the eighth's "at least one term" fails at round 0 Evidence: `follows_*.csv`, `summary.json` (`statements_holding_in_every_result` empty in every run))
- `H3V7N5QF:paper/ninth/claim_ledger.md::D15` — stated in prose only (derived (paper §4). The unchosen reading of identification (the larger of the two, per relation) gives the same results, reachability and cost Evidence: paper §4 D15)
- `H3V7N5QF:paper/ninth/claim_ledger.md::R1` — stated in prose only (refuted. A change other than adding a term on the empty state Evidence: D1 (`first_change_adds_term9`))
- `H3V7N5QF:paper/ninth/claim_ledger.md::R2` — stated in prose only (refuted. Reaching the empty state from a state with a term; a non-empty sequence from the empty state to itself Evidence: D2 (`empty9_never_returned`, `no_cycle_at_empty9`))
- `H3V7N5QF:paper/ninth/claim_ledger.md::R3` — stated in prose only (refuted. A sequence of changes to a result shorter than its size Evidence: D4 (`fewest_changes9_lower`))
- `H3V7N5QF:paper/ninth/claim_ledger.md::R4` — stated in prose only (refuted. A well-formed two-relation state that is not a result; a pair of well-formed parts on the same terms that is not Evidence: D5 (`result9_iff`, `results_pair9`))
- `H3V7N5QF:paper/ninth/claim_ledger.md::R5` — stated in prose only (refuted. A change that keeps the size, or the round, where it was Evidence: D4(v) (`Step9.size_step`, `Reach9.size_parity`; `changes_keeping_the_round: 0`))
- `H3V7N5QF:paper/ninth/claim_ledger.md::R6` — stated in prose only (refuted. A shortest sequence containing a removal or an identification Evidence: D4(vi) (`shortest_are_additions9`))
- `H3V7N5QF:paper/ninth/claim_ledger.md::R7` — stated in prose only (refuted. Two results with a term that do not reach each other; two results neither of which reaches the other Evidence: D9 (`reach9_symm`, `reach9_total`))
- `H3V7N5QF:paper/ninth/claim_ledger.md::R8` — stated in prose only (refuted. A rewriting barred by the names: the two readings of sameness differing Evidence: D12)
- `H3V7N5QF:paper/ninth/claim_ledger.md::R9` — stated in prose only (refuted. The eighth's cost as the fewest changes here Evidence: D13 (`eighth_cost_fails`))
- `H3V7N5QF:paper/ninth/claim_ledger.md::R10` — stated in prose only (refuted. A result reached by no sequence; a result with no shortest sequence Evidence: D5, D10 (`reach9_by_additions`; every count ≥ 1))
- `H3V7N5QF:paper/ninth/claim_ledger.md::R11` — stated in prose only (refuted. The cost as the sum of the two parts' seventh costs, on a state with a term Evidence: D4 (`cost_not_sum_of_parts9`, `one_term_parts9`))
- `H3V7N5QF:paper/ninth/claim_ledger.md::R12` — stated in prose only (refuted. The count of results as the product of the single-relation counts, for two or more terms Evidence: D10 (`count_exceeds_product_for_two_or_more_terms`; 20 against 16, 8 against 4))
- `H3V7N5QF:paper/ninth/claim_ledger.md::N1` — stated in prose only (do not follow (derived from D5; computed witnesses). Anything about the asserting, in either relation or jointly, "at least one term" included (forty-two statements tested) Evidence: `follows_*.csv`, `summary.json` (`statements_that_do_not_follow`))
- `H3V7N5QF:paper/ninth/claim_ledger.md::N2` — stated in prose only (do not follow (computed witnesses: rounds 0, 1, 2, 3). That there is a term; exactly two; at least two Evidence: `follows_*.csv`)
- `H3V7N5QF:paper/ninth/claim_ledger.md::N3` — stated in prose only (does not follow (derived: D5, `results_pair9`; computed witnesses on one term). That the `s` part determines anything about the `r` part, or the converse Evidence: `results_*.csv`)
- `H3V7N5QF:paper/ninth/claim_ledger.md::N5` — stated in prose only (does not follow (D3: 3 for `a; nothing asserted`, 5 for `a; ara asa`). That results of one round with equally many terms have equally many changes Evidence: column `changes` of `results_*.csv`)
- `H3V7N5QF:paper/ninth/claim_ledger.md::N6` — stated in prose only (refuted (witnesses; `changes_lowering` in every run). That a multiplicity, the number of terms, either total, the size or the fewest classes in either relation never falls; that no `xrx`, or no `xsx`, stays asserted Evidence: `summary.json`; `tests/test_ninth_follows_invariants.py`)
- `H3V7N5QF:paper/ninth/claim_ledger.md::N8` — stated in prose only (without object. The eighth's notions of `bra`, the names, the given assertion and the destroyed givens Evidence: —)
- `H3V7N5QF:paper/ninth/claim_ledger.md::N12` — stated in prose only (refuted for `n ≥ 2`, holds for `n ≤ 1` (D10). That the number of results with `n` terms is the product of the seventh's single-relation counts Evidence: `counts.csv`, `summary.json`)
- `H3V7N5QF:paper/second/claim_ledger.md::D14` — stated in prose only (derived + computed. Within the bound the exploration is complete, rounds equal fewest changes without bound, and the frontier is exact Evidence: paper §4; `summary.json` (`explored_equals_independent_count`, `rounds_agreeing_with_unbounded_formula`, `frontier_entries_are_1_plus_2N_per_state_with_N_terms`), `evidence/second/frontier_*.csv`, `counts.csv`)
- `H3V7N5QF:paper/second/claim_ledger.md::R1` — stated in prose only (refuted. `a` and `b` are one term to begin with Evidence: D1)
- `H3V7N5QF:paper/second/claim_ledger.md::R2` — stated in prose only (refuted. Some answer makes adding `xrx` performable Evidence: D4)
- `H3V7N5QF:paper/second/claim_ledger.md::R3` — stated in prose only (refuted. The obstruction of some obstructed change can be removed; some change has the outcome of a removal Evidence: D7 (`Reach3.identify_images_obstructed`, `Step3.ne_remove`, `removal_answer_outcome_unreachable`), D4)
- `H3V7N5QF:paper/second/claim_ledger.md::R4` — stated in prose only (refuted. Some sequence of changes reaches a state with fewer than two terms Evidence: D6 (`reach3_givenA_two_terms`, `reach3_givenB_two_terms`, `oneTerm_unreachable_A`, `oneTerm_unreachable_B`))
- `H3V7N5QF:paper/second/claim_ledger.md::R5` — stated in prose only (refuted. Some sequence of changes identifies `a` and `b`, or un-asserts `arb` Evidence: D6 (`Reach3.names_apart`, `Reach3.arb_persists`))
- `H3V7N5QF:paper/second/claim_ledger.md::R6` — stated in prose only (refuted. Some answer, or some identification, reaches a result that additions do not reach Evidence: D10)
- `H3V7N5QF:paper/second/claim_ledger.md::R7` — stated in prose only (refuted. `bra` is asserted and asserting passes on; with `bra` given, some result passes on Evidence: D15 (`passing_on_refutes_bra`, `Reach3.bra_persists`))
- `H3V7N5QF:paper/second/claim_ledger.md::R8` — stated in prose only (refuted. The beginning with `bra` reaches the beginning without Evidence: D2 (`givenB_never_givenA`))
- `H3V7N5QF:paper/second/claim_ledger.md::R9` — stated in prose only (refuted. Some result does not contain what is given (1:D9 under this seed) Evidence: D9 (`reach3_givenA_contains`, `result_iff_A`))
- `H3V7N5QF:paper/second/claim_ledger.md::R10` — stated in prose only (refuted. Some result is reached in fewer changes than its size difference, or has fewer terms or assertions than what is given Evidence: D8, D6; `additions_never_negative`)
- `H3V7N5QF:paper/second/claim_ledger.md::R11` — stated in prose only (refuted. Some change lowers the fewest classes of a split Evidence: D13)
- `H3V7N5QF:paper/second/claim_ledger.md::N3` — stated in prose only (do not follow (computed witnesses). Never both ways; passing on; every term first; always both ways (from the beginning without `bra`; the first two are refuted in every result of the beginning with `bra`, D15) Evidence: `evidence/second/follows_*.csv`)
- `H3V7N5QF:paper/second/claim_ledger.md::N4` — stated in prose only (does not follow (computed witnesses: what is given; add a term). Exactly two terms (the other three items of 1:N4 now follow, D6) Evidence: `evidence/second/follows_*.csv`)
- `H3V7N5QF:paper/second/claim_ledger.md::N5` — stated in prose only (does not follow (derived from D9). Any statement about the asserting that holds in one legal state containing what is given and fails in another Evidence: D9)
- `H3V7N5QF:paper/second/claim_ledger.md::N6` — stated in prose only (does not follow (derived from D3, D7, D10). Which answer an obstructed change gets (refuse or build; removal never) Evidence: as cited)
- `H3V7N5QF:paper/second/claim_ledger.md::N7` — stated in prose only (does not follow (witnesses: what is given, a result one change away). Growth: that terms must be added Evidence: `evidence/second/added_*.csv`)
- `H3V7N5QF:paper/second/claim_ledger.md::N8` — stated in prose only (does not follow (computed witnesses). That the number of terms, of assertions, or the size never decreases Evidence: `evidence/second/attempts_bound3_anchored_without_bra.jsonl` (state `3:01:0-1`, "identify a and c", outcome `2:01:0-1`); paper §5)
- `H3V7N5QF:paper/second/claim_ledger.md::N9` — stated in prose only (do not follow (witness of N8; R8; `results_that_reach_what_is_given`). That a result once left is never returned to; that every result returns to what is given Evidence: `summary.json`, `results_*.csv`)
- `H3V7N5QF:paper/second/claim_ledger.md::N10` — stated in prose only (do not follow (computed: K7). That reachability among results is symmetric, or antisymmetric Evidence: `evidence/second/reach_bound3_*.csv`)
- `H3V7N5QF:paper/seventeenth/claim_ledger.md::D10` — stated in prose only (derived. Adding a term is never M1-obstructed, and the outcome has a new term, so there is no last round Evidence: paper §4, from the `addTerm` clause of `Step17.obstructedM1` (it is `False`) and `St.addTerm` (the term is new))
- `H3V7N5QF:paper/seventeenth/claim_ledger.md::R1` — stated in prose only (refuted. The struck sentence is still a given Evidence: G4)
- `H3V7N5QF:paper/seventeenth/claim_ledger.md::R2` — stated in prose only (refuted. Every result asserts no `xrx` Evidence: D6 (`mergedA_hasXrx`); it holds of A-replace results (D3))
- `H3V7N5QF:paper/seventeenth/claim_ledger.md::R3` — stated in prose only (refuted. A-replace and A-perform have the same results Evidence: D6 (`add_ara_not_unobstructed`); K1)
- `H3V7N5QF:paper/seventeenth/claim_ledger.md::R4` — stated in prose only (refuted. M1 and M2 disagree on some loop-free state Evidence: D1)
- `H3V7N5QF:paper/seventeenth/claim_ledger.md::R5` — stated in prose only (refuted. The base cost lower-bounds A-perform Evidence: D6)
- `H3V7N5QF:paper/seventeenth/claim_ledger.md::N2` — stated in prose only (does not follow. `a` and `b` are two terms in every result, and they are one term to begin with Evidence: they are two in the chosen beginning; they are one after the identification (D6, D8))
- `H3V7N5QF:paper/seventh/claim_ledger.md::D3` — stated in prose only (derived + computed. A result with `n` terms and `d` asserted pairs (diagonal included) has `C(n, 2) + d + 1 + n²` changes, `1 + n²` of them additions; on a result asserting no `xrx`, `n` plus the related pairs make some `xrx` asserted Evidence: `code/seventh/changes.py`, `tests/test_seventh_changes.py` (against the list); `summary.json` (`attempts_equal_formula`, `xrx_making_equal_sixth_formula` true in every run))
- `H3V7N5QF:paper/seventh/claim_ledger.md::D10` — stated in prose only (derived (paper §4) + computed. Within the bound the exploration is complete; the independent count with the empty state added certifies it; the frontier is one entry per result at the bound; the shortest-sequence counts are exact for every result; rounds `0 … N` agree wi... Evidence: `code/seventh/orbits.py`; `summary.json` (`explored_equals_independent_count`, `frontier_entries_are_1_per_state_with_N_terms`, `results_with_exact_sequence_count = results`, `rounds_agreeing_with_unbounded_formula` all true), `counts.csv`, `tests/test_seventh_orbits.py` (counts against listing every writing))
- `H3V7N5QF:paper/seventh/claim_ledger.md::D11` — stated in prose only (derived (paper §4) + computed. With at most two terms the results of round `r` are `[r = 0] + [r ≥ 1] + [r ≥ 2]·(C(r+1, 3) + [r even]·r/2)/2`, cubic; one-term results have one shortest sequence Evidence: `code/seventh/orbits.py` (`two_term_count`, `two_term_round_count`), `summary.json` (`two_term_rounds_equal_closed_form` true on all 40 rounds, `two_term_closed_form_mismatches` empty, `one_term_results_have_one_shortest_sequence` true), `tests/test_seventh_orbits.py`)
- `H3V7N5QF:paper/seventh/claim_ledger.md::D12` — stated in prose only (derived (paper §4) + computed. The two readings of sameness coincide: with no names every rewriting keeps the names Evidence: paper §4; `summary.json` (`sixth_results_names_forgotten` = `sixth_results_any_rewriting` in every run))
- `H3V7N5QF:paper/seventh/claim_ledger.md::D14` — stated in prose only (derived (from D5) + computed. No statement about the asserting holds in every result; the sixth's "at least one term" fails at round 0 Evidence: `follows_*.csv`, `summary.json` (`statements_holding_in_every_result` empty in every run))
- `H3V7N5QF:paper/seventh/claim_ledger.md::D15` — stated in prose only (derived (paper §4). The unchosen reading of identification (the larger of the two) gives the same results, reachability and cost Evidence: paper §4 D15)
- `H3V7N5QF:paper/seventh/claim_ledger.md::R1` — stated in prose only (refuted. A change other than adding a term on the empty state Evidence: D1 (`first_change_adds_term`))
- `H3V7N5QF:paper/seventh/claim_ledger.md::R2` — stated in prose only (refuted. Reaching the empty state from a state with a term; a non-empty sequence from the empty state to itself Evidence: D2 (`empty_never_returned`, `no_cycle_at_empty`))
- `H3V7N5QF:paper/seventh/claim_ledger.md::R3` — stated in prose only (refuted. A sequence of changes to a result shorter than its size Evidence: D4 (`fewest_changes7_lower`))
- `H3V7N5QF:paper/seventh/claim_ledger.md::R4` — stated in prose only (refuted. A well-formed state that is not a result Evidence: D5 (`result7_iff`))
- `H3V7N5QF:paper/seventh/claim_ledger.md::R5` — stated in prose only (refuted. A change that keeps the size, or the round, where it was Evidence: D4(v) (`Step7.size_step`, `Reach7.size_parity`; `changes_keeping_the_round: 0`))
- `H3V7N5QF:paper/seventh/claim_ledger.md::R6` — stated in prose only (refuted. A shortest sequence containing a removal or an identification Evidence: D4(vi) (`shortest_are_additions`))
- `H3V7N5QF:paper/seventh/claim_ledger.md::R7` — stated in prose only (refuted. Two results with a term that do not reach each other; two results neither of which reaches the other Evidence: D9 (`reach7_symm`, `reach7_total`))
- `H3V7N5QF:paper/seventh/claim_ledger.md::R8` — stated in prose only (refuted. A rewriting barred by the names: the two readings of sameness differing Evidence: D12)
- `H3V7N5QF:paper/seventh/claim_ledger.md::R9` — stated in prose only (refuted. The sixth's cost as the fewest changes here Evidence: D13 (`sixth_cost_fails`))
- `H3V7N5QF:paper/seventh/claim_ledger.md::R10` — stated in prose only (refuted. A result reached by no sequence; a result with no shortest sequence Evidence: D5, D10 (`reach7_by_additions`; every count ≥ 1))
- `H3V7N5QF:paper/seventh/claim_ledger.md::N1` — stated in prose only (do not follow (derived from D5; computed witnesses). Anything about the asserting: every one of the eighteen statements tested, "at least one term" included Evidence: `follows_*.csv`, `summary.json` (`statements_that_do_not_follow`))
- `H3V7N5QF:paper/seventh/claim_ledger.md::N2` — stated in prose only (do not follow (computed witnesses: rounds 0, 1, 2, 3). That there is a term; exactly two; at least two Evidence: `follows_*.csv`)
- `H3V7N5QF:paper/seventh/claim_ledger.md::N3` — stated in prose only (does not follow (witnesses: the empty state; one change each way from every result with a term). Growth: that terms, or assertions, must be added or must stay Evidence: `added_*.csv`, `summary.json` (`changes_lowering`))
- `H3V7N5QF:paper/seventh/claim_ledger.md::N5` — stated in prose only (does not follow (D3: 6 for `a b; nothing asserted`, 7 for `a b; bra`). That results of one round with equally many terms have equally many changes Evidence: column `changes` of `results_*.csv`)
- `H3V7N5QF:paper/seventh/claim_ledger.md::N6` — stated in prose only (refuted (witnesses; 29 602 / 42 563 / 29 602 / 72 165 / 1 161 / 12 783 changes in the 5-term run). That a multiplicity, the number of terms, the total, the size or the fewest classes never falls; that no `xrx` stays asserted Evidence: `summary.json` (`changes_lowering`); `tests/test_seventh_follows_invariants.py`)
- `H3V7N5QF:paper/seventh/claim_ledger.md::N7` — stated in prose only (refuted (witness: `a; ara` and its removal). That a state is contained in its outcome; that a sequence carries every assertion somewhere Evidence: `attempts_bound2_rounds4.jsonl`)
- `H3V7N5QF:paper/seventh/claim_ledger.md::N8` — stated in prose only (without object. The sixth's notions of `bra`, the names, the given assertion and the destroyed givens Evidence: —)
- `H3V7N5QF:paper/sixteenth/claim_ledger.md::R1` — stated in prose only (refuted. A change other than adding a term on the empty state Evidence: D13 (`first_change_adds_term16`))
- `H3V7N5QF:paper/sixteenth/claim_ledger.md::R2` — stated in prose only (refuted. Reaching the empty state from a state with a term Evidence: D13 (`reach16_empty_iff`))
- `H3V7N5QF:paper/sixteenth/claim_ledger.md::R3` — stated in prose only (refuted. A sequence to a result shorter than its potential; a shortest sequence with an admission Evidence: D3, D4 (`fewest_changes16_lower`, `no_fall_on_shortest16`))
- `H3V7N5QF:paper/sixteenth/claim_ledger.md::R4` — stated in prose only (refuted. A well-formed state that is not a result Evidence: D8 (`result16_iff`))
- `H3V7N5QF:paper/sixteenth/claim_ledger.md::R5` — stated in prose only (refuted. A change that keeps the potential Evidence: D3 (`Step16.potential_step`))
- `H3V7N5QF:paper/sixteenth/claim_ledger.md::R6` — stated in prose only (refuted. The size as the fewest changes off the empty-record results Evidence: D3 (`ninth_cost_fails_off_empty_record`))
- `H3V7N5QF:paper/sixteenth/claim_ledger.md::R7` — stated in prose only (refuted. The has-a-term criterion; mutual reachability among the states with a term Evidence: D5 (`has_term_criterion_fails16`, `one_way16`))
- `H3V7N5QF:paper/sixteenth/claim_ledger.md::R8` — stated in prose only (refuted. The ninth's add-then-remove as a cycle; a bound on the feedback Evidence: D9 (`add_remove_ne`, `admit_remove_unbounded`))
- `H3V7N5QF:paper/sixteenth/claim_ledger.md::R9` — stated in prose only (refuted. The count as the ninth's count times the record's, from two terms on Evidence: D8 (`count_exceeds_product_for_two_or_more_terms`))
- `H3V7N5QF:paper/sixteenth/claim_ledger.md::R10` — stated in prose only (refuted. Clearing a leftover is not one of the four kinds Evidence: D10 (`clearing_is_a_kind16`))
- `H3V7N5QF:paper/sixteenth/claim_ledger.md::R11` — stated in prose only (refuted. An admission raises the record, or a direct addition changes it Evidence: D10 (`record_moved_only_by_removal_and_admission`))
- `H3V7N5QF:paper/sixteenth/claim_ledger.md::N1` — stated in prose only (do not follow (computed witnesses). Anything about the asserting (forty-two ninth statements read on the ninth state) or about the record (empty; something recorded; a recorded pair asserted; every recorded pair unasserted) Evidence: `follows_*.csv`)
- `H3V7N5QF:paper/sixteenth/claim_ledger.md::N2` — stated in prose only (do not follow (computed witnesses). That a change leaves nothing, a pair, a merge, an admissible writing, or is an admission Evidence: `change_statements_that_do_not_follow`)
- `H3V7N5QF:paper/sixteenth/claim_ledger.md::N3` — stated in prose only (refuted (4 227 pairs). That the two mass invariants decide reachability Evidence: `summary.json` (`ordered_pairs_the_two_mass_invariants_admit_and_the_criterion_refuses`))
- `H3V7N5QF:paper/sixth/claim_ledger.md::D14` — stated in prose only (derived (paper §4) + computed. Within the bound the exploration is complete; the independent count with the diagonal pairs certifies it; the frontier is one entry per result at the bound; the shortest-sequence counts are exact where said (ANCHORED: fewer terms than the b... Evidence: `code/sixth/orbits.py`; `summary.json` (`explored_equals_independent_count`, `frontier_entries_are_1_per_state_with_N_terms`, `rounds_agreeing_with_unbounded_formula`, `results_with_exact_sequence_count`), `counts.csv`, `tests/test_sixth_orbits.py` (counts against listing every writing, with and without the cap))
- `H3V7N5QF:paper/sixth/claim_ledger.md::D17` — stated in prose only (derived (paper §4) + computed. Two terms, names kept: the results of round `r` are `C(r+3,3) + C(r+1,2) + C(r+1,3) + C(r−1,2) + one(r)` (no `bra`) and the corresponding form with `bra`; the shortest sequences to a result with the names apart are a multinomial coefficient Evidence: `code/sixth/evidence.py` (`two_term_round_count`, `_two_term_multinomial`), `summary.json` (`two_term_rounds_equal_closed_form`, `two_term_sequences_equal_multinomial` true on all rounds of both ANCHORED runs), `rounds_bound2_rounds20_*.csv`, `tests/test_sixth_explore.py::test_two_terms_all_rounds`)
- `H3V7N5QF:paper/sixth/claim_ledger.md::D18` — stated in prose only (derived + computed. Every state has a two-change cycle; no change keeps the round; the two ANCHORED explorations do not correspond round by round Evidence: D13, D8(v); `summary.json` (`results` 63 362 / 76 905))
- `H3V7N5QF:paper/sixth/claim_ledger.md::D19` — stated in prose only (derived (paper §4). The unchosen reading of identification (the larger of the two) gives the same results and reachability, the same cost without `bra`, and a different cost with `bra` given Evidence: paper §4 D19 (witness: `a b; arb bra` identified gives `ara(2)` in one change under the sum reading, `ara` under the other))
- `H3V7N5QF:paper/sixth/claim_ledger.md::R1` — stated in prose only (refuted. `a` and `b` one term to begin with Evidence: D1 (`names_apart_of_legal` on the given state))
- `H3V7N5QF:paper/sixth/claim_ledger.md::R2` — stated in prose only (refuted. An attempt that is refused, or obstructed Evidence: D3 (`try5_iff_step6`))
- `H3V7N5QF:paper/sixth/claim_ledger.md::R5` — stated in prose only (refuted. Telling `a` and `b` apart again after identifying them; reaching what is given from a one-term state Evidence: D7)
- `H3V7N5QF:paper/sixth/claim_ledger.md::R7` — stated in prose only (refuted. `bra` together with passing on in a state asserting no `xrx` Evidence: D15 (`passing_on_refutes_bra`))
- `H3V7N5QF:paper/sixth/claim_ledger.md::R8` — stated in prose only (refuted. A sequence of changes to a result shorter than its cost Evidence: D8 (`fewest_changes6_lower_A`, `_B`))
- `H3V7N5QF:paper/sixth/claim_ledger.md::R9` — stated in prose only (refuted. A well-formed state with at least one term that is not a result Evidence: D9)
- `H3V7N5QF:paper/sixth/claim_ledger.md::R10` — stated in prose only (refuted. A change that keeps the cost, or the round, where it was Evidence: D8(v) (`Reach6.size_parity`; `changes_keeping_the_round: 0`))
- `H3V7N5QF:paper/sixth/claim_ledger.md::R12` — stated in prose only (refuted. Two results with the names apart that do not reach each other; two results neither of which reaches the other Evidence: D13 (`reach6_symm`, `reach6_total`))
- `H3V7N5QF:paper/sixth/claim_ledger.md::R13` — stated in prose only (refuted. An attempt not performed Evidence: D3; `given.json` (`attempts_not_performed: 0`))
- `H3V7N5QF:paper/sixth/claim_ledger.md::R14` — stated in prose only (refuted. The fifth's potential as a lower bound on every result Evidence: D8 (`fifth_potential_fails`, `cost_loopState`))
- `H3V7N5QF:paper/sixth/claim_ledger.md::R15` — stated in prose only (refuted. "Removing the obstruction first or identifying first and lowering `uru` last give the same state" on every state Evidence: D5 (`first_or_last_fails`))
- `H3V7N5QF:paper/sixth/claim_ledger.md::N3` — stated in prose only (do not follow (derived from D9; computed witnesses). Any statement about the asserting other than "at least one term" (twenty-two tested), "no `xrx`" included Evidence: `follows_*.csv`, `summary.json` (`statements_that_do_not_follow`))
- `H3V7N5QF:paper/sixth/claim_ledger.md::N4` — stated in prose only (does not follow (computed witnesses: what is given; add a term; identify `a`, `b`). Exactly two terms Evidence: `follows_*.csv`)
- `H3V7N5QF:paper/sixth/claim_ledger.md::N5` — stated in prose only (do not follow (computed witnesses, first failing rounds 1, 1, 1, 1). That what is given survives: `arb` asserted; `a`, `b` two terms; something asserted; no `xrx` Evidence: `follows_*.csv`)
- `H3V7N5QF:paper/sixth/claim_ledger.md::N6` — stated in prose only (without object (D3, D10). Which answer an obstructed change gets Evidence: —)
- `H3V7N5QF:paper/sixth/claim_ledger.md::N7` — stated in prose only (does not follow (witnesses: what is given; one change each way). Growth: that terms, or assertions, must be added or must stay Evidence: `added_*.csv`)
- `H3V7N5QF:paper/sixth/claim_ledger.md::N9` — stated in prose only (does not follow (D3: 6 for `a b; nothing asserted`, 8 for `a b; arb ara`). That results of one round with equally many terms have equally many attempts Evidence: column `changes` of `results_*.csv`)
- `H3V7N5QF:paper/sixth/claim_ledger.md::N10` — stated in prose only (do not follow (computed witnesses). Nothing twice; `arb` once; all asserted equally often; both ways equally often Evidence: `follows_*.csv`)
- `H3V7N5QF:paper/sixth/claim_ledger.md::N11` — stated in prose only (does not follow (derived D9; computed: the same lists). That the two beginnings differ in what they reach or in which statements are independent Evidence: `summary.json`)
- `H3V7N5QF:paper/sixth/claim_ledger.md::N13` — stated in prose only (refuted (witnesses; 96 533 / 82 349 / 178 882 / 3 730 / 35 372 changes in the ANCHORED 4-term run). That a multiplicity, the number of terms, the total, the size or the fewest classes never falls; that no `xrx` stays asserted Evidence: `summary.json` (`changes_lowering`); `tests/test_sixth_follows_invariants.py`)
- `H3V7N5QF:paper/tenth/claim_ledger.md::D10` — stated in prose only (derived (identity) + computed. C-L1 results, rounds, sequences and count are the ninth's; count not a product for `n ≥ 2` Evidence: the C-L1 exploration *is* the ninth's (`tenth.explore.explore` wraps `ninth.explore.explore`), so `same_results`, the round and the sequence comparisons in `compare_with_ninth` agree by construction and show only determinism; the one independent check is `explored_equals_independent_count` (the ninth's orbit count, `ninth.orbits.count_results`), true in every run; 9:D10 for the non-product)
- `H3V7N5QF:paper/third/claim_ledger.md::D14` — stated in prose only (derived + computed. Within the bound the exploration is complete, rounds equal the length of every sequence without bound, the frontier is exact, and the number of sequences per result is exact Evidence: paper §4; `summary.json` (`explored_equals_independent_count`, `rounds_agreeing_with_unbounded_formula`, `frontier_entries_are_1_plus_2N_per_state_with_N_terms`), `evidence/third/frontier_*.csv`, `counts.csv`)
- `H3V7N5QF:paper/third/claim_ledger.md::R1` — stated in prose only (refuted. `a` and `b` are one term to begin with Evidence: D1)
- `H3V7N5QF:paper/third/claim_ledger.md::R2` — stated in prose only (refuted. Some answer makes adding `xrx` performable Evidence: D4 (`Reach2.xrx_still_obstructed`))
- `H3V7N5QF:paper/third/claim_ledger.md::R3` — stated in prose only (refuted. The obstruction of some obstructed change can be removed; some change has the outcome of a removal or of an identification Evidence: D7 (`no_change_asserts_xrx`, `xrx_outcome_unreachable`, `Step2.ne_remove`, `Step2.ne_identify`), D4)
- `H3V7N5QF:paper/third/claim_ledger.md::R4` — stated in prose only (refuted. Some sequence of changes reaches a state with fewer than two terms Evidence: D6 (`reach2_givenA_two_terms`, `reach2_givenB_two_terms`, `oneTerm_unreachable2_A`, `oneTerm_unreachable2_B`))
- `H3V7N5QF:paper/third/claim_ledger.md::R5` — stated in prose only (refuted. Some sequence of changes identifies `a` and `b`, or un-asserts `arb` Evidence: D6 (`Reach2.names_apart`, `Reach2.arb_persists`))
- `H3V7N5QF:paper/third/claim_ledger.md::R6` — stated in prose only (refuted. Some answer reaches a result that additions do not reach Evidence: D10)
- `H3V7N5QF:paper/third/claim_ledger.md::R7` — stated in prose only (refuted. `bra` is asserted and asserting passes on; with `bra` given, some result passes on Evidence: D15 (`passing_on_refutes_bra`, `Reach2.bra_persists`))
- `H3V7N5QF:paper/third/claim_ledger.md::R8` — stated in prose only (refuted. The beginning with `bra` reaches the beginning without Evidence: D2 (`givenB_never_givenA2`))
- `H3V7N5QF:paper/third/claim_ledger.md::R9` — stated in prose only (refuted. Some result does not contain what is given Evidence: D9 (`reach2_givenA_contains`, `result2_iff_A`))
- `H3V7N5QF:paper/third/claim_ledger.md::R10` — stated in prose only (refuted. Some sequence of changes reaches a result in fewer, or in more, changes than its size difference Evidence: D8 (`Reach2.length_unique`, `fewest_changes2_lower_A/B`))
- `H3V7N5QF:paper/third/claim_ledger.md::R11` — stated in prose only (refuted. Some change lowers the fewest classes of a split Evidence: D13 (`Reach2.split_mono`))
- `H3V7N5QF:paper/third/claim_ledger.md::R12` — stated in prose only (refuted. Some change lowers the number of terms or of assertions, leaves the size unchanged, or raises it by more than one Evidence: D6 (`Reach2.card_T_le`, `Reach2.card_A_le`), D8 (`Step2.size_eq`); `counts_lowered_by` empty)
- `H3V7N5QF:paper/third/claim_ledger.md::R13` — stated in prose only (refuted. Some result is returned to after being left; some result other than what is given reaches what is given Evidence: D13 (`Reach2.no_return`, `Reach2.antisymm`); `results_that_reach_what_is_given: 1`)
- `H3V7N5QF:paper/third/claim_ledger.md::R14` — stated in prose only (refuted. Two different results reach each other Evidence: D13 (`Reach2.antisymm`, `reach2_antisymm_writing`); `unordered_pairs_reachable_both_ways: 0`)
- `H3V7N5QF:paper/third/claim_ledger.md::N3` — stated in prose only (do not follow (computed witnesses). Never both ways; passing on; every term first; always both ways (from the beginning without `bra`; the first two are refuted in every result of the beginning with `bra`, D15) Evidence: `evidence/third/follows_*.csv`)
- `H3V7N5QF:paper/third/claim_ledger.md::N4` — stated in prose only (does not follow (computed witnesses: what is given; add a term). Exactly two terms Evidence: `evidence/third/follows_*.csv`)
- `H3V7N5QF:paper/third/claim_ledger.md::N5` — stated in prose only (does not follow (derived from D9). Any statement about the asserting that holds in one legal state containing what is given and fails in another Evidence: D9)
- `H3V7N5QF:paper/third/claim_ledger.md::N6` — stated in prose only (does not follow (derived from D3, D7, D10). Which answer an obstructed change gets (refuse or build; removal never, or refusal) Evidence: as cited)
- `H3V7N5QF:paper/third/claim_ledger.md::N7` — stated in prose only (does not follow (witnesses: what is given, a result one change away). Growth: that terms must be added Evidence: `evidence/third/added_*.csv`)
- `H3V7N5QF:paper/third/claim_ledger.md::N8` — stated in prose only (does not follow (computed witnesses: `a b c; arb` and `a b; arb bra`, round 1, neither contains the other). That any two results are comparable (one reaches the other) Evidence: `evidence/third/reach_bound3_anchored_without_bra.csv`)
- `H3V7N5QF:paper/third/claim_ledger.md::N10` — stated in prose only (does not follow (D3: `1 + n² − m`; 9 for `a b c; arb`, 3 for `a b; arb bra`). That results of one round have equally many attempts Evidence: column `changes_attempted` of `results_*.csv`)
- `H3V7N5QF:paper/thirteenth/claim_ledger.md::D10` — stated in prose only (derived (identity) + computed. C-C1 results, rounds, sequences and count are the ninth's; count not a product for `n ≥ 2` Evidence: the C-C1 exploration wraps the ninth's, so `same_results`, rounds and sequences agree by construction; the one independent check is `explored_equals_independent_count` (the ninth's orbit count); 9:D10 for the non-product)
- `H3V7N5QF:paper/twelfth/claim_ledger.md::D10` — stated in prose only (derived (identity) + computed. C-M1 results, rounds, sequences and count are the ninth's; count not a product for `n ≥ 2` Evidence: the C-M1 exploration wraps the ninth's, so `same_results`, rounds and sequences agree by construction; the one independent check is `explored_equals_independent_count` (the ninth's orbit count); 9:D10 for the non-product)
- `H3V7N5QF:paper/twentyfifth/claim_ledger.md::D15` — stated in prose only (derived. Counts: orbits of sets of filled triples under the stabilizer of each twenty-third result; with at most two terms the twenty-third's closed form. Evidence: paper D15; computed `count_mismatch`, `two_term_mismatch` empty, `counts.csv`)
- `H3V7N5QF:paper/twentyfifth/claim_ledger.md::D16` — stated in prose only (derived. The readings: C-F2 the twenty-third's results; C-I2 and fillings last the chosen results; C-O2, C-O3, C-O4, C-M2, C-B2 rounds at their cost; C-I3 cost and reachability fail. Evidence: paper §3, D16; computed `readings.json`, `readings_mismatch` empty)
- `H3V7N5QF:paper/twentyfifth/claim_ledger.md::D17` — stated in prose only (derived. No tested statement holds in every result with three terms or more; some depend on the state asserting the fewest. Evidence: computed `follows_*.csv`)
- `H3V7N5QF:paper/twentyfifth/claim_ledger.md::N9` — stated in prose only (derived. Reachability need not hold under every reading (C-I3). Evidence: paper D16; computed `readings.json`)
- `H3V7N5QF:paper/twentyfourth/claim_ledger.md::D1` — stated in prose only (derived; computed. `Same24` (the twenty-third's `Same3` and the same filled terms) is an equivalence keeping the terms, the filled count and whether a term is filled; the clauses generate exactly the classes of the mark. Evidence: `Same24.refl`, `Same24.symm`, `Same24.trans`, `Same24.fc`, `Same24.hasFilled`, `Same24.sameW24`; `summary.json` (`generated_sameness`: 6 and 29 classes))
- `H3V7N5QF:paper/twentyfourth/claim_ledger.md::D2` — stated in prose only (derived; computed. A filled term balances exactly when its loop's excess is zero; this is the same in every state of a result and in every writing. Evidence: `balances_iff`, `Same24.balances`, `SameW24.pointwise`, `SameW24.balances`; `balance_mismatch` empty)
- `H3V7N5QF:paper/twentyfourth/claim_ledger.md::D3a` — stated in prose only (derived; computed. The twenty-third's record counts no assertion exactly for the result asserting nothing on its terms. Evidence: `record_whether`, `cost3_nothing`; `record_question_mismatch` empty)
- `H3V7N5QF:paper/twentyfourth/claim_ledger.md::D3b` — stated in prose only (derived; computed. The twenty-third's record does not show which terms keep a result from being the one asserting nothing: `a b; ara` / `a b; arb` and `a b c; ara asb` / `a b c; arb bsa` record the same and are kept by one term / two, one / three. Evidence: `record23_does_not_show_which`, `record23_does_not_show_which_three`, `fewest_loopA`, `fewest_arbA`, `fewest_loopAsb`, `fewest_arcThree`; `given.json`: 17 of 37 records)
- `H3V7N5QF:paper/twentyfourth/claim_ledger.md::D4` — stated in prose only (derived; computed. The record of `X` differs from that of the result asserting nothing on its terms, the same filled, exactly when some filled term's loop has non-zero excess; such a result is not the one asserting nothing; told is a mark of the result in eve... Evidence: `told_iff`, `nothing_balances`, `balRec_nothing`, `told_not_nothing`, `Same24.told`, `SameW24.told`, `same24_nothing_iff`; `tell_mismatch` empty)
- `H3V7N5QF:paper/twentyfourth/claim_ledger.md::D5` — stated in prose only (derived; computed. Every result neither the one asserting nothing nor told is one filling away, or of the two-term kind, or of the three-term kind; in the last two no filling tells. Evidence: `not_told_cases`, `told_after_fill`, `never_told_of_loops_zero`, `awayOne_not_told`, `awayOne_fill_told`, `twoWayFilled_not_nothing`, `twoWayFilled_never_told`, `aroundFilled_never_told`, `toldOne_told`; `summary.json` classes)
- `H3V7N5QF:paper/twentyfourth/claim_ledger.md::D6` — stated in prose only (derived. Identifying two terms puts the two loops and the two-way sum on the one loop; it can make a result told, and it can merge a three-term witness away. Evidence: `identify_tells`; paper D6)
- `H3V7N5QF:paper/twentyfourth/claim_ledger.md::D7` — stated in prose only (derived; computed. Filling respects the sameness; adding a term does not. Evidence: `Same24.fill`; `respect_mismatch` empty)
- `H3V7N5QF:paper/twentyfourth/claim_ledger.md::D8` — stated in prose only (F. The cost of a result is the twenty-third's cost of its assertions plus its filled terms, `n + Evidence: + min_g Σ)
- `H3V7N5QF:paper/twentyfourth/claim_ledger.md::D9a` — stated in prose only (derived; computed. A change from a state asserting the fewest raises the cost by at most one; no change returns a state to its own result. Evidence: `Step24.cost_le`, `cost24_le_pot`, `Step24.not_same24`; `change_mismatch` empty)
- `H3V7N5QF:paper/twentyfourth/claim_ledger.md::D9b` — stated in prose only (derived; computed. Identifying two filled terms moves the cost by an even number (`a b` both filled: 4 to 2); under C-I1 every other change moves it by an odd number. Evidence: `identify_two_filled_even`, `pairFilled_wf`, `cost24_oneFilled`; `change_mismatch` empty; `summary.json` moves)
- `H3V7N5QF:paper/twentyfourth/claim_ledger.md::D10` — stated in prose only (derived (paper); computed. A one-term result has one shortest sequence unfilled and `t + 1` filled. Evidence: paper D10; `sequences_mismatch` empty)
- `H3V7N5QF:paper/twentyfourth/claim_ledger.md::D11a` — stated in prose only (derived. Under C-I1 a filled term never goes away. Evidence: `Step24.hasFilled`, `Reach24.hasFilled`, `idF_of`, `idF_iff`)
- `H3V7N5QF:paper/twentyfourth/claim_ledger.md::D11b` — stated in prose only (derived; computed. A result reaches another exactly when the other has a term or the first is empty, and the other has a filled term or the first has none. Evidence: `reach24_criterion`, `Reach24.forget`, `reach24_clear`, `reach24_collapse`, `reach24_grow`, `reach24_atoms`, `reach24_fillFrom`, `reach24_from_one`, `idF_move`, `glue_move`, `reach24_mutual`; `reach_mismatch` empty (1 034 of 1 369))
- `H3V7N5QF:paper/twentyfourth/claim_ledger.md::D11c` — stated in prose only (derived; computed. The twenty-third's criterion fails exactly on the pairs from a result with a filled term to one without. Evidence: `twentythird_criterion_fails`; `reach_bound2_rounds4.csv` (299 = 13 × 23))
- `H3V7N5QF:paper/twentyfourth/claim_ledger.md::D11d` — stated in prose only (derived (paper; witness in Lean); computed. Under C-I2 and C-I3 a filled term can go away and the twenty-third's criterion holds. Evidence: `i2_unfills`; paper D11; `reach_mismatch` empty (1 333 of 1 369))
- `H3V7N5QF:paper/twentyfourth/claim_ledger.md::D12` — stated in prose only (derived; computed. The exchange keeps the sameness, balance, told, the cost and reachability, and carries each change to one of the same kind. Evidence: `same24_swap_iff`, `Same24.swap`, `balances_swap`, `told_swap`, `cost24_swap`, `reach24_swap`, `Step24.swap`, `Reach24.swap`, `FSt.swap_swap`; `exchange_mismatch` empty)
- `H3V7N5QF:paper/twentyfourth/claim_ledger.md::D13` — stated in prose only (derived; computed. The twenty-third maps in one to one, each change carried to a change of the same kind; no two of its results are made one here, so the merge loses nothing. Evidence: `same24_ofSt_iff`, `sameW24_ofSt_iff`, `Step.toStep24`, `Reach.toReach24`, `idF_false`, `no_merge`, `ofSt_wf`, `ofSt_fc`; `twentythird_mismatch` empty)
- `H3V7N5QF:paper/twentyfourth/claim_ledger.md::D13a` — stated in prose only (derived. The twenty-second's, ninth's, seventh's and first's witnesses of 23:D9 merge here as there. Evidence: `seventh_pair_merge24`)
- `H3V7N5QF:paper/twentyfourth/claim_ledger.md::D14a` — stated in prose only (derived; computed. The map back returns the original on mapped results, answers "none" exactly with a filled term, and depends on the result only. Evidence: `readBack_ofSt`, `readBack_none_iff`, `readBack_some`, `readBack_congr`, `anyFilled_iff`; `read_back_mismatch` empty)
- `H3V7N5QF:paper/twentyfourth/claim_ledger.md::D14b` — stated in prose only (derived; computed. Every result answered "none" costs at least two; the smallest is `a` filled, nothing asserted, at cost two, the only one there. Evidence: `readBack_none_cost`, `fc_pos`, `smallest_none`, `smallest_none_unique`; first "none" at round 2 in every run)
- `H3V7N5QF:paper/twentyfourth/claim_ledger.md::D14c` — stated in prose only (derived; computed. The forgetting map answers every result, carries each change to a change or to none, and merges results differing only in their filled terms. Evidence: `Step24.forget`, `forget_merges`; `forget_mismatch` empty)
- `H3V7N5QF:paper/twentyfourth/claim_ledger.md::D15` — stated in prose only (derived (paper); computed. The counts: two-term closed forms `2t² + t + 1`, `4t² + 2`, `2t² + t + 1`; per round `8r² − 46r + 78` from `r = 4`; 2 482 245 within 100 rounds. Evidence: `counts.csv`, `summary.json`; `count_mismatch`, `two_term_mismatch` empty)
- `H3V7N5QF:paper/twentyfourth/claim_ledger.md::D16` — stated in prose only (derived; computed. The unchosen readings: C-F2 other results; C-F3, C-F4, C-I2, C-I3, C-E′ C-F1's results and rounds. Evidence: `fillLoops_same`; `readings.json`; `readings_mismatch` empty)
- `H3V7N5QF:paper/twentyfourth/claim_ledger.md::R1` — stated in prose only (refuted. A told result that is the one asserting nothing. Evidence: `told_not_nothing`)
- `H3V7N5QF:paper/twentyfourth/claim_ledger.md::R2` — stated in prose only (refuted. A told result with every loop zero, whatever is filled. Evidence: `never_told_of_loops_zero`)
- `H3V7N5QF:paper/twentyfourth/claim_ledger.md::R3` — stated in prose only (refuted. Fewer changes to a result than the twenty-third's cost plus its filled terms. Evidence: `cost24_eq`)
- `H3V7N5QF:paper/twentyfourth/claim_ledger.md::R4` — stated in prose only (refuted. A change from a state asserting the fewest raising the cost by more than one; a change returning a state to its own result. Evidence: `Step24.cost_le`, `Step24.not_same24`)
- `H3V7N5QF:paper/twentyfourth/claim_ledger.md::R5` — stated in prose only (refuted. Under C-I1, a sequence from a state with a filled term to one without. Evidence: `Reach24.hasFilled`)
- `H3V7N5QF:paper/twentyfourth/claim_ledger.md::R6` — stated in prose only (refuted. A result answered "none" costing less than two. Evidence: `readBack_none_cost`)
- `H3V7N5QF:paper/twentyfourth/claim_ledger.md::R7` — stated in prose only (refuted. Two twenty-third results made one here. Evidence: `no_merge`)
- `H3V7N5QF:paper/twentysecond/claim_ledger.md::D4` — stated in prose only (excess. The fewest changes to a result is `n + Σ Evidence: ` (the plain state's size); the ninth's size of a state exceeds it by the atoms of its pairs asserted together; a shortest sequence is additions only through plain states.)
- `H3V7N5QF:paper/twentysecond/claim_ledger.md::D11` — stated in prose only (derived. Each cycle of pairs of a rewriting contributes `(1 + x^L)/(1 − x^L)`; with at most two terms the results of round `r` are `[r = 0] + [r ≥ 1]·one(r − 1) + [r ≥ 2]·two(r − 2)`, `two(t) = 4t(t² + 2)/3 + [t even]·t`; 31 391 855 within 100 round... Evidence: paper D11; computed `count_mismatch`, `two_term_mismatch` empty, `counts.csv`; tests against a listing)
- `H3V7N5QF:paper/twentysecond/claim_ledger.md::D12` — stated in prose only (derived. A one-term result has one shortest sequence. Evidence: paper D12 (from D4); computed `one_term_not_one_sequence` empty)
- `H3V7N5QF:paper/twentysecond/claim_ledger.md::D13` — stated in prose only (derived. Within the bound the exploration is complete, the frontier exact, the shortest-sequence counts exact. Evidence: paper D13; computed `count_mismatch` empty, `frontier_entries_are_1_per_state_with_N_terms`)
- `H3V7N5QF:paper/twentysecond/claim_ledger.md::D14` — stated in prose only (derived. Under the unchosen "larger of the two" identification: same results, cost and reachability; an identification's outcome as a result depends on the state taken. Evidence: paper D14)
- `H3V7N5QF:paper/twentysecond/claim_ledger.md::D15` — stated in prose only (D. C-J2: a result is `(n, Σ M_r − Σ M_s)`, cost `n + Evidence: `; C-J3: cost the reduced size, a count by cycles; under C-J3 with C-X, round 3 is infinite.)
- `H3V7N5QF:paper/twentysecond/claim_ledger.md::D16` — stated in prose only (derived. No tested statement about the asserting holds in every result; "some pair asserted in both relations" holds in none, by construction of the plain state. Evidence: computed `follows_*.csv`, `statements_holding_in_every_result` empty)
- `H3V7N5QF:paper/twentysecond/claim_ledger.md::N5` — stated in prose only (derived. Two additions that undo need not be one pair, up to rewriting. Evidence: `given.json`)
- `H3V7N5QF:paper/twentysecond/claim_ledger.md::N8` — stated in prose only (derived. Results with equally many terms need not have equally many changes. Evidence: paper N8; `results_*.csv`)
- `H3V7N5QF:paper/twentysecond/claim_ledger.md::R3` — stated in prose only (excess. Fewer changes to a result than `n + Σ Evidence: `.)
- `H3V7N5QF:paper/twentythird/claim_ledger.md::D5` — stated in prose only (e(x, y) + g(x) − g(y). The cost is `n + min_g Σ Evidence: `, in every writing; two-term closed form; three-term closed form; the loops and two-way sums do not fix it; raising sets of terms while the count falls reaches it.)
- `H3V7N5QF:paper/twentythird/claim_ledger.md::D8` — stated in prose only (derived. What is recorded is the same on every state asserting the fewest. Evidence: paper D8; computed `record_mismatch` empty)
- `H3V7N5QF:paper/twentythird/claim_ledger.md::D14` — stated in prose only (derived. Two-term results recording `t` assertions: `2t² + t + 1`; round counts `[r = 0] + [r ≥ 1]·one(r − 1) + [r ≥ 2]·two(r − 2)`; three-term counts from the invariants; 642 248 results with at most two terms within 100 rounds. Evidence: paper D14; computed `count_mismatch`, `two_term_mismatch` empty, `counts.csv`)
- `H3V7N5QF:paper/twentythird/claim_ledger.md::D17` — stated in prose only (derived. No tested statement holds in every result; some depend on the state asserting the fewest taken. Evidence: computed `follows_*.csv`, `statements_holding_in_every_result` empty)
- `H3V7N5QF:paper/twentythird/claim_ledger.md::N8` — stated in prose only (derived. No earlier seed maps in one to one (as D9). Evidence: as D9)

## Proved theorems

Every other theorem or lemma named by some `evidence/**/lean_axioms.txt` `#print axioms` line, one entry each. Duplicate prints of the same qualified name in a later report are omitted. Count: 1706. Axioms are the first report's recorded list, inside `{none, propext, Classical.choice, Quot.sound}`.


### `lean4/H3V7N5QF/Finite.lean`

- `H3V7N5QF:lean4/H3V7N5QF/Finite.lean::addAssertion_legal_iff` — proved in Lean (module `lean4/H3V7N5QF/Finite.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/lean_axioms.txt`)
- `H3V7N5QF:lean4/H3V7N5QF/Finite.lean::adding_xrx_always_obstructed` — proved in Lean (module `lean4/H3V7N5QF/Finite.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/lean_axioms.txt`)
- `H3V7N5QF:lean4/H3V7N5QF/Finite.lean::addTerm_legal` — proved in Lean (module `lean4/H3V7N5QF/Finite.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/lean_axioms.txt`)

### `lean4/H3V7N5QF/Basic.lean`

- `H3V7N5QF:lean4/H3V7N5QF/Basic.lean::bra_not_derived` — proved in Lean (module `lean4/H3V7N5QF/Basic.lean`; axioms: propext; recorded in `evidence/lean_axioms.txt`)
- `H3V7N5QF:lean4/H3V7N5QF/Basic.lean::bra_not_refuted` — proved in Lean (module `lean4/H3V7N5QF/Basic.lean`; axioms: none; recorded in `evidence/lean_axioms.txt`)

### `lean4/H3V7N5QF/Answers.lean`

- `H3V7N5QF:lean4/H3V7N5QF/Answers.lean::build_answer` — proved in Lean (module `lean4/H3V7N5QF/Answers.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/lean_axioms.txt`)
- `H3V7N5QF:lean4/H3V7N5QF/Answers.lean::build_answer_reverse` — proved in Lean (module `lean4/H3V7N5QF/Answers.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/lean_axioms.txt`)
- `H3V7N5QF:lean4/H3V7N5QF/Answers.lean::build_gives_back` — proved in Lean (module `lean4/H3V7N5QF/Answers.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/lean_axioms.txt`)
- `H3V7N5QF:lean4/H3V7N5QF/Answers.lean::build_needs_term_and_assertion` — proved in Lean (module `lean4/H3V7N5QF/Answers.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/lean_axioms.txt`)
- `H3V7N5QF:lean4/H3V7N5QF/Answers.lean::build_reverse_gives_back` — proved in Lean (module `lean4/H3V7N5QF/Answers.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/lean_axioms.txt`)

### `lean4/H3V7N5QF/Paths.lean`

- `H3V7N5QF:lean4/H3V7N5QF/Paths.lean::edits_count` — proved in Lean (module `lean4/H3V7N5QF/Paths.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/lean_axioms.txt`)

### `lean4/Eighteenth/Writing.lean`

- `H3V7N5QF:lean4/Eighteenth/Writing.lean::given_ne_bra` — proved in Lean (module `lean4/Eighteenth/Writing.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighteenth/Writing.lean::swapped_ne_bra` — proved in Lean (module `lean4/Eighteenth/Writing.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighteenth/Writing.lean::swapped_ne_given` — proved in Lean (module `lean4/Eighteenth/Writing.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighteenth/lean_axioms.txt`)

### `lean4/Eighth/Reach.lean`

- `H3V7N5QF:lean4/Eighth/Reach.lean::antisymm_fails8` — proved in Lean (module `lean4/Eighth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Eighth/Compare.lean`

- `H3V7N5QF:lean4/Eighth/Compare.lean::cost_survives` — proved in Lean (module `lean4/Eighth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Eighth/Cost.lean`

- `H3V7N5QF:lean4/Eighth/Cost.lean::costA8_eq` — proved in Lean (module `lean4/Eighth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/Cost.lean::costA8_givenA8` — proved in Lean (module `lean4/Eighth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/Cost.lean::costA8_ofR` — proved in Lean (module `lean4/Eighth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Eighth/Rename.lean`

- `H3V7N5QF:lean4/Eighth/Rename.lean::costA8_rename` — proved in Lean (module `lean4/Eighth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Eighth/Cost.lean`

- `H3V7N5QF:lean4/Eighth/Cost.lean::costB8_eq` — proved in Lean (module `lean4/Eighth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/Cost.lean::costB8_givenB8` — proved in Lean (module `lean4/Eighth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/Cost.lean::costB8_ofR` — proved in Lean (module `lean4/Eighth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Eighth/Rename.lean`

- `H3V7N5QF:lean4/Eighth/Rename.lean::costB8_rename` — proved in Lean (module `lean4/Eighth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Eighth/Compare.lean`

- `H3V7N5QF:lean4/Eighth/Compare.lean::criterion_survives` — proved in Lean (module `lean4/Eighth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Eighth/Reach.lean`

- `H3V7N5QF:lean4/Eighth/Reach.lean::cycle2_8` — proved in Lean (module `lean4/Eighth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Eighth/State.lean`

- `H3V7N5QF:lean4/Eighth/State.lean::eq_ofR_of_nothing_in_s` — proved in Lean (module `lean4/Eighth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/State.lean::ext_proj` — proved in Lean (module `lean4/Eighth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Eighth/Cost.lean`

- `H3V7N5QF:lean4/Eighth/Cost.lean::fewest_changes8_A` — proved in Lean (module `lean4/Eighth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/Cost.lean::fewest_changes8_B` — proved in Lean (module `lean4/Eighth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Eighth/Rename.lean`

- `H3V7N5QF:lean4/Eighth/Rename.lean::fewest_changes8_every_writing_A` — proved in Lean (module `lean4/Eighth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/Rename.lean::fewest_changes8_every_writing_B` — proved in Lean (module `lean4/Eighth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Eighth/Cost.lean`

- `H3V7N5QF:lean4/Eighth/Cost.lean::fewest_changes8_lower_A` — proved in Lean (module `lean4/Eighth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/Cost.lean::fewest_changes8_lower_B` — proved in Lean (module `lean4/Eighth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/Cost.lean::fewest_changes8_of_r_A` — proved in Lean (module `lean4/Eighth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/Cost.lean::fewest_changes8_of_r_B` — proved in Lean (module `lean4/Eighth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Eighth/State.lean`

- `H3V7N5QF:lean4/Eighth/State.lean::givenA8_a` — proved in Lean (module `lean4/Eighth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/State.lean::givenA8_b` — proved in Lean (module `lean4/Eighth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/State.lean::givenA8_proj` — proved in Lean (module `lean4/Eighth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/State.lean::givenA8_wf` — proved in Lean (module `lean4/Eighth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/State.lean::givenB8_a` — proved in Lean (module `lean4/Eighth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/State.lean::givenB8_b` — proved in Lean (module `lean4/Eighth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/State.lean::givenB8_wf` — proved in Lean (module `lean4/Eighth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/State.lean::identify_zero` — proved in Lean (module `lean4/Eighth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Eighth/Compare.lean`

- `H3V7N5QF:lean4/Eighth/Compare.lean::interaction` — proved in Lean (module `lean4/Eighth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Eighth/Reach.lean`

- `H3V7N5QF:lean4/Eighth/Reach.lean::length_not_unique8` — proved in Lean (module `lean4/Eighth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/Reach.lean::merged_never_apart8` — proved in Lean (module `lean4/Eighth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/Reach.lean::no_return_fails8` — proved in Lean (module `lean4/Eighth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Eighth/State.lean`

- `H3V7N5QF:lean4/Eighth/State.lean::not_ne` — proved in Lean (module `lean4/Eighth/State.lean`; axioms: none; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/State.lean::ofR_addAssertion` — proved in Lean (module `lean4/Eighth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/State.lean::ofR_addTerm` — proved in Lean (module `lean4/Eighth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/State.lean::ofR_identify` — proved in Lean (module `lean4/Eighth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/State.lean::ofR_nothing_in_s` — proved in Lean (module `lean4/Eighth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/State.lean::ofR_remove` — proved in Lean (module `lean4/Eighth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/State.lean::ofR_wf` — proved in Lean (module `lean4/Eighth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/State.lean::proj_addAssertion_other` — proved in Lean (module `lean4/Eighth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/State.lean::proj_addAssertion_self` — proved in Lean (module `lean4/Eighth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/State.lean::proj_addTerm` — proved in Lean (module `lean4/Eighth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/State.lean::proj_identify` — proved in Lean (module `lean4/Eighth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/State.lean::proj_ofR_false` — proved in Lean (module `lean4/Eighth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/State.lean::proj_ofR_true` — proved in Lean (module `lean4/Eighth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/State.lean::proj_remove_other` — proved in Lean (module `lean4/Eighth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/State.lean::proj_remove_self` — proved in Lean (module `lean4/Eighth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Eighth/Rename.lean`

- `H3V7N5QF:lean4/Eighth/Rename.lean::proj_rename8` — proved in Lean (module `lean4/Eighth/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Eighth/Compare.lean`

- `H3V7N5QF:lean4/Eighth/Compare.lean::proj_results` — proved in Lean (module `lean4/Eighth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Eighth/Cost.lean`

- `H3V7N5QF:lean4/Eighth/Cost.lean::costA_le` — proved in Lean (module `lean4/Eighth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/Cost.lean::costB_le` — proved in Lean (module `lean4/Eighth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Eighth/Reach.lean`

- `H3V7N5QF:lean4/Eighth/Reach.lean::cycles` — proved in Lean (module `lean4/Eighth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Eighth/Step.lean`

- `H3V7N5QF:lean4/Eighth/Step.lean::eq_of_zero` — proved in Lean (module `lean4/Eighth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Ninth/Step.lean`

- `H3V7N5QF:lean4/Ninth/Step.lean::forget` — proved in Lean (module `lean4/Ninth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Eighth/Step.lean`

- `H3V7N5QF:lean4/Eighth/Step.lean::proj` — proved in Lean (module `lean4/Eighth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Eighth/Rename.lean`

- `H3V7N5QF:lean4/Eighth/Rename.lean::rename` — proved in Lean (module `lean4/Eighth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Eighth/Cost.lean`

- `H3V7N5QF:lean4/Eighth/Cost.lean::size_parity` — proved in Lean (module `lean4/Eighth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Eighth/Step.lean`

- `H3V7N5QF:lean4/Eighth/Step.lean::trans` — proved in Lean (module `lean4/Eighth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Eighth/Reach.lean`

- `H3V7N5QF:lean4/Eighth/Reach.lean::unbounded` — proved in Lean (module `lean4/Eighth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/Reach.lean::reach8_back_A` — proved in Lean (module `lean4/Eighth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/Reach.lean::reach8_clear_s` — proved in Lean (module `lean4/Eighth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Eighth/Cost.lean`

- `H3V7N5QF:lean4/Eighth/Cost.lean::reach8_from_ofR` — proved in Lean (module `lean4/Eighth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Eighth/Reach.lean`

- `H3V7N5QF:lean4/Eighth/Reach.lean::reach8_iff` — proved in Lean (module `lean4/Eighth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/Reach.lean::reach8_iff_r` — proved in Lean (module `lean4/Eighth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/Reach.lean::reach8_of_names` — proved in Lean (module `lean4/Eighth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Eighth/Cost.lean`

- `H3V7N5QF:lean4/Eighth/Cost.lean::reach8_raise` — proved in Lean (module `lean4/Eighth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Eighth/Reach.lean`

- `H3V7N5QF:lean4/Eighth/Reach.lean::reach8_symm` — proved in Lean (module `lean4/Eighth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/Reach.lean::reach8_total` — proved in Lean (module `lean4/Eighth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/Reach.lean::remove_addAssertion` — proved in Lean (module `lean4/Eighth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Eighth/Rename.lean`

- `H3V7N5QF:lean4/Eighth/Rename.lean::rename8_addAssertion` — proved in Lean (module `lean4/Eighth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/Rename.lean::rename8_addTerm` — proved in Lean (module `lean4/Eighth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/Rename.lean::rename8_identify` — proved in Lean (module `lean4/Eighth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/Rename.lean::rename8_ofR` — proved in Lean (module `lean4/Eighth/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/Rename.lean::rename8_remove` — proved in Lean (module `lean4/Eighth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Eighth/Reach.lean`

- `H3V7N5QF:lean4/Eighth/Reach.lean::result8_iff_A` — proved in Lean (module `lean4/Eighth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/Reach.lean::result8_iff_B` — proved in Lean (module `lean4/Eighth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Eighth/Compare.lean`

- `H3V7N5QF:lean4/Eighth/Compare.lean::results_grow` — proved in Lean (module `lean4/Eighth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/Compare.lean::results_ofR_A` — proved in Lean (module `lean4/Eighth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/Compare.lean::results_ofR_B` — proved in Lean (module `lean4/Eighth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Eighth/Reach.lean`

- `H3V7N5QF:lean4/Eighth/Reach.lean::results_pair` — proved in Lean (module `lean4/Eighth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Eighth/Compare.lean`

- `H3V7N5QF:lean4/Eighth/Compare.lean::results_r_iff` — proved in Lean (module `lean4/Eighth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Eighth/Cost.lean`

- `H3V7N5QF:lean4/Eighth/Cost.lean::s_costs_its_total` — proved in Lean (module `lean4/Eighth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Eighth/Reach.lean`

- `H3V7N5QF:lean4/Eighth/Reach.lean::s_is_a_result` — proved in Lean (module `lean4/Eighth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Eighth/Compare.lean`

- `H3V7N5QF:lean4/Eighth/Compare.lean::same_r_part_mutual` — proved in Lean (module `lean4/Eighth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Eighth/State.lean`

- `H3V7N5QF:lean4/Eighth/State.lean::size_eq` — proved in Lean (module `lean4/Eighth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/State.lean::size_givenA8` — proved in Lean (module `lean4/Eighth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/State.lean::size_givenB8` — proved in Lean (module `lean4/Eighth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/State.lean::size_ofR` — proved in Lean (module `lean4/Eighth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Eighth/Rename.lean`

- `H3V7N5QF:lean4/Eighth/Rename.lean::size_rename8` — proved in Lean (module `lean4/Eighth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Eighth/Cost.lean`

- `H3V7N5QF:lean4/Eighth/Cost.lean::costA_le` — proved in Lean (module `lean4/Eighth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/Cost.lean::costB_le` — proved in Lean (module `lean4/Eighth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Ninth/Step.lean`

- `H3V7N5QF:lean4/Ninth/Step.lean::forget` — proved in Lean (module `lean4/Ninth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Eighth/Step.lean`

- `H3V7N5QF:lean4/Eighth/Step.lean::proj` — proved in Lean (module `lean4/Eighth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/Step.lean::proj_self` — proved in Lean (module `lean4/Eighth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Eighth/Rename.lean`

- `H3V7N5QF:lean4/Eighth/Rename.lean::rename` — proved in Lean (module `lean4/Eighth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Eighth/Cost.lean`

- `H3V7N5QF:lean4/Eighth/Cost.lean::size_step` — proved in Lean (module `lean4/Eighth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eighth/Cost.lean::split` — proved in Lean (module `lean4/Eighth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Eighth/State.lean`

- `H3V7N5QF:lean4/Eighth/State.lean::wf_proj` — proved in Lean (module `lean4/Eighth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Eighth/Rename.lean`

- `H3V7N5QF:lean4/Eighth/Rename.lean::wf_rename8` — proved in Lean (module `lean4/Eighth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Eleventh/Step.lean`

- `H3V7N5QF:lean4/Eleventh/Step.lean::apart_determines_twoBetween` — proved in Lean (module `lean4/Eleventh/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eleventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eleventh/Step.lean::coarser_of_not_determines` — proved in Lean (module `lean4/Eleventh/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eleventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eleventh/Step.lean::collide_keeps_terms` — proved in Lean (module `lean4/Eleventh/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eleventh/lean_axioms.txt`)

### `lean4/Eleventh/Rename.lean`

- `H3V7N5QF:lean4/Eleventh/Rename.lean::determines_swap` — proved in Lean (module `lean4/Eleventh/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eleventh/lean_axioms.txt`)

### `lean4/Eleventh/Compare.lean`

- `H3V7N5QF:lean4/Eleventh/Compare.lean::fewest_changes11` — proved in Lean (module `lean4/Eleventh/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eleventh/lean_axioms.txt`)

### `lean4/Eleventh/Step.lean`

- `H3V7N5QF:lean4/Eleventh/Step.lean::first_change_adds_term11` — proved in Lean (module `lean4/Eleventh/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eleventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eleventh/Step.lean::identify_drops_a_term` — proved in Lean (module `lean4/Eleventh/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eleventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eleventh/Step.lean::inj_determines` — proved in Lean (module `lean4/Eleventh/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eleventh/lean_axioms.txt`)

### `lean4/Eleventh/Compare.lean`

- `H3V7N5QF:lean4/Eleventh/Compare.lean::labeled_cost_is_size` — proved in Lean (module `lean4/Eleventh/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eleventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eleventh/Compare.lean::labeled_extra` — proved in Lean (module `lean4/Eleventh/Compare.lean`; axioms: propext, Quot.sound; recorded in `evidence/eleventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eleventh/Compare.lean::no_cross_constraint` — proved in Lean (module `lean4/Eleventh/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eleventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eleventh/Compare.lean::no_third_rel` — proved in Lean (module `lean4/Eleventh/Compare.lean`; axioms: propext, Quot.sound; recorded in `evidence/eleventh/lean_axioms.txt`)

### `lean4/Eleventh/Step.lean`

- `H3V7N5QF:lean4/Eleventh/Step.lean::r_collision_not_s` — proved in Lean (module `lean4/Eleventh/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eleventh/lean_axioms.txt`)

### `lean4/Eleventh/Compare.lean`

- `H3V7N5QF:lean4/Eleventh/Compare.lean::reach11_iff` — proved in Lean (module `lean4/Eleventh/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eleventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eleventh/Compare.lean::results_pair11` — proved in Lean (module `lean4/Eleventh/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eleventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eleventh/Compare.lean::split_injective` — proved in Lean (module `lean4/Eleventh/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eleventh/lean_axioms.txt`)

### `lean4/Eleventh/Rename.lean`

- `H3V7N5QF:lean4/Eleventh/Rename.lean::swap` — proved in Lean (module `lean4/Eleventh/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eleventh/lean_axioms.txt`)

### `lean4/Eleventh/Step.lean`

- `H3V7N5QF:lean4/Eleventh/Step.lean::twoBetween_determines_s` — proved in Lean (module `lean4/Eleventh/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eleventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eleventh/Step.lean::twoBetween_not_determines_r` — proved in Lean (module `lean4/Eleventh/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eleventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Eleventh/Step.lean::writing_not_assertion` — proved in Lean (module `lean4/Eleventh/Step.lean`; axioms: propext, Quot.sound; recorded in `evidence/eleventh/lean_axioms.txt`)

### `lean4/Eleventh/Compare.lean`

- `H3V7N5QF:lean4/Eleventh/Compare.lean::writing_not_identify` — proved in Lean (module `lean4/Eleventh/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eleventh/lean_axioms.txt`)

### `lean4/H3V7N5QF/Paths.lean`

- `H3V7N5QF:lean4/H3V7N5QF/Paths.lean::fewest_changes_A` — proved in Lean (module `lean4/H3V7N5QF/Paths.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/lean_axioms.txt`)
- `H3V7N5QF:lean4/H3V7N5QF/Paths.lean::fewest_changes_B` — proved in Lean (module `lean4/H3V7N5QF/Paths.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/lean_axioms.txt`)

### `lean4/H3V7N5QF/Cost.lean`

- `H3V7N5QF:lean4/H3V7N5QF/Cost.lean::fewest_changes_lower_A` — proved in Lean (module `lean4/H3V7N5QF/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/lean_axioms.txt`)
- `H3V7N5QF:lean4/H3V7N5QF/Cost.lean::fewest_changes_lower_B` — proved in Lean (module `lean4/H3V7N5QF/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/lean_axioms.txt`)

### `lean4/Fifteenth/Step.lean`

- `H3V7N5QF:lean4/Fifteenth/Step.lean::admission_not_a_kind` — proved in Lean (module `lean4/Fifteenth/Step.lean`; axioms: none; recorded in `evidence/fifteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifteenth/Step.lean::admission_not_assertion` — proved in Lean (module `lean4/Fifteenth/Step.lean`; axioms: none; recorded in `evidence/fifteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifteenth/Step.lean::admission_not_in_M` — proved in Lean (module `lean4/Fifteenth/Step.lean`; axioms: propext, Quot.sound; recorded in `evidence/fifteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifteenth/Step.lean::admission_not_of_relation` — proved in Lean (module `lean4/Fifteenth/Step.lean`; axioms: none; recorded in `evidence/fifteenth/lean_axioms.txt`)

### `lean4/Fifteenth/Rename.lean`

- `H3V7N5QF:lean4/Fifteenth/Rename.lean::admission_swap` — proved in Lean (module `lean4/Fifteenth/Rename.lean`; axioms: none; recorded in `evidence/fifteenth/lean_axioms.txt`)

### `lean4/Fifteenth/Compare.lean`

- `H3V7N5QF:lean4/Fifteenth/Compare.lean::fewest_changes15` — proved in Lean (module `lean4/Fifteenth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifteenth/Compare.lean::no_cross_constraint` — proved in Lean (module `lean4/Fifteenth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifteenth/Compare.lean::no_third_rel` — proved in Lean (module `lean4/Fifteenth/Compare.lean`; axioms: propext, Quot.sound; recorded in `evidence/fifteenth/lean_axioms.txt`)

### `lean4/Fifteenth/Step.lean`

- `H3V7N5QF:lean4/Fifteenth/Step.lean::r_admission_is_s` — proved in Lean (module `lean4/Fifteenth/Step.lean`; axioms: none; recorded in `evidence/fifteenth/lean_axioms.txt`)

### `lean4/Fifteenth/Compare.lean`

- `H3V7N5QF:lean4/Fifteenth/Compare.lean::r_admission_is_s_result` — proved in Lean (module `lean4/Fifteenth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifteenth/Compare.lean::reach15_iff` — proved in Lean (module `lean4/Fifteenth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifteenth/Compare.lean::results_pair15` — proved in Lean (module `lean4/Fifteenth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifteenth/lean_axioms.txt`)

### `lean4/Fifteenth/Rename.lean`

- `H3V7N5QF:lean4/Fifteenth/Rename.lean::swap` — proved in Lean (module `lean4/Fifteenth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifteenth/lean_axioms.txt`)

### `lean4/Fifteenth/Compare.lean`

- `H3V7N5QF:lean4/Fifteenth/Compare.lean::tagged_cost_fails` — proved in Lean (module `lean4/Fifteenth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifteenth/Compare.lean::tagged_extra` — proved in Lean (module `lean4/Fifteenth/Compare.lean`; axioms: propext, Quot.sound; recorded in `evidence/fifteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifteenth/Compare.lean::tagged_one_nothing` — proved in Lean (module `lean4/Fifteenth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifteenth/lean_axioms.txt`)

### `lean4/Fifth/Reach.lean`

- `H3V7N5QF:lean4/Fifth/Reach.lean::add_identify_back` — proved in Lean (module `lean4/Fifth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/Reach.lean::antisymm_fails` — proved in Lean (module `lean4/Fifth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Fifth/Cost.lean`

- `H3V7N5QF:lean4/Fifth/Cost.lean::arb_removed` — proved in Lean (module `lean4/Fifth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fifth/Answers.lean`

- `H3V7N5QF:lean4/Fifth/Answers.lean::build_answer5` — proved in Lean (module `lean4/Fifth/Answers.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/Answers.lean::build_answer5_reverse` — proved in Lean (module `lean4/Fifth/Answers.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fifth/Compare.lean`

- `H3V7N5QF:lean4/Fifth/Compare.lean::contains4_reach5` — proved in Lean (module `lean4/Fifth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fifth/Cost.lean`

- `H3V7N5QF:lean4/Fifth/Cost.lean::contains_fails` — proved in Lean (module `lean4/Fifth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Fifth/Compare.lean`

- `H3V7N5QF:lean4/Fifth/Compare.lean::cost_survives_length_does_not` — proved in Lean (module `lean4/Fifth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fifth/Cost.lean`

- `H3V7N5QF:lean4/Fifth/Cost.lean::costA5_givenA4` — proved in Lean (module `lean4/Fifth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fifth/Rename.lean`

- `H3V7N5QF:lean4/Fifth/Rename.lean::costA5_rename` — proved in Lean (module `lean4/Fifth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fifth/Cost.lean`

- `H3V7N5QF:lean4/Fifth/Cost.lean::costB5_givenB4` — proved in Lean (module `lean4/Fifth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fifth/Rename.lean`

- `H3V7N5QF:lean4/Fifth/Rename.lean::costB5_rename` — proved in Lean (module `lean4/Fifth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fifth/Compare.lean`

- `H3V7N5QF:lean4/Fifth/Compare.lean::criterion_fails` — proved in Lean (module `lean4/Fifth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fifth/Reach.lean`

- `H3V7N5QF:lean4/Fifth/Reach.lean::cycle2` — proved in Lean (module `lean4/Fifth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fifth/Rename.lean`

- `H3V7N5QF:lean4/Fifth/Rename.lean::exists_writing5` — proved in Lean (module `lean4/Fifth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Fifth/Cost.lean`

- `H3V7N5QF:lean4/Fifth/Cost.lean::fewest_changes5_A` — proved in Lean (module `lean4/Fifth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/Cost.lean::fewest_changes5_B` — proved in Lean (module `lean4/Fifth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fifth/Rename.lean`

- `H3V7N5QF:lean4/Fifth/Rename.lean::fewest_changes5_every_writing_A` — proved in Lean (module `lean4/Fifth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/Rename.lean::fewest_changes5_every_writing_B` — proved in Lean (module `lean4/Fifth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fifth/Cost.lean`

- `H3V7N5QF:lean4/Fifth/Cost.lean::fewest_changes5_lower_A` — proved in Lean (module `lean4/Fifth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/Cost.lean::fewest_changes5_lower_B` — proved in Lean (module `lean4/Fifth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/Cost.lean::fewest_changes5_of_contains_A` — proved in Lean (module `lean4/Fifth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/Cost.lean::fewest_changes5_of_contains_B` — proved in Lean (module `lean4/Fifth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/Cost.lean::fewest_changes5_upper_A_apart` — proved in Lean (module `lean4/Fifth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/Cost.lean::fewest_changes5_upper_A_merged` — proved in Lean (module `lean4/Fifth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/Cost.lean::fewest_changes5_upper_B_apart` — proved in Lean (module `lean4/Fifth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/Cost.lean::fewest_changes5_upper_B_merged` — proved in Lean (module `lean4/Fifth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/Cost.lean::givenA4_to_oneTerm4` — proved in Lean (module `lean4/Fifth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fifth/Reach.lean`

- `H3V7N5QF:lean4/Fifth/Reach.lean::givenB4_remove_bra_eq` — proved in Lean (module `lean4/Fifth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fifth/Cost.lean`

- `H3V7N5QF:lean4/Fifth/Cost.lean::givenB4_to_oneTerm4` — proved in Lean (module `lean4/Fifth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fifth/Step.lean`

- `H3V7N5QF:lean4/Fifth/Step.lean::identify_legal_iff` — proved in Lean (module `lean4/Fifth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fifth/State.lean`

- `H3V7N5QF:lean4/Fifth/State.lean::identify_M_eq_zero_iff` — proved in Lean (module `lean4/Fifth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/State.lean::identify_M_ge` — proved in Lean (module `lean4/Fifth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/State.lean::identify_M_ne_zero` — proved in Lean (module `lean4/Fifth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fifth/Reach.lean`

- `H3V7N5QF:lean4/Fifth/Reach.lean::length_not_unique` — proved in Lean (module `lean4/Fifth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fifth/Cost.lean`

- `H3V7N5QF:lean4/Fifth/Cost.lean::lostA5_eq_zero_of_contains` — proved in Lean (module `lean4/Fifth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/Cost.lean::lostA5_identify` — proved in Lean (module `lean4/Fifth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/Cost.lean::lostA5_le_of_contains` — proved in Lean (module `lean4/Fifth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/Cost.lean::lostA5_le_two` — proved in Lean (module `lean4/Fifth/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/Cost.lean::lostA5_remove` — proved in Lean (module `lean4/Fifth/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fifth/Rename.lean`

- `H3V7N5QF:lean4/Fifth/Rename.lean::lostA5_rename` — proved in Lean (module `lean4/Fifth/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fifth/Cost.lean`

- `H3V7N5QF:lean4/Fifth/Cost.lean::lostB5_eq_zero_of_contains` — proved in Lean (module `lean4/Fifth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/Cost.lean::lostB5_identify` — proved in Lean (module `lean4/Fifth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/Cost.lean::lostB5_le_of_contains` — proved in Lean (module `lean4/Fifth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/Cost.lean::lostB5_le_three` — proved in Lean (module `lean4/Fifth/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/Cost.lean::lostB5_remove` — proved in Lean (module `lean4/Fifth/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fifth/Rename.lean`

- `H3V7N5QF:lean4/Fifth/Rename.lean::lostB5_rename` — proved in Lean (module `lean4/Fifth/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fifth/Cost.lean`

- `H3V7N5QF:lean4/Fifth/Cost.lean::mem_givenA4_T` — proved in Lean (module `lean4/Fifth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)

### `lean4/Fifth/State.lean`

- `H3V7N5QF:lean4/Fifth/State.lean::merge_eq_left_iff` — proved in Lean (module `lean4/Fifth/State.lean`; axioms: propext; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fifth/Reach.lean`

- `H3V7N5QF:lean4/Fifth/Reach.lean::merge_names` — proved in Lean (module `lean4/Fifth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fifth/Rename.lean`

- `H3V7N5QF:lean4/Fifth/Rename.lean::merge_perm` — proved in Lean (module `lean4/Fifth/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fifth/Reach.lean`

- `H3V7N5QF:lean4/Fifth/Reach.lean::merged_never_apart` — proved in Lean (module `lean4/Fifth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fifth/Cost.lean`

- `H3V7N5QF:lean4/Fifth/Cost.lean::miss5_le_of_le` — proved in Lean (module `lean4/Fifth/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fifth/Reach.lean`

- `H3V7N5QF:lean4/Fifth/Reach.lean::move_a_pair` — proved in Lean (module `lean4/Fifth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/Reach.lean::move_b_pair` — proved in Lean (module `lean4/Fifth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/Reach.lean::move_one` — proved in Lean (module `lean4/Fifth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/Reach.lean::no_return_fails` — proved in Lean (module `lean4/Fifth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fifth/Answers.lean`

- `H3V7N5QF:lean4/Fifth/Answers.lean::obstruction_persists5` — proved in Lean (module `lean4/Fifth/Answers.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fifth/Cost.lean`

- `H3V7N5QF:lean4/Fifth/Cost.lean::oneTerm4_contains` — proved in Lean (module `lean4/Fifth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/Cost.lean::costA_le` — proved in Lean (module `lean4/Fifth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/Cost.lean::costB_le` — proved in Lean (module `lean4/Fifth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fifth/Reach.lean`

- `H3V7N5QF:lean4/Fifth/Reach.lean::cycles` — proved in Lean (module `lean4/Fifth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fifth/Step.lean`

- `H3V7N5QF:lean4/Fifth/Step.lean::eq_of_zero` — proved in Lean (module `lean4/Fifth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fifth/Rename.lean`

- `H3V7N5QF:lean4/Fifth/Rename.lean::rename` — proved in Lean (module `lean4/Fifth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fifth/Cost.lean`

- `H3V7N5QF:lean4/Fifth/Cost.lean::size_parity` — proved in Lean (module `lean4/Fifth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Sixth/Step.lean`

- `H3V7N5QF:lean4/Sixth/Step.lean::toReach6` — proved in Lean (module `lean4/Sixth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)

### `lean4/Fifth/Step.lean`

- `H3V7N5QF:lean4/Fifth/Step.lean::trans` — proved in Lean (module `lean4/Fifth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fifth/Reach.lean`

- `H3V7N5QF:lean4/Fifth/Reach.lean::unbounded` — proved in Lean (module `lean4/Fifth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/Reach.lean::reach5_back_A` — proved in Lean (module `lean4/Fifth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/Reach.lean::reach5_back_B` — proved in Lean (module `lean4/Fifth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/Reach.lean::reach5_clear` — proved in Lean (module `lean4/Fifth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/Reach.lean::reach5_collapse` — proved in Lean (module `lean4/Fifth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/Reach.lean::reach5_iff` — proved in Lean (module `lean4/Fifth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fifth/Answers.lean`

- `H3V7N5QF:lean4/Fifth/Answers.lean::reach5_lower` — proved in Lean (module `lean4/Fifth/Answers.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fifth/Reach.lean`

- `H3V7N5QF:lean4/Fifth/Reach.lean::reach5_of_names` — proved in Lean (module `lean4/Fifth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/Reach.lean::reach5_symm` — proved in Lean (module `lean4/Fifth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/Reach.lean::reach5_total` — proved in Lean (module `lean4/Fifth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fifth/Answers.lean`

- `H3V7N5QF:lean4/Fifth/Answers.lean::remove_answer5` — proved in Lean (module `lean4/Fifth/Answers.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fifth/Step.lean`

- `H3V7N5QF:lean4/Fifth/Step.lean::remove_legal` — proved in Lean (module `lean4/Fifth/Step.lean`; axioms: propext, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fifth/State.lean`

- `H3V7N5QF:lean4/Fifth/State.lean::remove_M_of_ne` — proved in Lean (module `lean4/Fifth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/State.lean::remove_M_self` — proved in Lean (module `lean4/Fifth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fifth/Answers.lean`

- `H3V7N5QF:lean4/Fifth/Answers.lean::remove_obstruction_first_or_last5` — proved in Lean (module `lean4/Fifth/Answers.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fifth/Cost.lean`

- `H3V7N5QF:lean4/Fifth/Cost.lean::removed_arb_contains` — proved in Lean (module `lean4/Fifth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fifth/Rename.lean`

- `H3V7N5QF:lean4/Fifth/Rename.lean::rename4_identify` — proved in Lean (module `lean4/Fifth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/Rename.lean::rename4_remove` — proved in Lean (module `lean4/Fifth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Fifth/Reach.lean`

- `H3V7N5QF:lean4/Fifth/Reach.lean::result5_iff_A` — proved in Lean (module `lean4/Fifth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/Reach.lean::result5_iff_B` — proved in Lean (module `lean4/Fifth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fifth/Compare.lean`

- `H3V7N5QF:lean4/Fifth/Compare.lean::results_extend_A` — proved in Lean (module `lean4/Fifth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/Compare.lean::results_extend_B` — proved in Lean (module `lean4/Fifth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/Compare.lean::results_grow` — proved in Lean (module `lean4/Fifth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fifth/Cost.lean`

- `H3V7N5QF:lean4/Fifth/Cost.lean::size_can_fall` — proved in Lean (module `lean4/Fifth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fifth/State.lean`

- `H3V7N5QF:lean4/Fifth/State.lean::size_identify` — proved in Lean (module `lean4/Fifth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/State.lean::size_remove` — proved in Lean (module `lean4/Fifth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fifth/Step.lean`

- `H3V7N5QF:lean4/Fifth/Step.lean::cases4` — proved in Lean (module `lean4/Fifth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fifth/Cost.lean`

- `H3V7N5QF:lean4/Fifth/Cost.lean::costA_le` — proved in Lean (module `lean4/Fifth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/Cost.lean::costB_le` — proved in Lean (module `lean4/Fifth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fifth/Rename.lean`

- `H3V7N5QF:lean4/Fifth/Rename.lean::rename` — proved in Lean (module `lean4/Fifth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fifth/Cost.lean`

- `H3V7N5QF:lean4/Fifth/Cost.lean::size_step` — proved in Lean (module `lean4/Fifth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fifth/Step.lean`

- `H3V7N5QF:lean4/Fifth/Step.lean::toStep` — proved in Lean (module `lean4/Fifth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Sixth/Step.lean`

- `H3V7N5QF:lean4/Sixth/Step.lean::toStep6` — proved in Lean (module `lean4/Sixth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)

### `lean4/Fifth/Answers.lean`

- `H3V7N5QF:lean4/Fifth/Answers.lean::toTry5` — proved in Lean (module `lean4/Fifth/Answers.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fifth/Cost.lean`

- `H3V7N5QF:lean4/Fifth/Cost.lean::step_remove_arb` — proved in Lean (module `lean4/Fifth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)

### `lean4/Fifth/State.lean`

- `H3V7N5QF:lean4/Fifth/State.lean::toSt_identify` — proved in Lean (module `lean4/Fifth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/State.lean::toSt_remove` — proved in Lean (module `lean4/Fifth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/State.lean::total_identify` — proved in Lean (module `lean4/Fifth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/State.lean::total_remove` — proved in Lean (module `lean4/Fifth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Fifth/Answers.lean`

- `H3V7N5QF:lean4/Fifth/Answers.lean::legal_iff` — proved in Lean (module `lean4/Fifth/Answers.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/Answers.lean::obstructed_iff` — proved in Lean (module `lean4/Fifth/Answers.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fifth/Answers.lean::step5_or_obstructed` — proved in Lean (module `lean4/Fifth/Answers.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Sixth/Step.lean`

- `H3V7N5QF:lean4/Sixth/Step.lean::toStep6` — proved in Lean (module `lean4/Sixth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)

### `lean4/Fifth/Reach.lean`

- `H3V7N5QF:lean4/Fifth/Reach.lean::two_names_to` — proved in Lean (module `lean4/Fifth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fourteenth/Compare.lean`

- `H3V7N5QF:lean4/Fourteenth/Compare.lean::add_remove` — proved in Lean (module `lean4/Fourteenth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourteenth/lean_axioms.txt`)

### `lean4/Fourteenth/Step.lean`

- `H3V7N5QF:lean4/Fourteenth/Step.lean::clearing_not_a_kind` — proved in Lean (module `lean4/Fourteenth/Step.lean`; axioms: none; recorded in `evidence/fourteenth/lean_axioms.txt`)

### `lean4/Fourteenth/Compare.lean`

- `H3V7N5QF:lean4/Fourteenth/Compare.lean::fewest_changes14` — proved in Lean (module `lean4/Fourteenth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourteenth/lean_axioms.txt`)

### `lean4/Fourteenth/Step.lean`

- `H3V7N5QF:lean4/Fourteenth/Step.lean::first_change_leftover` — proved in Lean (module `lean4/Fourteenth/Step.lean`; axioms: none; recorded in `evidence/fourteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourteenth/Step.lean::leftover_addAssertion` — proved in Lean (module `lean4/Fourteenth/Step.lean`; axioms: none; recorded in `evidence/fourteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourteenth/Step.lean::leftover_addTerm` — proved in Lean (module `lean4/Fourteenth/Step.lean`; axioms: none; recorded in `evidence/fourteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourteenth/Step.lean::leftover_identify` — proved in Lean (module `lean4/Fourteenth/Step.lean`; axioms: none; recorded in `evidence/fourteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourteenth/Step.lean::leftover_not_answer` — proved in Lean (module `lean4/Fourteenth/Step.lean`; axioms: propext; recorded in `evidence/fourteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourteenth/Step.lean::leftover_not_assertion` — proved in Lean (module `lean4/Fourteenth/Step.lean`; axioms: none; recorded in `evidence/fourteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourteenth/Step.lean::leftover_not_in_M` — proved in Lean (module `lean4/Fourteenth/Step.lean`; axioms: propext, Quot.sound; recorded in `evidence/fourteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourteenth/Step.lean::leftover_remove` — proved in Lean (module `lean4/Fourteenth/Step.lean`; axioms: none; recorded in `evidence/fourteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourteenth/Step.lean::leftover_remove_ne_nothing` — proved in Lean (module `lean4/Fourteenth/Step.lean`; axioms: none; recorded in `evidence/fourteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourteenth/Step.lean::leftover_remove_r_s` — proved in Lean (module `lean4/Fourteenth/Step.lean`; axioms: none; recorded in `evidence/fourteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourteenth/Step.lean::leftover_remove_r_s_twoBoth` — proved in Lean (module `lean4/Fourteenth/Step.lean`; axioms: none; recorded in `evidence/fourteenth/lean_axioms.txt`)

### `lean4/Fourteenth/Rename.lean`

- `H3V7N5QF:lean4/Fourteenth/Rename.lean::leftover_swap_addTerm` — proved in Lean (module `lean4/Fourteenth/Rename.lean`; axioms: none; recorded in `evidence/fourteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourteenth/Rename.lean::leftover_swap_remove` — proved in Lean (module `lean4/Fourteenth/Rename.lean`; axioms: none; recorded in `evidence/fourteenth/lean_axioms.txt`)

### `lean4/Fourteenth/Compare.lean`

- `H3V7N5QF:lean4/Fourteenth/Compare.lean::no_cross_constraint` — proved in Lean (module `lean4/Fourteenth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourteenth/Compare.lean::no_third_rel` — proved in Lean (module `lean4/Fourteenth/Compare.lean`; axioms: propext, Quot.sound; recorded in `evidence/fourteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourteenth/Compare.lean::r_leftover_is_s` — proved in Lean (module `lean4/Fourteenth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourteenth/Compare.lean::reach14_iff` — proved in Lean (module `lean4/Fourteenth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourteenth/Compare.lean::results_pair14` — proved in Lean (module `lean4/Fourteenth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourteenth/lean_axioms.txt`)

### `lean4/Fourteenth/Rename.lean`

- `H3V7N5QF:lean4/Fourteenth/Rename.lean::swap` — proved in Lean (module `lean4/Fourteenth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourteenth/lean_axioms.txt`)

### `lean4/Fourteenth/Compare.lean`

- `H3V7N5QF:lean4/Fourteenth/Compare.lean::tagged_cost_fails` — proved in Lean (module `lean4/Fourteenth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourteenth/Compare.lean::tagged_extra` — proved in Lean (module `lean4/Fourteenth/Compare.lean`; axioms: propext, Quot.sound; recorded in `evidence/fourteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourteenth/Compare.lean::tagged_one_nothing` — proved in Lean (module `lean4/Fourteenth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourteenth/lean_axioms.txt`)

### `lean4/Fourteenth/Step.lean`

- `H3V7N5QF:lean4/Fourteenth/Step.lean::twoBoth_remove_r` — proved in Lean (module `lean4/Fourteenth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourteenth/Step.lean::twoBoth_remove_s` — proved in Lean (module `lean4/Fourteenth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifteenth/lean_axioms.txt`)

### `lean4/Fourth/Answers.lean`

- `H3V7N5QF:lean4/Fourth/Answers.lean::addAssertion_again_unobstructed` — proved in Lean (module `lean4/Fourth/Answers.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fourth/Contain.lean`

- `H3V7N5QF:lean4/Fourth/Contain.lean::adding_xrx_always_obstructed4` — proved in Lean (module `lean4/Fourth/Contain.lean`; axioms: propext, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fourth/Answers.lean`

- `H3V7N5QF:lean4/Fourth/Answers.lean::addTerm_unobstructed4` — proved in Lean (module `lean4/Fourth/Answers.lean`; axioms: propext, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fourth/Compare.lean`

- `H3V7N5QF:lean4/Fourth/Compare.lean::antisymm_survives` — proved in Lean (module `lean4/Fourth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/Contain.lean`

- `H3V7N5QF:lean4/Fourth/Contain.lean::arb_twice` — proved in Lean (module `lean4/Fourth/Contain.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/Compare.lean`

- `H3V7N5QF:lean4/Fourth/Compare.lean::arb_twice_result` — proved in Lean (module `lean4/Fourth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/Answers.lean`

- `H3V7N5QF:lean4/Fourth/Answers.lean::build_answer4` — proved in Lean (module `lean4/Fourth/Answers.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/Answers.lean::build_answer4_reverse` — proved in Lean (module `lean4/Fourth/Answers.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fourth/Contain.lean`

- `H3V7N5QF:lean4/Fourth/Contain.lean::antisymm` — proved in Lean (module `lean4/Fourth/Contain.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/Contain.lean::refl` — proved in Lean (module `lean4/Fourth/Contain.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/Contain.lean::toSt` — proved in Lean (module `lean4/Fourth/Contain.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/Contain.lean::total_le` — proved in Lean (module `lean4/Fourth/Contain.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/Contain.lean::trans` — proved in Lean (module `lean4/Fourth/Contain.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/Compare.lean`

- `H3V7N5QF:lean4/Fourth/Compare.lean::contains4_iff_contains` — proved in Lean (module `lean4/Fourth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/Contain.lean`

- `H3V7N5QF:lean4/Fourth/Contain.lean::contains4_of_toSt` — proved in Lean (module `lean4/Fourth/Contain.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/Rename.lean`

- `H3V7N5QF:lean4/Fourth/Rename.lean::exists_writing` — proved in Lean (module `lean4/Fourth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/Cost.lean`

- `H3V7N5QF:lean4/Fourth/Cost.lean::fewest_changes4_A` — proved in Lean (module `lean4/Fourth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/Cost.lean::fewest_changes4_B` — proved in Lean (module `lean4/Fourth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/Rename.lean`

- `H3V7N5QF:lean4/Fourth/Rename.lean::fewest_changes4_every_writing_A` — proved in Lean (module `lean4/Fourth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/Rename.lean::fewest_changes4_every_writing_B` — proved in Lean (module `lean4/Fourth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/Cost.lean`

- `H3V7N5QF:lean4/Fourth/Cost.lean::fewest_changes4_lower_A` — proved in Lean (module `lean4/Fourth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/Cost.lean::fewest_changes4_lower_B` — proved in Lean (module `lean4/Fourth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/Cost.lean::fewest_changes4_upper_A` — proved in Lean (module `lean4/Fourth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/Cost.lean::fewest_changes4_upper_B` — proved in Lean (module `lean4/Fourth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/State.lean`

- `H3V7N5QF:lean4/Fourth/State.lean::givenA4_arb` — proved in Lean (module `lean4/Fourth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/State.lean::givenA4_bra` — proved in Lean (module `lean4/Fourth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/Cost.lean`

- `H3V7N5QF:lean4/Fourth/Cost.lean::givenA4_contains` — proved in Lean (module `lean4/Fourth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/State.lean`

- `H3V7N5QF:lean4/Fourth/State.lean::givenA4_legal` — proved in Lean (module `lean4/Fourth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/Cost.lean`

- `H3V7N5QF:lean4/Fourth/Cost.lean::givenA4_to_givenB4` — proved in Lean (module `lean4/Fourth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fourth/State.lean`

- `H3V7N5QF:lean4/Fourth/State.lean::givenA4_wf` — proved in Lean (module `lean4/Fourth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/State.lean::givenB4_arb` — proved in Lean (module `lean4/Fourth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/State.lean::givenB4_bra` — proved in Lean (module `lean4/Fourth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/Cost.lean`

- `H3V7N5QF:lean4/Fourth/Cost.lean::givenB4_contains` — proved in Lean (module `lean4/Fourth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/State.lean`

- `H3V7N5QF:lean4/Fourth/State.lean::givenB4_legal` — proved in Lean (module `lean4/Fourth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/Cost.lean`

- `H3V7N5QF:lean4/Fourth/Cost.lean::givenB4_never_givenA4` — proved in Lean (module `lean4/Fourth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fourth/State.lean`

- `H3V7N5QF:lean4/Fourth/State.lean::givenB4_wf` — proved in Lean (module `lean4/Fourth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/Rename.lean`

- `H3V7N5QF:lean4/Fourth/Rename.lean::legal_rename4` — proved in Lean (module `lean4/Fourth/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/Rename.lean::mem_rename4_T` — proved in Lean (module `lean4/Fourth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)

### `lean4/Fourth/State.lean`

- `H3V7N5QF:lean4/Fourth/State.lean::names_apart_of_legal` — proved in Lean (module `lean4/Fourth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fourth/Answers.lean`

- `H3V7N5QF:lean4/Fourth/Answers.lean::no_change_asserts_xrx4` — proved in Lean (module `lean4/Fourth/Answers.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/Step.lean`

- `H3V7N5QF:lean4/Fourth/Step.lean::ofSt_addAssertion` — proved in Lean (module `lean4/Fourth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/Step.lean::ofSt_addTerm` — proved in Lean (module `lean4/Fourth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/State.lean`

- `H3V7N5QF:lean4/Fourth/State.lean::ofSt_legal` — proved in Lean (module `lean4/Fourth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/State.lean::ofSt_simple` — proved in Lean (module `lean4/Fourth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/State.lean::ofSt_toSt` — proved in Lean (module `lean4/Fourth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/State.lean::ofSt_wf` — proved in Lean (module `lean4/Fourth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/Cost.lean`

- `H3V7N5QF:lean4/Fourth/Cost.lean::oneTerm_unreachable4_A` — proved in Lean (module `lean4/Fourth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/Cost.lean::oneTerm_unreachable4_B` — proved in Lean (module `lean4/Fourth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/Cost.lean::antisymm` — proved in Lean (module `lean4/Fourth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fourth/Contain.lean`

- `H3V7N5QF:lean4/Fourth/Contain.lean::arb_mult_le` — proved in Lean (module `lean4/Fourth/Contain.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/Contain.lean::asserted_persists` — proved in Lean (module `lean4/Fourth/Contain.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/Contain.lean::card_T_le` — proved in Lean (module `lean4/Fourth/Contain.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/Contain.lean::contains` — proved in Lean (module `lean4/Fourth/Contain.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/Step.lean`

- `H3V7N5QF:lean4/Fourth/Step.lean::eq_of_zero` — proved in Lean (module `lean4/Fourth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/Cost.lean`

- `H3V7N5QF:lean4/Fourth/Cost.lean::length_unique` — proved in Lean (module `lean4/Fourth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fourth/Contain.lean`

- `H3V7N5QF:lean4/Fourth/Contain.lean::mult_le` — proved in Lean (module `lean4/Fourth/Contain.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/Contain.lean::name_a` — proved in Lean (module `lean4/Fourth/Contain.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/Contain.lean::name_b` — proved in Lean (module `lean4/Fourth/Contain.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/Cost.lean`

- `H3V7N5QF:lean4/Fourth/Cost.lean::no_return` — proved in Lean (module `lean4/Fourth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/Rename.lean`

- `H3V7N5QF:lean4/Fourth/Rename.lean::rename` — proved in Lean (module `lean4/Fourth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/Step.lean`

- `H3V7N5QF:lean4/Fourth/Step.lean::simple_of_simple` — proved in Lean (module `lean4/Fourth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/Cost.lean`

- `H3V7N5QF:lean4/Fourth/Cost.lean::size_eq` — proved in Lean (module `lean4/Fourth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/Contain.lean`

- `H3V7N5QF:lean4/Fourth/Contain.lean::term_persists` — proved in Lean (module `lean4/Fourth/Contain.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/Step.lean`

- `H3V7N5QF:lean4/Fourth/Step.lean::toReach2` — proved in Lean (module `lean4/Fourth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fifth/Step.lean`

- `H3V7N5QF:lean4/Fifth/Step.lean::toReach5` — proved in Lean (module `lean4/Fifth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fourth/Contain.lean`

- `H3V7N5QF:lean4/Fourth/Contain.lean::total_le` — proved in Lean (module `lean4/Fourth/Contain.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/Step.lean`

- `H3V7N5QF:lean4/Fourth/Step.lean::trans` — proved in Lean (module `lean4/Fourth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/Contain.lean`

- `H3V7N5QF:lean4/Fourth/Contain.lean::xrx_still_obstructed` — proved in Lean (module `lean4/Fourth/Contain.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/Cost.lean`

- `H3V7N5QF:lean4/Fourth/Cost.lean::reach4_addTerms` — proved in Lean (module `lean4/Fourth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/Rename.lean`

- `H3V7N5QF:lean4/Fourth/Rename.lean::reach4_antisymm_writing` — proved in Lean (module `lean4/Fourth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/Cost.lean`

- `H3V7N5QF:lean4/Fourth/Cost.lean::reach4_by_additions` — proved in Lean (module `lean4/Fourth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/Cost.lean::reach4_givenA_contains` — proved in Lean (module `lean4/Fourth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/Compare.lean`

- `H3V7N5QF:lean4/Fourth/Compare.lean::reach4_givenA_iff` — proved in Lean (module `lean4/Fourth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/Cost.lean`

- `H3V7N5QF:lean4/Fourth/Cost.lean::reach4_givenA_two_terms` — proved in Lean (module `lean4/Fourth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/Cost.lean::reach4_givenB_contains` — proved in Lean (module `lean4/Fourth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/Compare.lean`

- `H3V7N5QF:lean4/Fourth/Compare.lean::reach4_givenB_iff` — proved in Lean (module `lean4/Fourth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/Cost.lean`

- `H3V7N5QF:lean4/Fourth/Cost.lean::reach4_givenB_two_terms` — proved in Lean (module `lean4/Fourth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/Cost.lean::reach4_iff` — proved in Lean (module `lean4/Fourth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fourth/Compare.lean`

- `H3V7N5QF:lean4/Fourth/Compare.lean::reach4_iff_reach2` — proved in Lean (module `lean4/Fourth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/Rename.lean`

- `H3V7N5QF:lean4/Fourth/Rename.lean::reach4_iff_some_writing` — proved in Lean (module `lean4/Fourth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/Cost.lean`

- `H3V7N5QF:lean4/Fourth/Cost.lean::reach4_of_contains` — proved in Lean (module `lean4/Fourth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/Cost.lean::reach4_raise` — proved in Lean (module `lean4/Fourth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/Rename.lean`

- `H3V7N5QF:lean4/Fourth/Rename.lean::rename4_addAssertion` — proved in Lean (module `lean4/Fourth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/Rename.lean::rename4_addTerm` — proved in Lean (module `lean4/Fourth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/Rename.lean::rename4_M` — proved in Lean (module `lean4/Fourth/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/Rename.lean::rename4_symm_apply` — proved in Lean (module `lean4/Fourth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/Rename.lean::result4_iff_A` — proved in Lean (module `lean4/Fourth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/Rename.lean::result4_iff_B` — proved in Lean (module `lean4/Fourth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/Compare.lean`

- `H3V7N5QF:lean4/Fourth/Compare.lean::results_extend` — proved in Lean (module `lean4/Fourth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/Compare.lean::results_extend_B` — proved in Lean (module `lean4/Fourth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/Rename.lean`

- `H3V7N5QF:lean4/Fourth/Rename.lean::simple_rename4` — proved in Lean (module `lean4/Fourth/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/State.lean`

- `H3V7N5QF:lean4/Fourth/State.lean::size_addAssertion` — proved in Lean (module `lean4/Fourth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/State.lean::size_addTerm` — proved in Lean (module `lean4/Fourth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/State.lean::size_givenA4` — proved in Lean (module `lean4/Fourth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/State.lean::size_givenB4` — proved in Lean (module `lean4/Fourth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/Compare.lean`

- `H3V7N5QF:lean4/Fourth/Compare.lean::size_ofSt` — proved in Lean (module `lean4/Fourth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/Rename.lean`

- `H3V7N5QF:lean4/Fourth/Rename.lean::size_rename4` — proved in Lean (module `lean4/Fourth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fourth/State.lean`

- `H3V7N5QF:lean4/Fourth/State.lean::size_toSt` — proved in Lean (module `lean4/Fourth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/Contain.lean`

- `H3V7N5QF:lean4/Fourth/Contain.lean::contains` — proved in Lean (module `lean4/Fourth/Contain.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fourth/Step.lean`

- `H3V7N5QF:lean4/Fourth/Step.lean::mult_zero_of_simple` — proved in Lean (module `lean4/Fourth/Step.lean`; axioms: propext, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/Rename.lean`

- `H3V7N5QF:lean4/Fourth/Rename.lean::rename` — proved in Lean (module `lean4/Fourth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fourth/Step.lean`

- `H3V7N5QF:lean4/Fourth/Step.lean::simple_of_simple` — proved in Lean (module `lean4/Fourth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/Cost.lean`

- `H3V7N5QF:lean4/Fourth/Cost.lean::size_eq` — proved in Lean (module `lean4/Fourth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/Step.lean`

- `H3V7N5QF:lean4/Fourth/Step.lean::toStep2` — proved in Lean (module `lean4/Fourth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fifth/Step.lean`

- `H3V7N5QF:lean4/Fifth/Step.lean::toStep5` — proved in Lean (module `lean4/Fifth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Fourth/Answers.lean`

- `H3V7N5QF:lean4/Fourth/Answers.lean::toTry4` — proved in Lean (module `lean4/Fourth/Answers.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/Step.lean`

- `H3V7N5QF:lean4/Fourth/Step.lean::toSt_addAssertion` — proved in Lean (module `lean4/Fourth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/Step.lean::toSt_addTerm` — proved in Lean (module `lean4/Fourth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/State.lean`

- `H3V7N5QF:lean4/Fourth/State.lean::toSt_givenA4` — proved in Lean (module `lean4/Fourth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/State.lean::toSt_givenB4` — proved in Lean (module `lean4/Fourth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/State.lean::toSt_legal` — proved in Lean (module `lean4/Fourth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/State.lean::toSt_ofSt` — proved in Lean (module `lean4/Fourth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/State.lean::toSt_wf` — proved in Lean (module `lean4/Fourth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/State.lean::total_addAssertion` — proved in Lean (module `lean4/Fourth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/State.lean::total_addTerm` — proved in Lean (module `lean4/Fourth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Fourth/Rename.lean`

- `H3V7N5QF:lean4/Fourth/Rename.lean::total_rename4` — proved in Lean (module `lean4/Fourth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Fourth/Cost.lean`

- `H3V7N5QF:lean4/Fourth/Cost.lean::total_widen` — proved in Lean (module `lean4/Fourth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/Answers.lean`

- `H3V7N5QF:lean4/Fourth/Answers.lean::legal_iff` — proved in Lean (module `lean4/Fourth/Answers.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/Answers.lean::obstructed_iff` — proved in Lean (module `lean4/Fourth/Answers.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/Answers.lean::step4_or_xrx` — proved in Lean (module `lean4/Fourth/Answers.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/Answers.lean::two_sequences4` — proved in Lean (module `lean4/Fourth/Answers.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Fourth/Answers.lean::two_sequences_counted` — proved in Lean (module `lean4/Fourth/Answers.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/Rename.lean`

- `H3V7N5QF:lean4/Fourth/Rename.lean::wf_rename4` — proved in Lean (module `lean4/Fourth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Fourth/Answers.lean`

- `H3V7N5QF:lean4/Fourth/Answers.lean::xrx_outcome_unreachable4` — proved in Lean (module `lean4/Fourth/Answers.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/H3V7N5QF/Basic.lean`

- `H3V7N5QF:lean4/H3V7N5QF/Basic.lean::given_distinct` — proved in Lean (module `lean4/H3V7N5QF/Basic.lean`; axioms: none; recorded in `evidence/lean_axioms.txt`)

### `lean4/H3V7N5QF/Paths.lean`

- `H3V7N5QF:lean4/H3V7N5QF/Paths.lean::given_terms_subset` — proved in Lean (module `lean4/H3V7N5QF/Paths.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/H3V7N5QF/Cost.lean`

- `H3V7N5QF:lean4/H3V7N5QF/Cost.lean::givenA_to_givenB` — proved in Lean (module `lean4/H3V7N5QF/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/lean_axioms.txt`)

### `lean4/H3V7N5QF/Paths.lean`

- `H3V7N5QF:lean4/H3V7N5QF/Paths.lean::givenA_to_oneTerm` — proved in Lean (module `lean4/H3V7N5QF/Paths.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/lean_axioms.txt`)

### `lean4/H3V7N5QF/Cost.lean`

- `H3V7N5QF:lean4/H3V7N5QF/Cost.lean::givenB_to_givenA` — proved in Lean (module `lean4/H3V7N5QF/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/lean_axioms.txt`)

### `lean4/H3V7N5QF/Paths.lean`

- `H3V7N5QF:lean4/H3V7N5QF/Paths.lean::givenB_to_oneTerm` — proved in Lean (module `lean4/H3V7N5QF/Paths.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/lean_axioms.txt`)

### `lean4/H3V7N5QF/Basic.lean`

- `H3V7N5QF:lean4/H3V7N5QF/Basic.lean::identification_obstructed_iff` — proved in Lean (module `lean4/H3V7N5QF/Basic.lean`; axioms: propext; recorded in `evidence/lean_axioms.txt`)

### `lean4/H3V7N5QF/Finite.lean`

- `H3V7N5QF:lean4/H3V7N5QF/Finite.lean::identify_legal_iff` — proved in Lean (module `lean4/H3V7N5QF/Finite.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/lean_axioms.txt`)

### `lean4/H3V7N5QF/Basic.lean`

- `H3V7N5QF:lean4/H3V7N5QF/Basic.lean::image_loop_iff` — proved in Lean (module `lean4/H3V7N5QF/Basic.lean`; axioms: none; recorded in `evidence/lean_axioms.txt`)
- `H3V7N5QF:lean4/H3V7N5QF/Basic.lean::merge_eq_merge` — proved in Lean (module `lean4/H3V7N5QF/Basic.lean`; axioms: none; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/H3V7N5QF/Finite.lean`

- `H3V7N5QF:lean4/H3V7N5QF/Finite.lean::merge_mem_erase` — proved in Lean (module `lean4/H3V7N5QF/Finite.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)

### `lean4/Nineteenth/Partial.lean`

- `H3V7N5QF:lean4/Nineteenth/Partial.lean::cooccur_is_loop` — proved in Lean (module `lean4/Nineteenth/Partial.lean`; axioms: propext; recorded in `evidence/nineteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Nineteenth/Partial.lean::identify_smaller` — proved in Lean (module `lean4/Nineteenth/Partial.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/nineteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Nineteenth/Partial.lean::oneTerm_unreachable` — proved in Lean (module `lean4/Nineteenth/Partial.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/nineteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Nineteenth/Partial.lean::performPartial_terms` — proved in Lean (module `lean4/Nineteenth/Partial.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/nineteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Nineteenth/Partial.lean::card_ge` — proved in Lean (module `lean4/Nineteenth/Partial.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/nineteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Nineteenth/Partial.lean::card_ge` — proved in Lean (module `lean4/Nineteenth/Partial.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/nineteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Nineteenth/Partial.lean::side_not_identify` — proved in Lean (module `lean4/Nineteenth/Partial.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/nineteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Nineteenth/Partial.lean::side_partial_eq` — proved in Lean (module `lean4/Nineteenth/Partial.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/nineteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Nineteenth/Partial.lean::side_partial_legal` — proved in Lean (module `lean4/Nineteenth/Partial.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/nineteenth/lean_axioms.txt`)

### `lean4/Sixteenth/Step.lean`

- `H3V7N5QF:lean4/Sixteenth/Step.lean::embed` — proved in Lean (module `lean4/Sixteenth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixteenth/Step.lean::embed` — proved in Lean (module `lean4/Sixteenth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)

### `lean4/Ninth/State.lean`

- `H3V7N5QF:lean4/Ninth/State.lean::addTerm9_wf` — proved in Lean (module `lean4/Ninth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Ninth/Reach.lean`

- `H3V7N5QF:lean4/Ninth/Reach.lean::antisymm_fails9` — proved in Lean (module `lean4/Ninth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Ninth/Cost.lean`

- `H3V7N5QF:lean4/Ninth/Cost.lean::cost_adds_up9` — proved in Lean (module `lean4/Ninth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/Cost.lean::cost_adds_up9_swapped` — proved in Lean (module `lean4/Ninth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/Cost.lean::cost_not_sum_of_parts9` — proved in Lean (module `lean4/Ninth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/Cost.lean::cost_oneTerm9` — proved in Lean (module `lean4/Ninth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Ninth/Compare.lean`

- `H3V7N5QF:lean4/Ninth/Compare.lean::cost_survives7` — proved in Lean (module `lean4/Ninth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/Compare.lean::costA8_oneTerm9` — proved in Lean (module `lean4/Ninth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/Compare.lean::criterion_survives7` — proved in Lean (module `lean4/Ninth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/Compare.lean::criterion_survives8` — proved in Lean (module `lean4/Ninth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Ninth/Reach.lean`

- `H3V7N5QF:lean4/Ninth/Reach.lean::cycle2_9` — proved in Lean (module `lean4/Ninth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Ninth/Compare.lean`

- `H3V7N5QF:lean4/Ninth/Compare.lean::eighth_cost_fails` — proved in Lean (module `lean4/Ninth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/Compare.lean::eighth_never_empty` — proved in Lean (module `lean4/Ninth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Ninth/Reach.lean`

- `H3V7N5QF:lean4/Ninth/Reach.lean::empty9_is_a_result` — proved in Lean (module `lean4/Ninth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Ninth/Compare.lean`

- `H3V7N5QF:lean4/Ninth/Compare.lean::empty9_is_new` — proved in Lean (module `lean4/Ninth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Ninth/Reach.lean`

- `H3V7N5QF:lean4/Ninth/Reach.lean::empty9_never_returned` — proved in Lean (module `lean4/Ninth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Ninth/State.lean`

- `H3V7N5QF:lean4/Ninth/State.lean::empty9_not_nonempty` — proved in Lean (module `lean4/Ninth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/State.lean::empty9_size` — proved in Lean (module `lean4/Ninth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/State.lean::empty9_wf` — proved in Lean (module `lean4/Ninth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/State.lean::eq_empty9_of_wf` — proved in Lean (module `lean4/Ninth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/State.lean::eq_ofR9_of_nothing_in_s` — proved in Lean (module `lean4/Ninth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Ninth/Compare.lean`

- `H3V7N5QF:lean4/Ninth/Compare.lean::exchange_symmetry9` — proved in Lean (module `lean4/Ninth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Ninth/State.lean`

- `H3V7N5QF:lean4/Ninth/State.lean::ext_proj9` — proved in Lean (module `lean4/Ninth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Ninth/Cost.lean`

- `H3V7N5QF:lean4/Ninth/Cost.lean::fewest_changes9` — proved in Lean (module `lean4/Ninth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eleventh/lean_axioms.txt`)

### `lean4/Ninth/Rename.lean`

- `H3V7N5QF:lean4/Ninth/Rename.lean::fewest_changes9_every_writing` — proved in Lean (module `lean4/Ninth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Ninth/Cost.lean`

- `H3V7N5QF:lean4/Ninth/Cost.lean::fewest_changes9_lower` — proved in Lean (module `lean4/Ninth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Ninth/Step.lean`

- `H3V7N5QF:lean4/Ninth/Step.lean::first_change_adds_term9` — proved in Lean (module `lean4/Ninth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Ninth/State.lean`

- `H3V7N5QF:lean4/Ninth/State.lean::forget9_addAssertion` — proved in Lean (module `lean4/Ninth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/State.lean::forget9_addTerm` — proved in Lean (module `lean4/Ninth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/State.lean::forget9_identify` — proved in Lean (module `lean4/Ninth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/State.lean::forget9_remove` — proved in Lean (module `lean4/Ninth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/State.lean::forget_name9` — proved in Lean (module `lean4/Ninth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Ninth/Rename.lean`

- `H3V7N5QF:lean4/Ninth/Rename.lean::forget_rename8` — proved in Lean (module `lean4/Ninth/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Ninth/State.lean`

- `H3V7N5QF:lean4/Ninth/State.lean::identify_zero9` — proved in Lean (module `lean4/Ninth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Ninth/Compare.lean`

- `H3V7N5QF:lean4/Ninth/Compare.lean::interaction9` — proved in Lean (module `lean4/Ninth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Ninth/Reach.lean`

- `H3V7N5QF:lean4/Ninth/Reach.lean::length_not_unique9` — proved in Lean (module `lean4/Ninth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Ninth/State.lean`

- `H3V7N5QF:lean4/Ninth/State.lean::name9_addAssertion` — proved in Lean (module `lean4/Ninth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/State.lean::name9_addTerm` — proved in Lean (module `lean4/Ninth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/State.lean::name9_identify` — proved in Lean (module `lean4/Ninth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/State.lean::name9_names_one_term` — proved in Lean (module `lean4/Ninth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/State.lean::name9_remove` — proved in Lean (module `lean4/Ninth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/State.lean::name9_wf` — proved in Lean (module `lean4/Ninth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Ninth/Compare.lean`

- `H3V7N5QF:lean4/Ninth/Compare.lean::names_merged_vacuous9` — proved in Lean (module `lean4/Ninth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Ninth/Reach.lean`

- `H3V7N5QF:lean4/Ninth/Reach.lean::no_cycle_at_empty9` — proved in Lean (module `lean4/Ninth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/Reach.lean::no_return_fails9` — proved in Lean (module `lean4/Ninth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Ninth/State.lean`

- `H3V7N5QF:lean4/Ninth/State.lean::ofR9_addAssertion` — proved in Lean (module `lean4/Ninth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/State.lean::ofR9_addTerm` — proved in Lean (module `lean4/Ninth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/State.lean::ofR9_empty` — proved in Lean (module `lean4/Ninth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/State.lean::ofR9_identify` — proved in Lean (module `lean4/Ninth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/State.lean::ofR9_nothing_in_s` — proved in Lean (module `lean4/Ninth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/State.lean::ofR9_remove` — proved in Lean (module `lean4/Ninth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/State.lean::ofR9_wf` — proved in Lean (module `lean4/Ninth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Ninth/Cost.lean`

- `H3V7N5QF:lean4/Ninth/Cost.lean::one_term_parts9` — proved in Lean (module `lean4/Ninth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Ninth/State.lean`

- `H3V7N5QF:lean4/Ninth/State.lean::oneTerm9_wf` — proved in Lean (module `lean4/Ninth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/State.lean::proj9_addAssertion_other` — proved in Lean (module `lean4/Ninth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/State.lean::proj9_addAssertion_self` — proved in Lean (module `lean4/Ninth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/State.lean::proj9_addTerm` — proved in Lean (module `lean4/Ninth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/State.lean::proj9_identify` — proved in Lean (module `lean4/Ninth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/State.lean::proj9_remove_other` — proved in Lean (module `lean4/Ninth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/State.lean::proj9_remove_self` — proved in Lean (module `lean4/Ninth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/State.lean::proj9_swap` — proved in Lean (module `lean4/Ninth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/State.lean::proj_forget9` — proved in Lean (module `lean4/Ninth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/State.lean::proj_name9` — proved in Lean (module `lean4/Ninth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/State.lean::proj_ofR9_false` — proved in Lean (module `lean4/Ninth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/State.lean::proj_ofR9_true` — proved in Lean (module `lean4/Ninth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Ninth/Rename.lean`

- `H3V7N5QF:lean4/Ninth/Rename.lean::proj_rename9` — proved in Lean (module `lean4/Ninth/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Ninth/Compare.lean`

- `H3V7N5QF:lean4/Ninth/Compare.lean::proj_results9` — proved in Lean (module `lean4/Ninth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Ninth/Reach.lean`

- `H3V7N5QF:lean4/Ninth/Reach.lean::cycles` — proved in Lean (module `lean4/Ninth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Ninth/Step.lean`

- `H3V7N5QF:lean4/Ninth/Step.lean::eq_of_zero` — proved in Lean (module `lean4/Ninth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/Step.lean::name` — proved in Lean (module `lean4/Ninth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/Step.lean::proj` — proved in Lean (module `lean4/Ninth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Ninth/Rename.lean`

- `H3V7N5QF:lean4/Ninth/Rename.lean::rename` — proved in Lean (module `lean4/Ninth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Ninth/Cost.lean`

- `H3V7N5QF:lean4/Ninth/Cost.lean::size_le` — proved in Lean (module `lean4/Ninth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/Cost.lean::size_parity` — proved in Lean (module `lean4/Ninth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Ninth/Step.lean`

- `H3V7N5QF:lean4/Ninth/Step.lean::swap` — proved in Lean (module `lean4/Ninth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/Step.lean::trans` — proved in Lean (module `lean4/Ninth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Ninth/Reach.lean`

- `H3V7N5QF:lean4/Ninth/Reach.lean::unbounded` — proved in Lean (module `lean4/Ninth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Ninth/Cost.lean`

- `H3V7N5QF:lean4/Ninth/Cost.lean::reach9_addTerms` — proved in Lean (module `lean4/Ninth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/Cost.lean::reach9_by_additions` — proved in Lean (module `lean4/Ninth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Ninth/Step.lean`

- `H3V7N5QF:lean4/Ninth/Step.lean::reach9_empty_iff` — proved in Lean (module `lean4/Ninth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Ninth/Reach.lean`

- `H3V7N5QF:lean4/Ninth/Reach.lean::reach9_iff` — proved in Lean (module `lean4/Ninth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eleventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/Reach.lean::reach9_of_nonempty` — proved in Lean (module `lean4/Ninth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Ninth/Cost.lean`

- `H3V7N5QF:lean4/Ninth/Cost.lean::reach9_raise` — proved in Lean (module `lean4/Ninth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Ninth/Reach.lean`

- `H3V7N5QF:lean4/Ninth/Reach.lean::reach9_swap` — proved in Lean (module `lean4/Ninth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/Reach.lean::reach9_symm` — proved in Lean (module `lean4/Ninth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/Reach.lean::reach9_total` — proved in Lean (module `lean4/Ninth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Ninth/Rename.lean`

- `H3V7N5QF:lean4/Ninth/Rename.lean::rename8_name` — proved in Lean (module `lean4/Ninth/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/Rename.lean::rename9_addAssertion` — proved in Lean (module `lean4/Ninth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/Rename.lean::rename9_addTerm` — proved in Lean (module `lean4/Ninth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/Rename.lean::rename9_empty` — proved in Lean (module `lean4/Ninth/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/Rename.lean::rename9_identify` — proved in Lean (module `lean4/Ninth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/Rename.lean::rename9_remove` — proved in Lean (module `lean4/Ninth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/Rename.lean::rename9_swap` — proved in Lean (module `lean4/Ninth/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Ninth/Reach.lean`

- `H3V7N5QF:lean4/Ninth/Reach.lean::result9_iff` — proved in Lean (module `lean4/Ninth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/Reach.lean::result9_swap` — proved in Lean (module `lean4/Ninth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Ninth/Compare.lean`

- `H3V7N5QF:lean4/Ninth/Compare.lean::results_forget8_A` — proved in Lean (module `lean4/Ninth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/Compare.lean::results_forget8_B` — proved in Lean (module `lean4/Ninth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/Compare.lean::results_name8` — proved in Lean (module `lean4/Ninth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/Compare.lean::results_ofR7` — proved in Lean (module `lean4/Ninth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Ninth/Reach.lean`

- `H3V7N5QF:lean4/Ninth/Reach.lean::results_pair9` — proved in Lean (module `lean4/Ninth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eleventh/lean_axioms.txt`)

### `lean4/Ninth/Compare.lean`

- `H3V7N5QF:lean4/Ninth/Compare.lean::results_r_iff9` — proved in Lean (module `lean4/Ninth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/Compare.lean::results_s_iff9` — proved in Lean (module `lean4/Ninth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Ninth/Cost.lean`

- `H3V7N5QF:lean4/Ninth/Cost.lean::shortest_are_additions9` — proved in Lean (module `lean4/Ninth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Ninth/State.lean`

- `H3V7N5QF:lean4/Ninth/State.lean::size9_eq` — proved in Lean (module `lean4/Ninth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/State.lean::size9_swap` — proved in Lean (module `lean4/Ninth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/State.lean::size_addAssertion9` — proved in Lean (module `lean4/Ninth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/State.lean::size_addTerm9` — proved in Lean (module `lean4/Ninth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Ninth/Compare.lean`

- `H3V7N5QF:lean4/Ninth/Compare.lean::size_difference_survives9` — proved in Lean (module `lean4/Ninth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Ninth/State.lean`

- `H3V7N5QF:lean4/Ninth/State.lean::size_forget9` — proved in Lean (module `lean4/Ninth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/State.lean::size_identify9` — proved in Lean (module `lean4/Ninth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/State.lean::size_name9` — proved in Lean (module `lean4/Ninth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/State.lean::size_oneTerm9` — proved in Lean (module `lean4/Ninth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/State.lean::size_remove9` — proved in Lean (module `lean4/Ninth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Ninth/Rename.lean`

- `H3V7N5QF:lean4/Ninth/Rename.lean::size_rename9` — proved in Lean (module `lean4/Ninth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Sixteenth/Step.lean`

- `H3V7N5QF:lean4/Sixteenth/Step.lean::embed` — proved in Lean (module `lean4/Sixteenth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)

### `lean4/Ninth/Cost.lean`

- `H3V7N5QF:lean4/Ninth/Cost.lean::lowers_or_adds` — proved in Lean (module `lean4/Ninth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Ninth/Step.lean`

- `H3V7N5QF:lean4/Ninth/Step.lean::name` — proved in Lean (module `lean4/Ninth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/Step.lean::nonempty_out` — proved in Lean (module `lean4/Ninth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/Step.lean::proj` — proved in Lean (module `lean4/Ninth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Ninth/Rename.lean`

- `H3V7N5QF:lean4/Ninth/Rename.lean::rename` — proved in Lean (module `lean4/Ninth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Ninth/Cost.lean`

- `H3V7N5QF:lean4/Ninth/Cost.lean::size_step` — proved in Lean (module `lean4/Ninth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Ninth/Step.lean`

- `H3V7N5QF:lean4/Ninth/Step.lean::swap` — proved in Lean (module `lean4/Ninth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Ninth/State.lean`

- `H3V7N5QF:lean4/Ninth/State.lean::swap9_empty` — proved in Lean (module `lean4/Ninth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/State.lean::swap9_swap` — proved in Lean (module `lean4/Ninth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/State.lean::swap9_wf` — proved in Lean (module `lean4/Ninth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/State.lean::wf_forget9` — proved in Lean (module `lean4/Ninth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/State.lean::wf_of_name9` — proved in Lean (module `lean4/Ninth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Ninth/State.lean::wf_proj9` — proved in Lean (module `lean4/Ninth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Ninth/Rename.lean`

- `H3V7N5QF:lean4/Ninth/Rename.lean::wf_rename9` — proved in Lean (module `lean4/Ninth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/H3V7N5QF/Basic.lean`

- `H3V7N5QF:lean4/H3V7N5QF/Basic.lean::passing_on_refutes_bra` — proved in Lean (module `lean4/H3V7N5QF/Basic.lean`; axioms: none; recorded in `evidence/lean_axioms.txt`)

### `lean4/H3V7N5QF/Cost.lean`

- `H3V7N5QF:lean4/H3V7N5QF/Cost.lean::costA_le` — proved in Lean (module `lean4/H3V7N5QF/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/H3V7N5QF/Paths.lean`

- `H3V7N5QF:lean4/H3V7N5QF/Paths.lean::reach_by_edits` — proved in Lean (module `lean4/H3V7N5QF/Paths.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/lean_axioms.txt`)

### `lean4/H3V7N5QF/Answers.lean`

- `H3V7N5QF:lean4/H3V7N5QF/Answers.lean::remove_answer_one_way` — proved in Lean (module `lean4/H3V7N5QF/Answers.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/lean_axioms.txt`)
- `H3V7N5QF:lean4/H3V7N5QF/Answers.lean::remove_answer_two_way` — proved in Lean (module `lean4/H3V7N5QF/Answers.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/lean_axioms.txt`)

### `lean4/H3V7N5QF/Finite.lean`

- `H3V7N5QF:lean4/H3V7N5QF/Finite.lean::remove_legal` — proved in Lean (module `lean4/H3V7N5QF/Finite.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/lean_axioms.txt`)

### `lean4/H3V7N5QF/Answers.lean`

- `H3V7N5QF:lean4/H3V7N5QF/Answers.lean::remove_obstruction_first_or_last` — proved in Lean (module `lean4/H3V7N5QF/Answers.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/lean_axioms.txt`)

### `lean4/Second/Cost.lean`

- `H3V7N5QF:lean4/Second/Cost.lean::additions_count` — proved in Lean (module `lean4/Second/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Second/Answers.lean`

- `H3V7N5QF:lean4/Second/Answers.lean::build_answer3` — proved in Lean (module `lean4/Second/Answers.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/second/lean_axioms.txt`)
- `H3V7N5QF:lean4/Second/Answers.lean::build_answer3_reverse` — proved in Lean (module `lean4/Second/Answers.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/second/lean_axioms.txt`)

### `lean4/Second/Carry.lean`

- `H3V7N5QF:lean4/Second/Carry.lean::split` — proved in Lean (module `lean4/Second/Carry.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Second/Cost.lean`

- `H3V7N5QF:lean4/Second/Cost.lean::costA_eq_size_of_reach3` — proved in Lean (module `lean4/Second/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/second/lean_axioms.txt`)
- `H3V7N5QF:lean4/Second/Cost.lean::costB_eq_size_of_reach3` — proved in Lean (module `lean4/Second/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/second/lean_axioms.txt`)

### `lean4/Second/Rename.lean`

- `H3V7N5QF:lean4/Second/Rename.lean::exists_perm_of_ne` — proved in Lean (module `lean4/Second/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)

### `lean4/Second/Cost.lean`

- `H3V7N5QF:lean4/Second/Cost.lean::fewest_changes3_A` — proved in Lean (module `lean4/Second/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/second/lean_axioms.txt`)
- `H3V7N5QF:lean4/Second/Cost.lean::fewest_changes3_B` — proved in Lean (module `lean4/Second/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/second/lean_axioms.txt`)

### `lean4/Second/Rename.lean`

- `H3V7N5QF:lean4/Second/Rename.lean::fewest_changes3_every_writing_A` — proved in Lean (module `lean4/Second/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/second/lean_axioms.txt`)
- `H3V7N5QF:lean4/Second/Rename.lean::fewest_changes3_every_writing_B` — proved in Lean (module `lean4/Second/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/second/lean_axioms.txt`)

### `lean4/Second/Cost.lean`

- `H3V7N5QF:lean4/Second/Cost.lean::fewest_changes3_lower_A` — proved in Lean (module `lean4/Second/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/second/lean_axioms.txt`)
- `H3V7N5QF:lean4/Second/Cost.lean::fewest_changes3_lower_B` — proved in Lean (module `lean4/Second/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/second/lean_axioms.txt`)
- `H3V7N5QF:lean4/Second/Cost.lean::givenA_to_givenB3` — proved in Lean (module `lean4/Second/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/second/lean_axioms.txt`)
- `H3V7N5QF:lean4/Second/Cost.lean::givenB_never_givenA` — proved in Lean (module `lean4/Second/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Second/Rename.lean`

- `H3V7N5QF:lean4/Second/Rename.lean::legal_rename` — proved in Lean (module `lean4/Second/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)

### `lean4/Second/Cost.lean`

- `H3V7N5QF:lean4/Second/Cost.lean::lostA_eq_zero_of_reach3` — proved in Lean (module `lean4/Second/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/second/lean_axioms.txt`)
- `H3V7N5QF:lean4/Second/Cost.lean::lostB_eq_zero_of_reach3` — proved in Lean (module `lean4/Second/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/second/lean_axioms.txt`)
- `H3V7N5QF:lean4/Second/Cost.lean::oneTerm_unreachable_A` — proved in Lean (module `lean4/Second/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/second/lean_axioms.txt`)
- `H3V7N5QF:lean4/Second/Cost.lean::oneTerm_unreachable_B` — proved in Lean (module `lean4/Second/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/second/lean_axioms.txt`)

### `lean4/Second/Carry.lean`

- `H3V7N5QF:lean4/Second/Carry.lean::carries` — proved in Lean (module `lean4/Second/Carry.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/second/lean_axioms.txt`)

### `lean4/Second/Step.lean`

- `H3V7N5QF:lean4/Second/Step.lean::costA_le_inherited` — proved in Lean (module `lean4/Second/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/second/lean_axioms.txt`)
- `H3V7N5QF:lean4/Second/Step.lean::costB_le_inherited` — proved in Lean (module `lean4/Second/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/second/lean_axioms.txt`)

### `lean4/Second/Carry.lean`

- `H3V7N5QF:lean4/Second/Carry.lean::identify_images_obstructed` — proved in Lean (module `lean4/Second/Carry.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/second/lean_axioms.txt`)

### `lean4/Second/Rename.lean`

- `H3V7N5QF:lean4/Second/Rename.lean::rename` — proved in Lean (module `lean4/Second/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/second/lean_axioms.txt`)

### `lean4/Second/Cost.lean`

- `H3V7N5QF:lean4/Second/Cost.lean::size_le` — proved in Lean (module `lean4/Second/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/second/lean_axioms.txt`)

### `lean4/Second/Step.lean`

- `H3V7N5QF:lean4/Second/Step.lean::toReach` — proved in Lean (module `lean4/Second/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/second/lean_axioms.txt`)

### `lean4/Second/Cost.lean`

- `H3V7N5QF:lean4/Second/Cost.lean::reach3_by_additions` — proved in Lean (module `lean4/Second/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/second/lean_axioms.txt`)
- `H3V7N5QF:lean4/Second/Cost.lean::reach3_givenA_contains` — proved in Lean (module `lean4/Second/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/second/lean_axioms.txt`)
- `H3V7N5QF:lean4/Second/Cost.lean::reach3_givenA_two_terms` — proved in Lean (module `lean4/Second/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/second/lean_axioms.txt`)
- `H3V7N5QF:lean4/Second/Cost.lean::reach3_givenB_contains` — proved in Lean (module `lean4/Second/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/second/lean_axioms.txt`)
- `H3V7N5QF:lean4/Second/Cost.lean::reach3_givenB_two_terms` — proved in Lean (module `lean4/Second/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/second/lean_axioms.txt`)

### `lean4/Second/Answers.lean`

- `H3V7N5QF:lean4/Second/Answers.lean::removal_answer_outcome_unreachable` — proved in Lean (module `lean4/Second/Answers.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/second/lean_axioms.txt`)

### `lean4/Second/Rename.lean`

- `H3V7N5QF:lean4/Second/Rename.lean::rename_symm_apply` — proved in Lean (module `lean4/Second/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)
- `H3V7N5QF:lean4/Second/Rename.lean::result_iff_A` — proved in Lean (module `lean4/Second/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/second/lean_axioms.txt`)
- `H3V7N5QF:lean4/Second/Rename.lean::result_iff_B` — proved in Lean (module `lean4/Second/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/second/lean_axioms.txt`)

### `lean4/Second/Cost.lean`

- `H3V7N5QF:lean4/Second/Cost.lean::size_givenA` — proved in Lean (module `lean4/Second/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)
- `H3V7N5QF:lean4/Second/Cost.lean::size_givenB` — proved in Lean (module `lean4/Second/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)

### `lean4/Second/Rename.lean`

- `H3V7N5QF:lean4/Second/Rename.lean::size_rename` — proved in Lean (module `lean4/Second/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/second/lean_axioms.txt`)

### `lean4/Second/Step.lean`

- `H3V7N5QF:lean4/Second/Step.lean::remove_or_step3` — proved in Lean (module `lean4/Second/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/second/lean_axioms.txt`)

### `lean4/Second/Carry.lean`

- `H3V7N5QF:lean4/Second/Carry.lean::carries` — proved in Lean (module `lean4/Second/Carry.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/second/lean_axioms.txt`)

### `lean4/Second/Step.lean`

- `H3V7N5QF:lean4/Second/Step.lean::ne_remove` — proved in Lean (module `lean4/Second/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/second/lean_axioms.txt`)

### `lean4/Second/Rename.lean`

- `H3V7N5QF:lean4/Second/Rename.lean::rename` — proved in Lean (module `lean4/Second/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/second/lean_axioms.txt`)

### `lean4/Second/Cost.lean`

- `H3V7N5QF:lean4/Second/Cost.lean::size_le` — proved in Lean (module `lean4/Second/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/second/lean_axioms.txt`)

### `lean4/Second/Step.lean`

- `H3V7N5QF:lean4/Second/Step.lean::toStep` — proved in Lean (module `lean4/Second/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/second/lean_axioms.txt`)

### `lean4/Second/Rename.lean`

- `H3V7N5QF:lean4/Second/Rename.lean::wf_rename` — proved in Lean (module `lean4/Second/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)

### `lean4/Seventeenth/Perform.lean`

- `H3V7N5QF:lean4/Seventeenth/Perform.lean::add_ara_hasXrx` — proved in Lean (module `lean4/Seventeenth/Perform.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventeenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventeenth/Perform.lean::add_ara_not_unobstructed` — proved in Lean (module `lean4/Seventeenth/Perform.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventeenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventeenth/Perform.lean::add_ara_reach` — proved in Lean (module `lean4/Seventeenth/Perform.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventeenth/lean_axioms.txt`)

### `lean4/Seventeenth/Step.lean`

- `H3V7N5QF:lean4/Seventeenth/Step.lean::adding_xrx_obstructed` — proved in Lean (module `lean4/Seventeenth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventeenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventeenth/Step.lean::adding_xrx_step_obstructed` — proved in Lean (module `lean4/Seventeenth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventeenth/lean_axioms.txt`)

### `lean4/Seventeenth/Perform.lean`

- `H3V7N5QF:lean4/Seventeenth/Perform.lean::arb_not_gone` — proved in Lean (module `lean4/Seventeenth/Perform.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventeenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventeenth/Perform.lean::cost_not_lower_bound_A` — proved in Lean (module `lean4/Seventeenth/Perform.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventeenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventeenth/Perform.lean::cost_not_lower_bound_B` — proved in Lean (module `lean4/Seventeenth/Perform.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventeenth/lean_axioms.txt`)

### `lean4/Seventeenth/Embed.lean`

- `H3V7N5QF:lean4/Seventeenth/Embed.lean::fewest_changes17_A` — proved in Lean (module `lean4/Seventeenth/Embed.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventeenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventeenth/Embed.lean::fewest_changes17_B` — proved in Lean (module `lean4/Seventeenth/Embed.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventeenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventeenth/Embed.lean::fewest_changes17_lower_A` — proved in Lean (module `lean4/Seventeenth/Embed.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventeenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventeenth/Embed.lean::fewest_changes17_lower_B` — proved in Lean (module `lean4/Seventeenth/Embed.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventeenth/lean_axioms.txt`)

### `lean4/Seventeenth/State.lean`

- `H3V7N5QF:lean4/Seventeenth/State.lean::hasXrx_iff_not_legal` — proved in Lean (module `lean4/Seventeenth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventeenth/lean_axioms.txt`)

### `lean4/Seventeenth/Perform.lean`

- `H3V7N5QF:lean4/Seventeenth/Perform.lean::identify_givenA_reach` — proved in Lean (module `lean4/Seventeenth/Perform.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventeenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventeenth/Perform.lean::identify_givenA_step` — proved in Lean (module `lean4/Seventeenth/Perform.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventeenth/lean_axioms.txt`)

### `lean4/Seventeenth/Rename.lean`

- `H3V7N5QF:lean4/Seventeenth/Rename.lean::loopFree_rename` — proved in Lean (module `lean4/Seventeenth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventeenth/lean_axioms.txt`)

### `lean4/Seventeenth/Step.lean`

- `H3V7N5QF:lean4/Seventeenth/Step.lean::loopy_m1_allows` — proved in Lean (module `lean4/Seventeenth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventeenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventeenth/Step.lean::loopy_m2_obstructs` — proved in Lean (module `lean4/Seventeenth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventeenth/lean_axioms.txt`)

### `lean4/Seventeenth/State.lean`

- `H3V7N5QF:lean4/Seventeenth/State.lean::loopyWitness_hasXrx` — proved in Lean (module `lean4/Seventeenth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventeenth/lean_axioms.txt`)

### `lean4/Seventeenth/Step.lean`

- `H3V7N5QF:lean4/Seventeenth/Step.lean::m1_iff_m2_of_loopFree` — proved in Lean (module `lean4/Seventeenth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventeenth/lean_axioms.txt`)

### `lean4/Seventeenth/Perform.lean`

- `H3V7N5QF:lean4/Seventeenth/Perform.lean::mergedA_hasXrx` — proved in Lean (module `lean4/Seventeenth/Perform.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventeenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventeenth/Perform.lean::names_merged_with_loop` — proved in Lean (module `lean4/Seventeenth/Perform.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventeenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventeenth/Perform.lean::oneLoop_hasXrx` — proved in Lean (module `lean4/Seventeenth/Perform.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventeenth/lean_axioms.txt`)

### `lean4/Seventeenth/Answers.lean`

- `H3V7N5QF:lean4/Seventeenth/Answers.lean::perform_first_givenA` — proved in Lean (module `lean4/Seventeenth/Answers.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventeenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventeenth/Answers.lean::perform_first_intermediate_has_xrx` — proved in Lean (module `lean4/Seventeenth/Answers.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventeenth/lean_axioms.txt`)

### `lean4/Seventeenth/Embed.lean`

- `H3V7N5QF:lean4/Seventeenth/Embed.lean::toReach17` — proved in Lean (module `lean4/Seventeenth/Embed.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventeenth/lean_axioms.txt`)

### `lean4/Seventeenth/Step.lean`

- `H3V7N5QF:lean4/Seventeenth/Step.lean::loopFree` — proved in Lean (module `lean4/Seventeenth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventeenth/lean_axioms.txt`)

### `lean4/Seventeenth/Rename.lean`

- `H3V7N5QF:lean4/Seventeenth/Rename.lean::rename` — proved in Lean (module `lean4/Seventeenth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventeenth/lean_axioms.txt`)

### `lean4/Seventeenth/Embed.lean`

- `H3V7N5QF:lean4/Seventeenth/Embed.lean::toReach` — proved in Lean (module `lean4/Seventeenth/Embed.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventeenth/lean_axioms.txt`)

### `lean4/Seventeenth/Rename.lean`

- `H3V7N5QF:lean4/Seventeenth/Rename.lean::rename` — proved in Lean (module `lean4/Seventeenth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventeenth/lean_axioms.txt`)

### `lean4/Seventeenth/Answers.lean`

- `H3V7N5QF:lean4/Seventeenth/Answers.lean::remove_first_eq_perform_first` — proved in Lean (module `lean4/Seventeenth/Answers.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventeenth/lean_axioms.txt`)

### `lean4/Seventeenth/Embed.lean`

- `H3V7N5QF:lean4/Seventeenth/Embed.lean::toStep17` — proved in Lean (module `lean4/Seventeenth/Embed.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventeenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventeenth/Embed.lean::unobstructed17` — proved in Lean (module `lean4/Seventeenth/Embed.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventeenth/lean_axioms.txt`)

### `lean4/Seventeenth/Step.lean`

- `H3V7N5QF:lean4/Seventeenth/Step.lean::no_xrx_of_unobstructed` — proved in Lean (module `lean4/Seventeenth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventeenth/lean_axioms.txt`)

### `lean4/Seventeenth/Rename.lean`

- `H3V7N5QF:lean4/Seventeenth/Rename.lean::rename` — proved in Lean (module `lean4/Seventeenth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventeenth/lean_axioms.txt`)

### `lean4/Seventeenth/Embed.lean`

- `H3V7N5QF:lean4/Seventeenth/Embed.lean::toStep` — proved in Lean (module `lean4/Seventeenth/Embed.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventeenth/lean_axioms.txt`)

### `lean4/Seventh/Cost.lean`

- `H3V7N5QF:lean4/Seventh/Cost.lean::toStep7` — proved in Lean (module `lean4/Seventh/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventh/Cost.lean::toReach7` — proved in Lean (module `lean4/Seventh/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)

### `lean4/Seventh/State.lean`

- `H3V7N5QF:lean4/Seventh/State.lean::addTerm_wf` — proved in Lean (module `lean4/Seventh/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)

### `lean4/Seventh/Reach.lean`

- `H3V7N5QF:lean4/Seventh/Reach.lean::antisymm_fails7` — proved in Lean (module `lean4/Seventh/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)

### `lean4/Seventh/Cost.lean`

- `H3V7N5QF:lean4/Seventh/Cost.lean::name` — proved in Lean (module `lean4/Seventh/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventh/Cost.lean::cost_oneTerm` — proved in Lean (module `lean4/Seventh/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)

### `lean4/Seventh/Compare.lean`

- `H3V7N5QF:lean4/Seventh/Compare.lean::costA6_oneTerm7` — proved in Lean (module `lean4/Seventh/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventh/Compare.lean::criterion_survives` — proved in Lean (module `lean4/Seventh/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)

### `lean4/Seventh/Reach.lean`

- `H3V7N5QF:lean4/Seventh/Reach.lean::cycle2_7` — proved in Lean (module `lean4/Seventh/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventh/Reach.lean::empty_is_a_result` — proved in Lean (module `lean4/Seventh/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Seventh/Compare.lean`

- `H3V7N5QF:lean4/Seventh/Compare.lean::empty_is_new` — proved in Lean (module `lean4/Seventh/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)

### `lean4/Seventh/Reach.lean`

- `H3V7N5QF:lean4/Seventh/Reach.lean::empty_never_returned` — proved in Lean (module `lean4/Seventh/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Seventh/State.lean`

- `H3V7N5QF:lean4/Seventh/State.lean::empty_not_nonempty` — proved in Lean (module `lean4/Seventh/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventh/State.lean::empty_size` — proved in Lean (module `lean4/Seventh/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventh/State.lean::empty_wf` — proved in Lean (module `lean4/Seventh/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventh/State.lean::eq_empty_of_wf` — proved in Lean (module `lean4/Seventh/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)

### `lean4/Seventh/Cost.lean`

- `H3V7N5QF:lean4/Seventh/Cost.lean::fewest_changes7` — proved in Lean (module `lean4/Seventh/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Seventh/Rename.lean`

- `H3V7N5QF:lean4/Seventh/Rename.lean::fewest_changes7_every_writing` — proved in Lean (module `lean4/Seventh/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)

### `lean4/Seventh/Cost.lean`

- `H3V7N5QF:lean4/Seventh/Cost.lean::fewest_changes7_lower` — proved in Lean (module `lean4/Seventh/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)

### `lean4/Seventh/Step.lean`

- `H3V7N5QF:lean4/Seventh/Step.lean::first_change_adds_term` — proved in Lean (module `lean4/Seventh/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Seventh/State.lean`

- `H3V7N5QF:lean4/Seventh/State.lean::forget_addAssertion` — proved in Lean (module `lean4/Seventh/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventh/State.lean::forget_addTerm` — proved in Lean (module `lean4/Seventh/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventh/State.lean::forget_identify` — proved in Lean (module `lean4/Seventh/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventh/State.lean::forget_name` — proved in Lean (module `lean4/Seventh/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventh/State.lean::forget_remove` — proved in Lean (module `lean4/Seventh/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)

### `lean4/Seventh/Rename.lean`

- `H3V7N5QF:lean4/Seventh/Rename.lean::forget_rename4` — proved in Lean (module `lean4/Seventh/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)

### `lean4/Seventh/Reach.lean`

- `H3V7N5QF:lean4/Seventh/Reach.lean::identify_twoTerms7` — proved in Lean (module `lean4/Seventh/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventh/Reach.lean::length_not_unique7` — proved in Lean (module `lean4/Seventh/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)

### `lean4/Seventh/Rename.lean`

- `H3V7N5QF:lean4/Seventh/Rename.lean::mem_rename7_T` — proved in Lean (module `lean4/Seventh/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)

### `lean4/Seventh/State.lean`

- `H3V7N5QF:lean4/Seventh/State.lean::name_addAssertion` — proved in Lean (module `lean4/Seventh/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventh/State.lean::name_addTerm` — proved in Lean (module `lean4/Seventh/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventh/State.lean::name_identify` — proved in Lean (module `lean4/Seventh/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventh/State.lean::name_names_one_term` — proved in Lean (module `lean4/Seventh/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventh/State.lean::name_remove` — proved in Lean (module `lean4/Seventh/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventh/State.lean::name_wf` — proved in Lean (module `lean4/Seventh/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)

### `lean4/Seventh/Compare.lean`

- `H3V7N5QF:lean4/Seventh/Compare.lean::names_merged_vacuous` — proved in Lean (module `lean4/Seventh/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)

### `lean4/Seventh/Reach.lean`

- `H3V7N5QF:lean4/Seventh/Reach.lean::no_cycle_at_empty` — proved in Lean (module `lean4/Seventh/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventh/Reach.lean::no_return_fails7` — proved in Lean (module `lean4/Seventh/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)

### `lean4/Sixteenth/State.lean`

- `H3V7N5QF:lean4/Sixteenth/State.lean::identify_addTerm` — proved in Lean (module `lean4/Sixteenth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)

### `lean4/Seventh/Reach.lean`

- `H3V7N5QF:lean4/Seventh/Reach.lean::oneTerm7_wf` — proved in Lean (module `lean4/Seventh/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventh/Reach.lean::cycles` — proved in Lean (module `lean4/Seventh/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)

### `lean4/Seventh/Step.lean`

- `H3V7N5QF:lean4/Seventh/Step.lean::eq_of_zero` — proved in Lean (module `lean4/Seventh/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventh/Step.lean::name` — proved in Lean (module `lean4/Seventh/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)

### `lean4/Ninth/Step.lean`

- `H3V7N5QF:lean4/Ninth/Step.lean::ofR` — proved in Lean (module `lean4/Ninth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Seventh/Rename.lean`

- `H3V7N5QF:lean4/Seventh/Rename.lean::rename` — proved in Lean (module `lean4/Seventh/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)

### `lean4/Seventh/Cost.lean`

- `H3V7N5QF:lean4/Seventh/Cost.lean::size_le` — proved in Lean (module `lean4/Seventh/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventh/Cost.lean::size_parity` — proved in Lean (module `lean4/Seventh/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)

### `lean4/Seventh/Step.lean`

- `H3V7N5QF:lean4/Seventh/Step.lean::trans` — proved in Lean (module `lean4/Seventh/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)

### `lean4/Seventh/Reach.lean`

- `H3V7N5QF:lean4/Seventh/Reach.lean::unbounded` — proved in Lean (module `lean4/Seventh/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)

### `lean4/Seventh/Cost.lean`

- `H3V7N5QF:lean4/Seventh/Cost.lean::reach7_by_additions` — proved in Lean (module `lean4/Seventh/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)

### `lean4/Seventh/Step.lean`

- `H3V7N5QF:lean4/Seventh/Step.lean::reach7_empty_iff` — proved in Lean (module `lean4/Seventh/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)

### `lean4/Seventh/Reach.lean`

- `H3V7N5QF:lean4/Seventh/Reach.lean::reach7_iff` — proved in Lean (module `lean4/Seventh/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Seventh/Cost.lean`

- `H3V7N5QF:lean4/Seventh/Cost.lean::reach7_of_contains` — proved in Lean (module `lean4/Seventh/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)

### `lean4/Seventh/Reach.lean`

- `H3V7N5QF:lean4/Seventh/Reach.lean::reach7_of_nonempty` — proved in Lean (module `lean4/Seventh/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventh/Reach.lean::reach7_symm` — proved in Lean (module `lean4/Seventh/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventh/Reach.lean::reach7_total` — proved in Lean (module `lean4/Seventh/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)

### `lean4/Seventh/Rename.lean`

- `H3V7N5QF:lean4/Seventh/Rename.lean::rename4_name` — proved in Lean (module `lean4/Seventh/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventh/Rename.lean::rename7_addAssertion` — proved in Lean (module `lean4/Seventh/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventh/Rename.lean::rename7_addTerm` — proved in Lean (module `lean4/Seventh/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventh/Rename.lean::rename7_empty` — proved in Lean (module `lean4/Seventh/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventh/Rename.lean::rename7_identify` — proved in Lean (module `lean4/Seventh/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventh/Rename.lean::rename7_M` — proved in Lean (module `lean4/Seventh/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventh/Rename.lean::rename7_remove` — proved in Lean (module `lean4/Seventh/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)

### `lean4/Seventh/Reach.lean`

- `H3V7N5QF:lean4/Seventh/Reach.lean::result7_iff` — proved in Lean (module `lean4/Seventh/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Seventh/Compare.lean`

- `H3V7N5QF:lean4/Seventh/Compare.lean::results_forget_A` — proved in Lean (module `lean4/Seventh/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventh/Compare.lean::results_forget_B` — proved in Lean (module `lean4/Seventh/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventh/Compare.lean::results_name` — proved in Lean (module `lean4/Seventh/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)

### `lean4/Seventh/Cost.lean`

- `H3V7N5QF:lean4/Seventh/Cost.lean::shortest_are_additions` — proved in Lean (module `lean4/Seventh/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Seventh/Compare.lean`

- `H3V7N5QF:lean4/Seventh/Compare.lean::sixth_cost_fails` — proved in Lean (module `lean4/Seventh/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventh/Compare.lean::sixth_never_empty` — proved in Lean (module `lean4/Seventh/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)

### `lean4/Seventh/State.lean`

- `H3V7N5QF:lean4/Seventh/State.lean::size_addTerm7` — proved in Lean (module `lean4/Seventh/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)

### `lean4/Seventh/Compare.lean`

- `H3V7N5QF:lean4/Seventh/Compare.lean::size_difference_survives` — proved in Lean (module `lean4/Seventh/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)

### `lean4/Seventh/State.lean`

- `H3V7N5QF:lean4/Seventh/State.lean::size_forget` — proved in Lean (module `lean4/Seventh/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventh/State.lean::size_name` — proved in Lean (module `lean4/Seventh/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventh/State.lean::size_oneTerm7` — proved in Lean (module `lean4/Seventh/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)

### `lean4/Seventh/Rename.lean`

- `H3V7N5QF:lean4/Seventh/Rename.lean::size_rename7` — proved in Lean (module `lean4/Seventh/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)

### `lean4/Seventh/Cost.lean`

- `H3V7N5QF:lean4/Seventh/Cost.lean::lowers_or_adds` — proved in Lean (module `lean4/Seventh/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)

### `lean4/Seventh/Step.lean`

- `H3V7N5QF:lean4/Seventh/Step.lean::name` — proved in Lean (module `lean4/Seventh/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventh/Step.lean::nonempty_out` — proved in Lean (module `lean4/Seventh/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)

### `lean4/Ninth/Step.lean`

- `H3V7N5QF:lean4/Ninth/Step.lean::ofR` — proved in Lean (module `lean4/Ninth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/ninth/lean_axioms.txt`)

### `lean4/Seventh/Rename.lean`

- `H3V7N5QF:lean4/Seventh/Rename.lean::rename` — proved in Lean (module `lean4/Seventh/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)

### `lean4/Seventh/Cost.lean`

- `H3V7N5QF:lean4/Seventh/Cost.lean::size_step` — proved in Lean (module `lean4/Seventh/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventh/Cost.lean::step_first_term` — proved in Lean (module `lean4/Seventh/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)

### `lean4/Seventh/State.lean`

- `H3V7N5QF:lean4/Seventh/State.lean::total_addTerm7` — proved in Lean (module `lean4/Seventh/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventh/State.lean::wf_forget` — proved in Lean (module `lean4/Seventh/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Seventh/State.lean::wf_of_name` — proved in Lean (module `lean4/Seventh/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)

### `lean4/Seventh/Rename.lean`

- `H3V7N5QF:lean4/Seventh/Rename.lean::wf_rename7` — proved in Lean (module `lean4/Seventh/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)

### `lean4/Sixteenth/State.lean`

- `H3V7N5QF:lean4/Sixteenth/State.lean::add_remove_ne` — proved in Lean (module `lean4/Sixteenth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixteenth/State.lean::add_remove_st` — proved in Lean (module `lean4/Sixteenth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)

### `lean4/Sixteenth/Cost.lean`

- `H3V7N5QF:lean4/Sixteenth/Cost.lean::admission_costs_three` — proved in Lean (module `lean4/Sixteenth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)

### `lean4/Sixteenth/Compare.lean`

- `H3V7N5QF:lean4/Sixteenth/Compare.lean::clearing_is_a_kind16` — proved in Lean (module `lean4/Sixteenth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)

### `lean4/Sixteenth/Reach.lean`

- `H3V7N5QF:lean4/Sixteenth/Reach.lean::cycle2_16` — proved in Lean (module `lean4/Sixteenth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixteenth/Reach.lean::cycle2_assert16` — proved in Lean (module `lean4/Sixteenth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)

### `lean4/Sixteenth/Compare.lean`

- `H3V7N5QF:lean4/Sixteenth/Compare.lean::exchange_symmetry16` — proved in Lean (module `lean4/Sixteenth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)

### `lean4/Sixteenth/Cost.lean`

- `H3V7N5QF:lean4/Sixteenth/Cost.lean::fewest_changes16` — proved in Lean (module `lean4/Sixteenth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixteenth/Cost.lean::fewest_changes16_lower` — proved in Lean (module `lean4/Sixteenth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixteenth/Cost.lean::fewest_changes16_of_empty_record` — proved in Lean (module `lean4/Sixteenth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)

### `lean4/Sixteenth/Step.lean`

- `H3V7N5QF:lean4/Sixteenth/Step.lean::first_change_adds_term16` — proved in Lean (module `lean4/Sixteenth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)

### `lean4/Sixteenth/Reach.lean`

- `H3V7N5QF:lean4/Sixteenth/Reach.lean::has_term_criterion_fails16` — proved in Lean (module `lean4/Sixteenth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)

### `lean4/Sixteenth/State.lean`

- `H3V7N5QF:lean4/Sixteenth/State.lean::identify_addTerm16` — proved in Lean (module `lean4/Sixteenth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixteenth/State.lean::identify_addTerm9` — proved in Lean (module `lean4/Sixteenth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)

### `lean4/Sixteenth/Compare.lean`

- `H3V7N5QF:lean4/Sixteenth/Compare.lean::leftOne_is_new` — proved in Lean (module `lean4/Sixteenth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)

### `lean4/Sixteenth/State.lean`

- `H3V7N5QF:lean4/Sixteenth/State.lean::mass_addAssertion` — proved in Lean (module `lean4/Sixteenth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixteenth/State.lean::mass_addTerm` — proved in Lean (module `lean4/Sixteenth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixteenth/State.lean::mass_identify` — proved in Lean (module `lean4/Sixteenth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixteenth/State.lean::mass_remove` — proved in Lean (module `lean4/Sixteenth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)

### `lean4/Sixteenth/Cost.lean`

- `H3V7N5QF:lean4/Sixteenth/Cost.lean::ninth_cost_fails_off_empty_record` — proved in Lean (module `lean4/Sixteenth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)

### `lean4/Sixteenth/Compare.lean`

- `H3V7N5QF:lean4/Sixteenth/Compare.lean::ninth_round_survives` — proved in Lean (module `lean4/Sixteenth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)

### `lean4/Sixteenth/Cost.lean`

- `H3V7N5QF:lean4/Sixteenth/Cost.lean::no_fall_on_shortest16` — proved in Lean (module `lean4/Sixteenth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)

### `lean4/Sixteenth/Reach.lean`

- `H3V7N5QF:lean4/Sixteenth/Reach.lean::one_way16` — proved in Lean (module `lean4/Sixteenth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)

### `lean4/Sixteenth/State.lean`

- `H3V7N5QF:lean4/Sixteenth/State.lean::potential_addAssertion` — proved in Lean (module `lean4/Sixteenth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixteenth/State.lean::potential_addTerm` — proved in Lean (module `lean4/Sixteenth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixteenth/State.lean::potential_identify` — proved in Lean (module `lean4/Sixteenth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixteenth/State.lean::potential_remove` — proved in Lean (module `lean4/Sixteenth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixteenth/State.lean::potential_swap` — proved in Lean (module `lean4/Sixteenth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)

### `lean4/Sixteenth/Reach.lean`

- `H3V7N5QF:lean4/Sixteenth/Reach.lean::mass_le` — proved in Lean (module `lean4/Sixteenth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)

### `lean4/Sixteenth/Cost.lean`

- `H3V7N5QF:lean4/Sixteenth/Cost.lean::potential_le` — proved in Lean (module `lean4/Sixteenth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixteenth/Cost.lean::potential_parity` — proved in Lean (module `lean4/Sixteenth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)

### `lean4/Sixteenth/Step.lean`

- `H3V7N5QF:lean4/Sixteenth/Step.lean::proj` — proved in Lean (module `lean4/Sixteenth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixteenth/Step.lean::swap` — proved in Lean (module `lean4/Sixteenth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)

### `lean4/Sixteenth/Cost.lean`

- `H3V7N5QF:lean4/Sixteenth/Cost.lean::toReachD` — proved in Lean (module `lean4/Sixteenth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)

### `lean4/Sixteenth/Reach.lean`

- `H3V7N5QF:lean4/Sixteenth/Reach.lean::unbounded` — proved in Lean (module `lean4/Sixteenth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)

### `lean4/Sixteenth/Cost.lean`

- `H3V7N5QF:lean4/Sixteenth/Cost.lean::reach16_by_additions` — proved in Lean (module `lean4/Sixteenth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)

### `lean4/Sixteenth/Step.lean`

- `H3V7N5QF:lean4/Sixteenth/Step.lean::reach16_empty_iff` — proved in Lean (module `lean4/Sixteenth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)

### `lean4/Sixteenth/Cost.lean`

- `H3V7N5QF:lean4/Sixteenth/Cost.lean::reach16_record` — proved in Lean (module `lean4/Sixteenth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)

### `lean4/Sixteenth/Reach.lean`

- `H3V7N5QF:lean4/Sixteenth/Reach.lean::reach16_swap` — proved in Lean (module `lean4/Sixteenth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)

### `lean4/Sixteenth/Cost.lean`

- `H3V7N5QF:lean4/Sixteenth/Cost.lean::potential` — proved in Lean (module `lean4/Sixteenth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)

### `lean4/Sixteenth/Compare.lean`

- `H3V7N5QF:lean4/Sixteenth/Compare.lean::record_moved_only_by_removal_and_admission` — proved in Lean (module `lean4/Sixteenth/Compare.lean`; axioms: propext, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixteenth/Compare.lean::record_names_no_relation` — proved in Lean (module `lean4/Sixteenth/Compare.lean`; axioms: propext, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)

### `lean4/Sixteenth/State.lean`

- `H3V7N5QF:lean4/Sixteenth/State.lean::record_not_raised_by_addition` — proved in Lean (module `lean4/Sixteenth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixteenth/State.lean::remove_add9` — proved in Lean (module `lean4/Sixteenth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)

### `lean4/Sixteenth/Reach.lean`

- `H3V7N5QF:lean4/Sixteenth/Reach.lean::result16_iff` — proved in Lean (module `lean4/Sixteenth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixteenth/Reach.lean::result16_swap` — proved in Lean (module `lean4/Sixteenth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixteenth/Reach.lean::results_ninth_iff16` — proved in Lean (module `lean4/Sixteenth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixteenth/Reach.lean::results_pair16` — proved in Lean (module `lean4/Sixteenth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixteenth/Reach.lean::mass_le` — proved in Lean (module `lean4/Sixteenth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)

### `lean4/Sixteenth/Step.lean`

- `H3V7N5QF:lean4/Sixteenth/Step.lean::nonempty_out` — proved in Lean (module `lean4/Sixteenth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)

### `lean4/Sixteenth/Cost.lean`

- `H3V7N5QF:lean4/Sixteenth/Cost.lean::potential_step` — proved in Lean (module `lean4/Sixteenth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)

### `lean4/Sixteenth/Step.lean`

- `H3V7N5QF:lean4/Sixteenth/Step.lean::proj` — proved in Lean (module `lean4/Sixteenth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)

### `lean4/Sixteenth/Cost.lean`

- `H3V7N5QF:lean4/Sixteenth/Cost.lean::rise_or_fall` — proved in Lean (module `lean4/Sixteenth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)

### `lean4/Sixteenth/Step.lean`

- `H3V7N5QF:lean4/Sixteenth/Step.lean::swap` — proved in Lean (module `lean4/Sixteenth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixteenth/Step.lean::embed_identify` — proved in Lean (module `lean4/Sixteenth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixteenth/lean_axioms.txt`)

### `lean4/Sixth/Cost.lean`

- `H3V7N5QF:lean4/Sixth/Cost.lean::addAssertion_contains` — proved in Lean (module `lean4/Sixth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)

### `lean4/Sixth/Reach.lean`

- `H3V7N5QF:lean4/Sixth/Reach.lean::antisymm_fails6` — proved in Lean (module `lean4/Sixth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)

### `lean4/Sixth/Step.lean`

- `H3V7N5QF:lean4/Sixth/Step.lean::arb_gone_fails` — proved in Lean (module `lean4/Sixth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)

### `lean4/Sixth/Reach.lean`

- `H3V7N5QF:lean4/Sixth/Reach.lean::contains4_reach6` — proved in Lean (module `lean4/Sixth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)

### `lean4/Sixth/Compare.lean`

- `H3V7N5QF:lean4/Sixth/Compare.lean::cost_fails_names_merged` — proved in Lean (module `lean4/Sixth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)

### `lean4/Sixth/Cost.lean`

- `H3V7N5QF:lean4/Sixth/Cost.lean::cost_loopState` — proved in Lean (module `lean4/Sixth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)

### `lean4/Sixth/Compare.lean`

- `H3V7N5QF:lean4/Sixth/Compare.lean::cost_survives_names_apart` — proved in Lean (module `lean4/Sixth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixth/Compare.lean::cost_survives_on_legal` — proved in Lean (module `lean4/Sixth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)

### `lean4/Sixth/Cost.lean`

- `H3V7N5QF:lean4/Sixth/Cost.lean::costA6_eq_costA5_of_legal` — proved in Lean (module `lean4/Sixth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixth/Cost.lean::costA6_givenA4` — proved in Lean (module `lean4/Sixth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Sixth/Rename.lean`

- `H3V7N5QF:lean4/Sixth/Rename.lean::costA6_rename` — proved in Lean (module `lean4/Sixth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Sixth/Cost.lean`

- `H3V7N5QF:lean4/Sixth/Cost.lean::costB6_eq_costB5_of_legal` — proved in Lean (module `lean4/Sixth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixth/Cost.lean::costB6_givenB4` — proved in Lean (module `lean4/Sixth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Sixth/Rename.lean`

- `H3V7N5QF:lean4/Sixth/Rename.lean::costB6_rename` — proved in Lean (module `lean4/Sixth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Sixth/Reach.lean`

- `H3V7N5QF:lean4/Sixth/Reach.lean::criterion_not_containment` — proved in Lean (module `lean4/Sixth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)

### `lean4/Sixth/Compare.lean`

- `H3V7N5QF:lean4/Sixth/Compare.lean::criterion_survives` — proved in Lean (module `lean4/Sixth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)

### `lean4/Sixth/Reach.lean`

- `H3V7N5QF:lean4/Sixth/Reach.lean::cycle2_6` — proved in Lean (module `lean4/Sixth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)

### `lean4/Sixth/Cost.lean`

- `H3V7N5QF:lean4/Sixth/Cost.lean::fewest_changes6_A` — proved in Lean (module `lean4/Sixth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixth/Cost.lean::fewest_changes6_apart_A` — proved in Lean (module `lean4/Sixth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixth/Cost.lean::fewest_changes6_B` — proved in Lean (module `lean4/Sixth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Sixth/Rename.lean`

- `H3V7N5QF:lean4/Sixth/Rename.lean::fewest_changes6_every_writing_A` — proved in Lean (module `lean4/Sixth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixth/Rename.lean::fewest_changes6_every_writing_B` — proved in Lean (module `lean4/Sixth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)

### `lean4/Sixth/Cost.lean`

- `H3V7N5QF:lean4/Sixth/Cost.lean::fewest_changes6_lower_A` — proved in Lean (module `lean4/Sixth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixth/Cost.lean::fewest_changes6_lower_B` — proved in Lean (module `lean4/Sixth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixth/Cost.lean::fewest_changes6_of_contains_A` — proved in Lean (module `lean4/Sixth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixth/Cost.lean::fewest_changes6_of_contains_B` — proved in Lean (module `lean4/Sixth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixth/Cost.lean::fewest_changes6_of_legal_A` — proved in Lean (module `lean4/Sixth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixth/Cost.lean::fewest_changes6_of_legal_B` — proved in Lean (module `lean4/Sixth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixth/Cost.lean::fewest_changes6_upper_A_apart` — proved in Lean (module `lean4/Sixth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixth/Cost.lean::fewest_changes6_upper_A_merged` — proved in Lean (module `lean4/Sixth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixth/Cost.lean::fewest_changes6_upper_B_apart` — proved in Lean (module `lean4/Sixth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixth/Cost.lean::fewest_changes6_upper_B_merged` — proved in Lean (module `lean4/Sixth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixth/Cost.lean::fifth_potential_fails` — proved in Lean (module `lean4/Sixth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)

### `lean4/Sixth/Compare.lean`

- `H3V7N5QF:lean4/Sixth/Compare.lean::first_or_last_fails` — proved in Lean (module `lean4/Sixth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)

### `lean4/Sixth/Cost.lean`

- `H3V7N5QF:lean4/Sixth/Cost.lean::givenB4_to_loopState_one` — proved in Lean (module `lean4/Sixth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)

### `lean4/Sixth/Step.lean`

- `H3V7N5QF:lean4/Sixth/Step.lean::identify_given_ara` — proved in Lean (module `lean4/Sixth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)

### `lean4/Sixth/Cost.lean`

- `H3V7N5QF:lean4/Sixth/Cost.lean::identify_givenA4_eq` — proved in Lean (module `lean4/Sixth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixth/Cost.lean::identify_givenB4_eq` — proved in Lean (module `lean4/Sixth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)

### `lean4/Sixth/State.lean`

- `H3V7N5QF:lean4/Sixth/State.lean::identify_M_eq_zero_of_all_merged` — proved in Lean (module `lean4/Sixth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixth/State.lean::identify_M_ge_pair` — proved in Lean (module `lean4/Sixth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)

### `lean4/Sixth/Step.lean`

- `H3V7N5QF:lean4/Sixth/Step.lean::legal_not_kept` — proved in Lean (module `lean4/Sixth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)

### `lean4/Sixth/Compare.lean`

- `H3V7N5QF:lean4/Sixth/Compare.lean::legal_results_are_the_fifths` — proved in Lean (module `lean4/Sixth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)

### `lean4/Sixth/Reach.lean`

- `H3V7N5QF:lean4/Sixth/Reach.lean::length_not_unique6` — proved in Lean (module `lean4/Sixth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)

### `lean4/Sixth/State.lean`

- `H3V7N5QF:lean4/Sixth/State.lean::loopState_contains` — proved in Lean (module `lean4/Sixth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)

### `lean4/Sixth/Reach.lean`

- `H3V7N5QF:lean4/Sixth/Reach.lean::loopState_is_a_result` — proved in Lean (module `lean4/Sixth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixth/Reach.lean::loopState_never_apart` — proved in Lean (module `lean4/Sixth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)

### `lean4/Sixth/State.lean`

- `H3V7N5QF:lean4/Sixth/State.lean::loopState_wf` — proved in Lean (module `lean4/Sixth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixth/State.lean::loopState_zero` — proved in Lean (module `lean4/Sixth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)

### `lean4/Sixth/Cost.lean`

- `H3V7N5QF:lean4/Sixth/Cost.lean::lostA6_eq_lostA5_of_legal` — proved in Lean (module `lean4/Sixth/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixth/Cost.lean::lostA6_eq_lostA5_of_ne` — proved in Lean (module `lean4/Sixth/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixth/Cost.lean::lostA6_eq_zero_of_contains` — proved in Lean (module `lean4/Sixth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixth/Cost.lean::lostA6_identify` — proved in Lean (module `lean4/Sixth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixth/Cost.lean::lostA6_le_of_contains` — proved in Lean (module `lean4/Sixth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixth/Cost.lean::lostA6_le_two` — proved in Lean (module `lean4/Sixth/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixth/Cost.lean::lostA6_of_eq` — proved in Lean (module `lean4/Sixth/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixth/Cost.lean::lostA6_remove` — proved in Lean (module `lean4/Sixth/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)

### `lean4/Sixth/Rename.lean`

- `H3V7N5QF:lean4/Sixth/Rename.lean::lostA6_rename` — proved in Lean (module `lean4/Sixth/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)

### `lean4/Sixth/Cost.lean`

- `H3V7N5QF:lean4/Sixth/Cost.lean::lostB6_eq_lostB5_of_legal` — proved in Lean (module `lean4/Sixth/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixth/Cost.lean::lostB6_eq_lostB5_of_ne` — proved in Lean (module `lean4/Sixth/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixth/Cost.lean::lostB6_eq_zero_of_contains` — proved in Lean (module `lean4/Sixth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixth/Cost.lean::lostB6_identify` — proved in Lean (module `lean4/Sixth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixth/Cost.lean::lostB6_le_of_contains` — proved in Lean (module `lean4/Sixth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixth/Cost.lean::lostB6_le_three` — proved in Lean (module `lean4/Sixth/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixth/Cost.lean::lostB6_remove` — proved in Lean (module `lean4/Sixth/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)

### `lean4/Sixth/Rename.lean`

- `H3V7N5QF:lean4/Sixth/Rename.lean::lostB6_rename` — proved in Lean (module `lean4/Sixth/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)

### `lean4/Sixth/Reach.lean`

- `H3V7N5QF:lean4/Sixth/Reach.lean::merged_never_apart6` — proved in Lean (module `lean4/Sixth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixth/Reach.lean::no_return_fails6` — proved in Lean (module `lean4/Sixth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Sixth/Compare.lean`

- `H3V7N5QF:lean4/Sixth/Compare.lean::nothing_obstructed` — proved in Lean (module `lean4/Sixth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)

### `lean4/Sixth/Cost.lean`

- `H3V7N5QF:lean4/Sixth/Cost.lean::costA_le` — proved in Lean (module `lean4/Sixth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixth/Cost.lean::costB_le` — proved in Lean (module `lean4/Sixth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)

### `lean4/Sixth/Reach.lean`

- `H3V7N5QF:lean4/Sixth/Reach.lean::cycles` — proved in Lean (module `lean4/Sixth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)

### `lean4/Sixth/Step.lean`

- `H3V7N5QF:lean4/Sixth/Step.lean::eq_of_zero` — proved in Lean (module `lean4/Sixth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)

### `lean4/Seventh/Step.lean`

- `H3V7N5QF:lean4/Seventh/Step.lean::forget` — proved in Lean (module `lean4/Seventh/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)

### `lean4/Eighth/Step.lean`

- `H3V7N5QF:lean4/Eighth/Step.lean::ofR` — proved in Lean (module `lean4/Eighth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Sixth/Rename.lean`

- `H3V7N5QF:lean4/Sixth/Rename.lean::rename` — proved in Lean (module `lean4/Sixth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)

### `lean4/Sixth/Cost.lean`

- `H3V7N5QF:lean4/Sixth/Cost.lean::size_parity` — proved in Lean (module `lean4/Sixth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)

### `lean4/Sixth/Step.lean`

- `H3V7N5QF:lean4/Sixth/Step.lean::toReach5_of_legal_step` — proved in Lean (module `lean4/Sixth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixth/Step.lean::trans` — proved in Lean (module `lean4/Sixth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)

### `lean4/Sixth/Reach.lean`

- `H3V7N5QF:lean4/Sixth/Reach.lean::unbounded` — proved in Lean (module `lean4/Sixth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)

### `lean4/Sixth/Cost.lean`

- `H3V7N5QF:lean4/Sixth/Cost.lean::reach6_addTerms` — proved in Lean (module `lean4/Sixth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)

### `lean4/Sixth/Reach.lean`

- `H3V7N5QF:lean4/Sixth/Reach.lean::reach6_back_A` — proved in Lean (module `lean4/Sixth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixth/Reach.lean::reach6_back_B` — proved in Lean (module `lean4/Sixth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)

### `lean4/Sixth/Cost.lean`

- `H3V7N5QF:lean4/Sixth/Cost.lean::reach6_by_additions` — proved in Lean (module `lean4/Sixth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)

### `lean4/Sixth/Reach.lean`

- `H3V7N5QF:lean4/Sixth/Reach.lean::reach6_iff` — proved in Lean (module `lean4/Sixth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Sixth/Cost.lean`

- `H3V7N5QF:lean4/Sixth/Cost.lean::reach6_of_contains` — proved in Lean (module `lean4/Sixth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)

### `lean4/Sixth/Reach.lean`

- `H3V7N5QF:lean4/Sixth/Reach.lean::reach6_of_names` — proved in Lean (module `lean4/Sixth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Sixth/Cost.lean`

- `H3V7N5QF:lean4/Sixth/Cost.lean::reach6_raise` — proved in Lean (module `lean4/Sixth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Sixth/Reach.lean`

- `H3V7N5QF:lean4/Sixth/Reach.lean::reach6_symm` — proved in Lean (module `lean4/Sixth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixth/Reach.lean::reach6_total` — proved in Lean (module `lean4/Sixth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)

### `lean4/Sixth/Compare.lean`

- `H3V7N5QF:lean4/Sixth/Compare.lean::remove_answer_differs` — proved in Lean (module `lean4/Sixth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)

### `lean4/Sixth/Reach.lean`

- `H3V7N5QF:lean4/Sixth/Reach.lean::result6_iff_A` — proved in Lean (module `lean4/Sixth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixth/Reach.lean::result6_iff_B` — proved in Lean (module `lean4/Sixth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)

### `lean4/Sixth/Compare.lean`

- `H3V7N5QF:lean4/Sixth/Compare.lean::results_are_every_wf_state` — proved in Lean (module `lean4/Sixth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixth/Compare.lean::results_extend_A` — proved in Lean (module `lean4/Sixth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixth/Compare.lean::results_extend_B` — proved in Lean (module `lean4/Sixth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixth/Compare.lean::results_grow` — proved in Lean (module `lean4/Sixth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)

### `lean4/Sixth/State.lean`

- `H3V7N5QF:lean4/Sixth/State.lean::size_loopState` — proved in Lean (module `lean4/Sixth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)

### `lean4/Sixth/Cost.lean`

- `H3V7N5QF:lean4/Sixth/Cost.lean::costA_le` — proved in Lean (module `lean4/Sixth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixth/Cost.lean::costB_le` — proved in Lean (module `lean4/Sixth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Seventh/Step.lean`

- `H3V7N5QF:lean4/Seventh/Step.lean::forget` — proved in Lean (module `lean4/Seventh/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)

### `lean4/Sixth/Step.lean`

- `H3V7N5QF:lean4/Sixth/Step.lean::not_legal_iff` — proved in Lean (module `lean4/Sixth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)

### `lean4/Eighth/Step.lean`

- `H3V7N5QF:lean4/Eighth/Step.lean::ofR` — proved in Lean (module `lean4/Eighth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/eighth/lean_axioms.txt`)

### `lean4/Sixth/Rename.lean`

- `H3V7N5QF:lean4/Sixth/Rename.lean::rename` — proved in Lean (module `lean4/Sixth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)

### `lean4/Sixth/Cost.lean`

- `H3V7N5QF:lean4/Sixth/Cost.lean::size_step` — proved in Lean (module `lean4/Sixth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/seventh/lean_axioms.txt`)

### `lean4/Sixth/Step.lean`

- `H3V7N5QF:lean4/Sixth/Step.lean::toStep5` — proved in Lean (module `lean4/Sixth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixth/Step.lean::toTry5` — proved in Lean (module `lean4/Sixth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixth/Step.lean::step_identify_given` — proved in Lean (module `lean4/Sixth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)

### `lean4/Sixth/Cost.lean`

- `H3V7N5QF:lean4/Sixth/Cost.lean::step_identify_givenA4` — proved in Lean (module `lean4/Sixth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Sixth/Cost.lean::step_identify_givenB4` — proved in Lean (module `lean4/Sixth/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)

### `lean4/Sixth/Step.lean`

- `H3V7N5QF:lean4/Sixth/Step.lean::try5_iff_step6` — proved in Lean (module `lean4/Sixth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)

### `lean4/Sixth/Reach.lean`

- `H3V7N5QF:lean4/Sixth/Reach.lean::xrx_is_a_result` — proved in Lean (module `lean4/Sixth/Reach.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/sixth/lean_axioms.txt`)

### `lean4/H3V7N5QF/Cost.lean`

- `H3V7N5QF:lean4/H3V7N5QF/Cost.lean::size_addAssertion` — proved in Lean (module `lean4/H3V7N5QF/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)
- `H3V7N5QF:lean4/H3V7N5QF/Cost.lean::size_addTerm` — proved in Lean (module `lean4/H3V7N5QF/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)
- `H3V7N5QF:lean4/H3V7N5QF/Cost.lean::costA_le` — proved in Lean (module `lean4/H3V7N5QF/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/lean_axioms.txt`)
- `H3V7N5QF:lean4/H3V7N5QF/Cost.lean::costB_le` — proved in Lean (module `lean4/H3V7N5QF/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/lean_axioms.txt`)

### `lean4/Tenth/Step.lean`

- `H3V7N5QF:lean4/Tenth/Step.lean::clears_remove` — proved in Lean (module `lean4/Tenth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/tenth/lean_axioms.txt`)

### `lean4/Tenth/Compare.lean`

- `H3V7N5QF:lean4/Tenth/Compare.lean::fewest_changes10` — proved in Lean (module `lean4/Tenth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/tenth/lean_axioms.txt`)

### `lean4/Tenth/Step.lean`

- `H3V7N5QF:lean4/Tenth/Step.lean::first_change_leftover` — proved in Lean (module `lean4/Tenth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/tenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Tenth/Step.lean::identify_twoEmpty_restored` — proved in Lean (module `lean4/Tenth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/tenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Tenth/Step.lean::leftover_addAssertion` — proved in Lean (module `lean4/Tenth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/tenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Tenth/Step.lean::leftover_addTerm` — proved in Lean (module `lean4/Tenth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/tenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Tenth/Step.lean::leftover_identify_twoEmpty` — proved in Lean (module `lean4/Tenth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/tenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Tenth/Step.lean::leftover_not_assertion` — proved in Lean (module `lean4/Tenth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/tenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Tenth/Step.lean::leftover_remove` — proved in Lean (module `lean4/Tenth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/tenth/lean_axioms.txt`)

### `lean4/Tenth/Rename.lean`

- `H3V7N5QF:lean4/Tenth/Rename.lean::leftover_swap_addTerm` — proved in Lean (module `lean4/Tenth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/tenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Tenth/Rename.lean::leftover_swap_remove` — proved in Lean (module `lean4/Tenth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/tenth/lean_axioms.txt`)

### `lean4/Tenth/Compare.lean`

- `H3V7N5QF:lean4/Tenth/Compare.lean::no_third_rel` — proved in Lean (module `lean4/Tenth/Compare.lean`; axioms: propext, Quot.sound; recorded in `evidence/tenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Tenth/Compare.lean::other_rel_not_clear` — proved in Lean (module `lean4/Tenth/Compare.lean`; axioms: propext, Quot.sound; recorded in `evidence/tenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Tenth/Compare.lean::reach10_iff` — proved in Lean (module `lean4/Tenth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/tenth/lean_axioms.txt`)

### `lean4/Tenth/State.lean`

- `H3V7N5QF:lean4/Tenth/State.lean::remove_add_of_pos` — proved in Lean (module `lean4/Tenth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/tenth/lean_axioms.txt`)

### `lean4/Tenth/Compare.lean`

- `H3V7N5QF:lean4/Tenth/Compare.lean::results_pair10` — proved in Lean (module `lean4/Tenth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/tenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Tenth/Compare.lean::split_additions` — proved in Lean (module `lean4/Tenth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/tenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Tenth/Compare.lean::split_kinds` — proved in Lean (module `lean4/Tenth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/tenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Tenth/Compare.lean::split_removals` — proved in Lean (module `lean4/Tenth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/tenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Tenth/Compare.lean::tagged_cost_fails` — proved in Lean (module `lean4/Tenth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/tenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Tenth/Compare.lean::tagged_extra` — proved in Lean (module `lean4/Tenth/Compare.lean`; axioms: propext, Quot.sound; recorded in `evidence/tenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Tenth/Compare.lean::tagged_one_nothing` — proved in Lean (module `lean4/Tenth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/tenth/lean_axioms.txt`)

### `lean4/Third/Answers.lean`

- `H3V7N5QF:lean4/Third/Answers.lean::addTerm_unobstructed` — proved in Lean (module `lean4/Third/Answers.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)
- `H3V7N5QF:lean4/Third/Answers.lean::build_answer2` — proved in Lean (module `lean4/Third/Answers.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)
- `H3V7N5QF:lean4/Third/Answers.lean::build_answer2_reverse` — proved in Lean (module `lean4/Third/Answers.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)

### `lean4/Third/Contain.lean`

- `H3V7N5QF:lean4/Third/Contain.lean::antisymm` — proved in Lean (module `lean4/Third/Contain.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)
- `H3V7N5QF:lean4/Third/Contain.lean::carries` — proved in Lean (module `lean4/Third/Contain.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Fourth/Contain.lean`

- `H3V7N5QF:lean4/Fourth/Contain.lean::ofSt` — proved in Lean (module `lean4/Fourth/Contain.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Third/Cost.lean`

- `H3V7N5QF:lean4/Third/Cost.lean::costA_eq_size_of_reach2` — proved in Lean (module `lean4/Third/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)
- `H3V7N5QF:lean4/Third/Cost.lean::costB_eq_size_of_reach2` — proved in Lean (module `lean4/Third/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)
- `H3V7N5QF:lean4/Third/Cost.lean::fewest_changes2_A` — proved in Lean (module `lean4/Third/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Third/Cost.lean::fewest_changes2_B` — proved in Lean (module `lean4/Third/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Third/Rename.lean`

- `H3V7N5QF:lean4/Third/Rename.lean::fewest_changes2_every_writing_A` — proved in Lean (module `lean4/Third/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)
- `H3V7N5QF:lean4/Third/Rename.lean::fewest_changes2_every_writing_B` — proved in Lean (module `lean4/Third/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)

### `lean4/Third/Cost.lean`

- `H3V7N5QF:lean4/Third/Cost.lean::fewest_changes2_lower_A` — proved in Lean (module `lean4/Third/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)
- `H3V7N5QF:lean4/Third/Cost.lean::fewest_changes2_lower_B` — proved in Lean (module `lean4/Third/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)
- `H3V7N5QF:lean4/Third/Cost.lean::givenA_to_givenB2` — proved in Lean (module `lean4/Third/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Third/Cost.lean::givenB_never_givenA2` — proved in Lean (module `lean4/Third/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)
- `H3V7N5QF:lean4/Third/Cost.lean::lostA_eq_zero_of_reach2` — proved in Lean (module `lean4/Third/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)
- `H3V7N5QF:lean4/Third/Cost.lean::lostB_eq_zero_of_reach2` — proved in Lean (module `lean4/Third/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)

### `lean4/Third/Answers.lean`

- `H3V7N5QF:lean4/Third/Answers.lean::no_change_asserts_xrx` — proved in Lean (module `lean4/Third/Answers.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)

### `lean4/Third/Cost.lean`

- `H3V7N5QF:lean4/Third/Cost.lean::oneTerm_unreachable2_A` — proved in Lean (module `lean4/Third/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)
- `H3V7N5QF:lean4/Third/Cost.lean::oneTerm_unreachable2_B` — proved in Lean (module `lean4/Third/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)
- `H3V7N5QF:lean4/Third/Cost.lean::antisymm` — proved in Lean (module `lean4/Third/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Third/Contain.lean`

- `H3V7N5QF:lean4/Third/Contain.lean::asserted_persists` — proved in Lean (module `lean4/Third/Contain.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)
- `H3V7N5QF:lean4/Third/Contain.lean::card_A_le` — proved in Lean (module `lean4/Third/Contain.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)
- `H3V7N5QF:lean4/Third/Contain.lean::card_T_le` — proved in Lean (module `lean4/Third/Contain.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)
- `H3V7N5QF:lean4/Third/Contain.lean::contains` — proved in Lean (module `lean4/Third/Contain.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)

### `lean4/Third/Step.lean`

- `H3V7N5QF:lean4/Third/Step.lean::costA_le_inherited` — proved in Lean (module `lean4/Third/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)
- `H3V7N5QF:lean4/Third/Step.lean::costB_le_inherited` — proved in Lean (module `lean4/Third/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)
- `H3V7N5QF:lean4/Third/Step.lean::eq_of_zero` — proved in Lean (module `lean4/Third/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)

### `lean4/Third/Cost.lean`

- `H3V7N5QF:lean4/Third/Cost.lean::length_unique` — proved in Lean (module `lean4/Third/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Third/Contain.lean`

- `H3V7N5QF:lean4/Third/Contain.lean::name_a` — proved in Lean (module `lean4/Third/Contain.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)
- `H3V7N5QF:lean4/Third/Contain.lean::name_b` — proved in Lean (module `lean4/Third/Contain.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)

### `lean4/Third/Cost.lean`

- `H3V7N5QF:lean4/Third/Cost.lean::no_return` — proved in Lean (module `lean4/Third/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)

### `lean4/Third/Rename.lean`

- `H3V7N5QF:lean4/Third/Rename.lean::rename` — proved in Lean (module `lean4/Third/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)

### `lean4/Third/Cost.lean`

- `H3V7N5QF:lean4/Third/Cost.lean::size_eq` — proved in Lean (module `lean4/Third/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)

### `lean4/Third/Step.lean`

- `H3V7N5QF:lean4/Third/Step.lean::size_le_inherited` — proved in Lean (module `lean4/Third/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)

### `lean4/Third/Contain.lean`

- `H3V7N5QF:lean4/Third/Contain.lean::term_persists` — proved in Lean (module `lean4/Third/Contain.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)

### `lean4/Third/Step.lean`

- `H3V7N5QF:lean4/Third/Step.lean::toReach` — proved in Lean (module `lean4/Third/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)
- `H3V7N5QF:lean4/Third/Step.lean::toReach3` — proved in Lean (module `lean4/Third/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)

### `lean4/Fourth/Step.lean`

- `H3V7N5QF:lean4/Fourth/Step.lean::toReach4` — proved in Lean (module `lean4/Fourth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Third/Step.lean`

- `H3V7N5QF:lean4/Third/Step.lean::trans` — proved in Lean (module `lean4/Third/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)

### `lean4/Third/Contain.lean`

- `H3V7N5QF:lean4/Third/Contain.lean::xrx_still_obstructed` — proved in Lean (module `lean4/Third/Contain.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)

### `lean4/Third/Rename.lean`

- `H3V7N5QF:lean4/Third/Rename.lean::reach2_antisymm_writing` — proved in Lean (module `lean4/Third/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)

### `lean4/Third/Cost.lean`

- `H3V7N5QF:lean4/Third/Cost.lean::reach2_by_additions` — proved in Lean (module `lean4/Third/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)
- `H3V7N5QF:lean4/Third/Cost.lean::reach2_givenA_contains` — proved in Lean (module `lean4/Third/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)
- `H3V7N5QF:lean4/Third/Cost.lean::reach2_givenA_two_terms` — proved in Lean (module `lean4/Third/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)
- `H3V7N5QF:lean4/Third/Cost.lean::reach2_givenB_contains` — proved in Lean (module `lean4/Third/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)
- `H3V7N5QF:lean4/Third/Cost.lean::reach2_givenB_two_terms` — proved in Lean (module `lean4/Third/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)
- `H3V7N5QF:lean4/Third/Cost.lean::reach2_iff` — proved in Lean (module `lean4/Third/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Third/Rename.lean`

- `H3V7N5QF:lean4/Third/Rename.lean::reach2_iff_some_writing` — proved in Lean (module `lean4/Third/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Third/Cost.lean`

- `H3V7N5QF:lean4/Third/Cost.lean::reach2_of_contains` — proved in Lean (module `lean4/Third/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)

### `lean4/Third/Rename.lean`

- `H3V7N5QF:lean4/Third/Rename.lean::result2_iff_A` — proved in Lean (module `lean4/Third/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Third/Rename.lean::result2_iff_B` — proved in Lean (module `lean4/Third/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Third/Contain.lean`

- `H3V7N5QF:lean4/Third/Contain.lean::contains` — proved in Lean (module `lean4/Third/Contain.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)

### `lean4/Third/Step.lean`

- `H3V7N5QF:lean4/Third/Step.lean::ne_identify` — proved in Lean (module `lean4/Third/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)
- `H3V7N5QF:lean4/Third/Step.lean::ne_remove` — proved in Lean (module `lean4/Third/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)

### `lean4/Third/Rename.lean`

- `H3V7N5QF:lean4/Third/Rename.lean::rename` — proved in Lean (module `lean4/Third/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)

### `lean4/Third/Cost.lean`

- `H3V7N5QF:lean4/Third/Cost.lean::size_eq` — proved in Lean (module `lean4/Third/Cost.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Third/Step.lean`

- `H3V7N5QF:lean4/Third/Step.lean::toStep` — proved in Lean (module `lean4/Third/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fifth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Third/Step.lean::toStep3` — proved in Lean (module `lean4/Third/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)

### `lean4/Fourth/Step.lean`

- `H3V7N5QF:lean4/Fourth/Step.lean::toStep4` — proved in Lean (module `lean4/Fourth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)

### `lean4/Third/Answers.lean`

- `H3V7N5QF:lean4/Third/Answers.lean::toTry2` — proved in Lean (module `lean4/Third/Answers.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)

### `lean4/Third/Step.lean`

- `H3V7N5QF:lean4/Third/Step.lean::identify_or_step2` — proved in Lean (module `lean4/Third/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)

### `lean4/Third/Answers.lean`

- `H3V7N5QF:lean4/Third/Answers.lean::legal_iff` — proved in Lean (module `lean4/Third/Answers.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)
- `H3V7N5QF:lean4/Third/Answers.lean::obstructed_iff` — proved in Lean (module `lean4/Third/Answers.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)
- `H3V7N5QF:lean4/Third/Answers.lean::step2_or_xrx` — proved in Lean (module `lean4/Third/Answers.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)
- `H3V7N5QF:lean4/Third/Answers.lean::two_sequences` — proved in Lean (module `lean4/Third/Answers.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/fourth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Third/Answers.lean::xrx_outcome_unreachable` — proved in Lean (module `lean4/Third/Answers.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/third/lean_axioms.txt`)

### `lean4/Thirteenth/Step.lean`

- `H3V7N5QF:lean4/Thirteenth/Step.lean::coarse_addAssertion_r_s` — proved in Lean (module `lean4/Thirteenth/Step.lean`; axioms: propext, Quot.sound; recorded in `evidence/thirteenth/lean_axioms.txt`)

### `lean4/Thirteenth/Compare.lean`

- `H3V7N5QF:lean4/Thirteenth/Compare.lean::coarse_cost_descends` — proved in Lean (module `lean4/Thirteenth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/thirteenth/lean_axioms.txt`)

### `lean4/Thirteenth/State.lean`

- `H3V7N5QF:lean4/Thirteenth/State.lean::coarse_eq_sum` — proved in Lean (module `lean4/Thirteenth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/thirteenth/lean_axioms.txt`)

### `lean4/Thirteenth/Compare.lean`

- `H3V7N5QF:lean4/Thirteenth/Compare.lean::coarse_extra` — proved in Lean (module `lean4/Thirteenth/Compare.lean`; axioms: propext, Quot.sound; recorded in `evidence/thirteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Thirteenth/Compare.lean::coarse_has_term` — proved in Lean (module `lean4/Thirteenth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/thirteenth/lean_axioms.txt`)

### `lean4/Thirteenth/State.lean`

- `H3V7N5QF:lean4/Thirteenth/State.lean::coarse_not_assertion` — proved in Lean (module `lean4/Thirteenth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/thirteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Thirteenth/State.lean::coarse_swap` — proved in Lean (module `lean4/Thirteenth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/thirteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Thirteenth/State.lean::determines_of_nothing` — proved in Lean (module `lean4/Thirteenth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/thirteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Thirteenth/State.lean::empty_determines` — proved in Lean (module `lean4/Thirteenth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/thirteenth/lean_axioms.txt`)

### `lean4/Thirteenth/Compare.lean`

- `H3V7N5QF:lean4/Thirteenth/Compare.lean::fewest_changes13` — proved in Lean (module `lean4/Thirteenth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/thirteenth/lean_axioms.txt`)

### `lean4/Thirteenth/Step.lean`

- `H3V7N5QF:lean4/Thirteenth/Step.lean::first_change_adds_term13` — proved in Lean (module `lean4/Thirteenth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/thirteenth/lean_axioms.txt`)

### `lean4/Thirteenth/Compare.lean`

- `H3V7N5QF:lean4/Thirteenth/Compare.lean::no_cross_constraint` — proved in Lean (module `lean4/Thirteenth/Compare.lean`; axioms: propext, Quot.sound; recorded in `evidence/thirteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Thirteenth/Compare.lean::no_third_rel` — proved in Lean (module `lean4/Thirteenth/Compare.lean`; axioms: propext, Quot.sound; recorded in `evidence/thirteenth/lean_axioms.txt`)

### `lean4/Thirteenth/State.lean`

- `H3V7N5QF:lean4/Thirteenth/State.lean::not_determines_twoBetween` — proved in Lean (module `lean4/Thirteenth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/thirteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Thirteenth/State.lean::r_and_s_same_coarse` — proved in Lean (module `lean4/Thirteenth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/thirteenth/lean_axioms.txt`)

### `lean4/Thirteenth/Compare.lean`

- `H3V7N5QF:lean4/Thirteenth/Compare.lean::reach13_iff` — proved in Lean (module `lean4/Thirteenth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/thirteenth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Thirteenth/Compare.lean::results_pair13` — proved in Lean (module `lean4/Thirteenth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/thirteenth/lean_axioms.txt`)

### `lean4/Thirteenth/State.lean`

- `H3V7N5QF:lean4/Thirteenth/State.lean::size_coarse` — proved in Lean (module `lean4/Thirteenth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/thirteenth/lean_axioms.txt`)

### `lean4/Thirteenth/Rename.lean`

- `H3V7N5QF:lean4/Thirteenth/Rename.lean::swap` — proved in Lean (module `lean4/Thirteenth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/thirteenth/lean_axioms.txt`)

### `lean4/Twelfth/Step.lean`

- `H3V7N5QF:lean4/Twelfth/Step.lean::empty_record_restored_by_addTerm` — proved in Lean (module `lean4/Twelfth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/twelfth/lean_axioms.txt`)

### `lean4/Twelfth/Compare.lean`

- `H3V7N5QF:lean4/Twelfth/Compare.lean::fewest_changes12` — proved in Lean (module `lean4/Twelfth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/twelfth/lean_axioms.txt`)

### `lean4/Twelfth/Step.lean`

- `H3V7N5QF:lean4/Twelfth/Step.lean::first_change_adds_term12` — proved in Lean (module `lean4/Twelfth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/twelfth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Twelfth/Step.lean::identify_drops_a_term` — proved in Lean (module `lean4/Twelfth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/twelfth/lean_axioms.txt`)

### `lean4/Twelfth/Compare.lean`

- `H3V7N5QF:lean4/Twelfth/Compare.lean::no_cross_constraint` — proved in Lean (module `lean4/Twelfth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/twelfth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Twelfth/Compare.lean::no_third_rel` — proved in Lean (module `lean4/Twelfth/Compare.lean`; axioms: propext, Quot.sound; recorded in `evidence/twelfth/lean_axioms.txt`)

### `lean4/Twelfth/Step.lean`

- `H3V7N5QF:lean4/Twelfth/Step.lean::nonempty_not_restored` — proved in Lean (module `lean4/Twelfth/Step.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/twelfth/lean_axioms.txt`)

### `lean4/Twelfth/State.lean`

- `H3V7N5QF:lean4/Twelfth/State.lean::r_record_not_s` — proved in Lean (module `lean4/Twelfth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/twelfth/lean_axioms.txt`)

### `lean4/Twelfth/Compare.lean`

- `H3V7N5QF:lean4/Twelfth/Compare.lean::reach12_iff` — proved in Lean (module `lean4/Twelfth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/twelfth/lean_axioms.txt`)

### `lean4/Twelfth/State.lean`

- `H3V7N5QF:lean4/Twelfth/State.lean::record_determined_by_rel` — proved in Lean (module `lean4/Twelfth/State.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/twelfth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Twelfth/State.lean::record_not_assertion` — proved in Lean (module `lean4/Twelfth/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/twelfth/lean_axioms.txt`)

### `lean4/Twelfth/Compare.lean`

- `H3V7N5QF:lean4/Twelfth/Compare.lean::recorded_cost_is_size` — proved in Lean (module `lean4/Twelfth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/twelfth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Twelfth/Compare.lean::recorded_extra` — proved in Lean (module `lean4/Twelfth/Compare.lean`; axioms: propext, Quot.sound; recorded in `evidence/twelfth/lean_axioms.txt`)

### `lean4/Twelfth/Rename.lean`

- `H3V7N5QF:lean4/Twelfth/Rename.lean::recordOf_swap` — proved in Lean (module `lean4/Twelfth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/twelfth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Twelfth/Rename.lean::recordRel_swap` — proved in Lean (module `lean4/Twelfth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/twelfth/lean_axioms.txt`)

### `lean4/Twelfth/Compare.lean`

- `H3V7N5QF:lean4/Twelfth/Compare.lean::results_pair12` — proved in Lean (module `lean4/Twelfth/Compare.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/twelfth/lean_axioms.txt`)

### `lean4/Twelfth/Rename.lean`

- `H3V7N5QF:lean4/Twelfth/Rename.lean::swap` — proved in Lean (module `lean4/Twelfth/Rename.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/twelfth/lean_axioms.txt`)

### `lean4/Twentieth/Order.lean`

- `H3V7N5QF:lean4/Twentieth/Order.lean::added_cleared` — proved in Lean (module `lean4/Twentieth/Order.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentieth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Twentieth/Order.lean::added_oneTerm` — proved in Lean (module `lean4/Twentieth/Order.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentieth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Twentieth/Order.lean::additions_diverge` — proved in Lean (module `lean4/Twentieth/Order.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/twentieth/lean_axioms.txt`)
- `H3V7N5QF:lean4/Twentieth/Order.lean::reach_cleared` — proved in Lean (module `lean4/Twentieth/Order.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/twentieth/lean_axioms.txt`)

### `lean4/Twentyfirst/Refusal.lean`

- `H3V7N5QF:lean4/Twentyfirst/Refusal.lean::identify_given_illegal` — proved in Lean (module `lean4/Twentyfirst/Refusal.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/twentyfirst/lean_axioms.txt`)
- `H3V7N5QF:lean4/Twentyfirst/Refusal.lean::no_step_to_illegal` — proved in Lean (module `lean4/Twentyfirst/Refusal.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/twentyfirst/lean_axioms.txt`)

### `lean4/H3V7N5QF/Basic.lean`

- `H3V7N5QF:lean4/H3V7N5QF/Basic.lean::two_states_differ` — proved in Lean (module `lean4/H3V7N5QF/Basic.lean`; axioms: propext; recorded in `evidence/lean_axioms.txt`)
- `H3V7N5QF:lean4/H3V7N5QF/Basic.lean::two_states_on_given_terms` — proved in Lean (module `lean4/H3V7N5QF/Basic.lean`; axioms: propext, Classical.choice, Quot.sound; recorded in `evidence/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Reach.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Reach.lean::addTerm_not_respected25` — proved in Lean (module `lean4_core/Twentyfifth/Reach.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Record.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Record.lean::aLoop_wf` — proved in Lean (module `lean4_core/Twentyfifth/Record.lean`; axioms: propext; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Balance.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Balance.lean::arb_one_way` — proved in Lean (module `lean4_core/Twentyfifth/Balance.lean`; axioms: none; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Balance.lean::arcThree_told` — proved in Lean (module `lean4_core/Twentyfifth/Balance.lean`; axioms: none; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Record.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Record.lean::arcThree_wf` — proved in Lean (module `lean4_core/Twentyfifth/Record.lean`; axioms: propext; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Balance.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Balance.lean::around_add_loop` — proved in Lean (module `lean4_core/Twentyfifth/Balance.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Balance.lean::around_norm` — proved in Lean (module `lean4_core/Twentyfifth/Balance.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Balance.lean::around_nothing` — proved in Lean (module `lean4_core/Twentyfifth/Balance.lean`; axioms: none; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Rename.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Rename.lean::around_rename` — proved in Lean (module `lean4_core/Twentyfifth/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Balance.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Balance.lean::around_rot` — proved in Lean (module `lean4_core/Twentyfifth/Balance.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Balance.lean::around_swap` — proved in Lean (module `lean4_core/Twentyfifth/Balance.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Balance.lean::balanced_swap` — proved in Lean (module `lean4_core/Twentyfifth/Balance.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Blind.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Blind.lean::balanced` — proved in Lean (module `lean4_core/Twentyfifth/Blind.lean`; axioms: none; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Blind.lean::blind_five` — proved in Lean (module `lean4_core/Twentyfifth/Blind.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Blind.lean::blind_four` — proved in Lean (module `lean4_core/Twentyfifth/Blind.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Blind.lean::blind_four_not_nothing` — proved in Lean (module `lean4_core/Twentyfifth/Blind.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Blind.lean::blind_three_iff` — proved in Lean (module `lean4_core/Twentyfifth/Blind.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Balance.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Balance.lean::blind_three_not_nothing` — proved in Lean (module `lean4_core/Twentyfifth/Balance.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Blind.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Blind.lean::blind_twoWay_five` — proved in Lean (module `lean4_core/Twentyfifth/Blind.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Blind.lean::blindThree_blind` — proved in Lean (module `lean4_core/Twentyfifth/Blind.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Fill.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Fill.lean::carry_nil` — proved in Lean (module `lean4_core/Twentyfifth/Fill.lean`; axioms: propext; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Fill.lean::carry_wf` — proved in Lean (module `lean4_core/Twentyfifth/Fill.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Blind.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Blind.lean::cone_decides` — proved in Lean (module `lean4_core/Twentyfifth/Blind.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Cost.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Cost.lean::congr` — proved in Lean (module `lean4_core/Twentyfifth/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Cost.lean::le_psi` — proved in Lean (module `lean4_core/Twentyfifth/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Cost.lean::unique` — proved in Lean (module `lean4_core/Twentyfifth/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Cost.lean::cost25_embed_iff` — proved in Lean (module `lean4_core/Twentyfifth/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Cost.lean::cost25_eq` — proved in Lean (module `lean4_core/Twentyfifth/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Rename.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Rename.lean::cost25_every_writing` — proved in Lean (module `lean4_core/Twentyfifth/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Reach.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Reach.lean::cost25_swap` — proved in Lean (module `lean4_core/Twentyfifth/Reach.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Cost.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Cost.lean::cost3_nothing` — proved in Lean (module `lean4_core/Twentyfifth/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Record.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Record.lean::cost3_of_around3` — proved in Lean (module `lean4_core/Twentyfifth/Record.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Record.lean::cost3_of_sums3` — proved in Lean (module `lean4_core/Twentyfifth/Record.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Record.lean::cost3_three_ge_sums` — proved in Lean (module `lean4_core/Twentyfifth/Record.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Cost.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Cost.lean::cost_oneFilled` — proved in Lean (module `lean4_core/Twentyfifth/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Cost.lean::cost_oneFilledOther` — proved in Lean (module `lean4_core/Twentyfifth/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Fill.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Fill.lean::embed_reach` — proved in Lean (module `lean4_core/Twentyfifth/Fill.lean`; axioms: propext; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Rename.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Rename.lean::embed_rename` — proved in Lean (module `lean4_core/Twentyfifth/Rename.lean`; axioms: none; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Map.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Map.lean::embed_same_iff` — proved in Lean (module `lean4_core/Twentyfifth/Map.lean`; axioms: none; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Rename.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Rename.lean::embed_sameW_iff` — proved in Lean (module `lean4_core/Twentyfifth/Rename.lean`; axioms: none; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Fill.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Fill.lean::embed_step` — proved in Lean (module `lean4_core/Twentyfifth/Fill.lean`; axioms: propext; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Fill.lean::embed_wf` — proved in Lean (module `lean4_core/Twentyfifth/Fill.lean`; axioms: none; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Reach.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Reach.lean::empty25_swap` — proved in Lean (module `lean4_core/Twentyfifth/Reach.lean`; axioms: none; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Fill.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Fill.lean::empty25_wf` — proved in Lean (module `lean4_core/Twentyfifth/Fill.lean`; axioms: none; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Reach.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Reach.lean::empty_never_returned25` — proved in Lean (module `lean4_core/Twentyfifth/Reach.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Balance.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Balance.lean::excess_add` — proved in Lean (module `lean4_core/Twentyfifth/Balance.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Balance.lean::excess_add_loop` — proved in Lean (module `lean4_core/Twentyfifth/Balance.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Record.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Record.lean::excess_zero_of_plain_nil` — proved in Lean (module `lean4_core/Twentyfifth/Record.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Balance.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Balance.lean::exists_not_of_not_forall` — proved in Lean (module `lean4_core/Twentyfifth/Balance.lean`; axioms: propext; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Record.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Record.lean::fewest_arcThree` — proved in Lean (module `lean4_core/Twentyfifth/Record.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Record.lean::fewest_wLoop` — proved in Lean (module `lean4_core/Twentyfifth/Record.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Record.lean::fewest_wPair` — proved in Lean (module `lean4_core/Twentyfifth/Record.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Map.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Map.lean::first_pair_merge25` — proved in Lean (module `lean4_core/Twentyfifth/Map.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Map.lean::forget_loses` — proved in Lean (module `lean4_core/Twentyfifth/Map.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Map.lean::forget_same` — proved in Lean (module `lean4_core/Twentyfifth/Map.lean`; axioms: none; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Reach.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Reach.lean::swap_swap` — proved in Lean (module `lean4_core/Twentyfifth/Reach.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Balance.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Balance.lean::same25` — proved in Lean (module `lean4_core/Twentyfifth/Balance.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Rename.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Rename.lean::wf_iff` — proved in Lean (module `lean4_core/Twentyfifth/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Balance.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Balance.lean::gen25_iff_same25` — proved in Lean (module `lean4_core/Twentyfifth/Balance.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Rename.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Rename.lean::wf_iff` — proved in Lean (module `lean4_core/Twentyfifth/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Rename.lean::genW25_iff_sameW25` — proved in Lean (module `lean4_core/Twentyfifth/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Fill.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Fill.lean::length_carry_le` — proved in Lean (module `lean4_core/Twentyfifth/Fill.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Fill.lean::length_nub_le` — proved in Lean (module `lean4_core/Twentyfifth/Fill.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Balance.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Balance.lean::loop_unseen` — proved in Lean (module `lean4_core/Twentyfifth/Balance.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Balance.lean::loopFilled_wf` — proved in Lean (module `lean4_core/Twentyfifth/Balance.lean`; axioms: propext; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Blind.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Blind.lean::lt_four` — proved in Lean (module `lean4_core/Twentyfifth/Blind.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Rename.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Rename.lean::map_eq_self_tri` — proved in Lean (module `lean4_core/Twentyfifth/Rename.lean`; axioms: none; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Fill.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Fill.lean::mem_carry` — proved in Lean (module `lean4_core/Twentyfifth/Fill.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Fill.lean::mem_nub` — proved in Lean (module `lean4_core/Twentyfifth/Fill.lean`; axioms: propext; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Rename.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Rename.lean::nodup_map_of_inj` — proved in Lean (module `lean4_core/Twentyfifth/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Balance.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Balance.lean::not_told` — proved in Lean (module `lean4_core/Twentyfifth/Balance.lean`; axioms: none; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Balance.lean::nothing_balanced` — proved in Lean (module `lean4_core/Twentyfifth/Balance.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Fill.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Fill.lean::nothing_filled_of_lt_three` — proved in Lean (module `lean4_core/Twentyfifth/Fill.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Fill.lean::nub_nodup` — proved in Lean (module `lean4_core/Twentyfifth/Fill.lean`; axioms: propext; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Rename.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Rename.lean::oneFilled_sameW_other` — proved in Lean (module `lean4_core/Twentyfifth/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Cost.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Cost.lean::oneFilled_wf` — proved in Lean (module `lean4_core/Twentyfifth/Cost.lean`; axioms: propext; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Cost.lean::oneFilledOther_wf` — proved in Lean (module `lean4_core/Twentyfifth/Cost.lean`; axioms: propext; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Cost.lean::parity_fails` — proved in Lean (module `lean4_core/Twentyfifth/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Cost.lean::perm_nil_eq` — proved in Lean (module `lean4_core/Twentyfifth/Cost.lean`; axioms: propext; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Record.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Record.lean::phi_ge_sums3` — proved in Lean (module `lean4_core/Twentyfifth/Record.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Cost.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Cost.lean::psi_empty25` — proved in Lean (module `lean4_core/Twentyfifth/Cost.lean`; axioms: propext; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Rename.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Rename.lean::psi_rename` — proved in Lean (module `lean4_core/Twentyfifth/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Reach.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Reach.lean::n_pos` — proved in Lean (module `lean4_core/Twentyfifth/Reach.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Cost.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Cost.lean::proj` — proved in Lean (module `lean4_core/Twentyfifth/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Cost.lean::psi_le` — proved in Lean (module `lean4_core/Twentyfifth/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Fill.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Fill.lean::single` — proved in Lean (module `lean4_core/Twentyfifth/Fill.lean`; axioms: propext; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Reach.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Reach.lean::swap` — proved in Lean (module `lean4_core/Twentyfifth/Reach.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Fill.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Fill.lean::trans` — proved in Lean (module `lean4_core/Twentyfifth/Fill.lean`; axioms: propext; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Reach.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Reach.lean::reach25_clear` — proved in Lean (module `lean4_core/Twentyfifth/Reach.lean`; axioms: propext; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Reach.lean::reach25_collapse` — proved in Lean (module `lean4_core/Twentyfifth/Reach.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Reach.lean::reach25_criterion` — proved in Lean (module `lean4_core/Twentyfifth/Reach.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Reach.lean::reach25_fill_in` — proved in Lean (module `lean4_core/Twentyfifth/Reach.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Reach.lean::reach25_grow` — proved in Lean (module `lean4_core/Twentyfifth/Reach.lean`; axioms: propext; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Reach.lean::reach25_mutual` — proved in Lean (module `lean4_core/Twentyfifth/Reach.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Reach.lean::reach25_swap` — proved in Lean (module `lean4_core/Twentyfifth/Reach.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Cost.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Cost.lean::reach_build` — proved in Lean (module `lean4_core/Twentyfifth/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Cost.lean::reach_fill_all` — proved in Lean (module `lean4_core/Twentyfifth/Cost.lean`; axioms: propext; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Map.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Map.lean::readBack25_congr` — proved in Lean (module `lean4_core/Twentyfifth/Map.lean`; axioms: propext; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Map.lean::readBack25_embed` — proved in Lean (module `lean4_core/Twentyfifth/Map.lean`; axioms: none; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Map.lean::readBack25_none_cost` — proved in Lean (module `lean4_core/Twentyfifth/Map.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Map.lean::readBack25_none_iff` — proved in Lean (module `lean4_core/Twentyfifth/Map.lean`; axioms: propext; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Map.lean::readBack25_none_smallest` — proved in Lean (module `lean4_core/Twentyfifth/Map.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Rename.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Rename.lean::readBack25_none_smallest_writing` — proved in Lean (module `lean4_core/Twentyfifth/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Map.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Map.lean::readBack25_oneFilled` — proved in Lean (module `lean4_core/Twentyfifth/Map.lean`; axioms: none; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Map.lean::readBack25_some` — proved in Lean (module `lean4_core/Twentyfifth/Map.lean`; axioms: propext; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Record.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Record.lean::record_does_not_show_which_terms` — proved in Lean (module `lean4_core/Twentyfifth/Record.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Record.lean::record_pair_two_terms` — proved in Lean (module `lean4_core/Twentyfifth/Record.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Record.lean::record_shows_whether` — proved in Lean (module `lean4_core/Twentyfifth/Record.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Rename.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Rename.lean::rename25_comp` — proved in Lean (module `lean4_core/Twentyfifth/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Rename.lean::rename25_id` — proved in Lean (module `lean4_core/Twentyfifth/Rename.lean`; axioms: none; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Rename.lean::rename25_rename` — proved in Lean (module `lean4_core/Twentyfifth/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Rename.lean::rename25_wf` — proved in Lean (module `lean4_core/Twentyfifth/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Balance.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Balance.lean::balanced_iff` — proved in Lean (module `lean4_core/Twentyfifth/Balance.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Reach.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Reach.lean::fill` — proved in Lean (module `lean4_core/Twentyfifth/Reach.lean`; axioms: none; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Balance.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Balance.lean::n` — proved in Lean (module `lean4_core/Twentyfifth/Balance.lean`; axioms: none; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Balance.lean::refl` — proved in Lean (module `lean4_core/Twentyfifth/Balance.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Rename.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Rename.lean::rename` — proved in Lean (module `lean4_core/Twentyfifth/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Rename.lean::sameW25` — proved in Lean (module `lean4_core/Twentyfifth/Rename.lean`; axioms: none; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Reach.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Reach.lean::swap` — proved in Lean (module `lean4_core/Twentyfifth/Reach.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Balance.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Balance.lean::symm` — proved in Lean (module `lean4_core/Twentyfifth/Balance.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Rename.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Rename.lean::told_iff` — proved in Lean (module `lean4_core/Twentyfifth/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Balance.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Balance.lean::trans` — proved in Lean (module `lean4_core/Twentyfifth/Balance.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Reach.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Reach.lean::same25_swap_iff` — proved in Lean (module `lean4_core/Twentyfifth/Reach.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Balance.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Balance.lean::around25` — proved in Lean (module `lean4_core/Twentyfifth/Balance.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Cost.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Cost.lean::same_build` — proved in Lean (module `lean4_core/Twentyfifth/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Balance.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Balance.lean::sameRecord_nothing` — proved in Lean (module `lean4_core/Twentyfifth/Balance.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Rename.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Rename.lean::n` — proved in Lean (module `lean4_core/Twentyfifth/Rename.lean`; axioms: none; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Rename.lean::refl` — proved in Lean (module `lean4_core/Twentyfifth/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Rename.lean::symm` — proved in Lean (module `lean4_core/Twentyfifth/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Rename.lean::told_iff` — proved in Lean (module `lean4_core/Twentyfifth/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Rename.lean::trans` — proved in Lean (module `lean4_core/Twentyfifth/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Map.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Map.lean::seventh_pair_merge25` — proved in Lean (module `lean4_core/Twentyfifth/Map.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Cost.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Cost.lean::cost_le` — proved in Lean (module `lean4_core/Twentyfifth/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Reach.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Reach.lean::n_pos` — proved in Lean (module `lean4_core/Twentyfifth/Reach.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Cost.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Cost.lean::not_same` — proved in Lean (module `lean4_core/Twentyfifth/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Cost.lean::psi_le` — proved in Lean (module `lean4_core/Twentyfifth/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Reach.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Reach.lean::swap` — proved in Lean (module `lean4_core/Twentyfifth/Reach.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Reach.lean::swap25_wf` — proved in Lean (module `lean4_core/Twentyfifth/Reach.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Rename.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Rename.lean::swapBC_rw` — proved in Lean (module `lean4_core/Twentyfifth/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Map.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Map.lean::three_le_of_filled` — proved in Lean (module `lean4_core/Twentyfifth/Map.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Blind.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Blind.lean::three_others` — proved in Lean (module `lean4_core/Twentyfifth/Blind.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Balance.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Balance.lean::told_iff` — proved in Lean (module `lean4_core/Twentyfifth/Balance.lean`; axioms: propext; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Balance.lean::told_not_nothing` — proved in Lean (module `lean4_core/Twentyfifth/Balance.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Rename.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Rename.lean::told_rename` — proved in Lean (module `lean4_core/Twentyfifth/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Reach.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Reach.lean::told_swap` — proved in Lean (module `lean4_core/Twentyfifth/Reach.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Rename.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Rename.lean::distinct_map` — proved in Lean (module `lean4_core/Twentyfifth/Rename.lean`; axioms: none; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Fill.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Fill.lean::distinct_rot` — proved in Lean (module `lean4_core/Twentyfifth/Fill.lean`; axioms: none; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Rename.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Rename.lean::map_gf` — proved in Lean (module `lean4_core/Twentyfifth/Rename.lean`; axioms: none; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Rename.lean::map_map` — proved in Lean (module `lean4_core/Twentyfifth/Rename.lean`; axioms: none; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Rename.lean::map_rot` — proved in Lean (module `lean4_core/Twentyfifth/Rename.lean`; axioms: none; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Fill.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Fill.lean::norm_cases` — proved in Lean (module `lean4_core/Twentyfifth/Fill.lean`; axioms: none; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Fill.lean::norm_distinct` — proved in Lean (module `lean4_core/Twentyfifth/Fill.lean`; axioms: none; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Fill.lean::norm_eq_self` — proved in Lean (module `lean4_core/Twentyfifth/Fill.lean`; axioms: none; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Fill.lean::norm_least` — proved in Lean (module `lean4_core/Twentyfifth/Fill.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Rename.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Rename.lean::norm_map_norm` — proved in Lean (module `lean4_core/Twentyfifth/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Fill.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Fill.lean::norm_mk` — proved in Lean (module `lean4_core/Twentyfifth/Fill.lean`; axioms: none; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Fill.lean::norm_norm` — proved in Lean (module `lean4_core/Twentyfifth/Fill.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Fill.lean::norm_rot` — proved in Lean (module `lean4_core/Twentyfifth/Fill.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Fill.lean::norm_within` — proved in Lean (module `lean4_core/Twentyfifth/Fill.lean`; axioms: none; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Rename.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Rename.lean::rename_rename` — proved in Lean (module `lean4_core/Twentyfifth/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Rename.lean::within_map` — proved in Lean (module `lean4_core/Twentyfifth/Rename.lean`; axioms: none; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Fill.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Fill.lean::within_rot` — proved in Lean (module `lean4_core/Twentyfifth/Fill.lean`; axioms: none; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Map.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Map.lean::tri_three` — proved in Lean (module `lean4_core/Twentyfifth/Map.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Blind.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Blind.lean::two_triples_do_not_decide` — proved in Lean (module `lean4_core/Twentyfifth/Blind.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Fill.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Fill.lean::within_glue` — proved in Lean (module `lean4_core/Twentyfifth/Fill.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfifth/Record.lean`

- `H3V7N5QF:lean4_core/Twentyfifth/Record.lean::wLoop_wf` — proved in Lean (module `lean4_core/Twentyfifth/Record.lean`; axioms: propext; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfifth/Record.lean::wPair_wf` — proved in Lean (module `lean4_core/Twentyfifth/Record.lean`; axioms: propext; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Map.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Map.lean::anyFilled_iff` — proved in Lean (module `lean4_core/Twentyfourth/Map.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Map.lean::anyFilled_ofSt` — proved in Lean (module `lean4_core/Twentyfourth/Map.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Record.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Record.lean::arbA_wf` — proved in Lean (module `lean4_core/Twentyfourth/Record.lean`; axioms: propext; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Record.lean::arcThree_wf` — proved in Lean (module `lean4_core/Twentyfourth/Record.lean`; axioms: propext; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Tell.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Tell.lean::aroundFilled_never_told` — proved in Lean (module `lean4_core/Twentyfourth/Tell.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Tell.lean::awayOne_fill_told` — proved in Lean (module `lean4_core/Twentyfourth/Tell.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Tell.lean::awayOne_not_told` — proved in Lean (module `lean4_core/Twentyfourth/Tell.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Same.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Same.lean::balances_iff` — proved in Lean (module `lean4_core/Twentyfourth/Same.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Swap.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Swap.lean::balances_swap` — proved in Lean (module `lean4_core/Twentyfourth/Swap.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Tell.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Tell.lean::balRec_nothing` — proved in Lean (module `lean4_core/Twentyfourth/Tell.lean`; axioms: none; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Tell.lean::balRec_true` — proved in Lean (module `lean4_core/Twentyfourth/Tell.lean`; axioms: propext; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Cost.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Cost.lean::congr` — proved in Lean (module `lean4_core/Twentyfourth/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Cost.lean::unique` — proved in Lean (module `lean4_core/Twentyfourth/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Cost.lean::cost24_eq` — proved in Lean (module `lean4_core/Twentyfourth/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Rename.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Rename.lean::cost24_every_writing` — proved in Lean (module `lean4_core/Twentyfourth/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Cost.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Cost.lean::cost24_le_pot` — proved in Lean (module `lean4_core/Twentyfourth/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Cost.lean::cost24_ofSt` — proved in Lean (module `lean4_core/Twentyfourth/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Cost.lean::cost24_oneFilled` — proved in Lean (module `lean4_core/Twentyfourth/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Swap.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Swap.lean::cost24_swap` — proved in Lean (module `lean4_core/Twentyfourth/Swap.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Record.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Record.lean::cost3_nothing` — proved in Lean (module `lean4_core/Twentyfourth/Record.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Cost.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Cost.lean::decide_lt_succ` — proved in Lean (module `lean4_core/Twentyfourth/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Record.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Record.lean::dsum_le_length` — proved in Lean (module `lean4_core/Twentyfourth/Record.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Swap.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Swap.lean::empty24_swap` — proved in Lean (module `lean4_core/Twentyfourth/Swap.lean`; axioms: none; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Basic.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Basic.lean::empty24_wf` — proved in Lean (module `lean4_core/Twentyfourth/Basic.lean`; axioms: none; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Basic.lean::fc_addTerm` — proved in Lean (module `lean4_core/Twentyfourth/Basic.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Basic.lean::fc_fill` — proved in Lean (module `lean4_core/Twentyfourth/Basic.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Basic.lean::fc_identify_le` — proved in Lean (module `lean4_core/Twentyfourth/Basic.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Map.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Map.lean::fc_pos` — proved in Lean (module `lean4_core/Twentyfourth/Map.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Rename.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Rename.lean::fc_rename` — proved in Lean (module `lean4_core/Twentyfourth/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Record.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Record.lean::fewest_arbA` — proved in Lean (module `lean4_core/Twentyfourth/Record.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Record.lean::fewest_arcThree` — proved in Lean (module `lean4_core/Twentyfourth/Record.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Record.lean::fewest_loopA` — proved in Lean (module `lean4_core/Twentyfourth/Record.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Record.lean::fewest_loopAsb` — proved in Lean (module `lean4_core/Twentyfourth/Record.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Cost.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Cost.lean::fill_cost` — proved in Lean (module `lean4_core/Twentyfourth/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Same.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Same.lean::fillLoops_same` — proved in Lean (module `lean4_core/Twentyfourth/Same.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Map.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Map.lean::forget_merges` — proved in Lean (module `lean4_core/Twentyfourth/Map.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Basic.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Basic.lean::F_out` — proved in Lean (module `lean4_core/Twentyfourth/Basic.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Swap.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Swap.lean::swap_swap` — proved in Lean (module `lean4_core/Twentyfourth/Swap.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Reach.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Reach.lean::funext_plain_fill` — proved in Lean (module `lean4_core/Twentyfourth/Reach.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Reach.lean::glue_move` — proved in Lean (module `lean4_core/Twentyfourth/Reach.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Reach.lean::i2_unfills` — proved in Lean (module `lean4_core/Twentyfourth/Reach.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Tell.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Tell.lean::identify_tells` — proved in Lean (module `lean4_core/Twentyfourth/Tell.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Cost.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Cost.lean::identify_two_filled_even` — proved in Lean (module `lean4_core/Twentyfourth/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Basic.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Basic.lean::idF_false` — proved in Lean (module `lean4_core/Twentyfourth/Basic.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Basic.lean::idF_iff` — proved in Lean (module `lean4_core/Twentyfourth/Basic.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Reach.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Reach.lean::idF_move` — proved in Lean (module `lean4_core/Twentyfourth/Reach.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Basic.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Basic.lean::idF_of` — proved in Lean (module `lean4_core/Twentyfourth/Basic.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Basic.lean::ind_le_one` — proved in Lean (module `lean4_core/Twentyfourth/Basic.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Record.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Record.lean::length_pos_of_excess` — proved in Lean (module `lean4_core/Twentyfourth/Record.lean`; axioms: propext; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Record.lean::loopA_wf` — proved in Lean (module `lean4_core/Twentyfourth/Record.lean`; axioms: propext; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Record.lean::loopAsb_wf` — proved in Lean (module `lean4_core/Twentyfourth/Record.lean`; axioms: propext; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Map.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Map.lean::n_le_phi` — proved in Lean (module `lean4_core/Twentyfourth/Map.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Tell.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Tell.lean::never_told_of_loops_zero` — proved in Lean (module `lean4_core/Twentyfourth/Tell.lean`; axioms: none; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Same.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Same.lean::no_merge` — proved in Lean (module `lean4_core/Twentyfourth/Same.lean`; axioms: none; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Tell.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Tell.lean::not_told_cases` — proved in Lean (module `lean4_core/Twentyfourth/Tell.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Tell.lean::nothing_balances` — proved in Lean (module `lean4_core/Twentyfourth/Tell.lean`; axioms: none; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Basic.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Basic.lean::ofSt_empty` — proved in Lean (module `lean4_core/Twentyfourth/Basic.lean`; axioms: none; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Basic.lean::ofSt_fc` — proved in Lean (module `lean4_core/Twentyfourth/Basic.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Basic.lean::ofSt_wf` — proved in Lean (module `lean4_core/Twentyfourth/Basic.lean`; axioms: none; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Cost.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Cost.lean::oneFilled_wf` — proved in Lean (module `lean4_core/Twentyfourth/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Cost.lean::pairFilled_wf` — proved in Lean (module `lean4_core/Twentyfourth/Cost.lean`; axioms: none; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Record.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Record.lean::phi_nothing` — proved in Lean (module `lean4_core/Twentyfourth/Record.lean`; axioms: propext; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Cost.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Cost.lean::pot_empty` — proved in Lean (module `lean4_core/Twentyfourth/Cost.lean`; axioms: propext; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Cost.lean::pot_le_size24` — proved in Lean (module `lean4_core/Twentyfourth/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Rename.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Rename.lean::pot_rename` — proved in Lean (module `lean4_core/Twentyfourth/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Basic.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Basic.lean::toReach24` — proved in Lean (module `lean4_core/Twentyfourth/Basic.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Reach.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Reach.lean::forget` — proved in Lean (module `lean4_core/Twentyfourth/Reach.lean`; axioms: none; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Cost.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Cost.lean::pot_le` — proved in Lean (module `lean4_core/Twentyfourth/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Cost.lean::raising` — proved in Lean (module `lean4_core/Twentyfourth/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Basic.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Basic.lean::single` — proved in Lean (module `lean4_core/Twentyfourth/Basic.lean`; axioms: none; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Cost.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Cost.lean::size24_le` — proved in Lean (module `lean4_core/Twentyfourth/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Swap.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Swap.lean::swap` — proved in Lean (module `lean4_core/Twentyfourth/Swap.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Basic.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Basic.lean::trans` — proved in Lean (module `lean4_core/Twentyfourth/Basic.lean`; axioms: none; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Reach.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Reach.lean::reach24_atoms` — proved in Lean (module `lean4_core/Twentyfourth/Reach.lean`; axioms: none; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Reach.lean::reach24_clear` — proved in Lean (module `lean4_core/Twentyfourth/Reach.lean`; axioms: propext; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Reach.lean::reach24_collapse` — proved in Lean (module `lean4_core/Twentyfourth/Reach.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Reach.lean::reach24_criterion` — proved in Lean (module `lean4_core/Twentyfourth/Reach.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Reach.lean::reach24_fillFrom` — proved in Lean (module `lean4_core/Twentyfourth/Reach.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Cost.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Cost.lean::reach24_fillUpTo` — proved in Lean (module `lean4_core/Twentyfourth/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Reach.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Reach.lean::reach24_from_one` — proved in Lean (module `lean4_core/Twentyfourth/Reach.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Reach.lean::reach24_grow` — proved in Lean (module `lean4_core/Twentyfourth/Reach.lean`; axioms: none; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Reach.lean::reach24_mutual` — proved in Lean (module `lean4_core/Twentyfourth/Reach.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Swap.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Swap.lean::reach24_swap` — proved in Lean (module `lean4_core/Twentyfourth/Swap.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Cost.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Cost.lean::reach24_upper` — proved in Lean (module `lean4_core/Twentyfourth/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Map.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Map.lean::readBack_congr` — proved in Lean (module `lean4_core/Twentyfourth/Map.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Map.lean::readBack_none_cost` — proved in Lean (module `lean4_core/Twentyfourth/Map.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Map.lean::readBack_none_iff` — proved in Lean (module `lean4_core/Twentyfourth/Map.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Map.lean::readBack_ofSt` — proved in Lean (module `lean4_core/Twentyfourth/Map.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Map.lean::readBack_oneFilled` — proved in Lean (module `lean4_core/Twentyfourth/Map.lean`; axioms: none; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Map.lean::readBack_some` — proved in Lean (module `lean4_core/Twentyfourth/Map.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Record.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Record.lean::record23_does_not_show_which` — proved in Lean (module `lean4_core/Twentyfourth/Record.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Record.lean::record23_does_not_show_which_three` — proved in Lean (module `lean4_core/Twentyfourth/Record.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Record.lean::record_whether` — proved in Lean (module `lean4_core/Twentyfourth/Record.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Rename.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Rename.lean::rename_wf24` — proved in Lean (module `lean4_core/Twentyfourth/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Basic.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Basic.lean::rsum_image_le` — proved in Lean (module `lean4_core/Twentyfourth/Basic.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Basic.lean::rsum_ind_false` — proved in Lean (module `lean4_core/Twentyfourth/Basic.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Basic.lean::rsum_le` — proved in Lean (module `lean4_core/Twentyfourth/Basic.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Basic.lean::rsum_zero` — proved in Lean (module `lean4_core/Twentyfourth/Basic.lean`; axioms: propext; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Same.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Same.lean::balances` — proved in Lean (module `lean4_core/Twentyfourth/Same.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Same.lean::fc` — proved in Lean (module `lean4_core/Twentyfourth/Same.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Same.lean::fill` — proved in Lean (module `lean4_core/Twentyfourth/Same.lean`; axioms: none; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Same.lean::n` — proved in Lean (module `lean4_core/Twentyfourth/Same.lean`; axioms: none; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Same.lean::refl` — proved in Lean (module `lean4_core/Twentyfourth/Same.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Rename.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Rename.lean::sameW24` — proved in Lean (module `lean4_core/Twentyfourth/Rename.lean`; axioms: none; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Swap.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Swap.lean::swap` — proved in Lean (module `lean4_core/Twentyfourth/Swap.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Same.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Same.lean::symm` — proved in Lean (module `lean4_core/Twentyfourth/Same.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Tell.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Tell.lean::told` — proved in Lean (module `lean4_core/Twentyfourth/Tell.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Same.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Same.lean::trans` — proved in Lean (module `lean4_core/Twentyfourth/Same.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Tell.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Tell.lean::same24_nothing_iff` — proved in Lean (module `lean4_core/Twentyfourth/Tell.lean`; axioms: none; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Same.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Same.lean::same24_ofSt_iff` — proved in Lean (module `lean4_core/Twentyfourth/Same.lean`; axioms: none; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Reach.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Reach.lean::same24_plainSt` — proved in Lean (module `lean4_core/Twentyfourth/Reach.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Swap.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Swap.lean::same24_swap_iff` — proved in Lean (module `lean4_core/Twentyfourth/Swap.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Rename.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Rename.lean::balances` — proved in Lean (module `lean4_core/Twentyfourth/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Rename.lean::pointwise` — proved in Lean (module `lean4_core/Twentyfourth/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Rename.lean::told` — proved in Lean (module `lean4_core/Twentyfourth/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Rename.lean::sameW24_ofSt_iff` — proved in Lean (module `lean4_core/Twentyfourth/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Map.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Map.lean::seventh_pair_merge24` — proved in Lean (module `lean4_core/Twentyfourth/Map.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Cost.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Cost.lean::shortest24` — proved in Lean (module `lean4_core/Twentyfourth/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Map.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Map.lean::smallest_none` — proved in Lean (module `lean4_core/Twentyfourth/Map.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Map.lean::smallest_none_unique` — proved in Lean (module `lean4_core/Twentyfourth/Map.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Basic.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Basic.lean::toStep24` — proved in Lean (module `lean4_core/Twentyfourth/Basic.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Cost.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Cost.lean::cost_le` — proved in Lean (module `lean4_core/Twentyfourth/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Basic.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Basic.lean::forget` — proved in Lean (module `lean4_core/Twentyfourth/Basic.lean`; axioms: none; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Cost.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Cost.lean::not_same24` — proved in Lean (module `lean4_core/Twentyfourth/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Cost.lean::pot_le` — proved in Lean (module `lean4_core/Twentyfourth/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Cost.lean::size24_step` — proved in Lean (module `lean4_core/Twentyfourth/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Swap.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Swap.lean::swap` — proved in Lean (module `lean4_core/Twentyfourth/Swap.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Swap.lean::swap_wf24` — proved in Lean (module `lean4_core/Twentyfourth/Swap.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Tell.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Tell.lean::told_after_fill` — proved in Lean (module `lean4_core/Twentyfourth/Tell.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Tell.lean::told_iff` — proved in Lean (module `lean4_core/Twentyfourth/Tell.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Tell.lean::told_not_nothing` — proved in Lean (module `lean4_core/Twentyfourth/Tell.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Swap.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Swap.lean::told_swap` — proved in Lean (module `lean4_core/Twentyfourth/Swap.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Tell.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Tell.lean::toldOne_told` — proved in Lean (module `lean4_core/Twentyfourth/Tell.lean`; axioms: none; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Reach.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Reach.lean::twentythird_criterion_fails` — proved in Lean (module `lean4_core/Twentyfourth/Reach.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentyfourth/Tell.lean`

- `H3V7N5QF:lean4_core/Twentyfourth/Tell.lean::twoWayFilled_never_told` — proved in Lean (module `lean4_core/Twentyfourth/Tell.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentyfourth/Tell.lean::twoWayFilled_not_nothing` — proved in Lean (module `lean4_core/Twentyfourth/Tell.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentysecond/Undo.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Undo.lean::addition_undoes_addition` — proved in Lean (module `lean4_core/Twentysecond/Undo.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Undo.lean::addition_undoes_not_in_ninth` — proved in Lean (module `lean4_core/Twentysecond/Undo.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/State.lean`

- `H3V7N5QF:lean4_core/Twentysecond/State.lean::reach` — proved in Lean (module `lean4_core/Twentysecond/State.lean`; axioms: none; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/State.lean::size` — proved in Lean (module `lean4_core/Twentysecond/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/State.lean::trans` — proved in Lean (module `lean4_core/Twentysecond/State.lean`; axioms: none; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Cost.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Cost.lean::addReach_atoms` — proved in Lean (module `lean4_core/Twentysecond/Cost.lean`; axioms: none; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Cost.lean::addReach_terms` — proved in Lean (module `lean4_core/Twentysecond/Cost.lean`; axioms: none; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/State.lean`

- `H3V7N5QF:lean4_core/Twentysecond/State.lean::size` — proved in Lean (module `lean4_core/Twentysecond/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/State.lean::step` — proved in Lean (module `lean4_core/Twentysecond/State.lean`; axioms: none; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Seventh.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Seventh.lean::asa_wf` — proved in Lean (module `lean4_core/Twentysecond/Seventh.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Basic.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Basic.lean::eq_partner_comm` — proved in Lean (module `lean4_core/Twentysecond/Basic.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/State.lean`

- `H3V7N5QF:lean4_core/Twentysecond/State.lean::mapT_partner` — proved in Lean (module `lean4_core/Twentysecond/State.lean`; axioms: none; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Basic.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Basic.lean::partner_eq_iff` — proved in Lean (module `lean4_core/Twentysecond/Basic.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Basic.lean::partner_eq_partner_iff` — proved in Lean (module `lean4_core/Twentysecond/Basic.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Basic.lean::partner_inj` — proved in Lean (module `lean4_core/Twentysecond/Basic.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Basic.lean::partner_ne` — proved in Lean (module `lean4_core/Twentysecond/Basic.lean`; axioms: none; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Basic.lean::partner_partner` — proved in Lean (module `lean4_core/Twentysecond/Basic.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Seventh.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Seventh.lean::carried_additions_merge` — proved in Lean (module `lean4_core/Twentysecond/Seventh.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Same.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Same.lean::count_del_add` — proved in Lean (module `lean4_core/Twentysecond/Same.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Basic.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Basic.lean::count_del_ne` — proved in Lean (module `lean4_core/Twentysecond/Basic.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Basic.lean::count_del_self` — proved in Lean (module `lean4_core/Twentysecond/Basic.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Basic.lean::count_eq_zero_of_not_mem` — proved in Lean (module `lean4_core/Twentysecond/Basic.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Basic.lean::count_map_not_image` — proved in Lean (module `lean4_core/Twentysecond/Basic.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Basic.lean::count_map_of_inj` — proved in Lean (module `lean4_core/Twentysecond/Basic.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Plain.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Plain.lean::count_plain` — proved in Lean (module `lean4_core/Twentysecond/Plain.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Plain.lean::count_plain_le` — proved in Lean (module `lean4_core/Twentysecond/Plain.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Basic.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Basic.lean::count_pos_of_mem` — proved in Lean (module `lean4_core/Twentysecond/Basic.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Plain.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Plain.lean::count_together` — proved in Lean (module `lean4_core/Twentysecond/Plain.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Basic.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Basic.lean::del_cons_ne` — proved in Lean (module `lean4_core/Twentysecond/Basic.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Basic.lean::del_cons_self` — proved in Lean (module `lean4_core/Twentysecond/Basic.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Basic.lean::del_nil` — proved in Lean (module `lean4_core/Twentysecond/Basic.lean`; axioms: none; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Basic.lean::del_of_not_mem` — proved in Lean (module `lean4_core/Twentysecond/Basic.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Basic.lean::del_perm` — proved in Lean (module `lean4_core/Twentysecond/Basic.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Reach.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Reach.lean::empty_never_returned` — proved in Lean (module `lean4_core/Twentysecond/Reach.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/State.lean`

- `H3V7N5QF:lean4_core/Twentysecond/State.lean::empty_wf` — proved in Lean (module `lean4_core/Twentysecond/State.lean`; axioms: none; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/State.lean::eq_empty_of_wf` — proved in Lean (module `lean4_core/Twentysecond/State.lean`; axioms: none; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentysecond/Basic.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Basic.lean::eq_nil_of_count_zero` — proved in Lean (module `lean4_core/Twentysecond/Basic.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Swap.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Swap.lean::excess_swap` — proved in Lean (module `lean4_core/Twentysecond/Swap.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentysecond/Cost.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Cost.lean::fewest_changes` — proved in Lean (module `lean4_core/Twentysecond/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Rename.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Rename.lean::fewest_changes_every_writing` — proved in Lean (module `lean4_core/Twentysecond/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Reach.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Reach.lean::first_change_adds_term` — proved in Lean (module `lean4_core/Twentysecond/Reach.lean`; axioms: none; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Same.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Same.lean::same` — proved in Lean (module `lean4_core/Twentysecond/Same.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Rename.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Rename.lean::wf_iff` — proved in Lean (module `lean4_core/Twentysecond/Rename.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Same.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Same.lean::gen_iff_same` — proved in Lean (module `lean4_core/Twentysecond/Same.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Same.lean::gen_plain` — proved in Lean (module `lean4_core/Twentysecond/Same.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Same.lean::gen_strip` — proved in Lean (module `lean4_core/Twentysecond/Same.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Rename.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Rename.lean::wf_iff` — proved in Lean (module `lean4_core/Twentysecond/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Rename.lean::genW_iff_sameW` — proved in Lean (module `lean4_core/Twentysecond/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/State.lean`

- `H3V7N5QF:lean4_core/Twentysecond/State.lean::glue_lt` — proved in Lean (module `lean4_core/Twentysecond/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Record.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Record.lean::identify_takes` — proved in Lean (module `lean4_core/Twentysecond/Record.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Rename.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Rename.lean::comp` — proved in Lean (module `lean4_core/Twentysecond/Rename.lean`; axioms: none; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Rename.lean::id` — proved in Lean (module `lean4_core/Twentysecond/Rename.lean`; axioms: none; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Rename.lean::inj` — proved in Lean (module `lean4_core/Twentysecond/Rename.lean`; axioms: none; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Rename.lean::symm` — proved in Lean (module `lean4_core/Twentysecond/Rename.lean`; axioms: none; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Same.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Same.lean::ite_partner_left` — proved in Lean (module `lean4_core/Twentysecond/Same.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Same.lean::ite_partner_partner` — proved in Lean (module `lean4_core/Twentysecond/Same.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Basic.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Basic.lean::length_del` — proved in Lean (module `lean4_core/Twentysecond/Basic.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Cost.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Cost.lean::length_plain_cons` — proved in Lean (module `lean4_core/Twentysecond/Cost.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Plain.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Plain.lean::length_plain_le` — proved in Lean (module `lean4_core/Twentysecond/Plain.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Plain.lean::length_plain_map_le` — proved in Lean (module `lean4_core/Twentysecond/Plain.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Plain.lean::length_split` — proved in Lean (module `lean4_core/Twentysecond/Plain.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Record.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Record.lean::length_spread` — proved in Lean (module `lean4_core/Twentysecond/Record.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Record.lean::loops_together` — proved in Lean (module `lean4_core/Twentysecond/Record.lean`; axioms: none; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Basic.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Basic.lean::map_del_of_inj` — proved in Lean (module `lean4_core/Twentysecond/Basic.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Rename.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Rename.lean::map_del_of_injOn` — proved in Lean (module `lean4_core/Twentysecond/Rename.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Rename.lean::map_eq_self` — proved in Lean (module `lean4_core/Twentysecond/Rename.lean`; axioms: none; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Record.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Record.lean::map_spread` — proved in Lean (module `lean4_core/Twentysecond/Record.lean`; axioms: none; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Rename.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Rename.lean::mapT_inj` — proved in Lean (module `lean4_core/Twentysecond/Rename.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Swap.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Swap.lean::mem_map_partner` — proved in Lean (module `lean4_core/Twentysecond/Swap.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Basic.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Basic.lean::mem_of_count_pos` — proved in Lean (module `lean4_core/Twentysecond/Basic.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Basic.lean::mem_of_mem_del` — proved in Lean (module `lean4_core/Twentysecond/Basic.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Plain.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Plain.lean::mem_of_mem_plain` — proved in Lean (module `lean4_core/Twentysecond/Plain.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Plain.lean::mem_of_mem_together` — proved in Lean (module `lean4_core/Twentysecond/Plain.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Record.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Record.lean::mem_spread` — proved in Lean (module `lean4_core/Twentysecond/Record.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Merge.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Merge.lean::merge_loses` — proved in Lean (module `lean4_core/Twentysecond/Merge.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Undo.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Undo.lean::ninth_additions_never_return` — proved in Lean (module `lean4_core/Twentysecond/Undo.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Rename.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Rename.lean::ninth_additions_never_return_every_writing` — proved in Lean (module `lean4_core/Twentysecond/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Seventh.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Seventh.lean::ninth_not_one_to_one` — proved in Lean (module `lean4_core/Twentysecond/Seventh.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Record.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Record.lean::ninth_record_add` — proved in Lean (module `lean4_core/Twentysecond/Record.lean`; axioms: none; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Rename.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Rename.lean::ofR_rename` — proved in Lean (module `lean4_core/Twentysecond/Rename.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Seventh.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Seventh.lean::ofR_same_iff` — proved in Lean (module `lean4_core/Twentysecond/Seventh.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Rename.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Rename.lean::ofR_sameW_iff` — proved in Lean (module `lean4_core/Twentysecond/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Seventh.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Seventh.lean::ofR_wf` — proved in Lean (module `lean4_core/Twentysecond/Seventh.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Swap.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Swap.lean::partner_injective` — proved in Lean (module `lean4_core/Twentysecond/Swap.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Basic.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Basic.lean::perm_cons_del` — proved in Lean (module `lean4_core/Twentysecond/Basic.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Basic.lean::perm_of_count` — proved in Lean (module `lean4_core/Twentysecond/Basic.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Basic.lean::perm_of_perm_map_of_inj` — proved in Lean (module `lean4_core/Twentysecond/Basic.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Plain.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Plain.lean::perm_split` — proved in Lean (module `lean4_core/Twentysecond/Plain.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Cost.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Cost.lean::phi_asa` — proved in Lean (module `lean4_core/Twentysecond/Cost.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Cost.lean::phi_empty` — proved in Lean (module `lean4_core/Twentysecond/Cost.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Cost.lean::phi_le_size` — proved in Lean (module `lean4_core/Twentysecond/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Seventh.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Seventh.lean::phi_ofR` — proved in Lean (module `lean4_core/Twentysecond/Seventh.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Cost.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Cost.lean::phi_parity_size` — proved in Lean (module `lean4_core/Twentysecond/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Rename.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Rename.lean::phi_rename` — proved in Lean (module `lean4_core/Twentysecond/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Swap.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Swap.lean::phi_swap` — proved in Lean (module `lean4_core/Twentysecond/Swap.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Plain.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Plain.lean::plain_append_together` — proved in Lean (module `lean4_core/Twentysecond/Plain.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Plain.lean::plain_cons` — proved in Lean (module `lean4_core/Twentysecond/Plain.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Plain.lean::plain_cons_perm` — proved in Lean (module `lean4_core/Twentysecond/Plain.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Plain.lean::plain_eq_self` — proved in Lean (module `lean4_core/Twentysecond/Plain.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Rename.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Rename.lean::plain_eq_self_of_together_nil` — proved in Lean (module `lean4_core/Twentysecond/Rename.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Plain.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Plain.lean::plain_map_perm` — proved in Lean (module `lean4_core/Twentysecond/Plain.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Plain.lean::plain_nil` — proved in Lean (module `lean4_core/Twentysecond/Plain.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Seventh.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Seventh.lean::plain_ofR` — proved in Lean (module `lean4_core/Twentysecond/Seventh.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Plain.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Plain.lean::plain_parity` — proved in Lean (module `lean4_core/Twentysecond/Plain.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Plain.lean::plain_perm` — proved in Lean (module `lean4_core/Twentysecond/Plain.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Plain.lean::plain_perm_iff` — proved in Lean (module `lean4_core/Twentysecond/Plain.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Plain.lean::plain_plain` — proved in Lean (module `lean4_core/Twentysecond/Plain.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Plain.lean::plain_reduced` — proved in Lean (module `lean4_core/Twentysecond/Plain.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Rename.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Rename.lean::plain_rename` — proved in Lean (module `lean4_core/Twentysecond/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Merge.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Merge.lean::plain_states_stay_apart` — proved in Lean (module `lean4_core/Twentysecond/Merge.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Rename.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Rename.lean::plain_states_stay_apart_every_writing` — proved in Lean (module `lean4_core/Twentysecond/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Swap.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Swap.lean::plain_swap` — proved in Lean (module `lean4_core/Twentysecond/Swap.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Same.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Same.lean::plainSt_wf` — proved in Lean (module `lean4_core/Twentysecond/Same.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Seventh.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Seventh.lean::rAtom_inj` — proved in Lean (module `lean4_core/Twentysecond/Seventh.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/State.lean`

- `H3V7N5QF:lean4_core/Twentysecond/State.lean::additions` — proved in Lean (module `lean4_core/Twentysecond/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/State.lean::n_pos` — proved in Lean (module `lean4_core/Twentysecond/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentysecond/Cost.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Cost.lean::phi_le` — proved in Lean (module `lean4_core/Twentysecond/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/State.lean`

- `H3V7N5QF:lean4_core/Twentysecond/State.lean::single` — proved in Lean (module `lean4_core/Twentysecond/State.lean`; axioms: none; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/State.lean::size_le` — proved in Lean (module `lean4_core/Twentysecond/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/State.lean::trans` — proved in Lean (module `lean4_core/Twentysecond/State.lean`; axioms: none; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Seventh.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Seventh.lean::embed` — proved in Lean (module `lean4_core/Twentysecond/Seventh.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Reach.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Reach.lean::reach_clear` — proved in Lean (module `lean4_core/Twentysecond/Reach.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Reach.lean::reach_collapse` — proved in Lean (module `lean4_core/Twentysecond/Reach.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Reach.lean::reach_criterion` — proved in Lean (module `lean4_core/Twentysecond/Reach.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Reach.lean::reach_grow` — proved in Lean (module `lean4_core/Twentysecond/Reach.lean`; axioms: none; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Reach.lean::reach_mutual` — proved in Lean (module `lean4_core/Twentysecond/Reach.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Reach.lean::reach_of_same` — proved in Lean (module `lean4_core/Twentysecond/Reach.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Cost.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Cost.lean::reach_plainSt` — proved in Lean (module `lean4_core/Twentysecond/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentysecond/Seventh.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Seventh.lean::readBack_asa` — proved in Lean (module `lean4_core/Twentysecond/Seventh.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Seventh.lean::readBack_none_phi` — proved in Lean (module `lean4_core/Twentysecond/Seventh.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Rename.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Rename.lean::readBack_none_rename` — proved in Lean (module `lean4_core/Twentysecond/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Seventh.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Seventh.lean::readBack_none_smallest` — proved in Lean (module `lean4_core/Twentysecond/Seventh.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Seventh.lean::readBack_ofR` — proved in Lean (module `lean4_core/Twentysecond/Seventh.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Seventh.lean::readBack_same` — proved in Lean (module `lean4_core/Twentysecond/Seventh.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Record.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Record.lean::record_add` — proved in Lean (module `lean4_core/Twentysecond/Record.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Record.lean::record_addTerm` — proved in Lean (module `lean4_core/Twentysecond/Record.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Record.lean::record_identify` — proved in Lean (module `lean4_core/Twentysecond/Record.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Record.lean::record_remove` — proved in Lean (module `lean4_core/Twentysecond/Record.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Record.lean::recorded_same` — proved in Lean (module `lean4_core/Twentysecond/Record.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Record.lean::recorded_sum` — proved in Lean (module `lean4_core/Twentysecond/Record.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Basic.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Basic.lean::other_ne` — proved in Lean (module `lean4_core/Twentysecond/Basic.lean`; axioms: none; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Basic.lean::other_other` — proved in Lean (module `lean4_core/Twentysecond/Basic.lean`; axioms: none; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Rename.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Rename.lean::rename_comp` — proved in Lean (module `lean4_core/Twentysecond/Rename.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Rename.lean::rename_id` — proved in Lean (module `lean4_core/Twentysecond/Rename.lean`; axioms: none; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Rename.lean::rename_rename` — proved in Lean (module `lean4_core/Twentysecond/Rename.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Rename.lean::rename_wf` — proved in Lean (module `lean4_core/Twentysecond/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Seventh.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Seventh.lean::rParts_map` — proved in Lean (module `lean4_core/Twentysecond/Seventh.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Seventh.lean::rParts_none` — proved in Lean (module `lean4_core/Twentysecond/Seventh.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Seventh.lean::rParts_some` — proved in Lean (module `lean4_core/Twentysecond/Seventh.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Seventh.lean::rParts_some_of_all_r` — proved in Lean (module `lean4_core/Twentysecond/Seventh.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Same.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Same.lean::add` — proved in Lean (module `lean4_core/Twentysecond/Same.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Same.lean::addTerm` — proved in Lean (module `lean4_core/Twentysecond/Same.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Same.lean::identify` — proved in Lean (module `lean4_core/Twentysecond/Same.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Cost.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Cost.lean::phi` — proved in Lean (module `lean4_core/Twentysecond/Cost.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Same.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Same.lean::refl` — proved in Lean (module `lean4_core/Twentysecond/Same.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Same.lean::remove` — proved in Lean (module `lean4_core/Twentysecond/Same.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Rename.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Rename.lean::rename` — proved in Lean (module `lean4_core/Twentysecond/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Rename.lean::sameW` — proved in Lean (module `lean4_core/Twentysecond/Rename.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Swap.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Swap.lean::swap` — proved in Lean (module `lean4_core/Twentysecond/Swap.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Same.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Same.lean::symm` — proved in Lean (module `lean4_core/Twentysecond/Same.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Same.lean::trans` — proved in Lean (module `lean4_core/Twentysecond/Same.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Undo.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Undo.lean::same_add_add_iff` — proved in Lean (module `lean4_core/Twentysecond/Undo.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Same.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Same.lean::same_iff_excess` — proved in Lean (module `lean4_core/Twentysecond/Same.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Seventh.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Seventh.lean::same_ofR_of_readBack` — proved in Lean (module `lean4_core/Twentysecond/Seventh.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Same.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Same.lean::same_plainSt` — proved in Lean (module `lean4_core/Twentysecond/Same.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Same.lean::same_remove_add_partner` — proved in Lean (module `lean4_core/Twentysecond/Same.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Swap.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Swap.lean::same_swap_iff` — proved in Lean (module `lean4_core/Twentysecond/Swap.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Same.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Same.lean::same` — proved in Lean (module `lean4_core/Twentysecond/Same.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/State.lean`

- `H3V7N5QF:lean4_core/Twentysecond/State.lean::size` — proved in Lean (module `lean4_core/Twentysecond/State.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Rename.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Rename.lean::n` — proved in Lean (module `lean4_core/Twentysecond/Rename.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Rename.lean::phi` — proved in Lean (module `lean4_core/Twentysecond/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Rename.lean::refl` — proved in Lean (module `lean4_core/Twentysecond/Rename.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Rename.lean::symm` — proved in Lean (module `lean4_core/Twentysecond/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Rename.lean::trans` — proved in Lean (module `lean4_core/Twentysecond/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Cost.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Cost.lean::shortest_additions` — proved in Lean (module `lean4_core/Twentysecond/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Cost.lean::shortest_all_plain` — proved in Lean (module `lean4_core/Twentysecond/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Cost.lean::shortest_all_plain_aux` — proved in Lean (module `lean4_core/Twentysecond/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Cost.lean::shortest_prefix` — proved in Lean (module `lean4_core/Twentysecond/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Cost.lean::size_empty` — proved in Lean (module `lean4_core/Twentysecond/Cost.lean`; axioms: none; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Cost.lean::size_eq_phi_add_together` — proved in Lean (module `lean4_core/Twentysecond/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Rename.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Rename.lean::size_rename` — proved in Lean (module `lean4_core/Twentysecond/Rename.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Merge.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Merge.lean::state_of_result_and_together` — proved in Lean (module `lean4_core/Twentysecond/Merge.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/State.lean`

- `H3V7N5QF:lean4_core/Twentysecond/State.lean::n_pos` — proved in Lean (module `lean4_core/Twentysecond/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Cost.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Cost.lean::not_same` — proved in Lean (module `lean4_core/Twentysecond/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Cost.lean::phi_identify` — proved in Lean (module `lean4_core/Twentysecond/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Cost.lean::phi_le` — proved in Lean (module `lean4_core/Twentysecond/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Cost.lean::phi_parity` — proved in Lean (module `lean4_core/Twentysecond/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/State.lean`

- `H3V7N5QF:lean4_core/Twentysecond/State.lean::size_step` — proved in Lean (module `lean4_core/Twentysecond/State.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Swap.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Swap.lean::swap` — proved in Lean (module `lean4_core/Twentysecond/Swap.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Seventh.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Seventh.lean::embed` — proved in Lean (module `lean4_core/Twentysecond/Seventh.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Same.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Same.lean::step_of_same` — proved in Lean (module `lean4_core/Twentysecond/Same.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Swap.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Swap.lean::swap_swap` — proved in Lean (module `lean4_core/Twentysecond/Swap.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Swap.lean::swap_wf` — proved in Lean (module `lean4_core/Twentysecond/Swap.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentysecond/Plain.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Plain.lean::append` — proved in Lean (module `lean4_core/Twentysecond/Plain.lean`; axioms: none; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Plain.lean::count` — proved in Lean (module `lean4_core/Twentysecond/Plain.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Plain.lean::even` — proved in Lean (module `lean4_core/Twentysecond/Plain.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Plain.lean::map` — proved in Lean (module `lean4_core/Twentysecond/Plain.lean`; axioms: none; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Plain.lean::map_partner` — proved in Lean (module `lean4_core/Twentysecond/Plain.lean`; axioms: none; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Plain.lean::together_cons` — proved in Lean (module `lean4_core/Twentysecond/Plain.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Merge.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Merge.lean::together_eq_nil_of_plain` — proved in Lean (module `lean4_core/Twentysecond/Merge.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentysecond/Merge.lean::together_plain` — proved in Lean (module `lean4_core/Twentysecond/Merge.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Rename.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Rename.lean::together_rename_nil` — proved in Lean (module `lean4_core/Twentysecond/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Plain.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Plain.lean::together_together` — proved in Lean (module `lean4_core/Twentysecond/Plain.lean`; axioms: propext; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentysecond/Undo.lean`

- `H3V7N5QF:lean4_core/Twentysecond/Undo.lean::two_additions_return_iff` — proved in Lean (module `lean4_core/Twentysecond/Undo.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentysecond/lean_axioms.txt`)

### `lean4_core/Twentythird/Cost.lean`

- `H3V7N5QF:lean4_core/Twentythird/Cost.lean::adding_a_term_raises_the_cost` — proved in Lean (module `lean4_core/Twentythird/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Nothing.lean`

- `H3V7N5QF:lean4_core/Twentythird/Nothing.lean::addTerm_not_respected` — proved in Lean (module `lean4_core/Twentythird/Nothing.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentythird/Map.lean`

- `H3V7N5QF:lean4_core/Twentythird/Map.lean::arbOnce_wf` — proved in Lean (module `lean4_core/Twentythird/Map.lean`; axioms: propext; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Nothing.lean`

- `H3V7N5QF:lean4_core/Twentythird/Nothing.lean::arcThree_not_nothing` — proved in Lean (module `lean4_core/Twentythird/Nothing.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentythird/Cost.lean`

- `H3V7N5QF:lean4_core/Twentythird/Cost.lean::atom_ind` — proved in Lean (module `lean4_core/Twentythird/Cost.lean`; axioms: none; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Raise.lean`

- `H3V7N5QF:lean4_core/Twentythird/Raise.lean::atom_rr` — proved in Lean (module `lean4_core/Twentythird/Raise.lean`; axioms: none; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Raise.lean::atom_rs` — proved in Lean (module `lean4_core/Twentythird/Raise.lean`; axioms: none; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Raise.lean::atom_sr` — proved in Lean (module `lean4_core/Twentythird/Raise.lean`; axioms: none; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Raise.lean::atom_ss` — proved in Lean (module `lean4_core/Twentythird/Raise.lean`; axioms: none; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Map.lean`

- `H3V7N5QF:lean4_core/Twentythird/Map.lean::carried_additions_merge3` — proved in Lean (module `lean4_core/Twentythird/Map.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Cost.lean`

- `H3V7N5QF:lean4_core/Twentythird/Cost.lean::congr` — proved in Lean (module `lean4_core/Twentythird/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Cost.lean::parity` — proved in Lean (module `lean4_core/Twentythird/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Cost.lean::unique` — proved in Lean (module `lean4_core/Twentythird/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Map.lean`

- `H3V7N5QF:lean4_core/Twentythird/Map.lean::cost3_arbTwice` — proved in Lean (module `lean4_core/Twentythird/Map.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Rename.lean`

- `H3V7N5QF:lean4_core/Twentythird/Rename.lean::cost3_every_writing` — proved in Lean (module `lean4_core/Twentythird/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Cost.lean`

- `H3V7N5QF:lean4_core/Twentythird/Cost.lean::cost3_iff` — proved in Lean (module `lean4_core/Twentythird/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Cost.lean::cost3_iff_min` — proved in Lean (module `lean4_core/Twentythird/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Cost.lean::cost3_of_phi_le` — proved in Lean (module `lean4_core/Twentythird/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Reach.lean`

- `H3V7N5QF:lean4_core/Twentythird/Reach.lean::cost3_swap` — proved in Lean (module `lean4_core/Twentythird/Reach.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Cost.lean`

- `H3V7N5QF:lean4_core/Twentythird/Cost.lean::cost3_three_ge` — proved in Lean (module `lean4_core/Twentythird/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Cost.lean::cost3_two` — proved in Lean (module `lean4_core/Twentythird/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentythird/Rename.lean`

- `H3V7N5QF:lean4_core/Twentythird/Rename.lean::count_mapT_injOn` — proved in Lean (module `lean4_core/Twentythird/Rename.lean`; axioms: propext; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Cost.lean`

- `H3V7N5QF:lean4_core/Twentythird/Cost.lean::count_pairK_r` — proved in Lean (module `lean4_core/Twentythird/Cost.lean`; axioms: propext; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Cost.lean::count_pairK_s` — proved in Lean (module `lean4_core/Twentythird/Cost.lean`; axioms: propext; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Raise.lean`

- `H3V7N5QF:lean4_core/Twentythird/Raise.lean::count_raiseAtoms_r` — proved in Lean (module `lean4_core/Twentythird/Raise.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Raise.lean::count_raiseAtoms_s` — proved in Lean (module `lean4_core/Twentythird/Raise.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Cost.lean`

- `H3V7N5QF:lean4_core/Twentythird/Cost.lean::dsum_add` — proved in Lean (module `lean4_core/Twentythird/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Cost.lean::dsum_congr` — proved in Lean (module `lean4_core/Twentythird/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Cost.lean::dsum_point` — proved in Lean (module `lean4_core/Twentythird/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Cost.lean::dsum_three` — proved in Lean (module `lean4_core/Twentythird/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Cost.lean::dsum_two` — proved in Lean (module `lean4_core/Twentythird/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Cost.lean::dsum_zero` — proved in Lean (module `lean4_core/Twentythird/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Reach.lean`

- `H3V7N5QF:lean4_core/Twentythird/Reach.lean::empty_swap` — proved in Lean (module `lean4_core/Twentythird/Reach.lean`; axioms: none; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Map.lean`

- `H3V7N5QF:lean4_core/Twentythird/Map.lean::eq_nothing_of_length` — proved in Lean (module `lean4_core/Twentythird/Map.lean`; axioms: propext; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Nothing.lean`

- `H3V7N5QF:lean4_core/Twentythird/Nothing.lean::excess_nothing` — proved in Lean (module `lean4_core/Twentythird/Nothing.lean`; axioms: none; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Raise.lean`

- `H3V7N5QF:lean4_core/Twentythird/Raise.lean::excess_out` — proved in Lean (module `lean4_core/Twentythird/Raise.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Cost.lean`

- `H3V7N5QF:lean4_core/Twentythird/Cost.lean::excess_pairK` — proved in Lean (module `lean4_core/Twentythird/Cost.lean`; axioms: propext; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Raise.lean`

- `H3V7N5QF:lean4_core/Twentythird/Raise.lean::excess_raise` — proved in Lean (module `lean4_core/Twentythird/Raise.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Raise.lean::excess_raiseN` — proved in Lean (module `lean4_core/Twentythird/Raise.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Raise.lean::excess_raiseTo` — proved in Lean (module `lean4_core/Twentythird/Raise.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Raise.lean::excess_raiseTo_all` — proved in Lean (module `lean4_core/Twentythird/Raise.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Rename.lean`

- `H3V7N5QF:lean4_core/Twentythird/Rename.lean::excess_rename` — proved in Lean (module `lean4_core/Twentythird/Rename.lean`; axioms: propext; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentythird/Fewest.lean`

- `H3V7N5QF:lean4_core/Twentythird/Fewest.lean::plain` — proved in Lean (module `lean4_core/Twentythird/Fewest.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Map.lean`

- `H3V7N5QF:lean4_core/Twentythird/Map.lean::fewest3_length` — proved in Lean (module `lean4_core/Twentythird/Map.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Map.lean::fewest3_of_cost` — proved in Lean (module `lean4_core/Twentythird/Map.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Fewest.lean`

- `H3V7N5QF:lean4_core/Twentythird/Fewest.lean::fewest_iff` — proved in Lean (module `lean4_core/Twentythird/Fewest.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentythird/Map.lean`

- `H3V7N5QF:lean4_core/Twentythird/Map.lean::fewest_nothing` — proved in Lean (module `lean4_core/Twentythird/Map.lean`; axioms: none; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Fewest.lean`

- `H3V7N5QF:lean4_core/Twentythird/Fewest.lean::fewest_two_iff` — proved in Lean (module `lean4_core/Twentythird/Fewest.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Map.lean`

- `H3V7N5QF:lean4_core/Twentythird/Map.lean::first_pair_apart` — proved in Lean (module `lean4_core/Twentythird/Map.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Map.lean::first_pair_merge` — proved in Lean (module `lean4_core/Twentythird/Map.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Map.lean::first_pair_states` — proved in Lean (module `lean4_core/Twentythird/Map.lean`; axioms: none; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Fewest.lean`

- `H3V7N5QF:lean4_core/Twentythird/Fewest.lean::four_single_terms_do_not_find_the_fewest` — proved in Lean (module `lean4_core/Twentythird/Fewest.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Fewest.lean::fourWitness_wf` — proved in Lean (module `lean4_core/Twentythird/Fewest.lean`; axioms: propext; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Same.lean`

- `H3V7N5QF:lean4_core/Twentythird/Same.lean::same3` — proved in Lean (module `lean4_core/Twentythird/Same.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Cost.lean`

- `H3V7N5QF:lean4_core/Twentythird/Cost.lean::size_parity` — proved in Lean (module `lean4_core/Twentythird/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Rename.lean`

- `H3V7N5QF:lean4_core/Twentythird/Rename.lean::wf_iff` — proved in Lean (module `lean4_core/Twentythird/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Same.lean`

- `H3V7N5QF:lean4_core/Twentythird/Same.lean::gen3_iff_same3` — proved in Lean (module `lean4_core/Twentythird/Same.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Same.lean::gen3_raiseN` — proved in Lean (module `lean4_core/Twentythird/Same.lean`; axioms: propext; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Same.lean::gen3_raiseTo` — proved in Lean (module `lean4_core/Twentythird/Same.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Cost.lean`

- `H3V7N5QF:lean4_core/Twentythird/Cost.lean::gen_size_parity` — proved in Lean (module `lean4_core/Twentythird/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Rename.lean`

- `H3V7N5QF:lean4_core/Twentythird/Rename.lean::wf_iff` — proved in Lean (module `lean4_core/Twentythird/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Rename.lean::genW3_iff_sameW3` — proved in Lean (module `lean4_core/Twentythird/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Raise.lean`

- `H3V7N5QF:lean4_core/Twentythird/Raise.lean::ite_iff` — proved in Lean (module `lean4_core/Twentythird/Raise.lean`; axioms: none; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Cost.lean`

- `H3V7N5QF:lean4_core/Twentythird/Cost.lean::length_eq_dsum` — proved in Lean (module `lean4_core/Twentythird/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Fewest.lean`

- `H3V7N5QF:lean4_core/Twentythird/Fewest.lean::length_ge_plain` — proved in Lean (module `lean4_core/Twentythird/Fewest.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Raise.lean`

- `H3V7N5QF:lean4_core/Twentythird/Raise.lean::length_raiseAtoms` — proved in Lean (module `lean4_core/Twentythird/Raise.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Cost.lean`

- `H3V7N5QF:lean4_core/Twentythird/Cost.lean::lift_eq` — proved in Lean (module `lean4_core/Twentythird/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Cost.lean::loops_and_two_way_do_not_fix_the_cost` — proved in Lean (module `lean4_core/Twentythird/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Same.lean`

- `H3V7N5QF:lean4_core/Twentythird/Same.lean::lowBound_le` — proved in Lean (module `lean4_core/Twentythird/Same.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Map.lean`

- `H3V7N5QF:lean4_core/Twentythird/Map.lean::lt_three` — proved in Lean (module `lean4_core/Twentythird/Map.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Nothing.lean`

- `H3V7N5QF:lean4_core/Twentythird/Nothing.lean::lt_two` — proved in Lean (module `lean4_core/Twentythird/Nothing.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Raise.lean`

- `H3V7N5QF:lean4_core/Twentythird/Raise.lean::mem_raiseAtoms` — proved in Lean (module `lean4_core/Twentythird/Raise.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Map.lean`

- `H3V7N5QF:lean4_core/Twentythird/Map.lean::mem_two` — proved in Lean (module `lean4_core/Twentythird/Map.lean`; axioms: propext; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Rename.lean`

- `H3V7N5QF:lean4_core/Twentythird/Rename.lean::merge_loses3` — proved in Lean (module `lean4_core/Twentythird/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Cost.lean`

- `H3V7N5QF:lean4_core/Twentythird/Cost.lean::natAbs_add2` — proved in Lean (module `lean4_core/Twentythird/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Cost.lean::natAbs_add3` — proved in Lean (module `lean4_core/Twentythird/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Map.lean`

- `H3V7N5QF:lean4_core/Twentythird/Map.lean::ninth_pair_apart` — proved in Lean (module `lean4_core/Twentythird/Map.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Map.lean::nothing_wf` — proved in Lean (module `lean4_core/Twentythird/Map.lean`; axioms: none; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Map.lean::ofR_arbBra_wf` — proved in Lean (module `lean4_core/Twentythird/Map.lean`; axioms: propext; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Map.lean::ofR_arbTwice_wf` — proved in Lean (module `lean4_core/Twentythird/Map.lean`; axioms: propext; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Cost.lean`

- `H3V7N5QF:lean4_core/Twentythird/Cost.lean::pairK_nothing` — proved in Lean (module `lean4_core/Twentythird/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Cost.lean::pairK_wf` — proved in Lean (module `lean4_core/Twentythird/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Cost.lean::phi_eq_sum` — proved in Lean (module `lean4_core/Twentythird/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Cost.lean::phi_ge_around` — proved in Lean (module `lean4_core/Twentythird/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Cost.lean::phi_of_same3` — proved in Lean (module `lean4_core/Twentythird/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Cost.lean::plain_pairK` — proved in Lean (module `lean4_core/Twentythird/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Raise.lean`

- `H3V7N5QF:lean4_core/Twentythird/Raise.lean::raise_all_gen` — proved in Lean (module `lean4_core/Twentythird/Raise.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Raise.lean::raise_n` — proved in Lean (module `lean4_core/Twentythird/Raise.lean`; axioms: none; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Raise.lean::raise_size` — proved in Lean (module `lean4_core/Twentythird/Raise.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Raise.lean::raise_wf` — proved in Lean (module `lean4_core/Twentythird/Raise.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Raise.lean::raiseAtoms_other` — proved in Lean (module `lean4_core/Twentythird/Raise.lean`; axioms: propext; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Raise.lean::raiseAtoms_same` — proved in Lean (module `lean4_core/Twentythird/Raise.lean`; axioms: propext; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Nothing.lean`

- `H3V7N5QF:lean4_core/Twentythird/Nothing.lean::raisedPair_not_nothing22` — proved in Lean (module `lean4_core/Twentythird/Nothing.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Nothing.lean::raisedPair_nothing` — proved in Lean (module `lean4_core/Twentythird/Nothing.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Raise.lean`

- `H3V7N5QF:lean4_core/Twentythird/Raise.lean::raiseN_n` — proved in Lean (module `lean4_core/Twentythird/Raise.lean`; axioms: propext; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Raise.lean::raiseN_wf` — proved in Lean (module `lean4_core/Twentythird/Raise.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Raise.lean::raiseTo_n` — proved in Lean (module `lean4_core/Twentythird/Raise.lean`; axioms: propext; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Raise.lean::raiseTo_wf` — proved in Lean (module `lean4_core/Twentythird/Raise.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Reach.lean`

- `H3V7N5QF:lean4_core/Twentythird/Reach.lean::reach3_criterion` — proved in Lean (module `lean4_core/Twentythird/Reach.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Reach.lean::reach3_mutual` — proved in Lean (module `lean4_core/Twentythird/Reach.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Reach.lean::reach3_of_same3` — proved in Lean (module `lean4_core/Twentythird/Reach.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Reach.lean::reach3_swap` — proved in Lean (module `lean4_core/Twentythird/Reach.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Reach.lean::reach_swap` — proved in Lean (module `lean4_core/Twentythird/Reach.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Map.lean`

- `H3V7N5QF:lean4_core/Twentythird/Map.lean::congr` — proved in Lean (module `lean4_core/Twentythird/Map.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Map.lean::functional` — proved in Lean (module `lean4_core/Twentythird/Map.lean`; axioms: propext; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Map.lean::readBack3_answer_cost` — proved in Lean (module `lean4_core/Twentythird/Map.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Map.lean::readBack3_arb` — proved in Lean (module `lean4_core/Twentythird/Map.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Map.lean::readBack3_none` — proved in Lean (module `lean4_core/Twentythird/Map.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Map.lean::readBack3_raisedPair` — proved in Lean (module `lean4_core/Twentythird/Map.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Map.lean::readBack3_self_iff` — proved in Lean (module `lean4_core/Twentythird/Map.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Map.lean::readBack3_some_of_cost_le_three` — proved in Lean (module `lean4_core/Twentythird/Map.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Cost.lean`

- `H3V7N5QF:lean4_core/Twentythird/Cost.lean::rsum_add` — proved in Lean (module `lean4_core/Twentythird/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Cost.lean::rsum_congr` — proved in Lean (module `lean4_core/Twentythird/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Cost.lean::rsum_point` — proved in Lean (module `lean4_core/Twentythird/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Same.lean`

- `H3V7N5QF:lean4_core/Twentythird/Same.lean::same3` — proved in Lean (module `lean4_core/Twentythird/Same.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Nothing.lean`

- `H3V7N5QF:lean4_core/Twentythird/Nothing.lean::same22_nothing_iff` — proved in Lean (module `lean4_core/Twentythird/Nothing.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Nothing.lean::around` — proved in Lean (module `lean4_core/Twentythird/Nothing.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Nothing.lean::loop` — proved in Lean (module `lean4_core/Twentythird/Nothing.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentythird/Same.lean`

- `H3V7N5QF:lean4_core/Twentythird/Same.lean::n` — proved in Lean (module `lean4_core/Twentythird/Same.lean`; axioms: none; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Same.lean::refl` — proved in Lean (module `lean4_core/Twentythird/Same.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Rename.lean`

- `H3V7N5QF:lean4_core/Twentythird/Rename.lean::rename` — proved in Lean (module `lean4_core/Twentythird/Rename.lean`; axioms: propext; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Rename.lean::sameW3` — proved in Lean (module `lean4_core/Twentythird/Rename.lean`; axioms: none; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Cost.lean`

- `H3V7N5QF:lean4_core/Twentythird/Cost.lean::size_parity` — proved in Lean (module `lean4_core/Twentythird/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfourth/lean_axioms.txt`)

### `lean4_core/Twentythird/Reach.lean`

- `H3V7N5QF:lean4_core/Twentythird/Reach.lean::swap` — proved in Lean (module `lean4_core/Twentythird/Reach.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Same.lean`

- `H3V7N5QF:lean4_core/Twentythird/Same.lean::symm` — proved in Lean (module `lean4_core/Twentythird/Same.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Same.lean::trans` — proved in Lean (module `lean4_core/Twentythird/Same.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Nothing.lean`

- `H3V7N5QF:lean4_core/Twentythird/Nothing.lean::twoWay` — proved in Lean (module `lean4_core/Twentythird/Nothing.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Nothing.lean::same3_nothing_iff` — proved in Lean (module `lean4_core/Twentythird/Nothing.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentythird/Same.lean`

- `H3V7N5QF:lean4_core/Twentythird/Same.lean::same3_of_excess` — proved in Lean (module `lean4_core/Twentythird/Same.lean`; axioms: none; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Same.lean::same3_raise` — proved in Lean (module `lean4_core/Twentythird/Same.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Reach.lean`

- `H3V7N5QF:lean4_core/Twentythird/Reach.lean::same3_swap_iff` — proved in Lean (module `lean4_core/Twentythird/Reach.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Rename.lean`

- `H3V7N5QF:lean4_core/Twentythird/Rename.lean::n` — proved in Lean (module `lean4_core/Twentythird/Rename.lean`; axioms: none; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Rename.lean::refl` — proved in Lean (module `lean4_core/Twentythird/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Rename.lean::symm` — proved in Lean (module `lean4_core/Twentythird/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Rename.lean::trans` — proved in Lean (module `lean4_core/Twentythird/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Rename.lean::sameW3_nothing_iff` — proved in Lean (module `lean4_core/Twentythird/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Map.lean`

- `H3V7N5QF:lean4_core/Twentythird/Map.lean::seventh_pair_apart` — proved in Lean (module `lean4_core/Twentythird/Map.lean`; axioms: propext; recorded in `evidence/twentyfifth/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Map.lean::seventh_pair_merge` — proved in Lean (module `lean4_core/Twentythird/Map.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentythird/Nothing.lean`

- `H3V7N5QF:lean4_core/Twentythird/Nothing.lean::state_asserting_something_is_nothing22` — proved in Lean (module `lean4_core/Twentythird/Nothing.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Cost.lean`

- `H3V7N5QF:lean4_core/Twentythird/Cost.lean::state_of_shift` — proved in Lean (module `lean4_core/Twentythird/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Cost.lean::cost3_le` — proved in Lean (module `lean4_core/Twentythird/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Cost.lean::cost3_odd` — proved in Lean (module `lean4_core/Twentythird/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Cost.lean::not_same3` — proved in Lean (module `lean4_core/Twentythird/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentythird/Nothing.lean`

- `H3V7N5QF:lean4_core/Twentythird/Nothing.lean::step_of_same3_fails` — proved in Lean (module `lean4_core/Twentythird/Nothing.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Cost.lean`

- `H3V7N5QF:lean4_core/Twentythird/Cost.lean::sum_nine_ge` — proved in Lean (module `lean4_core/Twentythird/Cost.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Cost.lean::triSix_wf` — proved in Lean (module `lean4_core/Twentythird/Cost.lean`; axioms: propext; recorded in `evidence/twentythird/lean_axioms.txt`)
- `H3V7N5QF:lean4_core/Twentythird/Cost.lean::triTwelve_wf` — proved in Lean (module `lean4_core/Twentythird/Cost.lean`; axioms: propext; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Map.lean`

- `H3V7N5QF:lean4_core/Twentythird/Map.lean::twentysecond_pair_apart` — proved in Lean (module `lean4_core/Twentythird/Map.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentyfifth/lean_axioms.txt`)

### `lean4_core/Twentythird/Rename.lean`

- `H3V7N5QF:lean4_core/Twentythird/Rename.lean::two_additions_undo3` — proved in Lean (module `lean4_core/Twentythird/Rename.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)

### `lean4_core/Twentythird/Map.lean`

- `H3V7N5QF:lean4_core/Twentythird/Map.lean::two_single` — proved in Lean (module `lean4_core/Twentythird/Map.lean`; axioms: propext, Quot.sound; recorded in `evidence/twentythird/lean_axioms.txt`)

## Not available

- Infinite objects. States in `St`, `MSt`, `NSt`, `DSt`, `NDSt`, `RSt`, and the twenty-second `St` are finite carriers (`Finset` or a natural bound `n`). `paper/claim_ledger.md` O2 leaves rounds 21–100 uncomputed. No infinite carrier, infinite ordinal, or infinite result space is declared.
- Paths. `H3V7N5QF:lean4/H3V7N5QF/Paths.lean::reach_by_edits` is a finite sequence of edits, and `Reach` is a finite step count. There is no path object, path space, or path-algebra type. `meta/immune_system/genesis_correspondence.md` says an equation of endpoints is not a boundary-fill rule.
- Homotopy. No homotopy relation, homotopy group, or contraction is declared in `lean4/` or `lean4_core/`.
- Higher-cell composition. No `(k+1)`-cell constructor and no boundary-fill predicate. The same fenced note records that local path composition is not the higher-cell rule of `19L57G1`'s `lean4/Derivation/HigherStructure.lean`.
- Pre-Genesis, S(n), and MSS-N. Not located in this clone.
- `19L57G1` object-language primitives that this continuation does not add: `Regime`, `Inst`, `Ctx`, `derivable`, `collapsed`, `separable`, `Event.supply`, `Event.admitDatum`, `Event.admitForm`, `Event.admitInst`, `Event.admitRuleAll`, `Event.impose`, `R2L`, `R2F`, the 13-class transition codebook, and the primitive candidates `W`, `A`, `Bs`, `Bc`, `Bl`, `C`, `D`, `E`, `F` as defined in that repository.
- Fenced prototypes under `meta/next_ten/` and `meta/climbing/`. `meta/README.md` says they are not inherited theorems and that climbing runs are operator-targeted. They are not entries in the axiom reports above.
- Base gaps left open in Lean and not closed by a later citation in this inventory's "proved" list as a substitute: `paper/claim_ledger.md` O3 (rewriting invariance of cost for every writing; the second derivation proves a rewriting step for its own three-kind seed, which is not this gap) and O6 (obstruction persistence for a sequence of changes, as opposed to one change).

## Counts by mark

| Mark | Count |
|---|---|
| proved in Lean | 1828 |
| computed (exact) | 177 |
| stated in prose only | 285 |
| imported | 14 |

The proved-in-Lean figure is the three censuses added: 101 + 21 + 1706 = 1828 distinct axiom-report declarations. A name printed in more than one `lean_axioms.txt` is counted once. Data-type and primitive lines above are the carriers and operations; when the same declaration also appears in a census, the census line is the counted mark. Imported aliases are not inside the 1828.

| Census | Count |
|---|---|
| invariant census | 101 |
| admission theorems | 21 |
| other proved theorems | 1706 |
| computed ledger rows | 177 |
| prose-only ledger rows | 285 |
| imported aliases | 14 |
| declaration sites not resolved | 0 |
