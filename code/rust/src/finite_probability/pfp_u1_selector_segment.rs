//! Torsion of the rational unit circle (unit Gaussian rationals) and what finite phase carriers can select.
//!
//! Exact i128 replay of `code/python/src/qm/pfp_u1_selector_segment.py` for PFP batch 01, node
//! L1-U1-SELECTOR-OTHER-SEGMENT (a pointer node: the selection of C and U(1) from finite carriers is NOT established).
//! Record kinds `half` (the exhaustive cases 2x = k) and `point` (Cayley parameters (m, n)). Orders and p-adic valuations
//! are read from exact Gaussian-integer powers A^k / d^k. No completion, continuity or physical claim.
//! AuthorityEffect: None.

const ORDER_BOUND: usize = 12;
const POWERS: usize = 6;

fn gcd(a: i128, b: i128) -> i128 {
    let (mut a, mut b) = (a.abs(), b.abs());
    while b != 0 {
        let t = a % b;
        a = b;
        b = t;
    }
    a
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
struct Rat {
    n: i128,
    d: i128,
}

impl Rat {
    fn new(n: i128, d: i128) -> Rat {
        let g = gcd(n, d).max(1);
        let s = if d < 0 { -1 } else { 1 };
        Rat { n: s * n / g, d: s * d / g }
    }
    fn text(self) -> String {
        if self.d == 1 {
            format!("{}", self.n)
        } else {
            format!("{}/{}", self.n, self.d)
        }
    }
}

fn isqrt(n: i128) -> i128 {
    let mut r = (n as f64).sqrt() as i128;
    while r * r > n {
        r -= 1;
    }
    while (r + 1) * (r + 1) <= n {
        r += 1;
    }
    r
}

/// z = x + iy on the unit circle as A / d with A a Gaussian integer; returns (d, A^0 .. A^upto).
fn gaussian_powers(x: Rat, y: Rat, upto: usize) -> Option<(i128, Vec<(i128, i128)>)> {
    let d = x.d / gcd(x.d, y.d) * y.d;
    let a = (x.n * (d / x.d), y.n * (d / y.d));
    if a.0 * a.0 + a.1 * a.1 != d * d {
        return None;
    }
    let mut pw = vec![(1i128, 0i128)];
    for _ in 0..upto {
        let (u, v) = *pw.last().unwrap();
        let re = u.checked_mul(a.0)?.checked_sub(v.checked_mul(a.1)?)?;
        let im = u.checked_mul(a.1)?.checked_add(v.checked_mul(a.0)?)?;
        pw.push((re, im));
    }
    Some((d, pw))
}

fn order_of(x: Rat, y: Rat) -> Option<i64> {
    let (d, pw) = gaussian_powers(x, y, ORDER_BOUND)?;
    let mut dn: i128 = 1;
    for n in 1..=ORDER_BOUND {
        dn = dn.checked_mul(d)?;
        if pw[n] == (dn, 0) {
            return Some(n as i64);
        }
    }
    Some(0)
}

fn vp(mut n: i128, p: i128) -> i64 {
    let mut c = 0;
    while n % p == 0 {
        n /= p;
        c += 1;
    }
    c
}

fn smallest_prime_factor(n: i128) -> i128 {
    let mut d = 2;
    while d * d <= n {
        if n % d == 0 {
            return d;
        }
        d += 1;
    }
    n
}

fn line_half(k: i64) -> Option<String> {
    if !(-2..=2).contains(&k) {
        return None;
    }
    let x = Rat::new(k as i128, 2);
    let four_minus = 4 - (k * k) as i128; // y^2 = (4 - k^2) / 4
    let y2 = Rat::new(four_minus, 4);
    let s = isqrt(four_minus);
    if s * s != four_minus {
        return Some(format!("half\t{}\t{}\t{}\t-\t-\trefused_irrational_y", k, x.text(), y2.text()));
    }
    let y = Rat::new(s, 2);
    let mut ys = vec![Rat::new(-s, 2)];
    if s != 0 {
        ys.push(y);
    }
    let texts: Vec<String> = ys.iter().map(|v| v.text()).collect();
    let mut orders = Vec::new();
    for v in &ys {
        orders.push(order_of(x, *v)?.to_string());
    }
    Some(format!("half\t{}\t{}\t{}\t{}\t{}\tunit_points", k, x.text(), y2.text(), texts.join(","), orders.join(",")))
}

fn line_point(m: i64, n: i64) -> Option<String> {
    if (m, n) == (0, 0) || m.abs() > 50 || n.abs() > 50 {
        return None;
    }
    let (m, n) = (m as i128, n as i128);
    let c = n * n + m * m;
    let x = Rat::new(n * n - m * m, c);
    let y = Rat::new(2 * m * n, c);
    let twice = Rat::new(2 * x.n, x.d);
    let integral = twice.d == 1;
    let order = order_of(x, y)?;
    let (p, vals) = if integral {
        (0i128, "-".to_string())
    } else {
        let p = smallest_prime_factor(twice.d);
        let (d, pw) = gaussian_powers(x, y, POWERS)?;
        let mut v = Vec::new();
        for k in 1..=POWERS {
            let re = 2 * pw[k].0;
            if re == 0 {
                return None;
            }
            v.push((vp(re, p) - (k as i64) * vp(d, p)).to_string());
        }
        (p, v.join(","))
    };
    Some(format!(
        "point\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
        m,
        n,
        x.text(),
        y.text(),
        integral as i32,
        p,
        vals,
        order,
        matches!(order, 1 | 2 | 4) as i32
    ))
}

fn line_census(bound: i64) -> Option<String> {
    if !(1..=12).contains(&bound) {
        return None;
    }
    let mut pts = std::collections::BTreeSet::new();
    for m in -bound..=bound {
        for n in -bound..=bound {
            if (m, n) == (0, 0) {
                continue;
            }
            let (m, n) = (m as i128, n as i128);
            let c = n * n + m * m;
            let (x, y) = (Rat::new(n * n - m * m, c), Rat::new(2 * m * n, c));
            pts.insert((x.n, x.d, y.n, y.d));
        }
    }
    let (mut mu4, mut other, mut nonintegral) = (0usize, 0usize, true);
    for &(xn, xd, yn, yd) in &pts {
        let order = order_of(Rat { n: xn, d: xd }, Rat { n: yn, d: yd })?;
        if matches!(order, 1 | 2 | 4) {
            mu4 += 1;
        } else {
            other += 1;
            if Rat::new(2 * xn, xd).d == 1 {
                nonintegral = false;
            }
        }
    }
    Some(format!(
        "census\t{}\t{}\t{}\t{}\t{}\t{}",
        bound,
        pts.len(),
        mu4,
        other,
        pts.contains(&(-1, 1, 0, 1)) as i32,
        nonintegral as i32
    ))
}

fn line_ffcircle(p: i64) -> Option<String> {
    if !(2..=100).contains(&p) || (2..p).any(|d| p % d == 0) {
        return None;
    }
    let mut count = 0i64;
    let mut best = 0i64;
    for x in 0..p {
        for y in 0..p {
            if (x * x + y * y) % p == 1 % p {
                count += 1;
                let (mut a, mut b, mut k) = (x, y, 1i64);
                while (a, b) != (1 % p, 0) {
                    let na = (a * x - b * y).rem_euclid(p);
                    let nb = (a * y + b * x).rem_euclid(p);
                    a = na;
                    b = nb;
                    k += 1;
                }
                best = best.max(k);
            }
        }
    }
    let beyond = (1..=count).any(|d| count % d == 0 && !matches!(d, 1 | 2 | 4));
    Some(format!("ffcircle\t{}\t{}\t{}\t{}\t{}\t{}", p, count, best, (best == count) as i32, (count % 4 == 0) as i32, beyond as i32))
}

/// Replay one tab-separated public-input line `half\tk`, `point\tm\tn`, `census\tB` or `ffcircle\tp`.
pub fn replay(input: &str) -> Option<String> {
    let p: Vec<&str> = input.split('\t').collect();
    match *p.first()? {
        "half" if p.len() == 2 => line_half(p[1].parse().ok()?),
        "point" if p.len() == 3 => line_point(p[1].parse().ok()?, p[2].parse().ok()?),
        "census" if p.len() == 2 => line_census(p[1].parse().ok()?),
        "ffcircle" if p.len() == 2 => line_ffcircle(p[1].parse().ok()?),
        _ => None,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn pfp_u1_selector_segment_half_integer_x_refuses_the_sixth_root() {
        assert_eq!(replay("half\t1").unwrap(), "half\t1\t1/2\t3/4\t-\t-\trefused_irrational_y");
        assert_eq!(replay("half\t-1").unwrap(), "half\t-1\t-1/2\t3/4\t-\t-\trefused_irrational_y");
        assert_eq!(replay("half\t0").unwrap(), "half\t0\t0\t1\t-1,1\t4,4\tunit_points");
        assert_eq!(replay("half\t2").unwrap(), "half\t2\t1\t0\t0\t1\tunit_points");
        assert_eq!(replay("half\t-2").unwrap(), "half\t-2\t-1\t0\t0\t2\tunit_points");
    }

    #[test]
    fn pfp_u1_selector_segment_pythagorean_point_has_infinite_order_and_the_valuation_law() {
        assert_eq!(replay("point\t1\t2").unwrap(), "point\t1\t2\t3/5\t4/5\t0\t5\t-1,-2,-3,-4,-5,-6\t0\t0");
        assert_eq!(replay("point\t3\t4").unwrap(), "point\t3\t4\t7/25\t24/25\t0\t5\t-2,-4,-6,-8,-10,-12\t0\t0");
        assert_eq!(replay("point\t5\t12").unwrap(), "point\t5\t12\t119/169\t120/169\t0\t13\t-2,-4,-6,-8,-10,-12\t0\t0");
    }

    #[test]
    fn pfp_u1_selector_segment_unit_points_are_the_only_torsion_among_cayley_points() {
        let mut torsion = 0;
        for m in -9i64..=9 {
            for n in -9i64..=9 {
                if (m, n) == (0, 0) {
                    continue;
                }
                let l = replay(&format!("point\t{}\t{}", m, n)).unwrap();
                let cols: Vec<&str> = l.split('\t').collect();
                let order: i64 = cols[8].parse().unwrap();
                if cols[5] == "1" {
                    assert!(matches!(order, 1 | 2 | 4), "{}", l);
                    torsion += 1;
                } else {
                    assert_eq!(order, 0, "{}", l);
                }
            }
        }
        assert!(torsion > 0);
    }

    #[test]
    fn pfp_u1_selector_segment_census_and_finite_field_circles() {
        assert_eq!(replay("census	3").unwrap(), "census	3	16	4	12	1	1");
        assert_eq!(replay("census	6").unwrap(), "census	6	48	4	44	1	1");
        assert_eq!(replay("ffcircle	2").unwrap(), "ffcircle	2	2	2	1	0	0");
        assert_eq!(replay("ffcircle	3").unwrap(), "ffcircle	3	4	4	1	1	0");
        assert_eq!(replay("ffcircle	7").unwrap(), "ffcircle	7	8	8	1	1	1");
        assert_eq!(replay("ffcircle	13").unwrap(), "ffcircle	13	12	12	1	1	1");
        assert!(replay("ffcircle	9").is_none());
    }

    #[test]
    fn pfp_u1_selector_segment_mu4_points_and_malformed_inputs() {
        assert_eq!(replay("point\t0\t1").unwrap(), "point\t0\t1\t1\t0\t1\t0\t-\t1\t1");
        assert_eq!(replay("point\t1\t0").unwrap(), "point\t1\t0\t-1\t0\t1\t0\t-\t2\t1");
        assert_eq!(replay("point\t1\t1").unwrap(), "point\t1\t1\t0\t1\t1\t0\t-\t4\t1");
        assert!(replay("point\t0\t0").is_none());
        assert!(replay("half\t3").is_none());
        assert!(replay("other\t1").is_none());
    }
}
