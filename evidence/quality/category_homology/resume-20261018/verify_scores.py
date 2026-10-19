"""Recheck the 66 completed records; retain honest remaining-file status."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
BASE = ROOT / "code/rust/quality/category_homology"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


checks = []
mapping = json.loads((BASE / "assessments/metadata_assessment_map.json").read_text())
selections = [
    ("metadata", "20261018T233209Z", "20261018T233820Z-metrics", list(mapping),
     ["--assessment-map", "code/rust/quality/category_homology/assessments/metadata_assessment_map.json"]),
    ("rank", "20261018T233924Z", "20261018T233820Z-metrics", ["code/rust/src/homology/rank_certificate.rs"],
     ["--assessment", "code/rust/quality/category_homology/assessments/rank_certificate_current.json"]),
    ("degree-window", "20261018T234208Z", "20261018T233820Z-metrics", ["code/rust/src/category_theory/abelian/chain_complex_category.rs"],
     ["--assessment", "code/rust/quality/category_homology/assessments/chain_complex_category.json"]),
]
for name in ("finite_category", "finite_category_validation"):
    selections.append((name, "20261018T211047Z", "20261018T211112Z-metrics",
        ["code/rust/src/category_theory/" + name + ".rs"],
        ["--assessment", "code/rust/quality/category_homology/assessments/" + name + ".json"]))
for name, receipt, metrics, subjects, assessment in selections:
    args = [sys.executable, str(BASE / "write_scores.py"), "--check",
            "--receipt", "evidence/quality/category_homology/" + receipt,
            "--metrics", "evidence/quality/category_homology/" + metrics,
            *assessment, "--only", *subjects]
    run = subprocess.run(args, cwd=ROOT, capture_output=True, text=True)
    log = OUT / (name + "-score-check.log")
    log.write_text(run.stdout + run.stderr, encoding="utf-8")
    checks.append({"name":name,"command":args,"cwd":str(ROOT),"exit_code":run.returncode,
                   "log":log.relative_to(ROOT).as_posix(),"log_sha256":sha(log)})
    print(name, run.returncode, flush=True)
    if run.returncode:
        print(run.stdout + run.stderr, flush=True)

rows = []
for group in ("category_theory", "homology"):
    for subject in sorted((ROOT / "code/rust/src" / group).rglob("*.rs")):
        score = subject.with_suffix(".score.yaml")
        text = score.read_text(encoding="utf-8")
        def field(name):
            return re.search(r"^" + name + r": (.*)$", text, re.M)[1]
        recorded = re.search(r'^  sha256: "([a-f0-9]{64})"', text, re.M)[1]
        complete = field("is_complete") == "true"
        token = json.loads(field("score_token"))
        row = {"path":subject.relative_to(ROOT).as_posix(),"source_sha256":sha(subject),
            "record_source_matches":recorded == sha(subject),"level":json.loads(field("level")),
            "score_token":token,"is_complete":complete,
            "unassessed_gates":[gate for gate in ("G1","G2","G3","G4","G5")
                                if re.search(r"^  " + gate + r": null$",text,re.M)],
            "grade_ceiling":json.loads(field("grade_ceiling"))}
        row["next_action"] = "Retain current evidence and refuse future drift" if complete else \
            "Source-specific semantic, failure, consumer and challenge review; refactor structural ceilings below A"
        rows.append(row)
progress = {"AuthorityEffect":"None","goal_complete":False,"total_files":len(rows),
    "completed_A_files":sum(row["is_complete"] and row["score_token"].endswith("A") for row in rows),
    "incomplete_files":sum(not row["is_complete"] for row in rows),
    "all_source_records_match":all(row["record_source_matches"] for row in rows),"rows":rows}
(OUT / "progress.json").write_text(json.dumps(progress,indent=2) + "\n",encoding="utf-8")
(OUT / "score-checks.json").write_text(json.dumps({"checks":checks,"runner_sha256":sha(Path(__file__))},indent=2) + "\n",encoding="utf-8")
assert len(rows) == 192 and progress["completed_A_files"] == 66 and progress["incomplete_files"] == 126
assert progress["all_source_records_match"] and all(check["exit_code"] == 0 for check in checks)
print("Verified 66 A records and all 192 source hashes; 126 remain incomplete",flush=True)
