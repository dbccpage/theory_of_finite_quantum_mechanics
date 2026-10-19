"""Replay chain/cochain nominal alias faults against current providers in independent module namespaces.

AuthorityEffect: None. Two single-fault copies share compilation, not state
or assessed functions. Each candidate's tests are dispatched independently.
Compiler output is deleted as soon as its test executable has been copied.
"""

from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import shutil
import subprocess

from run_audit import (ROOT, RUST, bind_dependencies, clear_debug_outputs,
                       dependency_inventory, digest, execute, execute_build,
                       inventory, mutations, snapshot, write_json)


def alias_cases(work):
    declarations, records = [], []
    for index, (name, kind, peer) in enumerate([("Chain","ChainKind","CochainKind"),("Cochain","CochainKind","ChainKind")]):
        subject = "homology/" + name.lower() + ".rs"
        source = (RUST / "src" / subject).read_text(encoding="utf-8")
        needle = "GradedVector<super::graded_vector::" + kind + ">"
        replacement = "GradedVector<super::graded_vector::" + peer + ">"
        if source.count(needle) != 1:
            raise ValueError("Unsupported alias definition: " + subject)
        oracle = f"""
#[cfg(test)] mod nominal_identity {{
  #[test] fn exact_provider() {{
    assert_eq!(std::any::TypeId::of::<super::{name}>(),
      std::any::TypeId::of::<crate::homology::graded_vector::GradedVector<crate::homology::graded_vector::{kind}>>());
  }}
}}
"""
        for mutant in (False,True):
            module = "alias_replay_" + str(index) + ("_fault" if mutant else "_control")
            path = work / (module + ".rs")
            candidate = source.replace(needle,replacement,1) if mutant else source
            path.write_text(candidate + oracle,encoding="utf-8")
            quoted = json.dumps(path.resolve().as_posix())
            declarations.append(f'#[cfg(test)] mod {module} {{ use crate::homology::graded_vector; #[path={quoted}] mod alias; }}')
            if mutant:
                records.append({"id":"AL-" + name,"path":subject,"outcome":"unrun","needle":needle,"replacement":replacement,
                    "module":module,"subject_sha256":digest(RUST / "src" / subject),
                    "candidate_path":path.relative_to(ROOT).as_posix(),"candidate_sha256":digest(path)})
    return declarations, records


def main():
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output = ROOT / "evidence/quality/category_homology" / stamp
    output.mkdir(parents=True)
    work = RUST / "target/ac" / stamp[2:15]
    inputs = inventory()
    write_json(output / "source_manifest.json",inputs)
    shutil.copyfile(__file__,output / "run_alias_challenges.py")
    snapshot(work,"homology")
    declarations, records = alias_cases(work)
    with (work / "src/homology/mod.rs").open("a",encoding="utf-8") as stream:
        stream.write("\n" + "\n".join(declarations))
    roots, dependencies = bind_dependencies(work,output)
    tools = {key:subprocess.check_output([key,"--version"],text=True).strip() for key in ("cargo","rustc")}
    write_json(output / "mutations.json",records)
    binary, build = work / "alias-tests.exe", work / "target"
    baseline, restored, builds = [], [], []
    try:
        command = ["cargo","test","--offline","--locked","--lib","--no-run","--message-format=json","--target-dir",str(build)]
        try:
            run = execute_build(command,work,output / "build.log")
            builds.append(run)
            if run["exit_code"] == 0:
                for line in (ROOT / run["log"]).read_text(encoding="utf-8").splitlines():
                    try:
                        item = json.loads(line)
                    except ValueError:
                        continue
                    if item.get("reason") == "compiler-artifact" and item.get("executable"):
                        shutil.copyfile(item["executable"],binary)
        finally:
            clear_debug_outputs(build,work)
        if run["exit_code"] == 0:
            baseline.append(execute([str(binary),"homology::","--skip","alias_replay_"],work,output / "homology-baseline.log"))
            baseline.append(execute([str(binary),"_control::"],work,output / "namespace-baseline.log"))
            if all(r["exit_code"] == 0 for r in baseline):
                for record in records:
                    run = execute([str(binary),"homology::" + record["module"] + "::"],work,output / (record["id"]+".log"),timeout=30)
                    log = (ROOT / run["log"]).read_text(encoding="utf-8")
                    outcome = "inconclusive" if run["timed_out"] else "survived" if run["exit_code"] == 0 else "killed" if "test result: FAILED" in log else "inconclusive"
                    record.update(outcome=outcome,run=run)
                    write_json(output / "mutations.json",records)
                    print(record["id"],outcome,flush=True)
            restored.append(execute([str(binary),"homology::","--skip","alias_replay_"],work,output / "homology-restored.log"))
            restored.append(execute([str(binary),"_control::"],work,output / "namespace-restored.log"))
    finally:
        binary.unlink(missing_ok=True)
        if build.exists():
            clear_debug_outputs(build,work)
            shutil.rmtree(build)
    write_json(output / "baseline.json",{"tools":tools,"runs":baseline})
    write_json(output / "restored.json",{"tools":tools,"runs":restored})
    write_json(output / "builds.json",builds)
    write_json(output / "mutations.json",records)
    outcomes = Counter(row["outcome"] for row in records)
    eligible = sum(outcomes[key] for key in ("killed","survived","inconclusive","unrun"))
    final = {"AuthorityEffect":"None","tools":tools,"source_scope":"homology",
        "baseline_ok":len(baseline) == 2 and all(r["exit_code"] == 0 for r in baseline),
        "restored_baseline_ok":len(restored) == 2 and all(r["exit_code"] == 0 for r in restored),
        "source_manifest_sha256":digest(output / "source_manifest.json"),"source_unchanged":inputs == inventory(),
        "dependencies_unchanged":dependencies == dependency_inventory(roots),"dependency_receipt_sha256":digest(output / "dependency_receipt.json"),
        "generated":len(records),"mutation_accounting":{key:outcomes[key] for key in ("killed","survived","demonstrably_equivalent","invalid","inconclusive","unrun")},
        "conservative_ratio":outcomes["killed"] / eligible if eligible else None,
        "all_files_L5A":False,"build_outputs_removed":not build.exists(),"runner_sha256":digest(Path(__file__)),
        "scope":"Chain/cochain nominal alias replay. Each candidate changes the sealed kind parameter once and executes its local tests plus an independent same-binary TypeId identity control. Provider algorithms remain independently graded. The unchanged original homology namespace supplies composition checks. No compiler/MIR refinement or whole-workspace pass."}
    write_json(output / "summary.json",final)
    print("Receipt:",output,flush=True)
    print(json.dumps(final,indent=2),flush=True)
    return 0 if all(final[key] for key in ("baseline_ok","restored_baseline_ok","source_unchanged","dependencies_unchanged")) else 1


if __name__ == "__main__":
    raise SystemExit(main())
