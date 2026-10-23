# 19L57G1 object language, admission, readings L and F

Inventory of the public repository `dbccpage/19L57G1` at shallow clone
`85a83ae7ce64dc2123ff218568a4ecd37e566d33` ("Add Apache 2.0 License
attribution (#272)", 2026-10-17). Source tree read from
`C:\Users\a343o\AppData\Local\Temp\fable-src\19L57G1`. Lean was not
rebuilt. Axiom figures are the committed report
`artifacts/lean_axioms.txt`, parsed against the report shape in
`ci/check_lean_audit.py`. Python tests were not re-run.

Citation form: `19L57G1:path::declaration`. Each entry has exactly one
mark: proved in Lean, computed (exact), stated in prose only, or
imported.

This slice is the object language (data, forms, instances, rules,
requirements), admission events, readings L and F, and the minimum-response
tie. Later modules under `lean4/Derivation/` (contact, graph growth,
fidelity paths, declared simplices) are not re-listed theorem by theorem.
They are named only where a README or terminal-result sentence would
otherwise be misread.

## Headline figures

| Claim | What was checked | Result |
|---|---|---|
| 75 Lean modules | `lean4/Derivation/*.lean` and `artifacts/elaborated_modules.txt` | 75 files, 75 census lines, same names. Two further `.lean` files sit outside that census: `lean4/Derivation.lean` and `lean4/ParkedAudit.lean` (77 `.lean` files under `lean4/`). |
| 63 in the root import closure, 12 parked | Import lines of `lean4/Derivation.lean` and of each `lean4/Derivation/*.lean` | 62 direct imports. Transitive closure has 63 modules. The twelve outside it are `Composing`, `DiffAnchor`, `DiffAnchorCompat`, `FormRenaming`, `FormTransport`, `FormTransportCompat`, `IsoBridge`, `IsoBridgeCompat`, `IsoCanon`, `IsoCanonCompat`, `IsoCollapse`, `IsoCollapseCompat`. Those twelve are the imports and `parkedModules` list in `lean4/ParkedAudit.lean`. `LocalStrategy` is not parked: `G1Class` imports it and the root imports `G1Class`. |
| 1530 axiom reports inside `{propext, Quot.sound}` | Every non-empty line of `artifacts/lean_axioms.txt` | 1530 lines, 1530 reports, 1530 distinct quoted names, 0 lines of any other shape. 454 reports depend on no axioms. Among the rest, `propext` occurs in 1016 reports and `Quot.sound` in 890. No report names any other axiom. 1482 reports are emitted from `Derivation.lean`; 48 from `ParkedAudit.lean`. `ci/check_parked_audit.py` pins `EXPECTED_PARKED_REPORTS = 48`. |
| 140 `CL-*` claims | `^### CL-` headings in `paper/paper_claim_ledger.md` and `tests/claim_ledger_body_pin.txt` | 140 headings, 140 distinct ids, 140 pin lines, same id set. |
| Tied minima in readings L and F | Lean theorems, `artifacts/challenges.json`, `artifacts/claims.json`, `paper/paper.md` §11, ledger `CL-3-*` | Split below. Not one status for both readings. |

Toolchain pin in the clone: `lean4/lean-toolchain` is `leanprover/lean4:v4.33.0`.
`lean4/lakefile.toml` has libraries `Derivation` and `ParkedAudit` and no
Mathlib requirement.

The 1530 figure is the committed log artifact, not a fresh `lake build`.

## Tie result

The minimum response is underdetermined only under the declared item-count
measure `mu1`, and the two readings are not in the same status.

Reading L, proved in Lean. `mu1_minimum_not_unique` states that two
two-item responses are valid, that no response of length at most 1 is
valid, and that the results `U0` and `BL` are non-isomorphic:

```
theorem mu1_minimum_not_unique :
    validResponse R2L 0 1 deltaU0 ∧ validResponse R2L 0 1 deltaBL ∧
    deltaU0.length = 2 ∧ deltaBL.length = 2 ∧
    (∀ δ, δ.length ≤ 1 → ¬ validResponse R2L 0 1 δ) ∧
    applyDelta R2L deltaU0 = some U0 ∧
    applyDelta R2L deltaBL = some BL ∧
    (Iso U0 BL → False)
```

`19L57G1:lean4/Derivation/Minimality.lean::mu1_minimum_not_unique`.
Recorded axioms: `[propext, Quot.sound]`
(`19L57G1:artifacts/lean_axioms.txt`, report for
`Derivation.mu1_minimum_not_unique`).

The same file proves a third reading-L class `BD` with
`U0_not_iso_BD` and `BL_not_iso_BD`, collapses the two unary marks by the
definition `isoU1U0`, and proves a countably infinite family: for every
`k ≥ 1`, `deltaK k` is a valid two-item response and distinct arities are
non-isomorphic (`deltaK_valid`, `deltaK_length`, `markK_pairwise_noniso`).
That is an infinite family of finite regimes, not an infinite carrier.

Reading L, exact class count 3 inside `max_items = 2` and `max_arity = 2`,
is computed, not an exhaustiveness theorem. `challenges.json` records
three `iso_classes` under `challenge3.L.mu1`, `minimum_cost` `[2, -1]`,
and `valid_deltas_at_minimum` 6. No Lean theorem says those three are the
only classes inside the bounds.

Reading F, proved in Lean, is the cost floor and one witness, not a tie.
`cost1_insufficient_F` says no delta of length at most 1 is a valid
response on `R2F` for the pair `(1, 2)`. `deltaU0F_valid` says
`[.newForm 1, .newInst 0 [1]]` is valid. Together with the floor, the
minimum item count is 2. There is no reading-F analogue of
`mu1_minimum_not_unique` and no reading-F `markK` family. The ledger says
so: `CL-3-NONUNIQUE-MU1` is "theorem for reading L" and "for reading F,
finite computation", and "no reading-F non-isomorphism theorem exists in
Lean". `CL-3-INFINITE-TIES` is "theorem (reading L)" and "no F-side
analogue of the k-ary family is formalized".

Reading F, the five tied classes, is computed (exact) inside the same
bounds. `challenges.json` `challenge3.F.mu1` lists five `iso_classes`,
`minimum_cost` `[2, -1]`, `valid_deltas_at_minimum` 10. `claims.json`
`CL-3-NONUNIQUE-MU1` is `{"F": 5, "L": 3}`. Labels in the F list:
`form1+inst1` (class size 2), `form2+inst2diag` (size 2), and three
`form2+inst2` representatives with argument tuples `[1, 2]`, `[1, 0]`,
and `[0, 1]` (size 2 each). The L list is `form1+inst1` on argument
`[0]` (size 2), `form2+inst2diag` on `[0, 0]` (size 2), and
`form2+inst2` on `[0, 1]` (size 2).

Under `mu2` the minimum is not tied. `mu2_unique` (reading L) and
`mu2_unique_F` (reading F) are grammar-wide: every valid two-item
response whose new-form arity sum is at most 1 is isomorphic to `U0` or
`U0F` respectively. `claims.json` `CL-3-UNIQUE-MU2` is `{"F": 1, "L": 1}`.
The engine artifact still says, in both the L and the F `mu2` blocks,
"unique up to the implemented isomorphism ... (Lean, reading L)". That
sentence was not updated when `mu2_unique_F` was added. The ledger entry
`CL-3-UNIQUE-MU2-F` and `paper/paper.md` §11 clause (d) do name the
reading-F theorem.

Paper terminal wording, `paper/paper.md` §11, which is stronger on the
"three classes" tag than the ledger:

> (c) **[theorem]** The first separability requirement has minimum response cost exactly two items, absolutely over the item grammar, in both admission readings.
>
> (d) **[theorem, reading L]** Under the item-count measure the minimum is not unique — three non-isomorphic tied classes in reading L, and a countably infinite tie family indexed by arity (one member for every arity k >= 1), both stated over `R2L`. **[bounded theorem]** Five classes in reading F within the declared bounds, by engine enumeration; no reading-F Lean non-uniqueness or k-ary family exists.

Ledger, `paper/paper_claim_ledger.md` `CL-3-TIE-CLASSES`, class "bounded
theorem", bounds `max_items` 2 and `max_arity` 2:

> The tied mu1 minima at Challenge 3 form exactly 3 isomorphism classes in reading L (unary mark, binary link, binary self-loop) and exactly 5 in reading F (adding link-to and link-from the genesis datum).

The Lean non-isomorphism theorems support the distinctness half of the L
count. They do not, by themselves, prove that the bounded enumerator
found every class. The paper's "[theorem, reading L]" tag on the exact
count three is ahead of `CL-3-TIE-CLASSES`, which keeps both counts as a
bounded theorem.

A second underdetermination is the choice of reading, not the choice of
minimum. `CL-READING-UNDERDETERMINATION` is class "unresolved":

> The challenge text underdetermines admission semantics; readings L and F both survive the full derivation and no internal fact separates them.

§11 clause (h) repeats that tag. `code/derivation/engine.py` calls the
same split "a proved underdetermination". That sentence is prose. The
ledger does not classify it as a theorem.

`mu1` and `mu2` are declared measures, not derived ones
(`19L57G1:code/derivation/candidates.py::mu1`,
`19L57G1:code/derivation/candidates.py::mu2`;
`19L57G1:lean4/Derivation/Minimality.lean::aritySum`).

## Object language

Python keeps presentation tokens. Lean `Regime` stores a datum count.
The proved bridge is erasure, not a claim that the two types are the
same.

### Lean types and operations

E01. `Inst` — proved in Lean. `19L57G1:lean4/Derivation/Basic.lean::Inst`.
Abbreviation `Nat × List Nat` (form index, argument tuple). No axiom report.

E02. `Regime` — proved in Lean. `19L57G1:lean4/Derivation/Basic.lean::Regime`.
Fields `data : Nat`, `forms : List Nat`, `insts : List Inst`,
`rules : List Nat`, `reqs : List (Nat × Nat)`. No axiom report.

E03. `Regime.wf` — proved in Lean. `19L57G1:lean4/Derivation/Basic.lean::Regime.wf`.
Instances match form arity and datum bounds, rules name forms, requirements
are ordered pairs of admitted data, every form arity is at least 1.
Definition of a proposition, no axiom report.

E04. `Ctx` — proved in Lean. `19L57G1:lean4/Derivation/Basic.lean::Ctx`.
Fields `form : Nat`, `slots : List (Option Nat)`, with `none` a hole.
No axiom report.

E05. `plug` — proved in Lean. `19L57G1:lean4/Derivation/Basic.lean::plug`.
Fills every hole with one datum. No axiom report.

E06. `derivable` — proved in Lean. `19L57G1:lean4/Derivation/Basic.lean::derivable`.
`i ∈ r.insts ∨ i.1 ∈ r.rules`. No other inference. No axiom report.

E07. `slotOk` — proved in Lean. `19L57G1:lean4/Derivation/Basic.lean::slotOk`.
A slot is a hole or an index below the datum count. No axiom report.

E08. `wfCtx` — proved in Lean. `19L57G1:lean4/Derivation/Basic.lean::wfCtx`.
Form admitted, slot count equals arity, at least one hole, filled slots
in range. No axiom report.

E09. `collapsed` — proved in Lean. `19L57G1:lean4/Derivation/Basic.lean::collapsed`.
Every well-formed context has the same derivability after plugging either
datum. No axiom report.

E10. `separable` — proved in Lean. `19L57G1:lean4/Derivation/Basic.lean::separable`.
Some well-formed context breaks that equivalence. No axiom report.

E11. `separable_not_collapsed` — proved in Lean.
`19L57G1:lean4/Derivation/Basic.lean::separable_not_collapsed`.
Recorded axioms: `[propext]`.

E12. `Event` — proved in Lean. `19L57G1:lean4/Derivation/Basic.lean::Event`.
Constructors `supply`, `admitDatum`, `admitForm`, `admitInst`,
`admitRuleAll`, `impose`. No axiom report.

E13. `stepE` — proved in Lean. `19L57G1:lean4/Derivation/Basic.lean::stepE`.
One admission step. `none` is rejection. `supply` returns `some r`.
`admitDatum` always increments `data` by 1 (no token to dedup).
`admitForm` requires arity at least 1. `admitInst` requires a known form,
matching arity, and in-range arguments, then `insertNew` on instances.
`admitRuleAll` requires a known form, then `insertNew` on rules.
`impose` requires `i < j` and `j < data`, then `insertNew` on requirements.
No axiom report on the definition.

E14. `replayE` — proved in Lean. `19L57G1:lean4/Derivation/Basic.lean::replayE`.
`foldlM stepE`. An ill-formed event poisons the history. No axiom report.

E15. `insertNew` — proved in Lean. `19L57G1:lean4/Derivation/Basic.lean::insertNew`.
If the element is already present, the list is unchanged; otherwise it is
appended. Re-admission is idempotent. No axiom report.

E16. `insertNew_nil` — proved in Lean. `19L57G1:lean4/Derivation/Basic.lean::insertNew_nil`.
`rfl`. No axiom report.

E17. `insertNew_of_not_mem` — proved in Lean. `19L57G1:lean4/Derivation/Basic.lean::insertNew_of_not_mem`.
No axiom report.

E18. `insertNew_of_mem` — proved in Lean. `19L57G1:lean4/Derivation/Basic.lean::insertNew_of_mem`.
No axiom report.

E19. `mem_insertNew` — proved in Lean. `19L57G1:lean4/Derivation/Basic.lean::mem_insertNew`.
No axiom report.

E20. `Item` — proved in Lean. `19L57G1:lean4/Derivation/Basic.lean::Item`.
`newDatum`, `newForm`, `newInst`, `newRuleAll`. A response delta is a
`List Item`. `Impose` is not an item. No axiom report.

E21. `applyItem` — proved in Lean. `19L57G1:lean4/Derivation/Basic.lean::applyItem`.
Same guards as the matching admission constructors. No axiom report.

E22. `applyDelta` — proved in Lean. `19L57G1:lean4/Derivation/Basic.lean::applyDelta`.
`foldlM applyItem`. No axiom report.

E23. `validResponse` — proved in Lean. `19L57G1:lean4/Derivation/Basic.lean::validResponse`.
The delta applies, the result separates the target pair, and every
previously imposed requirement stays separated. No axiom report.

E24. `R2L` — proved in Lean. `19L57G1:lean4/Derivation/Basic.lean::R2L`.
`⟨2, [], [], [], [(0, 1)]⟩`. Two data, no forms, no instances, no rules,
one requirement. No axiom report.

E25. `R2F` — proved in Lean. `19L57G1:lean4/Derivation/Basic.lean::R2F`.
`⟨3, [], [], [], [(1, 2)]⟩`. Three data, requirement on the last two.
No axiom report.

E26. `R2L_wf` — proved in Lean. `19L57G1:lean4/Derivation/Basic.lean::R2L_wf`.
No axiom report.

E27. `R2F_wf` — proved in Lean. `19L57G1:lean4/Derivation/Basic.lean::R2F_wf`.
No axiom report.

E28. `genesis` — proved in Lean. `19L57G1:lean4/Derivation/Inertia.lean::genesis`.
`⟨0, [], [], [], []⟩`. No axiom report.

E29. `supply_no_op` — proved in Lean. `19L57G1:lean4/Derivation/Inertia.lean::supply_no_op`.
`stepE r (.supply t) = some r`. Recorded axioms: `[propext]`.

E30. `genesis_underivable` — proved in Lean. `19L57G1:lean4/Derivation/Inertia.lean::genesis_underivable`.
Nothing is derivable at `genesis`. Recorded axioms: none.

E31. `underivable_of_empty` — proved in Lean. `19L57G1:lean4/Derivation/Inertia.lean::underivable_of_empty`.
No instances and no rules implies nothing is derivable. Recorded axioms: none.

E32. `collapsed_of_no_insts` — proved in Lean. `19L57G1:lean4/Derivation/Inertia.lean::collapsed_of_no_insts`.
No instances implies every datum pair is collapsed. Uniform rules do not
separate. Recorded axioms: `[propext]`.

E33. `R2L_collapsed` — proved in Lean. `19L57G1:lean4/Derivation/Inertia.lean::R2L_collapsed`.
`collapsed R2L 0 1`. Recorded axioms: `[propext]`.

E34. `R2F_collapsed` — proved in Lean. `19L57G1:lean4/Derivation/Inertia.lean::R2F_collapsed`.
`collapsed R2F d d'` for every pair. Recorded axioms: `[propext]`.

E35. `historyL_replays` — proved in Lean. `19L57G1:lean4/Derivation/Inertia.lean::historyL_replays`.
`replayE [.supply 0, .supply 1, .supply 1, .supply 2, .admitDatum, .admitDatum, .impose 0 1] genesis = some R2L`.
Recorded axioms: `[propext]`. The Lean history has no tokens; the two
`admitDatum` steps are what produce the two data. This is not the Python
token history.

E36. `historyF_replays` — proved in Lean. `19L57G1:lean4/Derivation/Inertia.lean::historyF_replays`.
`replayE [.supply 0, .admitDatum, .supply 1, .supply 1, .supply 2, .admitDatum, .admitDatum, .impose 1 2] genesis = some R2F`.
Recorded axioms: `[propext]`.

E37. `admission_without_expressive_increase` — proved in Lean. `19L57G1:lean4/Derivation/Inertia.lean::admission_without_expressive_increase`.
Admitting one more datum from `R2L` changes the state and leaves pair
`(0, 1)` collapsed. Recorded axioms: `[propext]`.

E38. `replayE_append` — proved in Lean. `19L57G1:lean4/Derivation/Inertia.lean::replayE_append`.
Replay of a snoc is bind of `stepE` on the replayed prefix. Recorded
axioms: `[propext, Quot.sound]`.

### Token-aware layer and erasure

E39. `TRegime` — proved in Lean. `19L57G1:lean4/Derivation/Erasure.lean::TRegime`.
`tokens : List Nat` plus the same forms, instances, rules, and requirements.
No axiom report.

E40. `TEvent` — proved in Lean. `19L57G1:lean4/Derivation/Erasure.lean::TEvent`.
`admitDatum` carries a token. No axiom report.

E41. `stepT` — proved in Lean. `19L57G1:lean4/Derivation/Erasure.lean::stepT`.
Re-admitting a token already in `tokens` leaves the state. Otherwise the
token is appended. Other constructors match `stepE`. No axiom report.

E42. `TRegime.erase` — proved in Lean. `19L57G1:lean4/Derivation/Erasure.lean::TRegime.erase`.
Replaces the token list by its length. No axiom report.

E43. `eraseEvent` — proved in Lean. `19L57G1:lean4/Derivation/Erasure.lean::eraseEvent`.
A duplicate `admitDatum` erases to `supply`. No axiom report.

E44. `erase_step` — proved in Lean. `19L57G1:lean4/Derivation/Erasure.lean::erase_step`.
One token-aware step then erasure equals the erased step. Recorded axioms:
`[propext, Quot.sound]`.

E45. `replayT` — proved in Lean. `19L57G1:lean4/Derivation/Erasure.lean::replayT`.
No axiom report.

E46. `eraseHistory` — proved in Lean. `19L57G1:lean4/Derivation/Erasure.lean::eraseHistory`.
Threads `stepT` so each duplicate admission becomes a supply. On `none`,
the continuation is cut. No axiom report.

E47. `replayT_cons` — proved in Lean. `19L57G1:lean4/Derivation/Erasure.lean::replayT_cons`.
No axiom report.

E48. `replayE_cons` — proved in Lean. `19L57G1:lean4/Derivation/Erasure.lean::replayE_cons`.
No axiom report.

E49. `erase_replay` — proved in Lean. `19L57G1:lean4/Derivation/Erasure.lean::erase_replay`.
History-level simulation. Recorded axioms: `[propext, Quot.sound]`.

### Extensionality of the list presentation

Python stores `insts`, `rules`, and `reqs` as sets. Lean stores
deduplicated lists. Transport is proved for the observables below, not
for every later definition in the tree. The paper states that unrestricted
factorization is not proved (`paper/paper.md` §3).

E50. `SetEq` — proved in Lean. `19L57G1:lean4/Derivation/Ext.lean::SetEq`.
No axiom report.

E51. `SetEq.rfl'` — proved in Lean. `19L57G1:lean4/Derivation/Ext.lean::SetEq.rfl'`.
No axiom report.

E52. `SetEq.symm'` — proved in Lean. `19L57G1:lean4/Derivation/Ext.lean::SetEq.symm'`.
No axiom report.

E53. `SetEq.insertNew'` — proved in Lean. `19L57G1:lean4/Derivation/Ext.lean::SetEq.insertNew'`.
No axiom report.

E54. `RegimeExt` — proved in Lean. `19L57G1:lean4/Derivation/Ext.lean::RegimeExt`.
Equal `data` and `forms`, membership-equal instances, rules, and requirements.
No axiom report.

E55. `RegimeExt.refl'` — proved in Lean. `19L57G1:lean4/Derivation/Ext.lean::RegimeExt.refl'`.
No axiom report.

E56. `RegimeExt.symm'` — proved in Lean. `19L57G1:lean4/Derivation/Ext.lean::RegimeExt.symm'`.
No axiom report.

E57. `derivable_ext` — proved in Lean. `19L57G1:lean4/Derivation/Ext.lean::derivable_ext`.
Recorded axioms: none.

E58. `wfCtx_ext` — proved in Lean. `19L57G1:lean4/Derivation/Ext.lean::wfCtx_ext`.
Recorded axioms: `[propext]`.

E59. `collapsed_ext` — proved in Lean. `19L57G1:lean4/Derivation/Ext.lean::collapsed_ext`.
Recorded axioms: `[propext]`.

E60. `separable_ext` — proved in Lean. `19L57G1:lean4/Derivation/Ext.lean::separable_ext`.
Recorded axioms: `[propext]`.

E61. `OptExt` — proved in Lean. `19L57G1:lean4/Derivation/Ext.lean::OptExt`.
No axiom report.

E62. `applyItem_ext` — proved in Lean. `19L57G1:lean4/Derivation/Ext.lean::applyItem_ext`.
Recorded axioms: `[propext]`.

E63. `applyDelta_ext` — proved in Lean. `19L57G1:lean4/Derivation/Ext.lean::applyDelta_ext`.
Recorded axioms: `[propext]`.

E64. `validResponse_ext` — proved in Lean. `19L57G1:lean4/Derivation/Ext.lean::validResponse_ext`.
Recorded axioms: `[propext]`.

### Quotient barrier

E65. `quotient_barrier` — proved in Lean. `19L57G1:lean4/Derivation/Quot.lean::quotient_barrier`.
A function out of a `Quotient` agrees on identified elements, by
`congrArg` of `Quotient.sound`. Recorded axioms: `[Quot.sound]`.

E66. `quot_barrier` — proved in Lean. `19L57G1:lean4/Derivation/Quot.lean::quot_barrier`.
Same statement for `Quot`. Recorded axioms: `[Quot.sound]`.

E67. `collapseRel` — proved in Lean. `19L57G1:lean4/Derivation/Quot.lean::collapseRel`.
`collapsed r d d'`. No axiom report.

E68. `barrier_R2L` — proved in Lean. `19L57G1:lean4/Derivation/Quot.lean::barrier_R2L`.
Any map out of `Quot (collapseRel R2L)` identifies `0` and `1`.
Recorded axioms: `[propext, Quot.sound]`.

### Mention lemmas used by the reading-F `mu2` case

E69. `mem_plug_of_hole` — proved in Lean. `19L57G1:lean4/Derivation/Mention.lean::mem_plug_of_hole`.
Recorded axioms: `[propext, Quot.sound]`.

E70. `not_mem_of_arg_out_of_range` — proved in Lean. `19L57G1:lean4/Derivation/Mention.lean::not_mem_of_arg_out_of_range`.
Recorded axioms: none.

E71. `exists_out_of_range_slot` — proved in Lean. `19L57G1:lean4/Derivation/Mention.lean::exists_out_of_range_slot`.
Recorded axioms: `[propext]`.

E72. `collapsed_append_unmentioning` — proved in Lean. `19L57G1:lean4/Derivation/Mention.lean::collapsed_append_unmentioning`.
Appending instances that mention neither target datum preserves collapse
of that pair. Recorded axioms: `[propext, Quot.sound]`. Used by
`genesis_mark_not_separable`.

E73. `collapsed_fresh_datum` — proved in Lean. `19L57G1:lean4/Derivation/Mention.lean::collapsed_fresh_datum`.
A fresh unmentioned datum preserves collapse of an existing pair.
Recorded axioms: `[propext, Quot.sound]`.

E74. `getD_append_left` — proved in Lean. `19L57G1:lean4/Derivation/Mention.lean::getD_append_left`.
Recorded axioms: `[propext]`.

E75. `collapsed_fresh_form` — proved in Lean. `19L57G1:lean4/Derivation/Mention.lean::collapsed_fresh_form`.
Recorded axioms: `[propext]`.

### Challenge 3 minima

E76. `aritySum` — proved in Lean. `19L57G1:lean4/Derivation/Minimality.lean::aritySum`.
Sum of `newForm` arities. Second component of `mu2`. No axiom report.

E77. `applyDelta_single` — proved in Lean. `19L57G1:lean4/Derivation/Minimality.lean::applyDelta_single`.
No axiom report.

E78. `applyDelta_pair` — proved in Lean. `19L57G1:lean4/Derivation/Minimality.lean::applyDelta_pair`.
No axiom report.

E79. `U0` — proved in Lean. `19L57G1:lean4/Derivation/Minimality.lean::U0`.
Unary mark on datum 0: `⟨2, [1], [(0, [0])], [], [(0, 1)]⟩`. No axiom report.

E80. `U1` — proved in Lean. `19L57G1:lean4/Derivation/Minimality.lean::U1`.
Unary mark on datum 1. No axiom report.

E81. `BL` — proved in Lean. `19L57G1:lean4/Derivation/Minimality.lean::BL`.
Binary link `[(0, [0, 1])]`. No axiom report.

E82. `BD` — proved in Lean. `19L57G1:lean4/Derivation/Minimality.lean::BD`.
Binary self-loop `[(0, [0, 0])]`. No axiom report.

E83. `U0_separable` — proved in Lean. `19L57G1:lean4/Derivation/Minimality.lean::U0_separable`.
Recorded axioms: `[propext, Quot.sound]`.

E84. `U1_separable` — proved in Lean. `19L57G1:lean4/Derivation/Minimality.lean::U1_separable`.
Recorded axioms: `[propext, Quot.sound]`.

E85. `BL_separable` — proved in Lean. `19L57G1:lean4/Derivation/Minimality.lean::BL_separable`.
Recorded axioms: `[propext, Quot.sound]`.

E86. `BD_separable` — proved in Lean. `19L57G1:lean4/Derivation/Minimality.lean::BD_separable`.
Recorded axioms: `[propext, Quot.sound]`.

E87. `deltaU0` — proved in Lean. `19L57G1:lean4/Derivation/Minimality.lean::deltaU0`.
`[.newForm 1, .newInst 0 [0]]`. No axiom report.

E88. `deltaU1` — proved in Lean. `19L57G1:lean4/Derivation/Minimality.lean::deltaU1`.
No axiom report.

E89. `deltaBL` — proved in Lean. `19L57G1:lean4/Derivation/Minimality.lean::deltaBL`.
No axiom report.

E90. `deltaBD` — proved in Lean. `19L57G1:lean4/Derivation/Minimality.lean::deltaBD`.
No axiom report.

E91. `validResponse_R2L` — proved in Lean. `19L57G1:lean4/Derivation/Minimality.lean::validResponse_R2L`.
On `R2L`, separating `(0, 1)` preserves the only imposed requirement.
No axiom report.

E92. `deltaU0_valid` — proved in Lean. `19L57G1:lean4/Derivation/Minimality.lean::deltaU0_valid`.
Recorded axioms: `[propext, Quot.sound]`.

E93. `deltaU1_valid` — proved in Lean. `19L57G1:lean4/Derivation/Minimality.lean::deltaU1_valid`.
Recorded axioms: `[propext, Quot.sound]`.

E94. `deltaBL_valid` — proved in Lean. `19L57G1:lean4/Derivation/Minimality.lean::deltaBL_valid`.
Recorded axioms: `[propext, Quot.sound]`.

E95. `deltaBD_valid` — proved in Lean. `19L57G1:lean4/Derivation/Minimality.lean::deltaBD_valid`.
Recorded axioms: `[propext, Quot.sound]`.

E96. `no_insts_no_separation` — proved in Lean. `19L57G1:lean4/Derivation/Minimality.lean::no_insts_no_separation`.
Empty instance list contradicts separability. No axiom report.

E97. `cost1_insufficient_general` — proved in Lean. `19L57G1:lean4/Derivation/Minimality.lean::cost1_insufficient_general`.
On any form-less, instance-less regime, no delta of length at most 1 is
a valid response. Recorded axioms: `[propext]`.

E98. `cost1_insufficient` — proved in Lean. `19L57G1:lean4/Derivation/Minimality.lean::cost1_insufficient`.
Reading L. Recorded axioms: `[propext]`.

E99. `cost1_insufficient_F` — proved in Lean. `19L57G1:lean4/Derivation/Minimality.lean::cost1_insufficient_F`.
Reading F. Recorded axioms: `[propext]`.

E100. `deltaU0F_valid` — proved in Lean. `19L57G1:lean4/Derivation/Minimality.lean::deltaU0F_valid`.
`validResponse R2F 1 2 [.newForm 1, .newInst 0 [1]]`. Recorded axioms:
`[propext, Quot.sound]`.

E101. `sortPair` — proved in Lean. `19L57G1:lean4/Derivation/Minimality.lean::sortPair`.
Orders a requirement pair. No axiom report.

E102. `Iso` — proved in Lean. `19L57G1:lean4/Derivation/Minimality.lean::Iso`.
Structure, not a proposition: datum and form maps with two-sided inverses
on the admitted ranges, preserving arities, instances, rules, and
sorted requirement pairs. No axiom report. `ParkedAudit.lean` records
that this being `Type`-valued makes some parked isomorphism proofs `def`s,
so they emit no theorem report.

E103. `isoRefl` — proved in Lean. `19L57G1:lean4/Derivation/Minimality.lean::isoRefl`.
Identity isomorphism when requirements are already sorted. No axiom report.

E104. `swap01` — proved in Lean. `19L57G1:lean4/Derivation/Minimality.lean::swap01`.
No axiom report.

E105. `isoU1U0` — proved in Lean. `19L57G1:lean4/Derivation/Minimality.lean::isoU1U0`.
`Iso U1 U0` via `swap01`. Definitional witness, no axiom report.

E106. `U0_not_iso_BL` — proved in Lean. `19L57G1:lean4/Derivation/Minimality.lean::U0_not_iso_BL`.
Arity is invariant. Recorded axioms: `[propext, Quot.sound]`.

E107. `U0_not_iso_BD` — proved in Lean. `19L57G1:lean4/Derivation/Minimality.lean::U0_not_iso_BD`.
Recorded axioms: `[propext, Quot.sound]`.

E108. `BL_not_iso_BD` — proved in Lean. `19L57G1:lean4/Derivation/Minimality.lean::BL_not_iso_BD`.
A datum bijection cannot send both endpoints of the link to one loop index.
Recorded axioms: `[propext, Quot.sound]`.

E109. `mu1_minimum_not_unique` — proved in Lean. `19L57G1:lean4/Derivation/Minimality.lean::mu1_minimum_not_unique`.
Statement quoted in the tie section. Recorded axioms: `[propext, Quot.sound]`.
Reading L only. It exhibits two non-isomorphic minima (`U0` and `BL`),
not the bounded count three and not reading F.

E110. `markK` — proved in Lean. `19L57G1:lean4/Derivation/Minimality.lean::markK`.
`⟨2, [k], [(0, List.replicate k 1)], [], [(0, 1)]⟩`. No axiom report.

E111. `deltaK` — proved in Lean. `19L57G1:lean4/Derivation/Minimality.lean::deltaK`.
`[.newForm k, .newInst 0 (List.replicate k 1)]`. No axiom report.

E112. `deltaK_applies` — proved in Lean. `19L57G1:lean4/Derivation/Minimality.lean::deltaK_applies`.
For `1 ≤ k`. Recorded axioms: `[propext, Quot.sound]`.

E113. `markK_separable` — proved in Lean. `19L57G1:lean4/Derivation/Minimality.lean::markK_separable`.
Recorded axioms: `[propext, Quot.sound]`.

E114. `deltaK_valid` — proved in Lean. `19L57G1:lean4/Derivation/Minimality.lean::deltaK_valid`.
Recorded axioms: `[propext, Quot.sound]`.

E115. `deltaK_length` — proved in Lean. `19L57G1:lean4/Derivation/Minimality.lean::deltaK_length`.
Length 2, by `rfl`. Recorded axioms: none.

E116. `markK_pairwise_noniso` — proved in Lean. `19L57G1:lean4/Derivation/Minimality.lean::markK_pairwise_noniso`.
`j ≠ k` implies there is no `Iso (markK j) (markK k)`. Recorded axioms:
`[propext]`.

E117. `mu2_unique` — proved in Lean. `19L57G1:lean4/Derivation/Minimality.lean::mu2_unique`.
Every valid two-item response on `R2L` for `(0, 1)` with `aritySum ≤ 1`
lands in a regime isomorphic to `U0`. Recorded axioms: `[propext, Quot.sound]`.

E118. `U0F` — proved in Lean. `19L57G1:lean4/Derivation/MinimalityF.lean::U0F`.
`⟨3, [1], [(0, [1])], [], [(1, 2)]⟩`. No axiom report.

E119. `U2F` — proved in Lean. `19L57G1:lean4/Derivation/MinimalityF.lean::U2F`.
Mark on datum 2. No axiom report.

E120. `swap12` — proved in Lean. `19L57G1:lean4/Derivation/MinimalityF.lean::swap12`.
Swaps data 1 and 2 and fixes 0. No axiom report.

E121. `isoU2F_U0F` — proved in Lean. `19L57G1:lean4/Derivation/MinimalityF.lean::isoU2F_U0F`.
Definitional witness. No axiom report.

E122. `genesis_mark_not_separable` — proved in Lean. `19L57G1:lean4/Derivation/MinimalityF.lean::genesis_mark_not_separable`.
The unary mark on datum 0 does not separate `(1, 2)`. Recorded axioms:
`[propext, Quot.sound]`.

E123. `mu2_unique_F` — proved in Lean. `19L57G1:lean4/Derivation/MinimalityF.lean::mu2_unique_F`.
Every valid two-item response on `R2F` for `(1, 2)` with `aritySum ≤ 1`
lands in a regime isomorphic to `U0F`. Recorded axioms:
`[propext, Quot.sound]`.

### One concrete response, and the conditional round bound

E124. `mark_progress` — proved in Lean. `19L57G1:lean4/Derivation/Progress.lean::mark_progress`.
On a well-formed regime, for distinct in-range data whose imposed
requirements are already separated, the two-item fresh unary mark on the
second datum is a valid response. The module states that this does not
quantify over the candidate grammar. Recorded axioms: `[propext, Quot.sound]`.
This is the Lean form of paper §11 clause (e)'s existence claim only for
this one delta. The clause's wording "every supplied separation demand
... is answerable" is wider; the theorem's own comment refuses that width.

E125. `separable_of_subrules` — proved in Lean. `19L57G1:lean4/Derivation/Progress.lean::separable_of_subrules`.
Shrinking the rule list preserves separability. Recorded axioms: `[propext]`.
Supports `CL-PRUNE-RULE` part (i), which is a pruning fact used by the
bounded tie enumeration, not itself the tie.

E126. `getD_append_lt` — proved in Lean. `19L57G1:lean4/Derivation/Progress.lean::getD_append_lt`.
Recorded axioms: `[propext, Quot.sound]`. Helper for `mark_progress`.

E127. `old_inst_form_lt` — proved in Lean. `19L57G1:lean4/Derivation/Progress.lean::old_inst_form_lt`.
No axiom report. Helper.

E128. `getD_concat_self` — proved in Lean. `19L57G1:lean4/Derivation/Progress.lean::getD_concat_self`.
No axiom report. Helper.

E129. `derivable_extend` — proved in Lean. `19L57G1:lean4/Derivation/Progress.lean::derivable_extend`.
No axiom report. Helper.

E130. `index_le_strict_mono` — proved in Lean. `19L57G1:lean4/Derivation/Counting.lean::index_le_strict_mono`.
Recorded axioms: `[propext, Quot.sound]`.

E131. `strict_bounded_length` — proved in Lean. `19L57G1:lean4/Derivation/Counting.lean::strict_bounded_length`.
Recorded axioms: `[propext, Quot.sound]`.

E132. `no_supply_round_bound` — proved in Lean. `19L57G1:lean4/Derivation/Counting.lean::no_supply_round_bound`.
If a run's measure strictly increases and stays at most `n * (n - 1) / 2`,
then the length is at most that bound plus one. The module says the
engine's rounds meet those hypotheses only computationally, and that a
Lean theorem connecting the hypotheses to the transition system is not
proved. Recorded axioms: `[propext, Quot.sound]`.

E133. `allPairs` — proved in Lean. `19L57G1:lean4/Derivation/Counting.lean::allPairs`.
Ordered pairs `i < j < n`. No axiom report.

E134. `allPairs_length` — proved in Lean. `19L57G1:lean4/Derivation/Counting.lean::allPairs_length`.
`2 * (allPairs n).length = n * (n - 1)`. Recorded axioms:
`[propext, Quot.sound]`.

## Executable model and exact artifacts

E135. Python `Regime` — computed (exact). `19L57G1:code/derivation/model.py::Regime`.
`data: tuple[str, ...]`, `forms: tuple[int, ...]`, `insts: frozenset[Inst]`,
`rules: frozenset[int]`, `reqs: frozenset[Pair]`. Tokens are metatheoretic.

E136. `EMPTY` — computed (exact). `19L57G1:code/derivation/model.py::EMPTY`.

E137. `AdmissionError` — computed (exact). `19L57G1:code/derivation/model.py::AdmissionError`.
Ill-formed events raise. The Lean twin returns `none` instead.

E138. `Supply` — computed (exact). `19L57G1:code/derivation/model.py::Supply`.
`step` returns the same regime.

E139. `AdmitDatum` — computed (exact). `19L57G1:code/derivation/model.py::AdmitDatum`.
If the token is already in `data`, the state is unchanged. Otherwise the
token is appended. This dedup is in Python `step` and in Lean `stepT`,
not in Lean `stepE`.

E140. `AdmitForm` — computed (exact). `19L57G1:code/derivation/model.py::AdmitForm`.
Arity below 1 raises.

E141. `AdmitInst` — computed (exact). `19L57G1:code/derivation/model.py::AdmitInst`.
Unknown form, wrong arity, or out-of-range argument raises. Otherwise the
instance is unioned into the set.

E142. `AdmitRuleAll` — computed (exact). `19L57G1:code/derivation/model.py::AdmitRuleAll`.
Unknown form raises. Otherwise the form index is unioned into `rules`.

E143. `Impose` — computed (exact). `19L57G1:code/derivation/model.py::Impose`.
Requires `0 ≤ i < j < len(data)`. Otherwise raises. The pair is unioned
into `reqs`.

E144. `Event` — computed (exact). `19L57G1:code/derivation/model.py::Event`.
Union of the six classes above.

E145. `step` — computed (exact). `19L57G1:code/derivation/model.py::step`.

E146. `replay` — computed (exact). `19L57G1:code/derivation/model.py::replay`.
Fold of `step` from `EMPTY` unless another base is passed. It raises
rather than returning a failure value.

E147. `certify` — computed (exact). `19L57G1:code/derivation/model.py::certify`.
`replay(history) == claimed`.

E148. `Args`, `Inst`, `Pair` — computed (exact). `19L57G1:code/derivation/model.py::Args`,
`19L57G1:code/derivation/model.py::Inst`, `19L57G1:code/derivation/model.py::Pair`.

E149. `Context` — computed (exact). `19L57G1:code/derivation/observe.py::Context`.
`(form, slots)` with at least one hole.

E150. `contexts` — computed (exact). `19L57G1:code/derivation/observe.py::contexts`.

E151. `plug` — computed (exact). `19L57G1:code/derivation/observe.py::plug`.

E152. `derivable` — computed (exact). `19L57G1:code/derivation/observe.py::derivable`.
Rule coverage or instance membership.

E153. `profile` — computed (exact). `19L57G1:code/derivation/observe.py::profile`.
Contexts whose plugging is derivable. Lean has no separate `profile`
definition; `collapsed` quantifies over contexts directly.

E154. `separable` — computed (exact). `19L57G1:code/derivation/observe.py::separable`.
Profiles differ.

E155. `collapsed_pairs` — computed (exact). `19L57G1:code/derivation/observe.py::collapsed_pairs`.

E156. `satisfies` — computed (exact). `19L57G1:code/derivation/observe.py::satisfies`.
Every imposed pair has distinct profiles.

E157. `NewDatum`, `NewForm`, `NewInst`, `NewRuleAll`, `Item`, `Delta` — computed (exact).
`19L57G1:code/derivation/candidates.py::NewDatum` and the sibling classes
and aliases in that file.

E158. `mu1` — computed (exact). `19L57G1:code/derivation/candidates.py::mu1`.
`len(delta)`. Declared, not derived.

E159. `mu2` — computed (exact). `19L57G1:code/derivation/candidates.py::mu2`.
`(len(delta), sum of new-form arities)`. Declared, not derived.

E160. `Bounds` — computed (exact). `19L57G1:code/derivation/candidates.py::Bounds`.
Defaults `max_items = 2`, `max_arity = 2`. Same numbers in
`19L57G1:artifacts/bounds.json`.

E161. `min_responses` — computed (exact). `19L57G1:code/derivation/candidates.py::min_responses`.
Enumerator used to fill `challenges.json`. Not re-executed for this inventory.
The committed JSON is the exact artifact on disk.

E162. `canonical`, `isomorphic`, `find_iso` — computed (exact).
`19L57G1:code/derivation/iso.py::canonical`,
`19L57G1:code/derivation/iso.py::isomorphic`,
`19L57G1:code/derivation/iso.py::find_iso`.
The Lean `Iso` structure is the relation the paper says this implements.
Brute-force cross-check is `canonical_bruteforce` in the same file.
Perm budget default `100_000`, also `perm_budget` in `bounds.json`.

E163. `GENESIS_L` — computed (exact). `19L57G1:code/derivation/engine.py::GENESIS_L`.
`Supply("<>")`, `Supply("<a>")`, `Supply("<a>")`, `Supply("<ab>")`,
`AdmitDatum("<a>")`, `AdmitDatum("<ab>")`. The initial token is supplied
and never admitted.

E164. `GENESIS_F` — computed (exact). `19L57G1:code/derivation/engine.py::GENESIS_F`.
`Supply("<>")`, `AdmitDatum("<>")`, then the same `<a>` / `<ab>` supply
and retention as L. The initial token is admitted.

E165. `READING_L` — computed (exact). `19L57G1:code/derivation/engine.py::READING_L`.
Name `"L"`, target pair `(0, 1)`, history `GENESIS_L`.

E166. `READING_F` — computed (exact). `19L57G1:code/derivation/engine.py::READING_F`.
Name `"F"`, target pair `(1, 2)`, history `GENESIS_F`.

E167. `claims.json` `CL-3-MIN-TWO` — computed (exact).
`19L57G1:artifacts/claims.json::CL-3-MIN-TWO`.
Both readings `[2, -1]`. The `-1` is the unused second cost component
under `mu1`.

E168. `claims.json` `CL-3-NONUNIQUE-MU1` — computed (exact).
`19L57G1:artifacts/claims.json::CL-3-NONUNIQUE-MU1`.
`L` is 3, `F` is 5.

E169. `claims.json` `CL-3-UNIQUE-MU2` — computed (exact).
`19L57G1:artifacts/claims.json::CL-3-UNIQUE-MU2`.
`L` is 1, `F` is 1.

E170. `claims.json` `CL-3-FAIL-CURRENT` — computed (exact).
`19L57G1:artifacts/claims.json::CL-3-FAIL-CURRENT`.
Both readings `false`: the Challenge 2 regime does not already separate
the target.

E171. `challenges.json` `challenge3.L.mu1` — computed (exact).
`19L57G1:artifacts/challenges.json::challenge3`.
Three isomorphism classes, six valid minimum deltas, cost `[2, -1]`,
bounds arity 2 and items 2. See the tie section for the representatives.

E172. `challenges.json` `challenge3.F.mu1` — computed (exact).
`19L57G1:artifacts/challenges.json::challenge3`.
Five isomorphism classes, ten valid minimum deltas, cost `[2, -1]`,
same bounds.

E173. `challenges.json` `challenge3` `mu2` blocks — computed (exact).
`19L57G1:artifacts/challenges.json::challenge3`.
One class in each reading, cost `[2, 1]`, two valid deltas. The
`uniqueness_scope` string still says "Lean, reading L" inside the F block.
See the tie section.

## Stated in prose only

E174. Reading choice is unresolved — stated in prose only.
`19L57G1:paper/paper_claim_ledger.md::CL-READING-UNDERDETERMINATION`
and `19L57G1:paper/paper.md` §11 clause (h). Both readings are carried.
No theorem selects one. `R2L` and `R2F` are definitions of the two
branches, not a proof that the challenge text forces either.

E175. Engine docstring "proved underdetermination" — stated in prose only.
`19L57G1:code/derivation/engine.py` module comment. It disagrees with
the ledger class "unresolved" on the same split.

E176. README summary of the tie — stated in prose only.
`19L57G1:README.md` lines 33–44. It matches the split proved-plus-computed
result when "within the declared bounds" is kept on the counts three and
five, and when the infinite family is kept on reading L. It is not itself
a declaration with an axiom report.

E177. §11 clause (d) tag "[theorem, reading L]" on the exact count three —
stated in prose only as a classification tag. The non-isomorphism of
three named regimes is E106–E108. Exhaustiveness inside the bounds is
E171.

E178. No universal property — stated in prose only.
`19L57G1:paper/paper_claim_ledger.md::CL-NO-UNIVERSAL-PROPERTY`.
Class "unresolved — claim refused". No Lean name is cited.

E179. Pair-separation closure and external supply are declared policies —
stated in prose only as derivation status.
`19L57G1:paper/paper.md` §3 items 9 and 10, and the module comment of
`code/derivation/engine.py`. The closed-system numbers in `claims.json`
(`closed_L` terminal branches 3, `closed_F` terminal branches 16) are
artifact fields, not an object-language admission constructor. No
endogenous demand generator is claimed to have been derived.

E180. README test census — stated in prose only.
`19L57G1:README.md` row "55 files, 787 collected: 786 passed / 1 skipped"
dated 2026-09-19 in the following paragraph. No declaration of those
integers was found outside that prose. At this commit `tests/` contains
61 `.py` files. Pytest was not run.

E181. README sentence that four apparatus definitions in `ParkedAudit.lean`
carry `Classical.choice` — stated in prose only.
`19L57G1:README.md` near the axiom-clean bullet, attributed to a local
run of `ci/check_declaration_axioms.py` on 2026-09-18. The token
`Classical.choice` occurs in comments in `ParkedAudit.lean`,
`Breaking.lean`, `Composing.lean`, `Pigeonhole.lean`, and `Rounds.lean`.
No theorem in the 1530 reports names `Classical.choice`. This inventory
did not re-run the declaration scanner, so the four-definition measurement
was not rechecked.

## Imported

E182. `propext` — imported. Lean-core axiom. Not declared in this
repository. It is the only propositional-extensionality axiom named in
`artifacts/lean_axioms.txt`.

E183. `Quot.sound` — imported. Lean-core axiom. Not declared in this
repository. `quotient_barrier` and `quot_barrier` apply the corresponding
soundness lemma (`Quotient.sound` / `Quot.sound`) and the reports name
this axiom. No Mathlib import is present in `lean4/lakefile.toml`.

## Mark counts

| Mark | Entries |
|---|---|
| proved in Lean | 134 (E01–E134) |
| computed (exact) | 39 (E135–E173) |
| stated in prose only | 8 (E174–E181) |
| imported | 2 (E182–E183) |
| Total | 183 |

Of the 134 Lean entries, 61 have an individual line in
`artifacts/lean_axioms.txt` and 73 do not. The 73 are definitions or
unreported lemmas. Absence of a line is not a claim that the declaration
is axiom-free. Reports that do exist and say "does not depend on any
axioms" are E30, E31, E57, E70, and E115.

## Not available

Not in the object language, and not a theorem of the tie:

- An infinite admitted carrier. `Regime.data` is a finite count.
  `markK` is an infinite family of finite regimes (E110–E116). That
  family is available, and it is reading L only.
- An unbounded continuation. §11 clause (g) marks continuation past the
  exported depths unresolved. `no_supply_round_bound` (E132) does not
  discharge the engine's strict-increase hypothesis.
- A path type, a homotopy, or higher-cell composition inside `Regime`,
  `Event`, `stepE`, or `validResponse`. None of those declarations has
  a path, a homotopy, or a cell composer.
- The word homotopy. No `homotopy` declaration was found under `lean4/`.

Present in the same repository, outside this slice, so not "missing from
the tree" and not part of the admission kernel:

- `19L57G1:lean4/Derivation/HigherStructure.lean` declares a finite path
  graph grown from a passage, and a cell calculus whose header describes
  0-, 1-, 2-, and 3-simplices. The same header says the grown state
  contains no 2-cell data and that simplicial structure above dimension
  one enters only by declaration (`boundary_not_forced`). Those
  declarations were not inventoried here.
- `19L57G1:lean4/Derivation/FidelityClosure.lean::FidelityPath` is an
  inductive path on a `TranslationNetwork`, with reflexivity, symmetry,
  and transitivity constructors. It is not the Challenge 3 response
  language. No homotopy of those paths was found.
- `19L57G1:lean4/Derivation/Composing.lean` is one of the twelve parked
  modules. It is not an admission rule of `stepE`.

README claims checked and found, so not listed as missing: 75 Derivation
modules, the 63/12 split, 1530 axiom reports inside `{propext, Quot.sound}`,
140 `CL-*` headings, 60 `.py` files under `code/`, 40 JSON files in
`artifacts/`, and six gzip trees in `artifacts/full/`
(`closed_L`, `closed_F`, `tree_L_mu1`, `tree_L_mu2`, `tree_F_mu1`,
`tree_F_mu2`).

README claims with no matching declaration found: the 2026-09-19 test
census of 55 files and 787 collected tests (E180), and the unrechecked
`Classical.choice` measurement on four `ParkedAudit` apparatus definitions
(E181). `ci/check_lean_audit.py` only requires at least 40 reports
(`MIN_REPORTS = 40`); the integer 1530 is the artifact, not that constant.
