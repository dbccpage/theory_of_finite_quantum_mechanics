# Primary sources

**AuthorityEffect:** None.

These six files are the record of the pre-genesis trials. They are byte-for-byte
copies of the originals under `ow/pfp/pre_genesis_testing/` at commit
`cf95ddd8c` (2026-10-04), restored here because the later chapters that
replaced them misquoted them. Every citation in this strand points at a line in
one of these files. Do not edit them; corrections belong in the chapters.

| File | Original name | What it is |
| --- | --- | --- |
| `design_derivation_v0.md` | `omega_engine_derivation_v0.md` | The experimental design, written before any trial: principles, hidden comparison targets, pre-registered branches, controls. |
| `trial_1_transcript.md` | `oe_prompt_and_response_deepseek_v0.0.md` | Trial 1: prompts 1 to 13 and the model's replies. Controls 1 to 10 were sent inside code fences. |
| `analysis_derivation_v1.md` | `omega_engine_derivation_v1.md` | Analysis of Trial 1 (lines 1 to 583) and of Trial 2 up to Result 16 (lines 585 to 1190). Written in the second person to the author; who wrote it is not recorded. |
| `trial_2_transcript.md` | `oe_prompt_and_response_deepseek_v1.0.md` | Trial 2: prompts 1 to 17, raw controls, then an appended analysis from line 890 ("Verdict" to the closing spine). |
| `full_replay_prompt_pack.md` | `oe_prompt_and_response_deepseek_v1.1.md` | Prompts prepared for the full-history replay. All results are empty. |
| `full_replay_transcript.md` | `oe_full_generator_results_v1.md` | The full-history replay: prompts 11, 12, 14, 15, 17, 18 and 19 with replies. |

What the record does not contain:

- the model identifier, sampling settings or dates. The files are called
  "DeepSeek v0.0, v1.0, v1.1", but those are file versions, not model versions;
  the design asked for the model metadata to be recorded (`design_derivation_v0.md`
  line 414) and it was not;
- any count of trials beyond these three runs, or any pass rate;
- any host check of a reply. Every judgement of "admissible", "correct" or
  "lawful" in the analysis files is a human or advisor-model judgement.
