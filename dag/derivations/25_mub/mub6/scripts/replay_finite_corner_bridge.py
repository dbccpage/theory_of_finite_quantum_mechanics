"""Replay the concrete quartet bridge in a prepared, pinned external checkout.

AuthorityEffect: None. Requires the external Lake dependencies and caches to
be prepared already. Writes only copied MUB sources, their oleans, and logs in
the explicitly selected external checkout and output directory.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import zipfile


EXTERNAL_COMMIT = "57b03025ecbe259e474281f49e201ea7cb474e34"
ARCHIVE_SHA256 = "90b202d4da34649d9a9f3b2c1f7c218b3febbf543e105c18e583e25243a31d5e"
TOOLCHAIN = "leanprover/lean4:v4.33.0-rc2"
MATHLIB = "51e6992efd06126df61a496bebf8f49482a4e129"
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
ENDPOINTS = {
    "rawHadamard_iff_external", "monomialEquivalent_iff_external",
    "exists_retained_completion_of_rawQuartet",
    "exists_quartet_iff_retained_completion", "no_quartet_iff_retained_nonextension",
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkout", type=Path, required=True)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    checkout, out = args.checkout.resolve(), args.out.resolve()
    root = Path(__file__).resolve().parents[3]
    source = root / "lean4/research_programs/mub6"
    archive_bytes = args.archive.read_bytes()
    require(sha256(archive_bytes) == ARCHIVE_SHA256, "External archive digest mismatch")
    archive_names: set[str] = set()
    with zipfile.ZipFile(args.archive) as archive:
        for info in archive.infolist():
            if info.is_dir():
                continue
            relative = Path(*Path(info.filename).parts[1:])
            target = (checkout / relative).resolve()
            require(target.is_relative_to(checkout), "Unsafe archive path")
            require(target.read_bytes() == archive.read(info), f"External source changed: {relative}")
            archive_names.add(relative.as_posix())
    require(len(archive_names) == 215, "Unexpected external archive file count")
    require((checkout / "lean-toolchain").read_text().strip() == TOOLCHAIN, "External Lean pin changed")
    manifest = json.loads((checkout / "lake-manifest.json").read_text())
    require(next(p["rev"] for p in manifest["packages"] if p["name"] == "mathlib") == MATHLIB,
            "External Mathlib pin changed")
    for package in manifest["packages"]:
        path = checkout / ".lake/packages" / package["name"]
        head = subprocess.check_output(["git", "-C", str(path), "rev-parse", "HEAD"], text=True).strip()
        status = subprocess.check_output(
            ["git", "-C", str(path), "status", "--porcelain=v1", "--untracked-files=all"], text=True).strip()
        require(head == package["rev"] and not status, f"Dependency mismatch: {package['name']}")

    order: list[str] = []
    active: set[str] = set()
    seen: set[str] = set()

    def visit(module: str) -> None:
        require(module not in active, f"Local import cycle: {module}")
        if module in seen:
            return
        active.add(module)
        text = (source / f"{module}.lean").read_text(encoding="utf-8")
        for imported in re.findall(r"^import (\w+)\s*$", text, re.MULTILINE):
            if (source / f"{imported}.lean").is_file():
                visit(imported)
        active.remove(module)
        seen.add(module)
        order.append(module)

    visit("MubIndexTransport")
    visit("MubQuartetTransportBridge")
    out.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, LEAN_NUM_THREADS="1")
    commands = []

    def run(arguments: list[str], name: str) -> str:
        command = ["lake", f"+{TOOLCHAIN}", *arguments]
        log = out / f"{name}.log"
        with log.open("wb") as stream:
            completed = subprocess.run(command, cwd=checkout, env=env,
                                       stdout=stream, stderr=subprocess.STDOUT, check=False)
        raw = log.read_bytes()
        commands.append(dict(command=command, exit_code=completed.returncode,
                             log=log.name, log_sha256=sha256(raw)))
        require(completed.returncode == 0, f"Replay failed: {name}; see {log}")
        print(f"PASS {name}", flush=True)
        return raw.decode("utf-8-sig")

    run(["build", "+Hadamard6.PaperTheorem:olean"], "public_build")
    copied = []
    for module in order + ["MubFiniteCornerReduction"]:
        original = (source / f"{module}.lean" if module in order else
                    source / "external_classification/MubFiniteCornerReduction.lean")
        relative = f"{module}.lean"
        require(relative not in archive_names, f"External source collision: {relative}")
        raw = original.read_bytes()
        target = checkout / relative
        require(not target.exists() or target.read_bytes() == raw,
                f"Refusing to overwrite a different existing source: {target}")
        target.write_bytes(raw)
        copied.append(dict(module=module, path=original.relative_to(root).as_posix(), sha256=sha256(raw)))
        output = run(["env", "lean", relative, "-o", f".lake/build/lib/lean/{module}.olean"], module)

    reports = {}
    for theorem, body in re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", output):
        reports[theorem] = sorted(x.strip() for x in body.split(",") if x.strip())
    require({name.rsplit(".", 1)[-1] for name in reports} == ENDPOINTS, "Missing or unexpected bridge reports")
    require(all(set(axioms) <= ALLOWED_AXIOMS for axioms in reports.values()), "Unaccepted bridge axiom")
    receipt = dict(schema_version=1, authority_effect="None", result="BRIDGE_REPLAY_PASS",
                   external_commit=EXTERNAL_COMMIT, archive_sha256=ARCHIVE_SHA256,
                   external_archive_files_checked=len(archive_names), toolchain=TOOLCHAIN,
                   mathlib=MATHLIB, copied_sources=copied, commands=commands,
                   endpoint_axioms=reports,
                   scope="Actual quartet existence iff a retained finite-corner completion admits two further raw bases. Nonextension remains open.")
    (out / "replay.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
