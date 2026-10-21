"""Explicit, revision-bound source verification. No historical/current fallback."""
from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import subprocess
import tempfile
from importlib.resources import files
from pathlib import Path, PurePosixPath


def _root(value: Path) -> Path:
    root = value.resolve(strict=True)
    if not (root / "omega_engine/crates_rs/Cargo.toml").is_file() or not (root / ".git").exists():
        raise ValueError("PROJECT_ROOT_MUST_BE_THE_SYMBOL_GAME_CHECKOUT")
    return root


def _git(root: Path, *args: str) -> bytes:
    result = subprocess.run(["git", "-C", str(root), *args], capture_output=True, timeout=60, check=False)
    if result.returncode:
        raise ValueError("HISTORICAL_BYTES_UNAVAILABLE:" + result.stderr.decode("utf-8", errors="replace").strip())
    return result.stdout


def _unique_receipt_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("DUPLICATE_RECEIPT_KEY:" + key)
        result[key] = value
    return result


def _regular_file_snapshot(path: Path) -> tuple[tuple, bytes]:
    """Bind file identity as well as bytes; never follow a replaced control."""
    def identity(info):
        change_time = getattr(info, "st_birthtime_ns", info.st_ctime_ns) if os.name == "nt" else info.st_ctime_ns
        return (info.st_dev, info.st_ino, info.st_mode, info.st_size,
                info.st_mtime_ns, change_time, getattr(info, "st_file_attributes", 0))

    try:
        before = path.lstat()
        if (not stat.S_ISREG(before.st_mode)
                or getattr(before, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT):
            raise ValueError("EVIDENCE_CONTROL_NOT_REGULAR:" + str(path))
        with path.open("rb") as handle:
            opened = os.fstat(handle.fileno())
            if identity(opened) != identity(before):
                raise ValueError("EVIDENCE_CONTROL_CHANGED:" + str(path))
            content = handle.read()
            after = os.fstat(handle.fileno())
        if identity(after) != identity(before) or identity(path.lstat()) != identity(before):
            raise ValueError("EVIDENCE_CONTROL_CHANGED:" + str(path))
        return identity(before), content
    except OSError as exc:
        raise ValueError("EVIDENCE_CONTROL_UNREADABLE:" + str(path)) from exc


def _lean_source_snapshot(root: Path) -> dict:
    """Enumerate retained inputs, excluding only the two root build directories."""
    result = {}

    def traversal_error(error):
        raise ValueError("LEAN_SOURCE_TRAVERSAL_FAILED:" + str(error)) from error

    for directory, directories, filenames in os.walk(root, onerror=traversal_error, followlinks=False):
        parent = Path(directory)
        for name in list(directories):
            path = parent / name
            info = path.lstat()
            if (not stat.S_ISDIR(info.st_mode)
                    or getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT):
                raise ValueError("LEAN_SOURCE_NOT_REGULAR:" + str(path))
            relative = path.relative_to(root).as_posix()
            if relative in {"b", ".lake"}:
                directories.remove(name)
            else:
                result[relative + "/"] = (info.st_dev, info.st_ino, info.st_mode)
        for name in filenames:
            path = parent / name
            identity, content = _regular_file_snapshot(path)
            result[path.relative_to(root).as_posix()] = (identity, hashlib.sha256(content).hexdigest())
    return result


def check_manifest(project_root: Path, manifest: Path) -> dict:
    root = _root(project_root)
    snapshot = _regular_file_snapshot(manifest)

    def checked_git(*args):
        try:
            return _git(root, *args)
        finally:
            if _regular_file_snapshot(manifest) != snapshot:
                raise ValueError("EVIDENCE_CONTROL_CHANGED:" + str(manifest))

    data = json.loads(snapshot[1].decode("utf-8"), object_pairs_hook=_unique_receipt_object)
    if not isinstance(data, dict):
        raise ValueError("SOURCE_MANIFEST_OBJECT_REQUIRED")
    revision = data.get("baseline_commit", data.get("source_commit", ""))
    if not isinstance(revision, str) or not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("PINNED_COMMIT_REQUIRED")
    checked_git("cat-file", "-e", revision + "^{commit}")
    rows = data.get("files")
    if not isinstance(rows, list) or not rows:
        raise ValueError("NONEMPTY_SOURCE_MANIFEST_REQUIRED")
    seen = set()
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("INVALID_SOURCE_ENTRY")
        source = row.get("source", "")
        if not isinstance(source, str) or not source:
            raise ValueError("INVALID_SOURCE_PATH")
        path = PurePosixPath(source)
        if not source or path.is_absolute() or ".." in path.parts or "\\" in source or ":" in source:
            raise ValueError("INVALID_SOURCE_PATH")
        if source in seen:
            raise ValueError("DUPLICATE_SOURCE_ENTRY:" + source)
        seen.add(source)
        reference = f"{revision}:{path.as_posix()}"
        blob = checked_git("rev-parse", "--verify", reference).decode("ascii").strip()
        if blob != row.get("source_blob"):
            raise ValueError(f"SOURCE_BLOB_MISMATCH:{source}")
        content = checked_git("cat-file", "blob", reference)
        if hashlib.sha256(content).hexdigest() != row.get("git_sha256"):
            raise ValueError(f"SOURCE_DIGEST_MISMATCH:{source}")
    return {"status": "VERIFIED", "source_commit": revision, "files_verified": len(rows), "authority_effect": "None"}


def verify_bets(project_root: Path, revision: str) -> dict:
    """Replay the established C750-T553 receipt against one recorded revision."""
    root = _root(project_root)
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("PINNED_COMMIT_REQUIRED")
    prefix = "omega_engine_projects/finite_qm/campaigns/c750"
    registry_raw = _git(root, "cat-file", "blob", f"{revision}:{prefix}/sealed_targets.json")
    registry = json.loads(registry_raw)
    if not isinstance(registry, dict):
        raise ValueError("INVALID_SEALED_TARGETS_OBJECT")
    entries = registry.get("sealed_targets")
    if not isinstance(entries, list):
        raise ValueError("INVALID_SEALED_TARGETS_LIST")
    expected = {
        "BET-CLAUDE-C750-B01": "a186b28c53bca455085fcb07cd01fad27245c2f24a0a9a752c656bf3080492ef",
        "BET-JC-C750-B01": "c6e481932897f8555cf92d862c99674a07b0bc6fc7c964f4f94d7fb34b2490c0",
    }
    digests = {}
    duplicate_bets = []
    fill_count = 0
    for entry in entries:
        if not isinstance(entry, dict) or "bet_id" not in entry or "sha256" not in entry:
            raise ValueError("INVALID_SEALED_TARGET_ENTRY")
        bid = entry["bet_id"]
        sha = entry["sha256"]
        if not isinstance(bid, str) or not bid or not isinstance(sha, str) or not sha:
            raise ValueError("INVALID_SEALED_TARGET_ENTRY")
        if sha == "FILL_BEFORE_LAUNCH":
            fill_count += 1
        if bid in digests:
            duplicate_bets.append(bid)
            if digests[bid] != sha:
                duplicate_bets.append(f"{bid}(CONTRADICTORY_HASH)")
        else:
            digests[bid] = sha

    matches = (not duplicate_bets) and all(digests.get(key) == value for key, value in expected.items())
    names = set(_git(root, "ls-tree", "-r", "--name-only", revision, "--", prefix).decode("utf8").splitlines())
    all_bet_keys = set(expected.keys()) | set(digests.keys())
    plaintexts = sorted(
        name for name in names
        if any(PurePosixPath(name).stem == key or PurePosixPath(name).name == f"{key}.txt" for key in all_bet_keys)
    )
    refusal = None
    if duplicate_bets:
        refusal = f"Refusal: Duplicate bet entries in registry: {sorted(set(duplicate_bets))}"
    elif fill_count:
        refusal = f"Refusal: {fill_count} registered bet entries contain FILL_BEFORE_LAUNCH"
    elif plaintexts:
        refusal = f"Refusal: Unrevealed bet plaintext(s) found in executor path: {plaintexts}"
    elif not matches:
        refusal = "Refusal: Block 01 digests in registry do not match expected frozen hashes"
    return {"target_id": "C750-T553", "evidence_class": "METATHEORY", "verified": not refusal,
            "b01_digests_matched": matches, "fill_before_launch_count": fill_count,
            "readable_plaintexts_found": plaintexts, "refusal_reason": refusal,
            "details": {"registry_citation": registry.get("citation"), "total_sealed_targets_count": len(entries),
                        "checked_paths_count": len(names), "duplicate_bets_found": sorted(set(duplicate_bets)),
                        "b01_targets": {key: {"expected": value, "actual": digests.get(key),
                                              "matched": digests.get(key) == value and (key not in duplicate_bets)}
                                        for key, value in expected.items()}}}


def replay_lean(project_root: Path) -> dict:
    root = _root(project_root)
    pin = json.loads(files("src.qm.data").joinpath("source_pin.json").read_text(encoding="utf8"))
    revision = pin["baseline_commit"]
    prefix = pin["source_root"] + "/lean4/"
    log = []
    with tempfile.TemporaryDirectory(prefix="finite-qm-lean-") as stage:
        lean = Path(stage)
        for row in pin["files"]:
            source = row["source"]
            if source.startswith(prefix):
                relative = source[len(prefix):]
            elif source in pin["lean_dependencies"]:
                relative = PurePosixPath(source).name
            else:
                continue
            content = _git(root,"cat-file","blob",f"{revision}:{source}")
            if hashlib.sha256(content).hexdigest() != row["git_sha256"]:
                raise ValueError(f"SOURCE_DIGEST_MISMATCH:{source}")
            destination = lean / relative
            destination.parent.mkdir(parents=True,exist_ok=True)
            destination.write_bytes(content)
        toolchain = (lean / "lean-toolchain").read_text(encoding="utf8").strip()
        commands = [["lake","build"]]
        modules = {path.stem: path for path in lean.glob("*.lean") if path.stem != "lakefile"}
        ordered, visiting, complete = [], set(), set()
        def visit(name):
            if name in complete:
                return
            if name in visiting:
                raise ValueError("LEAN_IMPORT_CYCLE:" + name)
            visiting.add(name)
            for dependency in re.findall(r"^import (\w+)", modules[name].read_text(encoding="utf8"), re.M):
                if dependency in modules:
                    visit(dependency)
            visiting.remove(name)
            complete.add(name)
            ordered.append(name)
        for name in sorted(modules):
            visit(name)
        for name in ordered:
            commands.append(["lake","env","lean","-o",f"b/lib/lean/{name}.olean",f"{name}.lean"])
        source_snapshot = _lean_source_snapshot(lean)
        for command in commands:
            try:
                result = subprocess.run(command,cwd=lean,capture_output=True,encoding="utf8",errors="replace",timeout=1800,check=False)
            except subprocess.TimeoutExpired as exc:
                raise RuntimeError("LEAN_REPLAY_TIMEOUT:" + " ".join(command)) from exc
            finally:
                if _lean_source_snapshot(lean) != source_snapshot:
                    raise ValueError("LEAN_SOURCE_CHANGED_DURING_REPLAY")
            log.append("$ " + " ".join(command) + "\n" + result.stdout + result.stderr)
            if result.returncode:
                raise RuntimeError(f"LEAN_BUILD_FAILED:{result.returncode}\n"+"\n".join(log))
    return {"status":"BUILD_PASSED","source_commit":revision,"toolchain":toolchain,"modules":ordered,"log":"\n".join(log),"authority_effect":"None"}
