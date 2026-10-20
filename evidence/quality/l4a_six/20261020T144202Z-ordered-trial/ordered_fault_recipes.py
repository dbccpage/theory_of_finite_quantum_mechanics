"""Designated ordered candidate faults. AuthorityEffect: None."""
from scalar_port_faults import block


def recipes(source):
    result = []
    def add(identity, prefix, before, after, target="lib"):
        original = block(source, prefix)
        assert original.count(before) == 1, identity
        result.append({"id": identity, "before": original,
            "after": original.replace(before, after, 1), "target": target, "outcome": "unrun"})
    add("OD01-count-privacy", "pub struct Inertia {", "    positive: usize,\n    negative: usize,\n    zero: usize,",
        "    pub positive: usize,\n    pub negative: usize,\n    pub zero: usize,", "doc")
    add("OD02-count-admission", "    pub fn try_new(",
        ".ok_or(InertiaCountError::DimensionOverflow)?;", ".unwrap_or(0);")
    add("OD03-dimension-count", "    pub fn dimension(&self)",
        "self.positive + self.negative + self.zero", "self.positive + self.negative")
    add("OD04-rank-count", "    pub fn rank(&self)",
        "self.positive + self.negative", "self.positive")
    add("OD05-sign-range", "fn validated_sign(",
        "if !(-1..=1).contains(&sign) {", "if false {")
    add("OD06-sign-zero-consistency", "fn validated_sign(",
        "if (sign == 0) != is_zero {", "if false {")
    add("OD07-negative-pivot", "    fn step(",
        "Ordering::Less => Ok(Some(self.negative_pivot(column, conj)?)),", "Ordering::Less => Ok(None),")
    add("OD08-zero-column", "    fn zero_pivot_column(",
        "if !schur.try_is_zero()? {", "if schur.try_is_zero()? {")
    add("OD09-zero-witness-sign", "fn zero_pivot_coefficient<",
        "diagonal.try_add(&F::one())?.try_neg()?.try_mul(&inverse)?",
        "diagonal.try_add(&F::one())?.try_mul(&inverse)?")
    add("OD10-coupling-conjugation", "    fn coupling(",
        ".try_mul(&conj(self.lower.at(j, k))?)?", ".try_mul(self.lower.at(j, k))?")
    add("OD11-workspace-admission", "fn admit_ldl_workspace(",
        "        limits,", "        OperationLimits::UNLIMITED,")
    add("OD12-positive-column", "    fn positive_pivot_column(",
        ".try_mul(&inverse)?", ".try_add(&inverse)?")
    add("OD13-coupling-sign", "    fn coupling(", "sum = sum.try_add(", "sum = sum.try_sub(")
    add("OD14-zero-inertia", "fn count_signs<",
        "Ordering::Equal => inertia.zero += 1,", "Ordering::Equal => inertia.positive += 1,")
    add("OD15-negative-witness", "    fn negative_pivot(",
        "&[(column, F::one())]", "&[(column, F::zero())]")
    add("OD16-pivot-storage", "    fn step(",
        "self.pivots[column] = self.schur(a, column, column, conj)?;",
        "let _ignored_pivot = self.schur(a, column, column, conj)?;")
    assert len({entry["id"] for entry in result}) == len(result) == 16
    return result
