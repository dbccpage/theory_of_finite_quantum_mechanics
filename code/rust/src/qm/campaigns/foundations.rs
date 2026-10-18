//! Campaign module foundations.
//!
//! Addition on `Z/3Z` is a monoid: the operation is closed, `0` is an identity,
//! and both parenthesizations of `a+b+c` agree for every triple.

pub fn verify() -> Result<usize, &'static str> {
    let mut checked = 0usize;
    for a in 0..3i64 {
        if (a + 0).rem_euclid(3) != a || (0 + a).rem_euclid(3) != a {
            return Err("zero is not an identity");
        }
        for b in 0..3i64 {
            let sum = (a + b).rem_euclid(3);
            if !(0..3).contains(&sum) {
                return Err("addition left the carrier");
            }
            for c in 0..3i64 {
                let left = ((a + b).rem_euclid(3) + c).rem_euclid(3);
                let right = (a + (b + c).rem_euclid(3)).rem_euclid(3);
                let flat = (a + b + c).rem_euclid(3);
                if left != right || left != flat {
                    return Err("addition is not associative");
                }
                checked += 1;
            }
        }
    }
    if checked != 27 {
        return Err("not every triple was checked");
    }
    Ok(checked)
}
