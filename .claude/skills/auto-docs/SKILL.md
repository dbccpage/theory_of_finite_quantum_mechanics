---
name: auto-docs
description: Check that the documentation a change touches still matches the repository. Use in the audit umbrella, before opening a PR that edits Markdown, scripts or anything a generated page reads, and when asked to check docs. Runs scripts/auto/estate_audit.py docs (broken relative links, cited paths that do not exist, missing provenance headers in scripts/auto) and the repository's generated-doc checks (README facts block, status pages). Reports; regenerates only generated files, and only when asked.
---

# Docs check

**AuthorityEffect:** None. Imported from the_symbol_game `auto-docs`, adapted. The source wrote session logs into a
documentation tree of its own and ran a comment-slop router whose module is absent even in the source; neither exists
here, so this skill checks documents against the repository instead. The review file the audit umbrella writes is the
session record. Constraints: `.claude/rules/auto_skills_constraints.md`.

## Step 1. Links, paths and headers

```
python -I -X utf8 scripts/auto/estate_audit.py docs --changed-since origin/main
python -I -X utf8 scripts/auto/estate_audit.py docs --paths README.md docs/overclaim
```

| Rule | Sev | Meaning |
|---|---|---|
| BROKEN_LINK | MEDIUM | a relative Markdown link whose target does not exist (anchors are not checked) |
| MISSING_PATH | LOW | a backticked repository path that does not exist (placeholders such as `<date>` and globs are skipped; a gitignored local view such as an overclaim report also shows here) |
| MISSING_HEADER | LOW | a `scripts/auto/*.py` file whose docstring lacks Origin, Claim, AuthorityEffect or Scope Fence |

## Step 2. Generated documents

Run the checks the change calls for (CONTRIBUTING.md, "How a pull request is reviewed"):

```
python -I -X utf8 scripts/build_readme_facts.py --check
python -I -X utf8 scripts/build_status.py --check
```

If `build_readme_facts --check` fails because the change altered a counted file, regenerate with `--write` in the same
PR and say so. Never hand-edit the facts block. `build_status` pages are not committed.

## Step 3. Read the changed prose

For each changed Markdown file: does every number have a recomputation in the PR (overclaim-hunter Step 3)? Does every
node id it names carry the status the sentence implies (overclaim rule R6)? Is a new script or skill mentioned where a
reader would look for it (README, CONTRIBUTING.md, `.claude/skills/AUTO_SKILLS_IMPORT.md`)?

## Output

Findings with file:line, the generated-doc check results, and a list of documents a reader would need updated. In the
audit umbrella these go into the consolidated report.

## Rules for this skill

- Do not write session logs or move comments out of code. Do not touch `docs/overclaim/baseline.json`.
- Regenerate only generated files, with their own `--write` command.
