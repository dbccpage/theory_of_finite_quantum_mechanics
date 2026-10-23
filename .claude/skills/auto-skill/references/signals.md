# Signals for auto-skill

**AuthorityEffect:** None. Condensed and adapted from the_symbol_game `auto-skill/references/signal_reference_table.md`;
signals that only occur in the_symbol_game (councils, MCP servers, sprint tooling, databases) were dropped.

| Priority | Signal | Trigger | Record |
|---|---|---|---|
| HIGHEST | correction | the user says no, don't, always, never, "the convention is" | the quote and the implied rule |
| HIGHEST | passive rejection | the user edits the output, reverts it, or supplies an alternative | proposed vs actual |
| HIGH | tool rejection | the user blocks a tool call, or a shell guard refuses a command (heredoc, chained git, `$var` loop) | the tool, the call, the alternative that worked |
| HIGH | overclaim | a review narrows or reverts a node the session raised; a number in prose did not recompute | node id, claim, what the Lean states |
| HIGH | honesty-gate failure | a Lean admission token, a custom axiom, or a float in an independent check reached a commit | file:line, rule id |
| HIGH | CI or check failure | `validate_derivation_dag`, `overclaim_scan --strict`, `build_readme_facts --check`, the contract checks or pytest failed | job, error, root cause, fix |
| HIGH | environment failure | Windows MAX_PATH, CRLF hash mismatch, a full disk from Lean or cargo builds, a slow untracked-file walk | symptom, fix, prevention |
| HIGH | hallucination | a cited declaration, path or receipt that does not exist | what was claimed, what exists |
| MEDIUM | workflow order | a sync script run out of the order in the reading note; a merge before checks | expected vs actual order |
| MEDIUM | git state | wrong branch, wrong worktree, work in the shared stash | symptom, prevention |
| LOW | manual skill edit | a SKILL.md changed with no auto-skill proposal | the change, the missed signal |
| LOW | lost context | something from an earlier session or before compaction was not recalled | what was missed, where it now lives |

Quality filter: keep a signal only if it is explicit, specific to this repository and likely to recur. Generic advice,
a one-off, or something the skill already says is noise.
