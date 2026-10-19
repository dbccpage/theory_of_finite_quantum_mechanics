"""Check and bind the mathematical/refusal model, without exporting OLean files.

The receipt is proof-model evidence, not automatic Rust refinement or a grade.
Uses the repository's already prepared Lean/Mathlib project; never fetches it.
"""

from datetime import datetime, timezone
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

from run_audit import ROOT, digest, execute, write_json


def main():
    project = ROOT/"lean4"
    proof = Path(__file__).resolve().parent/"proofs/RankCertificate.lean"
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")+"-rank-proof"
    output = ROOT/"evidence/quality/category_homology"/stamp
    output.mkdir(parents=True)
    shutil.copyfile(proof,output/proof.name)
    inputs = {str(proof):digest(proof)}
    mathlib = project/".lake/packages/mathlib"
    inputs[str(mathlib/"Mathlib/LinearAlgebra/Matrix/Rank.lean")] = digest(mathlib/"Mathlib/LinearAlgebra/Matrix/Rank.lean")
    write_json(output/"source_manifest.json",inputs)
    tool = subprocess.run(["elan","which","lean"],cwd=project,text=True,capture_output=True)
    if tool.returncode != 0: raise RuntimeError("Cannot resolve the prepared Lean compiler")
    binary = Path(tool.stdout.strip())
    bootstrap = json.loads(subprocess.check_output(["lake","env",sys.executable,"-c",
        "import json,os; print(json.dumps({key:os.environ.get(key,'') for key in ('LEAN_PATH','LEAN_SRC_PATH')}))"],cwd=project,text=True))
    # Exclude mutable output modules of the user's main theory project. The
    # standalone model uses only the prepared third-party dependency libraries.
    package_dir = (project/".lake/packages").resolve()
    environment = {}
    for key,search_path in bootstrap.items():
        libraries = dict.fromkeys(Path(entry).resolve() for entry in search_path.split(";")
            if entry and Path(entry).resolve().is_relative_to(package_dir))
        if not libraries: raise RuntimeError("No prepared proof dependency path: "+key)
        environment[key] = ";".join(str(path) for path in libraries)
    write_json(output/"environment.json",{"lean_binary":str(binary),"environment":environment,"excluded_main_project_outputs":True})
    common = [str(binary),"--root="+str(proof.parent)]
    dependencies = execute([*common,"--deps",str(proof)],proof.parent,output/"dependencies.log",timeout=60,environment_overlay=environment)
    sources = execute([*common,"--src-deps",str(proof)],proof.parent,output/"dependency-sources.log",timeout=60,environment_overlay=environment)
    paths = set()
    for log in ("dependencies.log","dependency-sources.log"):
        for line in (output/log).read_text(encoding="utf-8").splitlines():
            candidate = Path(line.strip())
            if not candidate.is_absolute(): candidate = project/candidate
            if candidate.is_file():
                paths.add(candidate.resolve())
                # Lean 4 stores auxiliary private/server data next to OLean.
                for suffix in (".private",".server"):
                    if Path(str(candidate)+suffix).is_file(): paths.add(Path(str(candidate)+suffix))
    dependency_inputs = {str(path):digest(path) for path in sorted(paths)}
    write_json(output/"dependency_manifest.json",dependency_inputs)
    head_before = subprocess.check_output(["git","-C",str(mathlib),"rev-parse","HEAD"],text=True).strip()
    status_before = subprocess.check_output(["git","-C",str(mathlib),"status","--porcelain","--untracked-files=no"],text=True).strip()
    checked = execute([*common,str(proof)],proof.parent,output/"check.log",timeout=300,environment_overlay=environment)
    text = (output/"check.log").read_text(encoding="utf-8")
    reports = {name:[item.strip() for item in axioms.split(",") if item.strip()]
               for name,axioms in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",text)}
    reports.update({name:[] for name in re.findall(r"'([^']+)' does not depend on any axioms",text)})
    expected = {"TFQM.RankCertificate."+name for name in (
        "valid_rank","runChecks_ok_iff","admit_success","admit_success_rank",
        "producer_failure","explicit_failure","failed_predicate","first_error_preserved",
        "row_major_index_lt","pivot_increment_fits","augmented_column_lt","identity_area_le")}
    unexpected = sorted({axiom for axioms in reports.values() for axiom in axioms} - {"propext","Classical.choice","Quot.sound"})
    head_after = subprocess.check_output(["git","-C",str(mathlib),"rev-parse","HEAD"],text=True).strip()
    status_after = subprocess.check_output(["git","-C",str(mathlib),"status","--porcelain","--untracked-files=no"],text=True).strip()
    receipt = {
        "AuthorityEffect":"None", "proof_sha256":digest(proof),
        "source_manifest_sha256":digest(output/"source_manifest.json"),
        "dependency_manifest_sha256":digest(output/"dependency_manifest.json"),
        "sources_unchanged":all(Path(path).is_file() and digest(Path(path)) == value for path,value in inputs.items()),
        "direct_dependencies_unchanged":all(Path(path).is_file() and digest(Path(path)) == value for path,value in dependency_inputs.items()),
        "dependency_scope":"Direct import source/OLean roots and Lean 4 private/server data. Transitive sources use the clean pinned Mathlib revision and retained targeted build; not a complete compiler file-read trace.",
        "lean_version":subprocess.check_output([str(binary),"--version"],cwd=proof.parent,text=True).strip(),
        "lean_binary":None if binary is None else {"path":str(binary),"sha256":digest(binary)},
        "mathlib_head":head_after,"mathlib_revision_stable":head_before == head_after,
        "mathlib_tracked_source_clean":not status_before and not status_after,
        "environment_sha256":digest(output/"environment.json"),
        "runner_sha256":digest(Path(__file__)),
        "runs":[checked,dependencies,sources],
        "check_ok":checked["exit_code"] == 0 and dependencies["exit_code"] == 0 and sources["exit_code"] == 0 and expected == set(reports) and not unexpected,
        "axiom_reports":reports,"unexpected_axioms":unexpected,
        "unfinished_axiom_detected":"sorryAx" in text,
        "scope":"Exact Q-matrix rank theorem and explicit-refusal model. Rust construction/representation refinement, MIR, allocator totality and crash freedom require separate evidence.",
    }
    write_json(output/"receipt.json",receipt)
    print(json.dumps({"check_ok":receipt["check_ok"],"sources_unchanged":receipt["sources_unchanged"],"unfinished_axiom_detected":receipt["unfinished_axiom_detected"]}))
    print("Receipt:",output)
    return 0 if receipt["check_ok"] and receipt["sources_unchanged"] and receipt["direct_dependencies_unchanged"] and receipt["mathlib_revision_stable"] and receipt["mathlib_tracked_source_clean"] and not receipt["unfinished_axiom_detected"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
