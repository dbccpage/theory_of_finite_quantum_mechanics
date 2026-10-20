"""Validate individually authored gate reviews; passing replays never author one.

Reuses the existing category/homology proof, dependency and weakest-link checks.
The digest adapter is SHA-256 over the same bytes and supports Python 3.10.
"""
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import re

from context_refresh import verify_provider_context

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(reference):
    path = ROOT / reference["path"]
    if not path.is_file() or sha(path) != reference["sha256"]:
        raise ValueError("Reviewed evidence is stale: " + reference["path"])
    return json.loads(path.read_text(encoding="utf-8"))


def verify_run(run, successful=False):
    log = ROOT / run["log"]
    if not run.get("command") or not run.get("cwd") or sha(log) != run["log_sha256"]:
        raise ValueError("Execution custody mismatch")
    if run["timed_out"] or (successful and run["exit_code"] != 0):
        raise ValueError("Unsuccessful reviewed execution")
    return log.read_text(encoding="utf-8")


def reviewed(source):
    registry = HERE / "gate_reviews.json"
    if not registry.exists():
        return None
    references = json.loads(registry.read_text(encoding="utf-8"))
    reference = references.get(source.relative_to(ROOT).as_posix())
    if reference is None:
        return None
    assessment = load(reference)
    artifact = {"path": source.relative_to(ROOT).as_posix(), "sha256": sha(source), "language": "Rust"}
    if assessment["artifact"] != artifact or assessment["rubric_sha256"] != sha(ROOT / "SCORING.md"):
        raise ValueError("Assessment subject/rubric drift")
    canonical = HERE.parent / "category_homology/write_scores.py"
    specification = importlib.util.spec_from_file_location("legacy_score_checks", canonical)
    verifier = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(verifier)
    verifier.sha = sha

    primary = assessment["native_summary"]
    native = load(primary)
    native_dir = (ROOT / primary["path"]).parent
    required = ("baseline_ok", "restored_ok", "source_unchanged", "dependencies_unchanged", "build_outputs_removed")
    if not all(native[k] for k in required) or native["subject"] != {k: artifact[k] for k in ("path", "sha256")}:
        raise ValueError("Native receipt does not cover this current subject")
    policy = load(assessment["native_policy"])
    if sha(ROOT / assessment["native_policy"]["path"]) != native["policy_sha256"] or policy["subject"] != native["subject"]:
        raise ValueError("Native source/policy mismatch")
    for field, key in (("native_fixture", "fixture_sha256"), ("native_runner", "runner_sha256")):
        item = assessment[field]
        if sha(ROOT / item["path"]) != item["sha256"] or item["sha256"] != native[key]:
            raise ValueError("Native runtime snapshot mismatch")
    source_text = source.read_text(encoding="utf-8")
    fixture_text = (ROOT / assessment["native_fixture"]["path"]).read_text(encoding="utf-8")
    dependencies = assessment["native_dependencies"]
    load(dependencies)
    verifier.verify_dependencies(native_dir, {
        "dependencies_unchanged": True, "dependency_receipt_sha256": dependencies["sha256"]})
    manifest = load(assessment["native_sources"])
    if manifest.get(artifact["path"]) != artifact["sha256"]:
        raise ValueError("Native source manifest mismatch")
    if artifact["path"] == "code/rust/src/combinatorics/lib.rs":
        support = load(assessment["native_support_sources"])
        work = Path(native["baseline"][0]["command"][0]).parent
        expected = {
            ((work / "src/combinatorics/q" / f"n{index}" / Path(path).name).relative_to(ROOT).as_posix(), path, value)
            for index in range(len(policy["faults"]) + 1)
            for path, value in manifest.items()
            if path.endswith(".rs") and Path(path).name != "lib.rs"
        }
        records = support["copies"]
        actual = {(item["path"], item["source"], item["sha256"]) for item in records}
        if actual != expected or len(records) != len(expected):
            raise ValueError("Nested crate source coverage mismatch")
        if any(sha(ROOT / item["path"]) != item["sha256"] for item in records):
            raise ValueError("Nested crate source bytes changed")
    if artifact["path"] in {"code/rust/src/fusion_categories/lib.rs", "code/rust/src/fusion_categories/mod.rs", "code/rust/src/fusion_categories/fusion_ring.rs", "code/rust/src/fusion_categories/scalar.rs", "code/rust/src/fusion_categories/error.rs", "code/rust/src/fusion_categories/braid_group.rs", "code/rust/src/fusion_categories/yang_baxter.rs", "code/rust/src/fusion_categories/catalog.rs", "code/rust/src/fusion_categories/modular.rs", "code/rust/src/fusion_categories/su2_level.rs", "code/rust/src/fusion_categories/fusion_category.rs"}:
        support = load(assessment["native_support_sources"])
        work = Path(native["baseline"][0]["command"][0]).parent
        expected = {
            ((work / f"p{index}" / Path(path).name).relative_to(ROOT).as_posix(), path, value)
            for index in range(len(policy["faults"]) + 1)
            for path, value in manifest.items()
            if path.endswith(".rs") and Path(path).name != source.name
        }
        records = support["copies"]
        if {(x["path"], x["source"], x["sha256"]) for x in records} != expected or len(records) != len(expected):
            raise ValueError("Fusion package source coverage mismatch")
        if any(sha(ROOT / item["path"]) != item["sha256"] for item in records):
            raise ValueError("Fusion package source bytes changed")
        control = work / "p0" / source.name
        if control.read_text(encoding="utf-8") != source_text + "\n" + fixture_text:
            raise ValueError("Fusion control source mismatch")
    for run in native["builds"]:
        verify_run(run, successful=True)
    for run in native["baseline"] + native["restored"]:
        text = verify_run(run, successful=True)
        if not re.search(r"test result: ok\. [1-9][0-9]* passed;", text):
            raise ValueError("Native baseline lacks actual passing tests")
    mutants = load(assessment["native_mutations"])
    if len(mutants) != len(policy["faults"]):
        raise ValueError("Generated fault inventory mismatch")
    outcomes = Counter(item["outcome"] for item in mutants)
    keys = ("killed", "survived", "demonstrably_equivalent", "invalid", "inconclusive", "unrun")
    if {key: outcomes[key] for key in keys} != native["mutation_accounting"] or sum(outcomes.values()) != sum(native["mutation_accounting"].values()):
        raise ValueError("Six-outcome accounting mismatch")
    for item, recipe in zip(mutants, policy["faults"]):
        if any(item[key] != recipe[key] for key in ("id", "needle", "replacement")):
            raise ValueError("Mutation recipe mismatch")
        if sha(ROOT / item["candidate"]) != item["sha256"]:
            raise ValueError("Mutation candidate bytes changed")
        expected = source_text.replace(recipe["needle"], recipe["replacement"]) + "\n" + fixture_text
        if source_text.count(recipe["needle"]) != 1 or (ROOT / item["candidate"]).read_text(encoding="utf-8") != expected:
            raise ValueError("Compiled candidate is not the designated source fault")
        text = verify_run(item["run"])
        if item["outcome"] == "killed" and (item["run"]["exit_code"] == 0 or "test result: FAILED" not in text):
            raise ValueError("Fault lacks distinct failing test attribution")
    eligible = sum(outcomes[key] for key in ("killed", "survived", "inconclusive", "unrun"))
    ratio = outcomes["killed"] / eligible if eligible else None
    if ratio != native["conservative_ratio"] or ratio is None or ratio < .95:
        raise ValueError("Native challenge does not reach A")

    metric = load(assessment["metric_receipt"])
    metric_dir = (ROOT / assessment["metric_receipt"]["path"]).parent
    metric_manifest = load(assessment["metric_sources"])
    if not metric["sources_unchanged"] or metric["source_manifest_sha256"] != sha(metric_dir / "source_manifest.json") or metric_manifest.get(artifact["path"]) != artifact["sha256"]:
        raise ValueError("Metric/source binding mismatch")
    for path, expected in metric["tool_sources"].items():
        if sha(ROOT / path) != expected:
            raise ValueError("Calibrated metric tool drift")
    for run in metric["runs"]:
        verify_run(run, successful=True)
    measured = load(assessment["metric_output"])[artifact["path"]]
    if source.relative_to(ROOT).as_posix() == "code/rust/src/fusion_categories/scalar.rs":
        macro = load(assessment["macro_review"])
        template = macro["template"]
        start = source_text.index("macro_rules! cyclotomic_scalar")
        end = source_text.index("#[cfg(test)]", start)
        invocation_start = source_text.index("\ncyclotomic_scalar!", start)
        if template != source_text[start:invocation_start].strip():
            raise ValueError("Scalar macro template drift")
        entries = macro["invocations"]
        if len(entries) != 8 or len({x["type"] for x in entries}) != 8:
            raise ValueError("Scalar macro coverage mismatch")
        calls = []
        body = template.split("=> {", 1)[1].rsplit("    };", 1)[0].strip()
        expanded = "// Explicit macro substitution view for calibrated AST metrics only. Not compiled.\n"
        for item in entries:
            invocation = f"cyclotomic_scalar!({item['type']}, {item['order']}, {item['root']});"
            if invocation != item["invocation"]:
                raise ValueError("Scalar macro argument mismatch")
            calls.append(invocation)
            expanded += body.replace("$ty",item["type"]).replace("$order",item["order"]).replace("$root",item["root"]) + "\n"
        if re.sub(r"\s+", "", "".join(calls)) != re.sub(r"\s+", "", source_text[invocation_start:end]):
            raise ValueError("Scalar macro invocation drift")
        view = assessment["macro_view"]
        if sha(ROOT / view["path"]) != view["sha256"] or (ROOT / view["path"]).read_text(encoding="utf-8") != expanded:
            raise ValueError("Scalar macro metric view differs from substitution")
        if metric_manifest.get(view["path"]) != view["sha256"]:
            raise ValueError("Scalar macro metric view not measured")
        records = load(assessment["metric_output"])[view["path"]]
        names = Counter(x["name"] for x in records)
        if names != Counter({name:8 for name in ("to_rational","root_of_unity_order","primitive_root_of_unity","real_sign")}):
            raise ValueError("Scalar generated method coverage mismatch")
        if any(x["ccn"]>10 or x["cognitive_upper_bound"]>15 or x["control_nesting"]>3 or x["opaque_macros"] for x in records):
            raise ValueError("Scalar generated methods exceed A structure")
    mapped = list(assessment["symbol_map"].values())
    pairs = sorted((item["line"], re.search(r"\bfn\s+(\w+)", item["signature"])[1]) for item in mapped)
    if pairs != sorted((item["line"], item["name"]) for item in measured):
        raise ValueError("Source review does not map every measured body")
    lines = source_text.splitlines(keepends=True)
    for item in mapped:
        start = sum(map(len, lines[:item["line"] - 1]))
        brace = source_text.index("{", source_text.index("fn ", start))
        if (source_text[start:brace].strip() != item["signature"]
                or not item["body"].startswith("{") or not item["body"].endswith("}")
                or not source_text[brace:].startswith(item["body"])):
            raise ValueError("Mapped production signature/body differs from source")
    if any(item["ccn"] > 10 or item["cognitive_upper_bound"] > 15 or item["control_nesting"] > 3 for item in measured):
        raise ValueError("Source exceeds A structural ceiling")
    if "consumer_context_refresh" in assessment:
        bridge = load(assessment["consumer_context_refresh"])
        texts = []
        for key in ("previous_producer", "current_producer"):
            item = bridge[key]
            path = ROOT / item["path"]
            if sha(path) != item["sha256"]:
                raise ValueError("Consumer producer source drift")
            texts.append(path.read_text(encoding="utf-8"))
        marker = "#[cfg(test)]"
        tests = [text[text.index(marker):] for text in texts]
        if not bridge["tests_unchanged"] or tests[0] != tests[1]:
            raise ValueError("Consumer test boundary changed")
        if hashlib.sha256(tests[1].encode()).hexdigest() != bridge["normalized_tests_sha256"]:
            raise ValueError("Consumer test declaration mismatch")
        for name, signature in bridge["public_signatures"].items():
            for text in texts:
                match = re.search(r"(?m)^pub fn " + re.escape(name) + r"\b", text)
                if match is None or text[match.start():text.index("{", match.start())].strip() != signature:
                    raise ValueError("Consumer public signature changed")
        if any("pub const MAX_LEVEL: usize = 6;" not in text for text in texts):
            raise ValueError("Consumer level domain changed")
        composition = load(bridge["current_canonical"])
        flags = ("baseline_ok", "source_unchanged", "dependencies_unchanged",
                 "copied_sources_unchanged", "build_outputs_removed")
        if not all(composition[key] for key in flags):
            raise ValueError("Current consumer composition is unverified")
        producer = bridge["current_producer"]
        if load(bridge["current_canonical_sources"]).get(producer["path"]) != producer["sha256"]:
            raise ValueError("Consumer composition subject mismatch")
        if any(sha(ROOT/path) != value for path, value in load(bridge["current_canonical_copies"]).items()):
            raise ValueError("Consumer composition copy drift")
        verify_run(composition["build"], successful=True)
        for run in composition["runs"]:
            text = verify_run(run, successful=True)
            if not re.search(r"test result: ok\. [1-9][0-9]* passed;", text):
                raise ValueError("Current consumer composition has no passing tests")
    if "provider_context_refresh" in assessment:
        verify_provider_context(assessment["provider_context_refresh"], artifact, ROOT,
                                load, sha, verify_run, verifier.verify_dependencies)
    record = {"artifact": artifact, "level": assessment["level"], "gates": {f"G{i}": None for i in range(1,6)},
              "grade_ceiling": "A", "evidence": []}
    verifier.apply_assessment(record, ROOT / reference["path"])
    if not record["is_complete"] or record["composite_grade"] != "A" or record.get("open_findings"):
        raise ValueError("Review is not a complete A assessment")
    return ((ROOT / reference["path"], record), assessment)
