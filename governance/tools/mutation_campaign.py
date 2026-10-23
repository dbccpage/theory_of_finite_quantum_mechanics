"""Mechanical mutation campaign for the governance crate (SCORING.md section 3.4).

Every occurrence of a listed operator in the non-test part of each source file
(the text before its `#[cfg(test)]` line; comments, attributes and `use` lines
skipped) becomes one mutant. Each mutant is applied to a private copy of the
crate and the crate's own tests are run:

* lib modules: `cargo test --lib`; the binary: `cargo test --bin governance-check`.
* outcome KILLED (tests fail), SURVIVED (tests pass), INVALID (does not compile),
  INCONCLUSIVE (timeout). No mutant is classed as equivalent, so the ratio is the
  conservative R = killed / (killed + survived + inconclusive + unrun).

Usage: python -I -X utf8 governance/tools/mutation_campaign.py CRATE_DIR OUT_JSON [--workers N] [--scratch DIR]
No network access and no model calls; cargo runs with --offline --locked.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

OPERATORS = [
    ("eq->ne", re.compile(r"(?<![=!<>])==(?!=)"), "!="),
    ("ne->eq", re.compile(r"!="), "=="),
    ("lt->le", re.compile(r"(?<= )<(?= )"), "<="),
    ("le->lt", re.compile(r"(?<= )<=(?= )"), "<"),
    ("gt->ge", re.compile(r"(?<= )>(?= )"), ">="),
    ("ge->gt", re.compile(r"(?<= )>=(?= )"), ">"),
    ("and->or", re.compile(r"(?<= )&&(?= )"), "||"),
    ("or->and", re.compile(r"(?<= )\|\|(?= )"), "&&"),
    ("true->false", re.compile(r"\btrue\b"), "false"),
    ("false->true", re.compile(r"\bfalse\b"), "true"),
    ("is_some->is_none", re.compile(r"\.is_some\(\)"), ".is_none()"),
    ("is_none->is_some", re.compile(r"\.is_none\(\)"), ".is_some()"),
    ("any->all", re.compile(r"\.any\("), ".all("),
    ("all->any", re.compile(r"\.all\("), ".any("),
    ("min->max", re.compile(r"\.min\(\)"), ".max()"),
    ("first->last", re.compile(r"\.first\(\)"), ".last()"),
    ("not-removed", re.compile(r"(?<=[ (])!(?=[a-z_(])"), ""),
    ("is_empty-negated", re.compile(r"(?<=[ (])(?=[a-z_.]+\.is_empty\(\))"), "!"),
]
SKIP = re.compile(r"^\s*(//|#\[|#!|use |pub use |mod |pub mod )")


def mutants(crate: Path):
    for path in sorted((crate / "src").rglob("*.rs")):
        rel = path.relative_to(crate).as_posix()
        lines = path.read_text(encoding="utf-8").split("\n")
        end = next((i for i, line in enumerate(lines) if line.strip() == "#[cfg(test)]"), len(lines))
        for number, line in enumerate(lines[:end], start=1):
            if SKIP.match(line) or '"' in line and line.strip().startswith('"'):
                continue
            for name, pattern, replacement in OPERATORS:
                for match in pattern.finditer(line):
                    if line.count('"', 0, match.start()) % 2:
                        continue  # inside a string literal
                    mutated = line[:match.start()] + replacement + line[match.end():]
                    yield {"file": rel, "line": number, "operator": name, "original": line.strip(), "mutated": mutated.strip(),
                           "_full": (path, number, mutated)}


def run_one(item, crate: Path, scratch: Path, timeout: int):
    worker = scratch / ("w%d" % os.getpid())
    copy = worker / "gov"
    if not copy.exists():
        shutil.copytree(crate, copy, ignore=shutil.ignore_patterns("target"))
    path, number, mutated = item["_full"]
    rel = path.relative_to(crate)
    target_file = copy / rel
    original = path.read_text(encoding="utf-8")
    lines = original.split("\n")
    lines[number - 1] = mutated
    target_file.write_text("\n".join(lines), encoding="utf-8", newline="")
    env = dict(os.environ, CARGO_TARGET_DIR=str(worker / "target"), CARGO_INCREMENTAL="1", CARGO_PROFILE_DEV_DEBUG="0")
    selector = ["--bin", "governance-check"] if rel.as_posix().startswith("src/bin/") else ["--lib"]
    started = time.time()
    try:
        proc = subprocess.run(["cargo", "test", "--offline", "--locked", "-q", "--manifest-path", str(copy / "Cargo.toml"), *selector],
                              capture_output=True, text=True, env=env, timeout=timeout)
        out = proc.stdout + proc.stderr
        if proc.returncode == 0:
            outcome = "SURVIVED"
        elif "could not compile" in out or re.search(r"error\[E\d+\]", out):
            outcome = "INVALID"
        else:
            outcome = "KILLED"
    except subprocess.TimeoutExpired:
        outcome = "INCONCLUSIVE"
    finally:
        target_file.write_text(original, encoding="utf-8", newline="")
    result = {k: v for k, v in item.items() if not k.startswith("_")}
    result.update({"outcome": outcome, "seconds": round(time.time() - started, 1)})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("crate", type=Path)
    parser.add_argument("out", type=Path)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--scratch", type=Path, default=Path("C:/gt/mut"))
    parser.add_argument("--timeout", type=int, default=240)
    args = parser.parse_args()
    crate = args.crate.resolve()
    items = list(mutants(crate))
    print("mutants:", len(items), flush=True)
    results = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(run_one, item, crate, args.scratch, args.timeout) for item in items]
        for done, future in enumerate(concurrent.futures.as_completed(futures), start=1):
            results.append(future.result())
            if done % 10 == 0:
                print("done", done, flush=True)
    results.sort(key=lambda r: (r["file"], r["line"], r["operator"], r["mutated"]))
    sources = {p.relative_to(crate).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((crate / "src").rglob("*.rs"))}
    summary = {}
    for r in results:
        per = summary.setdefault(r["file"], {"KILLED": 0, "SURVIVED": 0, "INVALID": 0, "INCONCLUSIVE": 0, "UNRUN": 0, "EQUIVALENT": 0})
        per[r["outcome"]] += 1
    for per in summary.values():
        denominator = per["KILLED"] + per["SURVIVED"] + per["INCONCLUSIVE"] + per["UNRUN"]
        per["conservative_ratio"] = round(per["KILLED"] / denominator, 4) if denominator else None
    report = {"schema": "tfqm.mutation-campaign.v1", "AuthorityEffect": "None", "tool": "governance/tools/mutation_campaign.py",
              "rule": "R = killed / (killed + survived + inconclusive + unrun); no mutant classed equivalent",
              "rustc": subprocess.run(["rustc", "--version"], capture_output=True, text=True).stdout.strip(),
              "sources": sources, "summary": summary, "mutants": results}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    sys.exit(main())
