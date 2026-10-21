//! Realification R(A) = [[P, -Q], [Q, P]] of exact Gaussian-rational matrices and the declared complex structure J.
//!
//! Exact i128 replay of `code/python/src/qm/pfp_realification_j.py` for PFP batch 01, node L1-WDP-REALIFICATION-J.
//! Record kinds `prod`, `img`, `psd`, `jstruct`, `jcensus`. No selection of J, no state/positivity/instrument claim.
//! AuthorityEffect: None.
use std::cmp::Ordering;

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
struct Rat {
    n: i128,
    d: i128,
}

fn gcd(a: i128, b: i128) -> i128 {
    let (mut a, mut b) = (a.abs(), b.abs());
    while b != 0 {
        let t = a % b;
        a = b;
        b = t;
    }
    a
}

impl Rat {
    fn new(n: i128, d: i128) -> Option<Rat> {
        if d == 0 {
            return None;
        }
        let g = gcd(n, d).max(1);
        let s = if d < 0 { -1 } else { 1 };
        Some(Rat { n: s * n / g, d: s * d / g })
    }
    fn int(n: i128) -> Rat {
        Rat { n, d: 1 }
    }
    fn zero() -> Rat {
        Rat::int(0)
    }
    fn add(self, o: Rat) -> Rat {
        Rat::new(self.n * o.d + o.n * self.d, self.d * o.d).unwrap()
    }
    fn neg(self) -> Rat {
        Rat { n: -self.n, d: self.d }
    }
    fn sub(self, o: Rat) -> Rat {
        self.add(o.neg())
    }
    fn mul(self, o: Rat) -> Rat {
        Rat::new(self.n * o.n, self.d * o.d).unwrap()
    }
    fn parse(s: &str) -> Option<Rat> {
        match s.split_once('/') {
            Some((a, b)) => Rat::new(a.parse().ok()?, b.parse().ok()?),
            None => Some(Rat::int(s.parse().ok()?)),
        }
    }
    fn text(self) -> String {
        if self.d == 1 {
            format!("{}", self.n)
        } else {
            format!("{}/{}", self.n, self.d)
        }
    }
    fn div(self, o: Rat) -> Rat {
        Rat::new(self.n * o.d, self.d * o.n).unwrap()
    }
    fn cmp_zero(self) -> Ordering {
        self.n.cmp(&0)
    }
}

type Mat = Vec<Vec<Rat>>;
type Cx = (Rat, Rat);
type CMat = Vec<Vec<Cx>>;

fn matmul(x: &Mat, y: &Mat) -> Mat {
    let (r, c, k) = (x.len(), y[0].len(), y.len());
    let mut out = vec![vec![Rat::zero(); c]; r];
    for i in 0..r {
        for j in 0..c {
            let mut acc = Rat::zero();
            for t in 0..k {
                acc = acc.add(x[i][t].mul(y[t][j]));
            }
            out[i][j] = acc;
        }
    }
    out
}

fn transpose(x: &Mat) -> Mat {
    (0..x[0].len()).map(|j| (0..x.len()).map(|i| x[i][j]).collect()).collect()
}

fn neg_mat(x: &Mat) -> Mat {
    x.iter().map(|r| r.iter().map(|v| v.neg()).collect()).collect()
}

fn jmat(m: usize) -> Mat {
    let mut j = vec![vec![Rat::zero(); 2 * m]; 2 * m];
    for i in 0..m {
        j[i][m + i] = Rat::int(-1);
        j[m + i][i] = Rat::int(1);
    }
    j
}

fn cmatmul(a: &CMat, b: &CMat) -> CMat {
    let (m, n, k) = (a.len(), b.len(), b[0].len());
    let mut out = vec![vec![(Rat::zero(), Rat::zero()); k]; m];
    for i in 0..m {
        for j in 0..k {
            let (mut re, mut im) = (Rat::zero(), Rat::zero());
            for t in 0..n {
                re = re.add(a[i][t].0.mul(b[t][j].0)).sub(a[i][t].1.mul(b[t][j].1));
                im = im.add(a[i][t].0.mul(b[t][j].1)).add(a[i][t].1.mul(b[t][j].0));
            }
            out[i][j] = (re, im);
        }
    }
    out
}

fn realify(a: &CMat) -> Mat {
    let (m, n) = (a.len(), a[0].len());
    let mut r = vec![vec![Rat::zero(); 2 * n]; 2 * m];
    for i in 0..m {
        for j in 0..n {
            let (p, q) = a[i][j];
            r[i][j] = p;
            r[i][n + j] = q.neg();
            r[m + i][j] = q;
            r[m + i][n + j] = p;
        }
    }
    r
}

fn star(a: &CMat) -> CMat {
    let (m, n) = (a.len(), a[0].len());
    (0..n).map(|j| (0..m).map(|i| (a[i][j].0, a[i][j].1.neg())).collect()).collect()
}

fn imul(a: &CMat) -> CMat {
    a.iter().map(|row| row.iter().map(|z| (z.1.neg(), z.0)).collect()).collect()
}

fn recover(mm: &Mat) -> CMat {
    let (m, n) = (mm.len() / 2, mm[0].len() / 2);
    (0..m).map(|i| (0..n).map(|j| (mm[i][j], mm[i][n + j].neg())).collect()).collect()
}

/// Interleaved coordinate order (re_1, im_1, re_2, ...): R'[2i+a][2j+b] = R[i + a m][j + b n].
fn interleave(r: &Mat, m: usize, n: usize) -> Mat {
    let mut out = vec![vec![Rat::zero(); 2 * n]; 2 * m];
    for i in 0..m {
        for j in 0..n {
            for a in 0..2 {
                for b in 0..2 {
                    out[2 * i + a][2 * j + b] = r[i + a * m][j + b * n];
                }
            }
        }
    }
    out
}

fn cx_mul(u: Cx, v: Cx) -> Cx {
    (u.0.mul(v.0).sub(u.1.mul(v.1)), u.0.mul(v.1).add(u.1.mul(v.0)))
}

/// Positive semidefiniteness of a Hermitian matrix by exact symmetric elimination (LDL*).
fn hermitian_psd(a: &CMat) -> bool {
    let mut a = a.clone();
    let n = a.len();
    let zero = (Rat::zero(), Rat::zero());
    for k in 0..n {
        let pivot = a[k][k].0;
        if pivot.cmp_zero() == Ordering::Less {
            return false;
        }
        if pivot.cmp_zero() == Ordering::Equal {
            if (k..n).any(|j| a[k][j] != zero) {
                return false;
            }
            continue;
        }
        for i in (k + 1)..n {
            for j in (k + 1)..n {
                let num = cx_mul(a[i][k], a[k][j]);
                a[i][j] = (a[i][j].0.sub(num.0.div(pivot)), a[i][j].1.sub(num.1.div(pivot)));
            }
        }
    }
    true
}

fn line_psd(n: usize, atok: &str) -> Option<String> {
    if !(1..=4).contains(&n) {
        return None;
    }
    let a = gparse(atok, n, n)?;
    if star(&a) != a {
        return Some(format!("psd\t{}\t0\t-\t-\t-", n));
    }
    let cp = hermitian_psd(&a);
    let real: CMat = realify(&a).iter().map(|row| row.iter().map(|x| (*x, Rat::zero())).collect()).collect();
    let rp = hermitian_psd(&real);
    Some(format!("psd\t{}\t1\t{}\t{}\t{}", n, bit(cp), bit(rp), bit(cp == rp)))
}

fn bit(b: bool) -> &'static str {
    if b {
        "1"
    } else {
        "0"
    }
}

fn gtext(z: Cx) -> String {
    format!("{}:{}", z.0.text(), z.1.text())
}

fn gparse(tokens: &str, rows: usize, cols: usize) -> Option<CMat> {
    let toks: Vec<&str> = tokens.split(';').collect();
    if toks.len() != rows * cols {
        return None;
    }
    let mut vals = Vec::new();
    for t in toks {
        let (a, b) = t.split_once(':')?;
        vals.push((Rat::parse(a)?, Rat::parse(b)?));
    }
    Some(vals.chunks(cols).map(|c| c.to_vec()).collect())
}

fn trace(x: &Mat) -> Rat {
    (0..x.len()).fold(Rat::zero(), |a, i| a.add(x[i][i]))
}

fn line_prod(m: usize, n: usize, k: usize, atok: &str, btok: &str) -> Option<String> {
    if m == 0 || n == 0 || k == 0 {
        return None;
    }
    let a = gparse(atok, m, n)?;
    let b = gparse(btok, n, k)?;
    let ab = cmatmul(&a, &b);
    let (ra, rb, rab) = (realify(&a), realify(&b), realify(&ab));
    let mult = matmul(&ra, &rb) == rab;
    let inter = matmul(&jmat(m), &ra) == matmul(&ra, &jmat(n));
    let im_ok = realify(&imul(&a)) == matmul(&jmat(m), &ra);
    let star_ok = realify(&star(&a)) == transpose(&ra);
    let rt = recover(&ra) == a;
    let flat: Vec<String> = rab.iter().flat_map(|r| r.iter().map(|v| v.text())).collect();
    let rastar: Vec<String> = realify(&star(&a)).iter().flat_map(|r| r.iter().map(|v| v.text())).collect();
    let ras = interleave(&ra, m, n);
    let ras_flat: Vec<String> = ras.iter().flat_map(|r| r.iter().map(|v| v.text())).collect();
    let ras_comm = matmul(&jmat(m), &ras) == matmul(&ras, &jmat(n));
    let tail = if m == n {
        let trc = (
            (0..n).fold(Rat::zero(), |acc, i| acc.add(a[i][i].0)),
            (0..n).fold(Rat::zero(), |acc, i| acc.add(a[i][i].1)),
        );
        let trr = trace(&ra);
        let twice = Rat::int(2).mul(trc.0);
        [
            bit(star(&a) == a).to_string(),
            bit(transpose(&ra) == ra).to_string(),
            trr.text(),
            gtext(trc),
            bit(trr == twice).to_string(),
            bit(trr == twice && trc.1.cmp_zero() == Ordering::Equal).to_string(),
        ]
    } else {
        ["-".to_string(), "-".to_string(), "-".to_string(), "-".to_string(), "-".to_string(), "-".to_string()]
    };
    Some(format!(
        "prod\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
        m,
        n,
        k,
        flat.join(","),
        rastar.join(","),
        ras_flat.join(","),
        bit(ras_comm),
        bit(mult),
        bit(inter),
        bit(im_ok),
        bit(star_ok),
        bit(rt),
        tail.join("\t")
    ))
}

fn line_img(rows: usize, cols: usize, toks: &str) -> Option<String> {
    let parts: Vec<&str> = toks.split(';').collect();
    if rows == 0 || cols == 0 || parts.len() != rows * cols {
        return None;
    }
    let mut vals = Vec::new();
    for t in parts {
        vals.push(Rat::parse(t)?);
    }
    let mm: Mat = vals.chunks(cols).map(|c| c.to_vec()).collect();
    if rows % 2 == 1 || cols % 2 == 1 {
        return Some(format!("img\t{}\t{}\todd_dim\t-\t-\t-\t-\t-", rows, cols));
    }
    let (m, n) = (rows / 2, cols / 2);
    let jm = matmul(&jmat(m), &mm);
    let mj = matmul(&mm, &jmat(n));
    let commutes = jm == mj;
    let anti = jm == neg_mat(&mj);
    let sym = if rows == cols { bit(transpose(&mm) == mm).to_string() } else { "-".to_string() };
    let (herm, rec) = if commutes {
        let a = recover(&mm);
        let h = if m == n { bit(star(&a) == a).to_string() } else { "-".to_string() };
        let r: Vec<String> = a.iter().flat_map(|row| row.iter().map(|z| gtext(*z))).collect();
        (h, r.join(";"))
    } else {
        ("-".to_string(), "-".to_string())
    };
    Some(format!(
        "img\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
        rows,
        cols,
        if commutes { "ok" } else { "noncommuting" },
        bit(commutes),
        bit(anti),
        sym,
        herm,
        rec
    ))
}

type M2 = (i64, i64, i64, i64);

fn mul2(x: M2, y: M2) -> M2 {
    (x.0 * y.0 + x.1 * y.2, x.0 * y.1 + x.1 * y.3, x.2 * y.0 + x.3 * y.2, x.2 * y.1 + x.3 * y.3)
}

const J2: M2 = (0, -1, 1, 0);
const MINUS_J2: M2 = (0, 1, -1, 0);

fn line_jstruct(a: i64, b: i64, c: i64, d: i64) -> String {
    let x = (a, b, c, d);
    format!(
        "jstruct\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
        a,
        b,
        c,
        d,
        bit(mul2(x, x) == (-1, 0, 0, -1)),
        bit(x == J2 || x == MINUS_J2),
        bit(mul2(x, J2) == mul2(J2, x))
    )
}

/// Integer 2x2 square roots of -I with entries in [-bound, bound] via the trace-zero parametrization d = -a, bc = -(1 + a^2).
fn census(bound: i64) -> Vec<M2> {
    let mut found = Vec::new();
    for a in -bound..=bound {
        let big_n = 1 + a * a;
        for b in -bound..=bound {
            if b != 0 && big_n % b == 0 {
                let c = -big_n / b;
                if c.abs() <= bound {
                    found.push((a, b, c, -a));
                }
            }
        }
    }
    found
}

fn line_jcensus(bound: i64) -> Option<String> {
    if !(0..=40).contains(&bound) {
        return None;
    }
    let f = census(bound);
    let comm = f.iter().filter(|x| mul2(**x, J2) == mul2(J2, **x)).count();
    let pm = f.iter().filter(|x| **x == J2 || **x == MINUS_J2).count();
    Some(format!("jcensus\t{}\t{}\t{}\t{}", bound, f.len(), comm, pm))
}

/// Replay one tab-separated public-input line.
pub fn replay(input: &str) -> Option<String> {
    let p: Vec<&str> = input.split('\t').collect();
    match *p.first()? {
        "prod" if p.len() == 6 => line_prod(p[1].parse().ok()?, p[2].parse().ok()?, p[3].parse().ok()?, p[4], p[5]),
        "img" if p.len() == 4 => line_img(p[1].parse().ok()?, p[2].parse().ok()?, p[3]),
        "psd" if p.len() == 3 => line_psd(p[1].parse().ok()?, p[2]),
        "jstruct" if p.len() == 5 => Some(line_jstruct(p[1].parse().ok()?, p[2].parse().ok()?, p[3].parse().ok()?, p[4].parse().ok()?)),
        "jcensus" if p.len() == 2 => line_jcensus(p[1].parse().ok()?),
        _ => None,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn pfp_realification_j_trace_is_twice_the_real_part_not_the_complex_trace() {
        let l = replay("prod\t1\t1\t1\t1:1\t2:-3").unwrap();
        assert_eq!(l, "prod\t1\t1\t1\t5,1,-1,5\t1,1,-1,1\t1,-1,1,1\t1\t1\t1\t1\t1\t1\t0\t0\t2\t1:1\t1\t0");
        let l2 = replay("prod\t2\t2\t2\t0:1;0:0;0:0;0:1\t1:2;3:0;0:-1;1:1").unwrap();
        let cols: Vec<&str> = l2.split('\t').collect();
        assert_eq!((cols[15], cols[16], cols[17], cols[18]), ("0", "0:2", "1", "0"));
    }

    #[test]
    fn pfp_realification_j_multiplicative_and_intertwining_on_a_rectangular_case() {
        let l = replay("prod\t2\t3\t1\t1:2;0:1;3:-1;-1:0;2:2;0:0\t1:0;0:1;2:-1").unwrap();
        let cols: Vec<&str> = l.split('\t').collect();
        assert_eq!(&cols[8..13], &["1", "1", "1", "1", "1"]);
        assert_eq!(&cols[13..19], &["-", "-", "-", "-", "-", "-"]);
        assert_eq!(cols[4], "5,3,-3,-2,-3,5,2,-3");
    }

    #[test]
    fn pfp_realification_j_image_decision_refuses_unrestricted_real_matrices() {
        let diag1 = replay("img\t4\t4\t1;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0").unwrap();
        assert_eq!(diag1, "img\t4\t4\tnoncommuting\t0\t0\t1\t-\t-");
        let conj = replay("img\t2\t2\t1;0;0;-1").unwrap();
        assert_eq!(conj, "img\t2\t2\tnoncommuting\t0\t1\t1\t-\t-");
        assert_eq!(replay("img\t3\t3\t1;0;0;0;1;0;0;0;1").unwrap(), "img\t3\t3\todd_dim\t-\t-\t-\t-\t-");
        assert_eq!(replay("img\t2\t2\t2;3;-3;2").unwrap(), "img\t2\t2\tok\t1\t0\t0\t0\t2:-3");
        assert_eq!(replay("img\t2\t4\t1;3;-2;1;2;-1;1;3").unwrap(), "img\t2\t4\tok\t1\t0\t-\t-\t1:2;3:-1");
    }

    #[test]
    fn pfp_realification_j_square_roots_of_minus_one_census_and_only_pm_j_commute() {
        assert_eq!(replay("jcensus\t2").unwrap(), "jcensus\t2\t10\t2\t2");
        assert_eq!(replay("jcensus\t7").unwrap(), "jcensus\t7\t26\t2\t2");
        for bound in 1..9 {
            let brute = (-bound..=bound)
                .flat_map(|a| (-bound..=bound).flat_map(move |b| (-bound..=bound).flat_map(move |c| (-bound..=bound).map(move |d| (a, b, c, d)))))
                .filter(|x| mul2(*x, *x) == (-1, 0, 0, -1))
                .count();
            assert_eq!(census(bound).len(), brute);
        }
        assert_eq!(replay("jstruct\t1\t-1\t2\t-1").unwrap(), "jstruct\t1\t-1\t2\t-1\t1\t0\t0");
        assert_eq!(replay("jstruct\t0\t-1\t1\t0").unwrap(), "jstruct\t0\t-1\t1\t0\t1\t1\t1");
    }

    #[test]
    fn pfp_realification_j_positivity_instances_and_interleaved_ordering() {
        assert_eq!(replay("psd\t2\t2:0;1:-1;1:1;1:0").unwrap(), "psd\t2\t1\t1\t1\t1");
        assert_eq!(replay("psd\t2\t1:0;2:0;2:0;1:0").unwrap(), "psd\t2\t1\t0\t0\t1");
        assert_eq!(replay("psd\t2\t1:0;0:1;0:1;1:0").unwrap(), "psd\t2\t0\t-\t-\t-");
        assert_eq!(replay("psd\t3\t1:0;0:-1;1:0;0:1;1:0;0:1;1:0;0:-1;1:0").unwrap(), "psd\t3\t1\t1\t1\t1");
        assert_eq!(replay("psd\t2\t0:0;1:0;1:0;0:0").unwrap(), "psd\t2\t1\t0\t0\t1");
        let two = replay("prod\t2\t2\t2\t1:1;2:0;0:-1;3:0\t1:0;0:0;0:0;1:0").unwrap();
        let cols: Vec<&str> = two.split('\t').collect();
        assert_eq!(cols[7], "0");
    }

    #[test]
    fn pfp_realification_j_malformed_inputs_are_refused() {
        assert!(replay("prod\t2\t2\t2\t1:0;0:0\t1:0;0:0;0:0;1:0").is_none());
        assert!(replay("img\t2\t2\t1;0;0").is_none());
        assert!(replay("unknown\t1").is_none());
    }
}
