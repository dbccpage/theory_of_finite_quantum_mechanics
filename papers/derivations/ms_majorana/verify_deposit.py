#!/usr/bin/env python3
"""Deposit admission certificate for the PO-026 Majorana package.

Origin: papers/derivations/ms_majorana/the_majorana_problem_claim_ledger.md
and papers/derivations/ms_majorana/SHA256SUMS.
Claim: urn:omega:fqm:ms-majorana:deposit-gate:v1
AuthorityEffect: None
Mutation-Kills: 18 non-equivalent source mutants, executed by
papers/derivations/ms_majorana/test_verify_deposit.py.
Scope Fence: this file does not claim Majorana hardware, physical anyons,
or Lean theoremhood, and it does not inherit vendor or manuscript authority.
A zero process code is not a physics result. This file does not prove the
monograph.

Deposit admission is the conjunction of seven decidable predicates on a
finite package: the required file set is present; SHA256SUMS is a bijection
from that set minus itself onto 64-hex SHA-256 digests of the file bytes;
.zenodo.json is an object whose required fields are nonempty and contain no
decimal token; claim_ledger.yaml carries exactly MAJ-C1 through MAJ-C20,
each of which occurs in the markdown ledger; the manuscript contains the
authority mark; the pytest runner returns code 0; the lake runner returns
code 0 and no sorry marker. DepositCertificate is the witness of that
conjunction. Package verification admits the deposit only by constructing
that witness.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO, NoReturn, cast


REQUIRED_FILES: tuple[str, ...] = (
    ".zenodo.json",
    "README.md",
    "SHA256SUMS",
    "claim_ledger.yaml",
    "code/majorana_evaluator.py",
    "code/tests/conftest.py",
    "code/tests/e2e/test_majorana_problem_e2e.py",
    "code/tests/integration/test_tetron_surface_codes.py",
    "code/tests/unit/test_gf2_trichotomy.py",
    "code/tests/unit/test_open_system_transfer_bounds.py",
    "lean4/AXIOM_REPORT.txt",
    "lean4/MajoranaCore.lean",
    "lean4/MajoranaGinCore.lean",
    "lean4/PROVENANCE.md",
    "lean4/README.md",
    "lean4/lake-manifest.json",
    "lean4/lakefile.lean",
    "lean4/lean-toolchain",
    "the_majorana_problem.md",
    "the_majorana_problem_change_log.md",
    "the_majorana_problem_claim_ledger.md",
    "verify_deposit.py",
)

CLAIM_LO = 1
CLAIM_HI = 20
AUTHORITY_MARK = "AuthorityEffect: None"
ZENODO_KEYS: tuple[str, ...] = (
    "title",
    "description",
    "creators",
    "access_right",
    "license",
    "keywords",
)
PYTEST_TARGETS: tuple[str, ...] = (
    "tests/unit/test_gf2_trichotomy.py",
    "tests/unit/test_open_system_transfer_bounds.py",
    "tests/integration/test_tetron_surface_codes.py",
    "tests/e2e/test_majorana_problem_e2e.py",
)

_CHECKSUM_LINE = re.compile(r"([0-9a-f]{64})  (.+)")
_DECIMAL_TEXT = re.compile(r"(^|[^0-9A-Za-z_])[0-9]+\.[0-9]+")
_CLAIM_LINE = re.compile(r'^\s+- (?:id|claim_id):\s+"?(MAJ-C[0-9]+)"?\s*$')

Runner = Callable[[Path], object]


class DepositGateError(Exception):
    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        stored: dict[str, object] = {} if parameters is None else dict(parameters)
        self.invariant = invariant
        self.parameters = stored
        super().__init__(_message(invariant, stored))


class DecimalRefused(DepositGateError):
    pass


class BooleanRefused(DepositGateError):
    pass


class IntegerRequired(DepositGateError):
    pass


class PaperPathInvalid(DepositGateError):
    pass


class UnreadableFile(DepositGateError):
    pass


class MissingRequiredFile(DepositGateError):
    pass


class MalformedChecksumRecord(DepositGateError):
    pass


class UnexpectedManifestPath(DepositGateError):
    pass


class DuplicateManifestPath(DepositGateError):
    pass


class EscapingManifestPath(DepositGateError):
    pass


class MissingManifestTarget(DepositGateError):
    pass


class HashMismatch(DepositGateError):
    pass


class ManifestInventoryMismatch(DepositGateError):
    pass


class ZenodoMetadataMissing(DepositGateError):
    pass


class ZenodoJsonUnreadable(DepositGateError):
    pass


class ZenodoFieldMissing(DepositGateError):
    pass


class ClaimIdSetMismatch(DepositGateError):
    pass


class ClaimIdAbsentFromMarkdown(DepositGateError):
    pass


class AuthorityEffectMissing(DepositGateError):
    pass


class PytestGateFailed(DepositGateError):
    pass


class LeanGateFailed(DepositGateError):
    pass


class CommandUnavailable(DepositGateError):
    pass


class CommandResultInvalid(DepositGateError):
    pass


class CertificateShape(DepositGateError):
    pass


def _render_parameters(parameters: Mapping[str, object]) -> str:
    return ", ".join(f"{key}={parameters[key]}" for key in parameters)


def _message(invariant: str, parameters: Mapping[str, object]) -> str:
    rendered = _render_parameters(parameters)
    if rendered == "":
        return invariant
    return invariant + " (" + rendered + ")"


def _is_binary64(value: object) -> bool:
    return value.__class__.__name__ == "float"


def _raise_rejected_int(value: object, role: str) -> None:
    if isinstance(value, bool):
        raise BooleanRefused(
            "boolean refused where an exact integer was required",
            {"role": role},
        )
    raise IntegerRequired(
        "exact integer required",
        {"role": role, "received": value.__class__.__name__},
    )


def require_exact_int(value: object, role: str) -> int:
    if _is_binary64(value):
        raise DecimalRefused(
            "decimal refused at the deposit boundary",
            {"role": role, "received": "decimal"},
        )
    if isinstance(value, bool) or not isinstance(value, int) or type(value) is not int:
        _raise_rejected_int(value, role)
    return cast(int, value)


def _require_text(value: object, role: str) -> str:
    if _is_binary64(value):
        raise DecimalRefused(
            "decimal refused at the deposit boundary",
            {"role": role, "received": "decimal"},
        )
    if type(value) is bool:
        raise BooleanRefused(
            "boolean refused where text was required",
            {"role": role},
        )
    if type(value) is not str:
        raise PaperPathInvalid(
            "path is not text",
            {"role": role, "received": value.__class__.__name__},
        )
    return value


def require_directory(paper_dir: object) -> Path:
    if isinstance(paper_dir, Path):
        candidate = paper_dir
    else:
        candidate = Path(_require_text(paper_dir, "paper_dir"))
    if not candidate.is_dir():
        raise PaperPathInvalid(
            "paper path is not a directory",
            {"path": str(candidate)},
        )
    return candidate


def _feed(digest: "hashlib._Hash", handle: BinaryIO) -> None:
    while True:
        chunk = handle.read(65536)
        if chunk == b"":
            return
        digest.update(chunk)


def sha256_file(filepath: object) -> str:
    path = _require_text(filepath, "filepath")
    digest = hashlib.sha256()
    try:
        handle = open(path, "rb")
    except OSError as exc:
        raise UnreadableFile(
            "file bytes are unreadable",
            {"path": path, "detail": exc.__class__.__name__},
        ) from exc
    with handle:
        _feed(digest, handle)
    return digest.hexdigest()


def _missing_required(paper_dir: Path) -> tuple[str, ...]:
    missing: list[str] = []
    for rel_path in REQUIRED_FILES:
        if not (paper_dir / rel_path).is_file():
            missing.append(rel_path)
    return tuple(missing)


def require_files(paper_dir: Path) -> int:
    missing = _missing_required(paper_dir)
    if len(missing) != 0:
        raise MissingRequiredFile(
            "required file is absent",
            {"missing": missing[0], "count": len(missing)},
        )
    return len(REQUIRED_FILES)


def parse_checksum_line(line: str) -> tuple[str, str] | None:
    if line.strip() == "" or line.startswith("#"):
        return None
    match = _CHECKSUM_LINE.fullmatch(line)
    if match is None:
        raise MalformedChecksumRecord(
            "checksum record is malformed",
            {"line": line[:64]},
        )
    return match.group(1), match.group(2)


def _expected_paths() -> frozenset[str]:
    return frozenset(path for path in REQUIRED_FILES if path != "SHA256SUMS")


def _anchored_target(base: Path, relative: str) -> Path:
    candidate = Path(relative)
    if candidate.is_absolute():
        raise EscapingManifestPath(
            "manifest path is absolute",
            {"path": relative},
        )
    resolved = base.resolve()
    target = (resolved / relative).resolve()
    if not target.is_relative_to(resolved):
        raise EscapingManifestPath(
            "manifest path escapes the package root",
            {"path": relative},
        )
    return target


def _require_manifest_file(target: Path, relative: str) -> None:
    if not target.is_file():
        raise MissingManifestTarget(
            "manifest target is not a file",
            {"path": relative},
        )


def _accept_parsed(
    base: Path,
    expected: frozenset[str],
    seen: set[str],
    parsed: tuple[str, str],
) -> None:
    digest, relative = parsed
    target = _anchored_target(base, relative)
    if relative not in expected:
        raise UnexpectedManifestPath(
            "manifest path is not in the required inventory",
            {"path": relative},
        )
    if relative in seen:
        raise DuplicateManifestPath(
            "manifest path is duplicated",
            {"path": relative},
        )
    _require_manifest_file(target, relative)
    actual = sha256_file(str(target))
    if actual != digest:
        raise HashMismatch(
            "sha256 digest does not match the manifest",
            {"path": relative},
        )
    seen.add(relative)


def _consume_line(base: Path, expected: frozenset[str], seen: set[str], line: str) -> None:
    parsed = parse_checksum_line(line)
    if parsed is None:
        return
    _accept_parsed(base, expected, seen, parsed)


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise UnreadableFile(
            "text file is unreadable",
            {"path": str(path), "detail": exc.__class__.__name__},
        ) from exc


def _require_same_inventory(expected: frozenset[str], seen: set[str]) -> int:
    if seen != expected:
        missing = sorted(expected - seen)
        first = missing[0] if missing else ""
        raise ManifestInventoryMismatch(
            "manifest inventory does not match the required set",
            {"missing": first, "count": len(expected - seen)},
        )
    return len(seen)


def require_manifest(paper_dir: Path) -> int:
    base = paper_dir.resolve()
    expected = _expected_paths()
    seen: set[str] = set()
    for line in _read_text(base / "SHA256SUMS").splitlines():
        _consume_line(base, expected, seen, line)
    return _require_same_inventory(expected, seen)


def _reject_decimal_token(token: str) -> NoReturn:
    raise DecimalRefused(
        "decimal refused in zenodo metadata",
        {"role": "zenodo", "received": "decimal"},
    )


def _load_json_exact(text: str) -> object:
    try:
        return json.loads(text, parse_float=_reject_decimal_token)
    except DecimalRefused:
        raise
    except json.JSONDecodeError as exc:
        raise ZenodoJsonUnreadable(
            "zenodo json is unreadable",
            {"detail": exc.__class__.__name__},
        ) from exc


def _field_empty(value: object) -> bool:
    if value is None:
        return True
    if type(value) is str:
        return value == ""
    if type(value) is list:
        return len(value) == 0
    if type(value) is dict:
        return len(value) == 0
    return False


def _require_zenodo_field(data: Mapping[str, object], key: str) -> None:
    if key not in data:
        raise ZenodoFieldMissing("zenodo field is absent", {"field": key})
    if _field_empty(data[key]):
        raise ZenodoFieldMissing("zenodo field is empty", {"field": key})


def _require_object(loaded: object) -> dict[str, object]:
    if type(loaded) is not dict:
        raise ZenodoFieldMissing(
            "zenodo document is not an object",
            {"received": loaded.__class__.__name__},
        )
    document: dict[str, object] = {}
    for key, value in loaded.items():
        if type(key) is not str:
            raise ZenodoFieldMissing(
                "zenodo field name is not text",
                {"received": key.__class__.__name__},
            )
        document[key] = value
    return document


def require_zenodo(paper_dir: Path) -> int:
    path = paper_dir / ".zenodo.json"
    if not path.is_file():
        raise ZenodoMetadataMissing(
            "zenodo metadata is absent",
            {"path": ".zenodo.json"},
        )
    document = _require_object(_load_json_exact(_read_text(path)))
    for key in ZENODO_KEYS:
        _require_zenodo_field(document, key)
    return len(ZENODO_KEYS)


def expected_claim_ids() -> tuple[str, ...]:
    return tuple(f"MAJ-C{index}" for index in range(CLAIM_LO, CLAIM_HI + 1))


def _claim_id_from_line(line: str) -> str | None:
    if _DECIMAL_TEXT.search(line) is not None:
        raise DecimalRefused(
            "decimal refused in claim ledger text",
            {"role": "claim_ledger", "received": "decimal"},
        )
    match = _CLAIM_LINE.match(line)
    if match is None:
        return None
    return match.group(1)


def parse_claim_ids(text: object) -> tuple[str, ...]:
    body = _require_text(text, "claim_ledger")
    found: list[str] = []
    for line in body.splitlines():
        claim_id = _claim_id_from_line(line)
        if claim_id is not None:
            found.append(claim_id)
    return tuple(found)


def _require_claim_set(ids: tuple[str, ...]) -> int:
    if len(ids) != len(set(ids)):
        raise ClaimIdSetMismatch("claim ids are not unique", {"count": len(ids)})
    expected = expected_claim_ids()
    if set(ids) != set(expected):
        raise ClaimIdSetMismatch(
            "claim id set is not MAJ-C1 through MAJ-C20",
            {"count": len(ids), "expected": len(expected)},
        )
    return len(ids)


def _require_markdown_claim(markdown: str, claim_id: str) -> None:
    pattern = "(?<![A-Za-z0-9_-])" + re.escape(claim_id) + "(?![A-Za-z0-9_-])"
    if re.search(pattern, markdown) is None:
        raise ClaimIdAbsentFromMarkdown(
            "claim id is absent from the markdown ledger",
            {"claim_id": claim_id},
        )


def require_claim_ledger(paper_dir: Path) -> int:
    ids = parse_claim_ids(_read_text(paper_dir / "claim_ledger.yaml"))
    count = _require_claim_set(ids)
    markdown = _read_text(paper_dir / "the_majorana_problem_claim_ledger.md")
    for claim_id in ids:
        _require_markdown_claim(markdown, claim_id)
    return count


def require_authority_mark(manuscript: object) -> str:
    text = _require_text(manuscript, "manuscript")
    if AUTHORITY_MARK not in text:
        raise AuthorityEffectMissing(
            "manuscript lacks AuthorityEffect: None",
            {"mark": AUTHORITY_MARK},
        )
    return "None"


@dataclass(frozen=True)
class CommandResult:
    code: int
    output: str

    def __post_init__(self) -> None:
        require_exact_int(self.code, "command_code")
        if type(self.output) is not str:
            raise CommandResultInvalid(
                "command output is not text",
                {"received": self.output.__class__.__name__},
            )


def _require_zero_code(code: int, error: type[DepositGateError], invariant: str) -> int:
    checked = require_exact_int(code, invariant)
    if checked != 0:
        raise error(invariant, {"code": checked})
    return checked


def require_pytest_result(result: CommandResult) -> int:
    return _require_zero_code(result.code, PytestGateFailed, "pytest exit code is not zero")


def _reject_sorry_marker(output: str, code: int) -> None:
    if "sorryAx" in output:
        raise LeanGateFailed("lean output contains sorryAx", {"code": code})
    if "declaration uses 'sorry'" in output:
        raise LeanGateFailed(
            "lean output contains a sorry declaration",
            {"code": code},
        )


def require_lake_result(result: CommandResult) -> int:
    code = _require_zero_code(result.code, LeanGateFailed, "lake exit code is not zero")
    _reject_sorry_marker(result.output, code)
    return code


def pytest_command(executable: str, basetemp: str) -> tuple[str, ...]:
    prefix = (
        executable,
        "-m",
        "pytest",
        "-n",
        "8",
        "-q",
        "-p",
        "no:cacheprovider",
        "--basetemp=" + basetemp,
        "--cov=majorana_evaluator",
        "--cov-fail-under=95",
    )
    return prefix + PYTEST_TARGETS


def _pytest_env(coverage_file: str) -> dict[str, str]:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["COVERAGE_FILE"] = coverage_file
    return env


def run_command(
    command: tuple[str, ...],
    cwd: Path,
    env: Mapping[str, str] | None = None,
) -> CommandResult:
    if len(command) == 0:
        raise CommandUnavailable("command is empty", {"command": ""})
    merged = None if env is None else dict(env)
    try:
        completed = subprocess.run(
            list(command),
            cwd=cwd,
            env=merged,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except OSError as exc:
        raise CommandUnavailable(
            "command could not be started",
            {"command": command[0], "detail": exc.__class__.__name__},
        ) from exc
    output = completed.stdout + completed.stderr
    return CommandResult(code=completed.returncode, output=output)


def default_pytest_runner(paper_dir: Path) -> CommandResult:
    with tempfile.TemporaryDirectory(prefix="coda-maj-verify-") as scratch:
        coverage = str(Path(scratch) / ".coverage")
        basetemp = str(Path(scratch) / "pytest")
        command = pytest_command(sys.executable, basetemp)
        return run_command(command, paper_dir / "code", _pytest_env(coverage))


def default_lake_runner(paper_dir: Path) -> CommandResult:
    return run_command(("lake", "build"), paper_dir / "lean4", None)


def select_runner(runner: Runner | None, default: Runner) -> Runner:
    if runner is None:
        return default
    return runner


def _invoke(runner: Runner, paper_dir: Path) -> CommandResult:
    result = runner(paper_dir)
    if type(result) is not CommandResult:
        raise CommandResultInvalid(
            "runner did not return a command result",
            {"received": result.__class__.__name__},
        )
    return result


@dataclass(frozen=True)
class DepositCertificate:
    file_count: int
    digest_count: int
    claim_count: int
    pytest_code: int
    lake_code: int
    authority_effect: str

    def __post_init__(self) -> None:
        _require_certificate_law(
            self.file_count,
            self.digest_count,
            self.claim_count,
            self.pytest_code,
            self.lake_code,
            self.authority_effect,
        )


def _require_authority_witness(authority_effect: object) -> None:
    if type(authority_effect) is not str or authority_effect != "None":
        received = authority_effect if type(authority_effect) is str else authority_effect.__class__.__name__
        raise CertificateShape(
            "authority effect witness is not None",
            {"received": received},
        )


def _require_count_law(file_count: int, digest_count: int, claim_count: int) -> None:
    if file_count != len(REQUIRED_FILES):
        raise CertificateShape(
            "file witness is not the required inventory",
            {"count": file_count},
        )
    if digest_count != len(_expected_paths()):
        raise CertificateShape(
            "digest witness is not the manifest inventory",
            {"count": digest_count},
        )
    if claim_count != len(expected_claim_ids()):
        raise CertificateShape(
            "claim witness is not MAJ-C1 through MAJ-C20",
            {"count": claim_count},
        )


def _require_process_law(pytest_code: int, lake_code: int) -> None:
    if pytest_code != 0:
        raise CertificateShape("pytest witness is not zero", {"code": pytest_code})
    if lake_code != 0:
        raise CertificateShape("lake witness is not zero", {"code": lake_code})


def _require_certificate_law(
    file_count: object,
    digest_count: object,
    claim_count: object,
    pytest_code: object,
    lake_code: object,
    authority_effect: object,
) -> None:
    files = require_exact_int(file_count, "file_count")
    digests = require_exact_int(digest_count, "digest_count")
    claims = require_exact_int(claim_count, "claim_count")
    pytest_witness = require_exact_int(pytest_code, "pytest_code")
    lake_witness = require_exact_int(lake_code, "lake_code")
    _require_authority_witness(authority_effect)
    _require_count_law(files, digests, claims)
    _require_process_law(pytest_witness, lake_witness)


def certify_deposit(
    paper_dir: object,
    pytest_runner: Runner | None = None,
    lake_runner: Runner | None = None,
) -> DepositCertificate:
    base = require_directory(paper_dir)
    file_count = require_files(base)
    digest_count = require_manifest(base)
    require_zenodo(base)
    claim_count = require_claim_ledger(base)
    authority = require_authority_mark(_read_text(base / "the_majorana_problem.md"))
    pytest_code = require_pytest_result(_invoke(select_runner(pytest_runner, default_pytest_runner), base))
    lake_code = require_lake_result(_invoke(select_runner(lake_runner, default_lake_runner), base))
    return DepositCertificate(
        file_count,
        digest_count,
        claim_count,
        pytest_code,
        lake_code,
        authority,
    )


def _manifest_lines(paper_dir: Path) -> tuple[str, ...]:
    lines: list[str] = []
    for rel_path in sorted(REQUIRED_FILES):
        if rel_path == "SHA256SUMS":
            continue
        full = paper_dir / rel_path
        if full.is_file():
            lines.append(sha256_file(str(full)) + "  " + rel_path + "\n")
    return tuple(lines)


def update_sha256sums(paper_dir: object) -> int:
    base = require_directory(paper_dir)
    lines = _manifest_lines(base)
    (base / "SHA256SUMS").write_text("".join(lines), encoding="utf-8")
    print("Updated SHA256SUMS with " + str(len(lines)) + " files.")
    return len(lines)


def _root_from(paper_dir: object) -> object:
    if paper_dir is None:
        return Path(__file__).resolve().parent
    return paper_dir


def main(
    argv: list[str] | None = None,
    paper_dir: object = None,
    pytest_runner: Runner | None = None,
    lake_runner: Runner | None = None,
) -> int:
    parser = argparse.ArgumentParser(description="Verify PO-026 deposit")
    parser.add_argument("--update-sums", action="store_true", help="Update SHA256SUMS manifest")
    args = parser.parse_args(argv)
    root = _root_from(paper_dir)
    if args.update_sums:
        update_sha256sums(root)
        return 0
    try:
        certificate = certify_deposit(root, pytest_runner, lake_runner)
    except DepositGateError as exc:
        print("FAILURE: " + str(exc))
        return 1
    print(
        "SUCCESS: files="
        + str(certificate.file_count)
        + " digests="
        + str(certificate.digest_count)
        + " claims="
        + str(certificate.claim_count)
    )
    return 0


def _reconfigure_stdio() -> None:
    reconfigure_out = getattr(sys.stdout, "reconfigure", None)
    reconfigure_err = getattr(sys.stderr, "reconfigure", None)
    if callable(reconfigure_out):
        reconfigure_out(encoding="utf-8", errors="replace")
    if callable(reconfigure_err):
        reconfigure_err(encoding="utf-8", errors="replace")


if __name__ == "__main__":
    _reconfigure_stdio()
    sys.exit(main())
