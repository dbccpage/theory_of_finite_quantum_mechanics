//! Adjacent energy-spacing diagnostics from canonical checked Hermitian eigenpairs.
//! Multiplicity, zero spacing and the absence of spacing for singleton spectra
//! remain explicit. AuthorityEffect: None.
use linear_algebra::hermitian_eigen::{
    hermitian_eigen_checked, HermitianSpectrum, SpectrumError, SpectrumPolicy,
};
use nalgebra::DMatrix;
use num_complex::Complex64;
use serde::{Deserialize, Serialize};
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize, Deserialize)]
pub enum SpectrumAuthorityEffect {
    None,
}

/// Computation owner for finite Hermitian energy-spacing diagnostics.
#[derive(Debug, Clone, Copy, PartialEq, Serialize)]
pub struct QuantumGapFunctional {
    policy: SpectrumPolicy,
}

/// Private checked calculation, not a constructor from caller-asserted fields.
/// All adjacent spacings retain multiplicity, including zero spacing. For a
/// singleton spectrum there is no spacing; it is not replaced by zero.
///
/// ~~~compile_fail
/// use omega_functional::quantum_gaps::QuantumGaps;
/// let forged: QuantumGaps = serde_json::from_str("{}").unwrap();
/// ~~~
#[derive(Debug, Clone, PartialEq, Serialize)]
pub struct QuantumGaps {
    authority_effect: SpectrumAuthorityEffect,
    spectrum: HermitianSpectrum,
    adjacent_spacings: Vec<f64>,
}

impl QuantumGaps {
    pub fn authority_effect(&self) -> SpectrumAuthorityEffect {
        self.authority_effect
    }
    pub fn spectrum(&self) -> &HermitianSpectrum {
        &self.spectrum
    }
    pub fn adjacent_spacings(&self) -> &[f64] {
        &self.adjacent_spacings
    }
    /// The first adjacent spacing, including zero when the lowest level repeats.
    /// This does not skip a degenerate level to manufacture a positive gap.
    pub fn lowest_adjacent_spacing(&self) -> Option<f64> {
        self.adjacent_spacings.first().copied()
    }
}

impl QuantumGapFunctional {
    pub fn new(policy: SpectrumPolicy) -> Self {
        Self { policy }
    }
    pub fn policy(&self) -> SpectrumPolicy {
        self.policy
    }

    pub fn evaluate(&self, matrix: &DMatrix<Complex64>) -> Result<QuantumGaps, SpectrumError> {
        let spectrum = hermitian_eigen_checked(matrix, self.policy)?;
        let mut adjacent_spacings = Vec::with_capacity(spectrum.eigenvalues().len() - 1);
        for (index, pair) in spectrum.eigenvalues().windows(2).enumerate() {
            let spacing = pair[1] - pair[0];
            if !spacing.is_finite() {
                return Err(SpectrumError::UnrepresentableSpacing { index });
            }
            adjacent_spacings.push(spacing);
        }
        Ok(QuantumGaps {
            authority_effect: SpectrumAuthorityEffect::None,
            spectrum,
            adjacent_spacings,
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use nalgebra::DVector;
    #[test]
    fn independent_integer_fixtures_match_every_level_and_spacing() {
        #[derive(serde::Deserialize)]
        #[serde(deny_unknown_fields)]
        struct Fixtures {
            schema: String,
            authority_effect: String,
            cases: Vec<Case>,
        }
        #[derive(serde::Deserialize)]
        #[serde(deny_unknown_fields)]
        struct Case {
            name: String,
            matrix: Vec<Vec<[i32; 2]>>,
            eigenvalues: Vec<i32>,
            spacings: Vec<i32>,
        }
        let fixtures: Fixtures = serde_json::from_str(include_str!(concat!(
            env!("CARGO_MANIFEST_DIR"),
            "/../tests/omega_functional/fixtures/finite_hermitian_spectrum.json"
        )))
        .unwrap();
        assert_eq!(
            fixtures.schema,
            "omega.finite-hermitian-spectrum.fixtures.v1"
        );
        assert_eq!(fixtures.authority_effect, "None");
        assert_eq!(fixtures.cases.len(), 6);
        let mut names = std::collections::BTreeSet::new();
        for case in fixtures.cases {
            assert!(names.insert(case.name));
            let dimension = case.matrix.len();
            assert!(dimension > 0 && case.matrix.iter().all(|row| row.len() == dimension));
            let matrix = DMatrix::from_fn(dimension, dimension, |row, column| {
                let [re, im] = case.matrix[row][column];
                c(f64::from(re), f64::from(im))
            });
            let result = QuantumGapFunctional::new(policy())
                .evaluate(&matrix)
                .unwrap();
            assert_eq!(
                result.spectrum().eigenvalues().len(),
                case.eigenvalues.len()
            );
            assert_eq!(result.adjacent_spacings().len(), case.spacings.len());
            for (&actual, expected) in result.spectrum().eigenvalues().iter().zip(case.eigenvalues)
            {
                close(actual, f64::from(expected));
            }
            for (&actual, expected) in result.adjacent_spacings().iter().zip(case.spacings) {
                close(actual, f64::from(expected));
            }
        }
    }

    fn policy() -> SpectrumPolicy {
        SpectrumPolicy::new(16, 10_000, 1e-14, 1e-12).unwrap()
    }

    fn c(re: f64, im: f64) -> Complex64 {
        Complex64::new(re, im)
    }

    fn diagonal(values: &[f64]) -> DMatrix<Complex64> {
        DMatrix::from_diagonal(&DVector::from_iterator(
            values.len(),
            values.iter().map(|x| c(*x, 0.0)),
        ))
    }

    fn close(actual: f64, expected: f64) {
        assert!(
            actual.is_finite() && (actual - expected).abs() <= 1e-10 * expected.abs().max(1.0),
            "{actual:?} != {expected:?}"
        );
    }

    #[test]
    fn diagonal_levels_are_sorted_without_dropping_degeneracy() {
        let matrix = diagonal(&[4.0, -2.0, 4.0, 1.0]);
        let result = QuantumGapFunctional::new(policy())
            .evaluate(&matrix)
            .unwrap();
        assert_eq!(result.spectrum().eigenvalues(), &[-2.0, 1.0, 4.0, 4.0]);
        assert_eq!(result.adjacent_spacings(), &[3.0, 3.0, 0.0]);
        assert_eq!(result.lowest_adjacent_spacing(), Some(3.0));
        let repeated = QuantumGapFunctional::new(policy())
            .evaluate(&diagonal(&[1.0, 1.0, 4.0]))
            .unwrap();
        assert_eq!(repeated.lowest_adjacent_spacing(), Some(0.0));
        assert_eq!(repeated.adjacent_spacings(), &[0.0, 3.0]);
    }

    #[test]
    fn genuinely_complex_off_diagonals_determine_the_spectrum() {
        let matrix =
            DMatrix::from_row_slice(2, 2, &[c(2.0, 0.0), c(1.0, 1.0), c(1.0, -1.0), c(3.0, 0.0)]);
        // Characteristic polynomial lambda^2 - 5 lambda + 4 gives 1 and 4.
        let result = QuantumGapFunctional::new(policy())
            .evaluate(&matrix)
            .unwrap();
        for (&actual, expected) in result.spectrum().eigenvalues().iter().zip([1.0, 4.0]) {
            close(actual, expected);
        }
        close(result.adjacent_spacings()[0], 3.0);
        let pauli_y =
            DMatrix::from_row_slice(2, 2, &[c(0.0, 0.0), c(0.0, -1.0), c(0.0, 1.0), c(0.0, 0.0)]);
        let y = QuantumGapFunctional::new(policy())
            .evaluate(&pauli_y)
            .unwrap();
        close(y.spectrum().eigenvalues()[0], -1.0);
        close(y.spectrum().eigenvalues()[1], 1.0);
        close(y.adjacent_spacings()[0], 2.0);
    }

    #[test]
    fn serialized_gaps_keep_none_authority_and_no_verdict() {
        let result = QuantumGapFunctional::new(policy())
            .evaluate(&diagonal(&[1.0, 4.0]))
            .unwrap();
        assert_eq!(result.authority_effect(), SpectrumAuthorityEffect::None);
        let wire = serde_json::to_value(&result).unwrap();
        assert_eq!(wire["authority_effect"], "None");
        assert!(wire.get("verdict").is_none() && wire.get("accepted").is_none());
    }

    #[test]
    fn singleton_zero_and_subnormal_spectra_do_not_invent_missing_spacings() {
        let functional = QuantumGapFunctional::new(policy());
        let singleton = functional.evaluate(&diagonal(&[-7.0])).unwrap();
        assert_eq!(singleton.spectrum().eigenvalues(), &[-7.0]);
        assert!(singleton.adjacent_spacings().is_empty());
        assert_eq!(singleton.lowest_adjacent_spacing(), None);
        let zero = functional.evaluate(&diagonal(&[0.0, 0.0])).unwrap();
        assert_eq!(zero.adjacent_spacings(), &[0.0]);
        assert_eq!(zero.spectrum().normalization_scale(), 1.0);
        let tiny = f64::from_bits(1);
        let subnormal = functional.evaluate(&diagonal(&[tiny, 0.0])).unwrap();
        assert_eq!(subnormal.spectrum().eigenvalues(), &[0.0, tiny]);
        assert_eq!(subnormal.adjacent_spacings(), &[tiny]);
    }

    #[test]
    fn finite_input_does_not_authorize_overflowed_levels_or_spacings() {
        let functional = QuantumGapFunctional::new(policy());
        assert!(matches!(
            functional.evaluate(&DMatrix::from_element(2, 2, c(f64::MAX, 0.0))),
            Err(SpectrumError::UnrepresentableEigenvalue { .. })
        ));
        assert_eq!(
            functional.evaluate(&diagonal(&[-f64::MAX, f64::MAX])),
            Err(SpectrumError::UnrepresentableSpacing { index: 0 })
        );
    }
}
