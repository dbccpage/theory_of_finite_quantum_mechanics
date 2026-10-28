"""Designated semantic challenges in an owned source snapshot across the six QM/math directories; all outcomes retained.

AuthorityEffect: None. Does not certify unchallenged symbols or failure classes.
"""

import argparse
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path as _FilesystemPath
import sys as _contract_sys
_contract_sys.path.insert(0, str(_FilesystemPath(__file__).resolve().parents[4] / "scripts"))
from contract_scores import RecordPath as Path, copy_file as _copy_record_file
import shutil
import subprocess

from replay import (
    ROOT,
    RUST,
    digest,
    write,
    inventory,
    snapshot,
    execute,
    remove_owned,
    dependency_sources,
)


def candidates():
    recipes = [
        (
            "MAJ01-holonomy-flat",
            "majorana/holonomy.rs",
            "let flat = residual_weight == 0;",
            "let flat = residual_weight != 0;",
        ),
        (
            "MAJ02-repair-closed",
            "majorana/repair_limit.rs",
            "s.iter().all(|&v| v == 0)",
            "s.iter().all(|&v| v == 1)",
        ),
        (
            "MAJ03-classify-exact",
            "majorana/classify.rs",
            "if is_exact {\n        return (Terminal::Exact",
            "if !is_exact {\n        return (Terminal::Exact",
        ),
        (
            "MAJ04-braid-bijection",
            "majorana/braid_action.rs",
            "if !visited[start] && trace_cycle_length(start, &images, &mut visited) % 2 == 0 {",
            "if !visited[start] && trace_cycle_length(start, &images, &mut visited) % 2 != 0 {",
        ),
        (
            "MAJ05-pauli-noise-self-coupling",
            "majorana/pauli_noise.rs",
            "if a == b {\n                return Err(NoiseError::SelfCoupling { mode: *a });\n            }",
            "if a != b {\n                return Err(NoiseError::SelfCoupling { mode: *a });\n            }",
        ),
        (
            "MAJ06-complexes-boundary",
            "majorana/complexes.rs",
            "d1_data[fi][e_top] ^= 1;",
            "d1_data[fi][e_top] ^= 0;",
        ),
        (
            "MAJ07-gf2-terminalizer-closed",
            "majorana/gf2_terminalizer.rs",
            "let is_closed = d1_syndrome.iter().all(|&v| v == 0);",
            "let is_closed = d1_syndrome.iter().all(|&v| v == 1);",
        ),
        (
            "MUB01-overlap-check",
            "mub/lib.rs",
            "if expected_overlap != Ratio::new(1, 6) {",
            "if expected_overlap == Ratio::new(1, 6) {",
        ),
        (
            "MUB02-fourier-cross-ratio",
            "mub/native/mub6_fourier_landing_verifier.rs",
            "if computed_cr != target_cross_ratio {",
            "if computed_cr == target_cross_ratio {",
        ),
        (
            "MUB03-atlas-cover",
            "mub/native/global_atlas.rs",
            "let patch_for_every_class = certificate.patches.len() == certificate.class_count;",
            "let patch_for_every_class = certificate.patches.len() != certificate.class_count;",
        ),
        (
            "MUB04-basis-gluing-gate",
            "mub/native/basis_gluing_gate.rs",
            "let has_wall_patches =\n        inputs.accepted_patch_count > 0 && inputs.wall_transport_for_every_class;",
            "let has_wall_patches =\n        inputs.accepted_patch_count == 0 && inputs.wall_transport_for_every_class;",
        ),
        (
            "MUB05-d10-wall-status",
            "mub/native/d10_wall_status.rs",
            "if unitary + antiunitary > 0 {",
            "if unitary + antiunitary == 0 {",
        ),
        (
            "MUB06-d6-curvature-mu",
            "mub/native/d6_exact_curvature_cochain.rs",
            "if columns.len() != COLUMN_COUNT {",
            "if columns.len() == COLUMN_COUNT {",
        ),
        (
            "MUB07-d6-sos-pivot-sign",
            "mub/native/d6_exact_sos.rs",
            "if real_sign_cyc24(&pivot) != 1 {",
            "if real_sign_cyc24(&pivot) == 1 {",
        ),
        (
            "NT01-binary-field-add",
            "number_theory/binary_field.rs",
            "(left ^ right) & self.mask",
            "(left | right) & self.mask",
        ),
        (
            "NT02-binary-field-mul",
            "number_theory/binary_field.rs",
            "if right & 1 == 1 {",
            "if right & 1 == 0 {",
        ),
        (
            "NT03-cyclotomic-sign",
            "number_theory/cyclotomic_ordered.rs",
            "if !number.is_real() {\n        return Err(CyclotomicOrderError::NotReal);\n    }",
            "if number.is_real() {\n        return Err(CyclotomicOrderError::NotReal);\n    }",
        ),
        (
            "NT04-algebraic-real-width",
            "number_theory/algebraic_real.rs",
            "if !width.is_positive() {",
            "if width.is_positive() {",
        ),
        (
            "NT05-circle-haar-refinement",
            "number_theory/circle_haar.rs",
            "if !m.is_multiple_of(n) {\n        return Err(CircleHaarError::Refinement);\n    }",
            "if m.is_multiple_of(n) {\n        return Err(CircleHaarError::Refinement);\n    }",
        ),
        (
            "NT06-certified-angles-neg-radicand",
            "number_theory/certified_angles.rs",
            "if q < &Q::zero() {\n        return Err(AngleError::NegativeRadicand);\n    }",
            "if q > &Q::zero() {\n        return Err(AngleError::NegativeRadicand);\n    }",
        ),
        (
            "NT07-four-squares-verify",
            "number_theory/four_squares.rs",
            "if &sum == n {",
            "if &sum != n {",
        ),
        (
            "OP01-authority-ceiling",
            "operad_theory/kernel/model.rs",
            "if input.authority_effect.rank() > input.authority_ceiling.rank() {",
            "if input.authority_effect.rank() < input.authority_ceiling.rank() {",
        ),
        (
            "OP02-antibody-killed",
            "operad_theory/kernel/model.rs",
            "if screen.killed {",
            "if !screen.killed {",
        ),
        (
            "OP03-event-operand-receipts",
            "operad_theory/kernel/trace.rs",
            "if !seen_receipts.contains(&operand.admission_receipt_ref) {",
            "if seen_receipts.contains(&operand.admission_receipt_ref) {",
        ),
        (
            "OP04-canonical-digest",
            "operad_theory/kernel/canonical.rs",
            "if !is_digest(&normalized) {",
            "if is_digest(&normalized) {",
        ),
        (
            "OP05-observer-same-id",
            "operad_theory/kernel/observer.rs",
            "Ok(self.observer_id()? == other.observer_id()?)",
            "Ok(self.observer_id()? != other.observer_id()?)",
        ),
        (
            "OP06-capability-entry-over-entry",
            "operad_theory/kernel/capability.rs",
            "if check_entry_over_entry(&normalized.tree) {",
            "if !check_entry_over_entry(&normalized.tree) {",
        ),
        (
            "OP07-terms-slot-range",
            "operad_theory/kernel/terms.rs",
            "if slot >= outer_inputs.len() {",
            "if slot < outer_inputs.len() {",
        ),
        (
            "SH01-cech-cocycle",
            "sheaf_theory/cech.rs",
            "if !is_cocycle(&d1, &values).map_err(|e| e.to_string())? {",
            "if is_cocycle(&d1, &values).map_err(|e| e.to_string())? {",
        ),
        (
            "SH02-cech-coboundary",
            "sheaf_theory/cech.rs",
            "let is_trivial = is_coboundary(&d0, &values).map_err(|e| e.to_string())?;",
            "let is_trivial = !is_coboundary(&d0, &values).map_err(|e| e.to_string())?;",
        ),
        (
            "SH03-sheaf-compatible-family",
            "sheaf_theory/sheaf.rs",
            "if is_compatible_family(presheaf, cover, &fam) {",
            "if !is_compatible_family(presheaf, cover, &fam) {",
        ),
        (
            "SH04-presheaf-subset",
            "sheaf_theory/presheaf.rs",
            "if !v.is_subset(u) {",
            "if v.is_subset(u) {",
        ),
        (
            "SH05-epistemic-row-shape",
            "sheaf_theory/epistemic_observer.rs",
            "if seen[row.context][k] {",
            "if !seen[row.context][k] {",
        ),
        (
            "SH06-finite-report-gluing-incompat",
            "sheaf_theory/finite_report_gluing.rs",
            "if let Some(incompat) = Self::find_incompatibility(locals) {\n            return incompat;\n        }",
            "if let None = Self::find_incompatibility(locals) {\n            return FunctionGlueDecision::UniqueFunctionGlue { global: BTreeMap::new(), containing_context: BTreeMap::new() };\n        }",
        ),
        (
            "SH07-empirical-lp-verify",
            "sheaf_theory/empirical_presheaf/lp.rs",
            "if verify_l1_defect_receipt(generators, target, &receipt) {",
            "if !verify_l1_defect_receipt(generators, target, &receipt) {",
        ),
        (
            "QM01-clifton-kent-minor",
            "qm/campaigns/mub_reports.rs",
            "Ok(minor.as_rational().is_some_and(|r| r < r_zero_val))",
            "Ok(minor.as_rational().is_some_and(|r| r > r_zero_val))",
        ),
        (
            "QM02-clifton-kent-persists",
            "qm/campaigns/mub_reports.rs",
            "let persists = non_psd_count == total && purity_all_four && trace_all_one;",
            "let persists = non_psd_count != total && purity_all_four && trace_all_one;",
        ),
        (
            "QM03-textbook-atlas-verified",
            "qm/textbook_problems.rs",
            "let all_65_verified =\n        all_textbook_problems_verified && all_atlas_questions_verified(&questions);",
            "let all_65_verified =\n        !all_textbook_problems_verified && all_atlas_questions_verified(&questions);",
        ),
        (
            "QM04-born-normalization-trace",
            "qm/campaigns/born_normalization.rs",
            "let trace: BigRational = weights.iter().sum();\n    if trace != BigRational::one() {",
            "let trace: BigRational = weights.iter().sum();\n    if trace == BigRational::one() {",
        ),
        (
            "QM05-cancellations-unpairable",
            "qm/campaigns/cancellations.rs",
            "let is_unpairable = !info.all_minimal_sums_pairable;",
            "let is_unpairable = info.all_minimal_sums_pairable;",
        ),
        (
            "QM06-bridge-division-by-zero",
            "qm/bridge.rs",
            "ScalarError::DivisionByZero => (\"scalar division\", \"division by zero\"),",
            "ScalarError::DivisionByZero => (\"scalar division\", \"mutated division by zero\"),",
        ),
        (
            "QM07-report-fiber-stage",
            "qm/report_fiber.rs",
            "let c2 = usize::from(stage == 8);",
            "let c2 = usize::from(stage != 8);",
        ),
        (
            "QM08-simplicial-grav-angular",
            "qm/simplicial_grav.rs",
            "Ok(mx::is_zero_matrix(&j_sum)?)",
            "Ok(!mx::is_zero_matrix(&j_sum)?)",
        ),
    ]
    pkg_map = {
        "majorana": "tfqm_majorana",
        "mub": "tfqm_mub",
        "number_theory": "tfqm_number_theory",
        "operad_theory": "tfqm_operad_theory",
        "sheaf_theory": "tfqm_sheaf_theory",
        "qm": "tfqm_qm_audit",
    }
    result = []
    for identity, source, before, after in recipes:
        package = pkg_map[source.split("/")[0]]
        result.append(
            {
                "id": identity,
                "source": "code/rust/src/" + source,
                "snapshot_source": "src/" + source,
                "before": before,
                "after": after,
                "package": package,
                "outcome": "unrun",
            }
        )
    return result


def classify(run):
    if run["timed_out"]:
        return "inconclusive", "Cargo deadline expired; no kill is inferred."
    if run["exit_code"] == 0:
        return "survived", "Selected suite passed."
    log = (ROOT / run["log"]).read_text(encoding="utf-8")
    if any(text in log.lower() for text in ["not enough space", "no space left", "os error 112"]):
        return "inconclusive", "Resource exhaustion does not establish a semantic kill or an invalid recipe."
    if "could not compile" in log or "error[E" in log:
        return "invalid", "Compiler rejected candidate; excluded from eligible denominator."
    if "test result: FAILED" in log:
        return "killed", "Rust test harness reported an assertion/test failure."
    return "inconclusive", "Unsuccessful process without decisive compiler or assertion attribution."


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prefix")
    parser.add_argument("--release", action="store_true", help="Run the same designated faults with optimized overflow-checked snapshot profiles")
    args = parser.parse_args()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output = ROOT / "evidence/quality/l4a_qm_six" / (stamp + "-mutations")
    output.mkdir(parents=True)
    work_root = RUST / "target/l4a-qm-six" / (stamp + "-mutations")
    work = work_root / "code/rust"
    sources = inventory()
    write(output / "source_manifest.json", sources)
    _copy_record_file(__file__, output / "mutations.py")
    _copy_record_file(Path(__file__).with_name("replay.py"), output / "replay.py")
    entries = [c for c in candidates() if not args.prefix or c["id"].startswith(args.prefix)]
    write(output / "mutations.json", entries)
    receipt = {
        "AuthorityEffect": "None",
        "evaluation_timestamp": datetime.now(timezone.utc).isoformat(),
        "versions": {
            n: subprocess.check_output([n, "--version"], text=True).strip()
            for n in ("cargo", "rustc")
        },
        "source_manifest_sha256": digest(output / "source_manifest.json"),
        "runner_sha256": digest(output / "mutations.py"),
        "execution_helper_sha256": digest(output / "replay.py"),
        "baselines": [],
        "restored_baselines": [],
        "build_cache_disposals": [],
        "scope": "Designated semantic faults only; no whole-file or system score is inferred.",
    }
    print(output, flush=True)
    try:
        snapshot(work)
        command = ["cargo", "metadata", "--offline", "--quiet", "--format-version", "1"]
        meta = subprocess.run(command, cwd=work, text=True, capture_output=True)
        (output / "cargo_metadata.json").write_text(meta.stdout, encoding="utf-8", newline="\n")
        (output / "cargo_metadata_stderr.log").write_text(meta.stderr, encoding="utf-8", newline="\n")
        receipt["metadata_capture"] = {
            "command": command,
            "cwd": str(work),
            "exit_code": meta.returncode,
            "sha256": digest(output / "cargo_metadata.json"),
            "stderr_sha256": digest(output / "cargo_metadata_stderr.log"),
        }
        if meta.returncode != 0:
            return
        dependencies = dependency_sources(json.loads(meta.stdout))
        write(output / "dependency_sources.json", dependencies)
        receipt["dependency_sources_sha256"] = digest(output / "dependency_sources.json")
        packages = sorted({c["package"] for c in entries})
        common = ["--offline", "--target-dir", str(work_root / "build"), "--quiet"]
        if args.release:
            common.append("--release")

        def run_package(package, log, test_filter=None):
            if shutil.disk_usage(ROOT).free < 3500 * 1024**2:
                remove_owned(work_root / "build", work_root)
                receipt["build_cache_disposals"].append(
                    {
                        "before_log": log.name,
                        "reason": "Completed owned Cargo cache removed to recover 3 GiB headroom.",
                    }
                )
            if shutil.disk_usage(ROOT).free < 3 * 1024**3:
                return {"started": False, "exit_code": None, "reason": "Less than 3 GiB free"}
            cmd = ["cargo", "test", *common, "-p", package, "--lib"]
            if test_filter:
                cmd.append(test_filter)
            if package == "tfqm_mub":
                cmd.extend(
                    [
                        "--",
                        "--skip",
                        "deep_run::tests",
                        "--skip",
                        "base_mu_phase_stabilizer_on_step2_root_of_unity_grid",
                        "--skip",
                        "char_two_parametric_gate::tests",
                        "--skip",
                        "full_second_basepoint_campaign_usable_and_open",
                        "--skip",
                        "test_solve_continuous_manifold_residue_smoke",
                    ]
                )
            return execute(cmd, work, log)

        filter_by_source = {
            "src/majorana/holonomy.rs": "holonomy",
            "src/majorana/repair_limit.rs": "repair_limit",
            "src/majorana/classify.rs": "classify",
            "src/majorana/braid_action.rs": "braid_action",
            "src/majorana/pauli_noise.rs": "pauli_noise",
            "src/majorana/complexes.rs": "complexes::tests",
            "src/majorana/gf2_terminalizer.rs": "gf2_terminalizer::tests",
            "src/mub/lib.rs": "crate_tests",
            "src/mub/native/mub6_fourier_landing_verifier.rs": "mub6_fourier_landing_verifier",
            "src/mub/native/global_atlas.rs": "exact::global_atlas::tests",
            "src/mub/native/basis_gluing_gate.rs": "exact::basis_gluing_gate::tests",
            "src/mub/native/d10_wall_status.rs": "float_check::d10_wall_status::tests",
            "src/mub/native/d6_exact_curvature_cochain.rs": "exact::d6_exact_curvature_cochain::tests",
            "src/mub/native/d6_exact_sos.rs": "exact::d6_exact_sos::tests",
            "src/number_theory/binary_field.rs": "binary_field",
            "src/number_theory/cyclotomic_ordered.rs": "cyclotomic_ordered",
            "src/number_theory/algebraic_real.rs": "algebraic_real",
            "src/number_theory/circle_haar.rs": "circle_haar",
            "src/number_theory/certified_angles.rs": "certified_angles::tests",
            "src/number_theory/four_squares.rs": "four_squares::tests",
            "src/operad_theory/kernel/model.rs": "kernel::model",
            "src/operad_theory/kernel/trace.rs": "kernel::trace",
            "src/operad_theory/kernel/canonical.rs": "kernel::canonical",
            "src/operad_theory/kernel/observer.rs": "kernel::observer",
            "src/operad_theory/kernel/capability.rs": "kernel::capability::tests",
            "src/operad_theory/kernel/terms.rs": "kernel::terms::tests",
            "src/sheaf_theory/cech.rs": "cech",
            "src/sheaf_theory/sheaf.rs": "sheaf::",
            "src/sheaf_theory/presheaf.rs": "presheaf::tests",
            "src/sheaf_theory/epistemic_observer.rs": "epistemic_observer",
            "src/sheaf_theory/finite_report_gluing.rs": "finite_report_gluing::tests",
            "src/sheaf_theory/empirical_presheaf/lp.rs": "empirical_presheaf::lp::tests",
            "src/qm/campaigns/mub_reports.rs": "mub_reports",
            "src/qm/textbook_problems.rs": "textbook_problems",
            "src/qm/campaigns/born_normalization.rs": "born_normalization",
            "src/qm/campaigns/cancellations.rs": "cancellations",
            "src/qm/bridge.rs": "qm::bridge::tests",
            "src/qm/report_fiber.rs": "qm::report_fiber::tests",
            "src/qm/simplicial_grav.rs": "qm::simplicial_grav::tests",
        }

        for package in packages:
            baseline = run_package(package, output / (package + "-baseline.log"))
            receipt["baselines"].append({"package": package, **baseline})
            print("baseline", package, baseline["exit_code"], flush=True)
            pkg_entries = [e for e in entries if e["package"] == package]
            if baseline["exit_code"] != 0:
                for entry in pkg_entries:
                    entry["reason"] = "Baseline unavailable or unsuccessful."
                continue
            for entry in pkg_entries:
                path = work / entry["snapshot_source"]
                original = path.read_bytes()
                try:
                    source = original.decode("utf-8")
                    if source.count(entry["before"]) != 1:
                        entry.update(
                            outcome="invalid", reason="Recipe must match exactly one source site."
                        )
                        continue
                    path.write_bytes(
                        source.replace(entry["before"], entry["after"], 1).encode("utf-8")
                    )
                    entry["candidate_sha256"] = digest(path)
                    run = run_package(
                        entry["package"],
                        output / (entry["id"] + ".log"),
                        filter_by_source.get(entry["snapshot_source"]),
                    )
                    entry["run"] = run
                    entry["outcome"], entry["reason"] = classify(run)
                    print(entry["id"], entry["outcome"], run["elapsed_seconds"], flush=True)
                finally:
                    path.write_bytes(original)
                    entry["restored_sha256"] = digest(path)
            restored = run_package(package, output / (package + "-restored.log"))
            receipt["restored_baselines"].append({"package": package, **restored})
            print("restored", package, restored["exit_code"], flush=True)
        receipt["dependency_sources_unchanged"] = all(
            Path(p).is_file() and digest(Path(p)) == h for p, h in dependencies.items()
        )
        if (work / "Cargo.lock").is_file():
            _copy_record_file(work / "Cargo.lock", output / "Cargo.lock")
        _copy_record_file(work / "Cargo.toml", output / "snapshot.Cargo.toml")
    finally:
        write(output / "mutations.json", entries)
        counts = Counter(e["outcome"] for e in entries)
        for name in (
            "killed",
            "survived",
            "demonstrably_equivalent",
            "invalid",
            "inconclusive",
            "unrun",
        ):
            counts.setdefault(name, 0)
        denominator = sum(counts[n] for n in ("killed", "survived", "inconclusive", "unrun"))
        receipt.update(
            accounting=dict(counts),
            conservative_ratio=counts["killed"] / denominator if denominator else None,
            mutations_sha256=digest(output / "mutations.json"),
            sources_unchanged=sources == inventory(),
            snapshot_sources={
                str(p.relative_to(work)): digest(p)
                for p in work.rglob("*.rs")
                if p.is_file()
            },
        )
        remove_owned(work_root / "build", work_root)
        if work_root.exists():
            shutil.rmtree(work_root)
        receipt["owned_builds_removed"] = True
        write(output / "mutation_receipt.json", receipt)


if __name__ == "__main__":
    main()
