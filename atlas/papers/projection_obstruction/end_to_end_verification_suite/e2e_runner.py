#!/usr/bin/env python3
"""Standalone Command-Line Runner for Comprehensive E2E Verification Suite.

Validates Acceptance Criteria AC1 through AC6 across the 9-package estate.
AuthorityEffect: None.

Usage:
    python e2e_runner.py                      # Run all acceptance criteria
    python e2e_runner.py --ac 1,2,3           # Run specific acceptance criteria
    python e2e_runner.py --fast               # Run rapid structural checks
    python e2e_runner.py --json-report report.json  # Output JSON summary
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path

# Add parent directory to path so relative imports work when executed directly
SUITE_ROOT = Path(__file__).resolve().parent
ESTATE_ROOT = SUITE_ROOT.parent
sys.path.insert(0, str(SUITE_ROOT.parent))

from end_to_end_verification_suite.checks.anchor_checker import check_proof_anchors
from end_to_end_verification_suite.checks.bibliography_checker import check_bibliography
from end_to_end_verification_suite.checks.claim_hygiene_auditor import audit_all_packages_claim_hygiene
from end_to_end_verification_suite.checks.manifest_checker import check_manifest
from end_to_end_verification_suite.checks.r1_r10_checker import audit_all_r1_r10
from end_to_end_verification_suite.config import (
    ALL_PACKAGES,
    PO000_DIR,
    SIBLING_PACKAGES,
)


@dataclass
class ACResult:
    ac_id: str
    name: str
    status: str  # "PASS", "FAIL", "SKIP"
    duration_seconds: float
    details: str
    failures: list[str] = field(default_factory=list)


@dataclass
class E2ERunReport:
    timestamp: str
    estate_root: str
    total_criteria: int
    passed_criteria: int
    failed_criteria: int
    skipped_criteria: int
    total_duration_seconds: float
    overall_verdict: str  # "PASS" or "FAIL"
    results: list[ACResult] = field(default_factory=list)


class E2ERunner:
    def __init__(self, verbose: bool = False, fast_mode: bool = False):
        self.verbose = verbose
        self.fast_mode = fast_mode

    def log(self, message: str) -> None:
        print(f"[E2E] {message}")

    def log_verbose(self, message: str) -> None:
        if self.verbose:
            print(f"  [DEBUG] {message}")

    def run_ac1(self) -> ACResult:
        """AC1: Pytest passes with 0 failures and preserves manifest isolation."""
        self.log("Running AC1: Pytest execution & manifest isolation...")
        start_time = time.time()
        failures: list[str] = []

        manifest_sha256 = PO000_DIR / "MANIFEST.sha256"
        sha256sums = PO000_DIR / "SHA256SUMS"

        hash_m_before = manifest_sha256.read_bytes() if manifest_sha256.is_file() else b""
        hash_s_before = sha256sums.read_bytes() if sha256sums.is_file() else b""

        if self.fast_mode:
            # In fast mode, run single fast test to check isolation
            cmd = [sys.executable, "-m", "pytest", "code/tests/test_paper_artifacts.py", "-q"]
        else:
            cmd = [
                sys.executable,
                "-m",
                "pytest",
                "code/tests",
                "-m",
                "not native_integration",
                "-q",
                "--disable-warnings",
                "--tb=short",
            ]

        proc = subprocess.run(cmd, cwd=PO000_DIR, capture_output=True, text=True, timeout=300)

        hash_m_after = manifest_sha256.read_bytes() if manifest_sha256.is_file() else b""
        hash_s_after = sha256sums.read_bytes() if sha256sums.is_file() else b""

        if hash_m_before != hash_m_after:
            failures.append("Running pytest modified MANIFEST.sha256 in the live package root")
        if hash_s_before != hash_s_after:
            failures.append("Running pytest modified SHA256SUMS in the live package root")
        if proc.returncode != 0:
            failures.append(f"Pytest exited with return code {proc.returncode}:\n{proc.stdout[-500:]}\n{proc.stderr[-500:]}")

        duration = time.time() - start_time
        status = "FAIL" if failures else "PASS"
        details = "Pytest completed and live manifests remained byte-identical" if not failures else "Failures detected"
        return ACResult("AC1", "Pytest Suite & Manifest Isolation", status, duration, details, failures)

    def run_ac2(self) -> ACResult:
        """AC2: Proof anchors, bibliography completeness, and R1–R10 regressions."""
        self.log("Running AC2: Proof anchors, bibliography, and R1–R10 regression guards...")
        start_time = time.time()
        failures: list[str] = []

        # (a) Check proof anchors
        anchor_res = check_proof_anchors(PO000_DIR)
        if anchor_res.errors:
            failures.extend(anchor_res.errors)
        if anchor_res.unresolved_count > 0:
            failures.append(
                f"{anchor_res.unresolved_count} unresolved proof anchors (e.g. {[a['anchor'] for a in anchor_res.unresolved_anchors[:5]]})"
            )

        # (b) Check bibliography
        bib_res = check_bibliography(PO000_DIR)
        if bib_res.errors:
            failures.extend(bib_res.errors)
        if bib_res.orphan_references:
            failures.append(f"Orphan references in References section not cited in body: {bib_res.orphan_references}")
        if bib_res.missing_definitions:
            failures.append(f"Citations in body missing from References section: {bib_res.missing_definitions}")
        if not bib_res.ref36_valid:
            failures.append("Reference [36] historical URL pin invalid")
        if not bib_res.duhamel_priors_cited:
            failures.append("Duhamel prior literature (Martinazzo–Burghardt / Zoufal–Sutter–Woerner) not cited")

        # (c) R1–R10 checks
        r_res = audit_all_r1_r10(PO000_DIR)
        for r in r_res.reports.values():
            if not r.passed:
                failures.append(f"[{r.req_id}] {r.title}: {', '.join(r.violations)}")

        duration = time.time() - start_time
        status = "FAIL" if failures else "PASS"
        details = (
            f"Verified {anchor_res.resolved_count} anchors, {bib_res.total_references} references, and R1–R10 guards"
            if not failures
            else "Failures detected"
        )
        return ACResult("AC2", "Anchors, Bibliography, & Regression Guards", status, duration, details, failures)

    def run_ac3(self) -> ACResult:
        """AC3: Replay mechanization & certificate verification."""
        self.log("Running AC3: Replay mechanization & certificate verification...")
        start_time = time.time()
        failures: list[str] = []

        import tempfile

        with tempfile.TemporaryDirectory() as tmp_dir:
            cert_file = Path(tmp_dir) / "replay_cert.json"

            # 1. replay.py
            cmd_replay = [sys.executable, "code/replay.py", "--output", str(cert_file)]
            proc_r = subprocess.run(cmd_replay, cwd=PO000_DIR, capture_output=True, text=True, timeout=180)
            if proc_r.returncode != 0:
                failures.append(f"replay.py failed with code {proc_r.returncode}:\n{proc_r.stderr[:500]}")

            if not cert_file.is_file():
                failures.append("replay.py did not produce expected certificate file")
            else:
                # 2. verify_certificate.py
                cmd_verify = [sys.executable, "code/verify_certificate.py", str(cert_file)]
                proc_v = subprocess.run(cmd_verify, cwd=PO000_DIR, capture_output=True, text=True, timeout=60)
                if proc_v.returncode != 0:
                    failures.append(f"verify_certificate.py failed with code {proc_v.returncode}:\n{proc_v.stdout[:500]}")
                try:
                    out_json = json.loads(proc_v.stdout.strip())
                    if out_json.get("verdict") != "pass":
                        failures.append(f"Certificate verifier verdict was {out_json.get('verdict')}")
                    if out_json.get("errors"):
                        failures.append(f"Certificate verifier errors: {out_json.get('errors')}")
                except Exception as e:
                    failures.append(f"Failed parsing verify_certificate.py stdout as JSON: {e}")

        duration = time.time() - start_time
        status = "FAIL" if failures else "PASS"
        details = "Mechanization replay and independent certificate verifier passed" if not failures else "Failures detected"
        return ACResult("AC3", "Replay & Certificate Verification", status, duration, details, failures)

    def run_ac4(self) -> ACResult:
        """AC4: Rebuild artifacts and verify_deposit.py."""
        self.log("Running AC4: Rebuilt artifacts & PO-000 deposit verification...")
        start_time = time.time()
        failures: list[str] = []

        # 1. Check rebuilt files
        required = ["projection_obstruction.tex", "projection_obstruction.pdf", "MANIFEST.sha256", "SHA256SUMS"]
        for name in required:
            p = PO000_DIR / name
            if not p.is_file():
                failures.append(f"Required artifact {name} is missing from PO-000")

        # 2. Check release archive in dist
        dist_archives = list((PO000_DIR / "dist").glob("*.zip"))
        if not dist_archives:
            failures.append("No release archive found in dist/")

        # 3. Direct manifest check
        m_sums = check_manifest(PO000_DIR, "SHA256SUMS")
        if not m_sums.passed:
            failures.append(f"PO-000 SHA256SUMS check failed: {len(m_sums.mismatches)} mismatches, {len(m_sums.missing_files)} missing")

        # 4. verify_deposit.py --integrity-only
        proc_int = subprocess.run(
            [sys.executable, "verify_deposit.py", "--integrity-only"],
            cwd=PO000_DIR,
            capture_output=True,
            text=True,
            timeout=60,
        )
        if proc_int.returncode != 0:
            failures.append(f"verify_deposit.py --integrity-only failed (code {proc_int.returncode}):\n{proc_int.stdout[:400]}")

        # 5. verify_deposit.py full (if not in fast mode)
        if not self.fast_mode:
            proc_full = subprocess.run(
                [sys.executable, "verify_deposit.py"],
                cwd=PO000_DIR,
                capture_output=True,
                text=True,
                timeout=300,
            )
            if proc_full.returncode != 0:
                failures.append(f"verify_deposit.py full failed (code {proc_full.returncode}):\n{proc_full.stdout[:400]}")

        duration = time.time() - start_time
        status = "FAIL" if failures else "PASS"
        details = "All rebuild artifacts verified and verify_deposit passed cleanly" if not failures else "Failures detected"
        return ACResult("AC4", "PO-000 Rebuild & Deposit Verification", status, duration, details, failures)

    def run_ac5(self) -> ACResult:
        """AC5: All 8 sibling packages pass test suites and deposit gates."""
        self.log("Running AC5: Sibling packages test suites & deposit gates...")
        start_time = time.time()
        failures: list[str] = []

        for pkg_id, spec in sorted(SIBLING_PACKAGES.items()):
            self.log_verbose(f"Verifying sibling {spec.name} ({pkg_id})...")

            # Fast manifest check
            man_res = check_manifest(spec.path, "SHA256SUMS")
            if not man_res.passed:
                failures.append(f"Sibling {pkg_id} manifest failed: {len(man_res.mismatches)} mismatches")

            if not self.fast_mode:
                # Run pytest
                p_test = subprocess.run(spec.pytest_command, cwd=spec.path, capture_output=True, text=True, timeout=180)
                if p_test.returncode != 0:
                    failures.append(f"Sibling {pkg_id} pytest suite failed with code {p_test.returncode}")

                # Run deposit verifier
                p_dep = subprocess.run(spec.deposit_verifier_command, cwd=spec.path, capture_output=True, text=True, timeout=240)
                if p_dep.returncode != 0:
                    failures.append(f"Sibling {pkg_id} deposit verifier failed with code {p_dep.returncode}")

        duration = time.time() - start_time
        status = "FAIL" if failures else "PASS"
        details = "All 8 sibling packages passed test suites and deposit verification gates" if not failures else "Failures detected"
        return ACResult("AC5", "Sibling Packages Qualification", status, duration, details, failures)

    def run_ac6(self) -> ACResult:
        """AC6: Point-by-point audit of R1–R10 under Claim Hygiene."""
        self.log("Running AC6: Point-by-point R1–R10 audit & Claim Hygiene across all 9 packages...")
        start_time = time.time()
        failures: list[str] = []

        # Claim hygiene audit
        hygiene = audit_all_packages_claim_hygiene(ALL_PACKAGES)
        if not hygiene.passed:
            failures.append(f"Claim Hygiene audit found {hygiene.violations_count} forbidden/unqualified claims")

        # R1-R10 audit
        r1_r10 = audit_all_r1_r10(PO000_DIR)
        for r in r1_r10.reports.values():
            if not r.passed:
                failures.append(f"[{r.req_id}] {r.title}: {', '.join(r.violations)}")

        duration = time.time() - start_time
        status = "FAIL" if failures else "PASS"
        details = f"Scanned {hygiene.total_files_scanned} files across 9 packages under strict Claim Hygiene" if not failures else "Failures detected"
        return ACResult("AC6", "R1–R10 Audit & Estate Claim Hygiene", status, duration, details, failures)

    def run(self, ac_list: list[str] | None = None) -> E2ERunReport:
        start_all = time.time()
        active_acs = ac_list if ac_list else ["1", "2", "3", "4", "5", "6"]

        results: list[ACResult] = []
        ac_runners = {
            "1": self.run_ac1,
            "2": self.run_ac2,
            "3": self.run_ac3,
            "4": self.run_ac4,
            "5": self.run_ac5,
            "6": self.run_ac6,
        }

        for ac_num in ["1", "2", "3", "4", "5", "6"]:
            if ac_num in active_acs:
                runner = ac_runners[ac_num]
                res = runner()
                results.append(res)
                self.log(f"[{res.status}] {res.ac_id}: {res.name} ({res.duration_seconds:.2f}s)")
                if res.failures and self.verbose:
                    for f in res.failures:
                        print(f"      * {f}")
            else:
                results.append(ACResult(f"AC{ac_num}", f"Criterion {ac_num}", "SKIP", 0.0, "Skipped by selection"))

        total_duration = time.time() - start_all
        passed = sum(1 for r in results if r.status == "PASS")
        failed = sum(1 for r in results if r.status == "FAIL")
        skipped = sum(1 for r in results if r.status == "SKIP")
        overall = "PASS" if failed == 0 else "FAIL"

        return E2ERunReport(
            timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            estate_root=str(ESTATE_ROOT),
            total_criteria=len(results),
            passed_criteria=passed,
            failed_criteria=failed,
            skipped_criteria=skipped,
            total_duration_seconds=total_duration,
            overall_verdict=overall,
            results=results,
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--ac", type=str, default="all", help="Comma-separated AC numbers to run (e.g. 1,2,3 or all)")
    parser.add_argument("--fast", action="store_true", help="Run in fast mode (structural & manifest checks)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose diagnostics")
    parser.add_argument("--json-report", type=Path, default=None, help="Save structured JSON report to path")
    args = parser.parse_args()

    if args.ac == "all":
        ac_list = ["1", "2", "3", "4", "5", "6"]
    else:
        ac_list = [x.strip().lstrip("ACac") for x in args.ac.split(",") if x.strip()]

    runner = E2ERunner(verbose=args.verbose, fast_mode=args.fast)
    report = runner.run(ac_list=ac_list)

    print("\n" + "=" * 70)
    print(f"E2E Verification Summary: {report.overall_verdict}")
    print(f"Passed: {report.passed_criteria} | Failed: {report.failed_criteria} | Skipped: {report.skipped_criteria} | Time: {report.total_duration_seconds:.2f}s")
    print("=" * 70)

    if args.json_report:
        args.json_report.parent.mkdir(parents=True, exist_ok=True)
        args.json_report.write_text(json.dumps(asdict(report), indent=2), encoding="utf-8")
        print(f"Wrote report to {args.json_report}")

    return 0 if report.overall_verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
