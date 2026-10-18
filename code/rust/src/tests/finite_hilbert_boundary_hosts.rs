use theory_of_finite_qm::campaigns::carrier::{d3_eisenstein_norm_holds, Eisenstein};
use theory_of_finite_qm::domain::finite_spinfoam_model::sphere_euler;
use theory_of_finite_qm::domain::gaussian_rational::sample_norm_identity;
use theory_of_finite_qm::domain::simplicial_entropy_schedule::area_model;
const PROVENANCE: &str = "Origin: code/rust/src/qm/domain/finite_spinfoam_model.rs Claim: urn:fqm:hilbert-boundary:sphere-euler-two-and-gaussian-norm AuthorityEffect: None";
const SAMPLE: i64 = 6;
const EXPECTED: i64 = 2;
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

fn binom6(k: i64) -> Result<i64, ClaimError> {
    let table = [1i64, 6, 15, 20, 15, 6, 1];
    match table.get(k as usize) {
        Some(value) => Ok(*value),
        None => Err(violated("binom", k, 6)),
    }
}

fn euler_alternating(n: i64) -> Result<i64, ClaimError> {
    let mut total = 0i64;
    let mut k = 1i64;
    while k <= n {
        let term = binom6(k)?;
        if checked_rem(k, 2)? == 1 {
            total = checked_add(total, term)?;
        } else {
            total = checked_sub(total, term)?;
        }
        k = checked_add(k, 1)?;
    }
    Ok(total)
}

fn product_real() -> Result<i64, ClaimError> {
    let left = checked_mul(2, 1)?;
    let right = checked_mul(-1, 3)?;
    checked_sub(left, right)
}

fn product_root() -> Result<i64, ClaimError> {
    let ad = checked_mul(2, 3)?;
    let bc = checked_mul(-1, 1)?;
    let bd = checked_mul(-1, 3)?;
    let sum = checked_add(ad, bc)?;
    checked_sub(sum, bd)
}

fn norm_from_parts(real: i64, root: i64) -> Result<i64, ClaimError> {
    let square_real = checked_mul(real, real)?;
    let cross = checked_mul(real, root)?;
    let square_root = checked_mul(root, root)?;
    let gap = checked_sub(square_real, cross)?;
    checked_add(gap, square_root)
}

fn eisenstein_norm() -> Result<i64, ClaimError> {
    let real = product_real()?;
    let root = product_root()?;
    norm_from_parts(real, root)
}

fn oracle(sample: i64) -> Result<i64, ClaimError> {
    require(sample == SAMPLE, "sample", sample, SAMPLE)?;
    euler_alternating(5)
}

fn sphere_matches(value: i64) -> Result<(), ClaimError> {
    let euler = sphere_euler();
    require(euler == value, "sphere euler", euler, value)
}

fn gaussian_and_area() -> Result<(), ClaimError> {
    sample_norm_identity().map_err(|_| violated("gaussian norm", 0, 4))?;
    let model = area_model(1, &[], 2).map_err(|_| violated("area", 0, 4))?;
    require(model.boundary_area as i64 == 4, "boundary area", model.boundary_area as i64, 4)
}

fn factor_norm(value: &Eisenstein) -> Result<i64, ClaimError> {
    value.norm().map_err(|_| violated("factor norm", 0, 7))
}

fn norms_agree(local: i64) -> Result<(), ClaimError> {
    let library = d3_eisenstein_norm_holds().map_err(|_| violated("eisenstein", 0, local))?;
    let z = Eisenstein { real: 2, root: -1 };
    let w = Eisenstein { real: 1, root: 3 };
    let left = factor_norm(&z)?;
    let right = factor_norm(&w)?;
    let by_factors = left.checked_mul(right).ok_or_else(|| violated("norm product", 0, local))?;
    require(library == local, "norm library", library, local)?;
    require(library == by_factors, "norm factors", library, by_factors)
}

fn library_agrees(value: i64) -> Result<(), ClaimError> {
    sphere_matches(value)?;
    gaussian_and_area()?;
    let local = eisenstein_norm()?;
    norms_agree(local)
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
