"""Comprehensive Estate Fuzzer and Scanner.
Scans all .md, .tex, and claim ledger files across all 9 packages in 002_projection_obstruction
for any forbidden hype vocabulary under Claim Hygiene.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from e2e_verification_suite.checks.claim_hygiene_auditor import is_allowed_context
from e2e_verification_suite.config import ALL_PACKAGES, CLAIM_HYGIENE_FORBIDDEN_WORDS, ESTATE_ROOT


def run_comprehensive_fuzz():
    pattern = re.compile(r"\b(" + "|".join(CLAIM_HYGIENE_FORBIDDEN_WORDS) + r")\b", re.IGNORECASE)

    scanned_files = 0
    total_lines = 0
    violations = []
    allowed_matches = []

    print("=== STARTING COMPREHENSIVE ESTATE FUZZING ===")

    for pkg_id, spec in sorted(ALL_PACKAGES.items()):
        pkg_dir = spec.path
        assert pkg_dir.is_dir(), f"Package dir missing: {pkg_dir}"

        # Collect target files: all .md, all .tex, all *claim* files
        candidates = set()
        for ext in ("*.md", "*.tex", "*claim*"):
            for f in pkg_dir.rglob(ext):
                # Filter out build/dist/git artifacts if any
                parts = [p.lower() for p in f.parts]
                if "dist" in parts or ".pytest_cache" in parts or "__pycache__" in parts or ".git" in parts or "target" in parts:
                    continue
                if f.is_file():
                    candidates.add(f)

        print(f"Package {spec.name} ({pkg_id}): scanning {len(candidates)} files...")

        for file_path in sorted(candidates):
            scanned_files += 1
            try:
                content = file_path.read_text(encoding="utf-8", errors="replace")
            except Exception as e:
                print(f"  [WARN] Could not read {file_path}: {e}")
                continue

            lines = content.splitlines()
            total_lines += len(lines)

            for lineno, line in enumerate(lines, start=1):
                stripped = line.strip()
                # Skip comments or schema metadata keys
                if stripped.startswith("# AuthorityEffect:") or "AuthorityEffect:" in line or stripped.startswith("%"):
                    continue

                for m in pattern.finditer(line):
                    word = m.group(1).lower()
                    if is_allowed_context(line, word):
                        allowed_matches.append((pkg_id, file_path.relative_to(ESTATE_ROOT), lineno, word, stripped[:80]))
                    else:
                        violations.append((pkg_id, file_path.relative_to(ESTATE_ROOT), lineno, word, stripped[:100]))

    print("\n=== FUZZING SUMMARY ===")
    print(f"Total packages scanned: {len(ALL_PACKAGES)}")
    print(f"Total candidate files scanned: {scanned_files}")
    print(f"Total lines scanned: {total_lines}")
    print(f"Allowed mathematically qualified occurrences: {len(allowed_matches)}")
    print(f"Forbidden unhedged violations: {len(violations)}")

    if allowed_matches:
        print("\n--- Audited Allowed Matches ---")
        for pkg_id, fpath, lineno, word, snippet in allowed_matches:
            print(f"  [ALLOWED] [{pkg_id}] {fpath}:{lineno} word='{word}' snippet='{snippet}'")

    if violations:
        print("\n--- VIOLATIONS FOUND ---")
        for pkg_id, fpath, lineno, word, snippet in violations:
            print(f"  [VIOLATION] [{pkg_id}] {fpath}:{lineno} word='{word}' snippet='{snippet}'")
        sys.exit(1)
    else:
        print("\n>>> ZERO VIOLATIONS FOUND ACROSS ALL 9 PACKAGES <<<")
        sys.exit(0)


if __name__ == "__main__":
    run_comprehensive_fuzz()
