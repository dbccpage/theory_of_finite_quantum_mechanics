"""test_bench_openrouter_meron_2d.py: Test suite for 2D Meron OpenRouter Benchmark.

AuthorityEffect: None.

Verifies:
1. Benchmark prompt generation and lexical hygiene for 4 stages across zero-shot and few-shot conditions.
2. Candidate wire extraction from raw and conversational LLM responses.
3. Model response generation and provider response body hashing.
4. Full benchmark execution (24 evaluations) and metric aggregation over exact Fraction.
5. Master receipt emission and cryptographic SHA-256 digest recomputation.
6. Zero floating-point constants and calls (AST static audit).
"""

from __future__ import annotations

import ast
import hashlib
import json
import os
import sys
from pathlib import Path

DEMOS_DIR = Path(__file__).resolve().parent.parent
CODE_DIR = DEMOS_DIR.parent / "code"
REPO_ROOT = DEMOS_DIR
for p in DEMOS_DIR.parents:
    if (p / "omega_engine_pfp").exists():
        REPO_ROOT = p
        break

if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))
if str(DEMOS_DIR / "code") not in sys.path:
    sys.path.insert(0, str(DEMOS_DIR / "code"))
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from bench_openrouter_meron_2d import (  # noqa: E402
    MODELS_TO_BENCHMARK,
    build_benchmark_prompts,
    evaluate_model_turn,
    extract_wire_from_response,
    generate_mock_model_response,
    run_2d_meron_benchmark,
)
from demo_2d_gross_neveu_meron import validate_wire_string  # noqa: E402
from omega_engine_pfp.domain.tower.parser import GAMMA_38  # noqa: E402

from blind_problem import assert_lexical_hygiene  # noqa: E402

# ============================================================================
# Test Suite 1: Benchmark Prompts & Lexical Hygiene
# ============================================================================


class TestBenchmarkPromptsAndLexicalHygiene:
    """Verifies prompt generation across stages and strict claim hygiene."""

    def test_prompts_count_and_stages(self) -> None:
        """Benchmark builds 4 stages matching 2D Gross-Neveu turns."""
        turns = build_benchmark_prompts()
        assert len(turns) == 4
        expected_stages = [
            "PLAQUETTE_BREAKUP",
            "MEASURE_HOLONOMY",
            "LIFT_REQUEST",
            "EXACT_REPAIR",
        ]
        assert [t["stage"] for t in turns] == expected_stages

    def test_prompts_pass_lexical_hygiene(self) -> None:
        """All zero-shot and few-shot prompts pass blind problem lexical hygiene."""
        turns = build_benchmark_prompts()
        for t in turns:
            assert_lexical_hygiene(t["zero_shot_prompt"])
            assert_lexical_hygiene(t["few_shot_prompt"])

    def test_expected_wires_are_valid_gamma38(self) -> None:
        """Every expected wire string is 100% valid under validate_wire_string."""
        turns = build_benchmark_prompts()
        for t in turns:
            wire = t["expected_wire"]
            assert all(c in GAMMA_38 for c in wire)
            assert validate_wire_string(wire) is True


# ============================================================================
# Test Suite 2: Wire Extraction & Validation
# ============================================================================


class TestWireExtractionAndValidation:
    """Verifies extraction of Gamma38 wire packets from model outputs."""

    def test_extract_exact_raw_wire(self) -> None:
        """Direct wire output is extracted cleanly."""
        raw = "op<<1100><liftreq>>"
        extracted = extract_wire_from_response(raw)
        assert extracted == "op<<1100><liftreq>>"

    def test_extract_embedded_wire_from_prose(self) -> None:
        """Wire embedded inside reasoning prose is isolated and validated."""
        text = "Based on the calculation, the lift request is: op<<1100><liftreq>> and should be authorized."
        extracted = extract_wire_from_response(text)
        assert extracted == "op<<1100><liftreq>>"

    def test_rejects_corrupted_wire(self) -> None:
        """Corrupted wire with illegal uppercase characters returns None."""
        bad_text = "op<<1100><LIFTREQ>>"
        assert extract_wire_from_response(bad_text) is None

    def test_rejects_empty_or_whitespace_text(self) -> None:
        """Empty or blank response returns None."""
        assert extract_wire_from_response("") is None
        assert extract_wire_from_response("   \n\t  ") is None


# ============================================================================
# Test Suite 3: Mock Response Generation & Hashing
# ============================================================================


class TestMockResponseGeneration:
    """Verifies synthetic model response generation and provider body integrity."""

    def test_space_bunny_reasoning_tokens(self) -> None:
        """Space Bunny Alpha response includes reasoning tokens."""
        turns = build_benchmark_prompts()
        resp = generate_mock_model_response(
            model_id="stealth/space-bunny-alpha",
            prompt=turns[2]["few_shot_prompt"],
            turn_spec=turns[2],
            condition="few_shot",
        )
        usage = resp["usage"]
        assert usage["completion_tokens_details"]["reasoning_tokens"] > 0
        assert resp["client_latency_ms"] > 0
        assert "_raw_provider_body_sha256" in resp

    def test_llama_responses_conform_to_provider_schema(self) -> None:
        """Llama models return valid provider choice structures."""
        turns = build_benchmark_prompts()
        resp = generate_mock_model_response(
            model_id="meta-llama/llama-3.3-70b-instruct",
            prompt=turns[3]["zero_shot_prompt"],
            turn_spec=turns[3],
            condition="zero_shot",
        )
        assert len(resp["choices"]) == 1
        assert "content" in resp["choices"][0]["message"]


# ============================================================================
# Test Suite 4: Full Benchmark Runner & Receipt Integrity
# ============================================================================


class TestBenchmarkRunnerAndReceipt:
    """Verifies end-to-end benchmark execution and cryptographic receipt."""

    def test_evaluate_single_turn_metrics(self) -> None:
        """evaluate_model_turn correctly calculates match and opcode flags."""
        turns = build_benchmark_prompts()
        model = MODELS_TO_BENCHMARK[0]
        res = evaluate_model_turn(model, turns[0], "few_shot", live=False, api_key=None)

        assert res["model_id"] == model["id"]
        assert res["turn"] == 1
        assert res["is_wire_valid"] is True
        assert res["opcode_hit"] is True
        assert res["is_exact_match"] is True
        assert isinstance(res["latency_ms"], int)

    def test_full_benchmark_receipt_and_digest(self, tmp_path: Path) -> None:
        """Full benchmark executes 24 turns and emits SHA-256 verified receipt."""
        out_receipt = str(tmp_path / "test_benchmark_receipt.json")
        data = run_2d_meron_benchmark(live=False, api_key=None, output_receipt=out_receipt)

        assert os.path.exists(out_receipt)
        assert data["metrics_summary"]["total_evaluations"] == 24
        assert data["metrics_summary"]["valid_wire_count"] == 24
        assert data["metrics_summary"]["wire_validity_rate"] == "1"

        # Verify SHA-256 digest recomputation
        with open(out_receipt, "r", encoding="utf-8") as f:
            disk_data = json.load(f)

        embedded = disk_data.pop("sha256_digest")
        ser = json.dumps(disk_data, indent=2, sort_keys=True)
        recomp = hashlib.sha256(ser.encode("utf-8")).hexdigest()
        assert embedded == recomp


# ============================================================================
# Test Suite 5: Zero Floats AST Static Audit
# ============================================================================


class TestZeroFloatsASTStaticAudit:
    """Verifies that bench_openrouter_meron_2d contains 0 float literals or calls."""

    def test_source_code_has_zero_floats(self) -> None:
        src_path = DEMOS_DIR / "code" / "bench_openrouter_meron_2d.py"
        assert src_path.exists()
        tree = ast.parse(src_path.read_text(encoding="utf-8"))

        for node in ast.walk(tree):
            if isinstance(node, ast.Constant):
                assert type(node.value) is not float, f"Float literal found: {node.value}"
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    assert node.func.id != "float", "Call to built-in float() found"
