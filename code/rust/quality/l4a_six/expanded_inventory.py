"""Inventory the explicitly requested paths without assessing their quality."""
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path as _FilesystemPath
import sys as _contract_sys
_contract_sys.path.insert(0, str(_FilesystemPath(__file__).resolve().parents[4] / "scripts"))
from contract_scores import RecordPath as Path, copy_file as _copy_record_file
import shutil
from replay import ROOT, GROUPS, digest, write

PYTHON_GROUPS = (
    "bin category_theory combinatorics databases finite_probability fsp functional "
    "fusion_categories general_relativity higher_category_theory holonomy homology "
    "homotopy_type_theory lie_theory linear_algebra local_green_global_red_lggr "
    "majorana mub number_theory operad_theory qm sheaf_theory"
).split()
DIRECTORIES = [*("code/rust/src/" + name for name in (*GROUPS, "tests", "wdp")),
               *("code/python/src/" + name for name in PYTHON_GROUPS)]


def collect():
    sources, excluded = {}, Counter()
    for directory in DIRECTORIES:
        parent = ROOT / directory
        if not parent.is_dir():
            raise RuntimeError("Missing requested directory: " + directory)
        for path in sorted(parent.rglob("*")):
            if not path.is_file():
                continue
            relative = path.relative_to(parent)
            reason = next((part for part in relative.parts if part in ("__pycache__", "target", ".git", ".pytest_cache", ".mypy_cache")), None)
            if reason:
                excluded[reason] += 1
                continue
            if path.name.endswith((".scoring.yaml", ".contract.yaml", ".contract.score.yaml")):
                excluded["assessment sidecar (no recursive sidecars)"] += 1
                continue
            key = path.relative_to(ROOT).as_posix()
            sources[key] = {"sha256": digest(path), "bytes": path.stat().st_size,
                "directory": directory, "extension": path.suffix,
                "scoring_exists": Path(str(path) + ".scoring.yaml").is_file(),
                "contract_exists": Path(str(path) + ".contract.yaml").is_file()}
    return sources, excluded


def main():
    sources, excluded = collect()
    output = ROOT / "evidence/quality/l4a_six" / (datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-expanded-inventory")
    output.mkdir()
    _copy_record_file(__file__, output / "inventory.py")
    write(output / "subjects.json", sources)
    summary = {"AuthorityEffect": "None", "requested_directories": DIRECTORIES,
        "subject_count": len(sources), "counts": dict(Counter(item["directory"] for item in sources.values())),
        "extensions": dict(Counter(item["extension"] for item in sources.values())),
        "existing_scoring": sum(item["scoring_exists"] for item in sources.values()),
        "existing_contracts": sum(item["contract_exists"] for item in sources.values()),
        "excluded_generated_files": dict(excluded), "subjects_sha256": digest(output / "subjects.json"),
        "runner_sha256": digest(output / "inventory.py"),
        "scope": "All authored file types, including fixtures, data, manifests, and documentation. Inventory is not a capability or gate assessment."}
    write(output / "receipt.json", summary)
    print(output)
    print({k: summary[k] for k in ("subject_count", "extensions", "existing_scoring", "existing_contracts")})


if __name__ == "__main__":
    main()
