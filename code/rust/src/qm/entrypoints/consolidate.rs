
pub fn run_consolidate() -> Result<(), String> {
    let left = [1i64, 4, 2, 7];
    let right = [3i64, 0, 5, 1];
    let mut merged = Vec::with_capacity(left.len());
    for (a, b) in left.iter().zip(right.iter()) {
        merged.push(
            a.checked_add(*b)
                .ok_or_else(|| "consolidate overflow".to_string())?,
        );
    }
    let total_entries = checked_sum(&merged)?;
    let total_parts = checked_sum(&left)?.checked_add(checked_sum(&right)?).ok_or("consolidate overflow")?;
    let mut from_end = 0i64;
    for value in merged.iter().rev() {
        from_end = from_end.checked_add(*value).ok_or("consolidate overflow")?;
    }
    if total_entries != total_parts || total_entries != from_end {
        return Err(format!(
            "consolidated totals disagree: entries {total_entries}, parts {total_parts}, reverse {from_end}"
        ));
    }
    Ok(())
}

fn checked_sum(values: &[i64]) -> Result<i64, String> {
    let mut total = 0i64;
    for value in values {
        total = total.checked_add(*value).ok_or("consolidate overflow")?;
    }
    Ok(total)
}
