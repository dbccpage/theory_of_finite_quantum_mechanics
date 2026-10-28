"""Authored Rust custody review; a static registry does not inherit L4 capability."""
import json
from pathlib import Path

from record_batch2 import ROOT, add, pin, store

BASE = ROOT / "evidence/quality/expanded_scope"
SOURCE = "code/rust/tests/mub/fixture_receipts.rs"
ASSET = "code/rust/tests/mub/fixture_receipt_register.json"
FIRST = BASE / "20261020T225459Z-rust-fixture-challenge"
SECOND = BASE / "20261020T230113Z-rust-fixture-challenge"
BEFORE = BASE / "20261020T224042Z-fixture-register-before"
METRICS = BASE / "20261020T225535Z-rust-structure/receipt.json"


def document(source):
    target = source.with_name(source.stem + store.SUFFIX)
    return target, store.load(target) if target.is_file() else store.empty(source)


def main():
    first = json.loads((FIRST / "receipt.json").read_text())
    second = json.loads((SECOND / "receipt.json").read_text())
    review = json.loads((FIRST / "adversarial-review.json").read_text())
    metrics = json.loads(METRICS.read_text())
    audit = json.loads((FIRST / "host-custody-audit.json").read_text())
    assert first["outcomes"] == {"KILLED": 30, "SURVIVED": 1, "INVALID": 0, "INCONCLUSIVE": 0, "UNRUN": 0}
    assert review["reviewed_classification"] == {"KILLED": 30, "DEMONSTRABLY_EQUIVALENT": 1}
    assert review["receipt_sha256"] == pin(FIRST / "receipt.json")["sha256"]
    assert second["status"] == "PASS" and second["outcomes"]["KILLED"] == 1
    assert second["mutants"][0]["name"] == "overlapping traversal guards jointly omitted"
    for receipt in (first, second):
        assert receipt["inputs_unchanged"] and receipt["dependencies_unchanged"]
        assert receipt["source_sha256"] == pin(ROOT / SOURCE)["sha256"]
        assert receipt["baseline"]["status"] == receipt["release"]["status"] == "SURVIVED"
        assert receipt["clippy"]["status"] == "PASS" and receipt["invalid_control"]["status"] == "INVALID"
        for name, digest in receipt["inputs"].items():
            assert pin(ROOT / name)["sha256"] == digest, name
    assert metrics["status"] == "PASS" and metrics["source"] == pin(ROOT / SOURCE) and metrics["unchanged"]
    assert metrics["maxima"] == {"ast_decision_upper_bound": 14, "weighted_control_upper_bound": 17, "control_nesting": 2}
    assert audit["status"] == "PASS" and audit["entries"] == len(json.loads((ROOT / ASSET).read_text())["fixtures"])
    assert "all_passed=True" in (BASE / "batch5-atlas.log").read_text()
    assert "5 passed" in (BASE / "batch5-atlas-tests.log").read_text()
    evidence = [pin(p) for p in [FIRST / "receipt.json", SECOND / "receipt.json", FIRST / "adversarial-review.json",
        FIRST / "host-custody-audit.json", METRICS, BASE / "batch5-atlas.log", BASE / "batch5-atlas-tests.log"]]
    source = ROOT / SOURCE
    target, doc = document(source)
    doc["assurance"] = "Append-only compiled historical counterexamples and an independently reviewed, source-bound Rust custody assessment. No whole-scope certification."
    historical_source = BEFORE / "sources" / SOURCE
    old = {"path": SOURCE, "sha256": pin(historical_source)["sha256"]}
    old_evidence = [pin(BEFORE / p) for p in ["receipt.json", "review.json", "run.log"]] + [pin(historical_source)]
    add(doc, target, "historical-compiled-counterexample",
        {"AuthorityEffect": "None", "artifact": old, "profile": "Exact", "purpose": "Earlier unbounded Option-based fixture checker; later contracts are not retroactive.",
         "finding": "A missing path returns None, the same result as successful verification. Legacy manifest-relative registry reads fail. The Windows-prefix root probe is explicitly not used as independent grading evidence.", "evidence": old_evidence},
        {"AuthorityEffect": "None", "artifact": old, "rubric": pin(ROOT / "SCORING.md"), "profile": "Exact", "level": "L2",
         "level_basis": "Standard table/hash test utility without bounded typed admission, reliable registration or owned verified result API.",
         "gates": {"G1": None, "G2": "E", "G3": "E", "G4": "D", "G5": None}, "grade_ceiling": "E",
         "is_complete": False, "composite_grade": None, "score_token": None, "target_achieved": False, "evidence": old_evidence})
    contract = {"AuthorityEffect": "None", "artifact": pin(source), "profile": "Exact", "claim": "urn:omega:fqm:fixtures:bounded-register-custody:v1",
        "purpose": "Bounded local-file custody validation for a historical fixture register, with typed metadata and immutable owned observations.",
        "operations": {
            "parse_register": "Require <=1 MiB existing bytes and the declared serde schema. Duplicate/unknown fields, wrong authority/kinds, malformed SHA/path/text/list values and duplicate relocated receipt paths refuse. Returns owned metadata only, with no public deserialization bypass.",
            "verify_receipt": "Canonicalize a supplied local root, refuse unsafe relative/device paths and canonical escapes, require a regular file, stream complete SHA-256 under the per-file bound, then return an owned read-only observation of the bytes read at that call.",
            "verify_register": "Verify every receipt and existence of referenced fixture-value files, under the total byte cap. Return the first indexed typed refusal instead of partial success. Fixture-value bytes and producer/reason assertions are not independently certified.",
            "relocation": "Three explicit legacy prefix rules only: Rust test fixtures, MUB paper artifacts, and MUB source/fixture-value names. No basename search or external-repository fallback.",
            "registration": "The standalone code/rust/quality/fixture_register crate imports this actual source file and its pinned tests. Other test copies and the main Cargo workspace are not certified by this receipt."},
        "policy": "Register<=1 MiB, <=4096 entries, <=128 list items, path<=2048 UTF-8 bytes, text<=8192 UTF-8 bytes. Receipt<=16 MiB and all receipt reads<=64 MiB; one extra byte detects overrun before refusal. SHA streaming uses an 8192-byte buffer. All limits are declared engineering policies.",
        "failure_boundary": "ReceiptError variants retain validation/limit/JSON location/IO operation and ErrorKind/digest mismatch/containment distinctions; RegistryFailure adds the entry index. File handles use Rust ownership on all exits. VerifiedReceipt fields are private and do not alias caller data. The parser does not allocate or read the caller's initial byte slice.",
        "trust": "Pinned compiler/Cargo and Rust package sources plus declared serde/SHA/std semantics. Non-Rust dependency build assets and compiler internals remain trusted. This assumes local non-hostile filesystem state; no guarantee against replacement races, hostile concurrent writes, blocking OS IO, hash collisions or future file changes.",
        "cost": "Linear parsing in the admitted register bytes, metadata/path work in the admitted reference count, and streaming hashing in admitted total receipt bytes. Stores owned metadata/observations, not complete receipt files. No measured peak-heap or wall-clock guarantee.",
        "scope_ceiling": "20 historical fixture digest matches, never calculated MUB verdicts, categorification, mathematical proof, producer-truth certification or authority promotion.",
        "evidence": evidence}
    scoring = {"AuthorityEffect": "None", "artifact": pin(source), "profile": "Exact", "rubric": pin(ROOT / "SCORING.md"),
        "level": "L4", "level_basis": "Production API grain and custody: strict bounded admission, opaque admitted and verified states, owned observations, typed errors, root/path preflight and canonical containment, complete streaming IO with separate total/per-file limits, explicit registration and supervised source-bound fault checks.",
        "gates": {"G1": "C", "G2": "C", "G3": "C", "G4": "C", "G5": "B"},
        "basis": {
            "G1": "Exact source/asset/dependency pins, unique claim URN and literal authority ceiling. Historical annotations remain annotations; no complete downstream provenance or derivation claim.",
            "G2": "Known SHA-256 abc/empty controls, exact bounded counters, metadata admission and independent Python byte/digest audit of all 20 sealed inputs. No approximate arithmetic on admitted paths.",
            "G3": "Typed expected failure and indexed register refusal, private immutable observations and RAII file ownership. Actual Windows junction escape refused. No formal panic-freedom, filesystem-race immunity or hard real-time claim.",
            "G4": "14 debug and 14 release tests, Clippy with warnings denied, and compiled-source bindings. 31 distinct non-equivalent faults killed across two executions. One original survivor is retained and excluded only by the written absorption proof; two deliberate invalid controls are excluded, never kills. No exhaustive fault-space or alternate compiler claim.",
            "G5": "Complete syn AST function coverage, calibrated conservative decision/control bounds and reviewed linear cost envelope. Lizard's missed digest_text boundary is disclosed rather than replaced with a false zero or claimed agreement. No Sonar-conformance, expanded dependency, heap or runtime proof."},
        "metrics": metrics["maxima"], "mutation_outcomes": {"KILLED": 31, "DEMONSTRABLY_EQUIVALENT": 1},
        "is_complete": True, "composite_grade": "C", "score_token": "L4C", "requested_target": "L4E or higher", "target_achieved": True,
        "target_scope": "This exact Rust source only; full 24-directory objective remains open.", "evidence": evidence}
    add(doc, target, "bounded-rust-custody-review", contract, scoring)
    store.save(target, doc)
    rust_row = {"source": pin(source), "companion": pin(target), "score_token": "L4C", "evidence": evidence}
    asset = ROOT / ASSET
    asset_target, asset_doc = document(asset)
    asset_doc["assurance"] = "Historical bytes preserved and independently audited through the consumer. Static data remains below the requested L4 capability threshold."
    rename = json.loads((BEFORE / "rename.json").read_text())
    assert rename["byte_identical"] and rename["sha256"] == pin(asset)["sha256"]
    asset_contract = {"AuthorityEffect": "None", "artifact": pin(asset), "profile": "Non-Numeric", "claim": "urn:omega:fqm:fixtures:historical-registry-data:v1",
        "purpose": "Static historical fixture metadata; original bytes and digests preserved under a collision-free filename.",
        "former_path": rename["old"], "operations": "No executable operations. Consumed by the bounded Rust validator; its 20 receipt paths resolve explicitly and match the stored digests.",
        "scope_ceiling": "Annotations remain historical claims, not computed proof results. A static registry does not itself deliver L4 production API capability.",
        "evidence": evidence + [pin(BEFORE / "rename.json")]}
    asset_score = {"AuthorityEffect": "None", "artifact": pin(asset), "profile": "Non-Numeric", "rubric": pin(ROOT / "SCORING.md"),
        "level": "L1", "level_basis": "A static metadata table; a production consumer cannot confer its own capability level on the data file.",
        "gates": {"G1": "C", "G2": "C", "G3": "C", "G4": "C", "G5": "B"},
        "basis": "Byte-identical rename, declared historical authority ceiling, strict consumer schema/bounds, and independently audited resolution/digests of all 20 records. Bounded JSON data structure; imperative CCN is inapplicable, never asserted zero.",
        "is_complete": True, "composite_grade": "C", "score_token": "L1C", "requested_target": "L4E or higher", "target_achieved": False,
        "target_gap": "Static data does not meet the requested L4 capability threshold. Retained as an explicit below-target review; no relabeling or deletion to improve counts.", "evidence": asset_contract["evidence"]}
    add(asset_doc, asset_target, "historical-registry-data-review", asset_contract, asset_score)
    store.save(asset_target, asset_doc)
    ancillary = []
    for name in ["code/rust/quality/fixture_register/src/lib.rs", "code/rust/quality/fixture_register/src/validator_tests.rs", "code/rust/quality/fixture_register/src/bin/observe.rs",
                 "code/rust/quality/fixture_register/Cargo.toml", "code/rust/quality/fixture_register/Cargo.lock", "code/rust/quality/expanded_scope/check_fixture_register.py",
                 "code/rust/quality/expanded_scope/record_fixture_register.py", "code/rust/quality/expanded_scope/summarize.py"]:
        path = ROOT / name
        companion, auxiliary = document(path)
        auxiliary["assurance"] = "Partial review-support assessment only; unassessed gates and source hashes remain explicit."
        record = {"AuthorityEffect": "None", "artifact": pin(path), "purpose": "Owned review/registration support outside the requested directories; own source assurance remains partial.", "evidence": evidence}
        score = {"AuthorityEffect": "None", "artifact": pin(path), "rubric": pin(ROOT / "SCORING.md"), "level": None,
            "gates": {"G1": "C", "G2": None, "G3": None, "G4": None, "G5": None}, "is_complete": False, "composite_grade": None,
            "score_token": None, "target_achieved": False, "evidence": evidence}
        add(auxiliary, companion, "partial-review-support-" + pin(path)["sha256"][:12], record, score)
        store.save(companion, auxiliary)
        ancillary.append({"source": pin(path), "companion": pin(companion)})
    result = {"AuthorityEffect": "None", "full_scope_target_achieved": False, "files": {SOURCE: rust_row},
        "below_target_assets": {ASSET: {"source": pin(asset), "companion": pin(asset_target), "score_token": "L1C"}}, "ancillary_partial_reviews": ancillary}
    (BASE / "batch5-assessments.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"complete_at_target": 1, "reviewed_below_target": 1, "full_scope_target_achieved": False}))


if __name__ == "__main__":
    main()
