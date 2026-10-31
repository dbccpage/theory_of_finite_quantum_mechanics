"""Build FQCD and retain kernel axiom reports for every requested declaration.

AuthorityEffect: None. A successful replay says nothing beyond the Lean statements.
Use --verify-receipt to check source, toolchain, log and exact anchor coverage offline.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "lean4/FQCD/StrongCouplingAreaLaw.lean"
RECEIPT = "dag/research/campaign_tfq-1052_lean_replay.json"
LOG = "dag/research/campaign_tfq-1052_lean_replay.log"
REPORT = re.compile(r"'([^']+)' (?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)")
STANDARD_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
PIN_PATHS = (SOURCE, "lean4/lakefile.lean", "lean4/lake-manifest.json", "lean4/lean-toolchain")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def expected_anchors(source: str) -> list[str]:
    """This module uses one namespace; reject changes to that assumption."""
    if re.findall(r"^namespace (\S+)", source, re.M) != ["FQCD"]:
        raise ValueError("Expected the single FQCD namespace")
    names = re.findall(r"^#print axioms (.+)$", source, re.M)
    if (not names or len(names) != len(set(names))
            or any(not re.fullmatch(r"\w+", name) for name in names)):
        raise ValueError("Missing or duplicate source audit requests")
    return ["FQCD." + name for name in names]


def parse_reports(output: str, anchors: list[str]) -> dict[str, list[str]]:
    """Require exact fully qualified coverage; never infer success from exit code alone."""
    reports = REPORT.findall(output)
    names = [name for name, _ in reports]
    if not anchors or len(set(anchors)) != len(anchors):
        raise ValueError("Empty or duplicate anchors")
    if len(names) != len(anchors) or set(names) != set(anchors):
        raise ValueError("Kernel reports do not match the requested fully qualified anchors")
    axioms = {name: [a.strip() for a in values.split(",") if a.strip()] for name, values in reports}
    if any(not set(values) <= STANDARD_AXIOMS for values in axioms.values()):
        raise ValueError("Unexpected axiom in kernel report")
    return axioms


def verify_receipt() -> None:
    receipt = json.loads((ROOT / RECEIPT).read_text(encoding="utf-8"))
    result, = receipt["lean_replay"]["results"]
    if (set(receipt["source_pins"]) != set(PIN_PATHS) or result["source"] != SOURCE
            or result["module"] != "FQCD.StrongCouplingAreaLaw" or result["output"] != LOG):
        raise ValueError("Replay identity or required input pins differ")
    anchors = expected_anchors((ROOT / SOURCE).read_text(encoding="utf-8"))
    if result["anchors"] != anchors:
        raise ValueError("Receipt anchors differ from the source audit requests")
    log = (ROOT / LOG).read_bytes()
    if result["output_sha256"] != sha(log):
        raise ValueError("Replay log hash mismatch")
    if result["axioms"] != parse_reports(log.decode("utf-8"), anchors):
        raise ValueError("Receipt axioms differ from actual Lean output")
    for path, digest in receipt["source_pins"].items():
        if sha((ROOT / path).read_bytes()) != digest:
            raise ValueError("Stale replay pin: " + path)
    if result["sha256"] != sha((ROOT / SOURCE).read_bytes()):
        raise ValueError("Stale source hash")
    if not (receipt["lean_replay"]["all_passed"] and result["exit_code"] == 0
            and result["admission_scan_passed"] and result["axiom_audit_passed"]
            and result["anchors_reported"] and result["source_unchanged_during_build"]
            and result["sha256_after_build"] == result["sha256"]):
        raise ValueError("Receipt does not record a successful replay")


def replay() -> None:
    source = (ROOT / SOURCE).read_bytes()
    anchors = expected_anchors(source.decode("utf-8"))
    pins = {p: sha((ROOT / p).read_bytes()) for p in PIN_PATHS}
    lean_root = ROOT / "lean4"
    version = subprocess.run(["lake", "env", "lean", "--version"], cwd=lean_root,
                             capture_output=True, text=True, check=True).stdout.strip()
    expected = (ROOT / "lean4/lean-toolchain").read_text().strip().split(":v")[-1]
    if not re.search(r"\bversion " + re.escape(expected) + r"(?:\D|$)", version):
        raise ValueError("Lean version does not match the pinned toolchain")
    subprocess.run(["lake", "build", "FQCD"], cwd=lean_root, check=True)
    with tempfile.TemporaryDirectory(prefix="fqcd_audit_", dir=lean_root) as directory:
        audit = Path(directory) / "Audit.lean"
        audit.write_text("import FQCD.StrongCouplingAreaLaw\n" +
                         "\n".join("#print axioms " + a for a in anchors) + "\n", encoding="utf-8")
        run = subprocess.run(["lake", "env", "lean", str(audit)], cwd=lean_root,
                             capture_output=True, text=True, check=True)
    output = run.stdout + run.stderr
    axioms = parse_reports(output, anchors)
    if any(sha((ROOT / path).read_bytes()) != digest for path, digest in pins.items()):
        raise ValueError("Pinned inputs changed during build")
    # A fresh elaboration and the kernel axiom allowlist reject proof admissions.
    if re.search(r"\b(sorry|admit|axiom)\b", re.sub(r"/\-.*?\-/|--[^\n]*", "", source.decode(), flags=re.S)):
        raise ValueError("Proof admission or custom axiom in source")
    (ROOT / LOG).write_text(output, encoding="utf-8")
    result = dict(module="FQCD.StrongCouplingAreaLaw", dag_node="FQCD-STRONG-COUPLING-AREA-LAW",
                  source=SOURCE, sha256=pins[SOURCE], sha256_after_build=pins[SOURCE],
                  source_unchanged_during_build=True, exit_code=run.returncode,
                  admission_scan_passed=True, axiom_audit_passed=True, anchors=anchors,
                  anchors_reported=True, axioms=axioms, output=LOG, output_sha256=sha(output.encode()))
    receipt = dict(schema_version="campaign_lean_replay.v1", node_id="FQCD-STRONG-COUPLING-AREA-LAW",
                   lean_replay=dict(all_passed=True, results=[result]), toolchain=version,
                   generated_at=datetime.now(timezone.utc).isoformat(),
                   mathlib_revision=next(p["rev"] for p in json.loads(
                       (lean_root / "lake-manifest.json").read_text())["packages"] if p["name"] == "mathlib"),
                   source_pins=pins, lakefile_sha256=pins["lean4/lakefile.lean"],
                   command="python -I -X utf8 scripts/replay_fqcd_lean.py")
    (ROOT / RECEIPT).write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    verify_receipt()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify-receipt", action="store_true")
    args = parser.parse_args()
    verify_receipt() if args.verify_receipt else replay()
    print(json.dumps({"all_passed": True, "anchors_checked": len(expected_anchors(
        (ROOT / SOURCE).read_text(encoding="utf-8")))}))
