
const MODULUS: i128 = 1_000_003;
const POINT: i128 = 17;

pub fn evidence_checksum(items: &[i64]) -> Result<i128, &'static str> {
    if items.is_empty() {
        return Err("evidence row is empty");
    }
    let horner = horner(items)?;
    let powers = power_sum(items)?;
    if horner != powers {
        return Err("Horner and power-sum checksums disagree");
    }
    Ok(horner)
}

pub fn evidence_splits(items: &[i64]) -> Result<(), &'static str> {
    let checksum = evidence_checksum(items)?;
    let mut total = 0i128;
    for item in items {
        total = total
            .checked_add(i128::from(*item))
            .ok_or("evidence sum overflow")?;
    }
    let mut from_end = 0i128;
    for item in items.iter().rev() {
        from_end = from_end
            .checked_add(i128::from(*item))
            .ok_or("evidence sum overflow")?;
    }
    if total != from_end {
        return Err("evidence sum depends on order");
    }
    if items.len() > 1 && checksum == total.rem_euclid(MODULUS) && items.iter().all(|v| *v == 0) {
        return Err("nonzero row collapsed");
    }
    Ok(())
}

pub fn sample_evidence_holds() -> Result<(), &'static str> {
    evidence_splits(&[4, -2, 11, 7, 1])
}

fn horner(items: &[i64]) -> Result<i128, &'static str> {
    let mut acc = 0i128;
    for item in items.iter().rev() {
        acc = acc
            .checked_mul(POINT)
            .ok_or("checksum overflow")?
            .checked_add(i128::from(*item))
            .ok_or("checksum overflow")?;
        acc = acc.rem_euclid(MODULUS);
    }
    Ok(acc)
}

fn power_sum(items: &[i64]) -> Result<i128, &'static str> {
    let mut acc = 0i128;
    let mut power = 1i128;
    for item in items {
        let term = power
            .checked_mul(i128::from(*item))
            .ok_or("checksum overflow")?;
        acc = acc.checked_add(term).ok_or("checksum overflow")?;
        acc = acc.rem_euclid(MODULUS);
        power = power.checked_mul(POINT).ok_or("checksum overflow")?;
        power = power.rem_euclid(MODULUS);
    }
    Ok(acc)
}
