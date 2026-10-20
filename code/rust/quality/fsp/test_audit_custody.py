"""Adversarial checks for FSP evidence admission; no production sources are mutated."""
import importlib.util
import json
from pathlib import Path
import shutil
import pytest

HERE = Path(__file__).parent
spec = importlib.util.spec_from_file_location("fsp_audit", HERE / "run_fsp_scoring_audit.py")
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)
RECEIPT = next(p.parent for p in sorted((audit.ROOT / "evidence/quality/fsp").glob("*/summary.json"), reverse=True)
               if json.loads((p.parent / "source_manifest.json").read_text()) == audit.source_inventory())

def candidate(tmp_path):
    for name in ["summary.json", "source_manifest.json", "mutations.json", "metrics.json", "baseline.json", "restored.json", "metric_receipt.json"]:
        shutil.copyfile(RECEIPT / name, tmp_path / name)
    return tmp_path

def test_stale_sources_refused(tmp_path):
    dest = candidate(tmp_path)
    (dest / "source_manifest.json").write_text("{}")
    with pytest.raises(ValueError, match="source manifest"):
        audit.write_sidecars(dest, True)

def test_corrupt_bound_summary_refused(tmp_path):
    dest = candidate(tmp_path)
    (dest / "baseline.json").write_text("{}")
    with pytest.raises(ValueError, match="custody"):
        audit.write_sidecars(dest, True)

def test_failed_baseline_refused_even_with_rehashed_json(tmp_path):
    dest = candidate(tmp_path)
    baseline = json.loads((dest / "baseline.json").read_text())
    baseline["runs"][0]["exit_code"] = 1
    (dest / "baseline.json").write_text(json.dumps(baseline))
    summary = json.loads((dest / "summary.json").read_text())
    summary["baseline_sha256"] = audit.sha256_file(dest / "baseline.json")
    (dest / "summary.json").write_text(json.dumps(summary))
    with pytest.raises(ValueError, match="baseline"):
        audit.write_sidecars(dest, True)
