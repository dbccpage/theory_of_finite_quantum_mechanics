from __future__ import annotations
"""Python mirror of the Rust omega_contracts source file.

This module provides executable Python QA for packet coverage over the workspace.
"""


import json
from pathlib import Path
from typing import Set

RUST_SOURCE_PATH = "tests/packet_coverage_test.rs"
RUST_SOURCE_SHA256 = "fed4882a495cd8033bcbccb98aa1200634a2ee0728ea1325a49c8505d02ab396"
PORT_STATUS = "python_port_active"

UNGOVERNED = {
    "crates/constants",
    "crates/omega_topology",
    "crates/omega_sheaf_theory",
    "crates/omega_linear_algebra",
    "crates/omega_contract_core",
    "crates/omega_types",
    "crates/omega_contracts",
    "crates/omega_representation",
    "crates/omega_trace",
    "crates/omega_replay",
    "crates/omega_operator_algebra",
    "crates/omega_id_run",
    "crates/omega_solvers",
    "crates/omega_search",
    "crates/omega_engines",
    "crates/omega_homological",
    "crates/omega_measurement",
    "crates/omega_higher_category_theory",
    "crates/omega_homotopy_type_theory",
    "crates/omega_state",
    "crates/omega_functional",
    "crates/omega_epk",
    "crates/omega_certifiers",
    "crates/omega_governance",
    "crates/omega_self_review",
    "crates/omega_operator_candidates",
    "crates/omega_lifts",
    "crates/omega_category_theory",
    "crates/omega_llm_gateway",
    "crates/omega_pipelines",
    "crates/omega_engine_agents/conductor",
    "crates/omega_atlas_reconciliation",
    "crates/omega_conductor",
    "crates/omega_q",
    "crates/omega_mub",
    "crates/omega_rip_papers_runtime",
    "crates/omega_agent_registry",
    "omega_layer_applications/omega_sweeper_fast",
    "omega_layer_applications/omega_proofer",
    "omega_facade",
    "omega_business_contracts",
    "omega_layer_applications",
    "omega_layer_infrastructure",
    "crates/omega_maintenance",
    "omega_layer_applications/omega_ops",
}


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent.parent


def workspace_members(root: Path) -> Set[str]:
    manifest_path = root / "omega_engine" / "Cargo.toml"
    if not manifest_path.exists():
        return set()
    text = manifest_path.read_text(encoding="utf-8")
    if "members = [" not in text:
        return set()
    block = text.split("members = [")[1].split("]")[0]
    members = set()
    for line in block.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        for part in line.split(","):
            part = part.strip().strip('"').strip("'").rstrip("/")
            if part:
                members.add(part)
    return members


def registry_prefixes(root: Path) -> Set[str]:
    reg_path = root / "scripts" / "packet_registry.json"
    if not reg_path.exists():
        return set()
    data = json.loads(reg_path.read_text(encoding="utf-8"))
    mappings = data.get("mappings", [])
    prefixes = set()
    for m in mappings:
        prefix = m.get("prefix", "")
        if prefix.startswith("omega_engine/"):
            prefix = prefix[len("omega_engine/") :]
        prefixes.add(prefix.rstrip("/"))
    return prefixes


def is_fully_governed(member: str, prefixes: Set[str]) -> bool:
    m = member.rstrip("/")
    for p in prefixes:
        p_clean = p.rstrip("/")
        if m == p_clean or m.startswith(p_clean + "/"):
            return True
    return False


def test_all_workspace_crates_mapped() -> None:
    root = repo_root()
    members = workspace_members(root)
    if not members:
        return
    prefixes = registry_prefixes(root)
    for m in members:
        governed = is_fully_governed(m, prefixes)
        in_ungoverned = m in UNGOVERNED
        assert governed or in_ungoverned, (
            f"Workspace member '{m}' is neither governed by packet_registry.json nor listed in UNGOVERNED"
        )


def test_registry_prefixes_and_packets_exist() -> None:
    root = repo_root()
    reg_path = root / "scripts" / "packet_registry.json"
    if not reg_path.exists():
        return
    data = json.loads(reg_path.read_text(encoding="utf-8"))
    for m in data.get("mappings", []):
        prefix = m.get("prefix", "")
        packet = m.get("packet", "")
        assert (root / prefix).exists() or (root / "omega_engine" / prefix).exists(), (
            f"Prefix target {prefix} does not exist"
        )
        packet_path = root / data["packet_home"] / packet
        assert packet_path.exists(), f"Packet {packet} does not exist at {packet_path}"


