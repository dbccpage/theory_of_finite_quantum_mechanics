"""Designated semantic challenges in an owned source snapshot; all outcomes retained.

AuthorityEffect: None. Does not certify unchallenged symbols or failure classes.
"""

import argparse
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil

from replay import (ROOT, RUST, digest, write, inventory, snapshot, execute,
                    remove_owned, dependency_sources)
import subprocess


def candidates():
    lie = "lie_theory/lib.rs"
    lggr = "local_green_global_red_lggr/lggr_v.rs"
    holo = "holonomy/connection.rs"
    matrix = "holonomy/matrix.rs"
    # Each literal recipe is deliberately source-specific. No blind substitutions.
    recipes = [
        ("SL01-denominator-domain", lie, "if *a11.denom() == 0 || *a22.denom() == 0 {", "if false {"),
        ("SL02-sign", lie, "left == -right", "left == right"),
        ("SL03-old-overflow", lie, "    left == -right", "    num_traits::Zero::is_zero(&(a11 + a22))"),
        ("SL04-widening", lie, "i128::from(*a11.numer()) * i128::from(*a22.denom())", "i128::from(a11.numer().wrapping_mul(*a22.denom()))"),
        ("LG01-inclusive-budget", lggr, "if cells > MAX_LGGR_CELLS {", "if cells >= MAX_LGGR_CELLS {"),
        ("LG02-product-preflight", lggr, "    admit_cell_count(cells(q.rows(), d.cols())?)?;", ""),
        ("LG03-matrix-domain", lggr, '    admit_coefficients("D", d.as_slice())?;', ""),
        ("LG04-witness-domain", lggr, '    admit_coefficients("witness", witness)?;', ""),
        ("LG05-soundness-rank", lggr, "if qd_rank == d_rank {", "if qd_rank <= d_rank {"),
        ("LG06-witness-nonzero", lggr, "if !dv_nonzero {", "if false {"),
        ("HO01-missing-source", holo, "id: edge.source.clone(),", 'id: "wrong-source".into(),'),
        ("HO02-missing-target", holo, "id: edge.target.clone(),", 'id: "wrong-target".into(),'),
        ("SC01-zero-denominator", "linear_algebra/scalars.rs", "if d == 0 {", "if false {"),
        ("MX01-constructor-scalar", matrix, "        data.iter().try_for_each(ExactScalar::validate_exact)?;", ""),
        ("MX02-setter-scalar", matrix, "        value.validate_exact()?;\n        self.data[index] = value;", "        self.data[index] = value;"),
        ("MX03-decoder-admission", matrix, "Self::try_new(wire.rows, wire.cols, wire.data).map_err(serde::de::Error::custom)", "Ok(Self { rows: wire.rows, cols: wire.cols, data: wire.data })"),
        ("MX04-index-boundary", matrix, "if row >= self.rows || col >= self.cols {", "if row > self.rows || col > self.cols {"),
        ("MX05-inclusive-cells", matrix, "if requested > limits.max_cells {", "if requested >= limits.max_cells {"),
        ("MX06-inclusive-work", matrix, "if requested > limits.max_operations {", "if requested >= limits.max_operations {"),
        ("MX07-product-index", matrix, "other.at(k, c)", "other.at(c, k)"),
        ("MX08-determinant-sign", matrix, "                determinant = -determinant;", ""),
        ("MX09-rank-increment", matrix, "            rank += 1;", ""),
        ("MX10-inverse-block", matrix, "if index % self.cols >= n {", "if index % self.cols < n {"),
        ("MX11-complex-product", matrix, "im: add_ref(&mul_ref(&a.re, &b.im), &mul_ref(&a.im, &b.re)),", "im: sub_ref(&mul_ref(&a.re, &b.im), &mul_ref(&a.im, &b.re)),"),
        ("MX12-complex-zero-inverse", matrix, "if n_sq.is_zero() {\n            return Err(HolonomyError::ZeroDivision);", "if n_sq.is_zero() {\n            return Ok(Self::zero());"),
        ("MX13-rational-zero-inverse", matrix, "if self.is_zero() {\n            Err(HolonomyError::ZeroDivision)", "if self.is_zero() {\n            Ok(Self::zero())"),
        ("MX14-storage-privacy", matrix, "    rows: usize,\n    cols: usize,\n    data: Vec<T>,\n}\n\nimpl<T: ExactScalar>", "    pub rows: usize,\n    pub cols: usize,\n    pub data: Vec<T>,\n}\n\nimpl<T: ExactScalar>"),
        ("MX15-domain-seal", matrix, "mod sealed {", "pub mod sealed {"),
        ("MX16-borrow-privacy", matrix, "    value: &'a T,", "    pub value: &'a T,"),
        ("MX17-borrow-admission", matrix, "        value.validate_exact()?;\n        Ok(Self { value })", "        Ok(Self { value })"),
        ("MX18-input-admission", matrix, "        admit_cells(self.rows, self.cols, limits)?;\n        admit_cells(other.rows, other.cols, limits)?;", ""),
    ]
    for filename, field in (("empty_type", "id"), ("unit_type", "unit_term_ref"),
                            ("sum_type", "left_type_ref"), ("pi_type", "family_ref"),
                            ("sigma_type", "base_type_ref")):
        recipes.append(("HT-" + filename, "homotopy_type_theory/" + filename + ".rs",
                        f"if self.{field}.is_empty() {{", "if false {"))
    result = []
    for identity, source, before, after in recipes:
        package = {"lie_theory": "tfqm_lie_theory", "holonomy": "tfqm_holonomy",
                   "homotopy_type_theory": "tfqm_homotopy_type_theory",
                   "linear_algebra": "tfqm_homology_linear_audit",
                   "local_green_global_red_lggr": "tfqm_local_green_global_red_lggr"}[source.split("/")[0]]
        result.append({"id": identity, "source": "code/rust/src/" + source,
                       "snapshot_source": "src/" + source, "before": before, "after": after,
                       "package": package, "outcome": "unrun"})
    return result


def classify(run, output):
    if run["timed_out"]:
        return "inconclusive", "Cargo deadline expired; no kill is inferred."
    if run["exit_code"] == 0:
        return "survived", "Selected suite passed."
    log = (ROOT / run["log"]).read_text(encoding="utf-8")
    if "could not compile" in log or "error[E" in log:
        return "invalid", "Compiler rejected candidate; excluded from eligible denominator."
    if "test result: FAILED" in log:
        return "killed", "Rust test harness reported an assertion/test failure."
    return "inconclusive", "Unsuccessful process without decisive compiler or assertion attribution."


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prefix")
    args = parser.parse_args()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output = ROOT / "evidence/quality/l4a_six" / (stamp + "-mutations")
    output.mkdir(parents=True)
    work = RUST / "target/l4a-six" / (stamp + "-mutations")
    sources = inventory()
    write(output / "source_manifest.json", sources)
    shutil.copyfile(__file__, output / "mutations.py")
    shutil.copyfile(Path(__file__).with_name("replay.py"), output / "replay.py")
    entries = [c for c in candidates() if not args.prefix or c["id"].startswith(args.prefix)]
    write(output / "mutations.json", entries)
    receipt = {"AuthorityEffect": "None", "evaluation_timestamp": datetime.now(timezone.utc).isoformat(),
               "versions": {n: subprocess.check_output([n, "--version"], text=True).strip() for n in ("cargo", "rustc")},
               "source_manifest_sha256": digest(output / "source_manifest.json"),
               "runner_sha256": digest(output / "mutations.py"),
               "execution_helper_sha256": digest(output / "replay.py"),
               "baselines": [], "restored_baselines": [],
               "build_cache_disposals": [],
               "scope": "Designated semantic faults only; no whole-file or system score is inferred."}
    print(output, flush=True)
    try:
        snapshot(work)
        command = ["cargo", "metadata", "--offline", "--quiet", "--format-version", "1"]
        meta = subprocess.run(command, cwd=work, text=True, capture_output=True)
        (output / "cargo_metadata.json").write_text(meta.stdout, encoding="utf-8")
        (output / "cargo_metadata_stderr.log").write_text(meta.stderr, encoding="utf-8")
        receipt["metadata_capture"] = {"command": command, "cwd": str(work), "exit_code": meta.returncode,
                                       "sha256": digest(output / "cargo_metadata.json"),
                                       "stderr_sha256": digest(output / "cargo_metadata_stderr.log")}
        if meta.returncode != 0:
            return
        dependencies = dependency_sources(json.loads(meta.stdout))
        write(output / "dependency_sources.json", dependencies)
        receipt["dependency_sources_sha256"] = digest(output / "dependency_sources.json")
        packages = sorted({c["package"] for c in entries})
        common = ["--offline", "--target-dir", str(work / "build"), "--quiet"]

        def run_package(package, log):
            if shutil.disk_usage(ROOT).free < 3 * 1024**3:
                remove_owned(work / "build", work)
                receipt["build_cache_disposals"].append({"before_log": log.name,
                    "reason": "Completed Cargo cache removed to recover 3 GiB headroom."})
            if shutil.disk_usage(ROOT).free < 3 * 1024**3:
                return {"started": False, "exit_code": None, "reason": "Less than 3 GiB free"}
            # Holonomy includes compile-fail API boundary controls. Cargo's
            # default test target also executes doctests; --tests excludes them.
            targets = [] if package == "tfqm_holonomy" else ["--tests"]
            return execute(["cargo", "test", *common, "-p", package, *targets], work, log)

        eligible_packages = set()
        for package in packages:
            baseline = run_package(package, output / (package + "-baseline.log"))
            receipt["baselines"].append({"package": package, **baseline})
            if baseline["exit_code"] == 0:
                eligible_packages.add(package)
            print("baseline", package, baseline["exit_code"], flush=True)
        for entry in entries:
            if entry["package"] not in eligible_packages:
                entry["reason"] = "Baseline unavailable or unsuccessful."
                continue
            path = work / entry["snapshot_source"]
            original = path.read_bytes()
            try:
                source = original.decode("utf-8")
                if source.count(entry["before"]) != 1:
                    entry.update(outcome="invalid", reason="Recipe must match exactly one source site.")
                    continue
                path.write_bytes(source.replace(entry["before"], entry["after"], 1).encode("utf-8"))
                entry["candidate_sha256"] = digest(path)
                run = run_package(entry["package"], output / (entry["id"] + ".log"))
                entry["run"] = run
                if run.get("started") is False:
                    entry.update(outcome="unrun", reason=run["reason"])
                else:
                    outcome, reason = classify(run, output)
                    entry.update(outcome=outcome, reason=reason)
                print(entry["id"], entry["outcome"], flush=True)
            finally:
                path.write_bytes(original)
                entry["source_restored"] = digest(path) == sources[entry["source"]]
                write(output / "mutations.json", entries)
        for package in packages:
            receipt["restored_baselines"].append({"package": package,
                **run_package(package, output / (package + "-restored.log"))})
        receipt["dependency_sources_unchanged"] = all(Path(p).is_file() and digest(Path(p)) == h
                                                      for p, h in dependencies.items())
        shutil.copyfile(work / "Cargo.lock", output / "Cargo.lock")
        shutil.copyfile(work / "Cargo.toml", output / "snapshot.Cargo.toml")
    finally:
        counts = Counter(e["outcome"] for e in entries)
        for outcome in ("killed", "survived", "demonstrably_equivalent", "invalid", "inconclusive", "unrun"):
            counts.setdefault(outcome, 0)
        denominator = sum(counts[k] for k in ("killed", "survived", "inconclusive", "unrun"))
        receipt["accounting"] = {**counts, "conservative_ratio": counts["killed"] / denominator if denominator else None}
        receipt["sources_unchanged"] = sources == inventory()
        write(output / "mutations.json", entries)
        receipt["mutations_sha256"] = digest(output / "mutations.json")
        remove_owned(work / "build", work)
        receipt["owned_build_removed"] = True
        write(output / "receipt.json", receipt)
        print(receipt["accounting"], flush=True)


if __name__ == "__main__":
    main()
