"""Exact census, custody and adversarial certificate checks at the admitted bound."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import stat
import subprocess
import sys
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace

import pytest

PACKAGE = next(parent for parent in Path(__file__).resolve().parents
               if (parent / "witnessed_difference_programme.md").is_file())
sys.path.insert(0, str(PACKAGE / "code"))

from native_future_compression.certificate import (  # noqa: E402
    QUESTIONS,
    action_id,
    build_certificate,
    check_all_lifts,
    check_certificate,
    check_partitions,
    check_path,
    check_witnesses,
    compose_paths,
    fixture_inputs,
    lift_path,
    make_state,
    project_path,
)
from native_future_compression.model import (  # noqa: E402
    ACTIONS,
    NATIVE_SCHEMA,
    PROFILE,
    PROFILES,
    TASK,
    Model,
    Refusal,
    clipped_report,
    decode,
    mark,
    state_of,
)
from native_future_compression.replay import (  # noqa: E402
    NativeCustody,
    compare_native,
    compare_original,
    file_sha,
    read_artifact,
    strict_json,
    strict_json_with_snapshot,
    verify_closure,
    write_artifact,
)


@pytest.fixture(scope="module")
def model():
    return Model()


@pytest.fixture(scope="module")
def partitions(model):
    return model.partition()


@pytest.fixture(scope="module")
def expected_binding():
    # A unit-test binding is explicit; production CLI supplies checked source
    # and executable hashes, never this fixture.
    return {"task": TASK, "profile": deepcopy(PROFILE), "questions": deepcopy(QUESTIONS),
            "actions": deepcopy(ACTIONS), "source_sha256": {"test-input": "a"*64}}


@pytest.fixture(scope="module")
def certificate(model, partitions, expected_binding):
    return build_certificate(model, partitions, expected_binding)


def test_exact_census_layers_decoder_and_all_member_lifts(model, partitions, certificate, expected_binding):
    receipt = check_certificate(model, certificate, expected_binding)
    assert receipt["states"] == receipt["decoder_replays"] == 29771
    assert receipt["layer_counts"] == {PROFILES[0]: [4307, 29767, 29771],
                                       PROFILES[1]: [29465, 29771, 29771]}
    assert receipt["member_step_lifts"] == check_all_lifts(model, partitions) > 0
    assert len(ACTIONS) == 42 and certificate["summary"]["offers"] == 1250382
    for fiber in certificate["summary"]["result_mark_fibers"]:
        assert all(fiber["class_counts"][p][2] == fiber["raw_states"] for p in PROFILES)


@pytest.mark.parametrize("change", ("bound", "horizon", "terminal", "label", "source", "task"))
def test_changed_binding_refuses(model, certificate, expected_binding, change):
    bad = deepcopy(certificate)
    b = bad["binding"]
    if change == "bound":
        b["profile"]["max_count"] = 5
    elif change == "horizon":
        b["profile"]["horizon"] = 3
    elif change == "terminal":
        b["questions"]["terminal_profiles"][0] = PROFILES[1]
    elif change == "label":
        b["actions"][0]["y"] = 2
    elif change == "source":
        b["source_sha256"]["test-input"] = "b"*64
    else:
        b["task"] += "-changed"
    with pytest.raises(Refusal, match="binding"):
        check_certificate(model, bad, expected_binding)


@pytest.mark.parametrize("change", ("wrong_guard", "excluded_as_disabled", "missing_price",
                                     "missing_occurrence", "missing_face_key", "child_class"))
def test_supplied_bad_witness_is_refused(model, partitions, certificate, change):
    bad = deepcopy(certificate["witnesses"])
    offers = bad["offers"]
    if change == "wrong_guard":
        offers["invalid_address"]["edge"]["status"] = "admitted"
    elif change == "excluded_as_disabled":
        offers["term_exclusion"]["edge"]["status"] = "native_disabled"
    elif change == "missing_price":
        offers["count_exclusion"]["edge"]["price"] = None
    elif change == "missing_occurrence":
        offers["zero_price_remove"]["edge"]["occurrences"] = 0
    elif change == "missing_face_key":
        offers["face_key"]["present"]["balance"] = []
    else:
        bad["growth"]["left_path"]["quotient"]["classes"][-1] += 1
    with pytest.raises(Refusal):
        check_witnesses(model, partitions, bad)


def test_merged_distinct_state_and_changed_child_layer_refuse(model, partitions):
    bad = deepcopy(partitions)
    left, right, _ = fixture_inputs()["horizon_collision"]
    a, b = model.index[left], model.index[right]
    bad[PROFILES[0]][2][b] = bad[PROFILES[0]][2][a]
    with pytest.raises(Refusal, match="class"):
        check_partitions(model, bad)
    bad = deepcopy(partitions)
    bad[PROFILES[0]][0][0] = 1
    with pytest.raises(Refusal, match="class"):
        check_partitions(model, bad)


def test_original_start_and_suffix_horizon_binding(model, partitions, certificate):
    comp = certificate["witnesses"]["composition"]
    initial = make_state(2)
    bad = deepcopy(comp["prefix"])
    bad["original"] = make_state(2, r=((0, 1, 1),)).wire()
    with pytest.raises(Refusal, match="original"):
        check_path(model, partitions, bad, initial, 2, PROFILES[0])
    middle = model.states[comp["prefix"]["raw_ids"][-1]]
    reset = project_path(model, partitions, PROFILES[0], 2, middle,
                         comp["suffix"]["quotient"]["actions"])
    with pytest.raises(Refusal, match="horizon"):
        compose_paths(model, partitions, comp["prefix"], reset, initial, 2, PROFILES[0])
    # Both remaining horizons are valid individually, but the second raw start
    # must be exactly the first raw endpoint, including the filled set.
    substituted = project_path(model, partitions, PROFILES[0], 1,
                               make_state(3, filled=((0, 2, 1),)),
                               comp["suffix"]["quotient"]["actions"])
    with pytest.raises(Refusal, match="original"):
        compose_paths(model, partitions, comp["prefix"], substituted, initial, 2, PROFILES[0])


def test_lift_keeps_each_original_in_a_nonsingleton_layer(model, partitions):
    left, right, _ = fixture_inputs()["horizon_collision"]
    action = action_id("remove", relation="r", x=0, y=1)
    path = project_path(model, partitions, PROFILES[0], 1, left, [action])
    lifted = lift_path(model, partitions, path["quotient"], right, 1, PROFILES[0])
    assert lifted["original"] == right.wire() != path["original"]
    assert lifted["raw_ids"] != path["raw_ids"]
    assert lifted["quotient"] == path["quotient"]
    with pytest.raises(Refusal):
        lift_path(model, partitions, path["quotient"], right, 2, PROFILES[0])


def test_refusals_never_become_paths_and_terminal_has_no_execution(model, partitions):
    state = make_state(3)
    add = action_id("add_term")
    for profile in PROFILES:
        with pytest.raises(Refusal, match="refused"):
            project_path(model, partitions, profile, 2, state, [add])
        with pytest.raises(Refusal, match="horizon"):
            project_path(model, partitions, profile, 0, make_state(0), [add])
    assert model.edges[model.index[state]][add].status == "bound_excluded"
    assert model.edges[model.index[make_state(0)]][add].status == "admitted"


def test_count_reconstruction_special_cases_and_outside_bound():
    for r, s in ((3, 1), (2, 2), (4, 0), (0, 4)):
        state = make_state(1, r=((0, 0, r),), s=((0, 0, s),))
        assert decode(clipped_report(state)) == state
    left = make_state(2, r=((0, 1, 2), (1, 0, 3)))
    right = make_state(2, r=((0, 1, 3), (1, 0, 2)))
    assert clipped_report(left) == clipped_report(right) and mark(left) == mark(right)
    with pytest.raises(Refusal, match="bound"):
        state_of(left.wire())
    with pytest.raises(Refusal):
        decode(clipped_report(left))


@pytest.mark.parametrize("mutate", (
    lambda p: p.update(n=True),
    lambda p: p["r"].__setitem__(0, 1.0),
    lambda p: p["r"].__setitem__(0, -1),
    lambda p: p.update(filled=[[0, 0, 0]]),
    lambda p: p.update(extra=0),
))
def test_malformed_raw_packets_refuse(mutate):
    packet = make_state(1).wire()
    mutate(packet)
    with pytest.raises(Refusal):
        state_of(packet)


@pytest.mark.parametrize("text", ('{"n":0,"n":1}', '{"price":NaN}', '{"price":Infinity}',
                                  '{"price":1e999}', '{"price":1.0}'))
def test_strict_disk_json_refuses(tmp_path, text):
    path = tmp_path/"candidate.json"
    path.write_text(text, encoding="utf-8")
    with pytest.raises(ValueError):
        strict_json(path)


@pytest.mark.monorepo
def test_original_closure_and_all_original_states_and_offers(model, tmp_path):
    root = os.environ.get("WDP_ORIGINAL_SOURCE_ROOT")
    if not root:
        pytest.skip("Set WDP_ORIGINAL_SOURCE_ROOT to the recovered pinned revision for full original replay")
    manifest = PACKAGE/"manifests/source_replay_inputs.json"
    rows = verify_closure(root, manifest)
    assert len(rows) == 19
    replay = compare_original(model, root, manifest)
    assert replay["states"] == 29771 and replay["offers"] == 1250382
    # Changed manifest hashes are rejected before any original module is loaded.
    changed = json.loads(manifest.read_text(encoding="utf-8"))
    row = next(r for r in changed["files"] if r["repository"] == "H3V7N5QF")
    row["sha256"] = "0"*64
    forged = tmp_path/"changed_source_manifest.json"
    forged.write_text(json.dumps(changed), encoding="utf-8")
    with pytest.raises(Refusal, match="source bytes"):
        verify_closure(root, forged)


@pytest.mark.parametrize("change", ("binary", "owner", "adapter", "builder", "receipt",
                                     "added_source", "omitted_owner", "traversal_error", "broken_subtree",
                                     "omitted_dependency_package"))
def test_native_build_custody_refuses_changes(tmp_path, monkeypatch, change):
    root = tmp_path/"repo"
    workspace = root/"omega_engine/crates_rs"
    owner = workspace/"omega_wdp"
    (owner/"src").mkdir(parents=True)
    files = [workspace/"Cargo.toml", workspace/"Cargo.lock", owner/"Cargo.toml"]
    files += [owner/"src"/name for name in ("genesis_source_execution.rs", "genesis_marked_result.rs",
                                          "genesis_ongoing_adapter.rs", "native_future_compression.rs")]
    linked = workspace/"linked"
    (linked/"src").mkdir(parents=True)
    files += [linked/"Cargo.toml", linked/"src/lib.rs"]
    for path in files:
        path.write_bytes(b"source\n")
    (workspace/"Cargo.toml").write_text("[workspace]\n", encoding="utf-8")
    (owner/"Cargo.toml").write_text('[package]\nname="omega_wdp"\n[dependencies]\nlinked={path="../linked"}\n', encoding="utf-8")
    (linked/"Cargo.toml").write_text('[package]\nname="linked"\n', encoding="utf-8")
    package = root/"paper"
    adapter = package/"code/causal_certificates/native/main.rs"
    adapter.parent.mkdir(parents=True)
    adapter.write_bytes(b"adapter\n")
    builder = adapter.with_name("build_native.py")
    builder.write_bytes(b"builder\n")
    binary = tmp_path/"native.bin"
    binary.write_bytes(b"executable fixture\n")
    build = {"schema": "wdp-causal-native-build-v1", "authority_effect": "None",
             "sources": {p.relative_to(root).as_posix(): file_sha(p) for p in files},
             "binary_sha256": file_sha(binary), "adapter_sha256": file_sha(adapter),
             "adapter_builder_sha256": file_sha(builder)}
    receipt = tmp_path/"build.json"
    receipt.write_text(json.dumps(build), encoding="utf-8")
    custody = NativeCustody(binary, receipt, root, package)
    if change == "binary":
        binary.write_bytes(b"changed")
    elif change == "owner":
        (owner/"src/native_future_compression.rs").write_bytes(b"changed")
    elif change == "adapter":
        adapter.write_bytes(b"changed")
    elif change == "builder":
        builder.write_bytes(b"changed")
    elif change == "receipt":
        receipt.write_text(json.dumps(build, indent=2), encoding="utf-8")
    elif change == "added_source":
        (owner/"src/new.rs").write_bytes(b"new source")
    elif change == "traversal_error":
        def unreadable(path, **kwargs):
            kwargs["onerror"](OSError("injected unreadable source directory"))
            return iter(())
        monkeypatch.setattr("native_future_compression.replay.os.walk", unreadable)
        with pytest.raises(OSError, match="unreadable"):
            custody.verify()
        return
    elif change == "broken_subtree":
        broken = owner/"build"
        original_link, original_stat = Path.is_symlink, Path.lstat
        monkeypatch.setattr(Path, "is_symlink", lambda p: p == broken or original_link(p))
        monkeypatch.setattr(Path, "lstat", lambda p: SimpleNamespace(st_mode=stat.S_IFLNK,
                           st_file_attributes=0) if p == broken else original_stat(p))
        with pytest.raises(Refusal, match="subtree"):
            custody.verify()
        return
    elif change == "omitted_dependency_package":
        build["sources"] = {k: v for k, v in build["sources"].items() if "/linked/" not in k}
        receipt.write_text(json.dumps(build), encoding="utf-8")
        with pytest.raises(Refusal, match="manifest absent"):
            NativeCustody(binary, receipt, root, package)
        return
    else:
        del build["sources"][(owner/"src/native_future_compression.rs").relative_to(root).as_posix()]
        receipt.write_text(json.dumps(build), encoding="utf-8")
        with pytest.raises(Refusal, match="absent"):
            NativeCustody(binary, receipt, root, package)
        return
    with pytest.raises(Refusal):
        custody.verify()


def test_native_build_custody_accepts_an_aliased_source_root(tmp_path, monkeypatch):
    """A root named through an alias (a subst drive or an 8.3 short name) resolves
    to a different spelling; containment must compare resolved paths on both sides."""
    from native_future_compression import replay
    alias = tmp_path/"repo"
    workspace = alias/"omega_engine/crates_rs"
    owner = workspace/"omega_wdp"
    (owner/"src").mkdir(parents=True)
    files = [workspace/"Cargo.toml", workspace/"Cargo.lock", owner/"Cargo.toml"]
    files += [owner/"src"/name for name in ("genesis_source_execution.rs", "genesis_marked_result.rs",
                                          "genesis_ongoing_adapter.rs", "native_future_compression.rs")]
    for path in files:
        path.write_bytes(b"source\n")
    (workspace/"Cargo.toml").write_text("[workspace]\n", encoding="utf-8")
    (owner/"Cargo.toml").write_text('[package]\nname="omega_wdp"\n', encoding="utf-8")
    adapter = alias/"paper/code/causal_certificates/native/main.rs"
    adapter.parent.mkdir(parents=True)
    adapter.write_bytes(b"adapter\n")
    adapter.with_name("build_native.py").write_bytes(b"builder\n")
    binary = tmp_path/"native.bin"
    binary.write_bytes(b"executable fixture\n")
    sources = {p.relative_to(alias).as_posix(): file_sha(p) for p in files}
    receipt = tmp_path/"build.json"
    receipt.write_text(json.dumps({"schema": "wdp-causal-native-build-v1", "authority_effect": "None",
                                   "sources": sources, "binary_sha256": file_sha(binary),
                                   "adapter_sha256": file_sha(adapter),
                                   "adapter_builder_sha256": file_sha(adapter.with_name("build_native.py"))}),
                       encoding="utf-8")
    canonical = tmp_path/"canonical_spelling"
    original = Path.resolve
    def aliased(self, *args, **kwargs):
        path = original(self, *args, **kwargs)
        return canonical/path.relative_to(original(alias)) if path.is_relative_to(original(alias)) else path
    monkeypatch.setattr(Path, "resolve", aliased)
    manifests, _ = replay.local_dependency_manifests(alias, sources)
    assert manifests == {workspace/"Cargo.toml", owner/"Cargo.toml"}
    NativeCustody(binary, receipt, alias, alias/"paper").verify()


@pytest.mark.parametrize("change", ("extra", "state_bool", "state_double", "state_unknown",
                                     "edge_bool", "edge_double", "edge_unknown"))
def test_malformed_native_census_refuses(model, partitions, change):
    # Only the first row is needed: each altered row must fail before the
    # remaining placeholders can be read.
    native = {"schema": NATIVE_SCHEMA, "profile": deepcopy(PROFILE), "actions": deepcopy(ACTIONS),
              "states": [None]*len(model.states), "edges": [None]*len(model.states),
              "partitions": partitions}
    native["states"][0] = model.state_wire(0)
    native["edges"][0] = [e.wire() for e in model.edges[0]]
    if change == "extra":
        native["extra"] = 0
        error = "fields"
    elif change.startswith("state"):
        if change == "state_unknown":
            native["states"][0]["extra"] = 0
        else:
            native["states"][0]["n"] = False if change == "state_bool" else 0.0
        error = "native state or observation: 0"
    else:
        if change == "edge_unknown":
            native["edges"][0][0]["extra"] = 0
        else:
            native["edges"][0][0]["occurrences"] = False if change == "edge_bool" else 0.0
        error = "native offer: 0"
    with pytest.raises(Refusal, match=error):
        compare_native(model, partitions, native)


@pytest.mark.parametrize("node", ("symlink", "reparse", "directory"))
def test_source_custody_rejects_nonregular_nodes(tmp_path, monkeypatch, node):
    path = tmp_path/"manifest.json"
    path.write_text("{}", encoding="utf-8")
    original = Path.lstat
    def altered(self, *args, **kwargs):
        if self == path:
            return SimpleNamespace(st_mode={"symlink": stat.S_IFLNK, "directory": stat.S_IFDIR,
                                            "reparse": stat.S_IFREG}[node],
                                   st_file_attributes=0x400 if node == "reparse" else 0)
        return original(self, *args, **kwargs)
    monkeypatch.setattr(Path, "lstat", altered)
    with pytest.raises(Refusal, match="nonregular"):
        strict_json(path)
    with pytest.raises(Refusal, match="nonregular"):
        file_sha(path)


@pytest.mark.parametrize("change", ("content", "format", "same_bytes_replacement", "restored_bytes",
                                     "reparse", "parent_reparse"))
def test_exact_parsed_bytes_remain_bound_to_file_identity(tmp_path, monkeypatch, change):
    path = tmp_path/"candidate.json"
    raw = b'{ "answer" : 1 }\n'
    path.write_bytes(raw)
    parsed, snapshot = strict_json_with_snapshot(path)
    assert parsed == {"answer": 1} and snapshot.sha256 == hashlib.sha256(raw).hexdigest()
    if change == "content":
        path.write_bytes(b'{"answer":2}')
    elif change == "format":
        path.write_bytes(b'{"answer":1}')
    elif change == "same_bytes_replacement":
        replacement = tmp_path/"replacement.json"
        replacement.write_bytes(raw)
        replacement.replace(path)
    elif change == "restored_bytes":
        path.write_bytes(b'{"answer":2}')
        path.write_bytes(raw)
        os.utime(path, ns=(path.stat().st_atime_ns, snapshot.stamp[3]+1_000_000_000))
    else:
        target = path if change == "reparse" else tmp_path
        original = Path.lstat
        def changed(self, *args, **kwargs):
            if self == target:
                return SimpleNamespace(st_mode=stat.S_IFREG if self == path else stat.S_IFDIR,
                                       st_file_attributes=0x400)
            return original(self, *args, **kwargs)
        monkeypatch.setattr(Path, "lstat", changed)
    with pytest.raises(Refusal):
        snapshot.verify()


def test_source_parse_hash_cannot_bind_a_second_read(tmp_path, monkeypatch):
    from native_future_compression import replay
    path = tmp_path/"receipt.json"
    checked = b'{"source":"checked"}'
    path.write_bytes(checked)
    parse = replay.parse_json_bytes
    def mutate_after_read(data):
        path.write_bytes(b'{"source":"changed"}')
        return parse(data)
    monkeypatch.setattr(replay, "parse_json_bytes", mutate_after_read)
    value, snapshot = strict_json_with_snapshot(path)
    assert value == {"source": "checked"}
    assert snapshot.sha256 == hashlib.sha256(checked).hexdigest()
    with pytest.raises(Refusal):
        snapshot.verify()


@pytest.mark.parametrize("mode,change", (
    ("check", "none"), ("build", "none"),
    ("check", "candidate"), ("check", "census"), ("check", "source"),
    ("check", "original"), ("check", "build_receipt"), ("check", "same_bytes_replacement"),
    ("build", "build_output"), ("check", "replay_receipt"), ("check", "source_after_receipt"),
    ("check", "null_root"), ("check", "bool_root"), ("check", "number_root"),
    ("check", "string_root"), ("check", "array_root"), ("check", "native_timeout"),
))
def test_cli_refuses_changes_between_check_and_receipt(tmp_path, monkeypatch, capsys, mode, change):
    """Exercise real CLI artifact reads and publication gates around a controlled replay.

    Mathematical replay has its full-census tests above. Here controlled owners
    place mutations at the precise original-replay and output-write boundaries.
    """
    spec = importlib.util.spec_from_file_location("native_future_cli_io_test",
                                                PACKAGE/"scripts/check_native_future_compression.py")
    cli = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cli)
    root = tmp_path/"repo"
    root.mkdir()
    source = root/"checker.py"
    source.write_bytes(b"checked source\n")
    original_root = tmp_path/"original"
    original_root.mkdir()
    original = original_root/"source.py"
    original.write_bytes(b"checked original\n")
    census = tmp_path/"census.json"
    census_bytes = b'{ "census" : "checked" }\n'
    census.write_bytes(census_bytes)
    candidate = tmp_path/"certificate.json"
    candidate_bytes = b'{ "valid" : true, "partitions" : {} }\n'
    rejected_roots = {"null_root": b"null", "bool_root": b"false", "number_root": b"0",
                      "string_root": b'"text"', "array_root": b"[]"}
    candidate_bytes = rejected_roots.get(change, candidate_bytes)
    candidate.write_bytes(candidate_bytes)
    native_receipt = tmp_path/"build.json"
    native_receipt.write_bytes(b'{"build":"checked"}')
    binary = tmp_path/"binary.bin"
    binary.write_bytes(b"binary fixture")
    output_receipt = tmp_path/"replay.json"
    expected = {"source_sha256": {"checker.py": file_sha(source)},
                "original_source": [{"path": "source.py", "sha256": file_sha(original)}]}
    monkeypatch.setattr(cli, "binding", lambda package: deepcopy(expected))
    monkeypatch.setattr(cli, "verify_closure", lambda *args: None)
    class ControlledNative:
        def __init__(self, native_binary, receipt, *args):
            _, self.receipt_snapshot = strict_json_with_snapshot(receipt)
            self.artifacts = {binary: read_artifact(native_binary)[1]}
        def verify(self):
            self.receipt_snapshot.verify()
            for snapshot in self.artifacts.values():
                snapshot.verify()
        def reproduce(self, snapshot):
            if change == "native_timeout":
                raise subprocess.TimeoutExpired([str(binary)], 1200)
            snapshot.verify()
            return {"census_sha256": snapshot.sha256}
    monkeypatch.setattr(cli, "NativeCustody", ControlledNative)
    model_calls, partition_calls, producer_calls = [], [], []
    def partition():
        partition_calls.append(True)
        return {}
    def construct():
        model_calls.append(True)
        return SimpleNamespace(partition=partition)
    def produce(*args):
        producer_calls.append(True)
        return {"valid": True, "partitions": {}}
    monkeypatch.setattr(cli, "Model", construct)
    monkeypatch.setattr(cli, "build_certificate", produce)
    checked_candidates = []
    def check(model, value, bound):
        assert value == {"valid": True, "partitions": {}}
        checked_candidates.append(deepcopy(value))
        return {"fixture": "checked"}
    monkeypatch.setattr(cli, "check_certificate", check)
    def compare(model, partitions, value):
        assert value == {"census": "checked"}
        return {"fixture": "checked"}
    monkeypatch.setattr(cli, "compare_native", compare)
    def mutate(*args):
        targets = {"candidate": candidate, "census": census, "source": source,
                   "original": original, "build_receipt": native_receipt}
        if change in targets:
            targets[change].write_bytes(b'{"changed":true}')
        elif change == "same_bytes_replacement":
            replacement = tmp_path/"replacement.json"
            replacement.write_bytes(candidate_bytes)
            replacement.replace(candidate)
        return {"fixture": "checked"}
    monkeypatch.setattr(cli, "compare_original", mutate)
    def publish(path, data):
        snapshot = write_artifact(path, data)
        if ((change == "build_output" and path == candidate) or
                (change == "replay_receipt" and path == output_receipt)):
            path.write_bytes(b'{"changed":true}')
        if change == "source_after_receipt" and path == output_receipt:
            source.write_bytes(b"changed after output publication")
        return snapshot
    monkeypatch.setattr(cli, "write_artifact", publish)
    result = cli.main([mode, "--original-source-root", str(original_root), "--native-json", str(census),
                       "--native-bin", str(binary), "--native-build-receipt", str(native_receipt),
                       "--source-root", str(root), "--certificate", str(candidate),
                       "--receipt", str(output_receipt)])
    captured = capsys.readouterr()
    if mode == "check":
        assert not partition_calls and not producer_calls
    if change in rejected_roots:
        assert not model_calls and not checked_candidates and "root" in captured.err
    elif change == "native_timeout":
        assert not model_calls and not checked_candidates and "timed out" in captured.err
    else:
        assert checked_candidates
    if change == "none":
        assert result == 0
        receipt = strict_json(output_receipt)
        assert receipt["certificate_sha256"] == hashlib.sha256(candidate.read_bytes()).hexdigest()
        assert receipt["native_json_sha256"] == hashlib.sha256(census_bytes).hexdigest()
    else:
        assert result == 1 and "REFUSED:" in captured.err and not captured.out
