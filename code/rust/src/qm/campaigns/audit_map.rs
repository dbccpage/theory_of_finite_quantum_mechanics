
pub fn verify() -> Result<i64, &'static str> {
    let modulus = 8i64;
    let mut seen = [false; 8];
    let mut domain_sum = 0i64;
    let mut image_sum = 0i64;
    for index in 0..modulus {
        let image = (3 * index + 1).rem_euclid(modulus);
        let slot = usize::try_from(image).map_err(|_| "index")?;
        if seen[slot] {
            return Err("audit map collided");
        }
        seen[slot] = true;
        domain_sum = domain_sum.checked_add(index).ok_or("sum")?;
        image_sum = image_sum.checked_add(image).ok_or("sum")?;
        let restored = (3 * (image - 1)).rem_euclid(modulus);
        if restored != index {
            return Err("audit inverse failed");
        }
    }
    if seen.iter().any(|hit| !*hit) || domain_sum != image_sum {
        return Err("audit map is not a permutation");
    }
    Ok(image_sum)
}
