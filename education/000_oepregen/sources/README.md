# Primary sources

**AuthorityEffect:** None.

Six primary records are in this folder. `design_derivation_v0.md` and
`analysis_derivation_v1.md` were already tracked. `trial_1_transcript.md`,
`trial_2_transcript.md`, `full_replay_prompt_pack.md`, and
`full_replay_transcript.md` were restored from commit
`0622e7e666877c61ae9330fe55b6a223965e23eb` (the parent of `271004906a`, which
removed them). Plain-text copies remain in the atlas, and the lessons cite those
copies. The restored markdown and the atlas text are separate files. Do not edit
either copy; corrections belong in the chapters.

| File | Original name | What it is |
| --- | --- | --- |
| `design_derivation_v0.md` | `omega_engine_derivation_v0.md` | The experimental design, written before any trial: principles, hidden comparison targets, pre-registered branches, controls. |
| `trial_1_transcript.md` | `oe_prompt_and_response_deepseek_v0.0.md` | Trial 1: prompts 1 to 13 and the model's replies. Controls 1 to 10 were sent inside code fences. This markdown file is in this folder. Lessons cite the separate atlas copy [`trial_1_transcript.txt`](../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/pre_genesis/sources/trial_1_transcript.txt). |
| `analysis_derivation_v1.md` | `omega_engine_derivation_v1.md` | Analysis of Trial 1 (lines 1 to 583) and of Trial 2 up to Result 16 (lines 585 to 1190). Written in the second person to the author; who wrote it is not recorded. |
| `trial_2_transcript.md` | `oe_prompt_and_response_deepseek_v1.0.md` | Trial 2: prompts 1 to 17, raw controls, then an appended analysis from line 890 ("Verdict" to the closing spine). This markdown file is in this folder. Lessons cite the separate atlas copy [`trial_2_transcript.txt`](../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/pre_genesis/sources/trial_2_transcript.txt). |
| `full_replay_prompt_pack.md` | `oe_prompt_and_response_deepseek_v1.1.md` | Prompts prepared for the full-history replay. All results are empty. This markdown file is in this folder. The atlas copy is [`full_replay_prompt_pack.txt`](../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/pre_genesis/sources/full_replay_prompt_pack.txt). |
| `full_replay_transcript.md` | `oe_full_generator_results_v1.md` | The full-history replay: prompts 11, 12, 14, 15, 17, 18 and 19 with replies. This markdown file is in this folder. Lessons cite the separate atlas copy [`full_replay_transcript.txt`](../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/pre_genesis/sources/full_replay_transcript.txt). |

What the record does not contain:

- the model identifier, sampling settings or dates. The files are called
  "DeepSeek v0.0, v1.0, v1.1", but those are file versions, not model versions;
  the design asked for the model metadata to be recorded (`design_derivation_v0.md`
  line 414) and it was not;
- any count of trials beyond these three runs, or any pass rate;
- any host check of a reply. Every judgement of "admissible", "correct" or
  "lawful" in the analysis files is a human or advisor-model judgement.
