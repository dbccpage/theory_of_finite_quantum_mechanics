> **Recovered file.** Source: `C:\.ana\coda_university\coda_research\authorization_an_incompleteness_theory\_support\authorization_incompleteness_dtm1_token_code_red_team_dialogue_raw.md` (external, read-only).
> Recovery date: 2026-10-21. Recovered verbatim; statuses below are the source's, not audited.
> Audit and comparison with this repository: [RECOVERY_NOTES.md](../RECOVERY_NOTES.md).

---

# Authorization Incompleteness: DTM1 token-code Stage-0 scope dialogue

**Date:** 2026-08-20

**Target:** *Authorization as an Incompleteness Boundary*, v0.13

**Target source hash:**
`e5433420a3689d06499c155225d903d32cd0e87d8bad1bcd30a949653dd4b800`

**Base revision:** `97e881fab940f9432f2677cb9b278f1b8e041828`

**Candidate surface:**
`formal/direct_turing_machine_token_code_models.lean` (not yet written)

**Imported seed hash:**
`formal/direct_turing_machine_models.lean`
`0fb0e2bd0688bd926904235e3e666504b82ab45d4a72f7d53e3ddfcec46402c9`

**AuthorityEffect:** None.

## Independence and carrier freeze

This is a producer-side Stage-0 scope dialogue, not an independent I3
review receipt. It freezes the v0.13 paper and the DTM0 source before a
new token-code module, Lake-root change, claim binding, or prose update
is made.

The frozen PO-000 source is not a target of this packet. Its recorded
SHA-256 is
`fb7d2436f1e5da5969c8c4d9b1a143b4a2a0ba8024748568733f4290414d701e`.

## Round 1: What does a token-code theorem establish?

**Red DTM1-R1.** A `List Nat` representation is not a byte stream, a
source file, or a deployed parser. Calling it a byte encoding would
silently close the very syntax-and-encoding obligation that AIT-G5b
leaves open.

**Blue.** Conceded. The candidate will use the term *finite token code*.
It may encode the finite `Machine` record and parse that declared grammar;
it will not claim source bytes, UTF-8, an executable file format, or a
configuration/input encoding.

**Green.** Carry forward. All prose and declaration names must say
token-code or finite codeword, never byte parser.

## Round 2: Does the parser have an exact grammar and a round-trip law?

**Red DTM1-R2.** A hand-waved serialization can conceal ambiguous
framing, an unparsed suffix, duplicate parsing conventions, or an
invalid symbol/move code. A one-way encoder alone is not a parser
adequacy result.

**Blue.** Conceded. The candidate grammar will contain one halt-state
token followed by fixed-width five-token rule frames. The decoder will
consume the entire list, reject an empty header, incomplete frames, and
invalid symbol or movement tags, and prove
`decodeMachine (encodeMachine machine) = some machine` for every finite
rule-list machine.

**Green.** Carry forward. Include closed malformed fixtures in addition
to the generic round-trip theorem. Do not claim a converse uniqueness
theorem unless it is actually formalized.

## Round 3: What has not yet been encoded?

**Red DTM1-R3.** The DTM0 carrier contains a mathematical total tape and
a fuel-bounded evaluator. Encoding a finite rule list alone does not
encode an input configuration, prove parser-to-execution correspondence,
or supply an unbounded evaluator.

**Blue.** Conceded. DTM1 will be a syntax lift only. Its follow-on
obligation will be a separately named configuration/input-code and
bounded trace-agreement lift. The candidate inventory remains partial
on syntax and execution semantics.

**Green.** Carry forward. Do not mark any AIT-G5b admission field closed
or select a carrier from DTM1.

## Round 4: Turing, Rice, and complexity scope

**Red DTM1-R4.** A parser round trip might be presented as a
Turing-completeness witness, a universal-machine theorem, a halting
reduction, Rice's theorem, or progress on P versus NP.

**Blue.** Conceded. The only result will be a finite grammar and its
decoder behavior for DTM0 machine codes. It makes no universality,
extensionality, reduction, halting-decider, Rice, Godel, LLM, or
complexity claim.

**Green.** Carry forward. The proof program must make DTM1 a predecessor
to, not a replacement for, the G5b admission record.

## Round 5: P0, replay, and authorization scope

**Red DTM1-R5.** A deterministic parser can be mistaken for a replay
trust root or an authorization boundary. It may also be treated as proof
that a halt result has a fixed semantic or policy meaning.

**Blue.** Conceded. The parser is a declared syntax map. It does not
prove a report adequate for any semantic contract, bind its own source
bytes, establish custody, prove evaluator correspondence, select a
terminal policy, or alter PO-000's factorization condition.

**Green.** Carry forward. Retain P0, AIT-G3, AIT-G4, and AIT-G5c as
separate evidence surfaces with their existing ceilings.

## Findings carried into the update packet

<!-- markdownlint-disable MD013 -->
| Finding | Required disposition |
| --- | --- |
| DTM1-R1 | Name the new carrier a finite token code; retain byte/source parsing as open. |
| DTM1-R2 | Specify complete fixed-width grammar, malformed rejections, and a decoder-after-encoder theorem. |
| DTM1-R3 | Keep input/configuration encoding and trace agreement as later lifts; retain partial admission status. |
| DTM1-R4 | Preserve all global-computability and complexity nonclaims. |
| DTM1-R5 | Preserve P0, replay, custody, and terminal-policy boundaries. |
<!-- markdownlint-enable MD013 -->

## Findings not carried forward

No finding is rejected on factual grounds. The Stage-0 conclusion is not
that DTM1 completes a program-carrier admission; it only licenses a
narrow parser-round-trip implementation under the carried scope fences.

**AuthorityEffect:** None.
