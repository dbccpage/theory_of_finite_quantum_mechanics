# Projection Obstruction pending-edits review

AuthorityEffect: None. AI-assisted review and repairs of the two remaining paper packages against base `374eb25de257097a7ca96dc4077cbbf769453cea`. The original dirty checkout was read and left intact. `source_inventory.json` records the input snapshot, including files deliberately replaced or omitted during review; it is not a manifest of the final branch.

## Findings and corrections

| Finding | Correction |
|---|---|
| The supplemental replay expected an absent dependency archive; a higher-cell build filename also disagreed with the runner. | Require an explicitly prepared Mathlib cache; verify compiler and eight clean dependency revisions. Remove the incomplete vendor scaffold. |
| Replay evidence could advertise incomplete theorem/axiom results. | Require all 20 named theorems exactly once, allow only three standard axioms, and bind proof, census, runner, dependency pins and report. Add drift, missing/duplicate/unknown/truncated/forbidden-axiom tests. |
| The saved axiom report included a platform-specific compiler banner, so a fresh Linux replay could disagree with a Windows receipt. | Compare the portable axiom output and retain the compiler banner as metadata; add a Windows-to-Linux banner regression. |
| The witness checker used assertions, which disappear under optimized Python. | Use explicit schema/type/domain validation and nonzero refusal; test both normal and optimized subprocesses. |
| The jump argument cited a nonexistent companion section. | Derive the finite correction-jump identity directly in PO-000 section 5.18 and point PO-034 to it, with contractivity and regularity premises explicit. |
| NUM1 was missing from the main producer/verifier claim inventories. | Add it to both independent inventories and keep its general analytic claim outside Python theorem certification; add a regression. |
| Imported edits regressed current names, a dependency pin and release metadata. | Preserve current repository naming and Tornado pin, compose the new ledger entries, update actual versions and retain original historical receipts. |
| A new historical census imported only a subset of the modules it queried. | Omit that invalid historical census; retain original historical evidence and use the complete supplemental census for the new statements. |
| The higher-cell fresh-replay runner still required Lean 4.34.1 while the package pinned 4.35.0. | Match the existing package pin and successfully replay its seven historical targets. |
| The main release scripts did not import under required isolated Python. | Resolve their own script directory explicitly; add subprocess import regressions from an unrelated working directory. |
| The optional Lean text scan treated an English comment containing "admit" as a proof hole. | Ignore line/nested block comments and string contents, retain actual proof-token rejection, and add six regressions. This remains a lexical check, not elaboration. |
| The public-reference regression demanded a private URL removed from the manuscript. | Check the exact historical revision and explicit private-source scope without requiring a private URL. |
| PDFs and current manifests no longer represented the sources; historical receipts could be read as current verification. | Rebuild both PDFs, fix the missing set-difference glyph, inspect title/new-section/final pages, refresh manifests and keep current review records separate. Update the portable-font regression to accept both the family name and the actual bundled Latin Modern filename. |

## Verification boundary

The 20 new Lean declarations prove conditional scalar and normed-carrier implications. Continuous evolution, trace-norm tensor/partial-trace facts and validated numerical error enclosures remain explicit inputs. No derivation-DAG node status changes. The main package's standalone profile deliberately excludes 11 native measurement integration tests. Its historical Lean modules were not all freshly compiled.

The higher-cell full gate includes its fresh seven-target Lean replay and native Jupyter execution. The dedicated CI runs both Python suites, optimized admission checks, recorded Lean receipt checks and payload integrity. CI does not describe receipt checks as fresh compilation.

Every changed Python/Lean file has an adjacent byte-bound contract with a conservative artifact score (L1D, L2D or L3D). These atlas imports are outside the governed top-level code/Lean population. A code-mutation campaign was not performed, and no L4 or system-wide certification is claimed.

PDFs were built with Pandoc 3.7.0.2 and Tectonic 0.17.0: main paper 74 pages, higher-cell paper 26 pages. Neither final build reported missing glyphs or overfull boxes. Package-local PDF receipts bind the manuscript, generated TeX and PDF. Historical evidence is preserved as history, not rewritten to imply it ran on the current sources.

Final command results and source bindings are recorded in `verification.json`.
