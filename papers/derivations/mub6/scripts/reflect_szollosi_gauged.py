"""Format added coefficient rows and one candidate-box exclusion as Lean literals.

AuthorityEffect: None. Wire shape, literal formatting and byte custody only.
Lean checks the coefficient identities, box containment and semantic exclusion.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from reflect_szollosi_native import exact_keys, integer, rational_literal, read_json

PROOFS = r"""
def extraCoefficientCheck : Bool := tableKeys extraTerms ==
  tableKeys (extraExpressions.map normalizedExpr)

theorem extra_coefficients_checked : extraCoefficientCheck = true := by decide +kernel

theorem extra_terms_match : extraTerms = extraExpressions.map normalizedExpr :=
  table_keys_injective (beq_iff_eq.mp extra_coefficients_checked)

def augmentedNativeTerms : List (List CodedTerm) := nativeTerms ++ extraTerms

theorem augmented_native_terms_match :
    augmentedNativeTerms = augmentedExpressions.map normalizedExpr := by
  simp only [augmentedNativeTerms,augmentedExpressions,List.map_append,List.map_map,
    native_terms_match,extra_terms_match]
  rfl

def nativeLower (v : Variable) : Rat := ((nativeBounds[variableCode v]?).getD (0,0)).1
def nativeUpper (v : Variable) : Rat := ((nativeBounds[variableCode v]?).getD (0,0)).2

def nativeBoundCheck : Bool := allVariables.all fun v =>
  decide (lowRowLower v ≤ nativeLower v) && decide (nativeUpper v ≤ lowRowUpper v)

theorem native_bounds_checked : nativeBoundCheck = true := by decide +kernel

def InNativeBox (r : Variable → ℝ) : Prop :=
  ∀ v, (nativeLower v : ℝ) ≤ r v ∧ r v ≤ (nativeUpper v : ℝ)

theorem native_box_in_low_row (r : Variable → ℝ) (hb : InNativeBox r) : InLowRowBox r := by
  intro v
  have hv := List.all_eq_true.mp native_bounds_checked v (variables_complete v)
  simp only [Bool.and_eq_true,decide_eq_true_iff] at hv
  have hl : lowRowLower v ≤ nativeLower v := hv.1
  have hu : nativeUpper v ≤ lowRowUpper v := hv.2
  have hlr : (lowRowLower v : ℝ) ≤ nativeLower v := by exact_mod_cast hl
  have hur : (nativeUpper v : ℝ) ≤ lowRowUpper v := by exact_mod_cast hu
  exact ⟨hlr.trans (hb v).1,(hb v).2.trans hur⟩

theorem native_image_separated :
    decide (nativeUpper (rowVariable 0) < nativeImage.lo) = true := by decide +kernel

/-- The selected emitted image encloses the coordinate of every contained zero. -/
theorem native_image_semantics (r : Variable → ℝ) (h : AllExpressionsZero r)
    (hb : InNativeBox r) : nativeImage.Contains (r (rowVariable 0)) := by
  have hi := balanced_row_image r h (native_box_in_low_row r hb)
  norm_num [nativeImage,Bounds.Contains] at hi ⊢
  exact hi

theorem native_box_exclusion (r : Variable → ℝ) (h : AllExpressionsZero r)
    (hb : InNativeBox r) : False :=
  low_row_box_empty r h (native_box_in_low_row r hb)

def nativeWitness (v : Variable) : Rat := (nativeWitnessValues[variableCode v]?).getD 0

def witnessCheck : Bool := allVariables.all fun v =>
  decide (nativeLower v ≤ nativeWitness v) && decide (nativeWitness v ≤ nativeUpper v)

theorem native_witness_checked : witnessCheck = true := by decide +kernel

theorem native_witness_contains : InNativeBox (fun v => (nativeWitness v : ℝ)) := by
  intro v
  change (nativeLower v : ℝ) ≤ (nativeWitness v : ℝ) ∧ (nativeWitness v : ℝ) ≤ (nativeUpper v : ℝ)
  have hv := List.all_eq_true.mp native_witness_checked v (variables_complete v)
  simp only [Bool.and_eq_true,decide_eq_true_iff] at hv
  constructor
  · exact_mod_cast (hv.1 : nativeLower v ≤ nativeWitness v)
  · exact_mod_cast (hv.2 : nativeWitness v ≤ nativeUpper v)

theorem witness_parameters_eq :
    parameters (fun v => (nativeWitness v : ℝ)) = encodeParameters ![1,-1,1,Complex.I] := by
  funext q
  rcases q with ⟨i,b⟩
  fin_cases i <;> cases b <;>
    norm_num [parameters,nativeWitness,nativeWitnessValues,variableCode,bit,encodeParameters]

theorem witness_parameter_equations :
    ∀ e, MvPolynomial.eval (parameters (fun v => (nativeWitness v : ℝ)))
      (parameterPolynomial e) = 0 := by
  rw [witness_parameters_eq]
  apply (parameter_equations_iff _).mpr
  simpa [decode_encode] using boundary_parameter_point

/-- This box meets the admissible phase domain; the witness is not a quartet. -/
theorem native_box_has_admissible_phase_point :
    ∃ r : Variable → ℝ, InNativeBox r ∧
      ∀ e, MvPolynomial.eval (parameters r) (parameterPolynomial e) = 0 :=
  ⟨fun v => (nativeWitness v : ℝ),native_witness_contains,witness_parameter_equations⟩

def parentBounds : Variable → Bounds
  | .inr (.inr (a,i,j,b)) => if a = 2 ∧ i = 0 ∧ b = false then ⟨-3,3⟩
      else ⟨nativeLower (.inr (.inr (a,i,j,b))),nativeUpper (.inr (.inr (a,i,j,b)))⟩
  | v => ⟨nativeLower v,nativeUpper v⟩

def parentBoundCheck : Bool := allVariables.all fun v =>
  let b := SzollosiRectangularReflection.nativeRetainedBox (variableCode v)
  decide ((parentBounds v).lo ≤ max b.lo (gaugeLower v)) &&
    decide (min b.hi (gaugeUpper v) ≤ (parentBounds v).hi)

theorem parent_bounds_checked : parentBoundCheck = true := by decide +kernel

theorem augmented_solution_in_parent (r : Variable → ℝ) (h : AllExpressionsZero r) :
    ∀ v, (parentBounds v).Contains (r v) := by
  have hs := (augmented_zeros_iff r).mp h
  have hg := gauged_solution_in_box r hs.1 hs.2
  intro v
  have hb := SzollosiRectangularReflection.solution_in_native_retained r hs.1
    (variableCode v) (variableCode_lt v)
  rw [coded_point_code] at hb
  have hv := List.all_eq_true.mp parent_bounds_checked v (variables_complete v)
  simp only [Bool.and_eq_true,decide_eq_true_iff] at hv
  have hl : ((parentBounds v).lo : ℝ) ≤
      max ((SzollosiRectangularReflection.nativeRetainedBox (variableCode v)).lo : ℝ)
        (gaugeLower v : ℝ) := by exact_mod_cast hv.1
  have hu : min ((SzollosiRectangularReflection.nativeRetainedBox (variableCode v)).hi : ℝ)
      (gaugeUpper v : ℝ) ≤ (parentBounds v).hi := by exact_mod_cast hv.2
  exact ⟨hl.trans (max_le hb.1 (hg v).1),(le_min hb.2 (hg v).2).trans hu⟩

def nativeChartBounds (j : Fin 6) (v : Variable) : Bounds :=
  ⟨if v = rowVariable j then 1 else (parentBounds v).lo,(parentBounds v).hi⟩

def InNativeChart (r : Variable → ℝ) (j : Fin 6) : Prop :=
  ∀ v, (nativeChartBounds j v).Contains (r v)

theorem native_chart_cover (r : Variable → ℝ) (h : AllExpressionsZero r) :
    ∃ j, InNativeChart r j := by
  have hb := augmented_solution_in_parent r h
  obtain ⟨j,hj⟩ := augmented_solution_six_charts r h
  rw [row_coordinate] at hj
  refine ⟨j,fun v => ⟨?_,(hb v).2⟩⟩
  by_cases hv : v = rowVariable j
  · simpa [nativeChartBounds,hv] using hj
  · simpa [nativeChartBounds,hv] using (hb v).1

theorem native_chart_quartet_iff (p : ParameterCoord → ℝ)
    (hp : ∀ e, MvPolynomial.eval p (parameterPolynomial e) = 0) :
    (∃ r, parameters r = p ∧ AllExpressionsZero r ∧ ∃ j, InNativeChart r j) ↔
      ∃ U V, SzollosiQuartetSystem.Quartet
        (SzollosiQuartetSystem.bases (SzollosiQuartetSystem.parameterMatrix p) U V) := by
  rw [← augmented_exists_with_parameters_iff p hp]
  constructor
  · rintro ⟨r,hr,hz,_⟩
    exact ⟨r,hr,hz⟩
  · rintro ⟨r,hr,hz⟩
    exact ⟨r,hr,hz,native_chart_cover r hz⟩

def nativeChartJson : Lean.Json := .arr (((List.finRange 6).map fun j =>
  Lean.Json.mkObj [("chart",natJson j.val),("bounds",.arr ((allVariables.map fun v =>
    Lean.Json.mkObj [("index",natJson (variableCode v)),
      ("lo",.str (rationalText (nativeChartBounds j v).lo)),
      ("hi",.str (rationalText (nativeChartBounds j v).hi))]).toArray))]).toArray)

#print axioms parent_bounds_checked
#print axioms augmented_solution_in_parent
#print axioms native_chart_cover
#print axioms native_chart_quartet_iff

#print axioms augmented_native_terms_match
#print axioms native_bounds_checked
#print axioms native_image_semantics
#print axioms native_box_exclusion
#print axioms native_box_has_admissible_phase_point
end MUB.SzollosiGaugedReflection
"""


def format_receipt(
    inspection: Path,
    exclusion: Path,
    coefficients: Path,
    root_receipt: Path,
    system: Path,
    request: Path,
) -> str:
    raw, data = read_json(inspection)
    box_raw, box = read_json(exclusion)
    coeff_raw, reference = read_json(coefficients)
    root_raw, parent = read_json(root_receipt)
    system_raw, ast = read_json(system)
    request_raw, req = read_json(request)
    integer(ast["variable_count"], 440)
    integer(ast["equation_count"], 666)
    if ast["schema"] != "omega.mub6.szollosi-gauged-expressions.v1":
        raise ValueError("system schema")
    for receipt in (data, box, parent):
        if receipt["input_sha256"] != hashlib.sha256(system_raw).hexdigest():
            raise ValueError("system bytes are not bound")
        if receipt["coefficient_reference_sha256"] != hashlib.sha256(coeff_raw).hexdigest():
            raise ValueError("coefficient bytes are not bound")
        integer(receipt["checked_coefficient_rows"], 666)
        for key in ("full_56_cell_and_cusp_calculation_complete", "kernel_reflection_complete"):
            if receipt[key] is not False:
                raise ValueError("runtime scope promotion")
    if box["request_sha256"] != hashlib.sha256(request_raw).hexdigest() or box["request"] != req:
        raise ValueError("request bytes are not bound")
    if box["root_existence_claimed"] is not False or parent["root_existence_claimed"] is not False:
        raise ValueError("root existence promotion")
    integer(data["checked_coefficient_rows"], 666)
    integer(data["variable_count"], 440)
    if (
        data["coefficients"] != reference
        or not isinstance(reference, list)
        or len(reference) != 666
    ):
        raise ValueError("native and Lean coefficient tables differ")
    if box["status"] != "EXCLUDED_BOX" or box["excluded_coordinate"] != 368:
        raise ValueError("selected candidate box was not excluded")
    integer(box["request"]["equation_count"], 666)
    integer(box["request"]["variable_count"], 440)
    _, original_reference = read_json(
        Path(__file__).resolve().parents[1] / "artifacts/mub_szollosi_lean_coefficients.json"
    )
    if reference[:618] != original_reference:
        raise ValueError("the original 618 coefficient rows changed")
    bounds = box["request"]["bounds"]
    if len(bounds) != 440 or len(box["request"]["center"]) != 440:
        raise ValueError("candidate box dimension")
    retained = parent["intersections"]
    if len(retained) != 440:
        raise ValueError("parent box dimension")
    for i, (b, old) in enumerate(zip(bounds, retained, strict=True)):
        expected = dict(old)
        if i in range(368, 380, 2):
            if old != {"index": i, "lo": "-3", "hi": "3"}:
                raise ValueError("the reconstructed parent row bounds differ")
            expected.update(lo="-1/2", hi="1/2")
        if b != expected:
            raise ValueError("candidate box is not the specified parent restriction")
    lines = [
        "import SzollosiGaugedCover",
        "import SzollosiNativeReflection",
        "import SzollosiRectangularReflection",
        "",
        "/-!",
        "# Added native coefficients and one semantic candidate-box exclusion",
        "",
        "AuthorityEffect: None.",
        "",
        "All added coefficient rows and all input bounds are kernel checked.",
        "The selected image is derived from the actual transition balance identity.",
        "Other images and the generic Rust/JSON runtime are not verified here.",
        "No complete family/cusp cover or curvature closure is asserted.",
        "-/",
        "",
        "namespace MUB.SzollosiGaugedReflection",
        "open SzollosiGaugedCover SzollosiGaugedExecutable SzollosiNativeReflection",
        "open SzollosiColumnGauge SzollosiQuadraticSystem SzollosiTwoCirculant",
        "open SzollosiExecutableSystem SzollosiTermExpansion SzollosiIntervalExclusion",
        "",
        "set_option maxRecDepth 30000",
        "set_option maxHeartbeats 10000000",
        "",
        f"-- Native inspection SHA-256: {hashlib.sha256(raw).hexdigest()}",
        f"-- Native exclusion SHA-256: {hashlib.sha256(box_raw).hexdigest()}",
        f"-- Native parent SHA-256: {hashlib.sha256(root_raw).hexdigest()}",
        f"-- Lean coefficient SHA-256: {hashlib.sha256(coeff_raw).hexdigest()}",
        "",
        "def extraTerms : List (List CodedTerm) := [",
    ]
    for index, row in enumerate(reference[618:], start=618):
        exact_keys(row, {"index", "terms"})
        integer(row["index"], index)
        terms = []
        for term in row["terms"]:
            exact_keys(term, {"coefficient", "factors"})
            factors = term["factors"]
            if (
                not isinstance(factors, list)
                or len(factors) > 2
                or any(not 0 <= integer(n) < 440 for n in factors)
            ):
                raise ValueError("coefficient support")
            terms.append(
                f"({rational_literal(term['coefficient'])},[{','.join(map(str, factors))}])"
            )
        lines.append("  [" + ",".join(terms) + "]" + ("," if index < 665 else ""))
    lines += ["]", "", "def nativeBounds : List (Rat × Rat) := ["]
    for index, row in enumerate(bounds):
        exact_keys(row, {"index", "lo", "hi"})
        integer(row["index"], index)
        lines.append(
            f"  ({rational_literal(row['lo'])},{rational_literal(row['hi'])})"
            + ("," if index < 439 else "")
        )
    image = box["images"][368]
    exact_keys(image, {"index", "lo", "hi"})
    integer(image["index"], 368)
    lines += [
        "]",
        "",
        f"def nativeImage : Bounds := ⟨{rational_literal(image['lo'])},{rational_literal(image['hi'])}⟩",
        "",
    ]
    witness = list(box["request"]["center"])
    witness[:8] = ["1", "0", "-1", "0", "1", "0", "0", "1"]
    lines += [
        "def nativeWitnessValues : List Rat := ["
        + ",".join(rational_literal(q) for q in witness)
        + "]",
        PROOFS,
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inspection", required=True, type=Path)
    parser.add_argument("--exclusion", required=True, type=Path)
    parser.add_argument("--coefficients", required=True, type=Path)
    parser.add_argument("--root-receipt", required=True, type=Path)
    parser.add_argument("--system", required=True, type=Path)
    parser.add_argument("--request", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    sources = (
        args.inspection,
        args.exclusion,
        args.coefficients,
        args.root_receipt,
        args.system,
        args.request,
    )
    if args.output.resolve() in {path.resolve() for path in sources}:
        parser.error("output must differ from every input")
    result = format_receipt(*sources)
    args.output.write_bytes(result.encode("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
