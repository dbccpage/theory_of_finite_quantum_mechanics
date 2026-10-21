//! Off-image refusal of the pinned S(n) retraction on explicit universes of presentations.
//!
//! Exact integer replay of `code/python/src/qm/pfp_sn_off_image.py` for PFP batch 01, node PG-SN-OFF-IMAGE-REFUSAL.
//! The model is the pinned SnCarrier with the glyph alphabet abstracted to `g` glyphs; the pinned section and
//! retraction are executed on the whole universe and the refusal claims are counted. A second record kind covers
//! toy sections x -> c x with the refusing retraction built from the total left inverse y -> y / c.
//! Scope: the declared local model only; no cardinality theorem; nested terms as base members are outside the
//! model. AuthorityEffect: None.
use std::collections::BTreeMap;

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

/// Lax retraction: everything the pinned one refuses is accepted as the ground presentation.
fn lax_retr(n: usize, p: &Pres) -> Option<Pres> {
    retr(n, p).or(Some(Pres::Ground))
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

/// Wire line of an `offimage` record.
pub fn offimage_line(g: u8, stages: usize, maxlen: usize, n: usize) -> String {
    let base = bases(g);
    let uni = universe(g, stages, maxlen);
    let image: BTreeMap<Pres, Base> = base.iter().map(|b| (section_lift(n, b), b.clone())).collect();
    let (mut accepted, mut refused, mut iff_viol, mut payload_fail) = (0u64, 0u64, 0u64, 0u64);
    let (mut rt_holds, mut rt_fails, mut long_refused, mut lax_viol) = (0u64, 0u64, 0u64, 0u64);
    for p in &uni {
        let out = retr(n, p);
        let off = !image.contains_key(p);
        if out.is_none() != off {
            iff_viol += 1;
        }
        if lax_retr(n, p).is_none() {
            lax_viol += 1;
        }
        match out {
            Some(q) => {
                accepted += 1;
                match image.get(p) {
                    Some(b) => {
                        if q != to_pres(b) {
                            payload_fail += 1;
                        }
                        if section_lift(n, b) == *p {
                            rt_holds += 1;
                        } else {
                            rt_fails += 1;
                        }
                    }
                    None => {
                        payload_fail += 1;
                        rt_fails += 1;
                    }
                }
            }
            None => {
                refused += 1;
                rt_fails += 1;
                if let Pres::Lift(s, Body::Glyphs(gs)) = p {
                    if *s == n && gs.len() >= 3 {
                        long_refused += 1;
                    }
                }
            }
        }
    }
    let mut mismatch = 0u64;
    for m in 0..stages {
        if m != n {
            for b in &base {
                if retr(n, &section_lift(m, b)).is_none() {
                    mismatch += 1;
                }
            }
        }
    }
    let lax_law_holds = base.iter().filter(|b| lax_retr(n, &section_lift(n, b)) == Some(to_pres(b))).count() as u64;
    let fields = vec![
        "offimage".to_string(),
        g.to_string(),
        stages.to_string(),
        maxlen.to_string(),
        n.to_string(),
        uni.len().to_string(),
        accepted.to_string(),
        refused.to_string(),
        image.len().to_string(),
        (base.len() - image.len()).to_string(),
        iff_viol.to_string(),
        payload_fail.to_string(),
        rt_holds.to_string(),
        rt_fails.to_string(),
        mismatch.to_string(),
        long_refused.to_string(),
        lax_law_holds.to_string(),
        lax_viol.to_string(),
    ];
    fields.join("\t")
}

/// Wire line of a `toy` record: section x -> c x on 0..k, total left inverse y / c, refusal by the round trip.
pub fn toy_line(k: u64, c: u64) -> String {
    let s = |x: u64| c * x;
    let r = |y: u64| -> Option<u64> {
        let x = y / c;
        if s(x) == y {
            Some(x)
        } else {
            None
        }
    };
    let points = c * k;
    let on_image = (0..points).filter(|&y| r(y).is_some()).count();
    let refused = (0..points).filter(|&y| r(y).is_none()).count();
    let law_fail = (0..k).filter(|&x| r(s(x)) != Some(x)).count();
    let sound_fail = (0..points).filter(|&y| matches!(r(y), Some(x) if s(x) != y)).count();
    format!("toy\t{}\t{}\t{}\t{}\t{}\t{}\t{}", k, c, points, on_image, refused, law_fail, sound_fail)
}

/// Replay one tab-separated public-input line (`offimage\tg\tS\tL\tn` or `toy\tk\tc`).
pub fn replay(input: &str) -> Option<String> {
    let mut parts = input.split('\t');
    match parts.next()? {
        "offimage" => {
            let g: u8 = parts.next()?.parse().ok()?;
            let stages: usize = parts.next()?.parse().ok()?;
            let maxlen: usize = parts.next()?.parse().ok()?;
            let n: usize = parts.next()?.parse().ok()?;
            if g > 8 || stages == 0 || stages > 5 || !(2..=4).contains(&maxlen) || n >= stages {
                return None;
            }
            Some(offimage_line(g, stages, maxlen, n))
        }
        "toy" => {
            let k: u64 = parts.next()?.parse().ok()?;
            let c: u64 = parts.next()?.parse().ok()?;
            if k > 8 || c == 0 || c > 6 {
                return None;
            }
            Some(toy_line(k, c))
        }
        _ => None,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn pfp_sn_off_image_refusal_is_exactly_off_image() {
        for g in 0..=3u8 {
            for stages in 1..=3usize {
                let uni = universe(g, stages, 3);
                for n in 0..stages {
                    let image: Vec<Pres> = bases(g).iter().map(|b| section_lift(n, b)).collect();
                    for p in &uni {
                        assert_eq!(retr(n, p).is_none(), !image.contains(p));
                        if let Some(q) = retr(n, p) {
                            let b = bases(g).into_iter().find(|b| section_lift(n, b) == *p).unwrap();
                            assert_eq!(q, to_pres(&b));
                        }
                    }
                }
            }
        }
    }

    #[test]
    fn pfp_sn_off_image_other_stage_lifts_and_long_bodies_are_refused() {
        for g in 0..=3u8 {
            for n in 0..3usize {
                for m in 0..3usize {
                    if m != n {
                        assert!(bases(g).iter().all(|b| retr(n, &section_lift(m, b)).is_none()));
                    }
                }
            }
        }
        assert!(retr(2, &Pres::Lift(2, Body::Glyphs(vec![0, 1, 0]))).is_none());
        assert!(retr(2, &Pres::Retraction(2, Body::Glyphs(vec![]))).is_none());
        assert!(retr(2, &Pres::NonDescent).is_none());
    }

    #[test]
    fn pfp_sn_off_image_lax_retraction_obeys_law_and_refuses_nothing() {
        let l = offimage_line(2, 4, 3, 0);
        let cols: Vec<&str> = l.split('\t').collect();
        assert_eq!(cols[16], cols[8], "lax law holds on every base presentation");
        assert_eq!(cols[17], "0", "lax refuses nothing");
        assert_eq!(cols[8], cols[6], "image size equals accepted");
        assert_eq!(cols[9], "0", "no lift collisions");
        assert_eq!(cols[10], "0", "refusal is exactly off-image");
        assert_eq!(cols[11], "0", "payloads correct");
    }

    #[test]
    fn pfp_sn_off_image_toy_sections_count_divisibility_and_replay_matches_wire() {
        for k in 0..=6u64 {
            for c in 1..=5u64 {
                assert_eq!(toy_line(k, c), format!("toy\t{}\t{}\t{}\t{}\t{}\t0\t0", k, c, c * k, k, (c - 1) * k));
            }
        }
        assert_eq!(replay("toy\t3\t2").unwrap(), "toy\t3\t2\t6\t3\t3\t0\t0");
        assert_eq!(replay("offimage\t0\t2\t2\t0").unwrap(), "offimage\t0\t2\t2\t0\t6\t1\t5\t1\t0\t0\t0\t1\t5\t1\t0\t1\t0");
        assert!(replay("offimage\t1\t2\t2\t2").is_none());
        assert!(replay("toy\t3\t0").is_none());
        assert!(replay("other\t1").is_none());
    }
}
