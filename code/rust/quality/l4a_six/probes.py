"""Historical counterexample observations, separate from the quality baseline.

AuthorityEffect: None. Injection affects an owned snapshot only.
"""

from datetime import datetime, timezone
import argparse
import json
from pathlib import Path as _FilesystemPath
import sys as _contract_sys
_contract_sys.path.insert(0, str(_FilesystemPath(__file__).resolve().parents[4] / "scripts"))
from contract_scores import RecordPath as Path, copy_file as _copy_record_file
import shutil
import subprocess
import re

from replay import ROOT, RUST, digest, write, inventory, snapshot, execute, remove_owned, dependency_sources

CONTROLS = r'''
use num_rational::{BigRational, Rational64};
use tfqm_holonomy::{Connection, CellComplex, ConnectionLaplacian, ExactMatrix, Vertex};

fn reproduced(name: &str, operation: impl FnOnce() + std::panic::UnwindSafe) {
    if std::panic::catch_unwind(operation).is_err() {
        println!("DEFECT_CONFIRMED:{name}");
    } else {
        println!("NO_PANIC_OBSERVED:{name}");
    }
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
    use theory_of_finite_qm::linear_algebra::scalars::{GaussianRational, Field, Q, q};
    reproduced("gaussian_scalar_accepts_raw_invalid_rational_until_inverse_panics", || {
        let candidate = GaussianRational::new(Q::new_raw(1.into(), 0.into()), q(0));
        let _ = candidate.map(|value| value.try_inv());
    });
}

#[test]
fn provider_marks_overflowing_i64_as_exact() {
    use theory_of_finite_qm::linear_algebra::scalars::{ExactRing, Semiring};
    fn require_exact<T: ExactRing>() {}
    require_exact::<i64>();
    reproduced("provider_marks_overflowing_i64_as_exact", || {
        let _ = Semiring::add(&i64::MAX, &1);
    });
}

#[test]
fn lggr_undefined_float_is_coerced_to_exact_zero() {
    let value = tfqm_local_green_global_red_lggr::adequacy::float_to_rational(f64::NAN);
    if value.as_ref().is_ok_and(num_traits::Zero::is_zero) {
        println!("DEFECT_CONFIRMED:lggr_undefined_float_is_coerced_to_exact_zero");
    } else {
        println!("COERCION_NOT_REPRODUCED:lggr_undefined_float_is_coerced_to_exact_zero");
    }
}

#[test]
fn smith_sparse_zero_domain_can_panic_on_dense_result_allocation() {
    use theory_of_finite_qm::linear_algebra::smith_form::SparseColMatrix;
    let matrix = SparseColMatrix::new_checked(usize::MAX, 0, vec![]).unwrap();
    reproduced("smith_sparse_zero_domain_can_panic_on_dense_result_allocation", || {
        let _ = matrix.mul_vec(&[]);
    });
}

#[test]
fn boundary_zero_domain_can_panic_on_dense_result_allocation() {
    use theory_of_finite_qm::homology::{boundary::BoundaryMap, chain::Chain, ids::{BasisId, Degree}};
    use theory_of_finite_qm::linear_algebra::{BasicMatrix, Q};
    let matrix = BasicMatrix::<Q>::from_row_major(usize::MAX, 0, vec![]).unwrap();
    let map = BoundaryMap::new(Degree::new(1), Degree::new(0), matrix).unwrap();
    let input = Chain::new(Degree::new(1), BasisId::new("probe").unwrap(), vec![]).unwrap();
    reproduced("boundary_zero_domain_can_panic_on_dense_result_allocation", || { let _ = map.apply(&input); });
}

#[test]
fn coboundary_zero_domain_can_panic_on_dense_result_allocation() {
    use theory_of_finite_qm::homology::{coboundary::CoboundaryMap, cochain::Cochain, ids::{BasisId, Degree}};
    use theory_of_finite_qm::linear_algebra::{BasicMatrix, Q};
    let matrix = BasicMatrix::<Q>::from_row_major(usize::MAX, 0, vec![]).unwrap();
    let map = CoboundaryMap::new(Degree::new(0), Degree::new(1), matrix).unwrap();
    let input = Cochain::new(Degree::new(0), BasisId::new("probe").unwrap(), vec![]).unwrap();
    reproduced("coboundary_zero_domain_can_panic_on_dense_result_allocation", || { let _ = map.apply(&input); });
}
'''

FINDINGS = [
    ("matrix_public_index_panics_on_out_of_bounds", "holonomy/matrix.rs", "G3", "Valid 1x1 matrix; get(1,0) panics instead of returning a typed index refusal."),
    ("matrix_public_fields_bypass_storage_admission", "holonomy/matrix.rs", "G3", "Public rows=cols=1 with empty data; matmul reaches unchecked storage indexing."),
    ("matrix_admits_overflowing_rational64_scalar_arithmetic", "holonomy/matrix.rs", "G2", "Rational64(MAX) multiplied by Rational64(2) in the admitted ExactScalar matrix path overflows."),
    ("connection_accepts_forged_matrix_until_inverse_panics", "holonomy/connection.rs", "G3", "A public-field matrix with missing storage reaches inverse from set_connection and panics."),
    ("laplacian_accepts_forged_vertex_registry_until_lookup_panics", "holonomy/laplacian.rs", "G3", "A public vertex missing from vertex_map reaches an unwrap in compute."),
    ("gaussian_scalar_accepts_raw_invalid_rational_until_inverse_panics", "linear_algebra/scalars.rs", "G3", "GaussianRational::new accepts a raw denominator-zero real part; try_inv panics."),
    ("provider_marks_overflowing_i64_as_exact", "linear_algebra/scalars.rs", ("G2", "G3"), "The publicly reexported provider ExactRing admits i64, while Semiring::add(MAX,1) overflows and panics in the debug replay. The local Gaussian repair does not repair this provider marker/domain contract."),
    ("lggr_undefined_float_is_coerced_to_exact_zero", "local_green_global_red_lggr/adequacy.rs", "G2", "The public float_to_rational helper converts undefined NaN input into the exact rational zero, silently changing an invalid numerical input into mathematical evidence."),
    ("smith_sparse_zero_domain_can_panic_on_dense_result_allocation", "linear_algebra/smith_form.rs", "G3", "SparseColMatrix::new_checked(MAX,0,[]) admits cheap zero-domain metadata, then mul_vec([]) panics on an infallible dense result capacity request. Dense Smith workspace admission does not protect the separate sparse API."),
    ("boundary_zero_domain_can_panic_on_dense_result_allocation", "homology/boundary.rs", "G3", "Capacity probe: admit a canonical (MAX,0) boundary matrix and apply it to a degree-matched empty Chain. Only a caught panic confirms a failure; the current provider uses fallible reservation and the fresh probe observes no panic."),
    ("coboundary_zero_domain_can_panic_on_dense_result_allocation", "homology/coboundary.rs", "G3", "Capacity probe: admit a canonical (MAX,0) coboundary matrix and apply it to a degree-matched empty Cochain. Only a caught panic confirms a failure; the current provider uses fallible reservation and the fresh probe observes no panic."),
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prefix", help="Select one historical prefix. By default observe the Gaussian repair and the provider exact-ring domain; older matrix recipes are now type-excluded.")
    parser.add_argument("--min-free-gib", type=int, choices=(2, 3), default=3)
    args = parser.parse_args()
    prefixes = (args.prefix,) if args.prefix else ("gaussian_scalar", "provider_", "lggr_", "smith_", "boundary_", "coboundary_")
    findings_selected = [f for f in FINDINGS if f[0].startswith(prefixes)]
    if not findings_selected:
        parser.error("No matching controls")
    pieces = re.split(r"(?=\#\[test\]\nfn )", CONTROLS)
    names = {f[0] for f in findings_selected}
    controls = pieces[0] + "".join(piece for piece in pieces[1:]
        if re.match(r"\#\[test\]\nfn (\w+)", piece)[1] in names)
    needs_holonomy = any(f[1].startswith("holonomy/") for f in findings_selected)
    needs_lggr = any(f[1].startswith("local_green_global_red_lggr/") for f in findings_selected)
    if not needs_holonomy:
        controls = controls.replace("use num_rational::{BigRational, Rational64};\n", "")
        controls = controls.replace("use tfqm_holonomy::{Connection, CellComplex, ConnectionLaplacian, ExactMatrix, Vertex};\n", "")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output = ROOT / "evidence/quality/l4a_six" / (stamp + "-defect-controls")
    output.mkdir(parents=True)
    work = RUST / "target/l4a-six" / (stamp + "-defect-controls")
    sources = inventory()
    write(output / "source_manifest.json", sources)
    _copy_record_file(__file__, output / "probes.py")
    _copy_record_file(Path(__file__).with_name("replay.py"), output / "replay.py")
    (output / "expected_panic_controls.rs").write_text(controls, encoding="utf-8")
    receipt = {"AuthorityEffect": "None", "claim": "Counterexample observations distinguish the failure class in each witness: DEFECT_CONFIRMED establishes that witnessed failure, including panic or undefined-input coercion. NO_PANIC_OBSERVED is finite evidence only, not universal crash-freedom or quality certification.",
               "evaluation_timestamp": datetime.now(timezone.utc).isoformat(),
               "source_manifest_sha256": digest(output / "source_manifest.json"),
               "runner_sha256": digest(output / "probes.py"), "helper_sha256": digest(output / "replay.py"),
               "controls_sha256": digest(output / "expected_panic_controls.rs"),
               "selected_controls": sorted(names), "minimum_free_build_bytes": args.min_free_gib * 1024**3,
               "versions": {n: subprocess.check_output([n, "--version"], text=True).strip() for n in ("cargo", "rustc")}}
    print(output, flush=True)
    try:
        snapshot(work)
        manifest = work / "Cargo.toml"
        if needs_holonomy:
            manifest.write_text(manifest.read_text(encoding="utf-8").replace(
                "[dependencies]\n", '[dependencies]\ntfqm_holonomy = { path = "src/holonomy" }\n'), encoding="utf-8")
        if needs_lggr:
            manifest.write_text(manifest.read_text(encoding="utf-8").replace(
                "[dependencies]\n", '[dependencies]\ntfqm_local_green_global_red_lggr = { path = "src/local_green_global_red_lggr" }\n'), encoding="utf-8")
        (work / "tests").mkdir(exist_ok=True)
        (work / "tests/expected_panic_controls.rs").write_text(controls, encoding="utf-8")
        _copy_record_file(manifest, output / "snapshot.Cargo.toml")
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
        if shutil.disk_usage(ROOT).free < args.min_free_gib * 1024**3:
            receipt["run"] = {"started": False, "exit_code": None, "reason": f"Less than {args.min_free_gib} GiB free"}
            return
        run = execute(["cargo", "test", "--offline", "--target-dir", str(work / "build"), "--quiet",
                       "-p", "tfqm_homology_linear_audit", "--test", "expected_panic_controls", "--", "--nocapture", "--test-threads=1"],
                      work, output / "expected_panic_controls.log")
        receipt["run"] = run
        findings = []
        log = (output / "expected_panic_controls.log").read_text(encoding="utf-8")
        for name, source, gate, witness in findings_selected:
            gates = list(gate) if isinstance(gate, tuple) else [gate]
            findings.append({"id": name, "source": "code/rust/src/" + source,
                             "gate": gates[0], "affected_gates": gates, "grade": "E", "witness": witness,
                             "reproduced": f"DEFECT_CONFIRMED:{name}" in log,
                             "observation_kind": "undefined-float-coercion" if name.startswith("lggr_") else "panic-probe",
                             "no_panic_observed": None if name.startswith("lggr_") else f"NO_PANIC_OBSERVED:{name}" in log})
        write(output / "findings.json", findings)
        receipt["findings_sha256"] = digest(output / "findings.json")
        receipt["dependency_sources_unchanged"] = all(Path(p).is_file() and digest(Path(p)) == h
                                                     for p, h in dependencies.items())
        _copy_record_file(work / "Cargo.lock", output / "Cargo.lock")
        print([(f["id"], f["reproduced"]) for f in findings], flush=True)
    finally:
        receipt["sources_unchanged"] = sources == inventory()
        remove_owned(work / "build", work)
        receipt["owned_build_removed"] = True
        write(output / "receipt.json", receipt)


if __name__ == "__main__":
    main()
