
pub mod constant_functor;
pub mod copresheaf;
pub mod diagonal_functor;
pub mod equivalence_of_categories;
pub mod essentially_surjective;
pub mod faithful_functor;
pub mod forgetful_functor;
pub mod free_functor;
pub mod full_functor;
#[allow(clippy::module_inception)]
pub mod functor;
pub mod functor_category;
pub mod hom_functor;
pub mod horizontal_composition;
pub mod identity_functor;
pub mod isomorphism_of_categories;
pub mod nat_trans_components;
pub mod natural_transformation;
pub mod presheaf;
pub mod representable_functor;
pub mod vertical_composition;
pub mod yoneda;

pub use constant_functor::ConstantFunctor;
pub use copresheaf::Copresheaf;
pub use diagonal_functor::DiagonalFunctor;
pub use equivalence_of_categories::EquivalenceOfCategories;
pub use essentially_surjective::EssentiallySurjective;
pub use faithful_functor::FaithfulFunctor;
pub use forgetful_functor::ForgetfulFunctor;
pub use free_functor::FreeFunctor;
pub use full_functor::FullFunctor;
pub use functor::Functor;
pub use functor_category::FunctorCategory;
pub use hom_functor::HomFunctor;
pub use horizontal_composition::HorizontalComposition;
pub use identity_functor::IdentityFunctor;
pub use isomorphism_of_categories::IsomorphismOfCategories;
pub use nat_trans_components::NatTransComponents;
pub use natural_transformation::NaturalTransformation;
pub use presheaf::Presheaf;
pub use representable_functor::RepresentableFunctor;
pub use vertical_composition::VerticalComposition;
pub use yoneda::Yoneda;

pub const ORIGIN: &str = "Origin: code/rust/src/category_theory/functor/mod.rs";
pub const CLAIM: &str = "Claim: urn:tfqm:category-theory:functor_mod:facade-carrier-width";
pub const AUTHORITY_EFFECT: &str = "AuthorityEffect: None";
pub const MUTATION_KILLS: &str = "killed=3;suite=require_agreement_eq_flip,fold_carrier_add_to_sub,refuse_empty_eq_flip";

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum FacadeError {
    FloatRefused { invariant: &'static str, measured_len: usize },
    EmptyCarrier { invariant: &'static str, measured: usize },
    ClaimFailed { invariant: &'static str, measured: i64, expected: i64 },
    Overflow { invariant: &'static str, measured: i64 },
}

impl std::fmt::Display for FacadeError {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(formatter, "{self:?}")
    }
}

impl std::error::Error for FacadeError {}

fn refuse_empty(objects: usize) -> Result<(), FacadeError> {
    if objects == 0 {
        return Err(FacadeError::EmptyCarrier {
            invariant: "facade-carrier-nonempty",
            measured: objects,
        });
    }
    Ok(())
}

fn fold_carrier(measured: i64, objects: usize) -> Result<i64, FacadeError> {
    let width = match i64::try_from(objects) {
        Ok(value) => value,
        Err(_) => {
            return Err(FacadeError::Overflow {
                invariant: "facade-width-fits-i64",
                measured,
            });
        }
    };
    measured.checked_add(width).ok_or(FacadeError::Overflow {
        invariant: "facade-folded-width-fits-i64",
        measured,
    })
}

pub fn require_agreement(measured: i64, expected: i64) -> Result<i64, FacadeError> {
    if measured == expected {
        return Ok(measured);
    }
    Err(FacadeError::ClaimFailed {
        invariant: "facade-width-doubles",
        measured,
        expected,
    })
}

fn expected_double(objects: usize) -> Result<i64, FacadeError> {
    let width = match i64::try_from(objects) {
        Ok(value) => value,
        Err(_) => {
            return Err(FacadeError::Overflow {
                invariant: "facade-double-fits-i64",
                measured: 0,
            });
        }
    };
    width.checked_add(width).ok_or(FacadeError::Overflow {
        invariant: "facade-double-fits-i64",
        measured: width,
    })
}

pub fn facade_width(objects: usize) -> Result<i64, FacadeError> {
    refuse_empty(objects)?;
    let measured = match i64::try_from(objects) {
        Ok(value) => value,
        Err(_) => {
            return Err(FacadeError::Overflow {
                invariant: "facade-measured-width-fits-i64",
                measured: 0,
            });
        }
    };
    finish_width(measured, objects)
}

fn finish_width(measured: i64, objects: usize) -> Result<i64, FacadeError> {
    let folded = fold_carrier(measured, objects)?;
    let expected = expected_double(objects)?;
    require_agreement(folded, expected)
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

fn accumulate_digits(text: &str) -> Result<i64, FacadeError> {
    let mut value = 0i64;
    for byte in text.bytes() {
        value = value.checked_mul(10).ok_or(FacadeError::Overflow {
            invariant: "parsed-integer-fits-i64",
            measured: value,
        })?;
        let digit = i64::from(byte - 48);
        value = value.checked_add(digit).ok_or(FacadeError::Overflow {
            invariant: "parsed-integer-fits-i64",
            measured: value,
        })?;
    }
    Ok(value)
}

pub fn parse_exact_i64(text: &str) -> Result<i64, FacadeError> {
    if text_refused(text) {
        return Err(FacadeError::FloatRefused {
            invariant: "public-boundary-refuses-binary64-text",
            measured_len: text.len(),
        });
    }
    let (sign, digits) = split_sign(text);
    if !digits_only(digits) {
        return Err(FacadeError::FloatRefused {
            invariant: "public-boundary-refuses-non-integer-text",
            measured_len: text.len(),
        });
    }
    let magnitude = accumulate_digits(digits)?;
    magnitude.checked_mul(sign).ok_or(FacadeError::Overflow {
        invariant: "parsed-signed-integer-fits-i64",
        measured: magnitude,
    })
}

#[cfg(test)]
mod facade_tests {
    use super::*;

    const CHILD_EXPECT: i64 = 3;

    fn child_certificate() -> Result<i64, String> {
        yoneda::certify_claim("2;0>1;1>1").map_err(|err| format!("{err:?}"))
    }

    #[test]
    fn unit_facade_width_doubles() -> Result<(), String> {
        let width = facade_width(2).map_err(|err| format!("{err:?}"))?;
        if width != 4 {
            return Err(format!("width {width}"));
        }
        Ok(())
    }

    fn combined_child_and_facade() -> Result<i64, String> {
        let got = child_certificate()?;
        let width = facade_width(2).map_err(|err| format!("{err:?}"))?;
        match got.checked_add(width) {
            Some(sum) => Ok(sum),
            None => Err("overflow".into()),
        }
    }

    #[test]
    fn integration_child_and_facade() -> Result<(), String> {
        let sum = combined_child_and_facade()?;
        if sum != CHILD_EXPECT + 4 {
            return Err(format!("sum {sum}"));
        }
        Ok(())
    }

    #[test]
    fn e2e_parsed_width() -> Result<(), String> {
        let parsed = parse_exact_i64("2").map_err(|err| format!("{err:?}"))?;
        let width = width_from_parsed(parsed)?;
        if width != 4 {
            return Err(format!("width {width}"));
        }
        Ok(())
    }

    fn width_from_parsed(parsed: i64) -> Result<i64, String> {
        if parsed < 0 {
            return Err("negative width".into());
        }
        let objects = match usize::try_from(parsed) {
            Ok(value) => value,
            Err(_) => return Err("width exceeds usize".into()),
        };
        facade_width(objects).map_err(|err| format!("{err:?}"))
    }

    #[test]
    fn negative_empty_carrier() -> Result<(), String> {
        let err = facade_width(0).map_err(|err| format!("{err:?}"));
        match err {
            Err(text) => {
                if !text.contains("facade-carrier-nonempty") {
                    return Err(text);
                }
                Ok(())
            }
            Ok(_) => Err("empty carrier accepted".into()),
        }
    }

    #[test]
    fn negative_float_boundary() -> Result<(), String> {
        let err = parse_exact_i64("1.5").map_err(|err| format!("{err:?}"));
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
    fn negative_claim_disagreement() -> Result<(), String> {
        let err = require_agreement(1, 2).map_err(|err| format!("{err:?}"));
        match err {
            Err(text) => {
                if !text.contains("facade-width-doubles") {
                    return Err(text);
                }
                Ok(())
            }
            Ok(_) => Err("disagreement accepted".into()),
        }
    }

    #[test]
    fn negative_overflow_sum() -> Result<(), String> {
        let err = fold_carrier(i64::MAX, 1).map_err(|err| format!("{err:?}"));
        match err {
            Err(text) => {
                if !text.contains("facade-folded-width-fits-i64") {
                    return Err(text);
                }
                Ok(())
            }
            Ok(_) => Err("overflow accepted".into()),
        }
    }
}
