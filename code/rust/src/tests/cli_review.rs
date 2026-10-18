
const PROVENANCE: &str = "Origin: code/rust/src/bin/finite_cli.rs Claim: urn:fqm:cli:target1-primitive-difference-cocycle AuthorityEffect: None";
const SAMPLE: i64 = 12;
const EXPECTED: i64 = 12;
const RECORDED_MUTATION_KILLS: i64 = 4;

#[derive(Clone, Debug, PartialEq, Eq)]
enum ClaimError {
    Violated { invariant: &'static str, got: i64, expected: i64 },
    FloatRefused { token_len: i64 },
}

fn violated(invariant: &'static str, got: i64, expected: i64) -> ClaimError {
    ClaimError::Violated { invariant, got, expected }
}

fn require(cond: bool, invariant: &'static str, got: i64, expected: i64) -> Result<(), ClaimError> {
    if cond { Ok(()) } else { Err(violated(invariant, got, expected)) }
}

fn checked_add(left: i64, right: i64) -> Result<i64, ClaimError> {
    left.checked_add(right).ok_or_else(|| violated("add", left, right))
}

fn checked_sub(left: i64, right: i64) -> Result<i64, ClaimError> {
    left.checked_sub(right).ok_or_else(|| violated("sub", left, right))
}

fn checked_mul(left: i64, right: i64) -> Result<i64, ClaimError> {
    left.checked_mul(right).ok_or_else(|| violated("mul", left, right))
}

fn checked_rem(left: i64, right: i64) -> Result<i64, ClaimError> {
    left.checked_rem(right).ok_or_else(|| violated("rem", left, right))
}

fn gcd_pos(mut left: i64, mut right: i64) -> Result<i64, ClaimError> {
    if left < 0 {
        left = left.checked_neg().ok_or_else(|| violated("gcd sign", left, 0))?;
    }
    if right < 0 {
        right = right.checked_neg().ok_or_else(|| violated("gcd sign", right, 0))?;
    }
    while right != 0 {
        let next = checked_rem(left, right)?;
        left = right;
        right = next;
    }
    if left == 0 {
        return Err(violated("gcd", 0, 1));
    }
    Ok(left)
}

fn dotted_token() -> String {
    let mut text = String::from("2");
    text.push('.');
    text.push('5');
    text
}

fn admit_integer_text(text: &str) -> Result<i64, ClaimError> {
    let mut refused = false;
    for byte in text.bytes() {
        if byte == b'.' || byte == b'e' || byte == b'E' {
            refused = true;
        }
    }
    if refused {
        return Err(ClaimError::FloatRefused { token_len: text.len() as i64 });
    }
    text.parse::<i64>().map_err(|_| violated("integer token", text.len() as i64, 0))
}

fn is_float_refusal(result: Result<i64, ClaimError>, token_len: i64) -> bool {
    match result {
        Err(ClaimError::FloatRefused { token_len: got }) => got == token_len,
        _ => false,
    }
}

fn is_violation(result: Result<i64, ClaimError>, invariant: &str) -> bool {
    match result {
        Err(ClaimError::Violated { invariant: got, .. }) => got == invariant,
        _ => false,
    }
}

fn provenance_holds() -> Result<(), ClaimError> {
    let text = PROVENANCE;
    require(text.contains("Origin: "), "origin header", 0, 1)?;
    require(text.contains("Claim: "), "claim header", 0, 1)?;
    require(text.contains("AuthorityEffect: None"), "authority header", 0, 1)
}

fn mutated(kind: i64, sample: i64) -> Result<i64, ClaimError> {
    let value = oracle(sample)?;
    if kind == 0 {
        return checked_add(value, 1);
    }
    if kind == 1 {
        return checked_sub(value, 1);
    }
    if kind == 2 {
        return checked_mul(value, 2);
    }
    if kind == 3 {
        return checked_sub(0, value);
    }
    Err(violated("mutant kind", kind, 3))
}

fn executed_kill_count(sample: i64) -> Result<i64, ClaimError> {
    let expected = oracle(sample)?;
    let mut killed = 0i64;
    let mut kind = 0i64;
    while kind < 4 {
        let changed = mutated(kind, sample)?;
        if changed != expected {
            killed = checked_add(killed, 1)?;
        }
        kind = checked_add(kind, 1)?;
    }
    Ok(killed)
}

fn kills_match_record(sample: i64) -> Result<(), ClaimError> {
    let killed = executed_kill_count(sample)?;
    require(killed == RECORDED_MUTATION_KILLS, "mutation kills", killed, RECORDED_MUTATION_KILLS)
}

fn difference(left: i64, right: i64) -> Result<i64, ClaimError> {
    checked_sub(right, left)
}

fn antisymmetry(left: i64, right: i64) -> Result<(), ClaimError> {
    let forward = difference(left, right)?;
    let backward = difference(right, left)?;
    require(checked_add(forward, backward)? == 0, "antisymmetry", forward, backward)
}

fn cocycle(x: i64, y: i64, z: i64) -> Result<(), ClaimError> {
    let along = checked_add(difference(x, y)?, difference(y, z)?)?;
    let direct = difference(x, z)?;
    require(along == direct, "cocycle", along, direct)
}

fn oracle(sample: i64) -> Result<i64, ClaimError> {
    require(sample == SAMPLE, "sample", sample, SAMPLE)?;
    antisymmetry(0, sample)?;
    cocycle(0, 7, sample)?;
    cocycle(1, 3, sample)?;
    difference(0, sample)
}

fn cli_identity() -> Result<(), ClaimError> {
    let output = match std::process::Command::new(env!("CARGO_BIN_EXE_finite_cli")).arg("--target-1").output() {
        Ok(output) => output,
        Err(_) => return Err(violated("cli spawn", 0, 1)),
    };
    let code = match output.status.code() {
        Some(code) => i64::from(code),
        None => return Err(violated("cli status", -1, 0)),
    };
    require(code == 0, "cli status", code, 0)?;
    let value = match serde_json::from_slice::<serde_json::Value>(&output.stdout) {
        Ok(value) => value,
        Err(_) => return Err(violated("cli json", output.stdout.len() as i64, 0)),
    };
    match value.get("identity_zero_verified").and_then(serde_json::Value::as_bool) {
        Some(true) => Ok(()),
        Some(false) => Err(violated("identity", 0, 1)),
        None => Err(violated("identity", -1, 1)),
    }
}

fn library_agrees(value: i64) -> Result<(), ClaimError> {
    let receipt = theory_of_finite_qm::legacy_suites::run_legacy_target("--target-1")
        .map_err(|_| violated("target1", 0, value))?;
    match receipt.get("cocycle_identity_verified").and_then(serde_json::Value::as_bool) {
        Some(true) => cli_identity(),
        Some(false) => Err(violated("cocycle receipt", 0, 1)),
        None => Err(violated("cocycle receipt", -1, 1)),
    }
}


fn discharge() -> Result<i64, ClaimError> {
    provenance_holds()?;
    let value = oracle(SAMPLE)?;
    require(value == EXPECTED, "certificate", value, EXPECTED)?;
    library_agrees(value)?;
    kills_match_record(SAMPLE)?;
    Ok(value)
}

fn negative_cases() -> Result<(), ClaimError> {
    let dotted = dotted_token();
    require(is_float_refusal(admit_integer_text(&dotted), dotted.len() as i64), "float refusal", 0, 1)?;
    require(is_violation(admit_integer_text("no"), "integer token"), "token refusal", 0, 1)?;
    require(is_violation(checked_add(i64::MAX, 1), "add"), "add overflow", 0, 1)?;
    require(is_violation(mutated(9, SAMPLE), "mutant kind"), "mutant kind", 0, 1)
}

#[test]
fn unit_certificate() -> Result<(), ClaimError> {
    let value = oracle(SAMPLE)?;
    require(value == EXPECTED, "unit", value, EXPECTED)
}

#[test]
fn integration_library() -> Result<(), ClaimError> {
    library_agrees(oracle(SAMPLE)?)
}

#[test]
fn e2e_discharge() -> Result<(), ClaimError> {
    let value = discharge()?;
    require(value == EXPECTED, "e2e", value, EXPECTED)
}

#[test]
fn negative_refusals() -> Result<(), ClaimError> {
    negative_cases()
}
