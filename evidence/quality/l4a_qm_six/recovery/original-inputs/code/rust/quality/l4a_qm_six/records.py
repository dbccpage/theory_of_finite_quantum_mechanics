"""Write/check source-bound assessment and contract sidecars for majorana, mub, number_theory, operad_theory, sheaf_theory, and qm.

JSON documents are used as YAML 1.2. Public declarations are a lexical index,
not an AST coverage or semantic correctness claim. Python 3.11+.
AuthorityEffect: None.
"""

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import tomllib

from replay import ROOT, RUST, GROUPS, digest, subjects


PURPOSES = {
    "majorana": "Finite Majorana braid compilers, F2 chain/cochain complexes, Kitaev wire isolation, packet-wall classification, and exact rational Pauli noise thresholds.",
    "mub": "Finite mutually unbiased bases (MUB) in dimension 6, cyclotomic/rational Gramian diagnostics, dual witnesses, Fourier landing verifiers, and cover-tree exclusions.",
    "number_theory": "Finite fields, cyclotomic rings, exact rational arithmetic, modular arithmetic, quadratic forms, and Dirichlet character evaluations.",
    "operad_theory": "Colored planar/symmetric operads, operadic algebras, bar-cobar/Koszul duality structures, little-disks configurations, and kernel licensing checks.",
    "sheaf_theory": "Finite presheaves, sheaves, rational Cech cohomology, gluing obstructions, and contextuality sheaf diagnostics over finite covers.",
    "qm": "Finite quantum mechanics campaign certifiers, foundational targets 1..22, C250/C500 blocks, causal prices, entropy solvers, and textbook problem receipts.",
}
SPECS_PATH = Path(__file__).with_name("specs.json")


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def ref(path):
    return {"path": path.relative_to(ROOT).as_posix(), "sha256": digest(path)}


def declaration_index(source):
    """Only a line index; excludes neither cfg branches nor macro-generated items."""
    pattern = re.compile(
        r"^\s*pub(?:\([^)]*\))?\s+(?:(?:const|async|unsafe)\s+)?"
        r"(fn|struct|enum|trait|type|const|mod)\s+([A-Za-z_]\w*)"
    )
    result = []
    for number, line in enumerate(source.splitlines(), 1):
        match = pattern.match(line)
        if match:
            result.append(
                {
                    "kind": match[1],
                    "name": match[2],
                    "line": number,
                    "declaration_line": line.strip(),
                }
            )
    return result


def metric_ceiling(functions):
    def band(value, limits):
        return next((grade for upper, grade in limits if value <= upper), "E")

    order = ["E", "D", "C", "B", "A"]
    grade = "A"
    exceeding = []
    for item in functions:
        g_ccn = band(item["ccn"], [(10, "A"), (15, "B"), (20, "C"), (50, "D")])
        g_cog = band(
            item["cognitive_upper_bound"], [(15, "A"), (20, "B"), (25, "C"), (40, "D")]
        )
        g_nest = band(item["control_nesting"], [(3, "A"), (4, "B"), (5, "C"), (8, "D")])
        grades = [
            g_ccn,
            "D"
            if g_cog == "E" and item["ccn"] <= 50 and item["control_nesting"] <= 8
            else g_cog,
            g_nest,
        ]
        lowest = min(grades, key=order.index)
        grade = min((grade, lowest), key=order.index)
        if lowest != "A":
            exceeding.append({**item, "metric_ceiling": lowest})
    return grade, exceeding


def apply_individual_engineering_review(scoring, specification):
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
            required = {"C": 0.70, "B": 0.85, "A": 0.95, "A+": 1.0}.get(grade, 0)
            if (
                not baseline
                or baseline.get("exit_code") != 0
                or ratio is None
                or ratio < required
                or not scoring["verification"].get("mutation_restoration_baselines_ok")
            ):
                scoring["open_findings"].append(
                    "Individual G4 judgement withheld: execution or mutation prerequisite unmet."
                )
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
        scoring["grade_ceiling_basis"] = (
            "Minimum of explicit individual gate decisions and measured structural eligibility."
        )
    resolved_prefixes = []
    if scoring["gates"]["G1"] is not None:
        resolved_prefixes.append("Complete source-to-requirement")
    if all(scoring["gates"][gate] is not None for gate in ("G2", "G3")):
        resolved_prefixes.append("Domain admission, construction/deserialization")
    if scoring["gates"]["G4"] is not None:
        resolved_prefixes.append("Fresh baseline execution alone")
    scoring["open_findings"][:] = [
        item
        for item in scoring["open_findings"]
        if not any(item.startswith(prefix) for prefix in resolved_prefixes)
    ]
    scoring["open_findings"].extend(specification.get("open_obligations", []))


def record_for(path, receipt_path, receipt, metrics, mutation_path=None):
    relative = path.relative_to(ROOT).as_posix()
    group = path.relative_to(RUST / "src").parts[0]
    rel_parts = path.relative_to(RUST / "src").parts
    source = path.read_text(encoding="utf-8")
    disabled = source.lstrip().startswith("#![cfg(any())]")
    test_only = (
        path.name in ("l5a_challenges.rs", "test_support.rs", "tests.rs")
        or "tests" in rel_parts
    )
    mirror_tree = group == "mub" and len(rel_parts) > 1 and rel_parts[1] == "src"
    artifact = {
        "path": relative,
        "sha256": digest(path),
        "language": "Rust" if path.suffix == ".rs" else "Other",
    }
    specification = read(SPECS_PATH)["files"].get(
        path.relative_to(RUST / "src").as_posix()
    )
    index = declaration_index(source) if path.suffix == ".rs" else []
    functions = metrics.get(relative)
    ceiling, exceeding = metric_ceiling(functions or [])
    profile = "Non-Numeric" if path.name == "Cargo.toml" else "Exact"
    if disabled:
        level, basis = (
            "L1",
            "The entire file is disabled by cfg(any()); its mathematical declarations deliver no default runtime capability.",
        )
    elif path.name == "Cargo.toml":
        level, basis = "L1", "Build manifest; dependency and library target declarations."
    elif path.stem == "mod" or (path.stem == "lib" and not functions):
        level, basis = (
            "L1",
            "Module/export facade; composition evidence does not raise this file's own capability.",
        )
    else:
        level, basis = (
            "L3",
            "Provisional bounded-domain classification; requires individual capability review before promotion.",
        )
    capability = specification.get("capability_assessment") if specification else None
    if capability:
        if capability["source_sha256"] != artifact["sha256"]:
            raise RuntimeError("Stale individual capability review: " + relative)
        level, basis = capability["level"], capability["basis"]
    failures = [
        "Complete source-to-requirement and downstream consumer review is outstanding.",
        "Domain admission, construction/deserialization paths, panic freedom and dependency trust require individual review.",
        "Fresh baseline execution alone does not establish independent challenge or mutation adequacy.",
    ]
    if disabled:
        failures.append(
            "The entire file is disabled by cfg(any()); its declarations and tests are not compiled by the package baseline."
        )
    if test_only:
        failures.append(
            "Test/support artifact: source metrics below must not be interpreted as production execution complexity."
        )
    if mirror_tree:
        failures.append(
            "Compatibility mirror under mub/src/ retained for ownership-firewall and atlas path checks; primary compiled module tree is rooted at mub/lib.rs."
        )
    if functions is None and path.suffix == ".rs":
        failures.append("No fresh calibrated structural measurement for this file.")
    if exceeding:
        failures.append(
            "One or more source functions exceed an A structural ceiling; see structure.exceeding_A."
        )
    contract_path = Path(str(path) + ".contract.yaml")
    evidence = [ref(receipt_path), ref(receipt_path.parent / "source_manifest.json")]
    evidence.extend([ref(Path(__file__)), ref(SPECS_PATH)])
    metric_path = receipt_path.parent / "metrics.json"
    if functions is not None:
        evidence.append(ref(metric_path))
    runs = receipt["runs"]
    package = {
        "majorana": "tfqm_majorana",
        "mub": "tfqm_mub",
        "number_theory": "tfqm_number_theory",
        "operad_theory": "tfqm_operad_theory",
        "sheaf_theory": "tfqm_sheaf_theory",
        "qm": "tfqm_qm_audit",
    }[group]
    baseline = next(
        (r for r in runs if "-p" in r.get("command", []) and package in r["command"]),
        None,
    )
    if baseline is None and mutation_path:
        campaign = read(mutation_path)
        baseline = next(
            (run for run in campaign["baselines"] if run["package"] == package), None
        )
    doctests = [
        run
        for run in runs
        if "--doc" in run.get("command", []) and package in run["command"]
    ]
    contract = {
        "schema_version": "1.0.0",
        "AuthorityEffect": "None",
        "artifact": artifact,
        "contract_urn": "urn:tfqm:contract:"
        + relative.removeprefix("code/rust/src/").replace("/", ":"),
        "status": "draft_requires_semantic_review",
        "target": "L4A",
        "profile": profile,
        "purpose": PURPOSES[group],
        "subject_role": basis,
        "compilation": {
            "disabled_by_cfg_any": disabled,
            "test_or_support_file": test_only,
            "compatibility_mirror_tree": mirror_tree,
        },
        "declaration_index": index,
        "declaration_index_scope": "Lexical line index only; signatures may span lines, include test/cfg items and omit macros/reexports.",
        "requirements": [
            {
                "id": "G1",
                "requirement": "Bind this source digest, declared symbols, actual claims, dependencies and consumer boundaries.",
            },
            {
                "id": "G2",
                "requirement": "Admit all public input domains; preserve exact arithmetic and declared algebraic laws on each successful path.",
            },
            {
                "id": "G3",
                "requirement": "Enumerate typed refusals and preserve state/invariants on every failure; justify all indexing and scalar preconditions.",
            },
            {
                "id": "G4",
                "requirement": "Challenge each declared critical failure class using an independent basis; retain all six mutation outcomes and require R >= 0.95 for A.",
            },
            {
                "id": "G5",
                "requirement": "Meet CCN <= 10, cognitive upper bound <= 15 and nesting <= 3; audit allocations and operational bounds separately.",
            },
        ],
        "admission_policy": "Records with public fields or Deserialize are untrusted candidates until the specific validator admits them; a validator's name is not proof of completeness.",
        "resource_boundary": "No process-OOM, bit-complexity, timeout or global memory guarantee is inferred from element/work counters.",
        "authority_ceiling": "Runtime finite checks only. No formal theorem, physical derivation or authority promotion is certified.",
        "open_obligations": failures,
        "evidence": evidence,
    }
    if path.name == "Cargo.toml":
        manifest = tomllib.loads(source)
        contract["manifest"] = {
            key: manifest.get(key, {})
            for key in ("package", "lib", "dependencies", "dev-dependencies")
        }
        contract["admission_policy"] = (
            "Cargo resolves declared dependencies; absolute external path dependencies require independent source custody and portability review."
        )
    specification = read(SPECS_PATH)["files"].get(
        path.relative_to(RUST / "src").as_posix()
    )
    if specification:
        contract["reviewed_specification"] = specification
        contract["status"] = specification["status"]
    scoring = {
        "schema_version": "2.0.0",
        "AuthorityEffect": "None",
        "artifact": artifact,
        "profile": profile,
        "level": level,
        "level_basis": basis,
        "engineering_target": "A",
        "requested_target": "L4A",
        "gates": {"G1": None, "G2": None, "G3": None, "G4": None, "G5": None},
        "composite_grade": None,
        "score_token": None,
        "is_complete": False,
        "grade_ceiling": ceiling,
        "evaluation_timestamp": datetime.strptime(
            receipt_path.parent.name, "%Y%m%dT%H%M%SZ"
        )
        .replace(tzinfo=timezone.utc)
        .isoformat(),
        "grade_ceiling_basis": "Conservative source-metric eligibility ceiling; cognitive values are upper bounds, not demonstrated semantic failures.",
        "contract": {
            "path": contract_path.relative_to(ROOT).as_posix(),
            "status": contract["status"],
        },
        "evidence": evidence,
        "verification": {
            "baseline": baseline,
            "sources_unchanged": receipt["sources_unchanged"],
            "doctests": doctests,
            "disabled_by_cfg_any": disabled,
            "test_or_support_file": test_only,
            "compatibility_mirror_tree": mirror_tree,
            "dependency_sources_unchanged": receipt.get("dependency_sources_unchanged"),
            "compiled_scope": "Package unit/integration tests in the scoped six-directory snapshot. Compatibility mirror files under mub/src/ require separate compilation review.",
        },
        "mutation_accounting": {
            "killed": 0,
            "survived": 0,
            "demonstrably_equivalent": 0,
            "invalid": 0,
            "inconclusive": 0,
            "unrun": 0,
            "conservative_ratio": None,
        },
        "structure": {
            "tool": "syn source AST (see pinned metric_tool_sources in receipt)",
            "functions": functions,
            "exceeding_A": exceeding,
            "metric_ceiling": ceiling if functions is not None else None,
            "scope": "Explicit source bodies only; opaque macros and compiler expansion remain unassessed.",
        },
        "open_findings": failures,
    }
    if mutation_path:
        campaign = read(mutation_path)
        entries = [
            entry
            for entry in read(mutation_path.parent / "mutations.json")
            if entry["source"] == relative
        ]
        counts = Counter(entry["outcome"] for entry in entries)
        for name in (
            "killed",
            "survived",
            "demonstrably_equivalent",
            "invalid",
            "inconclusive",
            "unrun",
        ):
            counts.setdefault(name, 0)
        denominator = sum(
            counts[n] for n in ("killed", "survived", "inconclusive", "unrun")
        )
        scoring["mutation_accounting"] = {
            **counts,
            "conservative_ratio": counts["killed"] / denominator
            if denominator
            else None,
        }
        scoring["verification"]["designated_mutations"] = [
            entry["id"] for entry in entries
        ]
        scoring["verification"]["mutation_restoration_baselines_ok"] = (
            all(run["exit_code"] == 0 for run in campaign["restored_baselines"])
            if entries
            else None
        )
        evidence.extend(
            [ref(mutation_path), ref(mutation_path.parent / "mutations.json")]
        )
    if any(f["ccn"] > 50 or f["control_nesting"] >= 9 for f in functions or []):
        scoring["gates"]["G5"] = "E"
        scoring["composite_grade"] = "E"
        scoring["score_token"] = level + "E"
        scoring["open_findings"].append(
            "Established G5 E threshold in exact source CCN or nesting, preserved under SCORING.md section 1.4."
        )
    scoring["verification"]["reproduced_defects"] = []
    scoring["evaluation_timestamp_basis"] = (
        "Start of the latest bound assessment execution; execution durations are recorded in receipts."
    )
    apply_individual_engineering_review(scoring, specification)
    scoring["contract"]["sha256"] = hashlib.sha256(
        render(contract).encode("utf-8")
    ).hexdigest()
    return contract, scoring


def render(value):
    return (
        "# YAML 1.2 (JSON syntax). AuthorityEffect: None.\n"
        + json.dumps(value, indent=2, ensure_ascii=False)
        + "\n"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--mutations", type=Path)
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
        if any(
            (not Path(name).is_file() or digest(Path(name)) != expected)
            and "l4a-qm-six" not in Path(name).parts
            for name, expected in read(dependency_path).items()
        ):
            raise RuntimeError("Dependency sources changed since replay")
    mutation_path = args.mutations.resolve() if args.mutations else None
    if mutation_path:
        campaign = read(mutation_path)
        if not campaign["sources_unchanged"] or not campaign.get(
            "dependency_sources_unchanged"
        ):
            raise RuntimeError("Mutation inputs changed during execution")
        if read(mutation_path.parent / "source_manifest.json") != sources:
            raise RuntimeError("Mutation and baseline snapshots differ")
        if digest(mutation_path.parent / "mutations.json") != campaign["mutations_sha256"]:
            raise RuntimeError("Mutation report digest mismatch")
        entries = read(mutation_path.parent / "mutations.json")
        counts = Counter(entry["outcome"] for entry in entries)
        for outcome in (
            "killed",
            "survived",
            "demonstrably_equivalent",
            "invalid",
            "inconclusive",
            "unrun",
        ):
            if counts[outcome] != campaign["accounting"][outcome]:
                raise RuntimeError("Mutation accounting imbalance")
        for run in [
            *campaign["baselines"],
            *campaign["restored_baselines"],
            *(entry["run"] for entry in entries if "run" in entry),
        ]:
            if "log" in run and digest(ROOT / run["log"]) != run["log_sha256"]:
                raise RuntimeError("Changed mutation log")
    metrics_path = receipt_path.parent / "metrics.json"
    metrics = read(metrics_path) if metrics_path.is_file() else {}
    mismatches = []
    counts = Counter()
    generated = []
    for subject in subjects():
        contract, scoring = record_for(
            subject, receipt_path, receipt, metrics, mutation_path
        )
        counts[subject.relative_to(RUST / "src").parts[0]] += 1
        for suffix, record in ((".contract.yaml", contract), (".scoring.yaml", scoring)):
            path = Path(str(subject) + suffix)
            expected = render(record)
            if args.check:
                if not path.is_file() or path.read_text(encoding="utf-8") != expected:
                    mismatches.append(path.relative_to(ROOT).as_posix())
            else:
                path.write_text(expected, encoding="utf-8", newline="\n")
            generated.append(
                ref(path) if path.is_file() else {"path": str(path), "sha256": None}
            )
    manifest = {
        "AuthorityEffect": "None",
        "subject_counts": dict(counts),
        "sidecars": generated,
        "generator": ref(Path(__file__)),
        "specifications": ref(SPECS_PATH),
        "assessment_complete": False,
        "goal_complete": False,
        "scope": "Every Rust source and Cargo manifest in majorana, mub, number_theory, operad_theory, sheaf_theory, and qm.",
    }
    manifest_path = receipt_path.parent / "sidecars.json"
    if args.check:
        if not manifest_path.is_file() or read(manifest_path) != manifest:
            mismatches.append(str(manifest_path))
    else:
        manifest_path.write_text(
            json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n"
        )
    print(
        json.dumps(
            {
                "subjects": sum(counts.values()),
                "directories": dict(counts),
                "sidecars": len(generated),
                "mismatches": mismatches,
            },
            indent=2,
        )
    )
    if mismatches:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
