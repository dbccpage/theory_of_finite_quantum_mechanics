//! Campaign module stabilizer_codes.
//!
//! The repetition-code stabilizers `ZZI` and `IZZ`. Their symplectic product
//! is zero, so they commute, and the same count of anticommuting sites is
//! even. The `Z` support has a nonzero 2 by 2 minor, so the rank is 2 and
//! the code encodes `3-2 = 1` qubit.

pub fn verify() -> Result<usize, &'static str> {
    let zzi = ([0u8, 0, 0], [1u8, 1, 0]);
    let izz = ([0u8, 0, 0], [0u8, 1, 1]);
    let x_on_0 = ([1u8, 0, 0], [0u8, 0, 0]);
    if symplectic(&zzi.0, &zzi.1, &izz.0, &izz.1)? != 0 {
        return Err("repetition stabilizers anticommute");
    }
    let overlap = zzi.1.iter().zip(izz.0.iter()).filter(|(z, x)| **z & **x == 1).count();
    if overlap % 2 != 0 {
        return Err("overlap parity disagrees with the symplectic form");
    }
    if symplectic(&zzi.0, &zzi.1, &x_on_0.0, &x_on_0.1)? != 1 {
        return Err("X on the first qubit was not detected");
    }
    let minor = i32::from(zzi.1[0]) * i32::from(izz.1[1]) - i32::from(zzi.1[1]) * i32::from(izz.1[0]);
    if minor % 2 == 0 {
        return Err("stabilizer rank is short");
    }
    let encoded = 3usize - 2;
    if encoded != 1 {
        return Err("encoded dimension");
    }
    Ok(encoded)
}

fn symplectic(x1: &[u8; 3], z1: &[u8; 3], x2: &[u8; 3], z2: &[u8; 3]) -> Result<u8, &'static str> {
    let mut phase = 0u8;
    for q in 0..3 {
        if x1[q] > 1 || z1[q] > 1 || x2[q] > 1 || z2[q] > 1 {
            return Err("not an F2 bit");
        }
        phase ^= x1[q] & z2[q];
        phase ^= z1[q] & x2[q];
    }
    Ok(phase)
}
