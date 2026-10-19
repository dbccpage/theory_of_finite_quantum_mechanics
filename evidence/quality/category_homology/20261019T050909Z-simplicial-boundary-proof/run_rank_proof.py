"""Check and bind the mathematical/refusal model, without exporting OLean files.

The receipt is proof-model evidence, not automatic Rust refinement or a grade.
Uses the repository's already prepared Lean/Mathlib project; never fetches it.
"""

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

from run_audit import ROOT, digest, execute, write_json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model",choices=("rank","category","metadata","degree","counter","parameters","finite-set","literal-reversal","shape-inventory","root-records","homology-protocols","degree-repair","two-step-complex","simplicial-closure","simplicial-boundary"),default="rank")
    model = parser.parse_args().model
    if model == "rank":
        proof_name, import_name, namespace = "RankCertificate", "LinearAlgebra/Matrix/Rank", "TFQM.RankCertificate."
        declarations = ("valid_rank","runChecks_ok_iff","admit_success","admit_success_rank",
            "producer_failure","explicit_failure","failed_predicate","first_error_preserved",
            "row_major_index_lt","pivot_increment_fits","augmented_column_lt","identity_area_le")
        scope = "Exact Q-matrix rank theorem and explicit-refusal model."
    elif model == "category":
        proof_name, import_name, namespace = "FiniteCategory", "CategoryTheory/Category/Basic", "TFQM.FiniteCategory."
        declarations = ("checks_true_iff","admit_preserves_data","admit_success_laws","failed_guard",
            "composite_spec","composeArrow_spec","identity_compose","compose_identity",
            "compose_associative","categoryOfAdmitted")
        scope = "Finite table admission realizes Mathlib Category; explicit guard refusal and data preservation."
    elif model == "metadata":
        proof_name, import_name, namespace = "MetadataValidation", "Data/List/Basic", "TFQM.MetadataValidation."
        declarations = ("success_iff", "failed_head", "valid_head", "first_error_preserved",
                        "inspect_preserves_raw", "failed_check_returns_no_value")
        scope = "Ordered metadata predicates, exact first-error preservation and raw-value observation; no mathematical law certification."
    elif model == "degree":
        proof_name, import_name, namespace = "DegreeWindow", "Data/Int/Basic", "TFQM.DegreeWindow."
        declarations = ("ordered_span_fits_u32", "same_endpoint_zero", "inverted_span_negative")
        scope = "Exact i32 endpoint difference bounds, zero span and inverted-window refusal premise; no category-law claim."
    elif model == "simplicial-boundary":
        proof_name, import_name, namespace = "SimplicialBoundary", "Data/Matrix/Mul", "TFQM.SimplicialBoundary."
        declarations = ("paired_term", "pair_cancellation", "signed_faces_cancel", "mapMatrix_comp", "mapMatrix_identity")
        scope = "Alternating two-face cancellation and exact indicator-matrix composition; concrete list/basis and Rust representation correspondence requires separate review."
    elif model == "simplicial-closure":
        proof_name, import_name, namespace = "SimplicialClosure", "Data/Finset/Card", "TFQM.SimplicialClosure."
        declarations = ("initial_cover", "initial_frontier", "duplicate_cover", "fresh_cover", "duplicate_frontier",
                        "fresh_frontier", "fresh_sound", "finish_contains", "finish_closed", "fresh_card_bound",
                        "duplicate_potential", "fresh_potential", "erase_commute", "erase_preserves_distinct", "erase_preserves_order")
        scope = "Worklist coverage/soundness/closure, cardinality and decreasing work potential, and ordered/distinct face erasure; separate Rust representation review."
    elif model == "two-step-complex":
        proof_name, import_name, namespace = "TwoStepComplex", "Data/Matrix/Mul", "TFQM.TwoStepComplex."
        declarations = ("admission_success_iff", "admission_failure", "admission_preserves", "input_zero_product",
                        "differential_square_zero", "image_is_cycle", "failed_gate", "passed_gate")
        scope = "Two-step exact Q matrix admission, owned data preservation, differential square zero, image-as-cycles and typed guard propagation."
    elif model == "degree-repair":
        proof_name, import_name, namespace = "DegreeRepair", "Data/Int/Basic", "TFQM.DegreeRepair."
        declarations = ("payload_exact", "signed_index", "large_index", "dimension_zero", "dimension_one",
                        "dimension_two", "outside_support", "outside_payload", "scan_append", "scan_parity",
                        "parity_count", "scan_count", "orientation_sign")
        scope = "Exact full-index refusal and finite-support dimension payloads, with Boolean inversion parity and sign; no simplicial homology or rank theorem."
    elif model == "homology-protocols":
        proof_name, import_name, namespace = "HomologyProtocols", "Data/Int/Basic", "TFQM.HomologyProtocols."
        declarations = ("numeric_zero", "numeric_success_iff", "numeric_preserves_payload", "predecessor_success_iff",
                        "successor_success_iff", "predecessor_refusal_iff", "successor_refusal_iff", "degree_drop_inverts")
        scope = "Nonzero numeric identifier payload preservation and exact bounded i32 predecessor/successor refusal and inverse law."
    elif model == "root-records":
        proof_name, import_name, namespace = "RootRecords", "Data/Int/Basic", "TFQM.RootRecords."
        declarations = ("joinable_iff", "foreign_category_refused", "report_empty", "report_valid_head",
                        "report_failed_head", "threshold_iff", "mass_success_iff", "mass_label_first")
        scope = "Literal arrow/category guard, ordered missing-label diagnostics, inventory threshold and nonnegative defined mass; no categorical or model certification."
    elif model == "shape-inventory":
        proof_name, import_name, namespace = "ShapeInventory", "Data/Nat/Basic", "TFQM.ShapeInventory."
        declarations = ("context_shape", "context_law", "context_precondition", "contextual_failure",
                        "context_success_iff", "endomorphism_success_iff", "alignment_success_iff",
                        "members_success_iff", "label_binding_success_iff")
        scope = "Literal endomorphism boundary, optional inventory alignment, conditional label binding and exact typed-error context preservation."
    elif model == "literal-reversal":
        proof_name, import_name, namespace = "LiteralReversal", "Data/List/Basic", "TFQM.LiteralReversal."
        declarations = ("reverse_involution", "list_involution", "length_preserved", "names_and_order_preserved")
        scope = "Literal boundary-triple reversal involution, length, names and list-order preservation; no category-law claim."
    elif model == "finite-set":
        proof_name, import_name, namespace = "FiniteLiteralSet", "Data/Finset/Basic", "TFQM.FiniteLiteralSet."
        declarations = ("scan_success_iff", "first_empty", "first_duplicate", "cardinality_success_iff",
                        "bind_unit_success", "checks_success_iff", "admit_preserves_raw", "admit_invariants")
        scope = "Finite literal-string-set admission, first entry failures, optional cardinality, raw-data preservation and admitted invariants."
    elif model == "parameters":
        proof_name, import_name, namespace = "ParameterMetadata", "Data/Int/Basic", "TFQM.ParameterMetadata."
        declarations = ("signed_success_iff", "optional_level_success_iff", "positive_bound_success_iff",
                        "arity_success_iff", "variance_success_iff", "first_error", "accepted_prefix")
        scope = "Literal metadata threshold/tag admission and ordered typed refusal; no underlying mathematical law claim."
    else:
        proof_name, import_name, namespace = "BoundedCounter", "Data/Nat/Basic", "TFQM.BoundedCounter."
        declarations = ("clip_bound", "guard_exact", "increment_step", "decrement_step",
                        "increment_branch_bound", "separator_bound", "decrement_separator", "short_words_legal")
        scope = "Finite-depth clipping quotient, native guard correspondence, exact event steps and minimal decrement separators."
    project = ROOT/"lean4"
    proof = Path(__file__).resolve().parent/"proofs"/(proof_name+".lean")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")+"-"+model+"-proof"
    output = ROOT/"evidence/quality/category_homology"/stamp
    output.mkdir(parents=True)
    shutil.copyfile(proof,output/proof.name)
    runtime = {}
    for source in (Path(__file__),Path(__file__).parent/"run_audit.py"):
        shutil.copyfile(source,output/source.name)
        runtime[source.name] = digest(output/source.name)
    inputs = {str(proof):digest(proof)}
    mathlib = project/".lake/packages/mathlib"
    imported = mathlib/"Mathlib"/(import_name+".lean")
    inputs[str(imported)] = digest(imported)
    write_json(output/"source_manifest.json",inputs)
    tool = subprocess.run(["elan","which","lean"],cwd=project,text=True,capture_output=True)
    if tool.returncode != 0: raise RuntimeError("Cannot resolve the prepared Lean compiler")
    binary = Path(tool.stdout.strip())
    bootstrap = json.loads(subprocess.check_output(["lake","env",sys.executable,"-c",
        "import json,os; print(json.dumps({key:os.environ.get(key,'') for key in ('LEAN_PATH','LEAN_SRC_PATH')}))"],cwd=project,text=True))
    # Exclude mutable output modules of the user's main theory project. The
    # standalone model uses only the prepared third-party dependency libraries.
    package_dir = (project/".lake/packages").resolve()
    environment = {}
    for key,search_path in bootstrap.items():
        libraries = dict.fromkeys(Path(entry).resolve() for entry in search_path.split(";")
            if entry and Path(entry).resolve().is_relative_to(package_dir))
        if not libraries: raise RuntimeError("No prepared proof dependency path: "+key)
        environment[key] = ";".join(str(path) for path in libraries)
    write_json(output/"environment.json",{"lean_binary":str(binary),"environment":environment,"excluded_main_project_outputs":True})
    common = [str(binary),"--memory=1024","--threads=2","--root="+str(proof.parent)]
    dependencies = execute([*common,"--deps",str(proof)],proof.parent,output/"dependencies.log",timeout=60,environment_overlay=environment)
    sources = execute([*common,"--src-deps",str(proof)],proof.parent,output/"dependency-sources.log",timeout=60,environment_overlay=environment)
    paths = set()
    for log in ("dependencies.log","dependency-sources.log"):
        for line in (output/log).read_text(encoding="utf-8").splitlines():
            candidate = Path(line.strip())
            if not candidate.is_absolute(): candidate = project/candidate
            if candidate.is_file():
                paths.add(candidate.resolve())
                # Lean 4 stores auxiliary private/server data next to OLean.
                for suffix in (".private",".server"):
                    if Path(str(candidate)+suffix).is_file(): paths.add(Path(str(candidate)+suffix))
    dependency_inputs = {str(path):digest(path) for path in sorted(paths)}
    write_json(output/"dependency_manifest.json",dependency_inputs)
    head_before = subprocess.check_output(["git","-C",str(mathlib),"rev-parse","HEAD"],text=True).strip()
    status_before = subprocess.check_output(["git","-C",str(mathlib),"status","--porcelain","--untracked-files=no"],text=True).strip()
    checked = execute([*common,str(proof)],proof.parent,output/"check.log",timeout=300,environment_overlay=environment)
    text = (output/"check.log").read_text(encoding="utf-8")
    warnings = "warning:" in text
    reports = {name:[item.strip() for item in axioms.split(",") if item.strip()]
               for name,axioms in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",text)}
    reports.update({name:[] for name in re.findall(r"'([^']+)' does not depend on any axioms",text)})
    expected = {namespace+name for name in declarations}
    unexpected = sorted({axiom for axioms in reports.values() for axiom in axioms} - {"propext","Classical.choice","Quot.sound"})
    head_after = subprocess.check_output(["git","-C",str(mathlib),"rev-parse","HEAD"],text=True).strip()
    status_after = subprocess.check_output(["git","-C",str(mathlib),"status","--porcelain","--untracked-files=no"],text=True).strip()
    receipt = {
        "AuthorityEffect":"None", "proof_sha256":digest(proof),
        "source_manifest_sha256":digest(output/"source_manifest.json"),
        "dependency_manifest_sha256":digest(output/"dependency_manifest.json"),
        "sources_unchanged":all(Path(path).is_file() and digest(Path(path)) == value for path,value in inputs.items()),
        "direct_dependencies_unchanged":all(Path(path).is_file() and digest(Path(path)) == value for path,value in dependency_inputs.items()),
        "dependency_scope":"Direct import source/OLean roots and Lean 4 private/server data. Transitive sources use the clean pinned Mathlib revision and retained targeted build; not a complete compiler file-read trace.",
        "lean_version":subprocess.check_output([str(binary),"--version"],cwd=proof.parent,text=True).strip(),
        "lean_binary":None if binary is None else {"path":str(binary),"sha256":digest(binary)},
        "mathlib_head":head_after,"mathlib_revision_stable":head_before == head_after,
        "mathlib_tracked_source_clean":not status_before and not status_after,
        "environment_sha256":digest(output/"environment.json"),
        "runner_sha256":digest(Path(__file__)),
        "runtime_snapshots":runtime,
        "runs":[checked,dependencies,sources],
        "check_ok":checked["exit_code"] == 0 and dependencies["exit_code"] == 0 and sources["exit_code"] == 0 and expected == set(reports) and not unexpected and not warnings,
        "diagnostic_warnings_detected":warnings,
        "axiom_reports":reports,"unexpected_axioms":unexpected,
        "unfinished_axiom_detected":"sorryAx" in text,
        "scope":scope+" Rust construction/representation refinement, MIR, allocator totality and crash freedom require separate evidence.",
    }
    write_json(output/"receipt.json",receipt)
    print(json.dumps({"check_ok":receipt["check_ok"],"sources_unchanged":receipt["sources_unchanged"],"unfinished_axiom_detected":receipt["unfinished_axiom_detected"]}))
    print("Receipt:",output)
    return 0 if receipt["check_ok"] and receipt["sources_unchanged"] and receipt["direct_dependencies_unchanged"] and receipt["mathlib_revision_stable"] and receipt["mathlib_tracked_source_clean"] and not receipt["unfinished_axiom_detected"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
