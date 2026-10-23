"""Sequential, recoverable mutation of the existing governance sources.

One exclusive lease protects a campaign. A single-file recovery journal precedes
an edit; original bytes are restored after each test. Interrupted or conflicting
edits retain the journal and lease for manual recovery. No crate is copied.
Lexical candidates are not an AST enumeration; compiler rejection is INVALID.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from enum import Enum
from pathlib import Path
from typing import Iterator

# The CLI runs with -I; import the sibling module by its known local path.
import importlib.util
_spec = importlib.util.spec_from_file_location("capture_evidence", Path(__file__).with_name("capture_evidence.py"))
if _spec is None or _spec.loader is None:
    raise RuntimeError("missing evidence runner")
capture = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = capture
_spec.loader.exec_module(capture)

MAX_MUTANTS = 512
MAX_LOG_TOTAL = 32 * 1024 * 1024

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


class Outcome(str, Enum):
    KILLED = "KILLED"
    SURVIVED = "SURVIVED"
    INVALID = "INVALID"
    INCONCLUSIVE = "INCONCLUSIVE"
    UNRUN = "UNRUN"
    EQUIVALENT = "EQUIVALENT"


class RecoveryRequired(RuntimeError):
    """The lease and original bytes must be inspected before another campaign."""


@dataclass(frozen=True)
class Mutant:
    file: str
    line: int
    operator: str
    original: str
    mutated: str
    source_sha256: str


def mutants(crate: Path) -> Iterator[Mutant]:
    count = 0
    for path in sorted((crate / "src").rglob("*.rs")):
        if path.stat().st_size > capture.MAX_SOURCE:
            raise ValueError("mutation source exceeds the file bound")
        raw = path.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        lines = raw.decode("utf-8").splitlines(keepends=True)
        for number, line in enumerate(lines, start=1):
            if line.strip() == "#[cfg(test)]":
                break
            if SKIP.match(line) or line.strip().startswith('"'):
                continue
            for name, pattern, replacement in OPERATORS:
                for match in pattern.finditer(line):
                    if line.count('"', 0, match.start()) % 2:
                        continue
                    count += 1
                    if count > MAX_MUTANTS:
                        raise ValueError("mutation population exceeds 512; no candidates have run")
                    changed = line[:match.start()] + replacement + line[match.end():]
                    yield Mutant(path.relative_to(crate).as_posix(), number, name, line, changed, digest)


def classify_outcome(returncode: int, output: str) -> str:
    """Infrastructure failure never counts as a detected semantic fault."""
    if returncode == 0 and re.search(r"test result: ok\..* [1-9][0-9]* passed;", output):
        return Outcome.SURVIVED.value
    if returncode != 0 and re.search(r"test result: FAILED\..* [1-9][0-9]* failed;", output):
        return Outcome.KILLED.value
    if re.search(r"error\[E[0-9]+\]", output):
        return Outcome.INVALID.value
    return Outcome.INCONCLUSIVE.value


class MutationSession:
    """Cooperating-writer lease with durable one-file recovery bytes.

    This is not a filesystem transaction. Power loss requires manual recovery;
    foreign edits are never overwritten during restoration.
    """
    def __init__(self, crate: Path) -> None:
        self.crate = crate.resolve()
        self.lock = self.crate / ".mutation.lock"
        self.backup = self.crate / ".mutation.original"
        self.healthy = True
        self.owned = False
        self.before = capture.source_hashes(self.crate)

    def __enter__(self) -> MutationSession:
        if self.backup.exists():
            raise RecoveryRequired("an original-byte recovery journal already exists")
        with self.lock.open("x", encoding="utf-8") as stream:
            json.dump({"sources": self.before}, stream)
            stream.flush()
            os.fsync(stream.fileno())
        self.owned = True
        return self

    def __exit__(self, kind: object, value: object, trace: object) -> None:
        if self.healthy and self.owned and not self.backup.exists():
            self.lock.unlink()

    def apply(self, item: Mutant) -> tuple[Path, bytes, bytes]:
        if not self.owned or not self.healthy or capture.source_hashes(self.crate) != self.before:
            raise RecoveryRequired("source drift or inactive mutation lease")
        path = self.crate / item.file
        if not path.resolve().is_relative_to(self.crate) or path.is_symlink():
            raise ValueError("mutant source escapes the crate")
        original = path.read_bytes()
        if hashlib.sha256(original).hexdigest() != item.source_sha256:
            raise ValueError("mutant was generated for different bytes")
        lines = original.decode("utf-8").splitlines(keepends=True)
        if not 1 <= item.line <= len(lines) or lines[item.line - 1] != item.original:
            raise ValueError("mutant line no longer matches")
        lines[item.line - 1] = item.mutated
        changed = "".join(lines).encode("utf-8")
        self.healthy = False
        with self.backup.open("xb") as stream:
            stream.write(original)
            stream.flush()
            os.fsync(stream.fileno())
        # The lease contains the edited path and hashes needed for manual recovery.
        with self.lock.open("w", encoding="utf-8") as stream:
            json.dump({"path": item.file, "original_sha256": item.source_sha256,
                       "mutated_sha256": hashlib.sha256(changed).hexdigest()}, stream)
            stream.flush()
            os.fsync(stream.fileno())
        path.write_bytes(changed)
        return path, original, changed

    def restore(self, path: Path, original: bytes, changed: bytes) -> None:
        if path.read_bytes() != changed:
            raise RecoveryRequired("edited file changed during test; original journal and lease retained")
        path.write_bytes(original)
        if path.read_bytes() != original:
            raise RecoveryRequired("original-byte restoration failed")
        self.backup.unlink()
        self.healthy = True


def run_one(item: Mutant, session: MutationSession, log: Path, timeout: int) -> dict[str, object]:
    path, original, changed = session.apply(item)
    try:
        selector = ["--bin", "governance-check"] if item.file.startswith("src/bin/") else ["--lib"]
        result = capture.run(["cargo", "test", "--offline", "--locked", "-q", "--manifest-path",
                              str(capture.MANIFEST), *selector], capture.ROOT, capture.build_env(),
                             log, capture.Limits(timeout, 2 * 1024 * 1024))
    finally:
        session.restore(path, original, changed)
    outcome = Outcome.INCONCLUSIVE.value
    if result.state == capture.State.COMPLETED and result.exit_status is not None:
        outcome = classify_outcome(result.exit_status, capture.read_output(result))
    if capture.source_hashes(session.crate) != session.before:
        outcome = Outcome.INCONCLUSIVE.value
    return {**asdict(item), "outcome": outcome, "execution": asdict(result)}


def summarize(results: list[dict[str, object]]) -> dict[str, object]:
    counts = {outcome.value: 0 for outcome in Outcome}
    for result in results:
        counts[str(result["outcome"])] += 1
    denominator = sum(counts[x.value] for x in (Outcome.KILLED, Outcome.SURVIVED, Outcome.INCONCLUSIVE, Outcome.UNRUN))
    return {**counts, "eligible_denominator": denominator, "killed_numerator": counts["KILLED"],
            "conservative_ratio": f'{counts["KILLED"]}/{denominator}' if denominator else None}


def save_report(out: Path, report: dict[str, object]) -> None:
    temporary = out / "receipt.next"
    with temporary.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(report, indent=2) + "\n")
        stream.flush()
        os.fsync(stream.fileno())
    temporary.replace(out / "receipt.json")


def execute_items(items: list[Mutant], session: MutationSession, out: Path,
                  timeout: int, baseline: bool, report: dict[str, object]) -> list[dict[str, object]]:
    # baseline is stored as JSON; its passed flag is decided by the typed runner.
    results: list[dict[str, object]] = [{**asdict(item), "outcome": Outcome.UNRUN.value} for item in items]
    report["mutants"] = results
    save_report(out, report)
    budget = (out / "baseline.log").stat().st_size
    for index, item in enumerate(items):
        if not baseline or budget >= MAX_LOG_TOTAL:
            break
        try:
            results[index] = run_one(item, session, out / f"mutant-{index:04d}.log", timeout)
            budget += (out / f"mutant-{index:04d}.log").stat().st_size
        except (OSError, ValueError, RecoveryRequired, KeyboardInterrupt) as error:
            results[index] = {**asdict(item), "outcome": Outcome.INCONCLUSIVE.value, "error": str(error)}
            report["aborted"] = str(error)
            save_report(out, report)
            break
        save_report(out, report)
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("out", type=Path)
    parser.add_argument("--timeout", type=int, default=240)
    args = parser.parse_args()
    if not 1 <= args.timeout <= 3600:
        parser.error("timeout must be in 1..3600")
    out = args.out.resolve()
    try:
        items = list(mutants(capture.CRATE))
        out.mkdir(parents=True, exist_ok=True)
        # Refuse to overwrite evidence from any earlier campaign.
        with (out / "receipt.json").open("x", encoding="utf-8") as stream:
            json.dump({"phase": "preflight", "mutants": [{**asdict(i), "outcome": "UNRUN"} for i in items]}, stream)
        with MutationSession(capture.CRATE) as session:
            build = {"manifest": capture.sha(capture.MANIFEST), "lock": capture.sha(capture.MANIFEST.with_name("Cargo.lock"))}
            baseline = capture.run(["cargo", "test", "--offline", "--locked", "--manifest-path", str(capture.MANIFEST)],
                                   capture.ROOT, capture.build_env(), out / "baseline.log", capture.Limits(args.timeout))
            report: dict[str, object] = {"schema": "tfqm.mutation-campaign.v2", "AuthorityEffect": "None",
                "phase": "running", "baseline": asdict(baseline), "sources": session.before, "build_inputs": build,
                "tool_sources": {str(Path(__file__).relative_to(capture.ROOT)): capture.sha(Path(__file__)),
                                 "governance/tools/capture_evidence.py": capture.sha(Path(__file__).with_name("capture_evidence.py"))},
                "boundary": "Lexical candidates; cooperative writers; process output limits are polled."}
            results = execute_items(items, session, out, args.timeout, baseline.passed, report)
            unchanged = capture.source_hashes(capture.CRATE) == session.before
            unchanged = unchanged and build == {"manifest": capture.sha(capture.MANIFEST), "lock": capture.sha(capture.MANIFEST.with_name("Cargo.lock"))}
            if not unchanged:
                report["input_drift"] = True
                for record in results:
                    if record["outcome"] != "UNRUN":
                        record["outcome"] = "INCONCLUSIVE"
            report.update({"sources_unchanged": unchanged, "mutants": results, "summary": summarize(results), "phase": "finished"})
            save_report(out, report)
        return 0 if unchanged and baseline.passed and all(r["outcome"] in ("KILLED", "SURVIVED", "INVALID") for r in results) else 1
    except (OSError, ValueError, RecoveryRequired) as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
