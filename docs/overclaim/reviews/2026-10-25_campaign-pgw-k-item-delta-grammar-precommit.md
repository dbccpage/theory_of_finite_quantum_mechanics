# Review of campaign PGW-K-ITEM-DELTA-GRAMMAR

Scope: worktree branch derive/PGW-K-ITEM-DELTA-GRAMMAR before the pull request, against origin/main at 7fa69d621c27bed7045d0b7fe34bbb1d34b27248. Rule applied: PROVED_LEAN only if Lean declarations in the repository state the node's full statement and compile with only propext, Classical.choice and Quot.sound.

Method: read the node statement, bottleneck and TFQ-0490 record after the pregenesis sync; read lean4/CampaignPgwKItemDeltaGrammar.lean; read checks/independent/pgw-k-item-delta-grammar.py and dag/derivations/independent/pgw-k-item-delta-grammar.md. Scanner: `python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict` (HIGH 0, MEDIUM 0, LOW 3). This review did not rebuild Lean. The derivation build receipt is dag/research/campaign_pgw-k-item-delta-grammar_lean_replay.json.

Result: 0 nodes FULL, 1 NARROWED, 0 OVERCLAIM. No node was raised. Status stays OPEN.

Corrections to the PR's own text:
- None in the statement. The census claims are the added paragraph. The sealed cost-two grammar, arity two, and a grammar for 3 or more items stay in the bottleneck.

## Per-node table

| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| PGW-K-ITEM-DELTA-GRAMMAR | well_formed_singles_are, well_formed_pairs_are, separating_pairs_are_two, nine_well_formed, seven_leave_bits_equal, form_rule_both_true, rule_extension_equalizes, rule_extension_is_longer, off_target_instance_keeps_bits, fresh_datum_pairs_do_not_separate, ten_atoms, one_hundred_pairs, no_single_item_separates | NARROWED | One empty base, arity one, 10 atoms. The general pruning lemmas and the k-item grammar are not the theorems. |

Atomic claims:

| Claim | Declaration | Verdict |
|---|---|---|
| 10 atoms, 100 ordered pairs | ten_atoms (lean4/CampaignPgwKItemDeltaGrammar.lean:179), one_hundred_pairs (:182) | NARROWED to this universe |
| Well-formed singles are datum and form; seven named pairs are the well-formed pairs | well_formed_singles_are (:156), well_formed_pairs_are (:160) | NARROWED |
| No single item separates; the separators are form then i0t0 and form then i0t1 | no_single_item_separates (:172), separating_pairs_are_two (:175) | NARROWED |
| 9 well-formed deltas, 7 leave the target bits equal | nine_well_formed (:185), seven_leave_bits_equal (:189) | NARROWED |
| The three fresh-datum pairs do not separate | fresh_datum_pairs_do_not_separate (:193) | NARROWED |
| Form then the uniform rule sets both target bits true and does not separate | form_rule_both_true (:199) | NARROWED |
| The 2-item argument-0 instance separates; the 3-item rule extension equalizes the bits and is longer | rule_extension_equalizes (:202), rule_extension_is_longer (:206) | NARROWED |
| Datum, form, then argument 2 records that instance and keeps both target bits false | off_target_instance_keeps_bits (:211) | NARROWED |
| Unpruned cost-two grammar for arity at most two, on every base | not proved | NOT PROVED |
| A k-item grammar for k at least 3, with pruning lemmas against the unpruned space | not proved | NOT PROVED |
| rule_item_never_minimal and collapsed_fresh_datum, as general lemmas | cited, not rechecked in this module | NOT RECHECKED |

Axiom lines from the derivation build: twelve theorems depend on no axioms; rule_extension_equalizes depends on propext. No sorry, admit, axiom, native_decide or unsafe in the module.

## Numbers recomputed

| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| statement, ten_atoms | 10 atoms | Lean atoms.length = 10; Python len(ATOMS) == 10 | match |
| one_hundred_pairs, derivation note | 100 pairs | Lean pairs.length = 100; Python 10 * 10 == 100 | match |
| nine_well_formed | 9 well-formed deltas | Lean length sum = 9; Python len(singles)+len(pairs) == 9 | match |
| seven_leave_bits_equal | 7 leave bits equal | Lean 9 - 2 = 7; Python same subtraction | match |
| separating_pairs_are_two | 2 separators | Lean list of two pairs; Python the same two pairs | match |
| rule_extension_is_longer | lengths 2 and 3 | Lean list lengths 2 and 3; Python len of those sequences | match |
| independent check | 29 conditions, 0 failures | python -I -X utf8 checks/independent/pgw-k-item-delta-grammar.py | match |
| evidence map | E4 count 0 | build_evidence.py --write reported E4 0 | match |

The evidence page lists 28 symbols because each of the 13 campaign declarations is cited on the node and again on record TFQ-0490, and the two earlier imports are cited once each. The module has 13 theorems. Grade E3 counts files. It is not a statement match.

## Scanner output

HIGH 0, MEDIUM 0. LOW 3, none on this node: R10 TENSOR-ASSUMPTION-COUNTERMODELS; R5 tfq_1019 date 20261019; R5 tfq_0413 fractions 1/2 and 1/4. No baseline change.
