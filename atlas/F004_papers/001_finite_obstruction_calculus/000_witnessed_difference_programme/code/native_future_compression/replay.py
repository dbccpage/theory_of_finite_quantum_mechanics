"""Comparison with a byte-checked, isolated original dependency closure."""
from __future__ import annotations

import hashlib
import importlib
import importlib.abc
import importlib.util
import json
import os
import stat
import subprocess
import sys
import tempfile
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path

import tomllib

from .model import ACTIONS, NATIVE_SCHEMA, PROFILE, State, digest, fields, require, same, transition

REVISION = "5d9488324ce976817987bd83a28d901371cfc073"


def parse_json_bytes(data):
    def pairs(items):
        out = {}
        for key, value in items:
            require(key not in out, "duplicate JSON key")
            out[key] = value
        return out
    def constant(value):
        raise ValueError(f"nonfinite JSON literal: {value}")
    def fractional(value):
        raise ValueError(f"noninteger JSON literal: {value}")
    return json.loads(data.decode("utf-8"), object_pairs_hook=pairs,
                      parse_constant=constant, parse_float=fractional)


def strict_json_with_snapshot(path):
    data, snapshot = read_artifact(path)
    return parse_json_bytes(data), snapshot


def strict_json(path):
    return strict_json_with_snapshot(path)[0]


def original_rows(manifest):
    rows = [r for r in strict_json(manifest)["files"] if r["repository"] == "H3V7N5QF"]
    require(len(rows) == 19 and len({r["path"] for r in rows}) == 19, "source closure count")
    require(all(r["revision"] == REVISION for r in rows), "source revision")
    return rows


def verify_closure(root, manifest):
    root = Path(root).absolute()
    rows = original_rows(manifest)
    for row in rows:
        path = (root / row["path"]).absolute()
        require(path.resolve().is_relative_to(root.resolve()), "source path escapes closure")
        regular_file(path)
        data = path.read_bytes()
        require(len(data) == row["bytes"] and hashlib.sha256(data).hexdigest() == row["sha256"],
                f"source bytes mismatch: {row['path']}")
        git_blob = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
        require(git_blob == row["git_blob"], f"source blob mismatch: {row['path']}")
    return rows


class ClosureLoader(importlib.abc.Loader):
    def __init__(self, path, row):
        self.path, self.row = path, row

    def create_module(self, spec):
        return None

    def exec_module(self, module):
        regular_file(self.path)
        data = self.path.read_bytes()
        require(len(data) == self.row["bytes"] and hashlib.sha256(data).hexdigest() == self.row["sha256"],
                "source changed before import")
        module.__file__ = str(self.path)
        # Compile the checked source bytes directly; an ambient .pyc file
        # cannot replace the source that was checked above.
        exec(compile(data, str(self.path), "exec"), module.__dict__)


class ClosureFinder(importlib.abc.MetaPathFinder):
    def __init__(self, root, rows):
        self.paths = {r["path"][5:-3].replace("/", "."): root/r["path"] for r in rows}
        self.rows = {r["path"][5:-3].replace("/", "."): r for r in rows}
        self.packages = {name.split(".")[0] for name in self.paths}

    def find_spec(self, fullname, path=None, target=None):
        if fullname.split(".")[0] not in self.packages:
            return None
        if fullname in self.packages:
            spec = importlib.machinery.ModuleSpec(fullname, loader=None, is_package=True)
            spec.submodule_search_locations = []
            return spec
        require(fullname in self.paths, f"import outside pinned closure: {fullname}")
        return importlib.util.spec_from_loader(fullname, ClosureLoader(self.paths[fullname], self.rows[fullname]))


@contextmanager
def original_owner(root, manifest):
    # Verify every byte before a source module can execute. No ambient module may
    # satisfy a closure import, and only named manifest files can be imported.
    rows = verify_closure(root, manifest)
    finder = ClosureFinder(Path(root).absolute(), rows)
    saved = {k: v for k, v in sys.modules.items() if k.split(".")[0] in finder.packages}
    for key in saved:
        del sys.modules[key]
    old_bytecode = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    sys.meta_path.insert(0, finder)
    try:
        yield importlib.import_module("twentyfifth.state")
    finally:
        sys.meta_path.remove(finder)
        for key in list(sys.modules):
            if key.split(".")[0] in finder.packages:
                del sys.modules[key]
        sys.modules.update(saved)
        sys.dont_write_bytecode = old_bytecode
        verify_closure(root, manifest)


def regular_file(path):
    path = Path(path).absolute()
    for item in (path, *path.parents):
        metadata = item.lstat()
        require(not getattr(metadata, "st_file_attributes", 0) & 0x400 and
                (stat.S_ISREG(metadata.st_mode) if item == path else stat.S_ISDIR(metadata.st_mode)),
                f"nonregular custody path: {item}")


def file_stamp(metadata):
    return (metadata.st_dev, metadata.st_ino, metadata.st_size,
            metadata.st_mtime_ns, metadata.st_ctime_ns)


@dataclass(frozen=True)
class ArtifactSnapshot:
    path: Path
    sha256: str
    stamp: tuple
    handle_stamp: tuple

    def verify(self):
        _, current = read_artifact(self.path)
        require(current == self, f"artifact changed during replay: {self.path}")


def read_artifact(path):
    """The bytes parsed and the digest returned come from this one checked read."""
    path = Path(path).absolute()
    regular_file(path)
    before = file_stamp(path.lstat())
    with path.open("rb") as stream:
        handle_before = file_stamp(os.fstat(stream.fileno()))
        # Python 3.12 on Windows exposes creation time through path lstat's
        # ctime and change time through handle fstat's ctime. Retain each
        # clock separately; identity, size and mtime agree across both APIs.
        require(handle_before[:4] == before[:4], "artifact replaced before read")
        data = stream.read()
        require(file_stamp(os.fstat(stream.fileno())) == handle_before, "artifact changed while reading")
    regular_file(path)
    require(file_stamp(path.lstat()) == before, "artifact replaced after read")
    return data, ArtifactSnapshot(path, hashlib.sha256(data).hexdigest(), before, handle_before)


def write_artifact(path, data):
    """Write declared checked bytes, then bind the written file and verify it."""
    path = Path(path).absolute()
    path.parent.mkdir(parents=True, exist_ok=True)
    for parent in path.parents:
        meta = parent.lstat()
        require(stat.S_ISDIR(meta.st_mode) and not getattr(meta, "st_file_attributes", 0) & 0x400,
                "nonregular output directory")
    exists = path.exists() or path.is_symlink()
    if exists:
        regular_file(path)
        before = file_stamp(path.lstat())
    with path.open("r+b" if exists else "xb") as stream:
        opened = os.fstat(stream.fileno())
        require(stat.S_ISREG(opened.st_mode), "nonregular output file")
        if exists:
            require(file_stamp(opened)[:4] == before[:4], "output replaced before write")
        identity = opened.st_dev, opened.st_ino
        stream.seek(0)
        stream.write(data)
        stream.truncate()
        stream.flush()
        os.fsync(stream.fileno())
    written, snapshot = read_artifact(path)
    require(snapshot.stamp[:2] == identity and written == data, "checked output changed during publication")
    return snapshot


def file_sha(path):
    return read_artifact(path)[1].sha256


def local_dependency_manifests(root, expected_sources):
    """Derive this adapter's non-test local closure from live manifests."""
    root = Path(root).absolute()
    workspace = root/"omega_engine/crates_rs/Cargo.toml"
    snapshots = {}
    def checked_manifest(path):
        data, snapshot = read_artifact(path)
        name = path.relative_to(root).as_posix()
        require(name in expected_sources and snapshot.sha256 == expected_sources[name],
                f"native local dependency manifest absent or changed: {name}")
        snapshots[path] = snapshot
        return tomllib.loads(data.decode("utf-8"))
    config = checked_manifest(workspace)
    require(not config.get("patch") and not config.get("replace"), "unsupported workspace dependency override")
    inherited = config.get("workspace", {}).get("dependencies", {})
    pending = [workspace.parent/"omega_wdp/Cargo.toml"]
    seen = set()
    while pending:
        manifest = Path(os.path.abspath(pending.pop()))
        require(manifest.resolve().is_relative_to(root.resolve()), "local dependency escapes source root")
        if manifest in seen:
            continue
        seen.add(manifest)
        value = checked_manifest(manifest)
        require(not value.get("patch") and not value.get("replace"), "unsupported local dependency override")
        # The adapter builds this crate as a dependency. Its dev-dependencies
        # are not compiled; normal/build dependencies and target tables are.
        for scope in (value, *value.get("target", {}).values()):
            for kind in ("dependencies", "build-dependencies"):
                for name, descriptor in scope.get(kind, {}).items():
                    if type(descriptor) is not dict:
                        continue
                    parent = manifest.parent
                    if descriptor.get("workspace"):
                        require(name in inherited, "missing inherited dependency")
                        descriptor = inherited[name]
                        parent = workspace.parent
                    if type(descriptor) is dict and "path" in descriptor:
                        pending.append(parent/descriptor["path"]/"Cargo.toml")
    return seen | {workspace}, snapshots


class NativeCustody:
    """Validate a supplied build receipt and reproduce its census bytes."""
    def __init__(self, binary, receipt, source_root, package):
        self.binary = Path(binary).absolute()
        self.receipt = Path(receipt).absolute()
        self.root = Path(source_root).absolute()
        self.package = Path(package).absolute()
        self.build, self.receipt_snapshot = strict_json_with_snapshot(receipt)
        self.artifacts = {}
        require(self.build.get("schema") == "wdp-causal-native-build-v1" and
                self.build.get("authority_effect") == "None", "native build schema or authority")
        sources = self.build.get("sources")
        require(type(sources) is dict and bool(sources), "native build sources")
        for name in ("genesis_source_execution.rs", "genesis_marked_result.rs",
                     "genesis_ongoing_adapter.rs", "native_future_compression.rs"):
            require(f"omega_engine/crates_rs/omega_wdp/src/{name}" in sources,
                    f"native owner absent from build receipt: {name}")
        self.receipt_sha = self.receipt_snapshot.sha256
        self.verify()

    def check_artifact(self, path, expected):
        path = Path(path).absolute()
        if path in self.artifacts:
            snapshot = self.artifacts[path]
            snapshot.verify()
        else:
            _, snapshot = read_artifact(path)
            self.artifacts[path] = snapshot
        require(snapshot.sha256 == expected, f"native artifact digest mismatch: {path}")

    def verify(self):
        self.receipt_snapshot.verify()
        self.check_artifact(self.binary, self.build["binary_sha256"])
        manifests, snapshots = local_dependency_manifests(self.root, self.build["sources"])
        for path, snapshot in snapshots.items():
            if path in self.artifacts:
                require(snapshot == self.artifacts[path], "native dependency manifest changed during replay")
            else:
                self.artifacts[path] = snapshot
        supplied_manifests = {self.root/name for name in self.build["sources"] if name.endswith("/Cargo.toml")}
        require(supplied_manifests == manifests, "native local dependency closure mismatch")
        inventory = set()
        def traversal_error(error):
            raise error
        for name, sha in self.build["sources"].items():
            path = (self.root/name).absolute()
            require(path.resolve().is_relative_to(self.root.resolve()), "native source escapes root")
            self.check_artifact(path, sha)
            if path.name == "Cargo.toml":
                inventory.add(path)
                for folder in ("src", "build"):
                    subtree = path.parent/folder
                    if subtree.exists() or subtree.is_symlink():
                        meta = subtree.lstat()
                        require(stat.S_ISDIR(meta.st_mode) and
                                not getattr(meta, "st_file_attributes", 0) & 0x400,
                                "nonregular native source subtree")
                        for directory, dirs, files in os.walk(subtree, onerror=traversal_error):
                            for item in [Path(directory), *(Path(directory)/d for d in dirs)]:
                                meta = item.lstat()
                                require(stat.S_ISDIR(meta.st_mode) and
                                        not getattr(meta, "st_file_attributes", 0) & 0x400,
                                        "nonregular native source directory")
                            inventory.update(Path(directory)/f for f in files)
                if (path.parent/"build.rs").exists() or (path.parent/"build.rs").is_symlink():
                    inventory.add(path.parent/"build.rs")
        inventory.update(self.root/"omega_engine/crates_rs"/name for name in ("Cargo.toml", "Cargo.lock"))
        same(sorted(p.relative_to(self.root).as_posix() for p in inventory),
             sorted(self.build["sources"]), "native source inventory changed")
        adapter = self.package / "code/causal_certificates/native/main.rs"
        self.check_artifact(adapter, self.build["adapter_sha256"])
        self.check_artifact(adapter.with_name("build_native.py"), self.build["adapter_builder_sha256"])

    def reproduce(self, native_snapshot):
        self.verify()
        native_snapshot.verify()
        # A new process binds the submitted census to the binary in the receipt.
        # The transient table is outside the repository and removed on close.
        with tempfile.TemporaryFile() as output:
            process = subprocess.run([str(self.binary)], input=b'{"query":"bounded_future"}',
                                     stdout=output, stderr=subprocess.PIPE, timeout=1200, check=False)
            require(process.returncode == 0, f"native census refused: {process.stderr.decode(errors='replace')}")
            output.seek(0)
            observed = hashlib.file_digest(output, "sha256").hexdigest()
        require(observed == native_snapshot.sha256, "submitted native census differs from bound executable output")
        native_snapshot.verify()
        self.verify()
        return {"receipt_sha256": self.receipt_sha, "binary_sha256": self.build["binary_sha256"],
                "sources_sha256": digest(self.build["sources"]), "census_sha256": observed}


def compare_original(model, root, manifest, progress=None):
    offers = 0
    enabled = 0
    with original_owner(root, manifest) as owner:
        descriptors = []
        for a in ACTIONS:
            if a["kind"] == "fill":
                descriptors.append(owner.Filling(a["x"], a["y"], a["z"]))
            else:
                descriptors.append(owner.Change(getattr(owner.Kind, a["kind"].upper()),
                                                a.get("relation", ""), a.get("x", -1),
                                                a.get("y", -1)))
        for i, state in enumerate(model.states):
            original = owner.FState(owner.DState(state.n, state.r, state.s), state.filled)
            require(owner.result_mark(original) == model.marks[i], f"original mark: {i}")
            require(owner.balance_record(original) == model.balances[i], f"original balance: {i}")
            legal = set(owner.changes(original))
            for j, (action, descriptor, edge) in enumerate(zip(ACTIONS, descriptors, model.edges[i])):
                offers += 1
                admitted = descriptor in legal
                require(admitted == (edge.status != "native_disabled"), f"original guard: {i}/{j}")
                if not admitted:
                    continue
                enabled += 1
                source_price = (0, 0) if isinstance(descriptor, owner.Filling) else descriptor.additions
                require(source_price == edge.price, f"original price: {i}/{j}")
                post = owner.perform(original, descriptor)
                _, independent_post = transition(state, action)
                require(State(post.n, post.state.r, post.state.s, post.filled) == independent_post,
                        f"original transition: {i}/{j}")
            if progress and i % 5000 == 0:
                progress(f"Original source: {i + 1}/{len(model.states)} states")
        owner.forget_marks()
    return {"states": len(model.states), "offers": offers, "enabled_transitions": enabled,
            "closure_files": 19, "revision": REVISION}


def compare_native(model, partitions, native):
    fields(native, ("schema", "profile", "actions", "states", "edges", "partitions"), "native census")
    same(native["schema"], NATIVE_SCHEMA, "native schema")
    same(native["profile"], PROFILE, "native bound")
    same(native["actions"], ACTIONS, "native literal action labels")
    require(type(native["states"]) is list and len(native["states"]) == len(model.states), "native state count")
    require(type(native["edges"]) is list and len(native["edges"]) == len(model.states), "native offer rows")
    for i in range(len(model.states)):
        same(native["states"][i], model.state_wire(i), f"native state or observation: {i}")
        same(native["edges"][i], [e.wire() for e in model.edges[i]], f"native offer: {i}")
    same(native["partitions"], partitions, "native partitions")
    return {"states": len(model.states), "offers": len(model.states)*len(ACTIONS)}
