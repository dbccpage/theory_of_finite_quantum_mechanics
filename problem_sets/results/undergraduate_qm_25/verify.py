"""Execute the trusted, checked-in solution YAML blocks using existing math code.

This file handles loading, source provenance, compilation and comparison only.
It implements no quantum mechanics or scalar/matrix arithmetic. Run from any
directory with Python >=3.10 and PyYAML. Cargo defaults to offline operation.
"""
from __future__ import annotations

import argparse
import ast
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CATALOG = ROOT / "problem_sets/problems/undergraduate_qm_25.yaml"
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / "code/python"))


class UniqueLoader(yaml.SafeLoader):
    """Reject duplicate YAML keys rather than silently keeping the last one."""


def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ValueError(f"duplicate YAML key: {key!r}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def read_yaml(path):
    return yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueLoader)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def run(command, log_name, *, cwd=ROOT, timeout=600):
    start = time.monotonic()
    proc = subprocess.run(command, cwd=cwd, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", timeout=timeout,
                          env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONIOENCODING": "utf-8"})
    (HERE / log_name).write_text((proc.stdout + proc.stderr).rstrip() + "\n", encoding="utf-8", newline="\n")
    receipt = {"command": [str(x) for x in command], "exit_code": proc.returncode,
               "elapsed_seconds": round(time.monotonic()-start, 3), "log": log_name}
    if proc.returncode:
        raise RuntimeError(f"Command failed ({proc.returncode}); see {HERE / log_name}")
    return proc.stdout, receipt


def contained_source(relative):
    path = (ROOT / relative).resolve()
    if not path.is_relative_to(ROOT) or not path.is_file():
        raise ValueError(f"Missing or out-of-repository source: {relative}")
    return path


def declared_symbols(content, suffix):
    """Resolve the declaration forms used by this collection, not incidental mentions.

    Python uses its parser. Rust and Lean use declaration-line bindings; their
    compilers independently check the referenced source modules during replay.
    """
    if suffix == ".py":
        return {node.name for node in ast.parse(content).body
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))}
    if suffix == ".rs":
        pattern = r"^\s*(?:pub(?:\([^)]*\))?\s+)?(?:fn|struct|enum|trait|type)\s+(\w+)\b"
    elif suffix == ".lean":
        pattern = r"^\s*(?:noncomputable\s+)?(?:theorem|lemma|def|abbrev|structure|class)\s+(\w+)\b"
    else:
        raise ValueError(f"Unsupported reference source type: {suffix}")
    # Eliminate comment-only declarations, including nested Rust/Lean blocks.
    opener, closer, line = ("/*", "*/", "//") if suffix == ".rs" else ("/-", "-/", "--")
    cleaned, depth = [], 0
    for raw_line in content.splitlines():
        i, current = 0, []
        while i < len(raw_line):
            if raw_line.startswith(opener, i):
                depth += 1
                i += 2
            elif depth and raw_line.startswith(closer, i):
                depth -= 1
                i += 2
            elif not depth and raw_line.startswith(line, i):
                break
            else:
                if not depth:
                    current.append(raw_line[i])
                i += 1
        cleaned.append("".join(current))
    return set(re.findall(pattern, "\n".join(cleaned), re.MULTILINE))


def check_reference(reference):
    path = contained_source(reference["path"])
    content = path.read_text(encoding="utf-8")
    declarations = declared_symbols(content, path.suffix)
    symbols = reference.get("symbols", [reference.get("symbol")])
    for symbol in symbols:
        if not symbol or symbol not in declarations:
            raise ValueError(f"Unresolved symbol {symbol!r} in {path}")
    return path


def check_output(problem_id, language, actual, expected):
    if not isinstance(actual, dict) or set(actual) != set(expected):
        raise ValueError(f"{problem_id} {language}: output keys differ from expected")
    for key, value in actual.items():
        if type(value) is not str or str(Fraction(value)) != value:
            raise ValueError(f"{problem_id} {language}: {key} is not a canonical rational string")
        if value != expected[key]:
            raise ValueError(f"{problem_id} {language}: {key}: {value!r} != {expected[key]!r}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lean", action="store_true", help="Compile the existing referenced Lean source modules, sequentially.")
    parser.add_argument("--lean-executable", default="lean", help="Lean executable; useful when the pinned toolchain is not on PATH.")
    parser.add_argument("--online", action="store_true", help="Allow Cargo to download declared crates instead of using only its cache.")
    args = parser.parse_args()
    report = {"schema_version": 1, "status": "running", "started_utc": datetime.now(timezone.utc).isoformat(),
              "scope": "25 fixed teaching calculations, each executed in Python and Rust; no general continuum theorem is inferred.",
              "lean": {"status": "not_run", "scope": "Only existing referenced modules; not all analytic derivations."}}
    report_path = HERE / "verification.json"
    write_json(report_path, report)
    try:
        catalog = read_yaml(CATALOG)
        problems = catalog["problems"]
        expected_ids = [f"UQM-{i:02d}" for i in range(1, 26)]
        if [p["id"] for p in problems] != expected_ids:
            raise ValueError("The catalog must contain exactly UQM-01 through UQM-25 in order")
        solutions, sources, lean_sources = [], set(), set()
        inputs = {CATALOG, Path(__file__).resolve()}
        for problem in problems:
            path = contained_source(problem["solution"])
            solution = read_yaml(path)
            inputs.add(path)
            if solution["problem_id"] != problem["id"] or solution["title"] != problem["title"]:
                raise ValueError(f"Catalog/solution mismatch: {problem['id']}")
            if solution["problem_file"] != CATALOG.relative_to(ROOT).as_posix():
                raise ValueError("Broken problem backlink")
            if set(solution["solutions"]) != {"python", "rust"}:
                raise ValueError("Every problem needs exactly Python and Rust solutions")
            if len(solution["derivation"]) < 5:
                raise ValueError("Missing detailed derivation")
            if not solution["verification"]["not_established"] or not solution["improvement_target"]:
                raise ValueError("Missing scope boundary or improvement target")
            for lang in ("python", "rust"):
                block = solution["solutions"][lang]
                if len(block["walkthrough"]) < 3 or not block["code"].strip():
                    raise ValueError("Missing language walkthrough or executable code")
                sources.update(check_reference(ref) for ref in block["existing_sources"])
            for ref in solution["lean4"]["references"]:
                lean_sources.add(check_reference(ref))
            for value in solution["verification"]["expected_outputs"].values():
                if type(value) is not str or str(Fraction(value)) != value:
                    raise ValueError("Expected values must be canonical rational strings")
            solutions.append(solution)
        # The before/after source hashes reject edits to these inputs during execution.
        source_before = {p: digest(p) for p in sources | lean_sources | inputs}
        py_outputs = {}
        for solution in solutions:
            ident = solution["problem_id"]
            namespace = {"__name__": f"undergraduate_solution_{ident.replace('-', '_')}"}
            code = solution["solutions"]["python"]["code"]
            exec(compile(code, f"{ident}.yaml:solutions.python.code", "exec"), namespace)
            result = namespace["solve"]()
            check_output(ident, "python", result, solution["verification"]["expected_outputs"])
            py_outputs[ident] = result
        write_json(HERE / "python_outputs.json", py_outputs)
        print(f"Python: {len(py_outputs)}/25 solution blocks passed.", flush=True)

        runner = HERE / "rust_runner"
        (runner / "src").mkdir(parents=True, exist_ok=True)
        manifest = runner / "Cargo.toml"
        manifest.write_text('''[package]
name = "undergraduate_qm_25_runner"
version = "0.1.0"
edition = "2021"
publish = false

[workspace]

[dependencies]
num-bigint = { version = "0.4", features = ["serde"] }
num-rational = { version = "0.4", features = ["serde"] }
num-traits = "0.2"
num-integer = "0.1"
serde = { version = "1", features = ["derive"] }
serde_json = "1"
thiserror = "2"
blake3 = "1.5"
''', encoding="utf-8", newline="\n")
        rust_lines = ["// Generated from solution YAML by ../verify.py; edit the YAML, then rerun.",
                      "#![allow(dead_code, unused_imports)]",
                      '#[path = "../../../../../code/rust/src/linear_algebra/scalars.rs"]',
                      "mod scalars;"]
        for i, solution in enumerate(solutions, 1):
            rust_lines += [f"mod problem_{i:02d} {{", solution["solutions"]["rust"]["code"], "}"]
        rust_lines += ["fn main() {", "let mut outputs = serde_json::Map::new();"]
        for i, solution in enumerate(solutions, 1):
            rust_lines.append(f'outputs.insert("{solution["problem_id"]}".into(), problem_{i:02d}::solve());')
        rust_lines += ['println!("{}", serde_json::to_string_pretty(&outputs).unwrap());', "}"]
        (runner / "src/main.rs").write_text("\n".join(rust_lines) + "\n", encoding="utf-8", newline="\n")
        cargo = shutil.which("cargo")
        if cargo is None:
            raise RuntimeError("cargo was not found on PATH")
        command = [cargo, "run", "--quiet", "--manifest-path", str(manifest)]
        if not args.online:
            command.append("--offline")
        if (runner / "Cargo.lock").exists():
            command.append("--locked")
        rust_stdout, rust_run = run(command, "rust_run.log")
        rust_outputs = json.loads(rust_stdout)
        if set(rust_outputs) != set(expected_ids):
            raise ValueError("Rust output must contain all 25 problems exactly once")
        for solution in solutions:
            ident = solution["problem_id"]
            check_output(ident, "rust", rust_outputs[ident], solution["verification"]["expected_outputs"])
        if rust_outputs != py_outputs:
            raise ValueError("Rust/Python outputs disagree")
        write_json(HERE / "rust_outputs.json", rust_outputs)
        print("Rust: 25/25 solution blocks passed; exact Python parity passed.", flush=True)

        if args.lean:
            lean_exe = shutil.which(args.lean_executable) or args.lean_executable
            _, lean_version = run([lean_exe, "--version"], "lean_version.log", cwd=ROOT / "lean4")
            checks = []
            for path in sorted(lean_sources):
                _, receipt = run([lean_exe, "-j", "1", str(path)], f"lean_{path.stem}.log", cwd=ROOT / "lean4")
                receipt["source"] = path.relative_to(ROOT).as_posix()
                checks.append(receipt)
                print(f"Lean: {path.name} compiled.", flush=True)
            report["lean"] = {"status": "passed", "modules": checks, "version_check": lean_version,
                              "scope": "Recompiled the complete existing source modules containing cited statements. No new Lean proof of the 25 solutions was added."}

        for path, before in source_before.items():
            if digest(path) != before:
                raise RuntimeError(f"Source changed during verification: {path}")
        loaded_python = set()
        for module in tuple(sys.modules.values()):
            name = getattr(module, "__file__", None)
            if name:
                path = Path(name).resolve()
                if path.is_file() and path.is_relative_to(ROOT / "code/python"):
                    loaded_python.add(path)
        all_sources = sources | lean_sources | loaded_python
        versions = {"python": sys.version, "python_executable": sys.executable, "pyyaml": yaml.__version__}
        for executable in ("cargo", "rustc"):
            output, _ = run([executable, "--version"], f"{executable}_version.log")
            versions[executable] = output.strip()
        git = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True)
        report.update(status="passed", completed_utc=datetime.now(timezone.utc).isoformat(),
            problem_count=25, python_solutions_passed=25, rust_solutions_passed=25,
            exact_cross_language_parity=True,
            output_values_per_language=sum(len(x) for x in py_outputs.values()),
            source_symbol_references_checked=True, rust_execution=rust_run, runtime_versions=versions,
            repository_head=git.stdout.strip() if git.returncode == 0 else None,
            source_basis="Current local source bytes, including any pre-existing uncommitted changes. HEAD alone is not the source identity; use the hashes below.",
            source_sha256={p.relative_to(ROOT).as_posix(): digest(p) for p in sorted(all_sources)},
            input_sha256={p.relative_to(ROOT).as_posix(): digest(p) for p in sorted(inputs)},
            generated_sha256={p.relative_to(ROOT).as_posix(): digest(p) for p in [manifest, runner / "Cargo.lock", runner / "src/main.rs", HERE / "python_outputs.json", HERE / "rust_outputs.json"]},
            problems=[{"id": s["problem_id"], "outputs_checked": len(s["verification"]["expected_outputs"]),
                       "computational_scope": s["verification"]["computational_scope"],
                       "lean_reference_count": len(s["lean4"]["references"])} for s in solutions])
        write_json(report_path, report)
        print(f"Verified 25 paired solutions. Receipt: {report_path}", flush=True)
    except Exception as error:
        report.update(status="failed", error=f"{type(error).__name__}: {error}",
                      completed_utc=datetime.now(timezone.utc).isoformat())
        write_json(report_path, report)
        raise


if __name__ == "__main__":
    main()
