# Lean 4 WDP Presentation & Parity Verification Kernel

**AuthorityEffect:** None. GenesisEffect: None.

Mechanized Lean 4 inductive definitions, wire serializers, and deterministic parser for the Witnessed Difference Programme (WDP) grammar declared in [`../grammar/wdp.ebnf`](../grammar/wdp.ebnf).

## 1. Module Structure

- **[`WdpSyntax.lean`](WdpSyntax.lean):** Constructive, Mathlib-free inductive data structures representing Sigma36 glyphs, words, difference items, transport events, quotient witnesses, balance matrices, and typed refusal codes.
- **[`WdpParser.lean`](WdpParser.lean):** Total deterministic parser `parseWdp? : String → Option WdpStatement` with constructive round-trip parity guarantees.
- **[`Main.lean`](Main.lean):** Executable CLI harness `wdp_parity_check` enabling bidirectional cross-language conformance testing against Python.

## 2. Compilation & Verification

To compile the package and executable:
```bash
lake build
```

To run the parity CLI directly:
```bash
.lake/build/bin/wdp_parity_check "<a!=b>" "witness<fiber:w1,status:EXACT_REPAIR>"
```

To run cross-language parity tests from Python:
```bash
py -3.12 -m pytest ../code/tests/test_wdp_lean4_parity.py
```
