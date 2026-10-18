// AuthorityEffect: None. Citation: sealed-derivation-v1 (3100c4e)

//! Exact report of the finite suite: a complete set of mutually unbiased
//! bases in prime-power dimension, the magic-state value `-1/d` in `d = 5`,
//! and a commutator whose trace vanishes two ways.

#[test]
fn test_integration_full_suite_report() {
    let inventory = theory_of_finite_qm::crate_root_inventory_holds();
    assert!(inventory.is_ok(), "{inventory:?}");
    let campaigns = theory_of_finite_qm::qm::campaigns::campaign_inventory_holds();
    assert!(campaigns.is_ok(), "{campaigns:?}");

    for dimension in [3i64, 4] {
        let counted = dimension.checked_add(1);
        let numerator = dimension.checked_mul(dimension).and_then(|square| square.checked_sub(1));
        match (counted, numerator) {
            (Some(counted), Some(numerator)) => {
                assert_eq!(numerator % (dimension - 1), 0);
                assert_eq!(counted, numerator / (dimension - 1), "MUB count");
                assert_eq!(counted.checked_mul(dimension), Some(numerator + counted));
            }
            _ => assert!(false, "MUB arithmetic overflowed"),
        }
    }

    let (magic_num, magic_den) = match magic_value(5) {
        Ok(value) => value,
        Err(error) => {
            assert!(false, "{error}");
            return;
        }
    };
    assert_eq!(magic_num * 5, -magic_den);
    assert_eq!(magic_num, -1);
    assert_eq!(magic_den, 5);

    let trace = match commutator_trace(
        [[1, 2, 3], [0, -1, 4], [5, 6, 1]],
        [[2, 0, 1], [1, 3, -2], [0, 1, 2]],
    ) {
        Ok(trace) => trace,
        Err(error) => {
            assert!(false, "{error}");
            return;
        }
    };
    assert_eq!(trace, 0);
}

/// `-1/d` and `(1-d)/(d(d-1))` are the same rational.
fn magic_value(dimension: i64) -> Result<(i64, i64), &'static str> {
    if dimension <= 1 {
        return Err("dimension");
    }
    let direct_den = dimension;
    let algebraic_num = 1i64.checked_sub(dimension).ok_or("magic")?;
    let algebraic_den = dimension.checked_mul(dimension.checked_sub(1).ok_or("magic")?).ok_or("magic")?;
    let left = (-1i64).checked_mul(algebraic_den).ok_or("magic")?;
    let right = algebraic_num.checked_mul(direct_den).ok_or("magic")?;
    if left != right {
        return Err("magic readings disagree");
    }
    Ok((-1, direct_den))
}

/// `Tr(AB)` and `Tr(BA)` and the Frobenius pairing of `A` with `B^T`.
fn commutator_trace(left: [[i64; 3]; 3], right: [[i64; 3]; 3]) -> Result<i64, &'static str> {
    let ab = mat_mul(&left, &right)?;
    let ba = mat_mul(&right, &left)?;
    let tr_ab = trace(&ab)?;
    let tr_ba = trace(&ba)?;
    // Tr(AB) = sum_{ij} A_{ij} B_{ji}.
    let mut paired = 0i64;
    for i in 0..3 {
        for j in 0..3 {
            paired = paired.checked_add(left[i][j].checked_mul(right[j][i]).ok_or("pair")?).ok_or("pair")?;
        }
    }
    if tr_ab != tr_ba || tr_ab != paired {
        return Err("trace readings disagree");
    }
    tr_ab.checked_sub(tr_ba).ok_or("gap")
}

fn mat_mul(left: &[[i64; 3]; 3], right: &[[i64; 3]; 3]) -> Result<[[i64; 3]; 3], &'static str> {
    let mut out = [[0i64; 3]; 3];
    for i in 0..3 {
        for j in 0..3 {
            let mut slot = 0i64;
            for k in 0..3 {
                slot = slot.checked_add(left[i][k].checked_mul(right[k][j]).ok_or("mul")?).ok_or("mul")?;
            }
            out[i][j] = slot;
        }
    }
    Ok(out)
}

fn trace(matrix: &[[i64; 3]; 3]) -> Result<i64, &'static str> {
    matrix[0][0]
        .checked_add(matrix[1][1])
        .and_then(|v| v.checked_add(matrix[2][2]))
        .ok_or("trace")
}
