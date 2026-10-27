"""Replay reviewed C500 computations and check their evidence inventory.

This is a consistency/replay gate, not campaign launch approval or semantic proof.
The review source revision remains a trust input. AuthorityEffect: None.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[4] / "apps/finite_qm/campaigns/c500_execution"
APP_ROOT = ROOT.parents[1]
GIT_ROOT = Path(__file__).resolve().parents[4]
EVIDENCE_ROOTS = {
    "app": "apps/finite_qm",
    "rust_workspace": "omega_engine/crates_rs",
    "python_crate": "omega_engine/crates/finite_qm",
}
PUBLICATION_SOURCE_COMMIT = "b1b749a9c8fb1e61492673c251deb791ff2501a9"
BLOCK_MODULES = (
    ("weyl_ccr_residual", "WeylCcrResidual"),
    ("norm_approximation_frontier", "NormApproximationFrontier"),
    ("heisenberg_representation_uniqueness", "HeisenbergRepresentationUniqueness"),
    ("refinement_subsystem_tower", "RefinementSubsystemTower"),
    ("tower_topological_completion", "TowerTopologicalCompletion"),
    ("continuous_time_locality_limit", "ContinuousTimeLocalityLimit"),
    ("operational_axiom_selection", "OperationalAxiomSelection"),
    ("tensor_commuting_correlation_frontier", "TensorCommutingCorrelationFrontier"),
    ("lattice_gauge_manybody_benchmark", "LatticeGaugeManybodyBenchmark"),
    ("finite_operational_closure_contract", "FiniteOperationalClosureContract"),
)
DIGEST_RULE = "sha256(utf8_text_with_LF_line_endings)"
REVIEW_STATUS = "SCOPED_COMPUTATIONS_WITH_OPEN_TARGETS"
CLAUSE = re.compile(r"^([MJ]\d+) \[(NOT FORCED|FORCED)\]: (.*)$")
TARGET = re.compile(r"^\| (C500-T\d{3}) \| (.*?) \| (.*?) \|$")
FROZEN_PLAN_SHA256 = {
    "block_01": "9490911869d18169ce584a398530a55eadf6abfe4acd37173762bdf3a2be99c5",
    "block_02": "4b4188065551b95bcfeba943915f18703a5c85203fc61f1917828c7d78099fca",
    "block_03": "6d276cf5f12bf3f1cb094cfd610dd02ba6d55b3e686704d4b811ad24e711b712",
    "block_04": "27041266bfd273b5922a39c1d2f9f8e7b688311d0d44b301526ba448a06db4c6",
    "block_05": "682db6ca60d68c278539712312277f2400a6c026fd0c2a1bd8603e075d754511",
    "block_06": "ee832f4bbdeb684be1f38cae4f0504096384ce7f0dff542f32cfeb4f008d8cef",
    "block_07": "c70cbd4f6aa0a86473495eacfb94428872802ac62c4f5b65b5f65a0d90379307",
    "block_08": "e1e536aad508654c1314df11e8390938aafe46d47c4d078d4360ab61d98eb9e3",
    "block_09": "4dec62938cd44a7151a3f990bcb50039f7b6e32b76d4b95fdf3fa2619d5bd149",
    "block_10": "eafefb6147bcccbc73d4fde06959039644b57d74a8a7ec44e5d444f59121804b",
}


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise AssertionError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object)


def canonical_json(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def checked_path(relative):
    if not isinstance(relative, str) or "\\" in relative:
        raise AssertionError(f"invalid evidence path: {relative!r}")
    posix = PurePosixPath(relative)
    if not posix.parts or posix.is_absolute() or any(part in {".", ".."} for part in relative.split("/")):
        raise AssertionError(f"escaped evidence path: {relative}")
    base = APP_ROOT
    if posix.parts[0] in {"rust_workspace", "python_crate"}:
        if len(posix.parts) < 2:
            raise AssertionError(f"invalid evidence path: {relative!r}")
        repository = APP_ROOT.parents[1].resolve()
        base = repository / EVIDENCE_ROOTS[posix.parts[0]]
        if repository not in base.resolve().parents:
            raise AssertionError(f"escaped evidence root: {relative}")
        posix = PurePosixPath(*posix.parts[1:])
    path = base / posix
    if not path.is_file() or base.resolve() not in path.resolve().parents:
        raise AssertionError(f"missing or escaped evidence file: {relative}")
    return path


_SUPERSESSION_CACHE = {}


def supersession():
    """The withdrawal record beside the frozen manifest, or {} when there is none.

    Read once per (path, mtime, size): a full --check resolves 750 scoped-evidence
    references, and re-parsing this file for each of them was pure waste. The key
    includes mtime and size so a rewritten record is picked up, and the path so the
    fixtures' redirected ROOT never reads a cached copy of the real one.
    """
    path = ROOT / "replay_manifest_supersession.json"
    if not path.is_file():
        return {}
    stat = path.stat()
    key = (str(path), stat.st_mtime_ns, stat.st_size)
    if key not in _SUPERSESSION_CACHE:
        _SUPERSESSION_CACHE.clear()
        _SUPERSESSION_CACHE[key] = read_json(path)
    return _SUPERSESSION_CACHE[key]


def withdrawn_evidence():
    """Rows the replay manifest froze whose files have since been withdrawn."""
    return {row["path"]: row for row in supersession().get("withdrawn_entries", [])}


def adapted_evidence():
    """Rows still present whose bytes changed when their imports were repointed."""
    return {row["path"]: row for row in supersession().get("adapted_entries", [])}


def checked_reference(relative):
    """Resolve a frozen review's evidence reference.

    The block reviews are frozen and still name the files they were written
    against. Where such a file was a compatibility facade that has since been
    withdrawn, it is no longer in the working tree, so the reference is
    satisfied by the blob the supersession pins -- read and rehashed here, not
    taken on trust. Every other reference resolves in the tree as before.
    """
    row = withdrawn_evidence().get(relative)
    if row is None:
        return checked_path(relative)
    blob = subprocess.run(
        ["git", "cat-file", "blob", row["git_blob_oid"]],
        cwd=GIT_ROOT, capture_output=True,
    )
    if blob.returncode != 0 or not blob.stdout:
        raise AssertionError(f"withdrawn evidence unrecoverable in git: {relative}")
    if hashlib.sha256(blob.stdout.replace(b"\r\n", b"\n")).hexdigest() != row["recorded_sha256"]:
        raise AssertionError(f"withdrawn evidence does not match its recorded digest: {relative}")
    return None


def digest(path):
    data = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def frozen_targets(block):
    path = APP_ROOT / "campaigns/c500" / f"block_{block:02d}" / "PLAN.md"
    if digest(path) != FROZEN_PLAN_SHA256[f"block_{block:02d}"]:
        raise AssertionError(f"frozen plan digest changed: block_{block:02d}")
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        match = TARGET.fullmatch(line)
        if match:
            rows.append({"id": match[1], "action": match[2], "required_exit_evidence": match[3]})
    expected = [f"C500-T{n}" for n in range(301 + (block - 1) * 25, 326 + (block - 1) * 25)]
    if [row["id"] for row in rows] != expected:
        raise AssertionError(f"invalid frozen target inventory: block_{block:02d}")
    return rows


def frozen_clauses(path):
    clauses = []
    current = None
    for line in path.read_text(encoding="utf-8").splitlines():
        match = CLAUSE.fullmatch(line)
        if match:
            current = {"id": match[1], "forced": match[2] == "FORCED", "clause": match[3]}
            clauses.append(current)
        elif not line.strip():
            current = None
        elif current is not None:
            current["clause"] += " " + line.strip()
    if not clauses or len({row["id"] for row in clauses}) != len(clauses):
        raise AssertionError(f"invalid frozen clause inventory: {path}")
    return clauses


def verify_scores(rows, frozen):
    if not isinstance(rows, list) or len(rows) != len(frozen):
        raise AssertionError("incomplete clause score inventory")
    for actual, expected in zip(rows, frozen):
        if {key: actual.get(key) for key in expected} != expected:
            raise AssertionError(f"frozen clause changed: {expected['id']}")
        if actual.get("resolution") not in {"OPEN", "SCOPED_EVIDENCE", "INVALID"}:
            raise AssertionError(f"unsupported original-scope score: {expected['id']}")
        if not isinstance(actual.get("reason"), str) or not actual["reason"].strip():
            raise AssertionError(f"missing score reason: {expected['id']}")


def verify_review(block):
    path = ROOT / f"block_{block:02d}" / "review.json"
    review = read_json(path)
    expected = {
        "authority_effect": "None", "block": f"block_{block:02d}",
        "review_status": REVIEW_STATUS, "launch_preconditions": "NOT_ESTABLISHED",
        "campaign_target_execution_certified": False,
        "publication_source_commit": PUBLICATION_SOURCE_COMMIT,
    }
    for key, value in expected.items():
        if review.get(key) != value or type(review.get(key)) is not type(value):
            raise AssertionError(f"review scope changed: {path}: {key}")
    targets = review.get("targets")
    frozen = frozen_targets(block)
    if not isinstance(targets, list) or len(targets) != len(frozen):
        raise AssertionError(f"incomplete target review: {path}")
    for actual, target in zip(targets, frozen):
        if {key: actual.get(key) for key in target} != target:
            raise AssertionError(f"frozen target changed: {target['id']}")
        if actual.get("evidence_class") != "OPEN" or actual.get("plan_target_satisfied") is not False:
            raise AssertionError(f"unsupported target completion: {target['id']}")
        if not isinstance(actual.get("reason"), str) or not actual["reason"].strip():
            raise AssertionError(f"missing target disposition: {target['id']}")
        if not isinstance(actual.get("scoped_evidence"), list) or not actual["scoped_evidence"]:
            raise AssertionError(f"missing scoped evidence location: {target['id']}")
        for reference in actual["scoped_evidence"]:
            checked_reference(reference.split("::", 1)[0])
    bet = APP_ROOT / "campaigns/c500" / f"block_{block:02d}/bets/BET-CODEX-C500-B{block:02d}.txt"
    verify_scores(review.get("scores"), frozen_clauses(bet))
    return review


def evidence_paths():
    paths = {
        "campaigns/c500/sealed_targets.json", "campaigns/c500/INSTRUCTIONS.md",
        "campaigns/c500/README.md", "campaigns/c500/SOURCE_ANCHORS.md",
        "campaigns/c500/tools/verify_campaign.py", "campaigns/c500/bets/BET-CODEX-C500-STANDING.txt",
        "campaigns/c500_execution/README.md", "campaigns/c500_execution/WITHDRAWAL.md",
        "campaigns/c500_execution/withdrawn_pin_audit.json",
        "campaigns/c500_execution/standing_review.json", "campaigns/c500_execution/SCORE_STANDING.md",
        "claims/claim_ledger.yaml", "claims/gap_register.yaml", "finite_quantum_mechanics_claim_ledger.md",
        "finite_quantum_mechanics.md", "code/tests/unit/test_paper_consistency.py",
        "python_crate/local_source_relocation.json",
        "python_crate/__init__.py",
        "python_crate/domain/__init__.py",
        "python_crate/use_cases/__init__.py",
        "python_crate/entrypoints/__init__.py",
        "python_crate/domain/gaussian_rational.py",
        "python_crate/entrypoints/consolidate_sources.py",
        "python_crate/entrypoints/c500_verify_execution.py",
        "python_crate/use_cases/audit_map.py",
        "code_rs/Cargo.toml", "code_rs/Cargo.lock", "code_rs/src/lib.rs",
        "rust_workspace/Cargo.toml", "rust_workspace/Cargo.lock",
        "rust_workspace/omega_finite_qm/Cargo.toml",
        "rust_workspace/omega_finite_qm/local_source_relocation.json",
        "rust_workspace/omega_finite_qm/src/rational.rs",
        "rust_workspace/omega_finite_qm/src/lib.rs",
        "rust_workspace/omega_finite_qm/src/bin/finite_qm_cli.rs",
        "lean4/lean-toolchain", "lean4/lakefile.lean",
        "code/tests/unit/test_c500_campaign.py", "code/tests/unit/test_c500_execution.py",
        "code/tests/unit/test_c500_b01_b02_review.py",
        "code/tests/unit/test_c500_review_parity.py",
        "code/tests/unit/test_weyl_rust_parity.py",
        "rust_workspace/omega_finite_qm/tests/c500_cli_review.rs",
        "evidence/lake_replay_20260905.json", "evidence/c500_native_review_20260907.json",
    }
    for block, (module, lean) in enumerate(BLOCK_MODULES, start=1):
        paths.update({
            f"rust_workspace/omega_finite_qm/src/{module}.rs", f"lean4/{lean}.lean",
            f"python_crate/use_cases/{module}.py",
            f"code/tests/unit/test_{module}.py", f"evidence/{module}.json",
            f"campaigns/c500/block_{block:02d}/PLAN.md",
            f"campaigns/c500/block_{block:02d}/bets/BET-CODEX-C500-B{block:02d}.txt",
        })
        for name in ("result.json", "review.json", "RESULT.md", "SCORE.md"):
            paths.add(f"campaigns/c500_execution/block_{block:02d}/{name}")
    return sorted(paths)


def manifest():
    return {
        "authority_effect": "None", "digest_rule": DIGEST_RULE,
        "scope": "CURRENT_FILE_REPLAY_NOT_PRE_EXECUTION_CUSTODY",
        "publication_source_commit": PUBLICATION_SOURCE_COMMIT,
        "logical_roots": EVIDENCE_ROOTS,
        "files": [{"path": name, "sha256": digest(checked_path(name))} for name in evidence_paths()],
    }


def recorded_equivalent_manifest():
    """What the frozen manifest should say, given what has been withdrawn since.

    Live files contribute their current digest, except those the supersession
    marks adapted, which contribute the digest the manifest froze. Withdrawn
    rows contribute their frozen digest too. With no supersession present this
    is exactly `manifest()`.
    """
    withdrawn = withdrawn_evidence()
    adapted = adapted_evidence()
    live = manifest()
    composed = dict(live)
    composed["files"] = sorted(
        [
            {"path": f["path"], "sha256": adapted[f["path"]]["recorded_sha256"]}
            if f["path"] in adapted else f
            for f in live["files"]
        ]
        + [{"path": p, "sha256": r["recorded_sha256"]} for p, r in withdrawn.items()],
        key=lambda row: row["path"],
    )
    return composed


def verify_manifest():
    """Check the frozen manifest against what is on disk plus what was withdrawn.

    `replay_manifest.json` is left exactly as it was recorded. Some of the files
    it lists were compatibility facades that have since been withdrawn, so they
    are no longer on disk; `replay_manifest_supersession.json` names those rows
    and carries, for each, the sha256 the manifest recorded and the git blob id
    that still holds those bytes. A row is therefore satisfied either by the
    working tree or by that blob -- and the blob is read and rehashed here, so
    withdrawal is checked rather than asserted.
    """
    recorded = read_json(ROOT / "replay_manifest.json")

    for relative, row in withdrawn_evidence().items():
        blob = subprocess.run(
            ["git", "cat-file", "blob", row["git_blob_oid"]],
            cwd=GIT_ROOT, capture_output=True,
        )
        if blob.returncode != 0 or not blob.stdout:
            raise AssertionError(f"withdrawn evidence unrecoverable in git: {relative}")
        actual = hashlib.sha256(blob.stdout.replace(b"\r\n", b"\n")).hexdigest()
        if actual != row["recorded_sha256"]:
            raise AssertionError(f"withdrawn evidence does not match its recorded digest: {relative}")

    for relative, row in adapted_evidence().items():
        blob = subprocess.run(
            ["git", "cat-file", "blob", row["git_blob_oid_of_recorded_bytes"]],
            cwd=GIT_ROOT, capture_output=True,
        )
        if blob.returncode != 0 or not blob.stdout:
            raise AssertionError(f"adapted evidence: recorded bytes unrecoverable in git: {relative}")
        was = hashlib.sha256(blob.stdout.replace(b"\r\n", b"\n")).hexdigest()
        if was != row["recorded_sha256"]:
            raise AssertionError(f"adapted evidence: recorded digest does not match its blob: {relative}")
        if "current_sha256" not in row:
            raise AssertionError(f"adapted evidence: no current digest recorded: {relative}")
        if digest(checked_path(relative)) != row["current_sha256"]:
            raise AssertionError(f"adapted evidence changed since it was recorded: {relative}")

    if recorded != recorded_equivalent_manifest():
        raise AssertionError("replay manifest mismatch: missing, extra, stale, or changed evidence")


def replay_block(block, module):
    source = checked_path(f"python_crate/use_cases/{module}.py")
    script = """
import importlib.util, json, pathlib, sys
sys.dont_write_bytecode = True
sys.path.insert(0, sys.argv[1])
source = pathlib.Path(sys.argv[2]).resolve()
spec = importlib.util.spec_from_file_location('c500_selected_source', source)
loaded = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = loaded
spec.loader.exec_module(loaded)
assert pathlib.Path(loaded.__file__).resolve() == source
result = getattr(loaded, f'generate_canonical_block{int(sys.argv[3]):02d}_receipt')()
print(json.dumps(result, sort_keys=True, separators=(',', ':'), allow_nan=False))
"""
    replay = subprocess.run(
        [sys.executable, "-I", "-c", script, str(APP_ROOT.parents[1]), str(source), str(block)],
        capture_output=True, text=True, timeout=120,
    )
    if replay.returncode:
        raise AssertionError(f"selected Python source replay failed: {source}: {replay.stderr}")
    generated = json.loads(replay.stdout, object_pairs_hook=unique_object)
    expected = canonical_json(generated)
    for path in (APP_ROOT / f"evidence/{module}.json", ROOT / f"block_{block:02d}/result.json"):
        value = read_json(path)
        if "sha_pinned_predecessors" in value:
            raise AssertionError(f"kernel must not self-assert predecessor custody: {path}")
        if canonical_json(value) != expected:
            raise AssertionError(f"generated computation does not replay: {path}")


def verify_ledgers(reviews):
    import yaml

    ledger = yaml.safe_load((APP_ROOT / "claims/claim_ledger.yaml").read_text(encoding="utf-8"))
    rows = [row for row in ledger["application_claims"] if row["id"].startswith("FQM-C500-")]
    expected_ids = [f"FQM-C500-B{block:02d}-{number:03d}" for block in range(1, 11) for number in range(1, 5)]
    if [row["id"] for row in rows] != expected_ids:
        raise AssertionError("C500 application claim inventory changed")
    for row in rows:
        if row.get("type") not in {"FINITE COMPUTATION", "CONDITIONAL", "SCOPE FENCE", "OPEN"}:
            raise AssertionError(f"unsupported application claim type: {row['id']}")
        block = int(row["id"].split("-")[2][1:])
        expected_review = f"campaigns/c500_execution/block_{block:02d}/review.json"
        if row.get("review_record") != expected_review:
            raise AssertionError(f"missing application claim review: {row['id']}")
    register = yaml.safe_load((APP_ROOT / "claims/gap_register.yaml").read_text(encoding="utf-8"))
    gaps = {row["gap_id"]: row for row in register["gaps"]}
    for block, review in enumerate(reviews, start=1):
        gap = gaps.get(f"GAP-C500-B{block:02d}", {})
        targets = [row["id"] for row in review["targets"]]
        clauses = [row["id"] for row in review["scores"] if row["resolution"] in {"OPEN", "INVALID"}]
        if gap.get("unresolved_targets") != targets or gap.get("open_or_invalid_bet_clauses") != clauses:
            raise AssertionError(f"missing target/score gap disposition: block_{block:02d}")
    standing = read_json(ROOT / "standing_review.json")
    unresolved = [row["id"] for row in standing["scores"] if row["resolution"] in {"OPEN", "INVALID"}]
    if gaps.get("GAP-C500-LAUNCH", {}).get("open_or_invalid_standing_clauses") != unresolved:
        raise AssertionError("missing standing score gap disposition")


def verify(*, replay=True):
    verify_manifest()
    source = APP_ROOT / "campaigns/c500/tools/verify_campaign.py"
    spec = importlib.util.spec_from_file_location("c500_execution_planning_custody", source)
    planning = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(planning)
    planning.verify()
    reviews = []
    for block, (module, _) in enumerate(BLOCK_MODULES, start=1):
        reviews.append(verify_review(block))
        if replay:
            replay_block(block, module)
    verify_ledgers(reviews)
    standing = read_json(ROOT / "standing_review.json")
    if standing.get("launch_preconditions") != "NOT_ESTABLISHED" or standing.get("bettor_accuracy") is not None:
        raise AssertionError("standing review cannot claim original-scope campaign accuracy")
    bet = APP_ROOT / "campaigns/c500/bets/BET-CODEX-C500-STANDING.txt"
    verify_scores(standing.get("scores"), frozen_clauses(bet))
    return {
        "authority_effect": "None", "status": REVIEW_STATUS,
        "launch_preconditions": "NOT_ESTABLISHED", "reviewed_blocks": len(BLOCK_MODULES),
        "open_targets": len(BLOCK_MODULES) * 25, "campaign_target_execution_certified": False,
        "python_receipts_replayed": len(BLOCK_MODULES) if replay else 0,
        "semantic_proof_or_launch_approval": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--check", action="store_true", help="check hashes, review census, and reexecute ten kernels")
    action.add_argument("--write-manifest", action="store_true", help="record current files after review; does not validate claims")
    args = parser.parse_args()
    if args.write_manifest:
        record_path = ROOT / "replay_manifest_supersession.json"
        if record_path.is_file():
            record = read_json(record_path)
            for row in record.get("adapted_entries", []):
                row["current_sha256"] = digest(checked_path(row["path"]))
            record_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
            _SUPERSESSION_CACHE.clear()
        path = ROOT / "replay_manifest.json"
        path.write_text(
            json.dumps(recorded_equivalent_manifest(), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        print("Recorded current replay inventory; run --check to validate.")
    else:
        print(json.dumps(verify(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

__all__ = ['APP_ROOT', 'BLOCK_MODULES', 'CLAUSE', 'DIGEST_RULE', 'EVIDENCE_ROOTS', 'FROZEN_PLAN_SHA256', 'PUBLICATION_SOURCE_COMMIT', 'REVIEW_STATUS', 'ROOT', 'TARGET', 'canonical_json', 'checked_path', 'digest', 'evidence_paths', 'frozen_clauses', 'frozen_targets', 'main', 'manifest', 'read_json', 'replay_block', 'unique_object', 'verify', 'verify_ledgers', 'verify_manifest', 'verify_review', 'verify_scores']
