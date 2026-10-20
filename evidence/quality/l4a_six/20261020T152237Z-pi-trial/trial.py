"""Small standalone Cargo trial of the staged finite Pi model. AuthorityEffect: None."""
import json
from pathlib import Path
import shutil
import subprocess
from datetime import datetime, timezone
from collections import Counter
from replay import ROOT, RUST, inventory, digest, write, execute, dependency_sources, remove_owned
from scalar_port_faults import block
from mutations import classify


def recipes(source):
    entries = []
    def add(identity, prefix, before, after, mode="unit"):
        original = block(source, prefix)
        assert original.count(before) == 1, identity
        entries.append(dict(id=identity, before=original, after=original.replace(before, after, 1), mode=mode, outcome="unrun"))
    add("PI01-zero-fiber", "fn finite_pi_cardinality(", "if fibers.contains(&0) {", "if false {")
    add("PI02-cardinality-product", "fn finite_pi_cardinality(", ".checked_mul(*size)", ".checked_add(*size)")
    add("PI03-reference-limit", "    pub fn finite_model<'a>(", 'finite_pi_limit("reference bytes", bytes, limits.max_reference_bytes)?;', "")
    add("PI04-fiber-limit", "    pub fn finite_model<'a>(", 'finite_pi_limit("fibers", fiber_sizes.len(), limits.max_fibers)?;', "")
    add("PI05-cardinality-limit", "    pub fn finite_model<'a>(", 'finite_pi_limit("cardinality", cardinality, limits.max_cardinality)?;', "")
    add("PI06-admission-work", "    pub fn finite_model<'a>(", "finite_pi_work(fiber_sizes.len(), 4, limits.max_work)?;", "finite_pi_work(fiber_sizes.len(), 0, limits.max_work)?;")
    add("PI07-coordinate-boundary", "    fn admit_coordinates(", "if value >= size {", "if value > size {")
    add("PI08-empty-base", "fn finite_pi_cardinality(", "try_fold(1usize,", "try_fold(0usize,")
    add("PI09-rank-weight", "    pub fn rank(", "rank.checked_mul(size)", "rank.checked_add(size)")
    add("PI10-rank-arity", "    pub fn rank(", "self.arity(coordinates.len())?;", "")
    add("PI11-decode-arity", "    pub fn unrank_into(", "self.arity(output.len())?;", "")
    add("PI12-ordinal-boundary", "    pub fn unrank_into(", "if ordinal >= self.cardinality {", "if ordinal > self.cardinality {")
    add("PI13-output-digit", "    pub fn unrank_into(", "*slot = remaining % size;", "*slot = remaining / size;")
    add("PI14-output-quotient", "    pub fn unrank_into(", "remaining /= size;", "remaining %= size;")
    add("PI15-query-work", "    pub fn rank(", "finite_pi_work(self.fiber_sizes.len(), 6, self.limits.max_work)?;", "")
    add("PI16-model-privacy", "pub struct FinitePi<'a>", "    declaration: &'a PiType,\n    fiber_sizes: &'a [usize],\n    cardinality: usize,\n    limits: FinitePiLimits,", "    pub declaration: &'a PiType,\n    pub fiber_sizes: &'a [usize],\n    pub cardinality: usize,\n    pub limits: FinitePiLimits,", "doc")
    add("PI17-empty-product-query", "    pub fn rank(", "if self.cardinality == 0 {", "if false {")
    add("PI18-presentation-admission", "    pub fn finite_model<'a>(", "self.validate()?;", "")
    return entries


def main():
    candidate = ROOT / "evidence/quality/l4a_six/20261020-pi-candidate"
    original_manifest = json.loads((candidate / "candidate.json").read_text(encoding="utf8"))
    assert digest(ROOT / original_manifest["source"]) == original_manifest["origin_sha256"]
    original = (candidate / "pi_type.rs").read_bytes()
    entries = recipes(original.decode("utf8"))
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-pi-trial"
    out = ROOT / "evidence/quality/l4a_six" / stamp
    out.mkdir()
    work = RUST / "target/l4a-six" / stamp
    work.mkdir(parents=True)
    sources = inventory()
    write(out / "source_manifest.json", sources)
    shutil.copyfile(__file__, out / "trial.py")
    shutil.copyfile(Path(__file__).with_name("replay.py"), out / "replay.py")
    shutil.copyfile(candidate / "pi_type.rs", out / "candidate.rs")
    receipt = {"AuthorityEffect": "None", "scope": "Separate finite Pi candidate in the actual HoTT package source, with standalone workspace/profile declarations. Not installed-source or whole-root evidence.",
        "source_manifest_sha256": digest(out / "source_manifest.json"), "candidate_sha256": digest(out / "candidate.rs"),
        "runner_sha256": digest(out / "trial.py"), "helper_sha256": digest(out / "replay.py"),
        "versions": {name: subprocess.check_output([name, "--version"], text=True).strip() for name in ("rustc", "cargo")},
        "baselines": [], "restored_baselines": [], "admissions": []}
    print(out, flush=True)
    dependencies = None
    def run(name, mode):
        warm = (work / "target/debug/deps").is_dir()
        minimum = (256 * 1024**2) if warm else 1024**3
        free = shutil.disk_usage(ROOT).free
        receipt["admissions"].append({"warm_cache": warm, "free_bytes": free, "required_free_bytes": minimum, "admitted": free >= minimum})
        if free < minimum:
            return dict(started=False, exit_code=None, timed_out=False, reason="Small-package disk reserve unavailable")
        selection = ["--lib", "pi_type"] if mode == "unit" else ["--doc"] if mode == "doc" else []
        return execute(["cargo", "test", "--offline", "--quiet", *selection], work, out / (name + ".log"))
    try:
        for path in (RUST / "src/homotopy_type_theory").rglob("*"):
            if path.is_file() and (path.suffix == ".rs" or path.name == "Cargo.toml"):
                target = work / path.relative_to(RUST / "src/homotopy_type_theory")
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(path, target)
        with (work / "Cargo.toml").open("a", encoding="utf8") as stream:
            stream.write("\n[workspace]\n[profile.dev]\ndebug=0\n[profile.test]\ndebug=0\n")
        (work / "pi_type.rs").write_bytes(original)
        meta = subprocess.run(["cargo", "metadata", "--offline", "--quiet", "--format-version", "1"], cwd=work, capture_output=True, text=True)
        (out / "cargo_metadata.json").write_text(meta.stdout, encoding="utf8")
        (out / "metadata_stderr.log").write_text(meta.stderr, encoding="utf8")
        receipt["metadata"] = {"command": meta.args, "cwd": str(work), "exit_code": meta.returncode,
            "sha256": digest(out / "cargo_metadata.json"), "stderr_sha256": digest(out / "metadata_stderr.log")}
        if meta.returncode != 0:
            return
        dependencies = dependency_sources(json.loads(meta.stdout))
        write(out / "dependency_sources.json", dependencies)
        receipt["dependency_sources_sha256"] = digest(out / "dependency_sources.json")
        baseline = run("baseline", "all")
        receipt["baselines"].append(baseline)
        print("baseline", baseline["exit_code"], flush=True)
        if baseline["exit_code"] != 0:
            return
        path = work / "pi_type.rs"
        for entry in entries:
            try:
                path.write_bytes(original.decode("utf8").replace(entry["before"], entry["after"], 1).encode("utf8"))
                entry["candidate_sha256"] = digest(path)
                entry["run"] = run(entry["id"], entry["mode"])
                if entry["run"].get("started") is False:
                    entry["reason"] = entry["run"]["reason"]
                    break
                entry["outcome"], entry["reason"] = classify(entry["run"], out)
                print(entry["id"], entry["outcome"], flush=True)
            finally:
                path.write_bytes(original)
                entry["source_restored"] = digest(path) == receipt["candidate_sha256"]
                write(out / "mutations.json", entries)
        receipt["restored_baselines"].append(run("restored", "all"))
    finally:
        receipt["live_sources_unchanged"] = sources == inventory()
        receipt["candidate_unchanged"] = digest(candidate / "pi_type.rs") == receipt["candidate_sha256"]
        receipt["dependencies_unchanged"] = dependencies is not None and all(Path(name).is_file() and digest(Path(name)) == pin for name, pin in dependencies.items())
        counts = Counter(entry["outcome"] for entry in entries)
        for outcome in ("killed", "survived", "demonstrably_equivalent", "invalid", "inconclusive", "unrun"):
            counts.setdefault(outcome, 0)
        denominator = sum(counts[name] for name in ("killed", "survived", "inconclusive", "unrun"))
        receipt["accounting"] = {**counts, "conservative_ratio": counts["killed"] / denominator if denominator else None}
        write(out / "mutations.json", entries)
        receipt["mutations_sha256"] = digest(out / "mutations.json")
        if (work / "Cargo.lock").is_file():
            shutil.copyfile(work / "Cargo.lock", out / "Cargo.lock")
        remove_owned(work / "target", work)
        receipt["owned_build_removed"] = True
        write(out / "receipt.json", receipt)


if __name__ == "__main__":
    main()
