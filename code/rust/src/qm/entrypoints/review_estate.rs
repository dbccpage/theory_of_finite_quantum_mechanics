
pub fn run_review_estate() -> Result<(), String> {
    let claims = [8i64, 5, 13, 2, 1, 7];
    let accepted_mask = [true, false, true, true, false, true];
    if claims.len() != accepted_mask.len() {
        return Err("estate mask length".into());
    }
    let mut accepted = 0i64;
    let mut rejected = 0i64;
    let mut total = 0i64;
    for (claim, keep) in claims.iter().zip(accepted_mask.iter()) {
        total = total.checked_add(*claim).ok_or("estate overflow")?;
        if *keep {
            accepted = accepted.checked_add(*claim).ok_or("estate overflow")?;
        } else {
            rejected = rejected.checked_add(*claim).ok_or("estate overflow")?;
        }
    }
    let parts = accepted.checked_add(rejected).ok_or("estate overflow")?;
    let mut from_end = 0i64;
    for claim in claims.iter().rev() {
        from_end = from_end.checked_add(*claim).ok_or("estate overflow")?;
    }
    if parts != total || from_end != total {
        return Err(format!(
            "estate split {accepted}+{rejected}={parts} does not match total {total} (reverse {from_end})"
        ));
    }
    Ok(())
}
