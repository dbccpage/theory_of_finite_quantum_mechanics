use num_bigint::BigInt;
use num_rational::BigRational as Q;
use std::io::{self, BufRead};
use tfqm_finite_probability::entropy_exact::certify;
fn q(s: &str) -> Q {
    let (n, d) = s.split_once('/').unwrap_or((s, "1"));
    Q::new(n.parse::<BigInt>().unwrap(), d.parse::<BigInt>().unwrap())
}
fn main() {
    for line in io::stdin().lock().lines() {
        let line = line.unwrap();
        let f: Vec<_> = line.split('\t').collect();
        let terms: usize = f[1].parse().unwrap();
        let c = certify(f[2..].iter().map(|x| q(x)).collect(), terms).unwrap();
        let mut out = vec![f[0].to_string()];
        for x in &c.spectrum {
            out.push(x.to_string());
        }
        out.push(c.denominator.to_string());
        for x in &c.weights {
            out.push(x.to_string());
        }
        out.extend([
            c.terms.to_string(),
            c.purity.to_string(),
            c.deficit.to_string(),
        ]);
        for x in &c.integer_sums {
            out.push(x.to_string());
        }
        for x in &c.powers {
            out.push(x.to_string());
        }
        for b in &c.bounds {
            out.push(b.mode.to_string());
            for x in &b.values {
                out.push(x.to_string());
            }
        }
        out.extend([
            c.lower.to_string(),
            c.upper.to_string(),
            c.width.to_string(),
            c.classification.to_string(),
            "natural".to_string(),
            "EXPLICIT_UNPAID_HYPOTHESIS".to_string(),
        ]);
        println!("{}", out.join("\t"));
    }
}
