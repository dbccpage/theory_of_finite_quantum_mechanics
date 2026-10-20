
pub fn verify() -> Result<i64, &'static str> {
    let a = 3i64;
    let b = 4i64;
    let initial = build_initial_state(a, b)?;
    let rebuilt = rebuild_from_branches(a, b)?;
    if rebuilt != initial {
        return Err("Bell branches do not rebuild the teleported state");
    }
    let a_sq = a.checked_mul(a).ok_or("norm")?;
    let b_sq = b.checked_mul(b).ok_or("norm")?;
    a_sq.checked_add(b_sq).ok_or("norm")
}

fn build_initial_state(a: i64, b: i64) -> Result<[i64; 8], &'static str> {
    let mut initial = [0i64; 8];
    add(&mut initial, 0, 0, 0, a)?;
    add(&mut initial, 0, 1, 1, a)?;
    add(&mut initial, 1, 0, 0, b)?;
    add(&mut initial, 1, 1, 1, b)?;
    for amp in &mut initial {
        *amp = amp.checked_mul(2).ok_or("scale")?;
    }
    Ok(initial)
}

fn rebuild_from_branches(a: i64, b: i64) -> Result<[i64; 8], &'static str> {
    let mut rebuilt = [0i64; 8];
    branch(&mut rebuilt, &[(0, 0, 1), (1, 1, 1)], &[a, b])?;
    branch(&mut rebuilt, &[(0, 0, 1), (1, 1, -1)], &[a, -b])?;
    branch(&mut rebuilt, &[(0, 1, 1), (1, 0, 1)], &[b, a])?;
    branch(&mut rebuilt, &[(0, 1, 1), (1, 0, -1)], &[-b, a])?;
    Ok(rebuilt)
}

fn branch(
    target: &mut [i64; 8],
    bell: &[(i64, i64, i64)],
    bob: &[i64; 2],
) -> Result<(), &'static str> {
    for (c, alice, sign) in bell {
        for (bit, amplitude) in bob.iter().enumerate() {
            let contrib = sign.checked_mul(*amplitude).ok_or("branch")?;
            add(target, *c, *alice, i64::try_from(bit).map_err(|_| "bit")?, contrib)?;
        }
    }
    Ok(())
}

fn add(target: &mut [i64; 8], c: i64, alice: i64, bob: i64, value: i64) -> Result<(), &'static str> {
    let index = usize::try_from(c * 4 + alice * 2 + bob).map_err(|_| "index")?;
    let slot = target.get_mut(index).ok_or("index")?;
    *slot = slot.checked_add(value).ok_or("add")?;
    Ok(())
}
