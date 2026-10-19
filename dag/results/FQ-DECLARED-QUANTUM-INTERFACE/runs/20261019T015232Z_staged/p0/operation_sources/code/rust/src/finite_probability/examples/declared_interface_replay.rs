use num_bigint::BigInt;
use num_rational::BigRational as Q;
use std::io::{self, BufRead};
use tfqm_finite_probability::declared_interface::certify;
fn q(s: &str) -> Q {
    let (n, d) = s.split_once('/').unwrap_or((s, "1"));
    Q::new(n.parse::<BigInt>().unwrap(), d.parse::<BigInt>().unwrap())
}
fn main() {
    for line in io::stdin().lock().lines() {
        let line = line.unwrap();
        let f: Vec<_> = line.split('\t').collect();
        let count: usize = f[1].parse().unwrap();
        assert_eq!(f.len(), 2 + 12 + 4 * count);
        let mut at = 2;
        let mut take = || {
            let a = vec![
                vec![q(f[at]), q(f[at + 1])],
                vec![q(f[at + 2]), q(f[at + 3])],
            ];
            at += 4;
            a
        };
        let rho = take();
        let effect = take();
        let u = take();
        let ks = (0..count).map(|_| take()).collect();
        let c = certify(rho, effect, ks, u).unwrap();
        let mut out = vec![f[0].to_string()];
        for a in c.matrices {
            for r in a {
                for x in r {
                    out.push(x.to_string());
                }
            }
        }
        for x in c.scalars {
            out.push(x.to_string());
        }
        out.push("ADMITTED_INTERFACE_EXERCISED_ONLY".to_string());
        println!("{}", out.join("\t"));
    }
}
