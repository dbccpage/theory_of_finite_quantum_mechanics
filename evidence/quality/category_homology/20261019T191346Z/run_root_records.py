"""Replay nested inventories inside the actual root crate.

Canonical category tests and one-fault namespaces share compilation, not state.
Private helpers are tested without widening production visibility or replacing
providers. AuthorityEffect: None. No whole-workspace or extracted-proof claim.
"""
from collections import Counter
import argparse
import hashlib
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import shutil
import subprocess

from root_records import challenge, variants
from run_audit import (ROOT, RUST, bind_dependencies, clear_debug_outputs,
                       dependency_inventory, digest, execute, execute_build,
                       inventory, snapshot, write_json)


POLICY = Path(__file__).with_name("root_record_boundaries.json")


def test_ok(run):
    return run["exit_code"] == 0 and not run["timed_out"] and bool(re.search(
        r"test result: ok\. [1-9][0-9]* passed;",(ROOT/run["log"]).read_text(encoding="utf-8")))


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--policy",type=Path,default=POLICY)
    args=parser.parse_args()
    policy=args.policy.resolve()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output = ROOT/"evidence/quality/category_homology"/stamp
    output.mkdir(parents=True)
    work = RUST/"target/rr"/stamp[2:15]
    inputs = inventory()
    write_json(output/"source_manifest.json",inputs)
    for name in (Path(__file__).name,"root_records.py","category_diagnostics.py","functor_certificates.py","natural_transformations.py","archival_inventory.py","joint_carrier.py","simulation.py","independence.py"):
        shutil.copyfile(Path(__file__).with_name(name),output/name)
    shutil.copyfile(policy,output/policy.name)
    snapshot(work,"category")
    package = work/"src/category_theory"
    manifest = package/"Cargo.toml"
    text = manifest.read_text(encoding="utf-8")
    if "[dev-dependencies]" in text or "serde_json" in text:
        raise ValueError("Review the native test-dependency adapter for this manifest")
    manifest.write_text(text+'\n[dev-dependencies]\nserde_json="1.0"\n',encoding="utf-8")
    generated = package/"q"
    generated.mkdir()
    subjects = json.loads(policy.read_text(encoding="utf-8"))["records"]
    declarations, controls, records = {}, [], []
    for subject in subjects:
        path = ROOT/subject["path"]
        if digest(path) != subject["sha256"]:
            raise ValueError("Policy source drift: " + subject["path"])
        source = path.read_text(encoding="utf-8")
        copies = [("control",source,"",""),*variants(subject,source)]
        for tag, candidate, needle, replacement in copies:
            index = len(controls)+len(records)
            module = "root_record_replay_"+str(index)
            file = generated/("n"+str(index)+".rs")
            fixture = challenge(subject)
            alpha = []
            for method in subject.get("inherent_methods", []):
                if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", method):
                    raise ValueError("Invalid inherent method identifier")
                renamed = method + "_rr" + str(index)
                declaration = r"\bfn\s+" + method + r"\b"
                call = r"\." + method + r"\b"
                if len(re.findall(declaration, candidate)) != 1:
                    raise ValueError("Inherent replay needs exactly one own declaration")
                before = candidate
                candidate = re.sub(declaration, "fn " + renamed, candidate)
                candidate, own_calls = re.subn(call, "." + renamed, candidate)
                fixture, fixture_calls = re.subn(call, "." + renamed, fixture)
                alpha.append({"method":method,"renamed":renamed,
                    "own_calls":own_calls,"fixture_calls":fixture_calls,
                    "before_sha256":hashlib.sha256(before.encode("utf-8")).hexdigest(),
                    "after_sha256":hashlib.sha256(candidate.encode("utf-8")).hexdigest(),
                    "scope":"Test-only inherent method alpha renaming prevents duplicate implementations on the SAME actual receiver; provider imports/types/fields and all other method dispatch remain unchanged."})
            file.write_text(candidate+fixture,encoding="utf-8")
            quoted = json.dumps(file.resolve().as_posix())
            uses = "\n".join("use super::"+name+";" for name in subject.get("parent_aliases",[]))
            declarations.setdefault(subject["family"],[]).append(
                f'#[cfg(test)]\n#[allow(dead_code, unused_imports, unused_variables)]\nmod {module} {{\n{uses}\n#[path={quoted}] mod subject;\n}}')
            record = {"id":"RR-"+str(index)+"-"+tag,"path":subject["path"][len("code/rust/src/"):],
                "module":module+"::","subject_sha256":subject["sha256"],
                "candidate_path":file.relative_to(ROOT).as_posix(),"candidate_sha256":digest(file)}
            if alpha:
                record["method_alpha_renaming"] = alpha
            if tag == "control":
                controls.append(record)
            else:
                records.append({**record,"outcome":"unrun","needle":needle,"replacement":replacement})
    for family, blocks in declarations.items():
        with (package/"lib.rs").open("a",encoding="utf-8") as stream:
            stream.write("\n"+"\n".join(blocks))
    roots, dependencies = bind_dependencies(work,output)
    tools = {name:subprocess.check_output([name,"--version"],text=True).strip() for name in ("cargo","rustc")}
    write_json(output/"controls.json",controls)
    write_json(output/"mutations.json",records)
    baseline, restored, builds = [], [], []
    build, binary = work/"target", work/"root-record-tests.exe"
    try:
        command = ["cargo","test","--offline","--locked","--lib","--no-run","--message-format=json","--jobs","1",
                   "--target-dir",str(build),"-p","tfqm_category_theory"]
        try:
            run = execute_build(command,work,output/"build.log")
            builds.append(run)
            if run["exit_code"] == 0:
                for line in (ROOT/run["log"]).read_text(encoding="utf-8").splitlines():
                    try:
                        item = json.loads(line)
                    except ValueError:
                        continue
                    if item.get("reason") == "compiler-artifact" and item.get("executable"):
                        shutil.copyfile(item["executable"],binary)
        finally:
            clear_debug_outputs(build,work)
        if run["exit_code"] == 0:
            baseline.append(execute([str(binary),"--skip","root_record_replay_"],work,output/"category-baseline.log"))
            for index, control in enumerate(controls):
                baseline.append(execute([str(binary),control["module"]],work,output/f"control-{index}.log"))
            if all(test_ok(item) for item in baseline):
                for index, record in enumerate(records):
                    result = execute([str(binary),record["module"]],work,output/f"fault-{index}.log",timeout=30)
                    log = (ROOT/result["log"]).read_text(encoding="utf-8")
                    record["outcome"] = "inconclusive" if result["timed_out"] else "survived" if test_ok(result) else "killed" if result["exit_code"] != 0 and "test result: FAILED" in log else "inconclusive"
                    record["run"] = result
                    write_json(output/"mutations.json",records)
            for index, control in enumerate(controls):
                restored.append(execute([str(binary),control["module"]],work,output/f"restored-{index}.log"))
            restored.append(execute([str(binary),"--skip","root_record_replay_"],work,output/"category-restored.log"))
    finally:
        binary.unlink(missing_ok=True)
        if build.exists():
            clear_debug_outputs(build,work)
            shutil.rmtree(build)
    for name, data in (("baseline.json",{"tools":tools,"runs":baseline}),
                       ("restored.json",{"tools":tools,"runs":restored}),
                       ("builds.json",builds),("mutations.json",records)):
        write_json(output/name,data)
    counts = Counter(record["outcome"] for record in records)
    eligible = sum(counts[key] for key in ("killed","survived","inconclusive","unrun"))
    summary = {"AuthorityEffect":"None","source_scope":"category","tools":tools,
        "baseline_ok":len(baseline)==len(controls)+1 and all(test_ok(item) for item in baseline),
        "restored_baseline_ok":len(restored)==len(controls)+1 and all(test_ok(item) for item in restored),
        "source_unchanged":inputs==inventory(),"source_manifest_sha256":digest(output/"source_manifest.json"),
        "dependencies_unchanged":dependencies==dependency_inventory(roots),"dependency_receipt_sha256":digest(output/"dependency_receipt.json"),
        "generated":len(records),"mutation_accounting":{key:counts[key] for key in ("killed","survived","demonstrably_equivalent","invalid","inconclusive","unrun")},
        "conservative_ratio":counts["killed"]/eligible if eligible else None,"all_files_L5A":False,
        "compiled_subjects":[record["path"] for record in subjects],"compiled_scope":"Actual category crate and one-fault copies inside their real parent scopes; no visibility widening or provider replacement",
        "build_outputs_removed":not build.exists(),"runner_sha256":digest(output/Path(__file__).name),"policy_sha256":digest(output/policy.name),
        "runner_source_unchanged":digest(Path(__file__))==digest(output/Path(__file__).name),
        "policy_source_unchanged":digest(policy)==digest(output/policy.name),
        "scope":"Canonical category tests plus independently dispatched controls/faults. All copied candidate files reside inside the dependency-bound package. No whole-workspace, independent compiler or Rust/MIR proof."}
    write_json(output/"summary.json",summary)
    print("Receipt:",output,flush=True)
    print(json.dumps(summary,indent=2),flush=True)
    return 0 if all(summary[key] for key in ("baseline_ok","restored_baseline_ok","source_unchanged","dependencies_unchanged")) else 1


if __name__ == "__main__":
    raise SystemExit(main())
