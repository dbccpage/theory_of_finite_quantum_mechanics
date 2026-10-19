"""Replay rank faults against current providers in independent module namespaces.

AuthorityEffect: None. Eight single-fault copies share compilation, not state
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


ORACLE = '''
#[cfg(test)]
mod independent_rank_oracle {
    use super::*;
    #[test]
    fn determinant_on_all_ternary_two_by_two_matrices() {
        for code in 0..81usize {
            let values = [code % 3, (code / 3) % 3, (code / 9) % 3, (code / 27) % 3]
                .map(|value| value as i64 - 1);
            let expected = if values[0]*values[3] - values[1]*values[2] != 0 {
                2
            } else { usize::from(values != [0; 4]) };
            let matrix = BasicMatrix::from_row_major(2,2,values.map(q).to_vec()).unwrap();
            assert_eq!(certify_rank(&matrix).unwrap().rank(),expected);
        }
    }
}
'''


def main():
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output = ROOT / "evidence/quality/category_homology" / stamp
    output.mkdir(parents=True)
    work = RUST / "target/rc" / stamp[2:15]
    inputs = inventory()
    write_json(output / "source_manifest.json",inputs)
    shutil.copyfile(__file__,output / "run_rank_context_replay.py")
    snapshot(work,"homology")
    source = (RUST / "src/homology/rank_certificate.rs").read_text(encoding="utf-8")
    recipes = [(i,p,a,b) for i,p,a,b in mutations() if i.startswith("RK")]
    records, declarations = [], []
    for index, (identifier,path,needle,replacement) in enumerate([("baseline","homology/rank_certificate.rs","", ""),*recipes]):
        candidate = source
        if index:
            if source.count(needle) != 1:
                raise ValueError("Nonunique fault: " + identifier)
            candidate = source.replace(needle,replacement,1)
            if identifier in ("RK01-LU","RK02-VR","RK03-MUV"):
                label = replacement.strip('\",')
                blocks = [m.group(0) for m in re.finditer(r'        require_equal\([\s\S]*?\n        \)\?;',candidate)]
                matches = [block for block in blocks if '"'+label+'"' in block]
                if len(matches) != 1:
                    raise ValueError("Nonunique identity block: " + identifier)
                candidate = candidate.replace(matches[0],"",1)
        candidate_file = work / f"rank-{index}.rs"
        candidate_file.write_text(candidate + ORACLE,encoding="utf-8")
        module = "rank_replay_" + str(index)
        quoted = json.dumps(candidate_file.resolve().as_posix())
        declarations.append(f'#[cfg(test)]\nmod {module} {{\nuse super::{{errors, hashing, exact_scalar}};\n#[path={quoted}]\nmod rank_certificate;\n}}\n')
        if index:
            records.append({"id":identifier,"path":path,"outcome":"unrun","needle":needle,"replacement":replacement,
                "module":module,"subject_sha256":digest(RUST / "src" / path),
                "candidate_path":candidate_file.relative_to(ROOT).as_posix(),"candidate_sha256":digest(candidate_file)})
    with (work / "src/homology/mod.rs").open("a",encoding="utf-8") as stream:
        stream.write("\n" + "\n".join(declarations))
    roots, dependencies = bind_dependencies(work,output)
    tools = {key:subprocess.check_output([key,"--version"],text=True).strip() for key in ("cargo","rustc")}
    write_json(output / "mutations.json",records)
    binary, build = work / "rank-tests.exe", work / "target"
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
            baseline.append(execute([str(binary),"homology::","--skip","rank_replay_"],work,output / "homology-baseline.log"))
            baseline.append(execute([str(binary),"homology::rank_replay_0::"],work,output / "namespace-baseline.log"))
            if all(r["exit_code"] == 0 for r in baseline):
                for record in records:
                    run = execute([str(binary),"homology::" + record["module"] + "::"],work,output / (record["id"]+".log"),timeout=30)
                    log = (ROOT / run["log"]).read_text(encoding="utf-8")
                    outcome = "inconclusive" if run["timed_out"] else "survived" if run["exit_code"] == 0 else "killed" if "test result: FAILED" in log else "inconclusive"
                    record.update(outcome=outcome,run=run)
                    write_json(output / "mutations.json",records)
                    print(record["id"],outcome,flush=True)
            restored.append(execute([str(binary),"homology::","--skip","rank_replay_"],work,output / "homology-restored.log"))
            restored.append(execute([str(binary),"homology::rank_replay_0::"],work,output / "namespace-restored.log"))
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
        "scope":"Current-provider rank replay. Each rank module contains one designated fault and its own local tests plus an independent determinant oracle. The unchanged original homology namespace supplies composition checks. No compiler/MIR refinement or whole-workspace pass."}
    write_json(output / "summary.json",final)
    print("Receipt:",output,flush=True)
    print(json.dumps(final,indent=2),flush=True)
    return 0 if all(final[key] for key in ("baseline_ok","restored_baseline_ok","source_unchanged","dependencies_unchanged")) else 1


if __name__ == "__main__":
    raise SystemExit(main())
