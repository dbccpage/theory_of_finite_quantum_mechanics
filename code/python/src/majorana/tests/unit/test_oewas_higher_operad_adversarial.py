"""Construction-bypass and canonical mutation attacks."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from dataclasses import FrozenInstanceError, replace
from pathlib import Path

KERNEL_ROOT = Path(__file__).resolve().parents[1] / "kernel"
PACKAGE_ROOT = KERNEL_ROOT / "higher_operad"
if "higher_operad" not in sys.modules:
    spec = importlib.util.spec_from_file_location(
        "higher_operad",
        PACKAGE_ROOT / "__init__.py",
        submodule_search_locations=[str(PACKAGE_ROOT)],
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load higher_operad package")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

from higher_operad import (  # noqa: E402
    Attestation,
    AuthorityEffect,
    BoundarySignature,
    CertifiedPair,
    ComparisonEvidence,
    ComparisonVerdict,
    EquivalenceGrade,
    OperationSpec,
    PortSpec,
    Primitive,
    admit_certified_pair,
    normalize_term,
    pair_subject_digest,
)
from higher_operad.cells import _seal_replayed_attestation  # noqa: E402

D0 = "sha256:" + "0" * 64
D1 = "sha256:" + "1" * 64
D2 = "sha256:" + "2" * 64
D3 = "sha256:" + "3" * 64
D4 = "sha256:" + "4" * 64
D5 = "sha256:" + "5" * 64
D6 = "sha256:" + "6" * 64
D7 = "sha256:" + "7" * 64
D8 = "sha256:" + "8" * 64
D9 = "sha256:" + "9" * 64
SIG = "hmac-sha256:" + "a" * 64


def term(name: str):
    operation = OperationSpec(
        name,
        "v1",
        (PortSpec("input", "A", "schema:A:v1"),),
        PortSpec("output", "B", "schema:B:v1"),
        f"executor:{name}",
        D1,
    )
    return normalize_term(Primitive(operation)).unwrap()


def valid_material(source, target):
    comparison = ComparisonEvidence(
        source.canonical_id,
        target.canonical_id,
        "relation:iso",
        D2,
        D3,
        "verifier:independent",
        D4,
        D5,
        ComparisonVerdict.EQUIVALENT,
        EquivalenceGrade.CERTIFIED_ISOMORPHISM,
        D6,
        D7,
        D8,
        D9,
    )
    attestation = Attestation(
        pair_subject_digest(source, target, "relation:iso", D2),
        comparison.canonical_id,
        "relation:iso",
        "producer:model",
        "verifier:independent",
        D4,
        D5,
        D0,
        SIG,
    )
    return comparison, attestation


class ConstructionAttackTests(unittest.TestCase):
    def test_boundary_rejects_non_port_values_at_construction(self) -> None:
        with self.assertRaisesRegex(TypeError, "PortSpec"):
            BoundarySignature(("not-a-port",), PortSpec("output", "B", "schema:B:v1"))

    def test_direct_certified_pair_constructor_rechecks_attestation(self) -> None:
        source, target = term("source"), term("target")
        comparison, attestation = valid_material(source, target)
        with self.assertRaisesRegex(ValueError, "ATTESTATION_SUBJECT_MISMATCH"):
            CertifiedPair(
                source,
                target,
                comparison,
                _seal_replayed_attestation(replace(attestation, subject_digest=D0)),
            )

    def test_self_attestation_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "independent"):
            Attestation(D1, D2, "relation:iso", "same", "same", D3, D4, D5, SIG)

    def test_authority_bearing_attestation_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "AuthorityEffect None"):
            Attestation(
                D1,
                D2,
                "relation:iso",
                "producer:a",
                "verifier:b",
                D3,
                D4,
                D5,
                SIG,
                AuthorityEffect.FACT_ONLY,
            )

    def test_comparison_mutation_changes_id_and_invalidates_old_attestation(self) -> None:
        source, target = term("source"), term("target")
        comparison, attestation = valid_material(source, target)
        mutated = replace(comparison, fixture_set_digest=D0)
        self.assertNotEqual(mutated.canonical_id, comparison.canonical_id)
        result = admit_certified_pair(
            source, target, mutated, _seal_replayed_attestation(attestation)
        )
        self.assertEqual(result.error.code, "ATTESTATION_EVIDENCE_MISMATCH")

    def test_direct_refinement_construction_rechecks_all_bindings(self) -> None:
        from higher_operad import Refinement

        source, target = term("source"), term("target")
        comparison, attestation = valid_material(source, target)
        refinement = replace(
            comparison,
            verdict=ComparisonVerdict.REFINES,
            equivalence_grade=EquivalenceGrade.SCOPED_OBSERVATIONAL,
            relation_id="relation:refines",
        )
        bound = Attestation(
            pair_subject_digest(source, target, "relation:refines", D2),
            refinement.canonical_id,
            "relation:refines",
            "producer:model",
            "verifier:independent",
            D4,
            D5,
            D0,
            SIG,
        )
        with self.assertRaisesRegex(ValueError, "REPLAY_BINDING_MISMATCH"):
            Refinement(source, target, refinement, replace(bound, replay_receipt_ref=D0))

    def test_frozen_evidence_rejects_normal_assignment(self) -> None:
        source, target = term("source"), term("target")
        comparison, _ = valid_material(source, target)
        with self.assertRaises(FrozenInstanceError):
            comparison.verifier_ref = "verifier:evil"

    def test_digest_shape_and_boolean_theater_are_rejected(self) -> None:
        source, target = term("source"), term("target")
        with self.assertRaisesRegex(ValueError, "sha256"):
            ComparisonEvidence(
                source.canonical_id,
                target.canonical_id,
                "relation:iso",
                "PASS",
                D3,
                "verifier:independent",
                D4,
                D5,
                ComparisonVerdict.EQUIVALENT,
                EquivalenceGrade.CERTIFIED_ISOMORPHISM,
                D6,
                D7,
                D8,
                D9,
            )


if __name__ == "__main__":
    unittest.main()
