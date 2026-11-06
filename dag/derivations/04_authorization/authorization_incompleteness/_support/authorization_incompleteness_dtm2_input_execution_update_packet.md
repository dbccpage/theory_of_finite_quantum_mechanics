> **Recovered file.** Source: `C:\.ana\coda_university\coda_research\authorization_an_incompleteness_theory\_support\authorization_incompleteness_dtm2_input_execution_update_packet.md` (external, read-only).
> Recovery date: 2026-10-21. Recovered verbatim; statuses below are the source's, not audited.
> Audit and comparison with this repository: [RECOVERY_NOTES.md](../RECOVERY_NOTES.md).

---

# Authorization Incompleteness: DTM2 input-execution update packet

**Date:** 2026-08-21

**Paper target:** *Authorization as an Incompleteness Boundary*, v0.14

**Frozen paper hash:**
`f9c7d66b7ba173b0924df9b542fa44c1bc8997ae00fe55f2c00da4e659b01f19`

**Base revision:** `bcf932a5a1a636f687cbdd931c46d1084d5c61cb`

**Raw dialogue:**
`authorization_incompleteness_dtm2_input_execution_red_team_dialogue_raw.md`

**Status:** producer-side implementation plan; not an independent review
or authority-bearing receipt.

**AuthorityEffect:** None.

## 1. Accepted corrections

1. Add `formal/direct_turing_machine_input_execution_models.lean`,
   importing DTM0 and DTM1.
2. Define a finite initial-input word, its total-tape materialization, and
   an initial configuration fixed at state `0` and head position `0`.
3. Define one finite request grammar containing fuel, a declared DTM1
   machine-code length, one complete machine-code segment, and a complete
   input-word suffix.
4. Define a total encoder and partial all-consuming decoder for the
   request. Reject missing headers, length overruns, invalid machine
   segments, and invalid input-symbol tags.
5. Define a code-level bounded evaluator only by decoding a request and
   invoking DTM0's existing `execute` on its declared initial input.
6. Prove request decoder-after-encoder recovery and the named
   result-level invariant: encoded requests execute to the same
   `StepResult` as DTM0's declared fuel-bounded evaluator.
7. Add AIT-DTM2 as a narrow predecessor in the proof graph, claim ledger,
   carrier inventory, formal binding manifest, and prospectus. Keep
   AIT-G5b open and partial.

## 2. Withdrawn or forbidden claims

- Do not call an initial input word an encoding of every DTM0
  configuration or total tape.
- Do not claim intermediate configuration serialization, step-by-step
  trace agreement, source bytes, UTF-8, a deployed parser, or a runtime
  evaluator.
- Do not claim universality, Turing completeness, a universal machine,
  a halting result, Rice's theorem, Godel's theorem, an LLM reduction, or
  anything about P versus NP.
- Do not treat a successful parse or a returned `StepResult` as replay
  custody, hash binding, semantic adequacy, authorization, or terminal
  policy selection.
- Do not modify Paper 0.

## 3. Open obligations

1. Define a separately typed finite configuration-snapshot grammar.
2. Prove step-by-step bounded trace agreement after that grammar exists.
3. Bind actual source bytes, parser implementation, evaluator, toolchain,
   and replay command before asserting byte-level replay.
4. State and prove or audit a universality theorem for an admitted carrier.
5. Select a nontrivial extensional property, positive/negative witnesses,
   decision class, and effective reduction for AIT-G5.
6. Model the LLM-only corollary only after the preceding computability
   carrier and reduction are established.

## 4. Lean targets

- `formal/direct_turing_machine_input_execution_models.lean`
  - `decodeInputWord_encodeInputWord`
  - `decodeRunRequest_encodeRunRequest`
  - `executeRunRequestCode_encodeRunRequest`
  - `missing_request_header_is_rejected`
  - `machine_length_overrun_is_rejected`
  - `invalid_input_symbol_is_rejected`
  - `invalid_machine_segment_is_rejected`

The target must build through `AuthorizationIncompletenessTheory` and
record declaration-level axiom reports. Expected proof ceiling: no
`sorry` or `admit`, a finite initial-input request grammar only, and no
claim that it supplies a general configuration/trace or universal-machine
proof.

## 5. Nonclaims to preserve

- Turing's account of effective procedure is not refuted.
- P versus NP is not defined, attacked, or resolved.
- The existing DTM0 evaluator remains fuel-bounded.
- DTM2 has no general configuration or trace serialization theorem.
- An LLM has not been formally reduced to an admitted program carrier.
- Evaluation and authorization need not be physically separate; DTM2 has
  no physical or custodial model at all.
- P0's report-fiber condition, bounded-packet replay assumptions, and
  terminal-policy separation remain independent obligations.

## 6. Implementation order

1. Add this Stage-0 packet and frozen-carrier dialogue.
2. Add the DTM2 finite input-request Lean module and register it in the
   named Lake target.
3. Build the target, scan for `sorry`/`admit`, inspect every named
   theorem's axiom report, and kill each required fixture by mutation.
4. Add the DTM2 claim, proof-program node, machine-readable dependency,
   candidate-inventory ceiling, formal README, and binding-manifest entry.
5. Update the paper only with the exact finite request theorem and its
   unchanged global scope fence.
6. Recompute hashes, run target/replay/candidate tests, lint modified
   documents, and request independent review before status promotion.

## 7. Findings not carried forward

The packet does not require a general configuration grammar or
step-by-step trace agreement as a precondition for the DTM2 result-level
invariant. Those are later obligations, not completed work. It carries no
claim about semantic authorization, independent custody, physical
separation, or the LLM conclusion.

**AuthorityEffect:** None.
