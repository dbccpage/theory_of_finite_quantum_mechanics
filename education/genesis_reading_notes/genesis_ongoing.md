---
documentation_contract: education-documentation/v1
title: "Genesis Ongoing, reading notes for the H3V7N5QF pin"
kind: grammar-reference
audience:
  - researchers
  - engineers
  - coding-agents
status: active
maturity: draft
claim_status: verified
authority_effect: "None"
source_pin: "dbccpage/H3V7N5QF@5d9488324ce976817987bd83a28d901371cfc073"
source_paths:
  - atlas/papers/finite_obstruction_calculus/genesis_ongoing
  - atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/paper.md
  - atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/claim_ledger.md
  - atlas/papers/finite_obstruction_calculus/genesis_ongoing/research/notes.md
  - atlas/papers/finite_obstruction_calculus/genesis_ongoing/research/reading_the_seed.md
  - atlas/papers/finite_obstruction_calculus/genesis_ongoing/research/identification_only.py
last_verified: 2026-10-08
---

# Genesis Ongoing, reading notes for the H3V7N5QF pin

**AuthorityEffect:** None.

**Pin:** [`dbccpage/H3V7N5QF`](https://github.com/dbccpage/H3V7N5QF) `origin/main` at `5d9488324ce976817987bd83a28d901371cfc073` (2026-09-25, merge of pull request 54).

The package [`genesis_ongoing`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing) is a byte copy of that commit. Every file matches the Git blob. The checker is [`code/check_h3_pin.py`](code/check_h3_pin.py), against [`code/h3_origin_main_5d948832.lstree`](code/h3_origin_main_5d948832.lstree).

## The 25 manuscripts and research notes

`meta/review/derivation_review.md` audits 21 seeds, the base through the twenty-first. This commit also contains derivations 22 through 25, accompanied by working research notes in `research/`.

| # | Paper | Research Working Notes | Title & Semantic Mutation |
|---|---|---|---|
| 1 | [`paper/paper.md`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/paper.md) | [`research/reading_the_seed.md`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/research/reading_the_seed.md) | What follows from `arb`, no `xrx`, and four kinds of change (14 givens, loop ban, closed start) |
| 2 | [`paper/second/paper.md`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/second/paper.md) | [`research/second/reading_the_seed.md`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/research/second/reading_the_seed.md) | What follows from `arb`, no `xrx`, and three kinds of change (struck removal, carrying map $q$) |
| 3 | [`paper/third/paper.md`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/third/paper.md) | [`research/third/reading_the_seed.md`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/research/third/reading_the_seed.md) | What follows from `arb`, no `xrx`, and two kinds of change (struck identification, poset containment) |
| 4 | [`paper/fourth/paper.md`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/fourth/paper.md) | [`research/fourth/reading_the_seed.md`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/research/fourth/reading_the_seed.md) | What follows from `arb` once, no `xrx`, and assertions that are counted (multiplicities, support vs indicator) |
| 5 | [`paper/fifth/paper.md`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/fifth/paper.md) | [`research/fifth/reading_the_seed.md`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/research/fifth/reading_the_seed.md) | What follows from `arb` once, no `xrx`, counted assertions, and four kinds of change (mass conservation) |
| 6 | [`paper/sixth/paper.md`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/sixth/paper.md) | [`research/sixth/reading_the_seed.md`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/research/sixth/reading_the_seed.md) | What follows from `arb` once, counted assertions, four kinds of change, and nothing forbidden (no loop ban) |
| 7 | [`paper/seventh/paper.md`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/seventh/paper.md) | [`research/seventh/reading_the_seed.md`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/research/seventh/reading_the_seed.md) | What follows from nothing: counted assertions, four kinds of change, and an empty beginning (void start) |
| 8 | [`paper/eighth/paper.md`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/eighth/paper.md) | [`research/eighth/reading_the_seed.md`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/research/eighth/reading_the_seed.md) | What follows from `arb` once with a second relation `s` (two-relation asymmetry) |
| 9 | [`paper/ninth/paper.md`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/ninth/paper.md) | [`research/ninth/reading_the_seed.md`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/research/ninth/reading_the_seed.md) | What follows from nothing with two relations (empty start, `proj_ofR9`, `swap9_swap`) |
| 10 | [`paper/tenth/paper.md`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/tenth/paper.md) | [`research/tenth/reading_the_seed.md`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/research/tenth/reading_the_seed.md) | What follows once every change records a leftover (three outcome records, non-assertion ledger) |
| 11 | [`paper/eleventh/paper.md`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/eleventh/paper.md) | [`research/eleventh/reading_the_seed.md`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/research/eleventh/reading_the_seed.md) | What follows once a writing can collide terms it does not identify (collision without identification) |
| 12 | [`paper/twelfth/paper.md`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/twelfth/paper.md) | [`research/twelfth/reading_the_seed.md`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/research/twelfth/reading_the_seed.md) | What follows once identifying keeps a per-relation record (relational identification tracking) |
| 13 | [`paper/thirteenth/paper.md`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/thirteenth/paper.md) | [`research/thirteenth/reading_the_seed.md`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/research/thirteenth/reading_the_seed.md) | What follows once a coarser writing forgets which relation asserted (relational projection forgetfulness) |
| 14 | [`paper/fourteenth/paper.md`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/fourteenth/paper.md) | [`research/fourteenth/reading_the_seed.md`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/research/fourteenth/reading_the_seed.md) | What follows once leftover is a writing that is not an assertion (non-asserted lexical leftover) |
| 15 | [`paper/fifteenth/paper.md`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/fifteenth/paper.md) | [`research/fifteenth/reading_the_seed.md`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/research/fifteenth/reading_the_seed.md) | What follows once reaching a result does not make it admitted (admission gate boundary) |
| 16 | [`paper/sixteenth/paper.md`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/sixteenth/paper.md) | [`research/sixteenth/reading_the_seed.md`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/research/sixteenth/reading_the_seed.md) | What follows once a recorded leftover feeds back into the state (`Reach16.unbounded`) |
| 17 | [`paper/seventeenth/paper.md`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/seventeenth/paper.md) | [`research/seventeenth/reading_the_seed.md`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/research/seventeenth/reading_the_seed.md) | What follows when `xrx` is not forbidden, and is still obstructed (external obstruction gate) |
| 18 | [`paper/eighteenth/paper.md`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/eighteenth/paper.md) | `meta/review/derivation_review.md` | What follows when a different writing is a different result (lexical term discrimination) |
| 19 | [`paper/nineteenth/paper.md`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/nineteenth/paper.md) | `meta/review/derivation_review.md` | Identification in one chosen assertion (localized rewrite) |
| 20 | [`paper/twentieth/paper.md`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/twentieth/paper.md) | `meta/review/derivation_review.md` | Fewest total changes first (cost-ordered exploration priority) |
| 21 | [`paper/twentyfirst/paper.md`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/twentyfirst/paper.md) | `meta/review/derivation_review.md` | An obstructed change is refused (deterministic refusal enforcement) |
| 22 | [`paper/twentysecond/paper.md`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/twentysecond/paper.md) | [`research/twentysecond/reading_the_seed.md`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/research/twentysecond/reading_the_seed.md) | Two relations, nothing given, and a pair asserted in both relations taken out (H1 cancellation) |
| 23 | [`paper/twentythird/paper.md`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/twentythird/paper.md) | [`research/twentythird/reading_the_seed.md`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/research/twentythird/reading_the_seed.md) | Two relations, nothing given, pairs asserted together taken out, and raising (H2 raising operator) |
| 24 | [`paper/twentyfourth/paper.md`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/twentyfourth/paper.md) | [`research/twentyfourth/reading_the_seed.md`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/research/twentyfourth/reading_the_seed.md) | Two relations, nothing given, raising, and filled terms (H3 twin fills, Part 1) |
| 25 | [`paper/twentyfifth/paper.md`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/twentyfifth/paper.md) | [`research/twentyfifth/reading_the_seed.md`](/atlas/papers/finite_obstruction_calculus/genesis_ongoing/research/twentyfifth/reading_the_seed.md) | Two relations, nothing given, raising, and filled triples that balance (H3 twin fills, Part 2: cones) |

## Base carrier

The base seed is `prompt/seed_prompt.md`. `paper/paper.md` records fourteen givens. The four changes are identification, removal, adding a term, and adding an assertion. `xrx` is forbidden in the base seed.

`code/xry/state.py` defines `given`. Ledger D2 says that on the given terms exactly two legal states contain `arb`. Ledger D8 gives the fewest-change count. Ledger D9 is the reachability statement. Ledger N5 is the expressive ceiling that follows from D9.

## Research Working Notes & Side Analyses (`research/`)

The pinned package contains working research notes in `research/` that record the sentence-by-sentence textual analysis, rejected interpretations, and mathematical side explorations.

### 1. The Primordial Base Seed (`research/reading_the_seed.md`)

- **Lexical alphabet & term notation:** Terms are written with letters. The relation symbol `r` is deliberately omitted from term names so that strings like `arb` parse with an unambiguous relation slot without requiring multi-character lookahead.
- **Assertion semantics:** Directed order is enforced: `arb` and `bra` are distinct assertions because the seed declares `arb` given while flagging `bra` as "not given". In the base seed, multiplicity is excluded: an assertion is either asserted or not (reading C1).
- **Closed vs. open beginning:** The seed names `a` and `b`, asserts `arb`, and flags `bra` as not given. In the closed reading (C2), exactly `a` and `b` exist initially. In an open reading, any additional unmentioned initial terms would already be generated by term addition, showing that the closed start does not restrict reachable results.
- **Four discrete changes:** Adding what is asserted or removing what is unasserted changes nothing. Term count decreases only via identification (which requires two terms); there is no term deletion operation, so every state has at least one term (D6).
- **The three readings of "build structure":**
  1. *Post-change repair (rejected):* Performing an identification that creates `xrx` and attempting to repair it fails because no legal additions or identifications can eliminate `xrx`; only removing `xrx` restores legality.
  2. *Preparatory removal (rejected as "build"):* Clearing the obstruction beforehand reduces to "remove the obstruction", leaving "build structure" redundant.
  3. *Inversion stand-in (adopted, C7):* "Build structure" acts as a stand-in for the prohibited outcome: additions reaching a legal state that would reproduce the would-be outcome if the added terms were identified back.
- **Refusals:** Refused changes record an attempt and alter no state coordinates, establishing that exploration bounded by $k$ changes and exploration bounded by $k$ attempts yield identical result sets.
- **FREE vs. ANCHORED sameness:** Under FREE sameness, results are equivalent under any term rewriting permutation. Under ANCHORED sameness, the identities of given terms `a` and `b` are preserved.

### 2. Side Notes & Algorithmic Obstructions (`research/notes.md`)

- **Identifications alone (`research/identification_only.py`):** For all 238 legal states with $\le 4$ terms under FREE sameness, following unobstructed identifications alone terminates in end states where every pair is related. The fewest terms of an end state equals the chromatic/independent-set split bound (fewest classes into which terms partition with no two related terms in a class), while the most terms equals the maximal pairwise-related class partition. The script verifies that 238 of 238 states satisfy this split.
- **Single-count answered changes:** If an obstructed change and its answering removal counted as a single compound change, round numbers would shift downward (e.g. the one-term state appearing in round 1 instead of round 2), but the set of reachable results remains invariant.
- **The 100-round combinatorial horizon:** Exact enumeration of round $k$ corresponds to orbit counting by cycle types of permutations of $n$ terms. For $n \approx 100$, partition enumeration across all cycle types is computationally intractable in plain Python, leaving unbounded exact orbit counts beyond round 20 open (O2).
- **Rejection of recursive structural copying:** Reading "build structure" as forcing an automatic copy of $x$ with all its incident assertions would trigger an endless sequence $x r x' r x'' \dots$; this interpretation was rejected in adherence to the directive not to invent unstated operations.
- **Lean 4 toolchain containment:** Pinning to `leanprover/lean4:v4.33.1` requires invoking `lake` inside `lean4/` or with explicit `-d lean4` to avoid invoking the host's ambient Lean compiler.

### 3. Structural Mutation Families Across the 25 Derivations

The derivation suite explores distinct structural variations documented across `research/*/reading_the_seed.md`:

- **Contraction Family (Seeds 2 & 3):**
  - *Derivation 2 (`research/second/reading_the_seed.md`):* Removal is struck. Identifications and additions induce a monotonic *carrying map* $q$: once asserted, assertions cannot be unasserted. Obstructions persist permanently, and the one-term state becomes unreachable.
  - *Derivation 3 (`research/third/reading_the_seed.md`):* Identification is also struck, leaving only term and assertion additions. Reachability collapses to strict subset containment (a poset); size increases by exactly 1 per step.
- **Multiplicity Family (Seeds 4 & 5):**
  - *Derivation 4 (`research/fourth/reading_the_seed.md`):* Multiplicity is introduced. Assertions carry positive integer counts. Connects to earlier models via *support* (boolean projection) and *indicator* (unit multiplicity) maps.
  - *Derivation 5 (`research/fifth/reading_the_seed.md`):* Four kinds of change are restored on counted assertions, preserving total mass arithmetic.
- **Permissive & Void Beginning (Seeds 6 & 7):**
  - *Derivation 6 (`research/sixth/reading_the_seed.md`):* The loop ban `xrx` is dropped, eliminating obstructions and refusals.
  - *Derivation 7 (`research/seventh/reading_the_seed.md`):* Starts from the empty state (no terms, no assertions) under four changes and counted assertions.
- **Poly-Relational Family (Seeds 8 & 9):**
  - *Derivation 8 (`research/eighth/reading_the_seed.md`):* Introduces a second relation `s` alongside `r`.
  - *Derivation 9 (`research/ninth/reading_the_seed.md`):* Combines two relations with an empty beginning; verified with definitional projection (`proj_ofR9`) and relational swap involution (`swap9_swap`).
- **Ledger, Collision & Admission Boundaries (Seeds 10–15):**
  - *Derivation 10 (`research/tenth/reading_the_seed.md`):* Establishes a side ledger recording one of three leftover outcomes (cleared, uncleared, none) without altering assertion state.
  - *Derivation 11 (`research/eleventh/reading_the_seed.md`):* Investigates writing collisions where distinct terms collide in representation without underlying identification.
  - *Derivations 12–14:* Study per-relation attribution, projection coarsening, and non-asserted lexical leftovers.
  - *Derivation 15 (`research/fifteenth/reading_the_seed.md`):* Introduces the admission gate boundary: reaching a result does not admit it, establishing a formal separation between generation and authorization.
- **Dynamical Feedback (Seeds 16 & 17):**
  - *Derivation 16 (`research/sixteenth/reading_the_seed.md`):* Leftovers feed back into the carrier state, generating non-terminating path lengths (`Reach16.unbounded`).
  - *Derivation 17 (`research/seventeenth/reading_the_seed.md`):* Explores loops that are permitted in state representations but obstructed by external operational gates.
- **Climbing Rounds & Cones (Seeds 22–25):**
  - *Derivation 22 (`research/twentysecond/reading_the_seed.md`):* Round H1 cancellation quotient, equating states differing only by co-asserted `xry` and `xsy`.
  - *Derivation 23 (`research/twentythird/reading_the_seed.md`):* Round H2 state raising, allowing additions to invert prior additions.
  - *Derivations 24 & 25 (`research/twentyfourth/` and `twentyfifth/`):* Round H3 twin fills, studying filled terms and balanced triple cones (`told_iff`, `nothing_balanced`, `cone_decides`).

## Climbing rounds

| Round | Packet | Manuscript |
|---|---|---|
| H1 cancellation | `meta/climbing/h1_cancellation/packet.md` | `paper/twentysecond/paper.md` |
| H2 raising | `meta/climbing/h2_raising/score.md` | `paper/twentythird/paper.md` |
| H3 twin fills | `meta/climbing/h3_twin_fills/` | `paper/twentyfourth/paper.md` and `paper/twentyfifth/paper.md` |

H1 replaces one sameness sentence of the ninth seed, so that an `xry` and an `xsy` asserted together count as the same result. The wording is in the H1 packet, section 1.

## Gates

`ci/OEWAS_GATES.md` names four gates: vacuous self-comparison, definitional citation, mutation must bite, and cited Lean name in the derivation's own report.

## How to run the base code

From the package directory, with `code` on `PYTHONPATH` as `pyproject.toml` sets for pytest:

```text
python -B -m pytest tests/test_changes.py -q -p no:cacheprovider -o addopts=
```

The committed pytest addopts also run coverage and `code/xry/gate.py`. That is the repository's own gate. It is separate from the blob pin check.

## Education drawings

These 22 SVG files live in this documentation tree. They are schematics for the level pages. They are not figures exported by the pinned package.

- [`genesis_ongoing_00_primordial_seed.svg`](_images/genesis_ongoing_00_primordial_seed.svg)
- [`genesis_ongoing_01_relation_embedding.svg`](_images/genesis_ongoing_01_relation_embedding.svg)
- [`genesis_ongoing_02_loop_ban_mss002.svg`](_images/genesis_ongoing_02_loop_ban_mss002.svg)
- [`genesis_ongoing_03_discrete_cost_factor2.svg`](_images/genesis_ongoing_03_discrete_cost_factor2.svg)
- [`genesis_ongoing_04_bifurcation_lattice.svg`](_images/genesis_ongoing_04_bifurcation_lattice.svg)
- [`genesis_ongoing_05_monotone_mass_growth.svg`](_images/genesis_ongoing_05_monotone_mass_growth.svg)
- [`genesis_ongoing_06_stage_embeddings.svg`](_images/genesis_ongoing_06_stage_embeddings.svg)
- [`genesis_ongoing_07_graph_reachability_closure.svg`](_images/genesis_ongoing_07_graph_reachability_closure.svg)
- [`genesis_ongoing_08_discrete_primal_dual.svg`](_images/genesis_ongoing_08_discrete_primal_dual.svg)
- [`genesis_ongoing_09_involution_swap.svg`](_images/genesis_ongoing_09_involution_swap.svg)
- [`genesis_ongoing_10_five_structural_ceilings.svg`](_images/genesis_ongoing_10_five_structural_ceilings.svg)
- [`genesis_ongoing_11_positioned_confluence.svg`](_images/genesis_ongoing_11_positioned_confluence.svg)
- [`genesis_ongoing_12_meta_layer_apparatus.svg`](_images/genesis_ongoing_12_meta_layer_apparatus.svg)
- [`genesis_ongoing_13_cycle_classification.svg`](_images/genesis_ongoing_13_cycle_classification.svg)
- [`genesis_ongoing_14_bounded_search_horizon.svg`](_images/genesis_ongoing_14_bounded_search_horizon.svg)
- [`genesis_ongoing_15_admission_record_boundary.svg`](_images/genesis_ongoing_15_admission_record_boundary.svg)
- [`genesis_ongoing_16_derivation_lattice.svg`](_images/genesis_ongoing_16_derivation_lattice.svg)
- [`genesis_ongoing_17_packaging_isolation.svg`](_images/genesis_ongoing_17_packaging_isolation.svg)
- [`genesis_ongoing_18_leftovers_unboundedness.svg`](_images/genesis_ongoing_18_leftovers_unboundedness.svg)
- [`genesis_ongoing_19_round_r1_cancellation.svg`](_images/genesis_ongoing_19_round_r1_cancellation.svg)
- [`genesis_ongoing_20_round_r2_state_raising.svg`](_images/genesis_ongoing_20_round_r2_state_raising.svg)
- [`genesis_ongoing_21_round_r3_twin_fills.svg`](_images/genesis_ongoing_21_round_r3_twin_fills.svg)

## Level pages

[`levels/README.md`](levels/README.md)

## Neighbouring education trees

- [`../001_genesis/README.md`](../001_genesis/README.md)
- [`../002_s_n/README.md`](../002_s_n/README.md)
- [`../003_minimal_symbol_system_n_mssn/README.md`](../003_minimal_symbol_system_n_mssn/README.md)
- [`../030_the_symbol_game_proposal_fidelity_protocol_pfp/README.md`](../030_the_symbol_game_proposal_fidelity_protocol_pfp/README.md)
- [`../witnessed_difference_programme/README.md`](../witnessed_difference_programme/README.md)
