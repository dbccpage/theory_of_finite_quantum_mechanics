# Failure modes of a learning skill

**AuthorityEffect:** None.

1. **Missed durable correction.** The user gave an explicit, repeated, project-specific correction and no skill
   changed. Fix: add the signal to `auto-skill/references/signals.md` or tighten its trigger.
2. **Over-capture.** A proposal records generic advice, a one-off or something already written. Fix: tighten the
   quality filter.
3. **Additive bloat.** More prose where a check, a template or a shared rule would do. Fix: rewrite as one compressive
   change (a `scripts/auto/` rule with a test, or one line in the shared constraints file).
4. **Partial family propagation.** One skill of a family was updated and its siblings were not. Fix: put the rule in
   the shared file once and cite it; run `auto-symmetry-hunter`.
5. **Self-reference miss.** The session showed a flaw in the learning skill itself and no self-edit was proposed.
6. **Ephemeral change.** A skill under the gitignored `.claude/` was edited and never force-added, so the change was
   lost. Fix: `git add -f -- <path>` in the same PR.
7. **Authority creep.** A learned rule gives a skill a power it must not have: "raise a status", "accept its own
   output", or "treat a passing check as a proof". Always VETO.
