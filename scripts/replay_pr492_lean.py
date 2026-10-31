"""Regenerate and verify PR #492's related kernel receipts. AuthorityEffect: None."""
import argparse
import copy
import importlib.util
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("fqcd_replay", Path(__file__).with_name("replay_fqcd_lean.py"))
fqcd = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(fqcd)
FSP_SOURCE = "lean4/FoliatedFracton2Gauge.lean"
FSP_RECEIPT = "dag/research/campaign_tfq-1219_lean_replay.json"
FSP_LOG = "dag/research/campaign_tfq-1219_lean_replay.log"
RELATED = "dag/research/campaign_tfq-1050_lean_replay.json"


def verify() -> None:
    fqcd.verify_receipt()
    original = fqcd.RECEIPT
    try:
        fqcd.RECEIPT = RELATED
        fqcd.verify_receipt()
    finally:
        fqcd.RECEIPT = original
    d = json.loads((ROOT / FSP_RECEIPT).read_text())
    r, = d["lean_replay"]["results"]
    anchors = re.findall(r"^#print axioms (FoliatedFracton2Gauge\.\w+)$", (ROOT / FSP_SOURCE).read_text(), re.M)
    pins = (FSP_SOURCE, "lean4/lakefile.lean", "lean4/lake-manifest.json", "lean4/lean-toolchain")
    if set(d["source_pins"]) != set(pins) or r["anchors"] != anchors:
        raise ValueError("FSP input/anchor coverage differs")
    if any(fqcd.sha((ROOT / p).read_bytes()) != h for p, h in d["source_pins"].items()):
        raise ValueError("Stale FSP source pin")
    raw = (ROOT / FSP_LOG).read_bytes()
    if r["output_sha256"] != fqcd.sha(raw) or r["axioms"] != fqcd.parse_reports(raw.decode(), anchors):
        raise ValueError("FSP kernel output differs")
    if (r["module"] != "FoliatedFracton2Gauge" or r["source"] != FSP_SOURCE or r["output"] != FSP_LOG
            or r["sha256"] != d["source_pins"][FSP_SOURCE] or r["sha256_after_build"] != r["sha256"]
            or r["exit_code"] != 0 or not all(r[k] for k in ("admission_scan_passed", "axiom_audit_passed", "anchors_reported", "source_unchanged_during_build"))
            or not d["lean_replay"]["all_passed"]):
        raise ValueError("Invalid FSP replay identity or outcome")


def regenerate() -> None:
    fqcd.replay()
    base = json.loads((ROOT / fqcd.RECEIPT).read_text())
    related = copy.deepcopy(base)
    related["node_id"] = "FQCD-WILSON-DIRAC-GAMMA5-HERMITICITY"
    related["lean_replay"]["results"][0]["dag_node"] = related["node_id"]
    (ROOT / RELATED).write_text(json.dumps(related, indent=2) + "\n")
    pins = {p: fqcd.sha((ROOT / p).read_bytes()) for p in
            (FSP_SOURCE, "lean4/lakefile.lean", "lean4/lake-manifest.json", "lean4/lean-toolchain")}
    run = subprocess.run(["lake", "env", "lean", "FoliatedFracton2Gauge.lean"], cwd=ROOT / "lean4", capture_output=True, text=True, check=True)
    raw = run.stdout + run.stderr
    if any(fqcd.sha((ROOT / p).read_bytes()) != h for p, h in pins.items()):
        raise ValueError("FSP inputs changed during elaboration")
    source = (ROOT / FSP_SOURCE).read_text()
    if re.search(r"\b(sorry|admit|axiom)\b", re.sub(r"/\-.*?\-/|--[^\n]*", "", source, flags=re.S)):
        raise ValueError("FSP proof admission/custom axiom")
    anchors = re.findall(r"^#print axioms (FoliatedFracton2Gauge\.\w+)$", source, re.M)
    axioms = fqcd.parse_reports(raw, anchors)
    (ROOT / FSP_LOG).write_text(raw)
    result = dict(module="FoliatedFracton2Gauge", dag_node="FSP-HINGE-LINEON-SIGN-CLAIM", source=FSP_SOURCE,
                  sha256=pins[FSP_SOURCE], sha256_after_build=pins[FSP_SOURCE], source_unchanged_during_build=True,
                  exit_code=0, admission_scan_passed=True, axiom_audit_passed=True, anchors=anchors,
                  anchors_reported=True, axioms=axioms, output=FSP_LOG, output_sha256=fqcd.sha(raw.encode()))
    d = dict(schema_version="campaign_lean_replay.v1", node_id=result["dag_node"], source_pins=pins,
             lean_replay=dict(all_passed=True, results=[result]), toolchain=base["toolchain"],
             generated_at=base["generated_at"], lakefile_sha256=pins["lean4/lakefile.lean"])
    (ROOT / FSP_RECEIPT).write_text(json.dumps(d, indent=2) + "\n")
    verify()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify-receipts", action="store_true")
    args = parser.parse_args()
    verify() if args.verify_receipts else regenerate()
    print(json.dumps({"all_passed": True, "fqcd_anchors": len(json.loads((ROOT / fqcd.RECEIPT).read_text())["lean_replay"]["results"][0]["anchors"]),
                      "fsp_anchors": len(json.loads((ROOT / FSP_RECEIPT).read_text())["lean_replay"]["results"][0]["anchors"])}))
