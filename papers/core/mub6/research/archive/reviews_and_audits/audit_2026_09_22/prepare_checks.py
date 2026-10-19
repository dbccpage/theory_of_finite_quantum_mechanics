"""Prepare fresh Lean dependency scans and a standalone Rust probe in ignored scratch."""
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "scratch/audit_2026_09_22"
OUT.mkdir(parents=True, exist_ok=True)
groups = {
    "gluing": [ROOT / "lean4/gluing" / f"{name}.lean" for name in (
        "TargetA10GlobalCover", "TargetA11OrbitExhaustiveness", "TargetA12SmaleSentry",
        "TargetA13GrandSynthesis", "TargetB1ContinuousChaining", "TargetB2GlobalGluing",
        "TargetB3ManifoldIntegration")],
    "mathlib": [ROOT / "lean4/012_mutually_unbiased_bases/MUB" / f"{name}.lean" for name in (
        "ConcreteSemantics", "PolynomialEncoding", "CaseCoverage", "GroebnerBranch",
        "CADBranch", "CertificatePilot", "MasterClassification")],
}
for group, files in groups.items():
    imports = [f"import {'MUB.' if group == 'mathlib' else ''}{p.stem}" for p in files]
    declarations = []
    for p in files:
        namespace = []
        for line in p.read_text(encoding="utf-8").splitlines():
            m = re.match(r"namespace\s+(\S+)", line)
            if m:
                namespace.append(m.group(1))
            if line.startswith("end ") and namespace:
                namespace.pop()
            m = re.match(r"(?:private )?(?:noncomputable )?(?:theorem|lemma)\s+(\w+)", line)
            if m and not line.startswith("private "):
                declarations.append(".".join(namespace + [m.group(1)]))
    (OUT / f"{group}_axioms.lean").write_text("\n".join(imports +
        [f"#print axioms {name}" for name in declarations]) + "\n", encoding="utf-8")
    print(f"{group}: {len(declarations)} declaration dependency queries")

crate = OUT / "rust_probe"
(crate / "src").mkdir(parents=True, exist_ok=True)
(crate / "Cargo.toml").write_text('''[package]
name = "mub6_audit_probes_20260922"
version = "0.0.0"
edition = "2021"
[workspace]
[dependencies]
omega_mub = { path = "../../../omega_engine/crates_rs/omega_mub" }
num-bigint = { version = "0.4", features = ["serde"] }
num-rational = { version = "0.4", features = ["serde"] }
num-traits = "0.2"
serde = { version = "1", features = ["derive"] }
thiserror = "2"
[[bin]]
name = "baseline"
path = "src/main.rs"
[[bin]]
name = "patched"
path = "src/patched.rs"
''', encoding="utf-8")
shutil.copyfile(Path(__file__).with_name("rust_probes.rs"), crate / "src/main.rs")
shutil.copyfile(Path(__file__).with_name("patched_rust_checks.rs"), crate / "src/patched.rs")
print("Prepared Rust probe; generated files remain under scratch.")

patched_pilot = OUT / "patched/lean4/012_mutually_unbiased_bases/MUB/CertificatePilot.lean"
if patched_pilot.exists():
    extra = '''
open MUB.CertificatePilot
#eval checkCertificate { validPilotCertificate with
  branch_hypotheses := "not_registered", var_names := [],
  source_hash := hashSources [.const 1], sources := [.const 1], multipliers := [.const 1] }
#eval checkCertificate { validPilotCertificate with
  source_hash := hashSources [.const 1], sources := [.const 1], multipliers := [.const 1] }
'''
    (OUT / "proposed_pilot_probes.lean").write_text(patched_pilot.read_text(encoding="utf-8") + extra, encoding="utf-8")
