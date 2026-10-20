"""Activate a challenged ordered candidate, preserving source and assessment custody.

AuthorityEffect: None. Integration and individual scoring are separate steps.
"""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
from replay import ROOT, RUST, digest, write, inventory, subjects
from records import metric_ceiling


def read(path):
    return json.loads(path.read_text(encoding="utf8"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trial", required=True, type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    trial_path = args.trial.resolve()
    trial = read(trial_path)
    folder = trial_path.parent
    candidate = Path(__file__).with_name("ordered_port") / "ordered.rs"
    target = RUST / "src/linear_algebra/ordered.rs"
    origin = read(candidate.with_name("origin.json"))
    assert digest(target) == origin["sha256"], "Live ordered origin changed"
    assert digest(candidate) == trial["candidate_sha256"] == digest(folder / "candidate.rs")
    assert trial["live_sources_unchanged"] and trial["candidate_unchanged"] and trial["dependencies_unchanged"]
    assert read(folder / "source_manifest.json") == inventory(), "Live inventory changed after trial"
    assert digest(folder / "dependency_sources.json") == trial["dependency_sources_sha256"]
    assert all(Path(name).is_file() and digest(Path(name)) == pin
               for name, pin in read(folder / "dependency_sources.json").items())
    assert trial["accounting"] == dict(killed=16, survived=0, demonstrably_equivalent=0,
        invalid=0, inconclusive=0, unrun=0, conservative_ratio=1.0)
    assert digest(folder / "mutations.json") == trial["mutations_sha256"]
    assert len(trial["runs"]) == len(trial["restored_runs"]) == 2
    assert len(trial["metric_runs"]) == 3
    runs = [*trial["runs"], *trial["restored_runs"], *trial["metric_runs"],
            *(item["run"] for item in read(folder / "mutations.json"))]
    assert all(run.get("exit_code") == 0 and not run.get("timed_out")
               for run in [*trial["runs"], *trial["restored_runs"], *trial["metric_runs"]])
    assert all(digest(ROOT / run["log"]) == run["log_sha256"] for run in runs)
    measured = read(folder / "metrics.json")
    assert len(measured) == 1 and metric_ceiling(next(iter(measured.values())))[0] == "A"
    assert all(digest(ROOT / name) == pin for name, pin in trial["metric_tool_sources"].items())
    # One real root consumer reads the former public field directly.
    consumer = RUST / "src/qm/campaigns/gleason.rs"
    old = consumer.read_bytes()
    needle = b"        .negative\r\n        == 0;" if b"\r\n" in old else b"        .negative\n        == 0;"
    assert old.count(needle) == 1, "Review the direct inertia-count consumer again"
    replacement = old.replace(needle, needle.replace(b".negative", b".negative()"), 1)
    print("Validated ordered candidate, 16 challenges and direct QM getter migration.", flush=True)
    if args.check:
        return
    out = ROOT / "evidence/quality/l4a_six" / (datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-ordered-activation")
    out.mkdir()
    shutil.copyfile(__file__, out / "activate.py")
    updates = [(target, candidate.read_bytes()), (consumer, replacement)]
    before = {str(path.relative_to(ROOT)): digest(path) for path, _ in updates}
    for path, _ in updates:
        saved = out / "before" / path.relative_to(ROOT)
        saved.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, saved)
    for subject in subjects():
        for suffix in (".scoring.yaml", ".contract.yaml"):
            sidecar = Path(str(subject) + suffix)
            if sidecar.exists():
                saved = out / "previous_assessment" / sidecar.relative_to(ROOT)
                saved.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(sidecar, saved)
    changed = []
    try:
        for path, data in updates:
            assert digest(path) == before[str(path.relative_to(ROOT))], "Target changed during activation"
            path.write_bytes(data)
            changed.append(path)
    except BaseException:
        for path in reversed(changed):
            path.write_bytes((out / "before" / path.relative_to(ROOT)).read_bytes())
        raise
    write(out / "activation.json", {"AuthorityEffect": "None", "trial": str(trial_path.relative_to(ROOT)),
        "trial_sha256": digest(trial_path), "before": before,
        "after": {str(path.relative_to(ROOT)): digest(path) for path, _ in updates},
        "scope": "Source activation only. Fresh integrated evidence and sidecar validation remain required."})
    print(out, flush=True)


if __name__ == "__main__":
    main()
