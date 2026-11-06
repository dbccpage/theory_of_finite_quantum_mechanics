> **Recovered file.** Source: `C:\.ana\coda_university\coda_research\authorization_an_incompleteness_theory\_support\authorization_incompleteness_dtm2_input_execution_red_team_dialogue_raw.md` (external, read-only).
> Recovery date: 2026-10-21. Recovered verbatim; statuses below are the source's, not audited.
> Audit and comparison with this repository: [RECOVERY_NOTES.md](../RECOVERY_NOTES.md).

---

# Authorization Incompleteness: DTM2 input-execution Stage-0 dialogue

**Date:** 2026-08-21

**Target:** *Authorization as an Incompleteness Boundary*, v0.14

**Target source hash:**
`f9c7d66b7ba173b0924df9b542fa44c1bc8997ae00fe55f2c00da4e659b01f19`

**Base revision:** `bcf932a5a1a636f687cbdd931c46d1084d5c61cb`

**Candidate surface:**
`formal/direct_turing_machine_input_execution_models.lean` (not yet
written)

**Imported seed hashes:**

- `formal/direct_turing_machine_models.lean`
  `0fb0e2bd0688bd926904235e3e666504b82ab45d4a72f7d53e3ddfcec46402c9`
- `formal/direct_turing_machine_token_code_models.lean`
  `6d3aecf402c15951b53eccf49e1609180346bac425496f3cd85264e6ba527153`

**AuthorityEffect:** None.

## Independence and carrier freeze

This is a producer-side Stage-0 scope dialogue, not an independent I3
review receipt. It freezes the v0.14 paper, DTM0, and DTM1 before a
new input-request module, Lake-root change, claim binding, or prose update
is made.

The frozen PO-000 source is not a target of this packet. Its recorded
SHA-256 is
`fb7d2436f1e5da5969c8c4d9b1a143b4a2a0ba8024748568733f4290414d701e`.

## Round 1: What does an input word encode?

**Red DTM2-R1.** DTM0 configurations contain a total tape over all
integers. A finite `List Nat` cannot encode every such tape. Calling a
finite input word a general configuration encoding would erase the
infinite-carrier boundary.

**Blue.** Conceded. DTM2 will encode only an initial finite input word.
Its declared materialization starts in state `0` with head position `0`
and a tape that is blank outside the word's nonnegative positions. It
does not encode arbitrary DTM0 configurations or arbitrary total tapes.

**Green.** Carry forward. Name the carrier *initial input request*, not
configuration code. Reserve arbitrary finite configuration snapshots for a
later lift with its own carrier and loss accounting.

## Round 2: Is the request grammar framed and all-consuming?

**Red DTM2-R2.** Concatenating a machine code and an input code without a
declared boundary creates ambiguous parsing. A decoder that ignores a
suffix could execute something other than the proposal presented.

**Blue.** Conceded. One request will contain a fuel token, a machine-code
length token, the complete DTM1 machine segment, and the whole input-word
suffix. The decoder will reject a missing header, a declared machine length
that overruns the payload, an invalid machine segment, and an invalid input
symbol. It will consume every token in an accepted request.

**Green.** Carry forward. The implementation must prove a decoder-after-
encoder theorem for every declared finite request and include closed
malformed-request fixtures.

## Round 3: What does execution agreement mean here?

**Red DTM2-R3.** If a request contains a machine and input word, then
DTM2 must already encode every DTM0 configuration and every execution
trace; otherwise no execution agreement is possible.

**Blue.** Rebutted. The proposed agreement is narrower: the code-level
evaluator first decodes one declared initial request, materializes its
initial configuration, and calls DTM0's existing fuel-bounded evaluator.
The theorem compares those two results for encoded requests. It neither
serializes intermediate configurations nor proves step-by-step trace
correspondence.

**Green.** Red's necessity claim is false. A result-level agreement for a
declared initial-request boundary is meaningful and can be mechanized
without claiming a general configuration or trace grammar. Carry the
narrow result; do not add a configuration-completeness obligation to this
packet.

## Round 4: Does a finite request make the carrier universal?

**Red DTM2-R4.** A finite machine/input/fuel request can be described as a
program runner. That may be used to imply a universal machine,
Turing-completeness, Rice's theorem, a halting decider, or progress on P
versus NP.

**Blue.** Conceded. DTM2 only parses declared finite requests and invokes
the existing fuel-bounded evaluator. It gives no universal simulation,
unbounded execution, extensional property, nontriviality witnesses, or
effective reduction.

**Green.** Carry forward. The carrier inventory must remain partial and
must not select DTM0/DTM2 as the global-computability carrier.

## Round 5: Does parsed execution authorize or replay a proposal?

**Red DTM2-R5.** A successful parse and a deterministic bounded result
could be called a replayed authorization, especially when the proposal
source supplies both request and evaluator code.

**Blue.** Conceded. The result is only `Option StepResult` under declared
Lean definitions. It has no source-byte format, hash binding, custody,
independent trust root, semantic contract, or terminal-policy selection.
PO-000, AIT-G3, AIT-G4, and AIT-G5c remain separate boundaries.

**Green.** Carry forward. No DTM2 prose may call the parser or evaluator
an authority, a replay receipt, or a terminalizer.

## Findings carried into the update packet

<!-- markdownlint-disable MD013 -->
| Finding | Required disposition |
| --- | --- |
| DTM2-R1 | Encode only finite initial input words; record the total-tape and arbitrary-configuration limits. |
| DTM2-R2 | Use an explicit length-delimited request grammar, all-consuming decoder, round trip, and malformed fixtures. |
| DTM2-R4 | Preserve the open universality, extensionality, nontriviality, and reduction fields. |
| DTM2-R5 | Preserve the P0, replay, custody, policy, and authorization nonclaims. |
<!-- markdownlint-enable MD013 -->

## Findings not carried forward

DTM2-R3's claim that no result-level execution agreement is possible
without a general configuration/trace grammar is not carried forward.
The rejected claim would impose a stronger carrier than the proposed
initial-request theorem needs. Its rejected status does not close the
separate later configuration-snapshot and trace-agreement obligations.

**Concession rate:** four carried Red findings out of five opened
findings (`0.8`); DTM2-R3 was rebutted and rejected by Green.

**AuthorityEffect:** None.
