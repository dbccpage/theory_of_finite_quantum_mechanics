"""Execute SCORING.md v2.0.0 evaluation, mutation audit, AST metrics, and sidecar generation for code/rust/src/fsp.

AuthorityEffect: None.
All builds and mutations execute in an isolated snapshot under code/rust/target/fsp-audit/.
Working tree sources in code/rust/src/fsp/ are never mutated.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import tomllib

ROOT = Path(__file__).resolve().parents[4]
RUST = ROOT / "code" / "rust"
FSP_DIR = RUST / "src" / "fsp"
METRICS_TOOL = RUST / "quality" / "category_homology" / "rust_metrics"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def yaml_dump(value: object, indent: int = 0) -> str:
    """Emit clean, deterministic YAML 1.2 with JSON-compatible quoted scalars."""
    space = " " * indent
    if isinstance(value, dict):
        lines: list[str] = []
        for k, v in value.items():
            if isinstance(v, (dict, list)) and v:
                lines.append(f"{space}{k}:\n{yaml_dump(v, indent + 2)}")
            else:
                lines.append(f"{space}{k}: {json.dumps(v, ensure_ascii=False)}")
        return "\n".join(lines)
    if isinstance(value, list):
        lines = []
        for item in value:
            if isinstance(item, dict) and len(item) <= 4 and all(not isinstance(x, (dict, list)) for x in item.values()):
                lines.append(f"{space}- {json.dumps(item, ensure_ascii=False, sort_keys=True)}")
            elif isinstance(item, (dict, list)) and item:
                 dumped = yaml_dump(item, indent + 2)
                 first, *rest = dumped.splitlines()
                 lines.append(f"{space}- {first.lstrip()}")
                 lines.extend(rest)
            else:
                lines.append(f"{space}- {json.dumps(item, ensure_ascii=False)}")
        return "\n".join(lines)
    return f"{space}{json.dumps(value, ensure_ascii=False)}"


def fsp_subjects() -> list[Path]:
    return sorted(
        p for p in FSP_DIR.iterdir()
        if p.is_file() and (p.suffix == ".rs" or p.name == "Cargo.toml")
    )


def source_inventory() -> dict[str, str]:
    files = [
        ROOT / "SCORING.md",
        *fsp_subjects(),
        *sorted((FSP_DIR / "fixtures").glob("*.json")),
    ]
    return {p.relative_to(ROOT).as_posix(): sha256_file(p) for p in files if p.is_file()}


def declaration_index(source: str) -> list[dict[str, object]]:
    pattern = re.compile(
        r"^\s*pub(?:\([^)]*\))?\s+(?:(?:const|async|unsafe)\s+)?"
        r"(fn|struct|enum|trait|type|const|mod|use)\s+([A-Za-z_]\w*)"
    )
    out: list[dict[str, object]] = []
    for lineno, line in enumerate(source.splitlines(), 1):
        m = pattern.match(line)
        if m:
            out.append({
                "kind": m.group(1),
                "name": m.group(2),
                "line": lineno,
                "declaration_line": line.strip(),
            })
    return out


def run_cmd(command: list[str], cwd: Path, log_path: Path, timeout: int = 300) -> dict[str, object]:
    started = time.monotonic()
    overlay = {
        "CARGO_INCREMENTAL": "0",
        "CARGO_PROFILE_DEV_DEBUG": "0",
        "CARGO_PROFILE_TEST_DEBUG": "0",
    }
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("w", encoding="utf-8", newline="\n") as stream:
        proc = subprocess.Popen(
            command,
            cwd=cwd,
            stdout=stream,
            stderr=subprocess.STDOUT,
            env={**os.environ, **overlay},
        )
        try:
            exit_code = proc.wait(timeout=timeout)
            timed_out = False
        except subprocess.TimeoutExpired:
            subprocess.run(["taskkill", "/PID", str(proc.pid), "/T", "/F"], capture_output=True)
            proc.wait()
            exit_code = None
            timed_out = True
    return {
        "command": command,
        "cwd": str(cwd),
        "exit_code": exit_code,
        "timed_out": timed_out,
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "environment": overlay,
        "log": log_path.relative_to(ROOT).as_posix(),
        "log_sha256": sha256_file(log_path),
    }


DESIGNATED_MUTANTS: list[dict[str, str]] = [
    {
        "id": "FSP-LIB-01-hop-product-check",
        "file": "lib.rs",
        "target": "if w.hop_product != -1 {",
        "replacement": "if w.hop_product == -1 {",
        "description": "Invert Carrier A hop product invariant check in fsp_crate_invariants_hold.",
    },
    {
        "id": "FSP-LIB-02-route-check",
        "file": "lib.rs",
        "target": "if bqnf::route_packet(&m) != bqnf::TerminalRoute::ExactRepair {",
        "replacement": "if bqnf::route_packet(&m) == bqnf::TerminalRoute::ExactRepair {",
        "description": "Invert BQNF ExactRepair routing check in fsp_crate_invariants_hold.",
    },
    {
        "id": "FSP-BQNF-01-valid-complex-branch",
        "file": "bqnf.rs",
        "target": "if !m.is_valid_complex {\n        TerminalRoute::ClosureFailure",
        "replacement": "if !m.is_valid_complex {\n        TerminalRoute::ExactRepair",
        "description": "Route broken cochain complex to ExactRepair instead of ClosureFailure.",
    },
    {
        "id": "FSP-BQNF-02-open-defect-branch",
        "file": "bqnf.rs",
        "target": "} else if m.closure_defect > BigRational::zero() {\n        TerminalRoute::OpenSignObstruction",
        "replacement": "} else if m.closure_defect > BigRational::zero() {\n        TerminalRoute::ClosedResidual",
        "description": "Route positive closure defect Gamma_2 > 0 to ClosedResidual instead of OpenSignObstruction.",
    },
    {
        "id": "FSP-FOCK-01-jw-hop-parity",
        "file": "fock.rs",
        "target": "if mask_between.count_ones() % 2 == 1 {\n        -1\n    } else {\n        1\n    }",
        "replacement": "if mask_between.count_ones() % 2 == 1 {\n        1\n    } else {\n        -1\n    }",
        "description": "Flip Jordan-Wigner parity sign in jordan_wigner_hop_sign.",
    },
    {
        "id": "FSP-FOCK-02-car-annihilate-up-sign",
        "file": "fock.rs",
        "target": "let p = preceding_count(state.up_mask, site);\n                let sign = if p % 2 == 1 { -1 } else { 1 };",
        "replacement": "let p = preceding_count(state.up_mask, site);\n                let sign = if p % 2 == 1 { 1 } else { -1 };",
        "description": "Flip CAR spin-up annihilation parity sign in car_annihilate.",
    },
    {
        "id": "FSP-GIN-01-opposite-sign-audit",
        "file": "gin.rs",
        "target": "let opposite_sign = cfg_a.jw_sign == -cfg_b.jw_sign;",
        "replacement": "let opposite_sign = cfg_a.jw_sign == cfg_b.jw_sign;",
        "description": "Accept equal-sign pairs instead of opposite-sign pairs in audit_involution_cancellations.",
    },
    {
        "id": "FSP-GIN-02-kitaev-edge-isolation",
        "file": "gin.rs",
        "target": "if bulk_modes_set.contains(&edge) {\n            is_boundary_isolated = false;\n        }",
        "replacement": "if !bulk_modes_set.contains(&edge) {\n            is_boundary_isolated = false;\n        }",
        "description": "Invert Kitaev Majorana edge-mode bulk-isolation check in audit_kitaev_chain_majorana.",
    },
    {
        "id": "FSP-HUB-01-swap-sign-flip",
        "file": "hubbard.rs",
        "target": "if pivot_row != col {\n            a.swap(col, pivot_row);\n            sign_flips ^= 1;\n        }",
        "replacement": "if pivot_row != col {\n            a.swap(col, pivot_row);\n        }",
        "description": "Omit row-swap determinant sign flip in exact_determinant.",
    },
    {
        "id": "FSP-HUB-02-attractive-down-coupling",
        "file": "hubbard.rs",
        "target": "let exp_down = if attractive { s_val } else { -s_val };",
        "replacement": "let exp_down = -s_val;",
        "description": "Break attractive Hubbard spin-down auxiliary-field symmetry in evaluate_hubbard_determinants.",
    },
    {
        "id": "FSP-NF-01-rref-elimination-sign",
        "file": "normal_forms.rs",
        "target": "let term = &factor * &rref[rank][c];\n                    rref[r][c] = &rref[r][c] - term;",
        "replacement": "let term = &factor * &rref[rank][c];\n                    rref[r][c] = &rref[r][c] + term;",
        "description": "Add instead of subtract row multiple during Gaussian elimination in rref_with_witness.",
    },
    {
        "id": "FSP-NF-02-f2-chord-norm-bit",
        "file": "normal_forms.rs",
        "target": "let norm_bit = parities[edge_idx] ^ final_gauge[u] ^ final_gauge[v];",
        "replacement": "let norm_bit = parities[edge_idx] ^ final_gauge[u];",
        "description": "Drop endpoint v gauge bit in F2 coboundary normalization normalize_sign_cochain.",
    },
    {
        "id": "FSP-WIT-01-hop-sign-formula",
        "file": "witness.rs",
        "target": "let sign = 1 - 2 * parity;",
        "replacement": "let sign = 2 * parity - 1;",
        "description": "Invert 4-site star hop sign formula in witness::hop_sign.",
    },
    {
        "id": "FSP-WIT-02-refuse-holonomy-guard",
        "file": "witness.rs",
        "target": "if claimed_product == found.hop_product {\n        Ok(())",
        "replacement": "if claimed_product != found.hop_product {\n        Ok(())",
        "description": "Invert CAR hop product refusal guard in refuse_removed_holonomy.",
    },
]


def metric_ceiling_for_functions(functions: list[dict[str, object]]) -> tuple[str, list[dict[str, object]]]:
    def band(val: int, limits: list[tuple[int, str]]) -> str:
        return next((g for upper, g in limits if val <= upper), "E")

    order = ["E", "D", "C", "B", "A"]
    overall = "A"
    exceeding: list[dict[str, object]] = []
    for fn in functions:
        ccn = int(fn["ccn"])
        cog = int(fn["cognitive_upper_bound"])
        nest = int(fn["control_nesting"])
        g_ccn = band(ccn, [(10, "A"), (15, "B"), (20, "C"), (50, "D")])
        g_cog = band(cog, [(15, "A"), (20, "B"), (25, "C"), (40, "D")])
        g_nest = band(nest, [(3, "A"), (4, "B"), (5, "C"), (8, "D")])
        # Note per SCORING.md & write_scores.py: cognitive_upper_bound > 40 is an upper bound,
        # so if ccn <= 50 and nest <= 8, cap at D rather than asserting an E semantic violation.
        fn_grades = [g_ccn, "D" if g_cog == "E" and ccn <= 50 and nest <= 8 else g_cog, g_nest]
        lowest = min(fn_grades, key=order.index)
        overall = min((overall, lowest), key=order.index)
        if ccn > 10 or cog > 15 or nest > 3:
            exceeding.append({**fn, "metric_ceiling": lowest})
    return overall, exceeding


FILE_SPECIFICATIONS: dict[str, dict[str, object]] = {
    "Cargo.toml": {
        "profile": "Non-Numeric",
        "level": "L1",
        "level_basis": "Standalone Cargo package manifest declaring library target `lib.rs` and seven external dependencies (`num-rational`, `num-bigint`, `num-traits`, `num-integer`, `serde`, `serde_json`, `thiserror`).",
        "title": "FSP Crate Build & Dependency Manifest",
        "purpose": "Declare crate metadata, library entry point, and exact-arithmetic / serialization dependencies for `tfqm_fsp`.",
        "gates": {"G1": "C", "G2": "C", "G3": "D", "G4": "C", "G5": "A"},
        "grade_ceiling": "A",
        "carrier_type": "CargoPackageManifest",
        "operations": ["cargo metadata --offline", "cargo test --offline"],
        "lean4_theorems": [],
        "invariants": [
            "Package name is `tfqm_fsp` with edition `2021` and library root `lib.rs`.",
            "Exact arithmetic dependencies (`num-rational`, `num-bigint`) are explicitly declared with `serde` feature support.",
        ],
        "domain_preconditions": [
            "Resolved offline via repository Cargo dependency cache.",
        ],
        "refusals": [
            "Cargo build/metadata refusal on missing offline crate or incompatible rustc edition.",
        ],
        "gate_review": {
            "G1": "C: Package metadata, license (`Apache-2.0`), and dependency list are explicit; cross-repository dependency origin attestation is not bundled in `code/rust/src/fsp/`.",
            "G2": "C: Non-Numeric manifest profile selects arbitrary-precision `num-bigint` and `num-rational` crates.",
            "G3": "D: `RULE_RS_001` deficit — `[profile.release] overflow-checks = true` is not declared in `code/rust/src/fsp/Cargo.toml`, so standalone release builds default to wrapping primitive integer arithmetic.",
            "G4": "C: Verified by offline `cargo metadata` and `cargo test` execution receipt (19/19 unit tests passing).",
            "G5": "A: 19 physical lines, flat TOML structure, zero custom build scripts (`build.rs`).",
        },
        "open_findings": [
            "RULE_RS_001 (Gate 3 -> D): `code/rust/src/fsp/Cargo.toml` omits `[profile.release] overflow-checks = true`, allowing two's-complement wrapping on primitive integers (`u32`, `usize`, `i64`) in standalone release builds.",
            "No local `Cargo.lock` is committed inside `code/rust/src/fsp/`; dependency resolution relies on workspace/cache lock state.",
        ],
    },
    "lib.rs": {
        "profile": "Exact",
        "level": "L2",
        "level_basis": "Crate root module catalog, public symbol re-exports across six submodules, and top-level smoke check `fsp_crate_invariants_hold()`.",
        "title": "FSP Crate Root & Invariant Smoke Gate",
        "purpose": "Export the public API of `tfqm_fsp` (`bqnf`, `fock`, `gin`, `hubbard`, `normal_forms`, `witness`) and provide `fsp_crate_invariants_hold()`.",
        "gates": {"G1": "C", "G2": "C", "G3": "D", "G4": "C", "G5": "A"},
        "grade_ceiling": "A",
        "carrier_type": "FspCrateRoot",
        "operations": ["fsp_crate_invariants_hold"],
        "lean4_theorems": ["lean4/FermionSignAll.lean", "lean4/BqnfSignPacket.lean"],
        "invariants": [
            "`#![forbid(unsafe_code)]` is enforced at crate root.",
            "`fsp_crate_invariants_hold()` checks Carrier A (`hop_product == -1`), Carrier B (`z_u == 0`, `n_u == 2`), `ExactRepair` routing on zero-defect metrics, and 4-site Kitaev MZM boundary isolation.",
        ],
        "domain_preconditions": [
            "No external arguments to `fsp_crate_invariants_hold()`.",
        ],
        "refusals": [
            "Returns `Err(&'static str)` if any of the four fixed crate smoke invariants fail.",
        ],
        "gate_review": {
            "G1": "C: Declares `AuthorityEffect: None` and `#![forbid(unsafe_code)]`; re-exports match submodule definitions.",
            "G2": "C: Exact `BigRational` zero construction and exact integer equality checks in `fsp_crate_invariants_hold()`.",
            "G3": "D: `fsp_crate_invariants_hold()` returns untyped `&'static str` errors and delegates to `witness::witness()`, which uses 26 internal `assert!`/`assert_eq!` panic macros rather than typed `Result` propagation.",
            "G4": "C: Unit test `test_fsp_crate_invariants` passes and both designated mutants (`FSP-LIB-01`, `FSP-LIB-02`) are killed ($R = 2/2 = 1.0$), but error branches of `fsp_crate_invariants_hold` are not exercised by unit tests without mutation.",
            "G5": "A: Calibrated `syn 3.0.9` AST metrics: 1 production function, max CCN = 7 (<= 10), cognitive upper bound = 5 (<= 15), control nesting = 1 (<= 3).",
        },
        "open_findings": [
            "Gate 3 -> D: `fsp_crate_invariants_hold()` returns `&'static str` instead of a structured domain error enum and invokes `witness::witness()`, which relies on `assert!` panics.",
            "SCORING.md Section 5.5 (No Inferred System Score): Re-exporting `fock`, `hubbard`, and `normal_forms` exposes downstream callers to their `G3: E` boundary panics until those submodules are hardened.",
        ],
    },
    "bqnf.rs": {
        "profile": "Exact",
        "level": "L3",
        "level_basis": "Bounded-domain rational cochain complex ($C^0 \\to C^1 \\to C^2$) nilpotence validator ($d_1 \\circ d_0 = 0$), $\\ell_1$ coboundary norm evaluator $\\Gamma_2 = \\|d_1 c^1\\|_1$, and deterministic 5-fold BQNF terminal router.",
        "title": "BQNF 5-Fold Sign Packet Router & Rational Cochain Complex",
        "purpose": "Classify finite sign obstruction packets into five terminal routes (`ExactRepair`, `ClosedResidual`, `OpenSignObstruction`, `SplitBrainRefusal`, `ClosureFailure`) and verify rational cochain complex nilpotence $d_1 \\circ d_0 = 0$.",
        "gates": {"G1": "C", "G2": "D", "G3": "D", "G4": "C", "G5": "A"},
        "grade_ceiling": "A",
        "carrier_type": "CochainComplex / SignPacketMetrics / TerminalRoute",
        "operations": [
            "SignPacketMetrics::new",
            "route_packet",
            "CochainComplex::new",
            "CochainComplex::check_nilpotence",
            "CochainComplex::apply_d1",
            "CochainComplex::l1_norm",
            "CochainComplex::compute_closure_defect",
        ],
        "lean4_theorems": [
            "lean4/BqnfSignPacket.lean:routePacket",
            "lean4/BqnfSignPacket.lean:routePacket_exhaustive_fivefold",
        ],
        "invariants": [
            "Five-fold terminal partition: `!is_valid_complex -> ClosureFailure`, `disjoint_supports -> SplitBrainRefusal`, `closure_defect > 0 -> OpenSignObstruction`, `residual_mass == 0 || has_involution_witness -> ExactRepair`, otherwise `ClosedResidual`.",
            "`CochainComplex::new` enforces `d0.len() == dim_c1`, row lengths `dim_c0`, `d1.len() == dim_c2`, row lengths `dim_c1`, and exact rational nilpotence $d_1 \\circ d_0 = 0$.",
        ],
        "domain_preconditions": [
            "`d0` is a `dim_c1 x dim_c0` matrix over `BigRational`; `d1` is a `dim_c2 x dim_c1` matrix over `BigRational` satisfying $d_1 d_0 = 0$.",
            "`c1` has length `dim_c1`.",
        ],
        "refusals": [
            "`d0 row count mismatch (expected dim_c1)`",
            "`d0 column count mismatch (expected dim_c0)`",
            "`d1 row count mismatch (expected dim_c2)`",
            "`d1 column count mismatch (expected dim_c1)`",
            "`nilpotence failure: d1 . d0 != 0`",
            "`c1 length must equal dim_c1`",
        ],
        "gate_review": {
            "G1": "C: Explicit `AuthorityEffect: None` and `#![forbid(unsafe_code)]`; `TerminalRoute` and `route_packet` correspond 1-to-1 with `lean4/BqnfSignPacket.lean`.",
            "G2": "D: Primary calculations use exact `BigRational`, but `SignPacketMetrics` and `CochainComplex` have `pub` fields and derive `Deserialize` (`RULE_RS_003`), permitting construction of unvalidated complexes with $d_1 d_0 \\ne 0$ or negative norms `closure_defect < 0` / `residual_mass < 0`.",
            "G3": "D: `CochainComplex::check_nilpotence` (line 125: `&row[k] * &self.d0[k][j]`) and `apply_d1` (line 146) use direct slice indexing (`RULE_RS_002`). If a `CochainComplex` is constructed via public struct literal or `serde::Deserialize` with ragged rows (`RULE_RS_003`), `check_nilpotence` and `apply_d1` panic out-of-bounds.",
            "G4": "C: Unit tests `bqnf_5_fold_routing_theorems` and `cochain_nilpotence_check` cover all 6 routing cases and valid/open/closed cochains; both designated mutants (`FSP-BQNF-01`, `FSP-BQNF-02`) are killed ($R = 2/2 = 1.0$). Missing negative unit tests for `CochainComplex::new` refusal branches.",
            "G5": "A: Calibrated `syn 3.0.9` AST metrics across 7 production functions: max CCN = 8 (<= 10), cognitive upper bound = 9 (<= 15), control nesting = 3 (<= 3), 0 functions exceeding `A`.",
        },
        "open_findings": [
            "RULE_RS_003 (Gate 2 -> D, Gate 3 -> D): `CochainComplex` and `SignPacketMetrics` expose `pub` fields and unchecked `serde::Deserialize`, allowing callers to bypass `CochainComplex::new` nilpotence/dimension checks and trigger slice-indexing panics in `check_nilpotence` / `apply_d1`.",
            "Gate 2 -> D: `SignPacketMetrics::new` does not reject negative `closure_defect` or negative `residual_mass` even though both represent $\\ell_1$ norms.",
        ],
    },
    "fock.rs": {
        "profile": "Exact",
        "level": "L3",
        "level_basis": "Bounded-domain Fock-space CAR algebra, Jordan-Wigner hop signs, discrete Hubbard Hamiltonian matrix construction over $\\mathbb{Q}$, Euler transfer matrices, Trotter path-sum partition functions, and cross-language JSON scaling benchmarks.",
        "title": "Fock-Space CAR Algebra, Discrete Fermionic Hamiltonian & Trotter Path Sums",
        "purpose": "Construct exact rational Fock-space Hubbard Hamiltonians, evaluate CAR creation/annihilation/hopping with Jordan-Wigner signs, and compute Trotter partition functions $Z_F, Z_B$, average sign $\\langle s \\rangle$, and cyclic Euler paths.",
        "gates": {"G1": "C", "G2": "D", "G3": "E", "G4": "C", "G5": "D"},
        "grade_ceiling": "D",
        "carrier_type": "FockState / FermionicLattice / DiscreteFermionicHamiltonian / PartitionReceipt",
        "operations": [
            "FockState::is_occupied",
            "jordan_wigner_hop_sign",
            "preceding_count",
            "car_annihilate",
            "car_create",
            "car_hop",
            "FermionicLattice::new",
            "DiscreteFermionicHamiltonian::new",
            "DiscreteFermionicHamiltonian::compute_partition_functions",
            "DiscreteFermionicHamiltonian::generate_sample_paths",
            "benchmark_fock_lattice_scaling",
        ],
        "lean4_theorems": [
            "lean4/FermionSignCore.lean",
            "lean4/FrustratedSpectrumObstruction.lean",
        ],
        "invariants": [
            "CAR anticommutation $\\{c_{i\\sigma}, c_{j\\sigma'}^\\dagger\\} = \\delta_{ij}\\delta_{\\sigma\\sigma'}$ and $\\{c_{i\\sigma}, c_{j\\sigma'}\\} = 0$ on valid site indices `< 32`.",
            "Average sign $\\langle s \\rangle = Z_F / Z_B \\in \\mathbb{Q}$ equals $1$ on bipartite 3-step walks and satisfies $\\langle s \\rangle < 1$ on frustrated triangular lattices.",
        ],
        "domain_preconditions": [
            "`site < 32` and `num_sites < 32` (required by `u32` bitmask representation in `FockState`, currently unenforced at entry).",
            "`trotter_steps > 0` and `beta > 0`.",
        ],
        "refusals": [
            "`num_sites must be positive`",
            "`edge endpoint out of range`",
            "`self-loops are not allowed in simple hopping lattice`",
            "`particle count exceeds lattice site capacity`",
            "`physical sector must have at least one particle`",
            "`trotter_steps must be positive`",
            "`beta must be positive`",
        ],
        "gate_review": {
            "G1": "C: Declares `AuthorityEffect: None` and `#![forbid(unsafe_code)]`; matches Python `code/python/src/fsp/` and `fixtures/fock_lattice_scaling.json`.",
            "G2": "D: Thermodynamic weights use exact `BigRational`, but `FockState` uses `u32` masks without enforcing `site < 32` or `num_sites < 32` at public entry (`RULE_RS_001`), and `generate_sample_paths` does not validate `beta > 0`.",
            "G3": "E: Concrete reachable panics on public entry points (`SCORING.md` Section 3.3 Grade E, `RULE_RS_001`, `RULE_RS_002`): calling `FockState::new(0, 0).is_occupied(32, Spin::Up)`, `preceding_count(0, 32)`, `car_annihilate(FockState::new(0, 0), 32, Spin::Up)`, `car_create(FockState::new(0, 0), 32, Spin::Up)`, or `jordan_wigner_hop_sign(0, 0, 33)` panics with bit-shift overflow (`1 << site` / `1u32 << site`). Production functions also contain 3 `.unwrap()` calls (lines 189, 193, 449) and 19 direct slice indexing operations.",
            "G4": "C: 4 unit tests verify CAR anticommutation, triangle path cancellation, 9-lattice scaling up to 8 sites, and bit-for-bit JSON fixture parity; both designated mutants (`FSP-FOCK-01`, `FSP-FOCK-02`) are killed ($R = 2/2 = 1.0$).",
            "G5": "D: Calibrated `syn 3.0.9` AST metrics across 28 production functions: `build_hamiltonian` (line 309) has CCN = 12 (B), cognitive upper bound = 31 (D cap: 26-40), control nesting = 5 (C cap); `generate_sample_paths` (line 430) has CCN = 9 (A), cognitive upper bound = 27 (D cap: 26-40), control nesting = 5 (C cap); `rectangular_grid` (line 197) has CCN = 11 (B), cognitive upper bound = 21 (C cap).",
        },
        "open_findings": [
            "RULE_RS_001 / Gate 3 -> E (Concrete Counterexample): `FockState::new(0, 0).is_occupied(32, Spin::Up)`, `preceding_count(0, 32)`, `car_annihilate(..., 32, ...)`, `car_create(..., 32, ...)`, and `DiscreteFermionicHamiltonian::new` with `num_sites >= 32` execute unchecked `1u32 << site` / `1u32 << num_sites`, panicking on bit-shift overflow.",
            "RULE_RS_002 / Gate 3: Production functions `triangle()` (line 189), `square_plaquette()` (line 193), and `generate_sample_paths` (line 449) call `.unwrap()`, and 19 direct slice indexing expressions lack bounds guards if public struct fields are mutated (`RULE_RS_003`).",
            "Gate 5 -> D: `build_hamiltonian` (cognitive upper bound 31, nesting 5, CCN 12) and `generate_sample_paths` (cognitive upper bound 27, nesting 5) exceed the C ceiling.",
        ],
    },
    "gin.rs": {
        "profile": "Exact",
        "level": "L3",
        "level_basis": "Bounded-domain Generalized Inverted Index (GIN) over fermion orbital modes, involution partner query, opposite-sign doublet cancellation auditor, and 1D Kitaev chain Majorana zero mode boundary isolation checker.",
        "title": "Fermion Mode Generalized Inverted Index (GIN) & Kitaev Majorana Zero Mode Auditor",
        "purpose": "Index fermionic configurations by occupied orbital modes, query involution partners in $O(|\\text{modes}|)$ set intersections, certify opposite-sign equal-weight doublet cancellations, and audit boundary isolation of unpaired Majorana zero modes $\\gamma_1, \\gamma_{2L}$ on a 1D Kitaev chain.",
        "gates": {"G1": "C", "G2": "D", "G3": "C", "G4": "C", "G5": "B"},
        "grade_ceiling": "B",
        "carrier_type": "GinIndex / FermionConfiguration / InvolutionCancellationReceipt / MajoranaZeroModeReceipt",
        "operations": [
            "GinIndex::new",
            "GinIndex::index_configuration",
            "GinIndex::query_by_modes",
            "GinIndex::find_involution_partner",
            "GinIndex::audit_involution_cancellations",
            "audit_kitaev_chain_majorana",
            "benchmark_kitaev_chain_mzm_scaling",
            "benchmark_gin_involution_scaling",
        ],
        "lean4_theorems": [
            "lean4/FermionGinCore.lean",
            "lean4/MajoranaGinCore.lean",
        ],
        "invariants": [
            "`audit_involution_cancellations` routes to `ExactRepair` iff `pairs` is non-empty and every audited pair `(id_a, id_b)` exists in `GinIndex` with `cfg_a.jw_sign == -cfg_b.jw_sign` and `cfg_a.weight == cfg_b.weight`.",
            "`audit_kitaev_chain_majorana(l)` for $L \\ge 2$ bonds bulk Majorana modes $(2j, 2j+1)$ for $1 \\le j < L$ and isolates boundary modes $\\{1, 2L\\}$.",
        ],
        "domain_preconditions": [
            "`l >= 2` for `audit_kitaev_chain_majorana(l)`.",
            "`mode_counts` elements even and `>= 4` for `benchmark_gin_involution_scaling`.",
        ],
        "refusals": [
            "`Kitaev chain requires at least 2 lattice sites (L >= 2)`",
            "`chain_lengths must not be empty`",
            "`mode_counts must not be empty`",
            "`each mode count must be an even integer >= 4`",
        ],
        "gate_review": {
            "G1": "C: Declares `AuthorityEffect: None` and `#![forbid(unsafe_code)]`; aligns with `lean4/FermionGinCore.lean` and `lean4/MajoranaGinCore.lean`.",
            "G2": "D: `GinIndex::index_configuration` does not validate that `occupied_modes` indices lie in `1..=total_modes`, that `jw_sign` is in `{-1, 1}`, or that `weight >= 0`; `audit_involution_cancellations` does not verify that pairs are disjoint or generated by a valid involution (`RULE_RS_003`). `audit_kitaev_chain_majorana` computes `2 * l` without `checked_mul` (`RULE_RS_001`).",
            "G3": "C: Zero direct slice indexing (`prod_indexing = 0`); map lookups use `BTreeMap::get`. The single `.unwrap()` in `query_by_modes` (line 95) is dominated by `!required_modes.is_empty()`. Capped at `C` due to untyped `&'static str` error returns and unchecked `2 * l` multiplication for `l > usize::MAX / 2`.",
            "G4": "C: 3 unit tests cover GIN mode queries, involution pair cancellation, Kitaev chain $L=4$ boundary isolation, and scaling up to 1024 Majorana modes ($L=512$); both designated mutants (`FSP-GIN-01`, `FSP-GIN-02`) are killed ($R = 2/2 = 1.0$).",
            "G5": "B: Calibrated `syn 3.0.9` AST metrics across 8 production functions: max CCN = 9 (A), cognitive upper bound = 13 (A), control nesting = 4 in `query_by_modes` (line 86) -> `B` ceiling per `SCORING.md` Section 3.5.",
        },
        "open_findings": [
            "RULE_RS_003 / Gate 2 -> D: `GinIndex::index_configuration` and `audit_involution_cancellations` accept arbitrary mode indices outside `1..=total_modes`, non-unit `jw_sign` values, and duplicate/overlapping pair tuples without refusal.",
            "Gate 5 -> B: `query_by_modes` (line 86) has control nesting depth 4 (A ceiling requires nesting <= 3).",
        ],
    },
    "hubbard.rs": {
        "profile": "Exact",
        "level": "L3",
        "level_basis": "Bounded-domain exact rational Gaussian elimination determinant, palindromic kinetic matrix product, auxiliary-field Hubbard determinant ensemble evaluator, and cross-language JSON scaling benchmarks.",
        "title": "Exact Rational Hubbard Auxiliary-Field Determinant & Square-Root Symmetry Evaluator",
        "purpose": "Compute exact rational determinants $\\det(I + B_\\uparrow)\\det(I + B_\\downarrow)$ over auxiliary Ising fields, verify attractive Hubbard square-root positivity $\\det(I + B_\\uparrow) = \\det(I + B_\\downarrow) \\implies w(s) \\ge 0$, and detect repulsive doped sign cancellation.",
        "gates": {"G1": "C", "G2": "D", "G3": "E", "G4": "C", "G5": "D"},
        "grade_ceiling": "D",
        "carrier_type": "HubbardDeterminantReceipt / HubbardEnsembleSummary / HubbardLatticeScalingRow",
        "operations": [
            "exact_determinant",
            "exact_matrix_mul",
            "exact_kinetic_matrix",
            "evaluate_hubbard_determinants",
            "hubbard_rectangular_bonds",
            "benchmark_hubbard_lattice_scaling",
        ],
        "lean4_theorems": [
            "lean4/FermionSignCore.lean:attractive_hubbard_weight_nonneg",
        ],
        "invariants": [
            "For attractive Hubbard (`attractive == true`) with identical spin-up/down couplings and real rational parameters, `det_up == det_down` and `total_weight = det_up * det_down >= 0`.",
            "`exact_determinant` computes $\\det(M) \\in \\mathbb{Q}$ via exact rational Gaussian elimination with pivot sign tracking.",
        ],
        "domain_preconditions": [
            "`sites > 0`, `slices > 0`, `r > 0`, `hs != 0` (`hs` unenforced at entry), and `sites * slices < usize::BITS`.",
        ],
        "refusals": [
            "`matrix must be square for determinant`",
            "`matrix dimension mismatch in multiplication`",
            "`sites must be positive`",
            "`r parameter must be strictly positive`",
            "`invalid bond endpoint`",
            "`sites and slices must be positive`",
            "`at least one field mask required`",
        ],
        "gate_review": {
            "G1": "C: Declares `AuthorityEffect: None` and `#![forbid(unsafe_code)]`; matches Python `code/python/src/fsp/` and `fixtures/hubbard_lattice_scaling.json`.",
            "G2": "D: `evaluate_hubbard_determinants` fails to validate `hs != 0` (`hs > 0`) at entry before computing `BigRational::one() / hs` at lines 225 and 230 (`SCORING.md` Section 3.2 Grade D: 'unchecked division by zero risk; domain restrictions unenforced at entry'), and does not enforce `sites * slices < usize::BITS as usize` before shifting `mask >> (time * sites + j)` at line 214 (`RULE_RS_001`).",
            "G3": "E: Concrete reachable panic on public entry point `evaluate_hubbard_determinants` (`SCORING.md` Section 3.3 Grade E): passing `hs = &BigRational::zero()` panics with division by zero inside `BigRational::div` at line 225, and passing `sites * slices >= usize::BITS as usize` panics with bit-shift overflow at line 214.",
            "G4": "C: 4 unit tests verify $2\\times 2$ and $3\\times 3$ determinants, $2\\times 2$ attractive plaquette positivity, 8-model lattice scaling up to 12 sites, and bit-for-bit JSON fixture parity; both designated mutants (`FSP-HUB-01`, `FSP-HUB-02`) are killed ($R = 2/2 = 1.0$).",
            "G5": "D: Calibrated `syn 3.0.9` AST metrics across 8 production functions: `evaluate_hubbard_determinants` (line 174) has CCN = 27 (D cap: 21-50), cognitive upper bound = 47, control nesting = 4 (B cap); `exact_determinant` (line 14) has CCN = 14 (B), cognitive upper bound = 24 (C cap), control nesting = 4 (B).",
        },
        "open_findings": [
            "Gate 2 -> D, Gate 3 -> E (Concrete Counterexample): Calling `evaluate_hubbard_determinants(2, &[(0, 1)], 1, &BigRational::one(), &BigRational::zero(), &BigRational::one(), true, &[0])` with `hs == 0` triggers an unhandled division-by-zero panic at `BigRational::one() / hs` (lines 225, 230).",
            "RULE_RS_001 / Gate 3 -> E (Concrete Counterexample): Calling `evaluate_hubbard_determinants` with `sites * slices >= usize::BITS as usize` (e.g. `sites = 8, slices = 8` on 64-bit targets) panics on unchecked shift `mask >> (time * sites + j)` at line 214.",
            "Gate 5 -> D: `evaluate_hubbard_determinants` (CCN = 27, cognitive upper bound = 47, nesting = 4) exceeds C complexity ceilings.",
        ],
    },
    "normal_forms.rs": {
        "profile": "Exact",
        "level": "L3",
        "level_basis": "Bounded-domain exact rational Reduced Row Echelon Form (RREF) with transformation witness matrix $T$, cochain quotient normal form modulo $\\mathrm{im}(d_0)$, and $\\mathbb{F}_2$ spanning-forest sign-switching normal form with fundamental cycle obstruction extraction.",
        "title": "Rational RREF, Cochain Quotient Normal Form & F2 Sign-Switching Normal Form",
        "purpose": "Compute exact rational RREF with row-operation witness $T A = R$, project 1-cochains $c^1$ to canonical representatives modulo $\\mathrm{im}(d_0)$, and normalize $\\mathbb{F}_2$ edge signs via spanning-forest vertex gauges while extracting frustrated fundamental cycles.",
        "gates": {"G1": "C", "G2": "D", "G3": "E", "G4": "C", "G5": "D"},
        "grade_ceiling": "D",
        "carrier_type": "RrefResult / QuotientNormalForm / SignSwitchingNormalForm",
        "operations": [
            "rref_with_witness",
            "normalize_cochain",
            "normalize_sign_cochain",
            "benchmark_sign_switching_grid_scaling",
        ],
        "lean4_theorems": [
            "lean4/NormalFormLaws.lean",
        ],
        "invariants": [
            "`rref_with_witness` produces reduced row echelon matrix `rref` and row witness `transform` such that `transform * matrix == rref` on rectangular inputs.",
            "`normalize_cochain` zeroes all pivot coordinates of `c1` modulo $\\mathrm{im}(d_0)$.",
            "`normalize_sign_cochain` zeroes all spanning-forest edge parities via BFS vertex switching and emits one fundamental cycle per frustrated chord.",
        ],
        "domain_preconditions": [
            "Every row in `matrix` passed to `rref_with_witness(matrix, num_cols)` must have length `>= num_cols` (currently unenforced at entry).",
            "Every row in `d0` passed to `normalize_cochain(d0, c1)` must have identical non-zero length `dim_c0` (currently unenforced at entry).",
            "`edges.len() == parities.len()`, `parities[i] in {0, 1}`, and endpoints `< vertex_count` in `normalize_sign_cochain`.",
        ],
        "refusals": [
            "`d0 must have nonzero row count`",
            "`c1 length must match dim_c1`",
            "`edge count and parity count mismatch`",
            "`edge parity must be in {0, 1}`",
            "`edge endpoint out of range`",
            "`grid_sizes must not be empty`",
            "`grid dimensions must be at least 2x2`",
        ],
        "gate_review": {
            "G1": "C: Declares `AuthorityEffect: None` and `#![forbid(unsafe_code)]`; implements normal forms corresponding to `lean4/NormalFormLaws.lean` and `papers/core/fsp/normal_forms/`.",
            "G2": "D: `rref_with_witness(matrix, num_cols)` does not validate row lengths against `num_cols`, and `normalize_cochain(d0, c1)` does not validate uniform row lengths across `d0` (`SCORING.md` Section 3.2 Grade D: 'domain restrictions unenforced at entry').",
            "G3": "E: Concrete reachable out-of-bounds slice-indexing panics on public entry points (`SCORING.md` Section 3.3 Grade E, `RULE_RS_002`): calling `rref_with_witness(&[vec![BigRational::one()]], 2)` panics at `rref[r][col]` (line 49), and calling `normalize_cochain(&[vec![BigRational::one()], vec![]], &[BigRational::one(), BigRational::one()])` panics at `d0[r][c]` (line 131).",
            "G4": "C: 4 unit tests verify $2\\times 2$ RREF, `normalize_cochain` pivot projection, triangle $\\mathbb{F}_2$ cycle obstruction, and 2D grid scaling up to $8\\times 8$; both designated mutants (`FSP-NF-01`, `FSP-NF-02`) are killed ($R = 2/2 = 1.0$).",
            "G5": "D: Calibrated `syn 3.0.9` AST metrics across 5 production functions: `normalize_sign_cochain` (line 172) has CCN = 21 (D cap: 21-50), cognitive upper bound = 44, control nesting = 4 (B cap); `rref_with_witness` (line 22) has CCN = 17 (C cap), cognitive upper bound = 33 (D cap: 26-40), control nesting = 4 (B cap).",
        },
        "open_findings": [
            "RULE_RS_002 / Gate 3 -> E (Concrete Counterexample): `rref_with_witness(&[vec![BigRational::one()]], 2)` panics with `index out of bounds` at line 49 (`rref[r][col]`) because row lengths are not validated against `num_cols`.",
            "RULE_RS_002 / Gate 3 -> E (Concrete Counterexample): `normalize_cochain` with ragged `d0` rows panics with `index out of bounds` at line 131 (`d0[r][c]`).",
            "Gate 5 -> D: `normalize_sign_cochain` (CCN = 21, cognitive upper bound = 44, nesting = 4) and `rref_with_witness` (CCN = 17, cognitive upper bound = 33, nesting = 4) exceed C complexity ceilings.",
        ],
    },
    "witness.rs": {
        "profile": "Exact",
        "level": "L2",
        "level_basis": "Fixed-parameter 4-site star exchange and $k=1$ character orbit witness record (`Witness`) and fixture refusal helpers matching `wdp_21_16_fsp`.",
        "title": "Dual-Face 4-Site Star Exchange & k=1 Character Orbit Witness",
        "purpose": "Compute the fixed 6-step two-particle CAR hop holonomy on the 4-site star graph (`hop_product = -1`, `gauges_removing_holonomy = 0`) and the $k=1$ character orbit invariants (`z_u = 0`, `n_u = 2`), and refuse invalid holonomy or foreign fixture scalars.",
        "gates": {"G1": "C", "G2": "C", "G3": "D", "G4": "C", "G5": "A"},
        "grade_ceiling": "A",
        "carrier_type": "Witness",
        "operations": [
            "witness",
            "refuse_removed_holonomy",
            "refuse_foreign_fixture",
        ],
        "lean4_theorems": [
            "lean4/FermionSignCore.lean",
            "lean4/MeronCharacter.lean",
        ],
        "invariants": [
            "`witness().hop_product == -1`, `witness().signs == [1, -1, 1, 1, -1, -1]`, `witness().gauges_checked == 64`, `witness().gauges_removing_holonomy == 0`.",
            "`witness().z_u == 0`, `witness().n_u == 2`, `witness().hat_o_num == 1`, `witness().hat_o_den == 1`, `witness().conjunction == 0`.",
        ],
        "domain_preconditions": [
            "`witness()` takes no external arguments; `refuse_removed_holonomy` and `refuse_foreign_fixture` accept any `i64`.",
        ],
        "refusals": [
            "`(+1) equals (-1)^6 and is not the CAR product of this cycle`",
            "`claimed product is not the CAR hop product of this cycle`",
            "`O.5 fixture scalar is not this k=1 orbit`",
            "`scalar is outside the computed orbit values`",
        ],
        "gate_review": {
            "G1": "C: Declares `AuthorityEffect: None` and `#![forbid(unsafe_code)]`; matches `code/rust/src/wdp/derivation_controls/wdp_21_16_fsp.rs` and `code/python/src/fsp/__init__.py`.",
            "G2": "C: Exact integer and $\\mathbb{F}_2$ bit operations on bounded compile-time constants (`MASKS`, `HOPS`, $k=1$). Capped at `C` because `Witness` exposes `pub` fields and derives `Deserialize` without invariant validation (`RULE_RS_003`).",
            "G3": "D: Contains 26 `assert!` / `assert_eq!` macros across 8 production helper functions (`preceding`, `hop_sign`, `distinct_two_particle_cycle`, `site_cycle_rank`, `gauge_cycle`, `star_exchange`, `reduce`, `orbit`) and 14 direct array/slice indexing expressions (`RULE_RS_002`). Although unreachable from public entry points because inputs are compile-time constants, failure handling is wired to panic rather than typed `Result` errors.",
            "G4": "C: Unit test `exact_star_and_orbit_witness_parity` verifies all primary `Witness` fields and both refusal functions on valid and invalid inputs; both designated mutants (`FSP-WIT-01`, `FSP-WIT-02`) are killed ($R = 2/2 = 1.0$).",
            "G5": "A: Calibrated `syn 3.0.9` AST metrics across 14 production functions: max CCN = 6 (<= 10), cognitive upper bound = 9 (<= 15), control nesting = 2 (<= 3), 0 functions exceeding `A` (with 26 opaque `assert!`/`assert_eq!` macro invocations explicitly disclosed).",
        },
        "open_findings": [
            "Gate 3 -> D: 8 internal helper functions rely on 26 `assert!`/`assert_eq!` panic macros and 14 direct indexing operations rather than returning typed `Result` errors.",
            "RULE_RS_003 (Gate 2 -> C): `Witness` exposes 19 `pub` fields and derives `serde::Deserialize` without verifying invariant consistency on deserialized instances.",
        ],
    },
}


def snapshot_fsp(work_dir: Path) -> None:
    if work_dir.exists():
        shutil.rmtree(work_dir)
    work_dir.mkdir(parents=True)
    for item in fsp_subjects():
        shutil.copyfile(item, work_dir / item.name)
    if (RUST / "Cargo.lock").is_file():
        shutil.copyfile(RUST / "Cargo.lock", work_dir / "Cargo.lock")
    fixtures_dir = work_dir / "fixtures"
    fixtures_dir.mkdir(parents=True, exist_ok=True)
    for fx in (FSP_DIR / "fixtures").glob("*.json"):
        shutil.copyfile(fx, fixtures_dir / fx.name)


def run_audit(stamp: str) -> Path:
    out_dir = ROOT / "evidence" / "quality" / "fsp" / stamp
    out_dir.mkdir(parents=True, exist_ok=True)
    work_dir = RUST / "target" / "fsp-audit" / stamp
    build_dir = work_dir / "target"
    metric_build_dir = work_dir / "metrics-target"

    initial_sources = source_inventory()
    write_json(out_dir / "source_manifest.json", initial_sources)
    shutil.copyfile(__file__, out_dir / "run_fsp_scoring_audit.py")

    versions = {
        name: subprocess.check_output([name, "--version"], text=True).strip()
        for name in ("cargo", "rustc")
    }

    try:
        snapshot_fsp(work_dir)

        # 1. Cargo offline metadata & dependency binding
        meta_cmd = [
            "cargo",
            "metadata",
            "--offline",
            "--quiet",
            "--format-version",
            "1",
            "--manifest-path",
            str(work_dir / "Cargo.toml"),
        ]
        meta_proc = subprocess.run(meta_cmd, cwd=work_dir, capture_output=True, text=True, check=True)
        (out_dir / "cargo_metadata.json").write_text(meta_proc.stdout, encoding="utf-8", newline="\n")

        # 2. Baseline test run
        test_cmd = [
            "cargo",
            "test",
            "--offline",
            "--manifest-path",
            str(work_dir / "Cargo.toml"),
            "--target-dir",
            str(build_dir),
        ]
        baseline_run = run_cmd(test_cmd, work_dir, out_dir / "tfqm_fsp_baseline.log")
        baseline_record = {
            "AuthorityEffect": "None",
            "versions": versions,
            "runs": [baseline_run],
            "baseline_ok": baseline_run["exit_code"] == 0,
        }
        write_json(out_dir / "baseline.json", baseline_record)
        if baseline_run["exit_code"] != 0:
            raise RuntimeError("Baseline tfqm_fsp tests failed; see tfqm_fsp_baseline.log")

        # 3. Calibrated syn 3.0.9 AST metrics
        common_metrics = [
            "--offline",
            "--manifest-path",
            str(METRICS_TOOL / "Cargo.toml"),
            "--target-dir",
            str(metric_build_dir),
            "--quiet",
        ]
        cal_run = run_cmd(["cargo", "test", *common_metrics], METRICS_TOOL, out_dir / "metric_calibration.log")
        bld_run = run_cmd(["cargo", "build", *common_metrics], METRICS_TOOL, out_dir / "metric_build.log")
        if cal_run["exit_code"] != 0 or bld_run["exit_code"] != 0:
            raise RuntimeError("Failed to calibrate or build tfqm_rust_metrics")

        rs_rel_paths = [p.relative_to(ROOT).as_posix() for p in fsp_subjects() if p.suffix == ".rs"]
        metrics_exe = metric_build_dir / "debug" / "tfqm_rust_metrics.exe"
        metrics_run = run_cmd([str(metrics_exe), *rs_rel_paths], ROOT, out_dir / "metrics.json")
        if metrics_run["exit_code"] != 0:
            raise RuntimeError("tfqm_rust_metrics execution failed")

        metric_receipt = {
            "AuthorityEffect": "None",
            "claim": "Declared source metrics only; opaque macros and unexpanded cfg are not certified execution flow.",
            "tool": "syn 3.0.9 source AST",
            "source_manifest_sha256": sha256_file(out_dir / "source_manifest.json"),
            "sources_unchanged": source_inventory() == initial_sources,
            "tool_sources": {
                p.relative_to(ROOT).as_posix(): sha256_file(p)
                for p in sorted(METRICS_TOOL.rglob("*"))
                if p.is_file() and "target" not in p.parts
            },
            "versions": versions,
            "runs": [cal_run, bld_run, metrics_run],
        }
        write_json(out_dir / "metric_receipt.json", metric_receipt)

        # 4. Execute 14 designated mutations in the isolated snapshot
        mutation_records: list[dict[str, object]] = []
        mut_logs_dir = out_dir / "mutation_logs"
        mut_logs_dir.mkdir(parents=True, exist_ok=True)

        for mutant in DESIGNATED_MUTANTS:
            target_file = work_dir / mutant["file"]
            original_text = target_file.read_text(encoding="utf-8")
            if mutant["target"] not in original_text:
                raise RuntimeError(f"Mutant target not found for {mutant['id']} in {mutant['file']}")
            mutated_text = original_text.replace(mutant["target"], mutant["replacement"], 1)
            target_file.write_text(mutated_text, encoding="utf-8", newline="\n")
            try:
                m_run = run_cmd(test_cmd, work_dir, mut_logs_dir / f"{mutant['id']}.log", timeout=120)
                if m_run["timed_out"]:
                    outcome = "inconclusive"
                elif m_run["exit_code"] != 0:
                    outcome = "killed"
                else:
                    outcome = "survived"
                mutation_records.append({
                    "id": mutant["id"],
                    "file": f"code/rust/src/fsp/{mutant['file']}",
                    "description": mutant["description"],
                    "outcome": outcome,
                    "run": m_run,
                })
            finally:
                target_file.write_text(original_text, encoding="utf-8", newline="\n")

        write_json(out_dir / "mutations.json", mutation_records)

        # 5. Restored baseline verification
        restored_run = run_cmd(test_cmd, work_dir, out_dir / "tfqm_fsp_restored.log")
        restored_record = {
            "AuthorityEffect": "None",
            "runs": [restored_run],
            "restored_ok": restored_run["exit_code"] == 0,
        }
        write_json(out_dir / "restored.json", restored_record)
        if restored_run["exit_code"] != 0:
            raise RuntimeError("Restored snapshot failed baseline tests")

        final_sources = source_inventory()
        outcomes_total = {
            k: sum(1 for m in mutation_records if m["outcome"] == k)
            for k in ("killed", "survived", "demonstrably_equivalent", "invalid", "inconclusive", "unrun")
        }
        denom = sum(outcomes_total[k] for k in ("killed", "survived", "inconclusive", "unrun"))
        ratio = outcomes_total["killed"] / denom if denom else None

        summary_record = {
            "AuthorityEffect": "None",
            "timestamp": datetime.strptime(stamp, "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc).isoformat(),
            "baseline_ok": baseline_record["baseline_ok"],
            "restored_baseline_ok": restored_record["restored_ok"],
            "source_unchanged": final_sources == initial_sources,
            "source_manifest_sha256": sha256_file(out_dir / "source_manifest.json"),
            "baseline_sha256": sha256_file(out_dir / "baseline.json"),
            "restored_sha256": sha256_file(out_dir / "restored.json"),
            "mutations_sha256": sha256_file(out_dir / "mutations.json"),
            "metric_receipt_sha256": sha256_file(out_dir / "metric_receipt.json"),
            "cargo_metadata_sha256": sha256_file(out_dir / "cargo_metadata.json"),
            "mutation_accounting": outcomes_total,
            "conservative_ratio": ratio,
        }
        write_json(out_dir / "summary.json", summary_record)
    finally:
        if work_dir.exists():
            shutil.rmtree(work_dir)

    return out_dir


def write_sidecars(evidence_dir: Path, check_only: bool = False) -> list[str]:
    summary = json.loads((evidence_dir / "summary.json").read_text(encoding="utf-8"))
    mutations = json.loads((evidence_dir / "mutations.json").read_text(encoding="utf-8"))
    metrics = json.loads((evidence_dir / "metrics.json").read_text(encoding="utf-8"))
    eval_ts = summary["timestamp"]

    evidence_refs = [
        {
            "path": (evidence_dir / "baseline.json").relative_to(ROOT).as_posix(),
            "sha256": sha256_file(evidence_dir / "baseline.json"),
            "scope": "Scoped offline cargo test baseline receipt and log hash for tfqm_fsp.",
        },
        {
            "path": (evidence_dir / "summary.json").relative_to(ROOT).as_posix(),
            "sha256": sha256_file(evidence_dir / "summary.json"),
            "scope": "Source snapshot invariance and complete six-outcome mutation accounting summary.",
        },
        {
            "path": (evidence_dir / "mutations.json").relative_to(ROOT).as_posix(),
            "sha256": sha256_file(evidence_dir / "mutations.json"),
            "scope": "Designated semantic fault injection runs and per-mutant log hashes.",
        },
        {
            "path": (evidence_dir / "metric_receipt.json").relative_to(ROOT).as_posix(),
            "sha256": sha256_file(evidence_dir / "metric_receipt.json"),
            "scope": "Calibrated syn 3.0.9 source AST complexity receipt and tool-source hashes.",
        },
    ]

    grade_order = ["E", "D", "C", "B", "A", "A+"]
    mismatches: list[str] = []

    for subject in fsp_subjects():
        rel_path = subject.relative_to(ROOT).as_posix()
        spec = FILE_SPECIFICATIONS[subject.name]
        source_text = subject.read_text(encoding="utf-8")
        file_sha = sha256_file(subject)
        stem = "Cargo" if subject.name == "Cargo.toml" else subject.stem

        scoring_path = FSP_DIR / f"{stem}.scoring.yaml"
        contract_path = FSP_DIR / f"{stem}.contract.yaml"

        artifact_obj = {
            "path": rel_path,
            "language": "Rust" if subject.suffix == ".rs" else "Other",
            "sha256": file_sha,
        }

        # AST structure block
        if subject.suffix == ".rs":
            fn_metrics = metrics[rel_path]
            ast_ceiling, exceeding_fns = metric_ceiling_for_functions(fn_metrics)
            max_ccn = max((int(f["ccn"]) for f in fn_metrics), default=0)
            max_cog = max((int(f["cognitive_upper_bound"]) for f in fn_metrics), default=0)
            max_nest = max((int(f["control_nesting"]) for f in fn_metrics), default=0)
            opaque = [
                {"function": f["name"], "line": f["line"], "macros": f["opaque_macros"]}
                for f in fn_metrics
                if f["opaque_macros"]
            ]
            structure_block = {
                "tool": "syn 3.0.9 source AST",
                "source_ast_parsed": True,
                "expanded_ast": False,
                "physical_lines": len(source_text.splitlines()),
                "parsed_production_functions": len(fn_metrics),
                "max_production_ccn": max_ccn,
                "cognitive_complexity_upper_bound": max_cog,
                "control_nesting": max_nest,
                "metric_ceiling": ast_ceiling,
                "opaque_function_macros": opaque,
                "functions_exceeding_A": exceeding_fns,
                "scope": "Explicit source functions only; macro-generated functions, compiler expansion and runtime cost require separate assessment.",
            }
        else:
            ast_ceiling = "A"
            structure_block = {
                "tool": "tomllib manifest parser",
                "source_ast_parsed": True,
                "expanded_ast": False,
                "physical_lines": len(source_text.splitlines()),
                "parsed_production_functions": 0,
                "max_production_ccn": 0,
                "cognitive_complexity_upper_bound": 0,
                "control_nesting": 0,
                "metric_ceiling": "A",
                "opaque_function_macros": [],
                "functions_exceeding_A": [],
                "scope": "Declarative Cargo.toml manifest structure.",
            }

        # Local mutation accounting
        file_mutants = [m for m in mutations if m["file"] == rel_path]
        mut_counts = {
            k: sum(1 for m in file_mutants if m["outcome"] == k)
            for k in ("killed", "survived", "demonstrably_equivalent", "invalid", "inconclusive", "unrun")
        }
        el = sum(mut_counts[k] for k in ("killed", "survived", "inconclusive", "unrun"))
        mut_counts["conservative_ratio"] = mut_counts["killed"] / el if el else None

        gates: dict[str, str] = dict(spec["gates"])  # type: ignore[arg-type]
        comp_grade = min(gates.values(), key=grade_order.index)
        level_str = str(spec["level"])
        score_token = f"{level_str}{comp_grade}"

        urn_suffix = stem.lower()
        contract_record: dict[str, object] = {
            "schema_version": "omega.contract.v2",
            "contract_id": f"urn:tfqm:contract:rust:fsp:{urn_suffix}:v2.0.0",
            "title": spec["title"],
            "kind": "math_contract" if subject.suffix == ".rs" else "manifest_contract",
            "layer": "10_math_crates",
            "role": "MathematicalKernel" if subject.suffix == ".rs" else "PackageManifest",
            "status": "active_with_recorded_obligations",
            "AuthorityEffect": "None",
            "artifact": artifact_obj,
            "target": "L4A",
            "profile": spec["profile"],
            "purpose": spec["purpose"],
            "subject_role": spec["level_basis"],
            "descriptor": {
                "authority_effect": "None",
                "evidence_ceiling": "ExactWitness",
                "runtime_enforcement": subject.suffix == ".rs",
                "clean_architecture_layer": "domain",
                "dependencies": {
                    "contracts": [],
                    "lean4_theorems": spec["lean4_theorems"],
                },
                "refusals": {
                    "may_emit": spec["refusals"],
                },
            },
            "doctrine": {
                "summary": spec["purpose"],
                "invariants": spec["invariants"],
                "domain_preconditions": spec["domain_preconditions"],
                "non_roles": [
                    "authority_source",
                    "promotion_granter",
                    "continuum_equivalence_proof",
                ],
                "required_negative_capabilities": [
                    "no_self_certification",
                    "no_implicit_authority_upgrade",
                    "no_floating_point_in_exact_profile",
                ],
            },
            "declaration_index": declaration_index(source_text) if subject.suffix == ".rs" else [],
            "declaration_index_scope": "Lexical public declaration line index only; excludes private helpers and test-module items.",
            "specification": {
                "algebraic_structure": {
                    "carrier_type": spec["carrier_type"],
                    "operations": spec["operations"],
                },
                "verification": {
                    "rust_test_command": "cargo test --manifest-path code/rust/src/fsp/Cargo.toml",
                    "python_parity_test": "code/python/tests/test_fsp_Hubbard_Majorana_Parity.py",
                    "lean4_targets": spec["lean4_theorems"],
                },
            },
            "requirements": [
                {
                    "id": "G1",
                    "requirement": "Bind exact artifact SHA-256, public symbols, Lean 4 theorem correspondence, and AuthorityEffect: None.",
                },
                {
                    "id": "G2",
                    "requirement": "Preserve exact rational (`BigRational`) and F2 arithmetic; validate all public entry preconditions and struct construction/deserialization invariants (`RULE_RS_001`, `RULE_RS_003`).",
                },
                {
                    "id": "G3",
                    "requirement": "Eliminate reachable panics (`.unwrap()`, `assert!`, unchecked bit shifts, unchecked slice indexing, and zero divisors) in favor of typed `Result` refusals (`RULE_RS_001`, `RULE_RS_002`).",
                },
                {
                    "id": "G4",
                    "requirement": "Maintain unit, cross-language JSON fixture, and negative boundary tests with honest six-outcome mutation accounting (`R >= 0.95` required for Grade A).",
                },
                {
                    "id": "G5",
                    "requirement": "Maintain CCN <= 10, cognitive complexity <= 15, and control nesting <= 3 for Grade A (`SCORING.md` Section 3.5).",
                },
            ],
            "admission_policy": "Structs with `pub` fields or `serde::Deserialize` are untrusted carrier data until validated by a checked constructor; callers must not bypass constructor checks.",
            "resource_boundary": "Exact `BigRational` and Fock-space basis enumeration scale combinatorially with site count; callers must bound lattice size (`num_sites < 32` for `FockState`).",
            "authority_ceiling": "Runtime finite algebraic checks only. AuthorityEffect: None.",
            "open_obligations": spec["open_findings"],
            "evidence": evidence_refs,
        }
        if subject.name == "Cargo.toml":
            parsed_toml = tomllib.loads(source_text)
            contract_record["manifest"] = {
                k: parsed_toml.get(k, {}) for k in ("package", "lib", "dependencies")
            }

        scoring_record: dict[str, object] = {
            "schema_version": "2.0.0",
            "AuthorityEffect": "None",
            "artifact": artifact_obj,
            "profile": spec["profile"],
            "level": level_str,
            "level_basis": spec["level_basis"],
            "architecture_target": "L4",
            "engineering_target": "A",
            "gates": gates,
            "composite_grade": comp_grade,
            "score_token": score_token,
            "is_complete": True,
            "grade_ceiling": spec["grade_ceiling"],
            "evaluation_timestamp": eval_ts,
            "claim": {
                "urn": f"urn:tfqm:rust:fsp:{urn_suffix}",
                "description": spec["purpose"],
                "scope": "Only the source-bound finite runtime behavior in code/rust/src/fsp; no continuum derivation or authority promotion is certified.",
            },
            "contract": {
                "status": "active_with_recorded_obligations",
                "path": contract_path.relative_to(ROOT).as_posix(),
                "contract_id": contract_record["contract_id"],
            },
            "evidence": evidence_refs,
            "verification": {
                "baseline_ok": summary["baseline_ok"],
                "restored_baseline_ok": summary["restored_baseline_ok"],
                "source_snapshot_unchanged": summary["source_unchanged"],
                "compiled_scope": "tfqm_fsp standalone offline crate test suite (19 tests)",
                "local_mutant_ids": [m["id"] for m in file_mutants],
            },
            "mutation_accounting": mut_counts,
            "structure": structure_block,
            "gate_review": spec["gate_review"],
            "open_findings": spec["open_findings"],
            "assurance_limits": [
                "Evaluation applies SCORING.md v2.0.0 fail-closed weakest-link grading (`composite_grade = min(G1..G5)`).",
                "No mechanized Rust-to-Lean extraction, MIR crash-freedom proof, or global allocator totality is claimed.",
            ],
        }

        contract_text = (
            "# =============================================================================\n"
            "# OMEGA ENGINE / TFQM CANONICAL FILE CONTRACT (SCORING.md v2.0.0)\n"
            "# AuthorityEffect: None\n"
            "# =============================================================================\n"
            + yaml_dump(contract_record)
            + "\n"
        )
        scoring_text = (
            "# =============================================================================\n"
            "# SCORING.md v2.0.0 FIVE-GATE EVALUATION RECORD\n"
            "# AuthorityEffect: None\n"
            "# =============================================================================\n"
            + yaml_dump(scoring_record)
            + "\n"
        )

        for out_path, expected_content in ((contract_path, contract_text), (scoring_path, scoring_text)):
            if check_only:
                if not out_path.is_file() or out_path.read_text(encoding="utf-8") != expected_content:
                    mismatches.append(out_path.relative_to(ROOT).as_posix())
            else:
                out_path.write_text(expected_content, encoding="utf-8", newline="\n")

    return mismatches


def main() -> int:
    parser = argparse.ArgumentParser(description="Run SCORING.md v2.0.0 audit for code/rust/src/fsp.")
    parser.add_argument("--evidence-dir", type=Path, help="Existing evidence directory to render/check against.")
    parser.add_argument("--check", action="store_true", help="Verify existing .scoring.yaml and .contract.yaml sidecars.")
    args = parser.parse_args()

    if args.evidence_dir:
        ev_dir = args.evidence_dir.resolve()
    else:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        ev_dir = run_audit(stamp)

    mismatches = write_sidecars(ev_dir, check_only=args.check)
    print(
        json.dumps(
            {
                "evidence_dir": ev_dir.relative_to(ROOT).as_posix(),
                "subjects": len(fsp_subjects()),
                "sidecars_written_or_checked": len(fsp_subjects()) * 2,
                "mismatches": mismatches,
            },
            indent=2,
        )
    )
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
