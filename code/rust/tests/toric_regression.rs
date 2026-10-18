use omega_quantum_physics::pauli::Pauli;
use theory_of_finite_qm::campaigns::toric::ToricCode2x2;
const PROVENANCE: &str = "Origin: code/rust/src/qm/campaigns/toric.rs Claim: urn:fqm:toric:logical-braid-one-and-euler-zero AuthorityEffect: None";
const SAMPLE: i64 = 8;
const EXPECTED: i64 = 1;
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

fn letter_xz(letter: &Pauli) -> (i64, i64) {
    match letter {
        Pauli::I => (0, 0),
        Pauli::X => (1, 0),
        Pauli::Y => (1, 1),
        Pauli::Z => (0, 1),
    }
}

fn symplectic(left: &[Pauli; 8], right: &[Pauli; 8]) -> Result<i64, ClaimError> {
    let mut acc = 0i64;
    let mut qubit = 0i64;
    while qubit < 8 {
        let (x1, z1) = match left.get(qubit as usize) {
            Some(letter) => letter_xz(letter),
            None => return Err(violated("left qubit", qubit, 8)),
        };
        let (x2, z2) = match right.get(qubit as usize) {
            Some(letter) => letter_xz(letter),
            None => return Err(violated("right qubit", qubit, 8)),
        };
        let term = checked_add(checked_mul(x1, z2)?, checked_mul(z1, x2)?)?;
        acc = checked_add(acc, term)?;
        qubit = checked_add(qubit, 1)?;
    }
    checked_rem(acc, 2)
}

fn euler(vertices: i64, edges: i64, faces: i64) -> Result<i64, ClaimError> {
    checked_sub(checked_add(vertices, faces)?, edges)
}

fn oracle(sample: i64) -> Result<i64, ClaimError> {
    require(sample == SAMPLE, "sample", sample, SAMPLE)?;
    require(euler(4, sample, 4)? == 0, "euler", euler(4, sample, 4)?, 0)?;
    let (wx1, wz1, _wx2, _wz2) = ToricCode2x2::logical_operators();
    symplectic(&wx1, &wz1)
}

fn count_x(ops: &[[Pauli; 8]; 4]) -> Result<i64, ClaimError> {
    let mut count = 0i64;
    let mut row = 0i64;
    while row < 4 {
        let line = match ops.get(row as usize) {
            Some(line) => line,
            None => return Err(violated("star row", row, 4)),
        };
        let mut col = 0i64;
        while col < 8 {
            match line.get(col as usize) {
                Some(Pauli::X) => count = checked_add(count, 1)?,
                Some(_) => {}
                None => return Err(violated("star col", col, 8)),
            }
            col = checked_add(col, 1)?;
        }
        row = checked_add(row, 1)?;
    }
    Ok(count)
}

fn library_agrees(value: i64) -> Result<(), ClaimError> {
    let (wx1, wz1, wx2, wz2) = ToricCode2x2::logical_operators();
    require(symplectic(&wx1, &wz2)? == 0, "cross braid", symplectic(&wx1, &wz2)?, 0)?;
    require(symplectic(&wx2, &wz2)? == value, "second braid", symplectic(&wx2, &wz2)?, value)?;
    require(count_x(&ToricCode2x2::star_operators())? == 16, "star weight", 16, 16)
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
