from __future__ import annotations
"""Step 5 — cohomology, density, improvement receipt."""


import json
from pathlib import Path

import numpy as np
import pytest

from omega_engine.crates.runtime.rt_prompt_diagnosis import PromptDiagnosisEngine
from omega_engine.crates.pipeline.prompt_improvement import (
    DisclosurePolicy,
    PromptImprovementPipeline,
)
from omega_engine.crates.runtime.prompt_receipt_store import (
    load_receipt_json,
    write_receipt_json,
    write_receipt_yaml,
)


def test_d1_d0_zero_and_phi1() -> None:
    eng = PromptDiagnosisEngine()
    d = eng.diagnose("Must A.\nMust not B.\nAlways do C.")
    assert d.cohomology.d1_d0_zero is True
    assert d.cohomology.phi1_before >= 0
    assert d.cohomology.mapping_version.startswith("omega.prompt_cochain")


def test_density_trace_hermitian_psd() -> None:
    eng = PromptDiagnosisEngine(density_budget=32)
    d = eng.diagnose("clause one. clause two. clause three.")
    dens = d.density
    assert dens.budget_status == "OK"
    assert abs(dens.trace - 1.0) < 1e-9
    assert dens.hermiticity_error < 1e-12
    assert dens.psd is True
    assert dens.min_eigenvalue >= -1e-12
    mat = np.array(
        [[complex(re, im) for re, im in row] for row in dens.matrix],
        dtype=complex,
    )
    assert mat.shape == (dens.dimension, dens.dimension)


def test_budget_exceeded() -> None:
    eng = PromptDiagnosisEngine(density_budget=2)
    text = "\n".join(f"clause {i} must stay." for i in range(20))
    d = eng.diagnose(text)
    if d.cohomology.c1_dim > 2:
        assert d.density.budget_status in {"OK", "BUDGET_EXCEEDED"}
        if d.cohomology.c1_dim > eng.density_budget:
            assert d.density.budget_status == "BUDGET_EXCEEDED"
            assert d.density.matrix == tuple()


def test_full_text_only_when_requested(tmp_path: Path) -> None:
    secret = "MUST keep secret canary TOKEN_XYZ"
    pipe = PromptImprovementPipeline()
    hash_only = pipe.improve(secret, include_text=False)
    full = pipe.improve(secret, include_text=True)
    assert hash_only.contains_raw_text is False
    assert full.contains_raw_text is True
    assert secret not in json.dumps(hash_only.payload)
    assert secret in full.payload["original"]["text"]
    assert full.disclosure_policy is DisclosurePolicy.EXPLICIT_LOCAL_FULL_TEXT
    assert full.exportable is False
    assert full.authority_effect == "None"
    path = write_receipt_json(tmp_path, full.receipt_sha256, full.payload)
    loaded = load_receipt_json(path)
    assert (
        loaded.get("receipt_blake3") or loaded.get("receipt_sha256")
    ) == full.receipt_sha256


def test_yaml_roundtrip_preserves_hash(tmp_path: Path) -> None:
    pipe = PromptImprovementPipeline()
    receipt = pipe.improve("Must X.\nMust not Y.", include_text=True)
    ypath = write_receipt_yaml(tmp_path, receipt.receipt_sha256, receipt.payload)
    import yaml

    parsed = yaml.safe_load(ypath.read_text(encoding="utf-8"))
    clean = {
        k: v for k, v in parsed.items() if k not in {"receipt_sha256", "receipt_blake3"}
    }
    from omega_engine_pfp.domain import digest_payload

    assert digest_payload(clean) == receipt.receipt_sha256


def test_tamper_receipt_rejected(tmp_path: Path) -> None:
    pipe = PromptImprovementPipeline()
    receipt = pipe.improve("prompt", include_text=False)
    path = write_receipt_json(tmp_path, receipt.receipt_sha256, receipt.payload)
    data = json.loads(path.read_text(encoding="utf-8"))
    data["terminal"]["status"] = "TAMPER"
    path.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ValueError, match="tamper"):
        load_receipt_json(path)


def test_intent_preservation_failure() -> None:
    eng = PromptDiagnosisEngine()
    original = eng.diagnose(
        "Must preserve uniqueness.\nOther stuff.",
        retain_clause_text=True,
    )
    improved = eng.diagnose("Other stuff only.", retain_clause_text=True)
    cmp = eng.compare(original, improved)
    assert cmp["intent_preservation"]["passed"] is False
    assert cmp["criteria_passed"] is False


def test_no_cot_field_in_receipt() -> None:
    pipe = PromptImprovementPipeline()
    receipt = pipe.improve("solve this", include_text=True)
    blob = json.dumps(receipt.payload).casefold()
    assert "chain_of_thought" not in blob
    assert "hidden_cot" not in blob


def test_improvement_public_api_preserves_must() -> None:
    pipe = PromptImprovementPipeline()
    text = "Must write tests.\nDo the work."
    receipt = pipe.improve(text, include_text=True)
    improved = receipt.payload["improvement"]["text"]
    assert "Must write tests" in improved or "must write tests" in improved.casefold()




