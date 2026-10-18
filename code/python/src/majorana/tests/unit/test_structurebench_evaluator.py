"""StructureBench relational contracts, evaluated against real emitted bytes.

The contracts are specified in the Woland swarm design docs (spec 05) over the
four canonical files a bout emits. **Nothing validated them.**

The two tests that matter most drive the *real* emitter --
`persist_bout_run_folder` -- and show the evaluator reporting what it actually
produces: JSON with unsorted keys, and a receipt that cannot carry the digests
of files written after it. Those are findings about live code, not about a
fixture this file invented.
"""

from __future__ import annotations

import hashlib
import json
import pathlib

import pytest

from omega_engine_woland.use_cases.persistence import (
    persist_bout_run_folder,
)
from omega_engine_workflows_agents_skills.structurebench import (
    ACT_HEADERS,
    CONSTRAINT_IDS,
    ConstraintOutcome,
    ConstraintResult,
    StructureBenchError,
    StructureBenchReport,
    evaluate_bundle,
)

SPEC = (
    pathlib.Path(__file__).resolve().parents[2]
    / "omega_engine_woland"
    / "_design_docs"
    / "05_spec_structurebench_artifact_contracts_and_lossless_rendering.md"
)
EMITTER = (
    pathlib.Path(__file__).resolve().parents[2]
    / "omega_engine_woland"
    / "use_cases"
    / "persistence.py"
)


class StubReceipt:
    """A stand-in with the only method the emitter calls.

    `persist_bout_run_folder` never type-checks its receipt -- it calls
    `receipt.to_dict()` and serialises the result. The property under test is
    the emitter's *serialisation*, which a real `SwarmRunReceiptV1` would
    exercise identically while requiring a tree of digest-shaped domain objects
    that has nothing to do with key ordering. The stub keeps the test about the
    thing it is about.
    """

    def __init__(self, payload: dict) -> None:
        self._payload = payload

    def to_dict(self) -> dict:
        return self._payload


def novella_text(*, truncated: bool = False, timestamps: tuple[str, ...] = ()) -> str:
    parts = []
    for header in ACT_HEADERS:
        parts.append(f"{header} A Scene\n\nDialogue rendered in full.\n")
    for stamp in timestamps:
        parts.append(f"At {stamp} the scene turns.\n")
    if truncated:
        parts.append("... [truncated] ...\n")
    return "\n".join(parts)


def write_conforming_bundle(root: pathlib.Path) -> pathlib.Path:
    """A bundle that satisfies every declared constraint.

    The evaluator must be shown able to return clean, or a report of violations
    proves nothing -- a validator that always fails is not evidence about the
    bundle.
    """
    bundle = root / "conforming"
    bundle.mkdir()
    novella = novella_text(timestamps=("2026-08-28T00:00:00Z",))
    actions = (
        json.dumps(
            {"gamma_2": 0, "phi_1": 0, "timestamp": "2026-08-28T00:00:00Z"},
            sort_keys=True,
        )
        + "\n"
    )
    summary = (
        json.dumps(
            {
                "receipt_id": "sha256:" + "a" * 64,
                "selected_candidate_id": "cand-1",
                "task_key": "probe",
                "terminal_verdict": "PASS_TO_MASTER",
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )
    bundle.joinpath("novella.md").write_text(novella, encoding="utf-8", newline="\n")
    bundle.joinpath("dda_actions.jsonl").write_text(
        actions, encoding="utf-8", newline="\n"
    )
    bundle.joinpath("summary.json").write_text(summary, encoding="utf-8", newline="\n")

    def sha(name: str) -> str:
        return hashlib.sha256(
            bundle.joinpath(name).read_bytes()
        ).hexdigest()

    receipt = {
        "dda_actions_sha256": sha("dda_actions.jsonl"),
        "lean4_proof_hash": "sha256:" + "b" * 64,
        "novella_sha256": sha("novella.md"),
        "receipt_id": "sha256:" + "a" * 64,
        "selected_candidate_id": "cand-1",
        "summary_sha256": sha("summary.json"),
        "task_key": "probe",
    }
    bundle.joinpath("receipt.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return bundle


def outcome_of(report: StructureBenchReport, constraint_id: str) -> ConstraintOutcome:
    for result in report.results:
        if result.constraint_id == constraint_id:
            return result.outcome
    raise AssertionError(f"{constraint_id} not in the report")




def test_a_conforming_bundle_is_clean(tmp_path):
    report = evaluate_bundle(write_conforming_bundle(tmp_path))
    assert report.is_clean(), report.render()


def test_a_conforming_bundle_decides_every_constraint(tmp_path):
    """Coverage is full when the artifacts carry the fields the spec names."""
    report = evaluate_bundle(write_conforming_bundle(tmp_path))
    reachable, declared = report.coverage()
    assert reachable == declared == len(CONSTRAINT_IDS)




def test_the_live_emitter_writes_unsorted_json_keys(tmp_path):
    """Spec 2.1 requires ordinal key order. The emitter does not sort.

    Driven through `persist_bout_run_folder` rather than asserted from its
    source, so this is evidence about emitted bytes rather than about a line of
    code that might not be the one that runs.
    """
    result = persist_bout_run_folder(
        tmp_path,
        "probe",
        StubReceipt({"zulu": 1, "alpha": 2}),
        novella_text(),
        [{"zulu": 1, "alpha": 2}],
        {"zulu": 1, "alpha": 2, "terminal_verdict": "REFUSED"},
    )
    bundle = tmp_path / "runs" / "probe"
    assert bundle.is_dir(), f"the emitter refused: {result}"

    written = json.loads(bundle.joinpath("receipt.json").read_text(encoding="utf-8"))
    assert list(written) == ["zulu", "alpha"], (
        "document order should still be insertion order; if this fails the "
        "emitter now sorts and the finding below is stale"
    )

    report = evaluate_bundle(bundle)
    assert outcome_of(report, "C1_JSON_KEYS_SORTED") is ConstraintOutcome.VIOLATED


def test_the_live_emitter_cannot_bind_artifact_digests(tmp_path):
    """Spec 2.2 requires the receipt to record the other three files' digests.

    It is written **first**, before they exist, so it cannot. Reported
    `UNVERIFIABLE` rather than `VIOLATED`: the bundle is not failing a check, it
    is being measured against a receipt schema that was never built.
    """
    persist_bout_run_folder(
        tmp_path,
        "probe",
        StubReceipt({"schema_version": "omega.oeas.swarm-run-receipt.v1"}),
        novella_text(),
        [{"step": 1}],
        {"terminal_verdict": "REFUSED"},
    )
    report = evaluate_bundle(tmp_path / "runs" / "probe")
    assert outcome_of(report, "C2_HASH_BINDING") is ConstraintOutcome.UNVERIFIABLE


def test_the_live_emitter_writes_a_receipt_with_no_bijection_keys(tmp_path):
    """`task_key` and `selected_candidate_id` exist in no emitted receipt."""
    persist_bout_run_folder(
        tmp_path,
        "probe",
        StubReceipt({"schema_version": "omega.oeas.swarm-run-receipt.v1"}),
        novella_text(),
        [{"step": 1}],
        {"terminal_verdict": "REFUSED"},
    )
    report = evaluate_bundle(tmp_path / "runs" / "probe")
    assert (
        outcome_of(report, "C2_RECEIPT_SUMMARY_BIJECTION")
        is ConstraintOutcome.UNVERIFIABLE
    )


def test_a_live_bundle_is_not_clean(tmp_path):
    """The whole finding in one assertion."""
    persist_bout_run_folder(
        tmp_path,
        "probe",
        StubReceipt({"zulu": 1, "alpha": 2}),
        novella_text(),
        [{"zulu": 1}],
        {"zulu": 1, "terminal_verdict": "REFUSED"},
    )
    report = evaluate_bundle(tmp_path / "runs" / "probe")
    assert not report.is_clean()
    reachable, declared = report.coverage()
    assert reachable < declared, "some constraints must be unreachable here"


def test_the_emitter_has_no_sort_keys_call():
    """The source side of the dual evidence.

    The behavioural test above says the bytes come out unsorted; this says the
    call that would sort them is absent. Either alone is weaker: a passing
    behavioural test could be a fixture accident, and a source grep could be
    reading a line that never runs.
    """
    source = EMITTER.read_text(encoding="utf-8")
    assert "json.dumps" in source
    assert "sort_keys" not in source


def test_the_receipt_is_written_before_the_files_it_should_hash():
    """Why the hash binding is unreachable rather than merely missing."""
    source = EMITTER.read_text(encoding="utf-8")
    receipt_at = source.index('"receipt.json"')
    novella_at = source.index('"novella.md"')
    summary_at = source.index('"summary.json"')
    assert receipt_at < novella_at < summary_at


def test_the_spec_and_the_epic_disagree_about_the_hash_function():
    """`ESC-016-001` recurring, this time inside one epic's own documents.

    The epic's acceptance criterion 3 asks for BLAKE3-hashed receipts. The
    design spec it governs requires SHA256 digests. Pinned at both sources so
    the split stays visible rather than being settled by whichever document a
    reader opens first.
    """
    spec = SPEC.read_text(encoding="utf-8")
    assert "SHA256 digests" in spec

    epic = (
        pathlib.Path(__file__).resolve().parents[2]
        / "omega_engine_product_planning_office"
        / "plans"
        / "epics"
        / "epic_oe_oewas_007_polarized_debate_and_structurebench_contracts_plan.md"
    ).read_text(encoding="utf-8")
    assert "BLAKE3-hashed" in epic




def test_an_unverifiable_constraint_is_not_clean(tmp_path):
    """The central design decision, asserted directly.

    A bundle whose hash binding cannot be checked is not a bundle whose hash
    binding is sound.
    """
    bundle = write_conforming_bundle(tmp_path)
    receipt = json.loads(bundle.joinpath("receipt.json").read_text(encoding="utf-8"))
    for key in ("novella_sha256", "dda_actions_sha256", "summary_sha256"):
        receipt.pop(key)
    bundle.joinpath("receipt.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    report = evaluate_bundle(bundle)
    assert outcome_of(report, "C2_HASH_BINDING") is ConstraintOutcome.UNVERIFIABLE
    assert not report.is_clean()
    assert report.by_outcome(ConstraintOutcome.VIOLATED) == ()


def test_coverage_excludes_only_the_unverifiable(tmp_path):
    """Measured on a bundle that *has* unverifiable constraints.

    An earlier version of this test used the conforming bundle, where the
    unverifiable count is zero -- so `reachable == declared - 0` reduced to
    `declared == declared` and a mutation hardcoding that count to zero
    survived. The assertion has to be made where the quantity it subtracts is
    non-zero, or it is not an assertion about subtraction at all.
    """
    bundle = write_conforming_bundle(tmp_path)
    receipt = json.loads(bundle.joinpath("receipt.json").read_text(encoding="utf-8"))
    for key in ("novella_sha256", "dda_actions_sha256", "summary_sha256"):
        receipt.pop(key)
    bundle.joinpath("receipt.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    report = evaluate_bundle(bundle)
    unverifiable = report.by_outcome(ConstraintOutcome.UNVERIFIABLE)
    assert unverifiable, "the fixture must produce at least one unverifiable result"

    reachable, declared = report.coverage()
    assert declared == len(report.results)
    assert reachable == declared - len(unverifiable)
    assert reachable < declared


def test_coverage_is_a_pair_not_a_ratio(tmp_path):
    reachable, declared = evaluate_bundle(write_conforming_bundle(tmp_path)).coverage()
    assert isinstance(reachable, int) and isinstance(declared, int)


def test_the_report_states_all_three_counts(tmp_path):
    rendered = evaluate_bundle(write_conforming_bundle(tmp_path)).render()
    assert "constraints declared" in rendered
    assert "constraints decided" in rendered
    assert "unverifiable" in rendered




def test_a_missing_file_violates_presence(tmp_path):
    bundle = write_conforming_bundle(tmp_path)
    bundle.joinpath("summary.json").unlink()
    report = evaluate_bundle(bundle)
    assert outcome_of(report, "C1_FILES_PRESENT") is ConstraintOutcome.VIOLATED


def test_a_byte_order_mark_violates_encoding(tmp_path):
    bundle = write_conforming_bundle(tmp_path)
    raw = bundle.joinpath("novella.md").read_bytes()
    bundle.joinpath("novella.md").write_bytes(b"\xef\xbb\xbf" + raw)
    report = evaluate_bundle(bundle)
    assert outcome_of(report, "C1_UTF8_NO_BOM") is ConstraintOutcome.VIOLATED


def test_invalid_utf8_violates_encoding(tmp_path):
    bundle = write_conforming_bundle(tmp_path)
    bundle.joinpath("novella.md").write_bytes(b"\xff\xfe not utf-8")
    report = evaluate_bundle(bundle)
    assert outcome_of(report, "C1_UTF8_NO_BOM") is ConstraintOutcome.VIOLATED


def test_unparseable_json_violates_parsing(tmp_path):
    bundle = write_conforming_bundle(tmp_path)
    bundle.joinpath("summary.json").write_text("{not json", encoding="utf-8")
    report = evaluate_bundle(bundle)
    assert outcome_of(report, "C1_JSON_PARSES") is ConstraintOutcome.VIOLATED


def test_nested_unsorted_keys_are_caught(tmp_path):
    """Ordering is checked through the whole tree, not only at the top level."""
    bundle = write_conforming_bundle(tmp_path)
    bundle.joinpath("summary.json").write_text(
        '{\n  "a": {\n    "zulu": 1,\n    "alpha": 2\n  },\n  "b": 1\n}\n',
        encoding="utf-8",
    )
    report = evaluate_bundle(bundle)
    assert outcome_of(report, "C1_JSON_KEYS_SORTED") is ConstraintOutcome.VIOLATED


def test_unsorted_keys_inside_a_list_are_caught(tmp_path):
    bundle = write_conforming_bundle(tmp_path)
    bundle.joinpath("summary.json").write_text(
        '{\n  "a": [\n    {"zulu": 1, "alpha": 2}\n  ]\n}\n', encoding="utf-8"
    )
    report = evaluate_bundle(bundle)
    assert outcome_of(report, "C1_JSON_KEYS_SORTED") is ConstraintOutcome.VIOLATED


def test_an_unsorted_action_line_is_caught(tmp_path):
    bundle = write_conforming_bundle(tmp_path)
    bundle.joinpath("dda_actions.jsonl").write_text(
        '{"zulu": 1, "alpha": 2}\n', encoding="utf-8"
    )
    report = evaluate_bundle(bundle)
    assert outcome_of(report, "C1_JSON_KEYS_SORTED") is ConstraintOutcome.VIOLATED


def test_a_non_object_action_line_violates_the_jsonl_shape(tmp_path):
    bundle = write_conforming_bundle(tmp_path)
    bundle.joinpath("dda_actions.jsonl").write_text("[1, 2, 3]\n", encoding="utf-8")
    report = evaluate_bundle(bundle)
    assert (
        outcome_of(report, "C1_JSONL_ONE_OBJECT_PER_LINE")
        is ConstraintOutcome.VIOLATED
    )


def test_a_disagreeing_task_key_violates_the_bijection(tmp_path):
    bundle = write_conforming_bundle(tmp_path)
    summary = json.loads(bundle.joinpath("summary.json").read_text(encoding="utf-8"))
    summary["task_key"] = "a-different-key"
    bundle.joinpath("summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    report = evaluate_bundle(bundle)
    assert (
        outcome_of(report, "C2_RECEIPT_SUMMARY_BIJECTION")
        is ConstraintOutcome.VIOLATED
    )


def test_a_wrong_recorded_digest_violates_hash_binding(tmp_path):
    """Hash binding is checked against the bytes, not merely for presence."""
    bundle = write_conforming_bundle(tmp_path)
    receipt = json.loads(bundle.joinpath("receipt.json").read_text(encoding="utf-8"))
    receipt["novella_sha256"] = "0" * 64
    bundle.joinpath("receipt.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    report = evaluate_bundle(bundle)
    assert outcome_of(report, "C2_HASH_BINDING") is ConstraintOutcome.VIOLATED


def test_editing_a_hashed_file_violates_hash_binding(tmp_path):
    """The binding must follow the bytes, not the recorded string."""
    bundle = write_conforming_bundle(tmp_path)
    bundle.joinpath("novella.md").write_text(
        novella_text() + "\nan added line\n", encoding="utf-8", newline="\n"
    )
    report = evaluate_bundle(bundle)
    assert outcome_of(report, "C2_HASH_BINDING") is ConstraintOutcome.VIOLATED


def test_an_action_with_no_scene_turn_violates_the_step_bijection(tmp_path):
    bundle = write_conforming_bundle(tmp_path)
    bundle.joinpath("dda_actions.jsonl").write_text(
        json.dumps(
            {"gamma_2": 0, "phi_1": 0, "timestamp": "1999-01-01T00:00:00Z"},
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    report = evaluate_bundle(bundle)
    assert (
        outcome_of(report, "C2_NOVELLA_ACTION_BIJECTION")
        is ConstraintOutcome.VIOLATED
    )


def test_untimestamped_actions_make_the_step_bijection_unverifiable(tmp_path):
    bundle = write_conforming_bundle(tmp_path)
    bundle.joinpath("dda_actions.jsonl").write_text(
        json.dumps({"gamma_2": 0, "phi_1": 0}, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    report = evaluate_bundle(bundle)
    assert (
        outcome_of(report, "C2_NOVELLA_ACTION_BIJECTION")
        is ConstraintOutcome.UNVERIFIABLE
    )


def test_a_missing_act_violates_the_act_sections(tmp_path):
    bundle = write_conforming_bundle(tmp_path)
    bundle.joinpath("novella.md").write_text(
        novella_text().replace("# Act V:", "# Interlude:"),
        encoding="utf-8",
        newline="\n",
    )
    report = evaluate_bundle(bundle)
    assert outcome_of(report, "C3_ACT_SECTIONS_PRESENT") is ConstraintOutcome.VIOLATED


def test_acts_out_of_order_violate_the_act_sections(tmp_path):
    bundle = write_conforming_bundle(tmp_path)
    reordered = "".join(
        f"{header} Scene\n\ntext\n\n" for header in reversed(ACT_HEADERS)
    )
    bundle.joinpath("novella.md").write_text(
        reordered, encoding="utf-8", newline="\n"
    )
    report = evaluate_bundle(bundle)
    assert outcome_of(report, "C3_ACT_SECTIONS_PRESENT") is ConstraintOutcome.VIOLATED


def test_a_truncation_marker_violates_the_lossless_law(tmp_path):
    bundle = write_conforming_bundle(tmp_path)
    bundle.joinpath("novella.md").write_text(
        novella_text(truncated=True), encoding="utf-8", newline="\n"
    )
    report = evaluate_bundle(bundle)
    assert outcome_of(report, "C3_NO_TRUNCATION_MARKERS") is ConstraintOutcome.VIOLATED


def test_a_nonzero_terminal_defect_violates_pass_to_master(tmp_path):
    bundle = write_conforming_bundle(tmp_path)
    bundle.joinpath("dda_actions.jsonl").write_text(
        json.dumps(
            {"gamma_2": 0, "phi_1": 3, "timestamp": "2026-08-28T00:00:00Z"},
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    report = evaluate_bundle(bundle)
    assert (
        outcome_of(report, "C3_PASS_TO_MASTER_OBLIGATIONS")
        is ConstraintOutcome.VIOLATED
    )


def test_an_empty_lean4_proof_hash_violates_pass_to_master(tmp_path):
    bundle = write_conforming_bundle(tmp_path)
    receipt = json.loads(bundle.joinpath("receipt.json").read_text(encoding="utf-8"))
    receipt["lean4_proof_hash"] = ""
    bundle.joinpath("receipt.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    report = evaluate_bundle(bundle)
    assert (
        outcome_of(report, "C3_PASS_TO_MASTER_OBLIGATIONS")
        is ConstraintOutcome.VIOLATED
    )


def test_a_non_pass_verdict_discharges_the_obligations(tmp_path):
    """The antecedent is false, so the constraint is satisfied, not skipped."""
    bundle = write_conforming_bundle(tmp_path)
    summary = json.loads(bundle.joinpath("summary.json").read_text(encoding="utf-8"))
    summary["terminal_verdict"] = "REFUSED"
    bundle.joinpath("summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    receipt = json.loads(bundle.joinpath("receipt.json").read_text(encoding="utf-8"))
    receipt["summary_sha256"] = hashlib.sha256(
        bundle.joinpath("summary.json").read_bytes()
    ).hexdigest()
    bundle.joinpath("receipt.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    report = evaluate_bundle(bundle)
    assert (
        outcome_of(report, "C3_PASS_TO_MASTER_OBLIGATIONS")
        is ConstraintOutcome.SATISFIED
    )


def test_a_missing_terminal_verdict_is_unverifiable_not_satisfied(tmp_path):
    """An absent antecedent is not a discharged obligation."""
    bundle = write_conforming_bundle(tmp_path)
    bundle.joinpath("summary.json").write_text(
        json.dumps({"task_key": "probe"}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    report = evaluate_bundle(bundle)
    assert (
        outcome_of(report, "C3_PASS_TO_MASTER_OBLIGATIONS")
        is ConstraintOutcome.UNVERIFIABLE
    )




def test_a_report_must_cover_every_declared_constraint():
    """A partial report would be a sample presented as a verdict."""
    with pytest.raises(StructureBenchError) as excinfo:
        StructureBenchReport(
            results=(
                ConstraintResult(
                    "C1_FILES_PRESENT", ConstraintOutcome.SATISFIED, "ok"
                ),
            )
        )
    assert excinfo.value.code == "INCOMPLETE_REPORT"


def test_an_undeclared_constraint_id_is_refused():
    with pytest.raises(StructureBenchError) as excinfo:
        ConstraintResult("C9_INVENTED", ConstraintOutcome.SATISFIED, "ok")
    assert excinfo.value.code == "UNKNOWN_CONSTRAINT"


def test_a_verdict_without_a_reason_is_refused():
    with pytest.raises(StructureBenchError) as excinfo:
        ConstraintResult("C1_FILES_PRESENT", ConstraintOutcome.SATISFIED, "")
    assert excinfo.value.code == "EMPTY_DETAIL"


def test_an_absent_bundle_is_refused(tmp_path):
    with pytest.raises(StructureBenchError) as excinfo:
        evaluate_bundle(tmp_path / "nowhere")
    assert excinfo.value.code == "BUNDLE_ABSENT"


def test_every_declared_constraint_is_evaluated(tmp_path):
    report = evaluate_bundle(write_conforming_bundle(tmp_path))
    assert sorted(r.constraint_id for r in report.results) == sorted(CONSTRAINT_IDS)


def test_the_three_outcomes_are_distinct():
    assert len({o.value for o in ConstraintOutcome}) == 3
