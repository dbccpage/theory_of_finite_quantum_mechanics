"""Structural contracts, distinguished from mathematical normalization evidence.

AuthorityEffect: None. A schema pass is not a proof of normalization laws.
Runtime routing recomputes an actual finite cochain packet.

Claim Hygiene:
1. What this supports:
   - Structural schema linting and field validation of normal-form YAML contracts.
   - Runtime re-computation of sign packets on finite cochain complexes via BQNFSignEvaluator.
   - Strict separation between declarative schema compliance and mathematical normalization proofs.
2. What this does not support:
   - Proof of normalization laws (soundness, idempotence, completeness, determinism) purely from schema validity.
3. Narrowest defensible claim:
   - A schema pass verifies structural conformance only; mathematical correctness requires independent execution and verified normalization evidence.
4. Next test needed:
   - Cross-check candidate cochain quotients against Lean 4 Lake proof kernel theorems.
"""

from pathlib import Path
from typing import Any, Dict
import sys
import yaml
try:
    from .bqnf_sign_evaluator import BQNFSignEvaluator, CochainComplex
except (ImportError, ValueError):
    from bqnf_sign_evaluator import BQNFSignEvaluator, CochainComplex



class NormalFormEvaluator:
    def __init__(self, directory: Path):
        self.directory = Path(directory)
        self.yaml_files = sorted(self.directory.glob("nf.*.yaml"))
        with (self.directory / "normal_form_contract_schema.yaml").open(encoding="utf-8") as source:
            self.schema = yaml.safe_load(source)

    def lint_all_contracts(self) -> Dict[str, Dict[str, Any]]:
        return {path.name: self.lint_single_contract(path) for path in self.yaml_files}

    def lint_single_contract(self, file_path: Path) -> Dict[str, Any]:
        try:
            with Path(file_path).open(encoding="utf-8") as source:
                data = yaml.safe_load(source)
        except (OSError, yaml.YAMLError) as exc:
            return {"valid": False, "error": f"YAML parse/read error: {exc}"}
        errors = []
        if not isinstance(data, dict):
            return {"valid": False, "error": "Root structure is not a mapping"}
        for key in self.schema["required_top_level_sections"]:
            if key not in data:
                errors.append(f"Missing top-level section: {key}")
        if data.get("contract_kind") not in self.schema["contract_kinds"]["enum"]:
            errors.append("Invalid contract_kind")
        for key, spec in self.schema["section_definitions"].items():
            if key not in data:
                continue
            section = data[key]
            if spec.get("type") == "list":
                if not isinstance(section, list):
                    errors.append(f"{key} must be a list")
                continue
            if not isinstance(section, dict):
                errors.append(f"{key} must be a mapping")
                continue
            for field in spec.get("required_fields", []):
                if field not in section:
                    errors.append(f"Missing {key}.{field}")
            for field, field_type in spec.get("field_types", {}).items():
                if field not in section:
                    continue
                value = section[field]
                if isinstance(field_type, dict):
                    if value not in field_type["enum"]:
                        errors.append(f"Invalid enum {key}.{field}: {value}")
                else:
                    checks = {"string": isinstance(value, str),
                              "string_or_null": value is None or isinstance(value, str),
                              "list": isinstance(value, list), "object": isinstance(value, dict),
                              "boolean": type(value) is bool}
                    if not checks.get(field_type, False):
                        errors.append(f"Invalid type {key}.{field}")
        routes, mapping = data.get("terminal_routes"), data.get("terminal_route_map")
        if not isinstance(routes, list) or not routes or any(not isinstance(x, str) for x in routes):
            errors.append("terminal_routes must be a nonempty string list")
        elif len(set(routes)) != len(routes):
            errors.append("Duplicate terminal route")
        elif not isinstance(mapping, dict) or set(mapping) != set(routes):
            errors.append("terminal_route_map must map every local terminal exactly once")
        elif any(x not in self.schema["canonical_terminals"]["enum"] for x in mapping.values()):
            errors.append("Unknown canonical terminal")
        normalization = data.get("normalization", {})
        if isinstance(normalization, dict) and normalization.get("kind") == "canonicalizer":
            for field in ("domain", "equivalence", "normalizer", "representative_condition", "laws", "evidence"):
                if not normalization.get(field):
                    errors.append(f"Canonicalizer missing normalization.{field}")
            laws = normalization.get("laws", {})
            if not isinstance(laws, dict) or set(laws) != {"soundness", "idempotence", "completeness", "determinism"}:
                errors.append("Canonicalizer must declare all four normalization laws")
        if errors:
            return {"valid": False, "error": "; ".join(errors)}
        return {"valid": True, "id": data["identity"]["id"],
                "short_name": data["identity"]["short_name"], "route_count": len(routes),
                "normal_form_status": normalization["kind"],
                "proof_scope": "Schema only; consult normalization.evidence for mathematical laws"}

    def evaluate_bqnf_instance(self, data_packet: Dict[str, Any]) -> str:
        """Scalar residuals and asserted pairing flags alone cannot certify a route."""
        try:
            if not isinstance(data_packet, dict) or data_packet.get("dimension_error"):
                return "Refused"
            evaluator = BQNFSignEvaluator(CochainComplex(**data_packet["complex"]))
            return evaluator.evaluate_sign_packet(data_packet["c1_defect"], data_packet["path_signs"])["route"].value
        except (KeyError, TypeError, ValueError):
            return "Refused"


def main():
    repo_root = next((p for p in Path(__file__).resolve().parents if (p / "pyproject.toml").is_file()), Path(__file__).resolve().parents[4])
    candidates = [
        repo_root / "papers" / "core" / "fsp" / "normal_forms",
        Path(__file__).resolve().parent.parent / "normal_forms",
        Path(__file__).resolve().parent / "normal_forms",
    ]
    directory = next((d for d in candidates if d.is_dir()), candidates[0])
    results = NormalFormEvaluator(directory).lint_all_contracts()
    print(f"Structural contract audit: {len(results)} contracts (no theorem certification)")
    for name, result in results.items():
        print(f"{'PASS' if result['valid'] else 'FAIL'} {name}: {result.get('normal_form_status', result.get('error'))}")
    return 0 if results and all(result["valid"] for result in results.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
