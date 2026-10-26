# Listed-history summary: a choice-free reconstruction (note)

**AuthorityEffect:** None. Proposal only. Written against `origin/main`
`8ac5da188390a93252614dfbb707f15d2c4fba42` (merge of #1152, 2026-10-17); the
prompt was written against `9ac0cd73d`. Every line number below was re-read at
`8ac5da188`.

## Statement

The deposit `pregenesis_to_minimal_symbol_systems` has a proof of the history–report
criterion (`lean4/Paper.lean:7-24`): an answer `σ : H → S` factors through a report
`π : H → V` on the report image exactly when `σ` is constant on the fibers of
`π`. Its existence direction opens `classical` and builds the factor from
`Classical.choose`. `paper.md:186-188` records this and says the finite
listed-history reconstruction lives in the Python and Rust companions only.
`03_results_and_arguments.md:115-122` states the listed version in prose.

The Lean file `../lean4/ListedHistorySummary.lean` mechanizes that prose. With
`hs : List H`, `report : H → V`, `answer : H → S`, `[DecidableEq V]`:

```lean
def recon (hs : List H) (report : H → V) (answer : H → S) (v : V) : Option S :=
  (hs.find? (fun h => decide (report h = v))).map answer
```

| Part | Theorem (namespace `PreMssnListed`) | Content |
| --- | --- | --- |
| 1 | `recon_of_fiberConstant` | fiber constancy on `hs` gives `recon (report h) = some (answer h)` for every listed `h` |
| 2 | `fiberConstant_of_recon` | the converse; `listed_history_report_criterion` packages 1 and 2 as an `↔` |
| 3 | `recon_eq_none_iff`, `recon_eq_none_of_off_image`, `off_image_of_recon_eq_none` | `recon v = none` exactly when no listed history reports `v` |
| 4 | `recon_unique` | any `f : V → Option S` returning every listed answer agrees with `recon` on every listed report |
| 5 | `listed_factor_exists` | with a complete listing, the deposit's left-hand side (a `factor : ReportImage report → S`) is built from `recon` and `Option.get`, with no choice axiom |

`ReportImage` is restated with the deposit's definition; the file imports nothing.

## Proof sketch

Two list lemmas, each by induction on `hs`: `find?_of_mem` (a listed element
satisfying `p` makes `find?` return a listed element satisfying `p`) and
`find?_eq_none_iff'` (`find?` is `none` exactly when no listed element
satisfies `p`). Part 1: the first match `h₀` has `report h₀ = report h`, so
fiber constancy gives `answer h₀ = answer h`. Part 2: equal reports give equal
`recon` values. Part 3 is `find?_eq_none_iff'` through `Option.map`. Part 4
needs no fiber-constancy hypothesis: `f (report h) = some (answer h) =
f (report h₀) = some (answer h₀)`, so `f` supplies it. Part 5: `v.property` is
a `Prop`, so it may be eliminated to prove the `Prop` `(recon v.val).isSome =
true`; `Option.get` extracts the value, and the factor equation is part 1.

Instance checks (`decide`): population `[0, 1, 2]`, report `h % 2`. With
answer `h % 2` fiber constancy holds and `recon` returns `some 0`, `some 1`,
and `none` at the off-image report `2`. With answer `h`, histories `0` and `2`
share report `0` with answers `0 ≠ 2`; `recon 0 = some 0 ≠ some 2` refutes
part 2's hypothesis at the pair `(0, 2)`.

## What was reused and what was checked as "not yet attempted"

- Deposit `lean4/Paper.lean:7-24` (classical `mpr`), `:26`
  (`history_factor_unique`); `lean4/Observation.lean:38` `task_descent_iff` is
  choice-free but quotient-valued. At `8ac5da188`, `grep -rn
  "find?\|firstMatch\|enumeration" lean4/*.lean` in the deposit finds only
  census and graph enumerations.
- WDP Appendix L.2 is now at `witnessed_difference_programme.md:9073-9081`
  (the prompt's 9024-9031 moved). Register row GEN-WDP-03
  (`genesis_bridge_register.md:14`) cites
  `ProposalAdmissionBridge.factorization_iff_fiber_constancy`, which is a Lean
  theorem, not Rust or Python
  (`witnessed_difference_programme/lean4/WitnessedDifference/ProposalAdmissionBridge.lean:27`):
  `FactorsOnImage ↔ FiberConstant` for arbitrary types, `mpr` also classical
  (lines 37-43). Rows O01, O02 (`:87-88`) are unrelated. Neither states a
  list-valued reconstruction.
- `genesis_primitives/primitives/lean4/` roots: no `report` or `ReportImage`;
  `pregenesis_empty_mark/` had no `lean4/` folder.

## What is not covered

- Unlisted or infinite populations. The deposit's classical theorem remains the
  statement there; this file replaces its `mpr` only when `∀ h, h ∈ hs`.
- The refusal policy off the image is `none`, nothing richer: no typed reason,
  no nearest report, no partial answer.
- Agreement with the Python and Rust companions is not checked here.

## Proposed deposit sentence (for Jeremy; no deposit file was edited)

`paper.md:186-188` currently reads "…the finite listed-history reconstruction
in the Python and Rust companions is constructive." Proposed: "…the finite
listed-history reconstruction in the Python and Rust companions is
constructive, and is mechanized for listed histories in
`education/pregenesis_empty_mark/lean4/ListedHistorySummary.lean`."
Adopting it changes `SHA256SUMS` and `MANIFEST.sha256`, which is a repin.

`genesis_bridge_register.md` is inside the WDP deposit (`SHA256SUMS`,
`MANIFEST.sha256`), so no row was appended; it has a row shape (`L`) a repin
could use.

## Receipts

Toolchains came from the GitHub release tarballs (`elan toolchain install`
failed through the proxy; `curl` fetched them, `elan toolchain link` installed
them). Cwd `pregenesis_empty_mark/lean4`; scope: the single file, every `example`, 8
`#print axioms` lines.

| command | tool version | exit |
| --- | --- | --- |
| `lean ListedHistorySummary.lean` | Lean 4.33.0, commit d8b18978322de05a8f3dba51ef03cf5461676c17 | 0 |
| `lean ListedHistorySummary.lean` | Lean 4.34.0, commit 293d5d0c0c3f3dded4688b3ccd6a33939ac5102b | 0 |
| `lake build` (scratch copy of the three files, Lean 4.33.0) | Lake of 4.33.0 | 0, "Build completed successfully (3 jobs)" |

`#print axioms` output, identical on both toolchains:

```
'PreMssnListed.recon_of_fiberConstant' does not depend on any axioms
'PreMssnListed.fiberConstant_of_recon' does not depend on any axioms
'PreMssnListed.listed_history_report_criterion' does not depend on any axioms
'PreMssnListed.recon_eq_none_iff' does not depend on any axioms
'PreMssnListed.recon_eq_none_of_off_image' does not depend on any axioms
'PreMssnListed.off_image_of_recon_eq_none' does not depend on any axioms
'PreMssnListed.recon_unique' does not depend on any axioms
'PreMssnListed.listed_factor_exists' does not depend on any axioms
```

Part 5 needed no `propext` (`rw` and `Option.get`, no `simp`). Jeremy's local
check on Windows, from `education/pregenesis_empty_mark/lean4`:

```
lean ListedHistorySummary.lean
```

## Compaction envelope

- **Supports:** the listed criterion as an `↔`, refusal off the image as `none`
  both ways, uniqueness on the listed image, and a choice-free factor for
  complete listings; axiom set empty for every theorem on Lean 4.33.0 and
  4.34.0.
- **Does not support:** anything about unlisted or infinite `H`; agreement
  with the Python and Rust companions; any richer refusal; any change to the
  deposit, whose classical theorem stands as written.
- **Narrowest defensible claim:** on a listed population with decidable report
  equality, first-match reconstruction returns every listed answer exactly when
  the answer is constant on the listed fibers, with no choice axiom.
- **Next test:** `lean ListedHistorySummary.lean` on Jeremy's machine; then
  decide whether to adopt the proposed `paper.md` sentence (a repin).
- **Git changeset:** branch `claude/pregenesis-constructive-summary-bff2sh` from
  `8ac5da188`; new `pregenesis_empty_mark/lean4/{ListedHistorySummary.lean,
  lakefile.lean, lake-manifest.json, lean-toolchain}`, new
  `pregenesis_empty_mark/docs/listed_history_summary_note.md`, one sentence appended to
  `pregenesis_empty_mark/03_results_and_arguments.md` after line 122; no deposit file
  touched.
