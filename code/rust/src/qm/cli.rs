
fn is_float_byte(byte: u8) -> bool {
    byte == b'.' || byte == b'e' || byte == b'E'
}

fn has_float_token(line: &str) -> bool {
    for byte in line.bytes() {
        if is_float_byte(byte) {
            return true;
        }
    }
    false
}

fn parse_binary_args(
    parts: &mut std::str::SplitWhitespace<'_>,
    need_msg: &'static str,
    trail_msg: &'static str,
) -> Result<(i64, i64), String> {
    let left = parse_i64(parts.next().ok_or(need_msg)?)?;
    let right = parse_i64(parts.next().ok_or(need_msg)?)?;
    if parts.next().is_some() {
        return Err(trail_msg.into());
    }
    Ok((left, right))
}

fn exec_purity(parts: &mut std::str::SplitWhitespace<'_>) -> Result<i64, String> {
    if parts.next().is_some() {
        return Err("purity takes no arguments".into());
    }
    let by_entries = purity_numerator()?;
    let by_spectrum = spectrum_numerator()?;
    if by_entries != by_spectrum {
        return Err(format!("purity numerators {by_entries} and {by_spectrum}"));
    }
    Ok(by_entries)
}

pub fn execute(line: &str) -> Result<i64, String> {
    if has_float_token(line) {
        return Err("FLOAT_TOKEN_FORBIDDEN".into());
    }
    let mut parts = line.split_whitespace();
    let command = parts.next().ok_or("missing command")?;
    match command {
        "add" => {
            let (left, right) =
                parse_binary_args(&mut parts, "add needs two integers", "add has trailing tokens")?;
            left.checked_add(right).ok_or_else(|| "add overflow".to_string())
        }
        "mul" => {
            let (left, right) =
                parse_binary_args(&mut parts, "mul needs two integers", "mul has trailing tokens")?;
            left.checked_mul(right).ok_or_else(|| "mul overflow".to_string())
        }
        "purity" => exec_purity(&mut parts),
        other => Err(format!("unknown command {other}")),
    }
}

fn purity_numerator() -> Result<i64, String> {
    let num_36 = 9 + 9 + 1 + 1;
    if num_36 % 4 != 0 {
        return Err("purity did not reduce by 4".into());
    }
    Ok(num_36 / 4)
}

fn spectrum_numerator() -> Result<i64, String> {
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
