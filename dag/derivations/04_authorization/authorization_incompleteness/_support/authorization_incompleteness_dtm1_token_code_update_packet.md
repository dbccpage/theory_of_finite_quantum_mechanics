> **Recovered file.** Source: `C:\.ana\coda_university\coda_research\authorization_an_incompleteness_theory\_support\authorization_incompleteness_dtm1_token_code_update_packet.md` (external, read-only).
> Recovery date: 2026-10-21. Recovered verbatim; statuses below are the source's, not audited.
> Audit and comparison with this repository: [RECOVERY_NOTES.md](../RECOVERY_NOTES.md).

---

# Authorization Incompleteness: DTM1 token-code update packet

**Date:** 2026-08-20

**Paper target:** *Authorization as an Incompleteness Boundary*, v0.13

**Frozen paper hash:**
`e5433420a3689d06499c155225d903d32cd0e87d8bad1bcd30a949653dd4b800`

**Base revision:** `97e881fab940f9432f2677cb9b278f1b8e041828`

**Raw dialogue:**
`authorization_incompleteness_dtm1_token_code_red_team_dialogue_raw.md`

**Status:** producer-side implementation plan; not an independent review
or authority-bearing receipt.

**AuthorityEffect:** None.

## 1. Accepted corrections

1. Add `formal/direct_turing_machine_token_code_models.lean`, importing
   the existing DTM0 finite-rule machine source.
2. Define an explicit finite token grammar: one halt-state token followed
   by complete five-token frames for state, scanned symbol, next state,
   written symbol, and movement.
3. Define total encoders and partial decoders for symbols, movements,
   rules, and machines. The machine decoder must consume all tokens.
4. Prove the decoder-after-encoder round trip for every DTM0 `Machine`.
5. Include closed empty-header, truncated-frame, and invalid-tag rejection
   fixtures.
6. Add AIT-DTM1 as a narrow syntax predecessor in the proof graph, claim
   ledger, formal binding manifest, source inventory, and prospectus,
   while retaining every AIT-G5b field as open or partial.

## 2. Withdrawn or forbidden claims

- Do not call the finite token code a byte encoding, source-file parser,
  UTF-8 format, or deployed parser.
- Do not claim configuration/input encoding, parser-to-execution
  correspondence, exact trace agreement, or an unbounded evaluator.
- Do not claim universality, Turing completeness, a universal machine,
  a halting result, Rice's theorem, Godel's theorem, an LLM reduction, or
  anything about P versus NP.
- Do not treat deterministic parsing as replay custody, hash binding,
  semantic adequacy, authorization, or terminal-policy selection.
- Do not modify Paper 0.

## 3. Open obligations

1. Encode configurations and inputs through a separately declared grammar.
2. Prove exact bounded execution/trace agreement between parsed code and
   DTM0 operational semantics.
3. Bind an actual source-byte format, parser implementation, evaluator,
   toolchain, and replay command if a byte-level claim is wanted.
4. State and prove or audit a universality theorem for an admitted carrier.
5. Select a nontrivial extensional property, witnesses, decision class,
   and effective reduction for AIT-G5.
6. Model the LLM-only corollary only after the preceding computability
   carrier and reduction are established.

## 4. Lean targets

- `formal/direct_turing_machine_token_code_models.lean`
  - `decodeTapeSymbol_encodeTapeSymbol`
  - `decodeMove_encodeMove`
  - `decodeRules_encodeRules`
  - `decodeMachine_encodeMachine`
  - `empty_machine_code_is_rejected`
  - `truncated_rule_code_is_rejected`
  - `invalid_symbol_tag_is_rejected`
  - `invalid_move_tag_is_rejected`

The target must build through `AuthorizationIncompletenessTheory` and
record exact declaration-level axiom reports. Expected proof ceiling:
no `sorry` or `admit`, a finite token grammar only, and no claim that the
grammar already supplies a byte format or a universal-machine proof.

## 5. Nonclaims to preserve

- Turing's account of effective procedure is not refuted.
- P versus NP is not defined, attacked, or resolved.
- The existing finite DTM0 evaluator remains fuel-bounded.
- An LLM has not been formally reduced to an admitted program carrier.
- Evaluation and authorization need not be physically separate; DTM1 has
  no physical or custodial model at all.
- P0's report-fiber condition, bounded-packet replay assumptions, and
  terminal-policy separation remain independent obligations.

## 6. Implementation order

1. Add the Stage-0 packet and frozen-carrier dialogue.
2. Add the finite token-code Lean module and register it in the named
   Lake target.
3. Build the target, scan for `sorry`/`admit`, and inspect each named
   theorem's axiom report.
4. Add the DTM1 claim, proof-program node, machine-readable dependency,
   candidate-inventory ceiling, formal README, and binding-manifest entry.
5. Update the paper only with the exact finite grammar theorem and its
   unchanged global scope fence.
6. Recompute hashes, run target/replay/candidate tests, lint modified
   documents, and request independent review before any status promotion.

## 7. Findings not carried forward

The packet carries no claim that a finite token grammar is already a
universal or byte-level proposal carrier. It carries no claim about
semantic authorization, independent custody, physical separation, or
the LLM conclusion. Those surfaces remain separately open.

**AuthorityEffect:** None.
