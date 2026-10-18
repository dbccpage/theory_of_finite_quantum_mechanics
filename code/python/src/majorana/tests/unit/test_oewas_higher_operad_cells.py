"""Finite 2-cell admission, inversion, composition, and refinement tests."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from dataclasses import replace
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
    ComparisonEvidence,
    ComparisonVerdict,
    EquivalenceGrade,
    Err,
    Ok,
    OperationSpec,
    PortSpec,
    Primitive,
    admit_atomic_path2,
    admit_refinement,
    horizontal_compose,
    identity_path2,
    inverse2,
    normalize_term,
    pair_subject_digest,
    substitute,
    vertical_compose,
    whisker2,
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


def port(name: str, colour: str) -> PortSpec:
    return PortSpec(name, colour, f"schema:{colour}:v1")


def op(name: str, source: str = "A", target: str = "B") -> OperationSpec:
    return OperationSpec(
        name,
        "v1",
        (port(f"{name}-in", source),),
        port(f"{name}-out", target),
        f"executor:{name}",
        D1,
    )


def evidence_for(
    source,
    target,
    *,
    verdict: ComparisonVerdict = ComparisonVerdict.EQUIVALENT,
    grade: EquivalenceGrade = EquivalenceGrade.CERTIFIED_ISOMORPHISM,
    relation: str = "relation:iso",
):
    comparison = ComparisonEvidence(
        source.canonical_id,
        target.canonical_id,
        relation,
        D2,
        D3,
        "verifier:independent",
        D4,
        D5,
        verdict,
        grade,
        D6 if grade is EquivalenceGrade.CERTIFIED_ISOMORPHISM else "",
        D7 if grade is EquivalenceGrade.CERTIFIED_ISOMORPHISM else "",
        D8 if grade is EquivalenceGrade.CERTIFIED_ISOMORPHISM else "",
        D9 if grade is EquivalenceGrade.CERTIFIED_ISOMORPHISM else "",
    )
    attestation = Attestation(
        pair_subject_digest(source, target, relation, D2),
        comparison.canonical_id,
        relation,
        "producer:comparison",
        "verifier:independent",
        D4,
        D5,
        D0,
        SIG,
    )
    return comparison, attestation


class AtomicPathAdmissionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.f = normalize_term(Primitive(op("f"))).unwrap()
        self.g = normalize_term(Primitive(op("g"))).unwrap()

    def test_certified_isomorphism_admits_atomic_path_and_inverse(self) -> None:
        comparison, attestation = evidence_for(self.f, self.g)
        admitted = admit_atomic_path2(
            self.f, self.g, comparison, _seal_replayed_attestation(attestation)
        )
        self.assertIsInstance(admitted, Ok)
        inverse = inverse2(admitted.value).unwrap()
        self.assertEqual(inverse.source.canonical_id, self.g.canonical_id)
        self.assertEqual(inverse.target.canonical_id, self.f.canonical_id)
        self.assertEqual(inverse2(inverse).unwrap().canonical_id, admitted.value.canonical_id)

    def test_scoped_observational_and_refinement_cannot_enter_path2(self) -> None:
        scoped, scoped_attestation = evidence_for(
            self.f,
            self.g,
            grade=EquivalenceGrade.SCOPED_OBSERVATIONAL,
        )
        refused = admit_atomic_path2(self.f, self.g, scoped, scoped_attestation)
        self.assertIsInstance(refused, Err)
        self.assertEqual(refused.error.code, "WEAK_EQUIVALENCE_GRADE")

        refinement_evidence, refinement_attestation = evidence_for(
            self.f,
            self.g,
            verdict=ComparisonVerdict.REFINES,
            grade=EquivalenceGrade.SCOPED_OBSERVATIONAL,
            relation="relation:refines",
        )
        refused_path = admit_atomic_path2(self.f, self.g, refinement_evidence, refinement_attestation)
        self.assertEqual(refused_path.error.code, "NON_ADMISSIBLE_COMPARISON")
        refinement = admit_refinement(self.f, self.g, refinement_evidence, refinement_attestation)
        self.assertIsInstance(refinement, Ok)

    def test_candidate_comparison_cannot_enter_path2(self) -> None:
        candidate, attestation = evidence_for(
            self.f,
            self.g,
            grade=EquivalenceGrade.CANDIDATE,
            relation="relation:candidate",
        )
        refused = admit_atomic_path2(self.f, self.g, candidate, attestation)
        self.assertIsInstance(refused, Err)
        self.assertEqual(refused.error.code, "WEAK_EQUIVALENCE_GRADE")

    def test_definitional_grade_requires_same_normal_form(self) -> None:
        comparison, attestation = evidence_for(
            self.f,
            self.g,
            grade=EquivalenceGrade.DEFINITIONAL,
            relation="relation:defeq",
        )
        result = admit_atomic_path2(self.f, self.g, comparison, attestation)
        self.assertIsInstance(result, Err)
        self.assertEqual(result.error.code, "FALSE_DEFINITIONAL_EQUALITY")
        same_comparison, same_attestation = evidence_for(
            self.f,
            self.f,
            grade=EquivalenceGrade.DEFINITIONAL,
            relation="relation:defeq",
        )
        self.assertIsInstance(admit_atomic_path2(self.f, self.f, same_comparison, same_attestation), Ok)

    def test_missing_roundtrip_or_forged_endpoint_refuses(self) -> None:
        comparison, attestation = evidence_for(self.f, self.g)
        missing = replace(comparison, right_roundtrip_digest="")
        rebound = replace(attestation, evidence_digest=missing.canonical_id)
        result = admit_atomic_path2(
            self.f, self.g, missing, _seal_replayed_attestation(rebound)
        )
        self.assertIsInstance(result, Err)
        self.assertEqual(result.error.code, "INCOMPLETE_ISOMORPHISM")
        forged = replace(comparison, target_term_id=D0)
        forged_attestation = replace(attestation, evidence_digest=forged.canonical_id)
        endpoint_result = admit_atomic_path2(
            self.f, self.g, forged, _seal_replayed_attestation(forged_attestation)
        )
        self.assertEqual(endpoint_result.error.code, "COMPARISON_ENDPOINT_MISMATCH")

    def test_raw_digest_attestation_cannot_mint_certified_path(self) -> None:
        comparison, attestation = evidence_for(self.f, self.g)
        result = admit_atomic_path2(self.f, self.g, comparison, attestation)
        self.assertIsInstance(result, Err)
        self.assertEqual(result.error.code, "UNVERIFIED_REPLAY_ATTESTATION")

    def test_nonparallel_terms_refuse_before_certificate_promotion(self) -> None:
        different = normalize_term(Primitive(op("different", "A", "C"))).unwrap()
        comparison, attestation = evidence_for(self.f, different)
        result = admit_atomic_path2(self.f, different, comparison, attestation)
        self.assertIsInstance(result, Err)
        self.assertEqual(result.error.code, "NON_PARALLEL_TERMS")


class PathAlgebraTests(unittest.TestCase):
    def _path(self, source, target):
        comparison, attestation = evidence_for(source, target)
        return admit_atomic_path2(
            source, target, comparison, _seal_replayed_attestation(attestation)
        ).unwrap()

    def test_vertical_composition_requires_meeting_endpoint(self) -> None:
        f = normalize_term(Primitive(op("f"))).unwrap()
        g = normalize_term(Primitive(op("g"))).unwrap()
        h = normalize_term(Primitive(op("h"))).unwrap()
        fg = self._path(f, g)
        gh = self._path(g, h)
        composed = vertical_compose(fg, gh)
        self.assertIsInstance(composed, Ok)
        self.assertEqual(composed.value.source.canonical_id, f.canonical_id)
        self.assertEqual(composed.value.target.canonical_id, h.canonical_id)
        refused = vertical_compose(gh, fg)
        self.assertIsInstance(refused, Err)
        self.assertEqual(refused.error.code, "VERTICAL_BOUNDARY_MISMATCH")

    def test_vertical_composition_has_associative_canonical_id(self) -> None:
        f = normalize_term(Primitive(op("f"))).unwrap()
        g = normalize_term(Primitive(op("g"))).unwrap()
        h = normalize_term(Primitive(op("h"))).unwrap()
        k = normalize_term(Primitive(op("k"))).unwrap()
        fg, gh, hk = self._path(f, g), self._path(g, h), self._path(h, k)
        left = vertical_compose(vertical_compose(fg, gh).unwrap(), hk).unwrap()
        right = vertical_compose(fg, vertical_compose(gh, hk).unwrap()).unwrap()
        self.assertEqual(left.canonical_id, right.canonical_id)

    def test_vertical_units_and_inverses_normalize_at_the_path_id_boundary(self) -> None:
        f = normalize_term(Primitive(op("f"))).unwrap()
        g = normalize_term(Primitive(op("g"))).unwrap()
        path = self._path(f, g)
        left_unit = vertical_compose(identity_path2(f).unwrap(), path).unwrap()
        right_unit = vertical_compose(path, identity_path2(g).unwrap()).unwrap()
        self.assertEqual(left_unit.canonical_id, path.canonical_id)
        self.assertEqual(right_unit.canonical_id, path.canonical_id)

        inverse = inverse2(path).unwrap()
        right_inverse = vertical_compose(path, inverse).unwrap()
        left_inverse = vertical_compose(inverse, path).unwrap()
        self.assertEqual(
            right_inverse.canonical_id,
            identity_path2(f).unwrap().canonical_id,
        )
        self.assertEqual(
            left_inverse.canonical_id,
            identity_path2(g).unwrap().canonical_id,
        )

    def test_horizontal_composition_requires_fresh_composite_evidence(self) -> None:
        outer_f = normalize_term(Primitive(op("outer-f", "B", "C"))).unwrap()
        outer_g = normalize_term(Primitive(op("outer-g", "B", "C"))).unwrap()
        inner_f = normalize_term(Primitive(op("inner-f", "A", "B"))).unwrap()
        inner_g = normalize_term(Primitive(op("inner-g", "A", "B"))).unwrap()
        outer_path = self._path(outer_f, outer_g)
        inner_path = self._path(inner_f, inner_g)
        source = substitute(Primitive(op("outer-f", "B", "C")), 0, Primitive(op("inner-f", "A", "B"))).unwrap()
        target = substitute(Primitive(op("outer-g", "B", "C")), 0, Primitive(op("inner-g", "A", "B"))).unwrap()
        comparison, attestation = evidence_for(source, target)
        result = horizontal_compose(
            outer_path,
            0,
            inner_path,
            comparison,
            _seal_replayed_attestation(attestation),
        )
        self.assertIsInstance(result, Ok)
        self.assertEqual(result.value.source.canonical_id, source.canonical_id)
        self.assertEqual(result.value.target.canonical_id, target.canonical_id)

    def test_whisker_requires_fresh_composite_attestation(self) -> None:
        f = normalize_term(Primitive(op("f"))).unwrap()
        g = normalize_term(Primitive(op("g"))).unwrap()
        path = self._path(f, g)
        context = normalize_term(Primitive(op("context", "B", "C"))).unwrap()
        source = substitute(Primitive(op("context", "B", "C")), 0, Primitive(op("f"))).unwrap()
        target = substitute(Primitive(op("context", "B", "C")), 0, Primitive(op("g"))).unwrap()
        comparison, attestation = evidence_for(source, target)
        result = whisker2(
            context, 0, path, comparison, _seal_replayed_attestation(attestation)
        )
        self.assertIsInstance(result, Ok)
        forged = replace(attestation, subject_digest=D0)
        refused = whisker2(
            context, 0, path, comparison, _seal_replayed_attestation(forged)
        )
        self.assertIsInstance(refused, Err)
        self.assertEqual(refused.error.code, "ATTESTATION_SUBJECT_MISMATCH")


if __name__ == "__main__":
    unittest.main()
