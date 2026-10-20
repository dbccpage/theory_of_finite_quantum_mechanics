"""Expected-panic controls: a passing control reproduces a defect, not quality.

AuthorityEffect: None. Injection affects an owned snapshot only.
"""

from datetime import datetime, timezone
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import re

from replay import ROOT, RUST, digest, write, inventory, snapshot, execute, remove_owned, dependency_sources

CONTROLS = r'''
use num_rational::{BigRational, Rational64};
use tfqm_holonomy::{Connection, CellComplex, ConnectionLaplacian, ExactMatrix, Vertex};

fn reproduced(name: &str, operation: impl FnOnce() + std::panic::UnwindSafe) {
    assert!(std::panic::catch_unwind(operation).is_err(), "expected reachable panic was not reproduced");
    println!("DEFECT_CONFIRMED:{name}");
}

#[test]
fn matrix_public_index_panics_on_out_of_bounds() {
    let matrix = ExactMatrix::try_new(1, 1, vec![BigRational::from_integer(1.into())]).unwrap();
    reproduced("matrix_public_index_panics_on_out_of_bounds", || { matrix.get(1, 0); });
}

#[test]
fn matrix_public_fields_bypass_storage_admission() {
    let forged = ExactMatrix::<BigRational> { rows: 1, cols: 1, data: vec![] };
    let identity = ExactMatrix::<BigRational>::try_identity(1).unwrap();
    reproduced("matrix_public_fields_bypass_storage_admission", || { let _ = forged.matmul(&identity); });
}

#[test]
fn matrix_admits_overflowing_rational64_scalar_arithmetic() {
    let left = ExactMatrix::try_new(1, 1, vec![Rational64::from_integer(i64::MAX)]).unwrap();
    let right = ExactMatrix::try_new(1, 1, vec![Rational64::from_integer(2)]).unwrap();
    reproduced("matrix_admits_overflowing_rational64_scalar_arithmetic", || { let _ = left.matmul(&right); });
}

#[test]
fn connection_accepts_forged_matrix_until_inverse_panics() {
    let forged = ExactMatrix::<BigRational> { rows: 1, cols: 1, data: vec![] };
    let mut connection = Connection::new(1, Default::default());
    reproduced("connection_accepts_forged_matrix_until_inverse_panics", move || { let _ = connection.set_connection("u", "v", forged); });
}

#[test]
fn laplacian_accepts_forged_vertex_registry_until_lookup_panics() {
    let mut complex = CellComplex::new(Default::default());
    complex.vertices.push(Vertex { id: "v".into(), index: 0 });
    let connection = Connection::new(1, Default::default());
    reproduced("laplacian_accepts_forged_vertex_registry_until_lookup_panics", || { let _ = ConnectionLaplacian::compute(&complex, &connection, None); });
}

#[test]
fn gaussian_scalar_accepts_raw_invalid_rational_until_inverse_panics() {
    use tfqm_homology_linear_audit::linear_algebra::scalars::{GaussianRational, Field, Q, q};
    let candidate = GaussianRational::new(Q::new_raw(1.into(), 0.into()), q(0));
    reproduced("gaussian_scalar_accepts_raw_invalid_rational_until_inverse_panics", || { let _ = candidate.try_inv(); });
}
'''

FINDINGS = [
    ("matrix_public_index_panics_on_out_of_bounds", "holonomy/matrix.rs", "G3", "Valid 1x1 matrix; get(1,0) panics instead of returning a typed index refusal."),
    ("matrix_public_fields_bypass_storage_admission", "holonomy/matrix.rs", "G3", "Public rows=cols=1 with empty data; matmul reaches unchecked storage indexing."),
    ("matrix_admits_overflowing_rational64_scalar_arithmetic", "holonomy/matrix.rs", "G2", "Rational64(MAX) multiplied by Rational64(2) in the admitted ExactScalar matrix path overflows."),
    ("connection_accepts_forged_matrix_until_inverse_panics", "holonomy/connection.rs", "G3", "A public-field matrix with missing storage reaches inverse from set_connection and panics."),
    ("laplacian_accepts_forged_vertex_registry_until_lookup_panics", "holonomy/laplacian.rs", "G3", "A public vertex missing from vertex_map reaches an unwrap in compute."),
    ("gaussian_scalar_accepts_raw_invalid_rational_until_inverse_panics", "linear_algebra/scalars.rs", "G3", "GaussianRational::new accepts a raw denominator-zero real part; try_inv panics."),
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prefix", help="Run only the named historical defect class; retain the others as historical controls.")
    args = parser.parse_args()
    findings_selected = [f for f in FINDINGS if not args.prefix or f[0].startswith(args.prefix)]
    if not findings_selected:
        parser.error("No matching controls")
    pieces = re.split(r"(?=\#\[test\]\nfn )", CONTROLS)
    names = {f[0] for f in findings_selected}
    controls = pieces[0] + "".join(piece for piece in pieces[1:]
        if re.match(r"\#\[test\]\nfn (\w+)", piece)[1] in names)
    needs_holonomy = any(f[1].startswith("holonomy/") for f in findings_selected)
    if not needs_holonomy:
        controls = controls.replace("use num_rational::{BigRational, Rational64};\n", "")
        controls = controls.replace("use tfqm_holonomy::{Connection, CellComplex, ConnectionLaplacian, ExactMatrix, Vertex};\n", "")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output = ROOT / "evidence/quality/l4a_six" / (stamp + "-defect-controls")
    output.mkdir(parents=True)
    work = RUST / "target/l4a-six" / (stamp + "-defect-controls")
    sources = inventory()
    write(output / "source_manifest.json", sources)
    shutil.copyfile(__file__, output / "probes.py")
    shutil.copyfile(Path(__file__).with_name("replay.py"), output / "replay.py")
    (output / "expected_panic_controls.rs").write_text(controls, encoding="utf-8")
    receipt = {"AuthorityEffect": "None", "claim": "Expected-panic controls establish defects; their passing status is not a quality baseline.",
               "evaluation_timestamp": datetime.now(timezone.utc).isoformat(),
               "source_manifest_sha256": digest(output / "source_manifest.json"),
               "runner_sha256": digest(output / "probes.py"), "helper_sha256": digest(output / "replay.py"),
               "controls_sha256": digest(output / "expected_panic_controls.rs"),
               "selected_controls": sorted(names),
               "versions": {n: subprocess.check_output([n, "--version"], text=True).strip() for n in ("cargo", "rustc")}}
    print(output, flush=True)
    try:
        snapshot(work)
        manifest = work / "Cargo.toml"
        if needs_holonomy:
            manifest.write_text(manifest.read_text(encoding="utf-8").replace(
                "[dependencies]\n", '[dependencies]\ntfqm_holonomy = { path = "src/holonomy" }\n'), encoding="utf-8")
        (work / "tests").mkdir()
        (work / "tests/expected_panic_controls.rs").write_text(controls, encoding="utf-8")
        shutil.copyfile(manifest, output / "snapshot.Cargo.toml")
        command = ["cargo", "metadata", "--offline", "--quiet", "--format-version", "1"]
        meta = subprocess.run(command, cwd=work, text=True, capture_output=True)
        (output / "cargo_metadata.json").write_text(meta.stdout, encoding="utf-8")
        (output / "cargo_metadata_stderr.log").write_text(meta.stderr, encoding="utf-8")
        receipt["metadata_capture"] = {"command": command, "cwd": str(work), "exit_code": meta.returncode,
            "sha256": digest(output / "cargo_metadata.json"), "stderr_sha256": digest(output / "cargo_metadata_stderr.log")}
        if meta.returncode != 0:
            return
        dependencies = dependency_sources(json.loads(meta.stdout))
        write(output / "dependency_sources.json", dependencies)
        receipt["dependency_sources_sha256"] = digest(output / "dependency_sources.json")
        if shutil.disk_usage(ROOT).free < 3 * 1024**3:
            receipt["run"] = {"started": False, "exit_code": None, "reason": "Less than 3 GiB free"}
            return
        run = execute(["cargo", "test", "--offline", "--target-dir", str(work / "build"), "--quiet",
                       "-p", "tfqm_homology_linear_audit", "--test", "expected_panic_controls", "--", "--nocapture", "--test-threads=1"],
                      work, output / "expected_panic_controls.log")
        receipt["run"] = run
        findings = []
        log = (output / "expected_panic_controls.log").read_text(encoding="utf-8")
        for name, source, gate, witness in findings_selected:
            findings.append({"id": name, "source": "code/rust/src/" + source,
                             "gate": gate, "grade": "E", "witness": witness,
                             "reproduced": f"DEFECT_CONFIRMED:{name}" in log})
        write(output / "findings.json", findings)
        receipt["findings_sha256"] = digest(output / "findings.json")
        receipt["dependency_sources_unchanged"] = all(Path(p).is_file() and digest(Path(p)) == h
                                                     for p, h in dependencies.items())
        shutil.copyfile(work / "Cargo.lock", output / "Cargo.lock")
        print([(f["id"], f["reproduced"]) for f in findings], flush=True)
    finally:
        receipt["sources_unchanged"] = sources == inventory()
        remove_owned(work / "build", work)
        receipt["owned_build_removed"] = True
        write(output / "receipt.json", receipt)


if __name__ == "__main__":
    main()
