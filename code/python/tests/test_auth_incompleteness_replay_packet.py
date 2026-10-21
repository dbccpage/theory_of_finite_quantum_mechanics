"""Port of the 23-case PowerShell replay-packet corpus (code/tests/test_replay_packet.ps1).

Origin: papers/foundations/authorization_incompleteness/evidence/original/code/tests/test_replay_packet.ps1
Claim: urn:omega:fqm:authincomp:replay-packet-corpus-python-port:v1
AuthorityEffect: None
Mutation-Kills: 21 tamper mutations (cases 3-23) must be refused; case 1 verifies; case 2 shows the
source self-pass flag has no effect.
Scope Fence: this exercises the bounded packet under its manifest trust root only.
"""

from __future__ import annotations

import importlib
import json
import shutil
import sys
import types
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
# qm/__init__.py is not importable stand-alone; stage the sub-package as the sibling tests do.
_pkg = types.ModuleType("staged_auth_incompleteness")
_pkg.__path__ = [str(REPO / "code/python/src/qm/auth_incompleteness")]
sys.modules[_pkg.__name__] = _pkg
rp = importlib.import_module("staged_auth_incompleteness.replay_packet")
PACKET = rp.ORIGINAL_PREFIX + "code/replay_packet/"
ROLES_TO_TAMPER = ["contract", "terminal_policy", "evaluator", "verifier", "formal_model", "formal_dependency", "lean_toolchain"]


def _mapped(rel: str) -> str:
    return rp.map_path(rel, rp.PREFIX_MAP)


@pytest.fixture()
def fixture_root(tmp_path: Path) -> Path:
    manifest = json.loads((REPO / _mapped(rp.DEFAULT_MANIFEST)).read_text(encoding="utf-8"))
    rels = [rp.DEFAULT_MANIFEST] + [a["path"] for a in manifest["artifacts"]]
    for rel in rels:
        dest = tmp_path / _mapped(rel)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(REPO / _mapped(rel), dest)
    return tmp_path


def _path(root: Path, name: str) -> Path:
    return root / _mapped(PACKET + name)


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _store(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")


def _redigest(root: Path, role: str) -> None:
    manifest_path = _path(root, "packet_manifest.json")
    manifest = _load(manifest_path)
    artifact = next(a for a in manifest["artifacts"] if a["role"] == role)
    artifact["sha256"] = rp.sha256_file(root / _mapped(artifact["path"]))
    _store(manifest_path, manifest)


def _refused(action, needle: str) -> None:
    with pytest.raises(rp.ReplayPacketRefusal) as info:
        action()
    assert needle in str(info.value)


def test_case_01_good_packet_verifies() -> None:
    result = rp.invoke_replay_packet(REPO)
    assert result["verification_status"] == "verified"
    assert result["terminal"] == "open"
    assert result["source_claimed_pass_used"] is False
    ev = result["evaluation"]
    assert ev["clean_terminal_preserved"] is True
    assert ev["full_report_adequate"] is True
    assert ev["control_only_report_adequate"] is False
    assert ev["control_only_authorization"] == "open_due_to_inadequate_report"
    assert ev["control_only_counterexample"] == {"report": "stay", "first": "haltedBlank", "second": "haltedMarked"}
    # Both marked-accepting sources step to haltedBlank, which the marked-cell contract rejects.
    assert [c["source"] for c in ev["marked_countertraces"]] == ["runningMarked", "haltedMarked"]


def test_case_02_source_self_pass_flag_has_no_effect(fixture_root: Path) -> None:
    p = _path(fixture_root, "transition_proposal.json")
    proposal = _load(p)
    proposal["source_claimed_pass"] = False
    _store(p, proposal)
    _redigest(fixture_root, "proposal")
    result = rp.invoke_replay_packet(fixture_root)
    assert result["verification_status"] == "verified"
    assert result["source_claimed_pass_used"] is False
    assert result["evaluation"]["control_only_authorization"] == "open_due_to_inadequate_report"


def test_case_03_invalid_utf8_proposal(fixture_root: Path) -> None:
    p = _path(fixture_root, "transition_proposal.json")
    p.write_bytes(p.read_bytes() + b"\xff")
    _redigest(fixture_root, "proposal")
    _refused(lambda: rp.invoke_replay_packet(fixture_root), "not valid UTF-8 JSON")


def test_case_04_duplicate_json_property(fixture_root: Path) -> None:
    p = _path(fixture_root, "transition_proposal.json")
    text = p.read_text(encoding="utf-8").replace('"schema_version":', '"schema_version":"duplicate", "schema_version":')
    p.write_text(text, encoding="utf-8", newline="\n")
    _redigest(fixture_root, "proposal")
    _refused(lambda: rp.invoke_replay_packet(fixture_root), "duplicate JSON property schema_version")


def test_case_05_case_variant_property(fixture_root: Path) -> None:
    p = _path(fixture_root, "transition_proposal.json")
    p.write_text(p.read_text(encoding="utf-8").replace('"schema_version":', '"Schema_Version":'), encoding="utf-8", newline="\n")
    _redigest(fixture_root, "proposal")
    _refused(lambda: rp.invoke_replay_packet(fixture_root), "proposal has an invalid field set")


def test_case_06_case_variant_protocol_value(fixture_root: Path) -> None:
    p = _path(fixture_root, "transition_proposal.json")
    proposal = _load(p)
    proposal["proposal_id"] = "Finite-transition-table-v1"
    _store(p, proposal)
    _redigest(fixture_root, "proposal")
    _refused(lambda: rp.invoke_replay_packet(fixture_root), "proposal identifier is not licensed")


def test_case_07_coercible_expected_result(fixture_root: Path) -> None:
    p = _path(fixture_root, "transition_contract.json")
    contract = _load(p)
    contract["expected"]["clean_terminal_preserved"] = 1
    _store(p, contract)
    _redigest(fixture_root, "contract")
    _refused(lambda: rp.invoke_replay_packet(fixture_root), "clean_terminal_preserved must be Boolean")


def test_case_08_tampered_proposal_bytes(fixture_root: Path) -> None:
    p = _path(fixture_root, "transition_proposal.json")
    p.write_bytes(p.read_bytes() + b"\n")
    _refused(lambda: rp.check_packet(fixture_root), "artifact digest mismatch for proposal")


def test_case_09_manifest_path_escape(fixture_root: Path) -> None:
    m = _path(fixture_root, "packet_manifest.json")
    manifest = _load(m)
    next(a for a in manifest["artifacts"] if a["role"] == "contract")["path"] = "../outside.json"
    _store(m, manifest)
    _refused(lambda: rp.check_packet(fixture_root), "parent escape")


@pytest.mark.parametrize("role", ROLES_TO_TAMPER)
def test_cases_10_to_16_artifact_replacement(fixture_root: Path, role: str) -> None:
    manifest = _load(_path(fixture_root, "packet_manifest.json"))
    artifact = next(a for a in manifest["artifacts"] if a["role"] == role)
    target = fixture_root / _mapped(artifact["path"])
    target.write_bytes(target.read_bytes() + b"# tamper\n")
    _refused(lambda: rp.check_packet(fixture_root), f"artifact digest mismatch for {role}")


def test_case_17_proposal_schema_injection(fixture_root: Path) -> None:
    p = _path(fixture_root, "transition_proposal.json")
    proposal = _load(p)
    proposal["unlicensed_field"] = "injected"
    _store(p, proposal)
    _redigest(fixture_root, "proposal")
    _refused(lambda: rp.invoke_replay_packet(fixture_root), "proposal has an invalid field set")


def test_case_18_proposal_schema_substitution(fixture_root: Path) -> None:
    p = _path(fixture_root, "transition_proposal.json")
    proposal = _load(p)
    proposal["schema_version"] = "unlicensed.proposal.v1"
    _store(p, proposal)
    _redigest(fixture_root, "proposal")
    _refused(lambda: rp.invoke_replay_packet(fixture_root), "proposal schema version is not supported")


def test_case_19_declared_outcome_substitution(fixture_root: Path) -> None:
    p = _path(fixture_root, "transition_contract.json")
    contract = _load(p)
    contract["expected"]["control_only_report_adequate"] = True
    _store(p, contract)
    _redigest(fixture_root, "contract")
    _refused(lambda: rp.invoke_replay_packet(fixture_root),
             "evaluator disagrees with the declared control-only adequacy result")


def test_case_20_terminal_policy_substitution(fixture_root: Path) -> None:
    p = _path(fixture_root, "terminal_policy.json")
    policy = _load(p)
    policy["on_verified"] = "authorized"
    _store(p, policy)
    _redigest(fixture_root, "terminal_policy")
    _refused(lambda: rp.invoke_replay_packet(fixture_root), "terminal policy is not the declared bounded open policy")


@pytest.mark.parametrize(
    "key,value,needle",
    [
        ("json_parser", "unlicensed parser", "JSON parser is not the declared bounded parser"),
        ("formal_replay_workdir", "unlicensed workdir", "formal replay work directory is not licensed"),
        ("formal_replay_command", "unlicensed command", "formal replay command is not licensed"),
    ],
)
def test_cases_21_to_23_execution_profile_substitution(fixture_root: Path, key: str, value: str, needle: str) -> None:
    m = _path(fixture_root, "packet_manifest.json")
    manifest = _load(m)
    manifest["execution_profile"][key] = value
    _store(m, manifest)
    _refused(lambda: rp.check_packet(fixture_root), needle)


def sha256_of_manifest_file() -> str:
    return rp.sha256_file(REPO / _mapped(rp.DEFAULT_MANIFEST))


def test_recorded_artifact_digests_match_formal_binding_manifest() -> None:
    """The digests in the recovered packet manifest equal those listed in formal_binding_manifest.md."""
    text = (REPO / _mapped(rp.ORIGINAL_PREFIX + "formal_binding_manifest.md")).read_text(encoding="utf-8")
    manifest = _load(REPO / _mapped(rp.DEFAULT_MANIFEST))
    listed = {"evaluator", "verifier", "formal_model", "formal_dependency"}
    for artifact in manifest["artifacts"]:
        if artifact["role"] in listed:
            assert artifact["sha256"] in text
    assert sha256_of_manifest_file() in text


def test_verify_refusal_carries_open_terminal(fixture_root: Path) -> None:
    p = _path(fixture_root, "transition_proposal.json")
    p.write_bytes(p.read_bytes() + b" ")
    result = rp.verify(fixture_root)
    assert result["verification_status"] == "refused"
    assert result["terminal"] == "open"
    assert "REPLAY_PACKET_REFUSED" in result["reason"]


def test_path_must_be_repository_relative(fixture_root: Path) -> None:
    _refused(lambda: rp.resolve_path(fixture_root, "/etc/passwd", "x"), "not repository-relative")
    _refused(lambda: rp.resolve_path(fixture_root, "C:/Windows/x", "x"), "not repository-relative")


@pytest.mark.skipif(shutil.which("elan") is None, reason="elan is not installed")
def test_formal_replay_of_bound_original_lean_files() -> None:
    """Integration: the bound ORIGINAL tape models compile under the installed v4.35.0 toolchain."""
    result = rp.verify(REPO, formal_replay=True)
    assert result["verification_status"] == "verified"
    assert result["formal_replay"] == "pass"
    assert result["terminal"] == "open"
