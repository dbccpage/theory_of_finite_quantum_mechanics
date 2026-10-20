"""Exercise semantic refusal checks beyond the outer SHA envelope, without edits.

The probes replace decoded values in memory after normal digest validation.
No source, native receipt, proof or contract file is mutated by these controls.
"""
from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path as _FilesystemPath
import sys as _contract_sys
_contract_sys.path.insert(0, str(_FilesystemPath(__file__).resolve().parents[4] / "scripts"))
from contract_scores import RecordPath as Path, copy_file as _copy_record_file

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
    for stem in ("lib", "mod", "fusion_ring", "scalar", "error", "braid_group", "yang_baxter", "catalog", "modular", "su2_level", "fusion_category"):
        fusion_source = checks.ROOT / f"code/rust/src/fusion_categories/{stem}.rs"
        key = fusion_source.relative_to(checks.ROOT).as_posix()
        if key in registry:
            fusion_review = original_load(registry[key])
            probes.extend([
                (f"missing_fusion_{stem}_support", fusion_review["native_support_sources"], missing_support, fusion_source),
                (f"wrong_fusion_{stem}_support", fusion_review["native_support_sources"], false_support, fusion_source),
            ])
            if stem in ("catalog", "modular", "su2_level", "fusion_category"):
                probes.extend([
                    (f"unmapped_fusion_{stem}_body", registry[key], missing_body, fusion_source),
                    (f"incorrect_fusion_{stem}_body", registry[key], changed_body, fusion_source),
                ])
            if "provider_context_refresh" in fusion_review:
                def false_provider_api(value):
                    value["providers"][0]["public_api"]["functions"][0]["signature"] = "pub fn changed()"
                def false_provider_tests(value):
                    value["providers"][0]["tests_unchanged"] = False
                def false_provider_consumer(value):
                    value["consumers"][0]["current"]["sha256"] = "0" * 64
                def false_provider_test_count(value):
                    value["canonical_tests"][0] = 1
                probes.extend([
                    (f"false_fusion_{stem}_provider_api", fusion_review["provider_context_refresh"], false_provider_api, fusion_source),
                    (f"false_fusion_{stem}_provider_tests", fusion_review["provider_context_refresh"], false_provider_tests, fusion_source),
                    (f"false_fusion_{stem}_provider_consumer", fusion_review["provider_context_refresh"], false_provider_consumer, fusion_source),
                    (f"false_fusion_{stem}_provider_composition", fusion_review["provider_context_refresh"], false_provider_test_count, fusion_source),
                ])
            if "consumer_context_refresh" in fusion_review:
                def false_tests(value):
                    value["tests_unchanged"] = False
                def false_signature(value):
                    value["public_signatures"]["su2_level"] = "pub fn su2_level()"
                probes.extend([
                    (f"false_fusion_{stem}_consumer_tests", fusion_review["consumer_context_refresh"], false_tests, fusion_source),
                    (f"false_fusion_{stem}_consumer_signature", fusion_review["consumer_context_refresh"], false_signature, fusion_source),
                ])
    scalar_key = "code/rust/src/fusion_categories/scalar.rs"
    if scalar_key in registry:
        scalar_source = checks.ROOT / scalar_key
        scalar_review = original_load(registry[scalar_key])
        def missing_macro(value):
            value["invocations"].pop()
        def wrong_macro_argument(value):
            value["invocations"][0]["order"] = "2"
        probes.extend([
            ("missing_scalar_macro_impl", scalar_review["macro_review"], missing_macro, scalar_source),
            ("wrong_scalar_macro_argument", scalar_review["macro_review"], wrong_macro_argument, scalar_source),
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
    for stem in ("lib", "mod", "fusion_ring", "scalar", "error", "braid_group", "yang_baxter", "catalog", "modular", "su2_level", "fusion_category"):
        fusion_source = checks.ROOT / f"code/rust/src/fusion_categories/{stem}.rs"
        if fusion_source.relative_to(checks.ROOT).as_posix() in registry:
            record, _ = checks.reviewed(fusion_source)
            expected = {"fusion_ring":"L4A", "scalar":"L3A", "braid_group":"L4A", "yang_baxter":"L4A", "catalog":"L4A", "modular":"L4A", "su2_level":"L4A", "fusion_category":"L4A"}.get(stem,"L1A")
            assert record[1]["score_token"] == expected
            cases.append({"control": f"unaltered_fusion_{stem}", "expected": "pass", "observed": expected})
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    output = checks.ROOT / "evidence/quality/six_module" / (stamp + "-review-controls.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    value = {"AuthorityEffect": "None", "checked_at": datetime.now(timezone.utc).isoformat(),
        "runner_sha256": checks.sha(Path(__file__)), "review_verifier_sha256": checks.sha(Path(checks.__file__)),
        "provider_context_verifier_sha256": checks.sha(checks.HERE / "context_refresh.py"),
        "scope": "In-memory decoded-value controls after validating the original outer reference digests; no artifact bytes edited.",
        "checks": cases}
    with output.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(value, indent=2) + "\n")
    print(f"{len(probes)} semantic false-evidence controls refused; the unaltered L4A review passes")
    print("Receipt:", output)


if __name__ == "__main__":
    main()
