//! Campaign module rungs.
//!
//! The rung of conductor `2^n` has degree `φ(2^n) = 2^{n-1}`. The degree is
//! the count of odd residues, and successive rungs double.

pub fn verify() -> Result<u64, &'static str> {
    let mut previous = 0u64;
    for n in 1u32..=8 {
        let counted = odd_residues(n)?;
        let closed = 1u64 << (n - 1);
        if counted != closed {
            return Err("totient of a power of two disagrees with the shift");
        }
        if n > 1 && counted != previous.checked_mul(2).ok_or("rung")? {
            return Err("rungs do not double");
        }
        previous = counted;
    }
    Ok(previous)
}

fn odd_residues(n: u32) -> Result<u64, &'static str> {
    if n == 0 || n > 20 {
        return Err("rung out of range");
    }
    let modulus = 1u64 << n;
    let mut count = 0u64;
    for residue in 0..modulus {
        if residue % 2 == 1 {
            count += 1;
        }
    }
    Ok(count)
}
