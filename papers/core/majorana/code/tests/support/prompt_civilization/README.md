# Prompt Civilization v0

This crate is a deterministic, `AuthorityEffect: None` reference runtime for
two separate capabilities:

- `omega-prompt` reviews a model-proposed prompt structure, preserves the
  original bytes, requires an explicit operator decision, and packetizes an
  approved prompt through the existing Symbol Game LLM-turn boundary.
- `auto-antiskill` segments supported IDE dialogues and emits provenance-bound
  candidate records. It has no admission operation.

## Typed operations

`operad.py` declares the finite nonsymmetric colored-operad presentation:

```text
PromptArtifact -> FindingSet
(PromptArtifact, FindingSet) -> PromptCandidate
(PromptArtifact, PromptCandidate) -> ReviewReceipt
(PromptCandidate, ReviewReceipt, OperatorDecision) -> ApprovedPrompt
ApprovedPrompt -> PacketEnvelope
RawDialogue -> EpisodeSet
EpisodeSet -> AntiSkillCandidateSet
```

These are one-operations. Candidate learning and admission are directed
refinements outside the mapping groupoid. The presentation declares no
`Path2`, quotient, symmetry, implicit copy/delete operation, or equivalence
between detection, repair, and verification.

## Security and evidence boundary

- JSON fields are exact; unknown fields refuse.
- IDs are domain-separated canonical content hashes and exclude timestamps.
- A content hash establishes byte integrity, not truth.
- An evaluation receipt is recomputed from named fixtures and reports
  `COMPUTED_PASS` or `COMPUTED_FAIL`; it grants no admission authority.
- Registry detectors use a closed structural grammar. There are no dynamic
  callables or executable regular expressions.
- `approve_prompt` independently replays review before accepting an operator
  decision.
- The CLI has no `send` or `admit` command.

The v0 CLI records an explicit operator identifier but does not authenticate
that identity. Host capability enforcement is therefore still required to
prevent model-controlled code from invoking approval. Approval grants no
execution authority and the packet remains `AuthorityEffect: None`.

Python object immutability is not a process isolation boundary. A future OEOS
adapter must put verifier keys, CAS, isolated executors, and capability tokens
outside model-controlled processes. This v0 intentionally stops at review and
packet construction.

## Skill admission state

This PR does not install `omega-prompt` or `auto-antiskill` into a live host
skill-discovery root. Their draft packages are preserved under
`.agents/skills/ooutwire/prompt-civilization-v0-drafts/` with non-discoverable
manifest names. Promotion requires a separate human admission decision, the
repository admission checklist, and byte-identical host installation.
