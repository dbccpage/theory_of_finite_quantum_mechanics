"""Exercise semantic refusal checks beyond the outer SHA envelope, without edits.

The probes replace decoded values in memory after normal digest validation.
No source, native receipt, proof or contract file is mutated by these controls.
"""
from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path

import reviewed_assessments as checks


def main():
    source = checks.ROOT / "code/rust/src/combinatorics/enumeration.rs"
    reference = json.loads((checks.HERE / "gate_reviews.json").read_text(encoding="utf-8"))[source.relative_to(checks.ROOT).as_posix()]
    original_load = checks.load
    assessment = original_load(reference)
    cases = []

    def changed_native(value):
        value["mutation_accounting"]["killed"] -= 1
        value["mutation_accounting"]["survived"] += 1

    def missing_failure(value):
        value[0]["run"]["exit_code"] = 0

    def wrong_metric(value):
        value[source.relative_to(checks.ROOT).as_posix()][0]["ccn"] = 11

    def missing_body(value):
        value["symbol_map"].pop(next(iter(value["symbol_map"])))

    def changed_body(value):
        value["symbol_map"][next(iter(value["symbol_map"]))]["body"] = "{ unreachable!() }"

    def missing_support(value):
        value["copies"].pop()

    def false_support(value):
        value["copies"][0]["sha256"] = "0" * 64

    probes = [
        ("false_six_outcome_counts", assessment["native_summary"], changed_native),
        ("kill_without_test_failure", assessment["native_mutations"], missing_failure),
        ("measured_A_ceiling_exceeded", assessment["metric_output"], wrong_metric),
        ("unmapped_production_body", reference, missing_body),
        ("incorrect_production_body", reference, changed_body),
    ]
    probes = [(name, target, mutate, source) for name, target, mutate in probes]
    lib_source = checks.ROOT / "code/rust/src/combinatorics/lib.rs"
    registry = json.loads((checks.HERE / "gate_reviews.json").read_text(encoding="utf-8"))
    if lib_source.relative_to(checks.ROOT).as_posix() in registry:
        lib_review = original_load(registry[lib_source.relative_to(checks.ROOT).as_posix()])
        probes.extend([
            ("missing_nested_crate_source", lib_review["native_support_sources"], missing_support, lib_source),
            ("wrong_nested_crate_source", lib_review["native_support_sources"], false_support, lib_source),
        ])
    for stem in ("lib", "mod"):
        fusion_source = checks.ROOT / f"code/rust/src/fusion_categories/{stem}.rs"
        key = fusion_source.relative_to(checks.ROOT).as_posix()
        if key in registry:
            fusion_review = original_load(registry[key])
            probes.extend([
                (f"missing_fusion_{stem}_support", fusion_review["native_support_sources"], missing_support, fusion_source),
                (f"wrong_fusion_{stem}_support", fusion_review["native_support_sources"], false_support, fusion_source),
            ])
    try:
        for name, target, mutate, probe_source in probes:
            def injected(item):
                value = original_load(item)
                if item["path"] == target["path"]:
                    value = deepcopy(value)
                    mutate(value)
                return value
            checks.load = injected
            try:
                checks.reviewed(probe_source)
            except (ValueError, SystemExit) as error:
                cases.append({"control": name, "expected": "refusal", "observed": str(error)})
            else:
                raise AssertionError("Undetected false evidence: " + name)
    finally:
        checks.load = original_load
    record, _ = checks.reviewed(source)
    assert record[1]["score_token"] == "L4A"
    cases.append({"control": "unaltered_current_review", "expected": "pass", "observed": record[1]["score_token"]})
    for stem in ("lib", "mod"):
        fusion_source = checks.ROOT / f"code/rust/src/fusion_categories/{stem}.rs"
        if fusion_source.relative_to(checks.ROOT).as_posix() in registry:
            record, _ = checks.reviewed(fusion_source)
            assert record[1]["score_token"] == "L1A"
            cases.append({"control": f"unaltered_fusion_{stem}", "expected": "pass", "observed": "L1A"})
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    output = checks.ROOT / "evidence/quality/six_module" / (stamp + "-review-controls.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    value = {"AuthorityEffect": "None", "checked_at": datetime.now(timezone.utc).isoformat(),
        "runner_sha256": checks.sha(Path(__file__)), "review_verifier_sha256": checks.sha(Path(checks.__file__)),
        "scope": "In-memory decoded-value controls after validating the original outer reference digests; no artifact bytes edited.",
        "checks": cases}
    with output.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(value, indent=2) + "\n")
    print(f"{len(probes)} semantic false-evidence controls refused; the unaltered L4A review passes")
    print("Receipt:", output)


if __name__ == "__main__":
    main()
