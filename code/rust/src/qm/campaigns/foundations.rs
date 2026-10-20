
pub fn verify() -> Result<usize, &'static str> {
    let mut checked = 0usize;
    for a in 0..3i64 {
        verify_zero_identity(a)?;
        for b in 0..3i64 {
            checked += verify_pair_associativity(a, b)?;
        }
    }
    if checked != 27 {
        return Err("not every triple was checked");
    }
    Ok(checked)
}

fn verify_zero_identity(a: i64) -> Result<(), &'static str> {
    if (a + 0).rem_euclid(3) != a || (0 + a).rem_euclid(3) != a {
        return Err("zero is not an identity");
    }
    Ok(())
}

fn verify_pair_associativity(a: i64, b: i64) -> Result<usize, &'static str> {
    let sum = (a + b).rem_euclid(3);
    if !(0..3).contains(&sum) {
        return Err("addition left the carrier");
    }
    let mut count = 0usize;
    for c in 0..3i64 {
        let left = (sum + c).rem_euclid(3);
        let right = (a + (b + c).rem_euclid(3)).rem_euclid(3);
        let flat = (a + b + c).rem_euclid(3);
        if left != right || left != flat {
            return Err("addition is not associative");
        }
        count += 1;
    }
    Ok(count)
}
