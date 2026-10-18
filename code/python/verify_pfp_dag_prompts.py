"""Standalone verifier for all 35 PFP operad-mined DAG prompts, receipts, and updated papers.

AuthorityEffect: None.
"""

from __future__ import annotations

import json
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]


def verify_all_35_pfp_dag_prompts() -> dict[str, object]:
    prompts_dir = REPO_ROOT / "dag" / "prompts"
    receipts_dir = REPO_ROOT / "evidence" / "receipts" / "pfp_dag_prompts"
    dossier_path = REPO_ROOT / "evidence" / "dossiers" / "pfp_dag_prompts_campaign.md"

    prompt_files = sorted(prompts_dir.glob("*.yaml"))
    if len(prompt_files) != 35:
        raise AssertionError(f"Expected 35 prompt files, found {len(prompt_files)}")

    verified_nodes: list[str] = []
    shadow_sum = 0
    counter_sum = 0
    updated_papers_set: set[str] = set()

    for pf in prompt_files:
        doc = yaml.safe_load(pf.read_text(encoding="utf-8"))
        node_id = doc["dag_node"]["node_id"]
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
        shadow_sum += int(reply["finite_shadow_witness_int"])
        counter_sum += int(reply["countermodel_witness_int"])

        for pref in rcpt["updated_papers"]:
            p_path = REPO_ROOT / pref
            if not p_path.exists():
                raise AssertionError(f"Missing paper {p_path}")
            txt = p_path.read_text(encoding="utf-8")
            header = f"## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`{node_id}`)"
            if header not in txt:
                raise AssertionError(f"Missing receipt section in {pref} for {node_id}")
            updated_papers_set.add(pref)

        verified_nodes.append(node_id)

    if shadow_sum != 2540 or counter_sum != 921:
        raise AssertionError(f"Unexpected witness sums: shadow={shadow_sum}, counter={counter_sum}")
    if not dossier_path.exists():
        raise AssertionError(f"Missing campaign dossier {dossier_path}")

    return {
        "status": "PASS",
        "verified_prompts_count": len(verified_nodes),
        "shadow_witness_sum": shadow_sum,
        "countermodel_witness_sum": counter_sum,
        "distinct_papers_updated": len(updated_papers_set),
    }


if __name__ == "__main__":
    res = verify_all_35_pfp_dag_prompts()
    print(json.dumps(res, indent=2))
