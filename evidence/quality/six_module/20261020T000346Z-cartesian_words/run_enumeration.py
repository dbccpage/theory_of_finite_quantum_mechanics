"""Actual combinatorics crate plus source-pinned one-fault enumeration copies.

Every build is followed by disposal of debug/temp outputs, even on failure.
Native controls support their recorded scope, never an automatic A award.
"""
from collections import Counter
from datetime import datetime, timezone
import argparse
import json
from pathlib import Path
import re
import shutil
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "category_homology"))
from run_audit import (ROOT, RUST, bind_dependencies, clear_debug_outputs,
                       dependency_inventory, digest, execute, execute_build, write_json)


def passed(run):
    return run["exit_code"] == 0 and not run["timed_out"] and bool(re.search(
        r"test result: ok\. [1-9][0-9]* passed;", (ROOT / run["log"]).read_text(encoding="utf-8")))


def inputs():
    folder = RUST / "src/combinatorics"
    return {p.relative_to(ROOT).as_posix(): digest(p) for p in sorted(folder.iterdir())
            if p.suffix == ".rs" or p.name == "Cargo.toml"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject", choices=("enumeration", "cartesian_words"), default="enumeration")
    args = parser.parse_args()
    name = args.subject
    prefix = name + "_subject_"
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output = ROOT / "evidence/quality/six_module" / (stamp + "-" + name)
    output.mkdir(parents=True)
    work = RUST / "target/six-module" / stamp
    package = work / "src/combinatorics"
    package.mkdir(parents=True)
    original = inputs()
    write_json(output / "source_manifest.json", original)
    for path in original:
        shutil.copyfile(ROOT / path, package / Path(path).name)
    (work / "Cargo.toml").write_text('[workspace]\nmembers=["src/combinatorics"]\nresolver="2"\n'
        '[profile.dev]\ndebug=0\n[profile.test]\ndebug=0\n', encoding="utf-8")
    for filename in (Path(__file__).name, name + "_challenges.rs", name + "_boundaries.json"):
        shutil.copyfile(HERE / filename, output / filename)
    policy = json.loads((HERE / (name + "_boundaries.json")).read_text(encoding="utf-8"))
    source = ROOT / policy["subject"]["path"]
    if digest(source) != policy["subject"]["sha256"]:
        raise ValueError("Policy/source drift")
    text = source.read_text(encoding="utf-8")
    fixture = (HERE / (name + "_challenges.rs")).read_text(encoding="utf-8")
    copies = [("control", text)]
    records = []
    for item in policy["faults"]:
        if text.count(item["needle"]) != 1:
            raise ValueError("Fault must designate one source occurrence: " + item["id"])
        candidate = text.replace(item["needle"], item["replacement"])
        copies.append((item["id"], candidate))
        records.append({**item, "outcome": "unrun"})
    generated = package / "q"
    generated.mkdir()
    declarations = []
    for index, (name, candidate) in enumerate(copies):
        path = generated / f"n{index}.rs"
        path.write_text(candidate + "\n" + fixture, encoding="utf-8")
        declarations.append(f'#[cfg(test)]\n#[path={json.dumps(path.resolve().as_posix())}] '
                            f'mod {prefix}{index};')
        if index:
            records[index-1].update({"candidate": str(path.relative_to(ROOT)), "sha256": digest(path)})
    with (package / "lib.rs").open("a", encoding="utf-8") as stream:
        stream.write("\n" + "\n".join(declarations) + "\n")
    write_json(output / "mutations.json", records)
    roots, dependencies = bind_dependencies(work, output)
    build, binary = work / "target", work / "tests.exe"
    baseline, restored, builds = [], [], []
    try:
        try:
            run = execute_build(["cargo", "test", "--offline", "--locked", "--lib", "--no-run",
                "--message-format=json", "--jobs", "1", "--target-dir", str(build)], work, output / "build.log")
            builds.append(run)
            if run["exit_code"] == 0:
                for line in (output / "build.log").read_text(encoding="utf-8").splitlines():
                    try:
                        item = json.loads(line)
                    except ValueError:
                        continue
                    if item.get("reason") == "compiler-artifact" and item.get("executable"):
                        shutil.copyfile(item["executable"], binary)
        finally:
            clear_debug_outputs(build, work)
        if run["exit_code"] == 0:
            baseline = [execute([str(binary), "--skip", prefix], work, output / "baseline.log"),
                        execute([str(binary), prefix + "0::"], work, output / "control.log")]
            if all(passed(item) for item in baseline):
                for index, record in enumerate(records, 1):
                    result = execute([str(binary), f"{prefix}{index}::"], work,
                                     output / f"fault-{index}.log", timeout=30)
                    log = (ROOT / result["log"]).read_text(encoding="utf-8")
                    record["outcome"] = ("inconclusive" if result["timed_out"] else
                        "survived" if passed(result) else "killed" if result["exit_code"] != 0
                        and "test result: FAILED" in log else "inconclusive")
                    record["run"] = result
                    write_json(output / "mutations.json", records)
            restored = [execute([str(binary), prefix + "0::"], work, output / "restored-control.log"),
                        execute([str(binary), "--skip", prefix], work, output / "restored.log")]
    finally:
        binary.unlink(missing_ok=True)
        if build.exists():
            clear_debug_outputs(build, work)
            if build.resolve().parent != work.resolve():
                raise ValueError("Unsafe cleanup target")
            shutil.rmtree(build)
    counts = Counter(record["outcome"] for record in records)
    outcomes = {key: counts[key] for key in ("killed", "survived", "demonstrably_equivalent", "invalid", "inconclusive", "unrun")}
    eligible = sum(outcomes[key] for key in ("killed", "survived", "inconclusive", "unrun"))
    summary = {"AuthorityEffect": "None", "baseline_ok": len(baseline) == 2 and all(map(passed, baseline)),
        "restored_ok": len(restored) == 2 and all(map(passed, restored)), "baseline": baseline,
        "restored": restored, "builds": builds, "mutation_accounting": outcomes,
        "conservative_ratio": counts["killed"] / eligible if eligible else None,
        "source_unchanged": original == inputs(), "dependencies_unchanged": dependencies == dependency_inventory(roots),
        "build_outputs_removed": not build.exists(), "subject": policy["subject"],
        "scope": "Actual standalone combinatorics crate, its canonical 44 tests and one-fault " + name + " copies with independent controls. No whole-workspace or Rust/MIR proof.",
        "runner_sha256": digest(output / Path(__file__).name), "policy_sha256": digest(output / (name + "_boundaries.json")),
        "fixture_sha256": digest(output / (name + "_challenges.rs"))}
    write_json(output / "summary.json", summary)
    print("Receipt:", output, flush=True)
    print(json.dumps(summary, indent=2), flush=True)
    return 0 if all(summary[k] for k in ("baseline_ok", "restored_ok", "source_unchanged", "dependencies_unchanged")) else 1


if __name__ == "__main__":
    raise SystemExit(main())
