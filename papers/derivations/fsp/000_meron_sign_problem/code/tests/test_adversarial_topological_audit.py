"""test_adversarial_topological_audit.py: Unit tests for Woland prosecution & master receipt.
AuthorityEffect: None.

Comprehensive unit test suite for:
1. Woland Retinue roster (10 characters: Hella, Begemot, Koroviev, Azazello, Woland,
   Margarita, The Master, Intern, Abadonna, Bezdomny).
2. Woland 7-Act dialectical prosecution circuit and individual act verifications.
3. Hostile adversarial mutation battery asserting 100% fail-closed typed refusal (Result::Err / Refusal).
4. Master receipt generation, canonical schema adherence (coda_meron_4d_ladder_receipt.json),
   deterministic SHA-256 hashing, and canonical dual export.
5. Zero-float static AST audit and runtime float rejection.
6. Claim and lexical hygiene conformance.
7. UTF-8 BOM cleanliness.
"""

from __future__ import annotations

import ast
import json
import os
import sys
from pathlib import Path

import pytest

# Ensure code directory and repo root are on path
_CODE_DIR = Path(__file__).resolve().parent.parent
_REPO_ROOT = _CODE_DIR
for p in Path(__file__).resolve().parents:
    if (p / "omega_engine_pfp").exists():
        _REPO_ROOT = p
        break

if str(_CODE_DIR) not in sys.path:
    sys.path.insert(0, str(_CODE_DIR))
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from omega_engine_operations.domain.rop.result import Refusal  # noqa: E402

from adversarial_topological_audit import (  # noqa: E402
    WOLAND_RETINUE,
    MutationSuiteResult,
    RetinueCharacter,
    WolandActRecord,
    WolandDialecticalProsecutor,
    WolandProsecutionResult,
    build_master_receipt_dict,
    execute_hostile_mutation_suite,
    execute_woland_7act_prosecution,
    export_canonical_master_receipts,
    generate_master_receipt,
    mutate_cluster_weight_attack,
    mutate_fermion_sign_attack,
    mutate_gamma38_wire_attack,
    mutate_loop_orientation_attack,
    mutate_second_chern_charge_attack,
    verify_master_receipt_digest,
)
from topological_half_instanton_4d import HalfInstantonCluster4D  # noqa: E402

# ============================================================================
# Test Suite 1: Woland Retinue Character Roster
# ============================================================================


class TestWolandRetinueRoster:
    """Verifies that all 10 canonical retinue characters are formalized with correct operators and maxims."""

    EXPECTED_CHARACTERS = (
        "Hella",
        "Begemot",
        "Koroviev",
        "Azazello",
        "Woland",
        "Margarita",
        "The Master",
        "Intern",
        "Abadonna",
        "Bezdomny",
    )

    def test_all_10_retinue_characters_present(self) -> None:
        """Asserts all 10 characters exist in WOLAND_RETINUE."""
        assert len(WOLAND_RETINUE) == 10
        for name in self.EXPECTED_CHARACTERS:
            assert name in WOLAND_RETINUE, f"Missing character: {name}"

    def test_retinue_character_fields_integrity(self) -> None:
        """Asserts every retinue character has complete, non-empty metadata fields."""
        for name, char in WOLAND_RETINUE.items():
            assert isinstance(char, RetinueCharacter)
            assert char.name == name
            assert char.operator.startswith("E_")
            assert len(char.role_title) > 0
            assert len(char.duty) > 0
            assert len(char.maxim) > 0

    def test_woland_terminal_operator_identity(self) -> None:
        """Asserts Woland is assigned the terminal reality gatekeeper operator E_terminal."""
        woland = WOLAND_RETINUE["Woland"]
        assert woland.operator == "E_terminal"
        assert "Terminal Gatekeeper" in woland.role_title
        assert "Manuscripts don't burn" in woland.maxim


# ============================================================================
# Test Suite 2: Woland 7-Act Dialectical Prosecution Circuit
# ============================================================================


class TestWolandDialecticalProsecutionCircuit:
    """Verifies turn-by-turn progression through all 7 Acts in Woland's prosecution circuit."""

    def test_prosecutor_initialization(self) -> None:
        """Asserts prosecutor initializes with internal cluster solver."""
        prosecutor = WolandDialecticalProsecutor()
        assert prosecutor.solver is not None

    def test_act_1_hygiene_audit_passes_clean_inputs(self) -> None:
        """Act I: Clean wire and defensible problem text pass pre-filter."""
        prosecutor = WolandDialecticalProsecutor()
        wire = "op<<11>op<<101><100><0><1><10><11><100>>op<<0><><0><1>>op<<10010><0><1><10>>>"
        text = "Closed string loops and topological charge cancellation on discrete torus."
        record = prosecutor.run_act_1_hygiene_audit(wire, text)

        assert record.act_number == 1
        assert record.verdict == "PASS"
        assert "Hella" in record.presiding_retinue
        assert "Bezdomny" in record.presiding_retinue
        assert record.details["wire_gamma38_valid"] is True
        assert record.details["lexical_hygiene_clean"] is True

    def test_act_1_hygiene_audit_refuses_corrupted_wire(self) -> None:
        """Act I: Invalid wire token triggers refusal."""
        prosecutor = WolandDialecticalProsecutor()
        corrupted_wire = "op<<11>_INVALID_TOKEN_>>"
        text = "Clean text."
        record = prosecutor.run_act_1_hygiene_audit(corrupted_wire, text)

        assert record.act_number == 1
        assert record.verdict == "REFUSE"
        assert record.details["wire_gamma38_valid"] is False

    def test_act_2_sign_inversion_prosecution(self) -> None:
        """Act II: Inverting odd half-instanton flips sign from -1 to +1."""
        prosecutor = WolandDialecticalProsecutor()
        record = prosecutor.run_act_2_sign_inversion_prosecution()

        assert record.act_number == 2
        assert record.verdict == "PASS"
        assert "Koroviev" in record.presiding_retinue
        assert "Begemot" in record.presiding_retinue
        assert record.details["exact_sign_reversal"] is True
        assert record.details["s_original"] == -1
        assert record.details["s_flipped"] == 1

    def test_act_3_weight_preservation_audit(self) -> None:
        """Act III: Weight symmetry w(tau(C)) == w(C) certifies zero duality gap."""
        prosecutor = WolandDialecticalProsecutor()
        record = prosecutor.run_act_3_weight_preservation_audit()

        assert record.act_number == 3
        assert record.verdict == "PASS"
        assert "Koroviev" in record.presiding_retinue
        assert "Azazello" in record.presiding_retinue
        assert record.details["weight_preserved"] is True
        assert record.details["duality_gap"] == "0"
        assert record.details["exact_zero_sum_doublet"] is True

    def test_act_4_gauge_break_carrier_lift(self) -> None:
        """Act IV: 9-dot dimensional lift measures winding parity, Hopf link, and c_2."""
        prosecutor = WolandDialecticalProsecutor()
        record = prosecutor.run_act_4_gauge_break_carrier_lift()

        assert record.act_number == 4
        assert record.verdict == "PASS"
        assert "Begemot" in record.presiding_retinue
        assert "Margarita" in record.presiding_retinue
        assert record.details["loop_winding_parity"] == 1
        assert abs(record.details["hopf_linking_number"]) == 1
        assert record.details["half_instanton_c2"] == "1/2"

    def test_act_5_doublet_cancellation_trial(self) -> None:
        """Act V: Involution cancellation evaluates odd sum == 0 and Z > 0."""
        prosecutor = WolandDialecticalProsecutor()
        record = prosecutor.run_act_5_doublet_cancellation_trial()

        assert record.act_number == 5
        assert record.verdict == "PASS"
        assert "Margarita" in record.presiding_retinue
        assert "The Master" in record.presiding_retinue
        assert record.details["odd_sectors_cancelled"] == 2
        assert record.details["odd_sum"] == "0"
        assert record.details["zero_sectors_positive"] is True

    def test_act_6_hostile_mutation_battery(self) -> None:
        """Act VI: Mutation battery achieves 100% fail-closed typed refusal."""
        prosecutor = WolandDialecticalProsecutor()
        record = prosecutor.run_act_6_hostile_mutation_battery()

        assert record.act_number == 6
        assert record.verdict == "PASS"
        assert "Azazello" in record.presiding_retinue
        assert "Abadonna" in record.presiding_retinue
        assert "Intern" in record.presiding_retinue
        assert record.details["all_fail_closed"] is True
        assert record.details["refusals"] == record.details["total_mutations"]

    def test_act_7_terminal_adjudication(self) -> None:
        """Act VII: Presided by Woland, confirms all prior acts passed and issues PASS_TO_MASTER."""
        prosecutor = WolandDialecticalProsecutor()
        # Mock 6 passing acts
        acts = [
            WolandActRecord(i, f"Act {i}", ("Actor",), "PASS", {})
            for i in range(1, 7)
        ]
        record = prosecutor.run_act_7_terminal_adjudication(acts)

        assert record.act_number == 7
        assert record.verdict == "PASS"
        assert "Woland" in record.presiding_retinue
        assert record.details["all_prior_acts_passed"] is True
        assert record.details["terminal_label"] == "PASS_TO_MASTER"
        assert record.details["manuscripts_burn"] is False
        assert record.details["duality_gap"] == "0/1"

    def test_full_7act_circuit_execution_pass_to_master(self) -> None:
        """End-to-end circuit runs all 7 acts and returns WolandProsecutionResult."""
        res = execute_woland_7act_prosecution()

        assert isinstance(res, WolandProsecutionResult)
        assert res.all_passed is True
        assert res.verdict == "PASS_TO_MASTER"
        assert res.total_acts == 7
        assert res.passed_acts == 7
        assert res.terminal_duality_gap == "0/1"
        assert res.authority_effect == "None"
        assert len(res.acts) == 7
        for idx, act in enumerate(res.acts, start=1):
            assert act.act_number == idx
            assert act.verdict == "PASS"


# ============================================================================
# Test Suite 3: Hostile Adversarial Mutation Suite
# ============================================================================


class TestHostileAdversarialMutationSuite:
    """Verifies fail-closed resilience against hostile mutations across all 5 vectors."""

    def test_mutation_1_perturbed_fermion_sign_attack(self) -> None:
        """Mutation 1: Perturbed sign produces typed Err(Refusal)."""
        res = mutate_fermion_sign_attack()
        assert res.is_err
        refusal = res.unwrap_err()
        assert isinstance(refusal, Refusal)
        assert refusal.code == "REFUSAL_SIGN_PERTURBED"
        assert "adversarial_topological_audit" in refusal.locus

    def test_mutation_2_perturbed_cluster_weight_attack(self) -> None:
        """Mutation 2: Perturbed weight produces typed Err(Refusal)."""
        res = mutate_cluster_weight_attack()
        assert res.is_err
        refusal = res.unwrap_err()
        assert isinstance(refusal, Refusal)
        assert refusal.code == "REFUSAL_WEIGHT_ASYMMETRY"
        assert "adversarial_topological_audit" in refusal.locus

    def test_mutation_3_corrupted_loop_orientation_attack(self) -> None:
        """Mutation 3: Forcing negative sign on neutral cluster produces Err(Refusal)."""
        res = mutate_loop_orientation_attack()
        assert res.is_err
        refusal = res.unwrap_err()
        assert isinstance(refusal, Refusal)
        assert refusal.code == "REFUSAL_FORCED_ORIENTATION_CORRUPTION"
        assert "adversarial_topological_audit" in refusal.locus

    def test_mutation_4_tampered_second_chern_charge_attack(self) -> None:
        """Mutation 4: Non-half-integer topological charge produces Err(Refusal)."""
        res = mutate_second_chern_charge_attack()
        assert res.is_err
        refusal = res.unwrap_err()
        assert isinstance(refusal, Refusal)
        assert refusal.code == "REFUSAL_NON_HALF_INTEGER_CHARGE"
        assert "adversarial_topological_audit" in refusal.locus

    def test_mutation_5_corrupted_gamma38_wire_attack(self) -> None:
        """Mutation 5: Corrupted wire string produces Err(Refusal)."""
        res = mutate_gamma38_wire_attack()
        assert res.is_err
        refusal = res.unwrap_err()
        assert isinstance(refusal, Refusal)
        assert refusal.code == "REFUSAL_WIRE_LEXICAL_CORRUPTION"
        assert "adversarial_topological_audit" in refusal.locus

    def test_execute_hostile_mutation_suite_all_fail_closed(self) -> None:
        """Asserts entire hostile mutation suite has 100% fail-closed refusal rate."""
        mut_res = execute_hostile_mutation_suite()
        assert isinstance(mut_res, MutationSuiteResult)
        assert mut_res.total_mutations == 5
        assert mut_res.refusals == 5
        assert mut_res.all_fail_closed is True

        expected_codes = {
            "REFUSAL_SIGN_PERTURBED",
            "REFUSAL_WEIGHT_ASYMMETRY",
            "REFUSAL_FORCED_ORIENTATION_CORRUPTION",
            "REFUSAL_NON_HALF_INTEGER_CHARGE",
            "REFUSAL_WIRE_LEXICAL_CORRUPTION",
        }
        assert set(mut_res.rejection_codes) == expected_codes
        assert len(mut_res.refusal_objects) == 5


# ============================================================================
# Test Suite 4: Master Receipt Generator & SHA-256 Hashing
# ============================================================================


class TestMasterReceiptGenerator:
    """Verifies schema adherence, Target T3 & T5 inclusion, and SHA-256 digest determinism."""

    def test_build_master_receipt_dict_structure(self) -> None:
        """Asserts master receipt dictionary contains all required top-level keys."""
        data = build_master_receipt_dict()
        required_keys = {"receipt_version", "title", "verification_summary", "targets"}
        assert required_keys.issubset(set(data.keys()))
        assert data["receipt_version"] == "1.0.0"
        assert data["verification_summary"]["all_verified"] is True
        assert data["verification_summary"]["total_targets"] == 2
        assert data["verification_summary"]["dimensions_covered"] == [3, 4]

    def test_master_receipt_target_t3_parity(self) -> None:
        """Target T3 contains exact rational receipts and Pontryagin invariants."""
        data = build_master_receipt_dict()
        t3 = next(t for t in data["targets"] if t["target_id"] == "T3_3D_MERON_STRINGS_PONTRYAGIN_T3")
        assert t3["dimension"] == 3
        cert = t3["certified_rational_receipt"]
        assert cert["duality_gap"] == "0/1"
        assert cert["doublet_cancellation"] is True
        assert cert["winding_parity_evaluated"] is True
        assert cert["linking_pairing_symmetric"] is True
        assert cert["homology_group"] == "H1(T^3, Z) = Z^3"

    def test_master_receipt_target_t5_parity(self) -> None:
        """Target T5 contains second Chern class, fermion sign, and doublet cancellation."""
        data = build_master_receipt_dict()
        t5 = next(t for t in data["targets"] if t["target_id"] == "T5_4D_MERON_HALF_INSTANTON_CHERN_CANCELLATION")
        assert t5["dimension"] == 4
        cert = t5["certified_rational_receipt"]
        assert cert["duality_gap"] == "0/1"
        assert cert["doublet_sum_zero"] is True
        assert cert["exact_zero_sum_doublet"] is True
        assert cert["second_chern_charge"] == "1/2"
        assert cert["orientation_inversion"] == "-1/2"
        assert cert["fermion_determinant_sign"] == -1
        assert cert["inversion_fermion_sign"] == 1

    def test_generate_master_receipt_file_creation(self, tmp_path: Path) -> None:
        """Asserts master receipt generates valid JSON file on disk."""
        receipt_path = str(tmp_path / "test_receipt.json")
        data = generate_master_receipt(receipt_path)

        assert os.path.exists(receipt_path)
        with open(receipt_path, "r", encoding="utf-8") as f:
            loaded = json.load(f)

        assert loaded["receipt_version"] == "1.0.0"
        assert "sha256_digest" in loaded
        assert len(loaded["sha256_digest"]) == 64
        assert data["sha256_digest"] == loaded["sha256_digest"]

    def test_generate_master_receipt_deterministic_sha256(self, tmp_path: Path) -> None:
        """Recomputing SHA-256 over receipt body strictly matches embedded digest."""
        receipt_path = str(tmp_path / "test_receipt.json")
        data = generate_master_receipt(receipt_path)

        assert verify_master_receipt_digest(data) is True
        assert verify_master_receipt_digest(receipt_path) is True

        # Tamper with receipt and assert failure
        data_tampered = dict(data)
        data_tampered["title"] = "Tampered Title"
        assert verify_master_receipt_digest(data_tampered) is False

    def test_export_canonical_master_receipts(self, tmp_path: Path) -> None:
        """Asserts both canonical repository locations receive valid master receipts."""
        p1_tmp = str(tmp_path / "results" / "4d_topological_cluster_receipt.json")
        p2_tmp = str(tmp_path / "code" / "results" / "4d_topological_cluster_receipt.json")
        p1, p2 = export_canonical_master_receipts(p1_tmp, p2_tmp)

        assert os.path.exists(p1)
        assert os.path.exists(p2)
        assert verify_master_receipt_digest(p1) is True
        assert verify_master_receipt_digest(p2) is True


# ============================================================================
# Test Suite 5: Zero-Float Static AST Audit & Runtime Type Barriers
# ============================================================================


class TestZeroFloatDisciplineAndAstAudit:
    """Verifies that zero floating-point literals or constructor calls exist in code."""

    def test_ast_audit_adversarial_audit_zero_floats(self) -> None:
        """Scans AST of adversarial_topological_audit.py asserting zero float literals or calls."""
        source_path = _CODE_DIR / "adversarial_topological_audit.py"
        with open(source_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=str(source_path))

        for node in ast.walk(tree):
            if isinstance(node, ast.Constant):
                assert type(node.value) is not float, (
                    f"Forbidden float constant {node.value} at line {node.lineno}"
                )
            elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                assert node.func.id != "float", (
                    f"Forbidden float() constructor call at line {node.lineno}"
                )

    def test_runtime_rejection_of_float_weights(self) -> None:
        """Passing float weight to prosecutor or solver raises TypeError."""
        prosecutor = WolandDialecticalProsecutor()
        with pytest.raises(TypeError, match="Floating-point value forbidden"):
            prosecutor.solver.verify_zero_sum_doublet(
                HalfInstantonCluster4D(1, 0),
                weight=1.0,  # type: ignore
            )


# ============================================================================
# Test Suite 6: Claim & Lexical Hygiene Discipline
# ============================================================================


class TestClaimAndLexicalHygieneDiscipline:
    """Verifies claim hygiene across receipts and problem texts."""

    def test_master_receipt_claims_contain_no_unhedged_hype_verbs(self) -> None:
        """Asserts receipt claim summaries avoid forbidden hype verbs."""
        receipt = build_master_receipt_dict()
        forbidden_hype = ("flawless", "weaponized", "fundamentally", "true intelligence")

        for target in receipt["targets"]:
            claim = target.get("narrowest_defensible_claim", "")
            for word in forbidden_hype:
                assert word not in claim.lower(), f"Forbidden hype verb '{word}' found in claim: {claim}"


# ============================================================================
# Test Suite 7: UTF-8 BOM Cleanliness
# ============================================================================


class TestUtf8BomCleanliness:
    """Verifies that all authored files are encoded in pure UTF-8 without BOM."""

    def test_files_contain_no_utf8_bom(self) -> None:
        """Asserts neither source, test, nor receipt files start with \\xef\\xbb\\xbf."""
        files = [
            _CODE_DIR / "adversarial_topological_audit.py",
            Path(__file__),
            _REPO_ROOT / "results/4d_topological_cluster_receipt.json",
            _CODE_DIR / "results/4d_topological_cluster_receipt.json",
        ]
        for p in files:
            if p.exists():
                with open(p, "rb") as f:
                    header = f.read(3)
                    assert header != b"\xef\xbb\xbf", f"UTF-8 BOM detected in {p}"
