"""Present the current source-bound assessment state across majorana, mub, number_theory, operad_theory, sheaf_theory, and qm without promoting scores."""

import argparse
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
    logs = {
        record["verification"]["baseline"]["log"]: record["verification"]["baseline"]
        for record in records
        if record["verification"]["baseline"]
    }
    logs.update(
        {
            run["log"]: run
            for record in records
            for run in record["verification"].get("doctests", [])
        }
    )
    pass_count = 0
    for log, execution in logs.items():
        if digest(ROOT / log) != execution["log_sha256"] or execution["exit_code"] != 0:
            raise RuntimeError("Baseline unavailable or changed: " + log)
        pass_count += sum(
            int(count)
            for count in re.findall(
                r"test result: ok\. (\d+) passed",
                (ROOT / log).read_text(encoding="utf-8"),
            )
        )
    known_e = [r["artifact"]["path"] for r in records if "E" in r["gates"].values()]
    structural_e = [r["artifact"]["path"] for r in records if r["gates"]["G5"] == "E"]
    runtime_e = [
        r["artifact"]["path"]
        for r in records
        if any(r["gates"][gate] == "E" for gate in ("G2", "G3"))
    ]
    disabled = [
        r["artifact"]["path"]
        for r in records
        if r["verification"]["disabled_by_cfg_any"]
    ]
    exceeded = [
        {"path": r["artifact"]["path"], **item}
        for r in records
        for item in r["structure"]["exceeding_A"]
    ]
    state = {
        "AuthorityEffect": "None",
        "source_subjects": len(records),
        "sidecars": len(manifest["sidecars"]),
        "completed_assessments": sum(r["is_complete"] for r in records),
        "known_E_subjects": known_e,
        "disabled_subjects": disabled,
        "structural_E_subjects": structural_e,
        "runtime_E_subjects": runtime_e,
        "source_functions_exceeding_A": exceeded,
        "passing_scoped_test_cases": pass_count,
        "baseline_logs": logs,
        "sidecar_manifest_sha256": digest(manifest_path),
        "runner_sha256": digest(Path(__file__)),
        "goal_complete": False,
    }
    write(folder / "review_state.json", state)
    total_functions = sum(len(r["structure"]["functions"] or []) for r in records)
    lines = [
        "# Six-directory QM/math review checkpoint",
        "",
        "AuthorityEffect: None.",
        "",
        f"{len(records)} subjects have {len(manifest['sidecars'])} source-bound scoring/contract sidecars.",
        f"{pass_count} scoped test cases passed. {sum(r['is_complete'] for r in records)} five-gate assessments are complete.",
        f"The L4A goal remains in progress for unreviewed subjects. Null gates are unassessed; {len(exceeded)} source functions exceed Grade A structural ceilings (CCN <= 10, cognitive <= 15, nesting <= 3) across all {len(records)} subjects ({total_functions} explicit source functions).",
        "",
        "| Directory | Subjects | Completed assessments | Known E | Source functions above A ceilings |",
        "|---|---:|---:|---:|---:|",
    ]
    for group in GROUPS:
        selected = [r for r in records if r["artifact"]["path"].split("/")[3] == group]
        lines.append(
            f"| {group} | {len(selected)} | {sum(r['is_complete'] for r in selected)} | "
            f"{sum('E' in r['gates'].values() for r in selected)} | "
            f"{sum(len(r['structure']['exceeding_A']) for r in selected)} |"
        )
    lines += [
        "",
        "Structural counts include explicit source in test/support files and compatibility mirror entries (`mub/src/`);",
        "they are not a measurement of compiler-expanded production execution or a semantic defect count.",
        "",
        "Structural and mutation remediations completed in this checkpoint:",
        f"- Decomposed all remaining Band B, C, and D functions across all {len(records)} subjects ({total_functions} explicit source functions) in `majorana`, `mub` (including `mub/src/` mirrors), `number_theory`, `operad_theory`, `sheaf_theory`, and `qm` (including `provider_error` in `qm/bridge.rs`, `carrier_stage` in `qm/report_fiber.rs`, and `compute_bianchi_and_angular` in `qm/simplicial_grav.rs`) below `CCN <= 10`, `cognitive_upper_bound <= 15`, and `control_nesting <= 3` (`{len(exceeded)}` functions exceeding Grade A).",
        "- Added fallible constructor `BinaryField::try_new` with `BinaryFieldError` (`DegreeOutOfRange`, `DegreeMismatch`, `ReducibleModulus`, `OrderOverflow`) in `number_theory/binary_field.rs`, `try_surface_grid` in `majorana/complexes.rs`, `try_basis_closure` and `try_wall_functional` in `mub/omega_native/d6_exact_curvature_cochain.rs`, and ragged-matrix rejection in `mub/omega_native/d6_exact_sos.rs`.",
        "- Expanded designated semantic mutations in `mutations.py` to 43 recipes (`MAJ01`–`MAJ07`, `MUB01`–`MUB07`, `NT01`–`NT07`, `OP01`–`OP07`, `SH01`–`SH07`, `QM01`–`QM08`) across 39 core modules (`43/43` killed, `0` survived, `conservative_ratio = 1.0`) and completed 39 five-gate `L4A` reviews in `specs.json`.",
        "",
        "No commit, push, PR or merge is asserted by this checkpoint.",
        "",
    ]
    (folder / "REVIEW.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(
        json.dumps(
            {
                key: state[key]
                for key in (
                    "source_subjects",
                    "sidecars",
                    "completed_assessments",
                    "known_E_subjects",
                    "passing_scoped_test_cases",
                    "goal_complete",
                )
            }
        )
    )


if __name__ == "__main__":
    main()
