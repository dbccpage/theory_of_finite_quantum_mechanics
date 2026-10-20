"""Compare refactored code with sealed pre-refactor bodies in an owned snapshot.

AuthorityEffect: None. Differential cases are not counted as a production baseline.
The Smith workspace refusals intentionally have no legacy allocation replay.
"""

from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import subprocess

from replay import ROOT, RUST, digest, write, inventory, snapshot, execute, remove_owned, dependency_sources

ARCHIVE = ROOT / "evidence/quality/l4a_six/20261020-complexity-before"


def section(source, start, end):
    first = source.index(start)
    return source[first:source.index(end, first)]


def instrument(work):
    original_receipt = ROOT / "evidence/quality/l4a_six/20261020T004240Z/source_manifest.json"
    original_inputs = json.loads(original_receipt.read_text(encoding="utf-8"))
    sealed = {}
    for path in ARCHIVE.rglob("*.rs"):
        relative = path.relative_to(ARCHIVE).as_posix()
        if digest(path) != original_inputs["code/rust/src/" + relative]:
            raise RuntimeError("Pre-refactor bytes do not match the historical source manifest")
        sealed[path.relative_to(ROOT).as_posix()] = digest(path)
    old = (ARCHIVE / "linear_algebra/smith_form.rs").read_text(encoding="utf-8")
    legacy = section(old, "fn smith_normal_form_checked_with_iteration_limit(", "\nfn integer_numerator_from_rational64")
    legacy = legacy.replace("smith_normal_form_checked_with_iteration_limit", "legacy_smith")
    legacy = legacy.replace("egcd(", "legacy_egcd(").replace("bigint_identity(", "legacy_identity(")
    identity = section(old, "fn bigint_identity(", "\nfn bigint_abs(").replace("bigint_identity", "legacy_identity")
    euclid = section(old, "fn egcd(", "\npub fn sparse_column_gcd_heuristic").replace("egcd(", "legacy_egcd(")
    path = work / "src/linear_algebra/smith_form.rs"
    text = path.read_text(encoding="utf-8")
    before = "fn smith_normal_form_checked_with_iteration_limit("
    if text.count(before) != 1:
        raise RuntimeError("Smith interception site is not unique")
    text = text.replace(before, "fn replay_modern_smith(", 1)
    text += "\n" + legacy + "\n" + identity + "\n" + euclid
    text += r'''
fn smith_normal_form_checked_with_iteration_limit(matrix:&BasicMatrix<BigInt>,limit:usize)->Result<SmithNormalForm,SmithError> {
    let actual=replay_modern_smith(matrix,limit);
    if matches!(&actual,Err(SmithError::Overflow) | Err(SmithError::Matrix(MatrixError::AllocationLimitExceeded{..}))) {
        println!("DIFF_SMITH_RESOURCE_REFUSED"); return actual;
    }
    let expected=legacy_smith(matrix,limit);
    match (&actual,&expected) {
        (Ok(a),Ok(b))=> { assert_eq!(a.diagonal(),b.diagonal()); assert_eq!(a.diagonal_matrix(),b.diagonal_matrix()); assert_eq!(a.u(),b.u()); assert_eq!(a.v(),b.v()); },
        (Err(a),Err(b))=>assert_eq!(a,b),
        _=>panic!("Smith result kind differs from legacy"),
    }
    println!("DIFF_SMITH_COMPARED"); actual
}
'''
    # The default library test command compiles only the test form of this file.
    path.write_text(text, encoding="utf-8")
    old = (ARCHIVE / "local_green_global_red_lggr/adequacy.rs").read_text(encoding="utf-8")
    legacy = section(old, "fn exact_structural_failures(", "\nfn evidence_unresolved_reason(")
    legacy = legacy.replace("fn exact_structural_failures(", "fn legacy_structural_failures(", 1)
    path = work / "src/local_green_global_red_lggr/adequacy.rs"
    text = path.read_text(encoding="utf-8").replace("fn exact_structural_failures(", "fn replay_modern_structural_failures(", 1)
    text += "\n" + legacy
    text += r'''
fn exact_structural_failures(declaration:&DetectorDeploymentDeclaration,records:&[CompositionRecord],ledger:&TraceLedger,boundary:&BoundarySlice)->Vec<DetectorStructuralFailure> {
    let actual=replay_modern_structural_failures(declaration,records,ledger,boundary);
    let expected=legacy_structural_failures(declaration,records,ledger,boundary);
    assert_eq!(actual,expected); println!("DIFF_ADEQUACY_COMPARED"); actual
}
'''
    path.write_text(text, encoding="utf-8")
    old = (ARCHIVE / "linear_algebra/quintic_split.rs").read_text(encoding="utf-8")
    legacy = section(old, "pub fn validate_quintic_degree(", "\npub fn evaluate_request(")
    legacy = legacy.replace("pub fn validate_quintic_degree(", "fn legacy_validate_quintic(", 1)
    path = work / "src/linear_algebra/quintic_split.rs"
    text = path.read_text(encoding="utf-8").replace("pub fn validate_quintic_degree(", "pub fn replay_modern_validate_quintic(", 1)
    text += "\n" + legacy
    text += r'''
pub fn validate_quintic_degree(conductor:&Value,coefficients:&Value,certificate:&Value)->Result<()> {
    let actual=replay_modern_validate_quintic(conductor,coefficients,certificate);
    let expected=legacy_validate_quintic(conductor,coefficients,certificate);
    assert_eq!(actual,expected); println!("DIFF_QUINTIC_COMPARED"); actual
}
'''
    path.write_text(text, encoding="utf-8")
    return sealed, {p.relative_to(work).as_posix(): digest(p) for p in (
        work / "src/linear_algebra/smith_form.rs", work / "src/linear_algebra/quintic_split.rs",
        work / "src/local_green_global_red_lggr/adequacy.rs")}


def main():
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output = ROOT / "evidence/quality/l4a_six" / (stamp + "-differential")
    output.mkdir(parents=True)
    work = RUST / "target/l4a-six" / (stamp + "-differential")
    sources = inventory()
    write(output / "source_manifest.json", sources)
    shutil.copyfile(__file__, output / "differential.py")
    shutil.copyfile(Path(__file__).with_name("replay.py"), output / "replay.py")
    receipt = {"AuthorityEffect": "None", "claim": "Instrumented snapshot compares legacy and current outcomes on exercised cases only; not a production baseline or whole-file proof.",
               "source_manifest_sha256": digest(output / "source_manifest.json"),
               "runner_sha256": digest(output / "differential.py"), "helper_sha256": digest(output / "replay.py"), "runs": [],
               "versions": {n: subprocess.check_output([n, "--version"], text=True).strip() for n in ("cargo", "rustc")}}
    print(output, flush=True)
    try:
        snapshot(work)
        sealed, instrumented = instrument(work)
        receipt.update(sealed_legacy_sources=sealed, instrumented_sources=instrumented)
        command = ["cargo", "metadata", "--offline", "--quiet", "--format-version", "1"]
        meta = subprocess.run(command, cwd=work, text=True, capture_output=True)
        (output / "metadata.json").write_text(meta.stdout, encoding="utf-8")
        (output / "metadata_stderr.log").write_text(meta.stderr, encoding="utf-8")
        receipt["metadata"] = {"command": command, "cwd": str(work), "exit_code": meta.returncode,
                               "sha256": digest(output / "metadata.json"), "stderr_sha256": digest(output / "metadata_stderr.log")}
        if meta.returncode != 0:
            return
        dependencies = dependency_sources(json.loads(meta.stdout))
        write(output / "dependency_sources.json", dependencies)
        receipt["dependency_sources_sha256"] = digest(output / "dependency_sources.json")
        for package in ("tfqm_homology_linear_audit", "tfqm_local_green_global_red_lggr"):
            if shutil.disk_usage(ROOT).free < 3 * 1024**3:
                receipt["runs"].append({"started": False, "reason": "Less than 3 GiB free"}); break
            receipt["runs"].append(execute(["cargo", "test", "--offline", "--quiet", "--target-dir", str(work / "build"),
                                           "-p", package, "--lib", "--", "--nocapture"], work, output / (package + ".log")))
        receipt["dependency_sources_unchanged"] = all(Path(p).is_file() and digest(Path(p)) == h for p, h in dependencies.items())
        log = "\n".join((ROOT / r["log"]).read_text(encoding="utf-8") for r in receipt["runs"] if "log" in r)
        receipt["observations"] = {name: log.count(name) for name in (
            "DIFF_SMITH_COMPARED", "DIFF_SMITH_RESOURCE_REFUSED", "DIFF_ADEQUACY_COMPARED", "DIFF_QUINTIC_COMPARED")}
    finally:
        receipt["sources_unchanged"] = sources == inventory()
        remove_owned(work / "build", work)
        receipt["owned_build_removed"] = True
        write(output / "receipt.json", receipt)
        print(receipt.get("observations"), flush=True)


if __name__ == "__main__":
    main()
