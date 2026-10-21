//! Phase fibers over Gaussian integers and the unnormalized two-sector Hadamard readout.
//!
//! Exact i64 replay of `code/python/src/qm/pfp_phase_blind_fiber.py` for PFP batch 01, node
//! L1-QM122-PHASE-BLIND-FIBER-INTERFERENCE. Scope: Z[i] amplitudes only; no Hilbert-space,
//! normalization or physical claim. AuthorityEffect: None.
use std::collections::BTreeSet;

fn isqrt(n: i64) -> i64 {
    let mut r = (n as f64).sqrt() as i64;
    while r * r > n {
        r -= 1;
    }
    while (r + 1) * (r + 1) <= n {
        r += 1;
    }
    r
}

/// All Gaussian integers (x, y) with x^2 + y^2 == weight.
pub fn fiber(weight: i64) -> Vec<(i64, i64)> {
    let mut found = Vec::new();
    let r = isqrt(weight);
    for x in -r..=r {
        let rest = weight - x * x;
        let y = isqrt(rest);
        if y * y == rest {
            found.push((x, y));
            if y != 0 {
                found.push((x, -y));
            }
        }
    }
    found.sort();
    found
}

fn weight(z: (i64, i64)) -> i64 {
    z.0 * z.0 + z.1 * z.1
}

/// Unnormalized Hadamard mixing readout (|a+b|^2, |a-b|^2).
pub fn readout(a: (i64, i64), b: (i64, i64)) -> (i64, i64) {
    (weight((a.0 + b.0, a.1 + b.1)), weight((a.0 - b.0, a.1 - b.1)))
}

/// Wire line for one weight pair, identical to the Python `wire_lines` format.
pub fn line(w0: i64, w1: i64) -> String {
    let (f0, f1) = (fiber(w0), fiber(w1));
    let mut outs = BTreeSet::new();
    for a in &f0 {
        for b in &f1 {
            outs.insert(readout(*a, *b));
        }
    }
    let total = 2 * (w0 + w1);
    let doubled = outs.iter().all(|o| o.0 + o.1 == total);
    let reads: Vec<String> = outs.iter().map(|o| format!("{}:{}", o.0, o.1)).collect();
    let realizable = !f0.is_empty() && !f1.is_empty();
    format!(
        "fiber\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
        w0,
        w1,
        f0.len(),
        f1.len(),
        realizable as i32,
        outs.len(),
        doubled as i32,
        (outs.len() <= 1) as i32,
        if reads.is_empty() { "-".to_string() } else { reads.join(";") }
    )
}

/// Replay one tab-separated public-input line `fiber\tw0\tw1`.
pub fn replay(input: &str) -> Option<String> {
    let mut parts = input.split('\t');
    if parts.next()? != "fiber" {
        return None;
    }
    let w0: i64 = parts.next()?.parse().ok()?;
    let w1: i64 = parts.next()?.parse().ok()?;
    Some(line(w0, w1))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn pfp_phase_blind_fiber_sizes_are_sum_of_two_squares_counts() {
        let sizes: Vec<usize> = [0, 1, 2, 3, 4, 5, 9, 25].iter().map(|&n| fiber(n).len()).collect();
        assert_eq!(sizes, vec![1, 4, 4, 0, 4, 8, 4, 12]);
    }

    #[test]
    fn pfp_phase_blind_fiber_named_witnesses() {
        assert_eq!(readout((1, 0), (1, 0)), (4, 0));
        assert_eq!(readout((1, 0), (-1, 0)), (0, 4));
    }

    #[test]
    fn pfp_phase_blind_fiber_nonzero_realizable_sectors_never_descend() {
        for w0 in 1..30 {
            for w1 in 1..30 {
                let l = line(w0, w1);
                let cols: Vec<&str> = l.split('\t').collect();
                if cols[5] == "1" {
                    assert_eq!(cols[8], "0", "descends at ({}, {})", w0, w1);
                }
            }
        }
    }

    #[test]
    fn pfp_phase_blind_fiber_zero_sector_descends_and_total_doubles() {
        assert!(line(0, 5).split('\t').nth(8) == Some("1"));
        assert!(line(5, 0).split('\t').nth(8) == Some("1"));
        for w in 0..30 {
            assert_eq!(line(w, 3).split('\t').nth(7), Some("1"));
        }
        assert_eq!(replay("fiber\t1\t1").unwrap().split('\t').nth(6), Some("3"));
    }
}
