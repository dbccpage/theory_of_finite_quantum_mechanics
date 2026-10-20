"""Present the current source-bound assessment state without promoting scores."""

import argparse
from collections import Counter
import json
from pathlib import Path
import re

from replay import ROOT, GROUPS, digest, write


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    folder = args.receipt.resolve().parent
    manifest_path = folder / "sidecars.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    records = []
    for entry in manifest["sidecars"]:
        path = ROOT / entry["path"]
        if digest(path) != entry["sha256"]:
            raise RuntimeError("Changed sidecar: " + str(path))
        if path.name.endswith(".scoring.yaml"):
            records.append(json.loads(path.read_text(encoding="utf-8").split("\n", 1)[1]))
    logs = {record["verification"]["baseline"]["log"]: record["verification"]["baseline"]
            for record in records if record["verification"]["baseline"]}
    logs.update({run["log"]: run for record in records
                 for run in record["verification"].get("doctests", [])})
    pass_count = 0
    for log, execution in logs.items():
        if digest(ROOT / log) != execution["log_sha256"] or execution["exit_code"] != 0:
            raise RuntimeError("Baseline unavailable or changed: " + log)
        pass_count += sum(int(count) for count in re.findall(
            r"test result: ok\. (\d+) passed", (ROOT / log).read_text(encoding="utf-8")))
    known_e = [r["artifact"]["path"] for r in records if "E" in r["gates"].values()]
    structural_e = [r["artifact"]["path"] for r in records if r["gates"]["G5"] == "E"]
    runtime_e = [r["artifact"]["path"] for r in records if any(r["gates"][gate] == "E" for gate in ("G2", "G3"))]
    disabled = [r["artifact"]["path"] for r in records if r["verification"]["disabled_by_cfg_any"]]
    exceeded = [{"path": r["artifact"]["path"], **item} for r in records for item in r["structure"]["exceeding_A"]]
    # A production fault may also calibrate its allocation-observer test file.
    # Count each campaign execution once, rather than double-counting records
    # that explicitly share composition evidence under SCORING.md 3.4.
    campaigns, unique_faults = {}, {}
    for record in records:
        reference = record["verification"].get("mutation_campaign")
        if reference is None:
            continue
        key = reference["path"]
        if key not in campaigns:
            path = ROOT / key
            if digest(path) != reference["sha256"]:
                raise RuntimeError("Changed mutation campaign")
            receipt = json.loads(path.read_text(encoding="utf8"))
            entries_path = path.parent / "mutations.json"
            if digest(entries_path) != receipt["mutations_sha256"]:
                raise RuntimeError("Changed mutation outcomes")
            entries = json.loads(entries_path.read_text(encoding="utf8"))
            campaigns[key] = {entry["id"]: entry for entry in entries}
            if len(campaigns[key]) != len(entries):
                raise RuntimeError("Duplicate mutation IDs")
        for identity in record["verification"].get("designated_mutations", []):
            unique_faults[(key, identity)] = campaigns[key][identity]["outcome"]
    counts = Counter(unique_faults.values())
    outcomes = {name: counts[name] for name in
                ("killed", "survived", "demonstrably_equivalent", "invalid", "inconclusive", "unrun")}
    denominator = sum(outcomes[name] for name in ("killed", "survived", "inconclusive", "unrun"))
    outcomes["conservative_ratio"] = outcomes["killed"] / denominator if denominator else None
    consumer_receipts = {item["receipt"]["path"]: item["receipt"]["sha256"]
        for record in records for item in record["verification"].get("composition_runs", [])}
    consumer_logs = {}
    for name, expected in consumer_receipts.items():
        if digest(ROOT / name) != expected:
            raise RuntimeError("Changed consumer receipt: " + name)
        consumer = json.loads((ROOT / name).read_text(encoding="utf8"))
        for run in consumer.get("runs", [consumer["run"]]):
            if run["exit_code"] != 0 or run.get("timed_out") or digest(ROOT / run["log"]) != run["log_sha256"]:
                raise RuntimeError("Changed or failed selected consumer run")
            consumer_logs[run["log"]] = run
    consumer_count = sum(sum(map(int, re.findall(r"test result: ok\. (\d+) passed",
        (ROOT / name).read_text(encoding="utf8")))) for name in consumer_logs)
    state = {"AuthorityEffect": "None", "source_subjects": len(records), "sidecars": len(manifest["sidecars"]),
             "capability_counts": dict(Counter(r["level"] for r in records)),
             "designated_mutation_accounting": outcomes,
             "completed_assessments": sum(r["is_complete"] for r in records),
             "known_E_subjects": known_e, "disabled_subjects": disabled,
             "structural_E_subjects": structural_e, "runtime_E_subjects": runtime_e,
             "source_functions_exceeding_A": exceeded,
             "passing_scoped_test_cases": pass_count, "baseline_logs": logs,
             "passing_selected_root_consumer_case_executions": consumer_count,
             "selected_root_consumer_receipts": consumer_receipts,
             "sidecar_manifest_sha256": digest(manifest_path), "runner_sha256": digest(Path(__file__)),
             "goal_complete": False}
    write(folder / "review_state.json", state)
    lines = ["# Six-directory review checkpoint", "", "AuthorityEffect: None.", "",
             f"{len(records)} subjects have {len(manifest['sidecars'])} source-bound scoring/contract sidecars.",
             f"{pass_count} scoped test cases passed. {sum(r['is_complete'] for r in records)} five-gate assessments are complete.",
             "The L4A goal remains unfinished. Null gates are unassessed; known E findings remain visible.", "",
             f"Separately, {consumer_count} selected actual-root consumer case executions passed; no full-root or workspace suite success is inferred.", "",
             "Capability counts: " + ", ".join(f"{key}={value}" for key, value in sorted(state["capability_counts"].items())) + ".",
             "An individually reviewed L4 capability does not imply a completed grade A.", "",
             f"Designated faults: {outcomes['killed']} killed, {outcomes['survived']} survived, "
             f"{outcomes['demonstrably_equivalent']} equivalent, {outcomes['invalid']} invalid, "
             f"{outcomes['inconclusive']} inconclusive, {outcomes['unrun']} unrun. R={outcomes['conservative_ratio']}.",
             "Every survivor remains disclosed in the bound campaign; no survivor is silently reclassified as equivalent.",
             "The campaign ratio does not certify every file or all failure classes.", "",
             "| Directory | Subjects | Completed assessments | Known E | Source functions above A ceilings |",
             "|---|---:|---:|---:|---:|"]
    for group in GROUPS:
        selected = [r for r in records if r["artifact"]["path"].split("/")[3] == group]
        lines.append(f"| {group} | {len(selected)} | {sum(r['is_complete'] for r in selected)} | "
                     f"{sum('E' in r['gates'].values() for r in selected)} | "
                     f"{sum(len(r['structure']['exceeding_A']) for r in selected)} |")
    individual = [r for r in records if "engineering_review" in r]
    if individual:
        lines += ["", "Explicit individual gate decisions (null remains unassessed):", "",
                  "| Subject | G1 | G2 | G3 | G4 | G5 | Result |",
                  "|---|---|---|---|---|---|---|"]
        for record in individual:
            gates = " | ".join(record["gates"][gate] or "null" for gate in ("G1", "G2", "G3", "G4", "G5"))
            result = record["score_token"] or "incomplete"
            lines.append(f"| {record['artifact']['path'].removeprefix('code/rust/src/')} | {gates} | {result} |")
        lines += ["", "A completed B assessment remains below the requested A target."]
    lines += ["", "Structural counts include explicit source in disabled/test/support files and compatibility entries;",
              "they are not a measurement of compiler-expanded production execution or a semantic defect count.",
              "", "Established structural E subjects (none if the list is empty):", ""]
    lines += [f"- `{name}`" for name in structural_e]
    lines += ["", "Counterexample controls establish these semantic/failure E subjects:", ""]
    lines += [f"- `{name}`" for name in runtime_e]
    lines += ["", "These files are entirely disabled and still require executable L4 replacements:", ""]
    lines += [f"- `{name}`" for name in disabled]
    lines += ["", "Focused changes cover overflow-free trace comparison, typed rational construction,",
              "LGGR product/witness admission and lazy witness generation, and typed holonomy endpoint failures.",
              "The holonomy matrix now has private admitted storage, typed access/setters/decoding, a sealed Q/Q(i)",
              "scalar domain, borrowed admitted scalar operations, exact elimination and cell/work preflight.",
              "Its independent finite matrix challenges and API privacy doctests are recorded separately from grading.",
              "Root Gaussian components are now private and admitted through checked construction/decoding.",
              "Rational hashing refuses undefined fractions before hasher mutation; homology digest and manifest",
              "APIs propagate typed failures while retaining the existing valid-input byte frames.",
              "The four former CCN E functions have been factored into admitted/validation phases; the rank",
              "certificate identity phase is also factored. Smith workspace admission precedes allocation,",
              "and its extended-Euclid loop is iterative. Sealed differential controls are separate evidence",
              "and are never counted as ordinary production baseline tests.",
              "Sparse vector/dense conversion now admits output and metadata storage before fallible allocation.",
              "Finite binary64 conversion returns a typed refusal for NaN or infinity and preserves supplied binary values.",
              "Zero-rank certificates check M=0 after shape/domain admission and handle huge zero-area metadata directly.",
              "The formerly disabled substitution and quasi-category modules now provide bounded executable APIs:",
              "capture-avoiding finite prefix syntax and nerves of fully admitted finite category tables.",
              "The formerly disabled algebra module now admits strict finite cohomological A-infinity algebras over prime fields,",
              "with full grading, differential-square, signed Leibniz and associativity checks and bounded evaluations.",
              "Their individual gate decisions, independent challenges and remaining execution prerequisites appear above.",
              "`qr` now returns `Result<Q, RationalConstructionError>`. Remaining public graph/connection/scalar",
              "admission, external provider trust, consumer composition, numerical-interface policies,",
              "per-file independent challenges and operational costs still require individual review.",
              "", "No commit, push, PR or merge is asserted by this checkpoint.", ""]
    (folder / "REVIEW.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({key: state[key] for key in ("source_subjects", "sidecars", "completed_assessments",
          "passing_scoped_test_cases", "goal_complete")}))


if __name__ == "__main__":
    main()
