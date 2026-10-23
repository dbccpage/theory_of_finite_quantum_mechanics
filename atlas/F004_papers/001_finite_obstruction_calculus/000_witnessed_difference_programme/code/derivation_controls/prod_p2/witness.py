from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

_REPO_ROOT = next(p for p in Path(__file__).resolve().parents if (p / ".git").exists())
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from omega_engine_cognitive_operations.infrastructure.wdp_provenance_output_gate_adapter import (
    WdpProvenanceOutputGateAdapter,
)
from omega_engine_cognitive_operations.use_cases.provenance_output_gate import (
    ProvenanceMeasurementRequest,
    evaluate_provenance_output_gate,
)


def witness() -> dict[str, object]:
    adapter = WdpProvenanceOutputGateAdapter()

    valid_req = ProvenanceMeasurementRequest(
        sensor_id="sensor",
        sample_id="sample",
        indication=2,
        reported_display=-13,
        stated_uncertainty=Fraction(7, 5),
    )
    ok_res = evaluate_provenance_output_gate(valid_req, adapter)
    assert ok_res.is_ok()
    payload = ok_res.unwrap()

    bad_unc_req = ProvenanceMeasurementRequest(
        sensor_id="sensor",
        sample_id="sample",
        indication=2,
        reported_display=-13,
        stated_uncertainty=Fraction(-1, 10),
    )
    bad_unc_res = evaluate_provenance_output_gate(bad_unc_req, adapter)

    bad_key_req = ProvenanceMeasurementRequest(
        sensor_id="sensor",
        sample_id="sample",
        indication=2,
        reported_display=-13,
        stated_uncertainty=Fraction(7, 5),
        indication_key="missing_key",
    )
    bad_key_res = evaluate_provenance_output_gate(bad_key_req, adapter)

    return {
        "goal_id": "PROD-P2",
        "runtime_package": "omega_engine_cognitive_operations",
        "stage": payload["stage"],
        "replay_verified": payload["replay_verified"],
        "negative_uncertainty_refused": bad_unc_res.is_err(),
        "unmapped_key_refused": bad_key_res.is_err(),
        "authority_effect": payload["authority_effect"],
    }


if __name__ == "__main__":
    print(json.dumps(witness(), indent=2, sort_keys=True))
