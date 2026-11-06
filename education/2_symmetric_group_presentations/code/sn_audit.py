"""Read-only S(n) documentation checks. Python 3.10+; PyYAML for YAML only.

Public profiles are explicit. Formation, finite relation checks, and schema
checks emit separate evidence; none verifies a Postnikov realization or Lean
proof. No source-file rewriting, layout repair, or automatic profile selection.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

GLYPHS = "abcdefghijklmnopqrstuvwxyz0123456789"
GAMMA38 = frozenset(GLYPHS + "<>")
PROFILES = ("sn-wire-v1", "sn-wire-v2", "mss-boundary-v1")


@dataclass(frozen=True)
class SN:
    kind: str
    args: tuple[Any, ...] = ()


@dataclass(frozen=True)
class Packet:
    kind: str
    value: str | tuple[Packet, ...] = ""


def parse_sn(text: str, profile: str, max_depth: int = 128) -> SN:
    if profile not in PROFILES[:2]:
        raise ValueError("Declare sn-wire-v1 or sn-wire-v2")
    if type(max_depth) is not int or max_depth < 0:
        raise ValueError("max_depth must be a nonnegative integer")

    def parse(s: str, depth: int) -> SN:
        if depth > max_depth:
            raise ValueError("Declared parse-depth budget exceeded")
        if s == "<>":
            return SN("ground")
        if s == "NON_DESCENT":
            return SN("non_descent")
        for kind, pattern in (
            ("mark", r"<([a-z0-9])>"),
            ("pair", r"<([a-z0-9])([a-z0-9])>"),
            ("cut", r"<([a-z0-9])->([a-z0-9])>"),
            ("simplex", r"\[([a-z0-9]),([a-z0-9])\]"),
        ):
            match = re.fullmatch(pattern, s)
            if match:
                return SN(kind, match.groups())
        if profile == "sn-wire-v1":
            match = re.fullmatch(
                r"([ur])_([0-9]+)<([a-z0-9]*|[a-z0-9]->[a-z0-9]|[a-z0-9],[a-z0-9])>", s
            )
            if match:
                operation, index, body = match.groups()
                # Stage spelling, including leading zeroes, is retained.
                return SN(operation, (index, SN("legacy_body", (body,))))
        else:
            match = re.fullmatch(r"([ur])_([0-9]+)<([\s\S]*)>", s)
            if match:
                operation, index, body = match.groups()
                return SN(operation, (index, parse(body, depth + 1)))
        raise ValueError(f"Outside {profile}: {s!r}")

    return parse(text, 0)


def render_sn(node: SN, profile: str) -> str:
    if profile not in PROFILES[:2]:
        raise ValueError("Declare sn-wire-v1 or sn-wire-v2")
    if node.kind == "ground":
        return "<>"
    if node.kind == "non_descent":
        return "NON_DESCENT"
    if node.kind == "mark":
        return "<" + node.args[0] + ">"
    if node.kind == "pair":
        return "<" + "".join(node.args) + ">"
    if node.kind == "cut":
        return "<" + node.args[0] + "->" + node.args[1] + ">"
    if node.kind == "simplex":
        return "[" + ",".join(node.args) + "]"
    if node.kind in {"u", "r"}:
        index, body = node.args
        if profile == "sn-wire-v1":
            if body.kind != "legacy_body":
                raise ValueError("v1 requires a legacy body")
            payload = body.args[0]
        else:
            payload = render_sn(body, profile)
        return node.kind + "_" + index + "<" + payload + ">"
    raise ValueError(f"Unsupported AST kind: {node.kind}")


def parse_packet(text: str, max_depth: int = 128) -> Packet:
    if type(max_depth) is not int or max_depth < 0:
        raise ValueError("max_depth must be a nonnegative integer")
    if not text or any(c not in GAMMA38 for c in text):
        raise ValueError("Outside the declared Gamma38 alphabet")

    def parse(position: int, depth: int) -> tuple[Packet, int]:
        if depth > max_depth:
            raise ValueError("Declared parse-depth budget exceeded")
        if position >= len(text) or text[position] != "<":
            raise ValueError(f"Expected '<' at {position}")
        position += 1
        if position >= len(text):
            raise ValueError("Unclosed packet")
        if text[position] == ">":
            return Packet("ground"), position + 1
        if text[position] == "<":
            children = []
            while position < len(text) and text[position] == "<":
                child, position = parse(position, depth + 1)
                children.append(child)
            if position >= len(text) or text[position] != ">":
                raise ValueError("Composite must contain packets only and close")
            return Packet("composite", tuple(children)), position + 1
        begin = position
        while position < len(text) and text[position] in GLYPHS:
            position += 1
        if position == begin or position >= len(text) or text[position] != ">":
            raise ValueError("Atom must contain one or more Sigma36 glyphs")
        return Packet("atom", text[begin:position]), position + 1

    result, end = parse(0, 0)
    if end != len(text):
        raise ValueError(f"Unconsumed bytes/characters at {end}")
    return result


def render_packet(packet: Packet) -> str:
    if packet.kind == "ground":
        return "<>"
    if packet.kind == "atom":
        return "<" + packet.value + ">"
    if packet.kind == "composite":
        return "<" + "".join(render_packet(p) for p in packet.value) + ">"
    raise ValueError("Unknown packet kind")


def atom(text: str) -> Packet:
    if not text or any(c not in GLYPHS for c in text):
        raise ValueError("Atom payload must be a nonempty Sigma36 word")
    return Packet("atom", text)


def term(head: str, *arguments: Packet) -> Packet:
    if not all(isinstance(p, Packet) for p in arguments):
        raise ValueError("Term arguments must be packets")
    return Packet("composite", (atom(head), *arguments))


def encode_sn(node: SN) -> Packet:
    """Tagged Gamma38 codec, separate from the mathematical u/r maps."""
    if node.kind == "ground":
        return Packet("ground")
    if node.kind == "non_descent":
        return atom("nondescent")
    if node.kind in {"mark", "pair", "cut", "simplex"}:
        return term(node.kind, *(atom(value) for value in node.args))
    if node.kind == "legacy_body":
        body = node.args[0]
        if "->" in body:
            return term("bodycut", *(atom(value) for value in body.split("->")))
        if "," in body:
            return term("bodypair", *(atom(value) for value in body.split(",")))
        return term("bodyword", atom(body) if body else Packet("ground"))
    if node.kind in {"u", "r"}:
        index, body = node.args
        return term(node.kind, atom(index), encode_sn(body))
    raise ValueError("Unsupported S(n) node")


def decode_sn(packet: Packet, profile: str, max_depth: int = 128) -> SN:
    def decode(p: Packet, depth: int) -> SN:
        if depth > max_depth:
            raise ValueError("Declared decode-depth budget exceeded")
        if p.kind == "ground":
            return SN("ground")
        if p.kind == "atom" and p.value == "nondescent":
            return SN("non_descent")
        if p.kind != "composite" or not p.value or p.value[0].kind != "atom":
            raise ValueError("Missing declared constructor tag")
        head = p.value[0].value
        arguments = p.value[1:]
        if head in {"mark", "pair", "cut", "simplex"}:
            count = 1 if head == "mark" else 2
            if len(arguments) != count or any(a.kind != "atom" for a in arguments):
                raise ValueError("Wrong constructor arity/type")
            return SN(head, tuple(a.value for a in arguments))
        if head == "bodyword" and len(arguments) == 1:
            value = arguments[0]
            if value.kind not in {"ground", "atom"}:
                raise ValueError("Invalid legacy word body")
            return SN("legacy_body", ("" if value.kind == "ground" else value.value,))
        if head in {"bodycut", "bodypair"} and len(arguments) == 2:
            if any(a.kind != "atom" for a in arguments):
                raise ValueError("Invalid legacy pair body")
            separator = "->" if head == "bodycut" else ","
            return SN("legacy_body", (separator.join(a.value for a in arguments),))
        if head in {"u", "r"} and len(arguments) == 2 and arguments[0].kind == "atom":
            return SN(head, (arguments[0].value, decode(arguments[1], depth + 1)))
        raise ValueError("Unknown tag or constructor arity")

    node = decode(packet, 0)
    # Reject untyped or malformed nodes even when the boundary syntax is valid.
    # A canonical code is required; accepting aliases would break code round trips.
    if parse_sn(render_sn(node, profile), profile, max_depth) != node:
        raise ValueError("Decoded value is not in the selected S(n) profile")
    if encode_sn(node) != packet:
        raise ValueError("Noncanonical or undeclared codec shape")
    return node


def wire_issue(text: str, profile: str, max_depth: int = 128) -> str | None:
    if profile not in PROFILES:
        return f"Unknown explicit profile: {profile}"
    try:
        if profile == "mss-boundary-v1":
            parsed = parse_packet(text, max_depth)
            rendered = render_packet(parsed)
        else:
            parsed = parse_sn(text, profile, max_depth)
            rendered = render_sn(parsed, profile)
        if rendered != text:
            return "Exact spelling round trip failed"
    except ValueError as error:
        return str(error)
    return None


def verify_wir(
    carrier: tuple[str, ...], counts: dict[tuple[str, str], int], require_inhabited: bool = True
) -> dict[str, int]:
    """Finite presence model; identity is explicitly equality of carrier labels.

    The relation is defined by R(a,b) iff counts[a,b] > 0. This validates
    irreflexivity and returns measurements without conflating them.
    """
    if len(set(carrier)) != len(carrier):
        raise ValueError("Carrier identities must be unique")
    vertices = set(carrier)
    edges = []
    for (a, b), count in counts.items():
        if a not in vertices or b not in vertices:
            raise ValueError("Undeclared endpoint")
        if type(count) is not int or count < 0:
            raise ValueError("Multiplicity must be a nonnegative integer")
        if count > 0:
            if a == b:
                raise ValueError("Irreflexivity violated")
            edges.append((a, b))
    if require_inhabited and not edges:
        raise ValueError("No inhabited primitive distinction")
    return {
        "carrier_size": len(carrier),
        "primitive_endpoint_arity": 2,
        "asserted_pair_count": len(edges),
        "witness_occurrence_count": sum(counts.values()),
    }


def minimum_tag_values(
    vertices: tuple[str, ...], edges: tuple[tuple[str, str], ...], max_vertices: int = 6
) -> int:
    """Exact finite search for a constant-observation separation problem.

    Edges are pairs that must receive different tags. Returns chromatic number,
    not a unique minimizer. The explicit bound is an execution budget, not a
    theorem limiting S(n). This does not enumerate equivalence classes of tags.
    """
    if len(set(vertices)) != len(vertices):
        raise ValueError("Repeated vertex identity")
    if len(vertices) > max_vertices:
        raise ValueError("Declared finite search budget exceeded")
    index = {v: i for i, v in enumerate(vertices)}
    indexed = []
    for a, b in edges:
        if a not in index or b not in index or a == b:
            raise ValueError("Edges must have declared distinct endpoints")
        indexed.append((index[a], index[b]))
    if not vertices:
        return 0
    for k in range(1, len(vertices) + 1):
        for tags in itertools.product(range(k), repeat=len(vertices)):
            if all(tags[a] != tags[b] for a, b in indexed):
                return k
    raise AssertionError("Unique labels always color a finite loop-free graph")


def load_yaml(path: Path) -> Any:
    try:
        import yaml
    except ImportError as error:
        raise ValueError("Install PyYAML for the YAML contract command") from error

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
    """Interpret the supplied custom meta-schema; this is not JSON Schema."""
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
    """Audit all normal form contracts in 002_s_n/normal_forms using validate_contract."""
    if contracts_dir is None:
        contracts_dir = Path(__file__).resolve().parents[1] / "normal_forms"
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


def check_fixtures(cases: list[dict], profile: str) -> list[str]:
    starts = {
        "sn_presentation": None,
        "ground_token": "ground",
        "supplied_token": "mark",
        "retained_pair": "pair",
        "directed_cut": "cut",
        "simplex_cut": "simplex",
        "relation_token": {"pair", "cut", "simplex"},
        "section_lift": "u",
        "retraction_map": "r",
        "non_descent": "non_descent",
    }
    failures = []
    ids = set()
    for case in cases:
        if case["id"] in ids:
            raise ValueError("Duplicate fixture id")
        ids.add(case["id"])
        if type(case["accept"]) is not bool:
            raise ValueError("Fixture acceptance must be boolean")
        text, start = case["text"], case["start"]
        if start == "glyph":
            actual = len(text) == 1 and text in GLYPHS
        elif start == "digits":
            actual = re.fullmatch(r"[0-9]+", text) is not None
        else:
            if start not in starts:
                raise ValueError(f"Unsupported fixture start {start}")
            try:
                node = parse_sn(text, profile)
                kind = starts[start]
                actual = (
                    kind is None or node.kind == kind or (type(kind) is set and node.kind in kind)
                )
            except ValueError:
                actual = False
        if actual != case["accept"]:
            failures.append(case["id"])
    return failures


def audit_markdown(path: Path) -> list[dict]:
    """Only explicitly tagged fences are parsed; text/ASCII/metasyntax is ignored.

    Removing the opening Markdown fence margin is a declared source adapter,
    not whitespace trimming of a submitted wire expression. No blank payload
    lines are removed. Multi-line wire remains multi-line and fails this profile.
    """
    findings = []
    lines = path.read_text(encoding="utf-8").splitlines()
    opening = re.compile(r"^( {0,3})(`{3,})([^`]*)$")
    position = 0
    while position < len(lines):
        match = opening.fullmatch(lines[position])
        if not match:
            position += 1
            continue
        begin = position
        margin, width, profile = len(match.group(1)), len(match.group(2)), match.group(3)
        closing = re.compile(r"^ {0,3}`{" + str(width) + r",}[ \t]*$")
        position += 1
        body = []
        while position < len(lines) and not closing.fullmatch(lines[position]):
            line = lines[position]
            removed = min(margin, len(line) - len(line.lstrip(" ")))
            body.append(line[removed:])
            position += 1
        closed = position < len(lines)
        position += 1
        # Consume unknown outer fences as a whole; embedded shorter fences
        # inside a literal Markdown example are not executable examples.
        if profile not in PROFILES:
            continue
        issue = wire_issue("\n".join(body), profile) if closed else "Unclosed tagged code fence"
        findings.append(
            {"line": begin + 2, "profile": profile, "syntax_accept": issue is None, "issue": issue}
        )
    return findings


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    wire = commands.add_parser("wire")
    wire.add_argument("--profile", choices=PROFILES, required=True)
    wire.add_argument("text")
    fixtures = commands.add_parser("fixtures")
    fixtures.add_argument("--profile", choices=PROFILES[:2], required=True)
    fixtures.add_argument("path", type=Path)
    contracts = commands.add_parser("contracts")
    contracts.add_argument("--schema", type=Path, required=True)
    contracts.add_argument("paths", type=Path, nargs="+")
    documents = commands.add_parser("documents")
    documents.add_argument("paths", type=Path, nargs="+")
    args = parser.parse_args()
    if args.command == "wire":
        issue = wire_issue(args.text, args.profile)
        result = {"profile": args.profile, "syntax_accept": issue is None, "issue": issue}
        failed = issue is not None
    elif args.command == "fixtures":
        cases = json.loads(args.path.read_text(encoding="utf-8"))
        failures = check_fixtures(cases, args.profile)
        result = {"profile": args.profile, "cases": len(cases), "failures": failures}
        failed = bool(failures)
    elif args.command == "contracts":
        schema = load_yaml(args.schema)
        result = {
            str(path): {
                "sha256": digest(path),
                "issues": validate_contract(load_yaml(path), schema),
            }
            for path in args.paths
        }
        failed = any(item["issues"] for item in result.values())
    else:
        result = {
            str(path): {"sha256": digest(path), "wire_fences": audit_markdown(path)}
            for path in args.paths
        }
        failed = any(
            not item["syntax_accept"]
            for document in result.values()
            for item in document["wire_fences"]
        )
    print(json.dumps(result, sort_keys=True, ensure_ascii=False, allow_nan=False, indent=2))
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
