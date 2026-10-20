"""Write/check source-bound assessment and contract sidecars, without auto-awarding A.

JSON documents are used as YAML 1.2. Public declarations are a lexical index,
not an AST coverage or semantic correctness claim. Python 3.11+.
"""

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys
import tomllib

from replay import ROOT, RUST, GROUPS, CHALLENGES, COMPOSITION_SOURCES, digest, subjects


PURPOSES = {
    "holonomy": "Finite graph connections, exact matrix transport, loop holonomy and gauge calculations.",
    "homology": "Finite rational chain/cochain data, admitted carriers and rank certificates.",
    "homotopy_type_theory": "Finite presentation/reference records and their explicit validators; executable finite checks only.",
    "lie_theory": "Finite exact matrix/group/algebra constructions over the scalar domains admitted by each API.",
    "linear_algebra": "Exact matrix, elimination, polynomial and finite algebraic calculations with explicit domain/resource refusals.",
    "local_green_global_red_lggr": "Finite local/global residual, composition, soundness and continuation evidence checks.",
}
SPECS_PATH = Path(__file__).with_name("specs.json")


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def ref(path):
    return {"path": path.relative_to(ROOT).as_posix(), "sha256": digest(path)}


def declaration_index(source):
    """Only a line index; excludes neither cfg branches nor macro-generated items."""
    pattern = re.compile(r"^\s*pub(?:\([^)]*\))?\s+(?:(?:const|async|unsafe)\s+)?"
                         r"(fn|struct|enum|trait|type|const|mod)\s+([A-Za-z_]\w*)")
    result = []
    for number, line in enumerate(source.splitlines(), 1):
        match = pattern.match(line)
        if match:
            result.append({"kind": match[1], "name": match[2], "line": number,
                           "declaration_line": line.strip()})
    return result


def metric_ceiling(functions):
    def band(value, limits):
        return next((grade for upper, grade in limits if value <= upper), "E")
    order = ["E", "D", "C", "B", "A"]
    grade = "A"
    exceeding = []
    for item in functions:
        grades = [band(item["ccn"], [(10, "A"), (15, "B"), (20, "C"), (50, "D")]),
                  band(item["cognitive_upper_bound"], [(15, "A"), (20, "B"), (25, "C"), (40, "D")]),
                  band(item["control_nesting"], [(3, "A"), (4, "B"), (5, "C"), (8, "D")])]
        lowest = min(grades, key=order.index)
        grade = min((grade, lowest), key=order.index)
        if lowest != "A":
            exceeding.append({**item, "metric_ceiling": lowest})
    return grade, exceeding


def package_runs_pass(runs, packages):
    """Require one successful run per relevant package, including restoration.

    An empty or truncated restored-baseline list is missing evidence, never a
    vacuously successful restoration. Duplicate runs are ambiguous custody.
    """
    selected = [run for run in runs if run["package"] in packages]
    return (bool(packages) and Counter(run["package"] for run in selected)
            == Counter({package: 1 for package in packages})
            and all(run.get("exit_code") == 0 and not run.get("timed_out") for run in selected))


def select_challenges(entries, relative, links):
    """Explicit composition evidence may support a test harness and its subject.

    This selects evidence, not a grade. Each linked fault needs a source and a
    claim in the source-pinned specification. Missing links withhold G4.
    """
    if any(not link.get("source") or not link.get("claim") for link in links.values()):
        raise RuntimeError("A linked challenge needs an explicit source and claim")
    present = {entry["id"]: entry["source"] for entry in entries}
    complete = all(present.get(identity) == link["source"] for identity, link in links.items())
    selected = [entry for entry in entries if entry["source"] == relative
                or (entry["id"] in links and entry["source"] == links[entry["id"]]["source"])]
    return selected, complete


def apply_individual_engineering_review(scoring, specification):
    """Apply a source-pinned review, retaining failures and unmet prerequisites.

    Gate judgements are explicit reviewer inputs. Execution and a mutation
    fraction can refuse a judgement, but can never manufacture an A grade.
    """
    review = specification.get("engineering_assessment") if specification else None
    if not review:
        return
    if review["source_sha256"] != scoring["artifact"]["sha256"]:
        raise RuntimeError("Stale engineering review: " + scoring["artifact"]["path"])
    grades = ["E", "D", "C", "B", "A", "A+"]
    decisions = review["gates"]
    if set(decisions) != set(scoring["gates"]):
        raise RuntimeError("Engineering review must disclose all five gates")
    scoring["engineering_review"] = review
    for gate, decision in decisions.items():
        grade = decision["grade"]
        if grade is not None and grade not in grades:
            raise RuntimeError("Unknown engineering grade")
        if not decision.get("basis"):
            raise RuntimeError("Missing engineering judgement basis")
        if scoring["gates"][gate] == "E":
            continue
        if gate == "G4" and grade in ("C", "B", "A", "A+"):
            ratio = scoring["mutation_accounting"]["conservative_ratio"]
            baseline = scoring["verification"]["baseline"]
            required = {"C": .70, "B": .85, "A": .95, "A+": 1.0}.get(grade, 0)
            if (not baseline or baseline.get("exit_code") != 0 or ratio is None
                    or ratio < required
                    or not scoring["verification"].get("designated_challenges_present", True)
                    or not scoring["verification"].get("mutation_restoration_baselines_ok")):
                scoring["open_findings"].append("Individual G4 judgement withheld: execution or mutation prerequisite unmet.")
                continue
            if grade in ("A", "A+") and not scoring["verification"].get("designated_critical_faults_decisive"):
                scoring["open_findings"].append("Individual G4 A judgement withheld: a designated critical fault lacks decisive detection.")
                continue
        if gate == "G5" and grade is not None:
            ceiling = scoring["structure"]["metric_ceiling"]
            if ceiling is None or grades.index(grade) > grades.index(ceiling):
                raise RuntimeError("Engineering G5 exceeds measured structural ceiling")
        scoring["gates"][gate] = grade
    known = [g for g in scoring["gates"].values() if g is not None]
    complete = len(known) == 5
    scoring["is_complete"] = complete
    if complete or "E" in known:
        grade = min(known, key=grades.index)
        scoring["composite_grade"] = grade
        scoring["score_token"] = scoring["level"] + grade
    if known:
        lowest = min(known, key=grades.index)
        scoring["grade_ceiling"] = min((lowest, scoring["grade_ceiling"]), key=grades.index)
        scoring["grade_ceiling_basis"] = "Minimum of explicit individual gate decisions and measured structural eligibility."
    resolved_prefixes = []
    if scoring["gates"]["G1"] is not None:
        resolved_prefixes.append("Complete source-to-requirement")
    if all(scoring["gates"][gate] is not None for gate in ("G2", "G3")):
        resolved_prefixes.append("Domain admission, construction/deserialization")
    if scoring["gates"]["G4"] is not None:
        resolved_prefixes.append("Fresh baseline execution alone")
    # Contract and score share this list; update it in place before binding the
    # contract digest so neither document retains a resolved generic finding.
    scoring["open_findings"][:] = [item for item in scoring["open_findings"]
        if not any(item.startswith(prefix) for prefix in resolved_prefixes)]
    scoring["open_findings"].extend(specification.get("open_obligations", []))


def record_for(path, receipt_path, receipt, metrics, mutation_path=None, baseline_extras=(), defect_controls=(), compositions=(), differentials=()):
    relative = path.relative_to(ROOT).as_posix()
    group = path.relative_to(RUST / "src").parts[0]
    source = path.read_text(encoding="utf-8")
    disabled = source.lstrip().startswith("#![cfg(any())]")
    test_only = path.name in ("l5a_challenges.rs", "test_support.rs", "tests.rs") or "tests" in path.relative_to(RUST / "src").parts
    artifact = {"path": relative, "sha256": digest(path),
                "language": "Rust" if path.suffix == ".rs" else "Other"}
    specification = read(SPECS_PATH)["files"].get(path.relative_to(RUST / "src").as_posix())
    index = declaration_index(source) if path.suffix == ".rs" else []
    functions = metrics.get(relative)
    ceiling, exceeding = metric_ceiling(functions or [])
    profile = "Non-Numeric" if group == "homotopy_type_theory" or path.name == "Cargo.toml" else "Exact"
    if specification and "profile" in specification:
        profile = specification["profile"]
    if disabled:
        level, basis = "L1", "The entire file is disabled by cfg(any()); its mathematical declarations deliver no default runtime capability."
    elif path.name == "Cargo.toml":
        level, basis = "L1", "Build manifest; dependency and library target declarations."
    elif path.stem == "mod" or (path.stem == "lib" and not functions):
        level, basis = "L1", "Module/export facade; composition evidence does not raise this file's own capability."
    elif group == "homotopy_type_theory" and path.stem in (
            "unit_type", "empty_type", "sum_type", "pi_type", "sigma_type", "contractible_type"):
        level, basis = "L2", "Reference-record validation; mathematical terminology does not establish a type theory implementation."
    else:
        level, basis = "L3", "Provisional bounded-domain classification; requires individual capability review before promotion."
    capability = specification.get("capability_assessment") if specification else None
    if capability:
        if capability["source_sha256"] != artifact["sha256"]:
            raise RuntimeError("Stale individual capability review: " + relative)
        level, basis = capability["level"], capability["basis"]
    failures = ["Complete source-to-requirement and downstream consumer review is outstanding.",
                "Domain admission, construction/deserialization paths, panic freedom and dependency trust require individual review.",
                "Fresh baseline execution alone does not establish independent challenge or mutation adequacy."]
    if disabled:
        failures.append("The entire file is disabled by cfg(any()); its declarations and tests are not compiled by the package baseline.")
    if test_only:
        failures.append("Test/support artifact: source metrics below must not be interpreted as production execution complexity.")
    if functions is None and path.suffix == ".rs":
        failures.append("No fresh calibrated structural measurement for this file.")
    if exceeding:
        failures.append("One or more source functions exceed an A structural ceiling; see structure.exceeding_A.")
    if path.name == "mod.rs" and group in ("holonomy", "homotopy_type_theory", "lie_theory", "local_green_global_red_lggr"):
        failures.append("Compatibility module is outside its package lib.rs build target; its own compilation needs separate evidence.")
    contract_path = Path(str(path) + ".contract.yaml")
    evidence = [ref(receipt_path), ref(receipt_path.parent / "source_manifest.json")]
    evidence.extend([ref(Path(__file__)), ref(SPECS_PATH)])
    if specification:
        historical = [*specification.get("origin_and_staged_evidence", []),
            *specification.get("repaired_historical_findings", {}).get("controls", [])]
        for reference in historical:
            if digest(ROOT / reference["path"]) != reference["sha256"]:
                raise RuntimeError("Changed reviewed historical evidence: " + reference["path"])
            evidence.append(reference)
    evidence.extend(ref(extra_path) for extra_path, _ in baseline_extras)
    evidence.extend(ref(control_path) for control_path, _ in defect_controls)
    evidence.extend(ref(control_path.parent / "INTERPRETATION.md") for control_path, _ in defect_controls
                    if (control_path.parent / "INTERPRETATION.md").is_file())
    evidence.extend(ref(composition_path) for composition_path, _ in compositions)
    evidence.extend(ref(p) for p, _ in differentials)
    metric_path = receipt_path.parent / "metrics.json"
    if functions is not None:
        evidence.append(ref(metric_path))
    runs = receipt["runs"]
    package = {"holonomy": "tfqm_holonomy", "homotopy_type_theory": "tfqm_homotopy_type_theory",
               "lie_theory": "tfqm_lie_theory", "local_green_global_red_lggr": "tfqm_local_green_global_red_lggr",
               "linear_algebra": "tfqm_homology_linear_audit", "homology": "tfqm_homology_linear_audit"}[group]
    baseline = next((r for r in runs if "-p" in r.get("command", [])
                     and package in r["command"]), None)
    if baseline is None:
        baseline = next((run for _, extra in baseline_extras for run in extra["runs"]
                         if "-p" in run.get("command", []) and package in run["command"]), None)
    # A designated campaign already executes the untouched package before any
    # injection. Reuse that exact source-bound run rather than rebuilding it.
    if baseline is None and mutation_path:
        campaign = read(mutation_path)
        baseline = next((run for run in campaign["baselines"] if run["package"] == package), None)
    # The current designated campaign may contain additional package-local
    # integration fixtures. Prefer its complete untouched baseline when present.
    if mutation_path:
        campaign = read(mutation_path)
        candidate_baseline = next((run for run in campaign["baselines"]
                                   if run["package"] == package and run.get("exit_code") == 0), None)
        if candidate_baseline is not None:
            baseline = candidate_baseline
    doctests = [run for run in runs if "--doc" in run.get("command", []) and package in run["command"]]
    if baseline and not any(flag in baseline.get("command", []) for flag in ("--doc", "--lib", "--tests", "--test")):
        # A default Cargo test baseline already executes doctests. Do not count
        # a second historical doc run as additional independent cases.
        doctests = []
    contract = {"schema_version": "1.0.0", "AuthorityEffect": "None", "artifact": artifact,
                "contract_urn": "urn:tfqm:contract:" + relative.removeprefix("code/rust/src/").replace("/", ":"),
                "status": "draft_requires_semantic_review", "target": "L4A", "profile": profile,
                "purpose": PURPOSES[group],
                "subject_role": basis,
                "compilation": {"disabled_by_cfg_any": disabled, "test_or_support_file": test_only},
                "declaration_index": index,
                "declaration_index_scope": "Lexical line index only; signatures may span lines, include test/cfg items and omit macros/reexports.",
                "requirements": [
                    {"id": "G1", "requirement": "Bind this source digest, declared symbols, actual claims, dependencies and consumer boundaries."},
                    {"id": "G2", "requirement": "Admit all public input domains; preserve exact arithmetic and declared algebraic laws on each successful path."},
                    {"id": "G3", "requirement": "Enumerate typed refusals and preserve state/invariants on every failure; justify all indexing and scalar preconditions."},
                    {"id": "G4", "requirement": "Challenge each declared critical failure class using an independent basis; retain all six mutation outcomes and require R >= 0.95 for A."},
                    {"id": "G5", "requirement": "Meet CCN <= 10, cognitive upper bound <= 15 and nesting <= 3; audit allocations and operational bounds separately."}],
                "admission_policy": "Records with public fields or Deserialize are untrusted candidates until the specific validator admits them; a validator's name is not proof of completeness.",
                "resource_boundary": "No process-OOM, bit-complexity, timeout or global memory guarantee is inferred from element/work counters.",
                "authority_ceiling": "Runtime finite checks only. No formal theorem, physical derivation or authority promotion is certified.",
                "open_obligations": failures,
                "evidence": evidence}
    if path.name == "Cargo.toml":
        manifest = tomllib.loads(source)
        contract["manifest"] = {key: manifest.get(key, {}) for key in ("package", "lib", "dependencies", "dev-dependencies")}
        contract["admission_policy"] = "Cargo resolves declared dependencies; absolute external path dependencies require independent source custody and portability review."
    if group == "homotopy_type_theory":
        contract["authority_ceiling"] = "Names and reference validators do not verify HoTT axioms, inhabitance, univalence or higher coherence. Only explicit finite algorithms are assessed."
    if specification:
        contract["reviewed_specification"] = specification
        contract["status"] = specification["status"]
    scoring = {"schema_version": "2.0.0", "AuthorityEffect": "None", "artifact": artifact,
               "profile": profile, "level": level, "level_basis": basis,
               "engineering_target": "A", "requested_target": "L4A",
               "gates": {"G1": None, "G2": None, "G3": None, "G4": None, "G5": None},
               "composite_grade": None, "score_token": None, "is_complete": False,
               "grade_ceiling": ceiling, "evaluation_timestamp": datetime.strptime(receipt_path.parent.name, "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc).isoformat(),
               "grade_ceiling_basis": "Conservative source-metric eligibility ceiling; cognitive values are upper bounds, not demonstrated semantic failures.",
               "contract": {"path": contract_path.relative_to(ROOT).as_posix(), "status": contract["status"]},
               "evidence": evidence,
               "verification": {"baseline": baseline, "sources_unchanged": receipt["sources_unchanged"],
                                "doctests": doctests,
                                "composition_runs": [{"receipt": ref(p), "claim": c["claim"], "run": c["run"]} for p, c in compositions],
                                "differential_controls": [{"receipt": ref(p), "claim": c["claim"], "observations": c["observations"]} for p, c in differentials],
                                "disabled_by_cfg_any": disabled, "test_or_support_file": test_only,
                                "dependency_sources_unchanged": receipt.get("dependency_sources_unchanged"),
                                "compiled_scope": "Package unit/integration tests, plus separately listed doctests or doctests in a default Cargo-test campaign baseline. Compatibility mod.rs targets require separate review."},
               "mutation_accounting": {"killed": 0, "survived": 0, "demonstrably_equivalent": 0,
                                       "invalid": 0, "inconclusive": 0, "unrun": 0, "conservative_ratio": None},
               "structure": {"tool": "syn source AST (see pinned metric_tool_sources in receipt)",
                             "functions": functions, "exceeding_A": exceeding,
                             "metric_ceiling": ceiling if functions is not None else None,
                             "scope": "Explicit source bodies only; opaque macros and compiler expansion remain unassessed."},
               "open_findings": failures}
    if mutation_path:
        campaign = read(mutation_path)
        links = specification.get("verification_challenges", {}) if specification else {}
        entries, links_present = select_challenges(read(mutation_path.parent / "mutations.json"), relative, links)
        counts = Counter(entry["outcome"] for entry in entries)
        for name in ("killed", "survived", "demonstrably_equivalent", "invalid", "inconclusive", "unrun"):
            counts.setdefault(name, 0)
        denominator = sum(counts[n] for n in ("killed", "survived", "inconclusive", "unrun"))
        scoring["mutation_accounting"] = {**counts, "conservative_ratio": counts["killed"] / denominator if denominator else None}
        scoring["verification"]["designated_mutations"] = [entry["id"] for entry in entries]
        scoring["verification"]["designated_challenges_present"] = links_present
        scoring["verification"]["linked_challenges"] = links
        scoring["verification"]["mutation_campaign"] = ref(mutation_path)
        packages = {entry["package"] for entry in entries}
        scoring["verification"]["mutation_restoration_baselines_ok"] = (
            package_runs_pass(campaign["baselines"], packages)
            and package_runs_pass(campaign["restored_baselines"], packages)
            and all(entry.get("source_restored") is True for entry in entries
                    if entry.get("run", {}).get("started") is not False and "run" in entry)) if entries else None
        if not links_present:
            failures.append("One or more explicitly linked challenge IDs/sources are absent from this campaign.")
        scoring["verification"]["designated_critical_faults_decisive"] = (
            bool(entries) and links_present and all(entry["outcome"] == "killed" for entry in entries))
        evidence.extend([ref(mutation_path), ref(mutation_path.parent / "mutations.json")])
        if campaign.get("continued_campaign"):
            continuation = campaign["continued_campaign"]
            evidence.append({key: continuation[key] for key in ("path", "sha256")})
    # Known E findings must remain visible even with other gates unassessed.
    # Cognitive values are an upper bound, so exceeding that alone is a ceiling,
    # not evidence that actual cognitive complexity violates an E threshold.
    if any(f["ccn"] > 50 or f["control_nesting"] >= 9 for f in functions or []):
        scoring["gates"]["G5"] = "E"
        scoring["composite_grade"] = "E"
        scoring["score_token"] = level + "E"
        scoring["open_findings"].append("Established G5 E threshold in exact source CCN or nesting, preserved under SCORING.md section 1.4.")
    local_defects = []
    for control_path, control in defect_controls:
        findings_path = control_path.parent / "findings.json"
        for finding in read(findings_path):
            if finding["source"] == relative and finding["reproduced"]:
                for gate in finding.get("affected_gates", [finding["gate"]]):
                    scoring["gates"][gate] = "E"
                scoring["composite_grade"] = "E"
                scoring["score_token"] = level + "E"
                scoring["grade_ceiling"] = "E"
                scoring["open_findings"].append(finding["witness"])
                local_defects.append(finding)
        if local_defects:
            evidence.append(ref(findings_path))
    scoring["verification"]["reproduced_defects"] = local_defects
    scoring["evaluation_timestamp"] = max(
        [scoring["evaluation_timestamp"], *[control["evaluation_timestamp"] for _, control in defect_controls]])
    scoring["evaluation_timestamp_basis"] = "Start of the latest bound assessment execution; execution durations are recorded in receipts."
    apply_individual_engineering_review(scoring, specification)
    scoring["contract"]["sha256"] = hashlib.sha256(render(contract).encode("utf-8")).hexdigest()
    return contract, scoring


def render(value):
    return "# YAML 1.2 (JSON syntax). AuthorityEffect: None.\n" + json.dumps(value, indent=2, ensure_ascii=False) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--mutations", type=Path)
    parser.add_argument("--baseline-extra", type=Path, action="append", default=[])
    parser.add_argument("--defect-controls", type=Path, action="append", default=[])
    parser.add_argument("--composition", type=Path, action="append", default=[])
    parser.add_argument("--differential", type=Path, action="append", default=[])
    args = parser.parse_args()
    receipt_path = args.receipt.resolve()
    receipt = read(receipt_path)
    sources = read(receipt_path.parent / "source_manifest.json")
    if digest(receipt_path.parent / "source_manifest.json") != receipt["source_manifest_sha256"]:
        raise RuntimeError("Source manifest digest mismatch")
    if not receipt["sources_unchanged"]:
        raise RuntimeError("Replay source changed during execution")
    expected_names = {p.relative_to(ROOT).as_posix() for p in subjects()}
    expected_names.update(("SCORING.md", "code/rust/Cargo.toml"))
    expected_names.update(p.relative_to(ROOT).as_posix() for p in CHALLENGES)
    expected_names.update(p.relative_to(ROOT).as_posix() for p in COMPOSITION_SOURCES)
    if sources.keys() != expected_names:
        raise RuntimeError("Receipt subject set differs from current scope")
    for name, expected in sources.items():
        if digest(ROOT / name) != expected:
            raise RuntimeError("Stale replay source: " + name)
    for run in receipt["runs"]:
        if "log" in run and digest(ROOT / run["log"]) != run["log_sha256"]:
            raise RuntimeError("Changed replay log: " + run["log"])
    for name, expected in receipt.get("metric_tool_sources", {}).items():
        if digest(ROOT / name) != expected:
            raise RuntimeError("Stale metric tool: " + name)
    dependency_path = receipt_path.parent / "dependency_sources.json"
    if dependency_path.is_file():
        if digest(dependency_path) != receipt["dependency_sources_sha256"]:
            raise RuntimeError("Dependency manifest digest mismatch")
        if any(not Path(name).is_file() or digest(Path(name)) != expected
               for name, expected in read(dependency_path).items()):
            raise RuntimeError("Dependency sources changed since replay")
    mutation_path = args.mutations.resolve() if args.mutations else None
    if mutation_path:
        campaign = read(mutation_path)
        artifact_keys = {
            "source_manifest.json": "source_manifest_sha256",
            "mutations.py": "runner_sha256",
            "replay.py": "execution_helper_sha256",
            "a_infinity_trial.py": "algebra_recipe_source_sha256",
            "rank_trial.py": "canonical_recipe_source_sha256",
            "smith_trial_recipes.py": "smith_recipe_source_sha256",
            "scalar_port_faults.py": "scalar_recipe_source_sha256",
            "ordered_fault_recipes.py": "ordered_recipe_source_sha256",
            "hott_model_faults.py": "hott_recipe_source_sha256",
            "curvature_faults.py": "curvature_recipe_source_sha256",
            "dependency_sources.json": "dependency_sources_sha256",
        }
        for filename, key in artifact_keys.items():
            if key in campaign and digest(mutation_path.parent / filename) != campaign[key]:
                raise RuntimeError("Changed mutation artifact: " + filename)
        if not campaign["sources_unchanged"] or not campaign.get("dependency_sources_unchanged"):
            raise RuntimeError("Mutation inputs changed during execution")
        if any(not Path(name).is_file() or digest(Path(name)) != expected
               for name, expected in read(mutation_path.parent / "dependency_sources.json").items()):
            raise RuntimeError("Mutation dependency sources changed since execution")
        if read(mutation_path.parent / "source_manifest.json") != sources:
            raise RuntimeError("Mutation and baseline snapshots differ")
        if digest(mutation_path.parent / "mutations.json") != campaign["mutations_sha256"]:
            raise RuntimeError("Mutation report digest mismatch")
        entries = read(mutation_path.parent / "mutations.json")
        if len({entry["id"] for entry in entries}) != len(entries):
            raise RuntimeError("Ambiguous duplicate mutation IDs")
        if campaign.get("continued_campaign"):
            from mutations import resume_kills
            continuation = campaign["continued_campaign"]
            prior_path = ROOT / continuation["path"]
            if digest(prior_path) != continuation["sha256"]:
                raise RuntimeError("Changed continuation parent")
            checked = [dict(entry) for entry in entries]
            verified = resume_kills(checked, prior_path, sources, campaign["versions"])
            reused = [entry for entry in entries if entry.get("reused_from")]
            if verified != continuation or len(reused) != verified["reused_killed"]:
                raise RuntimeError("Continuation reuse count/provenance differs")
            by_id = {entry["id"]: entry for entry in checked}
            for entry in reused:
                if any(entry.get(key) != by_id[entry["id"]].get(key) for key in
                       ("run", "outcome", "candidate_sha256", "source_restored", "reused_from")):
                    raise RuntimeError("Continued fault execution differs: " + entry["id"])
        counts = Counter(entry["outcome"] for entry in entries)
        for outcome in ("killed", "survived", "demonstrably_equivalent", "invalid", "inconclusive", "unrun"):
            if counts[outcome] != campaign["accounting"][outcome]:
                raise RuntimeError("Mutation accounting imbalance")
        for run in [*campaign["baselines"], *campaign["restored_baselines"],
                    *(entry["run"] for entry in entries if "run" in entry)]:
            if "log" in run and digest(ROOT / run["log"]) != run["log_sha256"]:
                raise RuntimeError("Changed mutation log")
    metrics_path = receipt_path.parent / "metrics.json"
    metrics = read(metrics_path) if metrics_path.is_file() else {}
    baseline_extras = []
    for extra_arg in args.baseline_extra:
        extra_path = extra_arg.resolve()
        extra = read(extra_path)
        if not extra["sources_unchanged"] or not extra.get("dependency_sources_unchanged"):
            raise RuntimeError("Supplemental baseline inputs changed during execution")
        if read(extra_path.parent / "source_manifest.json") != sources:
            raise RuntimeError("Supplemental baseline snapshot differs")
        for run in extra["runs"]:
            if "log" in run and digest(ROOT / run["log"]) != run["log_sha256"]:
                raise RuntimeError("Changed supplemental baseline log")
        baseline_extras.append((extra_path, extra))
    defect_controls = []
    for control_arg in args.defect_controls:
        control_path = control_arg.resolve()
        control = read(control_path)
        if not control["sources_unchanged"] or read(control_path.parent / "source_manifest.json") != sources:
            raise RuntimeError("Defect controls differ from the current source snapshot")
        dependency_path = control_path.parent / "dependency_sources.json"
        if not control.get("dependency_sources_unchanged") or not dependency_path.is_file():
            raise RuntimeError("Defect control dependency custody is unavailable")
        if digest(dependency_path) != control["dependency_sources_sha256"] or any(
                not Path(name).is_file() or digest(Path(name)) != expected
                for name, expected in read(dependency_path).items()):
            raise RuntimeError("Defect control dependencies changed")
        if digest(control_path.parent / "findings.json") != control["findings_sha256"]:
            raise RuntimeError("Defect finding digest mismatch")
        run = control["run"]
        if "log" not in run or digest(ROOT / run["log"]) != run["log_sha256"]:
            raise RuntimeError("Defect control execution missing or changed")
        defect_controls.append((control_path, control))
    compositions = []
    for composition_arg in args.composition:
        composition_path = composition_arg.resolve()
        composition = read(composition_path)
        if not composition["sources_unchanged"] or read(composition_path.parent / "source_manifest.json") != sources:
            raise RuntimeError("Composition source snapshot differs")
        run = composition.get("run")
        if not run or run["exit_code"] != 0 or run["timed_out"] or composition["metadata_capture"]["exit_code"] != 0:
            raise RuntimeError("Composition execution did not succeed")
        if digest(ROOT / run["log"]) != run["log_sha256"]:
            raise RuntimeError("Changed composition log")
        if "runs" in composition:
            if not composition.get("all_runs_passed") or not composition["runs"]:
                raise RuntimeError("One or more selected composition runs did not succeed")
            for selected_run in composition["runs"]:
                if (selected_run.get("exit_code") != 0 or selected_run.get("timed_out")
                        or digest(ROOT / selected_run["log"]) != selected_run["log_sha256"]):
                    raise RuntimeError("Changed or unsuccessful selected composition run")
        dependency_path = composition_path.parent / "dependency_sources.json"
        if not composition["dependency_sources_unchanged"] or digest(dependency_path) != composition["dependency_sources_sha256"]:
            raise RuntimeError("Composition dependency custody failed")
        if any(not Path(name).is_file() or digest(Path(name)) != expected
               for name, expected in read(dependency_path).items()):
            raise RuntimeError("Composition dependencies changed")
        if not composition["cargo_lock_unchanged"] or digest(RUST / "Cargo.lock") != composition["cargo_lock_before"]:
            raise RuntimeError("Composition lockfile changed")
        compositions.append((composition_path, composition))
    differentials = []
    for differential_arg in args.differential:
        path = differential_arg.resolve()
        control = read(path)
        if not control["sources_unchanged"] or read(path.parent / "source_manifest.json") != sources:
            raise RuntimeError("Differential source snapshot differs")
        if not control["runs"] or any(r.get("exit_code") != 0 or r.get("timed_out") for r in control["runs"]):
            raise RuntimeError("Differential execution did not succeed")
        for run in control["runs"]:
            if digest(ROOT / run["log"]) != run["log_sha256"]:
                raise RuntimeError("Changed differential log")
        dependencies = path.parent / "dependency_sources.json"
        if not control["dependency_sources_unchanged"] or digest(dependencies) != control["dependency_sources_sha256"]:
            raise RuntimeError("Differential dependency custody failed")
        if any(not Path(name).is_file() or digest(Path(name)) != expected for name, expected in read(dependencies).items()):
            raise RuntimeError("Differential inputs changed")
        if any(digest(ROOT / name) != expected for name, expected in control["sealed_legacy_sources"].items()):
            raise RuntimeError("Sealed legacy source changed")
        work = Path(control["runs"][0]["cwd"])
        if any(digest(work / name) != expected for name, expected in control["instrumented_sources"].items()):
            raise RuntimeError("Differential instrumentation changed")
        differentials.append((path, control))
    mismatches = []
    counts = Counter()
    generated = []
    for subject in subjects():
        contract, scoring = record_for(subject, receipt_path, receipt, metrics, mutation_path, baseline_extras, defect_controls, compositions, differentials)
        counts[subject.relative_to(RUST / "src").parts[0]] += 1
        for suffix, record in ((".contract.yaml", contract), (".scoring.yaml", scoring)):
            path = Path(str(subject) + suffix)
            expected = render(record)
            if args.check:
                if not path.is_file() or path.read_text(encoding="utf-8") != expected:
                    mismatches.append(path.relative_to(ROOT).as_posix())
            else:
                path.write_text(expected, encoding="utf-8", newline="\n")
            generated.append(ref(path) if path.is_file() else {"path": str(path), "sha256": None})
    manifest = {"AuthorityEffect": "None", "subject_counts": dict(counts), "sidecars": generated,
                "generator": ref(Path(__file__)), "specifications": ref(SPECS_PATH),
                "assessment_complete": False, "goal_complete": False,
                "scope": "Every Rust source and Cargo manifest in the six directories; existing assessment YAMLs are historical metadata, not recursive subjects."}
    manifest_path = receipt_path.parent / "sidecars.json"
    if args.check:
        if not manifest_path.is_file() or read(manifest_path) != manifest:
            mismatches.append(str(manifest_path))
    else:
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"subjects": sum(counts.values()), "directories": dict(counts),
                      "sidecars": len(generated), "mismatches": mismatches}))
    if mismatches:
        sys.exit(1)


if __name__ == "__main__":
    main()
