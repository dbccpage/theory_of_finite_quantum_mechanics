"""Exact-item executable witness for publicly constructible inertia overflow.

AuthorityEffect: None. No whole-package compilation is claimed.
"""
from datetime import datetime, timezone
from pathlib import Path
import shutil
import subprocess
from native_scalar_probe import item
from replay import ROOT, RUST, digest, inventory, write, execute, remove_owned


def main():
    subject = RUST / "src/linear_algebra/ordered.rs"
    source = subject.read_bytes().decode("utf8")
    headers = ["pub struct Inertia {", "impl Inertia {"]
    excerpts = [item(source, header) for header in headers]
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-inertia-control"
    out = ROOT / "evidence/quality/l4a_six" / stamp
    out.mkdir()
    work = RUST / "target/l4a-six" / stamp
    build = work / "build"
    build.mkdir(parents=True)
    harness = "\n\n".join(excerpts) + r'''
fn main() {
    let rank = std::panic::catch_unwind(|| Inertia { positive: usize::MAX, negative: 1, zero: 0 }.rank());
    let dimension = std::panic::catch_unwind(|| Inertia { positive: usize::MAX, negative: 0, zero: 1 }.dimension());
    assert!(rank.is_err(), "public rank overflow did not reproduce");
    assert!(dimension.is_err(), "public dimension overflow did not reproduce");
    println!("DEFECT_CONFIRMED:public_inertia_rank_and_dimension_overflow");
}
'''
    (out / "inertia_items.rs").write_bytes(harness.encode("utf8"))
    shutil.copyfile(__file__, out / "probe.py")
    shutil.copyfile(Path(__file__).with_name("replay.py"), out / "replay.py")
    sources = inventory()
    write(out / "source_manifest.json", sources)
    dependencies = {str(subject): digest(subject)}
    write(out / "dependency_sources.json", dependencies)
    write(out / "extraction.json", {"AuthorityEffect": "None", "headers": headers,
        "source_sha256": digest(subject), "scope": "Unconditional primitive-only struct and impl copied byte-for-byte. Public fields admit these exact inputs. Does not compile the whole crate."})
    receipt = {"AuthorityEffect": "None", "evaluation_timestamp": datetime.now(timezone.utc).isoformat(),
        "claim": "Source-grounded public inertia count-overflow counterexamples; exact item excerpts only.",
        "versions": {name: subprocess.check_output([name, "--version"], text=True).strip() for name in ("rustc", "cargo")},
        "source_manifest_sha256": digest(out / "source_manifest.json"),
        "dependency_sources_sha256": digest(out / "dependency_sources.json"),
        "runner_sha256": digest(out / "probe.py"), "helper_sha256": digest(out / "replay.py"),
        "excerpt_sha256": digest(out / "inertia_items.rs"), "extraction_sha256": digest(out / "extraction.json")}
    print(out, flush=True)
    try:
        compiled = execute(["rustc", "--edition", "2021", "-C", "overflow-checks=on",
            str(out / "inertia_items.rs"), "-o", str(build / "witness.exe")], work, out / "compile.log", timeout=90)
        receipt["compilation"] = compiled
        if compiled["exit_code"] != 0:
            return
        run = execute([str(build / "witness.exe")], work, out / "witness.log", timeout=90)
        receipt["run"] = run
        reproduced = run["exit_code"] == 0 and "DEFECT_CONFIRMED:" in (out / "witness.log").read_text(encoding="utf8")
        findings = [{"id": "public_inertia_count_overflow", "source": "code/rust/src/linear_algebra/ordered.rs",
            "gate": "G3", "affected_gates": ["G2", "G3"], "grade": "E", "reproduced": reproduced,
            "observation_kind": "source-grounded-native-overflow",
            "witness": "Public Inertia fields accept positive=usize::MAX with negative=1 or zero=1. Exact unchanged rank/dimension item bodies panic under explicit overflow checks. These are reachable public inputs, distinct from valid internally produced inertia counts. This excerpt execution is not a whole-root compilation."}]
        write(out / "findings.json", findings)
        receipt["findings_sha256"] = digest(out / "findings.json")
        print("public inertia overflow reproduced", reproduced, flush=True)
    finally:
        receipt["sources_unchanged"] = sources == inventory()
        receipt["dependency_sources_unchanged"] = all(digest(Path(p)) == h for p, h in dependencies.items())
        remove_owned(build, work)
        receipt["owned_build_removed"] = True
        write(out / "receipt.json", receipt)


if __name__ == "__main__":
    main()
