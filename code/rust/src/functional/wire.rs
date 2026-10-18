//! Shared parsing of rational wire strings for the Phi2/Phi3/Phi4 certificates.
//! Each caller supplies its own refusal for an unparsable string.

use num_rational::BigRational;
use std::str::FromStr;

pub(crate) fn parse_rational_vec<E>(
    values: &[String],
    invalid: fn(String) -> E,
) -> Result<Vec<BigRational>, E> {
    values
        .iter()
        .map(|s| BigRational::from_str(s).map_err(|_| invalid(s.clone())))
        .collect()
}

pub(crate) fn parse_rational_matrix<E>(
    rows: &[Vec<String>],
    invalid: fn(String) -> E,
) -> Result<Vec<Vec<BigRational>>, E> {
    rows.iter()
        .map(|row| parse_rational_vec(row, invalid))
        .collect()
}
