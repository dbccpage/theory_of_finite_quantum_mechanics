//! Campaign module advanced_targets.
//!
//! Conductors 3 and 4 are coprime, so the totient ladder multiplies:
//! `φ(3) φ(4) = φ(12)`. Each totient is counted by residues and by the
//! product formula.

pub fn verify() -> Result<usize, &'static str> {
    let phi_3 = totient(3)?;
    let phi_4 = totient(4)?;
    let phi_12 = totient(12)?;
    let product = phi_3.checked_mul(phi_4).ok_or("totient overflow")?;
    if product != phi_12 {
        return Err("φ(3)φ(4) is not φ(12)");
    }
    Ok(phi_12)
}

fn totient(n: usize) -> Result<usize, &'static str> {
    if n == 0 {
        return Err("conductor 0");
    }
    let mut counted = 0usize;
    for k in 1..=n {
        if gcd(k, n) == 1 {
            counted += 1;
        }
    }
    let mut formula = n;
    let mut rest = n;
    let mut prime = 2usize;
    while prime.saturating_mul(prime) <= rest {
        if rest % prime == 0 {
            formula = formula / prime * (prime - 1);
            while rest % prime == 0 {
                rest /= prime;
            }
        }
        prime += 1;
    }
    if rest > 1 {
        formula = formula / rest * (rest - 1);
    }
    if counted != formula {
        return Err("totient readings disagree");
    }
    Ok(counted)
}

fn gcd(mut a: usize, mut b: usize) -> usize {
    while b != 0 {
        let r = a % b;
        a = b;
        b = r;
    }
    a
}
