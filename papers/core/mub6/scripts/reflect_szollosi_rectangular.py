"""Format native rectangular data for exact Lean kernel checks.

AuthorityEffect: None. Python checks wire shape and byte custody only. The
emitted Lean declarations check coefficients, Jacobian bounds and images.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from reflect_szollosi_native import exact_keys, integer, rational_literal, read_json

PROOFS = r"""
def ratKey (q : Rat) : Int × Nat := (q.num,q.den)
def nativeCenter : Nat → Rat := fun _ => 0
def weightRows (i : Nat) := (nativeWeights[i]?).getD []
def activeEquations (i : Nat) : Finset Nat := ((weightRows i).map Prod.fst).toFinset
def nativeWeight (i e : Nat) : Rat := ((weightRows i).lookup e).getD 0
def expectedImage (i : Nat) : Bounds :=
  imageOn (usedCoordinates rows (activeEquations i) i) (activeEquations i)
    rows codedFullBox nativeCenter nativeWeight i
def nativeImage (i : Nat) : Bounds := (nativeImages[i]?).getD (Bounds.point 0)
def nativeRetainedBox (i : Nat) : Bounds := (nativeRetained[i]?).getD (Bounds.point 0)

def inputCheck : Bool := nativeInputs.map boundsKey == (List.range 440).map (boundsKey ∘ codedFullBox)
theorem native_inputs_checked : inputCheck = true := by decide +kernel
def centerCheck : Bool := nativeCenters.map ratKey == (List.replicate 440 (0 : Rat)).map ratKey
theorem native_center_checked : centerCheck = true := by decide +kernel
def residualCheck : Bool := nativeResiduals.map (boundsKey ∘ Bounds.point) ==
  (List.range 618).map (fun e => boundsKey (listRange (fun _ => Bounds.point 0) (rows e)))
theorem native_residuals_checked : residualCheck = true := by decide +kernel

def expectedJacobian : List (List (Nat × Bounds)) :=
  (List.range 618).map expectedJacobianRow

theorem native_jacobian_eq : nativeJacobian = expectedJacobian := by
  rw [native_jacobian_literal_eq,jacobian_indices_checked]
  rfl

def jacobianCheck : Bool := jacKeys nativeJacobian == jacKeys expectedJacobian
theorem native_jacobian_checked : jacobianCheck = true := by
  simp [jacobianCheck,native_jacobian_eq]

theorem native_jacobian_row (e : Nat) (he : e<618) :
    (nativeJacobian[e]?).getD [] =
      (supportList (rows e)).map
        (fun k => (k, RectangularQuadraticExclusion.listGradient codedFullBox (rows e) k)) := by
  simp [native_jacobian_eq,expectedJacobian,expectedJacobianRow,he]

theorem native_jacobian_entry_eq (e : Nat) (he : e<618) (p : Nat × Bounds)
    (hp : p∈(nativeJacobian[e]?).getD []) :
    p.2 = RectangularQuadraticExclusion.listGradient codedFullBox (rows e) p.1 := by
  rw [native_jacobian_row e he] at hp
  obtain ⟨k,_,hk⟩ := List.mem_map.mp hp
  cases hk
  rfl

/-- Every emitted support entry bounds an actual formal quartet derivative. -/
theorem native_jacobian_entry_enclosed (r : Variable → ℝ)
    (hr : ∀ v, (fullBox v).Contains (r v)) (e : Equation) (p : Nat × Bounds)
    (hp : p∈(nativeJacobian[equationCode e]?).getD []) :
    p.2.Contains (codedEval (codedPoint r)
      (MvPolynomial.pderiv p.1 (MvPolynomial.rename variableCode (equationPolynomial e)))) := by
  rw [native_jacobian_entry_eq (equationCode e) (equationCode_lt e) p hp]
  exact derivative_enclosed r hr e p.1

def imageCheck : Bool := nativeImages.map boundsKey == (List.range 440).map (boundsKey ∘ expectedImage)
theorem native_images_checked : imageCheck = true := by decide +kernel
theorem native_images_eq : nativeImages = (List.range 440).map expectedImage :=
  map_injective _ bounds_key_injective (beq_iff_eq.mp native_images_checked)
theorem native_image_eq (i : Nat) (hi : i<440) : nativeImage i = expectedImage i := by
  simp [nativeImage,native_images_eq,hi]

def intersectBounds (a b : Bounds) : Bounds := ⟨max a.lo b.lo,min a.hi b.hi⟩
def retainedCheck : Bool := nativeRetained.map boundsKey ==
  (List.range 440).map (fun i => boundsKey (intersectBounds (codedFullBox i) (nativeImage i)))
theorem native_retained_checked : retainedCheck = true := by decide +kernel
theorem native_retained_eq : nativeRetained =
    (List.range 440).map (fun i => intersectBounds (codedFullBox i) (nativeImage i)) :=
  map_injective _ bounds_key_injective (beq_iff_eq.mp native_retained_checked)
theorem intersect_contains (a b : Bounds) (x : ℝ) (ha : a.Contains x) (hb : b.Contains x) :
    (intersectBounds a b).Contains x := by
  rcases ha with ⟨ha1,ha2⟩
  rcases hb with ⟨hb1,hb2⟩
  change ((max a.lo b.lo : Rat):ℝ) ≤ x ∧ x ≤ ((min a.hi b.hi : Rat):ℝ)
  rw [Rat.cast_max,Rat.cast_min]
  exact ⟨max_le ha1 hb1,le_min ha2 hb2⟩

theorem zero_center_in_box : ∀ n, (codedFullBox n).Contains (nativeCenter n : ℝ) := by
  intro n
  simp only [codedFullBox,List.getElem?_map,nativeCenter]
  cases hg : allVariables[n]? with
  | none => simp [Bounds.Contains,Bounds.point]
  | some v =>
    rcases v with p | (p | p) <;>
      norm_num [Bounds.Contains,fullBox,eRadius]

/-- Every actual system zero remains in every emitted rectangular image. -/
theorem solution_in_native_image (r : Variable → ℝ)
    (hz : ∀ e, realEval r (equationPolynomial e)=0) (i : Nat) (hi : i<440) :
    (nativeImage i).Contains (codedPoint r i) := by
  rw [native_image_eq i hi]
  apply root_in_used_image (activeEquations i) rows codedFullBox nativeCenter nativeWeight
    (codedPoint r) zero_center_in_box (coded_point_in_box r (solution_in_fullBox r hz))
  · intro e _ t ht
    exact (rows_shape e t ht).1
  · intro e _
    exact rows_zero_of_solution r hz e

/-- Actual system zeros remain in the intersection recorded by the native run. -/
theorem solution_in_native_retained (r : Variable → ℝ)
    (hz : ∀ e, realEval r (equationPolynomial e)=0) (i : Nat) (hi : i<440) :
    (nativeRetainedBox i).Contains (codedPoint r i) := by
  have h := intersect_contains (codedFullBox i) (nativeImage i) (codedPoint r i)
    (coded_point_in_box r (solution_in_fullBox r hz) i) (solution_in_native_image r hz i hi)
  simpa [nativeRetainedBox,native_retained_eq,hi] using h

def contractedCoordinates : List Nat := (List.range 440).filter fun i =>
  boundsKey (nativeRetainedBox i) != boundsKey (codedFullBox i)
theorem native_contracted_coordinates_checked : contractedCoordinates = recordedContracted := by decide +kernel
/-- This run does not narrow either additional basis's raw coordinates. -/
theorem native_additional_bases_unchanged :
    (List.range 144).all (fun n =>
      boundsKey (nativeRetainedBox (80+n)) == boundsKey (codedFullBox (80+n))) = true := by decide +kernel

def overlaps (a b : Bounds) : Bool := decide (a.lo ≤ b.hi ∧ b.lo ≤ a.hi)
theorem native_images_have_no_separation :
    (List.range 440).all (fun i => overlaps (codedFullBox i) (nativeImage i)) = true := by decide +kernel

#print axioms native_inputs_checked
#print axioms native_residuals_checked
#print axioms native_jacobian_eq
#print axioms native_jacobian_entry_enclosed
#print axioms native_images_eq
#print axioms solution_in_native_image
#print axioms solution_in_native_retained
#print axioms native_contracted_coordinates_checked
#print axioms native_additional_bases_unchanged
#print axioms native_images_have_no_separation
end MUB.SzollosiRectangularReflection
"""


PRELUDE = "def jacEntryKey (p : Nat × Bounds) := (p.1,boundsKey p.2)\ndef jacKeys (table : List (List (Nat × Bounds))) := table.map (List.map jacEntryKey)\ntheorem jac_entry_key_injective : Function.Injective jacEntryKey := by\n  intro a b h\n  change (a.1,boundsKey a.2) = (b.1,boundsKey b.2) at h\n  exact Prod.ext (congrArg (fun z : Nat × (Int × Nat × Int × Nat) => z.1) h) (bounds_key_injective (congrArg (fun z : Nat × (Int × Nat × Int × Nat) => z.2) h))\ntheorem jac_keys_injective : Function.Injective jacKeys :=\n  map_injective _ (map_injective _ jac_entry_key_injective)\ndef supportList (ts : List CodedTerm) : List Nat :=\n  (List.insertionSort (· ≤ ·) (ts.flatMap Prod.snd)).eraseDups\n\ntheorem support_list_mem (ts : List CodedTerm) (k : Nat) :\n    k∈supportList ts ↔ k∈coordinateSupport ts := by\n  simp [supportList,coordinateSupport]\n\ndef expectedJacobianRow (e : Nat) : List (Nat × Bounds) :=\n  (supportList (rows e)).map fun k =>\n    (k, RectangularQuadraticExclusion.listGradient codedFullBox (rows e) k)\n\n"


def ordered_rows(value: object, count: int) -> list:
    if not isinstance(value, list) or len(value) != count:
        raise ValueError("incomplete ordered rows")
    for index, row in enumerate(value):
        if not isinstance(row, dict):
            raise ValueError("row is not an object")
        integer(row.get("index"), index)
    return value


def interval(row: object, index: int) -> str:
    exact_keys(row, {"index", "lo", "hi"})
    integer(row["index"], index)
    return f"⟨{rational_literal(row['lo'])},{rational_literal(row['hi'])}⟩"


def format_receipt(
    receipt: Path, system: Path, coefficients: Path, request: Path
) -> tuple[str, dict[str, str]]:
    raw, data = read_json(receipt)
    system_raw, ast = read_json(system)
    coeff_raw, _ = read_json(coefficients)
    request_raw, req = read_json(request)
    fields = {
        "schema",
        "status",
        "input_sha256",
        "coefficient_reference_sha256",
        "request_sha256",
        "checked_coefficient_rows",
        "nonzero_preconditioner_entries",
        "request",
        "center_residuals",
        "jacobian",
        "images",
        "intersections",
        "excluded_coordinate",
        "contracted_coordinates",
        "root_existence_claimed",
        "full_56_cell_and_cusp_calculation_complete",
        "kernel_reflection_complete",
    }
    exact_keys(data, fields)
    if (
        data["schema"] != "omega.mub6.rectangular-replay.v1"
        or data["status"] != "CONTRACTED_UNRESOLVED_BOX"
    ):
        raise ValueError("wrong receipt schema or status")
    for field, content in [
        ("input_sha256", system_raw),
        ("coefficient_reference_sha256", coeff_raw),
        ("request_sha256", request_raw),
    ]:
        if data[field] != hashlib.sha256(content).hexdigest():
            raise ValueError(f"byte binding mismatch: {field}")
    integer(data["checked_coefficient_rows"], 618)
    for field in [
        "root_existence_claimed",
        "full_56_cell_and_cusp_calculation_complete",
        "kernel_reflection_complete",
    ]:
        if data[field] is not False:
            raise ValueError(f"unexpected runtime scope flag: {field}")
    if data["excluded_coordinate"] is not None or data["request"] != req:
        raise ValueError("unexpected exclusion or request body mismatch")
    exact_keys(
        req, {"schema", "variable_count", "equation_count", "bounds", "center", "preconditioner"}
    )
    if req["schema"] != "omega.mub6.rectangular-request.v1" or not isinstance(ast, dict):
        raise ValueError("invalid request or system")
    integer(req["variable_count"], 440)
    integer(req["equation_count"], 618)
    if ast.get("schema") != "omega.mub6.szollosi-expressions.v1" or req["bounds"] != ast.get("box"):
        raise ValueError("this reflection requires the actual full containing box")
    if req["center"] != ["0"] * 440:
        raise ValueError("this reflection requires the zero center")
    bounds = [interval(row, i) for i, row in enumerate(ordered_rows(req["bounds"], 440))]
    images = [interval(row, i) for i, row in enumerate(ordered_rows(data["images"], 440))]
    retained = [interval(row, i) for i, row in enumerate(ordered_rows(data["intersections"], 440))]
    centers = [rational_literal(q) for q in req["center"]]
    if not isinstance(data["center_residuals"], list) or len(data["center_residuals"]) != 618:
        raise ValueError("incomplete center residuals")
    residuals = [rational_literal(q) for q in data["center_residuals"]]
    weights = []
    count = 0
    for row in ordered_rows(req["preconditioner"], 440):
        exact_keys(row, {"index", "entries"})
        if not isinstance(row["entries"], list):
            raise ValueError("invalid preconditioner entries")
        entries = []
        previous = -1
        for entry in row["entries"]:
            exact_keys(entry, {"equation", "coefficient"})
            e = integer(entry["equation"])
            q = rational_literal(entry["coefficient"])
            if not previous < e < 618 or entry["coefficient"] == "0":
                raise ValueError("invalid sparse preconditioner")
            previous = e
            entries.append(f"({e},{q})")
        count += len(entries)
        weights.append("[" + ",".join(entries) + "]")
    integer(data["nonzero_preconditioner_entries"], count)
    jacrows = []
    for row in ordered_rows(data["jacobian"], 618):
        exact_keys(row, {"index", "entries"})
        if not isinstance(row["entries"], list):
            raise ValueError("invalid Jacobian entries")
        entries = []
        previous = -1
        for entry in row["entries"]:
            k = integer(entry.get("index"))
            if not previous < k < 440:
                raise ValueError("invalid Jacobian coordinate")
            previous = k
            entries.append(f"({k},{interval(entry, k)})")
        jacrows.append("[" + ",".join(entries) + "]")
    contracted = data["contracted_coordinates"]
    if not isinstance(contracted, list) or any(not 0 <= integer(i) < 440 for i in contracted):
        raise ValueError("invalid contracted coordinates")
    if contracted != sorted(set(contracted)):
        raise ValueError("contracted coordinates are not ordered")
    header = """import SparseRectangularExclusion
import SzollosiRectangularExclusion

/-!
# Kernel reflection of the actual native rectangular run

AuthorityEffect: None.

All 618 sparse Jacobian rows and 440 images are checked against the actual
quartet polynomial table and full containing box. Every actual system zero
remains in every recorded intersection. The run contracts 24 coordinates and
excludes none. Full 56-cell/cusp coverage and curvature remain open.
-/
namespace MUB.SzollosiRectangularReflection
open SzollosiTermExpansion SzollosiNativeInterval SzollosiIntervalExclusion
open SzollosiExecutableSystem SzollosiQuadraticSystem SzollosiNativeReflection
open SzollosiRectangularExclusion SparseRectangularExclusion
set_option maxRecDepth 30000
set_option maxHeartbeats 100000000

"""
    for label, content in [
        ("Native rectangular receipt", raw),
        ("Executable system", system_raw),
        ("Lean coefficient reference", coeff_raw),
        ("Native request", request_raw),
    ]:
        header += f"-- {label} SHA-256: {hashlib.sha256(content).hexdigest()}\n"
    generated = {
        "SzollosiRectangularJacobianCore.lean": header
        + PRELUDE
        + "\nend MUB.SzollosiRectangularReflection\n"
    }
    chunk_names = []
    for chunk, first in enumerate(range(0, 618, 80)):
        name = f"SzollosiRectangularJacobian{chunk}"
        chunk_names.append(name)
        content = "import SzollosiRectangularJacobianCore\n"
        content += header[header.index("namespace MUB.SzollosiRectangularReflection") :]
        for index in range(first, min(first + 80, 618)):
            content += f"""
def nativeJacobianRow{index} : List (Nat × Bounds) := {jacrows[index]}
theorem nativeJacobianRow{index}_eq :
    nativeJacobianRow{index} = expectedJacobianRow {index} := by
  apply map_injective _ jac_entry_key_injective
  apply beq_iff_eq.mp
  decide +kernel
"""
        generated[name + ".lean"] = content + "\nend MUB.SzollosiRectangularReflection\n"
    header = "\n".join("import " + name for name in chunk_names) + "\n" + header
    definitions = ""
    definitions += (
        "\n\ndef nativeJacobian : List (List (Nat × Bounds)) := [\n"
        + ",\n".join(f"  nativeJacobianRow{i}" for i in range(618))
        + "\n]\n"
    )
    definitions += "\ndef jacobianIndices : List Nat := [" + ",".join(map(str, range(618))) + "]\n"
    definitions += (
        """
theorem jacobian_indices_checked : jacobianIndices = List.range 618 := by decide +kernel
theorem native_jacobian_literal_eq :
    nativeJacobian = jacobianIndices.map expectedJacobianRow := by
  simp only [nativeJacobian,jacobianIndices,List.map_cons,List.map_nil,
"""
        + ",\n".join(f"    nativeJacobianRow{i}_eq" for i in range(618))
        + "]\n"
    )
    for name, typ, items in [
        ("nativeInputs", "Bounds", bounds),
        ("nativeCenters", "Rat", centers),
        ("nativeResiduals", "Rat", residuals),
        ("nativeWeights", "List (Nat × Rat)", weights),
        ("nativeImages", "Bounds", images),
        ("nativeRetained", "Bounds", retained),
    ]:
        definitions += (
            f"\ndef {name} : List ({typ}) := [\n"
            + ",\n".join("  " + item for item in items)
            + "\n]\n"
        )
    definitions += (
        "\ndef recordedContracted : List Nat := [" + ",".join(map(str, contracted)) + "]\n"
    )
    return header + definitions + PROOFS, generated


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ["receipt", "system", "coefficients", "request", "output"]:
        parser.add_argument("--" + name, type=Path, required=True)
    args = parser.parse_args()
    if args.output.resolve() in {
        args.receipt.resolve(),
        args.system.resolve(),
        args.coefficients.resolve(),
        args.request.resolve(),
    }:
        raise ValueError("output aliases an input")
    text, generated = format_receipt(args.receipt, args.system, args.coefficients, args.request)
    inputs = {
        args.receipt.resolve(),
        args.system.resolve(),
        args.coefficients.resolve(),
        args.request.resolve(),
    }
    targets = {args.output.parent / name: content for name, content in generated.items()}
    targets[args.output] = text
    if any(path.resolve() in inputs for path in targets):
        raise ValueError("generated output aliases an input")
    for path, content in targets.items():
        path.write_bytes(content.encode("utf-8"))
    print(f"Wrote reflected data: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
