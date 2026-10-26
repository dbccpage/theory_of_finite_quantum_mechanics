# Supply erasure at the replay level (Genesis, genesis_primitives)

**AuthorityEffect:** None. Proposal only.

Sources: `dbccpage/the_symbol_game` `origin/main` at `8ac5da188390a93252614dfbb707f15d2c4fba42`
(prompt written against `9ac0cd73d`; nothing cited moved); `dbccpage/19L57G1` at
`f1d56c010e6ba10a3b9418bd7cc5953c067250f2` (`sealed-derivation-v1`), read only.

## Statement

With `isSupply : Event → Bool` true exactly on `.supply _` and `notSupply e := !isSupply e`,
for every `h : List Event` and `base : Regime`:

```
replayE (h.filter notSupply) base = replayE h base      -- replayE_filter_supply
```

Corollaries in the same file: `replayE_cons_supply` (a leading supply is erasable),
`replayE_supply_only` (`replayE (ts.map Event.supply) base = some base`), and
`replayE_eq_of_filter_eq` (equal non-supply subsequences replay to the same regime:
presentations may be inserted or deleted anywhere without changing what is admitted).
Optional part, closed: `stepE r e = some r' → stepE r' e = some r'` for `admitInst`,
`admitRuleAll`, `impose` (`stepE_*_idem`), and witnesses that `admitDatum` and `admitForm`
are not idempotent (`stepE_admitDatum_not_idem`, `stepE_admitForm_not_idem`, by `decide`).

## Definitions

Copied byte for byte from 19L57G1 `lean4/Derivation/Basic.lean` into namespace `GenesisCopy`
of `primitives/lean4/SupplyErasure.lean`: `Inst` line 21, `insertNew` 25 to 26, `Regime` 53 to 59,
`Event` 134 to 141, `stepE` 145 to 162, `replayE` 166 to 167. The prompt's line numbers were
off by one or two against the pinned file; the diff receipt below checks these.
`supply_no_op` (`Inertia.lean` line 17) is re-proved by `rfl`. `replayE_append` (line 83) was
not needed: `replayE_cons` is `rfl`, since `List.foldlM` on `Option` unfolds to `Option.bind`.

## Proof

Induction on `h`, generalizing `base`. Nil: `rfl`. Cons `e :: rest`: case on `e`. For
`supply t` the filter drops the head by definitional unfolding (`show`), `replayE_cons_supply`
reduces the right side, and the hypothesis closes. For the five admissions the filter keeps the
head (`rfl`), `replayE_cons` rewrites both sides to `(stepE base e).bind …`, and a case split on
`stepE base e` gives `none = none` or the hypothesis at the new regime
(`replayE_filter_cons_keep`). The invariance corollary is three rewrites with the main theorem.

Idempotence: `dsimp only [stepE]` exposes the guard, `split at hs` and `cases hs` identify `r'`
with the guarded update, the guard still holds at `r'` (the update touches neither `forms` nor
`data`), and `insertNew_insertNew` collapses the second insertion; it rests on
`mem_insertNew_self`, proved from a hand induction `mem_append_singleton`. No `simp`, `if_pos`,
`by_cases` or `BEq` lemma is used.

## Axiom report and residual

Both toolchains elaborate the file with exit 0 and no `sorry`. The prompt expected an empty set.
Every theorem whose statement mentions `insertNew`, `stepE` or `replayE` prints `[propext]`;
`mem_append_singleton` prints none. The file prints why: `GenesisCopy.insertNew`,
`GenesisCopy.stepE`, `List.instDecidableMemOfLawfulBEq` and `List.getD` each depend on
`propext`. `#print axioms` closes over the statement's constants, and core Lean's proofs of decidable
list membership (the `a ∈ l` in `insertNew`) and of `List.getD` (in `stepE`) use `propext`.
Genesis records the same for its own theorem: 19L57G1 `artifacts/lean_axioms.txt` line 1 is
`'Derivation.supply_no_op' depends on axioms: [propext]`. The proofs add nothing beyond what
the definitions carry; `Quot.sound` and `Classical.choice` are absent.

```
RESIDUAL
  kind: DefinitionMismatch
  statement: #print axioms of replayE_filter_supply and its three corollaries is empty
  where_it_breaks: the copied insertNew and stepE depend on propext through core Lean, so the statement's closure is never empty
  what_is_proved: every theorem above with #print axioms = [propext]; mem_append_singleton with none
  narrowest_defensible_claim: replayE (h.filter notSupply) base = replayE h base for all h, base, with exactly the axiom set Genesis records for supply_no_op
  next_test: lean education/genesis_primitives/primitives/lean4/SupplyErasure.lean
```

## Scope and prior art

The theorem is about the Lean `replayE`; the Python `replay` in 19L57G1 `code/derivation/model.py`
is not covered. `primitives/code/tests/test_supply_erasure.py` checks the identity, the
supply-only case and interleaving on this repository's Python copy (`seed_and_regime.py`) over
20 seeded histories of 40 events: evidence for those histories only.

Re-run at `f1d56c01`: `grep -rn "filter\|erase" lean4/Derivation/*.lean` finds `Erasure.lean`
(`erase_step`, `erase_replay`: a token-erasure simulation `TRegime` to `Regime`, a different
statement that leans on supply being inert), `Bridge.lean` `order_erased_at_object_level`, and
prose; no filter identity, no ledger row. `genesis_primitives/primitives/lean4/` has an unrelated
`Event` in `DerivationEngine.lean` and no `stepE` or `replayE`.

## Receipts

- `lean SupplyErasure.lean`, Lean 4.34.0 (x86_64-unknown-linux-gnu, commit 293d5d0c), exit 0,
  scope: the one file, no imports:

```
'GenesisPrimitives.SupplyErasure.supply_no_op' depends on axioms: [propext]
'GenesisPrimitives.SupplyErasure.replayE_cons' depends on axioms: [propext]
'GenesisPrimitives.SupplyErasure.replayE_nil' depends on axioms: [propext]
'GenesisPrimitives.SupplyErasure.replayE_cons_supply' depends on axioms: [propext]
'GenesisPrimitives.SupplyErasure.replayE_filter_cons_keep' depends on axioms: [propext]
'GenesisPrimitives.SupplyErasure.replayE_filter_supply' depends on axioms: [propext]
'GenesisPrimitives.SupplyErasure.replayE_filter_not_isSupply' depends on axioms: [propext]
'GenesisPrimitives.SupplyErasure.replayE_supply_only' depends on axioms: [propext]
'GenesisPrimitives.SupplyErasure.replayE_eq_of_filter_eq' depends on axioms: [propext]
'GenesisPrimitives.SupplyErasure.mem_append_singleton' does not depend on any axioms
'GenesisPrimitives.SupplyErasure.mem_insertNew_self' depends on axioms: [propext]
'GenesisPrimitives.SupplyErasure.insertNew_insertNew' depends on axioms: [propext]
'GenesisPrimitives.SupplyErasure.stepE_admitInst_idem' depends on axioms: [propext]
'GenesisPrimitives.SupplyErasure.stepE_admitRuleAll_idem' depends on axioms: [propext]
'GenesisPrimitives.SupplyErasure.stepE_impose_idem' depends on axioms: [propext]
'GenesisPrimitives.SupplyErasure.stepE_admitDatum_not_idem' depends on axioms: [propext]
'GenesisPrimitives.SupplyErasure.stepE_admitForm_not_idem' depends on axioms: [propext]
'GenesisCopy.insertNew' depends on axioms: [propext]
'GenesisCopy.stepE' depends on axioms: [propext]
'GenesisCopy.replayE' depends on axioms: [propext]
'List.instDecidableMemOfLawfulBEq' depends on axioms: [propext]
'List.getD' depends on axioms: [propext]
```

- Same command, Lean 4.33.0 (commit d8b18978): exit 0, byte-identical output. Both toolchains
  came from the GitHub release tarballs; the elan host is blocked in the container.
- Copy identity (bash, from `genesis_primitives`, 19L57G1 checked out beside this repository), GNU diff, exit 0:

```
diff <(sed -n '21p;25,26p;53,59p;134,141p;145,162p;166,167p' ../../../../19L57G1/lean4/Derivation/Basic.lean) \
     <(sed -n '/^-- BEGIN COPY/,/^-- END COPY/p' primitives/lean4/SupplyErasure.lean | sed '1d;$d' | grep -v '^$')
```

- `python -m pytest .../primitives/code/tests/test_supply_erasure.py -q`: pytest 9.1.1,
  Python 3.13.16, exit 0, 4 passed; `ruff check` 0.16.8 on the test, exit 0.
- Forbidden-word scan over the new files: no hit. `source_crosswalk.md` line 82 carries a
  pre-existing word from the forbidden list, left as is (append-only file).

## Compaction envelope

- Supports: replay-level supply erasure and three corollaries over byte-identical Genesis
  definitions, on two toolchains; idempotence of the three `insertNew` admissions;
  non-idempotence of `admitDatum`, `admitForm`.
- Does not support: an empty axiom set; anything about 19L57G1's Python `model.py`; any
  change to `genesis.md` or a hypothesis H-10.
- Narrowest claim: for the Lean `replayE`, inserting or deleting supplies anywhere in a
  history leaves the replayed regime unchanged.
- Next test: `lean education/genesis_primitives/primitives/lean4/SupplyErasure.lean`.
- Changeset: branch `claude/genesis-supply-erasure-uwmfwi` from `main` `8ac5da188`; new
  `primitives/lean4/SupplyErasure.lean`, `docs/supply_erasure_note.md`,
  `primitives/code/tests/test_supply_erasure.py`; appended one root to
  `primitives/lean4/lakefile.lean` (previous last root gained its comma) and one section to
  `source_crosswalk.md`.
