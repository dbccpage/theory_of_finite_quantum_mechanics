"""Generate reviewable containment patches without modifying production sources.

These patches close specific admission bugs; they do not discharge any MUB premise.
AuthorityEffect: None.
stated region only; mints no authority
"""
from pathlib import Path
import difflib
import json

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "scratch/audit_2026_09_22/patched"
PATCH = Path(__file__).with_name("proposed_fixes.patch")
changes = {}


def replace(path, old, new):
    before = changes.get(path, (ROOT / path).read_text(encoding="utf-8"))
    if before.count(old) != 1:
        raise ValueError(f"Expected one replacement site: {path}: {old[:70]!r}")
    changes[path] = before.replace(old, new, 1)


PY = "omega_engine/crates/mub_verify/"
RS = "omega_engine/crates_rs/omega_mub/src/omega_native/"

p = RS + "mub6_smale_sentry.rs"
replace(p, "    ZeroPivotAt(usize),", "    ZeroPivotAt(usize),\n    CenterOutsideBox,")
replace(p, '            Self::SingularMatrix => write!(f, "Matrix is singular over Q"),',
    '            Self::SingularMatrix => write!(f, "Matrix is singular over Q"),\n'
    '            Self::CenterOutsideBox => write!(f, "Krawczyk center is outside the box"),')
replace(p, "    // 1. Evaluate F(x_0) and Jacobian DF(x_0)",
    "    if !x_box.contains_point(&x_0) {\n        return Err(LuError::CenterOutsideBox);\n    }\n\n"
    "    // 1. Evaluate F(x_0) and Jacobian DF(x_0)")
replace(p, "        let mut all_positive = true;", "        let mut all_positive = !cells.is_empty();")
replace(p, "        let mut min_margin = BigRational::from_integer(BigInt::from(1000000));",
    "        let mut min_margin = cells.first().map(|c| c.residual_margin.clone())\n"
    "            .unwrap_or_else(BigRational::zero);")

p = RS + "l1_discrete_solver/network_simplex.rs"
replace(p, "        let sum: i128 = self.demand.iter().sum();",
    "        let sum = self.demand.iter().try_fold(0i128, |acc, &d|\n"
    "            acc.checked_add(d).ok_or(NetworkSimplexError::ArithmeticOverflow))?;")
replace(p, "                .checked_add(d.abs())",
    "                .checked_add(d.checked_abs().ok_or(NetworkSimplexError::ArithmeticOverflow)?)")
replace(p, "        let m = 1 + sum_costs + sum_demands;",
    "        let m = sum_costs.checked_add(sum_demands).and_then(|v| v.checked_add(1))\n"
    "            .ok_or(NetworkSimplexError::ArithmeticOverflow)?;")
replace(p, "    pub fn solve(&mut self) -> Result<NetworkSimplexSolution, NetworkSimplexError> {\n",
    "    pub fn solve(&mut self) -> Result<NetworkSimplexSolution, NetworkSimplexError> {\n"
    "        if self.arcs.iter().any(|a| a.lower != 0 || a.upper.is_some()) {\n"
    "            return Err(NetworkSimplexError::InvalidCarrier {\n"
    '                message: "only zero lower bounds and unbounded upper capacities are supported".into(),\n'
    "            });\n        }\n")

p = PY + "l1_governor.py"
replace(p, "@dataclass(frozen=True)\nclass Edge:",
    'def require_exact(value):\n'
    '    if type(value) not in (int, Fraction):\n'
    '        raise TypeError("exact integer or Fraction required")\n'
    '    return Fraction(value)\n\n\n@dataclass(frozen=True)\nclass Edge:')
replace(p, "        if self.weight <= 0:", "        require_exact(self.weight)\n        if self.weight <= 0:")
replace(p, "    weights: Dict[Tuple[str, str], Fraction] = {}",
    "    for value in claims.values.values():\n        require_exact(value)\n"
    "    weights: Dict[Tuple[str, str], Fraction] = {}")
replace(p, "        val_frac = Fraction(value)", "        val_frac = require_exact(value)")
replace(p, "        if proposed_claims is not None:\n            # 1. Diagonal",
    "        if proposed_claims is not None:\n"
    "            if proposed_claims != self.edge_claims:\n"
    "                return GovernorVerdict(\n                    admitted=False, status=\"UnlicensedClaimChange\",\n"
    "                    defect_before=self.primary_obstruction(), defect_after=self.primary_obstruction(),\n"
    "                    details=\"Claim changes need a separate semantic certificate.\", step_id=sid)\n"
    "            # 1. Diagonal")

p = PY + "target_b1_continuous_chaining.py"
replace(p, "            if step > self.delta_crit:\n                return False, f\"Uncertified parameter gap between {t_curr} and {t_next}: step {step} > delta_crit {self.delta_crit}\"",
    "            if step > points[i].delta + points[i + 1].delta:\n"
    '                return False, f"Uncovered interval between {t_curr} and {t_next}"')
replace(p, '        return True, f"Dense chain of {len(points)} points verified without gaps"',
    "        if points[0].t - points[0].delta > T_MIN or points[-1].t + points[-1].delta < T_MAX:\n"
    '            return False, "Endpoint neighborhoods are not covered"\n'
    '        return True, f"Sample balls cover the declared interval; analytic witnesses still required"')

p = PY + "verify_all_receipts.py"
manifest = json.loads((ROOT / "artifacts/manifest.json").read_text(encoding="utf-8"))
expected = {(e["target"], e["filename"], e["schema_version"]) for e in manifest["receipts"]}
replace(p, "EXPECTED_TOTAL_RECEIPTS = 10", "EXPECTED_TOTAL_RECEIPTS = 10\nEXPECTED_RECEIPT_REGISTRY = " + repr(sorted(expected)))
replace(p, "    # Verification of individual receipts", "    actual_registry = [(e.get(\"target\"), e.get(\"filename\"), e.get(\"schema_version\"))\n"
    "                       for e in receipts_list if isinstance(e, dict)]\n"
    "    if len(actual_registry) != len(receipts_list) or set(actual_registry) != set(EXPECTED_RECEIPT_REGISTRY) or len(set(actual_registry)) != len(actual_registry):\n"
    '        return {"all_passed": False, "receipts_verified": 0, "errors": errors + ["Receipt registry mismatch or duplicate"]}\n\n'
    "    # Verification of individual receipts")
replace(p, "        receipt_file = resolved_artifacts / filename", "        receipt_file = (resolved_artifacts / filename).resolve()\n"
    "        if not receipt_file.is_relative_to(resolved_artifacts.resolve()):\n"
    '            errors.append(f"{entry_prefix}: receipt path outside artifacts root")\n            continue')

p = "lean4/012_mutually_unbiased_bases/MUB/CertificatePilot.lean"
original = (ROOT / p).read_text(encoding="utf-8")
start = original.index("def pilotSources : List Expr := [")
end = original.index("\n]\n", start) + len("\n]")
source_definition = original[start:end]
replace(p, "def checkCertificate (cert : Certificate) : Bool :=",
    source_definition.replace("def pilotSources", "def expectedPilotSources") + "\n\ndef checkCertificate (cert : Certificate) : Bool :=")
replace(p, '  else if cert.coefficient_field != "ℚ" then false',
    '  else if cert.coefficient_field != "ℚ" then false\n'
    '  else if cert.branch_hypotheses != "pilot_circle_tangent" then false\n'
    '  else if cert.sources != expectedPilotSources then false')
replace(p, source_definition, "def pilotSources : List Expr := expectedPilotSources")
replace(p, "    dsimp [sumProdExpr, pilotMultipliers, pilotSources, evalExpr]",
    "    dsimp [sumProdExpr, pilotMultipliers, pilotSources, expectedPilotSources, evalExpr]")

p = PY + "packet_firewall.py"
replace(p, "        return FirewallVerdict(admitted=True)\n\n    def evaluate_pipeline(",
    "        return FirewallVerdict(admitted=False,\n"
    "            refusal_code=FirewallRefusalCode.FW_MOVE_VIOLATION,\n"
    '            reason="Licensed rules and full host replay are required")\n\n    def evaluate_pipeline(')

patches = []
for name, after in changes.items():
    before = (ROOT / name).read_text(encoding="utf-8")
    path = OUT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(after, encoding="utf-8", newline="\n")
    patches.extend(difflib.unified_diff(before.splitlines(keepends=True), after.splitlines(keepends=True),
        fromfile="a/" + name, tofile="b/" + name))
PATCH.write_text("".join(patches), encoding="utf-8", newline="\n")
print(f"Wrote {len(changes)} proposed file diffs; production sources unchanged.")
