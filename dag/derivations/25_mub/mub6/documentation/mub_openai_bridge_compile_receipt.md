# Compile receipt: `lean4/MubOpenAIBridge.lean`

> **AuthorityEffect**: None. Dated 2026-10-21. Companion of `openai_mub6_le5_external_import.md`.

| Field | Value |
|---|---|
| File | `lean4/MubOpenAIBridge.lean` (not a lake root; not in the default target) |
| File SHA-256 | `b1e325ed5a5ade354736155489d05860d51d8ec2c453b0efe424493b020e12e1` |
| Toolchain | Lean (version 4.35.0, x86_64-w64-windows-gnu, commit eb6cafb7290e8bd5f2937522d8d804f58f02bafc, Release) |
| Mathlib | `56a005855ea17e0b0958f73ec801ae140b0a1679` (tag v4.35.0, as in `lean4/lake-manifest.json`; the shared cache `C:\lq\l4\.lake` has this HEAD) |
| Command | `lean -o <scratch>/MubOpenAIBridge.olean MubOpenAIBridge.lean` run in `lean4/` with `LEAN_PATH` = the cache's package libs plus a scratch directory holding the oleans of the two repo modules it imports (`Conjecture2GeneralMechanization`, `MubMonomialTransport`, compiled the same way). No `lake build`. |
| Exit code | 0 |
| Warnings | none; no `sorry` warning; no `sorry`, `axiom` or `native_decide` in the file |

The file does not import OpenAI's repository. The upstream model definitions it needs (`Coord`, `Space`,
`Basis`, `IsMUBFamily`, `Attainable`, `taoExponent`) are restated in `MUB.OpenAIBridge.OAIModel`, as in
upstream `Model.lean` at commit `1581d4cbdd69a0faf34b2089614fe2a814316a6a`. The upstream bound
`OAI.MUB6.family_size_le_five` is the hypothesis `OpenAIFamilyBound`; it is not proved here.

## Full compile output

```
'MUB.OpenAIBridge.mub6_family_le_five' depends on axioms: [propext, Classical.choice, Quot.sound]
'MUB.OpenAIBridge.mub6_card_le_five' depends on axioms: [propext, Classical.choice, Quot.sound]
'MUB.OpenAIBridge.attainable_iff' depends on axioms: [propext, Classical.choice, Quot.sound]
'MUB.OpenAIBridge.rawMU_iff_pairMU' depends on axioms: [propext, Classical.choice, Quot.sound]
'MUB.OpenAIBridge.tao_phase_bridge' depends on axioms: [propext, Classical.choice, Quot.sound]
```

An earlier run of the same file (before an unused `simp` fallback was removed from `tao_phase_bridge`)
printed the same five axiom lines plus one "this tactic is never executed" linter warning; the fallback was
deleted and the run above is clean.

## What is and is not proved

- Proved (kernel-checked): `attainable_iff` (OpenAI's `Attainable n` iff an `n`-member pairwise-MU family of
  unitary `6 x 6` matrices), `rawMU_iff_pairMU`, `tao_phase_bridge`, and the conditional statements
  `mub6_family_le_five` and `mub6_card_le_five`, whose hypothesis is `OpenAIFamilyBound`.
- Not proved here: `OpenAIFamilyBound` itself (OpenAI's `family_size_le_five`; external, not vendored, not
  replayed). So N(6) <= 5 is **not** established inside this repository; the DAG node
  `MUB6-OPENAI-FAMILY-LE-FIVE` stays `IMPORTED_ASSUMPTION`.
- Not done: the entry-level complex bridge for `tao`, and the step "raw quartet gives an OpenAI family of size 4".
- Caveat: the definitions of `OAIModel` are a restatement, checked by eye against upstream `Model.lean`, not
  by the compiler against upstream.
