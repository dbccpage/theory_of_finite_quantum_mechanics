"""Write/check honest adjacent SCORING v2 YAML records. AuthorityEffect: None.

Unknown gates stay null. Complexity is an upper-bound constraint, never a
semantic correctness result. Capability classifications are conservative and
explicitly separated from the requested architecture/engineering targets.
"""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[4]
RUST = ROOT / "code/rust"


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream,"sha256").hexdigest()


def yaml(value, indent=0):
    """Emit the small YAML subset used here, with JSON-compatible quoted scalars."""
    space = " " * indent
    if isinstance(value, dict):
        lines = []
        for key, item in value.items():
            if isinstance(item, (dict, list)) and item:
                lines.append(f"{space}{key}:\n{yaml(item, indent+2)}")
            else:
                lines.append(f"{space}{key}: {json.dumps(item, ensure_ascii=True)}")
        return "\n".join(lines)
    if isinstance(value, list):
        return "\n".join(f"{space}- {json.dumps(item, ensure_ascii=True)}" for item in value)
    raise TypeError(type(value))


def capability(path, source):
    key = path.relative_to(RUST / "src").as_posix()
    foundational = {
        "homology/rank_certificate.rs": "Exact rank factorization and split-map certificates with a separate identity checker.",
        "homology/carrier.rs": "Immutable cochain carrier admits laws and carries checked rank certificates.",
        "category_theory/finite_category.rs": "Law-checked immutable finite categories with explicit outside-domain lookup results.",
        "category_theory/cat_functor.rs": "Owned admitted endpoints and exhaustive finite functor-law admission.",
        "category_theory/natural_trans.rs": "Immutable natural-transformation certificates own lawful endpoint categories and functors and check every naturality square.",
        "category_theory/natural_trans_composition.rs": "Checked identity, vertical and horizontal composition re-admit natural-transformation certificates and enforce exact shared contexts and interchange.",
        "category_theory/rewriting.rs": "Immutable finite globular admission binds normal-form witnesses and separately checked decreasing-rank termination certificates; derived whiskering re-admits output before commit.",
        "category_theory/higher.rs": "Immutable finite strict 2-category admission owns checked underlying and vertical categories and exhaustively checks horizontal functor, unit, associativity and interchange laws under an admitted work budget.",
    }
    if key == "category_theory/category_contract_alignment.rs":
        return "L1", "Local static contract-label table and its owned copies; no registry or mechanization checking."
    if key == "category_theory/finite_category_builder.rs":
        return "L2", "Fluent raw declarations and a loop-boundary guard; complete law admission delegates to the canonical category certificate constructor."
    if key == "category_theory/eilenberg_moore.rs":
        return "L3", "Concrete Maybe transport and typed finite observations; generic Monad/marker records do not certify universal algebra or category laws."
    if key == "category_theory/lawvere.rs":
        return "L3", "Exact slot admission and finite raw-table diagnostics with borrowed lookup indexing; no admitted Lawvere theory or mathematical Cauchy-completeness certificate."
    if key == "category_theory/condensation.rs":
        return "L2", "Raw named splitting-equation observations and caller-supplied coherence flags with checked metadata updates; no verified higher cells or infinity-Cauchy certificate."
    if key == "category_theory/higher_functor.rs":
        return "L2", "Raw 2-functor map records, signature contracts and supplied boundary/name-membership diagnostics; no admitted higher functor or inverse/coherence certificate."
    if key == "category_theory/functor_composition.rs":
        return "L5", "Immutable finite functor certificates own snapshots after complete endpoint/category/map/law admission; raw derived declarations remain distinct and composition requires exact middle-context equality."
    if key == "category_theory/grothendieck_construction.rs":
        return "L1", "Archival documentation and a wholly commented-out sketch; no active Rust item, algorithm, type or test implementation is delivered by this file."
    if key == "category_theory/dagger.rs":
        return "L5", "Immutable owned finite dagger certificate admits the complete category and total reversed arrow map, involution, identity and every reversed composite before construction; raw declarations remain separate."
    if key == "category_theory/finite_groupoid.rs":
        return "L5", "Immutable owned finite groupoid admits a complete dagger context and both inverse equations for every arrow; connected components and reversible chosen-root isotropy coordinates match the underlying groupoid structure."
    if key in foundational:
        return "L5", foundational[key]
    if "#![cfg(any())]" in source:
        return "L1", "All items are excluded from compilation by cfg(any()); source text does not deliver its advertised algorithms."
    if path.name == "mod.rs" and len(source.splitlines()) < 60:
        return "L1", "Module declarations and re-exports; no independent foundational algorithm."
    if path.name in ("lib.rs", "mod.rs") and path.parent.name == "category_theory":
        return "L2", "Module catalog plus small trait and metadata declarations."
    if key in ("homology/chain.rs", "homology/cochain.rs"):
        return "L1", "Typed alias into the shared admitted graded-vector implementation; tests exercise that implementation."
    if key.endswith("l5a_challenges.rs"):
        return "L3", "Bounded independent mathematical oracles and adversarial admission challenges."
    if "shell" in source.split("#[cfg(test)]")[0].lower() and key != "category_theory/foundations/finite_set.rs":
        return "L2", "Explicit metadata/shape shell; categorical titles do not establish mathematical capabilities."
    if key in ("homology/mod.rs", "homology/exact_carrier.rs", "homology/chain_complex.rs", "homology/cochain_complex.rs", "homology/simplicial.rs"):
        return "L4", "Bounded exact domain implementation with checked constructors and typed failures; shared certificates support it."
    if path.stem in ("errors", "ids", "hashing", "witness", "carrier_manifest", "category_contract_alignment", "validation", "agent_functor", "morphism", "bridges", "density_matrix_functor", "zeta_functor", "mssn_functor_bridge", "simplicial_hott_bridge", "topos_hott_model", "hott_topos_bridge"):
        return "L2", "Structured data, identifiers, hashes, adapters or declarations; no independent foundational theorem is inferred."
    return "L3", "Conservative bounded-domain classification; no upgrade based solely on terminology or module size."


def structure_record(path, functions):
    """Declared source metrics, deliberately separate from expanded execution."""
    ccn = max((f["ccn"] for f in functions), default=0)
    cognitive = max((f["cognitive_upper_bound"] for f in functions), default=0)
    nesting = max((f["control_nesting"] for f in functions), default=0)
    bands = ("A", "B", "C", "D", "E")
    ccn_band = next(i for i, cap in enumerate((10,15,20,50,float("inf"))) if ccn <= cap)
    cognitive_band = next(i for i, cap in enumerate((15,20,25,40,float("inf"))) if cognitive <= cap)
    nesting_band = next(i for i, cap in enumerate((3,4,5,8,float("inf"))) if nesting <= cap)
    return {
        "tool":"syn 3.0.9 source AST", "source_ast_parsed":True, "expanded_ast":False,
        "physical_lines":len(path.read_text(encoding="utf-8").splitlines()),
        "parsed_production_functions":len(functions), "max_production_ccn":ccn,
        "cognitive_complexity_upper_bound":cognitive, "control_nesting":nesting,
        "opaque_function_macros":[{"function":f["name"],"macros":f["opaque_macros"]} for f in functions if f["opaque_macros"]],
        "functions_exceeding_A":[f for f in functions if f["ccn"] > 10 or f["cognitive_upper_bound"] > 15 or f["control_nesting"] > 3],
        "scope":"Explicit source functions only; macro-generated functions, compiler expansion and runtime cost require separate assessment.",
    }, bands[max(ccn_band,cognitive_band,nesting_band)]


def apply_assessment(record, path):
    """Apply an explicit, source-pinned gate review, never an inferred award."""
    assessment = json.loads(path.read_text(encoding="utf-8"))
    if assessment["artifact"] != record["artifact"] or assessment["AuthorityEffect"] != "None":
        raise SystemExit("Assessment subject or authority mismatch: "+str(path))
    grades = ("E","D","C","B","A","A+")
    for gate, value in assessment["gates"].items():
        if gate not in record["gates"] or value not in grades:
            raise SystemExit("Invalid reviewed gate")
        if not assessment["basis"].get(gate):
            raise SystemExit("Missing explicit review basis for "+gate)
        established = record["gates"][gate]
        if established is not None and grades.index(value) > grades.index(established):
            raise SystemExit("A review cannot override an established source-bound failure")
    for evidence in assessment["evidence"]:
        if sha(ROOT/evidence["path"]) != evidence["sha256"]:
            raise SystemExit("Assessment evidence drift")
    for proof in assessment.get("proof_receipts",[]):
        verify_proof_receipt(proof)
    verify_context_inputs(assessment.get("context_inputs",[]))
    if "G5" in assessment["gates"] and grades.index(assessment["gates"]["G5"]) > grades.index(record["grade_ceiling"]):
        raise SystemExit("Gate review exceeds structural ceiling")
    record["gates"].update(assessment["gates"])
    record["evaluation_timestamp"] = assessment["evaluation_timestamp"]
    assessed = [grade for grade in record["gates"].values() if grade is not None]
    record["grade_ceiling"] = min([record["grade_ceiling"],*assessed],key=grades.index)
    record["is_complete"] = all(grade is not None for grade in record["gates"].values())
    record["composite_grade"] = min(assessed,key=grades.index) if record["is_complete"] else None
    record["score_token"] = record["level"]+record["composite_grade"] if record["is_complete"] else None
    if record["is_complete"]:
        required = ("formal_specification","symbol_map","invariant_argument","failure_paths","trust_boundary","consumer_review","assurance_limits","open_findings")
        if any(key not in assessment for key in required):
            raise SystemExit("A completed assessment needs an explicit specification, all-entry-point invariant/failure review and trust/consumer boundaries")
    if "open_findings" in assessment:
        record["open_findings"] = assessment["open_findings"]
    if "assurance_limits" in assessment:
        record["assurance_limits"] = assessment["assurance_limits"]
    record["evidence"].append({"path":path.relative_to(ROOT).as_posix(),"sha256":sha(path),"scope":"Explicit source-pinned gate assessment with invariant and evidence mapping."})


def verify_context_inputs(references):
    """A subject's unchanged bytes cannot conceal changed callees/consumers."""
    for reference in references:
        subject = ROOT/reference["path"]
        if not subject.is_file() or sha(subject) != reference["sha256"]:
            raise SystemExit("Reviewed source context drift: "+reference["path"])


def verify_proof_receipt(reference):
    """Validate model evidence; this never grants a Rust refinement grade."""
    path = ROOT/reference["path"]
    if sha(path) != reference["sha256"]:
        raise SystemExit("Proof receipt altered")
    proof = json.loads(path.read_text())
    for name,value in proof.get("runtime_snapshots",{}).items():
        if sha(path.parent/name) != value:
            raise SystemExit("Proof runtime snapshot altered")
    required = ("check_ok","sources_unchanged","direct_dependencies_unchanged",
                "mathlib_revision_stable","mathlib_tracked_source_clean")
    if not all(proof[key] for key in required) or proof["unexpected_axioms"] or proof["unfinished_axiom_detected"]:
        raise SystemExit("Unsuccessful, drifting or unfinished proof model")
    for name,key in (("source_manifest.json","source_manifest_sha256"),("dependency_manifest.json","dependency_manifest_sha256")):
        manifest = path.parent/name
        if sha(manifest) != proof[key]: raise SystemExit("Proof manifest altered")
        for subject,value in json.loads(manifest.read_text()).items():
            if not Path(subject).is_file() or sha(Path(subject)) != value:
                raise SystemExit("Proof input drift: "+subject)
    for run in proof["runs"]:
        if run["exit_code"] != 0 or sha(ROOT/run["log"]) != run["log_sha256"]:
            raise SystemExit("Proof execution evidence altered or unsuccessful")
        if Path(run["log"]).name == "check.log" and "warning:" in (ROOT/run["log"]).read_text(encoding="utf-8"):
            raise SystemExit("Proof check contains unresolved warnings")
    if sha(ROOT/reference["proof"]) != proof["proof_sha256"]:
        raise SystemExit("Proof source drift")
    if "environment_sha256" in proof:
        if sha(path.parent/"environment.json") != proof["environment_sha256"]:
            raise SystemExit("Proof execution environment altered")
        environment = json.loads((path.parent/"environment.json").read_text())
        if any(any(run["environment"].get(key) != value for key,value in environment["environment"].items()) for run in proof["runs"]):
            raise SystemExit("Proof execution environment mismatch")
    binary = proof["lean_binary"]
    if binary is None or sha(Path(binary["path"])) != binary["sha256"]:
        raise SystemExit("Lean binary unavailable or altered")
    mathlib = ROOT/reference["mathlib_root"]
    head = subprocess.check_output(["git","-C",str(mathlib),"rev-parse","HEAD"],text=True).strip()
    dirty = subprocess.check_output(["git","-C",str(mathlib),"status","--porcelain","--untracked-files=no"],text=True).strip()
    if head != proof["mathlib_head"] or dirty:
        raise SystemExit("Mathlib proof dependency revision/source drift")


def verify_dependencies(receipt, summary):
    if "dependencies_unchanged" not in summary:
        return # Historical receipts explicitly lack dependency-content evidence.
    if not summary["dependencies_unchanged"]:
        raise SystemExit("Dependency contents changed during replay")
    dependency_path = receipt/"dependency_receipt.json"
    if sha(dependency_path) != summary["dependency_receipt_sha256"]:
        raise SystemExit("Dependency receipt digest mismatch")
    dependency = json.loads(dependency_path.read_text())
    checks = {"cargo-metadata.json":"metadata_sha256", "cargo-metadata.stderr.log":"stderr_sha256",
              "dependency_manifest.json":"dependency_manifest_sha256", "run_audit.py":"harness_sha256"}
    for name, key in checks.items():
        if sha(receipt/name) != dependency[key]:
            raise SystemExit("Dependency evidence altered: "+name)
    manifest = json.loads((receipt/"dependency_manifest.json").read_text())
    for path, value in manifest.items():
        if not Path(path).is_file() or sha(Path(path)) != value:
            raise SystemExit("Dependency input drift: "+path)
    for binary in dependency["tool_binaries"].values():
        if sha(Path(binary["path"])) != binary["sha256"]:
            raise SystemExit("Compiler/tool binary drift: "+binary["path"])


def make_record(path, receipt, summary, mutations, metrics, metric_receipt):
    source = path.read_text(encoding="utf-8")
    level, basis = capability(path, source)
    key = path.relative_to(RUST / "src").as_posix()
    structure, grade_ceiling = structure_record(path, metrics[path.relative_to(ROOT).as_posix()])
    local_mutants = [m for m in mutations if m["path"] == key]
    outcomes = {name:sum(m["outcome"] == name for m in local_mutants) for name in ("killed","survived","demonstrably_equivalent","invalid","inconclusive","unrun")}
    eligible = sum(outcomes[k] for k in ("killed","survived","inconclusive","unrun"))
    outcomes["conservative_ratio"] = outcomes["killed"]/eligible if eligible else None
    disabled = "#![cfg(any())]" in source
    gates = {key:None for key in ("G1","G2","G3","G4","G5")}
    if disabled:
        gates["G4"] = "D"
        grade_ceiling = "D" if grade_ceiling in ("A","B","C") else grade_ceiling
    findings = ["A complete five-gate semantic, failure and consumer audit has not been established for this file.",
                "Source AST metrics do not certify macro-generated bodies, compiler expansion, termination or operational bounds.",
                "External path dependency source contents have not received a separate origin/content attestation."]
    if disabled:
        findings.append("Verification mechanism is disabled by cfg(any()); passing package tests do not execute these items.")
    if structure["functions_exceeding_A"]:
        findings.append(f"Declared source metrics impose a conservative {grade_ceiling} ceiling; exceeding functions are listed in structure. Cognitive values are upper bounds, not counterexamples to semantic correctness.")
    timestamp = datetime.strptime(receipt.name,"%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc).isoformat()
    baseline_path = receipt / "baseline.json"
    mutation_path = receipt / "mutations.json"
    description = " ".join(line[3:].strip() for line in source.splitlines() if line.startswith("//!"))
    return {
        "schema_version":"2.0.0",
        "artifact":{"path":path.relative_to(ROOT).as_posix(),"language":"Rust","sha256":sha(path)},
        "profile":"Non-Numeric" if key in ("category_theory/arrow.rs", "category_theory/validation.rs") else "Exact" if key in ("category_theory/abelian/chain_complex_category.rs",
            "category_theory/abelian/exact_category.rs", "category_theory/foundations/hlevel.rs",
            "category_theory/foundations/truncation.rs", "category_theory/foundations/universe.rs",
            "category_theory/functor/diagonal_functor.rs", "category_theory/foundations/finite_set.rs",
            "category_theory/foundations/set.rs", "category_theory/limits_colimits/product.rs",
            "category_theory/limits_colimits/coproduct.rs") else "Non-Numeric" if "shell" in source.split("#[cfg(test)]")[0].lower() else "Exact",
        "level":level,"level_basis":basis,"architecture_target":"L5","engineering_target":"A",
        "gates":gates,"composite_grade":None,"score_token":None,"is_complete":False,
        "grade_ceiling":grade_ceiling,"evaluation_timestamp":timestamp,"AuthorityEffect":"None",
        "claim":{"urn":"urn:tfqm:rust:"+key[:-3].replace("/",":"),"description":description[:1200] or "Declarations and runtime behavior in the bound source.",
                 "scope":"Only the source-bound runtime behavior; no formal theorem, physical derivation or authority promotion is certified."},
        "contract":{"status":"pending","path":None,"note":"Reserved for a later user-requested contract; none created or asserted here."},
        "evidence":[{"path":baseline_path.relative_to(ROOT).as_posix(),"sha256":sha(baseline_path),"scope":"Shared scoped package tests; execution flags, versions, cwd, exits and log hashes are in the receipt."},
                    {"path":(receipt/"summary.json").relative_to(ROOT).as_posix(),"sha256":sha(receipt/"summary.json"),"scope":"Source snapshot binding and complete six-outcome accounting."},
                    {"path":mutation_path.relative_to(ROOT).as_posix(),"sha256":sha(mutation_path),"scope":"Designated critical faults only; outcomes for this file are enumerated below."},
                    {"path":(metric_receipt/"receipt.json").relative_to(ROOT).as_posix(),"sha256":sha(metric_receipt/"receipt.json"),"scope":"Calibrated AST source metrics, tool-source hashes and execution logs; no compiler expansion is inferred."}],
        "verification":{"baseline_ok":summary["baseline_ok"],"source_snapshot_unchanged":summary["source_unchanged"],
                        "compiled_scope":"excluded by cfg(any())" if disabled else "compatibility root not independently built" if key == "category_theory/mod.rs" else summary.get("compiled_scope","shared scoped crate build"),
                        "local_mutant_ids":[m["id"] for m in local_mutants],
                        **({"fault_injection_scope":"Production providers named below are mutated; assessed consumer bodies remain unchanged in each native copy. These are sensitivity challenges of this test artifact, not test-source mutations.",
                            "provider_faults":[{"id":m["id"],"provider":m["provider_fault"],"unchanged_consumer":m["unchanged_consumer"]} for m in local_mutants]}
                           if local_mutants and all("provider_fault" in m and "unchanged_consumer" in m for m in local_mutants) else {})},
        "mutation_accounting":outcomes,
        "structure":structure,
        "open_findings":findings,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt",type=Path,required=True)
    parser.add_argument("--metrics",type=Path,required=True)
    parser.add_argument("--assessment",type=Path,help="Explicit gate review for a single --only artifact; no automatic grade promotion.")
    parser.add_argument("--assessment-map",type=Path,help="JSON map from each selected artifact path to its explicit reviewed assessment; never infers gates.")
    parser.add_argument("--check",action="store_true")
    parser.add_argument("--only",nargs="+",help="Repository-relative Rust paths; update only these source-bound records.")
    args = parser.parse_args()
    if args.assessment and args.assessment_map:
        parser.error("Select either --assessment or --assessment-map")
    receipt = args.receipt.resolve()
    if json.loads((receipt/"summary.json").read_text()).get("primary_eligible", True) is not True:
        raise SystemExit("Auxiliary replay cannot be a primary grading receipt")
    metric_receipt = args.metrics.resolve()
    metric_summary = json.loads((metric_receipt/"receipt.json").read_text())
    metric_sources = json.loads((metric_receipt/"source_manifest.json").read_text())
    if not metric_summary["sources_unchanged"] or metric_summary["source_manifest_sha256"] != sha(metric_receipt/"source_manifest.json"):
        raise SystemExit("AST source receipt drift")
    for run in metric_summary["runs"]:
        if run["exit_code"] != 0 or sha(ROOT/run["log"]) != run["log_sha256"]:
            raise SystemExit("Unsuccessful or stale AST metric execution")
    for key, value in metric_summary["tool_sources"].items():
        if sha(ROOT/key) != value:
            raise SystemExit("AST tool source drift: "+key)
    metrics = json.loads((metric_receipt/"metrics.json").read_text())
    summary = json.loads((receipt/"summary.json").read_text())
    if not summary["baseline_ok"] or not summary["source_unchanged"] or not summary.get("restored_baseline_ok"):
        raise SystemExit("Refusing scores from an unsuccessful or drifting baseline")
    verify_dependencies(receipt,summary)
    inputs = json.loads((receipt/"source_manifest.json").read_text())
    mutations = json.loads((receipt/"mutations.json").read_text())
    if summary["source_manifest_sha256"] != sha(receipt/"source_manifest.json"):
        raise SystemExit("Source manifest digest mismatch")
    baseline = json.loads((receipt/"baseline.json").read_text())
    restored = json.loads((receipt/"restored.json").read_text())
    for run in baseline["runs"] + restored["runs"] + [m["run"] for m in mutations if "run" in m]:
        log = ROOT / run["log"]
        if not log.exists() or sha(log) != run["log_sha256"]:
            raise SystemExit("Missing or altered execution log: "+str(log))
        if not run["command"] or not run["cwd"]:
            raise SystemExit("Incomplete tool execution record")
    if sum(summary["mutation_accounting"].values()) != len(mutations):
        raise SystemExit("Mutation accounting does not balance")
    for outcome, count in summary["mutation_accounting"].items():
        if count != sum(m["outcome"] == outcome for m in mutations):
            raise SystemExit("Mutation outcome mismatch: "+outcome)
    denominator = sum(summary["mutation_accounting"][k] for k in ("killed","survived","inconclusive","unrun"))
    ratio = summary["mutation_accounting"]["killed"]/denominator if denominator else None
    if ratio != summary["conservative_ratio"]:
        raise SystemExit("Conservative mutation ratio mismatch")
    paths = sorted(p for group in ("category_theory","homology") for p in (RUST/"src"/group).rglob("*.rs"))
    if args.only:
        selected = {(ROOT / item).resolve() for item in args.only}
        if not selected.issubset(set(paths)):
            raise SystemExit("--only must name Rust sources in the two assessed directories")
        paths = [path for path in paths if path in selected]
    if summary.get("source_scope", "all") == "category" and any("homology" in path.parts for path in paths):
        raise SystemExit("Category-only execution cannot support homology score records; use --only")
    if summary.get("source_scope", "all") == "homology" and any("category_theory" in path.parts for path in paths):
        raise SystemExit("Homology-only execution cannot support category score records; use --only")
    if "compiled_subjects" in summary and any(path.relative_to(ROOT).as_posix() not in summary["compiled_subjects"] for path in paths):
        raise SystemExit("Selected artifact was not compiled by this scoped receipt")
    if args.assessment and len(paths) != 1:
        raise SystemExit("An explicit gate assessment must select exactly one artifact")
    assessment_map = {}
    if args.assessment_map:
        assessment_map = json.loads(args.assessment_map.read_text(encoding="utf-8"))
        selected_keys = {path.relative_to(ROOT).as_posix() for path in paths}
        if not isinstance(assessment_map,dict) or set(assessment_map) != selected_keys:
            raise SystemExit("Assessment map must cover exactly the selected artifacts")
        if any(not isinstance(value,str) or not (ROOT/value).is_file() for value in assessment_map.values()):
            raise SystemExit("Assessment map references a missing review")
    manifest, failures = {}, []
    for path in paths:
        key = path.relative_to(ROOT).as_posix()
        if inputs.get(key) != sha(path):
            raise SystemExit("Source changed after replay: "+key)
        if metric_sources.get(key) != sha(path) or key not in metrics:
            raise SystemExit("Source changed after AST measurement: "+key)
        record = make_record(path,receipt,summary,mutations,metrics,metric_receipt)
        if "dependencies_unchanged" in summary:
            dependency = receipt/"dependency_receipt.json"
            record["evidence"].append({"path":dependency.relative_to(ROOT).as_posix(),"sha256":sha(dependency),"scope":"Cargo metadata, dependency file content stability, harness and tool-binary binding; no cross-repository origin attestation or compiler-read trace is inferred."})
            record["verification"]["dependency_contents_stable"] = summary["dependencies_unchanged"]
        if args.assessment:
            apply_assessment(record,args.assessment.resolve())
        elif args.assessment_map:
            apply_assessment(record,(ROOT/assessment_map[key]).resolve())
        text = "# SCORING.md v2; incomplete gates deliberately remain null.\n"+yaml(record)+"\n"
        destination = path.with_suffix(".score.yaml")
        if args.check:
            if not destination.exists() or destination.read_text(encoding="utf-8") != text:
                failures.append(str(destination))
        else:
            destination.write_text(text,encoding="utf-8",newline="\n")
        if destination.exists(): manifest[destination.relative_to(ROOT).as_posix()] = sha(destination)
    if failures:
        raise SystemExit("Missing/stale score records:\n"+"\n".join(failures))
    # Keep every historical batch immutable, even when a review changes while
    # the primary source/metrics stay identical. Select by current record bytes.
    score_manifest = metric_receipt / ("score_manifest-"+receipt.name+".json")
    stored = json.loads(score_manifest.read_text()) if score_manifest.exists() else {}
    matches = all(stored.get(key) == value for key,value in manifest.items())
    if score_manifest.exists() and (not matches or (not args.only and manifest != stored)):
        batch = hashlib.sha256(json.dumps(manifest,sort_keys=True).encode("utf-8")).hexdigest()[:16]
        score_manifest = score_manifest.with_name(score_manifest.stem+"-"+batch+".json")
        stored = json.loads(score_manifest.read_text()) if score_manifest.exists() else {}
    if not args.check:
        if score_manifest.exists():
            if any(stored.get(key) != value for key,value in manifest.items()) or (not args.only and manifest != stored):
                raise SystemExit("Refusing to replace a historical score manifest")
        else:
            score_manifest.write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8",newline="\n")
    else:
        if args.only:
            # Selected records may have been refreshed in separate immutable
            # batches. Each current digest must be witnessed in this same
            # primary/metric ledger; do not invent a combined execution batch.
            stem = "score_manifest-"+receipt.name
            batches = [metric_receipt/(stem+".json"),*sorted(metric_receipt.glob(stem+"-*.json"))]
            covered = set()
            for batch in batches:
                if not batch.exists(): continue
                entries = json.loads(batch.read_text(encoding="utf-8"))
                if not isinstance(entries,dict):
                    raise SystemExit("Invalid source-bound score manifest")
                covered.update(key for key,value in manifest.items() if entries.get(key)==value)
            if set(manifest)-covered:
                raise SystemExit("Score manifest mismatch: "+", ".join(sorted(set(manifest)-covered)))
        elif not score_manifest.exists() or manifest != stored:
            raise SystemExit("Score manifest mismatch")
    print(("Verified" if args.check else "Wrote"),len(paths),"adjacent score YAML files")


if __name__ == "__main__":
    main()
