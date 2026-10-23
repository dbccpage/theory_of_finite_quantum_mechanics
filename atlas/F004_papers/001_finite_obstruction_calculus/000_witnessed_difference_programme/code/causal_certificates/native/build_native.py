"""Build an explicit omega_wdp dependency; retain file and executable custody.

No checkout or executable is discovered implicitly. The generated build tree is
outside the paper; the caller chooses it. This adapter owns no transition math.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import subprocess
from pathlib import Path


def sha(path: Path) -> str:
    for parent in path.parents:
        metadata = parent.lstat()
        if not stat.S_ISDIR(metadata.st_mode) or getattr(metadata, "st_file_attributes", 0) & 0x400:
            raise ValueError(f"non-regular source directory: {parent}")
    metadata = path.lstat()
    if not stat.S_ISREG(metadata.st_mode) or getattr(metadata, "st_file_attributes", 0) & 0x400:
        raise ValueError(f"non-regular source file: {path}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_snapshot(root: Path, packages: list[dict]) -> dict[str, str]:
    """Bind the whole local dependency inventory before and after compilation."""
    files = set()

    def traversal_error(error: OSError) -> None:
        raise error

    for package in packages:
        manifest = Path(package["manifest_path"]).absolute()
        if package.get("source") is not None or not manifest.is_relative_to(root):
            continue
        files.add(manifest)
        for name in ("src", "build"):
            subtree = manifest.parent / name
            if not subtree.exists() and not subtree.is_symlink():
                continue
            for directory, subdirectories, filenames in os.walk(subtree, onerror=traversal_error):
                for entry in [Path(directory), *(Path(directory) / item for item in subdirectories)]:
                    metadata = entry.lstat()
                    if not stat.S_ISDIR(metadata.st_mode) or getattr(metadata, "st_file_attributes", 0) & 0x400:
                        raise ValueError(f"non-regular source directory: {entry}")
                files.update(Path(directory) / item for item in filenames)
        build_script = manifest.parent / "build.rs"
        if build_script.exists() or build_script.is_symlink():
            files.add(build_script)
    files.update(root / "omega_engine/crates_rs" / name for name in ("Cargo.toml", "Cargo.lock"))
    return {path.relative_to(root).as_posix(): sha(path) for path in sorted(files)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--build-dir", type=Path, required=True)
    args = parser.parse_args()
    root, build = args.source_root.resolve(), args.build_dir.resolve()
    owner = root / "omega_engine/crates_rs/omega_wdp"
    source = Path(__file__).with_name("main.rs").absolute()
    build.mkdir(parents=True, exist_ok=True)
    manifest = build / "Cargo.toml"
    manifest.write_text(
        '[package]\nname="wdp_causal_replay"\nversion="0.1.0"\nedition="2021"\n'
        '[workspace]\n[dependencies]\n'
        f'omega_wdp={{path={json.dumps(owner.as_posix())}}}\n'
        'num-bigint="0.4"\nserde={version="1",features=["derive"]}\nserde_json="1"\n'
        f'[[bin]]\nname="wdp_causal_replay"\npath={json.dumps(source.as_posix())}\n',
        encoding="utf-8", newline="\n",
    )
    # Start from the explicit owner's locked registry versions; Cargo only adds
    # this adapter package and prunes unrelated workspace packages.
    (build / "Cargo.lock").write_bytes((root / "omega_engine/crates_rs/Cargo.lock").read_bytes())
    command = ["cargo", "build", "--offline", "--manifest-path", str(manifest), "-j", "1"]
    metadata = subprocess.run(
        ["cargo", "metadata", "--offline", "--format-version", "1", "--manifest-path", str(manifest)],
        check=True, capture_output=True, text=True,
    )
    metadata_value = json.loads(metadata.stdout)
    packages = metadata_value["packages"]
    snapshot = source_snapshot(root, packages)
    adapter_hash = sha(source)
    builder_hash = sha(Path(__file__).absolute())
    manifest_hash = sha(manifest)
    lock_hash = sha(build / "Cargo.lock")
    subprocess.run(command, check=True)
    if (snapshot != source_snapshot(root, packages) or adapter_hash != sha(source)
            or builder_hash != sha(Path(__file__).absolute())
            or manifest_hash != sha(manifest) or lock_hash != sha(build / "Cargo.lock")):
        raise ValueError("dependency or adapter source changed during build")
    executable = Path(metadata_value["target_directory"]) / "debug/wdp_causal_replay.exe"
    if not executable.exists():
        executable = executable.with_suffix("")
    version = subprocess.run(["rustc", "--version"], check=True, capture_output=True, text=True)
    receipt = {
        "schema": "wdp-causal-native-build-v1", "authority_effect": "None",
        "compiler": version.stdout.strip(), "command": command,
        "adapter_sha256": adapter_hash, "sources": snapshot,
        "adapter_builder_sha256": builder_hash,
        "binary_sha256": sha(executable), "cargo_lock_sha256": sha(build / "Cargo.lock"),
        "packages": [{"name": p["name"], "version": p["version"], "source": p["source"]}
                     for p in packages],
    }
    (build / "native_build_receipt.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n",
    )
    print(executable)


if __name__ == "__main__":
    main()
