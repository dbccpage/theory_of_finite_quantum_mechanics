"""Offline Rust source/claim challenge, with explicit compile/refusal accounting."""
from datetime import datetime, timezone
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[4]
SOURCE = "code/rust/src/tests/omega_mub/fixture_receipts.rs"
CRATE = "code/rust/quality/fixture_register"
TESTS = CRATE + "/src/validator_tests.rs"
ASSET = "code/rust/src/tests/omega_mub/fixture_receipt_register.json"
MUTANTS = [
    ("register byte quota omitted", "if bytes.len() > MAX_REGISTER_BYTES {", "if false {"),
    ("schema or authority allowed", 'wire.schema != "omega_mub.fixture_receipts.v1" || wire.authority_effect != "None"', 'wire.schema != "omega_mub.fixture_receipts.v1" && wire.authority_effect != "None"'),
    ("empty register admitted", "if wire.fixtures.is_empty() {", "if false {"),
    ("entry quota omitted", "if wire.fixtures.len() > MAX_ENTRIES {", "if false {"),
    ("duplicate projected receipt admitted", "if !paths.insert(relocate(&record.path)) {", "if false && !paths.insert(relocate(&record.path)) {"),
    ("computed evidence kind admitted", 'if record.evidence_kind != "fixture" {', "if false {"),
    ("empty fields admitted", "strings(&record.fields, false)?;", "strings(&record.fields, true)?;"),
    ("empty producer location admitted", "text(producer)?;", "// producer guard omitted"),
    ("literal source locations omitted", "record.kind == Kind::NoProducer", "true"),
    ("text quota omitted", "if value.len() > MAX_TEXT_BYTES {", "if false {"),
    ("list quota omitted", "if values.len() > MAX_LIST_ITEMS {", "if false {"),
    ("blank text admitted", "if value.trim().is_empty() {", "if false {"),
    ("path quota omitted", "if value.len() > MAX_PATH_BYTES {", "if false {"),
    ("path namespace guard omitted", "if value.is_empty() || value.contains(['\\\\', ':', '\\0']) {", "if false {"),
    ("parent components admitted", 'part == ".."', "false"),
    ("device ports admitted", "|| device_port(stem)", "|| false"),
    ("root containment guard omitted", "if !candidate.starts_with(root) {", "if false {"),
    ("directory receipt classification omitted", "if !candidate.is_file() {", "if false {"),
    ("root directory guard omitted", "if !root.is_dir() {", "if false {"),
    ("digest length guard omitted", "value.len() != 64", "false"),
    ("digest alphabet guard omitted", ".all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))", ".all(|_| true)"),
    ("unknown record fields admitted", "#[serde(deny_unknown_fields)]\nstruct Record", "struct Record"),
    ("stream overrun admitted", "if count > limit {", "if false {"),
    ("silently truncated stream", "file.take((limit + 1) as u64)", "file.take(limit as u64)"),
    ("one byte per chunk omitted", "hasher.update(&buffer[..n]);", "hasher.update(&buffer[..n.saturating_sub(1)]);"),
    ("digest mismatch admitted", "if actual != expected {", "if false {"),
    ("per-file quota omitted", "remaining.min(MAX_RECEIPT_BYTES)", "remaining"),
    ("total quota never decreases", "remaining -= result.bytes;", "remaining -= 0;"),
    ("fixture-value existence check omitted", "resolved(root, value)?;", "// value-file check omitted"),
    ("fixture-value unsafe path admitted", "relative_path(value)?;", "// value path guard omitted"),
    ("wrong historical relocation", '"code/rust/src/tests/"', '"code/rust/src/absent-tests/"'),
    ("overlapping traversal guards jointly omitted", 'if part.is_empty() || part == "." || part == ".." || part.ends_with([\'.\', \' \']) {', 'if part.is_empty() || part == "." {'),
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def execute(command, log, expected=None, timeout=240):
    env = {**os.environ, "CARGO_INCREMENTAL": "0", "CARGO_BUILD_JOBS": "2"}
    if expected is not None:
        env["TFQM_EXPECTED_COMPILED_SOURCE"] = str(expected)
    try:
        with log.open("w", encoding="utf-8", newline="\n") as stream:
            process = subprocess.Popen(command, cwd=ROOT, env=env, stdout=stream, stderr=subprocess.STDOUT)
            code = process.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        cleanup = subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"], capture_output=True)
        process.wait(timeout=30)
        if cleanup.returncode:
            raise RuntimeError("Timed-out process tree cleanup not verified; refusing further candidates")
        return {"status": "INCONCLUSIVE", "reason": "process timeout, tree terminated, not a kill", "command": command, "log_sha256": sha(log)}
    text = log.read_text(encoding="utf-8")
    binding = None
    if expected is not None:
        candidates = re.findall(r"COMPILED_SOURCE ([^\r\n]+)", text)
        binding = any(Path(p).is_file() and os.path.samefile(p, expected) for p in candidates)
    if expected is None:
        status = "PASS" if code == 0 else "REVIEW_REQUIRED"
    elif binding and code == 0 and "test result: ok. 14 passed" in text:
        status = "SURVIVED"
    elif binding and code == 101 and "test result: FAILED." in text:
        status = "KILLED"
    elif code == 101 and "could not compile" in text and "test result:" not in text:
        status = "INVALID"
    else:
        status = "INCONCLUSIVE"
    return {"status": status, "command": command, "exit_code": code,
            "candidate_binding": binding, "log_sha256": sha(log)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", action="append")
    args = parser.parse_args()
    selected = [row for row in MUTANTS if not args.only or row[0] in args.only]
    if not selected:
        raise SystemExit("No declared mutation selected")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    work = ROOT / "evidence/quality/expanded_scope" / (stamp + "-rust-fixture-challenge")
    work.mkdir()
    print(work.relative_to(ROOT).as_posix(), flush=True)
    (work / "runner.py").write_bytes(Path(__file__).read_bytes())
    (work / "configuration.json").write_text(json.dumps(selected, indent=2) + "\n", encoding="utf-8")
    source = (ROOT / SOURCE).read_bytes()
    for name, old, new in selected:
        assert source.decode().count(old) == 1, (name, source.decode().count(old))
    compiler = subprocess.check_output(["rustc", "-vV"], text=True)
    (work / "rustc-version.txt").write_text(compiler, encoding="utf-8")
    host = next(line.removeprefix("host: ") for line in compiler.splitlines() if line.startswith("host: "))
    manifest = ROOT / CRATE / "Cargo.toml"
    metadata = subprocess.check_output(["cargo", "metadata", "--offline", "--locked", "--format-version", "1", "--filter-platform", host, "--manifest-path", str(manifest)], cwd=ROOT, text=True)
    (work / "metadata.json").write_text(metadata, encoding="utf-8")
    dependencies = {}
    for package in json.loads(metadata)["packages"]:
        home = Path(package["manifest_path"]).parent
        for path in home.rglob("*"):
            if path.is_file() and path.suffix in (".rs", ".toml", ".lock") and "target" not in path.relative_to(home).parts:
                dependencies[str(path)] = sha(path)
    (work / "dependency-pins.json").write_text(json.dumps(dependencies, indent=2) + "\n", encoding="utf-8")
    inputs = {SOURCE, TESTS, ASSET, "SCORING.md", CRATE + "/Cargo.toml", CRATE + "/Cargo.lock", CRATE + "/src/lib.rs", CRATE + "/src/bin/observe.rs"}
    rules = [("omega_engine/crates_rs/tests/", "code/rust/src/tests/"), ("omega_engine_atlas/coda_atlas/F004_papers/010_mub6/", "papers/core/mub6/"), ("omega_engine/crates_rs/omega_mub/", "code/rust/src/mub/")]
    for record in json.loads((ROOT / ASSET).read_text())["fixtures"]:
        for name in [record["path"], *record.get("fixture_values", [])]:
            for old, new in rules:
                if name.startswith(old):
                    name = new + name[len(old):]
                    break
            inputs.add(name)
    pins = {}
    for name in sorted(inputs):
        path = ROOT / name
        pins[name] = sha(path)
        target = work / "inputs" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(path.read_bytes())
    target = ROOT / "code/rust/target/expanded-fixture-register"
    common = ["--offline", "--locked", "--manifest-path", str(manifest), "--target-dir", str(target)]
    receipt = {"AuthorityEffect": "None", "profile": "Exact", "source": SOURCE, "source_sha256": sha(ROOT / SOURCE), "inputs": pins,
        "compiler_version_sha256": sha(work / "rustc-version.txt"), "dependency_pins_sha256": sha(work / "dependency-pins.json"),
        "scope": "This exact Rust source, registering crate, 14 tests and 20 historical fixture digests only. Compiler/stdlib and non-Rust dependency assets remain trusted/unbound. No other copied tests, MUB theorem or whole-scope score is certified.", "mutants": []}
    baseline = execute(["cargo", "test", *common, "--lib", "--", "--test-threads=1", "--nocapture"], work / "baseline.log", ROOT / SOURCE)
    receipt["baseline"] = baseline
    assert baseline["status"] == "SURVIVED", baseline
    receipt["release"] = execute(["cargo", "test", *common, "--release", "--lib", "--", "--test-threads=1", "--nocapture"], work / "release.log", ROOT / SOURCE)
    receipt["clippy"] = execute(["cargo", "clippy", *common, "--all-targets", "--", "-D", "warnings"], work / "clippy.log")
    mirror = ROOT / ".pytest_cache" / ("fixture-candidates-" + stamp)
    for name in [SOURCE, TESTS, CRATE + "/Cargo.toml", CRATE + "/Cargo.lock", CRATE + "/src/lib.rs"]:
        destination = mirror / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes((ROOT / name).read_bytes())
    candidate = mirror / SOURCE
    candidate_common = ["--offline", "--locked", "--manifest-path", str(mirror / CRATE / "Cargo.toml"), "--target-dir", str(target)]
    receipt["mirror_baseline"] = execute(["cargo", "test", *candidate_common, "--lib", "--", "--test-threads=1", "--nocapture"], work / "mirror-baseline.log", candidate)
    assert receipt["mirror_baseline"]["status"] == "SURVIVED"
    for index, (name, old, new) in enumerate(selected):
        changed = source.decode().replace(old, new, 1).encode()
        snapshot = work / f"mutant-{index:02d}.rs"
        snapshot.write_bytes(changed)
        candidate.write_bytes(changed)
        row = execute(["cargo", "test", *candidate_common, "--lib", "--", "--test-threads=1", "--nocapture"], work / f"mutant-{index:02d}.log", candidate)
        row.update({"name": name, "source_sha256": sha(snapshot)})
        receipt["mutants"].append(row)
        print(json.dumps({"name": name, "status": row["status"]}), flush=True)
    # A deliberately invalid control must never inflate the killed denominator.
    candidate.write_bytes(source + b"\nfn deliberately_invalid( {\n")
    (work / "invalid-control.rs").write_bytes(candidate.read_bytes())
    receipt["invalid_control"] = execute(["cargo", "test", *candidate_common, "--lib"], work / "invalid-control.log", candidate)
    candidate.write_bytes(source)
    receipt["inputs_unchanged"] = all(sha(ROOT / p) == h for p, h in pins.items())
    receipt["dependencies_unchanged"] = all(Path(p).is_file() and sha(Path(p)) == h for p, h in dependencies.items())
    receipt["outcomes"] = {s: sum(row["status"] == s for row in receipt["mutants"]) for s in ["KILLED", "SURVIVED", "INVALID", "INCONCLUSIVE", "UNRUN"]}
    receipt["status"] = "PASS" if (all(row["status"] == "KILLED" for row in receipt["mutants"]) and receipt["invalid_control"]["status"] == "INVALID" and receipt["release"]["status"] == "SURVIVED" and receipt["clippy"]["status"] == "PASS" and receipt["inputs_unchanged"] and receipt["dependencies_unchanged"]) else "REVIEW_OUTCOMES"
    (work / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"path": work.relative_to(ROOT).as_posix(), "status": receipt["status"], "outcomes": receipt["outcomes"]}), flush=True)


if __name__ == "__main__":
    main()
