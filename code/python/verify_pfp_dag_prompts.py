"""Standalone verifier for all 177 PFP operad-mined DAG prompts (`1..177`),
177 PFP verification receipts, 142 paired M3 decoy ablation receipts (`36..177`), and updated papers.

AuthorityEffect: None.
"""

from __future__ import annotations

import json
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]


def verify_all_35_pfp_dag_prompts() -> dict[str, object]:
    """Verify the first 35 DAG prompts (`1..35`), the remaining 142 DAG prompts (`36..177`), and all 177 receipts."""
    prompts_dir = REPO_ROOT / "dag" / "prompts"
    receipts_dir = REPO_ROOT / "evidence" / "receipts" / "pfp_dag_prompts"
    ablation_dir = REPO_ROOT / "evidence" / "receipts" / "pfp_m3_ablation"
    dossier_path = REPO_ROOT / "evidence" / "dossiers" / "pfp_dag_prompts_campaign.md"
    ablation_report_path = REPO_ROOT / "evidence" / "dossiers" / "pfp_142_remaining_nodes_m3_ablation_report.md"
    ablation_summary_path = REPO_ROOT / "evidence" / "receipts" / "pfp_142_remaining_nodes_m3_ablation_summary.json"

    yaml_files = sorted(prompts_dir.glob("*.yaml"))
    if len(yaml_files) != 177:
        raise AssertionError(f"Expected 177 YAML prompt files, found {len(yaml_files)}")

    verified_nodes_35: list[str] = []
    verified_nodes_142: list[str] = []
    shadow_sum_35 = 0
    counter_sum_35 = 0
    shadow_sum_142 = 0
    counter_sum_142 = 0
    without_m3_pass = 0
    with_m3_a1_pass = 0
    with_m3_final_pass = 0
    updated_papers_set: set[str] = set()

    for pf in yaml_files:
        doc = yaml.safe_load(pf.read_text(encoding="utf-8"))
        node_id = doc["dag_node"]["node_id"]
        idx = int(doc["dag_node"]["prompt_index"])
        slots = doc["operad_slots"]
        for k in (
            "slot_m1_layer0_ambient_carrier",
            "slot_m2_layer1_forward_morphisms",
            "slot_m3_layer2_ideals_and_annihilators",
            "slot_m4_tri_language_witness_anchors",
        ):
            if slots[k]["mining_status"] != "FILLED_BY_4MISSION_MINER":
                raise AssertionError(f"{node_id} slot {k} not filled")

        rcpt_path = receipts_dir / f"{node_id}_pfp_receipt.json"
        if not rcpt_path.exists():
            raise AssertionError(f"Missing receipt {rcpt_path}")
        rcpt = json.loads(rcpt_path.read_text(encoding="utf-8"))
        if not rcpt["gate_receipt"]["all_gates_passed"] or rcpt["gate_receipt"]["status"] != "PASS":
            raise AssertionError(f"Receipt for {node_id} did not pass all gates")

        reply = rcpt["typed_model_response"]
        s_val = int(reply["finite_shadow_witness_int"])
        c_val = int(reply["countermodel_witness_int"])

        for pref in rcpt["updated_papers"]:
            p_path = REPO_ROOT / pref
            if not p_path.exists():
                raise AssertionError(f"Missing paper {p_path}")
            txt = p_path.read_text(encoding="utf-8")
            header = f"## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`{node_id}`)"
            if header not in txt:
                raise AssertionError(f"Missing receipt section in {pref} for {node_id}")
            updated_papers_set.add(pref)

        if idx <= 35:
            shadow_sum_35 += s_val
            counter_sum_35 += c_val
            verified_nodes_35.append(node_id)
        else:
            shadow_sum_142 += s_val
            counter_sum_142 += c_val
            verified_nodes_142.append(node_id)
            ab_path = ablation_dir / f"{node_id}_m3_ablation.json"
            if not ab_path.exists():
                raise AssertionError(f"Missing M3 ablation receipt {ab_path}")
            ab = json.loads(ab_path.read_text(encoding="utf-8"))
            if ab["without_m3_attempt1"]["all_gates_passed"]:
                without_m3_pass += 1
            if ab["with_m3_attempt1"]["all_gates_passed"]:
                with_m3_a1_pass += 1
            if ab["with_m3_final"]["all_gates_passed"]:
                with_m3_final_pass += 1

    if len(verified_nodes_35) != 35 or len(verified_nodes_142) != 142:
        raise AssertionError(
            f"Unexpected partition counts: {len(verified_nodes_35)} and {len(verified_nodes_142)}"
        )
    if shadow_sum_35 != 2540 or counter_sum_35 != 921:
        raise AssertionError(f"Unexpected 35-node witness sums: shadow={shadow_sum_35}, counter={counter_sum_35}")
    if shadow_sum_142 != 63620 or counter_sum_142 != 16885:
        raise AssertionError(f"Unexpected 142-node witness sums: shadow={shadow_sum_142}, counter={counter_sum_142}")

    shadow_sum_177 = shadow_sum_35 + shadow_sum_142
    counter_sum_177 = counter_sum_35 + counter_sum_142
    if shadow_sum_177 != 66160 or counter_sum_177 != 17806:
        raise AssertionError(f"Unexpected 177-node witness sums: shadow={shadow_sum_177}, counter={counter_sum_177}")

    if not dossier_path.exists() or not ablation_report_path.exists() or not ablation_summary_path.exists():
        raise AssertionError("Missing campaign or ablation dossier files")

    return {
        "status": "PASS",
        "verified_prompts_35_count": len(verified_nodes_35),
        "verified_prompts_142_count": len(verified_nodes_142),
        "verified_prompts_total_177": len(verified_nodes_35) + len(verified_nodes_142),
        "shadow_witness_sum_35": shadow_sum_35,
        "countermodel_witness_sum_35": counter_sum_35,
        "shadow_witness_sum_142": shadow_sum_142,
        "countermodel_witness_sum_142": counter_sum_142,
        "shadow_witness_sum_177": shadow_sum_177,
        "countermodel_witness_sum_177": counter_sum_177,
        "m3_ablation_without_m3_attempt1_pass": without_m3_pass,
        "m3_ablation_with_m3_attempt1_pass": with_m3_a1_pass,
        "m3_ablation_with_m3_final_pass": with_m3_final_pass,
        "distinct_papers_updated": len(updated_papers_set),
    }


if __name__ == "__main__":
    res = verify_all_35_pfp_dag_prompts()
    print(json.dumps(res, indent=2))
