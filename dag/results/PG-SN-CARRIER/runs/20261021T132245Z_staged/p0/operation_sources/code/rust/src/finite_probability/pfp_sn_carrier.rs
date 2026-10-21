//! The S(n) base presentations, their section lift and retraction, and the declared carrier table.
//!
//! Exact integer replay of `code/python/src/qm/pfp_sn_carrier.py` for PFP batch 01, node PG-SN-CARRIER. The model is
//! the pinned SnCarrier with the glyph alphabet abstracted to `g` glyphs; the pinned functions are executed on an
//! explicit universe of presentations. Scope: the declared local model only; no cardinality theorem is proved here.
//! AuthorityEffect: None.
use std::collections::BTreeSet;

#[derive(Clone, PartialEq, Eq, PartialOrd, Ord, Debug)]
enum Body {
    Arrow(u8, u8),
    Pair(u8, u8),
    Glyphs(Vec<u8>),
}

#[derive(Clone, PartialEq, Eq, PartialOrd, Ord, Debug)]
enum Pres {
    Ground,
    Supplied(u8),
    /// kind 0 = retained pair, 1 = directed cut, 2 = simplex cut
    Rel(u8, u8, u8),
    Lift(usize, Body),
    Retraction(usize, Body),
    NonDescent,
}

#[derive(Clone, PartialEq, Eq, Debug)]
enum Base {
    Ground,
    Supplied(u8),
    Relation(u8, u8, u8),
}

const TABLE: [u64; 7] = [0, 1, 2, 2, 4, 5, 6];

fn carrier_card(n: usize) -> u64 {
    if n < TABLE.len() {
        TABLE[n]
    } else {
        n as u64
    }
}

fn bases(g: u8) -> Vec<Base> {
    let mut out = vec![Base::Ground];
    out.extend((0..g).map(Base::Supplied));
    for kind in 0..3u8 {
        for a in 0..g {
            for b in 0..g {
                out.push(Base::Relation(kind, a, b));
            }
        }
    }
    out
}

fn to_pres(b: &Base) -> Pres {
    match b {
        Base::Ground => Pres::Ground,
        Base::Supplied(m) => Pres::Supplied(*m),
        Base::Relation(k, a, c) => Pres::Rel(*k, *a, *c),
    }
}

fn section_lift(n: usize, b: &Base) -> Pres {
    match b {
        Base::Ground => Pres::Lift(n, Body::Glyphs(vec![])),
        Base::Supplied(m) => Pres::Lift(n, Body::Glyphs(vec![*m])),
        Base::Relation(0, a, c) => Pres::Lift(n, Body::Glyphs(vec![*a, *c])),
        Base::Relation(1, a, c) => Pres::Lift(n, Body::Arrow(*a, *c)),
        Base::Relation(_, a, c) => Pres::Lift(n, Body::Pair(*a, *c)),
    }
}

/// `Some(accepted presentation)` or `None` for NON_DESCENT.
fn retr(n: usize, p: &Pres) -> Option<Pres> {
    match p {
        Pres::Lift(s, body) if *s == n => match body {
            Body::Glyphs(gs) => match gs.len() {
                0 => Some(Pres::Ground),
                1 => Some(Pres::Supplied(gs[0])),
                2 => Some(Pres::Rel(0, gs[0], gs[1])),
                _ => None,
            },
            Body::Arrow(a, c) => Some(Pres::Rel(1, *a, *c)),
            Body::Pair(a, c) => Some(Pres::Rel(2, *a, *c)),
        },
        _ => None,
    }
}

fn unrestricted_lift(n: usize, p: &Pres) -> Pres {
    match p {
        Pres::Ground => Pres::Lift(n, Body::Glyphs(vec![])),
        Pres::Supplied(m) => Pres::Lift(n, Body::Glyphs(vec![*m])),
        Pres::Rel(k, a, c) => section_lift(n, &Base::Relation(*k, *a, *c)),
        _ => Pres::Lift(n, Body::Glyphs(vec![])),
    }
}

fn glyph_words(g: u8, len: usize) -> Vec<Vec<u8>> {
    let mut words: Vec<Vec<u8>> = vec![vec![]];
    for _ in 0..len {
        let mut next = Vec::new();
        for w in &words {
            for x in 0..g {
                let mut v = w.clone();
                v.push(x);
                next.push(v);
            }
        }
        words = next;
    }
    words
}

fn bodies(g: u8, maxlen: usize) -> Vec<Body> {
    let mut out = Vec::new();
    for a in 0..g {
        for b in 0..g {
            out.push(Body::Arrow(a, b));
        }
    }
    for a in 0..g {
        for b in 0..g {
            out.push(Body::Pair(a, b));
        }
    }
    for k in 0..=maxlen {
        out.extend(glyph_words(g, k).into_iter().map(Body::Glyphs));
    }
    out
}

fn universe(g: u8, stages: usize, maxlen: usize) -> Vec<Pres> {
    let mut items = vec![Pres::Ground];
    items.extend((0..g).map(Pres::Supplied));
    for kind in 0..3u8 {
        for a in 0..g {
            for b in 0..g {
                items.push(Pres::Rel(kind, a, b));
            }
        }
    }
    for n in 0..stages {
        for body in bodies(g, maxlen) {
            items.push(Pres::Lift(n, body.clone()));
            items.push(Pres::Retraction(n, body));
        }
    }
    items.push(Pres::NonDescent);
    items
}

fn list<T: ToString>(xs: &[T]) -> String {
    if xs.is_empty() {
        "-".to_string()
    } else {
        xs.iter().map(|x| x.to_string()).collect::<Vec<_>>().join(",")
    }
}

/// Wire line for one case, identical to the Python `wire_lines` format.
pub fn line(g: u8, stages: usize, maxlen: usize) -> String {
    let base = bases(g);
    let gg = g as u64;
    let shapes = [1, gg, gg * gg, gg * gg, gg * gg];
    let (mut checked, mut failures) = (0u64, 0u64);
    let mut sizes = Vec::new();
    for n in 0..stages {
        for b in &base {
            checked += 1;
            if retr(n, &section_lift(n, b)) != Some(to_pres(b)) {
                failures += 1;
            }
        }
        let image: BTreeSet<Pres> = base.iter().map(|b| section_lift(n, b)).collect();
        sizes.push(image.len());
    }
    let uni = universe(g, stages, maxlen);
    let total = base.len() as u64;
    let ground_lift = Pres::Lift(0, Body::Glyphs(vec![]));
    let image0: BTreeSet<Pres> = uni.iter().map(|p| unrestricted_lift(0, p)).collect();
    let fibre = uni.iter().filter(|p| unrestricted_lift(0, p) == ground_lift).count();
    let rt = retr(0, &unrestricted_lift(0, &Pres::NonDescent));
    let stage_shapes = [1, gg, gg * gg, 2 * gg * gg];
    let table_prefix: Vec<u64> = (0..4).map(carrier_card).collect();
    let matches: Vec<u8> = (0..4).map(|i| (carrier_card(i) == stage_shapes[i]) as u8).collect();
    let equal_total: Vec<usize> = (0..7).filter(|&n| carrier_card(n) == total).collect();
    let mut mismatch = 0u64;
    for n in 0..stages {
        for m in 0..stages {
            if m != n {
                mismatch += base.iter().filter(|b| retr(n, &section_lift(m, b)).is_none()).count() as u64;
            }
        }
    }
    let long_refused = uni
        .iter()
        .filter(|p| matches!(p, Pres::Lift(n, Body::Glyphs(gs)) if gs.len() >= 3 && retr(*n, p).is_none()))
        .count();
    let cumulative = [1, 1 + gg, 1 + gg + gg * gg, total];
    let cum_matches: Vec<u8> = (0..4).map(|i| (carrier_card(i) == cumulative[i]) as u8).collect();
    let fields = vec![
        "carrier".to_string(),
        g.to_string(),
        stages.to_string(),
        maxlen.to_string(),
        list(&shapes),
        total.to_string(),
        list(&stage_shapes),
        list(&table_prefix),
        list(&matches),
        list(&equal_total),
        checked.to_string(),
        failures.to_string(),
        list(&sizes),
        uni.len().to_string(),
        (uni.len() as u64 - total).to_string(),
        image0.len().to_string(),
        fibre.to_string(),
        ((fibre <= 1) as u8).to_string(),
        ((rt == Some(Pres::Ground)) as u8).to_string(),
        ((rt == Some(Pres::NonDescent)) as u8).to_string(),
        mismatch.to_string(),
        long_refused.to_string(),
        list(&cumulative),
        list(&cum_matches),
    ];
    fields.join("\t")
}

/// Replay one tab-separated public-input line `carrier\tg\tstages\tmaxlen`.
pub fn replay(input: &str) -> Option<String> {
    let mut parts = input.split('\t');
    if parts.next()? != "carrier" {
        return None;
    }
    let g: u8 = parts.next()?.parse().ok()?;
    let stages: usize = parts.next()?.parse().ok()?;
    let maxlen: usize = parts.next()?.parse().ok()?;
    if g > 8 || stages == 0 || stages > 5 || !(2..=4).contains(&maxlen) {
        return None;
    }
    Some(line(g, stages, maxlen))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn pfp_sn_carrier_old_image_law_and_lift_injective_on_every_stage() {
        for g in 0..=5u8 {
            let base = bases(g);
            assert_eq!(base.len() as u64, 1 + g as u64 + 3 * (g as u64) * (g as u64));
            for n in 0..7usize {
                let mut image = BTreeSet::new();
                for b in &base {
                    assert_eq!(retr(n, &section_lift(n, b)), Some(to_pres(b)));
                    image.insert(section_lift(n, b));
                }
                assert_eq!(image.len(), base.len());
            }
        }
    }

    #[test]
    fn pfp_sn_carrier_declared_table_matches_no_alphabet() {
        for g in 0..60u64 {
            let total = 1 + g + 3 * g * g;
            assert_ne!(carrier_card(0), total);
            assert_ne!(carrier_card(2), total);
            assert_ne!(carrier_card(3), total);
            assert_eq!(carrier_card(1) == total, g == 0);
            assert!(!(g == carrier_card(1) && g * g == carrier_card(2)));
        }
    }

    #[test]
    fn pfp_sn_carrier_unrestricted_lift_collapses_and_refusal_token_changes() {
        let uni = universe(2, 3, 3);
        let nonbase = uni.len() - bases(2).len();
        let ground_lift = Pres::Lift(1, Body::Glyphs(vec![]));
        let fibre = uni.iter().filter(|p| unrestricted_lift(1, p) == ground_lift).count();
        assert_eq!(fibre, nonbase + 1);
        assert_eq!(retr(0, &unrestricted_lift(0, &Pres::NonDescent)), Some(Pres::Ground));
    }

    #[test]
    fn pfp_sn_carrier_stage_guard_and_long_bodies_are_refused() {
        for g in 0..=3u8 {
            for n in 0..4usize {
                for m in 0..4usize {
                    if m != n {
                        assert!(bases(g).iter().all(|b| retr(n, &section_lift(m, b)).is_none()));
                    }
                }
            }
        }
        assert!(retr(1, &Pres::Lift(1, Body::Glyphs(vec![0, 1, 0]))).is_none());
    }

    #[test]
    fn pfp_sn_carrier_replay_matches_wire_lines() {
        let l = replay("carrier\t2\t4\t3").unwrap();
        assert_eq!(l, "carrier\t2\t4\t3\t1,2,4,4,4\t15\t1,2,4,8\t0,1,2,2\t0,0,0,0\t-\t60\t0\t15,15,15,15\t200\t185\t15\t186\t0\t1\t0\t180\t32\t1,3,7,15\t0,0,0,0");
        assert!(replay("carrier\t2\t4\t1").is_none());
        assert!(replay("other\t1\t1\t2").is_none());
    }
}
