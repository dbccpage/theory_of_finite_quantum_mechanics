"""Generate the project status page and the daily digests under docs/status/.

AuthorityEffect: None. This script reports counts and changes that it computes from
`dag/derivation_dag.json`, `dag/pfp/campaign/LOG.md` and the git history. It adds no
result and promotes no status.

    python -I -X utf8 scripts/build_status.py --write              # docs/status/README.md, daily/*.md
    python -I -X utf8 scripts/build_status.py --write --with-prs   # also list open pull requests (needs gh)
    python -I -X utf8 scripts/build_status.py --check              # exit 1 if docs/status/README.md is stale

What is generated
-----------------
docs/status/README.md
    Node counts by status and by stage, the most recently changed nodes (from the history of the DAG
    file), the campaign log, and links. Everything in it is a function of the working-tree DAG, the
    campaign log and the first-parent history of the DAG file. It contains no date, no commit hash of
    the checked-out revision and no clock reading, so `--check` is stable for a given repository state.
    The one exception is the open-pull-request block between the `prs` markers: it depends on GitHub at
    build time, so `--write --with-prs` fills it and `--check` ignores it.
docs/status/daily/<YYYY-MM-DD>.md and docs/status/daily/index.md
    One digest per UTC day in a window that ends at `--as-of` (default: the UTC date of the newest
    commit): the first-parent commits of that day by subject, the DAG nodes whose status or statement
    differs between the end of the previous day and the end of that day, and the campaign log lines
    added in the same interval. A digest is a function of the git history alone, so the daily
    workflow can regenerate the whole window without committing anything to main.

Shallow clones cannot supply the history; the workflow checks out with `fetch-depth: 0`.
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

ROOT = Path(__file__).resolve().parents[1]
DAG_PATH = "dag/derivation_dag.json"
LOG_PATH = "dag/pfp/campaign/LOG.md"
CAMPAIGN_README = "dag/pfp/campaign/README.md"
OUT_DIR = "docs/status"
REPO_URL = "https://github.com/dbccpage/theory_of_finite_quantum_mechanics"
BLOB = REPO_URL + "/blob/main/"
PRS_BEGIN = "<!-- prs:begin -->"
PRS_END = "<!-- prs:end -->"
PRS_PLACEHOLDER = "Open pull requests are listed when the page is built by the daily workflow."
LOG_LINE = re.compile(r"^\d{4}-\d{2}-\d{2}\s*\|")
RECENT_DAG_COMMITS = 12      # commits of the DAG file examined for "most recently changed nodes"
RECENT_NODES_SHOWN = 15
DEFAULT_DAYS = 14

STATUS_ORDER = ("PROVED_LEAN", "PROVED_PROSE", "COMPUTATIONALLY_CHECKED", "CONDITIONAL", "IMPORTED_ASSUMPTION",
                "DEFINITION", "ADMITTED_PRIMITIVE", "SOURCE_RECORD", "OPEN", "REFUTED")
STAGE_COLUMNS = (("PROVED_LEAN", "Lean"), ("PROVED_PROSE", "Prose"), ("COMPUTATIONALLY_CHECKED", "Comp. checked"),
                 ("CONDITIONAL", "Conditional"), ("IMPORTED_ASSUMPTION", "Imported"), ("OPEN", "Open"))


# ----------------------------------------------------------------------------- helpers

def git(*args: str, check: bool = True) -> str:
    proc = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=False)
    if check and proc.returncode != 0:
        raise RuntimeError("git %s failed: %s" % (" ".join(args), proc.stderr.decode("utf-8", "replace").strip()))
    return proc.stdout.decode("utf-8", "replace") if proc.returncode == 0 else ""


def esc(text: str, limit: int | None = None) -> str:
    """Make text safe inside a Markdown table cell and a Liquid-processed page."""
    text = " ".join(str(text).split())
    if limit is not None and len(text) > limit:
        text = text[: limit - 1].rstrip() + "…"
    return text.replace("|", "\\|").replace("{{", "{ {").replace("{%", "{ %").replace("<", "&lt;")


def blob(rel: str, label: str | None = None) -> str:
    return "[`%s`](%s%s)" % (label or rel, BLOB, rel)


def normalise_eol(text: str) -> str:
    return text.replace("\r\n", "\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))


# ----------------------------------------------------------------------------- git history

class Commit:
    __slots__ = ("sha", "when", "subject")

    def __init__(self, sha: str, when: dt.datetime, subject: str):
        self.sha, self.when, self.subject = sha, when, subject

    @property
    def short(self) -> str:
        return self.sha[:9]


def first_parent_commits(rev: str, *paths: str, limit: int | None = None) -> list[Commit]:
    args = ["log", "--first-parent", "--format=%H%x1f%cI%x1f%s"]
    if limit:
        args.append("--max-count=%d" % limit)
    args.append(rev)
    if paths:
        args += ["--", *paths]
    rows = []
    for line in git(*args).splitlines():
        sha, when, subject = line.split("\x1f", 2)
        rows.append(Commit(sha, dt.datetime.fromisoformat(when).astimezone(dt.timezone.utc), subject))
    return rows


_node_cache: dict[str, dict] = {}


def nodes_of(doc: dict) -> dict[str, dict]:
    return {n["id"]: {"status": n.get("status", ""), "statement": n.get("statement") or "", "stage": n.get("stage", "")}
            for n in doc.get("nodes", [])}


def nodes_at(sha: str | None) -> dict[str, dict]:
    if sha is None:
        return {}
    if sha not in _node_cache:
        text = git("show", "%s:%s" % (sha, DAG_PATH), check=False)
        _node_cache[sha] = nodes_of(json.loads(text)) if text else {}
    return _node_cache[sha]


def diff_nodes(old: dict[str, dict], new: dict[str, dict]) -> list[tuple[str, str, str, str]]:
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


def log_lines_at(sha: str | None) -> list[str]:
    if sha is None:
        return []
    return [line.strip() for line in git("show", "%s:%s" % (sha, LOG_PATH), check=False).splitlines() if LOG_LINE.match(line)]


# ----------------------------------------------------------------------------- status page

def counts(nodes: dict[str, dict]) -> tuple[collections.Counter, dict[str, collections.Counter]]:
    by_status: collections.Counter = collections.Counter()
    by_stage: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    for node in nodes.values():
        by_status[node["status"]] += 1
        by_stage[node["stage"]][node["status"]] += 1
    return by_status, by_stage


def status_order(by_status: collections.Counter) -> list[str]:
    return [s for s in STATUS_ORDER if s in by_status] + sorted(s for s in by_status if s not in STATUS_ORDER)


def recent_changes(rev: str) -> list[dict]:
    """Latest change per node over the last RECENT_DAG_COMMITS commits of the DAG file."""
    commits = first_parent_commits(rev, DAG_PATH, limit=RECENT_DAG_COMMITS + 1)
    latest: dict[str, dict] = {}
    for newer, older in zip(commits, commits[1:]):   # newest pair first, so the first sighting is the latest change
        for node_id, kind, before, after in diff_nodes(nodes_at(older.sha), nodes_at(newer.sha)):
            if node_id not in latest:
                latest[node_id] = {"id": node_id, "kind": kind, "before": before, "after": after, "commit": newer}
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


def prs_block(with_prs: bool) -> str:
    if not with_prs:
        return PRS_PLACEHOLDER
    try:
        out = subprocess.run(["gh", "pr", "list", "--state", "open", "--limit", "40", "--json",
                              "number,title,author,isDraft,updatedAt,url"], cwd=ROOT, capture_output=True, check=True, timeout=60)
        prs = json.loads(out.stdout.decode("utf-8"))
    except (OSError, subprocess.SubprocessError, ValueError):
        return "Open pull requests could not be listed at build time."
    if not prs:
        return "There are no open pull requests."
    prs.sort(key=lambda p: p["number"], reverse=True)
    lines = ["| PR | Title | Author | State | Updated (UTC) |", "|---|---|---|---|---|"]
    for pr in prs:
        lines.append("| [#%d](%s) | %s | %s | %s | %s |" % (
            pr["number"], pr["url"], esc(pr["title"], 110), esc((pr.get("author") or {}).get("login", "")),
            "draft" if pr.get("isDraft") else "ready", pr["updatedAt"][:10]))
    return "\n".join(lines)


def campaign_section() -> list[str]:
    lines = ["## Derivation campaign", ""]
    log = ROOT / LOG_PATH
    if not (ROOT / CAMPAIGN_README).is_file():
        lines += ["The derivation campaign, a ranked queue of unattempted targets with a per-target protocol, is proposed in "
                  "[pull request #180](%s/pull/180) and is not yet on `main`." % REPO_URL, ""]
        return lines
    entries = []
    if log.is_file():
        entries = [l.strip() for l in normalise_eol(log.read_text(encoding="utf-8")).splitlines() if LOG_LINE.match(l)]
    lines += ["The protocol is %s and the log is %s." % (blob(CAMPAIGN_README), blob(LOG_PATH)), ""]
    if not entries:
        lines += ["The log has no entries yet.", ""]
    else:
        lines += ["Targets recorded in the log: %d. Latest entries:" % len(entries), ""]
        lines += ["- %s" % esc(e, 240) for e in entries[-5:][::-1]]
        lines.append("")
    return lines


def build_readme(rev: str, with_prs: bool) -> str:
    doc = json.loads(normalise_eol((ROOT / DAG_PATH).read_text(encoding="utf-8")))
    nodes = nodes_of(doc)
    legend = doc.get("status_legend", {})
    by_status, by_stage = counts(nodes)
    out: list[str] = []
    out += ["# Where the project stands", "",
            "This page is generated by `scripts/build_status.py` from the derivation DAG, the campaign log and the git history. "
            "It reports; it does not argue. Daily digests are in [the digest index](daily/index.md).", "",
            "## How to read the numbers", "",
            "- A status label is only as strong as its evidence. `PROVED_LEAN` means a named Lean declaration exists in the "
            "checkout and the source cites it. It does not mean that every node with that label was re-elaborated for this page, "
            "and a node count is not a count of theorems.",
            "- `COMPUTATIONALLY_CHECKED` means an exact finite computation exists. It is not a proof of a general statement.",
            "- `CONDITIONAL` and `IMPORTED_ASSUMPTION` nodes depend on structure that is supplied, not derived.",
            "- Labels have been lowered in the past when review found them too strong. The record of those cases is in the "
            "%s section “How claims are kept honest”." % blob("README.md"),
            "- The per-node evidence pages are being built; see [the evidence map (in progress)](../evidence/README.md).", "",
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
    stage_names = [s for s in doc.get("stages", []) if s in by_stage] + sorted(s for s in by_stage if s not in doc.get("stages", []))
    for stage in stage_names:
        row = by_stage[stage]
        shown = [row.get(key, 0) for key, _ in STAGE_COLUMNS]
        other = sum(row.values()) - sum(shown)
        out.append("| `%s` | %d | %s | %d |" % (stage, sum(row.values()), " | ".join(str(v) for v in shown), other))
    out += ["", "## Most recently changed nodes", ""]
    try:
        changes = recent_changes(rev)
        note = ("The latest change per node over the last %d commits of `%s`, newest first. Only status and statement changes "
                "are listed; edits to other fields are not." % (RECENT_DAG_COMMITS, DAG_PATH))
    except RuntimeError as exc:
        changes, note = [], "The git history is not available to this build (%s)." % esc(str(exc), 120)
    out += [note, ""]
    if changes:
        out += ["| Node | Stage | Change | Commit | Date (UTC) | Subject |", "|---|---|---|---|---|---|"]
        for row in changes:
            node = nodes.get(row["id"])
            out.append("| `%s` | %s | %s | [`%s`](%s/commit/%s) | %s | %s |" % (
                row["id"], "`%s`" % node["stage"] if node else "", describe_change(row), row["commit"].short, REPO_URL,
                row["commit"].sha, row["commit"].when.strftime("%Y-%m-%d"), esc(row["commit"].subject, 100)))
        out.append("")
    out += campaign_section()
    out += ["## Open pull requests", "", PRS_BEGIN, prs_block(with_prs), PRS_END, "",
            "## Links", "",
            "- [Project landing page](../index.md)",
            "- [The evidence map (in progress)](../evidence/README.md)",
            "- %s: three ways to help" % blob("CONTRIBUTING.md"),
            "- %s: how a review works and how credit is given" % blob("REVIEWING.md"),
            "- [Example prompts](../contribute/example_prompts.md) that anyone can run",
            "- [Reviewer credit list](../reviewers.md)",
            "- %s: how the DAG is built" % blob("dag/derivation_dag_reading_note.md")]
    return "\n".join(out)


# ----------------------------------------------------------------------------- digests

def render_digest(day: dt.date, commits: list[Commit], window_commits: list[Commit]) -> tuple[str, dict]:
    start = dt.datetime.combine(day, dt.time(0, 0), tzinfo=dt.timezone.utc)
    end = start + dt.timedelta(days=1)
    in_day = [c for c in window_commits if start <= c.when < end]
    base = next((c for c in window_commits if c.when < start), None)
    head = next((c for c in window_commits if c.when < end), None)
    stats = {"commits": len(in_day), "node_changes": 0}
    out = ["# Status digest: %s" % day.isoformat(), "",
           "Generated by `scripts/build_status.py`. Interval: first-parent commits with a committer date on %s (UTC)." % day.isoformat()]
    if head is not None:
        out[-1] += " Last commit at the end of the interval: [`%s`](%s/commit/%s)." % (head.short, REPO_URL, head.sha)
    out += ["", "## Merged commits (%d)" % len(in_day), ""]
    out += ["- [`%s`](%s/commit/%s) %s" % (c.short, REPO_URL, c.sha, esc(c.subject, 200)) for c in in_day] or ["No commits on this date."]
    out.append("")
    if head is not None and (base is None or base.sha != head.sha):
        changes = diff_nodes(nodes_at(base.sha if base else None), nodes_at(head.sha))
        stats["node_changes"] = len(changes)
        out += ["## DAG nodes whose status or statement changed (%d)" % len(changes), ""]
        if changes:
            kinds = collections.Counter(kind for _, kind, _, _ in changes)
            summary = ", ".join("%d %s" % (kinds[k], k) for k in ("added", "status", "statement", "removed") if kinds[k])
            out += ["Compared with the DAG at the end of the previous day: %s. A statement change is listed by id only; "
                    "the diff is in the commit." % summary, "",
                    "| Node | Change | Status before | Status after |", "|---|---|---|---|"]
            changes.sort(key=lambda r: (r[1] == "added", r[0]))   # status and statement changes first
            shown = changes[:60]
            out += ["| `%s` | %s | %s | %s |" % (i, kind, "`%s`" % b if b else "", "`%s`" % a if a else "") for i, kind, b, a in shown]
            if len(changes) > len(shown):
                out.append("")
                out.append("%d further changes are not listed." % (len(changes) - len(shown)))
        else:
            out.append("No node changed status or statement.")
        out.append("")
        old_log, new_log = set(log_lines_at(base.sha if base else None)), log_lines_at(head.sha)
        added = [l for l in new_log if l not in old_log]
        out += ["## New campaign log lines (%d)" % len(added), ""]
        out += ["- %s" % esc(l, 300) for l in added] or ["None."]
        out.append("")
        by_status, _ = counts(nodes_at(head.sha))
        if by_status:
            out += ["## Counts at the end of the interval", "",
                    "Nodes: %d. " % sum(by_status.values()) + ", ".join("%s %d" % (s, by_status[s]) for s in status_order(by_status)) + ".", ""]
    else:
        out += ["## DAG nodes whose status or statement changed (0)", "", "No node changed status or statement.", "",
                "## New campaign log lines (0)", "", "None.", ""]
    return "\n".join(out), stats


def build_digests(rev: str, as_of: dt.date | None, days: int) -> dict[str, str]:
    commits = first_parent_commits(rev)
    if not commits:
        return {}
    last = as_of or max(c.when for c in commits).date()
    files, rows = {}, []
    for offset in range(days):
        day = last - dt.timedelta(days=offset)
        text, stats = render_digest(day, commits, commits)
        files["%s/daily/%s.md" % (OUT_DIR, day.isoformat())] = text
        rows.append((day, stats))
    index = ["# Daily digests", "",
             "One page per UTC day for the last %d days, newest first. Each page is generated from the git history by "
             "`scripts/build_status.py`; a day with no commits says so. The overview is [where the project stands](../README.md)." % days, "",
             "| Date (UTC) | Commits | Nodes changed in status or statement |", "|---|---:|---:|"]
    index += ["| [%s](%s.md) | %d | %d |" % (d.isoformat(), d.isoformat(), s["commits"], s["node_changes"]) for d, s in rows]
    files["%s/daily/index.md" % OUT_DIR] = "\n".join(index) + "\n"
    return files


# ----------------------------------------------------------------------------- main

def normalise_prs(text: str) -> str:
    pattern = re.compile(re.escape(PRS_BEGIN) + r".*?" + re.escape(PRS_END), re.S)
    return pattern.sub(PRS_BEGIN + "\n" + PRS_PLACEHOLDER + "\n" + PRS_END, normalise_eol(text))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="write docs/status/README.md and the daily digests")
    mode.add_argument("--check", action="store_true", help="exit 1 if docs/status/README.md is not current")
    parser.add_argument("--with-prs", action="store_true", help="list open pull requests through gh (skipped if gh is unavailable)")
    parser.add_argument("--rev", default="HEAD", help="revision whose first-parent history is used (default HEAD)")
    parser.add_argument("--as-of", default=None, help="last digest date, YYYY-MM-DD (default: UTC date of the newest commit)")
    parser.add_argument("--days", type=int, default=DEFAULT_DAYS, help="number of daily digests (default %d)" % DEFAULT_DAYS)
    args = parser.parse_args(argv)
    readme_path = ROOT / OUT_DIR / "README.md"
    readme = build_readme(args.rev, args.with_prs) + "\n"
    if args.check:
        if not readme_path.is_file():
            print("docs/status/README.md is missing; run scripts/build_status.py --write", file=sys.stderr)
            return 1
        if normalise_prs(readme_path.read_text(encoding="utf-8")) != normalise_prs(readme):
            print("docs/status/README.md is stale; run python -I -X utf8 scripts/build_status.py --write", file=sys.stderr)
            return 1
        print("docs/status/README.md is current")
        return 0
    as_of = dt.date.fromisoformat(args.as_of) if args.as_of else None
    write_text(readme_path, readme)
    digests = build_digests(args.rev, as_of, args.days)
    for rel, text in digests.items():
        write_text(ROOT / rel, text if text.endswith("\n") else text + "\n")
    print("wrote docs/status/README.md and %d digest files" % len(digests))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
