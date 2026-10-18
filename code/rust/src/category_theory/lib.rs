
extern crate self as omega_category_theory;
pub mod abelian;
pub mod adjunction;
pub mod category;
pub mod enriched;
pub mod finite_continuation;
pub mod foundations;
pub mod functor;
pub mod limits_colimits;
pub mod monad;
pub mod monoidal;

pub mod core {
    pub trait Category {
        type Ob: Clone + PartialEq + Eq + std::fmt::Debug;
        type Mor: Clone + PartialEq + Eq + std::fmt::Debug;

        fn identity<A>(object: &A) -> Self::Mor;
        fn compose<A, B, C>(first: &Self::Mor, second: &Self::Mor) -> Option<Self::Mor>;
    }

    pub trait MorphismEq: Category {
        fn morphism_eq<A, B>(left: &Self::Mor, right: &Self::Mor) -> bool {
            left == right
        }
    }
}

pub mod errors {
    #[derive(Debug, Clone, PartialEq, Eq)]
    pub enum ArithmosError {
        LawViolation(String),
        PreconditionFailed(String),
        InvalidShape(String),
    }
}

pub mod witness {
    #[derive(Debug, Clone, PartialEq, Eq)]
    pub struct Witness {
        pub name: String,
    }

    impl Witness {
        pub fn new(name: impl Into<String>) -> Self {
            Self { name: name.into() }
        }
    }
}

pub mod law {
    use super::errors::ArithmosError;
    use super::witness::Witness;

    pub trait Law {
        type Subject;
        fn check(subject: &Self::Subject) -> Result<Witness, ArithmosError>;
    }
}

pub mod braided_monoidal {
    pub trait BraidedMonoidalCategory: super::monoidal_category::MonoidalCategory {
        fn braiding<A, B>() -> Self::Mor
        where
            Self: super::core::Category;
    }
}

pub mod monoidal_category {
    use super::core::Category;

    pub trait MonoidalCategory: Category {
        type TensorProduct<A, B>: Clone;
        fn unit() -> Self::Ob;
    }
}

pub mod agent_functor;
pub mod arrow;
pub mod bridges;
pub mod cat_functor;
pub mod category_contract_alignment;
pub mod cauchy;
pub mod coend;
pub mod colimits;
pub mod condensation;
pub mod density_matrix_functor;
pub mod eilenberg_moore;
pub mod family_category;
pub mod finite_category;
pub mod finite_category_builder;
pub mod finite_category_validation;
pub mod finite_groupoid;
pub mod finite_profunctor;
pub mod functor_composition;
pub mod grothendieck_construction;
pub mod higher;
pub mod higher_functor;
pub mod hom_adjunction;
pub mod hott_topos_bridge;
pub mod kleisli_category;
pub mod lawvere;
pub mod legacy_adjunction;
pub mod legacy_monad;
pub mod limits;
pub mod morphism;
pub mod mssn_functor_bridge;
pub mod natural_trans;
pub mod natural_trans_composition;
pub mod nerve;
pub mod operad;
pub mod rewriting;
pub mod simplicial_hott_bridge;
pub mod topos_hott_model;
pub mod validation;
pub mod zeta_functor;

pub use legacy_adjunction as adjunction_legacy;
pub use legacy_monad as monad_legacy;

pub mod bounded_counter;
pub mod finite_functional_dependencies;
pub mod finite_moore;
pub mod finite_path;
pub mod finite_relational;

pub mod context_reflection;

pub mod finite_functional_classification;
pub mod finite_retention_choices;
pub mod finite_self_reference;

pub mod dagger;
pub mod finite_history_context;
pub mod finite_partial_structure;
pub mod finite_question_family;
pub mod finite_report_repair;
pub mod finite_report_descent;
pub mod finite_report_query;
pub mod finite_section_separation;

pub mod finite_independence;
pub mod finite_trace;
pub mod finite_joint_carrier;
pub mod finite_joint_dynamics;
pub mod finite_simulation;

pub const ORIGIN: &str = "Origin: code/rust/src/category_theory/lib.rs";
pub const CLAIM: &str = "Claim: urn:tfqm:category-theory:lib:facade-carrier-width";
pub const AUTHORITY_EFFECT: &str = "AuthorityEffect: None";

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
        crate::functor::yoneda::certify_claim("2;0>1;1>1").map_err(|err| format!("{err:?}"))
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
