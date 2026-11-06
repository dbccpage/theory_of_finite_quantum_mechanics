# Mode 01: Hieroglyphics & Wire Representations

**Mode ID:** 1  
**Cluster:** Cluster I: Carrier & Representation  
**AuthorityEffect:** None  

## Overview

Mode 01 enforces an operational prose restriction: all prompt, state, and transition expressions must conform strictly to a declared glyph profile or grammar contract without supplementary explanatory prose. Alphabet restriction alone does not prove absence of semantic meaning; rather, it provides a machine-checked syntactic envelope.

## Integration with Prompt Subsystem & Dialect Inventory

Drawing from the retired PFP demo_001 round 1 wire file (deleted in PR #568) and the Component Reuse ADR (`adr_reuse_decision.md`), Mode 01 supports multiple distinct wire dialects, each with its own declared terminal alphabet, grammar, and layout policy:

### 1. Distinct Wire Dialects (Tiers H and D)

Tier H and Tier D are distinct operational dialects whose terminal inventories extend beyond the 38-glyph base $\Gamma_{38}$ by incorporating uppercase Latin letters, whitespace, underscores, commas, and punctuation symbols. They are governed by separate explicit contracts and must not be identified with `mss-boundary-v1`.

- **Tier H (Head-word notation):** Structured head-word packets over an extended alphabet $\Sigma_H = \Gamma_{38} \cup \{\text{whitespace}, \text{newline}, ',', '=', '+', '*', '-'\}$:
  ```text
  int<
    var<x>
    dom<type<int>, min<0>, max<10>>
    carrier<undeclared>
    measure<undeclared>
    need<carrier, measure, terminal_rule>
  >
  ```
  *Contract:* Head-words specify application signatures; whitespace and linebreaks provide layout boundaries; commas separate argument slots.

- **Tier D (PFP Directives):** Directive assertions carrying formal role bindings over $\Sigma_D = \Gamma_{38} \cup \{\text{A-Z}, \text{whitespace}, '\_', '<', '>'\}$:
  ```text
  <assume p1 <op_int>>
  <assume p2 <var_x>>
  <assume p3 <bound_int_0_10>>
  <check carrier_declared>
  <refusal ERR_UNDECLARED_CARRIER>
  ```
  *Contract:* Space-delimited command verbs and identifiers inside balanced brackets; uppercase error tokens denote typed refusal outcomes.

### 2. The `mss-boundary-v1` Dialect

Pair-balanced boundaries belong specifically to the `mss-boundary-v1` dialect; they are not a universal axiom of MSS-N (unwrapped paths like `a>b>c` or `a0>b2>c1>a0` remain valid in raw or path profiles).

- **Substrate:** Single-root pair-balanced boundary wire syntax:
  ```text
  <<p><v1><<q><s0>><<c><s1>><<c><s2>><<u><s3>>>>
  ```
- **External Codebook & Legend:**
  - Role tokens: `p` (prompt), `v1` (version 1), `q` (task), `c` (constraint), `d` (context), `o` (output), `u` (unresolved).
  - External JSON legend binds slot tokens `s0, s1, ...` to slices.
  - **Source-Byte vs. AST Recovery:** Distinguish lossless AST reconstruction from exact source-byte recovery. Lossless source recovery requires an explicitly defined inverse mapping that tracks whitespace layout, token order, and non-canonical formatting. AST recovery reconstructs parsed node hierarchies without preserving superficial layout gaps.
- **Cost Accounting:** Token overhead for the codebook and legend must be measured under the actual tokenizer (e.g. byte-level BPE) and amortization assumptions across multi-turn sessions.
