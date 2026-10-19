"""Source-bound metadata challenges. AuthorityEffect: None.

Each candidate is a separate, state-free Rust module containing one source
mutation. Its own tests run separately by namespace; faults are never combined
in one assessed module. Several independent modules share a compilation to
avoid recompiling serde for every label. This is not an alternate compiler.
"""

import argparse
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import subprocess

from run_audit import (ROOT, RUST, bind_dependencies, clear_debug_outputs,
                       dependency_inventory, digest, execute, execute_build,
                       inventory, snapshot, write_json)


POLICY = Path(__file__).with_name("metadata_boundaries.json")


def challenge(record):
    """Generate tests from the separately reviewed schema, never its guards."""
    if record.get("collection_schema"):
        from collection_metadata import challenge as collection_challenge
        return collection_challenge(record)
    if record.get("parameter_schema"):
        from parameter_metadata import challenge as parameter_challenge
        return parameter_challenge(record)
    kind, fields = record["type"], record["required_fields"]
    assignments = "\n".join(f'        value.{f} = format!("{f}:alpha\\0");' for f in fields)
    clear = "\n".join(f'            if mask & (1 << {i}) != 0 {{ value.{f}.clear(); }}'
                       for i, f in enumerate(fields))
    field_names = ", ".join(json.dumps(f) for f in fields)
    generated = '''
#[cfg(test)]
mod schema_challenge {
    use super::*;
    #[test]
    fn exhaustive_required_fields() {
        let fields = [FIELD_NAMES];
        for mask in 0usize..(1 << fields.len()) {
            let mut value = TYPE::default();
ASSIGNMENTS
CLEAR
            let before = value.clone();
            let expected = (0..fields.len()).find(|i| mask & (1 << i) != 0);
            match (expected, value.validate_shell()) {
                (None, Ok(())) => (),
                (Some(i), Err(ArithmosError::InvalidShape(message))) => {
                    assert_eq!(message, format!("empty {}", fields[i]));
                }
                (wanted, got) => panic!("mask {mask}, expected {wanted:?}, got {got:?}"),
            }
            assert_eq!(value, before, "validation must leave the raw record unchanged");
            let bytes = serde_json::to_vec(&value).unwrap();
            let decoded: TYPE = serde_json::from_slice(&bytes).unwrap();
            assert_eq!(decoded, value, "serde returns raw data, never a law certificate");
            assert_eq!(decoded.validate_shell(), value.validate_shell());
        }
    }
    #[test]
    fn labels_are_literal_not_mathematical_certificates() {
        assert_eq!(TYPE::new("literal-label").label, "literal-label");
        for text in [" ", "α\\0", "unverified mathematical declaration"] {
            let mut value = TYPE::default();
LITERAL_ASSIGNMENTS
            assert!(value.validate_shell().is_ok());
        }
    }
}
'''.replace("FIELD_NAMES", field_names).replace("TYPE", kind).replace(
        "ASSIGNMENTS", assignments).replace("CLEAR", clear).replace(
        "LITERAL_" + assignments, "\n".join(f'            value.{f} = text.into();' for f in fields))
    if record["type"] == "AbelianCategory":
        generated += '''
#[cfg(test)]
mod checklist_challenge {
    use super::*;
    #[test]
    fn every_raw_checklist_is_conjunction_without_law_promotion() {
        for mask in 0u8..8 {
            let value = AbelianCategory::with_flags("raw", mask & 1 != 0, mask & 2 != 0, mask & 4 != 0);
            assert_eq!(value.checklist_complete(), mask == 7);
            assert_eq!((value.additive, value.has_kernels, value.has_cokernels),
                (mask & 1 != 0, mask & 2 != 0, mask & 4 != 0));
            assert!(value.validate_shell().is_ok(), "raw shape admission is not a law claim");
        }
        assert!(AbelianCategory::claimed_abelian("declared").checklist_complete());
    }
}
'''
    elif record["type"] == "Additivity":
        generated += '''
#[cfg(test)]
mod checklist_challenge {
    use super::*;
    #[test]
    fn each_raw_flag_combination_remains_a_declaration() {
        for mask in 0u8..4 {
            let value = Additivity::with_flags("raw", mask & 1 != 0, mask & 2 != 0);
            assert_eq!((value.has_biproducts, value.zero_object), (mask & 1 != 0, mask & 2 != 0));
            assert!(value.validate_shell().is_ok());
        }
    }
}
'''
    return generated


def variants(record, source):
    if record.get("collection_schema"):
        from collection_metadata import variants as collection_variants
        return collection_variants(record, source)
    if record.get("parameter_schema"):
        from parameter_metadata import variants as parameter_variants
        return parameter_variants(record, source)
    rows = []
    for field in record["required_fields"]:
        for suffix, needle, replacement in (
            ("skip", f"if self.{field}.is_empty() {{", "if false {"),
            ("diagnostic", f'"empty {field}".into()', '"wrong field diagnostic".into()'),
        ):
            if source.count(needle) != 1:
                raise ValueError(f"Nonunique {record['path']}:{field}:{suffix}")
            rows.append((field + "-" + suffix, source.replace(needle, replacement, 1), needle, replacement))
    needle = "        Ok(())"
    if source.count(needle) != 1:
        raise ValueError("Nonunique validator commit: " + record["path"])
    replacement = '        Err(ArithmosError::InvalidShape("reject valid".into()))'
    rows.append(("reject-valid", source.replace(needle, replacement, 1), needle, replacement))
    needle = "label: label.into()"
    if needle not in source:
        raise ValueError("Missing new-label assignment: " + record["path"])
    replacement = "label: String::new()"
    rows.append(("drop-new-label", source.replace(needle, replacement, 1), needle, replacement))
    extras = []
    if record["type"] == "AbelianCategory":
        extras = [
            ("checklist-additive", "self.additive &&", "true &&"),
            ("checklist-kernels", "&& self.has_kernels &&", "&& true &&"),
            ("checklist-cokernels", "&& self.has_cokernels", "&& true"),
            ("claimed-checklist", "Self::with_flags(label, true, true, true)", "Self::with_flags(label, false, true, true)"),
        ]
    elif record["type"] == "Additivity":
        extras = [("distinct-flag-bindings", "            has_biproducts,\n            zero_object,", "            has_biproducts: zero_object,\n            zero_object: has_biproducts,")]
    for tag, needle, replacement in extras:
        if source.count(needle) != 1:
            raise ValueError("Nonunique checklist fault: " + record["path"] + ":" + tag)
        rows.append((tag,source.replace(needle,replacement,1),needle,replacement))
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy", type=Path, default=POLICY)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--batch-size", type=int, default=8)
    args = parser.parse_args()
    if args.batch_size < 1 or args.offset < 0 or (args.limit is not None and args.limit < 1):
        parser.error("positive batch/limit and nonnegative offset required")
    policy = args.policy.resolve()
    records = json.loads(policy.read_text(encoding="utf-8"))["records"]
    records = records[args.offset:None if args.limit is None else args.offset + args.limit]
    if not records:
        parser.error("empty selection")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output = ROOT / "evidence/quality/category_homology" / stamp
    output.mkdir(parents=True)
    work = RUST / "target/ms" / stamp[2:15]
    inputs = inventory()
    write_json(output / "source_manifest.json", inputs)
    shutil.copyfile(__file__, output / "run_metadata_challenges.py")
    shutil.copyfile(policy, output / policy.name)
    if any(record.get("parameter_schema") for record in records):
        shutil.copyfile(Path(__file__).with_name("parameter_metadata.py"), output / "parameter_metadata.py")
    if any(record.get("collection_schema") for record in records):
        shutil.copyfile(Path(__file__).with_name("collection_metadata.py"), output / "collection_metadata.py")
    snapshot(work, "category")
    build = work / "target"
    members, campaigns = [], []
    for batch_index in range(0, len(records), args.batch_size):
        package = f"metadata_challenge_{batch_index // args.batch_size}"
        folder = work / package
        folder.mkdir()
        (folder / "Cargo.toml").write_text(
            f'[package]\nname="{package}"\nversion="0.0.0"\nedition="2021"\n'
            '[lib]\npath="lib.rs"\n[dependencies]\n'
            'omega_category_theory={package="tfqm_category_theory",path="../src/category_theory"}\n'
            'serde={version="1.0",features=["derive"]}\nserde_json="1.0"\n', encoding="utf-8")
        declarations = sorted({declaration for item in records[batch_index:batch_index + args.batch_size]
                               for declaration in item.get("harness_imports", [])})
        candidates = []
        for item in records[batch_index:batch_index + args.batch_size]:
            source_path = ROOT / item["path"]
            if digest(source_path) != item["sha256"]:
                raise ValueError("Policy source drift: " + item["path"])
            source = source_path.read_text(encoding="utf-8")
            copies = [("baseline", source, "", ""), *variants(item, source)]
            for tag, candidate, needle, replacement in copies:
                module = ("baseline_" if tag == "baseline" else "mutant_") + str(len(declarations))
                candidate_file = folder / (module + ".rs")
                candidate_file.write_text(candidate + challenge(item), encoding="utf-8")
                declarations.append(f'#[path="{module}.rs"]\nmod {module};')
                if tag != "baseline":
                    candidates.append({"id":item["path"].split("category_theory/")[1][:-3].replace("/", "-") + "-" + tag,
                        "path":"category_theory/" + item["path"].split("category_theory/")[1],
                        "outcome":"unrun", "module":module, "needle":needle, "replacement":replacement,
                        "candidate_sha256":digest(candidate_file), "candidate_path":str(candidate_file.relative_to(ROOT)),
                        "subject_sha256":item["sha256"], "failure_class":tag})
        (folder / "lib.rs").write_text("#![allow(dead_code, unused_variables)]\n" + "\n".join(declarations) + "\n", encoding="utf-8")
        members.append(package)
        campaigns.append((package, candidates))
    manifest = (work / "Cargo.toml").read_text(encoding="utf-8").replace(
        'members = ["src/category_theory"]', 'members = ' + json.dumps(["src/category_theory", *members]))
    (work / "Cargo.toml").write_text(manifest, encoding="utf-8")
    dependency_roots, dependency_inputs = bind_dependencies(work, output)
    tools = {key:subprocess.check_output([key,"--version"],text=True).strip() for key in ("cargo","rustc")}
    baseline, restored, builds = [], [], []
    all_candidates = [item for _, candidates in campaigns for item in candidates]
    write_json(output / "mutations.json", all_candidates)
    category_binary = work / "category-tests.exe"
    try:
        for index, (package, candidates) in enumerate(campaigns):
            command = ["cargo","test","--offline","--locked","--no-run","--message-format=json",
                       "--target-dir",str(build),"-p",package]
            if index == 0:
                command.extend(["-p","tfqm_category_theory"])
            binary = work / "metadata-tests.exe"
            try:
                run = execute_build(command, work, output / f"build-{index}.log")
                builds.append(run)
                if run["exit_code"] == 0:
                    for line in (ROOT / run["log"]).read_text(encoding="utf-8").splitlines():
                        try:
                            message = json.loads(line)
                        except ValueError:
                            continue
                        if message.get("reason") == "compiler-artifact" and message.get("executable"):
                            name = message["target"]["name"]
                            shutil.copyfile(message["executable"], category_binary if name == "tfqm_category_theory" else binary)
            finally:
                clear_debug_outputs(build, work)
            if run["exit_code"] != 0:
                for candidate in candidates:
                    candidate["reason"] = "Shared compilation did not finish; no isolated test result is attributed."
                break
            if index == 0:
                baseline.append(execute([str(category_binary)],work,output / "category-baseline.log"))
            before = execute([str(binary),"baseline_"],work,output / f"baseline-{index}.log")
            baseline.append(before)
            if before["exit_code"] == 0 and all(r["exit_code"] == 0 for r in baseline):
                for candidate in candidates:
                    run = execute([str(binary),candidate["module"] + "::"],work,output / (candidate["id"] + ".log"))
                    log = (ROOT / run["log"]).read_text(encoding="utf-8")
                    outcome = "inconclusive" if run["timed_out"] else "survived" if run["exit_code"] == 0 else "killed" if "test result: FAILED" in log else "inconclusive"
                    candidate.update(outcome=outcome,run=run)
            restored.append(execute([str(binary),"baseline_"],work,output / f"restored-{index}.log"))
            binary.unlink()
            write_json(output / "mutations.json",all_candidates)
            print(package,dict(Counter(c["outcome"] for c in candidates)),flush=True)
        if category_binary.exists():
            restored.append(execute([str(category_binary)],work,output / "category-restored.log"))
    finally:
        for name in ("metadata-tests.exe", "category-tests.exe"):
            (work / name).unlink(missing_ok=True)
        if build.exists():
            clear_debug_outputs(build, work)
            shutil.rmtree(build)
    write_json(output / "baseline.json",{"tools":tools,"runs":baseline})
    write_json(output / "restored.json",{"tools":tools,"runs":restored})
    write_json(output / "mutations.json",all_candidates)
    write_json(output / "builds.json",builds)
    outcomes = Counter(row["outcome"] for row in all_candidates)
    eligible = sum(outcomes[key] for key in ("killed","survived","inconclusive","unrun"))
    final = {"AuthorityEffect":"None","tools":tools,"source_scope":"category","baseline_ok":bool(baseline) and len(baseline) == len(campaigns) + 1 and all(r["exit_code"] == 0 for r in baseline),
        "restored_baseline_ok":bool(restored) and len(restored) == len(campaigns) + 1 and all(r["exit_code"] == 0 for r in restored),
        "source_manifest_sha256":digest(output / "source_manifest.json"),"source_unchanged":inputs == inventory(),
        "dependencies_unchanged":dependency_inputs == dependency_inventory(dependency_roots),
        "dependency_receipt_sha256":digest(output / "dependency_receipt.json"),"generated":len(all_candidates),
        "mutation_accounting":{key:outcomes[key] for key in ("killed","survived","demonstrably_equivalent","invalid","inconclusive","unrun")},
        "conservative_ratio":outcomes["killed"] / eligible if eligible else None,"all_files_L5A":False,
        "scope":"Independent single-fault module variants; module-local tests run separately. Source guards are not used to construct expected outcomes. No whole-directory grade, extracted proof or alternate compiler claim.",
        "selected_records":len(records),"policy_sha256":digest(policy),"runner_sha256":digest(Path(__file__)),"build_outputs_removed":not build.exists()}
    write_json(output / "summary.json",final)
    print("Receipt:",output,flush=True)
    print(json.dumps(final,indent=2),flush=True)
    return 0 if all(final[key] for key in ("baseline_ok","restored_baseline_ok","source_unchanged","dependencies_unchanged")) else 1


if __name__ == "__main__":
    raise SystemExit(main())
