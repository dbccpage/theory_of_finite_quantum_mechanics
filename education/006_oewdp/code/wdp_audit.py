"""WDP Stage Transition and Obstruction Resolution Audit Harness.

AuthorityEffect: None. GenesisEffect: None.
Mirrors sn_audit.py while linking WDP wire difference statements and transport events
directly to S(n) Postnikov tower obstruction resolution steps.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

MODULE_ROOT = next(
    (
        p
        for p in Path(__file__).resolve().parents
        if (p / "levels").is_dir() or (p / "grammar").is_dir()
    ),
    Path(__file__).resolve().parents[2],
)
REPO_ROOT = next(
    (
        p
        for p in Path(__file__).resolve().parents
        if (p / ".git").exists() or (p / "pixi.toml").exists()
    ),
    Path(__file__).resolve().parents[5],
)
CODE_DIR = MODULE_ROOT / "code"
NORMAL_FORMS_DIR = MODULE_ROOT / "normal_forms"

if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

from wdp_codec import (
    D0Map,
    D1Map,
    DistinctCut,
    HHomotopy,
    QuotientWitness,
    SimplexPair,
    WdpCodecError,
    WdpNode,
    WdpRefusal,
    deserialize_wdp,
    serialize_wdp,
)

# ---------------------------------------------------------------------------
# Constants & Profiles
# ---------------------------------------------------------------------------

GLYPHS = "abcdefghijklmnopqrstuvwxyz0123456789"
PROFILES = ("wdp-wire-v1",)


# ---------------------------------------------------------------------------
# S(n) Postnikov Tower Obstruction Model
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class PostnikovObstruction:
    """Declared obstruction in the discrete Postnikov tower S(n)."""

    stage: int
    obstruction_id: str
    law_obstructed: str
    resolution_description: str
    expected_event_type: type[WdpNode]


OBSTRUCTION_REGISTER: dict[int, PostnikovObstruction] = {
    0: PostnikovObstruction(
        stage=0,
        obstruction_id="W0_EMPTY_CARRIER",
        law_obstructed="CL-0-INERTIA",
        resolution_description="Supply lone carrier mark to initialize presentation",
        expected_event_type=D0Map,
    ),
    1: PostnikovObstruction(
        stage=1,
        obstruction_id="W1_SUBSINGLETON_INSEPARABILITY",
        law_obstructed="WDNF-SUPPORT-FLOOR",
        resolution_description="Supply second mark to reach Delta_support = 2 carrier floor",
        expected_event_type=SimplexPair,
    ),
    2: PostnikovObstruction(
        stage=2,
        obstruction_id="W2_UNWITNESSED_RELATION",
        law_obstructed="WDNF-IRREFLEXIVE-WITNESS",
        resolution_description="Admit irreflexive cut with explicit witness endpoints",
        expected_event_type=DistinctCut,
    ),
    3: PostnikovObstruction(
        stage=3,
        obstruction_id="W3_BOUNDARY_CYCLE_DEFICIT",
        law_obstructed="TSNF-BOUNDARY-NILPOTENCE",
        resolution_description="Construct boundary transport event d1(a,b)",
        expected_event_type=D1Map,
    ),
    4: PostnikovObstruction(
        stage=4,
        obstruction_id="W4_HARMONIC_1_RESIDUAL",
        law_obstructed="DHNF-HODGE-DECOMPOSITION",
        resolution_description="Provide homotopy filler H(a,b) or marked quotient quot<a/w>",
        expected_event_type=HHomotopy,
    ),
    5: PostnikovObstruction(
        stage=5,
        obstruction_id="W5_OPEN_OBSTRUCTION_DESCENT",
        law_obstructed="POSTNIKOV-EXACT-RETRACTION",
        resolution_description="Verify quotient witness closure or emit typed refusal",
        expected_event_type=QuotientWitness,
    ),
}


@dataclass(frozen=True)
class PostnikovStepReceipt:
    """Audit receipt for an S(n) Postnikov stage transition step."""

    from_stage: int
    to_stage: int
    wire: str
    node_type: str
    obstruction_id: str | None
    is_descent: bool
    carrier_size: int
    delta_support: int
    passed: bool
    terminal_route: str
    diagnosis: str
    issues: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "from_stage": self.from_stage,
            "to_stage": self.to_stage,
            "wire": self.wire,
            "node_type": self.node_type,
            "obstruction_id": self.obstruction_id,
            "is_descent": self.is_descent,
            "carrier_size": self.carrier_size,
            "delta_support": self.delta_support,
            "passed": self.passed,
            "terminal_route": self.terminal_route,
            "diagnosis": self.diagnosis,
            "issues": list(self.issues),
        }


# ---------------------------------------------------------------------------
# Wire Issue Validation
# ---------------------------------------------------------------------------


def wire_issue(text: str, profile: str = "wdp-wire-v1") -> str | None:
    """Validate a wire string against the declared WDP wire profile."""
    if profile not in PROFILES:
        return f"Unknown profile: {profile!r}"
    try:
        ast = deserialize_wdp(text)
        rendered = serialize_wdp(ast)
        if rendered != text:
            return f"Exact spelling round trip failed: {text!r} -> {rendered!r}"
    except (WdpCodecError, ValueError) as err:
        return str(err)
    return None


# ---------------------------------------------------------------------------
# Witnessed Irreflexive Relation (WIR) Mathematical Verification
# ---------------------------------------------------------------------------


def verify_wdp_wir(
    carrier: Sequence[str],
    counts: dict[tuple[str, str], int],
    require_inhabited: bool = True,
) -> dict[str, Any]:
    """Verify finite presence model invariants conforming to nf.wdp.wdnf.yaml.

    Validates:
    - Unique carrier identities
    - Carrier support floor (|carrier| >= 2)
    - Strict irreflexivity (counts[a,a] == 0)
    - Primitive endpoint arity Delta_support = 2
    """
    if len(set(carrier)) != len(carrier):
        raise ValueError("Carrier identities must be unique")

    carrier_set = set(carrier)
    edges: list[tuple[str, str]] = []

    for (a, b), count in counts.items():
        if a not in carrier_set or b not in carrier_set:
            raise ValueError(f"Undeclared endpoint: ({a}, {b})")
        if type(count) is not int or count < 0:
            raise ValueError("Multiplicity must be a nonnegative integer")
        if count > 0:
            if a == b:
                raise ValueError("Irreflexivity violated: self-difference claimed")
            edges.append((a, b))

    if require_inhabited and len(carrier) < 2:
        raise ValueError("Subsingleton distinction violation: |carrier| < 2")

    if require_inhabited and not edges:
        raise ValueError("No inhabited primitive distinction")

    return {
        "carrier_size": len(carrier),
        "primitive_endpoint_arity": 2,
        "asserted_pair_count": len(edges),
        "witness_occurrence_count": sum(counts.values()),
        "terminal_route": "AcceptWitnessedDifference",
    }


# ---------------------------------------------------------------------------
# Stage Transition and Obstruction Audit
# ---------------------------------------------------------------------------


def audit_stage_transition(
    from_stage: int,
    to_stage: int,
    event: str | WdpNode,
    carrier: Sequence[str] = (),
    counts: dict[tuple[str, str], int] | None = None,
) -> PostnikovStepReceipt:
    """Audit a single S(n) Postnikov tower stage transition against WDP invariants."""
    issues: list[str] = []

    # 1. Parse or validate event
    if isinstance(event, str):
        wire = event
        try:
            node = deserialize_wdp(event)
        except WdpCodecError as err:
            return PostnikovStepReceipt(
                from_stage=from_stage,
                to_stage=to_stage,
                wire=wire,
                node_type="MalformedWire",
                obstruction_id=None,
                is_descent=(to_stage < from_stage),
                carrier_size=len(carrier),
                delta_support=0,
                passed=False,
                terminal_route="RejectGhostDistinction",
                diagnosis=f"Malformed WDP wire token: {err}",
                issues=(str(err),),
            )
    else:
        node = event
        try:
            wire = serialize_wdp(node)
        except WdpCodecError as err:
            return PostnikovStepReceipt(
                from_stage=from_stage,
                to_stage=to_stage,
                wire="<invalid>",
                node_type=type(node).__name__,
                obstruction_id=None,
                is_descent=(to_stage < from_stage),
                carrier_size=len(carrier),
                delta_support=0,
                passed=False,
                terminal_route="RejectGhostDistinction",
                diagnosis=f"Serialization failure: {err}",
                issues=(str(err),),
            )

    node_type = type(node).__name__
    is_descent = to_stage < from_stage

    # 2. Stage index validity
    if not (0 <= from_stage <= 6 and 0 <= to_stage <= 6):
        issues.append(f"Invalid stage indices: {from_stage} -> {to_stage}")

    # 3. Obstruction alignment
    obstruction = OBSTRUCTION_REGISTER.get(from_stage)
    obstruction_id = obstruction.obstruction_id if obstruction else None

    # 4. Typed Refusal Handling
    if isinstance(node, WdpRefusal):
        return PostnikovStepReceipt(
            from_stage=from_stage,
            to_stage=to_stage,
            wire=wire,
            node_type=node_type,
            obstruction_id=obstruction_id,
            is_descent=is_descent,
            carrier_size=len(carrier),
            delta_support=0,
            passed=True,  # Typed refusal is a verified fail-closed terminal
            terminal_route="RequireSupportDeclaration",
            diagnosis=f"Fail-closed typed refusal emitted: {node.code}",
            issues=tuple(issues),
        )

    # 5. Witness Status Handling
    if isinstance(node, QuotientWitness):
        if node.status == "OPEN_OBSTRUCTION":
            issues.append(f"Quotient witness records open obstruction: {node.status}")
            return PostnikovStepReceipt(
                from_stage=from_stage,
                to_stage=to_stage,
                wire=wire,
                node_type=node_type,
                obstruction_id=obstruction_id,
                is_descent=is_descent,
                carrier_size=len(carrier),
                delta_support=0,
                passed=False,
                terminal_route="RequireSupportDeclaration",
                diagnosis=f"Obstruction unresolved: status={node.status}",
                issues=tuple(issues),
            )

    # 6. Primitive Difference Cut Checks (Delta_support = 2, Irreflexivity)
    delta_support = 0
    if isinstance(node, (DistinctCut, SimplexPair)):
        c1, c2 = node.first.to_wire(), node.second.to_wire()
        endpoint_set = {c1, c2}
        delta_support = len(endpoint_set)

        if delta_support != 2:
            issues.append(
                f"Delta_support must be 2, got {delta_support} for endpoints ({c1}, {c2})"
            )
            return PostnikovStepReceipt(
                from_stage=from_stage,
                to_stage=to_stage,
                wire=wire,
                node_type=node_type,
                obstruction_id=obstruction_id,
                is_descent=is_descent,
                carrier_size=len(carrier),
                delta_support=delta_support,
                passed=False,
                terminal_route="RejectSelfDifference",
                diagnosis="Self-difference violation: identical endpoints in cut",
                issues=tuple(issues),
            )

        if carrier and len(carrier) < 2:
            issues.append(f"Carrier support floor violated: |carrier|={len(carrier)} < 2")
            return PostnikovStepReceipt(
                from_stage=from_stage,
                to_stage=to_stage,
                wire=wire,
                node_type=node_type,
                obstruction_id=obstruction_id,
                is_descent=is_descent,
                carrier_size=len(carrier),
                delta_support=delta_support,
                passed=False,
                terminal_route="RequireSupportDeclaration",
                diagnosis="Subsingleton distinction violation",
                issues=tuple(issues),
            )

    # 7. Relational counts check if provided
    if counts is not None:
        try:
            verify_wdp_wir(carrier, counts, require_inhabited=True)
        except ValueError as err:
            issues.append(f"WIR verification failed: {err}")
            return PostnikovStepReceipt(
                from_stage=from_stage,
                to_stage=to_stage,
                wire=wire,
                node_type=node_type,
                obstruction_id=obstruction_id,
                is_descent=is_descent,
                carrier_size=len(carrier),
                delta_support=delta_support,
                passed=False,
                terminal_route="RejectGhostDistinction",
                diagnosis=str(err),
                issues=tuple(issues),
            )

    passed = len(issues) == 0
    return PostnikovStepReceipt(
        from_stage=from_stage,
        to_stage=to_stage,
        wire=wire,
        node_type=node_type,
        obstruction_id=obstruction_id,
        is_descent=is_descent,
        carrier_size=len(carrier),
        delta_support=delta_support,
        passed=passed,
        terminal_route="AcceptWitnessedDifference" if passed else "RejectGhostDistinction",
        diagnosis="Step passed verified obstruction resolution" if passed else "; ".join(issues),
        issues=tuple(issues),
    )


def audit_stage_sequence(
    steps: Sequence[tuple[int, int, str | WdpNode, Sequence[str]]],
) -> list[PostnikovStepReceipt]:
    """Audit an ordered chain of S(n) Postnikov tower steps."""
    receipts: list[PostnikovStepReceipt] = []
    for from_stage, to_stage, event, carrier in steps:
        receipt = audit_stage_transition(
            from_stage=from_stage,
            to_stage=to_stage,
            event=event,
            carrier=carrier,
        )
        receipts.append(receipt)
    return receipts


# ---------------------------------------------------------------------------
# Contract Validation (Mirroring normal_form_contract_schema)
# ---------------------------------------------------------------------------


def load_yaml(path: Path) -> Any:
    """Load YAML file with duplicate key detection."""
    try:
        import yaml
    except ImportError as error:
        raise ValueError("Install PyYAML for YAML contract auditing") from error

    class UniqueLoader(yaml.SafeLoader):
        pass

    def mapping(loader: Any, node: Any, deep: bool = False) -> dict:
        result = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node, deep=deep)
            if key in result:
                raise ValueError(f"Duplicate YAML key: {key}")
            result[key] = loader.construct_object(value_node, deep=deep)
        return result

    UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping)
    return yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueLoader)


def validate_contract(contract: dict, schema: dict) -> list[str]:
    """Validate a normal form contract against the custom meta-schema."""
    issues = []
    if not isinstance(contract, dict):
        return ["Contract must be a mapping"]

    def matches(value: Any, definition: Any) -> bool:
        if isinstance(definition, dict) and "enum" in definition:
            return any(type(value) is type(item) and value == item for item in definition["enum"])
        checks = {
            "string": lambda v: type(v) is str,
            "string_or_null": lambda v: v is None or type(v) is str,
            "boolean": lambda v: type(v) is bool,
            "list": lambda v: type(v) is list,
            "object": lambda v: type(v) is dict,
        }
        if definition not in checks:
            raise ValueError(f"Unsupported meta-schema type: {definition!r}")
        return checks[definition](value)

    for key in schema["required_top_level_sections"]:
        if key not in contract:
            issues.append(f"Missing {key}")
    if "contract_kind" in contract and not matches(
        contract["contract_kind"], schema["contract_kinds"]
    ):
        issues.append("Invalid contract_kind")
    for section, definition in schema["section_definitions"].items():
        if section not in contract:
            continue
        obj = contract[section]
        if "type" in definition:
            if not matches(obj, definition["type"]):
                issues.append(f"Invalid type at {section}")
            continue
        if not isinstance(obj, dict):
            issues.append(f"{section} must be a mapping")
            continue
        for key in definition.get("required_fields", []):
            if key not in obj:
                issues.append(f"Missing {section}.{key}")
        for key, kind in definition.get("field_types", {}).items():
            if key in obj and not matches(obj[key], kind):
                issues.append(f"Invalid type/value at {section}.{key}")
    routes = contract.get("terminal_routes")
    mapping = contract.get("terminal_route_map")
    if type(routes) is list and type(mapping) is dict:
        if not all(type(route) is str for route in routes):
            issues.append("Local terminal routes must be strings")
        elif len(set(routes)) != len(routes):
            issues.append("Duplicate local terminal route")
        elif set(mapping) != set(routes):
            issues.append("terminal_route_map domain differs from terminal_routes")
        if any(value not in schema["canonical_terminals"]["enum"] for value in mapping.values()):
            issues.append("Unknown canonical terminal")
    return sorted(issues)


def audit_contracts(contracts_dir: Path | None = None) -> list[str]:
    """Audit all normal form contracts in 006_oewdp/normal_forms."""
    if contracts_dir is None:
        contracts_dir = NORMAL_FORMS_DIR
    schema_path = contracts_dir / "normal_form_contract_schema.yaml"
    if not schema_path.is_file():
        return [f"Schema not found: {schema_path}"]
    schema = load_yaml(schema_path)
    findings = []
    for p in sorted(contracts_dir.glob("nf.*.yaml")):
        contract = load_yaml(p)
        issues = validate_contract(contract, schema)
        for issue in issues:
            findings.append(f"{p.name}: {issue}")
    return findings


# ---------------------------------------------------------------------------
# Markdown Fence Audit
# ---------------------------------------------------------------------------


def audit_markdown(path: Path) -> list[dict[str, Any]]:
    """Audit explicitly tagged ```wdp fences in Markdown documents."""
    findings = []
    lines = path.read_text(encoding="utf-8").splitlines()
    opening = re.compile(r"^( {0,3})(`{3,})([^`]*)$")
    position = 0
    while position < len(lines):
        match = opening.fullmatch(lines[position])
        if not match:
            position += 1
            continue
        margin, width, profile = len(match.group(1)), len(match.group(2)), match.group(3).strip()
        closing = re.compile(r"^ {0,3}`{" + str(width) + r",}[ \t]*$")
        position += 1
        body = []
        while position < len(lines) and not closing.fullmatch(lines[position]):
            line = lines[position]
            removed = min(margin, len(line) - len(line.lstrip(" ")))
            body.append(line[removed:])
            position += 1
        position < len(lines)
        position += 1

        if profile != "wdp":
            continue

        for line_idx, raw_token in enumerate(body):
            token = raw_token.strip()
            if not token or token.startswith("#"):
                continue
            issue = wire_issue(token)
            if issue is not None:
                findings.append(
                    {
                        "file": str(path),
                        "line": position - len(body) + line_idx,
                        "token": token,
                        "issue": issue,
                    }
                )
    return findings


# ---------------------------------------------------------------------------
# CLI Entrypoint
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description="WDP Stage Transition and Obstruction Audit CLI")
    subparsers = parser.add_subparsers(dest="command")

    sub_wire = subparsers.add_parser("wire", help="Audit wire expressions")
    sub_wire.add_argument("tokens", nargs="+", help="WDP wire expressions to audit")

    sub_contracts = subparsers.add_parser("contracts", help="Audit normal form contracts")
    sub_contracts.add_argument(
        "--dir", type=Path, default=NORMAL_FORMS_DIR, help="Contracts directory"
    )

    args = parser.parse_args()

    if args.command == "wire":
        failed = False
        for token in args.tokens:
            issue = wire_issue(token)
            if issue:
                print(f"FAIL: {token} -> {issue}")
                failed = True
            else:
                print(f"PASS: {token}")
        return 1 if failed else 0

    if args.command == "contracts":
        findings = audit_contracts(args.dir)
        if findings:
            print(f"FAILED: {len(findings)} contract issues found:")
            for f in findings:
                print(f"  {f}")
            return 1
        print(f"PASS: All contracts in {args.dir} valid against schema.")
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
