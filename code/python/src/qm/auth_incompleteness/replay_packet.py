"""Bounded SHA-256 replay packet for the four-configuration transition table (Python port).

Origin: PowerShell module replay_packet.psm1 and verify_transition_packet.ps1, recovered from
C:/.ana/coda_university/coda_research/authorization_an_incompleteness_theory/code/replay_packet
(recovery 2026-10-21). The PowerShell sources are kept byte-for-byte under
papers/foundations/authorization_incompleteness/evidence/original/code/ and were read, never run.
Claim: urn:omega:fqm:authincomp:replay-packet-python-port:v1
AuthorityEffect: None

What this computes: it checks that every artifact named by a packet manifest has its licensed role,
path, kind and SHA-256 digest; it parses the proposal, contract and terminal policy under exact key
sets; it enumerates the transition table, tests the clean-terminal contract, finds marked-cell
countertraces and compares the full-configuration report with the control-only report. Terminal is
`open` after a verified replay.

Differences from the PowerShell original (all deliberate):
* The PowerShell 7.6.3 runtime pin is not checked (there is no PowerShell here). The manifest's
  recorded execution-profile strings are still required verbatim.
* Manifest paths are repository-relative in the ORIGINAL layout; `PREFIX_MAP` redirects them to the
  recovered evidence tree. The path-escape, parent-segment and link checks still apply.
* The optional formal replay uses an installed Lean toolchain chosen by `toolchain` (default
  leanprover/lean4:v4.35.0), not the recorded v4.32.2, which is not installed here.

Scope Fence: a verified replay is a bounded finite check under the manifest's own trust root. It is
not custody, collision resistance, evaluator soundness, a Lean-correspondence theorem or authority.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

PACKET_SCHEMA = "coda.authorization_incompleteness.replay-packet.v1"
MANIFEST_SCHEMA = "coda.authorization_incompleteness.packet-manifest.v1"
PACKET_ID = "AIT-G3-FINITE-TRANSITION-REPLAY-V4"
PROPOSAL_SCHEMA = "coda.authorization_incompleteness.transition-proposal.v1"
CONTRACT_SCHEMA = "coda.authorization_incompleteness.transition-contract.v1"
POLICY_SCHEMA = "coda.authorization_incompleteness.terminal-policy.v1"

ORIGINAL_PREFIX = "coda_university/coda_research/authorization_an_incompleteness_theory/"
EVIDENCE_REL = "papers/foundations/authorization_incompleteness/evidence/"
DEFAULT_MANIFEST = ORIGINAL_PREFIX + "code/replay_packet/packet_manifest.json"

# Original repository-relative prefix -> path relative to the recovery repository root.
PREFIX_MAP: dict[str, str] = {
    ORIGINAL_PREFIX: EVIDENCE_REL + "original/",
    "lean4/genx/lean-toolchain": EVIDENCE_REL + "reconstructed/lean-toolchain",
}

EXPECTED_ARTIFACT: dict[str, dict[str, str]] = {
    "proposal": {"path": ORIGINAL_PREFIX + "code/replay_packet/transition_proposal.json", "kind": "proposal"},
    "contract": {"path": ORIGINAL_PREFIX + "code/replay_packet/transition_contract.json", "kind": "contract"},
    "terminal_policy": {"path": ORIGINAL_PREFIX + "code/replay_packet/terminal_policy.json", "kind": "terminal_policy"},
    "evaluator": {"path": ORIGINAL_PREFIX + "code/replay_packet/replay_packet.psm1", "kind": "evaluator"},
    "verifier": {"path": ORIGINAL_PREFIX + "code/replay_packet/verify_transition_packet.ps1", "kind": "verifier"},
    "formal_model": {
        "path": ORIGINAL_PREFIX + "formal/tape_transition_invariant_models.lean",
        "kind": "formal_model",
    },
    "formal_dependency": {
        "path": ORIGINAL_PREFIX + "formal/tape_control_authorization_models.lean",
        "kind": "formal_dependency",
    },
    "lean_toolchain": {"path": "lean4/genx/lean-toolchain", "kind": "lean_toolchain"},
}

CONFIGURATIONS = ("runningBlank", "runningMarked", "haltedBlank", "haltedMarked")
OUTCOMES = ("advance", "stay", "halt")
MANIFEST_KEYS = (
    "schema_version",
    "packet_id",
    "authority_effect",
    "manifest_trust_boundary",
    "terminal_policy",
    "evidence_ceiling",
    "tcb",
    "execution_profile",
    "artifacts",
)
RECORDED_PROFILE = {
    "runtime": "PowerShell 7.6.3; Lean 4.32.2",
    "json_parser": "PowerShell ConvertFrom-Json 7.6.3",
    "lean_toolchain": "leanprover/lean4:v4.32.2",
    "formal_replay_command": "elan run leanprover/lean4:v4.32.2 lean",
    "formal_replay_workdir": ORIGINAL_PREFIX + "formal",
}
DEFAULT_TOOLCHAIN = "leanprover/lean4:v4.35.0"


class ReplayPacketRefusal(Exception):
    """A refusal; the message always starts with REPLAY_PACKET_REFUSED."""

    def __init__(self, message: str) -> None:
        super().__init__("REPLAY_PACKET_REFUSED: " + message)


def refuse(message: str) -> None:
    raise ReplayPacketRefusal(message)


def assert_exact_keys(obj: Any, expected: tuple[str, ...] | list[str], context: str) -> None:
    if not isinstance(obj, dict):
        refuse(f"{context} must be a JSON object")
    actual = set(obj)
    want = set(expected)
    missing = [k for k in expected if k not in actual]
    extra = [k for k in obj if k not in want]
    if missing or extra:
        parts = []
        if missing:
            parts.append("missing: " + ", ".join(missing))
        if extra:
            parts.append("extra: " + ", ".join(extra))
        refuse(f"{context} has an invalid field set ({'; '.join(parts)})")


def assert_non_empty_string(value: Any, context: str) -> None:
    if not isinstance(value, str) or not value.strip():
        refuse(f"{context} must be a non-empty string")


def assert_exact_string_set(value: Any, expected: list[str], context: str) -> None:
    if not isinstance(value, list):
        refuse(f"{context} must be an array of strings")
    if any(not isinstance(item, str) for item in value):
        refuse(f"{context} must contain only strings")
    if len(set(value)) != len(value):
        refuse(f"{context} contains duplicate values")
    if set(value) != set(expected):
        refuse(f"{context} differs from its declared finite carrier")


def _is_link(path: Path) -> bool:
    if path.is_symlink():
        return True
    is_junction = getattr(os.path, "isjunction", None)
    return bool(is_junction and is_junction(path))


def map_path(relative: str, prefix_map: dict[str, str] | None) -> str:
    """Redirect an original-layout relative path through the prefix map."""
    for prefix, target in (prefix_map or {}).items():
        if relative == prefix.rstrip("/") or relative.startswith(prefix):
            return target + relative[len(prefix):]
    return relative


def resolve_path(root: Path, relative: str, context: str, prefix_map: dict[str, str] | None = None) -> Path:
    assert_non_empty_string(relative, f"{context} path")
    if os.path.isabs(relative) or relative.startswith(("/", "\\")) or (len(relative) > 1 and relative[1] == ":"):
        refuse(f"{context} path is not repository-relative")
    segments = relative.replace("\\", "/").split("/")
    if ".." in segments:
        refuse(f"{context} path contains a parent escape")
    base = Path(os.path.abspath(root))
    mapped = map_path(relative.replace("\\", "/"), prefix_map)
    candidate = Path(os.path.abspath(base / mapped))
    if candidate != base and base not in candidate.parents:
        refuse(f"{context} path resolves outside the repository")
    if not candidate.is_file():
        refuse(f"{context} path does not name a file")
    current = base
    for segment in mapped.split("/"):
        current = current / segment
        if _is_link(current):
            refuse(f"{context} path may not traverse a reparse point")
    return candidate


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    seen: dict[str, Any] = {}
    for key, value in pairs:
        if key in seen:
            raise ValueError(f"duplicate JSON property {key}")
        seen[key] = value
    return seen


def read_json(path: Path, context: str) -> dict[str, Any]:
    try:
        text = path.read_bytes().decode("utf-8")
        value = json.loads(text, object_pairs_hook=_no_duplicates)
    except (ValueError, UnicodeDecodeError) as exc:
        refuse(f"{context} is not valid UTF-8 JSON: {exc}")
    if not isinstance(value, dict):
        refuse(f"{context} must be a JSON object")
    return value


def _is_bool(value: Any) -> bool:
    return type(value) is bool


def _check_manifest_header(manifest: dict[str, Any]) -> None:
    assert_exact_keys(manifest, MANIFEST_KEYS, "manifest")
    if manifest["schema_version"] != MANIFEST_SCHEMA:
        refuse("manifest schema version is not supported")
    if manifest["packet_id"] != PACKET_ID:
        refuse("manifest packet identifier is not licensed")
    if manifest["authority_effect"] != "None":
        refuse("manifest must declare AuthorityEffect None")
    if manifest["manifest_trust_boundary"] != "fixed_outside_proposal_bytes":
        refuse("manifest does not declare its proposal-external trust boundary")
    if manifest["terminal_policy"] != "open_after_verified":
        refuse("manifest terminal policy is not the bounded open policy")
    assert_non_empty_string(manifest["evidence_ceiling"], "manifest evidence ceiling")
    tcb_fields = ("hash_algorithm", "collision_resistance_assumption", "evaluator_soundness_assumption", "custody_assumption")
    assert_exact_keys(manifest["tcb"], tcb_fields, "manifest trusted computing base")
    if manifest["tcb"]["hash_algorithm"] != "SHA-256":
        refuse("manifest names an unsupported hash algorithm")
    for field in tcb_fields[1:]:
        assert_non_empty_string(manifest["tcb"][field], f"manifest tcb {field}")


def _check_execution_profile(profile: Any) -> None:
    assert_exact_keys(profile, tuple(RECORDED_PROFILE), "manifest execution profile")
    messages = {
        "runtime": "manifest execution profile is not the declared bounded profile",
        "json_parser": "manifest JSON parser is not the declared bounded parser",
        "lean_toolchain": "manifest Lean toolchain is not the declared bounded toolchain",
        "formal_replay_command": "manifest formal replay command is not licensed",
        "formal_replay_workdir": "manifest formal replay work directory is not licensed",
    }
    for key, message in messages.items():
        if profile[key] != RECORDED_PROFILE[key]:
            refuse(message)


def manifest_artifact_paths(manifest: dict[str, Any], root: Path, prefix_map: dict[str, str] | None) -> dict[str, Path]:
    artifacts = manifest["artifacts"]
    if not isinstance(artifacts, list):
        refuse("manifest artifacts must be an array")
    if len(artifacts) != len(EXPECTED_ARTIFACT):
        refuse("manifest does not bind the exact artifact inventory")
    seen: set[str] = set()
    paths: dict[str, Path] = {}
    for artifact in artifacts:
        assert_exact_keys(artifact, ("role", "path", "kind", "sha256"), "manifest artifact")
        assert_non_empty_string(artifact["role"], "manifest artifact role")
        role = artifact["role"]
        if role in seen:
            refuse("manifest contains a duplicate artifact role")
        seen.add(role)
        if role not in EXPECTED_ARTIFACT:
            refuse(f"manifest names an unlicensed artifact role {role}")
        expected = EXPECTED_ARTIFACT[role]
        actual = resolve_path(root, artifact["path"], f"artifact {role}", prefix_map)
        if artifact["path"] != expected["path"]:
            refuse(f"artifact {role} does not use its licensed path")
        if artifact["kind"] != expected["kind"]:
            refuse(f"artifact {role} does not use its licensed kind")
        digest = artifact["sha256"]
        if not isinstance(digest, str) or len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
            refuse(f"artifact {role} has an invalid SHA-256 digest")
        if sha256_file(actual) != digest:
            refuse(f"artifact digest mismatch for {role}")
        paths[role] = actual
    for role in EXPECTED_ARTIFACT:
        if role not in seen:
            refuse(f"manifest omits artifact role {role}")
    return paths


def check_packet(
    root: str | Path,
    manifest_path: str = DEFAULT_MANIFEST,
    prefix_map: dict[str, str] | None = PREFIX_MAP,
) -> dict[str, Any]:
    """Port of Test-ReplayPacket: verify the manifest and every bound artifact digest."""
    root = Path(root)
    manifest_file = resolve_path(root, manifest_path, "manifest", prefix_map)
    manifest = read_json(manifest_file, "manifest")
    _check_manifest_header(manifest)
    _check_execution_profile(manifest["execution_profile"])
    paths = manifest_artifact_paths(manifest, root, prefix_map)
    declared = paths["lean_toolchain"].read_bytes().decode("utf-8").strip()
    if declared != manifest["execution_profile"]["lean_toolchain"]:
        refuse("Lean toolchain file does not match the declared runtime")
    return {"valid": True, "manifest": manifest, "artifact_paths": paths}


def _check_proposal(proposal: Any) -> dict[str, dict[str, str]]:
    assert_exact_keys(proposal, ("schema_version", "proposal_id", "authority_effect", "source_claimed_pass", "transitions"), "proposal")
    if proposal["schema_version"] != PROPOSAL_SCHEMA:
        refuse("proposal schema version is not supported")
    if proposal["proposal_id"] != "finite-transition-table-v1":
        refuse("proposal identifier is not licensed")
    if proposal["authority_effect"] != "None":
        refuse("proposal must declare AuthorityEffect None")
    if not _is_bool(proposal["source_claimed_pass"]):
        refuse("proposal source_claimed_pass must be Boolean")
    rows = proposal["transitions"]
    if not isinstance(rows, list):
        refuse("proposal transitions must be an array")
    if len(rows) != len(CONFIGURATIONS):
        refuse("proposal does not contain one transition for every configuration")
    table: dict[str, dict[str, str]] = {}
    for row in rows:
        assert_exact_keys(row, ("from", "outcome", "to"), "transition row")
        for field in ("from", "outcome", "to"):
            assert_non_empty_string(row[field], f"transition {field}")
        if row["from"] not in CONFIGURATIONS or row["to"] not in CONFIGURATIONS:
            refuse("transition configuration is outside the declared carrier")
        if row["outcome"] not in OUTCOMES:
            refuse("transition outcome is outside the declared carrier")
        if row["from"] in table:
            refuse("proposal contains a duplicate transition source")
        table[row["from"]] = row
    for configuration in CONFIGURATIONS:
        if configuration not in table:
            refuse(f"proposal omits transition source {configuration}")
    return table


def _check_contract(contract: Any) -> None:
    assert_exact_keys(
        contract,
        ("schema_version", "contract_id", "authority_effect", "clean_terminal_rejects", "marked_cell_accepts", "reports", "expected"),
        "contract",
    )
    if contract["schema_version"] != CONTRACT_SCHEMA:
        refuse("contract schema version is not supported")
    if contract["contract_id"] != "finite-transition-adequacy-v1":
        refuse("contract identifier is not licensed")
    if contract["authority_effect"] != "None":
        refuse("contract must declare AuthorityEffect None")
    assert_exact_string_set(contract["clean_terminal_rejects"], ["haltedMarked"], "contract clean_terminal_rejects")
    assert_exact_string_set(contract["marked_cell_accepts"], ["runningMarked", "haltedMarked"], "contract marked_cell_accepts")
    assert_exact_keys(contract["reports"], ("full_report", "control_only_report"), "contract reports")
    if contract["reports"]["full_report"] != "configuration" or contract["reports"]["control_only_report"] != "transition_control":
        refuse("contract report interfaces are not the declared pair")
    expected = contract["expected"]
    assert_exact_keys(
        expected,
        ("clean_terminal_preserved", "required_marked_countertrace", "full_report_adequate", "control_only_report_adequate", "control_only_authorization"),
        "contract expected results",
    )
    for field in ("clean_terminal_preserved", "full_report_adequate", "control_only_report_adequate"):
        if not _is_bool(expected[field]):
            refuse(f"contract expected {field} must be Boolean")
    if expected["required_marked_countertrace"] != "runningMarked":
        refuse("contract expected required_marked_countertrace is not licensed")
    if expected["control_only_authorization"] != "open_due_to_inadequate_report":
        refuse("contract expected control_only_authorization is not licensed")


def _control_counterexample(table: dict[str, dict[str, str]], marked_accepts: list[str]) -> dict[str, str] | None:
    groups: dict[str, list[str]] = {}
    for configuration in CONFIGURATIONS:
        groups.setdefault(table[configuration]["outcome"], []).append(configuration)
    for report, group in groups.items():
        for i, left in enumerate(group):
            for right in group[i + 1:]:
                if (left in marked_accepts) != (right in marked_accepts):
                    return {"report": report, "first": left, "second": right}
    return None


def transition_evaluation(proposal: Any, contract: Any) -> dict[str, Any]:
    """Port of Get-TransitionEvaluation (exact-key checks, then enumeration, then expectation checks)."""
    table = _check_proposal(proposal)
    _check_contract(contract)
    clean_rejects = contract["clean_terminal_rejects"]
    marked_accepts = contract["marked_cell_accepts"]
    clean_preserved = True
    countertraces: list[dict[str, str]] = []
    for configuration in CONFIGURATIONS:
        successor = table[configuration]["to"]
        if successor in clean_rejects:
            clean_preserved = False
        if configuration in marked_accepts and successor not in marked_accepts:
            countertraces.append({"source": configuration, "successor": successor})
    counterexample = _control_counterexample(table, marked_accepts)
    control_adequate = counterexample is None
    evaluation = {
        "clean_terminal_preserved": clean_preserved,
        "marked_countertraces": countertraces,
        "full_report_adequate": True,  # identity report: constant by construction, as in the original
        "control_only_report_adequate": control_adequate,
        "control_only_counterexample": counterexample,
        "control_only_authorization": "eligible_for_scoped_decision" if control_adequate else "open_due_to_inadequate_report",
        "source_claimed_pass_used": False,
    }
    expected = contract["expected"]
    if evaluation["clean_terminal_preserved"] != expected["clean_terminal_preserved"]:
        refuse("evaluator disagrees with the declared clean-terminal result")
    if evaluation["full_report_adequate"] != expected["full_report_adequate"]:
        refuse("evaluator disagrees with the declared full-report adequacy result")
    if evaluation["control_only_report_adequate"] != expected["control_only_report_adequate"]:
        refuse("evaluator disagrees with the declared control-only adequacy result")
    if evaluation["control_only_authorization"] != expected["control_only_authorization"]:
        refuse("evaluator disagrees with the declared control-only authorization route")
    if expected["required_marked_countertrace"] not in [c["source"] for c in countertraces]:
        refuse("evaluator did not find the required marked-cell countertrace")
    return evaluation


def invoke_replay_packet(
    root: str | Path,
    manifest_path: str = DEFAULT_MANIFEST,
    prefix_map: dict[str, str] | None = PREFIX_MAP,
) -> dict[str, Any]:
    """Port of Invoke-ReplayPacket: bindings, then terminal policy, then evaluation."""
    packet = check_packet(root, manifest_path, prefix_map)
    paths = packet["artifact_paths"]
    proposal = read_json(paths["proposal"], "proposal")
    contract = read_json(paths["contract"], "contract")
    policy = read_json(paths["terminal_policy"], "terminal policy")
    assert_exact_keys(policy, ("schema_version", "policy_id", "authority_effect", "on_verified", "on_rejected"), "terminal policy")
    if (
        policy["schema_version"] != POLICY_SCHEMA
        or policy["policy_id"] != "leave-verified-open-v1"
        or policy["authority_effect"] != "None"
        or policy["on_verified"] != "open"
        or policy["on_rejected"] != "rejected"
    ):
        refuse("terminal policy is not the declared bounded open policy")
    evaluation = transition_evaluation(proposal, contract)
    return {
        "schema_version": PACKET_SCHEMA,
        "packet_id": packet["manifest"]["packet_id"],
        "authority_effect": "None",
        "verification_status": "verified",
        "terminal": policy["on_verified"],
        "source_claimed_pass": proposal["source_claimed_pass"],
        "source_claimed_pass_used": evaluation["source_claimed_pass_used"],
        "evaluation": evaluation,
    }


def run_formal_replay(packet: dict[str, Any], toolchain: str = DEFAULT_TOOLCHAIN, elan: str | None = None) -> str:
    """Compile the bound dependency then the bound transition model with an installed Lean.

    Mirrors the PowerShell `-RunFormalReplay` switch: the dependency is compiled to a temporary
    .olean, the model is compiled against it, and the temporary directory is removed. Returns
    "pass"; raises ReplayPacketRefusal on any compilation failure.
    """
    elan = elan or shutil.which("elan")
    if elan is None:
        refuse("formal replay requires elan on PATH")
    dependency = Path(packet["artifact_paths"]["formal_dependency"])
    model = Path(packet["artifact_paths"]["formal_model"])
    with tempfile.TemporaryDirectory(prefix="ait-formal-replay-") as tmp:
        out = Path(tmp) / (dependency.stem + ".olean")
        first = subprocess.run([elan, "run", toolchain, "lean", "-o", str(out), str(dependency)],
                               capture_output=True, text=True, cwd=dependency.parent, check=False)
        if first.returncode != 0:
            refuse("local formal dependency compilation failed")
        env = dict(os.environ, LEAN_PATH=tmp)
        second = subprocess.run([elan, "run", toolchain, "lean", str(model)],
                                capture_output=True, text=True, cwd=model.parent, env=env, check=False)
        if second.returncode != 0:
            refuse("local formal model compilation failed")
    return "pass"


def verify(root: str | Path, formal_replay: bool = False, toolchain: str = DEFAULT_TOOLCHAIN,
           manifest_path: str = DEFAULT_MANIFEST, prefix_map: dict[str, str] | None = PREFIX_MAP) -> dict[str, Any]:
    """Port of verify_transition_packet.ps1: a verified result dict or a refusal dict (terminal open)."""
    try:
        packet = check_packet(root, manifest_path, prefix_map)
        result = invoke_replay_packet(root, manifest_path, prefix_map)
        result["formal_replay"] = run_formal_replay(packet, toolchain) if formal_replay else "not_requested"
        return result
    except ReplayPacketRefusal as exc:
        return {
            "schema_version": PACKET_SCHEMA,
            "authority_effect": "None",
            "verification_status": "refused",
            "terminal": "open",
            "reason": str(exc),
        }


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", default=".")
    parser.add_argument("--formal-replay", action="store_true")
    parser.add_argument("--toolchain", default=DEFAULT_TOOLCHAIN)
    args = parser.parse_args(argv)
    result = verify(args.root, args.formal_replay, args.toolchain)
    print(json.dumps(result, indent=2))
    return 0 if result["verification_status"] == "verified" else 1


if __name__ == "__main__":
    raise SystemExit(main())
