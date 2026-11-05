"""Pinned Git tree and live tracked-worktree ingestion, without executing paper code."""
from __future__ import annotations

import hashlib
import json
import os
import stat
import subprocess
from pathlib import Path

from .models import (
    ClaimCodeMap,
    CodeFolder,
    DocsFolder,
    EvidenceFolder,
    FileArtifact,
    Folder,
    ImagesFolder,
    JupyterNotebooksFolder,
    Lean4Folder,
    ManifestsFolder,
    Provenance,
    ResearchPaper,
    ScriptsFolder,
    TestsFolder,
    relative_path,
)
from .parser import parse_document, parse_ledger

MANUSCRIPT = "witnessed_difference_programme.md"
LEDGER = "witnessed_difference_programme_claim_ledger.md"
BASELINE = "manifests/paper_contract.baseline.json"
FOLDER_TYPES = {"code": CodeFolder, "docs": DocsFolder, "evidence": EvidenceFolder,
                "jupyter_notebooks": JupyterNotebooksFolder, "lean4": Lean4Folder,
                "scripts": ScriptsFolder, "images": ImagesFolder, "manifests": ManifestsFolder}


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def from_git_tree(manuscript: str, ledger: str, tree: dict, *, repository: str, claim_code_map: str | None = None) -> ResearchPaper:
    """The tree must be complete and pinned; missing/malformed entries fail closed."""
    if tree.get("truncated"):
        raise ValueError("refuse a truncated Git tree")
    entries = tree["entries"]
    paths = [e["path"] for e in entries]
    if len(paths) != len(set(paths)):
        raise ValueError("duplicate tree entry")
    if len(paths) != len({p.casefold() for p in paths}):
        raise ValueError("case-colliding inventory path")
    directories, files = [], []
    for entry in entries:
        path = relative_path(entry["path"])
        if path == BASELINE:
            continue  # Its digest would be self-referential; the trusted base supplies it.
        if entry["type"] == "tree" and entry["mode"] == "040000":
            directories.append(path)
        elif entry["type"] == "blob" and entry["mode"] in {"100644", "100755"}:
            files.append(FileArtifact(path=path, git_blob_sha=entry["sha"], bytes=entry["size"], mode=entry["mode"]))
        else:
            raise ValueError(f"unsupported Git entry (symlink/submodule): {path}")
    directories.sort()
    files.sort(key=lambda f: f.path)
    for file in files:
        if "/" in file.path and file.path.rpartition("/")[0] not in directories:
            raise ValueError(f"file parent missing from Git tree: {file.path}")
    for path in directories:
        if "/" in path and path.rpartition("/")[0] not in directories:
            raise ValueError(f"directory parent missing from Git tree: {path}")
    folders = {}
    extra = []
    for name in (d for d in directories if "/" not in d):
        kwargs = {"path": name, "directories": tuple(d for d in directories if d.startswith(name + "/")),
                  "files": tuple(f for f in files if f.path.startswith(name + "/"))}
        if name == "code":
            if "code/tests" not in directories:
                raise ValueError("required folder code/tests is missing")
            kwargs["tests"] = TestsFolder(directories=tuple(d for d in directories if d.startswith("code/tests/")),
                                           files=tuple(f for f in files if f.path.startswith("code/tests/")))
        cls = FOLDER_TYPES.get(name)
        if cls:
            folders[name] = cls(**kwargs)
        else:
            extra.append(Folder(**kwargs))
    missing = {"code", "docs", "lean4", "scripts"} - folders.keys()
    if missing:
        raise ValueError(f"required folders are missing: {sorted(missing)}")
    mapping = None
    if any(f.path == "manifests/claim_code_map.json" for f in files):
        if claim_code_map is None:
            raise ValueError("inventoried claim-code map must be supplied for validation")
        mapping = ClaimCodeMap.model_validate_json(json.dumps({"raw": claim_code_map, **json.loads(claim_code_map)}))
    return ResearchPaper(
        provenance=Provenance(repository=repository, commit=tree["commit"], paper_root=tree["root"],
                              inventory_source=tree.get("inventory_source", "github_git_tree")),
        manuscript=parse_document(manuscript, MANUSCRIPT), claim_ledger=parse_ledger(ledger, LEDGER), claim_code_map=mapping,
        root_files=tuple(f for f in files if "/" not in f.path), additional_folders=tuple(extra), **folders,
    )


def _git(root: Path, *args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(root), *args], stderr=subprocess.PIPE)


def regular_path(path: Path, *, directory: bool = False) -> Path:
    """Reject redirected ancestors before resolving or reading source bytes."""
    path = Path(os.path.abspath(path))
    for current in (*reversed(path.parents), path):
        info = current.lstat()
        is_dir = current != path or directory
        if (stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400
                or not (stat.S_ISDIR(info.st_mode) if is_dir else stat.S_ISREG(info.st_mode))):
            raise ValueError(f"missing/nonregular inventory path: {current}")
    return path


def worktree_snapshot(paper_root: Path, *, repository: str) -> ResearchPaper:
    """Include tracked files AND untracked nonignored additions; hash actual working bytes."""
    paper_root = regular_path(paper_root, directory=True)
    repo_root = Path(_git(paper_root, "rev-parse", "--show-toplevel").decode().strip())
    relative = paper_root.relative_to(repo_root).as_posix()
    if relative == ".":
        raise ValueError("paper must be a subdirectory of its Git repository")
    paths = _git(repo_root, "ls-files", "-z", "--cached", "--others", "--exclude-standard", "--", relative).split(b"\0")
    modes = {}
    for line in _git(repo_root, "ls-files", "-z", "--stage", "--", relative).split(b"\0"):
        if line:
            meta, path = line.split(b"\t", 1)
            mode, _, stage = meta.split()
            if stage != b"0":
                raise ValueError("unmerged inventory entry")
            modes[path.decode("utf-8")] = mode.decode()
    entries = []
    source_bytes = {}
    directories = set()
    for path_bytes in sorted(set(paths) - {b""}):
        path = path_bytes.decode("utf-8")
        local = repo_root / path
        rel = local.relative_to(paper_root).as_posix()
        if rel == BASELINE:
            continue
        if local.is_symlink() or not local.is_file():
            raise ValueError(f"missing/nonregular inventory file: {rel}")
        data = regular_path(local).read_bytes()
        source_bytes[rel] = data
        executable = bool(local.stat().st_mode & 0o111)
        mode = "100755" if executable else "100644"
        tracked_mode = modes.get(path)
        if tracked_mode not in {None, "100644", "100755"}:
            raise ValueError(f"unsupported tracked file mode: {rel}")
        entries.append({"path": rel, "type": "blob", "mode": mode, "sha": git_blob(data), "size": len(data)})
        parent = Path(rel).parent
        while parent.as_posix() != ".":
            directories.add(parent.as_posix())
            parent = parent.parent
    entries.extend({"path": p, "type": "tree", "mode": "040000"} for p in sorted(directories))
    tree = {"entries": entries, "root": relative, "commit": _git(repo_root, "rev-parse", "HEAD").decode().strip(),
            "inventory_source": "git_worktree"}
    mapping = source_bytes.get("manifests/claim_code_map.json")
    return from_git_tree(source_bytes[MANUSCRIPT].decode("utf-8"),
                         source_bytes[LEDGER].decode("utf-8"), tree, repository=repository,
                         claim_code_map=mapping.decode("utf-8") if mapping is not None else None)


def load_github_snapshot(source: Path, *, repository="dbccpage/the_symbol_game") -> ResearchPaper:
    return from_git_tree((source / MANUSCRIPT).read_bytes().decode("utf-8"),
                         (source / LEDGER).read_bytes().decode("utf-8"),
                         json.loads((source / "github_tree.json").read_text(encoding="utf-8")), repository=repository,
                         claim_code_map=(source / "claim_code_map.json").read_bytes().decode("utf-8"))
