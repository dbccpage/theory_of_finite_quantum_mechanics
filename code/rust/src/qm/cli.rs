//! Finite QM module cli.
//!
//! A tiny exact command language. Decimal points and exponent markers are
//! refused. `add` and `mul` run on integers. `purity` reports the numerator
//! of the standard qubit purity after clearing the denominator 9.

pub fn execute(line: &str) -> Result<i64, String> {
    if line.bytes().any(|byte| matches!(byte, b'.' | b'e' | b'E')) {
        return Err("FLOAT_TOKEN_FORBIDDEN".into());
    }
    let mut parts = line.split_whitespace();
    let command = parts.next().ok_or("missing command")?;
    match command {
        "add" => {
            let left = parse_i64(parts.next().ok_or("add needs two integers")?)?;
            let right = parse_i64(parts.next().ok_or("add needs two integers")?)?;
            if parts.next().is_some() {
                return Err("add has trailing tokens".into());
            }
            left.checked_add(right).ok_or_else(|| "add overflow".to_string())
        }
        "mul" => {
            let left = parse_i64(parts.next().ok_or("mul needs two integers")?)?;
            let right = parse_i64(parts.next().ok_or("mul needs two integers")?)?;
            if parts.next().is_some() {
                return Err("mul has trailing tokens".into());
            }
            left.checked_mul(right).ok_or_else(|| "mul overflow".to_string())
        }
        "purity" => {
            if parts.next().is_some() {
                return Err("purity takes no arguments".into());
            }
            // Independent of api.rs: diagonal 1/2, off-diagonal 1/6.
            // Tr(ρ²) = 2*(1/2)² + 2*(1/6)² = 1/2 + 1/18 = 10/18 = 5/9.
            let by_entries = purity_numerator()?;
            let by_spectrum = spectrum_numerator()?;
            if by_entries != by_spectrum {
                return Err(format!("purity numerators {by_entries} and {by_spectrum}"));
            }
            Ok(by_entries)
        }
        other => Err(format!("unknown command {other}")),
    }
}

fn purity_numerator() -> Result<i64, String> {
    // Common denominator 36: (1/2)² = 9/36, (1/6)² = 1/36.
    // Two diagonal and two off-diagonal terms: 9+9+1+1 = 20 over 36 = 5/9.
    let num_36 = 9 + 9 + 1 + 1;
    if num_36 % 4 != 0 {
        return Err("purity did not reduce by 4".into());
    }
    Ok(num_36 / 4)
}

fn spectrum_numerator() -> Result<i64, String> {
    // det = 1/4 - 1/36 = 8/36 = 2/9. Sum of squares = tr² - 2 det = 1 - 4/9 = 5/9.
    let trace_sq = 1i64;
    let two_det_num = 4i64;
    let two_det_den = 9i64;
    let num = trace_sq
        .checked_mul(two_det_den)
        .and_then(|v| v.checked_sub(two_det_num))
        .ok_or_else(|| "spectrum overflow".to_string())?;
    if two_det_den != 9 || num != 5 {
        return Err(format!("spectrum numerator {num}"));
    }
    Ok(num)
}

fn parse_i64(token: &str) -> Result<i64, String> {
    token
        .parse::<i64>()
        .map_err(|_| format!("not an integer: {token}"))
}
