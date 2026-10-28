//! Explicit provider transport and diagnostic compatibility for QM consumers.
//! Local arithmetic always uses the checked scalar protocol. Provider records
//! retain their existing nominal types. Receiving-provider algorithms are not
//! upgraded or certified by this adapter. AuthorityEffect: None.
use crate::linear_algebra::scalars::{ExactRing, Field, Involution, Operation, ScalarError};
use crate::linear_algebra::{BasicMatrix as Local, ExactFieldError as LocalError};
use ::linear_algebra::backend::basic_matrix::BasicMatrix as Provider;
pub(crate) use ::linear_algebra::exact_field::ExactFieldError;
fn scalar_refusal(error: ScalarError) -> ExactFieldError {
    let (operation, violation) = match error {
        ScalarError::ZeroDenominator => ("coefficient admission", "zero rational denominator"),
        ScalarError::NegativeDenominator => {
            ("coefficient admission", "negative rational denominator")
        }
        ScalarError::NonReduced => ("coefficient admission", "non-reduced rational"),
        ScalarError::DivisionByZero => ("scalar division", "division by zero"),
        ScalarError::InvalidDomain { domain, reason } => (domain, reason),
        ScalarError::InversionRefused { domain } => (
            domain,
            "provider refused inverse of an admitted nonzero value",
        ),
        ScalarError::OutOfRange { operation } => (
            operation_name(operation),
            "exact result is not representable in the bounded scalar",
        ),
    };
    // The receiving API has ScalarContract rather than the newer Scalar variant.
    // Keep explicit operation/refusal classifications; no refusal becomes success.
    ExactFieldError::ScalarContract {
        operation,
        violation,
    }
}
fn operation_name(operation: Operation) -> &'static str {
    match operation {
        Operation::Add => "checked addition",
        Operation::Subtract => "checked subtraction",
        Operation::Multiply => "checked multiplication",
        Operation::Negate => "checked negation",
        Operation::Invert => "checked inversion",
        Operation::Divide => "checked division",
    }
}
fn provider_domain_error(error: LocalError) -> ExactFieldError {
    match error {
        LocalError::Singular { rank, size } => ExactFieldError::Singular { rank, size },
        LocalError::NotSymmetric { row, col } => ExactFieldError::NotSymmetric { row, col },
        LocalError::NotHermitian { row, col } => ExactFieldError::NotHermitian { row, col },
        LocalError::CharacteristicTwo { operation } => {
            ExactFieldError::CharacteristicTwo { operation }
        }
        LocalError::NotRepresentable { row, col } => ExactFieldError::NotRepresentable { row, col },
        LocalError::ScalarContract {
            operation,
            violation,
        } => ExactFieldError::ScalarContract {
            operation,
            violation,
        },
        LocalError::ReplayFailed { operation } => ExactFieldError::ReplayFailed { operation },
        LocalError::CertificateRejected { reason } => {
            ExactFieldError::CertificateRejected { reason }
        }
        LocalError::LawViolated { law } => ExactFieldError::LawViolated { law },
        _ => ExactFieldError::LawViolated {
            law: "unexpected local error variant",
        },
    }
}
pub(crate) fn provider_error(error: LocalError) -> ExactFieldError {
    match error {
        LocalError::Scalar(error) => scalar_refusal(error),
        LocalError::Matrix(value) => ExactFieldError::Matrix(value),
        LocalError::ShapeMismatch {
            operation,
            left,
            right,
        } => ExactFieldError::ShapeMismatch {
            operation,
            left,
            right,
        },
        LocalError::NotSquare {
            operation,
            rows,
            cols,
        } => ExactFieldError::NotSquare {
            operation,
            rows,
            cols,
        },
        LocalError::RaggedRows { row, len, expected } => {
            ExactFieldError::RaggedRows { row, len, expected }
        }
        LocalError::VectorLength {
            operation,
            expected,
            got,
        } => ExactFieldError::VectorLength {
            operation,
            expected,
            got,
        },
        other => provider_domain_error(other),
    }
}

fn unary<F: Field + ExactRing, R>(
    a: &Provider<F>,
    f: impl FnOnce(&Local<F>) -> Result<R, LocalError>,
) -> Result<R, ExactFieldError> {
    let a = Local::try_from_provider(a).map_err(provider_error)?;
    f(&a).map_err(provider_error)
}
fn binary<F: Field + ExactRing>(
    a: &Provider<F>,
    b: &Provider<F>,
    f: impl FnOnce(&Local<F>, &Local<F>) -> Result<Local<F>, LocalError>,
) -> Result<Provider<F>, ExactFieldError> {
    let a = Local::try_from_provider(a).map_err(provider_error)?;
    let b = Local::try_from_provider(b).map_err(provider_error)?;
    f(&a, &b)
        .and_then(Local::into_provider)
        .map_err(provider_error)
}
impl From<LocalError> for engine_lie_theory::lorentz::LorentzError {
    fn from(error: LocalError) -> Self {
        Self::Matrix(provider_error(error))
    }
}
impl From<LocalError> for engine_general_relativity::simplicial_dynamics::SimplicialDynamicsError {
    fn from(error: LocalError) -> Self {
        Self::Matrix(provider_error(error))
    }
}
pub(crate) mod matrix {
    pub(crate) fn from_fn<F: Field + ExactRing, G: FnMut(usize, usize) -> F>(
        m: usize,
        n: usize,
        f: G,
    ) -> Result<Provider<F>, ExactFieldError> {
        core::from_fn(m, n, f)
            .and_then(Local::into_provider)
            .map_err(provider_error)
    }
    pub(crate) fn multiply_vector<F: Field + ExactRing>(
        a: &Provider<F>,
        v: &[F],
    ) -> Result<Vec<F>, ExactFieldError> {
        unary(a, |a| core::multiply_vector(a, v))
    }
    pub(crate) fn to_rows<F: Field + ExactRing>(
        a: &Provider<F>,
    ) -> Result<Vec<Vec<F>>, ExactFieldError> {
        unary(a, core::to_rows)
    }

    pub(crate) fn kronecker_with_limits<F: Field + ExactRing>(
        a: &Provider<F>,
        b: &Provider<F>,
        limits: OperationLimits,
    ) -> Result<Provider<F>, ExactFieldError> {
        binary(a, b, |a, b| core::kronecker_with_limits(a, b, limits))
    }
    pub(crate) fn commutes<F: Field + ExactRing>(
        a: &Provider<F>,
        b: &Provider<F>,
    ) -> Result<bool, ExactFieldError> {
        let a = Local::try_from_provider(a).map_err(provider_error)?;
        let b = Local::try_from_provider(b).map_err(provider_error)?;
        core::commutes(&a, &b).map_err(provider_error)
    }

    use super::*;
    use crate::linear_algebra::matrix as core;
    pub(crate) fn add<F: Field + ExactRing>(
        a: &Provider<F>,
        b: &Provider<F>,
    ) -> Result<Provider<F>, ExactFieldError> {
        binary(a, b, core::add)
    }
    pub(crate) fn sub<F: Field + ExactRing>(
        a: &Provider<F>,
        b: &Provider<F>,
    ) -> Result<Provider<F>, ExactFieldError> {
        binary(a, b, core::sub)
    }
    pub(crate) fn multiply<F: Field + ExactRing>(
        a: &Provider<F>,
        b: &Provider<F>,
    ) -> Result<Provider<F>, ExactFieldError> {
        binary(a, b, core::multiply)
    }
    pub(crate) fn kronecker<F: Field + ExactRing>(
        a: &Provider<F>,
        b: &Provider<F>,
    ) -> Result<Provider<F>, ExactFieldError> {
        binary(a, b, core::kronecker)
    }
    pub(crate) fn commutator<F: Field + ExactRing>(
        a: &Provider<F>,
        b: &Provider<F>,
    ) -> Result<Provider<F>, ExactFieldError> {
        binary(a, b, core::commutator)
    }
    pub(crate) fn anticommutator<F: Field + ExactRing>(
        a: &Provider<F>,
        b: &Provider<F>,
    ) -> Result<Provider<F>, ExactFieldError> {
        binary(a, b, core::anticommutator)
    }
    pub(crate) fn direct_sum<F: Field + ExactRing>(
        a: &Provider<F>,
        b: &Provider<F>,
    ) -> Result<Provider<F>, ExactFieldError> {
        binary(a, b, core::direct_sum)
    }
    pub(crate) fn hstack<F: Field + ExactRing>(
        a: &Provider<F>,
        b: &Provider<F>,
    ) -> Result<Provider<F>, ExactFieldError> {
        binary(a, b, core::hstack)
    }
    pub(crate) fn vstack<F: Field + ExactRing>(
        a: &Provider<F>,
        b: &Provider<F>,
    ) -> Result<Provider<F>, ExactFieldError> {
        binary(a, b, core::vstack)
    }
    pub(crate) fn transpose<F: Field + ExactRing>(
        a: &Provider<F>,
    ) -> Result<Provider<F>, ExactFieldError> {
        unary(a, |a| core::transpose(a)?.into_provider())
    }
    pub(crate) fn neg<F: Field + ExactRing>(
        a: &Provider<F>,
    ) -> Result<Provider<F>, ExactFieldError> {
        unary(a, |a| core::neg(a)?.into_provider())
    }
    pub(crate) fn is_scalar_matrix<F: Field + ExactRing>(
        a: &Provider<F>,
    ) -> Result<bool, ExactFieldError> {
        unary(a, core::is_scalar_matrix)
    }
    pub(crate) fn is_zero_matrix<F: Field + ExactRing>(
        a: &Provider<F>,
    ) -> Result<bool, ExactFieldError> {
        unary(a, core::is_zero_matrix)
    }
    pub(crate) fn is_identity_matrix<F: Field + ExactRing>(
        a: &Provider<F>,
    ) -> Result<bool, ExactFieldError> {
        unary(a, core::is_identity_matrix)
    }
    pub(crate) fn is_symmetric<F: Field + ExactRing>(
        a: &Provider<F>,
    ) -> Result<bool, ExactFieldError> {
        unary(a, core::is_symmetric)
    }

    pub(crate) fn trace<F: Field + ExactRing>(a: &Provider<F>) -> Result<F, ExactFieldError> {
        unary(a, core::trace)
    }
    pub(crate) fn power<F: Field + ExactRing>(
        a: &Provider<F>,
        n: u64,
    ) -> Result<Provider<F>, ExactFieldError> {
        unary(a, |a| core::power(a, n)?.into_provider())
    }
    pub(crate) fn scale<F: Field + ExactRing>(
        a: &Provider<F>,
        x: &F,
    ) -> Result<Provider<F>, ExactFieldError> {
        unary(a, |a| core::scale(a, x)?.into_provider())
    }
    pub(crate) fn identity<F: Field + ExactRing>(n: usize) -> Result<Provider<F>, ExactFieldError> {
        core::identity(n)
            .and_then(Local::into_provider)
            .map_err(provider_error)
    }
    pub(crate) fn zeros<F: Field + ExactRing>(
        m: usize,
        n: usize,
    ) -> Result<Provider<F>, ExactFieldError> {
        core::zeros(m, n)
            .and_then(Local::into_provider)
            .map_err(provider_error)
    }
    pub(crate) fn diagonal<F: Field + ExactRing>(a: &[F]) -> Result<Provider<F>, ExactFieldError> {
        core::diagonal(a)
            .and_then(Local::into_provider)
            .map_err(provider_error)
    }
    pub(crate) fn from_rows<F: Field + ExactRing>(
        a: Vec<Vec<F>>,
    ) -> Result<Provider<F>, ExactFieldError> {
        core::from_rows(a)
            .and_then(Local::into_provider)
            .map_err(provider_error)
    }
    pub(crate) fn dot<F: Field + ExactRing>(a: &[F], b: &[F]) -> Result<F, ExactFieldError> {
        core::dot(a, b).map_err(provider_error)
    }
}
pub(crate) mod involution {
    pub(crate) fn outer_product<F: Involution>(
        a: &[F],
        b: &[F],
    ) -> Result<Provider<F>, ExactFieldError> {
        core::outer_product(a, b)
            .and_then(Local::into_provider)
            .map_err(provider_error)
    }

    use super::*;
    use crate::linear_algebra::involution as core;
    pub(crate) fn adjoint<F: Involution>(a: &Provider<F>) -> Result<Provider<F>, ExactFieldError> {
        unary(a, |a| core::adjoint(a)?.into_provider())
    }
    pub(crate) fn is_hermitian<F: Involution>(a: &Provider<F>) -> Result<bool, ExactFieldError> {
        unary(a, core::is_hermitian)
    }
    pub(crate) fn hs_inner<F: Involution>(
        a: &Provider<F>,
        b: &Provider<F>,
    ) -> Result<F, ExactFieldError> {
        let a = Local::try_from_provider(a).map_err(provider_error)?;
        let b = Local::try_from_provider(b).map_err(provider_error)?;
        core::hs_inner(&a, &b).map_err(provider_error)
    }
}
pub(crate) mod elimination {
    pub(crate) fn principal_minors<F: Field + ExactRing>(
        a: &Provider<F>,
    ) -> Result<Vec<F>, ExactFieldError> {
        unary(a, core::principal_minors)
    }

    pub(crate) fn rank<F: Field + ExactRing>(a: &Provider<F>) -> Result<usize, ExactFieldError> {
        unary(a, core::rank)
    }

    use super::*;
    use crate::linear_algebra::elimination as core;
    pub(crate) fn inverse<F: Field + ExactRing>(
        a: &Provider<F>,
    ) -> Result<Provider<F>, ExactFieldError> {
        unary(a, |a| core::inverse(a)?.into_provider())
    }
    pub(crate) fn determinant<F: Field + ExactRing>(a: &Provider<F>) -> Result<F, ExactFieldError> {
        unary(a, core::determinant)
    }
}
pub(crate) mod ordered {
    use super::*;
    use crate::linear_algebra::ordered::{self as core, OrderedExactField};
    pub(crate) fn is_positive_semidefinite<F: OrderedExactField>(
        a: &Provider<F>,
    ) -> Result<bool, ExactFieldError> {
        unary(a, core::is_positive_semidefinite)
    }
    pub(crate) fn is_positive_definite<F: OrderedExactField>(
        a: &Provider<F>,
    ) -> Result<bool, ExactFieldError> {
        unary(a, core::is_positive_definite)
    }
}

pub(crate) use crate::linear_algebra::scalars::Q;
pub(crate) use ::linear_algebra::backend::basic_matrix::{
    BasicMatrix, MatrixError, OperationLimits,
};

pub(crate) mod basic_matrix {
    pub(crate) use super::{BasicMatrix, MatrixError, OperationLimits};
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::linear_algebra::scalars::{q, Q};
    #[test]
    fn checked_transport_keeps_values_and_refuses_raw_domains_without_mutation() {
        let a = Provider::from_row_major(2, 2, vec![q(1), q(2), q(3), q(4)]).unwrap();
        let expected = Provider::from_row_major(2, 2, vec![q(7), q(10), q(15), q(22)]).unwrap();
        assert_eq!(matrix::multiply(&a, &a).unwrap(), expected);
        for raw in [
            Q::new_raw(1.into(), 0.into()),
            Q::new_raw(1.into(), (-1).into()),
            Q::new_raw(2.into(), 2.into()),
        ] {
            let bad = Provider::from_row_major(1, 1, vec![raw]).unwrap();
            let before = serde_json::to_string(&bad).unwrap();
            let zero = Provider::from_row_major(1, 1, vec![q(0)]).unwrap();
            assert!(matches!(
                matrix::multiply(&bad, &zero),
                Err(ExactFieldError::ScalarContract {
                    operation: "coefficient admission",
                    ..
                })
            ));
            assert!(matches!(
                matrix::multiply(&zero, &bad),
                Err(ExactFieldError::ScalarContract {
                    operation: "coefficient admission",
                    ..
                })
            ));
            assert_eq!(serde_json::to_string(&bad).unwrap(), before);
        }
    }
    #[test]
    fn error_translation_retains_shape_and_expected_scalar_refusal_classifications() {
        let shape = LocalError::ShapeMismatch {
            operation: "multiply",
            left: (2, 3),
            right: (4, 2),
        };
        assert_eq!(
            provider_error(shape),
            ExactFieldError::ShapeMismatch {
                operation: "multiply",
                left: (2, 3),
                right: (4, 2)
            }
        );
        let max =
            Provider::from_row_major(1, 1, vec![num_rational::Rational64::from_integer(i64::MAX)])
                .unwrap();
        let one = Provider::from_row_major(1, 1, vec![num_rational::Rational64::from_integer(1)])
            .unwrap();
        assert!(matches!(
            matrix::add(&max, &one),
            Err(ExactFieldError::ScalarContract {
                operation: "checked addition",
                violation: "exact result is not representable in the bounded scalar"
            })
        ));
        assert_eq!(
            scalar_refusal(ScalarError::InvalidDomain {
                domain: "F5",
                reason: "noncanonical residue"
            }),
            ExactFieldError::ScalarContract {
                operation: "F5",
                violation: "noncanonical residue"
            }
        );
        assert_eq!(
            scalar_refusal(ScalarError::DivisionByZero),
            ExactFieldError::ScalarContract {
                operation: "scalar division",
                violation: "division by zero"
            }
        );
    }
}
