# 04. Named failure modes

**AuthorityEffect:** None.
**Sources:** [`02_trial_record.md`](02_trial_record.md) and the files in [`sources/`](sources/README.md).

The trials showed a handful of ways a model, or an auditor of a model, goes
wrong with a bare symbol. The names below were given after the fact. None of
them is a detector, a refusal code or an admitted antibody in the repository;
they are labels for what happened, each tied to the reply where it happened.

| Name | What happened | Where |
| --- | --- | --- |
| Semantic overcompletion | Given a bare `<>` in a code fence, the model listed programming, markup and physics readings. Unfenced, it mostly asked what was meant. The analysis coined the term and credits the fenced prompt with turning it into "epistemic abstention". | [T1 32](../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/pre_genesis/sources/trial_1_transcript.txt#L32), [T2 13](../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/pre_genesis/sources/trial_2_transcript.txt#L13), [v1 28](sources/analysis_derivation_v1.md#L28) |
| Premature relation | Asked whether the regime distinguishes `<a>` and `<ab>`, the model said it "identifies them", though no identity rule existed. | [T1 385](../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/pre_genesis/sources/trial_1_transcript.txt#L385), [v1 151](sources/analysis_derivation_v1.md#L151) |
| Metalanguage mistaken for import | The blind auditor flagged "We" and "rule", words the prompt itself licensed, as structure imported into the regime. | [T1 447](../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/pre_genesis/sources/trial_1_transcript.txt#L447), [T2 469](../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/pre_genesis/sources/trial_2_transcript.txt#L469) |
| Accepted false provenance | Prompt 14 attributed a claim to the model that it had not made in that run. Trial 2 answered the question without objecting; the full replay said "I did not make that claim". | [T2 475](../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/pre_genesis/sources/trial_2_transcript.txt#L475), [FR 145](../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/pre_genesis/sources/full_replay_transcript.txt#L145) |
| Lost state | Given a task about `<a>` and `<ab>`, Trial 2 answered "The regime contains only <>", although `<a>` had been supplied. | [T2 552](../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/pre_genesis/sources/trial_2_transcript.txt#L552) |
| Stale certification | The two-level auditor, shown only Result 15, found nothing wrong ("None."). The error was in the history, which it never saw. | [T2 693](../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/pre_genesis/sources/trial_2_transcript.txt#L693), [v1 818](sources/analysis_derivation_v1.md#L818) |
| Local green, global red | Each step of Result 15 was consistent with its premise; the premise was false for the actual history. | [v1 808 to 816](sources/analysis_derivation_v1.md#L808) |
| Bundled extension | The full replay's four "one-step" extensions each needed several undeclared capabilities (branching, matching, rewriting). | [FR 197](../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/pre_genesis/sources/full_replay_transcript.txt#L197), [FR 468](../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/pre_genesis/sources/full_replay_transcript.txt#L468) |

## How the later system answers them

These failures are why the Proposal Fidelity Protocol (PFP, strand
[`030`](../030_the_symbol_game_proposal_fidelity_protocol_pfp/README.md))
treats every model reply as an untrusted candidate. Its four objects are
problem, candidate, verifier and receipt, and a candidate "must never assert
its own validity"; only the host's receipt carries a status
([`06_prompt_packet_stage_synthesis.md`](../030_the_symbol_game_proposal_fidelity_protocol_pfp/docs/06_prompt_packet_stage_synthesis.md)).
Replay necessity (chapter 03, result 6) requires the auditor's input to preserve
the answer being checked. Retaining the full history and every raw reply is
PFP's provenance policy; the theorem also allows a sufficient state summary.

That is a design response to these trials. It does not mean the trials tested
PFP, or that PFP removes these failures; the trials ran before PFP existed and
no PFP gate was applied to them.
