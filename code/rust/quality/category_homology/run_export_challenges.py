"""Challenge declared public type identities, not the providers' mathematics.

The actual category crate supplies canonical controls. Mutant import blocks
rebind public child modules to that same crate and change one type re-export.
This preserves the relevant namespace environment without cloning provider
algorithms. The source adapter and its narrow observation are explicit.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import shutil
import subprocess

from run_audit import (ROOT, RUST, bind_dependencies, clear_debug_outputs,
                       dependency_inventory, digest, execute, execute_build,
                       inventory, snapshot, write_json)


POLICY = Path(__file__).with_name("export_boundaries.json")


def canonical(record, path):
    return "omega_category_theory::" + (path[7:] if path.startswith("crate::") else record["family"] + "::" + path)


def import_block(record):
    source = (ROOT / record["path"]).read_text(encoding="utf-8")
    modules = re.findall(r"^pub mod (\w+);$",source,re.M)
    actual = {}
    for match in re.finditer(r"pub use ([^;]+);",source):
        clause = match[1]
        if "{" in clause:
            prefix,names = clause.split("{")
            actual.update({name.strip():prefix + name.strip() for name in names.rstrip("}").split(",")})
        else:
            actual[clause.split("::")[-1]] = clause
    residual = re.sub(r"^\s*//[^\n]*", "", source, flags=re.M)
    residual = residual.replace("#[allow(clippy::module_inception)]", "")
    residual = re.sub(r"pub mod \w+;|pub use [^;]+;", "", residual)
    if residual.strip() or actual != record["exports"] or digest(ROOT / record["path"]) != record["sha256"]:
        raise ValueError("Unsupported or changed export interface: " + record["path"])
    declarations = [f'pub use omega_category_theory::{record["family"]}::{name};' for name in modules]
    uses = [f"pub use {path};" for path in actual.values()]
    return "\n".join([*declarations,*uses])


def tests(record, selected=None):
    rows = []
    for name,path in record["exports"].items():
        if selected is not None and name != selected:
            continue
        label = "identity" if selected is not None else "export_" + name
        rows.append(f'#[test] fn {label}() {{ assert_eq!(std::any::TypeId::of::<super::{name}>(), std::any::TypeId::of::<{canonical(record,path)}>()); }}')
    return "\n#[cfg(test)] mod tests {\n" + "\n".join(rows) + "\n}\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jobs", type=int, default=2)
    args = parser.parse_args()
    if args.jobs < 1:
        parser.error("positive compiler job count required")
    records = json.loads(POLICY.read_text(encoding="utf-8"))["records"]
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output = ROOT / "evidence/quality/category_homology" / stamp
    output.mkdir(parents=True)
    work = RUST / "target/ex" / stamp[2:15]
    inputs = inventory()
    write_json(output / "source_manifest.json",inputs)
    shutil.copyfile(__file__,output / "run_export_challenges.py")
    shutil.copyfile(POLICY,output / POLICY.name)
    snapshot(work,"category")
    folder = work / "export_challenges"
    folder.mkdir()
    (folder / "Cargo.toml").write_text('[package]\nname="export_challenges"\nversion="0.0.0"\nedition="2021"\n[lib]\npath="lib.rs"\n[dependencies]\nomega_category_theory={package="tfqm_category_theory",path="../src/category_theory"}\n',encoding="utf-8")
    declarations = ['#![allow(non_snake_case, unused_imports, dead_code)]',
                    'pub use omega_category_theory::legacy_adjunction;']
    controls, candidates = [], []
    for record in records:
        original = import_block(record)
        name = "baseline_" + record["family"]
        path = folder / (name + ".rs")
        path.write_text(original + tests(record),encoding="utf-8")
        declarations.append(f'#[path="{path.name}"] mod {name};')
        exports = list(record["exports"].items())
        for public,path_text in exports:
            controls.append(f'#[test] fn {record["family"]}_{public}() {{ assert_eq!(std::any::TypeId::of::<omega_category_theory::{record["family"]}::{public}>(), std::any::TypeId::of::<{canonical(record,path_text)}>()); }}')
            peer,peer_path = next((key,value) for key,value in exports if key != public)
            needle, replacement = f"pub use {path_text};", f"pub use {peer_path} as {public};"
            if original.count(needle) != 1:
                raise ValueError("Nonunique normalized import: " + needle)
            module = "mutant_" + str(len(candidates))
            candidate = folder / (module + ".rs")
            candidate.write_text(original.replace(needle,replacement,1) + tests(record,public),encoding="utf-8")
            declarations.append(f'#[path="{candidate.name}"] mod {module};')
            candidates.append({"id":"EX-" + record["family"] + "-" + public,
                "path":"category_theory/" + record["family"] + "/mod.rs", "outcome":"unrun",
                "module":module,"public_name":public,"original_export":path_text,"replacement_export":peer_path,
                "subject_sha256":record["sha256"],"candidate_sha256":digest(candidate),
                "candidate_path":candidate.relative_to(ROOT).as_posix(),
                "adapter":"Child module declarations alias the actual canonical provider modules; grouped imports split without changing their nominal identity."})
    declarations.append("#[cfg(test)] mod canonical_api {\n" + "\n".join(controls) + "\n}")
    (folder / "lib.rs").write_text("\n".join(declarations) + "\n",encoding="utf-8")
    (work / "Cargo.toml").write_text((work / "Cargo.toml").read_text().replace(
        'members = ["src/category_theory"]','members = ["src/category_theory", "export_challenges"]'),encoding="utf-8")
    roots,dependencies = bind_dependencies(work,output)
    tools = {name:subprocess.check_output([name,"--version"],text=True).strip() for name in ("cargo","rustc")}
    write_json(output / "mutations.json",candidates)
    build = work / "target"
    binaries = {"export_challenges":work / "exports.exe","tfqm_category_theory":work / "category.exe"}
    baseline, restored, builds = [], [], []
    try:
        try:
            command = ["cargo","test","--offline","--locked","--lib","--no-run","--message-format=json","--jobs",str(args.jobs),"--target-dir",str(build),"-p","export_challenges","-p","tfqm_category_theory"]
            run = execute_build(command,work,output / "build.log")
            builds.append(run)
            if run["exit_code"] == 0:
                for line in (ROOT / run["log"]).read_text(encoding="utf-8").splitlines():
                    try:
                        item = json.loads(line)
                    except ValueError:
                        continue
                    name = item.get("target",{}).get("name")
                    if item.get("reason") == "compiler-artifact" and item.get("executable") and name in binaries:
                        shutil.copyfile(item["executable"],binaries[name])
        finally:
            clear_debug_outputs(build,work)
        if run["exit_code"] == 0:
            def controls_for(phase):
                return [execute([str(binaries["tfqm_category_theory"])],work,output / (phase + "-category.log")),
                        execute([str(binaries["export_challenges"]),"canonical_api::"],work,output / (phase + "-canonical.log")),
                        execute([str(binaries["export_challenges"]),"baseline_"],work,output / (phase + "-normalized.log"))]
            baseline = controls_for("baseline")
            if all(row["exit_code"] == 0 for row in baseline):
                for candidate in candidates:
                    test_name = candidate["module"] + "::tests::identity"
                    run = execute([str(binaries["export_challenges"]),test_name,"--exact"],work,output / (candidate["id"] + ".log"))
                    text = (ROOT / run["log"]).read_text(encoding="utf-8")
                    outcome = "inconclusive" if run["timed_out"] else "survived" if run["exit_code"] == 0 else "killed" if "test result: FAILED" in text else "inconclusive"
                    candidate.update(outcome=outcome,run=run)
                write_json(output / "mutations.json",candidates)
            restored = controls_for("restored")
    finally:
        for binary in binaries.values():
            binary.unlink(missing_ok=True)
        if build.exists():
            clear_debug_outputs(build,work)
            shutil.rmtree(build)
    write_json(output / "baseline.json",{"tools":tools,"runs":baseline})
    write_json(output / "restored.json",{"tools":tools,"runs":restored})
    write_json(output / "builds.json",builds)
    write_json(output / "mutations.json",candidates)
    counts = Counter(row["outcome"] for row in candidates)
    eligible = sum(counts[key] for key in ("killed","survived","inconclusive","unrun"))
    summary = {"AuthorityEffect":"None","source_scope":"category","tools":tools,
        "baseline_ok":len(baseline) == 3 and all(row["exit_code"] == 0 for row in baseline),
        "restored_baseline_ok":len(restored) == 3 and all(row["exit_code"] == 0 for row in restored),
        "source_unchanged":inputs == inventory(),"source_manifest_sha256":digest(output / "source_manifest.json"),
        "dependencies_unchanged":dependencies == dependency_inventory(roots),"dependency_receipt_sha256":digest(output / "dependency_receipt.json"),
        "generated":len(candidates),"mutation_accounting":{key:counts[key] for key in ("killed","survived","demonstrably_equivalent","invalid","inconclusive","unrun")},
        "conservative_ratio":counts["killed"] / eligible if eligible else None,
        "all_files_L5A":False,"build_outputs_removed":not build.exists(),"runner_sha256":digest(Path(__file__)),
        "policy_sha256":digest(POLICY),"compiled_scope":"Actual category crate plus explicitly adapted nominal export identities; no child mathematical/engineering grade inheritance",
        "scope":"Canonical public controls validate actual source exports; single-fault normalized import blocks use the actual canonical child modules and change one type binding. Compiler/std TypeId identity is trusted within this binary only."}
    write_json(output / "summary.json",summary)
    print("Receipt:",output,flush=True)
    print(json.dumps(summary,indent=2),flush=True)
    return 0 if all(summary[key] for key in ("baseline_ok","restored_baseline_ok","source_unchanged","dependencies_unchanged")) else 1


if __name__ == "__main__":
    raise SystemExit(main())
