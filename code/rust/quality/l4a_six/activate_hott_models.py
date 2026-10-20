"""Install already challenged finite models with exact-byte conflict checks."""
from datetime import datetime, timezone
import json
from pathlib import Path as _FilesystemPath
import sys as _contract_sys
_contract_sys.path.insert(0, str(_FilesystemPath(__file__).resolve().parents[4] / "scripts"))
from contract_scores import RecordPath as Path, copy_file as _copy_record_file
import shutil
from replay import ROOT, digest, write


def main():
    items = [
        ("20261020-pi-candidate", "pi_type", "20261020T152451Z-pi-trial"),
        ("20261020-unit-cost-candidate", "unit_type", "20261020T160638Z-unit-trial"),
    ]
    base = ROOT / "evidence/quality/l4a_six"
    prepared = []
    for directory, module, trial in items:
        candidate = base / directory
        manifest = json.loads((candidate / "candidate.json").read_text(encoding="utf8"))
        source = ROOT / manifest["source"]
        replacement = candidate / (module + ".rs")
        receipt = json.loads((base / trial / "receipt.json").read_text(encoding="utf8"))
        if digest(source) != manifest["origin_sha256"]:
            raise RuntimeError(f"Concurrent change: {source}")
        if digest(replacement) != manifest["candidate_sha256"] or receipt["candidate_sha256"] != digest(replacement):
            raise RuntimeError("Candidate custody mismatch")
        if receipt["accounting"]["conservative_ratio"] != 1 or not all(
            receipt[key] for key in ("live_sources_unchanged", "candidate_unchanged", "dependencies_unchanged")
        ) or not all(run["exit_code"] == 0 and not run["timed_out"] for run in receipt["baselines"] + receipt["restored_baselines"]):
            raise RuntimeError("Focused trial incomplete")
        prepared.append((source, replacement, manifest, trial))
    output = base / (datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-hott-model-activation")
    output.mkdir()
    _copy_record_file(__file__, output / "activation.py")
    changes = []
    for source, replacement, manifest, trial in prepared:
        for path in (source, Path(str(source) + ".scoring.yaml"), Path(str(source) + ".contract.yaml")):
            if path.exists():
                target = output / "before" / path.relative_to(ROOT)
                target.parent.mkdir(parents=True, exist_ok=True)
                _copy_record_file(path, target)
        # Repeat the comparison immediately before each write; never replace an
        # observed concurrent edit with the historical candidate's origin.
        if digest(source) != manifest["origin_sha256"]:
            raise RuntimeError(f"Concurrent change before install: {source}")
        source.write_bytes(replacement.read_bytes())
        changes.append({"source": source.relative_to(ROOT).as_posix(), "before_sha256": manifest["origin_sha256"],
                        "after_sha256": digest(source), "focused_trial": trial})
        write(output / "activation.json", {"AuthorityEffect": "None", "changes": changes,
            "status": "Installed; fresh combined-package execution and sidecar refresh required."})
    print(output)


if __name__ == "__main__":
    main()
