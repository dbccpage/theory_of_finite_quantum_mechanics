"""Falsification harness for the PO-026 deposit admission certificate.

Origin: papers/derivations/ms_majorana/verify_deposit.py
Claim: urn:omega:fqm:ms-majorana:deposit-gate-harness:v1
AuthorityEffect: None
Mutation-Kills: 3 non-equivalent harness mutants, executed by
test_harness_mutants_are_killed in this file. The library kill count is
recorded on verify_deposit.py.
Scope Fence: this harness does not claim Majorana hardware, does not inherit
the monograph's physics, and does not treat a green deposit certificate as
a theorem. It does not mint authority.

HarnessCertificate records that every listed mutant of this harness was
rejected by an oracle that recomputes SHA-256 and rereads the claim ledger.
"""

from __future__ import annotations

import importlib.util
import io
import re
import struct
import sys
import tempfile
from collections.abc import Callable, Mapping
from typing import Protocol, cast
from contextlib import redirect_stdout
from dataclasses import dataclass
from pathlib import Path

import pytest

import verify_deposit as gate
from verify_deposit import (
    AuthorityEffectMissing,
    BooleanRefused,
    CertificateShape,
    ClaimIdAbsentFromMarkdown,
    ClaimIdSetMismatch,
    CommandResult,
    CommandResultInvalid,
    CommandUnavailable,
    DecimalRefused,
    DepositCertificate,
    DuplicateManifestPath,
    EscapingManifestPath,
    HashMismatch,
    IntegerRequired,
    LeanGateFailed,
    MalformedChecksumRecord,
    ManifestInventoryMismatch,
    MissingManifestTarget,
    MissingRequiredFile,
    PaperPathInvalid,
    PytestGateFailed,
    UnexpectedManifestPath,
    UnreadableFile,
    ZenodoFieldMissing,
    ZenodoJsonUnreadable,
    ZenodoMetadataMissing,
    certify_deposit,
    default_pytest_runner,
    expected_claim_ids,
    main,
    parse_checksum_line,
    parse_claim_ids,
    pytest_command,
    require_authority_mark,
    require_claim_ledger,
    require_directory,
    require_exact_int,
    require_files,
    require_lake_result,
    require_manifest,
    require_pytest_result,
    require_zenodo,
    run_command,
    select_runner,
    sha256_file,
    update_sha256sums,
)

_FIPS_EMPTY_HEAD = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852"
_FIPS_EMPTY_TAIL = "b855"
_FIPS_ABC_HEAD = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f200"
_FIPS_ABC_TAIL = "15ad"
_CLAIM_TOTAL = 20

SPEC_FILES: tuple[str, ...] = (
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

PACKAGE = Path(__file__).resolve().parent
MODULE_PATH = PACKAGE / "verify_deposit.py"
HARNESS_PATH = Path(__file__)
Mutant = tuple[str, str, str]
Oracle = Callable[[dict[str, object]], bool]


class HarnessError(Exception):
    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters: dict[str, object] = {} if parameters is None else dict(parameters)
        super().__init__(invariant)


@dataclass(frozen=True)
class HarnessCertificate:
    killed: int
    cases: int

    def __post_init__(self) -> None:
        _require_kill_count(self.killed, "killed")
        _require_kill_count(self.cases, "cases")
        if self.killed != self.cases:
            raise HarnessError(
                "not every mutant was killed",
                {"killed": self.killed, "cases": self.cases},
            )
        if self.killed <= 0:
            raise HarnessError("kill count is not positive", {"killed": self.killed})


def _require_kill_count(value: object, role: str) -> int:
    if type(value) is bool:
        raise HarnessError(
            "boolean refused where a kill count was required",
            {"role": role},
        )
    if type(value) is not int:
        raise HarnessError(
            "kill count is not an integer",
            {"role": role, "received": value.__class__.__name__},
        )
    return value


def fips_empty_digest() -> str:
    return _FIPS_EMPTY_HEAD + _FIPS_EMPTY_TAIL


def fips_abc_digest() -> str:
    return _FIPS_ABC_HEAD + _FIPS_ABC_TAIL


def claim_total() -> int:
    return _CLAIM_TOTAL


def _decimal_probe() -> object:
    probed = struct.unpack(">d", bytes.fromhex("3ff0000000000000"))
    return probed[0]


def _claim_yaml() -> str:
    lines = ["claims:"]
    index = 1
    while index <= claim_total():
        lines.append('  - id: "MAJ-C' + str(index) + '"')
        index = index + 1
    return "\n".join(lines) + "\n"


def _claim_markdown() -> str:
    lines: list[str] = []
    index = 1
    while index <= claim_total():
        lines.append("MAJ-C" + str(index))
        index = index + 1
    return "\n".join(lines) + "\n"


def _zenodo_text() -> str:
    return (
        '{"title":"t","description":"d","creators":["a"],'
        '"access_right":"open","license":"CC-BY-4.0","keywords":["k"]}'
    )


def _zenodo_decimal() -> str:
    return (
        '{"title":"t","description":"d","creators":["a"],'
        '"access_right":"open","license":"CC-BY-4.0","keywords":["k"],'
        '"extra":1' + ".5}"
    )


def _body(rel_path: str) -> str:
    if rel_path == "claim_ledger.yaml":
        return _claim_yaml()
    if rel_path == "the_majorana_problem_claim_ledger.md":
        return _claim_markdown()
    if rel_path == "the_majorana_problem.md":
        return "AuthorityEffect: None\n"
    if rel_path == ".zenodo.json":
        return _zenodo_text()
    if rel_path == "SHA256SUMS":
        return ""
    return rel_path + "\n"


def _write_spec_files(root: Path) -> None:
    for rel_path in SPEC_FILES:
        if rel_path == "SHA256SUMS":
            continue
        destination = root / rel_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(_body(rel_path), encoding="utf-8")


def _write_manifest(root: Path) -> None:
    lines: list[str] = []
    for rel_path in sorted(SPEC_FILES):
        if rel_path == "SHA256SUMS":
            continue
        digest = sha256_file(str(root / rel_path))
        lines.append(digest + "  " + rel_path + "\n")
    (root / "SHA256SUMS").write_text("".join(lines), encoding="utf-8")


def populate(root: Path) -> None:
    _write_spec_files(root)
    _write_manifest(root)


def _ok_runner(_paper_dir: Path) -> CommandResult:
    return CommandResult(code=0, output="ok")


def _manifest_lines(root: Path) -> list[str]:
    return (root / "SHA256SUMS").read_text(encoding="utf-8").splitlines()


def _write_lines(root: Path, lines: list[str]) -> None:
    (root / "SHA256SUMS").write_text("\n".join(lines) + "\n", encoding="utf-8")


def test_fips_vectors_match_sha256() -> None:
    with tempfile.TemporaryDirectory(prefix="maj-fips-") as scratch:
        root = Path(scratch)
        empty = root / "empty"
        abc = root / "abc"
        empty.write_bytes(b"")
        abc.write_bytes(b"abc")
        assert sha256_file(str(empty)) == fips_empty_digest()
        assert sha256_file(str(abc)) == fips_abc_digest()


def test_inventory_matches_specification() -> None:
    assert gate.REQUIRED_FILES == SPEC_FILES
    assert len(expected_claim_ids()) == claim_total()
    assert expected_claim_ids()[0] == "MAJ-C1"
    assert expected_claim_ids()[-1] == "MAJ-C20"


def test_decimal_integer_is_refused() -> None:
    with pytest.raises(DecimalRefused) as caught:
        require_exact_int(_decimal_probe(), "command_code")
    assert caught.value.invariant == "decimal refused at the deposit boundary"
    assert caught.value.parameters["role"] == "command_code"


def test_boolean_integer_is_refused() -> None:
    with pytest.raises(BooleanRefused) as caught:
        require_exact_int(True, "command_code")
    assert caught.value.invariant == "boolean refused where an exact integer was required"
    assert caught.value.parameters["role"] == "command_code"


def test_non_integer_is_refused() -> None:
    with pytest.raises(IntegerRequired) as caught:
        require_exact_int("1", "command_code")
    assert caught.value.invariant == "exact integer required"
    assert caught.value.parameters["received"] == "str"


def test_boolean_command_result_is_refused() -> None:
    with pytest.raises(BooleanRefused) as caught:
        CommandResult(code=True, output="ok")
    assert caught.value.invariant == "boolean refused where an exact integer was required"


def test_decimal_command_result_is_refused() -> None:
    with pytest.raises(DecimalRefused) as caught:
        CommandResult(code=cast(int, _decimal_probe()), output="ok")
    assert caught.value.parameters["role"] == "command_code"


def test_decimal_directory_is_refused() -> None:
    with pytest.raises(DecimalRefused) as caught:
        require_directory(_decimal_probe())
    assert caught.value.parameters["role"] == "paper_dir"


def test_boolean_directory_is_refused() -> None:
    with pytest.raises(BooleanRefused) as caught:
        require_directory(True)
    assert caught.value.invariant == "boolean refused where text was required"


def test_non_text_directory_is_refused() -> None:
    with pytest.raises(PaperPathInvalid) as caught:
        require_directory(1)
    assert caught.value.invariant == "path is not text"


def test_missing_directory_is_refused(tmp_path: Path) -> None:
    with pytest.raises(PaperPathInvalid) as caught:
        require_directory(tmp_path / "absent")
    assert caught.value.invariant == "paper path is not a directory"


def test_unreadable_file_is_refused(tmp_path: Path) -> None:
    with pytest.raises(UnreadableFile) as caught:
        sha256_file(str(tmp_path / "absent"))
    assert caught.value.invariant == "file bytes are unreadable"


def test_missing_required_file_names_the_gap(tmp_path: Path) -> None:
    with pytest.raises(MissingRequiredFile) as caught:
        require_files(tmp_path)
    assert caught.value.invariant == "required file is absent"
    assert caught.value.parameters["missing"] == SPEC_FILES[0]
    assert caught.value.parameters["count"] == len(SPEC_FILES)


def test_malformed_checksum_is_refused(tmp_path: Path) -> None:
    (tmp_path / "SHA256SUMS").write_text("zz  README.md\n", encoding="utf-8")
    with pytest.raises(MalformedChecksumRecord) as caught:
        require_manifest(tmp_path)
    assert caught.value.invariant == "checksum record is malformed"


def test_unexpected_manifest_path_is_refused(tmp_path: Path) -> None:
    populate(tmp_path)
    lines = _manifest_lines(tmp_path)
    lines.append(fips_empty_digest() + "  not-required.txt")
    _write_lines(tmp_path, lines)
    with pytest.raises(UnexpectedManifestPath) as caught:
        require_manifest(tmp_path)
    assert caught.value.invariant == "manifest path is not in the required inventory"
    assert caught.value.parameters["path"] == "not-required.txt"


def test_duplicate_manifest_path_is_refused(tmp_path: Path) -> None:
    populate(tmp_path)
    lines = _manifest_lines(tmp_path)
    lines.append(lines[0])
    _write_lines(tmp_path, lines)
    with pytest.raises(DuplicateManifestPath) as caught:
        require_manifest(tmp_path)
    assert caught.value.invariant == "manifest path is duplicated"


def test_absolute_manifest_path_is_refused(tmp_path: Path) -> None:
    populate(tmp_path)
    lines = _manifest_lines(tmp_path)
    lines[0] = fips_empty_digest() + "  " + str(Path(tmp_path).resolve().anchor) + "outside.txt"
    _write_lines(tmp_path, lines)
    with pytest.raises(EscapingManifestPath) as caught:
        require_manifest(tmp_path)
    assert caught.value.invariant == "manifest path is absolute"


def test_escaping_manifest_path_is_refused(tmp_path: Path) -> None:
    populate(tmp_path)
    lines = _manifest_lines(tmp_path)
    _digest, relative = lines[0].split("  ", 1)
    lines[0] = fips_empty_digest() + "  ../" + relative
    _write_lines(tmp_path, lines)
    with pytest.raises(EscapingManifestPath) as caught:
        require_manifest(tmp_path)
    assert caught.value.invariant == "manifest path escapes the package root"


def test_missing_manifest_target_is_refused(tmp_path: Path) -> None:
    populate(tmp_path)
    (tmp_path / "README.md").unlink()
    with pytest.raises(MissingManifestTarget) as caught:
        require_manifest(tmp_path)
    assert caught.value.invariant == "manifest target is not a file"


def test_hash_mismatch_is_refused(tmp_path: Path) -> None:
    populate(tmp_path)
    lines = _manifest_lines(tmp_path)
    _digest, relative = lines[0].split("  ", 1)
    lines[0] = fips_empty_digest() + "  " + relative
    _write_lines(tmp_path, lines)
    with pytest.raises(HashMismatch) as caught:
        require_manifest(tmp_path)
    assert caught.value.invariant == "sha256 digest does not match the manifest"
    assert caught.value.parameters["path"] == relative


def test_manifest_inventory_mismatch_names_the_gap(tmp_path: Path) -> None:
    populate(tmp_path)
    lines = _manifest_lines(tmp_path)
    _write_lines(tmp_path, lines[1:])
    with pytest.raises(ManifestInventoryMismatch) as caught:
        require_manifest(tmp_path)
    assert caught.value.invariant == "manifest inventory does not match the required set"
    assert caught.value.parameters["count"] == 1


def test_zenodo_absence_is_refused(tmp_path: Path) -> None:
    with pytest.raises(ZenodoMetadataMissing) as caught:
        require_zenodo(tmp_path)
    assert caught.value.invariant == "zenodo metadata is absent"


def test_zenodo_json_is_refused(tmp_path: Path) -> None:
    (tmp_path / ".zenodo.json").write_text("{", encoding="utf-8")
    with pytest.raises(ZenodoJsonUnreadable) as caught:
        require_zenodo(tmp_path)
    assert caught.value.invariant == "zenodo json is unreadable"


def test_zenodo_decimal_is_refused(tmp_path: Path) -> None:
    (tmp_path / ".zenodo.json").write_text(_zenodo_decimal(), encoding="utf-8")
    with pytest.raises(DecimalRefused) as caught:
        require_zenodo(tmp_path)
    assert caught.value.invariant == "decimal refused in zenodo metadata"


def test_zenodo_missing_field_is_refused(tmp_path: Path) -> None:
    (tmp_path / ".zenodo.json").write_text('{"title":"t"}', encoding="utf-8")
    with pytest.raises(ZenodoFieldMissing) as caught:
        require_zenodo(tmp_path)
    assert caught.value.invariant == "zenodo field is absent"
    assert caught.value.parameters["field"] == "description"


def test_zenodo_empty_field_is_refused(tmp_path: Path) -> None:
    text = _zenodo_text().replace('"t"', '""', 1)
    (tmp_path / ".zenodo.json").write_text(text, encoding="utf-8")
    with pytest.raises(ZenodoFieldMissing) as caught:
        require_zenodo(tmp_path)
    assert caught.value.invariant == "zenodo field is empty"
    assert caught.value.parameters["field"] == "title"


def test_claim_decimal_is_refused() -> None:
    with pytest.raises(DecimalRefused) as caught:
        parse_claim_ids("weight: 1" + ".5\n")
    assert caught.value.invariant == "decimal refused in claim ledger text"


def test_claim_set_mismatch_is_refused(tmp_path: Path) -> None:
    populate(tmp_path)
    (tmp_path / "claim_ledger.yaml").write_text('  - id: "MAJ-C1"\n', encoding="utf-8")
    with pytest.raises(ClaimIdSetMismatch) as caught:
        require_claim_ledger(tmp_path)
    assert caught.value.invariant == "claim id set is not MAJ-C1 through MAJ-C20"


def test_duplicate_claim_id_is_refused(tmp_path: Path) -> None:
    text = _claim_yaml().replace('  - id: "MAJ-C1"\n', '  - id: "MAJ-C1"\n  - id: "MAJ-C1"\n', 1)
    (tmp_path / "claim_ledger.yaml").write_text(text, encoding="utf-8")
    (tmp_path / "the_majorana_problem_claim_ledger.md").write_text(_claim_markdown(), encoding="utf-8")
    with pytest.raises(ClaimIdSetMismatch) as caught:
        require_claim_ledger(tmp_path)
    assert caught.value.invariant == "claim ids are not unique"


def test_claim_absent_from_markdown_is_refused(tmp_path: Path) -> None:
    populate(tmp_path)
    (tmp_path / "the_majorana_problem_claim_ledger.md").write_text("MAJ-C1\n", encoding="utf-8")
    with pytest.raises(ClaimIdAbsentFromMarkdown) as caught:
        require_claim_ledger(tmp_path)
    assert caught.value.invariant == "claim id is absent from the markdown ledger"


def test_authority_mark_absence_is_refused() -> None:
    with pytest.raises(AuthorityEffectMissing) as caught:
        require_authority_mark("no mark here")
    assert caught.value.invariant == "manuscript lacks AuthorityEffect: None"


def test_pytest_nonzero_is_refused() -> None:
    with pytest.raises(PytestGateFailed) as caught:
        require_pytest_result(CommandResult(code=1, output=""))
    assert caught.value.invariant == "pytest exit code is not zero"
    assert caught.value.parameters["code"] == 1


def test_lake_nonzero_is_refused() -> None:
    with pytest.raises(LeanGateFailed) as caught:
        require_lake_result(CommandResult(code=2, output="ok"))
    assert caught.value.invariant == "lake exit code is not zero"
    assert caught.value.parameters["code"] == 2


def test_sorry_ax_is_refused() -> None:
    with pytest.raises(LeanGateFailed) as caught:
        require_lake_result(CommandResult(code=0, output="uses sorryAx later"))
    assert caught.value.invariant == "lean output contains sorryAx"


def test_sorry_declaration_is_refused() -> None:
    with pytest.raises(LeanGateFailed) as caught:
        require_lake_result(CommandResult(code=0, output="declaration uses 'sorry'"))
    assert caught.value.invariant == "lean output contains a sorry declaration"


def test_empty_command_is_refused(tmp_path: Path) -> None:
    with pytest.raises(CommandUnavailable) as caught:
        run_command((), tmp_path)
    assert caught.value.invariant == "command is empty"


def test_missing_command_is_refused(tmp_path: Path) -> None:
    with pytest.raises(CommandUnavailable) as caught:
        run_command(("this-command-does-not-exist-maj",), tmp_path)
    assert caught.value.invariant == "command could not be started"
    assert caught.value.parameters["command"] == "this-command-does-not-exist-maj"


def test_runner_type_is_refused(tmp_path: Path) -> None:
    populate(tmp_path)

    def bad(_paper_dir: Path) -> object:
        return object()

    with pytest.raises(CommandResultInvalid) as caught:
        certify_deposit(tmp_path, bad, _ok_runner)
    assert caught.value.invariant == "runner did not return a command result"


def test_certificate_rejects_nonzero_pytest() -> None:
    with pytest.raises(CertificateShape) as caught:
        DepositCertificate(len(SPEC_FILES), len(SPEC_FILES) - 1, claim_total(), 1, 0, "None")
    assert caught.value.invariant == "pytest witness is not zero"
    assert caught.value.parameters["code"] == 1


def test_certificate_rejects_nonzero_lake() -> None:
    with pytest.raises(CertificateShape) as caught:
        DepositCertificate(len(SPEC_FILES), len(SPEC_FILES) - 1, claim_total(), 0, 3, "None")
    assert caught.value.invariant == "lake witness is not zero"


def test_certificate_rejects_bad_authority() -> None:
    with pytest.raises(CertificateShape) as caught:
        DepositCertificate(len(SPEC_FILES), len(SPEC_FILES) - 1, claim_total(), 0, 0, "Vendor")
    assert caught.value.invariant == "authority effect witness is not None"


def test_certificate_rejects_bad_file_witness() -> None:
    with pytest.raises(CertificateShape) as caught:
        DepositCertificate(0, len(SPEC_FILES) - 1, claim_total(), 0, 0, "None")
    assert caught.value.invariant == "file witness is not the required inventory"


def test_certificate_admits_the_conjunction() -> None:
    certificate = DepositCertificate(
        len(SPEC_FILES),
        len(SPEC_FILES) - 1,
        claim_total(),
        0,
        0,
        "None",
    )
    assert certificate.file_count == len(SPEC_FILES)
    assert certificate.digest_count + 1 == certificate.file_count
    assert certificate.claim_count == claim_total()


def test_select_runner_keeps_the_default_and_the_override() -> None:
    assert select_runner(None, default_pytest_runner) is default_pytest_runner
    assert select_runner(_ok_runner, default_pytest_runner) is _ok_runner


def test_pytest_command_lists_the_four_suites() -> None:
    command = pytest_command("python", "base")
    assert command[0] == "python"
    assert "--basetemp=base" in command
    assert "--cov-fail-under=95" in command
    assert "tests/unit/test_gf2_trichotomy.py" in command
    assert "tests/unit/test_open_system_transfer_bounds.py" in command
    assert "tests/integration/test_tetron_surface_codes.py" in command
    assert "tests/e2e/test_majorana_problem_e2e.py" in command


def test_real_ledger_and_manuscript_integration() -> None:
    count = require_claim_ledger(PACKAGE)
    assert count == claim_total()
    assert count == len(_independent_claim_ids())
    manuscript = (PACKAGE / "the_majorana_problem.md").read_text(encoding="utf-8")
    assert require_authority_mark(manuscript) == "None"
    assert "MAJ-C1" in (PACKAGE / "the_majorana_problem_claim_ledger.md").read_text(encoding="utf-8")
    assert "MAJ-C20" in (PACKAGE / "the_majorana_problem_claim_ledger.md").read_text(encoding="utf-8")


def test_real_manifest_grammar_integration() -> None:
    text = (PACKAGE / "SHA256SUMS").read_text(encoding="utf-8")
    parsed = 0
    for line in text.splitlines():
        item = parse_checksum_line(line)
        if item is None:
            continue
        digest, relative = item
        assert len(digest) == 64
        assert relative != ""
        parsed = parsed + 1
    assert parsed == len(SPEC_FILES) - 1


def test_origin_resolves_to_the_ledger_and_manifest() -> None:
    source = MODULE_PATH.read_text(encoding="utf-8")
    assert "Origin: papers/derivations/ms_majorana/the_majorana_problem_claim_ledger.md" in source
    assert "Claim: urn:omega:fqm:ms-majorana:deposit-gate:v1" in source
    assert "AuthorityEffect: None" in source
    assert "Scope Fence:" in source
    assert (PACKAGE / "the_majorana_problem_claim_ledger.md").is_file()
    assert (PACKAGE / "SHA256SUMS").is_file()
    assert (PACKAGE / "the_majorana_problem.md").is_file()


def test_end_to_end_admits_synthetic_package(tmp_path: Path) -> None:
    populate(tmp_path)
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        code = main([], tmp_path, _ok_runner, _ok_runner)
    assert code == 0
    text = buffer.getvalue()
    assert "SUCCESS:" in text
    assert "claims=" + str(claim_total()) in text


def test_end_to_end_rejects_missing_file(tmp_path: Path) -> None:
    populate(tmp_path)
    (tmp_path / "README.md").unlink()
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        code = main([], tmp_path, _ok_runner, _ok_runner)
    assert code == 1
    assert "required file is absent" in buffer.getvalue()


def test_end_to_end_update_sums(tmp_path: Path) -> None:
    populate(tmp_path)
    (tmp_path / "SHA256SUMS").write_text("", encoding="utf-8")
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        code = main(["--update-sums"], tmp_path)
    assert code == 0
    expected = "Updated SHA256SUMS with " + str(len(SPEC_FILES) - 1) + " files."
    assert expected in buffer.getvalue()
    assert require_manifest(tmp_path) == len(SPEC_FILES) - 1
    assert update_sha256sums(tmp_path) == len(SPEC_FILES) - 1


def test_harness_certificate_rejects_a_survivor() -> None:
    with pytest.raises(HarnessError) as caught:
        HarnessCertificate(2, 3)
    assert caught.value.invariant == "not every mutant was killed"
    assert caught.value.parameters["killed"] == 2
    assert caught.value.parameters["cases"] == 3


def test_harness_certificate_rejects_boolean_counts() -> None:
    with pytest.raises(HarnessError) as caught:
        HarnessCertificate(True, 1)
    assert caught.value.invariant == "boolean refused where a kill count was required"


def test_harness_certificate_rejects_a_zero_kill_count() -> None:
    with pytest.raises(HarnessError) as caught:
        HarnessCertificate(0, 0)
    assert caught.value.invariant == "kill count is not positive"


def _independent_claim_ids() -> set[str]:
    text = (PACKAGE / "claim_ledger.yaml").read_text(encoding="utf-8")
    return set(re.findall(r'id: "(MAJ-C[0-9]+)"', text))


def _hash_bytes(sha: Callable[[object], object], payload: bytes) -> object:
    with tempfile.TemporaryDirectory(prefix="maj-sha-") as scratch:
        path = Path(scratch) / "payload"
        path.write_bytes(payload)
        return sha(str(path))


def _independent_empty_sha() -> str:
    return str(_hash_bytes(sha256_file, b""))


def _independent_abc_sha() -> str:
    return str(_hash_bytes(sha256_file, b"abc"))


def _load(source: str, name: str, origin: Path) -> dict[str, object]:
    spec = importlib.util.spec_from_loader(name, loader=None)
    if spec is None:
        raise HarnessError("mutant module spec was not allocated", {"name": name})
    module = importlib.util.module_from_spec(spec)
    module.__dict__["__file__"] = str(origin)
    sys.modules[name] = module
    try:
        exec(compile(source, name + ".py", "exec"), module.__dict__)
    except Exception:
        sys.modules.pop(name, None)
        raise
    loaded: dict[str, object] = {}
    for key, value in module.__dict__.items():
        loaded[str(key)] = value
    return loaded


def _caught_invariant(caught: BaseException) -> str | None:
    invariant = getattr(caught, "invariant", None)
    if type(invariant) is str:
        return invariant
    return None


def _invariant(namespace: dict[str, object], error_name: str, probe: Callable[[], object]) -> str | None:
    error = namespace.get(error_name)
    if not isinstance(error, type) or not issubclass(error, BaseException):
        return None
    try:
        probe()
    except error as caught:
        return _caught_invariant(caught)
    except Exception:
        return None
    return None


def _hashes_ok(namespace: dict[str, object]) -> bool:
    sha = namespace.get("sha256_file")
    if not callable(sha):
        return False
    empty = _hash_bytes(sha, b"")
    abc = _hash_bytes(sha, b"abc")
    return empty == fips_empty_digest() and abc == fips_abc_digest()


def _refusals_ok(namespace: dict[str, object]) -> bool:
    require_int = namespace.get("require_exact_int")
    require_dir = namespace.get("require_directory")
    if not callable(require_int) or not callable(require_dir):
        return False
    decimal_name = _invariant(namespace, "DecimalRefused", lambda: require_int(_decimal_probe(), "command_code"))
    bool_name = _invariant(namespace, "BooleanRefused", lambda: require_int(True, "command_code"))
    text_bool = _invariant(namespace, "BooleanRefused", lambda: require_dir(True))
    if decimal_name != "decimal refused at the deposit boundary":
        return False
    if bool_name != "boolean refused where an exact integer was required":
        return False
    return text_bool == "boolean refused where text was required"


def _json_decimal_ok(namespace: dict[str, object]) -> bool:
    require = namespace.get("require_zenodo")
    if not callable(require):
        return False
    with tempfile.TemporaryDirectory(prefix="maj-json-") as scratch:
        root = Path(scratch)
        (root / ".zenodo.json").write_text(_zenodo_decimal(), encoding="utf-8")
        seen = _invariant(namespace, "DecimalRefused", lambda: require(root))
    return seen == "decimal refused in zenodo metadata"


def _ledger_decimal_ok(namespace: dict[str, object]) -> bool:
    parse = namespace.get("parse_claim_ids")
    if not callable(parse):
        return False
    seen = _invariant(namespace, "DecimalRefused", lambda: parse("weight: 1" + ".5\n"))
    return seen == "decimal refused in claim ledger text"


def _law_ok(namespace: dict[str, object]) -> bool:
    certificate = namespace.get("DepositCertificate")
    if not isinstance(certificate, type):
        return False
    seen = _invariant(
        namespace,
        "CertificateShape",
        lambda: certificate(len(SPEC_FILES), len(SPEC_FILES) - 1, claim_total(), 1, 0, "None"),
    )
    return seen == "pytest witness is not zero"


class _CommandFactory(Protocol):
    def __call__(self, *, code: int, output: str) -> object: ...


def _bound_runner(result_type: object) -> Callable[[Path], object]:
    factory = cast(_CommandFactory, result_type)

    def run(_paper_dir: Path) -> object:
        return factory(code=0, output="ok")

    return run


def _certify_ok(namespace: dict[str, object], root: Path) -> object:
    certify = namespace.get("certify_deposit")
    result_type = namespace.get("CommandResult")
    if not callable(certify) or not isinstance(result_type, type):
        return None
    runner = _bound_runner(result_type)
    try:
        return certify(root, runner, runner)
    except Exception:
        return None


def _fields_ok(certificate: object) -> bool:
    if certificate is None:
        return False
    file_count = getattr(certificate, "file_count", None)
    digest_count = getattr(certificate, "digest_count", None)
    claim_count = getattr(certificate, "claim_count", None)
    pytest_code = getattr(certificate, "pytest_code", None)
    lake_code = getattr(certificate, "lake_code", None)
    authority = getattr(certificate, "authority_effect", None)
    if file_count != len(SPEC_FILES):
        return False
    if digest_count != len(SPEC_FILES) - 1:
        return False
    if claim_count != claim_total():
        return False
    if pytest_code != 0 or lake_code != 0:
        return False
    return authority == "None"


def _package_ok(namespace: dict[str, object]) -> bool:
    with tempfile.TemporaryDirectory(prefix="maj-pkg-") as scratch:
        root = Path(scratch)
        populate(root)
        return _fields_ok(_certify_ok(namespace, root))


def _select_ok(namespace: dict[str, object]) -> bool:
    select = namespace.get("select_runner")
    default = namespace.get("default_pytest_runner")
    if not callable(select) or not callable(default):
        return False
    if select(None, default) is not default:
        return False

    def sentinel(_paper_dir: Path) -> object:
        return None

    return select(sentinel, default) is sentinel


def _call_main(main_fn: Callable[..., object], root: Path, runner: Callable[[Path], object]) -> tuple[int, str] | None:
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        try:
            code = main_fn([], root, runner, runner)
        except Exception:
            return None
    if type(code) is not int:
        return None
    return code, buffer.getvalue()


def _main_ok(namespace: dict[str, object]) -> bool:
    main_fn = namespace.get("main")
    result_type = namespace.get("CommandResult")
    if not callable(main_fn) or not isinstance(result_type, type):
        return False
    with tempfile.TemporaryDirectory(prefix="maj-main-") as scratch:
        root = Path(scratch)
        populate(root)
        outcome = _call_main(main_fn, root, _bound_runner(result_type))
    if outcome is None:
        return False
    code, text = outcome
    return code == 0 and "SUCCESS:" in text


def _library_oracle(namespace: dict[str, object]) -> bool:
    if not _hashes_ok(namespace):
        return False
    if not _refusals_ok(namespace):
        return False
    if not _json_decimal_ok(namespace):
        return False
    if not _ledger_decimal_ok(namespace):
        return False
    if not _law_ok(namespace):
        return False
    if not _select_ok(namespace):
        return False
    if not _package_ok(namespace):
        return False
    return _main_ok(namespace)


def _harness_oracle(namespace: dict[str, object]) -> bool:
    empty = namespace.get("fips_empty_digest")
    abc = namespace.get("fips_abc_digest")
    total = namespace.get("claim_total")
    if not callable(empty) or not callable(abc) or not callable(total):
        return False
    if empty() != _independent_empty_sha():
        return False
    if abc() != _independent_abc_sha():
        return False
    counted = total()
    if type(counted) is not int:
        return False
    return counted == len(_independent_claim_ids())


def _one_killed(
    source: str,
    name: str,
    old: str,
    new: str,
    holds: Oracle,
    label: str,
    origin: Path,
) -> bool:
    count = source.count(old)
    if count != 1:
        raise HarnessError("mutant site is not unique", {"name": name, "count": count})
    namespace = _load(source.replace(old, new, 1), label, origin)
    try:
        survived = _holds_quietly(holds, namespace)
    finally:
        sys.modules.pop(label, None)
    return not survived


def _holds_quietly(holds: Oracle, namespace: dict[str, object]) -> bool:
    try:
        return holds(namespace)
    except Exception:
        return False


def count_kills(
    source: str,
    mutants: tuple[Mutant, ...],
    holds: Oracle,
    prefix: str,
    origin: Path,
) -> int:
    killed = 0
    for index, (name, old, new) in enumerate(mutants):
        label = prefix + str(index)
        if not _one_killed(source, name, old, new, holds, label, origin):
            raise HarnessError("mutant survived", {"name": name})
        killed = killed + 1
    return killed


_LIBRARY_MUTANTS: tuple[Mutant, ...] = (
    (
        "decimal class gate removed",
        'return value.__class__.__name__ == "float"',
        "return False",
    ),
    (
        "boolean integer gate removed",
        "if isinstance(value, bool):",
        "if False and isinstance(value, bool):",
    ),
    (
        "missing file polarity",
        "if len(missing) != 0:",
        "if len(missing) == 0:",
    ),
    (
        "hash compare polarity",
        "if actual != digest:",
        "if actual == digest:",
    ),
    (
        "authority mark polarity",
        "if AUTHORITY_MARK not in text:",
        "if AUTHORITY_MARK in text:",
    ),
    (
        "process code polarity",
        "if checked != 0:",
        "if checked == 0:",
    ),
    (
        "sorryAx polarity",
        'if "sorryAx" in output:',
        'if "sorryAx" not in output:',
    ),
    (
        "sorry declaration polarity",
        '''if "declaration uses 'sorry'" in output:''',
        '''if "declaration uses 'sorry'" not in output:''',
    ),
    (
        "claim upper bound dropped",
        "range(CLAIM_LO, CLAIM_HI + 1)",
        "range(CLAIM_LO, CLAIM_HI)",
    ),
    (
        "escape polarity",
        "if not target.is_relative_to(resolved):",
        "if target.is_relative_to(resolved):",
    ),
    (
        "duplicate polarity",
        "if relative in seen:",
        "if relative not in seen:",
    ),
    (
        "empty zenodo field polarity",
        "if _field_empty(data[key]):",
        "if not _field_empty(data[key]):",
    ),
    (
        "inventory polarity",
        "if seen != expected:",
        "if seen == expected:",
    ),
    (
        "zenodo decimal token admitted",
        '''    raise DecimalRefused(
        "decimal refused in zenodo metadata",
        {"role": "zenodo", "received": "decimal"},
    )''',
        "    return token",
    ),
    (
        "unexpected path polarity",
        "if relative not in expected:",
        "if relative in expected:",
    ),
    (
        "markdown claim polarity",
        "if re.search(pattern, markdown) is None:",
        "if re.search(pattern, markdown) is not None:",
    ),
    (
        "runner default polarity",
        "if runner is None:",
        "if runner is not None:",
    ),
    (
        "update sums polarity",
        "if args.update_sums:",
        "if not args.update_sums:",
    ),
)


_HARNESS_MUTANTS: tuple[Mutant, ...] = (
    (
        "empty digest tail",
        "_FIPS_EMPTY_TAIL = " + '"b855"',
        "_FIPS_EMPTY_TAIL = " + '"b856"',
    ),
    (
        "abc digest tail",
        "_FIPS_ABC_TAIL = " + '"15ad"',
        "_FIPS_ABC_TAIL = " + '"15ae"',
    ),
    (
        "claim total",
        "_CLAIM_TOTAL = " + "20",
        "_CLAIM_TOTAL = " + "19",
    ),
)


def test_mutation_suite_kills_non_equivalent_mutants() -> None:
    source = MODULE_PATH.read_text(encoding="utf-8")
    baseline = _load(source, "deposit_baseline", MODULE_PATH)
    try:
        assert _library_oracle(baseline) is True
    finally:
        sys.modules.pop("deposit_baseline", None)
    killed = count_kills(source, _LIBRARY_MUTANTS, _library_oracle, "deposit_mutant_", MODULE_PATH)
    certificate = HarnessCertificate(killed, len(_LIBRARY_MUTANTS))
    assert certificate.killed == 18
    assert "Mutation-Kills: 18 non-equivalent" in source


def test_harness_mutants_are_killed() -> None:
    source = HARNESS_PATH.read_text(encoding="utf-8")
    baseline = _load(source, "harness_baseline", HARNESS_PATH)
    try:
        assert _harness_oracle(baseline) is True
    finally:
        sys.modules.pop("harness_baseline", None)
    killed = count_kills(source, _HARNESS_MUTANTS, _harness_oracle, "harness_mutant_", HARNESS_PATH)
    certificate = HarnessCertificate(killed, len(_HARNESS_MUTANTS))
    assert certificate.killed == 3
    assert "Mutation-Kills: 3 non-equivalent" in source
