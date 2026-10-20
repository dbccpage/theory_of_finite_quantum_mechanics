"""Verify every completed adjacent record using its explicit pinned evidence.

This replays the score writer in check mode; it never infers or awards gates.
Incomplete records receive only a source-digest/status inventory check.
"""
from collections import defaultdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path as _FilesystemPath
import sys as _contract_sys
_contract_sys.path.insert(0, str(_FilesystemPath(__file__).resolve().parents[4] / "scripts"))
from contract_scores import RecordPath as Path, copy_file as _copy_record_file
import re
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[4]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output = ROOT / "evidence/quality/category_homology" / (stamp + "-score-verification")
    output.mkdir(parents=True)
    _copy_record_file(__file__,output / "verify_current_scores.py")
    writer = output / "write_scores.py"
    _copy_record_file(Path(__file__).with_name("write_scores.py"),writer)
    groups, rows = defaultdict(dict), []
    for folder in ("category_theory", "homology"):
        for source in sorted((ROOT / "code/rust/src" / folder).rglob("*.rs")):
            score = source.with_suffix(".score.yaml")
            text = score.read_text(encoding="utf-8")
            def field(name):
                return json.loads(re.search(r"^" + name + r": (.*)$",text,re.M)[1])
            token, complete = field("score_token"), field("is_complete")
            record = {"path":source.relative_to(ROOT).as_posix(),"source_sha256":sha(source),
                "score_sha256":sha(score),
                "record_source_matches":re.search(r'^  sha256: "([a-f0-9]{64})"',text,re.M)[1] == sha(source),
                "level":field("level"),"score_token":token,"is_complete":complete,
                "grade_ceiling":field("grade_ceiling"),
                "unassessed_gates":[gate for gate in ("G1","G2","G3","G4","G5")
                                    if re.search(r"^  " + gate + r": null$",text,re.M)]}
            rows.append(record)
            if complete:
                block = text.split("\nevidence:\n")[1].split("\nverification:")[0]
                references = [json.loads(line.strip()[2:]) for line in block.splitlines()
                              if line.strip().startswith("- {")]
                receipt = next(Path(item["path"]).parent.as_posix() for item in references
                               if item["path"].endswith("/baseline.json"))
                metrics = next(Path(item["path"]).parent.as_posix() for item in references
                               if item["path"].endswith("-metrics/receipt.json"))
                assessment = [item["path"] for item in references
                              if item.get("scope","").startswith("Explicit source-pinned gate assessment")]
                if len(assessment) != 1:
                    raise ValueError("A completed record needs one explicit review: " + record["path"])
                groups[(receipt,metrics)][record["path"]] = assessment[0]
    checks = []
    for index, ((receipt,metrics), mapping) in enumerate(groups.items()):
        map_path = output / f"assessments-{index}.json"
        map_path.write_text(json.dumps(mapping,indent=2) + "\n",encoding="utf-8")
        command = [sys.executable,str(writer),"--check",
                   "--receipt",receipt,"--metrics",metrics,"--assessment-map",str(map_path),"--only",*mapping]
        run = subprocess.run(command,cwd=ROOT,capture_output=True,text=True)
        log = output / f"check-{index}.log"
        log.write_text(run.stdout + run.stderr,encoding="utf-8")
        checks.append({"subjects":list(mapping),"command":command,"cwd":str(ROOT),
                       "assessment_map":map_path.relative_to(ROOT).as_posix(),"assessment_map_sha256":sha(map_path),
                       "exit_code":run.returncode,"log":log.relative_to(ROOT).as_posix(),"log_sha256":sha(log)})
        print("group",index,"subjects",len(mapping),"exit",run.returncode,flush=True)
        if run.returncode:
            print(run.stdout + run.stderr,flush=True)
    summary = {"AuthorityEffect":"None","goal_complete":False,"total_files":len(rows),
        "completed_A_files":sum(row["is_complete"] and row["score_token"].endswith("A") for row in rows),
        "incomplete_files":sum(not row["is_complete"] for row in rows),
        "all_source_records_match":all(row["record_source_matches"] for row in rows),
        "source_records_unchanged":all(sha(ROOT/row["path"]) == row["source_sha256"] and
            sha((ROOT/row["path"]).with_suffix(".score.yaml")) == row["score_sha256"] for row in rows),
        "completed_checks_passed":all(check["exit_code"] == 0 for check in checks),
        "rows":rows,"checks":checks,"runner_sha256":sha(Path(__file__)),
        "score_writer_sha256":sha(writer),
        "scope":"All completed records are revalidated; incomplete records remain unassessed, regardless of passing package tests."}
    (output / "summary.json").write_text(json.dumps(summary,indent=2) + "\n",encoding="utf-8")
    print("Receipt:",output,flush=True)
    return 0 if summary["all_source_records_match"] and summary["source_records_unchanged"] and summary["completed_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
