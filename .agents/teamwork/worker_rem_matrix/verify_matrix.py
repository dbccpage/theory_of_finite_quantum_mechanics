#!/usr/bin/env python3
"""
Standalone Verification Script for TRACEABILITY_MATRIX.md
Ensures 100% of referenced Python files, Rust test symbols, and Lean 4 modules exist on disk.
Also verifies adherence to Claim Hygiene rules.
"""

import os
import re
import sys

def verify_matrix():
    matrix_path = "TRACEABILITY_MATRIX.md"
    if not os.path.isfile(matrix_path):
        print(f"ERROR: {matrix_path} not found!")
        sys.exit(1)

    with open(matrix_path, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.splitlines()
    print(f"Loaded {matrix_path}: {len(lines)} lines, {len(content)} bytes.")

    errors = []
    py_files_checked = set()
    rust_tests_checked = set()
    lean_modules_checked = set()

    # Regex patterns for tables
    # Table 1.1, 2.1, 3.1 row pattern:
    # | **ID** | Name | Scope | `py_mod`<br>`py_test` | `rust_file`<br>`rust_test` | `lean_mod.lean` (thms) | ...
    # Or in Table 3.1:
    # | **ID** | Title | Premise | `py_mod`<br>`py_test` | `rust_file`<br>`rust_test` | `lean_mod.lean` | Status |

    # 1. Audit Table 1.1, 2.1, 3.1 Claims
    # Find all table rows with Claim IDs
    claim_rows = re.findall(
        r'\|\s*\*\*(MUB6-C\d+|PO-023-C\d+|GIN-C\d+|NF-\d+|MERON-\d+|HUBBARD-\d+|ORIGIN-\d+|MAJ-C\d+)\*\*\s*\|(.*?)\|',
        content
    )
    print(f"\n1. Auditing Claim Tables (Found {len(claim_rows)} claims)...")

    for cid in ['MUB6-C01', 'PO-023-C1', 'GIN-C1', 'NF-001', 'MERON-001', 'HUBBARD-001', 'ORIGIN-001', 'MAJ-C1']:
        found = any(c[0] == cid for c in claim_rows)
        if not found:
            errors.append(f"Missing expected claim {cid} in tables")

    for line in lines:
        if not line.startswith("| **"):
            continue
        parts = [p.strip() for p in line.split("|")[1:-1]]
        if len(parts) < 6:
            continue
        cid_match = re.search(r'\*\*(MUB6-C\d+|PO-023-C\d+|GIN-C\d+|NF-\d+|MERON-\d+|HUBBARD-\d+|ORIGIN-\d+|MAJ-C\d+)\*\*', parts[0])
        if not cid_match:
            continue
        cid = cid_match.group(1)

        # Python column
        py_col = parts[3]
        py_matches = re.findall(r'`([^`]+\.py)`', py_col)
        for py_path in py_matches:
            py_files_checked.add(py_path)
            if not os.path.isfile(py_path):
                errors.append(f"[{cid}] Python file does not exist: {py_path}")

        # Rust column
        rust_col = parts[4]
        # Matches `path/to/file.rs`<br>`test_fn_name`
        rust_matches = re.findall(r'`([^`]+)`', rust_col)
        if len(rust_matches) >= 2:
            r_file = rust_matches[0]
            r_test = rust_matches[1]
            rust_tests_checked.add((r_file, r_test))
            if not os.path.isfile(r_file):
                errors.append(f"[{cid}] Rust file does not exist: {r_file}")
            else:
                with open(r_file, "r", encoding="utf-8", errors="ignore") as rfp:
                    r_content = rfp.read()
                if r_test not in r_content:
                    errors.append(f"[{cid}] Rust test '{r_test}' not found in {r_file}")

        # Lean column
        lean_col = parts[5]
        lean_matches = re.findall(r'`([a-zA-Z0-9_]+)\.lean`', lean_col)
        for l_mod in lean_matches:
            lean_modules_checked.add(l_mod)
            l_path = os.path.join("lean4", l_mod + ".lean")
            if not os.path.isfile(l_path):
                errors.append(f"[{cid}] Lean 4 module does not exist: {l_path}")

    print(f"  Claims checked: {len(claim_rows)} (Target: 96)")
    print(f"  Unique Python files verified: {len(py_files_checked)}")
    print(f"  Unique Rust test functions verified: {len(rust_tests_checked)}")
    print(f"  Unique Lean 4 modules verified: {len(lean_modules_checked)}")

    # 2. Audit Table 2.2 (FSP Derivations)
    print("\n2. Auditing Table 2.2 FSP Derivations...")
    t2_match = re.search(r'### 2\.3 Table 2\.2: FSP Derivation DAG Register.*?\n(\|.*?)\n\n## Section 3', content, re.DOTALL)
    if t2_match:
        t2_lines = [l for l in t2_match.group(1).splitlines() if l.startswith("| **FSP-DERIV-")]
        print(f"  Found {len(t2_lines)} FSP derivation rows.")
        for row in t2_lines:
            cols = [c.strip() for c in row.split("|")[1:-1]]
            did = cols[0]
            lean_entry = cols[7].replace("`", "")
            lean_mod = lean_entry.split("::")[0].strip()
            if "/" in lean_mod or "\\" in lean_mod:
                errors.append(f"[{did}] Un-migrated non-flat Lean 4 path in Table 2.2: {lean_entry}")
            lean_path = os.path.join("lean4", lean_mod)
            if not os.path.isfile(lean_path):
                errors.append(f"[{did}] Lean 4 file in Table 2.2 does not exist: {lean_path}")

    # 3. Audit Claim Hygiene
    print("\n3. Auditing Claim Hygiene & Forbidden Words...")
    forbidden_words = [
        "proves", "guarantees", "mathematically verifies", "fundamentally",
        "true intelligence", "impossible", "flawless", "perfectly",
        "clearly", "obviously", "simply", "merely", "weaponized"
    ]
    for word in forbidden_words:
        # Case insensitive word match
        matches = re.finditer(rf'\b{re.escape(word)}\b', content, re.IGNORECASE)
        for m in matches:
            # Check context
            start = max(0, m.start() - 30)
            end = min(len(content), m.end() + 30)
            snippet = content[start:end].replace("\n", " ")
            errors.append(f"Forbidden word '{word}' found at byte {m.start()}: \"...{snippet}...\"")

    # Audit 'universal' occurrences (allowed only when negatively scoped)
    univ_matches = [m.start() for m in re.finditer(r'\buniversal\b', content, re.IGNORECASE)]
    for pos in univ_matches:
        start = max(0, pos - 40)
        end = min(len(content), pos + 40)
        snippet = content[start:end].replace("\n", " ").lower()
        if not ("not" in snippet or "troyer-wiese" in snippet or "barrier" in snippet):
            errors.append(f"Unhedged promotional use of 'universal' near byte {pos}: \"...{snippet}...\"")

    # 4. Mandatory Section 6 Summaries
    print("\n4. Auditing Mandatory Section 6 Summaries...")
    for sec_num, sec_name in [("6.1", "MUB(6)"), ("6.2", "FSP"), ("6.3", "Majorana")]:
        if f"### {sec_num}" not in content:
            errors.append(f"Missing Section {sec_num} ({sec_name}) summary in Section 6")
        for item in ["1. **What it supports:**", "2. **What it does not support:**", "3. **The narrowest defensible claim:**", "4. **The next test needed:**"]:
            if item not in content:
                errors.append(f"Section 6 missing required 4-point bullet: {item}")

    print("\n" + "=" * 60)
    if errors:
        print(f"VERIFICATION FAILED: {len(errors)} errors detected!")
        for e in errors:
            print("  - " + e)
        sys.exit(1)
    else:
        print("VERIFICATION SUCCESS: 100% of referenced Python files, Rust test symbols,")
        print("and Lean 4 modules exist on disk with 0 errors. Claim hygiene passes.")
        print("=" * 60)
        sys.exit(0)

if __name__ == "__main__":
    verify_matrix()
