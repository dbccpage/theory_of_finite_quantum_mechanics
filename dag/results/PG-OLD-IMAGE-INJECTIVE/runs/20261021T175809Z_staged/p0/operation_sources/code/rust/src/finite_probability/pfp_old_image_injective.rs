//! Exhaustive census of lifts `u : A -> B` with typed recoveries `r : B -> A + {refusal}` on the old image.
//!
//! Exact integer replay of `code/python/src/qm/pfp_old_image_injective.py` for PFP batch 01, node
//! PG-OLD-IMAGE-INJECTIVE. Every pair (u, r) is enumerated; index `a` of `r` means the refusal summand.
//! Scope: finite sets and functions only; no statement about S(n), repair of an engine obstruction or physics.
//! AuthorityEffect: None.

/// Advance `t` as an odometer over `0..base`; returns false after the last tuple.
fn next_tuple(t: &mut [usize], base: usize) -> bool {
    for i in (0..t.len()).rev() {
        t[i] += 1;
        if t[i] < base {
            return true;
        }
        t[i] = 0;
    }
    false
}

/// Call `f` on every tuple of length `len` over `0..base` (once, the empty tuple, when `len == 0`).
fn each_tuple<F: FnMut(&[usize])>(len: usize, base: usize, mut f: F) {
    if base == 0 && len > 0 {
        return;
    }
    let mut t = vec![0usize; len];
    loop {
        f(&t);
        if len == 0 || !next_tuple(&mut t, base) {
            break;
        }
    }
}

/// The ten counts: pairs_total, law, law_noninjective, law_refusing, law_nonrefusing, injective_u,
/// obs_total, obs_preserved, persists, cleared.
pub fn census(a: usize, b: usize, o: usize) -> [u64; 10] {
    let (mut pairs, mut law, mut law_noninj, mut law_ref, mut injective) = (0u64, 0u64, 0u64, 0u64, 0u64);
    let (mut obs_total, mut obs_pres, mut persists, mut cleared) = (0u64, 0u64, 0u64, 0u64);
    each_tuple(a, b, |u| {
        let mut seen = vec![false; b];
        let mut is_inj = true;
        for &y in u {
            if seen[y] {
                is_inj = false;
            }
            seen[y] = true;
        }
        if is_inj {
            injective += 1;
        }
        each_tuple(b, a + 1, |r| {
            pairs += 1;
            if !(0..a).all(|x| r[u[x]] == x) {
                return;
            }
            law += 1;
            if !is_inj {
                law_noninj += 1;
            }
            if (0..b).all(|y| seen[y] || r[y] == a) {
                law_ref += 1;
            }
            each_tuple(a, o, |q| {
                each_tuple(b, o, |qq| {
                    obs_total += 1;
                    if (0..a).all(|x| qq[u[x]] == q[x]) {
                        obs_pres += 1;
                    }
                });
            });
            each_tuple(a, 2, |oa| {
                each_tuple(b, 2, |ob| {
                    let hit = (0..a).any(|x| oa[x] == 1 && ob[u[x]] == 1);
                    if hit {
                        persists += 1;
                    }
                    if !hit && oa.iter().any(|&v| v == 1) {
                        cleared += 1;
                    }
                });
            });
        });
    });
    [pairs, law, law_noninj, law_ref, law - law_ref, injective, obs_total, obs_pres, persists, cleared]
}

/// Wire line for one case, identical to the Python `wire_lines` format.
pub fn line(a: usize, b: usize, o: usize) -> String {
    let c = census(a, b, o);
    let mut parts = vec!["lift".to_string(), a.to_string(), b.to_string(), o.to_string()];
    parts.extend(c.iter().map(|x| x.to_string()));
    parts.join("\t")
}

/// Replay one tab-separated public-input line `lift\ta\tb\to` (sizes are bounded to keep the census finite and fast).
pub fn replay(input: &str) -> Option<String> {
    let mut parts = input.split('\t');
    if parts.next()? != "lift" {
        return None;
    }
    let a: usize = parts.next()?.parse().ok()?;
    let b: usize = parts.next()?.parse().ok()?;
    let o: usize = parts.next()?.parse().ok()?;
    if a > 4 || b > 5 || o > 3 {
        return None;
    }
    Some(line(a, b, o))
}

#[cfg(test)]
mod tests {
    use super::*;

    fn falling(b: u64, a: u64) -> u64 {
        if a > b {
            0
        } else {
            (0..a).map(|k| b - k).product()
        }
    }

    #[test]
    fn pfp_old_image_injective_law_forces_injective_and_counts_match_closed_form() {
        for a in 0..=3usize {
            for b in 0..=4usize {
                let c = census(a, b, 2);
                assert_eq!(c[2], 0, "non-injective law pair at ({}, {})", a, b);
                let inj = falling(b as u64, a as u64);
                let law = if a <= b { inj * (a as u64 + 1).pow((b - a) as u32) } else { 0 };
                assert_eq!(c[1], law);
                assert_eq!(c[5], inj);
                assert_eq!(c[3], inj);
            }
        }
    }

    #[test]
    fn pfp_old_image_injective_off_image_rejection_is_not_implied() {
        assert_eq!(census(2, 3, 2)[4], 12);
        assert_eq!(census(3, 4, 2)[4], 72);
        assert_eq!(census(2, 2, 2)[4], 0);
    }

    #[test]
    fn pfp_old_image_injective_observations_and_obstructions_unconstrained() {
        let c = census(2, 2, 2);
        assert_eq!((c[6], c[7]), (32, 8));
        assert_eq!((c[8], c[9]), (14, 10));
    }

    #[test]
    fn pfp_old_image_injective_degenerate_cases_and_replay() {
        assert_eq!(census(3, 2, 2)[1], 0);
        let c = census(0, 3, 2);
        assert_eq!((c[1], c[3], c[5], c[8], c[9]), (1, 1, 1, 0, 0));
        assert_eq!(replay("lift\t2\t3\t2").unwrap(), "lift\t2\t3\t2\t243\t18\t0\t6\t12\t6\t576\t144\t252\t180");
        assert!(replay("lift\t9\t1\t1").is_none());
        assert!(replay("other\t1\t1\t1").is_none());
    }
}
