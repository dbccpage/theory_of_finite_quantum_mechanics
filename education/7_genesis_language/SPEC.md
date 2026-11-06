# Admit

Admit is a deep embedding, in Lean, of a finite fragment of the Genesis regime calculus as that calculus is recorded in this repository. It is not a derivation of later mathematics or of physics. A later theory is not derived from the core. It can be written down only as an import record: the axioms are named, the cost is named, and conservativity is either proved or left open.

The Lean modules are `lean4/AdmitCore.lean`, `lean4/AdmitReflect.lean`, `lean4/AdmitInterpret.lean`, and `lean4/AdmitImport.lean`. AuthorityEffect of each module is None.

## What the core takes from Genesis

The core uses only structure that the repository states for Genesis.

- A regime has admitted data, forms, instances, rules, and requirements, and it changes by an admission event or by impose. Supply is external (TFQ-0378). Admit stores three of those fields: `data`, `forms`, and `cuts`. A cut is the stored instance of a distinction. Rules and requirements are not fields. They are the open import `rulesImport`.
- A supply step returns the same regime (TFQ-0379, `supply_noop`). The core has no reading flag, so the step does not select reading L or reading F.
- The ban on a reflexive cut is part of the cut-admission rule. From an admitted cut the endpoints are distinct (`endpoints_apart`). Two distinct data indices do not by themselves yield a cut (`distinct_not_cut`). The opposite ordered cut is not derived (`reverse_not_held`). This is the fragment corresponding to TFQ-0387 and to `lean4/AdmissionFloor.lean` (`endpoints_apart`, `law_not_derived_from_distinctness`). The target relation in `identification_breaks_law` is supplied data, as in `AdmissionFloor.identification_breaks_law`.
- Presentation tokens, indices, and equality of indices are metatheory. An object datum is an admitted index (TFQ-0430). `token_not_typed` is the corresponding refusal.
- Positive form arity, and refusal of a repeated data admission, are extra clauses in the ledger, not consequences of the regime inscription (TFQ-0378). The core therefore allows arity 0 (`zero_arity_types`) and a repeated `admitData` (`readmit_present`).
- Impose is an event constructor and has no step rule (`impose_no_step`).

S(n) is not a core constructor. TFQ-0510 records the two boxed laws as design rules of the 002_oesn strand, not as theorems of 19L57G1, and records that no checker enforces them. TFQ-0528 records MSS-N as an externally designed atlas, with MSS-2 not equal to S(2), and with licensed depth 0. Both are open imports below. `lean4/ChainRetraction.lean` is not used: a chain retraction is not an admission rule of this fragment.

The cost-two floor of TFQ-0381 is not a theorem here. It is stated there for one declared response grammar, and the same note says a change of grammar can change the cost. Admit does not recompute that minimum. Costs in import records are names, not that number.

## Syntax

```
Kind   ::= dataK | distK

Expr   ::= token Nat
         | datum Nat
         | form Nat (List Nat)
         | cut Nat Nat

Event  ::= supply Nat
         | admitData Nat
         | admitForm Nat Nat
         | admitCut Nat Nat
         | impose

Judg   ::= typed Expr Kind
         | admittedData Nat
         | admittedForm Nat Nat
         | admittedCut Nat Nat
         | apart Nat Nat

Regime ::= { data : List Nat, forms : List (Nat × Nat), cuts : List (Nat × Nat) }
```

`Regime.empty` is three empty lists. A form entry is a pair `(index, arity)`. A cut entry is an ordered pair of data indices. Form arguments are data indices, not general expressions. There is no kind for a form declaration: a form is an `admittedForm` judgment, and a form application is an instance of kind `dataK`.

## Typing rules

`Typed Γ e k` is the typing relation.

1. If `n ∈ Γ.data`, then `datum n` has kind `dataK`.
2. If `(i, length idx) ∈ Γ.forms` and every index in `idx` is in `Γ.data`, then `form i idx` has kind `dataK`.
3. If `a ∈ Γ.data`, `b ∈ Γ.data`, `(a, b) ∈ Γ.cuts`, and `a ≠ b`, then `cut a b` has kind `distK`.

There is no rule for `token n` (`token_not_typed`). A form application whose arity does not match the declared pair is not typed. The witness is `wrong_arity_not_typed`: in a regime whose only form is `(0, 0)`, `form 0 [1]` is not typed at `dataK`.

## Admission rules

`Step Γ ev Γ'` is one event.

1. `supply n` steps from `Γ` to `Γ`.
2. `admitData n` steps to the regime with `n` consed onto `data`. Membership of `n` is not consulted.
3. `admitForm i k` steps to the regime with `(i, k)` consed onto `forms`. The arity `k` may be 0.
4. `admitCut a b` steps only when `a ∈ Γ.data`, `b ∈ Γ.data`, and `a ≠ b`. The pair `(a, b)` is then consed onto `cuts`.
5. `impose` does not step.

`Reaches` is the reflexive-transitive closure of `Step`.

`Holds Γ J` reads a judgment off a regime.

1. `typed e k` holds when `Typed Γ e k` holds.
2. `admittedData n` holds when `n ∈ Γ.data`.
3. `admittedForm i k` holds when `(i, k) ∈ Γ.forms`.
4. `admittedCut a b` holds when `(a, b) ∈ Γ.cuts` and `a ≠ b`.
5. `apart a b` holds under the same condition as `admittedCut a b`. The two judgments are equivalent (`apart_iff_cut`). `apart` is not a second stored relation.

Preservation: a step, and therefore a reachability chain, keeps every judgment and every typing that already held (`holds_preserved`, `holds_reaches`, `typed_preserved`, `typed_reaches`). Data, forms, and cuts already present stay present (`data_mono`, `forms_mono`, `cuts_mono`).

Concrete derivation. From `Regime.empty`, `admitData 0`, then `admitData 1`, then `admitCut 0 1`, reaches `regime3`, whose data list is `[1, 0]` and whose only cut is `(0, 1)`. In that regime `apart 0 1`, `admittedCut 0 1`, and `Typed (cut 0 1) distK` all hold (`reaches_example`, `example_apart`, `example_admitted_cut`, `example_typed_cut`).

Concrete non-derivation. `apart 0 1` does not hold in `Regime.empty` (`empty_not_apart`). The same judgment is the named non-derivability `AdmitImport.apartOnEmpty`.

Further refusals proved from the same rules: a supply from the empty regime does not admit the supplied index (`supply_not_admit`); a self-cut does not step (`self_cut_refused`); `admittedCut 1 0` does not hold in the regime whose only cut is `(0, 1)`.

## Reflection

`AdmitReflect` quotes expressions, events, judgments, and regimes. For each of those four sorts the quote map and the unquote map are inverses (`unquote_quote_*`, `quote_unquote_*`). That is the whole syntax of the core, not a smaller fragment of it.

`QStep qΓ qe qΓ'` means `Step` on the unquoted triple. For every core regime and event, `QStep` of the quoted triple is equivalent to `Step` (`qstep_sound`). On quoted syntax, supply does not change the quoted regime (`quoted_supply_noop`), a self-cut does not step (`quoted_self_cut_refused`), impose does not step (`quoted_impose_no_step`), and unquoting a quoted token does not type it as data (`quoted_token_not_data`).

This layer does not define a truth predicate. It does not prove a biconditional between a quoted judgment and the holding of that judgment beyond the transport of `Step` and the refusals just named. A Gödel or Tarski fixed point is not constructed.

## Import records

```
ConsStatus ::= proved | openStatus

ImportRecord ::= {
  name            : String,
  axiomsNamed     : List String,
  costName        : String,
  conservativity  : ConsStatus
}

Packed ::= { regime : Regime, imports : List ImportRecord }
```

`coreHolds` ignores `imports` and calls `Holds` on `regime`. Therefore:

- writing one record does not change which judgments hold (`write_import_iff`);
- two packs with the same regime hold the same judgments (`coreHolds_eq_regime`);
- for any record list, the empty regime still does not hold `apart 0 1` (`import_is_not_a_core_derivation`).

The named records, each with `conservativity = openStatus`, are:

| record | axioms named | cost name |
| --- | --- | --- |
| `snImport` | the two boxed laws of TFQ-0510 | unpriced design rule from 002_oesn, not a 19L57G1 theorem |
| `mssnImport` | the MSS-N row atlas, MSS-2 is not S(2), licensed depth 0 | unpriced atlas assumption of TFQ-0528; row count is not depth |
| `rulesImport` | the rules field and the requirements field | unpriced; named in TFQ-0378; no introduction rule in `AdmitCore` |

`sn_import_does_not_derive_apart` is the instance of the general theorem for these three records together. Writing them does not make `apart 0 1` hold in the empty regime.

No import in this development has `conservativity = proved`.

## Interpretations

Each reading is scoped to what `AdmitInterpret` proves. Conservativity over the core is claimed only for the conjunction stated in `id_conservative`.

### IdRefl(2), narrowed

The object theory has two atoms, `zero` and `one`, and one rule: `refl a : IdJudg a a`. There is no `J`, no dependent product, and no universe. Those are not proved.

`twoPoint` is the regime reached from empty by admitting index 1 and then index 0, so the data list is `[0, 1]`.

- Soundness (`id_sound`): a derivable `IdJudg a b` implies that index `atomIndex a` is admitted in `twoPoint` and that `a = b` in the metatheory.
- Conservativity of that conjunction (`id_conservative`): if the index is admitted in `twoPoint` and `a = b`, then `IdJudg a b` is derivable. The claim is only this conjunction, on these two atoms.
- Separation (`admission_is_not_identity`, `not_id_zero_one`): index 0 being admitted does not yield `IdJudg zero one`. Bare admission is not identity.

### Finite 1-skeletal data, defined in this module

An `Edge` is a pair of `Nat` endpoints with a proof they differ. There are no 2-simplices, no horns, and no higher cells. Those are not proved. This module does not import any other agent's simplicial file.

- Soundness (`cut_as_edge`): an admitted cut determines an edge with those endpoints.
- Representation (`edge_realizable`): every such edge is an admitted cut in some regime reached from empty, by admitting the target index, then the source index, then the cut.
- The empty regime holds no cut (`edge_not_held_in_empty`). Existence of an edge is therefore not conservative over the empty regime. Conservativity over an arbitrary fixed regime is not claimed.

### Hereditarily finite terms, finite fragment

`HF` has `empty` and `insert`. `Mem` is the membership relation generated by those constructors. `vonNeumann` sends `0` to `empty` and `n+1` to the insert of `vonNeumann n` into itself. `vn_inj` is injectivity of that map.

- Soundness (`cut_hf_sound`, and the instance `example_cut_hf` for the cut `(0, 1)`): an admitted cut sends the two von Neumann terms to distinct members of `pairSet`.
- The term model distinguishes insertion order (`insert_order_differs`). Extensionality is not proved, and it is false for these terms.
- Infinity, power set, replacement, and the other axioms of a set theory are not proved. Conservativity of this reading over the core is open.

## Gödel and Tarski, and what an import means

No consistent, effectively axiomatised theory contains every truth, and a theory that can represent its own syntax and that has a truth predicate satisfying the usual biconditional cannot, if consistent, contain that predicate for itself. Admit does not escape those limits. It also does not construct a Gödel sentence, and it does not prove a truth-predicate biconditional. The quotation layer is an inverse pair of syntax maps plus transport of the step relation.

An import record is a piece of data sitting beside a regime. It names the axioms being set aside, it names a cost, and it says whether conservativity over the core was proved. "Absorb" means that this record was written. It does not mean that the core derives the named axioms, that the axioms are true, that the extension is consistent, or that no new core judgment becomes derivable. The last of these is a theorem only for the operation of writing the record (`import_is_not_a_core_derivation`): the record is not fed to `Holds`. An extension that added the named axioms as new step rules is a different calculus, and none is defined here.
