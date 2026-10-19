"""Replay scoped tests and designated mutations in a source snapshot.

AuthorityEffect: None. This receipt is evidence, not an automatic L5A award.
Requires Python 3.11+, Cargo, and the repository's existing offline dependencies.
No mutation touches the working source tree. Every generated outcome is retained.
"""

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import time
import tomllib


ROOT = Path(__file__).resolve().parents[4]
RUST = ROOT / "code/rust"
TARGETS = ("category_theory", "homology")


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream,"sha256").hexdigest()


def inventory():
    paths = [ROOT / "SCORING.md"]
    for name in TARGETS:
        paths.extend(p for p in (RUST / "src" / name).rglob("*")
                     if p.is_file() and not p.name.endswith(".score.yaml"))
    return {p.relative_to(ROOT).as_posix(): digest(p) for p in sorted(paths)}


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def dependency_inventory(package_roots):
    """Over-approximate package inputs, excluding each package's build tree.

    This binds files, not authorship or a compiler file-read trace. In particular
    an internal src/target directory is source and must NOT be excluded.
    """
    paths = set()
    for base in package_roots:
        for folder, directories, names in os.walk(base):
            directories[:] = [name for name in directories if name != ".git" and
                              not (Path(folder) == base and name == "target")]
            paths.update(Path(folder)/name for name in names)
        for ancestor in [base, *base.parents]:
            for name in ("Cargo.toml","rust-toolchain","rust-toolchain.toml",".cargo/config",".cargo/config.toml"):
                candidate = ancestor/name
                if candidate.is_file(): paths.add(candidate)
    cargo_home = Path(os.environ.get("CARGO_HOME",Path.home()/".cargo"))
    for name in ("config","config.toml"):
        if (cargo_home/name).is_file(): paths.add(cargo_home/name)
    return {str(path.resolve()):digest(path) for path in sorted(paths)}


def bind_dependencies(work, output):
    command = ["cargo","metadata","--offline","--quiet","--format-version","1"]
    started = time.monotonic()
    run = subprocess.run(command,cwd=work,text=True,capture_output=True)
    metadata_path = output/"cargo_metadata.json"
    metadata_path.write_text(run.stdout,encoding="utf-8")
    (output/"cargo_metadata_stderr.log").write_text(run.stderr,encoding="utf-8")
    if run.returncode != 0: raise RuntimeError("Offline dependency metadata failed; see retained stderr")
    metadata = json.loads(run.stdout)
    packages = metadata["packages"]
    roots = sorted({Path(package["manifest_path"]).resolve().parent for package in packages})
    inputs = dependency_inventory(roots)
    write_json(output/"dependency_manifest.json",inputs)
    harness = Path(__file__).resolve()
    shutil.copyfile(harness,output/"run_audit.py")
    tool_binaries = {}
    for name in ("cargo","rustc"):
        located = shutil.which(name)
        if located:
            binary = Path(located)
            tool_binaries[name] = {"path":str(binary),"sha256":digest(binary)}
        if shutil.which("rustup"):
            resolved = subprocess.run(["rustup","which",name],text=True,capture_output=True)
            if resolved.returncode == 0:
                binary = Path(resolved.stdout.strip())
                tool_binaries[name+"_rustup_resolved"] = {"path":str(binary),"sha256":digest(binary)}
    flags = ("RUSTFLAGS","RUSTDOCFLAGS","CARGO_ENCODED_RUSTFLAGS","CARGO_BUILD_TARGET",
             "RUSTC","RUSTC_WRAPPER","RUSTC_WORKSPACE_WRAPPER","RUSTUP_TOOLCHAIN")
    record = {"AuthorityEffect":"None","command":command,"cwd":str(work),"exit_code":run.returncode,
              "elapsed_seconds":round(time.monotonic()-started,3),"metadata_sha256":digest(metadata_path),
              "stderr_sha256":digest(output/"cargo_metadata_stderr.log"),
              "dependency_manifest_sha256":digest(output/"dependency_manifest.json"),
              "harness_sha256":digest(output/"run_audit.py"),"tool_binaries":tool_binaries,
              "rustc_verbose":subprocess.check_output(["rustc","-vV"],text=True).strip(),
              "inherited_compile_environment":{key:os.environ.get(key) for key in flags},
              "package_roots":[str(root) for root in roots],
              "scope":"Cargo metadata and package file content binding; includes unexecuted files. Not origin attestation, exact compiler read tracing or a proof against transient edits."}
    write_json(output/"dependency_receipt.json",record)
    return roots,inputs


def execute(command, cwd, log, timeout=300, environment_overlay=None):
    start = time.monotonic()
    with log.open("w", encoding="utf-8") as stream:
        environment = dict(os.environ, CARGO_INCREMENTAL="0")
        environment.update(environment_overlay or {})
        process = subprocess.Popen(command, cwd=cwd, stdout=stream, stderr=subprocess.STDOUT, env=environment)
        try:
            code = process.wait(timeout=timeout)
            timed_out = False
        except subprocess.TimeoutExpired:
            # Stop the entire compiler/test process tree before restoring a snapshot.
            subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"], capture_output=True)
            process.wait()
            code, timed_out = None, True
    return {"command": command, "cwd": str(cwd), "exit_code": code,
            "timed_out": timed_out, "elapsed_seconds": round(time.monotonic()-start, 3),
            "log": str(log.relative_to(ROOT)), "log_sha256": digest(log),
            "environment":{"CARGO_INCREMENTAL":"0",**(environment_overlay or {})}}


def snapshot(destination, scope="all"):
    destination.mkdir(parents=True)
    if scope == "category":
        shutil.copytree(RUST/"src/category_theory", destination/"src/category_theory", copy_function=shutil.copyfile)
        (destination/"Cargo.toml").write_text('[workspace]\nmembers = ["src/category_theory"]\nresolver = "2"\n[profile.dev]\ndebug = 0\n[profile.test]\ndebug = 0\n',encoding="utf-8")
        return
    groups = ("homology", "linear_algebra") if scope == "homology" else (*TARGETS, "linear_algebra")
    for name in groups:
        shutil.copytree(RUST / "src" / name, destination / "src" / name, copy_function=shutil.copyfile)
    dependencies = tomllib.loads((RUST / "Cargo.toml").read_text())["dependencies"]
    selected = ["num-rational", "num-bigint", "num-traits", "num-integer", "serde",
                "serde_json", "thiserror", "blake3", "hex", "nalgebra", "linear_algebra", "omega_homology"]
    members = '["."]' if scope == "homology" else '[".", "src/category_theory"]'
    lines = ["[workspace]", 'members = '+members, 'resolver = "2"',
             "[package]", 'name = "tfqm_category_homology_audit"', 'version = "0.0.0"',
             'edition = "2021"', "[dependencies]"]
    for name in selected:
        value = dependencies[name]
        if isinstance(value, str):
            encoded = json.dumps(value)
        else:
            encoded = "{ " + ", ".join(f"{k} = {json.dumps(v)}" for k,v in value.items()) + " }"
        lines.append(f"{name} = {encoded}")
    if scope != "homology": lines.append('tfqm_category_theory = { path = "src/category_theory" }')
    lines.extend(["[profile.dev]", "debug = 0", "[profile.test]", "debug = 0",
                  "[profile.release]", "overflow-checks = true"])
    (destination / "Cargo.toml").write_text("\n".join(lines)+"\n", encoding="utf-8")
    (destination / "src/lib.rs").write_text(
        "pub mod linear_algebra;\npub mod homology;\n", encoding="utf-8")


def mutations():
    # (id, module-relative path, literal needle, replacement). Each change is
    # a designated semantic fault; this is not an exhaustive mutation operator set.
    h = "homology/"
    c = "category_theory/"
    return [
        ("H01-basis", h+"graded_vector.rs", "if self.basis_id != other.basis_id {", "if false {"),
        ("H02-degree-hash", h+"hashing.rs", "hasher.update(&degree.to_le_bytes());", "hasher.update(&0i32.to_le_bytes());"),
        ("H03-basis-hash", h+"hashing.rs", "hasher.update(basis.as_bytes());", 'hasher.update(b"fixed");'),
        ("H04-vector-kind", h+"graded_vector.rs", 'const TAG: &\'static [u8] = b"cochain";', 'const TAG: &\'static [u8] = b"chain";'),
        ("H05-down-degree", h+"boundary.rs", "if chain.degree != self.from_degree {", "if false {"),
        ("H06-up-degree", h+"coboundary.rs", "if cochain.degree != self.from_degree {", "if false {"),
        ("H07-provenance", h+"cochain_complex.rs", "if verification_source.trim().is_empty() {", "if false {"),
        ("H08-zero-id", h+"ids.rs", "if id == 0 {", "if false {"),
        ("H09-simplex-order", h+"simplicial.rs", "if pair[1] <= pair[0] {", "if false {"),
        ("H10-orientation", h+"simplicial.rs", "if value.orientation != 1 && value.orientation != -1 {", "if false {"),
        ("H11-LU", h+"rank_certificate.rs", '"LU=I",', '"LU=I-SKIP",'),
        ("H12-VR", h+"rank_certificate.rs", '"VR=I",', '"VR=I-SKIP",'),
        ("H13-MUV", h+"rank_certificate.rs", '"M=UV",', '"M=UV-SKIP",'),
        ("H14-zero-product", h+"exact_scalar.rs", "if !product.as_slice().iter().all(Zero::is_zero) {", "if false {"),
        ("H15-positive-weights", h+"carrier.rs", "if *w <= Q::zero() {", "if false {"),
        ("H16-self-loop", h+"exact_carrier.rs", "if src == tgt {", "if false {"),
        ("H17-raw-rationals", h+"exact_scalar.rs", "admit_coefficients(matrix.as_slice())", "Ok(())"),
        ("H18-rank-output", h+"rank_certificate.rs", "        self.rank\n", "        0\n"),
        ("RK01-LU", h+"rank_certificate.rs", '"LU=I",', '"LU=I-SKIP",'),
        ("RK02-VR", h+"rank_certificate.rs", '"VR=I",', '"VR=I-SKIP",'),
        ("RK03-MUV", h+"rank_certificate.rs", '"M=UV",', '"M=UV-SKIP",'),
        ("RK04-rank-output", h+"rank_certificate.rs", "        self.rank\n", "        0\n"),
        ("RK05-candidate-domain", h+"rank_certificate.rs", "        check_coefficients(matrix, &candidate)?;", ""),
        ("RK06-empty-fast-path", h+"rank_certificate.rs", "if matrix.rows() == 0 || matrix.cols() == 0 {", "if false {"),
        ("RK07-typed-inverse", h+"rank_certificate.rs", ".map_err(|source| HomologicalError::RankInverseFailed { source })", ".map_err(|source| HomologicalError::UnsupportedOperation(source.to_string()))"),
        ("RK09-producer-domain-valid", h+"rank_certificate.rs", "    super::exact_scalar::admit_matrix(matrix)?;\n    if matrix.rows()", "    if matrix.rows()"),
        ("C01-functor-composition", c+"cat_functor.rs", "        candidate.check_compositions()?;", ""),
        ("C02-functor-domain", c+"cat_functor.rs", "        candidate.check_maps()?;", ""),
        ("C03-functor-identity", c+"cat_functor.rs", "        candidate.check_identities()?;", ""),
        ("C04-functor-boundary", c+"cat_functor.rs", "        candidate.check_boundaries()?;", ""),
        ("C05-set-duplicates", c+"foundations/finite_set.rs", "if !seen.insert(e) {", "if false {"),
        ("C08-set-duplicates-valid", c+"foundations/finite_set.rs", "if !seen.insert(e) {", "if seen.insert(e) && false {"),
        ("C06-weight-negatives", c+"finite_profunctor.rs", "if weight.denom() <= &0.into() || weight < BigRational::zero() {", "if false {"),
        ("C07-category-associativity", c+"finite_category_validation.rs", "        check_associativity(category),", "        Vec::new(),"),
        ("FC01-names", c+"finite_category_validation.rs", "        check_nonempty_names(category),", "        Vec::new(),"),
        ("FC02-object-domain", c+"finite_category_validation.rs", "        check_object_references(category),", "        Vec::new(),"),
        ("FC03-identities", c+"finite_category_validation.rs", "        check_identity_totality(category),", "        Vec::new(),"),
        ("FC04-unit-laws", c+"finite_category_validation.rs", "        check_identity_laws(category),", "        Vec::new(),"),
        ("FC05-totality-report", c+"finite_category_validation.rs", "        check_composition_totality(category),", "        Vec::new(),"),
        ("FC06-closure", c+"finite_category_validation.rs", "        check_composition_closure(category),", "        Vec::new(),"),
        ("FC07-boundaries", c+"finite_category_validation.rs", "        check_composition_boundaries(category),", "        Vec::new(),"),
        ("FC08-associativity", c+"finite_category_validation.rs", "        check_associativity(category),", "        Vec::new(),"),
        ("FC09-constructor", c+"finite_category.rs", "if report.all_passed() {", "if true {"),
        ("FC10-id-domain", c+"finite_category.rs", "self.declared.identity_of(x).map(str::to_string)", "self.declared.identity_of(x).or_else(|| self.declared.identities.values().next().map(String::as_str)).map(str::to_string)"),
        ("FC11-boundary-domain", c+"finite_category.rs", ".get(morphism)", ".get(morphism).or_else(|| self.morphisms.values().next())"),
        ("FC12-composition-domain", c+"finite_category.rs", ".get(&(f.into(), g.into()))", ".get(&(f.into(), g.into())).or_else(|| self.compositions.values().next())"),
        ("FC13-table-view", c+"finite_category_validation.rs", "self.rows.get(index).map(|(_, composite)| *composite)", "None"),
        ("NT01-square-equality", c+"natural_trans.rs", "if left != right {", "if false {"),
        ("NT02-component-domain", c+"natural_trans.rs", "if !nat.components.keys().eq(source.objects.iter()) {", "if false {"),
        ("NT03-functor-laws", c+"natural_trans.rs", 'report.add_typed("nat::source_functor", checked_f.typed_violations);', 'report.add_typed("nat::source_functor", Vec::new());'),
        ("NT04-category-laws", c+"functor_composition.rs", 'report.add_typed("functor::source_category", checked_source.typed_violations);', 'report.add_typed("functor::source_category", Vec::new());'),
        ("NT05-functor-domain", c+"functor_composition.rs", "check_mapping_domains(functor, source),", "Vec::new(),"),
        ("NT06-exact-middle", c+"functor_composition.rs", "if first.target() != second.source() {", "if first.target().name != second.source().name {"),
        ("NT07-interchange", c+"natural_trans_composition.rs", "if left != right {", "if false {"),
        ("NT08-horizontal-context", c+"natural_trans_composition.rs", "if alpha.target_category() != beta.source_category() {", "if alpha.target_category().name != beta.source_category().name {"),
        ("NT09-vertical-context", c+"natural_trans_composition.rs", "    check_vertical_context(alpha, beta)?;", ""),
        ("RW01-admission", c+"rewriting.rs", "        validate_records(&sys)?;", ""),
        ("RW02-term-boundary", c+"rewriting.rs", "if cell.source.is_some() || cell.target.is_some() || cell.rule.is_some() {", "if false {"),
        ("RW03-edge-rule", c+"rewriting.rs", "if rule.lhs != source || rule.rhs != target {", "if false {"),
        ("RW04-two-cell-binding", c+"rewriting.rs", "if cell.rule.is_some() || sys.homotopies.get(&cell.name) != Some(&expected) {", "if cell.rule.is_some() {"),
        ("RW05-globular-parallelism", c+"rewriting.rs", "if a.source != b.source || a.target != b.target {", "if false {"),
        ("RW06-rank-domain", c+"rewriting.rs", "if !ranks.keys().eq(terms) {", "if ranks.keys().eq(terms) && false {"),
        ("RW07-rank-descent", c+"rewriting.rs", "if a <= b {", "if false {"),
        ("RW08-inverse-orientation", c+"rewriting.rs", "if inverse {", "if false {"),
        ("RW09-path-composition", c+"rewriting.rs", "if target != next_source {", "if false {"),
        ("RW10-producer-output", c+"rewriting.rs", "let ranks = ForwardGraph::new(self).decreasing_ranks()?;", "let ranks = BTreeMap::new();"),
        ("RW11-orphan-homotopy", c+"rewriting.rs", "    errors.extend(check_homotopies(sys));", ""),
        ("RW12-truncation", c+"rewriting.rs", "if sys.truncation_level != max_level {", "if false {"),
        ("RW13-name-domain", c+"rewriting.rs", "let mut errors = check_names(sys);", "let mut errors = Vec::new();"),
        ("RW14-atomicity", c+"rewriting.rs", "let next = self.whisker_candidate(name, path, homotopy, true)?;", "self.cells.clear();\n        let next = self.whisker_candidate(name, path, homotopy, true)?;"),
        ("RW15-false-join", c+"rewriting.rs", "if !left.is_disjoint(&right) {", "if true {"),
        ("RW16-equal-ranks", c+"rewriting.rs", "if a <= b {", "if a < b {"),
        ("TC01-horizontal-admission", c+"higher.rs", "        candidate.check_horizontal_laws()?;", ""),
        ("TC02-strict-units", c+"higher.rs", "        self.check_horizontal_units()?;", ""),
        ("TC03-associativity", c+"higher.rs", "        self.check_horizontal_associativity()?;", ""),
        ("TC04-identity-functor", c+"higher.rs", "        self.check_horizontal_identities()?;", ""),
        ("TC05-interchange-admission", c+"higher.rs", "        self.check_interchange()?;", ""),
        ("TC06-one-domain", c+"higher.rs", "Ok(self.one(f)?.source.clone())", 'Ok(self.one("e")?.source.clone())'),
        ("TC07-two-domain", c+"higher.rs", "Ok(self.two(a)?.target.clone())", 'Ok(self.two("0")?.target.clone())'),
        ("TC08-composition-domain", c+"higher.rs", ".get(&(a.into(), b.into()))", ".values().next()"),
        ("TC09-vertical-boundary", c+"higher.rs", "if cat.target_2(a)? != cat.source_2(b)? {", "if false {"),
        ("TC10-horizontal-boundary", c+"higher.rs", "if target != source {", "if false {"),
        ("TC11-work-admission", c+"higher.rs", "        check_work_budget(&declared, limit)?;", ""),
        ("TC12-overflow", c+"higher.rs", ".checked_pow(power)", ".checked_pow(1)"),
        ("TC13-budget-boundary", c+"higher.rs", "if needed > limit {", "if needed >= limit {"),
        ("TC14-interchange-equality", c+"higher.rs", "let (left, right) = interchange_values(cat, a, b, c, d)?;", "let (left, _right) = interchange_values(cat, a, b, c, d)?;\n    let right = left.clone();"),
    ]


def clear_debug_outputs(build, work):
    """User policy: discard a completed build's debug/temp artifacts."""
    resolved_build = build.resolve()
    if resolved_build.parent != work.resolve() or resolved_build.name != "target":
        raise RuntimeError("Cleanup target is not this run's build directory")
    for name in ("debug", "tmp"):
        candidate = (resolved_build/name).resolve()
        if candidate.parent != resolved_build or candidate.name != name:
            raise RuntimeError("Cleanup escaped the build directory")
        if candidate.exists():
            shutil.rmtree(candidate)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mutations", action="store_true")
    parser.add_argument("--scope", choices=("all","category","homology"), default="all")
    parser.add_argument("--mutation-prefix", default="")
    args = parser.parse_args()
    if shutil.disk_usage(ROOT).free < 3 * 1024**3:
        raise SystemExit("Audit requires at least 3 GiB free for a fresh isolated build")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output = ROOT / "evidence/quality/category_homology" / stamp
    output.mkdir(parents=True)
    inputs = inventory()
    write_json(output / "source_manifest.json", inputs)
    work = RUST / "target/category-homology-audit" / stamp
    snapshot(work,args.scope)
    dependency_roots, dependency_inputs = bind_dependencies(work,output)
    tools = {name: subprocess.check_output([name,"--version"],text=True).strip() for name in ("cargo","rustc")}
    tools["python"] = subprocess.check_output([__import__("sys").executable,"--version"],text=True).strip()
    records = []
    # Never share crate artifacts across source snapshots: Cargo's mtime-based
    # freshness checks can otherwise reuse a last-mutated binary from another root.
    build = work / "target"
    def test(package, name, challenge=False):
        command = ["cargo","test","--target-dir",str(build),"-p",package,"--lib","--offline","--locked","--quiet"]
        command.append("l5a_challenges" if challenge else ("homology" if package.endswith("audit") else ""))
        try:
            return execute([x for x in command if x], work, output / (name+".log"))
        finally:
            clear_debug_outputs(build, work)
    packages = [] if args.scope == "homology" else [("tfqm_category_theory","category")]
    if args.scope != "category": packages.append(("tfqm_category_homology_audit","homology"))
    baselines = [test(package,name+"-baseline") for package,name in packages]
    write_json(output / "baseline.json", {"tools":tools,"runs":baselines})
    print("baseline exits:",[r["exit_code"] for r in baselines],flush=True)
    if args.mutations:
        records = [{"id":i,"path":p,"outcome":"unrun","needle":a,"replacement":b}
                   for i,p,a,b in mutations() if i.startswith(args.mutation_prefix)
                   and (args.scope == "all" or p.startswith("homology/" if args.scope == "homology" else "category_theory/"))]
        write_json(output / "mutations.json", records)
    baseline_ok = all(r["exit_code"] == 0 for r in baselines)
    for record in records if baseline_ok else []:
        path = work / "src" / record["path"]
        original_bytes = path.read_bytes()
        original = original_bytes.decode("utf-8").replace("\r\n","\n")
        if original.count(record["needle"]) != 1:
            record.update(outcome="invalid",reason="mutation site is not unique")
            write_json(output / "mutations.json",records)
            continue
        mutant = original.replace(record["needle"],record["replacement"],1)
        if record["id"] in ("H11-LU","H12-VR","H13-MUV","RK01-LU","RK02-VR","RK03-MUV"):
            # Remove just the designated identity check, preserving the other two.
            label = record["replacement"].strip('",')
            blocks = [m.group(0) for m in re.finditer(r'        require_equal\([\s\S]*?\n        \)\?;',mutant)]
            matches = [block for block in blocks if '"'+label+'"' in block]
            if len(matches) != 1:
                record.update(outcome="invalid",reason="identity site did not resolve")
                write_json(output / "mutations.json",records)
                continue
            mutant = mutant.replace(matches[0],"",1)
        try:
            path.write_bytes(mutant.encode("utf-8"))
            record["candidate_sha256"] = digest(path)
            package = "tfqm_category_theory" if record["path"].startswith("category_theory/") else "tfqm_category_homology_audit"
            run = test(package,record["id"])
            log = (ROOT / run["log"]).read_text(encoding="utf-8",errors="replace")
            if run["timed_out"]: outcome = "inconclusive"
            elif run["exit_code"] == 0: outcome = "survived"
            elif "test result: FAILED" in log: outcome = "killed"
            elif "could not compile" in log: outcome = "invalid"
            else: outcome = "inconclusive"
            record.update(outcome=outcome,run=run)
            if outcome == "invalid":
                record["reason"] = "Compiler rejected the candidate; its diagnostics are retained in the hashed log. Excluded from eligible semantic faults."
        finally:
            path.write_bytes(original_bytes)
        write_json(output / "mutations.json",records)
        print(record["id"],record["outcome"],flush=True)
    restored = [test(package,name+"-restored") for package,name in packages] if baseline_ok else []
    write_json(output / "restored.json", {"tools":tools,"runs":restored})
    restored_ok = bool(restored) and all(r["exit_code"] == 0 for r in restored)
    # Persist the final ledger even if its last candidate took a continue path,
    # or a failed baseline left every generated candidate unrun.
    write_json(output / "mutations.json",records)
    outcomes = Counter(r["outcome"] for r in records)
    eligible = sum(outcomes[k] for k in ("killed","survived","inconclusive","unrun"))
    final = {"AuthorityEffect":"None", "tools":tools,"baseline_ok":baseline_ok,"restored_baseline_ok":restored_ok,
             "source_manifest_sha256":digest(output / "source_manifest.json"),
             "source_unchanged":inputs == inventory(),"generated":len(records),
             "dependencies_unchanged":dependency_inputs == dependency_inventory(dependency_roots),
             "dependency_receipt_sha256":digest(output/"dependency_receipt.json"),
             "mutation_accounting":{k:outcomes[k] for k in ("killed","survived","demonstrably_equivalent","invalid","inconclusive","unrun")},
             "conservative_ratio":outcomes["killed"]/eligible if eligible else None,
             "all_files_L5A":False,"score_token":None,
             "scope":"Designated critical faults only; no inference of a whole-directory grade.",
             "source_scope":args.scope,"mutation_prefix":args.mutation_prefix}
    write_json(output / "summary.json",final)
    shutil.copy2(work / "Cargo.lock", output / "snapshot_cargo.lock")
    print(json.dumps(final,indent=2),flush=True)
    print("Receipt:",output,flush=True)
    # Only this run's derived binaries are disposable; preserve sources and logs.
    resolved_build, resolved_work = build.resolve(), work.resolve()
    if resolved_build.parent != resolved_work or resolved_build.name != "target" or not resolved_work.is_relative_to((RUST/"target/category-homology-audit").resolve()):
        raise SystemExit("Refusing build cleanup outside the checked audit workspace")
    shutil.rmtree(resolved_build)
    return 0 if baseline_ok and restored_ok and final["source_unchanged"] and final["dependencies_unchanged"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
