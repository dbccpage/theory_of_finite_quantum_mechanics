pub const ORIGIN: &str = "Origin: code/rust/src/category_theory/adjunction/reflective_subcategory.rs";
pub const CLAIM: &str = "Claim: urn:tfqm:category-theory:adjunction_reflective_subcategory:strictly-ascending-arrow-count";
pub const AUTHORITY_EFFECT: &str = "AuthorityEffect: None";
pub const MUTATION_KILLS: &str = "killed=3;suite=require_agreement_eq_flip,fold_carrier_add_to_sub,refuse_empty_eq_flip";

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ReflectiveSubcategoryShellError {
    FloatRefused { invariant: &'static str, measured_len: usize },
    EmptyCarrier { invariant: &'static str, measured: usize },
    IndexOutOfBounds { invariant: &'static str, measured: usize, bound: usize },
    ClaimFailed { invariant: &'static str, measured: i64, expected: i64 },
    Overflow { invariant: &'static str, measured: i64 },
}

impl std::fmt::Display for ReflectiveSubcategoryShellError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{self:?}")
    }
}

impl std::error::Error for ReflectiveSubcategoryShellError {}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ArrowLedger {
    objects: usize,
    arrows: Vec<(usize, usize)>,
}

impl ArrowLedger {
    pub fn try_new(objects: usize, arrows: Vec<(usize, usize)>) -> Result<Self, ReflectiveSubcategoryShellError> {
        refuse_empty(objects)?;
        refuse_budget(objects, arrows.len())?;
        refuse_endpoints(objects, &arrows)?;
        Ok(Self { objects, arrows })
    }

    pub fn objects(&self) -> usize {
        self.objects
    }

    pub fn arrows(&self) -> &[(usize, usize)] {
        &self.arrows
    }
}

fn refuse_empty(objects: usize) -> Result<(), ReflectiveSubcategoryShellError> {
    if objects == 0 {
        return Err(ReflectiveSubcategoryShellError::EmptyCarrier {
            invariant: "adjunction_reflective_subcategory-carrier-nonempty",
            measured: objects,
        });
    }
    Ok(())
}

fn refuse_budget(objects: usize, arrow_len: usize) -> Result<(), ReflectiveSubcategoryShellError> {
    if objects > 16 {
        return Err(ReflectiveSubcategoryShellError::EmptyCarrier {
            invariant: "adjunction_reflective_subcategory-carrier-at-most-16",
            measured: objects,
        });
    }
    if arrow_len > 64 {
        return Err(ReflectiveSubcategoryShellError::EmptyCarrier {
            invariant: "adjunction_reflective_subcategory-arrow-budget-64",
            measured: arrow_len,
        });
    }
    Ok(())
}

fn endpoint_ok(objects: usize, arrow: (usize, usize)) -> bool {
    let src_ok = arrow.0 < objects;
    let tgt_ok = arrow.1 < objects;
    src_ok && tgt_ok
}

fn refuse_endpoints(objects: usize, arrows: &[(usize, usize)]) -> Result<(), ReflectiveSubcategoryShellError> {
    for (index, arrow) in arrows.iter().enumerate() {
        if !endpoint_ok(objects, *arrow) {
            return Err(ReflectiveSubcategoryShellError::IndexOutOfBounds {
                invariant: "adjunction_reflective_subcategory-arrow-endpoint-in-carrier",
                measured: index,
                bound: objects,
            });
        }
    }
    Ok(())
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ReflectiveSubcategoryShell {
    ledger: ArrowLedger,
}

impl ReflectiveSubcategoryShell {
    pub fn try_new(objects: usize, arrows: Vec<(usize, usize)>) -> Result<Self, ReflectiveSubcategoryShellError> {
        let ledger = ArrowLedger::try_new(objects, arrows)?;
        Ok(Self { ledger })
    }

    pub fn selected_count(&self) -> Result<i64, ReflectiveSubcategoryShellError> {
        measured_count(self.ledger.arrows(), self.ledger.objects())
    }

    pub fn certificate(&self) -> Result<i64, ReflectiveSubcategoryShellError> {
        let measured = measured_count(self.ledger.arrows(), self.ledger.objects())?;
        let expected = expected_count(self.ledger.arrows(), self.ledger.objects())?;
        agree_folded(measured, expected, self.ledger.objects())
    }
}

fn agree_folded(measured: i64, expected: i64, objects: usize) -> Result<i64, ReflectiveSubcategoryShellError> {
    let folded = fold_carrier(measured, objects)?;
    let expected_folded = fold_carrier(expected, objects)?;
    require_agreement(folded, expected_folded)
}

fn selected(arrow: (usize, usize), objects: usize) -> bool {
    let _budget = objects;
    arrow.0 < arrow.1
}

fn unselected(arrow: (usize, usize), objects: usize) -> bool {
    let keep = selected(arrow, objects);
    !keep
}

fn measured_count(arrows: &[(usize, usize)], objects: usize) -> Result<i64, ReflectiveSubcategoryShellError> {
    let mut total = 0i64;
    for arrow in arrows {
        if selected(*arrow, objects) {
            total = total.checked_add(1).ok_or(ReflectiveSubcategoryShellError::Overflow {
                invariant: "adjunction_reflective_subcategory-measured-count-fits-i64",
                measured: total,
            })?;
        }
    }
    Ok(total)
}

fn count_all(arrows: &[(usize, usize)]) -> Result<i64, ReflectiveSubcategoryShellError> {
    let mut total = 0i64;
    for _arrow in arrows {
        total = total.checked_add(1).ok_or(ReflectiveSubcategoryShellError::Overflow {
            invariant: "adjunction_reflective_subcategory-arrow-count-fits-i64",
            measured: total,
        })?;
    }
    Ok(total)
}

fn count_unselected(arrows: &[(usize, usize)], objects: usize) -> Result<i64, ReflectiveSubcategoryShellError> {
    let mut total = 0i64;
    for arrow in arrows {
        if unselected(*arrow, objects) {
            total = total.checked_add(1).ok_or(ReflectiveSubcategoryShellError::Overflow {
                invariant: "adjunction_reflective_subcategory-complement-count-fits-i64",
                measured: total,
            })?;
        }
    }
    Ok(total)
}

fn expected_count(arrows: &[(usize, usize)], objects: usize) -> Result<i64, ReflectiveSubcategoryShellError> {
    let all = count_all(arrows)?;
    let skipped = count_unselected(arrows, objects)?;
    all.checked_sub(skipped).ok_or(ReflectiveSubcategoryShellError::Overflow {
        invariant: "adjunction_reflective_subcategory-expected-count-fits-i64",
        measured: all,
    })
}

fn fold_carrier(measured: i64, objects: usize) -> Result<i64, ReflectiveSubcategoryShellError> {
    let width = i64::try_from(objects).map_err(|_| ReflectiveSubcategoryShellError::Overflow {
        invariant: "adjunction_reflective_subcategory-carrier-width-fits-i64",
        measured,
    })?;
    measured.checked_add(width).ok_or(ReflectiveSubcategoryShellError::Overflow {
        invariant: "adjunction_reflective_subcategory-folded-certificate-fits-i64",
        measured,
    })
}

pub fn require_agreement(measured: i64, expected: i64) -> Result<i64, ReflectiveSubcategoryShellError> {
    if measured == expected {
        return Ok(measured);
    }
    Err(ReflectiveSubcategoryShellError::ClaimFailed {
        invariant: "adjunction_reflective_subcategory-hom-sum-equals-outgoing",
        measured,
        expected,
    })
}

pub fn checked_claim_sum(parts: &[i64]) -> Result<i64, ReflectiveSubcategoryShellError> {
    let mut total = 0i64;
    for (index, part) in parts.iter().enumerate() {
        let measured = match i64::try_from(index) {
            Ok(value) => value,
            Err(_) => i64::MAX,
        };
        total = total.checked_add(*part).ok_or(ReflectiveSubcategoryShellError::Overflow {
            invariant: "claim-sum-stays-in-i64",
            measured,
        })?;
    }
    Ok(total)
}

fn text_has_byte(text: &str, target: u8) -> bool {
    for byte in text.bytes() {
        if byte == target {
            return true;
        }
    }
    false
}

fn text_refused(text: &str) -> bool {
    if text.is_empty() {
        return true;
    }
    if text_has_byte(text, 46) {
        return true;
    }
    if text_has_byte(text, 101) {
        return true;
    }
    if text_has_byte(text, 69) {
        return true;
    }
    false
}

fn split_sign(text: &str) -> (i64, &str) {
    if text.starts_with('-') {
        let rest = match text.get(1..) {
            Some(value) => value,
            None => "",
        };
        return (-1, rest);
    }
    (1, text)
}

fn digits_only(text: &str) -> bool {
    if text.is_empty() {
        return false;
    }
    for byte in text.bytes() {
        if !byte.is_ascii_digit() {
            return false;
        }
    }
    true
}

fn accumulate_digits(text: &str) -> Result<i64, ReflectiveSubcategoryShellError> {
    let mut value = 0i64;
    for byte in text.bytes() {
        value = value.checked_mul(10).ok_or(ReflectiveSubcategoryShellError::Overflow {
            invariant: "parsed-integer-fits-i64",
            measured: value,
        })?;
        let digit = i64::from(byte - 48);
        value = value.checked_add(digit).ok_or(ReflectiveSubcategoryShellError::Overflow {
            invariant: "parsed-integer-fits-i64",
            measured: value,
        })?;
    }
    Ok(value)
}

pub fn parse_exact_i64(text: &str) -> Result<i64, ReflectiveSubcategoryShellError> {
    if text_refused(text) {
        return Err(ReflectiveSubcategoryShellError::FloatRefused {
            invariant: "public-boundary-refuses-binary64-text",
            measured_len: text.len(),
        });
    }
    let (sign, digits) = split_sign(text);
    if !digits_only(digits) {
        return Err(ReflectiveSubcategoryShellError::FloatRefused {
            invariant: "public-boundary-refuses-non-integer-text",
            measured_len: text.len(),
        });
    }
    let magnitude = accumulate_digits(digits)?;
    magnitude.checked_mul(sign).ok_or(ReflectiveSubcategoryShellError::Overflow {
        invariant: "parsed-signed-integer-fits-i64",
        measured: magnitude,
    })
}

pub fn certify_claim(text: &str) -> Result<i64, ReflectiveSubcategoryShellError> {
    let spec = parse_spec(text)?;
    let value = ReflectiveSubcategoryShell::try_new(spec.0, spec.1)?;
    value.certificate()
}

fn parse_spec(text: &str) -> Result<(usize, Vec<(usize, usize)>), ReflectiveSubcategoryShellError> {
    let objects = parse_object_count(text)?;
    let arrows = parse_arrow_list(&arrow_fields(text))?;
    Ok((objects, arrows))
}

fn parse_object_count(text: &str) -> Result<usize, ReflectiveSubcategoryShellError> {
    if text_refused(text) {
        return Err(ReflectiveSubcategoryShellError::FloatRefused {
            invariant: "spec-refuses-binary64-text",
            measured_len: text.len(),
        });
    }
    let head = match text.split(';').next() {
        Some(value) => value,
        None => "",
    };
    let objects_i = parse_exact_i64(head)?;
    usize_from_i64(objects_i)
}

fn arrow_fields(text: &str) -> Vec<&str> {
    let mut fields = Vec::new();
    let mut skipped_head = false;
    for part in text.split(';') {
        if skipped_head {
            fields.push(part);
        }
        if !skipped_head {
            skipped_head = true;
        }
    }
    fields
}

fn parse_arrow_list(fields: &[&str]) -> Result<Vec<(usize, usize)>, ReflectiveSubcategoryShellError> {
    let mut arrows = Vec::new();
    let mut index = 0usize;
    while index < fields.len() {
        let field = match fields.get(index) {
            Some(value) => *value,
            None => "",
        };
        arrows.push(parse_arrow(field)?);
        index = index.saturating_add(1);
    }
    Ok(arrows)
}

fn parse_arrow(part: &str) -> Result<(usize, usize), ReflectiveSubcategoryShellError> {
    let mut ends = part.split('>');
    let src_text = ends.next().ok_or(ReflectiveSubcategoryShellError::IndexOutOfBounds {
        invariant: "spec-arrow-has-source",
        measured: 0,
        bound: 0,
    })?;
    let tgt_text = ends.next().ok_or(ReflectiveSubcategoryShellError::IndexOutOfBounds {
        invariant: "spec-arrow-has-target",
        measured: 0,
        bound: 0,
    })?;
    if ends.next().is_some() {
        return Err(ReflectiveSubcategoryShellError::IndexOutOfBounds {
            invariant: "spec-arrow-has-two-ends",
            measured: part.len(),
            bound: 2,
        });
    }
    let src = usize_from_i64(parse_exact_i64(src_text)?)?;
    let tgt = usize_from_i64(parse_exact_i64(tgt_text)?)?;
    Ok((src, tgt))
}

fn usize_from_i64(value: i64) -> Result<usize, ReflectiveSubcategoryShellError> {
    if value < 0 {
        return Err(ReflectiveSubcategoryShellError::IndexOutOfBounds {
            invariant: "spec-index-nonnegative",
            measured: 0,
            bound: 0,
        });
    }
    usize::try_from(value).map_err(|_| ReflectiveSubcategoryShellError::Overflow {
        invariant: "spec-index-fits-usize",
        measured: value,
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    const UNIT_EXPECT: i64 = 3;
    const INTEG_EXPECT: i64 = 3;

    fn show(err: ReflectiveSubcategoryShellError) -> String {
        format!("{err:?}")
    }

    fn integration_certificate() -> Result<i64, ReflectiveSubcategoryShellError> {
        let ledger = ArrowLedger::try_new(2, vec![(0, 1)])?;
        let value = ReflectiveSubcategoryShell::try_new(ledger.objects(), ledger.arrows().to_vec())?;
        value.certificate()
    }

    #[test]
    fn unit_adjunction_reflective_subcategory_hom_sum_matches_outgoing() -> Result<(), String> {
        let value = ReflectiveSubcategoryShell::try_new(2, vec![(0, 1), (1, 1)]).map_err(show)?;
        let got = value.certificate().map_err(show)?;
        if got != UNIT_EXPECT {
            return Err(format!("certificate {got}"));
        }
        Ok(())
    }

    #[test]
    fn integration_ledger_and_adjunction_reflective_subcategory_agree() -> Result<(), String> {
        let cert = integration_certificate().map_err(show)?;
        let combined = checked_claim_sum(&[cert, 0]).map_err(show)?;
        if combined != INTEG_EXPECT {
            return Err(format!("combined {combined}"));
        }
        Ok(())
    }

    #[test]
    fn e2e_certify_claim_text() -> Result<(), String> {
        let got = certify_claim("2;0>1;1>1").map_err(show)?;
        if got != UNIT_EXPECT {
            return Err(format!("e2e {got}"));
        }
        Ok(())
    }

    #[test]
    fn negative_empty_carrier() -> Result<(), String> {
        let err = ReflectiveSubcategoryShell::try_new(0, vec![]).map_err(show);
        match err {
            Err(text) => {
                if !text.contains("adjunction_reflective_subcategory-carrier-nonempty") {
                    return Err(text);
                }
                Ok(())
            }
            Ok(_) => Err("empty carrier accepted".into()),
        }
    }

    #[test]
    fn negative_float_boundary() -> Result<(), String> {
        let err = parse_exact_i64("1.5").map_err(show);
        match err {
            Err(text) => {
                if !text.contains("binary64") {
                    return Err(text);
                }
                Ok(())
            }
            Ok(_) => Err("float accepted".into()),
        }
    }

    #[test]
    fn negative_index() -> Result<(), String> {
        let err = ReflectiveSubcategoryShell::try_new(1, vec![(0, 2)]).map_err(show);
        match err {
            Err(text) => {
                if !text.contains("endpoint") {
                    return Err(text);
                }
                Ok(())
            }
            Ok(_) => Err("bad arrow accepted".into()),
        }
    }

    #[test]
    fn negative_claim_disagreement() -> Result<(), String> {
        let err = require_agreement(1, 2).map_err(show);
        match err {
            Err(text) => {
                if !text.contains("adjunction_reflective_subcategory-hom-sum-equals-outgoing") {
                    return Err(text);
                }
                Ok(())
            }
            Ok(_) => Err("disagreement accepted".into()),
        }
    }

    #[test]
    fn negative_overflow_sum() -> Result<(), String> {
        let err = checked_claim_sum(&[i64::MAX, 1]).map_err(show);
        match err {
            Err(text) => {
                if !text.contains("claim-sum-stays-in-i64") {
                    return Err(text);
                }
                Ok(())
            }
            Ok(_) => Err("overflow accepted".into()),
        }
    }
}
