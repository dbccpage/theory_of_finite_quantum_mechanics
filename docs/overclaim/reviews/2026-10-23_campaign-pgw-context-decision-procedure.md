# Review of the finite Genesis context campaign

AuthorityEffect: None. AI self-review, awaiting human review.

Scope: PGW-CONTEXT-DECISION-PROCEDURE and its dependent
COMP-C3-CONTEXT-DECISION-PARTIAL cross-reference, against origin/main
3924d378ff1de685948bf2b419dc63a5a9560881. Compiled source commit:
6cdc1d9eade109f77b9884491039bddccf22afcd.

Method: read the source definitions, the new Lean declarations, independent
checker and note; matched each theorem audit to the committed source. No
Lean/Lake/Cargo build was performed as part of this review. The campaign build
receipt supplies the completed build and preserves its legacy import warnings.
The external observation sources read locally match the DAG's pinned sibling
commit, including the Python and Rust context definitions.

Result: 0 FULL, 2 NARROWED, 0 OVERCLAIM across the changed DAG records. The
complete finite-context theorem is derived; the larger original bundle still
contains first-count, Y-2 necessity and implementation-refinement obligations.
Both node statuses remain OPEN. The outcome class is provisional.

## Statement versus theorem

All new declarations are in `lean4/CampaignGenesisContextDecision.lean`.

| Atomic claim | Declaration and source line | Verdict |
|---|---|---|
| Enumerates exactly all well-formed finite slot contexts, every admitted arity and hole multiplicity | `mem_slotTuples`, line 34; `mem_contexts`, line 52 | FULL for the declared language |
| Collapse is decided by the complete finite search | `collapseTest_correct`, line 69 | FULL for the declared language |
| Separation is decided; a returned witness distinguishes, and none is equivalent to collapse | `separable_iff_not_collapsed`, line 76; `witness_none_iff`, line 87; `witness_sound`, line 91 | FULL for the declared language |
| Profiles coincide exactly for contextually collapsed data | `profile_eq_iff`, line 104 | FULL |
| Executable count equals the cardinality of the semantic quotient on admitted data | `classCount_eq_quotient_card`, line 202, with `Collapsed` as the quotient relation | FULL |
| Holding two is decided and is equivalent to at least two classes | `HoldsTwo` decision instance, line 119; `holdsTwo_iff_classCount`, line 157 | FULL |
| Form exhaustion is decided, with uniform-rule sufficiency | `exhaustionTest_correct`, line 130; `uniform_rule_exhausted`, line 142 | FULL |
| First-count existence and history-level necessity Y-2 | not proved | NOT PROVED |
| Operational refinement to the sealed Python/Rust driver | not proved | NOT PROVED |
| C3's earlier module remains unary-only; the new module supplies the finite-context procedure | existing `GenesisComputation.UnarySep`, line 123, and the new declarations above | NARROWED cross-reference; no broader history result |

The independently executable class count is a finite image cardinality. The
semantic quotient is defined by the universal raw-context predicate; its
cardinality is not prescribed to equal the computed answer. Equality is proved
by the injective quotient-to-profile map and a proof of its exact image.

## Corrections and scope fences

- No fixed arity bound occurs in the Lean theorem. The independent census has
  an explicit smaller domain and is not the basis for that generality.
- The one-hole mutation tests witness order. It is not a counterexample to
  deciding collapse with all one-hole contexts. Unary-only search really does
  miss the binary example.
- Uniform-rule sufficiency is distinct from the historical necessity claim Y-2.
- A computational cross-check is not an external program-refinement theorem.
- New code is assessed L4D. Declarative Lake registration remains L1C under the
  configuration exception; no capability increase is inferred from its name.
- Only the new module, the unchanged GenesisComputation dependency and Lake
  configuration compiled. The default library and PR #203 modules were not
  rebuilt. Existing and new legacy-mode compatibility warnings are preserved.

## Numbers recomputed

| Quantity | Recalculation | Result |
|---|---|---|
| 849 regimes; class-count histogram 11 / 420 / 418 | exhaustive fact/rule subsets in the independent checker | match |
| Context counts for binary, ternary and arity-four fixtures | independent Cartesian and hole-mask constructions; SymPy integer power formula | match |
| Concrete class counts two, one and zero | Lean `explicit_class_counts` and independent quotient grouping | match |
| Four killed mutations; seven domain refusals | explicit challenge calls with fail-closed checks under normal and optimized Python | match |
| Twenty new theorem audit lines; forty-three dependency audit lines | terminal print commands matched to parsed build output and allowed axiom sets | match |
| Regression results | 32 passed, 1 skipped in the initial run; the skipped citation test passed when its known sibling root was supplied | match |
| Generated README inventory | canonical generator and check | current; inventory is not a full build |

Normal and optimized independent outputs are identical. The exact source
hashes of the externally read definitions are recorded in the checks receipt.

## Scanner and unresolved diagnostics

The changed-since strict scan reports HIGH=0, MEDIUM=0, LOW=3. The LOW findings
concern existing tensor coverage and numeric-note metadata, not these new
context declarations. No baseline entry was added.

The required synchronization, structural, receipt, evidence and regression
checks pass after regeneration. The additional all-missing prompt diagnostic
still reports the executed TFQ-0084 manual delta. The additional whole-repository
contract check still reports malformed JSON in the unchanged
HilbertLiftOperators companion. The campaign companions have valid history
records and current source hashes. The prompt generator also refreshed the
existing TFQ-0016 pins after preserving its statement while repairing its YAML
scalar quoting. No theorem in that module was rebuilt.

## What the scanner could not decide

Source-model interpretation, the remaining history predicates, refinement to
external implementations and the final campaign classification need human
review. The node's remaining obligations are retained rather than inferred
from the finite census or the existence of a compiled module.
