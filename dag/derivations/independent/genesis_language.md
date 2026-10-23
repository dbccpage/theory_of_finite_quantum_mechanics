Status: AI-drafted, awaiting human review.

# Admit: a fragment of the Genesis regime, with priced imports

Admit is the language defined in `research/genesis_language/SPEC.md` and embedded in `lean4/AdmitCore.lean`, `lean4/AdmitReflect.lean`, `lean4/AdmitInterpret.lean`, and `lean4/AdmitImport.lean`. The core stores admitted data, form declarations, and ordered cuts. Supply does not change a regime. A cut is admitted only between two data indices that differ. An import record names axioms and a cost and sits beside the regime; `Holds` does not read it.

S(n) and MSS-N are not core rules. TFQ-0510 records the two boxed laws as design rules, not as theorems of 19L57G1. TFQ-0528 records the MSS-N atlas as external, with MSS-2 not equal to S(2) and licensed depth 0. Both are open imports.

## Statement versus theorem

| Statement | Lean declaration | Verdict |
| --- | --- | --- |
| Supply returns the same regime and does not admit the supplied index | `AdmitCore.supply_noop`, `AdmitCore.supply_not_admit` | FULL for this step relation |
| Impose has no step | `AdmitCore.impose_no_step` | FULL for this event |
| A self-cut does not step | `AdmitCore.self_cut_refused` | FULL |
| Endpoints of an admitted cut differ | `AdmitCore.endpoints_apart` | FULL |
| `apart` and `admittedCut` are the same condition | `AdmitCore.apart_iff_cut` | FULL |
| A map into an irreflexive target cannot identify the endpoints of an admitted cut | `AdmitCore.identification_breaks_law` | NARROWED: one target relation supplied as data, not a general quotient |
| A token is not typed | `AdmitCore.token_not_typed` | FULL |
| Distinct data do not yield a cut; the opposite cut is not derived | `AdmitCore.distinct_not_cut`, `AdmitCore.reverse_not_held` | FULL for the two concrete regimes |
| Judgments and typings survive steps | `AdmitCore.holds_preserved`, `AdmitCore.holds_reaches`, `AdmitCore.typed_preserved`, `AdmitCore.typed_reaches` | FULL for the rules defined here |
| Arity 0 is allowed; a mismatched arity is not typed; re-admission is allowed | `AdmitCore.zero_arity_types`, `AdmitCore.wrong_arity_not_typed`, `AdmitCore.readmit_present` | FULL for these rules; positive arity and dedup are not theorems |
| From empty, admit 0, admit 1, admit cut 0 1, and `apart 0 1` holds | `AdmitCore.reaches_example`, `AdmitCore.example_apart` | FULL for this example |
| The empty regime does not derive `apart 0 1` | `AdmitCore.empty_not_apart` | FULL |
| Quotation of expressions, events, judgments, and regimes is an inverse pair | `AdmitReflect.unquote_quote_expr`, `quote_unquote_expr`, and the event, judgment, and regime twins | FULL for that syntax |
| Quoted steps are core steps | `AdmitReflect.qstep_sound` | FULL for transport of `Step` |
| Quotation does not type a token as data, and a quoted self-cut or impose does not step | `AdmitReflect.quoted_token_not_data`, `quoted_self_cut_refused`, `quoted_impose_no_step` | FULL for those refusals |
| A truth predicate for Admit | none | NOT PROVED |
| IdRefl(2): reflexivity on two atoms is sound, and the conjunction with metatheoretic equality is conservative | `AdmitInterpret.id_sound`, `AdmitInterpret.id_conservative` | NARROWED |
| `J`, dependent products, universes | none | NOT PROVED |
| Bare admission is not identity of distinct atoms | `AdmitInterpret.admission_is_not_identity` | FULL for atoms 0 and 1 |
| An admitted cut is an edge with distinct endpoints, and every such edge arises from some reached regime | `AdmitInterpret.cut_as_edge`, `AdmitInterpret.edge_realizable` | NARROWED to dimension at most 1, as defined in the module |
| Edge existence is conservative over the empty regime | `AdmitInterpret.edge_not_held_in_empty` shows it is not | not claimed; the negative statement is proved |
| Higher simplices, horns, Kan conditions | none | NOT PROVED |
| An admitted cut interprets as two distinct members of an insert-pair of von Neumann terms | `AdmitInterpret.cut_hf_sound`, `AdmitInterpret.example_cut_hf` | NARROWED to this term model |
| Extensional hereditarily finite sets, infinity, and the other set-theoretic axioms | `AdmitInterpret.insert_order_differs` shows these terms are not extensional | NOT PROVED; conservativity of the reading is open |
| Writing an import record does not make `apart 0 1` hold in the empty regime | `AdmitImport.import_is_not_a_core_derivation`, `AdmitImport.sn_import_does_not_derive_apart` | FULL for `coreHolds` |
| S(n) boxed laws, the MSS-N atlas, and the rules and requirements fields | `AdmitImport.snImport`, `mssnImport`, `rulesImport`, each `openStatus` | NOT PROVED; recorded as open imports |
| Conservativity of any of those three imports | none | NOT PROVED |

## What is proved

The step and typing rules above, preservation along those steps, the example derivation of `apart 0 1`, the empty-regime refusal of that judgment, the quotation round trip, transport of `Step`, the narrowed identity and edge and hereditarily-finite readings named in the table, and the fact that an import record is not consulted by `Holds`.

The independent script `checks/independent/genesis_language.py` recomputes the example derivation and the empty-regime non-derivation with a second copy of the same rules, and also checks supply, self-cut, impose, the opposite cut, arity, and the irrelevance of a side list of records.

## What is assumed

The core rules are a chosen fragment of the Genesis regime, not a theorem that the fragment is forced. The irreflexive ban is part of `admitCut`. The three open imports name assumptions taken from TFQ-0378, TFQ-0510, and TFQ-0528; none of those assumptions is used as a premise of a core derivation. `IdJudg` and `Edge` and `HF` are definitions in `AdmitInterpret`, not imports from another development. Metatheoretic equality of atoms is the standard equality of the inductive type `Atom`.

## What is open

A truth predicate. The identity eliminator `J` and any larger fragment of Martin-Löf type theory. Simplices above dimension 1. Extensional hereditarily finite sets and conservativity of that reading. Any conservativity proof for `snImport`, `mssnImport`, or `rulesImport`. A Gödel sentence inside Admit. The cost-two floor of TFQ-0381. Readings L and F. The effect of impose. Chain retractions.
