"""Replay both actual fusion crate roots with admission boundary challenges.

No production Rust substitutions/stubs. Only the second Cargo package name and
lib path change to select mod.rs as its crate root. Builds always lose owned
debug/temp outputs; copied test binaries are removed after use.
"""
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import shutil
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "category_homology"))
from run_audit import (ROOT, RUST, bind_dependencies, clear_debug_outputs,
                       dependency_inventory, digest, execute, execute_build, write_json)


def main():
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output = ROOT / "evidence/quality/six_module" / (stamp + "-fusion-audit")
    output.mkdir(parents=True)
    work = RUST / "target/six-module" / (stamp + "-fusion")
    work.mkdir(parents=True)
    source_dir = RUST / "src/fusion_categories"
    sources = {p.relative_to(ROOT).as_posix(): digest(p) for p in sorted(source_dir.iterdir())
               if p.suffix == ".rs" or p.name == "Cargo.toml"}
    write_json(output / "source_manifest.json", sources)
    (work / "Cargo.toml").write_text('[workspace]\nmembers=["lib-root","mod-root"]\nresolver="2"\n'
        '[profile.dev]\ndebug=0\n[profile.test]\ndebug=0\n', encoding="utf-8")
    for tag in ("lib", "mod"):
        package = work / (tag + "-root")
        package.mkdir()
        for source in sources:
            shutil.copyfile(ROOT / source, package / Path(source).name)
        if tag == "mod":
            manifest = package / "Cargo.toml"
            text = manifest.read_text(encoding="utf-8")
            text = text.replace('name = "tfqm_fusion_categories"', 'name = "tfqm_fusion_categories_mod_root"')
            text = text.replace('path = "lib.rs"', 'path = "mod.rs"')
            manifest.write_text(text, encoding="utf-8")
        for target, fixture in ((tag + ".rs", "fusion_sum_challenges.rs"),
                                ("fusion_ring.rs", "fusion_admission_challenges.rs")):
            with (package / target).open("a", encoding="utf-8") as stream:
                stream.write("\n" + (HERE / fixture).read_text(encoding="utf-8"))
    for filename in (Path(__file__).name, "fusion_sum_challenges.rs", "fusion_admission_challenges.rs"):
        shutil.copyfile(HERE / filename, output / filename)
    copied = {p.relative_to(ROOT).as_posix(): digest(p) for p in sorted(work.rglob("*")) if p.is_file()}
    write_json(output / "copied_sources.json", copied)
    roots, dependencies = bind_dependencies(work, output)
    build = work / "target"
    binaries, runs = [], []
    try:
        try:
            compiled = execute_build(["cargo", "test", "--offline", "--locked", "--workspace", "--lib",
                "--no-run", "--message-format=json", "--jobs", "1", "--target-dir", str(build)],
                work, output / "build.log")
            if compiled["exit_code"] == 0:
                for line in (output / "build.log").read_text(encoding="utf-8").splitlines():
                    try:
                        item = json.loads(line)
                    except ValueError:
                        continue
                    if item.get("reason") == "compiler-artifact" and item.get("executable"):
                        binary = work / (item["target"]["name"] + ".exe")
                        shutil.copyfile(item["executable"], binary)
                        binaries.append(binary)
        finally:
            clear_debug_outputs(build, work)
        if compiled["exit_code"] == 0:
            for binary in binaries:
                runs.append(execute([str(binary), "--test-threads=1"], work,
                                    output / (binary.stem + ".log"), timeout=300))
    finally:
        for binary in binaries:
            binary.unlink(missing_ok=True)
        if build.exists():
            shutil.rmtree(build)
    okay = len(runs) == 2 and all(item["exit_code"] == 0 and not item["timed_out"] and
        re.search(r"test result: ok\. [1-9][0-9]* passed;", (ROOT / item["log"]).read_text(encoding="utf-8")) for item in runs)
    receipt = {"AuthorityEffect": "None", "baseline_ok": okay, "build": compiled, "runs": runs,
        "source_unchanged": all(digest(ROOT / path) == value for path, value in sources.items()),
        "dependencies_unchanged": dependency_inventory(roots) == dependencies,
        "copied_sources_unchanged": all(digest(ROOT / path) == value for path, value in copied.items()),
        "build_outputs_removed": not build.exists() and not any(p.exists() for p in binaries),
        "scope": "Both actual local fusion crate roots and appended pure arithmetic/admission challenges; external path dependencies are content-bound. No mutation campaign, full grade or whole-workspace success is inferred."}
    write_json(output / "receipt.json", receipt)
    print("Receipt:", output, flush=True)
    print(json.dumps({k: value for k, value in receipt.items() if isinstance(value, bool)}), flush=True)
    return 0 if all(value for value in receipt.values() if isinstance(value, bool)) else 1


if __name__ == "__main__":
    raise SystemExit(main())
