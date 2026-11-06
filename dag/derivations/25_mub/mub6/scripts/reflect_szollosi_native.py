"""Format the exact native replay data as kernel-checked Lean literals.

AuthorityEffect: None. This script validates wire shape and byte custody. It
performs no contractor, polynomial normalization or interval certification.
The generated Lean equalities and semantic theorems carry those checks.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from pathlib import Path

PROOFS = """
def termKey (t : CodedTerm) : Int × Nat × List Nat := (t.1.num,t.1.den,t.2)
theorem term_key_injective : Function.Injective termKey := by
  intro a b h
  have hn := congrArg Prod.fst h
  have hd := congrArg (fun z : Int × Nat × List Nat => z.2.1) h
  have hf := congrArg (fun z : Int × Nat × List Nat => z.2.2) h
  exact Prod.ext (Rat.ext hn hd) hf

theorem map_injective {α β : Type} (f : α → β) (hf : Function.Injective f) :
    Function.Injective (List.map f) := by
  intro as bs h
  induction as generalizing bs with
  | nil =>
    cases bs with
    | nil => rfl
    | cons b bs => simp at h
  | cons a as ih =>
    cases bs with
    | nil => simp at h
    | cons b bs =>
      simp only [List.map_cons,List.cons.injEq] at h
      exact congrArg₂ List.cons (hf h.1) (ih h.2)

def tableKeys (ts : List (List CodedTerm)) := ts.map (List.map termKey)
theorem table_keys_injective : Function.Injective tableKeys :=
  map_injective _ (map_injective _ term_key_injective)

def nativeCoefficientCheck : Bool := tableKeys nativeTerms == tableKeys (equations.map normalizedEquation)

theorem native_coefficients_checked : nativeCoefficientCheck = true := by decide +kernel

theorem native_terms_match : nativeTerms = equations.map normalizedEquation :=
  table_keys_injective (beq_iff_eq.mp native_coefficients_checked)

theorem equation_lookup (e : Equation) : equations[equationCode e]? = some e := by
  have h : (equations.map equationCode)[equationCode e]? = some (equationCode e) := by
    rw [equation_codes]
    simp [equationCode_lt e]
  rw [List.getElem?_map] at h
  cases hg : equations[equationCode e]? with
  | none => simp [hg] at h
  | some d =>
    have hc : equationCode d = equationCode e := by simpa [hg] using h
    have hd := equationCode_injective hc
    simp [hd]

def nativeCoefficients (e : Equation) : List CodedTerm := (nativeTerms[equationCode e]?).getD []

theorem native_coefficients_eq (e : Equation) : nativeCoefficients e = normalizedEquation e := by
  simp only [nativeCoefficients,native_terms_match,List.getElem?_map,equation_lookup,
    Option.map_some,Option.getD_some]

theorem native_coefficients_polynomial (e : Equation) :
    codedListPolynomial (nativeCoefficients e) =
      MvPolynomial.rename variableCode (equationPolynomial e) := by
  rw [native_coefficients_eq,normalized_equation_polynomial]

theorem variable_lookup (v : Variable) : allVariables[variableCode v]? = some v := by
  have h : (allVariables.map variableCode)[variableCode v]? = some (variableCode v) := by
    rw [variable_codes]
    simp [variableCode_lt v]
  rw [List.getElem?_map] at h
  cases hg : allVariables[variableCode v]? with
  | none => simp [hg] at h
  | some w =>
    have hc : variableCode w = variableCode v := by simpa [hg] using h
    have hw := variableCode_injective hc
    simp [hw]

def codedFullBox (n : Nat) : Bounds := ((allVariables.map fullBox)[n]?).getD (Bounds.point 0)

noncomputable def codedPoint (r : Variable → ℝ) (n : Nat) : ℝ :=
  ((allVariables.map r)[n]?).getD 0

theorem coded_point_code (r : Variable → ℝ) (v : Variable) :
    codedPoint r (variableCode v) = r v := by
  simp only [codedPoint,List.getElem?_map,variable_lookup,Option.map_some,Option.getD_some]

theorem coded_point_in_box (r : Variable → ℝ) (hr : ∀ v, (fullBox v).Contains (r v)) :
    ∀ n, (codedFullBox n).Contains (codedPoint r n) := by
  intro n
  simp only [codedFullBox,codedPoint,List.getElem?_map]
  cases hg : allVariables[n]? with
  | none => simp [Bounds.Contains,Bounds.point]
  | some v => simpa only [Option.map_some,Option.getD_some] using hr v

theorem coded_eval_rename (r : Variable → ℝ) (p : QPoly) :
    codedEval (codedPoint r) (MvPolynomial.rename variableCode p) = realEval r p := by
  simp only [codedEval,realEval,MvPolynomial.eval₂Hom_rename]
  have h : codedPoint r ∘ variableCode = r := funext (coded_point_code r)
  rw [h]

def boundsKey (b : Bounds) : Int × Nat × Int × Nat := (b.lo.num,b.lo.den,b.hi.num,b.hi.den)

theorem bounds_key_injective : Function.Injective boundsKey := by
  intro a b h
  have hlo := Rat.ext (congrArg Prod.fst h) (congrArg (fun z : Int × Nat × Int × Nat => z.2.1) h)
  have hhi := Rat.ext (congrArg (fun z : Int × Nat × Int × Nat => z.2.2.1) h)
    (congrArg (fun z : Int × Nat × Int × Nat => z.2.2.2) h)
  cases a
  cases b
  cases hlo
  cases hhi
  rfl

def nativeRangeCheck : Bool := nativeRanges.map boundsKey == (nativeTerms.map (listRange codedFullBox)).map boundsKey

theorem native_ranges_checked : nativeRangeCheck = true := by decide +kernel

theorem native_ranges_match : nativeRanges = nativeTerms.map (listRange codedFullBox) :=
  map_injective _ bounds_key_injective (beq_iff_eq.mp native_ranges_checked)

def nativeInterval (e : Equation) : Bounds := (nativeRanges[equationCode e]?).getD (Bounds.point 0)

theorem native_interval_eq (e : Equation) :
    nativeInterval e = listRange codedFullBox (nativeCoefficients e) := by
  simp only [nativeInterval,native_ranges_match,List.getElem?_map,native_terms_match,
    equation_lookup,Option.map_some,Option.getD_some,native_coefficients_eq]

/-- Each emitted interval encloses the actual rational quartet equation. -/
theorem native_interval_enclosed (r : Variable → ℝ)
    (hr : ∀ v, (fullBox v).Contains (r v)) (e : Equation) :
    (nativeInterval e).Contains (realEval r (equationPolynomial e)) := by
  have h := polynomial_enclosed codedFullBox (codedPoint r)
    (coded_point_in_box r hr) (nativeCoefficients e)
  rw [native_coefficients_polynomial,coded_eval_rename] at h
  rwa [native_interval_eq]

/-- The current full containing-box computation has no zero-excluding row. -/
theorem native_full_box_unresolved : nativeRanges.all (fun b => !b.excludesZero) = true := by decide +kernel

/-- Actual solutions, if any, give zero in every emitted full-box interval. -/
theorem solution_zero_in_native_interval (r : Variable → ℝ)
    (h : ∀ e, realEval r (equationPolynomial e) = 0) (e : Equation) :
    (nativeInterval e).Contains 0 := by
  simpa only [h e] using native_interval_enclosed r (solution_in_fullBox r h) e

#print axioms native_terms_match
#print axioms native_coefficients_polynomial
#print axioms native_ranges_match
#print axioms native_interval_enclosed
#print axioms native_full_box_unresolved
#print axioms solution_zero_in_native_interval
end MUB.SzollosiNativeReflection
"""


def exact_keys(value: object, keys: set[str]) -> dict:
    if not isinstance(value, dict) or set(value) != keys:
        raise ValueError(f"expected exactly these keys: {sorted(keys)}")
    return value


def integer(value: object, expected: int | None = None) -> int:
    if type(value) is not int or (expected is not None and value != expected):
        raise ValueError("invalid integer field")
    return value


def rational_literal(value: object) -> str:
    if (
        not isinstance(value, str)
        or re.fullmatch(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?", value) is None
    ):
        raise ValueError("invalid rational wire text")
    parts = value.split("/")
    numerator = int(parts[0])
    denominator = int(parts[1]) if len(parts) == 2 else 1
    if (
        math.gcd(numerator, denominator) != 1
        or value == "-0"
        or (len(parts) == 2 and denominator == 1)
    ):
        raise ValueError("rational wire text is not canonical")
    return f"({value})"


def unique_object(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON field: {key}")
        result[key] = value
    return result


def read_json(path: Path) -> tuple[bytes, object]:
    raw = path.read_bytes()
    if len(raw) > 8_000_000:
        raise ValueError("input exceeds the byte bound")
    return raw, json.loads(raw.decode("utf-8"), object_pairs_hook=unique_object)


def format_receipt(receipt: Path, system: Path, coefficients: Path) -> str:
    raw, data = read_json(receipt)
    system_raw, system_data = read_json(system)
    reference_raw, reference = read_json(coefficients)
    if not isinstance(data, dict) or data.get("schema") != "omega.mub6.szollosi-native-replay.v1":
        raise ValueError("wrong native receipt schema")
    if data.get("input_sha256") != hashlib.sha256(system_raw).hexdigest():
        raise ValueError("system byte binding mismatch")
    if data.get("coefficient_reference_sha256") != hashlib.sha256(reference_raw).hexdigest():
        raise ValueError("coefficient byte binding mismatch")
    for field, count in [
        ("variable_count", 440),
        ("equation_count", 618),
        ("checked_coefficient_rows", 618),
    ]:
        integer(data.get(field), count)
    if (
        not isinstance(system_data, dict)
        or system_data.get("schema") != "omega.mub6.szollosi-expressions.v1"
    ):
        raise ValueError("wrong executable system schema")
    if data.get("coefficients") != reference:
        raise ValueError("native coefficients differ from the independent Lean export")
    rows = data["coefficients"]
    intervals = data.get("intervals")
    if (
        not isinstance(rows, list)
        or len(rows) != 618
        or not isinstance(intervals, list)
        or len(intervals) != 618
    ):
        raise ValueError("incomplete coefficient or interval rows")
    term_rows = []
    count = 0
    for index, row in enumerate(rows):
        exact_keys(row, {"index", "terms"})
        integer(row["index"], index)
        if not isinstance(row["terms"], list):
            raise ValueError("terms must be a list")
        terms = []
        previous_key = None
        for term in row["terms"]:
            exact_keys(term, {"coefficient", "factors"})
            coefficient = rational_literal(term["coefficient"])
            factors = term["factors"]
            if term["coefficient"] == "0" or not isinstance(factors, list) or len(factors) > 2:
                raise ValueError("invalid sparse term")
            for factor in factors:
                if not 0 <= integer(factor) < 440:
                    raise ValueError("variable index out of range")
            key = tuple(factors)
            if list(key) != sorted(key) or (previous_key is not None and previous_key >= key):
                raise ValueError("sparse factors or terms are not ordered")
            previous_key = key
            terms.append(f"({coefficient},[{','.join(map(str, factors))}])")
        count += len(terms)
        term_rows.append("  [" + ",".join(terms) + "]")
    integer(data.get("sparse_terms"), count)
    range_rows = []
    for index, row in enumerate(intervals):
        exact_keys(row, {"index", "lo", "hi"})
        integer(row["index"], index)
        range_rows.append(f"  ⟨{rational_literal(row['lo'])},{rational_literal(row['hi'])}⟩")
    header = """import SzollosiNativeInterval

/-!
# Reflection of the emitted native coefficient and interval data

AuthorityEffect: None.

The formatter supplies literals. Kernel reduction checks every coefficient and
interval row against the executable Lean definitions. Semantic theorems bind
these rows to all actual polynomial values in the full containing box.
The current intervals exclude no row from zero. No complete cell/cusp cover,
Krawczyk contraction, deltoid transport or variety emptiness is supplied here.
-/

namespace MUB.SzollosiNativeReflection
open SzollosiTermExpansion SzollosiExecutableSystem SzollosiQuadraticSystem
open SzollosiIntervalExclusion SzollosiNativeInterval

set_option maxRecDepth 30000
set_option maxHeartbeats 10000000

"""
    header += f"-- Native receipt SHA-256: {hashlib.sha256(raw).hexdigest()}\n"
    header += f"-- Executable system SHA-256: {hashlib.sha256(system_raw).hexdigest()}\n"
    header += (
        f"-- Lean coefficient reference SHA-256: {hashlib.sha256(reference_raw).hexdigest()}\n"
    )
    row_definitions = "\n".join(
        f"private def nativeTermsRow{index} : List CodedTerm := {row.strip()}"
        for index, row in enumerate(term_rows)
    )
    row_names = ",\n".join(f"  nativeTermsRow{index}" for index in range(len(term_rows)))
    return (
        header
        + row_definitions
        + "\n\ndef nativeTerms : List (List CodedTerm) := [\n"
        + row_names
        + "\n]\n\ndef nativeRanges : List Bounds := [\n"
        + ",\n".join(range_rows)
        + "\n]\n"
        + PROOFS
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--system", type=Path, required=True)
    parser.add_argument("--coefficients", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    if output in {args.receipt.resolve(), args.system.resolve(), args.coefficients.resolve()}:
        raise ValueError("output aliases an input")
    text = format_receipt(args.receipt, args.system, args.coefficients)
    output.write_bytes(text.encode("utf-8"))
    print(f"Wrote reflected data: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
