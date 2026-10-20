"""Prepare the next holonomy admission candidate outside the active Cargo source tree.

AuthorityEffect: None. No live source replacement or scoring promotion.
"""
from datetime import datetime, timezone
from pathlib import Path as _FilesystemPath
import sys as _contract_sys
_contract_sys.path.insert(0, str(_FilesystemPath(__file__).resolve().parents[4] / "scripts"))
from contract_scores import RecordPath as Path, copy_file as _copy_record_file
from replay import ROOT, RUST, digest, write


def replace_once(text, before, after):
    assert text.count(before) == 1, before
    return text.replace(before, after, 1)


def main():
    out = ROOT / "evidence/quality/l4a_six" / (datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-holonomy-matrix-candidate")
    out.mkdir()
    names = ["matrix.rs", "Cargo.toml", "laplacian.rs", "gauge_fixing.rs", "tests/matrix_contracts.rs"]
    originals = {name: (RUST / "src/holonomy" / name).read_bytes() for name in names}
    source = originals["matrix.rs"].decode("utf8").replace("\r\n", "\n")
    source = replace_once(source, "use num_traits::{One, Zero};", "use num_traits::{One, Zero};\nuse num_integer::Integer;")
    source = replace_once(source,
        "    fn conjugate(&self) -> Self {\n        self.clone()\n    }",
        "    fn conjugate_admitted(value: ScalarRef<'_, Self>) -> Self {\n        value.value.clone()\n    }")
    source = replace_once(source,
        "        let reduced = self.reduced();\n        if self.numer() != reduced.numer() || self.denom() != reduced.denom() {",
        "        if !self.numer().gcd(self.denom()).is_one() {")
    source = replace_once(source,
        "    pub fn conjugate_eq(self, rhs: Self) -> bool {\n        T::conjugate_eq_admitted(self, rhs)\n    }",
        "    pub fn conjugate_eq(self, rhs: Self) -> bool {\n        T::conjugate_eq_admitted(self, rhs)\n    }\n    /// Conjugate only after exact-domain admission.\n    pub fn conjugate(self) -> T {\n        T::conjugate_admitted(self)\n    }")
    source = replace_once(source,
        "    fn conjugate(&self) -> Self {\n        Self {\n            re: self.re.clone(),\n            im: -self.im.clone(),\n        }\n    }",
        "    fn conjugate_admitted(value: ScalarRef<'_, Self>) -> Self {\n        Self {\n            re: value.value.re.clone(),\n            im: -value.value.im.clone(),\n        }\n    }")
    source = replace_once(source,
        "                data.push(self.at(r, c).conjugate());",
        "                data.push(T::conjugate_admitted(ScalarRef { value: self.at(r, c) }));")
    source = replace_once(source, "            tr += self.at(i, i).clone();",
        "            tr = add_ref(&tr, self.at(i, i));")
    marker = "pub struct ScalarRef<'a, T: ExactScalar> {"
    source = replace_once(source, marker,
        "/// Raw rationals cannot invoke conjugation without admission:\n"
        "/// ```compile_fail\n"
        "/// use num_rational::BigRational;\n"
        "/// use tfqm_holonomy::ExactScalar;\n"
        "/// let raw = BigRational::new_raw(1.into(), 0.into());\n"
        "/// let _ = raw.conjugate();\n"
        "/// ```\n" + marker)
    candidates = {"matrix.rs": source}
    cargo = originals["Cargo.toml"].decode("utf8").replace("\r\n", "\n")
    candidates["Cargo.toml"] = replace_once(cargo, 'num-traits = "0.2.19"',
        'num-traits = "0.2.19"\nnum-integer = "0.1.46"')
    laplacian = originals["laplacian.rs"].decode("utf8").replace("\r\n", "\n")
    candidates["laplacian.rs"] = replace_once(laplacian,
        "            sum += psi[r].conjugate() * row_acc;",
        "            sum += crate::matrix::ScalarRef::try_new(&psi[r])?.conjugate() * row_acc;")
    gauge = originals["gauge_fixing.rs"].decode("utf8").replace("\r\n", "\n")
    candidates["gauge_fixing.rs"] = replace_once(gauge,
        "                    value += d.get(row, i)?.conjugate()",
        "                    value += d.get_scalar(row, i)?.conjugate()")
    tests = originals["tests/matrix_contracts.rs"].decode("utf8").replace("\r\n", "\n")
    tests = replace_once(tests, "                    assert_eq!(m.determinant(), Ok(q(determinant)));",
        "                    assert_eq!(m.trace(), Ok(q(a + d)));\n                    assert_eq!(m.determinant(), Ok(q(determinant)));")
    candidates["tests/matrix_contracts.rs"] = tests + '''
#[test]
fn conjugation_requires_admitted_coefficients_and_preserves_exact_coordinates() {
    for raw in [BigRational::new_raw(1.into(), 0.into()),
                BigRational::new_raw(1.into(), (-1).into()),
                BigRational::new_raw(2.into(), 2.into())] {
        assert!(ScalarRef::try_new(&raw).is_err());
    }
    let real = BigRational::new((-2).into(), 3.into());
    assert_eq!(ScalarRef::try_new(&real).unwrap().conjugate(), real);
    let complex = GaussianRational::new(q(2), q(3)).unwrap();
    let conjugate = ScalarRef::try_new(&complex).unwrap().conjugate();
    assert_eq!(conjugate.real(), &q(2));
    assert_eq!(conjugate.imag(), &q(-3));
    assert_eq!(ScalarRef::try_new(&conjugate).unwrap().conjugate(), complex);
}
'''
    for name in names:
        saved = out / "before" / name
        saved.parent.mkdir(parents=True, exist_ok=True)
        saved.write_bytes(originals[name])
        candidate = out / "candidate" / name
        candidate.parent.mkdir(parents=True, exist_ok=True)
        candidate.write_bytes(candidates[name].encode("utf8"))
    write(out / "candidate.json", {"AuthorityEffect": "None", "status": "staged_not_activated_or_graded",
        "origins": {"code/rust/src/holonomy/" + name: digest(out / "before" / name) for name in names},
        "candidates": {name: digest(out / "candidate" / name) for name in names},
        "scope": "Borrowed GCD domain admission, admitted conjugation API, borrowed trace and three real consumer/test adaptations. Full candidate execution, fault replay, resource review and integration remain required."})
    print(out, flush=True)


if __name__ == "__main__":
    main()
