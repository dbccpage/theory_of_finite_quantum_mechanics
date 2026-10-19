"""Replay hash protocol faults against current providers in independent module namespaces.

AuthorityEffect: None. Independent single-fault copies share compilation, not state
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


ORACLE = Path(__file__).with_name("hash_protocol_oracle.rs").read_text(encoding="utf-8")


def hash_mutations(source):
    records = []
    def fault(name, needle, replacement):
        records.append(("HS" + str(len(records)+1).zfill(2) + "-" + name,"homology/hashing.rs",needle,replacement))
    fault("undefined-domain", "if value.denom().is_zero() {", "if false {")
    fault("defined-normalization", "hash_rational(hasher, value);", "hash_bigint(hasher, value.numer()); hash_bigint(hasher, value.denom());")
    starts = list(re.finditer(r"pub fn (hash_\w+)\(",source))
    for start in starts:
        end = source.index("\n}", start.start()) + 2
        block = source[start.start():end]
        statements = re.findall(r"    hasher.update\([^;]+;",block)
        for index, statement in enumerate(statements):
            # A distinct, valid omission of each tag/framing/binding field.
            fault(start[1] + "-field-" + str(index),block,block.replace(statement,"",1))
        for statement in re.findall(r"        hash_stored_rational\([^;]+;",block):
            fault(start[1] + "-scalar-payload",block,block.replace(statement,"",1))
    fault("scalar-numerator", "hash_bigint(hasher, value.numer());", "hash_bigint(hasher, &BigInt::from(0));")
    fault("scalar-denominator", "hash_bigint(hasher, value.denom());", "hash_bigint(hasher, &BigInt::from(1));")
    fault("integer-payload", "hash_bigint(&mut hasher, val);", "hash_bigint(&mut hasher, &BigInt::from(0));")
    fault("digest-hex", "hex::encode(self.0)", "hex::encode([0u8; 32])")
    fault("digest-display", "&self.0[28..]", "&self.0[..4]")
    return records


def main():
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output = ROOT / "evidence/quality/category_homology" / stamp
    output.mkdir(parents=True)
    work = RUST / "target/hc" / stamp[2:15]
    inputs = inventory()
    write_json(output / "source_manifest.json",inputs)
    shutil.copyfile(__file__,output / "run_hash_context_replay.py")
    snapshot(work,"homology")
    source = (RUST / "src/homology/hashing.rs").read_text(encoding="utf-8")
    recipes = hash_mutations(source)
    records, declarations = [], []
    for index, (identifier,path,needle,replacement) in enumerate([("baseline","homology/hashing.rs","", ""),*recipes]):
        candidate = source
        if index:
            if source.count(needle) != 1:
                raise ValueError("Nonunique fault: " + identifier)
            candidate = source.replace(needle,replacement,1)
        candidate_file = work / f"hash-{index}.rs"
        candidate_file.write_text(candidate + ORACLE,encoding="utf-8")
        module = "hash_replay_" + str(index)
        quoted = json.dumps(candidate_file.resolve().as_posix())
        declarations.append(f'#[cfg(test)]\nmod {module} {{\n#[path={quoted}]\nmod hashing;\n}}\n')
        if index:
            records.append({"id":identifier,"path":path,"outcome":"unrun","needle":needle,"replacement":replacement,
                "module":module,"subject_sha256":digest(RUST / "src" / path),
                "candidate_path":candidate_file.relative_to(ROOT).as_posix(),"candidate_sha256":digest(candidate_file)})
    with (work / "src/homology/mod.rs").open("a",encoding="utf-8") as stream:
        stream.write("\n" + "\n".join(declarations))
    shutil.copyfile(Path(__file__).with_name("hash_protocol_oracle.rs"),output / "hash_protocol_oracle.rs")
    roots, dependencies = bind_dependencies(work,output)
    tools = {key:subprocess.check_output([key,"--version"],text=True).strip() for key in ("cargo","rustc")}
    write_json(output / "mutations.json",records)
    binary, build = work / "hash-tests.exe", work / "target"
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
            baseline.append(execute([str(binary),"homology::","--skip","hash_replay_"],work,output / "homology-baseline.log"))
            baseline.append(execute([str(binary),"homology::hash_replay_0::"],work,output / "namespace-baseline.log"))
            if all(r["exit_code"] == 0 for r in baseline):
                for record in records:
                    run = execute([str(binary),"homology::" + record["module"] + "::"],work,output / (record["id"]+".log"),timeout=30)
                    log = (ROOT / run["log"]).read_text(encoding="utf-8")
                    outcome = "inconclusive" if run["timed_out"] else "survived" if run["exit_code"] == 0 else "killed" if "test result: FAILED" in log else "inconclusive"
                    record.update(outcome=outcome,run=run)
                    write_json(output / "mutations.json",records)
                    print(record["id"],outcome,flush=True)
            restored.append(execute([str(binary),"homology::","--skip","hash_replay_"],work,output / "homology-restored.log"))
            restored.append(execute([str(binary),"homology::hash_replay_0::"],work,output / "namespace-restored.log"))
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
        "all_files_L5A":False,"build_outputs_removed":not build.exists(),"runner_sha256":digest(Path(__file__)), "oracle_sha256":digest(output / "hash_protocol_oracle.rs"),
        "scope":"Current-provider hash protocol replay. Each hash module contains one designated fault and local tests plus independently constructed fixed-input wire encodings. The crypto primitive and BigInt storage remain trusted. The unchanged original homology namespace supplies composition checks. No compiler/MIR refinement or whole-workspace pass."}
    write_json(output / "summary.json",final)
    print("Receipt:",output,flush=True)
    print(json.dumps(final,indent=2),flush=True)
    return 0 if all(final[key] for key in ("baseline_ok","restored_baseline_ok","source_unchanged","dependencies_unchanged")) else 1


if __name__ == "__main__":
    raise SystemExit(main())
