"""Apply the existing calibrated Syn metric tool to all six goal directories."""
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "category_homology"))
import run_audit

MODULES = ("combinatorics", "category_theory", "finite_probability",
           "fusion_categories", "general_relativity", "higher_category_theory")


def inventory():
    paths = [run_audit.ROOT / "SCORING.md"]
    for module in MODULES:
        folder = run_audit.RUST / "src" / module
        paths.extend(folder.rglob("*.rs"))
        paths.append(folder / "Cargo.toml")
    macro_view = HERE / "fusion_scalar_macro_view.rs"
    if macro_view.exists():
        paths.append(macro_view)
    return {p.relative_to(run_audit.ROOT).as_posix(): run_audit.digest(p) for p in sorted(paths)}


if __name__ == "__main__":
    canonical = HERE.parent / "category_homology/run_metrics.py"
    specification = importlib.util.spec_from_file_location("canonical_metrics", canonical)
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    # Reuse its unmodified calibrated tool/build disposal, explicitly narrowing
    # input custody to Rust, manifests and rubric, rather than generated sidecars.
    module.inventory = inventory
    evidence = run_audit.ROOT / "evidence/quality/category_homology"
    before = set(evidence.glob("*-metrics"))
    module.main()
    created = set(evidence.glob("*-metrics")) - before
    matching = [p for p in created if json.loads((p / "source_manifest.json").read_text()) == inventory()]
    if len(matching) != 1:
        raise ValueError("Unable to identify this wrapper's exact metric run")
    run_audit.write_json(matching[0] / "six_module_scope.json", {
        "AuthorityEffect": "None", "modules": list(MODULES),
        "wrapper": str(Path(__file__).relative_to(run_audit.ROOT)), "wrapper_sha256": run_audit.digest(Path(__file__)),
        "canonical_runner": str(canonical.relative_to(run_audit.ROOT)), "canonical_runner_sha256": run_audit.digest(canonical),
        "scope": "The existing unmodified Syn parser and calibration, with an explicit six-directory Rust/manifest/rubric inventory; no sidecar status or runtime semantics measured."})
