# Completion supplement: exact diagnostics after repository migration

**AuthorityEffect: None.**


> **Historical record (2026-09-25).** The paths in this note describe an
> earlier layout. The deposit now sits at
> `sources/atlas/papers/mub6` in the source monorepo.
> Current replay commands are in [the README](README.md) and section 6 of
> [the paper](papers/paper.md).

The Python research modules live at [`code/mub_verify`](code/mub_verify)
(moved from the retired `omega_engine/crates/mub_verify` on 2026-09-25).
The Rust engines live in the source monorepo at
`omega_engine/crates_rs/omega_mub`; they are not part of this deposit.

## Completed repair and focused replay

The Q-soundness zero-float source test previously inspected a nonexistent
paper-local path. It now reads the imported module's `__file__`, so the audit
examines the code actually executed after migration. The mathematical checks
are unchanged. The completion receipt of that date (not shipped in this
deposit) covered:

- Exact cyclotomic arithmetic and its tested identities.
- Fixed-candidate Q-soundness obligations, rational rank/LDL calculations,
  polynomial-identity checks, and negative controls for unsupported scope.
- Packet-firewall acceptance and refusal behavior.

The 2026-09-25 command named test files under `tests/mub_verify/`, which this
deposit no longer ships. The current deposit suite runs from this directory:

```powershell
py -3.12 -m pytest tests -q -p no:cacheprovider
```

The central runner supplies a fresh temporary directory per replay. It does not
rebuild the full Rust/Lean estate or certify every historical receipt.

## How this binds to the Symbol Game

A fixed matrix and its exact LDL witness play the role of a declared carrier and
witness. A polynomial identity has an explicit coefficient ring and input
polynomials. Neither checked result silently quantifies over every MUB candidate.
That additional quantifier needs representation, coverage, and overlap arguments.

The [gap registry](research/mub6_gap_registry.json) and the paper state the
remaining obligations. Status lines in older research files that call Route C
"unconditional" are withdrawn; see the
[superseded notice](research/superseded_notice.md). In particular, synthetic matrix diagnostics need a bridge from every
candidate into the checked matrix model, and local cover data need complete
coverage and relative-interior overlap arguments. Digest agreement establishes
byte identity; it cannot fill either gap. This is the same scope discipline used
for a finite sign graph in Paper 002 and a route-specific oracle in Paper 003.
