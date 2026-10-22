"""Generate the project status page and the daily digests under docs/status/.

AuthorityEffect: None. This script reports counts and changes that it computes from
`dag/derivation_dag.json`, `dag/pfp/campaign/LOG.md` and the git history. It adds no
result and promotes no status.

    python -I -X utf8 scripts/build_status.py --write [--with-prs] [--as-of YYYY-MM-DD]
    python -I -X utf8 scripts/build_status.py --check [--strict]   [--as-of YYYY-MM-DD]

One status site
---------------
The generated files are `docs/status/README.md`, `docs/status/daily/<date>.md` and
`docs/status/daily/index.md`. They are **not committed**: they are listed in `.gitignore`, and the daily
workflow `.github/workflows/status.yml` writes them in its own workspace, checks them with `--check --strict`,
and publishes them with the hand-written pages of `docs/`. Committing them cannot work, because a digest
names commits and their subjects, and the commit that adds a digest, or a squash merge that rewrites a
subject, changes what the digest should say. So there is exactly one status site, the CI-generated one,
and `--check` enforces it:

* it rebuilds every generated file in memory and fails on any byte difference with the file on disk
  (the only region it ignores is the open-pull-request block of the README, which depends on GitHub);
* it fails if a file on disk under `docs/status/daily/` is not one the build would produce;
* it fails if any generated path is tracked by git;
* with `--strict` it also fails if a generated file is missing.

Git failures are errors, never empty data
-----------------------------------------
The build refuses to run on a shallow clone. A DAG or campaign-log snapshot is treated as empty only when
`git cat-file -e <commit>` shows that the commit exists and `git cat-file -e <commit>:<path>` shows that the
path does not. Any other git failure stops the build with exit code 2. A failed `git show` can therefore
never turn into "every node was added".

What the pages contain
----------------------
docs/status/README.md
    Node counts by status and by stage, the most recently changed nodes, the campaign log, open pull
    requests (only with `--write --with-prs`; if that was requested and `gh` fails, the build fails) and
    links. It contains no date and no hash of the checked-out revision.
docs/status/daily/<YYYY-MM-DD>.md
    One page per UTC day for the `--days` days ending at `--as-of` (default: the UTC date of the newest
    commit). One first-parent log is partitioned by committer date. For every commit of the day that changes
    the DAG, the page shows that commit's own changes against its first parent (added, removed, status and
    statement changes), so a node that is added and narrowed on the same day appears twice, as two events.
    New campaign-log lines are shown the same way.
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[1]
DAG_PATH = "dag/derivation_dag.json"
LOG_PATH = "dag/pfp/campaign/LOG.md"
CAMPAIGN_README = "dag/pfp/campaign/README.md"
EVIDENCE_README = "docs/evidence/README.md"
OUT_DIR = "docs/status"
REPO_URL = "https://github.com/dbccpage/theory_of_finite_quantum_mechanics"
BLOB = REPO_URL + "/blob/main/"
PRS_BEGIN = "<!-- prs:begin -->"
PRS_END = "<!-- prs:end -->"
PRS_PLACEHOLDER = "Open pull requests are listed when the page is built by the daily workflow."
LOG_LINE = re.compile(r"^\d{4}-\d{2}-\d{2}\s*\|")
RECENT_DAG_COMMITS = 12      # DAG-changing commits examined for "most recently changed nodes"
RECENT_NODES_SHOWN = 15
DEFAULT_DAYS = 14
ADDED_LISTED = 25
CHANGES_LISTED = 60

STATUS_ORDER = ("PROVED_LEAN", "PROVED_PROSE", "COMPUTATIONALLY_CHECKED", "CONDITIONAL", "IMPORTED_ASSUMPTION",
                "DEFINITION", "ADMITTED_PRIMITIVE", "SOURCE_RECORD", "OPEN", "REFUTED")
STAGE_COLUMNS = (("PROVED_LEAN", "Lean"), ("PROVED_PROSE", "Prose"), ("COMPUTATIONALLY_CHECKED", "Comp. checked"),
                 ("CONDITIONAL", "Conditional"), ("IMPORTED_ASSUMPTION", "Imported"), ("OPEN", "Open"))


class GitError(RuntimeError):
    """A git command failed in a way that is not 'this path does not exist in this commit'."""


# ----------------------------------------------------------------------------- text helpers

def esc(text: str, limit: int | None = None) -> str:
    """Make text safe inside a Markdown table cell and a Liquid-processed page."""
    text = " ".join(str(text).split())
    if limit is not None and len(text) > limit:
        text = text[: limit - 1].rstrip() + "…"
    return text.replace("|", "\\|").replace("{{", "{ {").replace("{%", "{ %").replace("<", "&lt;")


def blob_link(rel: str, label: str | None = None) -> str:
    return "[`%s`](%s%s)" % (label or rel, BLOB, rel)


def normalise_eol(text: str) -> str:
    return text.replace("\r\n", "\n")


# ----------------------------------------------------------------------------- git access

Runner = Callable[[list], tuple]


def run_git(args: list) -> tuple:
    """(return code, stdout, stderr) of `git <args>` in the repository root."""
    proc = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=False)
    return proc.returncode, proc.stdout.decode("utf-8", "replace"), proc.stderr.decode("utf-8", "replace")


class Commit:
    __slots__ = ("sha", "when", "subject")

    def __init__(self, sha: str, when: dt.datetime, subject: str):
        self.sha, self.when, self.subject = sha, when, subject

    @property
    def short(self) -> str:
        return self.sha[:9]


def nodes_of(doc: dict) -> dict:
    return {n["id"]: {"status": n.get("status", ""), "statement": n.get("statement") or "", "stage": n.get("stage", "")}
            for n in doc.get("nodes", [])}


def log_lines_of(text: str) -> list:
    return [line.strip() for line in normalise_eol(text).splitlines() if LOG_LINE.match(line)]


class GitSource:
    """The history the pages are built from. A test can replace it with any object that has the same methods:
    `commits` (newest first, first-parent), `nodes(sha)`, `dag_changed(sha, parent_sha)`, `log_lines(sha)`."""

    def __init__(self, rev: str = "HEAD", run: Runner = run_git):
        self.rev, self._run = rev, run
        self._commits: list | None = None
        self._touch = None
        self._absent: dict = {}
        self._nodes: dict = {}
        self._lines: dict = {}

    def git(self, *args: str) -> str:
        code, out, err = self._run(list(args))
        if code != 0:
            raise GitError("git %s failed (exit %d): %s" % (" ".join(args), code, err.strip()))
        return out

    def require_full_history(self) -> None:
        state = self.git("rev-parse", "--is-shallow-repository").strip()
        if state != "false":
            raise GitError("the repository is shallow (git reports %r); fetch the full history first, for example "
                           "with `git fetch --unshallow` or actions/checkout with fetch-depth: 0" % state)

    @property
    def commits(self) -> list:
        if self._commits is None:
            rows = []
            for line in self.git("log", "--first-parent", "--format=%H%x1f%cI%x1f%s", self.rev).splitlines():
                sha, when, subject = line.split("\x1f", 2)
                rows.append(Commit(sha, dt.datetime.fromisoformat(when).astimezone(dt.timezone.utc), subject))
            self._commits = rows
        return self._commits

    def _touches(self) -> tuple:
        """One call: for every commit of the first-parent log that touches the DAG or the campaign log, the new blob id of each
        path it touches (None when the commit deletes it). Also the index of every commit in the log."""
        if self._touch is None:
            out = self.git("log", "--first-parent", "-m", "--raw", "--no-abbrev", "--no-renames", "--format=%x01%H",
                           self.rev, "--", DAG_PATH, LOG_PATH)
            touch: dict = {}
            current = None
            for line in out.splitlines():
                if line.startswith("\x01"):
                    current = line[1:].strip()
                    touch[current] = {}
                elif line.startswith(":") and current is not None:
                    meta, path = line.split("\t", 1)
                    fields = meta.split()
                    touch[current][path] = None if set(fields[3]) == {"0"} else fields[3]
            self._touch = (touch, {c.sha: i for i, c in enumerate(self.commits)})
        return self._touch

    def blob(self, sha: str, path: str):
        """The blob id of `path` in commit `sha`, found from the path-limited log (the newest commit at or below `sha`
        that touches it). None means the path does not exist in `sha`, and is returned only after
        `git cat-file -e <sha>` confirms that the commit exists and `git cat-file -e <sha>:<path>` that the path does not."""
        touch, index = self._touches()
        if sha not in index:
            raise GitError("commit %s is not in the first-parent log of %s" % (sha, self.rev))
        found = None
        for commit in self.commits[index[sha]:]:
            if path in touch.get(commit.sha, {}):
                found = touch[commit.sha][path]
                break
        if found is not None:
            return found
        # No commit at or below `sha` touches the path, so it is absent in `sha` and in everything older. One verified
        # commit therefore covers every older one.
        if index[sha] >= self._absent.get(path, len(index)):
            return None
        if self._run(["cat-file", "-e", sha])[0] != 0:
            raise GitError("commit %s does not exist or cannot be read" % sha)
        if self._run(["cat-file", "-e", "%s:%s" % (sha, path)])[0] == 0:
            raise GitError("the log says %s is absent from %s, but git finds it" % (path, sha))
        self._absent[path] = index[sha]
        return None
    def nodes(self, sha) -> dict:
        if sha is None:
            return {}
        blob = self.blob(sha, DAG_PATH)
        if blob is None:
            return {}
        if blob not in self._nodes:
            try:
                self._nodes[blob] = nodes_of(json.loads(self.git("cat-file", "blob", blob)))
            except ValueError as exc:
                raise GitError("%s at %s is not valid JSON: %s" % (DAG_PATH, sha, exc)) from exc
        return self._nodes[blob]

    def dag_changed(self, sha: str, parent_sha) -> bool:
        return parent_sha is None or self.blob(sha, DAG_PATH) != self.blob(parent_sha, DAG_PATH)

    def log_lines(self, sha) -> list:
        if sha is None:
            return []
        blob = self.blob(sha, LOG_PATH)
        if blob is None:
            return []
        if blob not in self._lines:
            self._lines[blob] = log_lines_of(self.git("cat-file", "blob", blob))
        return self._lines[blob]


def tracked_generated_paths(run: Runner = run_git) -> list:
    """Generated files that git tracks. There must be none: the status site is generated in CI only."""
    code, out, err = run(["ls-files", "--", OUT_DIR])
    if code != 0:
        raise GitError("git ls-files failed: %s" % err.strip())
    return [p for p in out.splitlines() if p.strip()]


# ----------------------------------------------------------------------------- DAG differences

def diff_nodes(old: dict, new: dict) -> list:
    """(node id, kind, status before, status after); kind is added, removed, status or statement."""
    rows = []
    for node_id in sorted(set(old) | set(new)):
        before, after = old.get(node_id), new.get(node_id)
        if before is None:
            rows.append((node_id, "added", "", after["status"]))
        elif after is None:
            rows.append((node_id, "removed", before["status"], ""))
        elif before["status"] != after["status"]:
            rows.append((node_id, "status", before["status"], after["status"]))
        elif before["statement"] != after["statement"]:
            rows.append((node_id, "statement", before["status"], after["status"]))
    return rows


def commit_changes(src, commits: list, index: int) -> list:
    """The commit's own DAG changes against its first parent (the next entry of the first-parent log)."""
    parent = commits[index + 1].sha if index + 1 < len(commits) else None
    sha = commits[index].sha
    if not src.dag_changed(sha, parent):
        return []
    return diff_nodes(src.nodes(parent), src.nodes(sha))


def commit_log_additions(src, commits: list, index: int) -> list:
    parent = commits[index + 1].sha if index + 1 < len(commits) else None
    old = set(src.log_lines(parent))
    return [line for line in src.log_lines(commits[index].sha) if line not in old]


def counts(nodes: dict) -> tuple:
    by_status: collections.Counter = collections.Counter()
    by_stage: dict = collections.defaultdict(collections.Counter)
    for node in nodes.values():
        by_status[node["status"]] += 1
        by_stage[node["stage"]][node["status"]] += 1
    return by_status, by_stage


def status_order(by_status: collections.Counter) -> list:
    return [s for s in STATUS_ORDER if s in by_status] + sorted(s for s in by_status if s not in STATUS_ORDER)


def recent_changes(src) -> list:
    """The latest change per node over the last RECENT_DAG_COMMITS commits that changed the DAG."""
    commits = src.commits
    latest: dict = {}
    touched = 0
    for index, commit in enumerate(commits):
        changes = commit_changes(src, commits, index)
        if not changes:
            continue
        touched += 1
        for node_id, kind, before, after in changes:
            if node_id not in latest:
                latest[node_id] = {"id": node_id, "kind": kind, "before": before, "after": after, "commit": commit}
        if touched >= RECENT_DAG_COMMITS:
            break
    ordered = sorted(latest.values(), key=lambda r: (-r["commit"].when.timestamp(), r["id"]))
    return ordered[:RECENT_NODES_SHOWN]


def describe_change(row: dict) -> str:
    if row["kind"] == "added":
        return "added as `%s`" % row["after"]
    if row["kind"] == "removed":
        return "removed"
    if row["kind"] == "status":
        return "`%s` to `%s`" % (row["before"], row["after"])
    return "statement changed, status `%s`" % row["after"]


# ----------------------------------------------------------------------------- status page

def prs_block(with_prs: bool, run=None) -> str:
    """The open-pull-request table. If it was asked for and cannot be made, that is an error."""
    if not with_prs:
        return PRS_PLACEHOLDER
    runner = run or (lambda cmd: subprocess.run(cmd, cwd=ROOT, capture_output=True, timeout=90))
    try:
        proc = runner(["gh", "pr", "list", "--state", "open", "--limit", "40", "--json",
                       "number,title,author,isDraft,updatedAt,url"])
        if proc.returncode != 0:
            raise GitError("gh pr list failed (exit %d): %s" % (proc.returncode, proc.stderr.decode("utf-8", "replace").strip()))
        prs = json.loads(proc.stdout.decode("utf-8"))
    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        raise GitError("--with-prs was requested but the open pull requests could not be listed: %s" % exc) from exc
    if not prs:
        return "There are no open pull requests."
    prs.sort(key=lambda p: p["number"], reverse=True)
    lines = ["| PR | Title | Author | State | Updated (UTC) |", "|---|---|---|---|---|"]
    for pr in prs:
        lines.append("| [#%d](%s) | %s | %s | %s | %s |" % (
            pr["number"], pr["url"], esc(pr["title"], 110), esc((pr.get("author") or {}).get("login", "")),
            "draft" if pr.get("isDraft") else "ready", pr["updatedAt"][:10]))
    return "\n".join(lines)


def campaign_section(root: Path) -> list:
    lines = ["## Derivation campaign", ""]
    if not (root / CAMPAIGN_README).is_file():
        lines += ["The derivation campaign protocol is not on `main` in this build.", ""]
        return lines
    log = root / LOG_PATH
    entries = log_lines_of(log.read_text(encoding="utf-8")) if log.is_file() else []
    lines += ["The protocol is %s and the log is %s." % (blob_link(CAMPAIGN_README), blob_link(LOG_PATH)), ""]
    if not entries:
        lines += ["The log has no entries yet.", ""]
    else:
        lines += ["Targets recorded in the log: %d. Latest entries:" % len(entries), ""]
        lines += ["- %s" % esc(e, 240) for e in entries[-5:][::-1]]
        lines.append("")
    return lines


def evidence_line(root: Path) -> str:
    if (root / EVIDENCE_README).is_file():
        return "[the evidence map](../evidence/README.md)"
    return "the evidence map, which is proposed in [pull request #181](%s/pull/181) and is not on `main` yet" % REPO_URL


def build_readme(doc: dict, src, prs_text: str, root: Path = ROOT) -> str:
    nodes = nodes_of(doc)
    legend = doc.get("status_legend", {})
    by_status, by_stage = counts(nodes)
    out = ["# Where the project stands", "",
           "This page is generated by `scripts/build_status.py` from the derivation DAG, the campaign log and the git history. "
           "It reports; it does not argue. Daily digests are in [the digest index](daily/index.md).", "",
           "## How to read the numbers", "",
           "- A status label is only as strong as its evidence. `PROVED_LEAN` means a named Lean declaration exists in the "
           "checkout and the source cites it. It does not mean that every node with that label was re-elaborated for this page, "
           "and a node count is not a count of theorems.",
           "- `COMPUTATIONALLY_CHECKED` means an exact finite computation exists. It is not a proof of a general statement.",
           "- `CONDITIONAL` and `IMPORTED_ASSUMPTION` nodes depend on structure that is supplied, not derived.",
           "- Labels have been lowered in the past when review found them too strong. The record of those cases is in the "
           "%s section “How claims are kept honest”." % blob_link("README.md"),
           "- The per-node evidence pages are in %s." % evidence_line(root), "",
           "## Nodes by status", "",
           "The DAG has **%d** nodes and **%d** routes." % (len(nodes), len(doc.get("routes", []))), "",
           "| Status | Nodes | Meaning in the DAG legend |", "|---|---:|---|"]
    for status in status_order(by_status):
        out.append("| `%s` | %d | %s |" % (status, by_status[status], esc(legend.get(status, ""), 150)))
    out += ["", "## Nodes by stage", "",
            "Columns are the six statuses that carry the most weight; `Other` is the remainder (definitions, source records, "
            "admitted primitives, refuted). Stages follow the order of `stages` in the DAG.", "",
            "| Stage | Nodes | " + " | ".join(label for _, label in STAGE_COLUMNS) + " | Other |",
            "|---|---:|" + "---:|" * (len(STAGE_COLUMNS) + 1)]
    declared = doc.get("stages", [])
    for stage in [s for s in declared if s in by_stage] + sorted(s for s in by_stage if s not in declared):
        row = by_stage[stage]
        shown = [row.get(key, 0) for key, _ in STAGE_COLUMNS]
        out.append("| `%s` | %d | %s | %d |" % (stage, sum(row.values()), " | ".join(str(v) for v in shown), sum(row.values()) - sum(shown)))
    out += ["", "## Most recently changed nodes", "",
            "The latest change per node over the last %d commits that changed `%s`, newest first, each change taken against that "
            "commit's first parent. Only status and statement changes (and additions and removals) are listed." % (RECENT_DAG_COMMITS, DAG_PATH), ""]
    changes = recent_changes(src)
    if changes:
        out += ["| Node | Stage | Change | Commit | Date (UTC) | Subject |", "|---|---|---|---|---|---|"]
        for row in changes:
            node = nodes.get(row["id"])
            out.append("| `%s` | %s | %s | [`%s`](%s/commit/%s) | %s | %s |" % (
                row["id"], "`%s`" % node["stage"] if node else "", describe_change(row), row["commit"].short, REPO_URL,
                row["commit"].sha, row["commit"].when.strftime("%Y-%m-%d"), esc(row["commit"].subject, 100)))
        out.append("")
    out += campaign_section(root)
    out += ["## Open pull requests", "", PRS_BEGIN, prs_text, PRS_END, "",
            "## Links", "",
            "- [Project landing page](../index.md)",
            "- [Example prompts](../contribute/example_prompts.md) that anyone can run",
            "- [Reviewer credit list](../reviewers.md)",
            "- %s: three ways to help" % blob_link("CONTRIBUTING.md"),
            "- %s: how a review works and how credit is given" % blob_link("REVIEWING.md"),
            "- %s: how the DAG is built" % blob_link("dag/derivation_dag_reading_note.md"),
            "- " + evidence_line(root)[0].upper() + evidence_line(root)[1:]]
    return "\n".join(out) + "\n"


# ----------------------------------------------------------------------------- daily digests

def partition_by_day(commits: list) -> dict:
    """ONE partition of the first-parent log: UTC date -> indices into `commits` (newest first)."""
    days: dict = collections.defaultdict(list)
    for index, commit in enumerate(commits):
        days[commit.when.date()].append(index)
    return days


def render_digest(day: dt.date, commits: list, by_day: dict, src) -> tuple:
    indices = by_day.get(day, [])
    end = dt.datetime.combine(day + dt.timedelta(days=1), dt.time(0, 0), tzinfo=dt.timezone.utc)
    head_index = next((i for i, c in enumerate(commits) if c.when < end), None)   # newest commit at or before the end of the day
    stats = {"commits": len(indices), "node_changes": 0}
    out = ["# Status digest: %s" % day.isoformat(), "",
           "Generated by `scripts/build_status.py` from the first-parent history: commits with a committer date on %s (UTC)." % day.isoformat(), "",
           "## Merged commits (%d)" % len(indices), ""]
    out += ["- [`%s`](%s/commit/%s) %s" % (commits[i].short, REPO_URL, commits[i].sha, esc(commits[i].subject, 200)) for i in indices] or ["No commits on this date."]
    out.append("")
    events, log_added = [], []
    for i in reversed(indices):                      # chronological order within the day
        changes = commit_changes(src, commits, i)
        if changes:
            events.append((i, changes))
        log_added += commit_log_additions(src, commits, i)
    total = sum(len(c) for _, c in events)
    stats["node_changes"] = total
    out += ["## DAG changes by commit (%d changes in %d commits)" % (total, len(events)), ""]
    if not events:
        out += ["No commit of this day changed a node.", ""]
    else:
        out += ["Each commit's changes are taken against its own first parent, so a node that is added and then narrowed on "
                "the same day appears once under each commit. A statement change is listed by id only; the diff is in the commit.", ""]
    for i, changes in events:
        commit = commits[i]
        kinds = collections.Counter(kind for _, kind, _, _ in changes)
        summary = ", ".join("%d %s" % (kinds[k], k) for k in ("added", "status", "statement", "removed") if kinds[k])
        out += ["### [`%s`](%s/commit/%s) %s" % (commit.short, REPO_URL, commit.sha, esc(commit.subject, 160)), "",
                "%s UTC: %s." % (commit.when.strftime("%H:%M"), summary), ""]
        others = [r for r in changes if r[1] != "added"]
        added = [r for r in changes if r[1] == "added"]
        if others:
            out += ["| Node | Change | Status before | Status after |", "|---|---|---|---|"]
            out += ["| `%s` | %s | %s | %s |" % (n, k, "`%s`" % b if b else "", "`%s`" % a if a else "") for n, k, b, a in others[:CHANGES_LISTED]]
            if len(others) > CHANGES_LISTED:
                out += ["", "%d further changes are not listed." % (len(others) - CHANGES_LISTED)]
            out.append("")
        if added:
            by_status = collections.Counter(a for _, _, _, a in added)
            out += ["Added nodes by status: " + ", ".join("%s %d" % (s, by_status[s]) for s in status_order(by_status)) + ".", "",
                    "Added: " + ", ".join("`%s`" % n for n, _, _, _ in added[:ADDED_LISTED])
                    + (" and %d more." % (len(added) - ADDED_LISTED) if len(added) > ADDED_LISTED else "."), ""]
    out += ["## New campaign log lines (%d)" % len(log_added), ""]
    out += ["- %s" % esc(line, 300) for line in log_added] or ["None."]
    out.append("")
    if head_index is not None:
        by_status, _ = counts(src.nodes(commits[head_index].sha))
        if by_status:
            out += ["## Counts at the end of the day", "",
                    "Nodes: %d. " % sum(by_status.values()) + ", ".join("%s %d" % (s, by_status[s]) for s in status_order(by_status))
                    + ". From the DAG at [`%s`](%s/commit/%s)." % (commits[head_index].short, REPO_URL, commits[head_index].sha), ""]
    return "\n".join(out), stats


def build_digests(src, last_day: dt.date, days: int) -> dict:
    commits = src.commits
    by_day = partition_by_day(commits)
    files, rows = {}, []
    for offset in range(days):
        day = last_day - dt.timedelta(days=offset)
        text, stats = render_digest(day, commits, by_day, src)
        files["%s/daily/%s.md" % (OUT_DIR, day.isoformat())] = text.rstrip("\n") + "\n"
        rows.append((day, stats))
    index = ["# Daily digests", "",
             "One page per UTC day for the last %d days, newest first. Each page is generated from the git history by "
             "`scripts/build_status.py`; a day with no commits says so. The overview is [where the project stands](../README.md)." % days, "",
             "| Date (UTC) | Commits | Node changes (added, removed, status, statement) |", "|---|---:|---:|"]
    index += ["| [%s](%s.md) | %d | %d |" % (d.isoformat(), d.isoformat(), s["commits"], s["node_changes"]) for d, s in rows]
    files["%s/daily/index.md" % OUT_DIR] = "\n".join(index) + "\n"
    return files


# ----------------------------------------------------------------------------- generate, write, check

def generate(src, doc: dict, *, as_of=None, days: int = DEFAULT_DAYS, prs_text: str = PRS_PLACEHOLDER, root: Path = ROOT) -> dict:
    """Every generated file: relative path -> text. A function of the arguments, the history and the working tree."""
    commits = src.commits
    if not commits:
        raise GitError("the history of %s is empty" % src.rev)
    last_day = as_of or max(c.when for c in commits).date()
    files = {OUT_DIR + "/README.md": build_readme(doc, src, prs_text, root)}
    files.update(build_digests(src, last_day, days))
    return files


def normalise_prs(text: str) -> str:
    pattern = re.compile(re.escape(PRS_BEGIN) + r".*?" + re.escape(PRS_END), re.S)
    return pattern.sub(PRS_BEGIN + "\n" + PRS_PLACEHOLDER + "\n" + PRS_END, normalise_eol(text))


def comparable(rel: str, text: str) -> str:
    return normalise_prs(text) if rel == OUT_DIR + "/README.md" else normalise_eol(text)


def drift(files: dict, root: Path = ROOT, strict: bool = False) -> list:
    """Reasons the generated files on disk differ from `files`. An empty list means no drift."""
    problems = []
    for rel, text in sorted(files.items()):
        path = root / rel
        if not path.is_file():
            if strict:
                problems.append("missing: %s" % rel)
        elif comparable(rel, path.read_text(encoding="utf-8")) != comparable(rel, text):
            problems.append("stale: %s" % rel)
    daily = root / OUT_DIR / "daily"
    if daily.is_dir():
        for path in sorted(daily.glob("*.md")):
            rel = "%s/daily/%s" % (OUT_DIR, path.name)
            if rel not in files:
                problems.append("unexpected file: %s" % rel)
    return problems


def write_files(files: dict, root: Path = ROOT) -> None:
    daily = root / OUT_DIR / "daily"
    if daily.is_dir():
        for path in daily.glob("*.md"):
            if "%s/daily/%s" % (OUT_DIR, path.name) not in files:
                path.unlink()
    for rel, text in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text.encode("utf-8"))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="write the generated files (they are not committed)")
    mode.add_argument("--check", action="store_true", help="exit 1 if a generated file on disk differs from a rebuild, or if one is tracked")
    parser.add_argument("--with-prs", action="store_true", help="with --write: list open pull requests through gh; fails if gh fails")
    parser.add_argument("--strict", action="store_true", help="with --check: a missing generated file is an error")
    parser.add_argument("--rev", default="HEAD", help="revision whose first-parent history is used (default HEAD)")
    parser.add_argument("--as-of", default=None, help="last digest date, YYYY-MM-DD (default: UTC date of the newest commit)")
    parser.add_argument("--days", type=int, default=DEFAULT_DAYS, help="number of daily digests (default %d)" % DEFAULT_DAYS)
    args = parser.parse_args(argv)
    try:
        src = GitSource(args.rev)
        src.require_full_history()
        doc = json.loads(normalise_eol((ROOT / DAG_PATH).read_text(encoding="utf-8")))
        as_of = dt.date.fromisoformat(args.as_of) if args.as_of else None
        prs_text = prs_block(args.with_prs) if args.write else PRS_PLACEHOLDER
        files = generate(src, doc, as_of=as_of, days=args.days, prs_text=prs_text)
        if args.write:
            tracked = tracked_generated_paths()
            if tracked:
                raise GitError("generated files are tracked by git, which is not allowed: %s" % ", ".join(tracked))
            write_files(files)
            print("wrote %d generated files under %s (not to be committed)" % (len(files), OUT_DIR))
            return 0
        problems = drift(files, strict=args.strict)
        tracked = tracked_generated_paths()
        problems += ["tracked by git (the status site is generated in CI only): %s" % p for p in tracked]
        if problems:
            for problem in problems:
                print(problem, file=sys.stderr)
            print("generated status files are not current; run python -I -X utf8 scripts/build_status.py --write", file=sys.stderr)
            return 1
        print("generated status files are current (%d files checked)" % len(files))
        return 0
    except GitError as exc:
        print("build_status.py: %s" % exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
