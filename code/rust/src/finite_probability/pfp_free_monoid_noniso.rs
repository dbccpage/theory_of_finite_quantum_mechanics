//! Free monoids on alphabets of different sizes: exact counts, exhaustive homomorphism search, set bijection.
//!
//! Exact integer replay of `code/python/src/qm/pfp_free_monoid_noniso.py` for PFP batch 01, node
//! PG-FREE-MONOID-NONISO. For an alphabet pair (n, m) and image-length bound d <= 2: word counts and atoms by
//! brute force, every homomorphism with short generator images classified, the mutually inverse map pairs
//! (equivalences of discrete categories), and the explicit shortlex bijection of the underlying sets.
//! Finite instances; the general theorem is the Lean module FreeMonoidNoniso. AuthorityEffect: None.
use std::collections::{HashMap, HashSet};

const MAX_LEN: usize = 4;
const PREFIX: usize = 30;

type Word = Vec<u8>;

fn tuples(base: usize, len: usize) -> Vec<Vec<usize>> {
    let mut out: Vec<Vec<usize>> = vec![Vec::new()];
    for _ in 0..len {
        let mut next = Vec::with_capacity(out.len() * base);
        for t in &out {
            for x in 0..base {
                let mut u = t.clone();
                u.push(x);
                next.push(u);
            }
        }
        out = next;
    }
    out
}

/// All words of length <= max_len over `base` letters, by length then lexicographically.
fn words_upto(base: usize, max_len: usize) -> Vec<Word> {
    let mut out = Vec::new();
    for k in 0..=max_len {
        for t in tuples(base, k) {
            out.push(t.iter().map(|&x| x as u8).collect());
        }
    }
    out
}

/// Nonempty words of length <= max_len with no split into two nonempty words.
fn atoms(base: usize, max_len: usize) -> u64 {
    let mut found = 0;
    for w in words_upto(base, max_len) {
        if !w.is_empty() && !(1..w.len()).any(|i| !w[..i].is_empty() && !w[i..].is_empty()) {
            found += 1;
        }
    }
    found
}

fn pow(base: u128, k: usize) -> u128 {
    (0..k).fold(1u128, |a, _| a * base)
}

fn rank(word: &[u8], base: usize) -> u128 {
    let k = word.len();
    if base == 1 {
        return k as u128;
    }
    let b = base as u128;
    let mut value = 0u128;
    for &x in word {
        value = value * b + x as u128;
    }
    (pow(b, k) - 1) / (b - 1) + value
}

fn unrank(r: u128, base: usize) -> Word {
    if base == 1 {
        return vec![0u8; r as usize];
    }
    let b = base as u128;
    let mut k = 0usize;
    while (pow(b, k + 1) - 1) / (b - 1) <= r {
        k += 1;
    }
    let mut value = r - (pow(b, k) - 1) / (b - 1);
    let mut digits = Vec::with_capacity(k);
    for _ in 0..k {
        digits.push((value % b) as u8);
        value /= b;
    }
    digits.reverse();
    digits
}

fn hom_image(images: &[Word], word: &[u8]) -> Word {
    let mut out = Vec::new();
    for &x in word {
        out.extend_from_slice(&images[x as usize]);
    }
    out
}

fn set_bijection(n: usize, m: usize) -> (u64, u64) {
    if n == 0 || m == 0 {
        return if n == m { (1, 0) } else { (0, 0) };
    }
    let first_n: Vec<Word> = (0..PREFIX).map(|i| unrank(i as u128, n)).collect();
    let first_m: Vec<Word> = (0..PREFIX).map(|i| unrank(i as u128, m)).collect();
    let phi: HashMap<&Word, &Word> = first_n.iter().zip(first_m.iter()).collect();
    let image_set: HashSet<&Word> = phi.values().copied().collect();
    let target_set: HashSet<&Word> = first_m.iter().collect();
    let bijective = image_set.len() == PREFIX && image_set == target_set;
    let mut violations = 0u64;
    for u in &first_n {
        for v in &first_n {
            let mut uv = u.clone();
            uv.extend_from_slice(v);
            let mut want = phi[u].clone();
            want.extend_from_slice(phi[v]);
            if unrank(rank(&uv, n), m) != want {
                violations += 1;
            }
        }
    }
    (bijective as u64, violations)
}

fn join(values: &[u64]) -> String {
    values.iter().map(|x| x.to_string()).collect::<Vec<_>>().join(":")
}

/// Wire line identical to the Python `wire_lines` format.
pub fn line(n: usize, m: usize, d: usize) -> String {
    let pool = words_upto(m, d);
    let probe = words_upto(n, 2);
    let letters: Vec<Word> = (0..m).map(|b| vec![b as u8]).collect();
    let (mut homs, mut onto, mut inj, mut cand, mut not_perm, mut perms) = (0u64, 0u64, 0u64, 0u64, 0u64, 0u64);
    for choice in tuples(pool.len(), n) {
        let images: Vec<Word> = choice.iter().map(|&i| pool[i].clone()).collect();
        homs += 1;
        let values: Vec<Word> = probe.iter().map(|w| hom_image(&images, w)).collect();
        let value_set: HashSet<&Word> = values.iter().collect();
        let is_onto = letters.iter().all(|l| value_set.contains(l));
        let is_inj = value_set.len() == probe.len();
        onto += is_onto as u64;
        inj += is_inj as u64;
        let distinct: HashSet<&Word> = images.iter().collect();
        let is_perm = images.iter().all(|g| g.len() == 1) && distinct.len() == n && n == m;
        perms += is_perm as u64;
        if is_onto && is_inj {
            cand += 1;
            not_perm += (!is_perm) as u64;
        }
    }
    let mut discrete = 0u64;
    for f in tuples(m, n) {
        for g in tuples(n, m) {
            if (0..n).all(|x| g[f[x]] == x) && (0..m).all(|y| f[g[y]] == y) {
                discrete += 1;
            }
        }
    }
    let (flag, violations) = set_bijection(n, m);
    let words = |base: usize| -> Vec<u64> { (0..=MAX_LEN).map(|k| (base as u64).pow(k as u32)).collect() };
    format!(
        "monoid\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
        n,
        m,
        d,
        join(&words(n)),
        join(&words(m)),
        atoms(n, MAX_LEN),
        atoms(m, MAX_LEN),
        homs,
        onto,
        inj,
        cand,
        not_perm,
        perms,
        discrete,
        flag,
        violations
    )
}

/// Replay one tab-separated public-input line `monoid\tn\tm\td`.
pub fn replay(input: &str) -> Option<String> {
    let mut parts = input.split('\t');
    if parts.next()? != "monoid" {
        return None;
    }
    let n: usize = parts.next()?.parse().ok()?;
    let m: usize = parts.next()?.parse().ok()?;
    let d: usize = parts.next()?.parse().ok()?;
    if parts.next().is_some() || n > 4 || m > 4 || d > 2 {
        return None;
    }
    Some(line(n, m, d))
}

#[cfg(test)]
mod tests {
    use super::*;

    fn factorial(n: u64) -> u64 {
        (1..=n).product()
    }

    fn field(l: &str, i: usize) -> String {
        l.split('\t').nth(i).unwrap().to_string()
    }

    #[test]
    fn pfp_free_monoid_noniso_atoms_are_the_letters() {
        for n in 0..5 {
            assert_eq!(atoms(n, MAX_LEN), n as u64);
        }
    }

    #[test]
    fn pfp_free_monoid_noniso_bijective_candidates_are_letter_permutations() {
        for n in 0..4usize {
            for k in 0..4usize {
                let l = line(n, k, 2);
                let want = if n == k { factorial(n as u64) } else { 0 };
                assert_eq!(field(&l, 11), want.to_string(), "candidates ({}, {})", n, k);
                assert_eq!(field(&l, 12), "0");
                assert_eq!(field(&l, 14), want.to_string(), "discrete ({}, {})", n, k);
            }
        }
    }

    #[test]
    fn pfp_free_monoid_noniso_set_bijection_exists_but_is_not_multiplicative() {
        for (n, k) in [(1usize, 2usize), (2, 3), (3, 2), (2, 4)] {
            let (flag, violations) = set_bijection(n, k);
            assert_eq!(flag, 1);
            assert!(violations > 0);
        }
        for n in 1..5 {
            assert_eq!(set_bijection(n, n), (1, 0));
        }
        assert_eq!(set_bijection(0, 1), (0, 0));
        for base in 1..5 {
            for r in 0..200u128 {
                assert_eq!(rank(&unrank(r, base), base), r);
            }
        }
    }

    #[test]
    fn pfp_free_monoid_noniso_wire_line() {
        assert_eq!(
            replay("monoid\t2\t2\t2").unwrap(),
            "monoid\t2\t2\t2\t1:2:4:8:16\t1:2:4:8:16\t2\t2\t49\t2\t26\t2\t0\t2\t2\t1\t0"
        );
        assert!(replay("report\t2\t2\t2").is_none());
    }
}
